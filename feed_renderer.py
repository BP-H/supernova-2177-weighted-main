# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Simple renderer for a social feed."""

from __future__ import annotations

from typing import Iterable, Dict, Any

import streamlit as st

from streamlit_helpers import render_post_card

# Demo posts used when none are provided
DEMO_POSTS: list[dict[str, Any]] = [
    {
        "image": "https://placekitten.com/400/300",
        "text": "Look at this cute kitten!",
        "likes": 5,
    },
    {
        "image": "https://placekitten.com/500/300",
        "text": "Another adorable cat appears.",
        "likes": 3,
    },
    {
        "image": "https://placekitten.com/450/300",
        "text": "Cats everywhere!",
        "likes": 8,
    },
]


def render_feed(posts: Iterable[Dict[str, Any]] | None = None) -> None:
    """Render each post using :func:`render_post_card`."""
    if posts is None:
        posts = DEMO_POSTS

    posts = list(posts)
    if not posts:
        st.info("No posts to display")
        return

    for post in posts:
        render_post_card(post)
