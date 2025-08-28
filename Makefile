# Makefile for common development tasks

.PHONY: setup train serve test lint

setup:
	python -m venv .venv && \
	. .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt -c constraints.txt

train:
    # Run the data and model pipeline via DVC.  This will execute the
    # ingestion and training stages defined in dvc.yaml.  DVC will
    # compute which steps are out‑of‑date based on code and data
    # dependencies and only re‑execute what is necessary.
    dvc repro

serve:
	uvicorn src.serving.app:app --host $${API_HOST:-0.0.0.0} --port $${API_PORT:-8000}

test:
	pytest -q

lint:
	ruff check . && black --check .