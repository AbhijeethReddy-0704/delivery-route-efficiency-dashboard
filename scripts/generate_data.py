from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "delivery_records.csv"


def _pick_zone_profile(zone: str, outer_zones: set[str]) -> Dict[str, float]:
    if zone in outer_zones:
        return {"distance_low": 14.0, "distance_high": 42.0, "base_delay": 10.0}
    return {"distance_low": 2.0, "distance_high": 18.0, "base_delay": 0.0}


def main() -> None:
    rng = np.random.default_rng(42)
    n_records = 120_000

    route_ids = [f"R{idx:03d}" for idx in range(1, 31)]
    route_names = [f"Route-{idx:02d}" for idx in range(1, 31)]
    warehouses = [f"WH-{idx:02d}" for idx in range(1, 8)]
    zones = [f"Zone-{idx:02d}" for idx in range(1, 19)]
    drivers = [f"D{idx:04d}" for idx in range(1, 141)]

    vehicle_types = ["Van", "Bike", "Truck", "EV Van", "Cargo Bike", "Mini Truck"]
    vehicle_speed = {
        "Van": 0.95,
        "Bike": 1.35,
        "Truck": 0.90,
        "EV Van": 1.00,
        "Cargo Bike": 1.20,
        "Mini Truck": 0.92,
    }
    vehicle_cost_factor = {
        "Van": 1.00,
        "Bike": 0.70,
        "Truck": 1.28,
        "EV Van": 1.08,
        "Cargo Bike": 0.78,
        "Mini Truck": 1.12,
    }

    customer_segments = ["Residential", "SMB", "Enterprise", "Healthcare", "Retail"]
    package_priority_levels = ["Low", "Standard", "High", "Critical"]
    weather_conditions = ["Clear", "Rain", "Fog", "Storm", "Snow", "Heatwave"]
    traffic_conditions = ["Light", "Moderate", "Heavy", "Gridlock"]
    failure_reasons = [
        "Address Accuracy Issue",
        "Customer Not Available",
        "No Secure Drop Location",
        "Vehicle Breakdown",
        "Access Restricted",
    ]

    bottleneck_routes = {"R006", "R011", "R017", "R024", "R029"}
    challenged_routes = {"R003", "R006", "R009", "R011", "R017", "R019", "R022", "R024", "R027", "R029"}
    outer_zones = {"Zone-14", "Zone-15", "Zone-16", "Zone-17", "Zone-18"}

    scheduled_dates = pd.to_datetime("2025-05-25") + pd.to_timedelta(
        rng.integers(0, 365, size=n_records), unit="D"
    )
    delivery_ids = [f"DEL-{i:07d}" for i in range(1, n_records + 1)]

    route_idx = rng.integers(0, len(route_ids), size=n_records)
    route_id = np.array(route_ids)[route_idx]
    route_name = np.array(route_names)[route_idx]
    warehouse_id = rng.choice(warehouses, size=n_records, replace=True)
    delivery_zone = rng.choice(zones, size=n_records, replace=True)
    driver_id = rng.choice(drivers, size=n_records, replace=True)
    vehicle_type = rng.choice(vehicle_types, p=[0.34, 0.12, 0.22, 0.14, 0.08, 0.10], size=n_records)
    customer_segment = rng.choice(customer_segments, p=[0.50, 0.22, 0.12, 0.07, 0.09], size=n_records)
    package_priority = rng.choice(package_priority_levels, p=[0.15, 0.55, 0.22, 0.08], size=n_records)
    weather_condition = rng.choice(weather_conditions, p=[0.58, 0.18, 0.08, 0.05, 0.06, 0.05], size=n_records)
    traffic_condition = rng.choice(traffic_conditions, p=[0.26, 0.43, 0.23, 0.08], size=n_records)
    last_mile_flag = rng.choice([1, 0], p=[0.82, 0.18], size=n_records)

    scheduled_hour = rng.integers(8, 19, size=n_records)
    scheduled_minute = rng.choice([0, 10, 15, 20, 30, 40, 45, 50], size=n_records)
    scheduled_time_minutes = scheduled_hour * 60 + scheduled_minute

    weekday = scheduled_dates.dayofweek.to_numpy()
    monday_friday_dip = np.where(np.isin(weekday, [0, 4]), 8.0, 0.0)

    zone_profiles: List[Dict[str, float]] = [_pick_zone_profile(z, outer_zones) for z in delivery_zone]
    distance_miles = np.array(
        [rng.uniform(p["distance_low"], p["distance_high"]) for p in zone_profiles], dtype=float
    )

    base_travel = distance_miles * 5.6
    traffic_delay = np.select(
        [traffic_condition == "Light", traffic_condition == "Moderate", traffic_condition == "Heavy", traffic_condition == "Gridlock"],
        [0.0, rng.uniform(4, 12, n_records), rng.uniform(10, 22, n_records), rng.uniform(22, 45, n_records)],
    )
    weather_delay = np.select(
        [weather_condition == "Clear", weather_condition == "Rain", weather_condition == "Fog", weather_condition == "Storm", weather_condition == "Snow", weather_condition == "Heatwave"],
        [0.0, rng.uniform(3, 9, n_records), rng.uniform(5, 12, n_records), rng.uniform(15, 35, n_records), rng.uniform(12, 30, n_records), rng.uniform(4, 10, n_records)],
    )
    route_bottleneck_delay = np.where(np.isin(route_id, list(bottleneck_routes)), rng.uniform(12, 26, n_records), 0.0)
    route_challenge_delay = np.where(np.isin(route_id, list(challenged_routes)), rng.uniform(30, 60, n_records), 0.0)
    outer_zone_delay = np.where(np.isin(delivery_zone, list(outer_zones)), rng.uniform(6, 16, n_records), 0.0)
    priority_buffer = np.select(
        [package_priority == "Critical", package_priority == "High", package_priority == "Standard", package_priority == "Low"],
        [5.0, 2.0, 0.0, -2.0],
    )

    speed_factor = np.array([vehicle_speed[v] for v in vehicle_type])
    actual_minutes = (
        (base_travel / speed_factor)
        + traffic_delay
        + weather_delay
        + route_bottleneck_delay
        + route_challenge_delay
        + outer_zone_delay
        + monday_friday_dip
        - priority_buffer
    )

    customer_complexity = np.select(
        [customer_segment == "Residential", customer_segment == "SMB", customer_segment == "Enterprise", customer_segment == "Healthcare", customer_segment == "Retail"],
        [0.0, 2.0, 4.0, 5.0, 1.0],
    )
    actual_minutes = actual_minutes + customer_complexity + rng.normal(0, 4.2, n_records)
    actual_minutes = np.clip(actual_minutes, 8, None)

    sla_target_minutes = np.select(
        [package_priority == "Critical", package_priority == "High", package_priority == "Standard", package_priority == "Low"],
        [45, 75, 120, 180],
    ).astype(int)

    first_attempt_success_prob = (
        0.93
        - np.where(np.isin(delivery_zone, list(outer_zones)), 0.08, 0.0)
        - np.where(traffic_condition == "Gridlock", 0.04, 0.0)
        - np.where(np.isin(route_id, list(challenged_routes)), 0.26, 0.0)
    )
    first_attempt_success_prob = np.clip(first_attempt_success_prob, 0.70, 0.98)
    first_attempt_success_flag = (rng.random(n_records) < first_attempt_success_prob).astype(int)

    attempt_count = np.where(first_attempt_success_flag == 1, 1, rng.choice([2, 3], p=[0.86, 0.14], size=n_records))
    reattempt_penalty = np.where(attempt_count > 1, rng.uniform(18, 55, n_records), 0.0)
    actual_minutes = actual_minutes + reattempt_penalty

    on_time_flag = (actual_minutes <= (sla_target_minutes + 10)).astype(int)
    sla_met_flag = (actual_minutes <= sla_target_minutes).astype(int)

    failure_base_prob = (
        0.02
        + np.where(first_attempt_success_flag == 0, 0.08, 0.0)
        + np.where(weather_condition == "Storm", 0.03, 0.0)
        + np.where(np.isin(route_id, list(challenged_routes)), 0.16, 0.0)
    )
    failed_mask = rng.random(n_records) < np.clip(failure_base_prob, 0.01, 0.22)

    delivery_status = np.where(failed_mask, "Failed", np.where(sla_met_flag == 1, "Delivered On Time", "Delivered Late"))
    failure_reason = np.where(failed_mask, rng.choice(failure_reasons, size=n_records), "None")

    fuel_rate = np.select(
        [vehicle_type == "Bike", vehicle_type == "Cargo Bike", vehicle_type == "EV Van", vehicle_type == "Van", vehicle_type == "Truck", vehicle_type == "Mini Truck"],
        [0.0, 0.0, 0.04, 0.08, 0.17, 0.13],
    )
    fuel_consumed_gallons = np.round(distance_miles * fuel_rate + np.where(traffic_condition == "Gridlock", 0.25, 0.0), 3)
    fuel_consumed_gallons = np.clip(fuel_consumed_gallons, 0, None)

    vehicle_factor = np.array([vehicle_cost_factor[v] for v in vehicle_type])
    delivery_cost = (
        6.5
        + (distance_miles * 1.45 * vehicle_factor)
        + (actual_minutes * 0.22 * vehicle_factor)
        + (attempt_count - 1) * 4.2
        + np.where(weather_condition == "Storm", 3.0, 0.0)
    )
    delivery_cost = np.round(np.clip(delivery_cost, 2.5, None), 2)

    delay_minutes = np.where(actual_minutes > sla_target_minutes, np.round(actual_minutes - sla_target_minutes, 2), 0.0)
    sla_met_flag = np.where(delivery_status == "Failed", 0, sla_met_flag)
    on_time_flag = np.where(delivery_status == "Failed", 0, on_time_flag)

    actual_time_minutes = np.clip(np.round(scheduled_time_minutes + actual_minutes).astype(int), 0, (24 * 60) - 1)
    actual_date = scheduled_dates + pd.to_timedelta(actual_time_minutes // (24 * 60), unit="D")
    actual_time_of_day = actual_time_minutes % (24 * 60)

    scheduled_delivery_time = pd.to_datetime(scheduled_time_minutes, unit="m").strftime("%H:%M:%S")
    actual_delivery_time = pd.to_datetime(actual_time_of_day, unit="m").strftime("%H:%M:%S")

    df = pd.DataFrame(
        {
            "delivery_id": delivery_ids,
            "route_id": route_id,
            "route_name": route_name,
            "warehouse_id": warehouse_id,
            "delivery_zone": delivery_zone,
            "driver_id": driver_id,
            "vehicle_type": vehicle_type,
            "customer_segment": customer_segment,
            "scheduled_delivery_date": scheduled_dates.strftime("%Y-%m-%d"),
            "actual_delivery_date": actual_date.strftime("%Y-%m-%d"),
            "scheduled_delivery_time": scheduled_delivery_time,
            "actual_delivery_time": actual_delivery_time,
            "delivery_status": delivery_status,
            "sla_target_minutes": sla_target_minutes.astype(int),
            "actual_delivery_minutes": np.round(actual_minutes, 2),
            "distance_miles": np.round(distance_miles, 2),
            "fuel_consumed_gallons": fuel_consumed_gallons,
            "delivery_cost": delivery_cost,
            "attempt_count": attempt_count.astype(int),
            "first_attempt_success_flag": first_attempt_success_flag.astype(int),
            "on_time_flag": on_time_flag.astype(int),
            "sla_met_flag": sla_met_flag.astype(int),
            "delay_minutes": delay_minutes,
            "failure_reason": failure_reason,
            "weather_condition": weather_condition,
            "traffic_condition": traffic_condition,
            "package_priority": package_priority,
            "last_mile_flag": last_mile_flag.astype(int),
        }
    )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Generated {len(df):,} delivery records")
    print(f"Routes: {df['route_id'].nunique()} | Zones: {df['delivery_zone'].nunique()} | Warehouses: {df['warehouse_id'].nunique()} | Drivers: {df['driver_id'].nunique()}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
