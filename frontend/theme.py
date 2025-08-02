# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Color theme utilities for Streamlit frontend."""

from __future__ import annotations
from dataclasses import dataclass

import streamlit as st


# ──────────────────────────────────────────────────────────────────────────────
# Theme model
# ──────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ColorTheme:
    """Container for theme colors and common tokens."""
    bg: str
    card: str
    accent: str
    text: str
    text_muted: str
    radius: str = "1rem"
    transition: str = "0.4s ease"

    def css_vars(self) -> str:
        return "\n    ".join(
            [
                f"--bg: {self.bg};",
                f"--card: {self.card};",
                f"--accent: {self.accent};",
                f"--text: {self.text};",
                f"--text-muted: {self.text_muted};",
                f"--radius: {self.radius};",
                f"--transition: {self.transition};",
                "--font: 'Inter', sans-serif;",
            ]
        )


# ──────────────────────────────────────────────────────────────────────────────
# Palettes
# ──────────────────────────────────────────────────────────────────────────────

LIGHT_THEME = ColorTheme(
    bg="#F0F2F6",
    card="#FFFFFF",
    accent="#0077B5",  # LinkedIn-like blue
    text="#222222",
    text_muted="#666666",
)

DARK_THEME = ColorTheme(
    bg="#0A0F14",
    card="rgba(255,255,255,0.05)",
    accent="#00E5FF",  # Neon cyan
    text="#FFFFFF",
    text_muted="#AAAAAA",
)

THEMES: dict[str, ColorTheme] = {"light": LIGHT_THEME, "dark": DARK_THEME}


# ──────────────────────────────────────────────────────────────────────────────
# Internals
# ──────────────────────────────────────────────────────────────────────────────

def _resolve_mode(name: bool | str | None) -> str:
    """Return 'light' or 'dark' from a bool/str/None."""
    if isinstance(name, str):
        mode = name.lower()
        return mode if mode in THEMES else "light"
    if isinstance(name, bool):
        return "dark" if name else "light"
    # default
    return st.session_state.get("_theme", "light") if hasattr(st, "session_state") else "light"


def get_theme(name: bool | str | None = None) -> ColorTheme:
    """Return the ColorTheme for the given mode (or current)."""
    return THEMES[_resolve_mode(name)]


def _inject_assets_once() -> None:
    """Load fonts & icons once per session."""
    if st.session_state.get("_assets_injected"):
        return
    st.markdown(
        """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        """,
        unsafe_allow_html=True,
    )
    st.session_state["_assets_injected"] = True


def _base_css(th: ColorTheme) -> str:
    return f"""
<style>
:root {{
    {th.css_vars()}
}}
body {{
    background: var(--bg) !important;
    color: var(--text);
    font-family: var(--font);
    transition: background var(--transition), color var(--transition);
}}
.card {{ background: var(--card); }}
a {{ color: var(--accent); }}
.text-muted {{ color: var(--text-muted); }}

button, .stButton > button {{
    border-radius: var(--radius);
}}

@keyframes fade-in {{
  from {{ opacity: 0; }}
  to   {{ opacity: 1; }}
}}
</style>
""".strip()


def _modern_extras_css() -> str:
    return """
<style>
/* Glassmorphic cards */
.glass-card {
    background: var(--card);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: var(--radius);
    padding: 1rem;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

/* Accent gradient buttons */
.insta-btn, .linkedin-btn {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: var(--radius);
    color: #fff !important;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease;
}
.insta-btn { background: linear-gradient(45deg, #F58529, #DD2A7B, #8134AF); }
.linkedin-btn { background: var(--accent); }
.insta-btn:active, .linkedin-btn:active { transform: scale(0.97); }
</style>
""".strip()


def _apply_base_styles(mode: str) -> None:
    """Apply base CSS for the selected mode."""
    th = get_theme(mode)
    st.markdown(_base_css(th), unsafe_allow_html=True)


def _apply_extras_once() -> None:
    """Apply extras once per session (after base)."""
    if st.session_state.get("_extras_injected"):
        return
    st.markdown(_modern_extras_css(), unsafe_allow_html=True)
    st.session_state["_extras_injected"] = True


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def initialize_theme(mode: bool | str = "light") -> None:
    """
    Initialize the app theme & styles. Safe to call multiple times.
    Accepts 'light'/'dark' or True(dark)/False(light).
    """
    resolved = _resolve_mode(mode)
    st.session_state["_theme"] = resolved
    _inject_assets_once()
    _apply_base_styles(resolved)
    _apply_extras_once()


def apply_theme(name: bool | str = "light") -> None:
    """Backward-compatible alias."""
    initialize_theme(name)


def set_theme(name: bool | str = "light") -> None:
    """Set and apply the theme."""
    initialize_theme(name)


def inject_global_styles(theme: bool | str | None = None) -> None:
    """
    Ensure global assets & base styles are applied for the given theme (or current).
    Keeps extras idempotent.
    """
    resolved = _resolve_mode(theme)
    st.session_state["_theme"] = resolved
    _inject_assets_once()
    _apply_base_styles(resolved)
    _apply_extras_once()


def inject_modern_styles(theme: bool | str | None = None) -> None:
    """
    Back-compat helper. Ensures theme + extras are injected.
    """
    inject_global_styles(theme)


def get_accent_color() -> str:
    """Return the current accent color."""
    return get_theme(st.session_state.get("_theme", "light")).accent


__all__ = [
    "ColorTheme",
    "LIGHT_THEME",
    "DARK_THEME",
    "THEMES",
    "get_theme",
    "get_accent_color",
    "initialize_theme",
    "apply_theme",
    "set_theme",
    "inject_global_styles",
    "inject_modern_styles",
]
