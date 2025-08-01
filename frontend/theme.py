# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Color theme utilities for Streamlit frontend."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class ColorTheme:
    """Simple container for theme colors and common tokens."""

    bg: str
    card: str
    accent: str
    text_muted: str
    radius: str = "0.5rem"
    transition: str = "0.3s ease"


LIGHT_THEME = ColorTheme(
    bg="#F0F2F6",
    card="#FFFFFF",
    accent="#0A84FF",
    text_muted="#666666",
)

DARK_THEME = ColorTheme(
    bg="#001E26",
    card="#002B36",
    accent="#00F0FF",
    text_muted="#7e9aaa",
)


def get_theme(dark: bool = True) -> ColorTheme:
    """Return the dark or light :class:`ColorTheme`."""

    return DARK_THEME if dark else LIGHT_THEME


def get_global_css(dark: bool = True) -> str:
    """Return ``:root`` CSS variables for the selected theme."""

    theme = get_theme(dark)
    return f"""
<style>
:root {{
    --bg: {theme.bg};
    --card: {theme.card};
    --accent: {theme.accent};
    --text-muted: {theme.text_muted};
    --radius: {theme.radius};
    --transition: {theme.transition};
}}

.fade-in {{
    opacity: 0;
    animation: fade-in var(--transition) forwards;
}}

.rounded {{
    border-radius: var(--radius);
}}

@keyframes fade-in {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}
</style>
"""


def inject_modern_styles(dark: bool = True) -> None:
    """Inject the base CSS variables for the modern theme."""

    if st.session_state.get("_theme_injected"):
        return
    st.markdown(get_global_css(dark), unsafe_allow_html=True)
    st.session_state["_theme_injected"] = True


def get_accent_color() -> str:
    """Return the accent color for the current theme."""

    return get_theme(True).accent

