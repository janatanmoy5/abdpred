"""Run the original ABDpred models from a PubChem CID or descriptor CSV."""

import argparse
import csv
from functools import lru_cache
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
from operator import gt, le, lt
import os
import pickle
from pathlib import Path
import re
import sys
from threading import Lock
from urllib.error import HTTPError
from urllib.parse import parse_qs
from urllib.request import urlopen
import webbrowser


MODELS = Path(__file__).resolve().parent / "models"
PUBCHEM = "https://pubchem.ncbi.nlm.nih.gov"
XGB_PREDICTION_LOCK = Lock()
FEATURES = {
    "mw": "molecular_weight",
    "xlogp3": "xlogp",
    "hbdc": "h_bond_donor_count",
    "hdac": "h_bond_acceptor_count",
    "rbc": "rotatable_bond_count",
    "exact_mass": "exact_mass",
    "mono_mass": "monoisotopic_mass",
    "tpsa": "tpsa",
    "hac": "heavy_atom_count",
    "charge": "charge",
    "complex": "complexity",
    "isc": "isotope_atom_count",
    "dasc": "defined_atom_stereo_count",
    "uasc": "undefined_atom_stereo_count",
    "dbsc": "defined_bond_stereo_count",
    "ubsc": "undefined_bond_stereo_count",
    "cbu": "covalent_unit_count",
}


def descriptors(row):
    values = dict(row)
    if values.get("xlogp3") is None or str(values["xlogp3"]).strip() == "":
        values["xlogp3"] = 1.125
    result = {}
    for name in FEATURES:
        try:
            value = float(values[name])
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"Missing or invalid descriptor: {name}") from None
        if not math.isfinite(value):
            raise ValueError(f"Non-finite descriptor: {name}")
        result[name] = value
    return result


@lru_cache(maxsize=1)
def load_models():
    import numpy as np

    classical = {}
    for name, filename in (
        ("XGB", "model_XGB_5_fold_pubchem_1_1"),
        ("RF", "model0_RF_5_fold_pubchem_1_1"),
        ("GBC", "model_GBC_5_fold_pubchem_1_1"),
    ):
        with (MODELS / filename).open("rb") as file:
            classical[name] = pickle.load(file)
    with np.load(MODELS / "dnn_weights.npz", allow_pickle=False) as weights:
        dnn = [(weights[f"{i}_kernel"], weights[f"{i}_bias"]) for i in range(1, 4)]
    return classical, dnn


def dnn_probability(matrix, weights):
    import numpy as np
    from scipy.special import expit

    hidden = matrix.astype(np.float32)
    for kernel, bias in weights[:-1]:
        hidden = np.maximum(hidden @ kernel + bias, 0)
    kernel, bias = weights[-1]
    return expit(hidden @ kernel + bias)


def predict(features):
    import numpy as np
    classical, dnn = load_models()
    import xgboost as xgb
    matrix = np.asarray([list(features.values())], dtype=np.float64)
    predictions = {}
    for name, model in classical.items():
        if name == "XGB":
            booster = model.get_booster()
            # The old PHP CSV included spaces in some feature headers.
            data = xgb.DMatrix(matrix, feature_names=booster.feature_names)
            with XGB_PREDICTION_LOCK:
                positive = float(booster.predict(data)[0])
            label = int(positive > 0.5)
        else:
            positive = float(model.predict_proba(matrix)[0, list(model.classes_).index(1)])
            label = int(model.predict(matrix)[0])
        predictions[name] = score(label, positive)
    positive = float(dnn_probability(matrix, dnn)[0, 0])
    predictions["DNN"] = score(int(positive > 0.55), positive)
    mean = sum(result["antibiotic_probability"] for result in predictions.values()) / len(predictions)
    return {"models": predictions, "consensus": score(int(mean > 0.5), mean)}


def score(label, positive):
    return {
        "prediction": "Antibiotic" if label else "Non-antibiotic",
        "antibiotic_probability": positive,
        "non_antibiotic_probability": 1.0 - positive,
    }


@lru_cache(maxsize=1)
def reference_compounds():
    with (MODELS / "reference_compounds.csv").open(newline="", encoding="utf-8") as file:
        return [
            (row["cid"], row["name"], int(row["fingerprint"], 16))
            for row in csv.DictReader(file)
        ]


def similarity_matches(fingerprint):
    if not fingerprint:
        return []
    query = int(fingerprint, 16)
    matches = []
    for cid, name, reference in reference_compounds():
        similarity = bin(query & reference).count("1") / bin(query | reference).count("1")
        matches.append({"cid": cid, "name": name, "similarity": similarity})
    return sorted(matches, key=lambda item: item["similarity"], reverse=True)


