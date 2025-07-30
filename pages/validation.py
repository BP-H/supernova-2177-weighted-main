"""Streamlit entry point for the Validation page."""

import streamlit as st
from transcendental_resonance_frontend.pages.validation import main as _frontend_main

# Optional: custom sidebar styles
try:
    from modern_ui_components import SIDEBAR_STYLES
    st.markdown(f"<style>{SIDEBAR_STYLES}</style>", unsafe_allow_html=True)
except Exception:
    pass  # no sidebar styling defined

def render() -> None:
    """Render the validation dashboard."""
    _frontend_main()

if __name__ == "__main__":  # pragma: no cover - manual execution
    render()

