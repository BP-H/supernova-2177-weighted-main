"""Entry point for the Validation page used by Streamlit multipage."""

from transcendental_resonance_frontend.pages.validation import main

try:
    from modern_ui_components import SIDEBAR_STYLES
except Exception:  # pragma: no cover - optional styling
    SIDEBAR_STYLES = ""

# optional: custom sidebar styles if you define SIDEBAR_STYLES globally
try:
    import streamlit as st
    st.markdown(f"<style>{SIDEBAR_STYLES}</style>", unsafe_allow_html=True)
except NameError:
    pass  # no sidebar styling defined yet

from transcendental_resonance_frontend.pages.validation import main

if __name__ == "__main__":  # pragma: no cover - executed by Streamlit
    main()


