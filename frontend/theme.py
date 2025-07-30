# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Minimal theme helpers for Streamlit apps."""

from __future__ import annotations

import streamlit as st


def get_global_css(dark: bool) -> str:
    """Return CSS defining global theme variables."""
    if dark:
        bg = "#001E26"
        card = "#002B36"
        accent = "#00F0FF"
        muted = "#6c757d"
    else:
        bg = "#F0F2F6"
        card = "#FFFFFF"
        accent = "#0A84FF"
        muted = "#6c757d"

    return (
        "<style>"
        " :root {"
        f" --bg: {bg};"
        f" --card: {card};"
        f" --accent: {accent};"
        f" --text-muted: {muted};"
        " }"
        "</style>"
    )


def inject_modern_styles(dark: bool = True) -> None:
    """Inject the base CSS variables for the modern theme."""
    if st.session_state.get("_theme_injected"):
        return
    st.markdown(get_global_css(dark), unsafe_allow_html=True)
    st.session_state["_theme_injected"] = True
