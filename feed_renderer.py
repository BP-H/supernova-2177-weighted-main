# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Utilities for rendering a simple (or custom) social feed."""

from __future__ import annotations

from typing import Iterable, Dict, Any

import streamlit as st

from streamlit_helpers import render_post_card

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
    """
    Render a list of post dictionaries using :func:`render_post_card`.

    Parameters
    ----------
    posts
        An iterable of post dictionaries.  If *None* (default) the built-in
        ``DEMO_POSTS`` will be shown.  Each post dict should at minimum contain
        ``image`` and ``text`` keys; ``user`` and ``likes`` are optional.
    """
    if posts is None:
        posts = DEMO_POSTS

    posts = list(posts)
    if not posts:
        st.info("No posts to display")
        return

    for post in posts:
        render_post_card(post)


def render_mock_feed() -> None:
    """Convenience wrapper that simply calls :func:`render_feed` with demo data."""
    render_feed(DEMO_POSTS)


__all__ = ["render_feed", "render_mock_feed", "DEMO_POSTS"]

