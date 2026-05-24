from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "delivery_records.csv"


def load_delivery_data(csv_path: Path | str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load delivery data from CSV with basic date parsing."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Delivery data not found at {path}")

    df = pd.read_csv(path)
    df["scheduled_delivery_date"] = pd.to_datetime(df["scheduled_delivery_date"], errors="coerce")
    df["actual_delivery_date"] = pd.to_datetime(df["actual_delivery_date"], errors="coerce")
    return df
