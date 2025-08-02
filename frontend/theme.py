# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Color theme utilities for Streamlit frontend."""

from __future__ import annotations
from dataclasses import dataclass

import streamlit as st


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
        """Return CSS variable declarations for this theme."""
        return "\n    ".join(
            [
                f"--bg: {self.bg};",
                f"--card: {self.card};",
                f"--accent: {self.accent};",
                f"--text: {self.text};",
                f"--text-muted: {self.text_muted};",
                f"--radius: {self.radius};",
                f"--transition: {self.transition};",
            ]
        )


# Modern “light” and “dark” palettes
LIGHT_THEME = ColorTheme(
    bg="#F0F2F6",
    card="#FFFFFF",
    accent="#0077B5",  # LinkedIn-blue accent
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

THEMES = {"light": LIGHT_THEME, "dark": DARK_THEME}


def get_theme(name: bool | str = True) -> ColorTheme:
    """
    Return the selected ColorTheme by name or boolean flag.
    - name == True  ⇒ dark
    - name == False ⇒ light
    - name == "light"/"dark"
    """
    if isinstance(name, str):
        return THEMES.get(name.lower(), LIGHT_THEME)
    return DARK_THEME if name else LIGHT_THEME

def _resolve_mode(name: bool | str) -> str:
    """Normalize ``name`` to ``light`` or ``dark``."""
    if isinstance(name, str):
        mode = name.lower()
        return mode if mode in THEMES else "light"
    return "dark" if name else "light"


def inject_global_styles(theme: bool | str = True) -> None:
    """Inject global CSS variables, fonts, and base styles.

    This loads the Inter font and FontAwesome icons, sets root CSS
    variables (``--bg``, ``--card``, ``--accent``, ``--text``, etc.)
    and adds foundational styling. It runs only once per session.
    """
    mode = _resolve_mode(theme)
    st.session_state["_theme"] = mode

    if st.session_state.get("_global_styles_injected"):
        return

    th = get_theme(mode)
    html = f"""
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

    body {{
        background: var(--bg) !important;
        color: var(--text);
        font-family: var(--font);
        transition: background var(--transition);
    }}

    .card {{
        background: var(--card);
    }}

    a {{
        color: var(--accent);
    }}

    .text-muted {{
        color: var(--text-muted);
    }}

    button, .stButton > button {{
        border-radius: var(--radius);
    }}

    @keyframes fade-in {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    </style>
    """

    st.markdown(html, unsafe_allow_html=True)
    st.session_state["_global_styles_injected"] = True

    <style>
    :root {{
        --bg: {th.bg};
        --card: {th.card};
        --accent: {th.accent};
        --text: {th.text};
        --font: 'Inter', sans-serif;
    }}
    body {{
        background: var(--bg) !important;
        color: var(--text);
        font-family: var(--font);
        transition: background var(--transition, 0.4s ease);
    }}
    /* Glassmorphic card styles */
    .glass-card {{
        background: var(--card);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: var(--radius, 1rem);
        padding: 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }}
    </style>
    """
    st.markdown(html, unsafe_allow_html=True)
    st.session_state["_global_styles_injected"] = True


def apply_theme(name: bool | str = True) -> None:
    """Legacy alias for :func:`inject_global_styles`."""
    inject_global_styles(name)


def inject_modern_styles(theme: bool | str = True) -> None:
    """Inject modern extras, ensuring global styles are present."""
    mode = _resolve_mode(theme)
    inject_global_styles(mode)
    if st.session_state.get("_styles_injected"):
        return

    extra = """
    <style>
    /* Accent gradient buttons */
    .insta-btn, .linkedin-btn {
        padding: 0.6rem 1.2rem;
        border: none;
        border-radius: var(--radius, 1rem);
        color: white !important;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s ease;
    }
    .insta-btn {
        background: linear-gradient(45deg, #F58529, #DD2A7B, #8134AF);
    }
    .linkedin-btn {
        background: var(--accent);
    }
    .insta-btn:active, .linkedin-btn:active {
        transform: scale(0.97);
    }
    </style>
    """
    st.markdown(extra, unsafe_allow_html=True)
    st.session_state["_theme_initialized"] = True


def inject_modern_styles(theme: bool | str = True) -> None:
    """Backward compatible wrapper for :func:`initialize_theme`."""
    initialize_theme(theme)


def inject_global_styles(theme: bool | str | None = None) -> None:
    """Inject modern styles and global fonts/icons once per session."""
    mode = theme if theme is not None else st.session_state.get("_theme", "light")
    inject_modern_styles(mode)
    if not st.session_state.get("_global_styles_loaded"):
        st.markdown(
            (
                '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
                '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&'
                'display=swap" rel="stylesheet">\n'
                '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/'
                'css/all.min.css">\n'
            ),
            unsafe_allow_html=True,
        )
        st.session_state["_global_styles_loaded"] = True


def set_theme(name: str) -> None:
    """Store ``name`` in session state and inject styles."""
    mode = _resolve_mode(name)
    st.session_state["_theme"] = mode
    initialize_theme(mode)

def initialize_theme(name: bool | str = True) -> None:
    """Initialize theme and styles in a single call."""
    set_theme(name if isinstance(name, (str, bool)) else "light")


def initialize_theme(mode: bool | str = True) -> None:
    """Initialize the app theme and inject all global styles.

    This is a thin wrapper around `inject_global_styles` to preserve
    compatibility with older code or usages that expect this function name.
    """
    inject_global_styles(mode)

def get_accent_color() -> str:
    """Return the accent color for the current theme."""
    try:
        mode = st.session_state.get("_theme", "light")
    except Exception:
        mode = "light"
    return get_theme(mode).accent


__all__ = [
    "apply_theme",
    "set_theme",
    "initialize_theme",
    "inject_modern_styles",
    "inject_global_styles",
    "get_accent_color",
    "initialize_theme",
]
