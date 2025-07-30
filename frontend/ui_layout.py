"""UI Layout Helpers

Reusable Streamlit layout helpers and navigation components for pages.

These functions are lightweight and centralized for easy reuse across modules
without introducing heavy dependencies.

Features:
- `main_container()` – returns a generic container for page content
- `sidebar_container()` – accesses the sidebar container
- `render_sidebar_nav(pages)` – vertical sidebar navigation
- `render_title_bar(icon, label)` – renders a header with an icon

UI Ideas:
- Glassy navbar with icons
- Title bar with emoji label
- Preview badge overlay for unfinished pages
"""

from __future__ import annotations

from typing import Dict, Iterable, Optional
from uuid import uuid4
import os
import streamlit as st
from modern_ui_components import SIDEBAR_STYLES

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


def render_profile_card(username: str, avatar_url: str) -> None:
    """Render a compact profile card with an environment badge."""
    env = os.getenv("APP_ENV", "development").lower()
    badge = "🚀 Production" if env.startswith("prod") else "🧪 Development"
    st.markdown(
        f"""
        <div class='glass-card' style='display:flex;align-items:center;gap:0.5rem;'>
            <img src="{avatar_url}" alt="avatar" width="48" style="border-radius:50%;" />
            <div>
                <strong>{username}</strong><br/>
                <span style='font-size:0.85rem'>{badge}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_sidebar_nav(
    page_links: Iterable[str] | Dict[str, str],
    icons: Optional[Iterable[str]] = None,
    key: Optional[str] = None,
    default: Optional[str] = None,
    session_key: str = "active_page",
) -> str:
    """Render a vertical sidebar navigation and return the selected label.

    The selected page label is also stored in ``st.session_state`` using
    ``session_key`` so other components can react to the active page.
    """
    opts = list(page_links.items()) if isinstance(page_links, dict) else [
        (str(o), str(o)) for o in page_links
    ]
    icon_list = list(icons or [None] * len(opts))
    key = key or uuid4().hex

    active = st.session_state.get(session_key, default or opts[0][0])
    if active not in [label for label, _ in opts]:
        active = opts[0][0]
    index = [label for label, _ in opts].index(active)

    choice = active
    container = st.sidebar.container()
    with container:
        st.markdown(SIDEBAR_STYLES, unsafe_allow_html=True)
        st.markdown("<div class='glass-card sidebar-nav'>", unsafe_allow_html=True)
        if hasattr(st.sidebar, "page_link"):
            for (label, path), icon in zip(opts, icon_list):
                try:
                    st.sidebar.page_link(path, label=label, icon=icon, help=label)
                except Exception:
                    url = f"?page={label}"
                    st.sidebar.link_button(label, url=url, icon=icon)
        elif USE_OPTION_MENU and option_menu is not None:
            choice = option_menu(
                menu_title=None,
                options=[label for label, _ in opts],
                icons=[icon or "dot" for icon in icon_list],
                orientation="vertical",
                key=key,
                default_index=index,
            )
        else:
            labels = [f"{icon or ''} {label}".strip() for (label, _), icon in zip(opts, icon_list)]
            choice = st.radio("", labels, index=index, key=key)
            choice = opts[labels.index(choice)][0]

        st.markdown("</div>", unsafe_allow_html=True)

    st.session_state[session_key] = choice
    return choice



def render_sidebar_nav(*args, **kwargs):
    """Wrapper to allow legacy patching via ``render_modern_sidebar``."""
    if globals().get("render_modern_sidebar") is not render_sidebar_nav:
        return globals()["render_modern_sidebar"](*args, **kwargs)
    return _render_sidebar_nav(*args, **kwargs)


# Legacy name used in older modules
render_modern_sidebar = render_sidebar_nav


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
    "render_sidebar_nav",
    "render_title_bar",
    "show_preview_badge",
    "render_profile_card",
]
