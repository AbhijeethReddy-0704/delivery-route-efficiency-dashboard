from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "data" / "processed" / "delivery_records.csv"
DB_PATH = BASE_DIR / "data" / "database" / "delivery_analytics.db"


def data_available() -> bool:
    return CSV_PATH.exists() or DB_PATH.exists()


def load_deliveries() -> pd.DataFrame:
    """Load deliveries with SQLite-first fallback to CSV."""
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        try:
            df = pd.read_sql_query("SELECT * FROM deliveries", conn)
        finally:
            conn.close()
    elif CSV_PATH.exists():
        df = pd.read_csv(CSV_PATH)
    else:
        raise FileNotFoundError("No local data found.")

    df["scheduled_delivery_date"] = pd.to_datetime(df["scheduled_delivery_date"], errors="coerce")
    df["actual_delivery_date"] = pd.to_datetime(df["actual_delivery_date"], errors="coerce")
    return df


def load_sql_view(view_name: str) -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    try:
        return pd.read_sql_query(f"SELECT * FROM {view_name}", conn)
    finally:
        conn.close()


def apply_filters(df: pd.DataFrame, filters: dict[str, Any]) -> pd.DataFrame:
    out = df.copy()
    if filters["date_range"] and len(filters["date_range"]) == 2:
        start, end = filters["date_range"]
        out = out[(out["scheduled_delivery_date"] >= pd.to_datetime(start)) & (out["scheduled_delivery_date"] <= pd.to_datetime(end))]

    for col, key in [
        ("route_id", "route"),
        ("delivery_zone", "delivery_zone"),
        ("warehouse_id", "warehouse"),
        ("vehicle_type", "vehicle_type"),
        ("driver_id", "driver"),
        ("customer_segment", "customer_segment"),
        ("delivery_status", "delivery_status"),
        ("package_priority", "package_priority"),
    ]:
        vals = filters.get(key, [])
        if vals:
            out = out[out[col].isin(vals)]

    return out


def get_data_quality_checks(df: pd.DataFrame) -> dict[str, tuple[bool, str]]:
    checks: dict[str, tuple[bool, str]] = {}
    checks["Row count >= 100,000"] = (len(df) >= 100_000, f"{len(df):,} rows")
    dupes = int(df["delivery_id"].duplicated().sum())
    checks["No duplicate delivery_id"] = (dupes == 0, f"{dupes} duplicates")
    missing = int(df.isna().sum().sum())
    checks["Missing values"] = (missing == 0, f"{missing} missing cells")
    date_ok = df["actual_delivery_date"].ge(df["scheduled_delivery_date"]).mean() >= 0.95
    checks["Date consistency"] = (bool(date_ok), "actual date mostly >= scheduled date")
    sla_ok = set(df["sla_met_flag"].dropna().unique()).issubset({0, 1})
    checks["SLA flag validity"] = (bool(sla_ok), "sla_met_flag in {0,1}")
    return checks
