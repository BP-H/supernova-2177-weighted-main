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
    """Render horizontal navigation links using ``st.page_link`` and return the
    selected label.

    Parameters
    ----------
    page_links:
        Mapping or iterable of label-to-target page links.
    icons:
        Optional iterable of emoji or icon names for each label.
    key:
        Session state key used to track the currently selected page. If omitted,
        a unique key is generated using :func:`uuid4`.
    default:
        The label selected initially when the navbar is first rendered.
    """
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
        if hasattr(sidebar, "page_link"):
            sidebar.markdown(
                "<style>.nav-links a{margin-right:0.5rem;}</style>",
                unsafe_allow_html=True,
            )
            with sidebar.container():
                sidebar.markdown("<div class='nav-links'>", unsafe_allow_html=True)
                for (label, target), icon in zip(opts, icon_list):
                    sidebar.page_link(target, label=label, icon=icon)
                sidebar.markdown("</div>", unsafe_allow_html=True)
            sidebar.divider()

        # Fallback to horizontal columns if sidebar fails or for main area display
        if not st.session_state.get(key, None):
            st.session_state[key] = default or opts[0][0]  # Initialize with default or first option
        cols = st.columns(len(opts))
        for col, ((label, target), icon) in zip(cols, zip(opts, icon_list)):
            with col:
                if st.button(label, key=f"{key}_{label}", help=target):
                    st.session_state[key] = label
        return st.session_state.get(key, opts[0][0])  # Return current selection

    except Exception as e:
        st.warning(f"Navigation setup failed: {e}. Falling back to radio.")
        if USE_OPTION_MENU:
            icon_list = list(icons or ["dot"] * len(opts))
            return option_menu(
                menu_title=None,
                options=[label for label, _ in opts],
                icons=icon_list,
                orientation="horizontal",
                key=key,
                default_index=index,
            )
        else:
            labels = [f"{icon} {label}" if icon else label for label, _ in opts for icon in icon_list[:len(opts)]]
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
