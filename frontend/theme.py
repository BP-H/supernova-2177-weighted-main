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
    text_muted: str
    radius: str = "1rem"
    transition: str = "0.4s ease"

    def css_vars(self) -> str:
        """Return CSS variable declarations for this theme."""
        return "\n    ".join([
            f"--bg: {self.bg};",
            f"--card: {self.card};",
            f"--accent: {self.accent};",
            f"--text-muted: {self.text_muted};",
            f"--radius: {self.radius};",
            f"--transition: {self.transition};",
        ])


# Modern “light” and “dark” palettes
LIGHT_THEME = ColorTheme(
    bg="#F0F2F6",
    card="#FFFFFF",
    accent="#0077B5",        # LinkedIn-blue accent
    text_muted="#666666",
)
DARK_THEME = ColorTheme(
    bg="#0A0F14",
    card="rgba(255,255,255,0.05)",
    accent="#00E5FF",        # Neon cyan
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


def get_global_css(theme: bool | str = True) -> str:
    """
    Return a `<style>` block setting :root CSS variables
    for the selected theme.
    """
    # resolve the theme into “light” or “dark”
    resolved = "dark" if theme is True else theme or "light"
    theme_obj = get_theme(resolved)
    return f"""<style>
:root {{
    {theme_obj.css_vars()}
}}

body {{
    background: var(--bg) !important;
    font-family: Helvetica, Arial, sans-serif;
    transition: background var(--transition);
}}

button, .stButton>button {{
    border-radius: var(--radius);
}}

@keyframes fade-in {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}
</style>"""


def apply_theme(name: bool | str = True) -> None:
    """
    Inject the global CSS variables for the given theme,
    and remember it in session state.
    """
    st.markdown(get_global_css(name), unsafe_allow_html=True)
    st.session_state["_theme"] = name


def inject_modern_styles(theme: bool | str = True) -> None:
    """
    Inject global CSS variables and modern card styles
    (glassmorphic + gradients + smooth fades).
    """
    if st.session_state.get("_styles_injected"):
        return

    apply_theme(theme)

    extra = """
    <style>
    /* Glassmorphic cards */
    .glass-card {
        background: var(--card);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: var(--radius);
        padding: 1rem;
        animation: fade-in var(--transition) forwards;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }

    /* Accent gradient buttons */
    .insta-btn, .linkedin-btn {
        padding: 0.6rem 1.2rem;
        border: none;
        border-radius: var(--radius);
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
    st.session_state["_styles_injected"] = True


def get_accent_color() -> str:
    """Return the accent color for the current theme."""
    return get_theme(st.session_state.get("_theme", "light")).accent
