# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Utilities for rendering a simple (or custom) social feed."""

from __future__ import annotations

from typing import Iterable, Dict, Any, Tuple

import streamlit as st

from streamlit_helpers import render_post_card

import html

# --- default demo posts -------------------------------------------------------
DEMO_POSTS: list[Tuple[str, str, str]] = [
    (
        "alice",
        "https://picsum.photos/seed/alice/400/300",
        "Enjoying the sunshine!",
    ),
    (
        "bob",
        "https://picsum.photos/seed/bob/400/300",
        "Hiking adventures today.",
    ),
    (
        "carol",
        "https://picsum.photos/seed/carol/400/300",
        "Coffee time at my favourite spot.",
    ),
]


# -----------------------------------------------------------------------------


def render_feed(posts: Iterable[Any] | None = None) -> None:
    """Render a simple scrolling feed of posts."""

    active = st.session_state.get("active_user", "guest")
    if posts is None or not list(posts):
        posts = DEMO_POSTS if active in {"guest", "demo_user"} else []
    else:
        posts = list(posts)

    if not posts:
        st.info("No posts to display")
        return

    for entry in posts:
        if isinstance(entry, dict):
            user = entry.get("user") or entry.get("username", "")
            image = entry.get("image", "")
            caption = entry.get("text") or entry.get("caption", "")
            likes = entry.get("likes", 0)
        else:
            user, image, caption = entry
            likes = 0

        render_post_card({
            "image": image,
            "text": f"**{html.escape(user)}**: {caption}",
            "likes": likes,
        })


def render_mock_feed() -> None:
    """Convenience wrapper that simply calls :func:`render_feed` with demo data."""
    render_feed(DEMO_POSTS)


__all__ = ["render_feed", "render_mock_feed", "DEMO_POSTS"]

