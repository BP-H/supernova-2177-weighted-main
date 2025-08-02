# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for superNova_2177."""
import sys
from pathlib import Path
import streamlit as st

# Setup path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Safe imports
try:
    from streamlit_helpers import alert, header, theme_selector, safe_container, get_active_user, ensure_active_user
    from frontend.theme import initialize_theme, apply_theme  # Added alias for compat
except ImportError as e:
    st.error(f"Critical import failed: {e}. App may not function.")
    # Dummies
    def alert(msg, type="info"): st.warning(msg)
    def header(txt): st.header(txt)
    def theme_selector(): pass
    def safe_container(): return st.container()
    def get_active_user(): return "guest"
    def ensure_active_user(): pass
    def initialize_theme(theme="light"): pass
    def apply_theme(theme="light"): pass  # Dummy for alias

# Page loader (fixes "Could not find page")
def load_page(page_name: str):
    try:
        module_path = Path(__file__).parent.parent / "pages" / f"{page_name}.py"
        if not module_path.exists():
            st.error(f"Page file missing: {module_path}")
            return
        import importlib.util
        spec = importlib.util.spec_from_file_location(page_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'main'):
            module.main()
        elif hasattr(module, 'render'):
            module.render()
        else:
            st.warning(f"No entry function in {page_name}.py")
    except Exception as e:
        st.error(f"Error loading {page_name}: {e}")

# Main
def main() -> None:
    st.set_page_config(
        page_title="superNova_2177",
        layout="wide",
        initial_sidebar_state="collapsed"  # Fixes double sidebars
    )
    st.session_state.setdefault("theme", "light")
    initialize_theme(st.session_state["theme"])  # Or apply_theme for compat

    with st.sidebar:
        st.title("🌌 superNova")
        PAGES = {
            "Feed": "feed",
            "Chat": "chat",
            "Messages": "messages",
            "Agents": "agents",
            "Voting": "voting",
            "Profile": "profile",
            "Music": "music",
        }
        page_selection = st.radio("Navigation", list(PAGES.keys()))
        theme_selector()

    page_to_load = PAGES.get(page_selection)
    if page_to_load:
        load_page(page_to_load)
    else:
        st.write("Select a page.")

if __name__ == "__main__":
    main()
