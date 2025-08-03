# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for superNova_2177."""
import sys
from pathlib import Path
import streamlit as st
import importlib.util
import numpy as np # For random low stats
import warnings
# Suppress potential deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
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
# Main - Dark theme like LinkedIn, modern buttons (small, rounded, blue hover)
def main() -> None:
    st.set_page_config(
        page_title="superNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("conversations", {}) # Fix NoneType
    st.session_state.setdefault("current_page", "feed") # Default page
    initialize_theme(st.session_state["theme"])
    # CSS for LinkedIn-like dark theme (dark gray sidebar, black bottom, blue accents/hover), hide old sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none !important;} /* Hide old default sidebar */
            [data-testid="stSidebar"] {
                background-color: #18181b; /* Dark gray like LinkedIn */
                color: white;
                border-radius: 10px; /* Square curve */
                padding: 20px;
                margin: 10px;
                width: 300px; /* Wider */
            }
            .stSidebar > div {text-align: left;} /* Align left for professional look */
            .stSidebar hr {border-color: #333;}
            .stSidebar button {background-color: #282828; color: white; border-radius: 20px; padding: 8px 16px; margin: 5px 0; width: 100%; cursor: pointer; border: none; font-size: 14px;} /* Pill-shaped modern */
            .stSidebar button:hover {background-color: #0a66c2; color: white;} /* LinkedIn blue hover */
            .bottom-nav {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #0a0a0a; /* Dark black */
                padding: 10px;
                display: flex;
                justify-content: space-around;
                z-index: 100;
                box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
            }
            .bottom-nav button {background: none; border: none; color: #a0a0a0; cursor: pointer; font-size: 16px; padding: 5px; display: flex; flex-direction: column; align-items: center;}
            .bottom-nav button:hover {color: #0a66c2;} /* Blue hover */
            .stApp {background-color: #0a0a0a; color: white;} /* Main dark */
            /* Add padding to main content to avoid overlap with bottom nav */
            .block-container {padding-bottom: 80px;}
            /* Content card style for feed */
            .content-card {background-color: #1f1f1f; border: 1px solid #333; border-radius: 8px; padding: 16px; margin-bottom: 16px;}
            .action-button {background-color: #282828; color: white; border-radius: 20px; padding: 8px 16px; border: none; font-weight: bold;}
            .action-button:hover {background-color: #0a66c2;}
        </style>
    """, unsafe_allow_html=True)
    # Sidebar - LinkedIn-like, with icons, added sections, no placeholders
    with st.sidebar:
        # Profile top with avatar
        st.image("https://via.placeholder.com/100?text=Profile+Pic", width=100, caption="")  # Replace with real avatar URL
        st.subheader("Taha Gungor")
        st.caption("CEO / AccessAI.Tech")
        st.caption("Artist / 0111 ≡ ...")
        st.caption("New York, New York, United States")
        st.caption("AccessAI.Tech")
        st.divider()
        st.metric("Profile viewers", np.random.randint(2000, 2500))
        st.metric("Post impressions", np.random.randint(1400, 1600))
        st.divider()
        # Manage pages with icons/logos
        st.subheader("Manage pages")
        if st.button("🔹 AccessAI.Tech", key="manage_accessai"):
            st.session_state.current_page = "accessai"
            st.rerun()
        if st.button("🌟 supernova_2177", key="manage_supernova"):
            st.session_state.current_page = "supernova_2177"
            st.rerun()
        if st.button("🌍 GLOBALRUNWAY", key="manage_globalrunway"):
            st.session_state.current_page = "globalrunway"
            st.rerun()
        if st.button("📂 Show all >", key="manage_showall"):
            st.write("All pages (placeholder list).")
        st.divider()
        # Added sections like LinkedIn
        st.subheader("Puzzle Games")
        st.subheader("Premium features")
        st.subheader("Settings")
        st.divider()
        # Navigation - pill buttons, clickable
        if st.button("Feed", key="nav_feed"):
            st.session_state.current_page = "feed"
            st.rerun()
        if st.button("Chat", key="nav_chat"):
            st.session_state.current_page = "chat"
            st.rerun()
        if st.button("Messages", key="nav_messages"):
            st.session_state.current_page = "messages"
            st.rerun()
        if st.button("Agents", key="nav_agents"):
            st.session_state.current_page = "agents"
            st.rerun()
        if st.button("Voting", key="nav_voting"):
            st.session_state.current_page = "voting"
            st.rerun()
        if st.button("Profile", key="nav_profile"):
            st.session_state.current_page = "profile"
            st.rerun()
        if st.button("Music", key="nav_music"):
            st.session_state.current_page = "music"
            st.rerun()
        st.divider()
        theme_selector() # Theme bottom
    # Main content - Load selected page
    load_page(st.session_state.current_page)
    # Dark bottom nav like LinkedIn - Icons with labels, added Jobs
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
    bottom_cols = st.columns(5)
    with bottom_cols[0]:
        if st.button("🏠\nHome", key="bottom_home"):
            st.session_state.current_page = "feed"
            st.rerun()
    with bottom_cols[1]:
        if st.button("📹\nVideo", key="bottom_video"):
            st.session_state.current_page = "video_chat"
            st.rerun()
    with bottom_cols[2]:
        if st.button("👥\nMy Network", key="bottom_network"):
            st.session_state.current_page = "social"
            st.rerun()
    with bottom_cols[3]:
        if st.button("🔔\nNotifications", key="bottom_notifications"):
            st.session_state.current_page = "messages"
            st.rerun()
    with bottom_cols[4]:
        if st.button("💼\nJobs", key="bottom_jobs"):
            st.session_state.current_page = "jobs"  # Add jobs.py if needed
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
if __name__ == "__main__":
    main()
