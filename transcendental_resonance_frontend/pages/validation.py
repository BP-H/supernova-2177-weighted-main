# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Validation analysis page."""

import streamlit as st
from ui import render_validation_ui


def main(main_container=None) -> None:
    """Render the validation UI within ``main_container``."""
    if main_container is None:
        render_validation_ui()
    else:
        render_validation_ui(main_container=main_container)


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
