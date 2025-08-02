# streamlit_helpers.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Unified Streamlit helper utilities (single source-of-truth)."""
from __future__ import annotations

import html
from contextlib import contextmanager, nullcontext
from typing import Any, ContextManager, Iterable, Literal

import streamlit as st
# Import directly from the source to prevent circular dependencies
from frontend.theme import inject_global_styles

# --- Graceful fallback for optional component lib ---
class _DummyElement:
    def __init__(self, cm: ContextManager | None = None) -> None:
        self._cm = cm or nullcontext()
    def __enter__(self): return self._cm.__enter__()
    def __exit__(self, exc_type, exc, tb): self._cm.__exit__(exc_type, exc, tb)
    def classes(self, *_a, **_k): return self
    def style(self, *_a, **_k): return self

class _DummyUI:
    def image(self, *_a, **_k): return _DummyElement()
    def element(self, *_a, **_k): return _DummyElement()
    def card(self, *_a, **_k): return _DummyElement()
    def badge(self, *_a, **_k): return _DummyElement()

try:
    import streamlit_shadcn_ui as ui
except ImportError:
    ui = _DummyUI()

# --- Core HTML / Layout Helpers ---
def sanitize_text(x: Any) -> str:
    return html.escape(str(x), quote=False) if x is not None else ""

@contextmanager
def safe_container(container=None):
    yield container or st

def header(txt: str):
    st.markdown(f"<h2>{sanitize_text(txt)}</h2>", unsafe_allow_html=True)

def alert(msg: str, type: Literal["info", "warning", "error"] = "info"):
    getattr(st, type, st.info)(msg)

# --- Theme Helpers & Legacy Wrappers ---
def theme_toggle(label: str = "Dark mode", *, key_suffix: str = "def") -> str:
    from frontend.theme import set_theme # Local import to avoid circularity
    key = f"theme_toggle_{key_suffix}"
    cur = st.session_state.get("theme", "light")
    dark = st.toggle(label, value=(cur == "dark"), key=key)
    new = "dark" if dark else "light"
    if new!= cur:
        st.session_state["theme"] = new
        set_theme(new)
        st.rerun()
    return new

def theme_selector(label: str = "Theme", *, key_suffix: str = "legacy") -> str:
    from frontend.theme import set_theme # Local import to avoid circularity
    mapping = {"Light": "light", "Dark": "dark"}
    rev = {v: k for k, v in mapping.items()}
    cur_lbl = rev.get(st.session_state.get("theme", "light"), "Light")
    choice = st.selectbox(
        label, list(mapping),
        index=list(mapping).index(cur_lbl),
        key=f"theme_sel_{key_suffix}"
    )
    sel = mapping[choice]
    if sel!= st.session_state.get("theme", "light"):
        st.session_state["theme"] = sel
        set_theme(sel)
        st.rerun()
    return sel

# --- Backward-Compatibility Stubs for Older Pages ---
def get_active_user() -> str | None:
    return st.session_state.get("active_user")

def ensure_active_user():
    st.session_state.setdefault("active_user", "guest")

@contextmanager
def centered_container(**kw):
    with st.container(**kw) as c:
        st.markdown(
            "<style>[data-testid='column']"
            "{margin-left:auto!important;margin-right:auto!important;}</style>",
            unsafe_allow_html=True,
        )
        yield c

def render_post_card(*args, **kwargs):
    st.warning("`render_post_card` is a placeholder and has not been implemented.")

def render_instagram_grid(*args, **kwargs):
    st.info("`render_instagram_grid` is a placeholder.")

def render_mock_feed(container=None):
    import feed # Local import to avoid circular dependency at startup
    feed.main(main_container=container)

# --- Chat-State Upgrader to Fix the Messages Page Crash ---
def _normalise_conversations_state() -> None:
    """
    Intelligently fixes the chat data structure on the fly.
    It checks if the data is in the old list format and converts it
    to the new dict format, preventing the AttributeError on the messages page.
    """
    convs = st.session_state.get("conversations")
    if isinstance(convs, list):
        upgraded: dict[str, dict[str, Any]] = {}
        for c in convs:
            if not isinstance(c, dict):
                continue
            user = c.get("user", "unknown")
            msgs = c.get("messages",) # Corrected: removed trailing comma
            upgraded[user] = {
                "messages": msgs,
                "preview": msgs[-1]["content"] if msgs else "",
            }
        st.session_state["conversations"] = upgraded

# --- Run Initialization Logic on Import ---
_normalise_conversations_state()
inject_global_styles()

# --- Define Public API for Other Modules ---
__all__: Iterable[str] = (
    "ui", "sanitize_text", "safe_container", "alert", "header",
    "theme_toggle", "theme_selector",
    "get_active_user", "ensure_active_user", "centered_container",
    "render_mock_feed", "render_post_card", "render_instagram_grid",
)
