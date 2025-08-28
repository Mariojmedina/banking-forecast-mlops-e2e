"""
Minimal training script for a gradient boosted tree model.

This script trains an XGBoost regressor on a synthetic dataset and logs
parameters, metrics and the trained model to MLflow.  In a realistic
forecasting pipeline you would replace the ``load_data`` function with
feature ingestion and engineering steps that read data from ``data/processed``.
"""

import mlflow
import mlflow.sklearn
import numpy as np
from pathlib import Path
from xgboost import XGBRegressor


def load_data() -> tuple[np.ndarray, np.ndarray]:
    """Generate a simple synthetic regression dataset.

    Returns
    -------
    X: np.ndarray
        Feature matrix with shape (n_samples, n_features).
    y: np.ndarray
        Target vector with shape (n_samples,).
    """
    # Replace this with real feature loading (e.g. from Parquet)
    rng = np.random.default_rng(seed=42)
    X = rng.random((200, 5))
    # Define a target that is the sum of features plus noise
    y = X.sum(axis=1) + rng.normal(0, 0.1, 200)
    return X, y


def main() -> None:
    """Train an XGBoost regressor and log results to MLflow."""
    X, y = load_data()
    # Define hyperparameters; tune these in your experiments
    params = {"n_estimators": 50, "max_depth": 3, "random_state": 42}
    model = XGBRegressor(**params)
    # Start an MLflow run
    with mlflow.start_run():
        model.fit(X, y)
        # Log parameters
        mlflow.log_params(params)
        # Evaluate on the training set (for demo purposes)
        preds = model.predict(X)
        rmse = float(np.sqrt(((preds - y) ** 2).mean()))
        mlflow.log_metric("rmse_train", rmse)
        # Persist the model in the MLflow run's artifact store
        mlflow.sklearn.log_model(model, "model")
        print({"rmse_train": rmse})


if __name__ == "__main__":
    main()