RULES = {
    "Lipinski": (("mw", le, 500), ("hbdc", le, 5), ("hdac", le, 10), ("xlogp3", le, 5)),
    "Pfizer 3/75 risk flag": (("xlogp3", gt, 3), ("tpsa", lt, 75)),
    "Veber": (("tpsa", le, 140), ("rbc", le, 10)),
    "Egan": (("tpsa", le, 131.6), ("xlogp3", le, 5.88)),
}
PROPERTY_LABELS = {
    "mw": ("Molecular weight", " g/mol"),
    "hbdc": ("H-bond donors", ""),
    "hdac": ("H-bond acceptors", ""),
    "xlogp3": ("XLogP", ""),
    "tpsa": ("TPSA", " Å²"),
    "rbc": ("Rotatable bonds", ""),
}
COMPARISON_LABELS = {le: "≤", lt: "<", gt: ">"}


def druglikeness(properties):
    return {
        name: all(compare(properties[key], limit) for key, compare, limit in criteria)
        for name, criteria in RULES.items()
    }


def predict_cid(cid):
    if not re.fullmatch(r"[1-9][0-9]{0,11}", cid):
        raise ValueError("Enter a positive numeric PubChem CID.")
    from pubchempy import Compound

    try:
        with urlopen(f"{PUBCHEM}/rest/pug/compound/cid/{cid}/JSON", timeout=20) as response:
            record = json.load(response)["PC_Compounds"][0]
    except HTTPError as exc:
        if exc.code == 404:
            raise ValueError(f"PubChem CID {cid} was not found.") from None
        raise
    compound = Compound(record)
    pubchem_values = {name: getattr(compound, attr) for name, attr in FEATURES.items()}
    features = descriptors(pubchem_values)
    properties = {key: features[key] for key in PROPERTY_LABELS}
    try:
        with urlopen(f"{PUBCHEM}/rest/pug/compound/cid/{cid}/synonyms/JSON", timeout=5) as response:
            entries = json.load(response).get("InformationList", {}).get("Information", [])
        synonyms = entries[0].get("Synonym", []) if entries else []
    except (OSError, ValueError):
        synonyms = []
    return {
        "cid": cid,
        "synonyms": synonyms,
        "pubchem_url": f"{PUBCHEM}/compound/{cid}",
        "structure_url": f"{PUBCHEM}/rest/pug/compound/cid/{cid}/PNG",
        "molecular_formula": compound.molecular_formula,
        "iupac_name": compound.iupac_name,
        "descriptors": features,
        **predict(features),
        "physicochemical_properties": properties,
        "xlogp_imputed": pubchem_values["xlogp3"] is None,
        "druglikeness": druglikeness(properties),
        "similarity_matches": similarity_matches(compound.fingerprint),
    }


def predict_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        columns = {name.strip() for name in reader.fieldnames or []}
        if missing := FEATURES.keys() - columns:
            raise ValueError(f"CSV is missing columns: {', '.join(sorted(missing))}")
        results = []
        for row_number, row in enumerate(reader, start=2):
            try:
                values = descriptors({key.strip(): value for key, value in row.items() if key is not None})
                results.append({"row": row_number, **predict(values)})
            except ValueError as exc:
                raise ValueError(f"CSV row {row_number}: {exc}") from exc
    if not results:
        raise ValueError("The descriptor CSV contains no data rows.")
    return results


