# frontend/theme.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Color theme utilities for Streamlit frontend (clean, single-source)."""

from __future__ import annotations
from dataclasses import dataclass
import streamlit as st


@dataclass(frozen=True)
class ColorTheme:
    bg: str
    card: str
    accent: str
    text: str
    text_muted: str
    radius: str = "1rem"
    transition: str = "0.4s ease"


LIGHT_THEME = ColorTheme(
    bg="#F0F2F6",
    card="#FFFFFF",
    accent="#0077B5",   # LinkedIn-like blue
    text="#222222",
    text_muted="#666666",
)

DARK_THEME = ColorTheme(
    bg="#0A0F14",
    card="rgba(255,255,255,0.06)",
    accent="#00E5FF",
    text="#FFFFFF",
    text_muted="#AAAAAA",
)

THEMES = {"light": LIGHT_THEME, "dark": DARK_THEME}


def _resolve_mode(name: bool | str = True) -> str:
    if isinstance(name, str):
        n = name.lower()
        return n if n in THEMES else "light"
    return "dark" if name else "light"


def get_theme(name: bool | str = True) -> ColorTheme:
    return THEMES[_resolve_mode(name)]


def _base_css(th: ColorTheme) -> str:
    return f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
:root {{
  --bg: {th.bg};
  --card: {th.card};
  --accent: {th.accent};
  --text: {th.text};
  --text-muted: {th.text_muted};
  --radius: {th.radius};
  --transition: {th.transition};
  --font: 'Inter', sans-serif;
}}

html, body {{
  background: var(--bg) !important;
  color: var(--text);
  font-family: var(--font);
  transition: background var(--transition), color var(--transition);
}}

a {{ color: var(--accent); }}
.text-muted {{ color: var(--text-muted); }}

button, .stButton > button {{ border-radius: var(--radius); }}

.card, .glass-card {{
  background: var(--card);
  border-radius: var(--radius);
}}

.glass-card {{
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.12);
  box-shadow: 0 8px 20px rgba(0,0,0,0.10);
}}

@keyframes fade-in {{ from {{opacity:0;}} to {{opacity:1;}} }}
</style>
"""


def inject_global_styles(theme: bool | str = True) -> None:
    """Inject global variables and base CSS once per session."""
    mode = _resolve_mode(theme)
    st.session_state["_theme"] = mode
    if not st.session_state.get("_global_styles_injected"):
        st.markdown(_base_css(get_theme(mode)), unsafe_allow_html=True)
        st.session_state["_global_styles_injected"] = True
    else:
        # If already injected, still ensure the chosen theme is recorded
        st.session_state["_theme"] = mode


def inject_modern_styles(theme: bool | str = True) -> None:
    """Optional extra polish (safe to call many times)."""
    inject_global_styles(theme)
    if st.session_state.get("_modern_styles_injected"):
        return
    extra = """
    <style>
      .insta-btn, .linkedin-btn {
        padding: .6rem 1.2rem;
        border: none;
        border-radius: var(--radius);
        color: #fff !important;
        font-weight: 600;
        cursor: pointer;
        transition: transform .2s ease;
      }
      .insta-btn { background: linear-gradient(45deg,#F58529,#DD2A7B,#8134AF); }
      .linkedin-btn { background: var(--accent); }
      .insta-btn:active, .linkedin-btn:active { transform: scale(0.97); }
    </style>
    """
    st.markdown(extra, unsafe_allow_html=True)
    st.session_state["_modern_styles_injected"] = True


# Compatibility helpers expected across the codebase
def apply_theme(name: bool | str = True) -> None:
    inject_global_styles(name)


def set_theme(name: bool | str = "light") -> None:
    mode = _resolve_mode(name)
    st.session_state["_theme"] = mode
    inject_global_styles(mode)


def initialize_theme(name: bool | str = "light") -> None:
    set_theme(name)
    inject_modern_styles(name)


def get_accent_color() -> str:
    return get_theme(st.session_state.get("_theme", "light")).accent


__all__ = [
    "apply_theme",
    "set_theme",
    "initialize_theme",
    "inject_global_styles",
    "inject_modern_styles",
    "get_accent_color",
    "get_theme",
]
