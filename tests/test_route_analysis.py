from __future__ import annotations

from src.metrics.route_analysis import (
    bottleneck_route_count,
    build_route_metrics,
    identify_bottleneck_routes,
    rank_routes_by_delay,
    rank_routes_by_sla,
    top_worst_performing_routes,
)


def test_route_rankings_and_shapes(full_df) -> None:
    df = full_df
    metrics = build_route_metrics(df)
    assert len(metrics) >= 25

    by_sla = rank_routes_by_sla(df)
    by_delay = rank_routes_by_delay(df)
    worst_10 = top_worst_performing_routes(df, n=10)

    assert len(by_sla) == len(metrics)
    assert len(by_delay) == len(metrics)
    assert len(worst_10) == 10


def test_bottleneck_detection_returns_routes(sample_df) -> None:
    df = sample_df
    bottlenecks = identify_bottleneck_routes(df)
    assert len(bottlenecks) > 0
    assert bottleneck_route_count(df) == len(bottlenecks)
