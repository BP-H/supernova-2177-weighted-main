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

try:
    from streamlit_helpers import alert, header, theme_selector, safe_container
    from frontend.theme import initialize_theme
except ImportError as e:
    def alert(text): st.info(text)
    def header(text): st.header(text)
    def theme_selector(): st.selectbox("Theme", ["dark"], key="theme")
    def safe_container(): return st.container()
    def initialize_theme(theme): pass
    st.warning(f"Helpers import failed: {e}, using fallbacks.")

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
    st.set_page_config(page_title="supernNova_2177", layout="wide", initial_sidebar_state="expanded")
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("conversations", {})
    st.session_state.setdefault("current_page", "feed")
    initialize_theme(st.session_state["theme"])

    # CSS: Left-aligned text, handle long text with ellipsis, modern buttons with transitions/shadows
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none !important;}
            [data-testid="stSidebar"] {
                position: sticky; top: 0; height: 100vh; overflow-y: auto; background-color: #18181b; color: white; 
                border-radius: 10px; padding: 20px; margin: 10px; width: 300px; 
            }
            .stSidebar > div { display: flex; flex-direction: column; align-items: flex-start; text-align: left !important; }
            .stSidebar subheader, .stSidebar caption, .stSidebar p { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; margin: 2px 0; }
            .stSidebar button { background-color: rgba(255,255,255,0.05); color: white; border-radius: 20px; padding: 8px 16px; margin: 4px 0; width: 100%; cursor: pointer; border: none; font-size: 14px; transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .stSidebar button:hover { background-color: rgba(255,20,147,0.2); box-shadow: 0 4px 8px rgba(255,20,147,0.3); transform: translateY(-2px); }
            .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #0a0a0a; padding: 5px 0; display: flex; justify-content: space-around; z-index: 100; box-shadow: 0 -2px 10px rgba(0,0,0,0.2); border-top-left-radius: 20px; border-top-right-radius: 20px; }
            .bottom-nav .stButton > button { font-size: 12px; padding: 2px 4px; display: flex; flex-direction: column; align-items: center; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; transition: all 0.3s ease; }
            .bottom-nav button:hover { color: #ff1493; transform: scale(1.05); }
            .bottom-nav .badge { background: #ff1493; color: white; border-radius: 50%; padding: 2px 6px; font-size: 12px; margin-top: -10px; box-shadow: 0 1px 2px rgba(0,0,0,0.2); }
            .stApp { background-color: #0a0a0a; color: white; }
            .block-container { padding-bottom: 80px !important; padding-left: 20px; padding-right: 20px; }
            .content-card { background-color: #1f1f1f; border: 1px solid #333; border-radius: 8px; padding: 16px; margin-bottom: 16px; transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
            .content-card:hover { border: 1px solid #ff1493; box-shadow: 0 4px 8px rgba(255,20,147,0.3); transform: translateY(-2px); }
            [data-testid="stTextInput"] { background-color: #282828; border-radius: 20px; padding: 8px; width: 100%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
            @media (max-width: 768px) { 
                .stSidebar { width: 100%; margin: 0; border-radius: 0; }
                .stSidebar button { font-size: 12px; padding: 6px 12px; }
                .content-card { padding: 12px; margin-bottom: 12px; }
                .bottom-nav { padding: 2px 0; } 
                .bottom-nav .stButton > button { font-size: 10px; padding: 1px 2px; }
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar: Supernova at top left-aligned, profile pic below, all text left-aligned with ellipsis for long lines
    with st.sidebar:
        st.markdown("""
            <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;">
                <svg width="200" height="50" viewBox="0 0 200 50" fill="none" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto;">
                    <rect width="200" height="50" fill="#FF00FF"/>
                    <text x="10" y="35" font-family="Arial" font-size="20" font-weight="bold" fill="white">supernNova_2177</text>
                </svg>
            </div>
        """, unsafe_allow_html=True)
        st.image("https://via.placeholder.com/100?text=Profile+Pic", width=100)
        st.subheader("taha gungor")
        st.caption("ceo / test_tech")
        st.caption("artist / 0111 ≡ ...")
        st.caption("New York, New York, United States")
        st.caption("test_tech")
        st.divider()
        st.metric("Profile viewers", np.random.randint(2000, 2500))
        st.metric("Post impressions", np.random.randint(1400, 1600))
        st.divider()
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
        if st.button("🔮 Enter Metaverse", key="nav_metaverse"):
            st.session_state.current_page = "enter_metaverse"
            st.rerun()
        st.caption("Mathematically sucked into a supernNova_2177 void – stay tuned for 3D immersion!")
        st.subheader("Premium features")
        if st.button("⚙️ Settings", key="nav_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
        theme_selector()
        st.divider()
        st.subheader("Navigation")
        nav_cols = st.columns(2)
        nav_buttons = [
            ("Feed", "feed"),
            ("Chat", "chat"),
            ("Messages", "messages"),
            ("Agents", "agents"),
            ("Voting", "voting"),
            ("Profile", "profile"),
            ("Music", "music")
        ]
        for i, (label, page) in enumerate(nav_buttons):
            col = nav_cols[i % 2]
            if col.button(label, key=f"nav_{page}"):
                st.session_state.current_page = page
                st.rerun()

    # Main content
    st.text_input("Search", key="search_bar", placeholder="Search posts, people, jobs...")
    load_page(st.session_state.current_page)

    # Bottom nav
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
        st.markdown('<div class="badge">8</div>', unsafe_allow_html=True)
        if st.button("🔔\nNotifications", key="bottom_notifications"):
            st.session_state.current_page = "messages"
            st.rerun()
    with bottom_cols[4]:
        if st.button("💼\nJobs", key="bottom_jobs"):
            st.session_state.current_page = "jobs"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # JS for alignment and ellipsis enforcement
    st.components.v1.html("""
        <script>
            const sidebar = parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.style.position = 'sticky';
                sidebar.style.top = '0';
                sidebar.style.height = '100vh';
                sidebar.style.overflowY = 'auto';
                const elements = sidebar.querySelectorAll('p, caption, button, [kind="subheader"]');
                elements.forEach(el => {
                    el.style.textAlign = 'left';
                    el.style.whiteSpace = 'nowrap';
                    el.style.overflow = 'hidden';
                    el.style.textOverflow = 'ellipsis';
                    el.style.maxWidth = '100%';
                    el.style.transition = 'all 0.3s ease';
                });
            }
            const bottomNav = parent.document.querySelector('.bottom-nav');
            if (bottomNav) {
                bottomNav.style.display = 'flex';
                bottomNav.style.flexDirection = 'row';
                bottomNav.style.justifyContent = 'space-around';
                bottomNav.style.alignItems = 'center';
            }
            const mainContent = parent.document.querySelector('.block-container');
            if (mainContent) {
                mainContent.style.paddingBottom = '80px';
                mainContent.style.display = 'flex';
                mainContent.style.flexDirection = 'column';
                mainContent.style.alignItems = 'flex-start';
                mainContent.style.gap = '10px';
            }
            const buttons = parent.document.querySelectorAll('.stButton > button');
            buttons.forEach(btn => {
                btn.style.whiteSpace = 'nowrap';
                btn.style.overflow = 'hidden';
                btn.style.textOverflow = 'ellipsis';
                btn.style.maxWidth = '100%';
            });
        </script>
    """, height=0)

if __name__ == "__main__":
    main()
