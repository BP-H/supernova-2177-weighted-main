# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for supernNova_2177."""
import sys
from pathlib import Path
import streamlit as st
import importlib.util
import numpy as np  # For random low stats
import warnings

# Suppress potential deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Path for Cloud/local
sys.path.insert(0, str(Path(__file__).parent / "mount/src")) if Path(__file__).parent.joinpath("mount/src").exists() else sys.path.insert(0, str(Path(__file__).parent))

# Imports
try:
    from streamlit_helpers import alert, header, theme_selector, safe_container
    from frontend.theme import initialize_theme
except ImportError as e:
    # Use fallback functions instead of stopping
    def alert(text): st.info(text)
    def header(text): st.header(text)
    def theme_selector(): st.selectbox("Theme", ["dark"], key="theme")
    def safe_container(): return st.container()
    def initialize_theme(theme): pass
    st.warning(f"Helpers import failed: {e}, using fallbacks.")

def load_page(page_name: str):
    # CORRECTED base_paths to include transcendental_resonance_frontend/pages
    base_paths = [
        Path("mount/src/pages"),
        Path(__file__).parent / "pages",
        Path(__file__).parent / "transcendental_resonance_frontend/pages"
    ]
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
            st.write(f"Placeholder for {page_name.capitalize()} (add main() to {page_name}.py)")
    except Exception as e:
        st.error(f"Error loading {page_name}: {e}")
        st.exception(e)

