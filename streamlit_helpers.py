# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Streamlit UI helper utilities."""

from __future__ import annotations
import html
from contextlib import contextmanager, nullcontext
from datetime import datetime, timezone
from typing import Any, ContextManager, Iterable, Literal
import streamlit as st
from frontend.theme import set_theme, inject_global_styles

# Optional modern UI components (fallback if not installed)
try:
    from modern_ui_components import (
        render_validation_card,
        render_post_card,
        render_stats_section,
    )
except ImportError:
    def render_validation_card(*_a: Any, **_k: Any) -> None:
        st.info("validation card unavailable")
    def render_post_card(*_a: Any, **_k: Any) -> None:
        st.info("post card unavailable")
    def render_stats_section(*_a: Any, **_k: Any) -> None:
        st.info("stats section unavailable")

# Fallback for optional Shadcn UI (streamlit_shadcn_ui)
class _DummyElement:
    def __init__(self, cm: ContextManager | None = None) -> None:
        self._cm = cm or nullcontext()
    def __enter__(self) -> Any:
        return self._cm.__enter__()
    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self._cm.__exit__(exc_type, exc, tb)
    def classes(self, *args: Any, **kwargs: Any) -> "_DummyElement":
        return self
    def style(self, *args: Any, **kwargs: Any) -> "_DummyElement":
        return self

class _DummyUI:
    def image(self, *args: Any, **kwargs: Any) -> _DummyElement:
        return _DummyElement()
    def element(self, *args: Any, **kwargs: Any) -> _DummyElement:
        return _DummyElement()
    def card(self, *args: Any, **kwargs: Any) -> _DummyElement:
        return _DummyElement()
    def badge(self, *args: Any, **kwargs: Any) -> _DummyElement:
        return _DummyElement()

try:
    import streamlit_shadcn_ui as ui  # type: ignore
except ImportError:
    ui = _DummyUI()  # Provide dummy UI element if Shadcn UI is not available:contentReference[oaicite:0]{index=0}

# Tiny utility helpers
def sanitize_text(x: Any) -> str:
    """Escape text for safe HTML rendering."""
    return html.escape(str(x), quote=False) if x is not None else ""

@contextmanager
def safe_container(container=None):
    """Yield a write target (default to the page itself if no container given)."""
    yield container or st

def header(txt: str) -> None:
    """Render a section header with sanitized HTML."""
    st.markdown(f"<h2>{sanitize_text(txt)}</h2>", unsafe_allow_html=True)

def alert(msg: str, type: Literal["info", "warning", "error"] = "info") -> None:
    """Show a Streamlit alert of the given type with the message."""
    getattr(st, type, st.info)(msg)

# --- Theme Controls ---
def theme_toggle(label: str = "Dark Mode", *, key_suffix: str = "default") -> str:
    """
    Toggle between light and dark themes. Uses Streamlit’s built-in st.toggle on v1.35+:contentReference[oaicite:1]{index=1},
    falling back to a checkbox if needed. Automatically applies the theme and triggers a rerun.
    """
    key = f"theme_toggle_{key_suffix}"
    current = st.session_state.get("theme", "light")
    # Use Streamlit's native toggle if available (Streamlit >= 1.35)
    if hasattr(st, "toggle"):
        is_dark = st.toggle(label, value=(current == "dark"), key=key)
    else:
        # Fallback: use a checkbox if toggle widget is not available
        is_dark = st.checkbox(label, value=(current == "dark"), key=key)
    new_theme = "dark" if is_dark else "light"
    if new_theme != current:
        st.session_state["theme"] = new_theme
        set_theme(new_theme)  # apply new theme styles
        st.rerun()  # force a full rerun so styles take effect
    return new_theme

# Legacy theme selector (for older pages expecting a selectbox)
def theme_selector(label: str = "Theme", *, key_suffix: str = "legacy") -> str:
    mapping = {"Light": "light", "Dark": "dark"}
    inv_map = {v: k for k, v in mapping.items()}
    cur_label = inv_map[st.session_state.get("theme", "light")]
    choice = st.selectbox(label, list(mapping.keys()), index=list(mapping.keys()).index(cur_label), key=f"theme_sel_{key_suffix}")
    new_theme = mapping[choice]
    if new_theme != st.session_state.get("theme", "light"):
        st.session_state["theme"] = new_theme
        set_theme(new_theme)
        st.rerun()
    return new_theme

# --- Page-Shim Helpers (for profile/social pages) ---
def get_active_user() -> str | None:
    """Return the username that the profile/social pages treat as the current user."""
    return st.session_state.get("active_user")

def ensure_active_user() -> str:
    """
    Ensure an 'active_user' is set in session state, defaulting to 'guest' if not present.
    """
    return st.session_state.setdefault("active_user", "guest")

@contextmanager
def centered_container(**st_container_kwargs):
    """Create a container where inner columns are centered horizontally."""
    with st.container(**st_container_kwargs) as c:
        # Inject CSS to center all column blocks inside this container
        st.markdown(
            "<style>[data-testid='column']{margin-left:auto!important;margin-right:auto!important;}</style>",
            unsafe_allow_html=True,
        )
        yield c

# Feed shim (so social page can render the feed without heavy imports twice)
def render_mock_feed(container=None) -> None:
    import feed  # import the feed module (assumed to be part of the project)
    feed.main(main_container=container)

# --- Chat State Normalization ---
def _normalise_conversations_state() -> None:
    """
    Normalize the structure of chat conversations in session state.
    Converts old format (list) to new format (dict) to prevent KeyError/AttributeError:contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}.
    """
    convs = st.session_state.get("conversations")
    if convs is None:
        return
    if isinstance(convs, list):
        upgraded: dict[str, dict[str, Any]] = {}
        for c in convs:
            if isinstance(c, dict):
                user = c.get("user", "unknown")
                messages: list[dict[str, str]] = c.get("messages", [])
                preview = messages[-1]["content"] if messages else ""
                upgraded[user] = {"messages": messages, "preview": preview}
        st.session_state["conversations"] = upgraded
        # After this conversion, st.session_state["conversations"] is a dict mapping user -> data:contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}

# Perform one-time normalization and global style injection on import
_normalise_conversations_state()
inject_global_styles()  # Inject base (theme-agnostic) styles exactly once

__all__: Iterable[str] = (
    "ui",
    "sanitize_text",
    "safe_container",
    "alert",
    "header",
    "theme_toggle",
    "theme_selector",
    "get_active_user",
    "ensure_active_user",
    "centered_container",
    "render_mock_feed",
    "render_validation_card",
    "render_post_card",
    "render_stats_section",
)
