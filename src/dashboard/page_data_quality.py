from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.dashboard.components import section_header, status_badge
from src.dashboard.dashboard_data import BASE_DIR, get_data_quality_checks


def render(df: pd.DataFrame) -> None:
    st.subheader("Data Quality and Validation")
    st.caption("Hiring manager note: this page demonstrates governance readiness with auditable validation outputs.")

    checks = get_data_quality_checks(df)
    section_header("Validation Status Cards")
    cols = st.columns(3)
    for i, (name, (ok, detail)) in enumerate(checks.items()):
        with cols[i % 3]:
            st.markdown(status_badge(ok, name), unsafe_allow_html=True)
            st.caption(detail)

    c1, c2, c3 = st.columns(3)
    dupes = int(df["delivery_id"].duplicated().sum())
    missing = int(df.isna().sum().sum())
    failed_rule = int(df[(df["delivery_status"] == "Failed") & (df["sla_met_flag"] != 0)].shape[0])
    c1.metric("Row Count Validation", "PASS" if len(df) >= 100_000 else "FAIL", f"{len(df):,} rows")
    c2.metric("Duplicate Delivery IDs", "PASS" if dupes == 0 else "FAIL", f"{dupes} duplicates")
    c3.metric("SLA Consistency", "PASS" if failed_rule == 0 else "FAIL", f"{failed_rule} failed-rule rows")

    section_header("Missing Value Summary")
    miss = df.isna().sum().reset_index()
    miss.columns = ["column", "missing_count"]
    st.dataframe(miss.sort_values("missing_count", ascending=False), use_container_width=True)

    summary_file = BASE_DIR / "data" / "processed" / "validation_summary.csv"
    section_header("Validation Summary Table")
    if summary_file.exists():
        summary_df = pd.read_csv(summary_file)
        st.dataframe(summary_df, use_container_width=True)
        freshness = pd.Timestamp(summary_file.stat().st_mtime, unit="s")
        st.caption(f"Data freshness: validation summary updated at {freshness}.")
    else:
        st.info("Validation summary not found. Run `python scripts/validate_data.py`.")
