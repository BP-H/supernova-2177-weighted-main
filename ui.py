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

# Suppress potential deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Path for Cloud/local
sys.path.insert(0, str(Path("/mount/src") if 'mount' in str(Path(__file__)) else Path(__file__).parent))

# Imports with fallback
try:
    from streamlit_helpers import alert, header, theme_selector, safe_container
    from frontend.theme import initialize_theme
except ImportError as e:
    # Fallback implementations
    def alert(text): st.info(text)
    def header(text): st.header(text)
    def theme_selector(): 
        return st.selectbox("Theme", ["Dark", "Light"], key="theme_select")
    def safe_container(): return st.container()
    def initialize_theme(theme): pass
    st.warning(f"Some imports failed: {e}, using fallbacks.")

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

    # FIXED CSS - Properly implements sticky positioning and alignment
    st.markdown("""
        <style>
            /* --- Base Styles --- */
            .stApp {
                background-color: #0a0a0a;
                color: white;
            }
            
            /* --- Hide default Streamlit navigation --- */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            
            /* --- STICKY SIDEBAR (Left Panel) --- */
            [data-testid="stSidebar"] {
                position: sticky !important;
                top: 0 !important;
                height: 100vh !important;
                overflow-y: auto !important;
                background-color: #18181b !important;
                border-right: 1px solid #333 !important;
                padding: 20px !important;
                z-index: 50 !important;
            }
            
            /* --- LEFT ALIGN all sidebar content --- */
            [data-testid="stSidebarUserContent"] {
                display: flex !important;
                flex-direction: column !important;
                align-items: flex-start !important;  /* LEFT ALIGN */
                text-align: left !important;
            }
            
            /* Ensure all sidebar children are left-aligned */
            [data-testid="stSidebar"] * {
                text-align: left !important;
            }
            
            /* Sidebar buttons with left-aligned content */
            [data-testid="stSidebar"] .stButton > button {
                display: flex !important;
                justify-content: flex-start !important;  /* LEFT ALIGN content */
                align-items: center !important;
                text-align: left !important;
                background-color: rgba(255,255,255,0.05) !important;
                color: white !important;
                border-radius: 20px !important;
                padding: 8px 12px !important;
                margin: 5px 0 !important;
                width: 100% !important;
                border: none !important;
                font-size: 14px !important;
                transition: all 0.2s !important;
            }
            
            [data-testid="stSidebar"] .stButton > button:hover {
                background-color: rgba(255,20,147,0.2) !important;
                box-shadow: 0 0 8px #ff1493 !important;
            }
            
            /* --- STICKY SEARCH BAR --- */
            .sticky-search-container {
                position: sticky !important;
                top: 0 !important;
                background-color: #0a0a0a !important;
                padding: 1rem !important;
                z-index: 999 !important;
                border-bottom: 1px solid #333 !important;
                margin-bottom: 1rem !important;
            }
            
            /* Style the search input */
            .sticky-search-container input {
                background-color: #282828 !important;
                border-radius: 20px !important;
                border: 1px solid #333 !important;
                color: white !important;
                padding: 8px 16px !important;
            }
            
            /* --- FIXED BOTTOM NAVIGATION --- */
            .bottom-nav-container {
                position: fixed !important;
                bottom: 0 !important;
                left: 0 !important;
                right: 0 !important;
                background-color: #18181b !important;
                border-top: 1px solid #333 !important;
                padding: 10px 20px !important;
                z-index: 1000 !important;
                display: flex !important;
                justify-content: space-around !important;
                align-items: center !important;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.5) !important;
            }
            
            /* Bottom nav buttons - ensure horizontal layout */
            .bottom-nav-container .stButton > button {
                background: transparent !important;
                border: none !important;
                color: #a0a0a0 !important;
                font-size: 12px !important;
                padding: 5px 10px !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                min-width: 60px !important;
                transition: color 0.2s !important;
            }
            
            .bottom-nav-container .stButton > button:hover {
                color: #ff1493 !important;
            }
            
            /* Notification badge */
            .notification-badge {
                position: relative !important;
                display: inline-block !important;
            }
            
            .notification-badge .badge {
                position: absolute !important;
                top: -5px !important;
                right: -5px !important;
                background: #ff1493 !important;
                color: white !important;
                border-radius: 50% !important;
                padding: 2px 6px !important;
                font-size: 10px !important;
                font-weight: bold !important;
            }
            
            /* --- Main content padding to avoid overlap --- */
            .main .block-container {
                padding-top: 0 !important;
                padding-bottom: 100px !important;  /* Space for bottom nav */
            }
            
            /* Content cards */
            .content-card {
                background-color: #1f1f1f !important;
                border: 1px solid #333 !important;
                border-radius: 8px !important;
                padding: 16px !important;
                margin-bottom: 16px !important;
                transition: border-color 0.2s !important;
            }
            
            .content-card:hover {
                border-color: #ff1493 !important;
            }
            
            /* Ensure columns in bottom nav stay horizontal */
            .bottom-nav-container > div {
                display: flex !important;
                flex-direction: row !important;
                justify-content: space-around !important;
                width: 100% !important;
            }
            
            /* Force horizontal layout for bottom nav columns */
            .bottom-nav-container [data-testid="column"] {
                flex: 1 !important;
                display: flex !important;
                justify-content: center !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR CONTENT ---
    with st.sidebar:
        # Logo
        st.markdown("""
            <svg width="200" height="50" viewBox="0 0 200 50" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="50" fill="#FF00FF"/>
                <text x="10" y="35" font-family="Arial" font-size="20" font-weight="bold" fill="white">supernNova_2177</text>
            </svg>
        """, unsafe_allow_html=True)
        
        # Profile
        st.image("https://via.placeholder.com/100?text=Profile+Pic", width=100)
        st.subheader("taha gungor")
        st.caption("ceo / test_tech")
        st.caption("artist / 0111 ≡ ...")
        st.caption("New York, New York, United States")
        st.caption("test_tech")
        st.divider()
        
        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Profile viewers", np.random.randint(2000, 2500))
        with col2:
            st.metric("Post impressions", np.random.randint(1400, 1600))
        st.divider()
        
        # Manage pages
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
        
        # Special sections
        if st.button("🔮 Enter Metaverse", key="nav_metaverse", use_container_width=True):
            st.session_state.current_page = "enter_metaverse"
            st.rerun()
        st.caption("Mathematically sucked into a supernNova_2177 void – stay tuned for 3D immersion!")
        
        st.subheader("Premium features")
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.session_state.current_page = "settings"
            st.rerun()
        theme_selector()
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        nav_items = [
            ("Feed", "feed"),
            ("Chat", "chat"),
            ("Messages", "messages"),
            ("Agents", "agents"),
            ("Voting", "voting"),
            ("Profile", "profile"),
            ("Music", "music")
        ]
        
        for label, page in nav_items:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()

    # --- MAIN CONTENT AREA ---
    
    # Sticky search bar at top
    st.markdown('<div class="sticky-search-container">', unsafe_allow_html=True)
    st.text_input("Search", key="search_bar", placeholder="Search posts, people, jobs...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Load page content
    load_page(st.session_state.current_page)
    
    # --- FIXED BOTTOM NAVIGATION ---
    st.markdown('<div class="bottom-nav-container">', unsafe_allow_html=True)
    
    # Create 5 columns for bottom nav items
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
        # Notifications with badge
        st.markdown('<div class="notification-badge">', unsafe_allow_html=True)
        if st.button("🔔\nNotifications", key="bottom_notifications"):
            st.session_state.current_page = "messages"
            st.rerun()
        st.markdown('<span class="badge">8</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with bottom_cols[4]:
        if st.button("💼\nJobs", key="bottom_jobs"):
            st.session_state.current_page = "jobs"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
