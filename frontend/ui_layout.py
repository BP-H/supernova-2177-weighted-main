"""Shared layout helpers for Streamlit-based frontends."""

from __future__ import annotations

import streamlit as st
from typing import Iterable, Optional

# Reusable container factories

def main_container() -> st.delta_generator.DeltaGenerator:
    """Return a new main content container."""
    return st.container()


def sidebar_container() -> st.delta_generator.DeltaGenerator:
    """Return the sidebar container."""
    return st.sidebar


def render_title_bar(icon: str, label: str) -> None:
    """Render a simple title bar with an icon."""
    st.markdown(f"### {icon} {label}")


def render_navbar(options: Iterable[str], *, icons: Optional[Iterable[str]] = None, key: str = "navbar") -> str:
    """Render a sidebar navigation menu and return the selected label."""
    opts = list(options)
    if icons and len(list(icons)) == len(opts):
        icon_list = list(icons)
        labels = [f"{icon_list[i]} {opts[i]}" for i in range(len(opts))]
        choice = st.sidebar.radio("Navigate", labels, key=key)
        return opts[labels.index(choice)]
    return st.sidebar.radio("Navigate", opts, key=key)


def overlay_badge(text: str = "Preview Mode") -> None:
    """Display a fixed badge in the top right corner of the page."""
    st.markdown(
        f"""
        <div style='position:fixed;top:0.5rem;right:0.5rem;background:#f0ad4e;
             color:#fff;padding:0.25rem 0.5rem;border-radius:4px;font-size:0.75rem;
             z-index:1000;'>
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


"""\
## UI Ideas

- Glassmorphism cards for data panels
- Sidebar navigation with emoji icons
- Animated progress bars for background tasks
- Reaction badges for interactive elements
"""
