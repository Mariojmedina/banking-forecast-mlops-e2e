"""
Minimal FastAPI application exposing a health endpoint and a prediction
endpoint.

This API is designed to be extended.  During the health check it
reports the model version via the ``MODEL_VERSION`` environment
variable.  The prediction endpoint currently sums the input features
as a placeholder.  When you integrate a real model (for example via
MLflow's model registry) you can load it in the startup event and
call it inside ``predict``.
"""

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import os

try:
    import xgboost as xgb  # Optional dependency for real models
except ImportError:
    xgb = None  # type: ignore

app = FastAPI(title="Banking Forecast API")


class PredictRequest(BaseModel):
    features: list[float]


model: Optional[object] = None


def load_model(path: Path) -> Optional[object]:
    """Attempt to load a trained XGBoost model from disk.

    If XGBoost is not installed or the model file is missing, returns
    ``None``.  This allows the API to fall back to a dummy prediction.
    """
    if xgb is None:
        return None
    if not path.exists():
        return None
    m = xgb.XGBRegressor()
    m.load_model(path)
    return m


@app.on_event("startup")
async def startup_event() -> None:
    """Load the model at application startup if present."""
    global model
    model = load_model(Path("models/model.pkl"))


@app.get("/health")
async def health() -> dict[str, str]:
    """Return service health and model version."""
    return {
        "status": "ok",
        "model_version": os.getenv("MODEL_VERSION", "dev"),
    }


@app.post("/predict")
async def predict(req: PredictRequest) -> dict[str, float]:
    """Return a prediction for the provided feature vector.

    If a trained model is loaded, it is used to compute the prediction.
    Otherwise, the prediction is computed as the sum of the input
    features (a simple baseline).
    """
    arr = np.array(req.features).reshape(1, -1)
    if model is not None:
        try:
            # type: ignore[attr-defined]
            pred = float(model.predict(arr)[0])
        except Exception as exc:
            # Fallback to sum if something goes wrong
            pred = float(arr.sum())
    else:
        pred = float(arr.sum())
    return {"prediction": pred}