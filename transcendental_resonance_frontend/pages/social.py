# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Friends & Followers page."""

import streamlit as st
from social_tabs import render_social_tab


def main(main_container=None) -> None:
    """Render the social page content within ``main_container``."""
    if main_container is None:
        main_container = st

    render_social_tab(main_container=main_container)


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
