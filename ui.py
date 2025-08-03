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
import warnings  # Suppress potential deprecation warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Path for Cloud/local
sys.path.insert(0, str(Path("/mount/src") if 'mount' in str(Path(__file__)) else Path(__file__).parent))

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

# Loader with better fallback for missing pages, including fixes for login and animate_gaussian
def load_page(page_name: str):
    base_paths = [Path("/mount/src/pages"), Path(__file__).parent / "pages"]
    module_path = None
    for base in base_paths:
        candidate = base / f"{page_name}.py"
        if candidate.exists():
            module_path = candidate
            break
    if not module_path:
        if page_name in ["login", "animate_gaussian"]:
            st.info(f"Page '{page_name}' is under development. Showing placeholder.")
            if page_name == "login":
                st.write("Login Placeholder: Enter credentials here.")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.button("Login"):
                    st.success("Logged in (placeholder).")
            elif page_name == "animate_gaussian":
                st.write("Animate Gaussian Placeholder: Animation would go here.")
                st.image("https://via.placeholder.com/300x200?text=Gaussian+Animation", caption="Placeholder Animation")
        else:
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

    # 🎯 FIXED CSS - Rectangle buttons with tiny radius (4px), colorless (transparent), hover tint more pronounced (0.2 opacity pink), text left-aligned, no border
    st.markdown("""
        <style>
            .main { position: relative; }
            .sticky-search { position: fixed; top: 0; left: 0; width: 100%; background: #1a1a1a; padding: 10px; z-index: 1000; }
            .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #1a1a1a; padding: 10px; z-index: 1000; border-top-left-radius: 20px; border-top-right-radius: 20px; }
            .stSidebar button { background-color: transparent; color: white; border-radius: 4px; /* Tiny fillet */ padding: 6px 12px; margin: 5px 0; width: 100%; cursor: pointer; border: none; font-size: 13px; text-align: left; transition: background-color 0.3s; } /* Colorless, left-aligned text */
            .stSidebar button:hover { background-color: rgba(255,20,147,0.2); /* More pronounced pink tint on hover, no border */ color: white; }
            [data-testid="stSidebar"] { background-color: #18181b; color: white; }
            .stApp { background-color: #0a0a0a; color: white; }
            .content-card { background-color: #1f1f1f; border: 1px solid #333; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
            .block-container { padding-bottom: 80px; }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar - Search at top, vertical buttons with left-aligned text, integrated bottom nav as additional buttons
    with st.sidebar:
        # Search bar at top of sidebar
        st.text_input("Search", key="search_bar", placeholder="Search posts, people, companies...")

        # Profile top with avatar and SVG logo
        st.markdown("""
            <h1>supernNova_2177</h1>
        """, unsafe_allow_html=True)
        st.image("https://via.placeholder.com/100?text=Profile+Pic", width=100, caption="")
        st.subheader("taha gungor")
        st.caption("ceo / test_tech")
        st.caption("artist / 0111 ≡ ...")
        st.caption("New York, New York, United States")
        st.caption("test_tech")
        st.divider()
        st.metric("Profile viewers", np.random.randint(2000, 2500))
        st.metric("Post impressions", np.random.randint(1400, 1600))
        st.divider()

        # Manage pages with logical logos
        st.subheader("Manage pages")
        if st.button("🔬 test_tech", key="manage_test_tech"):
            st.session_state.current_page = "test_tech"
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
        if st.button("AI Assist", key="nav_ai_assist"):
            st.session_state.current_page = "ai_assist"
            st.rerun()
        if st.button("Animate Gaussian", key="nav_animate_gaussian"):
            st.session_state.current_page = "animate_gaussian"
            st.rerun()
        if st.button("Login", key="nav_login"):
            st.session_state.current_page = "login"
            st.rerun()

        # Integrated bottom nav as additional vertical buttons in sidebar
        st.divider()
        st.subheader("Quick Nav")
        if st.button("🏠 Home"):
            st.session_state.current_page = "feed"
            st.rerun()
        if st.button("📹 Video"):
            st.session_state.current_page = "video_chat"
            st.rerun()
        if st.button("👥 My Network"):
            st.session_state.current_page = "social"
            st.rerun()
        st.markdown('<div style="background: #ff1493; color: white; border-radius: 50%; padding: 2px 6px; font-size: 12px; display: inline-block; margin-bottom: 5px;">8</div>', unsafe_allow_html=True)
        if st.button("🔔 Notifications"):
            st.session_state.current_page = "messages"
            st.rerun()
        if st.button("💼 Jobs"):
            st.session_state.current_page = "jobs"
            st.rerun()

    # Main content - Load the current page
    load_page(st.session_state.current_page)

if __name__ == "__main__":
    main()
