# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Validation analysis page."""

import streamlit as st
from ui import render_validation_ui


def main(main_container=None) -> None:
    """Render the validation UI within ``main_container``."""
    # Determine the main container to use
    container = main_container if main_container is not None else st.container()

    try:
        # Try to use the container as a context manager
        with container:
            render_validation_ui()
    except AttributeError:
        # If the container isn't a context manager, call directly
        render_validation_ui()

        render_validation_ui()
    else:
        render_validation_ui(main_container=main_container)


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
