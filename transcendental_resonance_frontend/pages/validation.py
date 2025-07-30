# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Validation analysis page."""

import streamlit as st
from contextlib import nullcontext
from ui import render_validation_ui


def main(main_container=None) -> None:
    """Render the validation UI inside a container safely."""
    if main_container is None:
        main_container = st

    container_ctx = (
        main_container()
        if callable(main_container)
        else main_container
        if hasattr(main_container, "__enter__")
        else nullcontext()
    )

    try:
        with container_ctx:
            render_validation_ui(main_container=main_container)
    except AttributeError:
        # Fallback: in case container_ctx fails due to unexpected type
        render_validation_ui(main_container=main_container)

def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
