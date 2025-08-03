# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

"""Main Streamlit UI entry point for supernNova_2177."""

import sys
import hashlib
from pathlib import Path
import streamlit as st
import importlib.util
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from midiutil import MIDIFile
from sqlalchemy import create_engine, text
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Path adjustment for cloud/local
sys.path.insert(0, str(Path("/mount/src") if 'mount' in str(Path(__file__)) else Path(__file__).parent))

# DB setup (adjust URL if needed)
DB_URL = "sqlite:///harmonizers.db"
engine = create_engine(DB_URL)

# Seed sample data if not exists
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"))
    conn.execute(text("CREATE TABLE IF NOT EXISTS profile_views (id INTEGER PRIMARY KEY)"))  # Placeholder for metrics
    conn.execute(text("CREATE TABLE IF NOT EXISTS posts (impressions INTEGER)"))
    # Seed users if empty
    if not conn.execute(text("SELECT * FROM users WHERE username = 'admin'")).fetchone():
        conn.execute(text("INSERT INTO users VALUES ('admin', '" + hashlib.sha256("password".encode()).hexdigest() + "')"))
        conn.execute(text("INSERT INTO users VALUES ('guest', '" + hashlib.sha256("password".encode()).hexdigest() + "')"))
        conn.execute(text("INSERT INTO users VALUES ('demo_user', '" + hashlib.sha256("password".encode()).hexdigest() + "')"))
    conn.commit()

# Page loader: Prioritize transcendental_resonance_frontend/pages, then pages
def load_page(page_name: str):
    base_paths = [Path(__file__).parent / "transcendental_resonance_frontend/pages", Path(__file__).parent / "pages", Path("/mount/src/transcendental_resonance_frontend/pages"), Path("/mount/src/pages")]
    module_path = None
    for base in base_paths:
        candidate = base / f"{page_name}.py"
        if candidate.exists():
            module_path = candidate
            break
    if not module_path:
        st.info(f"Page '{page_name}' under construction! 🚧")
        return
    try:
        spec = importlib.util.spec_from_file_location(page_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'main'):
            module.main()
        else:
            st.warning(f"No main in {page_name}.py - placeholder shown.")
            st.write(f"Placeholder for {page_name.capitalize()} 🌟")
    except Exception as e:
        st.error(f"Load failed: {e}")

# Resonance music generation
def generate_resonance_music():
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)
    for i, note in enumerate([60, 64, 67, 72]):
        midi.addNote(0, 0, note, i, 1, 100)
    with open("resonance.mid", "wb") as f:
        midi.writeFile(f)
    return "resonance.mid"

# Network graph
def render_network_graph():
    G = nx.random_geometric_graph(10, 0.2)
    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(G, ax=ax, node_color='#ff1493', edge_color='#c71585')
    st.pyplot(fig)

