from __future__ import annotations

from pathlib import Path

import pandas as pd

from scripts.validate_data import REQUIRED_COLUMNS, run_validation


BASE_DIR = Path(__file__).resolve().parents[1]
SUMMARY_FILE = BASE_DIR / "data" / "processed" / "validation_summary.csv"


def test_validation_passes_for_full_dataset(full_df: pd.DataFrame) -> None:
    passed, summary = run_validation(full_df, summary_path=SUMMARY_FILE)
    assert passed
    assert not summary.empty


def test_validation_summary_schema_written(full_df: pd.DataFrame) -> None:
    run_validation(full_df, summary_path=SUMMARY_FILE)
    assert SUMMARY_FILE.exists()
    summary = pd.read_csv(SUMMARY_FILE)
    expected_cols = ["check_name", "result", "expected_value", "actual_value", "status", "notes"]
    assert list(summary.columns) == expected_cols
    assert set(summary["status"]).issubset({"PASS", "FAIL"})


def test_validation_catches_duplicate_ids(sample_df: pd.DataFrame) -> None:
    df = sample_df.copy()
    df.loc[1, "delivery_id"] = df.loc[0, "delivery_id"]
    passed, summary = run_validation(
        df,
        required_columns=REQUIRED_COLUMNS,
        expected_min_rows=1,
        expected_min_routes=1,
        summary_path=SUMMARY_FILE,
    )
    assert not passed
    row = summary[summary["check_name"] == "duplicate_delivery_id"].iloc[0]
    assert row["status"] == "FAIL"
