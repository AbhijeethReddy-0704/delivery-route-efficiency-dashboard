from __future__ import annotations

import streamlit as st


def section_intro(text: str) -> None:
    st.caption(text)


def metric_row(items: list[tuple[str, str]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)


def status_card(label: str, passed: bool, detail: str) -> None:
    icon = "PASS" if passed else "FAIL"
    color = "green" if passed else "red"
    st.markdown(f"**{label}**")
    st.markdown(f":{color}[{icon}] - {detail}")
