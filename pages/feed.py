# pages/feed.py
import streamlit as st
import numpy as np
from faker import Faker
import time
import random

# Data Generation (realistic LinkedIn-like posts)
@st.cache_data
def generate_post_data(num_posts=5):
    """Generates realistic post data for the feed."""
    fake = Faker()
    posts = []
    for i in range(num_posts):
        posts.append({
            "id": f"post_{i}_{int(time.time())}",
            "author_name": fake.name(),
            "author_title": f"{fake.job()} at {fake.company()} • {random.choice(['1st', '2nd', '3rd'])}",
            "author_avatar": f"https://avatar.iran.liara.run/public/{np.random.randint(1, 100)}",
            "post_text": fake.paragraph(nb_sentences=random.randint(1, 4)),
            "image_url": random.choice([None, f"https://picsum.photos/800/400?random={np.random.randint(1, 1000)}"]),
            "edited": random.choice([True, False]),
            "promoted": random.choice([True, False]),
            "likes": np.random.randint(10, 500),
            "comments": np.random.randint(0, 100),
            "reposts": np.random.randint(0, 50),
        })
    return posts

# UI Rendering for a single post (LinkedIn-style card)
def render_post(post):
    """Renders a single post card."""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        st.image(post["author_avatar"], width=48)
    with col2:
        st.subheader(post["author_name"])
        st.caption(post["author_title"])
    if post["promoted"]:
        st.caption("Promoted")
    st.write(post["post_text"])
    if post["image_url"]:
        st.image(post["image_url"], use_container_width=True)
    edited_text = " • Edited" if post["edited"] else ""
    st.caption(f"{post['likes']} likes • {post['comments']} comments • {post['reposts']} reposts{edited_text}")
    cols_actions = st.columns(4)
    cols_actions[0].button("👍 Like", key=f"like_{post['id']}", help="Like this post")
    cols_actions[1].button("💬 Comment", key=f"comment_{post['id']}", help="Add a comment")
    cols_actions[2].button("🔁 Repost", key=f"repost_{post['id']}", help="Repost this")
    cols_actions[3].button("➡️ Send", key=f"send_{post['id']}", help="Send to someone")
    st.markdown('</div>', unsafe_allow_html=True)

# Main function for page loading
def main():
    st.markdown("### Your Feed")
    posts_data = generate_post_data()
    for post in posts_data:
        render_post(post)

if __name__ == "__main__":
    main()
