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

# Loader with placeholder
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
        st.write(f"Placeholder for {page_name.capitalize()}.")  # Placeholder
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

# Main - LinkedIn-like structure
def main() -> None:
    st.set_page_config(
        page_title="superNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.setdefault("theme", "dark")  # Default dark like LinkedIn
    st.session_state.setdefault("conversations", {})  # Fix NoneType
    initialize_theme(st.session_state["theme"])

    # CSS for LinkedIn-like dark scheme and square sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #1a1a1a;  # LinkedIn dark
                color: white;
                border-radius: 10px;  # Square with curve
                padding: 20px;
                margin: 10px;
                width: 300px;  # Wider for profile
            }
            .stSidebar > div {text-align: center;}  # Center profile
            .stSidebar hr {border-color: #333;}
            .stSidebar a {color: white !important;}
            .bottom-nav {position: fixed; bottom: 0; width: 100%; background-color: #1a1a1a; padding: 10px; display: flex; justify-content: space-around;}
            .bottom-nav button {background: none; border: none; color: white; cursor: pointer;}
        </style>
    """, unsafe_allow_html=True)

    # Green circled sidebar (LinkedIn-like with profile top)
    with st.sidebar:
        # Profile pic top
        st.image("https://via.placeholder.com/100", caption="Your Profile Pic", use_column_width=True)
        st.write("Your Name")
        st.write("CEO / AccessAI.Tech")
        st.write("Artist / 0111 ≡ ...")
        st.write("New York, New York, United States")
        st.write("AccessAI.Tech")
        st.divider()
        st.write("2,103 profile viewers")
        st.write("1,450 post impressions")
        st.divider()
        # Manage pages section
        st.write("Manage pages")
        st.write("AccessAI.Tech")
        st.write("supernova_2177")
        st.write("GLOBALRUNWAY")
        st.write("Show all >")
        st.divider()
        # Puzzle games, Premium, Settings
        st.write("Puzzle games")
        st.write("Premium features")
        st.write("Settings")
        st.divider()
        theme_selector()  # Theme at bottom

    # Main content
    PAGES = {
        "Feed": "feed",
        "Chat": "chat",
        "Messages": "messages",
        "Agents": "agents",
        "Voting": "voting",
        "Profile": "profile",
        "Music": "music",
    }
    page_selection = st.selectbox("Select Page", list(PAGES.keys()))
    page_to_load = PAGES.get(page_selection)
    if page_to_load:
        load_page(page_to_load)
    else:
        st.write("Select a page from sidebar.")

    # Orange bottom nav (LinkedIn-like icons)
    with st.container():
        st.markdown('<div class="bottom-nav">'
                    '<button>Home</button>'
                    '<button>Video</button>'
                    '<button>My Network</button>'
                    '<button>Notifications</button>'
                    '<button>Jobs</button>'
                    '</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
