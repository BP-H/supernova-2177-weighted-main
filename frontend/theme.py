# frontend/theme.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Theme management for superNova_2177."""

import streamlit as st

_THEME_CSS_KEY = "_theme_css_injected"

def set_theme(theme: str):
    """Sets the app theme."""
    # Your existing theme logic here, e.g., custom CSS based on theme
    if theme == "dark":
        st.markdown("<style>body { background-color: #333; color: white; }</style>", unsafe_allow_html=True)
    else:
        st.markdown("<style>body { background-color: white; color: black; }</style>", unsafe_allow_html=True)

def inject_global_styles(force: bool = False) -> None:
    """Injects global CSS with guard to prevent duplicates."""
    if st.session_state.get(_THEME_CSS_KEY) and not force:
        return  # Already injected
    # Your existing global styles here, e.g.:
    st.markdown("""
        <style>
            .stApp { font-family: Arial, sans-serif; }
            /* Add more global styles */
        </style>
    """, unsafe_allow_html=True)
    st.session_state[_THEME_CSS_KEY] = True

def initialize_theme(name: str = "light") -> None:
    """Public helper to initialize theme safely."""
    set_theme(name)
    inject_global_styles(force=True)  # Force if needed for changes
