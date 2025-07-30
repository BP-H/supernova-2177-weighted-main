# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Validation analysis page."""

import streamlit as st
from ui import render_validation_ui


def main(main_container=None) -> None:
    """Render the validation UI inside a container."""
    if main_container is None:
        main_container = st.container()

    with main_container:
        render_validation_ui()


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
