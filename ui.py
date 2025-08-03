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
import base64

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

# Helper function to encode image to Base64
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

# Main function
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

    # --- MODIFICATION: New logic to safely load the image ---
    img_b64 = ""
    is_clickable = False
    image_path = Path(__file__).parent / "assets" / "profile_pic.png"

    if image_path.exists():
        img_b64 = image_to_base64(image_path)
        is_clickable = True
    # The 'else' case is handled in the sidebar rendering below

    st.markdown(f"""
    <style>
        /* (All previous CSS styles remain the same) */
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
        .stApp {{ background-color: #0a0a0a !important; color: white !important; }}

        /* CSS for original, non-clickable image */
        [data-testid="stSidebar"] img {{
            border-radius: 50% !important;
            margin: 0 auto 10px auto !important; /* Centered with margin-bottom */
            display: block !important;
        }}

        /* CSS for the clickable button version */
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

    # Sidebar
    with st.sidebar:
        st.text_input(
            "Search", key="search_bar", placeholder="🔍 Search posts, people...",
            label_visibility="collapsed"
        )
        if st.button("💫supernNova_2177💫", use_container_width=True):
            st.session_state.search_bar = ""
            st.session_state.current_page = "feed"
            st.rerun()

        # --- MODIFICATION: New logic to show either the button or a fallback ---
        if is_clickable:
            # If the image was found, show the clickable button
            if st.button("", key="profile_pic_button"):
                st.session_state.current_page = "profile"
                st.rerun()
        else:
            # If image was not found, show an error and the non-clickable original image
            st.error(f"Clickable pic failed. File not found at: assets/profile_pic.png")
            st.image("assets/profile_pic.png", width=100)

        st.subheader("taha_gungor")
        st.caption("ceo / test_tech")
        st.caption("artist / will = ...")
        st.caption("New York, New York, United States")
        st.caption("test_tech")
        st.divider()
        st.metric("Profile viewers", np.random.randint(2000, 2500))
        st.metric("Post impressions", np.random.randint(1400, 1600))
        st.divider()

        # (Rest of sidebar buttons)
        if st.button("🏠 Test Tech", key="manage_test_tech"):
            st.session_state.current_page = "test_tech"
            st.rerun()
        if st.button("📰 Feed", key="nav_feed"):
            st.session_state.current_page = "feed"
            st.rerun()
        if st.button("👤 Profile", key="nav_profile"):
            st.session_state.current_page = "profile"
            st.rerun()
        # Add other buttons as needed...

    # Main content area
    with st.container():
        if st.session_state.search_bar:
            st.header(f"Searching for: \"{st.session_state.search_bar}\"")
            st.info("Search results would appear here.")
        else:
            load_page(st.session_state.current_page)

if __name__ == "__main__":
    main()
