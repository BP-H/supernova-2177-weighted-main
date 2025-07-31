# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Chat page with text, video, and voice features."""

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container, header, theme_selector
from status_indicator import render_status_icon
from chat_ui import (
    render_chat_interface,
    render_video_call_controls,
    render_voice_chat_controls,
)

inject_modern_styles()


def main(main_container=None) -> None:
    """Render the chat page."""
    if main_container is None:
        main_container = st
    theme_selector("Theme", key_suffix="chat")

    container_ctx = safe_container(main_container)
    with container_ctx:
        header_col, status_col = st.columns([8, 1])
        with header_col:
            header("💬 Chat")
        with status_col:
            render_status_icon()
        render_chat_interface()
        st.divider()
        render_video_call_controls()
        st.divider()
        render_voice_chat_controls()


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()


if __name__ == "__main__":
    main()
