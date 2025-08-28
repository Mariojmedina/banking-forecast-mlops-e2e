"""
Simple data ingestion script.

In a production system this module would download and transform raw data from
external sources (for example, FRED, energy markets or internal databases).
For this minimal demo it generates a small synthetic dataset and writes it
to a Parquet file in ``data/processed``.  Writing to a Parquet file makes it
easy to demonstrate DVC pipelines and downstream training with Pandas.
"""

import os
from pathlib import Path

import pandas as pd


def run() -> None:
    """Generate a tiny dataset and persist it as a Parquet file.

    The generated dataset contains two feature columns (x1, x2) and a target
    column y which is a simple linear combination of the features.  In a real
    application you would replace this with logic that reads raw files from
    ``data/raw``, performs feature engineering and writes the processed
    features to ``data/processed``.
    """
    # Create a simple DataFrame with dummy values
    df = pd.DataFrame({
        "x1": [1.0, 2.0, 3.0],
        "x2": [4.0, 5.0, 6.0],
    })
    # Target is sum of features plus noise for demonstration
    df["y"] = df["x1"] + df["x2"]
    # Ensure the processed directory exists
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "features.parquet"
    df.to_parquet(out_path, index=False)
    print(f"Wrote features to {out_path}")


if __name__ == "__main__":
    run()