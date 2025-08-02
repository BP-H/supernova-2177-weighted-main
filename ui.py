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

# Loader
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
        st.write(f"Placeholder for {page_name.capitalize()}.")
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
            st.warning(f"No main/render in {page_name}.py.")
            st.write(f"Placeholder for {page_name.capitalize()}.")
    except Exception as e:
        st.error(f"Error loading {page_name}: {e}")
        st.exception(e)

# Main - LinkedIn-like
def main() -> None:
    st.set_page_config(
        page_title="superNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("conversations", {})  # Fix NoneType
    initialize_theme(st.session_state["theme"])

    # CSS for LinkedIn dark scheme and square sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #1a1a1a;  # Dark like LinkedIn
                color: white;
                border-radius: 10px;  # Square with curve
                padding: 20px;
                margin: 10px;
                width: 300px;  # Wider for profile
            }
            .stSidebar > div {text-align: center;}  # Center profile
            .stSidebar hr {border-color: #333;}
            .stSidebar a, .stSidebar button {color: white !important; text-decoration: none;}
            .bottom-nav {position: fixed; bottom: 0; width: 100%; background-color: #1a1a1a; padding: 10px; display: flex; justify-content: space-around; z-index: 100;}
            .bottom-nav button {background: none; border: none; color: white; cursor: pointer; font-size: 20px;}
        </style>
    """, unsafe_allow_html=True)

    # Green circled sidebar - Exact LinkedIn structure
    with st.sidebar:
        # Profile top
        st.image("https://via.placeholder.com/100", caption="Taha Gungor")  # Replace with your pic URL
        st.write("CEO / AccessAI.Tech")
        st.write("Artist / 0111 ≡ ...")
        st.write("New York, New York, United States")
        st.write("AccessAI.Tech")
        st.divider()
        st.write("2,103 profile viewers")
        st.write("1,450 post impressions")
        st.divider()
        # Manage pages - clickable to load pages
        st.write("Manage pages")
        if st.button("AccessAI.Tech"):
            load_page("accessai")  # Replace with actual page slug if exists
        if st.button("supernova_2177"):
            load_page("supernova")  # Replace
        if st.button("GLOBALRUNWAY"):
            load_page("globalrunway")  # Replace
        st.button("Show all >")  # Can link to all pages page
        st.divider()
        # Navigation as buttons (your pages)
        if st.button("Feed"):
            load_page("feed")
        if st.button("Chat"):
            load_page("chat")
        if st.button("Messages"):
            load_page("messages")
        if st.button("Agents"):
            load_page("agents")
        if st.button("Voting"):
            load_page("voting")
        if st.button("Profile"):
            load_page("profile")
        if st.button("Music"):
            load_page("music")
        st.divider()
        theme_selector()  # Theme at bottom

    # Main content - Load selected page (from buttons)
    st.write("Main Content Area - Select from sidebar.")

    # Orange bottom nav - Clickable icons mapped to pages
    bottom_cols = st.columns(5)
    with bottom_cols[0]:
        if st.button("🏠 Home"):
            load_page("feed")  # Map to Feed
    with bottom_cols[1]:
        if st.button("📹 Video"):
            load_page("video_chat")  # Map if exists, or placeholder
    with bottom_cols[2]:
        if st.button("👥 My Network"):
            load_page("social")
    with bottom_cols[3]:
        if st.button("🔔 Notifications"):
            st.write("Notifications placeholder.")
    with bottom_cols[4]:
        if st.button("💼 Jobs"):
            st.write("Jobs placeholder.")

if __name__ == "__main__":
    main()
