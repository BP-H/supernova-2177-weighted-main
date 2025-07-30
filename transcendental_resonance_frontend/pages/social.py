# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Friends & Followers page."""

import streamlit as st
from modern_ui import inject_modern_styles
from social_tabs import render_social_tab
from streamlit_helpers import safe_container

inject_modern_styles()


def main(main_container=None) -> None:
    """Render the social page content within ``main_container``."""
    if main_container is None:
        main_container = st

    container_ctx = safe_container(main_container)
    with container_ctx:
        render_social_tab()


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
