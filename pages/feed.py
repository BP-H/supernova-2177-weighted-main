# pages/1_Feed.py
import streamlit as st

st.title("Feed")

# --- Sticky Search Bar ---
# By putting this first, it will be at the top of the main content area
with st.container():
    st.markdown('<div class="sticky-header">', unsafe_allow_html=True)
    st.text_input("Search", placeholder="Search posts, users, topics...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)


# --- Post Loop ---
# Dummy data for posts
posts = [
    {"author": "UserA", "content": "Just discovered a new supernova! 🔭 #astronomy"},
    {"author": "UserB", "content": "Loving the new features in the latest Streamlit update."},
    {"author": "UserC", "content": "Here's a cool data visualization I made with Python."},
]

for post in posts:
    st.markdown('<div class="post-card">', unsafe_allow_html=True) # Open a styled div
    st.subheader(f"@{post['author']}")
    st.write(post['content'])
    
    # Responsive action buttons
    c1, c2, c3, c4 = st.columns(4)
    c1.button("Like 👍", key=f"like_{post['author']}", use_container_width=True)
    c2.button("Comment 💬", key=f"comment_{post['author']}", use_container_width=True)
    c3.button("Repost 🔁", key=f"repost_{post['author']}", use_container_width=True)
    c4.button("Send ✉️", key=f"send_{post['author']}", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # Close the styled div


# --- Sticky Bottom Nav ---
# We use markdown to inject our custom div with the 'bottom-nav' class
st.markdown("""
<div class="bottom-nav">
    <button>🏠</button>
    <button>👥</button>
    <button>➕</button>
    <button>🔔</button>
    <button>💼</button>
</div>
""", unsafe_allow_html=True)
