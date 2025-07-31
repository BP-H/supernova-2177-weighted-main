# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Messages and chat center with placeholder data."""

from __future__ import annotations

import asyncio
import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container, header, theme_selector
from transcendental_resonance_frontend.src.utils import api
from status_indicator import render_status_icon

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


def _run_async(coro):
    """Execute ``coro`` in any event loop state."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        return loop.run_until_complete(coro)


def send_message(target: str, text: str) -> None:
    """Send ``text`` to ``target`` handling offline mode and errors."""
    try:
        if api.OFFLINE_MODE:
            st.session_state["_conversations"].setdefault(target, []).append(
                {"user": "You", "text": text}
            )
        else:
            result = _run_async(api.api_call("POST", f"/messages/{target}", {"text": text}))
            if result is None:
                st.toast("Message failed to send", icon="⚠️")
    except Exception as exc:  # pragma: no cover - UI feedback
        st.toast(f"Failed to send message: {exc}", icon="⚠️")


def main(main_container=None) -> None:
    """Render the Messages / Chat Center page."""
    if main_container is None:
        main_container = st
    theme_selector("Theme", key_suffix="msg_center")

    container_ctx = safe_container(main_container)
    with container_ctx:
        header_col, status_col = st.columns([8, 1])
        with header_col:
            header("💬 Messages")
        with status_col:
            render_status_icon()
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
                send_message(selected, msg)
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
