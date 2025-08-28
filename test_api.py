"""
Smoke tests for the FastAPI serving layer.

These tests start the FastAPI app in memory using TestClient and
exercise the health check and prediction endpoints.  They assert
that the API responds with the expected status codes and JSON
structure.  When you add a real model and preprocessing, extend
these tests to validate the predictions.
"""

from fastapi.testclient import TestClient

from src.serving.app import app


client = TestClient(app)


def test_health() -> None:
    """Health endpoint should return status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


def test_predict() -> None:
    """Prediction endpoint should return a numeric prediction."""
    payload = {"features": [1.0, 2.0, 3.0]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "prediction" in body
    assert isinstance(body["prediction"], (int, float))