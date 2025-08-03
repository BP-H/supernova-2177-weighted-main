# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
# ruff: noqa: E501

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List

import streamlit as st

from frontend.theme import apply_theme
from streamlit_helpers import (
    inject_global_styles,
    safe_container,
    sanitize_text,
    theme_toggle,
)

apply_theme("light")
inject_global_styles()


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
    return [
        Post(
            id=start + i,
            user=random.choice(users),
            media=f"https://placehold.co/600x400?text=Post+{start+i+1}",
            caption=f"Demo caption for post {start+i+1}",
            timestamp=now - timedelta(minutes=5 * i),
        )
        for i in range(count)
    ]


def _render_stories(users: List[User]) -> None:
    """Render the horizontal story-strip using st.columns as a robust alternative."""
    if not users:
        st.info("No stories available.")
        return
    cols = st.columns(len(users))
    for i, u in enumerate(users):
        with cols[i]:
            st.image(u.avatar, caption=sanitize_text(u.username), width=60)


def _render_post(post: Post) -> None:
    """Render an individual post card."""
    st.session_state.setdefault("reactions", {}).setdefault(
        post.id, post.reactions.copy()
    )
    comments = st.session_state.setdefault("comments", {}).setdefault(
        post.id, post.comments.copy()
    )

    with st.container():
        header_cols = st.columns([1, 8, 2])
        with header_cols[0]:
            st.image(post.user.avatar, width=48)
        with header_cols[1]:
            st.markdown(
                f"**{sanitize_text(post.user.username)}** {' '.join(post.user.badges)}"
            )
        with header_cols[2]:
            st.caption(f"{post.timestamp:%H:%M}")

        st.image(
            post.media,
            caption=sanitize_text(post.caption),
            use_container_width=True,
        )

        with st.expander("💬 Comments"):
            for c in comments:
                st.write(f"**{sanitize_text(c['user'])}**: {sanitize_text(c['text'])}")
            new_comment = st.text_input("Add a comment", key=f"c_{post.id}")
            if st.button("Post", key=f"cbtn_{post.id}") and new_comment:
                comments.append({"user": "you", "text": new_comment})
                st.session_state["comments"][post.id] = comments
                st.rerun()


def _init_state() -> None:
    """Initialize the session state for the feed."""
    if "posts" not in st.session_state:
        st.session_state["posts"] = _generate_posts(6)
    st.session_state.setdefault("post_offset", 3)
    st.session_state.setdefault("reactions", {})
    st.session_state.setdefault("comments", {})


def main(main_container=None) -> None:
    """Render the feed page."""
    container = main_container or st
    with safe_container(container):
        _init_state()
        theme_toggle("Dark Mode", key_suffix="feed")

        posts = st.session_state["posts"]
        users = _sample_users()

        _render_stories(users)

        for p in posts:
            _render_post(p)
            st.divider()


if __name__ == "__main__":
    main()
