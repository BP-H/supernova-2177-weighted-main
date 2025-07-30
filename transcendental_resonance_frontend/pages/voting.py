# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Governance and voting page."""

import streamlit as st
from voting_ui import render_voting_tab


def main(main_container=None) -> None:
    """Render the Governance and Voting page inside ``main_container``."""
    if main_container is None:
        main_container = st

    with main_container:
        render_voting_tab(main_container=main_container)


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()
