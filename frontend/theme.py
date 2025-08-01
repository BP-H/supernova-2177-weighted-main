# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Color theme utilities for Streamlit frontend."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class ColorTheme:
    """Simple container for theme colors."""

    bg: str
    card: str
    accent: str
    text_muted: str

    def css_vars(self) -> str:
        """Return CSS variable declarations for this theme."""
        return (
            f"--bg: {self.bg};\n"
            f"    --card: {self.card};\n"
            f"    --accent: {self.accent};\n"
            f"    --text-muted: {self.text_muted};"
        )


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

THEMES = {"light": LIGHT_THEME, "dark": DARK_THEME}


def get_theme(name: bool | str = True) -> ColorTheme:
    """Return the selected :class:`ColorTheme` by name or boolean flag."""

    if isinstance(name, str):
        return THEMES.get(name.lower(), LIGHT_THEME)
    return DARK_THEME if name else LIGHT_THEME


def get_global_css(theme: bool | str = True) -> str:
    """Return ``:root`` CSS variables for the selected theme."""

    cfg = get_theme(theme)
    return (
        "<style>\n:root {\n    "
        + cfg.css_vars()
        + "\n}\n</style>"
    )


def apply_theme(name: str) -> None:
    """Apply the selected theme by injecting global CSS variables."""

    st.markdown(get_global_css(name), unsafe_allow_html=True)
    st.session_state["theme"] = name


def inject_modern_styles(theme: bool | str = True) -> None:
    """Inject global CSS variables and basic card styles."""

    if st.session_state.get("_theme_injected"):
        return

    apply_theme("dark" if theme is True else theme)

    css = """
    <style>
    @keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
    .glass-card,
    .insta-card,
    .card {
        border-radius: 1rem;
        animation: fade-in 0.3s ease forwards;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.session_state["_theme_injected"] = True


def get_accent_color() -> str:
    """Return the accent color for the current theme."""

    return get_theme(True).accent

