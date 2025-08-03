# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

"""Main Streamlit UI entry point for supernNova_2177."""

import sys
from pathlib import Path
import streamlit as st
import importlib.util  # Correct import for dynamic loading
import numpy as np  # For random metrics
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Path adjustment for cloud/local
sys.path.insert(0, str(Path("/mount/src") if 'mount' in str(Path(__file__)) else Path(__file__).parent))

# Placeholder imports (assume streamlit_helpers.py exists; otherwise, define helpers inline)
try:
    # from streamlit_helpers import alert, header, theme_selector, safe_container
    # For this improved version, define minimal helpers inline
    def header(text): st.header(text)
    def alert(text): st.info(text)
    def theme_selector(): st.selectbox("Theme", ["dark", "light"], key="theme")
    def safe_container(): return st.container()
    from frontend.theme import initialize_theme
except ImportError as e:
    st.error(f"Critical import failed: {e}")
    st.stop()

# Improved page loader with better error handling and fallback
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
        module = importlib.util.module_from_spec(spec)  # Fixed potential typo here
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

# Main function with improvements
def main() -> None:
    st.set_page_config(
        page_title="supernNova_2177",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("conversations", {})
    st.session_state.setdefault("current_page", "feed")
    st.session_state.setdefault("logged_in", False)  # Added for simple login

    initialize_theme(st.session_state["theme"])

    # Enhanced CSS for modern look: pink accents, curved elements, responsive
    st.markdown("""
        <style>
            .stButton > button { opacity: 0.95; border-radius: 8px; background-color: #333; color: white; }
            .stButton > button:hover { background-color: #ff1493; opacity: 1; }
            .sidebar .sidebar-content { background-color: #1e1e1e; }
        </style>
    """, unsafe_allow_html=True)

    # Simple login if not logged in
    if not st.session_state.logged_in:
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            # Simulate DB check (use real SQLAlchemy in production)
            if username in ["admin", "guest", "demo_user"] and password == "password":
                st.session_state.logged_in = True
                st.sidebar.success("Logged in!")
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")
        return

    # Sidebar with profile and navigation
    with st.sidebar:
        st.markdown("""<h1 style='color: #ff1493;'>supernNova_2177</h1>""", unsafe_allow_html=True)
        st.image("https://via.placeholder.com/100?text=Profile+Pic", width=100)
        st.subheader("taha gungor")
        st.caption("ceo / test_tech")
        st.caption("artist / 0111 ≡ ...")
        st.caption("New York, New York, United States")
        st.caption("test_tech")
        st.divider()
        st.metric("Profile viewers", np.random.randint(2000, 2500))
        st.metric("Post impressions", np.random.randint(1400, 1600))
        # New: Resonance and Entropy metrics
        st.metric("Network Resonance", f"{np.random.uniform(0.8, 1.0):.2f}")
        st.metric("Interaction Entropy", f"{np.random.randint(100, 200)}")
        st.divider()

        # Manage pages
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

        # Enter Metaverse
        if st.button("🔮 Enter Metaverse", key="nav_metaverse"):
            st.session_state.current_page = "enter_metaverse"
            st.rerun()
        st.caption("Mathematically sucked into a supernNova_2177 void – stay tuned for 3D immersion!")
        st.subheader("Premium features")

        # Settings and theme
        if st.button("⚙️ Settings", key="nav_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
        theme_selector()
        st.divider()

        # Enhanced navigation with icons
        nav_options = {
            "Feed": "feed",
            "Chat": "chat",
            "Messages": "messages",
            "Agents": "agents",
            "Voting": "voting",
            "Profile": "profile",
            "Music": "music"
        }
        for label, page in nav_options.items():
            if st.button(f"📌 {label}", key=f"nav_{page}"):
                st.session_state.current_page = page
                st.rerun()

    # Main content area: load selected page or fallback to demo
    with safe_container():
        header(f"Welcome to {st.session_state.current_page.capitalize()}")
        if st.session_state.current_page == "feed":
            st.image("https://via.placeholder.com/800x400?text=Sample+Post", caption="Sample post with 312 likes, 39 comments, 32 reposts")
            st.button("👍 Like")
            st.button("💬 Comment")
            st.button("🔄 Repost")
            st.button("➡️ Send")
        elif st.session_state.current_page == "chat":
            st.write("Simple chat simulation")
            message = st.text_input("Type a message")
            if st.button("Send"):
                st.write(f"You: {message}")
                st.write("AI Agent: Acknowledged! Entropy increased.")
        elif st.session_state.current_page == "music":
            st.write("Music player demo")
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        elif st.session_state.current_page == "voting":
            st.write("Voting mechanic demo")
            st.radio("Vote on proposal", ["Yes", "No"])
            if st.button("Submit Vote"):
                st.success("Vote cast! Resonance updated.")
        elif st.session_state.current_page == "agents":
            st.write("Agents section: Simulate AI agents")
            st.button("Interact with Agent")
        else:
            load_page(st.session_state.current_page)  # Dynamic load for other pages

if __name__ == "__main__":
    main()