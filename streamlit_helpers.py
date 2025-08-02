# streamlit_helpers.py  – authoritative single copy
from __future__ import annotations

import html
from contextlib import contextmanager, nullcontext
from typing import Any, ContextManager, Iterable, Literal

import streamlit as st
from frontend.theme import set_theme, inject_global_styles


# ── Fallback UI elements ──────────────────────────────────────────────────────
class _DummyElement:
    def __init__(self, cm: ContextManager | None = None) -> None:
        self._cm = cm or nullcontext()
    def __enter__(self): return self._cm.__enter__()
    def __exit__(self, exc_type, exc, tb): self._cm.__exit__(exc_type, exc, tb)
    def classes(self, *_a, **_k): return self
    def style(self, *_a, **_k):   return self


class _DummyUI:
    def image(self, *_a, **_k): return _DummyElement()
    def element(self, *_a, **_k): return _DummyElement()
    def card(self, *_a, **_k): return _DummyElement()
    def badge(self, *_a, **_k): return _DummyElement()


try:
    import streamlit_shadcn_ui as ui          # real component lib
except ImportError:
    ui = _DummyUI()                           # silent fallback


# ── Tiny utilities ────────────────────────────────────────────────────────────
def sanitize_text(x: Any) -> str:
    return html.escape(str(x), quote=False) if x is not None else ""


@contextmanager
def safe_container(container=None):
    yield container or st


def header(txt: str):
    st.markdown(f"<h2>{sanitize_text(txt)}</h2>", unsafe_allow_html=True)


def alert(msg: str, type: Literal["info", "warning", "error"] = "info"):
    getattr(st, type, st.info)(msg)


# ── Theme controls ────────────────────────────────────────────────────────────
def theme_toggle(label: str = "Dark mode",
                 *, key_suffix: str = "def") -> str:
    key = f"theme_toggle_{key_suffix}"
    cur = st.session_state.get("theme", "light")
    dark = st.toggle(label, value=(cur == "dark"), key=key)
    new = "dark" if dark else "light"
    if new != cur:
        st.session_state["theme"] = new
        set_theme(new)
        st.rerun()
    return new


# **Legacy selector still imported by many pages**
def theme_selector(label: str = "Theme",
                   *, key_suffix: str = "legacy") -> str:
    mapping = {"Light": "light", "Dark": "dark"}
    rev = {v: k for k, v in mapping.items()}
    cur_lbl = rev[st.session_state.get("theme", "light")]
    choice = st.selectbox(label, list(mapping),
                          index=list(mapping).index(cur_lbl),
                          key=f"theme_sel_{key_suffix}")
    sel = mapping[choice]
    if sel != st.session_state.get("theme", "light"):
        st.session_state["theme"] = sel
        set_theme(sel)
        st.rerun()
    return sel


# ── Stubs still expected by other pages ───────────────────────────────────────
def get_active_user() -> str | None:
    return st.session_state.get("active_user")


@contextmanager
def centered_container(**kw):
    with st.container(**kw) as c:
        st.markdown(
            "<style>[data-testid='column']"
            "{margin-left:auto!important;margin-right:auto!important;}</style>",
            unsafe_allow_html=True,
        )
        yield c


def render_mock_feed(container=None):       # used by social_tabs
    import feed                               # local import avoids circularity
    feed.main(main_container=container)


# ── Chat‑state normaliser (fixes 'preview' / .keys() crashes) ────────────────
def _upgrade_conversation_state():
    convs = st.session_state.get("conversations")
    if convs is None:
        return
    if isinstance(convs, dict):              # already new shape
        for v in convs.values():
            v.setdefault("preview",
                          v["messages"][-1]["content"] if v.get("messages") else "")
        return
    if isinstance(convs, list):              # old list → dict
        upgraded: dict[str, dict[str, Any]] = {}
        for c in convs:
            if not isinstance(c, dict):           # skip bad rows
                continue
            user = c.get("user", "unknown")
            msgs = c.get("messages", [])
            upgraded[user] = {
                "messages": msgs,
                "preview": msgs[-1]["content"] if msgs else "",
            }
        st.session_state["conversations"] = upgraded


_upgrade_conversation_state()
inject_global_styles()

# everything we intend external modules to import
__all__: Iterable[str] = (
    "ui", "sanitize_text", "safe_container", "alert", "header",
    "theme_toggle", "theme_selector",
    "get_active_user", "centered_container", "render_mock_feed",
)
