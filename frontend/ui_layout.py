"""UI Layout Helpers

Reusable Streamlit layout helpers and navigation components for pages.

These functions are lightweight and centralized for easy reuse across modules
without introducing heavy dependencies.

Features:
- `main_container()` – returns a generic container for page content
- `sidebar_container()` – accesses the sidebar container
- `render_navbar(pages)` – horizontal page links UI
- `render_title_bar(icon, label)` – renders a header with an icon

UI Ideas:
- Glassy navbar with icons
- Title bar with emoji label
- Preview badge overlay for unfinished pages
"""

from __future__ import annotations

from typing import Dict, Iterable, Optional
from uuid import uuid4
import streamlit as st

try:
    from streamlit_option_menu import option_menu
    USE_OPTION_MENU = True
except ImportError:
    USE_OPTION_MENU = False


def main_container() -> st.delta_generator.DeltaGenerator:
    """Return a container for the main content area."""
    return st.container()



def sidebar_container() -> st.delta_generator.DeltaGenerator:
    """Return the sidebar container."""
    return st.sidebar


def render_navbar(
    page_links: Iterable[str] | Dict[str, str],
    icons: Optional[Iterable[str]] = None,
    key: Optional[str] = None,
    default: Optional[str] = None,
) -> str:
    """Render a vertical sidebar navigation and return the selected label."""

    opts = (
        list(page_links.items()) if isinstance(page_links, dict) else [(str(o), str(o)) for o in page_links]
    )
    icon_list = list(icons or [None] * len(opts))
    key = key or uuid4().hex

    index = 0
    if default is not None and default in [label for label, _ in opts]:
        index = [label for label, _ in opts].index(default)

    try:
        sidebar = st.sidebar
        labels = [f"{icon or ''} {label}".strip() for (label, _), icon in zip(opts, icon_list)]
        with sidebar.container():
            sidebar.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
            choice = sidebar.radio("", labels, index=index, key=key)
            sidebar.markdown('</div>', unsafe_allow_html=True)
        return opts[labels.index(choice)][0]

    except Exception as e:
        st.toast(f"Navigation setup failed: {e}. Falling back to radio.", icon="⚠️")

        try:
            if USE_OPTION_MENU and option_menu is not None:
                icon_list = list(icons or ["dot"] * len(opts))
                return option_menu(
                    menu_title=None,
                    options=[label for label, _ in opts],
                    icons=icon_list,
                    orientation="horizontal",
                    key=key,
                    default_index=index,
                )
        except Exception:
            pass  # silently fallback if option_menu fails unexpectedly

        # Final fallback: plain radio with or without icons
        labels = [
            f"{icon} {label}" if icons else label
            for (label, _), icon in zip(opts, icons or [""] * len(opts))
        ]
        choice = st.sidebar.radio("Navigate", labels, key=key, index=index)
        return [label for label, _ in opts][labels.index(choice)] if icons else choice


def render_title_bar(icon: str, label: str) -> None:
    """Display a stylized page title with icon."""
    st.markdown(
        f"<h1 style='display:flex;align-items:center;'>"
        f"<span style='margin-right:0.5rem'>{icon}</span>{label}</h1>",
        unsafe_allow_html=True,
    )


def show_preview_badge(text: str = "🚧 Preview Mode") -> None:
    """Overlay a badge used when a fallback or WIP page is shown."""
    st.markdown(
        f"<div style='position:fixed; top:1rem; right:1rem; background:#ffc107; "
        f"color:#000; padding:0.25rem 0.5rem; border-radius:4px; z-index:1000;'>"
        f"{text}</div>",
        unsafe_allow_html=True,
    )


"""\
## UI Ideas

- Glassmorphism cards for data panels
- Sidebar navigation with emoji icons
- Animated progress bars for background tasks
- Reaction badges for interactive elements
"""

__all__ = [
    "main_container",
    "sidebar_container",
    "render_navbar",
    "render_title_bar",
    "show_preview_badge",
]
