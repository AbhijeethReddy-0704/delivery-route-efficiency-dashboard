from __future__ import annotations

from datetime import timedelta

import pandas as pd

from src.dashboard.dashboard_data import apply_filters, get_data_quality_checks, load_deliveries


def test_load_deliveries_returns_expected_columns(full_df: pd.DataFrame) -> None:
    df = load_deliveries()
    assert not df.empty
    for col in ["delivery_id", "route_id", "scheduled_delivery_date", "delivery_status"]:
        assert col in df.columns


def test_apply_filters_reduces_dataset(sample_df: pd.DataFrame) -> None:
    df = sample_df.copy()
    start = df["scheduled_delivery_date"].min()
    end = start + timedelta(days=30)
    some_route = [df["route_id"].iloc[0]]
    filtered = apply_filters(
        df,
        {
            "date_range": (start, end),
            "route": some_route,
            "delivery_zone": [],
            "warehouse": [],
            "vehicle_type": [],
            "driver": [],
            "customer_segment": [],
            "delivery_status": [],
            "package_priority": [],
        },
    )
    assert len(filtered) <= len(df)
    if not filtered.empty:
        assert filtered["route_id"].isin(some_route).all()


def test_data_quality_checks_shape(sample_df: pd.DataFrame) -> None:
    checks = get_data_quality_checks(sample_df)
    assert "No duplicate delivery_id" in checks
    assert all(len(v) == 2 for v in checks.values())
