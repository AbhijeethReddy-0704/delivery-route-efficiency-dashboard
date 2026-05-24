from __future__ import annotations

from src.metrics import kpi_calculations as kpi


def test_core_kpis_are_in_expected_ranges(sample_df) -> None:
    df = sample_df
    assert kpi.total_deliveries(df) > 0
    assert kpi.total_deliveries(df) <= 2000
    assert 0 <= kpi.on_time_delivery_rate(df) <= 100
    assert 0 <= kpi.sla_attainment_rate(df) <= 100
    assert 0 <= kpi.first_attempt_success_rate(df) <= 100
    assert kpi.average_delivery_delay(df) >= 0
    assert kpi.average_cost_per_delivery(df) > 0
    assert kpi.cost_per_mile(df) > 0
    assert kpi.average_delivery_attempts(df) >= 1
    assert 0 <= kpi.failed_delivery_rate(df) <= 100


def test_composite_scores_are_bounded(sample_df) -> None:
    df = sample_df
    assert 0 <= kpi.route_efficiency_score(df) <= 100
    assert 0 <= kpi.driver_productivity_score(df) <= 100
    assert 0 <= kpi.vehicle_utilization_efficiency(df) <= 100
    assert 0 <= kpi.last_mile_sla_attainment(df) <= 100
