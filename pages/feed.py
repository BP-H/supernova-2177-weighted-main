# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
# ruff: noqa: E501

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List

import streamlit as st
import asyncpg
from sqlalchemy.exc import OperationalError

from frontend.theme import apply_theme
from streamlit_helpers import (
    inject_global_styles,
    safe_container,
    sanitize_text,
    theme_toggle,
)

# Apply theme and global styles
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

async def _fetch_users_from_db() -> List[User]:
    """Fetch users from the database."""
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="your_password",  # Replace with your DB credentials
            database="supernova_db",
            host="localhost",
            port=5432
        )
        rows = await conn.fetch("SELECT username, avatar, bio, badges FROM users LIMIT 3")
        users = [
            User(
                username=row["username"],
                avatar=row["avatar"],
                bio=row["bio"],
                badges=row["badges"] if row["badges"] else []
            )
            for row in rows
        ]
        await conn.close()
        return users
    except Exception as e:
        st.error(f"Failed to fetch users from database: {e}")
        return []

async def _fetch_posts_from_db(count: int, start: int = 0) -> List[Post]:
    """Fetch posts from the database."""
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="your_password",  # Replace with your DB credentials
            database="supernova_db",
            host="localhost",
            port=5432
        )
        users = await _fetch_users_from_db()
        user_map = {u.username: u for u in users}
        rows = await conn.fetch(
            "SELECT id, username, media, caption, timestamp, reactions, comments "
            "FROM posts WHERE id >= $1 ORDER BY id LIMIT $2",
            start, count
        )
        posts = [
            Post(
                id=row["id"],
                user=user_map.get(row["username"], User("unknown", "https://placehold.co/48x48?text=U", "Unknown")),
                media=row["media"],
                caption=row["caption"],
                timestamp=row["timestamp"],
                reactions=row["reactions"] if row["reactions"] else {"❤️": 0, "🔥": 0, "👍": 0},
                comments=row["comments"] if row["comments"] else []
            )
            for row in rows
        ]
        await conn.close()
        return posts
    except Exception as e:
        st.error(f"Failed to fetch posts from database: {e}")
        return []

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
        # Try database first
        try:
            posts = asyncio.run(_fetch_posts_from_db(6))
            if posts:
                st.session_state["posts"] = posts
            else:
                st.session_state["posts"] = _generate_posts(6)
        except Exception as e:
            st.error(f"Database initialization failed: {e}")
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

        # Fetch users, try database first
        users = asyncio.run(_fetch_users_from_db())
        if not users:
            users = _sample_users()

        posts = st.session_state["posts"]

        _render_stories(users)

        for p in posts:
            _render_post(p)
            st.divider()

if __name__ == "__main__":
    main()