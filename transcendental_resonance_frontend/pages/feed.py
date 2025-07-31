"""Interactive social feed with mock posts."""

# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict

import random
import streamlit as st

from modern_ui import inject_modern_styles
from streamlit_helpers import theme_selector, safe_container


@dataclass
class User:
    username: str
    avatar: str
    bio: str
    badges: List[str] = field(default_factory=list)


@dataclass
class Post:
    id: int
    user: User
    media: str
    caption: str
    timestamp: datetime
    reactions: Dict[str, int] = field(default_factory=lambda: {"❤️": 0, "🔥": 0, "👍": 0})
    comments: List[Dict[str, str]] = field(default_factory=list)


def _sample_users() -> List[User]:
    return [
        User("Alice", "https://placehold.co/48x48?text=A", "Explorer", ["🌟 Super"],),
        User("Bob", "https://placehold.co/48x48?text=B", "Creator", ["🥇 Pro"]),
        User("Carol", "https://placehold.co/48x48?text=C", "Hacker", ["💯 Elite"]),
    ]


def _generate_posts(count: int, start: int = 0) -> List[Post]:
    users = _sample_users()
    now = datetime.utcnow()
    posts: List[Post] = []
    for i in range(count):
        u = random.choice(users)
        posts.append(
            Post(
                id=start + i,
                user=u,
                media=f"https://placehold.co/600x400?text=Post+{start+i+1}",
                caption=f"Demo caption {start+i+1}",
                timestamp=now - timedelta(minutes=5 * i),
            )
        )
    return posts


# ──────────────────────────────────────────────────────────────────────────────
# Rendering helpers
# ──────────────────────────────────────────────────────────────────────────────

STORY_CSS = """
<style>
.story-strip{display:flex;overflow-x:auto;gap:0.5rem;padding:0.5rem;margin-bottom:1rem;}
.story-item{flex:0 0 auto;text-align:center;font-size:0.8rem;color:var(--text-muted);}
.story-item img{border-radius:50%;border:2px solid var(--accent);} 
.post-card{background:var(--card);padding:0.5rem 0;border-radius:12px;margin-bottom:1rem;box-shadow:0 1px 2px rgba(0,0,0,0.05);} 
.post-header{display:flex;align-items:center;gap:0.5rem;padding:0 0.5rem;margin-bottom:0.5rem;}
.post-header img{border-radius:50%;width:40px;height:40px;}
.post-media{width:100%;border-radius:8px;}
.post-actions{display:flex;align-items:center;gap:0.5rem;padding:0 0.5rem;}
.post-caption{padding:0.25rem 0.5rem;}
</style>
"""


def _render_stories(users: List[User]) -> None:
    st.markdown(STORY_CSS, unsafe_allow_html=True)
    html = "<div class='story-strip'>"
    for u in users:
        html += (
            f"<div class='story-item'><img src='{u.avatar}' width='60'/><br>{u.username}</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def _render_post(post: Post) -> None:
    with st.container():
        st.markdown("<div class='post-card'>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='post-header'><img src='{post.user.avatar}'/>"
            f"<strong>{post.user.username}</strong>"
            f" <span>{' '.join(post.user.badges)}</span>"
            f" <span style='margin-left:auto;font-size:0.75rem;'>{post.timestamp:%H:%M}</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.image(post.media, use_column_width=True, output_format="JPEG")
        st.markdown(f"<div class='post-caption'>{post.caption}</div>", unsafe_allow_html=True)
        with st.container():
            cols = st.columns(len(post.reactions) + 1)
            for idx, (emoji, count) in enumerate(post.reactions.items()):
                if cols[idx].button(f"{emoji} {count}", key=f"react_{post.id}_{emoji}"):
                    post.reactions[emoji] += 1
                    st.experimental_rerun()
            with cols[-1]:
                with st.popover("💬"):
                    st.markdown("### Comments")
                    for c in post.comments:
                        st.write(f"**{c['user']}**: {c['text']}")
                    new = st.text_input("Add a comment", key=f"c_{post.id}")
                    if st.button("Post", key=f"cbtn_{post.id}") and new:
                        post.comments.append({"user": "You", "text": new})
                        st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        if st.session_state.get("beta_mode"):
            if st.button("Remix", key=f"remix_{post.id}"):
                st.toast("AI Remix pending")


def _init_state() -> None:
    if "posts" not in st.session_state:
        st.session_state["posts"] = _generate_posts(6)
    st.session_state.setdefault("post_offset", 3)


# ──────────────────────────────────────────────────────────────────────────────
# Main entry
# ──────────────────────────────────────────────────────────────────────────────

inject_modern_styles()


def main() -> None:
    _init_state()
    theme_selector("Theme", key_suffix="feed")
    st.toggle("Beta Mode", key="beta_mode")

    posts: List[Post] = st.session_state["posts"]
    users = _sample_users()
    _render_stories(users)

    offset = st.session_state["post_offset"]
    for p in posts[:offset]:
        _render_post(p)

    if offset < len(posts):
        if st.button("Load More", key="load_more"):
            st.session_state["post_offset"] += 3
            st.experimental_rerun()
    else:
        if st.button("Load More", key="load_more"):  # generate more
            start = len(posts)
            posts.extend(_generate_posts(3, start=start))
            st.session_state["post_offset"] += 3
            st.experimental_rerun()


def render() -> None:
    container_ctx = safe_container(st)
    with container_ctx:
        main()


if __name__ == "__main__":
    render()
