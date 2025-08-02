# streamlit_helpers.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Unified Streamlit UI helper utilities for the entire application."""
from __future__ import annotations

import html
from contextlib import contextmanager, nullcontext
from typing import Any, Literal, Dict, List

import streamlit as st
# Import directly from the source to prevent circular dependencies
from frontend.theme import set_theme, inject_global_styles


# --- Fallback UI Elements (for when streamlit_shadcn_ui is not installed) ---
class _DummyElement:
    """A fallback UI element that does nothing but allows chaining."""
    def __init__(self, cm: nullcontext | None = None) -> None: self._cm = cm or nullcontext()
    def __enter__(self) -> Any: return self._cm.__enter__()
    def __exit__(self, *a: Any) -> None: self._cm.__exit__(*a)
    def classes(self, *_a: Any, **_k: Any) -> "_DummyElement": return self
    def style(self, *_a: Any, **_k: Any) -> "_DummyElement": return self


class _DummyUI:
    """A complete fallback UI to prevent AttributeError for missing components."""
    def image(self, *_a, **_k) -> _DummyElement: return _DummyElement()
    def element(self, *_a, **_k) -> _DummyElement: return _DummyElement()
    def card(self, *_a, **_k) -> _DummyElement: return _DummyElement()
    def badge(self, *_a, **_k) -> _DummyElement: return _DummyElement()


try:
    import streamlit_shadcn_ui as ui
except ImportError:
    ui = _DummyUI()


# --- Core Utility Helpers ---
def sanitize_text(x: Any) -> str:
    """Returns text as a safe HTML-escaped string."""
    return html.escape(str(x), quote=False) if x is not None else ""


@contextmanager
def safe_container(container=None):
    """A context manager for safely using Streamlit containers."""
    yield container or st


def header(txt: str):
    """Renders a standard page header."""
    st.markdown(f"<h2>{sanitize_text(txt)}</h2>", unsafe_allow_html=True)


def alert(msg: str, type: Literal["info", "warning", "error"] = "info"):
    """Displays a simple alert message using Streamlit's native components."""
    getattr(st, type, st.info)(msg)


# --- Theme Controls ---
def theme_toggle(label: str = "Dark mode", *, key_suffix: str = "default") -> str:
    """Renders a modern toggle switch to control the light/dark theme."""
    key = f"theme_toggle_{key_suffix}"
    cur = st.session_state.get("theme", "light")
    is_dark = st.toggle(label, value=(cur == "dark"), key=key)
    new = "dark" if is_dark else "light"
    if new != cur:
        st.session_state["theme"] = new
        set_theme(new)
        st.rerun()
    return new


# --- Legacy & Compatibility Wrappers ---
def theme_selector(label: str = "Theme", *, key_suffix: str = "legacy") -> str:
    """LEGACY wrapper for older pages that use a selectbox for the theme."""
    mapping = {"Light": "light", "Dark": "dark"}
    rev = {v: k for k, v in mapping.items()}
    cur = rev.get(st.session_state.get("theme", "light"), "Light")
    choice = st.selectbox(label, list(mapping), index=list(mapping).index(cur), key=f"theme_sel_{key_suffix}")
    if mapping[choice] != st.session_state.get("theme", "light"):
        st.session_state["theme"] = mapping[choice]
        set_theme(mapping[choice])
        st.rerun()
    return mapping[choice]


def get_active_user() -> str | None:
    """Return the username the profile/social pages treat as 'me'."""
    return st.session_state.get("active_user")


def ensure_active_user():
    """Ensure an active user is set in the session state."""
    st.session_state.setdefault("active_user", "guest")


@contextmanager
def centered_container(**st_container_kwargs):
    """Streamlit container whose internal columns are centred."""
    with st.container(**st_container_kwargs) as c:
        st.markdown(
            "<style>[data-testid='column']{margin-left:auto!important;margin-right:auto!important;}</style>",
            unsafe_allow_html=True,
        )
        yield c


def render_post_card(*args, **kwargs):
    """Shim to prevent import errors. The real function is likely in a page module."""
    st.warning("`render_post_card` is a placeholder.")


def render_instagram_grid(*args, **kwargs):
    """Shim to prevent import errors."""
    st.info("Instagram grid placeholder.")


# --- Global State Normalization (runs once on import) ---
def _normalise_conversations_state():
    """
    This function intelligently fixes the chat data structure on the fly
    to prevent crashes on the messages page.
    """
    convs = st.session_state.get("conversations")
    if isinstance(convs, list):
        upgraded: Dict[str, Dict[str, Any]] = {}
        for c in convs:
            if isinstance(c, dict):
                user = c.get("user", "unknown")
                msgs: List[Dict[str, str]] = c.get("messages", [])  # Fixed syntax from assessments
                preview = msgs[-1]["content"] if msgs else ""
                upgraded[user] = {"messages": msgs, "preview": preview}
        st.session_state["conversations"] = upgraded

_normalise_conversations_state()

# Always make sure base CSS is present
inject_global_styles()


# --- Exports for other modules ---
__all__ = [
    "ui", "sanitize_text", "safe_container", "alert", "header",
    "theme_toggle", "theme_selector", "get_active_user",
    "centered_container", "render_post_card", "render_instagram_grid",
    "ensure_active_user",
]
