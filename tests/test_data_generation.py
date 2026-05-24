from __future__ import annotations

from pathlib import Path

import pandas as pd

from scripts.validate_data import REQUIRED_COLUMNS


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "processed" / "delivery_records.csv"


def test_generated_data_file_exists() -> None:
    assert DATA_FILE.exists()


def test_generated_data_meets_shape_and_uniqueness(full_df: pd.DataFrame) -> None:
    df = full_df
    assert len(df) >= 100_000
    assert df["route_id"].nunique() >= 25
    assert df["delivery_id"].duplicated().sum() == 0


def test_generated_data_has_required_columns(full_df: pd.DataFrame) -> None:
    df = full_df
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    assert not missing
