# frontend/theme.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Theme management for superNova_2177."""

import streamlit as st

_THEME_CSS_KEY = "_theme_css_injected"

def set_theme(theme: str):
    """Applies a basic light or dark theme background."""
    if theme == "dark":
        st.markdown("<style>body { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
    else:
        st.markdown("<style>body { background-color: #FFFFFF; color: black; }</style>", unsafe_allow_html=True)

def inject_global_styles(force: bool = False) -> None:
    """Injects global CSS. Uses a session state flag to run only once."""
    if st.session_state.get(_THEME_CSS_KEY) and not force:
        return
    st.markdown("""
        <style>
            .stApp { font-family: Arial, sans-serif; }
            /* Add other global styles here */
        </style>
    """, unsafe_allow_html=True)
    st.session_state[_THEME_CSS_KEY] = True

def initialize_theme(name: str = "light") -> None:
    """The main function to set up the theme and styles."""
    st.session_state.setdefault("theme", name)
    set_theme(st.session_state["theme"])
    inject_global_styles(force=True)

# --- Aliases for Backward Compatibility ---
# These aliases will resolve all the ImportError issues from your logs.

def apply_theme(name: str = "light") -> None:
    """Alias for initialize_theme. Fixes import errors in legacy pages."""
    initialize_theme(name)

def inject_modern_styles(force: bool = False) -> None:
    """Alias for inject_global_styles. Fixes import errors in modern_ui.py."""
    inject_global_styles(force)
