# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Messages and chat page wrapping reusable chat UI."""

from __future__ import annotations

import streamlit as st

from transcendental_resonance_frontend.ui.chat_ui import render_chat_ui


def main(main_container=None) -> None:
    render_chat_ui(main_container)


def render() -> None:
    main()


if __name__ == "__main__":
    main()
