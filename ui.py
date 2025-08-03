# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for superNova_2177."""
import sys
from pathlib import Path
import streamlit as st
import importlib.util
import numpy as np  # For random low stats

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
        st.error(f"Page missing: {page_name}.py not found - add it to pages/.")
        st.write(f"Placeholder for {page_name.capitalize()} (add main() to {page_name}.py).")
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
            st.write(f"Placeholder for {page_name.capitalize()} (add main() to {page_name}.py).")
    except Exception as e:
        st.error(f"Error loading {page_name}: {e}")
        st.exception(e)

# Main - Green sidebar exact + orange bottom, modern buttons (small, rounded, blue hover)
def main() -> None:
    st.set_page_config(
        page_title="superNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("conversations", {})  # Fix NoneType
    initialize_theme(st.session_state["theme"])

    # CSS for dark gray (#1a1a1a background, white text, blue #4f8bf9 accents/hover), hide old sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none !important;}  # Hide old default sidebar
            [data-testid="stSidebar"] {
                background-color: #1a1a1a;  # Dark gray
                color: white;
                border-radius: 10px;  # Square curve
                padding: 20px;
                margin: 10px;
                width: 300px;  # Wider
            }
            .stSidebar > div {text-align: center;}  # Center profile
            .stSidebar hr {border-color: #333;}
            .stSidebar button {background-color: #282828; color: white; border-radius: 5px; padding: 8px; margin: 5px 0; width: 100%; cursor: pointer; border: none; font-size: 14px;}  # Small modern
            .stSidebar button:hover {background-color: #4f8bf9; color: white;}  # Blue hover
            .bottom-nav {position: fixed; bottom: 0; width: 100%; background-color: #1a1a1a; padding: 10px; display: flex; justify-content: space-around; z-index: 100;}
            .bottom-nav button {background: none; border: none; color: white; cursor: pointer; font-size: 20px; padding: 10px;}
            .bottom-nav button:hover {color: #4f8bf9;}  # Blue hover
            .stApp {background-color: #0E1117; color: white;}  # Main dark
        </style>
    """, unsafe_allow_html=True)

    # Green sidebar - Exact, small buttons clickable, low random stats
    with st.sidebar:
        # Profile top
        st.image("https://via.placeholder.com/100?text=Profile+Pic", use_container_width=True)  # Placeholder
        st.write("Taha Gungor")
        st.write("CEO / AccessAI.Tech")
        st.write("Artist / 0111 ≡ ...")
        st.write("New York, New York, United States")
        st.write("AccessAI.Tech")
        st.divider()
        st.write(f"{np.random.randint(100, 200)} profile viewers (placeholder)")
        st.write(f"{np.random.randint(400, 600)} post impressions (placeholder)")
        st.divider()
        # Manage pages - small clickable buttons
        st.write("Manage pages")
        if st.button("AccessAI.Tech"):
            load_page("accessai")
        if st.button("supernova_2177"):
            load_page("supernova_2177")
        if st.button("GLOBALRUNWAY"):
            load_page("globalrunway")
        if st.button("Show all >"):
            st.write("All pages (placeholder list).")
        st.divider()
        # Navigation - small buttons, clickable
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
        theme_selector()  # Theme bottom

    # Main content - Load selected page (from buttons)
    st.write("Main Content Area - Select from sidebar.")

    # Orange bottom nav - Icons clickable, mapped to pages (4 buttons, no jobs)
    bottom_cols = st.columns(4)
    with bottom_cols[0]:
        if st.button("🏠 Home"):
            load_page("feed")
    with bottom_cols[1]:
        if st.button("📹 Video"):
            load_page("video_chat")
    with bottom_cols[2]:
        if st.button("👥 My Network"):
            load_page("social")
    with bottom_cols[3]:
        if st.button("🔔 Notifications"):
            load_page("messages")

if __name__ == "__main__":
    main()
