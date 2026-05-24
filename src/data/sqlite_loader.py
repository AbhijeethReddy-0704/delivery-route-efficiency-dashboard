from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def execute_sql_file(conn: sqlite3.Connection, sql_file: Path) -> None:
    """Execute a SQL script file against an open SQLite connection."""
    sql_text = sql_file.read_text(encoding="utf-8")
    conn.executescript(sql_text)


def load_processed_csv_to_sqlite(
    csv_path: Path,
    db_path: Path,
    schema_sql_path: Path,
    views_sql_path: Path,
) -> dict[str, int]:
    """
    Build the analytics SQLite database from processed CSV data and SQL scripts.
    Returns row counts by table for validation and reporting.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Processed CSV not found: {csv_path}")
    if not schema_sql_path.exists():
        raise FileNotFoundError(f"Schema SQL not found: {schema_sql_path}")
    if not views_sql_path.exists():
        raise FileNotFoundError(f"Views SQL not found: {views_sql_path}")

    db_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(csv_path, keep_default_na=False)

    conn = sqlite3.connect(db_path)
    try:
        execute_sql_file(conn, schema_sql_path)
        df.to_sql("deliveries", conn, if_exists="append", index=False)

        conn.executescript(
            """
            INSERT INTO routes(route_id, route_name)
            SELECT DISTINCT route_id, route_name FROM deliveries;

            INSERT INTO drivers(driver_id)
            SELECT DISTINCT driver_id FROM deliveries;

            INSERT INTO warehouses(warehouse_id)
            SELECT DISTINCT warehouse_id FROM deliveries;

            INSERT INTO vehicles(vehicle_type)
            SELECT DISTINCT vehicle_type FROM deliveries;

            INSERT INTO delivery_zones(delivery_zone)
            SELECT DISTINCT delivery_zone FROM deliveries;
            """
        )

        execute_sql_file(conn, views_sql_path)
        conn.commit()

        counts = {}
        for table in ["deliveries", "routes", "drivers", "warehouses", "vehicles", "delivery_zones"]:
            counts[table] = int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
    finally:
        conn.close()

    return counts