# Main - Dark theme with subtle pink polish, FIXED STICKY LAYOUT
def main() -> None:
    st.set_page_config(
        page_title="supernNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("conversations", {})  # Fix NoneType
    st.session_state.setdefault("current_page", "feed")  # Default page
    initialize_theme(st.session_state["theme"])

    # Fixed CSS - Invisible buttons (match background), hover mid-grey, uniform size, no wrapping, visible metric text, feed button text
    st.markdown("""
    <style>
        /* Hide Streamlit's top navigation tabs */
        [data-testid="stSidebarNav"] { display: none !important; }
        
        /* 🔥 STICKY SIDEBAR */
        [data-testid="stSidebar"] {
            position: sticky !important;
            top: 0 !important;
            height: 100vh !important;
            overflow-y: auto !important;
            background-color: #18181b !important;
            color: white !important;
            border-radius: 10px;
            padding: 20px;
            margin: 0px;
            width: 300px;
            z-index: 98;
        }
        
        /* 🔥 LEFT ALIGN SIDEBAR CONTENT */
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stButton,
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] > div {
            text-align: left !important;
        }
        
        /* 🔥 SIDEBAR BUTTONS - Invisible (match bg), hover mid-grey, uniform height, no wrap */
        [data-testid="stSidebar"] button {
            background-color: #18181b !important; /* Match sidebar bg for invisibility */
            color: white !important;
            padding: 8px 12px !important;
            margin: 5px 0 !important;
            width: 100% !important;
            height: 40px !important; /* Fixed height for uniformity */
            border: none !important;
            border-radius: 4px !important;
            font-size: 13px !important;
            display: flex !important;
            justify-content: flex-start !important;
            align-items: center !important;
            white-space: nowrap !important; /* Prevent text wrapping */
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: #2a2a2e !important; /* Mid between bg (#18181b) and white (#fff) */
            box-shadow: 0 0 5px rgba(255, 20, 147, 0.3) !important;
            outline: none !important; /* This is the key change */
        }
        
        /* 🔥 MAIN CONTENT AREA */
        .stApp {
            background-color: #0a0a0a !important;
            color: white !important;
        }
        .main .block-container {
            padding-top: 20px !important;
            padding-bottom: 90px !important;
        }
        
        /* Content cards */
        .content-card {
            border: 1px solid #333;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            transition: border 0.2s;
            color: white !important; /* Ensure text visible */
        }
        .content-card:hover {
            border: 1px solid #ff1493;
        }
        
        /* Metrics text visible */
        [data-testid="stMetricLabel"] {
            color: white !important;
        }
        [data-testid="stMetricValue"] {
            color: white !important;
        }
        
        /* Feed buttons text visible */
        .feed-button-container button {
            color: white !important; /* Ensure button text is white */
        }
        
        /* Profile pic circular */
        [data-testid="stSidebar"] img {
            border-radius: 50% !important;
            margin: 0 auto !important;
            display: block !important;
        }
        
        /* Search bar styling */
        [data-testid="stTextInput"] {
            background-color: #28282b !important;
            border-radius: 20px !important;
            border: 1px solid #28282b !important;
            padding: 8px !important;
            color: white !important;
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            [data-testid="stSidebar"] button {
                height: 35px !important;
                font-size: 12px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar - Search at top, profile pic circular, all in sidebar including notifications
    with st.sidebar:
        # Search bar at the very top
        st.text_input("Search", key="search_bar", placeholder="Search posts, people, companies...")

        # Logo
        st.markdown(f"""
            <svg width="200" height="50" viewBox="0 0 200 50" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="50" fill="#0a0a0a"/>
                <text x="10" y="35" font-family="Arial" font-size="20" font-weight="bold" fill="white">supernNova</text>
            </svg>
            """, unsafe_allow_html=True)
        
        # Profile pic (circular via CSS)
        st.image("https://via.placeholder.com/100?text=Profile+Pic", width=100)
        
        st.subheader("taha_gungor")
        st.caption("ceo / test_tech")
        st.caption("artist / will = ...")
        st.caption("New York, New York, United States")
        st.caption("test_tech")
        st.divider()
        st.metric("Profile viewers", np.random.randint(2000, 2500))
        st.metric("Post impressions", np.random.randint(1400, 1600))
        st.divider()
        
        # Manage pages with logical logos
        if st.button("🏠 Test Tech", key="manage_test_tech"):
            st.session_state.current_page = "test_tech"
            st.rerun()
        if st.button("✨ supernNova_2177", key="manage_supernova"):
            st.session_state.current_page = "supernova_2177"
            st.rerun()
        if st.button("🌍 GLOBALRUNWAY", key="manage_globalrunway"):
            st.session_state.current_page = "globalrunway"
            st.rerun()
        if st.button("🖼️ Show all >", key="manage_showall"):
            st.write("All pages (placeholder list).")
        st.divider()
        
        # Enter Metaverse (clickable)
        if st.button("🌌 Enter Metaverse", key="nav_metaverse"):
            st.session_state.current_page = "enter_metaverse"
            st.rerun()
        st.caption("Mathematically sucked into a supernNova_2177 void - stay tuned for 3D immersion")
        st.subheader("Premium features")
        
        # Settings clickable with theme nearby
        if st.button("⚙️ Settings", key="nav_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
        theme_selector()
        st.divider()
        
        # Navigation - small shaded buttons
        if st.button("📰 Feed", key="nav_feed"):
            st.session_state.current_page = "feed"
            st.rerun()
        if st.button("💬 Chat", key="nav_chat"):
            st.session_state.current_page = "chat"
            st.rerun()
        if st.button("📬 Messages", key="nav_messages"):
            st.session_state.current_page = "messages"
            st.rerun()
        if st.button("🤖 Agents", key="nav_agents"):
            st.session_state.current_page = "agents"
            st.rerun()
        if st.button("🗳️ Voting", key="nav_voting"):
            st.session_state.current_page = "voting"
            st.rerun()
        if st.button("👤 Profile", key="nav_profile"):
            st.session_state.current_page = "profile"
            st.rerun()
        if st.button("🎶 Music", key="nav_music"):
            st.session_state.current_page = "music"
            st.rerun()
        if st.button("✨ AI assist", key="nav_ai_assist"):
            st.session_state.current_page = "ai_assist"
            st.rerun()
        if st.button("🌀 Animate Gaussian", key="nav_animate_gaussian"):
            st.session_state.current_page = "animate_gaussian"
            st.rerun()
        if st.button("🚪 Login", key="nav_login"):
            st.session_state.current_page = "login"
            st.rerun()
        
        # Notifications and quick nav in sidebar
        st.divider()
        st.subheader("Quick Nav")
        if st.button("🏠 Home", key="quick_home"):
            st.session_state.current_page = "feed"
            st.rerun()
        if st.button("📹 Video", key="quick_video"):
            st.session_state.current_page = "video_chat"
            st.rerun()
        if st.button("👥 My Network", key="quick_network"):
            st.session_state.current_page = "social"
            st.rerun()
        if st.button("🔔 Notifications (8)", key="quick_notifications"):
            st.session_state.current_page = "messages"
            st.rerun()
        if st.button("💼 Jobs", key="quick_jobs"):
            st.session_state.current_page = "jobs"
            st.rerun()

    # Main content area - Load selected page
    with st.container():
        load_page(st.session_state.current_page)

if __name__ == "__main__":
    main()
