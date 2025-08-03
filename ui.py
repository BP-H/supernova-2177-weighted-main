# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for supernNova_2177."""
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
# Loader with better fallback for missing pages
def load_page(page_name: str):
    base_paths = [Path("/mount/src/pages"), Path(__file__).parent / "pages"]
    module_path = None
    for base in base_paths:
        candidate = base / f"{page_name}.py"
        if candidate.exists():
            module_path = candidate
            break
    if not module_path:
        st.info(f"Page '{page_name}' is coming soon! Stay tuned for updates.")
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
# Main - Dark theme with subtle pink polish (accents on hover/logos), modern buttons with opacity shading
def main() -> None:
    st.set_page_config(
        page_title="supernNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("conversations", {}) # Fix NoneType
    st.session_state.setdefault("current_page", "feed") # Default page
    initialize_theme(st.session_state["theme"])
    # CSS updates: Uniform small buttons with 5% opacity shading, subtle pink accents (hover glow #ff1493), curved bottom nav aligned like LinkedIn
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
            .stSidebar button {background-color: rgba(255,255,255,0.05); /* 5% opacity shading */ color: white; border-radius: 20px; padding: 6px 12px; /* Smaller size */ margin: 5px 0; width: 100%; cursor: pointer; border: none; font-size: 13px;} /* Modern non-90s */
            .stSidebar button:hover {background-color: rgba(255,20,147,0.2); color: white; box-shadow: 0 0 5px #ff1493;} /* Modern pink glow hover */
            .bottom-nav {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #0a0a0a; /* Dark black */
                padding: 8px 0; /* Smaller padding for alignment */
                display: flex;
                justify-content: space-around;
                z-index: 100;
                box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
                border-top-left-radius: 20px; border-top-right-radius: 20px; /* Curved */
            }
            .bottom-nav button {background: none; border: none; color: #a0a0a0; cursor: pointer; font-size: 12px; /* Smaller labels */ padding: 2px 0; display: flex; flex-direction: column; align-items: center; min-width: 60px;} /* Even spacing like LinkedIn */
            .bottom-nav button .stButton > button {font-size: 20px; /* Icons size */ margin-bottom: 2px;} /* Icon above label */
            .bottom-nav button:hover {color: #ff1493;} /* Pink hover */
            .bottom-nav .badge {background: #ff1493; color: white; border-radius: 50%; padding: 2px 6px; font-size: 12px; margin-top: -10px;} /* Pink badge */
            .stApp {background-color: #0a0a0a; color: white;} /* Main dark */
            /* Add padding to main content to avoid overlap with bottom nav */
            .block-container {padding-bottom: 80px;}
            /* Content card style for feed with subtle pink borders on hover */
            .content-card {background-color: #1f1f1f; border: 1px solid #333; border-radius: 8px; padding: 16px; margin-bottom: 16px; transition: border 0.2s;}
            .content-card:hover {border: 1px solid #ff1493;}
            .action-button {background-color: #282828; color: white; border-radius: 20px; padding: 8px 16px; border: none; font-weight: bold;}
            .action-button:hover {background-color: #ff1493;}
            /* Search bar polish */
            [data-testid="stTextInput"] {background-color: #282828; border-radius: 20px; padding: 8px;}
        </style>
    """, unsafe_allow_html=True)
    # Sidebar - LinkedIn-like, with better logos, new sections clickable, lowercase name
    with st.sidebar:
        # Profile top with avatar
        st.image("https://via.placeholder.com/100?text=Profile+Pic", width=100, caption="")  # Replace with real avatar URL
        st.subheader("taha gungor")
        st.caption("ceo / accessAI_tech")
        st.caption("artist / 0111 ≡ ...")
        st.caption("New York, New York, United States")
        st.caption("accessAI_tech")
        st.divider()
        st.metric("Profile viewers", np.random.randint(2000, 2500))
        st.metric("Post impressions", np.random.randint(1400, 1600))
        st.divider()
        # Manage pages with logical logos
        st.subheader("Manage pages")
        if st.button("🔬 accessAI_tech", key="manage_accessai"):
            st.session_state.current_page = "accessai"
            st.rerun()
        if st.button("🌌 supernNova_2177", key="manage_supernova"):
            st.session_state.current_page = "supernova_2177"
            st.rerun()
        if st.button("✈️ GLOBALRUNWAY", key="manage_globalrunway"):
            st.session_state.current_page = "globalrunway"
            st.rerun()
        if st.button("📂 Show all >", key="manage_showall"):
            st.write("All pages (placeholder list).")
        st.divider()
        # Enter Metaverse (clickable)
        if st.button("🔮 Enter Metaverse", key="nav_metaverse"):
            st.session_state.current_page = "enter_metaverse"
            st.rerun()
        st.caption("Mathematically sucked into a supernNova_2177 void – stay tuned for 3D immersion!")
        st.subheader("Premium features")
        # Settings clickable with theme nearby
        if st.button("⚙️ Settings", key="nav_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
        theme_selector()  # Theme near settings
        st.divider()
        # Navigation - small shaded buttons
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
    # Main content - Add search bar on top, then load page
    st.text_input("Search", key="search_bar", placeholder="Search posts, people, jobs...")
    load_page(st.session_state.current_page)
    # Bottom nav - Curved dark with labels aligned down like LinkedIn, pink badge on Notifications
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
        st.markdown('<div class="badge">8</div>', unsafe_allow_html=True)  # Pink badge
        if st.button("🔔\nNotifications", key="bottom_notifications"):
            st.session_state.current_page = "messages"
            st.rerun()
    with bottom_cols[4]:
        if st.button("💼\nJobs", key="bottom_jobs"):
            st.session_state.current_page = "jobs"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
if __name__ == "__main__":
    main()
