# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Agent insights page."""

import streamlit as st
from agent_ui import render_agent_insights_tab


def main(main_container=None) -> None:
    """Render the Agent Insights page within ``main_container``."""
    if main_container is None:
        main_container = st

    with main_container:
        render_agent_insights_tab(main_container=main_container)
