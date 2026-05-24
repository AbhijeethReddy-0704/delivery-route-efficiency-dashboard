from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.components import insight_box, metric_card, section_header
from src.metrics.kpi_calculations import (
    average_cost_per_delivery,
    failed_delivery_rate,
    first_attempt_success_rate,
    on_time_delivery_rate,
    sla_attainment_rate,
    total_deliveries,
)
from src.metrics.sla_opportunity import improvement_opportunity_percentage


def render(df: pd.DataFrame) -> None:
    st.subheader("Executive Overview")
    st.caption("Hiring manager note: this page demonstrates clear executive KPI communication and prioritization-ready insights.")

    k1, k2, k3 = st.columns(3)
    with k1:
        metric_card("Total Deliveries", f"{total_deliveries(df):,}")
    with k2:
        metric_card("SLA Attainment Rate", f"{sla_attainment_rate(df):.2f}%")
    with k3:
        metric_card("On-Time Delivery Rate", f"{on_time_delivery_rate(df):.2f}%")

    k4, k5, k6 = st.columns(3)
    with k4:
        metric_card("First Attempt Success", f"{first_attempt_success_rate(df):.2f}%")
    with k5:
        metric_card("Average Cost / Delivery", f"${average_cost_per_delivery(df):.2f}")
    with k6:
        metric_card("Failed Delivery Rate", f"{failed_delivery_rate(df):.2f}%")

    opp = improvement_opportunity_percentage(df)
    st.markdown(
        f"<div class='hero-card'><div style='font-size:0.9rem;'>SLA Improvement Opportunity (Synthetic)</div>"
        f"<div style='font-size:2rem;font-weight:800;'>{opp:.2f}%</div>"
        f"<div class='hero-sub'>Modeled uplift by improving bottom-performing routes to median route SLA.</div></div>",
        unsafe_allow_html=True,
    )
    insight_box(
        "Executive insight: the synthetic network suggests a concentrated opportunity in underperforming routes. "
        "A focused improvement program on route bottlenecks can materially improve last-mile SLA attainment."
    )

    section_header("Trend Monitoring", "Monthly SLA and volume movement")
    monthly = (
        df.assign(month=df["scheduled_delivery_date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)
        .agg(deliveries=("delivery_id", "count"), sla_rate=("sla_met_flag", lambda s: s.mean() * 100))
    )
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.line(monthly, x="month", y="sla_rate", markers=True, title="Monthly SLA Trend")
        fig1.update_layout(yaxis_title="SLA Attainment (%)", xaxis_title="Month")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.area(monthly, x="month", y="deliveries", title="Delivery Volume Trend")
        fig2.update_layout(yaxis_title="Deliveries", xaxis_title="Month")
        st.plotly_chart(fig2, use_container_width=True)

    status = pd.DataFrame(
        {"status": ["On-Time", "Late"], "count": [int(df["on_time_flag"].sum()), int((1 - df["on_time_flag"]).sum())]}
    )
    fig3 = px.pie(status, values="count", names="status", hole=0.55, title="On-Time vs Late Delivery Mix", color="status", color_discrete_map={"On-Time": "#16a34a", "Late": "#dc2626"})
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("Methodology Notes"):
        st.write("SLA improvement opportunity is synthetic and estimated from route-level uplift to median SLA performance.")
