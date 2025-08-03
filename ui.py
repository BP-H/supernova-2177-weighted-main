# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for supernNova_2177."""
import sys
from pathlib import Path
import streamlit as st
import importlib.util
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
sys.path.insert(0, str(Path("/mount/src") if 'mount' in str(Path(__file__)) else Path(__file__).parent))

# Handle imports with fallbacks
try:
    from streamlit_helpers import alert, header, theme_selector, safe_container
    from frontend.theme import initialize_theme
except ImportError as e:
    # Fallback functions if imports fail
    def alert(text): st.info(text)
    def header(text): st.header(text)
    def theme_selector(): st.selectbox("Theme", ["dark"], key="theme")
    def safe_container(): return st.container()
    def initialize_theme(theme): pass
    st.warning(f"Some imports failed: {e}, using fallbacks.")

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
            st.write(f"Placeholder for {page_name.capitalize()}")
    except Exception as e:
        st.error(f"Error loading {page_name}: {e}")

def main() -> None:
    st.set_page_config(
        page_title="supernNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("conversations", {})
    st.session_state.setdefault("current_page", "feed")
    initialize_theme(st.session_state["theme"])

    # CRITICAL CSS FOR STICKY LAYOUT
    st.markdown("""
        <style>
            /* Base styles */
            .stApp {
                background-color: #0a0a0a;
            }

            /* Hide default navigation */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }

            /* STICKY SIDEBAR */
            section[data-testid="stSidebar"] {
                position: sticky !important;
                top: 0 !important;
                height: 100vh !important;
                background-color: #18181b;
                border-right: 1px solid #333;
                overflow-y: auto;
            }

            /* Left-align sidebar content */
            [data-testid="stSidebarUserContent"] {
                display: flex;
                flex-direction: column;
                align-items: flex-start !important;
                text-align: left !important;
            }

            /* Sidebar buttons */
            [data-testid="stSidebar"] .stButton button {
                display: flex;
                justify-content: flex-start;
                align-items: center;
                background-color: rgba(255,255,255,0.05);
                color: white;
                border-radius: 20px;
                padding: 8px 12px;
                margin: 4px 0;
                width: 100%;
                border: none;
                font-size: 14px;
                text-align: left;
            }

            [data-testid="stSidebar"] .stButton button:hover {
                background-color: rgba(255,20,147,0.2);
                box-shadow: 0 0 5px #ff1493;
            }

            /* STICKY SEARCH BAR */
            .sticky-search {
                position: sticky;
                top: 0;
                background-color: #0a0a0a;
                padding: 1rem 0;
                z-index: 99;
                border-bottom: 1px solid #333;
                margin-bottom: 1rem;
            }

            /* FIXED BOTTOM NAV */
            .bottom-nav-container {
                position: fixed !important;
                bottom: 0 !important;
                left: 0 !important;
                right: 0 !important;
                background-color: #18181b;
                border-top: 1px solid #333;
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
                padding: 10px 0;
                z-index: 1000;
                display: flex;
                justify-content: space-around;
                align-items: center;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
            }

            /* Bottom nav buttons */
            .bottom-nav-container .stButton > button {
                background: transparent !important;
                border: none !important;
                color: #a0a0a0 !important;
                font-size: 12px !important;
                padding: 5px !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
            }

            .bottom-nav-container .stButton > button:hover {
                color: #ff1493 !important;
            }

            /* Badge */
            .notification-badge {
                position: absolute;
                background: #ff1493;
                color: white;
                border-radius: 50%;
                padding: 2px 6px;
                font-size: 10px;
                top: 5px;  /* Adjusted for better alignment */
                right: 25%; /* Adjusted for better alignment */
            }

            /* Main content padding */
            .main .block-container {
                padding-bottom: 100px !important; /* Space for bottom nav */
                padding-top: 0 !important; /* Remove any extra top padding */
            }

            /* Content card */
            .content-card {
                background-color: #1f1f1f;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
            }

            .content-card:hover {
                border: 1px solid #ff1493;
            }
        </style>
    """, unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.markdown("""
            <svg width="200" height="50" viewBox="0 0 200 50" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="50" fill="#FF00FF"/>
                <text x="10" y="35" font-family="Arial" font-size="20" font-weight="bold" fill="white">supernNova_2177</text>
            </svg>
        """, unsafe_allow_html=True)

        st.image("https://via.placeholder.com/100?text=Profile+Pic", width=100)
        st.subheader("taha gungor")
        st.caption("ceo / test_tech")
        st.caption("artist / 0111 ≡ ...")
        st.caption("New York, New York, United States")
        st.caption("test_tech")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Profile viewers", np.random.randint(2000, 2500))
        with col2:
            st.metric("Post impressions", np.random.randint(1400, 1600))
        st.divider()

        st.subheader("Manage pages")
        if st.button("🔬 test_tech", key="manage_test_tech", use_container_width=True):
            st.session_state.current_page = "test_tech"
            st.rerun()
        if st.button("🌌 supernNova_2177", key="manage_supernova", use_container_width=True):
            st.session_state.current_page = "supernova_2177"
            st.rerun()
        if st.button("✈️ GLOBALRUNWAY", key="manage_globalrunway", use_container_width=True):
            st.session_state.current_page = "globalrunway"
            st.rerun()
        if st.button("📂 Show all >", key="manage_showall", use_container_width=True):
            st.write("All pages (placeholder list).")
        st.divider()

        if st.button("🔮 Enter Metaverse", key="nav_metaverse", use_container_width=True):
            st.session_state.current_page = "enter_metaverse"
            st.rerun()
        st.caption("Mathematically sucked into a supernNova_2177 void!")

        st.subheader("Premium features")
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.session_state.current_page = "settings"
            st.rerun()
        theme_selector()
        st.divider()

        st.subheader("Navigation")
        nav_buttons = [
            ("Feed", "feed"), ("Chat", "chat"), ("Messages", "messages"),
            ("Agents", "agents"), ("Voting", "voting"), ("Profile", "profile"),
            ("Music", "music")
        ]
        for label, page_key in nav_buttons:
            if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

    # MAIN CONTENT AREA
    # *** THIS IS THE FIX ***
    # The sticky search bar is placed directly in the main column, NOT in a separate container.
    st.markdown('<div class="sticky-search">', unsafe_allow_html=True)
    st.text_input("Search", key="search_bar", placeholder="Search posts, people, jobs...")
    st.markdown('</div>', unsafe_allow_html=True)

    # Load page content
    load_page(st.session_state.current_page)

    # FIXED BOTTOM NAV
    st.markdown('<div class="bottom-nav-container">', unsafe_allow_html=True)
    cols = st.columns(5)

    with cols[0]:
        if st.button("🏠\nHome", key="bottom_home"):
            st.session_state.current_page = "feed"
            st.rerun()

    with cols[1]:
        if st.button("📹\nVideo", key="bottom_video"):
            st.session_state.current_page = "video_chat"
            st.rerun()

    with cols[2]:
        if st.button("👥\nMy Network", key="bottom_network"):
            st.session_state.current_page = "social"
            st.rerun()

    with cols[3]:
        # The badge is placed after the button so it can be positioned 'absolute' relative to it
        if st.button("🔔\nNotifications", key="bottom_notifications"):
            st.session_state.current_page = "messages"
            st.rerun()
        st.markdown('<div style="position: relative;"><span class="notification-badge">8</span></div>', unsafe_allow_html=True)

    with cols[4]:
        if st.button("💼\nJobs", key="bottom_jobs"):
            st.session_state.current_page = "jobs"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
