# frontend/theme.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Theme and style injection logic for the application."""
import streamlit as st

# A key to track if CSS has been injected in the current session
_THEME_CSS_KEY = "_theme_css_injected"

def set_theme(theme: str = "light") -> None:
    """Sets the active theme in the session state."""
    st.session_state["theme"] = theme
    # Force re-injection of styles when the theme is explicitly changed
    inject_global_styles(force=True)

def inject_global_styles(force: bool = False) -> None:
    """
    Injects the global CSS styles into the app.
    Includes an idempotent guard to prevent multiple injections per run.
    """
    # The Guard: if styles are already injected and we are not forcing a change, stop.
    if st.session_state.get(_THEME_CSS_KEY) and not force:
        return

    # Your existing CSS styles go here
    st.markdown("""
        <style>
            /* Add all your global CSS rules here */
            body {
                color: #333;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Mark that styles have been injected for this session run
    st.session_state = True

def initialize_theme(name: str = "light") -> None:
    """
    Public helper used by the main ui.py to set the initial theme.
    This ensures backward compatibility for any pages that might call it.
    """
    set_theme(name)
