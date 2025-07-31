# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Utilities for rendering a simple (or custom) social feed."""

from __future__ import annotations

from typing import Iterable, Dict, Any

import streamlit as st

import html

from streamlit_helpers import sanitize_text

# --- default demo posts -------------------------------------------------------
DEMO_POSTS: list[dict[str, Any]] = [
    {
        "user": "alice",
        "image": "https://placekitten.com/400/300",
        "text": "Cute kitten!",
        "likes": 5,
    },
    {
        "user": "bob",
        "image": "https://placebear.com/400/300",
        "text": "Bear with me.",
        "likes": 3,
    },
    {
        "user": "carol",
        "image": "https://placekitten.com/401/301",
        "text": "Another kitty.",
        "likes": 8,
    },
]


# -----------------------------------------------------------------------------


def render_feed(posts: Iterable[Dict[str, Any]] | None = None) -> None:
    """Render a list of posts as simple cards."""
    if posts is None:
        posts = DEMO_POSTS

    posts = list(posts)
    if not posts:
        st.info("No posts to display")
        return

    for post in posts:
        user = sanitize_text(post.get("user", ""))
        caption = sanitize_text(post.get("caption") or post.get("text", ""))
        image = sanitize_text(post.get("image", ""))

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if user:
            st.markdown(f"**{html.escape(user)}**")
        if image:
            st.image(image, use_column_width=True)
        if caption:
            st.markdown(html.escape(caption))
        st.markdown(
            "<div style='font-size:1.2rem;'>❤️ 🔁 💬</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_mock_feed() -> None:
    """Convenience wrapper that simply calls :func:`render_feed` with demo data."""
    render_feed(DEMO_POSTS)


__all__ = ["render_feed", "render_mock_feed", "DEMO_POSTS"]

