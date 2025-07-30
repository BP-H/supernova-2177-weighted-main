# pages/validation.py

import time
import streamlit as st


def render() -> None:
    """Simple validation page used during tests."""
    try:
        st.markdown(f"<style>{SIDEBAR_STYLES}</style>", unsafe_allow_html=True)
    except NameError:  # pragma: no cover - style constant not defined
        pass

    st.title("🔍 Validation Dashboard")

    # simulate a short loading delay if needed
    time.sleep(0.1)

    st.info("Validation page loaded successfully.")


if __name__ == "__main__":  # pragma: no cover - manual execution
    render()
