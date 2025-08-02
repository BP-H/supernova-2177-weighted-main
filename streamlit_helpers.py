# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Streamlit UI helper utilities."""

from __future__ import annotations
import html
from contextlib import contextmanager, nullcontext
from typing import Any, ContextManager, Literal
import streamlit as st
from frontend.theme import set_theme, inject_global_styles

# Fallback UI for when advanced components are not available
class _DummyElement:
    def __init__(self, cm: ContextManager | None = None) -> None:
        self._cm = cm or nullcontext()
    def __enter__(self) -> Any:
        return self._cm.__enter__()
    def __exit__(exc_type: Any, exc: Any, tb: Any) -> None:
        self._cm.__exit__(exc_type, exc, tb)
    def classes(self, *_a: Any, **_k: Any) -> "_DummyElement":
        return self
    def style(self, *_a: Any, **_k: Any) -> "_DummyElement":
        return self

class _DummyUI:
    def image(self, img: str) -> _DummyElement:
        st.image(img, use_container_width=True)
        return _DummyElement()
    def element(self, *_a: Any, **_k: Any) -> _DummyElement:
        return _DummyElement()
    def card(self, *_a: Any, **_k: Any) -> _DummyElement:
        return _DummyElement()
    def badge(self, *_a: Any, **_k: Any) -> _DummyElement:
        return _DummyElement()

try:
    import streamlit_shadcn_ui as ui
except ImportError:
    ui = _DummyUI()

def sanitize_text(text: Any) -> str:
    """Return `text` as a safe string."""
    return html.escape(str(text), quote=False) if text else ""

@contextmanager
def safe_container(container=None):
    """A context manager for safely using Streamlit containers."""
    if container is None:
        container = st
    yield container

def header(title: str, *, layout: str = "centered") -> None:
    """Render a standard page header."""
    st.markdown(f"<h1>{sanitize_text(title)}</h1>", unsafe_allow_html=True)

def theme_toggle(label: str = "Dark Mode", *, key_suffix: str = None) -> str:
    """Switch between light and dark themes using a toggle widget."""
    key = f"theme_toggle_{key_suffix or 'default'}"
    current_theme = st.session_state.get("theme", "light")
    
    is_dark = st.toggle(label, value=(current_theme == "dark"), key=key)
    chosen_theme = "dark" if is_dark else "light"
    if chosen_theme != current_theme:
        st.session_state["theme"] = chosen_theme
        set_theme(chosen_theme)
        st.rerun()
        
    return chosen_theme

def alert(message: str, type: Literal["info", "error"] = "info") -> None:
    """Display an alert box."""
    if type == "info":
        st.info(message)
    elif type == "error":
        st.error(message)
