from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.components import insight_box, metric_card, section_header


def render(df: pd.DataFrame) -> None:
    st.subheader("Delivery Trend Analysis")
    st.caption("Hiring manager note: this page demonstrates time-series monitoring and weekday behavior diagnostics.")

    daily = (
        df.groupby("scheduled_delivery_date", as_index=False)
        .agg(deliveries=("delivery_id", "count"), sla_rate=("sla_met_flag", lambda s: s.mean() * 100), on_time=("on_time_flag", lambda s: s.mean() * 100), delay=("delay_minutes", "mean"))
        .sort_values("scheduled_delivery_date")
    )
    daily["late_rate"] = 100 - daily["on_time"]
    daily["late_roll_7"] = daily["late_rate"].rolling(7, min_periods=1).mean()
    monthly = (
        df.assign(month=df["scheduled_delivery_date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)
        .agg(volume=("delivery_id", "count"), sla=("sla_met_flag", lambda s: s.mean() * 100))
    )

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.area(monthly, x="month", y="volume", title="Monthly Delivery Volume"), use_container_width=True)
    with c2:
        st.plotly_chart(px.line(monthly, x="month", y="sla", markers=True, title="SLA Trend by Month"), use_container_width=True)

    dow = (
        df.assign(day=df["scheduled_delivery_date"].dt.day_name())
        .groupby("day", as_index=False)
        .agg(on_time=("on_time_flag", lambda s: s.mean() * 100), sla=("sla_met_flag", lambda s: s.mean() * 100))
    )
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow["day"] = pd.Categorical(dow["day"], order, ordered=True)
    dow = dow.sort_values("day")
    st.plotly_chart(px.bar(dow.melt(id_vars="day", value_vars=["on_time", "sla"]), x="day", y="value", color="variable", barmode="group", title="On-Time & SLA by Day of Week"), use_container_width=True)

    monday_friday = df[df["scheduled_delivery_date"].dt.day_name().isin(["Monday", "Friday"])]["on_time_flag"].mean() * 100
    midweek = df[df["scheduled_delivery_date"].dt.day_name().isin(["Tuesday", "Wednesday", "Thursday"])]["on_time_flag"].mean() * 100
    cc1, cc2 = st.columns(2)
    with cc1:
        metric_card("Monday/Friday On-Time", f"{monday_friday:.2f}%")
    with cc2:
        metric_card("Mid-Week On-Time", f"{midweek:.2f}%")

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(px.line(daily, x="scheduled_delivery_date", y="delay", title="Delay Minutes Trend"), use_container_width=True)
    with c4:
        st.plotly_chart(px.line(daily, x="scheduled_delivery_date", y="late_roll_7", title="Late Delivery 7-Day Rolling Average"), use_container_width=True)
    insight_box("Watch Monday/Friday vs mid-week gaps as an operational stress signal.")
