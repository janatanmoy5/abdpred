# ABDpred

## Live web app

[Open ABDpred on Render](https://abdpred.onrender.com/). Enter PubChem CID
`45267103` (Gramicidin D) and select **Predict** to try the example from the
published paper. The consensus score is approximately 0.78.

[View the complete example output (PDF)](examples/ABDpred.pdf).

ABDpred uses 17 PubChem compound descriptors to classify a compound as
antibiotic or non-antibiotic. The local browser app reports the predictions
from XGBoost, Random Forest, Gradient Boosting and the neural network, along
with a soft-vote consensus, drug-likeness checks and Tanimoto similarities to
the original reference set.

The archived PHP form in `index.php` submitted to `prediction_result1.php`.
That page called the model scripts, drug-likeness checks and similarity search.
`prediction_result.php` was another prediction page. The source folder did
not contain `proces.php`. The Python app uses the original model artifacts
and reference fingerprints copied from that archive.

In the web app, choose **PubChem CID**, **Chemical name or synonym**, or
**SMILES** under **Search by**. For example, enter CID `5904` or the synonym
`benzylpenicillin`. Name and SMILES lookups resolve to PubChem CIDs before
prediction. If PubChem returns multiple records, enter the CID you intend to use.

## Cite ABDpred

Jana T, Sarkar D, Ganguli D, Mukherjee SK, Mandal RS, Das S. ABDpred: Prediction
of active antimicrobial compounds using supervised machine learning techniques.
*Indian J Med Res.* 2024 Jan 1;159(1):78–90.
[DOI 10.4103/ijmr.ijmr_1832_22](https://doi.org/10.4103/ijmr.ijmr_1832_22) ·
[PubMed PMID 38345040](https://pubmed.ncbi.nlm.nih.gov/38345040/).

## Run locally

Use **64-bit x86 CPython 3.8**. The serialized scikit-learn 0.23.2 models require a
compatible runtime. On macOS, XGBoost 1.2.0 also needs an Intel OpenMP library. If using an Intel Conda
environment with `llvm-openmp`, set `DYLD_LIBRARY_PATH="$CONDA_PREFIX/lib"` when
running the launcher.

```sh
python3.8 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

The launcher opens [the local app](http://127.0.0.1:8765/). Enter a PubChem CID
such as `5904` and select **Predict**. CID lookup needs access to PubChem.
Press Ctrl+C in the terminal to stop the app.

On Apple Silicon with Rosetta and Conda, create an Intel environment using:

```sh
CONDA_SUBDIR=osx-64 conda create -n abdpred -c conda-forge python=3.8 pip llvm-openmp
conda activate abdpred
python -m pip install -r requirements.txt
DYLD_LIBRARY_PATH="$CONDA_PREFIX/lib" python run.py
```

## Run with Docker

This installs the x86-64 Linux dependencies in an isolated container.

```sh
docker build --platform linux/amd64 -t abdpred .
docker run --rm --platform linux/amd64 -p 127.0.0.1:8765:8765 abdpred
```

Open [the local app](http://127.0.0.1:8765/) in your browser.

## Run from GitHub Codespaces

After the project files are in a GitHub repository, choose **Code → Codespaces
→ Create codespace**. Wait for the dev container to build, then run
`python run.py` in the Codespaces terminal. Open **ABDpred** from the **Ports**
panel if the browser tab does not open automatically. Enter a PubChem CID
such as `5904` and select **Predict**.

The repository workflow builds the same image and checks model inference and
browser startup on pushes and pull requests. For persistent public hosting,
use a host that can run the Python server. GitHub Pages provides static hosting.

## Deploy from GitHub to Render

Push this project, including the `models/` directory, to GitHub. In Render,
create a **Blueprint** and select the repository. Render reads `render.yaml`
and uses the Dockerfile to install the pinned model dependencies. The server
uses Render's `PORT` and exposes `/healthz` for readiness checks. Open the
service URL in your browser after the deployment succeeds.

BioRender is a scientific illustration tool. Its uploads accept figure images
such as PNG, JPG, and SVG. Run the interactive predictor locally, in
Codespaces, or on Render.

## Get JSON output

```sh
python run.py --cid 5904
python run.py --cid 5904 2244
python run.py --csv models/example.csv
```

The CSV route works offline. It accepts one or more rows with the 17 columns in
`models/example.csv`. Legacy headers with spaces and the optional `Label`
column are accepted. Missing XLogP uses the original model input fallback of
1.125.

The DNN runs the original SavedModel weights using NumPy and SciPy and keeps
its original 0.55 classification cutoff. The TensorFlow artifact is included
for reference. Its antibiotic
probability is the raw sigmoid output. The consensus averages the four
antibiotic probabilities at full precision and predicts antibiotic above
0.5. The Python version corrects the legacy PHP workflow's swapped DNN
probabilities below the cutoff and the reversed upper bounds in its Veber
and Egan checks.
