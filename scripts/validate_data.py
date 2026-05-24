from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.metrics.sla_opportunity import calculate_sla_improvement_opportunity


DATA_FILE = BASE_DIR / "data" / "processed" / "delivery_records.csv"
SUMMARY_FILE = BASE_DIR / "data" / "processed" / "validation_summary.csv"

REQUIRED_COLUMNS = [
    "delivery_id",
    "route_id",
    "route_name",
    "warehouse_id",
    "delivery_zone",
    "driver_id",
    "vehicle_type",
    "customer_segment",
    "scheduled_delivery_date",
    "actual_delivery_date",
    "scheduled_delivery_time",
    "actual_delivery_time",
    "delivery_status",
    "sla_target_minutes",
    "actual_delivery_minutes",
    "distance_miles",
    "fuel_consumed_gallons",
    "delivery_cost",
    "attempt_count",
    "first_attempt_success_flag",
    "on_time_flag",
    "sla_met_flag",
    "delay_minutes",
    "failure_reason",
    "weather_condition",
    "traffic_condition",
    "package_priority",
    "last_mile_flag",
]


def run_validation(
    df: pd.DataFrame,
    required_columns: list[str] | None = None,
    expected_min_rows: int = 100_000,
    expected_min_routes: int = 25,
    summary_path: Path | None = None,
) -> tuple[bool, pd.DataFrame]:
    required = required_columns or REQUIRED_COLUMNS
    results: list[dict[str, str]] = []

    def add_check(name: str, passed: bool, expected: str, actual: str, notes: str = "") -> None:
        results.append(
            {
                "check_name": name,
                "result": "pass" if passed else "fail",
                "expected_value": expected,
                "actual_value": actual,
                "status": "PASS" if passed else "FAIL",
                "notes": notes,
            }
        )

    row_count = len(df)
    unique_routes = int(df["route_id"].nunique()) if "route_id" in df.columns else 0
    duplicate_ids = int(df["delivery_id"].duplicated().sum()) if "delivery_id" in df.columns else -1
    missing_cols = [c for c in required if c not in df.columns]

    add_check("row_count_minimum", row_count >= expected_min_rows, f">={expected_min_rows}", str(row_count))
    add_check("unique_routes_minimum", unique_routes >= expected_min_routes, f">={expected_min_routes}", str(unique_routes))
    add_check("duplicate_delivery_id", duplicate_ids == 0, "0", str(duplicate_ids))
    add_check("required_columns_present", len(missing_cols) == 0, "none missing", ",".join(missing_cols) if missing_cols else "none")

    if not missing_cols:
        add_check("cost_non_negative", bool((df["delivery_cost"] >= 0).all()), "all >= 0", f"min={df['delivery_cost'].min():.2f}")
        add_check("distance_positive", bool((df["distance_miles"] > 0).all()), "all > 0", f"min={df['distance_miles'].min():.2f}")
        add_check(
            "on_time_flag_valid",
            set(df["on_time_flag"].dropna().unique()).issubset({0, 1}),
            "subset of {0,1}",
            str(sorted(df["on_time_flag"].dropna().unique().tolist())),
        )
        add_check(
            "sla_met_flag_valid",
            set(df["sla_met_flag"].dropna().unique()).issubset({0, 1}),
            "subset of {0,1}",
            str(sorted(df["sla_met_flag"].dropna().unique().tolist())),
        )

        scheduled_dates = pd.to_datetime(df["scheduled_delivery_date"], errors="coerce")
        actual_dates = pd.to_datetime(df["actual_delivery_date"], errors="coerce")
        add_check("scheduled_date_valid", bool(scheduled_dates.notna().all()), "all parseable", f"invalid={(~scheduled_dates.notna()).sum()}")
        add_check("actual_date_valid", bool(actual_dates.notna().all()), "all parseable", f"invalid={(~actual_dates.notna()).sum()}")

        failed_sla_break = int(df[(df["delivery_status"] == "Failed") & (df["sla_met_flag"] != 0)].shape[0])
        add_check(
            "failed_delivery_sla_rule",
            failed_sla_break == 0,
            "failed deliveries have sla_met_flag=0",
            str(failed_sla_break),
            "business rule check",
        )

        opportunity = calculate_sla_improvement_opportunity(df)
        improvement_pct = float(opportunity["improvement_opportunity_percentage"])
        add_check(
            "sla_improvement_opportunity_range",
            9.0 <= improvement_pct <= 15.0,
            "between 9% and 15%",
            f"{improvement_pct:.2f}%",
            "synthetic dataset expectation (~12%)",
        )
    else:
        improvement_pct = float("nan")

    summary_df = pd.DataFrame(results)
    out_path = summary_path or SUMMARY_FILE
    out_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(out_path, index=False)
    all_passed = bool((summary_df["status"] == "PASS").all())
    return all_passed, summary_df


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}. Run scripts/generate_data.py first.")

    df = pd.read_csv(DATA_FILE)
    passed, summary_df = run_validation(df)
    if not passed:
        failed = summary_df[summary_df["status"] == "FAIL"]
        raise AssertionError(f"Validation failed. Failing checks: {failed['check_name'].tolist()}")

    improvement_row = summary_df.loc[summary_df["check_name"] == "sla_improvement_opportunity_range", "actual_value"]
    improvement_display = improvement_row.iloc[0] if not improvement_row.empty else "n/a"
    print("Validation passed")
    print(f"Rows: {len(df):,}")
    print(f"Unique routes: {df['route_id'].nunique()}")
    print(f"Unique drivers: {df['driver_id'].nunique()}")
    print(f"Synthetic SLA improvement opportunity (bottom routes to median route SLA): {improvement_display}")
    print(f"Validation summary written: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
