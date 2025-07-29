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
        if theme == "dark":
            css = """
                <style>
                :root {
                    --bg-color: #0a0a0a;
                    --text-color: #ffffff;
                    --accent-color: #00D2FF;
                }
                .stApp {
                    background-color: var(--bg-color);
                    color: var(--text-color);
                }
                </style>
            """
        else:
            css = """
                <style>
                :root {
                    --bg-color: #ffffff;
                    --text-color: #000000;
                    --accent-color: #0A84FF;
                }
                .stApp {
                    background-color: var(--bg-color);
                    color: var(--text-color);
                }
                </style>
            """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Theme application failed: {e}")


def apply_theme(theme: str) -> None:
    """Apply theme with fallback."""
    safe_apply_theme(theme)


def inject_global_styles() -> None:
    """Inject custom CSS styling for containers, cards and buttons."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body, .stApp {
            background-color: var(--background, #F0F2F6);
            color: var(--text-color, #333333);
            font-family: var(--font-family, 'Inter', sans-serif);
        }
        .custom-container {
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(0,0,0,0.05);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            background-color: var(--secondary-bg, #FFFFFF);
        }
        .card {
            background-color: var(--secondary-bg, #FFFFFF);
            padding: 1rem;
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .stButton>button {
            border-radius: 6px;
            background: linear-gradient(90deg, var(--primary-color, #0A84FF), #2F70FF);
            color: var(--text-color, #FFFFFF);
            transition: filter 0.2s ease-in-out;
        }
        .stButton>button:hover {
            filter: brightness(1.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def theme_selector(label: str = "Theme") -> str:
    """Modern theme selector with visual toggle."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"

    col1, col2 = st.columns([4, 1])
    with col2:
        current_theme = st.session_state.get("theme", "dark")

        theme_choice = st.selectbox(
            "Theme",
            ["Light", "Dark"],
            index=1 if current_theme == "dark" else 0,
            key="theme_select",
        )

        st.session_state["theme"] = theme_choice.lower()

    apply_theme(st.session_state["theme"])
    return st.session_state["theme"]


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
