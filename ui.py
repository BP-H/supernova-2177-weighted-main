import sys
from pathlib import Path
import streamlit as st
import importlib.util
import numpy as np
import warnings

# --- Page Configuration and Setup ---
warnings.filterwarnings("ignore", category=UserWarning)
st.set_page_config(page_title="supernNova_2177", layout="wide", initial_sidebar_state="expanded")

# --- Helper Functions ---
def load_css(file_path):
    """Loads a CSS file and injects it into the Streamlit app."""
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_page(page_name: str):
    """Dynamically loads and runs a page module from the 'pages' directory."""
    # This is your page loader, kept as is.
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
        if hasattr(module, 'render'):
            module.render()
        else:
            st.warning(f"Page '{page_name}' has no render() function.")
    except Exception as e:
        st.error(f"Error loading page '{page_name}': {e}")
        st.exception(e)

# --- Main App Execution ---
def main():
    # Load the external CSS file
    load_css("styles.css")

    # Initialize session state
    st.session_state.setdefault("current_page", "feed")

    # --- Sidebar ---
    # This uses Streamlit's native sidebar, styled by our CSS.
    with st.sidebar:
        # Using a placeholder for the SVG to avoid potential rendering issues.
        st.header("supernNova_2177")
        st.image("https://avatar.iran.liara.run/public/boy?username=taha", width=100)
        st.subheader("Taha Gungor")
        st.caption("CEO / Artist / AI Architect")
        st.caption("New York, New York, United States")
        st.divider()
        st.metric("Profile Viewers", np.random.randint(2000, 2500))
        st.metric("Post Impressions", np.random.randint(1400, 1600))
        st.divider()

        st.subheader("Navigation")
        if st.button("Feed", use_container_width=True):
             st.session_state.current_page = "feed"
             st.rerun()
        if st.button("My Network", use_container_width=True):
             st.session_state.current_page = "social"
             st.rerun()
        if st.button("Jobs", use_container_width=True):
             st.session_state.current_page = "jobs"
             st.rerun()

        st.divider()
        st.caption("© 2025 supernNova")


    # --- Header (for Search Bar) ---
    # This custom div will be made sticky by our CSS.
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.text_input("Search", key="search_bar", placeholder="Search posts, people, jobs...")
    st.markdown('</div>', unsafe_allow_html=True)


    # --- Main Content Area ---
    # This custom div provides the correct padding for our fixed header/footer.
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    load_page(st.session_state.current_page)
    st.markdown('</div>', unsafe_allow_html=True)


    # --- Bottom Navigation ---
    # This custom div will be fixed to the bottom by our CSS.
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
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
        # The badge is now properly contained and styled via CSS
        st.markdown("""
        <div class="badge-container">
            <button class="st-emotion-cache-q8sbsg ef3psqc12">🔔<br>Notifications</button>
            <div class="badge">8</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[4]:
        if st.button("💼\nJobs", key="bottom_jobs"):
            st.session_state.current_page = "jobs"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
