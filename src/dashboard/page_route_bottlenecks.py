from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.components import insight_box, section_header, styled_dataframe
from src.metrics.route_analysis import build_route_metrics, identify_bottleneck_routes, top_worst_performing_routes


def render(df: pd.DataFrame) -> None:
    st.subheader("Route Bottleneck Analysis")
    st.caption("Hiring manager note: this page highlights route prioritization logic and bottleneck targeting maturity.")

    route_metrics = build_route_metrics(df).sort_values("sla_attainment_rate")
    section_header("Route Performance Leaderboard", "Lowest SLA routes appear first for quick prioritization.")
    styled_dataframe(route_metrics, "sla_attainment_rate")

    c1, c2 = st.columns(2)
    with c1:
        worst = top_worst_performing_routes(df, n=10).sort_values("worst_route_score")
        fig = px.bar(worst, x="worst_route_score", y="route_id", orientation="h", title="Top 10 Bottleneck Routes")
        fig.update_layout(xaxis_title="Bottleneck Severity Score", yaxis_title="Route")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.histogram(route_metrics, x="route_efficiency_score", nbins=16, title="Route Efficiency Score Distribution")
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        heat_df = route_metrics[["route_id", "sla_attainment_rate"]].copy()
        heat_df["metric"] = "SLA"
        fig3 = px.density_heatmap(heat_df, x="route_id", y="metric", z="sla_attainment_rate", title="SLA Attainment by Route Heatmap")
        st.plotly_chart(fig3, use_container_width=True)
    with c4:
        fig4 = px.scatter(
            route_metrics,
            x="delivery_volume",
            y="sla_attainment_rate",
            size="avg_delay_minutes",
            color="failed_delivery_rate",
            hover_name="route_id",
            title="Route Volume vs SLA (Bubble = Avg Delay)",
        )
        st.plotly_chart(fig4, use_container_width=True)

    bottlenecks = identify_bottleneck_routes(df)
    median_sla = route_metrics["sla_attainment_rate"].median()
    bottlenecks["opportunity_to_median_sla"] = (median_sla - bottlenecks["sla_attainment_rate"]).clip(lower=0)
    fig5 = px.bar(
        bottlenecks.sort_values("opportunity_to_median_sla", ascending=False).head(15),
        x="route_id",
        y="opportunity_to_median_sla",
        title="Improvement Opportunity by Route (to Median SLA)",
    )
    st.plotly_chart(fig5, use_container_width=True)
    insight_box("Focus first on the few routes with the largest SLA gap-to-median and high delivery volume.")
