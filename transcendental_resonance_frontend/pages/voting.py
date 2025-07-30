# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Governance and voting page."""

import streamlit as st
from voting_ui import render_voting_tab
from contextlib import nullcontext


def main(main_container=None) -> None:
    """Render the Governance and Voting page inside ``main_container``."""
    if main_container is None:
        main_container = st

    container_ctx = (
        main_container()
        if callable(main_container)
        else main_container
        if hasattr(main_container, "__enter__")
        else nullcontext()
    )
    with container_ctx:
        render_voting_tab(main_container=main_container)


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
