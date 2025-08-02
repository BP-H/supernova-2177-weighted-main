# ui.py

# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for superNova_2177."""

import os
import sys
from pathlib import Path
import streamlit as st
import logging

# --- Setup Project Path ---
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO)

# --- Safe Imports with Fallbacks ---
try:
    from streamlit_helpers import (
        alert, header, theme_selector, safe_container
    )
    from frontend.theme import apply_theme
    from modern_ui import apply_modern_styles, render_modern_header, render_stats_section
    from status_indicator import render_status_icon
except ImportError as e:
    st.error(f"A critical component failed to import: {e}. The app may not function correctly.")
    def alert(msg, type="info"): st.warning(msg)
    def header(txt): st.header(txt)
    def theme_selector(): pass
    def safe_container(): return st.container()
    def apply_theme(theme="light"): pass
    def apply_modern_styles(): pass
    def render_modern_header(): st.title("superNova_2177")
    def render_stats_section(stats={}): pass
    def render_status_icon(): pass

# --- Page Loading Logic ---
PAGES_DIR = Path(__file__).resolve().parent / "pages"

def load_page(page_name: str):
    """Dynamically imports and runs a page module."""
    try:
        if not page_name or not page_name.replace("_", "").isalnum():
             st.error(f"Invalid page name: {page_name}")
             return
        
        module = __import__(f"pages.{page_name}", fromlist=["main"])
        
        if hasattr(module, 'main'):
            module.main()
        elif hasattr(module, 'render'):
            module.render()
        else:
            st.warning(f"Page '{page_name}' has no main() or render() function.")

    except ImportError:
        st.error(f"Could not find page: {page_name}.py")
    except Exception as e:
        st.error(f"Error loading page '{page_name}': {e}")
        st.exception(e)

# --- Main Application Logic ---
def main() -> None:
    """Entry point with comprehensive error handling and modern UI."""
    st.set_page_config(
        page_title="superNova_2177",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.session_state.setdefault("theme", "light")
    apply_theme(st.session_state.theme)
    apply_modern_styles()
    
    render_modern_header()

    # --- Sidebar Rendering ---
    with st.sidebar:
        st.title("🌌 superNova")
        
        PAGES = {
            "Feed": "feed",
            "Chat": "chat",
            "Messages": "messages_center",
            "Agents": "agents",
            "Voting": "voting",
            "Profile": "profile",
            "Music": "resonance_music",
        }
        
        page_selection = st.radio("Navigation", list(PAGES.keys()))
        
        st.divider()
        header("Settings")
        theme_selector()
        render_status_icon()

    # --- Main Content Area ---
    page_to_load = PAGES.get(page_selection)
    if page_to_load:
        load_page(page_to_load)
    else:
        header("Welcome to superNova_2177")
        alert("Please select a page from the navigation bar.", type="info")
        render_stats_section()

if __name__ == "__main__":
    main()
