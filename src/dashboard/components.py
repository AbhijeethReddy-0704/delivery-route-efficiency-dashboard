from __future__ import annotations

import pandas as pd
import streamlit as st


def inject_dashboard_css() -> None:
    st.markdown(
        """
        <style>
        .main > div {padding-top: 1rem;}
        .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
        .stSidebar {border-right: 1px solid #e8e8ef;}
        .metric-card {
            background: #ffffff;
            border: 1px solid #ececf3;
            border-radius: 10px;
            padding: 14px 16px;
            box-shadow: 0 4px 14px rgba(16, 24, 40, 0.06);
            min-height: 104px;
        }
        .metric-label {font-size: 0.82rem; color: #667085; margin-bottom: 4px;}
        .metric-value {font-size: 1.65rem; font-weight: 700; color: #101828;}
        .hero-card {
            background: linear-gradient(135deg, #0f4c81, #2563eb);
            color: white;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 8px 18px rgba(37,99,235,0.22);
        }
        .hero-sub {opacity: 0.9; font-size: 0.9rem;}
        .insight-box {
            background: #f8fafc;
            border-left: 4px solid #2563eb;
            padding: 12px 14px;
            border-radius: 8px;
            margin: 4px 0 10px 0;
        }
        .section-title {font-size: 1.05rem; font-weight: 700; color: #111827; margin: 2px 0 8px 0;}
        .status-good {color: #027a48; font-weight: 700;}
        .status-bad {color: #b42318; font-weight: 700;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)


def metric_card(label: str, value: str, help_text: str = "") -> None:
    st.markdown(
        f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>",
        unsafe_allow_html=True,
    )
    if help_text:
        st.caption(help_text)


def insight_box(text: str) -> None:
    st.markdown(f"<div class='insight-box'>{text}</div>", unsafe_allow_html=True)


def status_badge(passed: bool, label: str) -> str:
    klass = "status-good" if passed else "status-bad"
    text = "PASS" if passed else "FAIL"
    return f"<span class='{klass}'>{label}: {text}</span>"


def styled_dataframe(df: pd.DataFrame, color_col: str | None = None) -> None:
    if color_col and color_col in df.columns:
        styled = df.style.background_gradient(subset=[color_col], cmap="Blues")
        st.dataframe(styled, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
