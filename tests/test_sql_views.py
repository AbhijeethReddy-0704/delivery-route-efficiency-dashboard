from __future__ import annotations

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "database" / "delivery_analytics.db"

EXPECTED_VIEWS = [
    "vw_daily_delivery_kpis",
    "vw_route_performance",
    "vw_driver_performance",
    "vw_vehicle_efficiency",
    "vw_failure_reason_summary",
    "vw_sla_improvement_opportunity",
]


def test_expected_views_exist() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='view'").fetchall()
        found = {r[0] for r in rows}
    finally:
        conn.close()
    for view_name in EXPECTED_VIEWS:
        assert view_name in found


def test_sla_opportunity_view_returns_expected_range() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        row = conn.execute(
            "SELECT improvement_opportunity_percentage FROM vw_sla_improvement_opportunity"
        ).fetchone()
    finally:
        conn.close()
    assert row is not None
    assert 9.0 <= float(row[0]) <= 15.0
