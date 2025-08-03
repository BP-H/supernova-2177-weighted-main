# ui.py
import streamlit as st
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="supernNova_2177",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS for the full sticky layout ---
# This single block of CSS creates the fixed sidebar, sticky top search bar, and fixed bottom navigation.
st.markdown("""
<style>
    /* 1. HIDE STREAMLIT DEFAULTS */
    /* Hide the hamburger menu and the top-right toolbar */
    [data-testid="stToolbar"], [data-testid="stHeader"] {
        display: none !important;
    }
    /* Hide the multi-page navigation that Streamlit tries to add */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* 2. STICKY/FIXED ELEMENTS */
    /* Make the sidebar truly fixed to the viewport */
    [data-testid="stSidebar"] {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        width: 21rem; /* Set a fixed width */
        background-color: #18181b;
        border-right: 1px solid #333;
        padding: 1rem;
    }

    /* Make the bottom nav truly fixed to the viewport */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0; /* Align with the full page width */
        right: 0;
        background-color: #18181b;
        border-top: 1px solid #333;
        padding: 0.5rem;
        display: flex;
        justify-content: space-around;
        z-index: 99;
    }
    
    /* Make the search bar sticky to the top of the main content area */
    .search-container {
        position: sticky;
        top: 0;
        background-color: #0e1117; /* Match app background */
        padding: 1rem 0;
        z-index: 98;
        border-bottom: 1px solid #333;
    }

    /* 3. LAYOUT ADJUSTMENTS */
    /* Push the main content to the right to avoid the fixed sidebar */
    .main .block-container {
        margin-left: 21rem;
        padding-top: 0 !important;
        padding-bottom: 5rem !important; /* Add space to not be hidden by the bottom nav */
    }
    
    /* 4. SIDEBAR & BUTTON STYLING */
    [data-testid="stSidebar"] .stButton button {
        background-color: rgba(255,255,255,0.05);
        color: white;
        border: none;
        text-align: left;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255,20,147,0.2);
        color: #ff1493;
    }

    /* Center the sidebar logo and image */
    [data-testid="stSidebar"] [data-testid="stImage"],
    .sidebar-logo {
        margin-left: auto;
        margin-right: auto;
        display: block;
    }
    .sidebar-logo {
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
        color: #ff1493;
        margin-bottom: 1rem;
    }

    /* 5. MOBILE RESPONSIVENESS */
    @media (max-width: 768px) {
        /* On mobile, hide the sidebar and let main content take full width */
        [data-testid="stSidebar"] {
            display: none;
        }
        .main .block-container {
            margin-left: 0rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# --- Reusable Page Components ---
# Instead of a complex loader, we use simple functions for each "page".
def render_feed():
    """Renders the main content feed."""
    st.title("Feed")
    
    # --- Sticky Search Bar ---
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        st.text_input("Search", placeholder="Search posts, users...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Post Loop ---
    for i in range(5): # Create 5 dummy posts
        st.subheader(f"User {i+1}")
        st.write("Cost performance entire set. Democrat throw along individual stay. Performance table able become or mean too on.")
        st.image("https://via.placeholder.com/600x300.png?text=Post+Image", use_column_width=True)
        cols = st.columns(4)
        cols[0].button("Like 👍", key=f"like_{i}", use_container_width=True)
        cols[1].button("Comment 💬", key=f"comment_{i}", use_container_width=True)
        cols[2].button("Repost 🔁", key=f"repost_{i}", use_container_width=True)
        cols[3].button("Send ✉️", key=f"send_{i}", use_container_width=True)
        st.divider()

def render_placeholder_page(title):
    """A placeholder for pages that are not yet built."""
    st.title(title)
    st.info(f"The '{title}' page is coming soon!")
    st.image("https://via.placeholder.com/600x300.png?text=Under+Construction", use_column_width=True)


# --- App State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "Feed"

# --- Sidebar Definition ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">supernNova_2177</div>', unsafe_allow_html=True)
    st.image("https://via.placeholder.com/100?text=Profile", width=100)
    st.subheader("taha gungor")
    st.caption("ceo / test_tech")
    st.divider()
    
    c1, c2 = st.columns(2)
    c1.metric("Profile viewers", f"{np.random.randint(2000, 2500)}")
    c2.metric("Post impressions", f"{np.random.randint(1400, 1600)}")
    st.divider()

    st.subheader("Navigation")
    # This is a much simpler way to handle navigation without st.rerun()
    if st.button("Feed", use_container_width=True):
        st.session_state.page = "Feed"
    if st.button("Chat", use_container_width=True):
        st.session_state.page = "Chat"
    if st.button("Messages", use_container_width=True):
        st.session_state.page = "Messages"


# --- Main Content Area ---
# This simple logic displays the correct "page" based on the session state.
if st.session_state.page == "Feed":
    render_feed()
elif st.session_state.page == "Chat":
    render_placeholder_page("Chat")
elif st.session_state.page == "Messages":
    render_placeholder_page("Messages")
else:
    render_feed() # Default to the feed


# --- Bottom Navigation Bar ---
# This is a simple container with buttons. The CSS makes it fixed to the bottom.
st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    if st.button("🏠", key="bottom_home"): st.session_state.page = "Feed"
with cols[1]:
    if st.button("👥", key="bottom_network"): st.session_state.page = "Network"
with cols[2]:
    if st.button("➕", key="bottom_post"): st.session_state.page = "Post"
with cols[3]:
    if st.button("🔔", key="bottom_notifs"): st.session_state.page = "Notifications"
with cols[4]:
    if st.button("💼", key="bottom_jobs"): st.session_state.page = "Jobs"
st.markdown('</div>', unsafe_allow_html=True)
