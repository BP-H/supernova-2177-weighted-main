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

# Main - Exact LinkedIn structure/colors
def main() -> None:
    st.set_page_config(
        page_title="superNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("conversations", {})  # Fix NoneType
    initialize_theme(st.session_state["theme"])

    # CSS for LinkedIn dark gray scheme (#1a1a1a background, white text, blue accents #4f8bf9)
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #1a1a1a;  # Gray dark
                color: white;
                border-radius: 10px;  # Square curve
                padding: 20px;
                margin: 10px;
                width: 300px;  # Wider
            }
            .stSidebar > div {text-align: center;}  # Center profile
            .stSidebar hr {border-color: #333;}
            .stSidebar button {background-color: #4f8bf9; color: white; border-radius: 5px; padding: 8px; margin: 5px 0; width: 100%; cursor: pointer;}
            .stSidebar button:hover {background-color: #3a6bb9;}
            .bottom-nav {position: fixed; bottom: 0; width: 100%; background-color: #1a1a1a; padding: 10px; display: flex; justify-content: space-around; z-index: 100;}
            .bottom-nav button {background: none; border: none; color: white; cursor: pointer; font-size: 20px; padding: 10px;}
            .bottom-nav button:hover {color: #4f8bf9;}
            .stApp {background-color: #0E1117; color: white;}  # Main area dark
        </style>
    """, unsafe_allow_html=True)

    # Green sidebar - Exact structure, clickable buttons
    with st.sidebar:
        # Profile pic as toggle button (click to open/close sidebar - Streamlit toggle via JS)
        st.markdown("""
            <script>
                let sidebar = document.querySelector('[data-testid="stSidebar"]');
                let toggleBtn = document.querySelector('.profile-pic-button');
                toggleBtn.addEventListener('click', () => {
                    sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
                });
            </script>
        """, unsafe_allow_html=True)
        st.image("https://via.placeholder.com/100", width=100, use_column_width=True)  # Placeholder pic - replace URL
        st.button("Taha Gungor", key="profile_toggle", help="Toggle sidebar")  # Toggle button
        st.write("CEO / AccessAI.Tech")
        st.write("Artist / 0111 ≡ ...")
        st.write("New York, New York, United States")
        st.write("AccessAI.Tech")
        st.divider()
        st.write("2,103 profile viewers")
        st.write("1,450 post impressions")
        st.divider()
        # Manage pages - clickable buttons
        st.write("Manage pages")
        if st.button("AccessAI.Tech"):
            load_page("accessai")  # Replace slug if exists
        if st.button("supernova_2177"):
            load_page("supernova")
        if st.button("GLOBALRUNWAY"):
            load_page("globalrunway")
        if st.button("Show all >"):
            st.write("All pages placeholder.")  # Link to all
        st.divider()
        # Navigation buttons - clickable to load pages
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

    # Orange bottom nav - Clickable icons, mapped to pages
    bottom_cols = st.columns(4)
    with bottom_cols[0]:
        if st.button("🏠 Home"):
            load_page("feed")
    with bottom_cols[1]:
        if st.button("📹 Video"):
            load_page("video_chat")  # If exists, else placeholder
    with bottom_cols[2]:
        if st.button("👥 My Network"):
            load_page("social")
    with bottom_cols[3]:
        if st.button("🔔 Notifications"):
            st.write("Notifications placeholder.")

if __name__ == "__main__":
    main()