def result_html(result):
    cid = result["cid"]
    def prediction_row(name, item):
        return (
            f"<tr><th scope='row'>{name}</th><td>{item['prediction']}</td>"
            f"<td>{item['antibiotic_probability']:.2f}</td>"
            f"<td>{item['non_antibiotic_probability']:.2f}</td></tr>"
        )

    rows = "".join(prediction_row(name, item) for name, item in result["models"].items())
    consensus = prediction_row("Soft vote", result["consensus"])
    checks = []
    verdict = {True: "Followed", False: "Not Followed"}
    properties = result["physicochemical_properties"]
    for name, criteria in RULES.items():
        passed = result["druglikeness"][name]
        observed = []
        thresholds = []
        for key, compare, limit in criteria:
            label, unit = PROPERTY_LABELS[key]
            value = properties[key]
            fallback = " (fallback)" if key == "xlogp3" and result["xlogp_imputed"] else ""
            observed.append(f"{label} {value:g}{unit}{fallback}")
            thresholds.append(f"{label} {COMPARISON_LABELS[compare]} {limit:g}{unit}")
        checks.append(
            f"<tr><th scope='row'>{name}</th><td>{'<br>'.join(observed)}</td>"
            f"<td>{'<br>'.join(escape(text) for text in thresholds)}</td><td>{verdict[passed]}</td></tr>"
        )
    synonyms = "".join(f"<li>{escape(name)}</li>" for name in result["synonyms"][:8])
    synonyms = f"<ul>{synonyms}</ul>" if synonyms else "Unavailable"
    descriptor_rows = "".join(
        f"<tr><th>{key}</th><td>{value:g}</td></tr>"
        for key, value in result["descriptors"].items()
    )
    reference_matches = result["similarity_matches"]
    close_matches = [item for item in reference_matches if item["similarity"] > 0.60]

    reference_annotation = ""
    if cid == "2349":
        reference_annotation = (
            f'<p><strong>PubChem annotation:</strong> '
            f'<a href="{PUBCHEM}/compound/2349">Penicillins</a> are an antibiotic class. '
            'The classifier table shows the model output for CID 2349.</p>'
        )
    stereo_notice = ""
    if result["descriptors"]["uasc"] or result["descriptors"]["ubsc"]:
        candidates = [
            item for item in reference_matches
            if item["similarity"] == 1 and item["cid"] != cid
        ]
        buttons = "".join(
            f'<button name="cid" value="{item["cid"]}">Predict {escape(item["name"])} '
            f'(CID {item["cid"]})</button> ' for item in candidates
        )
        candidate_form = f'<form method="post" action="/">{buttons}</form>' if buttons else ""
        stereo_notice = (
            "<p>This PubChem record contains undefined stereochemistry. ABDpred uses "
            "stereochemistry counts as model inputs. A 2D fingerprint match of 1.000 "
            "can occur for different stereochemical records.</p>" + candidate_form
        )

    def similarity_rows(matches):
        return "".join(
            f'<tr><td>{escape(item["name"])}</td>'
            f'<td><a href="{PUBCHEM}/compound/{item["cid"]}">{item["cid"]}</a></td>'
            f'<td>{item["similarity"]:.3f}</td></tr>'
            for item in matches
        )

    similarity_header = ("<thead><tr><th>Reference compound</th><th>PubChem CID</th>"
                         "<th>Tanimoto score</th></tr></thead>")
    matches = similarity_rows(close_matches) or '<tr><td colspan="3">No matches above 0.60.</td></tr>'
    all_matches = similarity_rows(reference_matches)
    structure = escape(result["structure_url"], quote=True)
    name = escape(result["iupac_name"] or f"CID {cid}")
    formula = escape(result["molecular_formula"] or "")
    score_header = "<th>Prediction</th><th>Positive score</th><th>Negative score</th>"
    return f"""
<section><h2>Input compound details</h2>
<table class="compound"><thead><tr><th>PubChem CID</th><th>Structure</th><th>Synonyms</th></tr></thead>
<tbody><tr><td><a href="{result['pubchem_url']}">{cid}</a><p>{formula}</p></td>
<td><a href="{structure}"><img src="{structure}" alt="Structure for PubChem CID {cid}" width="280" height="280"></a></td>
<td>{synonyms}</td></tr></tbody></table>
<details><summary>IUPAC name and model descriptors</summary><p>{name}</p><table>{descriptor_rows}</table></details>
</section>
<section><h2>Drug-likeness and bioavailability profile</h2>
<p>Screening rules use the numeric model descriptors. ABDpred uses XLogP 1.125 when PubChem has no estimate.
For Pfizer 3/75, “Followed” means the risk flag is triggered.</p>
<table><thead><tr><th>Rule</th><th>Values used</th><th>Criteria</th><th>Result</th></tr></thead>
<tbody>{''.join(checks)}</tbody></table></section>
<section><h2>Predictions by classifier</h2>
{reference_annotation}
{stereo_notice}
<table><thead><tr><th>Classifier</th>{score_header}</tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Consensus prediction</h2>
<table><thead><tr><th>Method</th>{score_header}</tr></thead><tbody>{consensus}</tbody></table></section>
<section><h2>Similar antimicrobial compounds</h2>
<p>Tanimoto scores above 0.60</p>
<table>{similarity_header}<tbody>{matches}</tbody></table>
<details><summary>All {len(reference_matches)} reference entries</summary>
<table>{similarity_header}<tbody>{all_matches}</tbody></table></details></section>
"""


