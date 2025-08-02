# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Theme helpers and safe CSS injection for Streamlit pages."""

from __future__ import annotations
from typing import Literal
import streamlit as st

# Define your theme colors
LIGHT_THEME = {
    "bg": "#FFFFFF",
    "text": "#000000",
    "text-muted": "#555555",
    "card": "#F0F2F6",
    "accent": "#0077B5",
}
DARK_THEME = {
    "bg": "#0E1117",
    "text": "#FFFFFF",
    "text-muted": "#AAAAAA",
    "card": "#161B22",
    "accent": "#3498DB",
}
THEMES = {"light": LIGHT_THEME, "dark": DARK_THEME}


def _get_active_theme() -> dict[str, str]:
    """Gets the currently selected theme from session state."""
    name = st.session_state.get("_theme_name", "light")
    return THEMES.get(name, LIGHT_THEME)


def set_theme(name: Literal["light", "dark"] | str) -> None:
    """Sets the theme name in the session state."""
    if name not in THEMES:
        name = "light"
    st.session_state["_theme_name"] = name


def apply_theme(name: Literal["light", "dark"] | str = "light") -> None:
    """Applies the selected theme and injects the necessary CSS."""
    set_theme(name)
    inject_global_styles(once=False) # Re-inject styles when theme changes


def get_accent_color() -> str:
    """Returns the accent color of the current theme."""
    return _get_active_theme().get("accent", "#0077B5")


def inject_global_styles(*, once: bool = True) -> None:
    """Injects CSS variables and base styles into the app."""
    if once and st.session_state.get("_theme_css_injected"):
        return

    theme_colors = _get_active_theme()

    # This CSS block is now correctly encapsulated in a multi-line string
    css = f"""
    <style>
        :root {{
            --bg: {theme_colors['bg']};
            --text: {theme_colors['text']};
            --text-muted: {theme_colors['text-muted']};
            --card: {theme_colors['card']};
            --accent: {theme_colors['accent']};
            --transition: 0.4s ease; /* The line that caused the error is now safe */
        }}

        .stButton > button {{
            transition: background var(--transition);
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.session_state["_theme_css_injected"] = True


def inject_modern_styles() -> None:
    """Backward-compatibility alias."""
    inject_global_styles(once=True)
