from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.components import insight_box, section_header


def render(df: pd.DataFrame) -> None:
    st.subheader("Driver and Vehicle Performance")
    st.caption("Hiring manager note: this page shows workforce and fleet performance segmentation for operational coaching.")

    driver = (
        df.groupby("driver_id", as_index=False)
        .agg(
            delivery_volume=("delivery_id", "count"),
            first_attempt_success=("first_attempt_success_flag", lambda s: s.mean() * 100),
            sla_rate=("sla_met_flag", lambda s: s.mean() * 100),
            avg_cost=("delivery_cost", "mean"),
            avg_delay=("delay_minutes", "mean"),
        )
    )
    driver["productivity"] = (driver["first_attempt_success"] * 0.45 + driver["sla_rate"] * 0.45 + (100 - driver["avg_delay"].clip(0, 25) * 4) * 0.10).clip(0, 100)

    top = driver.sort_values("productivity", ascending=False).head(10).assign(segment="Top 10")
    bottom = driver.sort_values("productivity").head(10).assign(segment="Bottom 10")
    leaderboard = pd.concat([top, bottom]).sort_values(["segment", "productivity"], ascending=[True, False])
    section_header("Driver Leaderboard")
    st.dataframe(leaderboard.style.background_gradient(subset=["productivity"], cmap="RdYlGn"), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            px.scatter(
                driver,
                x="delivery_volume",
                y="productivity",
                size="avg_delay",
                color="first_attempt_success",
                hover_name="driver_id",
                title="Driver Productivity Scatter",
            ),
            use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            px.bar(
                driver.sort_values("first_attempt_success", ascending=False).head(20),
                x="driver_id",
                y="first_attempt_success",
                title="First-Attempt Success by Driver (Top 20)",
            ),
            use_container_width=True,
        )

    vehicle = (
        df.groupby("vehicle_type", as_index=False)
        .agg(
            avg_cost=("delivery_cost", "mean"),
            fuel=("fuel_consumed_gallons", "sum"),
            distance=("distance_miles", "sum"),
            volume=("delivery_id", "count"),
        )
    )
    vehicle["fuel_efficiency"] = vehicle["distance"] / vehicle["fuel"].replace(0, pd.NA)
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(px.bar(vehicle, x="vehicle_type", y="avg_cost", title="Vehicle Type Cost Comparison"), use_container_width=True)
    with c4:
        st.plotly_chart(px.bar(vehicle, x="vehicle_type", y="fuel_efficiency", title="Fuel Efficiency by Vehicle Type"), use_container_width=True)

    heavy = vehicle[vehicle["vehicle_type"].isin(["Truck", "Mini Truck"])]
    if not heavy.empty:
        delta = heavy["avg_cost"].mean() - vehicle["avg_cost"].mean()
        insight_box(f"Heavy vehicle cost impact: heavy fleet runs ${delta:.2f} higher average cost per delivery versus network average.")