def main() -> None:
    st.set_page_config(page_title="supernNova_2177", layout="wide", initial_sidebar_state="expanded")
    st.session_state["theme"] = "dark"  # Force dark
    st.session_state.setdefault("current_page", "feed")
    st.session_state.setdefault("logged_in", False)

    # CSS: Pink/black theme, gradients, shadows, responsive
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] { background-color: #000; color: #fff; }
            .stButton > button { background: linear-gradient(#ff1493, #c71585); color: #fff; border: none; border-radius: 20px; padding: 10px 20px; transition: 0.3s; box-shadow: 0 4px 8px rgba(255,20,147,0.3); }
            .stButton > button:hover { transform: scale(1.05); box-shadow: 0 6px 12px rgba(255,20,147,0.5); }
            .sidebar .sidebar-content { background: linear-gradient(#121212, #000); padding: 20px; border-radius: 15px; box-shadow: 0 0 20px rgba(255,20,147,0.2); }
            [data-testid="stMetric"] { background-color: #1a1a1a; border-radius: 10px; padding: 10px; color: #ff1493; }
            .stTextInput > div > div > input { background-color: #1a1a1a; color: #fff; border: 1px solid #ff1493; border-radius: 10px; }
            .stExpander { background-color: #1a1a1a; border-radius: 10px; }
            h1, h2, h3 { color: #ff1493; text-shadow: 1px 1px #c71585; }
            @media (max-width: 768px) { .stButton { width: 100%; margin-bottom: 10px; } }
        </style>
    """, unsafe_allow_html=True)

    # Login handling
    if not st.session_state.logged_in:
        st.sidebar.header("Login to supernNova_2177 🌌")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login 🔑"):
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_pw}'"))
                if result.fetchone():
                    st.session_state.logged_in = True
                    st.sidebar.success("Logged in! 🎉")
                    st.rerun()
                else:
                    st.sidebar.error("Invalid credentials ❌")
        return
    else:
        if st.sidebar.button("Logout 👋"):
            st.session_state.logged_in = False
            st.rerun()

    # Sidebar: Structured with expanders and columns
    with st.sidebar:
        st.markdown("<h1 style='color: #ff1493;'>supernNova_2177 🌌</h1>", unsafe_allow_html=True)
        st.image("https://via.placeholder.com/100?text=Avatar 🦸", width=100)
        st.subheader("taha gungor 😎")
        st.caption("CEO / test_tech 🚀 • Artist / 0111 ≡ ... 🎨")
        st.caption("New York, NY, USA 🗽 • test_tech 🔬")
        bio = st.text_area("Bio", "Your cosmic bio... ✨", height=50)
        st.divider()
        # Metrics from DB or random
        with engine.connect() as conn:
            viewers = conn.execute(text("SELECT COUNT(*) FROM profile_views")).scalar() or np.random.randint(2000, 3000)
            impressions = conn.execute(text("SELECT SUM(impressions) FROM posts")).scalar() or np.random.randint(1400, 2000)
        st.metric("Profile Viewers 👀", viewers)
        st.metric("Post Impressions 📈", impressions)
        st.metric("Resonance ✨", f"{np.random.uniform(0.8, 1.0):.2f}")
        st.metric("Entropy ⚡", np.random.randint(100, 300))
        st.divider()

        # Manage pages expander
        with st.expander("Manage Pages 📂", expanded=True):
            cols = st.columns(2)
            if cols[0].button("🔬 Test Tech"):
                st.session_state.current_page = "test_tech"
                st.rerun()
            if cols[1].button("🌌 Supernova"):
                st.session_state.current_page = "supernova_2177"
                st.rerun()
            if cols[0].button("✈️ Globalrunway"):
                st.session_state.current_page = "globalrunway"
                st.rerun()
            if cols[1].button("📂 Show All"):
                st.write("All pages list...")

        st.divider()
        if st.button("🔮 Enter Metaverse 🌠"):
            st.session_state.current_page = "enter_metaverse"
            st.rerun()
        st.divider()

        # Navigation subheader with columns
        st.subheader("Navigation 🧭")
        cols = st.columns(2)
        nav_options = [
            ("📡 Feed", "feed"),
            ("💬 Chat", "chat"),
            ("✉️ Messages", "messages"),
            ("🤖 Agents", "agents"),
            ("🗳️ Voting", "voting"),
            ("👤 Profile", "profile"),
            ("🎵 Music", "music"),
            ("🎶 Resonance", "resonance_music")
        ]
        for i, (label, page) in enumerate(nav_options):
            with cols[i % 2]:
                if st.button(label):
                    st.session_state.current_page = page
                    st.rerun()

    # Main content area
    st.header(f"{st.session_state.current_page.capitalize()} Hub 🌟")
    page = st.session_state.current_page
    if page == "feed":
        st.image("https://via.placeholder.com/800x400?text=Dynamic+Post 🌟", caption="Promoted Post: 439 likes • 18 comments • 24 reposts")
        cols = st.columns(4)
        cols[0].button("👍 Like")
        cols[1].button("💬 Comment")
        cols[2].button("🔄 Repost")
        cols[3].button("➡️ Send")
    elif page == "chat":
        message = st.text_area("Type message 💬")
        if st.button("Send 📤"):
            st.write(f"You: {message}")
            st.write("AI: Resonance acknowledged! 🤖")
    elif page == "voting":
        proposal = st.selectbox("Proposal", ["New Feature", "UI Update"])
        vote = st.radio("Vote 🗳️", ["Yes 👍", "No 👎"])
        if st.button("Cast Vote"):
            st.success(f"Voted {vote} on {proposal}! 🎊")
    elif page == "music":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    elif page == "resonance_music":
        if st.button("Generate Resonance MIDI 🎹"):
            midi_file = generate_resonance_music()
            with open(midi_file, "rb") as f:
                st.download_button("Download 🎶", f, "resonance.mid")
    elif page == "agents":
        st.write("AI Agents Network 🤖")
        render_network_graph()
    elif page == "profile":
        st.write("Your Profile Details 👤")
        st.write("Bio: " + bio)
    else:
        load_page(page)

if __name__ == "__main__":
    main()
