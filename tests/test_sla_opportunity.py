from __future__ import annotations

from src.metrics.route_analysis import bottleneck_route_count
from src.metrics.sla_opportunity import calculate_sla_improvement_opportunity, improvement_opportunity_percentage


def test_sla_opportunity_dict_contains_expected_fields(sample_df) -> None:
    df = sample_df
    result = calculate_sla_improvement_opportunity(df)
    expected_keys = {
        "current_overall_sla_attainment",
        "median_route_sla_attainment",
        "bottom_route_count",
        "projected_sla_attainment",
        "improvement_opportunity_percentage",
    }
    assert expected_keys.issubset(result.keys())


def test_sla_opportunity_is_approximately_twelve_percent(full_df) -> None:
    df = full_df
    improvement = improvement_opportunity_percentage(df)
    assert 9.0 <= improvement <= 15.0
    assert bottleneck_route_count(df) > 0
