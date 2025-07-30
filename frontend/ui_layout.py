"""Reusable Streamlit layout helpers.

This module centralizes small layout utilities and container factories used
across pages. The functions are intentionally lightweight so other modules can
import them without heavy dependencies.

# UI ideas
- glassy navbar with icons
- title bar with emoji label
- preview badge overlay for unfinished pages
"""

from __future__ import annotations

import inspect
from typing import Dict, Iterable

import streamlit as st
from streamlit_option_menu import option_menu

# Basic containers reused across the UI
main_container = st.container()
sidebar_container = st.sidebar


def render_navbar(pages: Dict[str, str], *, icons: Iterable[str] | None = None) -> str:
    """Render a simple horizontal nav bar and return the selected label."""
    opts = list(pages.keys())
    icons = list(icons or ["dot"] * len(opts))
    return option_menu(
        menu_title=None,
        options=opts,
        icons=icons,
        orientation="horizontal",
        key="main_nav_menu",
    )


def render_title_bar(icon: str, label: str) -> None:
    """Display a stylised page title."""
    st.markdown(f"## {icon} {label}")


def render_preview_badge(text: str = "Preview Mode") -> None:
    """Overlay a badge indicating a stub page."""
    st.markdown(
        f"<div style='position:fixed; top:1rem; right:1rem; background:#e0a800; color:#fff; padding:0.25rem 0.75rem; border-radius:6px; z-index:1000;'> {text} </div>",
        unsafe_allow_html=True,
    )
