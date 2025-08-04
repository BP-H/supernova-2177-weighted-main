# pages/feed.py

import streamlit as st
import numpy as np
from faker import Faker
import time
import random

fake = Faker()

@st.cache_data
def generate_post_data(start_index=0, num_posts=5):
    """Generates realistic post data for the feed."""
    posts = []
    for i in range(start_index, start_index + num_posts):
        name = fake.name()
        seed = name.replace(" ", "") + str(random.randint(0, 99999))
        posts.append({
            "id": f"post_{i}_{int(time.time())}",
            "author_name": name,
            "author_title": f"{fake.job()} at {fake.company()} • {random.choice(['1st', '2nd', '3rd'])}",
            "author_avatar": f"https://api.dicebear.com/7.x/thumbs/svg?seed={seed}",
            "post_text": fake.paragraph(nb_sentences=random.randint(1, 4)),
            "image_url": random.choice([None, f"https://picsum.photos/800/400?random={np.random.randint(1, 1000)}"]),
            "edited": random.choice([True, False]),
            "promoted": random.choice([True, False]),
            "likes": np.random.randint(10, 500),
            "comments": np.random.randint(0, 100),
            "reposts": np.random.randint(0, 50),
        })
    return posts

def render_post(post):
    """Renders a single post card."""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        if post["author_avatar"]:
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

    like_col, comment_col, repost_col, send_col = st.columns(4)
    with like_col:
        st.button("👍 Like", key=f"like_{post['id']}", use_container_width=True)
    with comment_col:
        st.button("💬 Comment", key=f"comment_{post['id']}", use_container_width=True)
    with repost_col:
        st.button("🔁 Repost", key=f"repost_{post['id']}", use_container_width=True)
    with send_col:
        st.button("➡️ Send", key=f"send_{post['id']}", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.markdown("### Your Feed ↩️")
    st.info("This is a prototype content stream. Posts below are AI-generated placeholders for testing visual flow.")

    # Init offset
    if "feed_offset" not in st.session_state:
        st.session_state.feed_offset = 0
    if "feed_data" not in st.session_state:
        st.session_state.feed_data = []

    # Load initial or more
    if st.session_state.feed_offset == 0 or st.session_state.get("load_more_trigger"):
        new_posts = generate_post_data(start_index=st.session_state.feed_offset, num_posts=4)
        st.session_state.feed_data.extend(new_posts)
        st.session_state.feed_offset += 4
        st.session_state.load_more_trigger = False

    # Render posts
    for post in st.session_state.feed_data:
        render_post(post)

    st.write("")
    if st.button("🔄 Load more"):
        st.session_state.load_more_trigger = True
        st.experimental_rerun()

if __name__ == "__main__":
    main()
