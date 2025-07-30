# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Streamlit UI helper utilities.

This module provides small helpers used across the Streamlit
applications to keep the UI code concise and consistent.
"""

from __future__ import annotations

import html
from typing import Literal

import streamlit as st
from modern_ui import inject_premium_styles


def alert(
    message: str,
    level: Literal["warning", "error", "info"] = "info",
    *,
    show_icon: bool = True,
) -> None:
    """Display a minimally intrusive alert box."""
    icons = {"warning": "\u26A0", "error": "\u274C", "info": "\u2139"}
    colors = {
        "warning": ("#fff7e6", "#f0ad4e"),
        "error": ("#fdecea", "#f44336"),
        "info": ("#e8f4fd", "#1e88e5"),
    }
    bg_color, border_color = colors.get(level, colors["info"])
    icon_html = f"<span class='icon'>{icons.get(level, '')}</span>" if show_icon else ""
    st.markdown(
        f"<div class='custom-alert' style='border-left:4px solid {border_color};"
        f"background-color:{bg_color};padding:0.5em;border-radius:4px;"
        f"margin-bottom:1em;display:flex;align-items:center;gap:0.5rem;'>"
        f"{icon_html}{html.escape(message)}</div>",
        unsafe_allow_html=True,
    )


def header(title: str, *, layout: str = "centered") -> None:
    """Render a standard page header and apply base styling."""
    st.markdown(
        "<style>.app-container{padding:1rem 2rem;}" "</style>",
        unsafe_allow_html=True,
    )
    st.header(title)


def safe_apply_theme(theme: str) -> None:
    """Apply theme with error handling."""
    try:
        # Note: @import url for fonts is handled by apply_global_styles
        # This function defines the CSS variables and app-wide styles.
        if theme.lower() == "dark":
            css = """
                <style>
                :root {
                    --background: #181818;
                    --secondary-bg: #242424;
                    --text-color: #e8e6e3;
                    --primary-color: #4a90e2;
                    --font-family: monospace; /* Consistent with main branch's dark theme */
                }
                .stApp {
                    background-color: var(--background);
                    color: var(--text-color);
                    font-family: var(--font-family);
                }
                a { color: var(--primary-color); } /* Explicitly include link color for consistency */
                </style>
            """
        elif theme.lower() == "codex":
            css = """
                <style>
                :root {
                    --background: #202123;
                    --secondary-bg: #343541;
                    --text-color: #ECECF1;
                    --primary-color: #19C37D;
                    --font-family: 'Iosevka', monospace; /* Specific font for codex theme */
                }
                .stApp {
                    background-color: var(--background);
                    color: var(--text-color);
                    font-family: var(--font-family);
                }
                a { color: var(--primary-color); } /* Explicitly include link color for consistency */
                </style>
            """
        else: # Default light theme
            css = """
                <style>
                :root {
                    --background: #F0F2F6;
                    --secondary-bg: #FFFFFF;
                    --text-color: #333333;
                    --primary-color: #0A84FF;
                    --font-family: 'Inter', sans-serif; /* Consistent with apply_global_styles' default */
                }
                .stApp {
                    background-color: var(--background);
                    color: var(--text-color);
                    font-family: var(--font-family);
                }
                a { color: var(--primary-color); } /* Explicitly include link color for consistency */
                </style>
            """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Theme application failed: {e}")


def apply_theme(theme: str) -> None:
    """Apply theme with fallback."""
    safe_apply_theme(theme)


def inject_global_styles() -> None:
    """Deprecated wrapper that forwards to :func:`modern_ui.inject_premium_styles`."""
    inject_premium_styles()


def theme_selector(label: str = "Theme", *, key_suffix: str | None = None) -> str:
    """Select and apply a theme."""

    if key_suffix is None:
        key_suffix = "default"

    if "theme" not in st.session_state:
        st.session_state["theme"] = "light"

    unique_key = f"theme_selector_{key_suffix}_{id(st)}"

    try:
        current_theme = st.session_state.get("theme", "light")
        theme_choice = st.selectbox(
            label,
            ["Light", "Dark"],
            index=0 if current_theme == "light" else 1,
            key=unique_key,
        )

        st.session_state["theme"] = theme_choice.lower()
        apply_theme(st.session_state["theme"])
        return st.session_state["theme"]
    except Exception as e:
        st.warning(f"Theme selector error: {e}")
        return st.session_state.get("theme", "light")


def centered_container(max_width: str = "900px") -> "st.delta_generator.DeltaGenerator":
    """Return a container with standardized width constraints."""
    st.markdown(
        f"<style>.main .block-container{{max-width:{max_width};margin:auto;}}</style>",
        unsafe_allow_html=True,
    )
    return st.container()


__all__ = [
    "alert",
    "header",
    "apply_theme",
    "theme_selector",
    "centered_container",
    "inject_global_styles",
]
