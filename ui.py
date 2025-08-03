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

REPO_ROOT = Path(__file__).parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "transcendental_resonance_frontend"))

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
   base_paths = [REPO_ROOT / "pages", REPO_ROOT / "transcendental_resonance_frontend" / "pages"]
   module_path = None
   for base in base_paths:
       candidate = base / f"{page_name}.py"
       if candidate.exists():
           module_path = candidate
           break
   if not module_path:
       st.info(f"Page '{page_name}' not found. Please check the path.")
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
   except Exception as e:
       st.error(f"Error loading page '{page_name}': {e}")
       st.exception(e)

def main() -> None:
   st.set_page_config(page_title="supernNova_2177", layout="wide", initial_sidebar_state="expanded")
   st.session_state.setdefault("theme", "dark")
   st.session_state.setdefault("current_page", "feed")
   initialize_theme(st.session_state["theme"])

   st.markdown("""
       <style>
           body { margin: 0; font-family: sans-serif; background-color: #0a0a0a; color: #fff; }
           [data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stSidebarNav"] { display: none !important; }
           [data-testid="stSidebar"] {
               background-color: #18181b !important; padding: 15px !important; width: 300px !important;
               position: fixed; height: 100vh; overflow-y: auto; z-index: 100;
           }
           [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 { font-size: 1.5em; margin-bottom: 0.5em; color: #fff; }
           [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { margin-bottom: 0.2em; font-size: 0.9em; color: #aaa; }
           [data-testid="stSidebar"] .stImage img { border-radius: 50%; margin-bottom: 10px; display: block; margin-left: auto; margin-right: auto;} /* Centered and circular profile pic */
           [data-testid="stSidebar"] .stMetric { background-color: #2a2a2a; padding: 10px; border-radius: 8px; margin-bottom: 5px; }
           [data-testid="stSidebar"] .stMetric label { color: #aaa !important; font-size: 0.9em !important; } /* Metric label color */
           [data-testid="stSidebar"] .stMetric div[data-testid="metric-container"] div { color: #fff !important; font-size: 1.2em !important;} /* Metric value color */
           [data-testid="stSidebar"] .stButton button {
               background-color: #18181b !important; /* Button invisible */
               color: #fff !important; border-radius: 8px !important; padding: 8px 12px !important; margin: 4px 0 !important;
               width: 100% !important; border: 1px solid #18181b !important; /* Invisible border */
               font-size: 14px !important; text-align: left !important; display: flex; align-items: center;
               height: 40px !important; line-height: 1.2em !important; overflow: hidden !important;
               text-overflow: ellipsis !important; white-space: nowrap !important;
           }
           [data-testid="stSidebar"] .stButton button:hover { background-color: #333 !important; border: 1px solid #444 !important; } /* Visible on hover */
           [data-testid="stSidebar"] .stTextInput input { background-color: #2a2a2a; color: white; border-radius: 8px; border: 1px solid #333; }
           [data-testid="stSidebar"] .stDivider { margin: 10px 0;}
           /* Main Content Styling */
           .main-content-wrapper { margin-left: 300px; padding: 20px; background-color: #0a0a0a; min-height: 100vh; color: #fff !important; }
           .content-card { background-color: #1f1f1f; border: 1px solid #333; border-radius: 8px; padding: 16px; margin-bottom: 16px; color: #fff !important; }
           .content-card * { color: #fff !important; } /* Force white text within content cards */
           /* Feed Buttons Specific Styling */
           .feed-buttons .stButton button {
               height: 30px !important; width: auto !important; padding: 4px 8px !important; font-size: 12px !important;
               background-color: #333 !important; border-radius: 4px !important; margin: 2px !important;
               display: inline-flex !important; color: #ccc !important; white-space: nowrap !important; border: none !important;
           }
           .feed-buttons .stButton button:hover { background-color: #444 !important; color: white !important; }
           .feed-button-container { display: flex; justify-content: space-around; padding-top: 10px; gap: 5px;}
       </style>""", unsafe_allow_html=True)

   with st.sidebar:
       st.text_input("Search", key="search_bar_sidebar", placeholder="Search...", label_visibility="collapsed")
       st.image("https://via.placeholder.com/80?text=User", width=80) # Profile Pic
       st.markdown("<p style='text-align:center; margin-top: -10px; margin-bottom: 10px;'>taha gungor</p>", unsafe_allow_html=True)
       st.metric("Profile viewers", np.random.randint(2000, 2500))
       st.metric("Post impressions", np.random.randint(1400, 1600))
       st.divider()
       st.subheader("Navigation")
       nav_items = {"feed": "📰 Feed", "chat": "💬 Chat", "messages": "📬 Messages", "agents": "🤖 Agents", 
                    "voting": "🗳️ Voting", "profile": "👤 Profile", "music": "🎶 Music", 
                    "ai_assist": "✨ AI Assist", "animate_gaussian": "🌀 Animate Gaussian", "login": "🚪 Login"}
       for page, label in nav_items.items():
           if st.button(label, key=f"nav_{page}"): st.session_state.current_page = page; st.rerun()
       st.divider()
       st.subheader("Premium Features")
       if st.button("✨ Enter Metaverse", key="prem_meta"): st.session_state.current_page = "enter_metaverse"; st.rerun()
       if st.button("⚙️ Settings", key="prem_settings"): st.session_state.current_page = "settings"; st.rerun()
       theme_selector()
       st.divider()
       st.subheader("Quick Nav")
       if st.button("🏠 Home", key="qn_home"): st.session_state.current_page = "feed"; st.rerun()
       if st.button("🔔 Notifications (8)", key="qn_notif"): st.session_state.current_page = "messages"; st.rerun()
       if st.button("💼 Jobs", key="qn_jobs"): st.session_state.current_page = "jobs"; st.rerun()

   st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
   load_page(st.session_state.current_page)
   st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
   main()
