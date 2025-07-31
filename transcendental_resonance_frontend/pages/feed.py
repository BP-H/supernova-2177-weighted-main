# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Simple page showcasing a mock social feed."""

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container
from feed_renderer import render_mock_feed

inject_modern_styles()


def main(main_container=None) -> None:
    """Render the mock feed within ``main_container``."""
    container = main_container if main_container is not None else st
    with safe_container(container):
        render_mock_feed()


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
