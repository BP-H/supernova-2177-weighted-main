# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Friends & Followers page."""

import streamlit as st
from social_tabs import render_social_tab
from streamlit_helpers import safe_container


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
