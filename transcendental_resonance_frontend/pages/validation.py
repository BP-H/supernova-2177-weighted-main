# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Validation analysis page."""

import streamlit as st
from streamlit_helpers import safe_container
from ui import render_validation_ui


def main(main_container=None) -> None:
    """Render the validation UI inside ``main_container`` safely."""
    if main_container is None:
        main_container = st

    container_ctx = safe_container(main_container)

    try:
        with container_ctx:
            render_validation_ui(main_container=main_container)
    except AttributeError:
        render_validation_ui(main_container=main_container)


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
