# pages/feed.py
import streamlit as st
import numpy as np
from faker import Faker
import time

# Data Generation (placeholder posts)
@st.cache_data
def generate_post_data(num_posts=5):
    """Generates placeholder post data for the feed."""
    fake = Faker()
    posts = []
    for i in range(num_posts):
        posts.append({
            "id": f"post_{i}_{int(time.time())}",
            "author_name": fake.name(),
            "author_title": f"{fake.job()} at {fake.company()}",
            "author_avatar": f"https://avatar.iran.liara.run/public/{np.random.randint(1, 100)}",
            "post_text": fake.paragraph(nb_sentences=np.random.randint(3, 7)),
            "image_url": f"https://picsum.photos/800/400?random={np.random.randint(1, 1000)}",
            "likes": np.random.randint(5, 150),
            "comments": np.random.randint(0, 40),
            "reposts": np.random.randint(0, 15),
        })
    return posts

# UI Rendering for a single post
def render_post(post):
    """Renders a single post card with custom styling."""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.image(post["author_avatar"], width=50)
    with col2:
        st.subheader(post["author_name"])
        st.caption(post["author_title"])
    st.write(post["post_text"])
    if post["image_url"]:
        st.image(post["image_url"], use_container_width=True)
    st.caption(f"🌍 {post['likes']} likes • {post['comments']} comments • {post['reposts']} reposts")
    st.divider()
    cols_actions = st.columns(4)
    cols_actions[0].button("👍 Like", key=f"like_{post['id']}", use_container_width=True)
    cols_actions[1].button("💬 Comment", key=f"comment_{post['id']}", use_container_width=True)
    cols_actions[2].button("🔁 Repost", key=f"repost_{post['id']}", use_container_width=True)
    cols_actions[3].button("📤 Send", key=f"send_{post['id']}", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main function for page loading
def main():
    st.markdown("### Recent Activity (Feed Page)")
    st.caption("This is a demonstration feed using placeholder data. Implement real data here.")
    posts_data = generate_post_data()
    for post in posts_data:
        render_post(post)

if __name__ == "__main__":
    main()
