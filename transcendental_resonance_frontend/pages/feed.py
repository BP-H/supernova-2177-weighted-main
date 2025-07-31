# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Interactive social-feed page with mock stories, posts, reactions, and comments."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any

import random
import streamlit as st

from modern_ui import inject_modern_styles
from streamlit_helpers import theme_selector, safe_container

# ──────────────────────────────────────────────────────────────────────────────
# Sample data models
# ──────────────────────────────────────────────────────────────────────────────


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
    reactions: Dict[str, int] = field(
        default_factory=lambda: {"❤️": 0, "🔥": 0, "👍": 0}
    )
    comments: List[Dict[str, str]] = field(default_factory=list)


# ──────────────────────────────────────────────────────────────────────────────
# Demo content generators
# ──────────────────────────────────────────────────────────────────────────────


def _sample_users() -> List[User]:
    """Return three hard-coded demo users."""
    return [
        User("alice", "https://placehold.co/48x48?text=A", "Explorer", ["🌟 super"]),
        User("bob", "https://placehold.co/48x48?text=B", "Creator", ["🥇 pro"]),
        User("carol", "https://placehold.co/48x48?text=C", "Hacker", ["💯 elite"]),
    ]


def _generate_posts(count: int, start: int = 0) -> List[Post]:
    """Generate `count` pseudo-random demo posts."""
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
                caption=f"demo caption {start+i+1}",
                timestamp=now - timedelta(minutes=5 * i),
            )
        )
    return posts


# ──────────────────────────────────────────────────────────────────────────────
# Rendering helpers
# ──────────────────────────────────────────────────────────────────────────────

_STORY_CSS = """
<style>
.story-strip{display:flex;overflow-x:auto;gap:0.5rem;padding:0.5rem;margin-bottom:1rem;}
.story-item{flex:0 0 auto;text-align:center;font-size:0.8rem;color:var(--text-muted);}
.story-item img{border-radius:50%;border:2px solid var(--accent);}
.post-card{background:var(--card);padding:0.5rem 0;border-radius:12px;
           margin-bottom:1rem;box-shadow:0 1px 2px rgba(0,0,0,0.05);}
.post-header{display:flex;align-items:center;gap:0.5rem;padding:0 0.5rem;margin-bottom:0.5rem;}
.post-header img{border-radius:50%;width:40px;height:40px;}
.post-caption{padding:0.25rem 0.5rem;}
</style>
"""


def _render_stories(users: List[User]) -> None:
    """Render the horizontal story-strip."""
    st.markdown(_STORY_CSS, unsafe_allow_html=True)
    html = "<div class='story-strip'>"
    for u in users:
        html += (
            f"<div class='story-item'><img src='{u.avatar}' width='60'/><br>{u.username}</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def _render_post(post: Post) -> None:
    """Render an individual post card with reactions & comments."""
    with st.container():
        st.markdown("<div class='post-card'>", unsafe_allow_html=True)
        # Header
        st.markdown(
            f"<div class='post-header'><img src='{post.user.avatar}'/>"
            f"<strong>{post.user.username}</strong> "
            f"<span>{' '.join(post.user.badges)}</span>"
            f"<span style='margin-left:auto;font-size:0.75rem;'>{post.timestamp:%H:%M}</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        # Media
        st.image(post.media, use_column_width=True, output_format="JPEG")
        # Caption
        st.markdown(f"<div class='post-caption'>{post.caption}</div>", unsafe_allow_html=True)

        # Reactions & comments
        cols = st.columns(len(post.reactions) + 1)
        for idx, (emoji, count) in enumerate(post.reactions.items()):
            if cols[idx].button(f"{emoji} {count}", key=f"react_{post.id}_{emoji}"):
                post.reactions[emoji] += 1
                st.experimental_rerun()

        # Pop-over for comments
        with cols[-1]:
            with st.popover("💬"):
                st.markdown("### comments")
                for c in post.comments:
                    st.write(f"**{c['user']}**: {c['text']}")
                new = st.text_input("Add a comment", key=f"c_{post.id}")
                if st.button("post", key=f"cbtn_{post.id}") and new:
                    post.comments.append({"user": "you", "text": new})
                    st.experimental_rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Page-state helpers
# ──────────────────────────────────────────────────────────────────────────────


def _init_state() -> None:
    if "posts" not in st.session_state:
        st.session_state["posts"] = _generate_posts(6)
    st.session_state.setdefault("post_offset", 3)


# ──────────────────────────────────────────────────────────────────────────────
# Page entrypoints
# ──────────────────────────────────────────────────────────────────────────────

inject_modern_styles()


def _page_body() -> None:
    """Render the main feed inside the current container."""
    _init_state()

    theme_selector("Theme", key_suffix="feed")
    st.toggle("beta mode", key="beta_mode")

    posts: List[Post] = st.session_state["posts"]
    users = _sample_users()

    _render_stories(users)

    offset = st.session_state["post_offset"]
    for p in posts[:offset]:
        _render_post(p)

    if offset < len(posts):
        if st.button("load more", key="load_more"):
            st.session_state["post_offset"] += 3
            st.experimental_rerun()
    else:
        # Fetch / generate additional demo posts
        if st.button("load more", key="load_more"):
            start = len(posts)
            posts.extend(_generate_posts(3, start=start))
            st.session_state["post_offset"] += 3
            st.experimental_rerun()


def main(main_container=None) -> None:
    """Render the feed inside ``main_container`` (or root Streamlit)."""
    container = main_container or st
    with safe_container(container):
        _page_body()


def render() -> None:
    """Wrapper for Streamlit multipage routing."""
    main()


if __name__ == "__main__":
    render()

