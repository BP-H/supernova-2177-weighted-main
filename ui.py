# app.py
import streamlit as st
import numpy as np

# --- Page Configuration ---
# This must be the first Streamlit command
st.set_page_config(
    page_title="supernNova_2177",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Custom CSS ---
def load_css(file_name):
    """A function to inject a local CSS file."""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")


# --- Sidebar ---
with st.sidebar:
    # Use markdown to wrap the logo and give it a class for styling
    st.markdown('<div class="logo-container">supernNova_2177</div>', unsafe_allow_html=True)
    
    st.image("https://via.placeholder.com/100?text=Profile", width=100)
    
    st.subheader("Taha Gungor")
    st.caption("CEO / Artist / 0111")
    st.divider()
    
    col1, col2 = st.columns(2)
    col1.metric("Viewers", f"{np.random.randint(2000, 2500)}")
    col2.metric("Impressions", f"{np.random.randint(1400, 1600)}")
    st.divider()

    st.subheader("Navigation")
    # Streamlit's multi-page feature creates the navigation from files in the `pages/` dir.
    # We don't need buttons with st.rerun() anymore.
    st.page_link("pages/1_Feed.py", label="Feed", icon="🏠")
    st.page_link("pages/2_Jobs.py", label="Jobs (Coming Soon)", icon="💼") # Example of a new page
    st.page_link("pages/3_Messages.py", label="Messages (Coming Soon)", icon="✉️")

    st.divider()
    if st.button("Enter Metaverse", use_container_width=True):
        st.toast("Entering the void... 🔮")
