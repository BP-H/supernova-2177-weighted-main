# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Messages and chat center with placeholder data."""

from __future__ import annotations

import asyncio
import streamlit as st
from frontend.light_theme import inject_light_theme
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container, header, theme_selector
from transcendental_resonance_frontend.src.utils import api
from status_indicator import render_status_icon

from frontend.light_theme import inject_light_theme
inject_light_theme()

# ──────────────────────────────────────────────────────────────────────────────
# Styles
# ──────────────────────────────────────────────────────────────────────────────
MESSAGE_CSS = """
<style>
.msg-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.msg-bubble {
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    max-width: 80%;
    word-wrap: break-word;
}
.msg-bubble.receiver {
    align-self: flex-start;
    background: #eee;
}
.msg-bubble.sender {
    align-self: flex-end;
    background: #DCF8C6;
}
.msg-row {
    display: flex;
    gap: 0.5rem;
    align-items: flex-end;
}
.msg-row.sender {
    flex-direction: row-reverse;
}
.msg-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
}
</style>
"""

inject_modern_styles()

# ──────────────────────────────────────────────────────────────────────────────
# Dummy data
# ──────────────────────────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
def _render_messages(messages: list[dict]) -> None:
    """Display chat messages with optional media using bubbles."""
    st.markdown(MESSAGE_CSS, unsafe_allow_html=True)
    st.markdown("<div class='msg-container'>", unsafe_allow_html=True)

    for entry in messages:
        user = entry.get("user", "?")
        text = entry.get("text", "")
        cls = "sender" if user == "You" else "receiver"
        avatar = entry.get("avatar") or f"https://robohash.org/{user}.png?size=50x50"

        st.markdown(f"<div class='msg-row {cls}'>", unsafe_allow_html=True)
        st.markdown(f"<img class='msg-avatar' src='{avatar}' />", unsafe_allow_html=True)
        if image := entry.get("image"):
            st.image(image, use_container_width=True)
        if video := entry.get("video"):
            st.video(video)
        bubble = f"<div class='msg-bubble {cls}'><strong>{user}:</strong> {text}</div>"
        st.markdown(bubble, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _run_async(coro):
    """Execute *coro* regardless of whether an event loop is already running."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    if loop.is_running():
        return asyncio.run_coroutine_threadsafe(coro, loop).result()
    return loop.run_until_complete(coro)


def send_message(target: str, text: str) -> None:
    """Append or POST a message, depending on offline mode."""
    try:
        if api.OFFLINE_MODE:
            st.session_state["_conversations"].setdefault(target, []).append(
                {"user": "You", "text": text}
            )
        else:
            result = _run_async(api.api_call("POST", f"/messages/{target}", {"text": text}))
            if result is None:
                st.toast("Message failed to send", icon="⚠️")
    except Exception as exc:  # pragma: no cover – UI feedback only
        st.toast(f"Failed to send message: {exc}", icon="⚠️")

# ──────────────────────────────────────────────────────────────────────────────
# Page
# ──────────────────────────────────────────────────────────────────────────────
def main(main_container=None) -> None:
    """Render the Messages / Chat Center page."""
    if main_container is None:
        main_container = st

    page = "messages_center"
    st.session_state["active_page"] = page
    key_prefix = f"{page}_"
    theme_selector("Theme", key_suffix="msg_center")

    with safe_container(main_container):
        header_col, status_col = st.columns([8, 1])
        with header_col:
            header("💬 Messages")
        with status_col:
            render_status_icon()

        # Initialise conversations on first visit
        st.session_state.setdefault("_conversations", DUMMY_CONVERSATIONS.copy())
        convos = list(st.session_state["_conversations"].keys())

        # Top-level tabs
        tab_msgs, tab_calls = st.tabs(["Messages", "Calls"])

        # ── Messages tab ───────────────────────────────────────────
        with tab_msgs:
            left, right = st.columns([1, 3])

            # Conversation selector
            with left:
                st.markdown("**Conversations**")
                selected = st.radio(
                    "Conversations",

                    convos,
                    key=f"{key_prefix}selected_convo",
                    label_visibility="collapsed",
                )

            # Thread & send box
            with right:
                msgs = st.session_state["_conversations"].setdefault(selected, [])
                _render_messages(msgs)

                col_msg, col_send, col_refresh = st.columns([4, 1, 1])
                with col_msg:
                    msg_input = st.text_input(
                        "Message",
                        key=f"{key_prefix}msg_input",
                    )
                with col_send:
                    if st.button("Send", key=f"{key_prefix}send_msg") and msg_input:
                        send_message(selected, msg_input)
                        st.session_state.msg_input = ""
                        st.experimental_rerun()
                with col_refresh:
                    st.button(
                        "🔄",
                        key=f"{key_prefix}refresh_chat",
                        on_click=st.experimental_rerun,
                    )

        # ── Calls tab ──────────────────────────────────────────────
        with tab_calls:
            from .chat import render_video_call_controls, render_voice_chat_controls

            render_video_call_controls(key_prefix=f"{page}_")
            st.divider()
            render_voice_chat_controls(key_prefix=f"{page}_")


# Streamlit multipage support --------------------------------------------------
def render() -> None:
    main()


if __name__ == "__main__":
    main()
