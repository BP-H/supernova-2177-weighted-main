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


def apply_theme(theme: str) -> None:
    """Apply light or dark theme styles based on ``theme``."""
    if theme == "dark":
        css = """
            <style>
            body, .stApp { background-color: #1e1e1e; color: #f0f0f0; }
            </style>
        """
    else:
        css = """
            <style>
            body, .stApp { background-color: #ffffff; color: #000000; }
            </style>
        """
    st.markdown(css, unsafe_allow_html=True)


def inject_global_styles() -> None:
    """Inject custom CSS styling for containers and buttons."""
    st.markdown(
        """
        <style>
        .custom-container {
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 2px 4px rgba(0,0,0,0.4);
            margin-bottom: 1rem;
        }
        .stButton>button {border-radius:6px;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def theme_selector(label: str = "Theme") -> str:
    """Render a radio selector for the app theme and return the choice."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "light"
    choice = st.radio(
        label,
        ["Light", "Dark"],
        index=(1 if st.session_state["theme"] == "dark" else 0),
        horizontal=True,
    )
    st.session_state["theme"] = choice.lower()
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
