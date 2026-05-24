from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.components import insight_box, metric_card, section_header
from src.metrics.failure_analysis import (
    address_issue_analysis,
    customer_unavailable_analysis,
    failure_reason_breakdown,
    failure_reason_by_zone,
)


def render(df: pd.DataFrame) -> None:
    st.subheader("Failure Reason Analysis")
    st.caption("Hiring manager note: this page demonstrates root-cause decomposition and targeted corrective action framing.")

    fr = failure_reason_breakdown(df)
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(fr, names="failure_reason", values="failed_deliveries", hole=0.55, title="Failure Reason Donut"), use_container_width=True)
    with c2:
        top_reason = fr.iloc[0]["failure_reason"] if not fr.empty else "N/A"
        top_share = fr.iloc[0]["failure_share_pct"] if not fr.empty else 0.0
        metric_card("Top Failure Driver", top_reason, f"Share of failures: {top_share:.2f}%")

    fz = failure_reason_by_zone(df)
    section_header("Zone and Route Root-Cause Patterns")
    st.plotly_chart(
        px.bar(
            fz,
            x="delivery_zone",
            y="failed_deliveries",
            color="failure_reason",
            title="Failure Reason by Zone (Stacked)",
        ),
        use_container_width=True,
    )

    route_reason = (
        df[df["delivery_status"] == "Failed"]
        .groupby(["route_id", "failure_reason"], as_index=False)
        .agg(failed=("delivery_id", "count"))
    )
    st.plotly_chart(
        px.density_heatmap(route_reason, x="route_id", y="failure_reason", z="failed", title="Route vs Failure Reason Heatmap"),
        use_container_width=True,
    )

    c3, c4 = st.columns(2)
    with c3:
        addr = address_issue_analysis(df).head(12)
        st.plotly_chart(px.bar(addr, x="delivery_zone", y="address_issue_failures", title="Top Address-Issue Zones"), use_container_width=True)
    with c4:
        cu = customer_unavailable_analysis(df)
        route_base = df.groupby(["scheduled_delivery_date"], as_index=False).agg(
            cust_unavailable=("failure_reason", lambda s: (s == "Customer Not Available").sum())
        )
        st.plotly_chart(px.line(route_base, x="scheduled_delivery_date", y="cust_unavailable", title="Customer Unavailable Trend"), use_container_width=True)

    failed_total = int((df["delivery_status"] == "Failed").sum())
    address_count = int((df["failure_reason"] == "Address Accuracy Issue").sum())
    insight_box(
        f"Root-cause insight: {failed_total:,} failures observed; address accuracy contributed {address_count:,} events. "
        "This indicates process gains from geocoding/address-validation interventions."
    )
