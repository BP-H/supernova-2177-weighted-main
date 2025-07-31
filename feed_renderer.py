# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Utilities for displaying a simple mock social feed."""

from streamlit_helpers import render_post_card


def render_mock_feed() -> None:
    """Render a short feed of sample posts using ``render_post_card``."""
    sample_posts = [
        ("alice", "https://placekitten.com/400/300", "Cute kitten!"),
        ("bob", "https://placebear.com/400/300", "Bear with me."),
        ("carol", "https://placekitten.com/401/301", "Another kitty."),
    ]
    for username, image, caption in sample_posts:
        render_post_card({"user": username, "image": image, "text": caption})
