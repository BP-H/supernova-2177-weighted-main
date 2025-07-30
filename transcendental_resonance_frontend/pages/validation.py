# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Validation analysis page."""

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container
from ui import render_validation_ui

inject_modern_styles()


def _page_decorator(func):
    if hasattr(st, "experimental_page"):
        return st.experimental_page("Validation")(func)
    return func


@_page_decorator
def main(main_container=None) -> None:
    """Render the validation UI inside a container safely."""
    if main_container is None:
        main_container = st

    container_ctx = safe_container(main_container)

    try:
        with container_ctx:
            render_validation_ui(main_container=main_container)
    except AttributeError:
        # Fallback: in case container_ctx fails due to unexpected type
        render_validation_ui(main_container=main_container)

def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
