from __future__ import annotations

import pandas as pd

from src.metrics.route_analysis import build_route_metrics


def calculate_sla_improvement_opportunity(df: pd.DataFrame, bottom_share: float = 0.33) -> dict[str, float]:
    """
    Estimate SLA uplift if bottom-performing routes improve up to median route SLA.
    Returns percentages in points, not proportions.
    """
    route_metrics = build_route_metrics(df)
    current_overall_sla = float(df["sla_met_flag"].mean() * 100)
    median_route_sla = float(route_metrics["sla_attainment_rate"].median())

    bottom_n = max(1, int(len(route_metrics) * bottom_share))
    bottom_routes = route_metrics.nsmallest(bottom_n, "sla_attainment_rate").copy()
    gap = (median_route_sla - bottom_routes["sla_attainment_rate"]).clip(lower=0)

    weighted_uplift = float((gap * bottom_routes["delivery_volume"]).sum() / max(route_metrics["delivery_volume"].sum(), 1))
    projected_sla = current_overall_sla + weighted_uplift

    return {
        "current_overall_sla_attainment": current_overall_sla,
        "median_route_sla_attainment": median_route_sla,
        "bottom_route_count": float(bottom_n),
        "projected_sla_attainment": projected_sla,
        "improvement_opportunity_percentage": weighted_uplift,
    }


def improvement_opportunity_percentage(df: pd.DataFrame) -> float:
    return float(calculate_sla_improvement_opportunity(df)["improvement_opportunity_percentage"])
