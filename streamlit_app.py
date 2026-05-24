from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Delivery Performance & Route Efficiency", layout="wide")

from src.dashboard.dashboard_data import apply_filters, data_available, load_deliveries
from src.dashboard.components import inject_dashboard_css
from src.dashboard.page_cost_efficiency import render as render_cost_eff
from src.dashboard.page_data_quality import render as render_data_quality
from src.dashboard.page_delivery_trends import render as render_delivery_trends
from src.dashboard.page_driver_vehicle import render as render_driver_vehicle
from src.dashboard.page_executive_overview import render as render_exec
from src.dashboard.page_failure_analysis import render as render_failure
from src.dashboard.page_route_bottlenecks import render as render_routes


st.title("Delivery Performance & Route Efficiency Dashboard")
st.caption("Logistics analytics for third-party delivery operations using synthetic 100K+ records.")
inject_dashboard_css()

if not data_available():
    st.info(
        "No local dataset found. Generate data and build SQLite first:\n\n"
        "`python scripts/generate_data.py`\n\n"
        "`python scripts/build_sqlite_db.py`"
    )
    st.stop()

try:
    df_all = load_deliveries()
except Exception as exc:
    st.error("Could not load local data.")
    st.code(str(exc))
    st.info("Run:\n\n`python scripts/generate_data.py`\n\n`python scripts/build_sqlite_db.py`")
    st.stop()

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Page",
    [
        "Executive Overview",
        "Route Bottleneck Analysis",
        "Delivery Trend Analysis",
        "Failure Reason Analysis",
        "Driver and Vehicle Performance",
        "Cost and Efficiency Analysis",
        "Data Quality and Validation",
    ],
)

st.sidebar.header("Filters")
min_date = df_all["scheduled_delivery_date"].min().date()
max_date = df_all["scheduled_delivery_date"].max().date()
date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(date_range, tuple):
    normalized_date_range = date_range
elif isinstance(date_range, list) and len(date_range) == 2:
    normalized_date_range = (date_range[0], date_range[1])
else:
    normalized_date_range = (min_date, max_date)

def _ms(label: str, values: list[str]) -> list[str]:
    return st.sidebar.multiselect(label, values)

filters = {
    "date_range": normalized_date_range,
    "route": _ms("Route", sorted(df_all["route_id"].dropna().unique().tolist())),
    "delivery_zone": _ms("Delivery Zone", sorted(df_all["delivery_zone"].dropna().unique().tolist())),
    "warehouse": _ms("Warehouse", sorted(df_all["warehouse_id"].dropna().unique().tolist())),
    "vehicle_type": _ms("Vehicle Type", sorted(df_all["vehicle_type"].dropna().unique().tolist())),
    "driver": _ms("Driver", sorted(df_all["driver_id"].dropna().unique().tolist())),
    "customer_segment": _ms("Customer Segment", sorted(df_all["customer_segment"].dropna().unique().tolist())),
    "delivery_status": _ms("Delivery Status", sorted(df_all["delivery_status"].dropna().unique().tolist())),
    "package_priority": _ms("Package Priority", sorted(df_all["package_priority"].dropna().unique().tolist())),
}

df = apply_filters(df_all, filters)
if df.empty:
    st.warning("No data matches current filters. Adjust filters to continue.")
    st.stop()

if page == "Executive Overview":
    render_exec(df)
elif page == "Route Bottleneck Analysis":
    render_routes(df)
elif page == "Delivery Trend Analysis":
    render_delivery_trends(df)
elif page == "Failure Reason Analysis":
    render_failure(df)
elif page == "Driver and Vehicle Performance":
    render_driver_vehicle(df)
elif page == "Cost and Efficiency Analysis":
    render_cost_eff(df)
elif page == "Data Quality and Validation":
    render_data_quality(df)
