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
import base64  # MODIFICATION: Added for image encoding

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

# MODIFICATION: Helper function to encode image to Base64
def image_to_base64(path: Path) -> str:
    """Encodes an image file to a Base64 string."""
    with path.open("rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

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
    st.session_state.setdefault("conversations", {})
    st.session_state.setdefault("current_page", "feed")
    initialize_theme(st.session_state["theme"])

    # MODIFICATION: More reliable way to find the image and encode it
    img_b64 = ""
    try:
        # Get the absolute path to the image relative to *this file*
        script_dir = Path(__file__).parent
        image_path = script_dir / "assets" / "profile_pic.png"
        img_b64 = image_to_base64(image_path)
    except FileNotFoundError:
        # If the image still isn't found, this error will show the exact path it tried.
        st.error(f"Profile picture not found! Please ensure 'assets/profile_pic.png' exists next to your ui.py file. Full path tried: {image_path.resolve()}")

    st.markdown(f"""
    <style>
        /* (All your other CSS is here) */
        [data-testid="stSidebarNav"] {{ display: none !important; }}
        [data-testid="stSidebar"] {{
            position: sticky !important; top: 0 !important; height: 100vh !important;
            overflow-y: auto !important; background-color: #18181b !important;
            color: white !important; border-radius: 10px; padding: 20px;
            margin: 0px; width: 300px; z-index: 98;
        }}
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stButton,
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] > div {{ text-align: left !important; }}
        [data-testid="stSidebar"] button {{
            background-color: #18181b !important; color: white !important;
            padding: 8px 12px !important; margin: 5px 0 !important;
            width: 100% !important; height: 40px !important; border: none !important;
            border-radius: 8px !important; font-size: 14px !important;
            display: flex !important; justify-content: flex-start !important;
            align-items: center !important; white-space: nowrap !important;
            overflow: hidden !important; text-overflow: ellipsis !important;
        }}
        [data-testid="stSidebar"] button:hover,
        [data-testid="stSidebar"] button:focus {{
            background-color: #2a2a2e !important;
            box-shadow: 0 0 5px rgba(255, 20, 147, 0.3) !important;
            outline: none !important;
        }}
        [data-testid="stSidebar"] button[kind="secondary"]:has(span:contains("supernNova")) {{
            font-size: 28px !important; font-weight: bold !important;
            justify-content: center !important; padding: 15px 0px !important;
            margin-bottom: 15px !important; height: auto !important;
        }}
        [data-testid="stSidebar"] button[kind="secondary"]:has(span:contains("supernNova")):hover {{
            box-shadow: none !important;
        }}
        .stApp {{ background-color: #0a0a0a !important; color: white !important; }}
        .main .block-container {{ padding-top: 20px !important; padding-bottom: 90px !important; }}
        [data-testid="stMetricLabel"] {{ color: white !important; }}
        [data-testid="stMetricValue"] {{ color: white !important; }}

        /* MODIFICATION: CSS for the new clickable profile picture button */
        button[data-testid="stButton"][key="profile_pic_button"] {{
            background-image: url("data:image/png;base64,{img_b64}");
            background-size: cover;
            background-position: center;
            border-radius: 50% !important;
            width: 100px !important;
            height: 100px !important;
            padding: 0 !important;
            margin: 0 auto 10px auto !important;
            display: block !important;
            border: 2px solid #2a2a2e !important;
        }}
        button[data-testid="stButton"][key="profile_pic_button"]:hover,
        button[data-testid="stButton"][key="profile_pic_button"]:focus {{
            border-color: #ff1493 !important;
            box-shadow: 0 0 8px rgba(255, 20, 147, 0.5) !important;
        }}
        button[data-testid="stButton"][key="profile_pic_button"] > div {{
            display: none;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Sidebar - Search at top, profile pic circular, all in sidebar including notifications
    with st.sidebar:
        # Modern search bar
        st.text_input(
            "Search",
            key="search_bar",
            placeholder="🔍 Search posts, people...",
            label_visibility="collapsed"
        )

        # Clickable Logo - navigates to feed
        if st.button("💫supernNova_2177💫", use_container_width=True):
            st.session_state.search_bar = ""
            st.session_state.current_page = "feed"
            st.rerun()
        
        # MODIFICATION: Replaced st.image with the new clickable button
        if st.button("", key="profile_pic_button"):
            st.session_state.current_page = "profile"
            st.rerun()
            
        st.subheader("taha_gungor")
        st.caption("ceo / test_tech")
        st.caption("artist / will = ...")
        st.caption("New York, New York, United States")
        st.caption("test_tech")
        st.divider()
        st.metric("Profile viewers", np.random.randint(2000, 2500))
        st.metric("Post impressions", np.random.randint(1400, 1600))
        st.divider()
        
        # (The rest of your sidebar is here)
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

        if st.button("📰 Feed", key="nav_feed"):
            st.session_state.current_page = "feed"
            st.rerun()
        if st.button("💬 Chat", key="nav_chat"):
            st.session_state.current_page = "chat"
            st.rerun()
        if st.button("📬 Messages", key="nav_messages"):
            st.session_state.current_page = "messages"
            st.rerun()
        if st.button("🗳 Voting", key="nav_voting"):
            st.session_state.current_page = "voting"
            st.rerun()
        if st.button("👤 Profile", key="nav_profile"):
            st.session_state.current_page = "profile"
            st.rerun()
            
        st.divider()
        
        st.subheader("Premium features")
        if st.button("🎶 Music", key="nav_music"):
            st.session_state.current_page = "music"
            st.rerun()
        if st.button("🚀 Agents", key="nav_agents"):
            st.session_state.current_page = "agents"
            st.rerun()
        if st.button("🌌 Enter Metaverse", key="nav_metaverse"):
            st.session_state.current_page = "enter_metaverse"
            st.rerun()
        st.caption("Mathematically sucked into a supernNova_2177 void - stay tuned for 3D immersion")
        st.divider()

        if st.button("⚙️ Settings", key="nav_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
        theme_selector()
        
    # Main content area - Load selected page or show search results
    with st.container():
        # Prioritize search results over page navigation
        if st.session_state.search_bar:
            st.header(f"Searching for: \"{st.session_state.search_bar}\"")
            st.info("This is where your database search results would appear. Connect this to your backend.")
            # Placeholder for search results display
            st.write("---")
            st.subheader("Example Post Result")
            st.write("**User:** taha_gungor")
            st.write("This is a sample post that matches the search query. #streamlit #search")
            st.write("---")
            st.subheader("Example Profile Result")
            st.write("**Profile:** artist_dev")
            st.write("Software developer and digital artist.")

        else:
            # Load the selected page if there is no active search
            load_page(st.session_state.current_page)

if __name__ == "__main__":
    main()
