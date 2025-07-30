# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Messages and chat center with placeholder data."""

from __future__ import annotations

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container

inject_modern_styles()

# Temporary in-memory conversation store
DUMMY_CONVERSATIONS = {
    "alice": [
        {"user": "alice", "text": "Hi there!"},
        {"user": "You", "text": "Hello!"},
    ],
    "bob": [
        {
            "user": "bob",
            "text": "Check out this image!",
            "image": "https://placehold.co/200x150",
        }
    ],
}


def _render_messages(messages: list[dict]) -> None:
    """Display chat messages with optional media."""
    for entry in messages:
        user = entry.get("user", "?")
        text = entry.get("text", "")
        if image := entry.get("image"):
            st.image(image, width=200)
        if video := entry.get("video"):
            st.video(video)
        st.markdown(f"**{user}**: {text}")


def main(main_container=None) -> None:
    """Render the Messages / Chat Center page."""
    if main_container is None:
        main_container = st

    container_ctx = safe_container(main_container)
    with container_ctx:
        st.subheader("💬 Messages")
        st.session_state.setdefault("_conversations", DUMMY_CONVERSATIONS.copy())
        convos = list(st.session_state["_conversations"].keys())
        selected = st.radio("Conversations", convos, key="selected_convo")
        msgs = st.session_state["_conversations"].setdefault(selected, [])
        _render_messages(msgs)
        cols = st.columns([4, 1])
        with cols[0]:
            msg = st.text_input("Message", key="msg_input")
        with cols[1]:
            if st.button("Send", key="send_msg") and msg:
                msgs.append({"user": "You", "text": msg})
                st.session_state.msg_input = ""
                st.experimental_rerun()
        st.divider()
        from .chat import (
            render_video_call_controls,
            render_voice_chat_controls,
        )
        render_video_call_controls()
        st.divider()
        render_voice_chat_controls()


def render() -> None:
    """Wrapper for Streamlit multipage support."""
    main()


if __name__ == "__main__":
    main()
