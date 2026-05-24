from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.components import insight_box, section_header


def render(df: pd.DataFrame) -> None:
    st.subheader("Cost and Efficiency Analysis")
    st.caption("Hiring manager note: this page emphasizes financial analytics and route-level cost-efficiency prioritization.")

    daily_cost = (
        df.groupby("scheduled_delivery_date", as_index=False)
        .agg(avg_cost=("delivery_cost", "mean"), avg_delay=("delay_minutes", "mean"))
        .sort_values("scheduled_delivery_date")
    )
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.line(daily_cost, x="scheduled_delivery_date", y="avg_cost", title="Cost per Delivery Trend"), use_container_width=True)
    with c2:
        st.plotly_chart(px.line(daily_cost, x="scheduled_delivery_date", y="avg_delay", title="Delay Minutes Trend"), use_container_width=True)

    route = (
        df.groupby("route_id", as_index=False)
        .agg(total_cost=("delivery_cost", "sum"), total_miles=("distance_miles", "sum"), avg_cost=("delivery_cost", "mean"))
    )
    route["cost_per_mile"] = route["total_cost"] / route["total_miles"].clip(lower=0.001)
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(px.bar(route.sort_values("cost_per_mile", ascending=False).head(20), x="route_id", y="cost_per_mile", title="Cost per Mile by Route"), use_container_width=True)
    with c4:
        st.plotly_chart(px.bar(route.sort_values("avg_cost", ascending=False).head(15), x="route_id", y="avg_cost", title="High-Cost Route Ranking"), use_container_width=True)

    vehicle_fuel = df.groupby("vehicle_type", as_index=False).agg(fuel=("fuel_consumed_gallons", "sum"))
    st.plotly_chart(px.bar(vehicle_fuel, x="vehicle_type", y="fuel", title="Fuel Consumption by Vehicle Type"), use_container_width=True)

    sample = df.sample(min(len(df), 6000), random_state=42)
    st.plotly_chart(
        px.scatter(sample, x="distance_miles", y="delivery_cost", color="vehicle_type", opacity=0.55, title="Route Distance vs Delivery Cost Scatter"),
        use_container_width=True,
    )

    delta = route["avg_cost"].max() - route["avg_cost"].median()
    section_header("Cost-Efficiency Opportunity")
    insight_box(f"Highest-cost routes are about ${delta:.2f} above median route cost per delivery, indicating a strong cost-normalization opportunity.")
