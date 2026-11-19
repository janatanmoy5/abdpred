FROM python:3.8-slim-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends git libgomp1 \
    && apt-get clean
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY run.py .
COPY models/ models/
ENTRYPOINT ["python", "run.py"]
CMD ["--no-browser", "--host", "0.0.0.0"]
