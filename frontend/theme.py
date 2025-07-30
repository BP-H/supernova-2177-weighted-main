# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Color theme utilities for Streamlit frontend."""

from __future__ import annotations

import streamlit as st

ACCENT_COLOR = "#00F0FF"  # Default fallback accent


def get_accent_color() -> str:
    """Return the current theme accent color."""
    return ACCENT_COLOR


def get_global_css(dark: bool) -> str:
    """Return ``:root`` CSS variables for dark or light mode."""
    if dark:
        bg = "#001E26"
        card = "#002B36"
        accent = "#00F0FF"
        muted = "#7e9aaa"
    else:
        bg = "#F0F2F6"
        card = "#FFFFFF"
        accent = "#0A84FF"
        muted = "#666666"

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

