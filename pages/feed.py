import streamlit as st
import numpy as np
from faker import Faker
import time
import random

@st.cache_data
def generate_post_data(num_posts=15):
    """Generates realistic post data for the feed."""
    fake = Faker()
    posts = []
    for i in range(num_posts):
        posts.append({
            "id": f"post_{i}_{int(time.time())}",
            "author_name": fake.name(),
            "author_title": f"{fake.job()} at {fake.company()}",
            "author_avatar": f"https://avatar.iran.liara.run/public/{np.random.randint(1, 100)}",
            "post_text": fake.paragraph(nb_sentences=random.randint(3, 6)),
            "image_url": random.choice([None, f"https://picsum.photos/800/400?random={np.random.randint(1, 1000)}"]),
            "likes": np.random.randint(10, 500),
            "comments": np.random.randint(0, 100),
        })
    return posts

def _render_single_post(post):
    """Renders a single post using the 'content-card' CSS class."""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.image(post["author_avatar"], width=48)
    with col2:
        st.subheader(post["author_name"])
        st.caption(post["author_title"])

    st.write(post["post_text"])
    if post["image_url"]:
        st.image(post["image_url"], use_container_width=True)

    st.caption(f"{post['likes']} likes • {post['comments']} comments")
    st.markdown("---")
    cols_actions = st.columns(4)
    actions = ["👍 Like", "💬 Comment", "🔁 Repost", "➡️ Send"]
    for i, label in enumerate(actions):
        cols_actions[i].button(label, key=f"{label}_{post['id']}", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render():
    """The main function for the feed page."""
    # A simple container to create a new post
    with st.container(border=True):
        st.text_area("What's on your mind?", placeholder="Share an update...", height=100)
        st.button("Post", type="primary")

    st.divider()

    # Generate and display the feed
    posts = generate_post_data(num_posts=15)
    for post in posts:
        _render_single_post(post)