class PredictionPage(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", "3")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return
        if self.path != "/":
            self.send_error(404)
            return
        self.show_page()

    def do_POST(self):
        if self.path != "/":
            self.send_error(404)
            return
        cid = ""
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 1024:
                raise ValueError("Enter a single PubChem CID.")
            fields = parse_qs(self.rfile.read(length).decode("utf-8"))
            cid = fields.get("cid", [""])[0].strip()
            self.show_page(result_html(predict_cid(cid)), cid=cid)
        except (ValueError, OSError) as exc:
            self.show_page(f'<p role="alert">{escape(str(exc))}</p>', 400, cid=cid)
        except Exception:
            import traceback

            traceback.print_exc()
            self.show_page('<p role="alert">Prediction failed. See the terminal for details.</p>', 500)

    def show_page(self, content="", status=200, cid=""):
        page = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ABDpred</title>
<style>
body {{font: 16px system-ui, sans-serif; color:#193536; background:#f4f8f7;
       max-width:55rem; margin:3rem auto; padding:0 1rem}}
section, form, details {{background:white; border:1px solid #c9dcda;
                         border-radius:.75rem; padding:1rem; margin:1rem 0; overflow:auto}}
h1 {{margin-bottom:.2rem}} h2 {{margin-top:0}} a {{color:#0b635b}}
input,button {{font:inherit; padding:.55rem; margin:.3rem 0; border-radius:.35rem}}
input {{border:1px solid #648883; max-width:100%}}
button {{border:1px solid #0b635b; background:#0b635b; color:white; cursor:pointer}}
table {{border-collapse:collapse; width:100%; margin-top:.5rem}}
th,td {{text-align:left; padding:.5rem; border-bottom:1px solid #dce7e6}}
thead {{background:#eaf3f1}}
.compound td {{vertical-align:top; overflow-wrap:anywhere}}
.compound img {{display:block; width:clamp(120px, 28vw, 280px); height:auto}}
.compound ul {{margin:0; padding-left:1.2rem}}
summary {{cursor:pointer}} [role=alert] {{color:#932e25}}
footer {{margin-top:2rem; padding-top:1rem; border-top:1px solid #c9dcda}}
</style>
<main><h1>ABDpred</h1><p>Antibiotic drug prediction from PubChem compound descriptors</p>
<form method="post" action="/"><label for="cid">PubChem CID</label>
<input id="cid" name="cid" inputmode="numeric" pattern="[1-9][0-9]{{0,11}}"
       maxlength="12" placeholder="e.g. 45267103" value="{escape(cid, quote=True)}" required>
<button>Predict</button></form>{content}</main>
<footer aria-labelledby="citation"><h2 id="citation">Cite ABDpred</h2>
<p>Jana T, Sarkar D, Ganguli D, Mukherjee SK, Mandal RS, Das S.
ABDpred: Prediction of active antimicrobial compounds using supervised machine learning techniques.
<em>Indian J Med Res.</em> 2024 Jan 1;159(1):78–90.</p>
<p><a href="https://doi.org/10.4103/ijmr.ijmr_1832_22">DOI 10.4103/ijmr.ijmr_1832_22</a>
· <a href="https://pubmed.ncbi.nlm.nih.gov/38345040/">PubMed PMID 38345040</a></p>
</footer></html>""".encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--cid", nargs="+", help="Predict one or more PubChem CIDs and print JSON.")
    source.add_argument("--csv", type=Path, help="Predict from a descriptor CSV without PubChem.")
    parser.add_argument("--host", choices=("127.0.0.1", "0.0.0.0"),
                        help="Override the default bind address.")
    parser.add_argument("--port", type=int, help="Override PORT or the local default of 8765.")
    parser.add_argument("--no-browser", action="store_true", help="Start the server without opening a tab.")
    args = parser.parse_args()
    try:
        if args.cid is not None:
            results = [predict_cid(cid) for cid in args.cid]
            output = results[0] if len(results) == 1 else results
            print(json.dumps(output, indent=2, allow_nan=False))
        elif args.csv:
            print(json.dumps(predict_csv(args.csv), indent=2, allow_nan=False))
        else:
            on_render = os.environ.get("RENDER") == "true"
            host = args.host or ("0.0.0.0" if on_render else "127.0.0.1")
            port = args.port if args.port is not None else int(
                os.environ.get("PORT", "10000" if on_render else "8765")
            )
            if not 0 <= port <= 65535:
                raise ValueError("Server port must be between 0 and 65535.")
            load_models()
            with ThreadingHTTPServer((host, port), PredictionPage) as server:
                url = f"http://127.0.0.1:{server.server_port}/"
                print(f"ABDpred is running at {url}", flush=True)
                if os.environ.get("CODESPACES") == "true":
                    print("Open ABDpred from the Codespaces Ports panel.", flush=True)
                elif not args.no_browser and not on_render and host == "127.0.0.1":
                    webbrowser.open(url)
                server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except (ValueError, OSError, ImportError) as exc:
        parser.exit(1, f"ABDpred: {exc}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
