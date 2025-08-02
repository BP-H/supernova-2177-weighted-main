# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Color theme utilities for Streamlit frontend."""

from __future__ import annotations
from dataclasses import dataclass

import streamlit as st


# ──────────────────────────────────────────────────────────────────────────────
# Theme tokens
# ──────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ColorTheme:
    """Container for theme colors and common tokens."""
    bg: str
    card: str
    accent: str
    text: str
    text_muted: str
    radius: str = "12px"
    transition: str = "0.4s ease"


# LinkedIn-leaning palettes
LIGHT_THEME = ColorTheme(
    bg="#F3F6F8",
    card="#FFFFFF",
    accent="#0A66C2",   # LinkedIn blue
    text="#1F2328",
    text_muted="#6B778C",
)

DARK_THEME = ColorTheme(
    bg="#0B1418",
    card="rgba(255,255,255,0.05)",
    accent="#00C1FF",   # Neon cyan
    text="#E7EEF2",
    text_muted="#9FB3C8",
)

THEMES = {"light": LIGHT_THEME, "dark": DARK_THEME}


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def get_theme(name: bool | str = True) -> ColorTheme:
    """
    Return a ColorTheme by name or boolean flag.
      - True  -> dark
      - False -> light
      - "light"/"dark" (case-insensitive)
    """
    if isinstance(name, str):
        return THEMES.get(name.lower(), LIGHT_THEME)
    return DARK_THEME if name else LIGHT_THEME


def _resolve_mode(name: bool | str) -> str:
    if isinstance(name, str):
        return name.lower() if name.lower() in THEMES else "light"
    return "dark" if name else "light"


def _font_links() -> str:
    return (
        "<link rel='preconnect' href='https://fonts.googleapis.com'>"
        "<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
        "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap' rel='stylesheet'>"
        "<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css'>"
    )


def _base_css(theme: ColorTheme) -> str:
    # NOTE: This is a plain f-string; CSS braces are literal and safe here.
    return f"""
<style>
:root {{
  --bg: {theme.bg};
  --card: {theme.card};
  --accent: {theme.accent};
  --text: {theme.text};
  --text-muted: {theme.text_muted};
  --radius: {theme.radius};
  --transition: {theme.transition};
  --font: 'Inter', sans-serif;
}}

html, body {{
  background: var(--bg) !important;
  color: var(--text);
  font-family: var(--font);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transition: background var(--transition), color var(--transition);
}}

a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

button, .stButton > button {{
  border-radius: var(--radius);
}}

.card {{
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
}}

.text-muted {{ color: var(--text-muted); }}

@keyframes fade-in {{
  from {{ opacity: 0; transform: translateY(2px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
</style>
"""


def _modern_css() -> str:
    return """
<style>
/* Modern extras */
.glass-card{
  background: var(--card);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius);
  padding: 1rem;
  box-shadow: 0 8px 20px rgba(0,0,0,0.10);
  animation: fade-in .4s ease 1;
}

.btn-accent, .linkedin-btn {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  padding: .6rem 1.2rem;
  border: 0;
  border-radius: var(--radius);
  background: var(--accent);
  color: #fff !important;
  font-weight: 600;
  cursor: pointer;
  transition: transform .16s ease, box-shadow .16s ease;
}
.btn-accent:active, .linkedin-btn:active { transform: scale(0.98); }

.badge {
  display: inline-block;
  padding: .2rem .6rem;
  border-radius: 999px;
  background: var(--card);
  box-shadow: 0 1px 2px rgba(0,0,0,.08);
  color: var(--text-muted);
  font-size: .85rem;
}
</style>
"""


# ──────────────────────────────────────────────────────────────────────────────
# Public API (idempotent)
# ──────────────────────────────────────────────────────────────────────────────

def apply_theme(name: bool | str = True) -> None:
    """Apply the base theme CSS immediately (no fonts/extras)."""
    mode = _resolve_mode(name)
    st.session_state["_theme"] = mode
    st.markdown(_base_css(get_theme(mode)), unsafe_allow_html=True)


def inject_global_styles(theme: bool | str = True) -> None:
    """
    Inject fonts and base CSS once per session (idempotent).
    Subsequent calls update the CSS variables if the mode changes.
    """
    mode = _resolve_mode(theme)
    st.session_state["_theme"] = mode

    if not st.session_state.get("_global_styles_injected"):
        st.markdown(_font_links() + _base_css(get_theme(mode)), unsafe_allow_html=True)
        st.session_state["_global_styles_injected"] = True
    else:
        # Update variables if theme changed mid-session
        apply_theme(mode)


def inject_modern_styles(theme: bool | str = True) -> None:
    """Inject optional modern component styles once (idempotent)."""
    mode = _resolve_mode(theme)
    inject_global_styles(mode)
    if st.session_state.get("_modern_styles_injected"):
        return
    st.markdown(_modern_css(), unsafe_allow_html=True)
    st.session_state["_modern_styles_injected"] = True


def set_theme(name: str) -> None:
    """Set the current theme mode in session and (re)apply base CSS."""
    mode = _resolve_mode(name)
    st.session_state["_theme"] = mode
    apply_theme(mode)


def initialize_theme(name: bool | str = "light") -> None:
    """
    One-call initializer used by pages:
      - sets theme
      - injects fonts & base CSS
      - injects modern extras
    """
    mode = _resolve_mode(name)
    st.session_state["_theme"] = mode
    inject_global_styles(mode)
    inject_modern_styles(mode)


def get_accent_color() -> str:
    """Return the accent color for the current theme."""
    mode = st.session_state.get("_theme", "light")
    return get_theme(mode).accent


__all__ = [
    "ColorTheme",
    "LIGHT_THEME",
    "DARK_THEME",
    "THEMES",
    "get_theme",
    "get_accent_color",
    "apply_theme",
    "inject_global_styles",
    "inject_modern_styles",
    "set_theme",
    "initialize_theme",
]
