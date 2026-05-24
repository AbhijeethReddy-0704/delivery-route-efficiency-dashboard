from __future__ import annotations

import numpy as np
import pandas as pd


def total_deliveries(df: pd.DataFrame) -> int:
    return int(len(df))


def on_time_delivery_rate(df: pd.DataFrame) -> float:
    return float(df["on_time_flag"].mean() * 100)


def sla_attainment_rate(df: pd.DataFrame) -> float:
    return float(df["sla_met_flag"].mean() * 100)


def first_attempt_success_rate(df: pd.DataFrame) -> float:
    return float(df["first_attempt_success_flag"].mean() * 100)


def average_delivery_delay(df: pd.DataFrame) -> float:
    return float(df["delay_minutes"].mean())


def average_cost_per_delivery(df: pd.DataFrame) -> float:
    return float(df["delivery_cost"].mean())


def cost_per_mile(df: pd.DataFrame) -> float:
    total_distance = df["distance_miles"].sum()
    if total_distance <= 0:
        return 0.0
    return float(df["delivery_cost"].sum() / total_distance)


def average_delivery_attempts(df: pd.DataFrame) -> float:
    return float(df["attempt_count"].mean())


def failed_delivery_rate(df: pd.DataFrame) -> float:
    return float((df["delivery_status"].eq("Failed").mean()) * 100)


def route_efficiency_score(df: pd.DataFrame) -> float:
    """Composite score [0,100] from SLA, delay, and cost per mile."""
    sla_score = sla_attainment_rate(df)
    delay_penalty = min(100.0, average_delivery_delay(df) * 2.0)
    cpm_penalty = min(100.0, max(0.0, cost_per_mile(df) - 1.0) * 20.0)
    return float(np.clip((sla_score * 0.65) + ((100 - delay_penalty) * 0.20) + ((100 - cpm_penalty) * 0.15), 0, 100))


def driver_productivity_score(df: pd.DataFrame) -> float:
    """Composite score [0,100] from first-attempt success, on-time rate, and attempts."""
    attempt_penalty = min(100.0, max(0.0, average_delivery_attempts(df) - 1.0) * 45.0)
    return float(
        np.clip(
            (first_attempt_success_rate(df) * 0.45)
            + (on_time_delivery_rate(df) * 0.45)
            + ((100 - attempt_penalty) * 0.10),
            0,
            100,
        )
    )


def vehicle_utilization_efficiency(df: pd.DataFrame) -> float:
    """
    Estimate efficiency [0,100] by balancing productivity (miles delivered) with fuel use.
    Non-fuel vehicles are treated favorably via low fuel intensity.
    """
    deliveries = max(len(df), 1)
    miles_per_delivery = df["distance_miles"].sum() / deliveries
    fuel_per_delivery = df["fuel_consumed_gallons"].sum() / deliveries
    raw = (miles_per_delivery * 8.0) - (fuel_per_delivery * 30.0) + 45.0
    return float(np.clip(raw, 0, 100))


def last_mile_sla_attainment(df: pd.DataFrame) -> float:
    last_mile = df[df["last_mile_flag"] == 1]
    if last_mile.empty:
        return 0.0
    return float(last_mile["sla_met_flag"].mean() * 100)
