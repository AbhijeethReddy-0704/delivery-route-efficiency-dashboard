from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

INPUT_FILE = BASE_DIR / "data" / "processed" / "delivery_records.csv"
DB_FILE = BASE_DIR / "data" / "database" / "delivery_analytics.db"
SCHEMA_SQL = BASE_DIR / "sql" / "schema.sql"
VIEWS_SQL = BASE_DIR / "sql" / "views.sql"

from src.data.sqlite_loader import load_processed_csv_to_sqlite


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {INPUT_FILE}. Run scripts/generate_data.py first.")

    df = pd.read_csv(INPUT_FILE)
    counts = load_processed_csv_to_sqlite(
        csv_path=INPUT_FILE,
        db_path=DB_FILE,
        schema_sql_path=SCHEMA_SQL,
        views_sql_path=VIEWS_SQL,
    )

    csv_rows = len(df)
    sqlite_rows = counts["deliveries"]
    if sqlite_rows != csv_rows:
        raise ValueError(
            f"Row count mismatch between CSV and SQLite deliveries table. "
            f"CSV={csv_rows}, SQLite={sqlite_rows}"
        )

    print(f"SQLite database created: {DB_FILE}")
    print("Tables loaded:")
    for table_name in ["deliveries", "routes", "drivers", "warehouses", "vehicles", "delivery_zones"]:
        print(f"- {table_name}: {counts[table_name]:,} rows")
    print(f"Row count validation passed: CSV={csv_rows:,} == SQLite deliveries={sqlite_rows:,}")
    print("Views created:")
    print("- vw_daily_delivery_kpis")
    print("- vw_route_performance")
    print("- vw_driver_performance")
    print("- vw_vehicle_efficiency")
    print("- vw_failure_reason_summary")
    print("- vw_sla_improvement_opportunity")


if __name__ == "__main__":
    main()
