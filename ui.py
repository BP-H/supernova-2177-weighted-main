# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for superNova_2177."""
import sys
from pathlib import Path
import streamlit as st
import importlib.util

# Path for Cloud/local
sys.path.insert(0, str(Path("/mount/src") if 'mount' in str(Path(__file__)) else Path(__file__).parent))

# Imports
try:
    from streamlit_helpers import alert, header, theme_selector, safe_container
    from frontend.theme import initialize_theme
except ImportError as e:
    st.error(f"Critical import failed: {e}")
    st.stop()

# Loader with fallback (fixes "no main/render")
def load_page(page_name: str):
    base_paths = [Path("/mount/src/pages"), Path(__file__).parent / "pages"]
    module_path = None
    for base in base_paths:
        candidate = base / f"{page_name}.py"
        if candidate.exists():
            module_path = candidate
            break
    if not module_path:
        st.error(f"Page missing: {page_name}.py not found.")
        # Fallback content
        st.write(f"Placeholder for {page_name.capitalize()} page.")
        return
    try:
        spec = importlib.util.spec_from_file_location(page_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'main'):
            module.main()
        elif hasattr(module, 'render'):
            module.render()
        else:
            st.warning(f"No main/render in {page_name}.py - showing placeholder.")
            st.write(f"Placeholder for {page_name.capitalize()} page.")
    except Exception as e:
        st.error(f"Error loading {page_name}: {e}")
        st.exception(e)

# Main (sidebar restored with square style via st.radio + CSS)
def main() -> None:
    st.set_page_config(
        page_title="superNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"  # Keeps your sidebar visible
    )
    st.session_state.setdefault("theme", "light")
    initialize_theme(st.session_state["theme"])

    # Custom square sidebar style
    st.markdown("""
        <style>
            [data-testid="stSidebar"] > div:first-child {
                background-color: #1a1a1a;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

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
        st.divider()
        theme_selector()

    page_to_load = PAGES.get(page_selection)
    if page_to_load:
        load_page(page_to_load)
    else:
        st.write("Select a page.")

if __name__ == "__main__":
    main()
