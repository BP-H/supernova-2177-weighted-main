# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Streamlit UI helper utilities."""
from __future__ import annotations
import html
from contextlib import contextmanager, nullcontext
from typing import Any, ContextManager
import streamlit as st
from frontend.theme import set_theme
# This re-export allows other files to import inject_global_styles from here if needed
from frontend.theme import inject_global_styles
class _DummyElement:
    """A fallback UI element that does nothing but allows chaining."""
    def __init__(self, cm: ContextManager | None = None) -> None: self._cm = cm or nullcontext()
    def __enter__(self) -> Any: return self._cm.__enter__()
    def __exit__(self, *a: Any) -> None: self._cm.__exit__(*a)
    def classes(self, *_a: Any, **_k: Any) -> "_DummyElement": return self
    def style(self, *_a: Any, **_k: Any) -> "_DummyElement": return self
class _DummyUI:
    """A complete fallback UI to prevent AttributeError when a component is not installed."""
    def image(self, img: str, width: Any = None) -> _DummyElement:
        # FIX: Removed unsupported `alt` parameter.
        st.image(img, use_container_width=True)
        return _DummyElement()
    def element(self, *a: Any, **k: Any) -> _DummyElement: return _DummyElement()
    def card(self, *a: Any, **k: Any) -> _DummyElement: return _DummyElement(st.container())
    def badge(self, *a: Any, **k: Any) -> _DummyElement: return _DummyElement()
    def alert(self, title: str = "Alert", **k: Any) -> _DummyElement:
        st.warning(title)
        return _DummyElement()
try:
    import streamlit_shadcn_ui as ui
except ImportError:
    ui = _DummyUI()
def sanitize_text(text: Any) -> str:
    """Returns text as a safe HTML-escaped string."""
    return html.escape(str(text), quote=False) if text else ""
@contextmanager
def safe_container(container=None):
    """A context manager for safely using Streamlit containers."""
    yield container or st
def header(title: str) -> None:
    """Renders a standard page header."""
    st.markdown(f"<h3>{sanitize_text(title)}</h3>", unsafe_allow_html=True)
def theme_toggle(label: str = "Dark Mode", *, key_suffix: str | None = None) -> str:
    """Renders a toggle switch to control the light/dark theme."""
    key = f"theme_toggle_{key_suffix or 'default'}"
    current_theme = st.session_state.get("_theme_name", "light")
   
    is_dark = st.toggle(label, value=(current_theme == "dark"), key=key)
    chosen_theme = "dark" if is_dark else "light"
   
    if chosen_theme != current_theme:
        set_theme(chosen_theme)
        st.rerun()
       
    return chosen_theme
def alert(message: str, type: str = "info") -> None:
    """Displays a simple alert message using Streamlit's native components."""
    if type == "info":
        st.info(message)
    elif type == "error":
        st.error(message)
    else:
        st.warning(message)
