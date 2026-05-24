from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "data" / "processed" / "delivery_records.csv"
DB_PATH = BASE_DIR / "data" / "database" / "delivery_analytics.db"


def test_sqlite_deliveries_row_count_matches_csv() -> None:
    csv_rows = len(pd.read_csv(CSV_PATH))
    conn = sqlite3.connect(DB_PATH)
    try:
        sqlite_rows = conn.execute("SELECT COUNT(*) FROM deliveries").fetchone()[0]
    finally:
        conn.close()
    assert sqlite_rows == csv_rows


def test_dimension_tables_have_values() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        for table in ["routes", "drivers", "warehouses", "vehicles", "delivery_zones"]:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            assert count > 0
    finally:
        conn.close()
