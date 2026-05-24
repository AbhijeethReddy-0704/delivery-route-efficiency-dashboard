from __future__ import annotations

import pandas as pd


def build_route_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate route-level metrics used for ranking and bottleneck detection."""
    grouped = (
        df.groupby(["route_id", "route_name"], as_index=False)
        .agg(
            delivery_volume=("delivery_id", "count"),
            sla_attainment_rate=("sla_met_flag", lambda s: s.mean() * 100),
            avg_delay_minutes=("delay_minutes", "mean"),
            failed_delivery_rate=("delivery_status", lambda s: s.eq("Failed").mean() * 100),
            first_attempt_success_rate=("first_attempt_success_flag", lambda s: s.mean() * 100),
            cost_per_delivery=("delivery_cost", "mean"),
            on_time_rate=("on_time_flag", lambda s: s.mean() * 100),
        )
        .copy()
    )

    delay_component = 100 - grouped["avg_delay_minutes"].clip(lower=0, upper=50) * 2
    cost_component = 100 - (grouped["cost_per_delivery"] - grouped["cost_per_delivery"].median()).clip(lower=-20, upper=20) * 2

    grouped["route_efficiency_score"] = (
        grouped["sla_attainment_rate"] * 0.50
        + grouped["first_attempt_success_rate"] * 0.20
        + grouped["on_time_rate"] * 0.15
        + delay_component * 0.10
        + cost_component * 0.05
    ).clip(lower=0, upper=100)

    return grouped.sort_values("route_id").reset_index(drop=True)


def rank_routes_by_sla(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    return build_route_metrics(df).sort_values("sla_attainment_rate", ascending=ascending).reset_index(drop=True)


def rank_routes_by_delay(df: pd.DataFrame, ascending: bool = False) -> pd.DataFrame:
    return build_route_metrics(df).sort_values("avg_delay_minutes", ascending=ascending).reset_index(drop=True)


def top_worst_performing_routes(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    metrics = build_route_metrics(df).copy()
    score = (
        (100 - metrics["sla_attainment_rate"]) * 0.45
        + metrics["avg_delay_minutes"] * 0.25
        + metrics["failed_delivery_rate"] * 0.20
        + (100 - metrics["first_attempt_success_rate"]) * 0.10
    )
    metrics["worst_route_score"] = score
    return metrics.sort_values("worst_route_score", ascending=False).head(n).reset_index(drop=True)


def identify_bottleneck_routes(
    df: pd.DataFrame,
    sla_threshold: float = 55.0,
    delay_threshold: float = 15.0,
    failure_threshold: float = 10.0,
) -> pd.DataFrame:
    metrics = build_route_metrics(df)
    mask = (
        (metrics["sla_attainment_rate"] <= sla_threshold)
        | (metrics["avg_delay_minutes"] >= delay_threshold)
        | (metrics["failed_delivery_rate"] >= failure_threshold)
    )
    return metrics.loc[mask].sort_values(["sla_attainment_rate", "avg_delay_minutes"], ascending=[True, False]).reset_index(drop=True)


def bottleneck_route_count(df: pd.DataFrame) -> int:
    return int(len(identify_bottleneck_routes(df)))
