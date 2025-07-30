"""# UI Layout Helpers

Reusable containers and navigation components for Streamlit pages.

## Features

- `main_container()` – return a generic container for page content
- `sidebar_container()` – access the sidebar container
- `render_navbar(options, default=None)` – simple radio navigation
- `render_title_bar(icon, label)` – header with icon

These helpers keep the UI consistent and make it easier to experiment with
different layouts.
"""

from __future__ import annotations

import streamlit as st
from typing import Iterable, Optional


def main_container() -> st.delta_generator.DeltaGenerator:
    """Return a container for the main content area."""
    return st.container()


def sidebar_container() -> st.delta_generator.DeltaGenerator:
    """Return the sidebar container."""
    return st.sidebar


def render_navbar(options: Iterable[str], default: Optional[str] = None) -> str:
    """Render a navigation radio and return the selected label."""
    opts = list(options)
    index = 0
    if default is not None and default in opts:
        index = opts.index(default)
    return st.radio("Navigation", opts, index=index)


def render_title_bar(icon: str, label: str) -> None:
    """Display a simple title header with icon."""
    st.markdown(
        f"<h1 style='display:flex;align-items:center;'>"
        f"<span style='margin-right:0.5rem'>{icon}</span>{label}</h1>",
        unsafe_allow_html=True,
    )


def show_preview_badge(text: str = "\ud83d\udea7 Preview Mode") -> None:
    """Overlay a badge used when a fallback page is shown."""
    st.markdown(
        f"<div style='position:fixed;top:1rem;right:1rem;"
        f"background:#ffc107;color:#000;padding:0.25rem 0.5rem;"
        f"border-radius:4px;z-index:1000;'>{text}</div>",
        unsafe_allow_html=True,
    )


__all__ = [
    "main_container",
    "sidebar_container",
    "render_navbar",
    "render_title_bar",
    "show_preview_badge",
]
