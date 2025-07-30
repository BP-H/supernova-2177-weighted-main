# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""User profile and API configuration page."""

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container
from api_key_input import render_api_key_ui

inject_modern_styles()


def main(main_container=None) -> None:
    """Render the user profile page."""
    if main_container is None:
        main_container = st

    container_ctx = safe_container(main_container)
    with container_ctx:
        st.subheader("👤 Profile")
        st.info("Manage API credentials for advanced features.")
        render_api_key_ui(key_prefix="profile")


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()


if __name__ == "__main__":
    main()
