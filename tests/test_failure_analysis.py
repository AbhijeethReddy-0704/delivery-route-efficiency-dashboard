from __future__ import annotations

from src.metrics.failure_analysis import (
    address_issue_analysis,
    customer_unavailable_analysis,
    failed_first_attempt_rate_by_route,
    failure_reason_breakdown,
    failure_reason_by_zone,
    weather_traffic_delay_analysis,
)


def test_failure_breakdowns_have_content(sample_df) -> None:
    df = sample_df
    assert not failure_reason_breakdown(df).empty
    assert not failed_first_attempt_rate_by_route(df).empty
    assert not failure_reason_by_zone(df).empty


def test_failure_specialized_views_have_content(sample_df) -> None:
    df = sample_df
    assert not address_issue_analysis(df).empty
    assert not customer_unavailable_analysis(df).empty
    assert not weather_traffic_delay_analysis(df).empty
