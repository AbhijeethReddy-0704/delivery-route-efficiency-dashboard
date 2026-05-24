from __future__ import annotations

import pandas as pd


def failure_reason_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    failed = df[df["delivery_status"] == "Failed"]
    out = (
        failed.groupby("failure_reason", as_index=False)
        .agg(failed_deliveries=("delivery_id", "count"))
        .sort_values("failed_deliveries", ascending=False)
        .reset_index(drop=True)
    )
    total = max(out["failed_deliveries"].sum(), 1)
    out["failure_share_pct"] = (out["failed_deliveries"] / total) * 100
    return out


def failed_first_attempt_rate_by_route(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("route_id", as_index=False)
        .agg(
            deliveries=("delivery_id", "count"),
            first_attempt_failure_rate=("first_attempt_success_flag", lambda s: (1 - s.mean()) * 100),
        )
        .sort_values("first_attempt_failure_rate", ascending=False)
        .reset_index(drop=True)
    )
    return out


def failure_reason_by_zone(df: pd.DataFrame) -> pd.DataFrame:
    failed = df[df["delivery_status"] == "Failed"]
    return (
        failed.groupby(["delivery_zone", "failure_reason"], as_index=False)
        .agg(failed_deliveries=("delivery_id", "count"))
        .sort_values(["delivery_zone", "failed_deliveries"], ascending=[True, False])
        .reset_index(drop=True)
    )


def address_issue_analysis(df: pd.DataFrame) -> pd.DataFrame:
    mask = df["failure_reason"].eq("Address Accuracy Issue")
    out = (
        df.loc[mask]
        .groupby("delivery_zone", as_index=False)
        .agg(address_issue_failures=("delivery_id", "count"))
        .sort_values("address_issue_failures", ascending=False)
        .reset_index(drop=True)
    )
    return out


def customer_unavailable_analysis(df: pd.DataFrame) -> pd.DataFrame:
    mask = df["failure_reason"].eq("Customer Not Available")
    return (
        df.loc[mask]
        .groupby("route_id", as_index=False)
        .agg(customer_unavailable_failures=("delivery_id", "count"))
        .sort_values("customer_unavailable_failures", ascending=False)
        .reset_index(drop=True)
    )


def weather_traffic_delay_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["weather_condition", "traffic_condition"], as_index=False)
        .agg(
            avg_delay_minutes=("delay_minutes", "mean"),
            sla_attainment_rate=("sla_met_flag", lambda s: s.mean() * 100),
            delivery_volume=("delivery_id", "count"),
        )
        .sort_values("avg_delay_minutes", ascending=False)
        .reset_index(drop=True)
    )
