# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Validation analysis page."""

import streamlit as st
from ui import render_validation_ui


def main(main_container=None) -> None:
from contextlib import nullcontext

def render_validation_entrypoint(main_container=None):
    """Render the validation UI inside a valid container context."""

    # Resolve the actual container to use
    if main_container is None:
        main_container = st

    # Determine whether we can use `with main_container:` directly
    container_ctx = (
        main_container()
        if callable(main_container)
        else main_container
        if hasattr(main_container, "__enter__")
        else nullcontext()
    )

    # Safely render within context (fallback if necessary)
    try:
        with container_ctx:
            render_validation_ui(main_container=main_container)
    except AttributeError:
        # fallback in case `with` is invalid for container
        render_validation_ui(main_container=main_container)



def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
