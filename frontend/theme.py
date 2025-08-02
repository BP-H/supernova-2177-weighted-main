# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Theme management for Streamlit UI (light/dark mode and global styles)."""

import streamlit as st

# Define base global styles that apply to both themes (e.g., hide Streamlit default widgets, set fonts)
_GLOBAL_CSS = """
<style>
/* Hide Streamlit default header (hamburger menu and page selection) and footer */
[data-testid="stHeader"] { visibility: hidden; height: 0px; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stFooter"] { display: none !important; }
/* (Optional) Custom global font or other base styles could go here */
</style>
"""

# Define Light and Dark theme CSS blocks
_LIGHT_THEME_CSS = """
<style>
/* Light theme background and text */
[data-testid="stAppViewContainer"] {
    background-color: #FFFFFF;
    color: #000000;
}
[data-testid="stSidebar"] {
    background-color: #F9F9F9;
}
[data-testid="stSidebar"] .stButton>button {
    background-color: #FFFFFF;
    color: #0A0A0A;
}
/* Ensure custom top bar (if any) matches light theme */
[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    background-color: #FFFFFF;
}
</style>
"""

_DARK_THEME_CSS = """
<style>
/* Dark theme background and text */
[data-testid="stAppViewContainer"] {
    background-color: #0E1117;
    color: #F0F2F6;
}
[data-testid="stSidebar"] {
    background-color: #1C1F26;
}
[data-testid="stSidebar"] .stButton>button {
    background-color: #2A2E36;
    color: #FFFFFF;
}
/* Ensure custom top bar and nav use dark background */
[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    background-color: #1C1F26;
}
</style>
"""

def inject_global_styles() -> None:
    """
    Inject theme-independent global CSS styles once. This includes hiding or styling 
    Streamlit's base UI elements (header, footer) to maintain a consistent look.
    """
    # Use a unique key to avoid injecting the same styles multiple times
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True, help=None)

def set_theme(theme: str) -> None:
    """
    Apply the CSS for the given theme ("light" or "dark"). This injects or updates 
    the style definitions so they don't accumulate on repeated toggles.
    """
    css = _DARK_THEME_CSS if theme.lower() == "dark" else _LIGHT_THEME_CSS
    # Inject theme-specific styles, using a consistent key to replace any previous theme CSS
    st.markdown(css, unsafe_allow_html=True, help=None, unsafe_allow_html=True, key="theme_style")

def initialize_theme(theme: str) -> None:
    """
    Ensure global styles are injected and set the initial theme.
    Call this at app startup to enforce the visual style before rendering content.
    """
    # Inject base global styles (only once; subsequent calls do nothing if already injected)
    if not st.session_state.get("_global_styles_injected"):
        inject_global_styles()
        st.session_state["_global_styles_injected"] = True
    # Apply the specified theme's styles
    set_theme(theme)

def apply_theme() -> None:
    """
    Legacy function for pages to re-apply the current theme.
    This will inject global styles (if not already) and set the CSS for the theme in session_state.
    """
    initialize_theme(st.session_state.get("theme", "light"))
