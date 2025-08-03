# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for supernNova_2177."""
import sys
from pathlib import Path
import streamlit as st
import importlib.util
import numpy as np # For random low stats
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
   # Use Fallback functions instead of stopping
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
   st.session_state.setdefault("conversations", {}) # Fix NoneType
   st.session_state.setdefault("current_page", "feed") # Default page
   initialize_theme(st.session_state["theme"])

   # Fixed CSS - This makes everything sticky and properly aligned
   st.markdown("""
   <style>
       /* Hide Streamlit's top navigation tabs */
       [data-testid="stSidebarNav"] { display: none !important; }
       
       /* 🔥 STICKY SIDEBAR - This is the key fix */
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

       /* 🔥 LEFT ALIGN SIDEBAR CONTENT - Emojis on the left */
       [data-testid="stSidebar"] .stMarkdown,
       [data-testid="stSidebar"] .stButton,
       [data-testid="stSidebar"] .stSelectbox,
       [data-testid="stSidebar"] > div {
           text-align: left !important;
       }
       
       /* 🔥 SIDEBAR BUTTONS - Left aligned with emoji on left */
       [data-testid="stSidebar"] button {
           background-color: rgba(255,255,255,0.05) !important;
           color: white !important;
           padding: 8px 12px !important;
           margin: 5px 0 !important;
           width: 100% !important;
           border: none !important;
           font-size: 13px !important;
           display: flex !important;
           justify-content: flex-start !important;
           align-items: center !important;
       }
       [data-testid="stSidebar"] button:hover {
           background-color: rgba(255,20,147,0.2) !important;
           box-shadow: 0 0 5px #ff1493 !important;
       }
       
       /* 🔥 SEARCH BAR */
       .search-container {
           position: sticky !important;
           top: 0 !important;
           background-color: #0a0a0a !important;
           padding: 1rem 0 !important;
           z-index: 97 !important;
           border-bottom: 1px solid #333;
           margin-left: 2rem;
           margin-right: 2rem;
       }

       /* 🔥 STICKY BOTTOM NAV - Horizontal buttons */
       .bottom-nav {
           position: fixed !important;
           bottom: 0 !important;
           left: 0 !important;
           width: 100% !important;
           background-color: #18181b !important;
           padding: 8px 0 !important;
           display: flex !important;
           justify-content: space-around !important;
           align-items: center !important;
           z-index: 100 !important;
           box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3) !important;
           border-top: 1px solid #333 !important;
           height: 70px !important;
       }
       .bottom-nav .stButton {
           flex: 1 !important;
           display: flex !important;
           justify-content: center !important;
           align-items: center !important;
           flex-direction: column !important;
           height: 100% !important;
           text-align: center !important;
       }
       .bottom-nav .stButton > button {
           background: none !important;
           border: none !important;
           color: #a0a0a0 !important;
           font-size: 12px !important;
           display: flex !important;
           flex-direction: column !important;
           align-items: center !important;
           height: 100% !important;
           width: 100% !important;
       }
       .bottom-nav .stButton:hover > button {
           color: #ff1493 !important;
       }

       /* 🔥 NOTIFICATION BADGE */
       .badge {
           position: absolute !important;
           top: 5px !important;
           right: 20px !important;
           background: #ff1493 !important;
           color: white !important;
           border-radius: 50% !important;
           padding: 0px 6px !important;
           font-size: 10px !important;
           z-index: 101 !important;
       }
       
       /* 🔥 MAIN CONTENT AREA - Prevent overlap */
       .stApp {
           background-color: #0a0a0a !important;
           color: white !important;
       }
       .main .block-container {
           padding-top: 90px !important; /* Space for bottom nav */
           padding-bottom: 90px !important; /* Space for bottom nav */
       }

       /* Content cards */
       .content-card {
           border: 1px solid #333;
           border-radius: 8px;
           padding: 16px;
           margin-bottom: 16px;
           transition: border 0.2s;
       }
       .content-card:hover {
           border: 1px solid #ff1493;
       }
       
       /* Search bar styling */
       [data-testid="stTextInput"] {
           background-color: #28282b !important;
           border-radius: 20px !important;
           border: 1px solid #28282b !important;
           padding: 8px !important;
       }

       /* Mobile responsiveness */
       @media (max-width: 768px) {
           .bottom-nav {
               padding: 4px 0 !important;
               height: 60px !important;
           }
           .bottom-nav .stButton {
               font-size: 10px !important;
               padding: 2px !important;
           }
           .main .block-container {
               padding-top: 70px !important;
               padding-bottom: 70px !important;
           }
       }
   """, unsafe_allow_html=True)

   # Sidebar - LinkedIn-like, with better logos, new sections clickable, lowercase name
   with st.sidebar:
       st.markdown(f"""
           <svg width="200" height="50" viewBox="0 0 200 50" fill="none" xmlns="http://www.w3.org/2000/svg">
               <rect width="200" height="50" fill="#0a0a0a"/>
               <text x="10" y="35" font-family="Arial" font-size="20" font-weight="bold" fill="white">supernNova</text>
           </svg>
           """, unsafe_allow_html=True)
       
       st.image("https://via.placeholder.com/100?text=Profile+Pic", width=100, caption="User")
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
       # CORRECTED typo gaussion -> gaussian
       if st.button("🌀 Animate Gaussian", key="nav_animate_gaussian"):
           st.session_state.current_page = "animate_gaussian"
           st.rerun()
       if st.button("🚪 Login", key="nav_login"):
           st.session_state.current_page = "login"
           st.rerun()

   # Main content area - Load selected page
   with st.container():
       load_page(st.session_state.current_page)

if __name__ == "__main__":
   main()
