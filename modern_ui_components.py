# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Reusable UI components with a modern aesthetic."""

from __future__ import annotations

import streamlit as st
from typing import Optional, Dict
from streamlit_helpers import safe_container

from modern_ui import inject_modern_styles

try:
    from streamlit_option_menu import option_menu
    USE_OPTION_MENU = True
except Exception:  # pragma: no cover - optional dependency
    option_menu = None  # type: ignore
    USE_OPTION_MENU = False

# Sidebar styling for a dark glass look with hover and active states
SIDEBAR_STYLES = """
<style>
.sidebar-nav {
    background: rgba(0, 0, 0, 0.35);
    border-radius: 12px;
    padding: 0.5rem;
    margin-bottom: 1rem;
}
.sidebar-nav .nav-item {
    color: #f0f4f8;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.25rem;
    transition: background 0.2s ease;
    display: flex;
    gap: 0.5rem;
    align-items: center;
}
.sidebar-nav .nav-item:hover {
    background: rgba(255, 255, 255, 0.05);
}
.sidebar-nav .nav-item.selected {
    background: rgba(255, 255, 255, 0.15);
}
@media (max-width: 768px) {
    .sidebar-nav {
        padding: 0.25rem;
    }
    .sidebar-nav .nav-item {
        padding: 0.75rem;
    }
}
</style>
"""


def render_modern_layout() -> None:
    """Apply global styles and base glassmorphism containers."""
    inject_modern_styles()
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
        .glass-card {
            background: rgba(255,255,255,0.3);
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.4);
            backdrop-filter: blur(14px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 1rem;
            margin-bottom: 1rem;
            transition: box-shadow 0.2s ease, transform 0.2s ease;
        }
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_modern_header(title: str) -> None:
    """Display a translucent header."""
    st.markdown(
        f"<div class='glass-card' style='text-align:center'>"
        f"<h2 style='margin:0'>{title}</h2>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_modern_sidebar(
    pages: Dict[str, str],
    container: Optional[st.delta_generator.DeltaGenerator] = None,
    icons: Optional[Dict[str, str]] = None,

) -> str:
    """Render a vertical navigation menu with optional icons."""
    if container is None:
        container = st.sidebar

    state = getattr(st, "session_state", {})
    if key not in state:
        state[key] = list(pages.keys())[0]

    opts = list(pages.keys())
    icon_map = icons or {}
    session_key = f"sidebar_{id(pages)}"
    st.session_state.setdefault(session_key, opts[0])

    container_ctx = safe_container(container)
    with container_ctx:
        st.markdown(SIDEBAR_STYLES, unsafe_allow_html=True)
        st.markdown("<div class='glass-card sidebar-nav'>", unsafe_allow_html=True)
    if USE_OPTION_MENU and option_menu is not None:
        choice = option_menu(
            menu_title=None,
            options=opts,
            icons=icons or ["dot"] * len(opts),
            orientation="vertical",
            key=key,
            default_index=opts.index(state.get(key, opts[0])),
        )
    else:
        choice = st.radio("Navigate", opts, key=key, index=opts.index(state.get(key, opts[0])))
    
    state[key] = choice
    st.markdown("</div>", unsafe_allow_html=True)
    return state[key]



def render_validation_card(entry: dict) -> None:
    """Display a single validation entry."""
    validator = entry.get("validator") or entry.get("validator_id", "N/A")
    target = entry.get("target", entry.get("subject", "N/A"))
    score = entry.get("score", "N/A")
    st.markdown(
        f"""
        <div class='glass-card'>
            <strong>{validator}</strong> → <em>{target}</em><br>
            <span>Score: {score}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats_section(stats: dict) -> None:
    """Show quick statistics in a styled block."""
    st.markdown(
        f"""
        <div class='glass-card'>
            <h4 style='margin-top:0'>Stats</h4>
            <div>Runs: {stats.get('runs', 0)}</div>
            <div>Proposals: {stats.get('proposals', 'N/A')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


__all__ = [
    "render_modern_layout",
    "render_modern_header",
    "render_modern_sidebar",
    "render_validation_card",
    "render_stats_section",
]
