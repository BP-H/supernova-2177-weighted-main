"""Simple light theme CSS injection for Streamlit."""

import streamlit as st

CSS = """
<style>
body, .stApp {
    background: white;
    font-family: Helvetica, Arial, sans-serif;
}
button, .stButton>button {
    border-radius: 8px;
}
</style>
"""


def inject_light_theme() -> None:
    """Inject the basic light theme CSS if not already added."""
    if st.session_state.get("_light_theme_injected"):
        return
    st.markdown(CSS, unsafe_allow_html=True)
    st.session_state["_light_theme_injected"] = True
