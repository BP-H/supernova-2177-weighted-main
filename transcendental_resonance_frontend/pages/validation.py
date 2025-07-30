# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Validation analysis page."""

import streamlit as st
from ui import render_validation_ui


def main(main_container=None) -> None:
    """Render the validation UI within ``main_container``."""
    container = main_container if main_container is not None else st.container()

    try:
        with container:
            render_validation_ui()
    except AttributeError:
        # ``container`` may not be a context manager
        render_validation_ui()


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
