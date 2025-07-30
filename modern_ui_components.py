# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Reusable UI components with a modern aesthetic."""

from __future__ import annotations

import streamlit as st
from typing import Optional, Dict
from pathlib import Path
from uuid import uuid4
from streamlit_helpers import safe_container

from modern_ui import inject_modern_styles

try:
    from streamlit_option_menu import option_menu
    USE_OPTION_MENU = True
except Exception:  # pragma: no cover - optional dependency
    option_menu = None  # type: ignore
    USE_OPTION_MENU = False

# Sidebar styling for lightweight text-based navigation.
# Inject this CSS string with ``st.markdown`` to keep sidebar navigation
# consistent across pages.
SIDEBAR_STYLES = """
<style>
[data-testid="stSidebar"] {
    background: rgba(20, 25, 40, 0.9);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    transition: width 0.3s ease;
}
[data-testid="stSidebar"] .stButton>button {
    width: 100%;
}
.sidebar-nav {
    display: flex;
    flex-direction: column;
    padding: 0;
    margin-bottom: 1rem;
    font-size: 0.75rem;
}
.sidebar-nav.horizontal {
    flex-direction: row;
    align-items: center;
}
.sidebar-nav .stButton>button {
    background: none;
    border: none;
    color: #f0f4f8;
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
    font-weight: 500;
    white-space: nowrap;
    border-radius: 8px;
    margin-bottom: 0.25rem;
    transition: background 0.2s ease;
    display: flex;
    gap: 0.5rem;
    align-items: center;
}
.sidebar-nav .stButton>button:hover {
    background: rgba(255, 255, 255, 0.05);
}
.sidebar-nav label {
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.25rem;
    transition: background 0.2s;
}
.sidebar-nav label:hover {
    background: rgba(255, 255, 255, 0.05);
}
.sidebar-nav input:checked + div {
    color: var(--neon-accent);
}
.sidebar-nav .nav-item {
    padding: 0.5rem 1rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: background 0.2s;
}
.sidebar-nav .nav-item:hover {
    background: rgba(255, 255, 255, 0.05);
}
.sidebar-nav .nav-item.active {
    background: rgba(255, 255, 255, 0.1);
    color: var(--neon-accent);
}
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        width: 14rem;
    }
}
@media (max-width: 600px) {
    .sidebar-nav.horizontal {
        flex-direction: column;
        align-items: stretch;
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
    *,
    session_key: str = "sidebar_nav",
    horizontal: bool = False,
) -> str:
    """Render navigation links styled as modern text tabs.

    ``session_key`` determines where the active page is stored in
    ``st.session_state`` so multiple sidebars can coexist without collisions.
    """
    if container is None:
        container = st.sidebar

    # Validate that referenced page files exist before rendering navigation
    page_dir_candidates = [
        Path.cwd() / "pages",
        Path(__file__).resolve().parent / "pages",
        Path(__file__).resolve().parent / "transcendental_resonance_frontend" / "pages",
    ]

    valid_pages: Dict[str, str] = {}
    for label, page_ref in pages.items():
        slug = str(page_ref).strip("/").split("?")[0].rsplit(".", 1)[-1]
        exists = any((d / f"{slug}.py").exists() for d in page_dir_candidates if d.exists())
        if exists:
            valid_pages[label] = page_ref
        else:
            st.warning(f"Page file missing for '{label}' -> {page_ref}", icon="⚠️")

    if not valid_pages:
        st.error("No valid pages available", icon="⚠️")
        return ""

    pages = valid_pages
    opts = list(pages.keys())
    icon_map = icons or {}

    # Default session state for selected page
    st.session_state.setdefault(session_key, opts[0])
    if st.session_state.get(session_key) not in opts:
        st.session_state[session_key] = opts[0]

    widget_key = f"{session_key}_ctrl"

    orientation_cls = "horizontal" if horizontal else "vertical"

    container_ctx = safe_container(container)
    with container_ctx:
        st.markdown(SIDEBAR_STYLES, unsafe_allow_html=True)
        st.markdown(
            f"<div class='glass-card sidebar-nav {orientation_cls}'>",
            unsafe_allow_html=True,
        )

        try:
            if USE_OPTION_MENU and option_menu is not None:
                choice = option_menu(
                    menu_title=None,
                    options=opts,
                    icons=[icon_map.get(o, "dot") for o in opts],
                    orientation="horizontal" if horizontal else "vertical",
                    key=widget_key,
                    default_index=opts.index(st.session_state.get(session_key, opts[0])),
                )
            elif horizontal:
                # Render as horizontal buttons
                columns = container.columns(len(opts))
                for col, label in zip(columns, opts):
                    disp = f"{icon_map.get(label, '')} {label}".strip()
                    if col.button(disp, key=f"{widget_key}_{label}"):
                        st.session_state[session_key] = label
                choice = st.session_state[session_key]
            else:
                # Vertical fallback (radio or buttons)
                choice_disp = st.radio(
                    "Navigate",
                    [f"{icon_map.get(o, '')} {o}".strip() for o in opts],
                    key=widget_key,
                    index=opts.index(st.session_state.get(session_key, opts[0])),
                )
                choice = opts[
                    [f"{icon_map.get(o, '')} {o}".strip() for o in opts].index(choice_disp)
                ]

        except Exception:
            # Final fallback
            choice = st.session_state.get(session_key, opts[0])

        if st.session_state.get(session_key) != choice:
            st.session_state[session_key] = choice

        st.markdown("</div>", unsafe_allow_html=True)
        return choice


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
    "SIDEBAR_STYLES",
    "render_modern_layout",
    "render_modern_header",
    "render_modern_sidebar",
    "render_validation_card",
    "render_stats_section",
]
