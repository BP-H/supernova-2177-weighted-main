# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Unified messages and chat center."""

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container, header, theme_selector
from transcendental_resonance_frontend.chat_ui import render_message_bubbles


inject_modern_styles()

DUMMY_CONVOS = [
    {"user": "Alice", "preview": "Hey there!"},
    {"user": "Bob", "preview": "Let's catch up."},
]


def _init_state() -> None:
    st.session_state.setdefault("conversations", DUMMY_CONVOS)
    st.session_state.setdefault(
        "messages", {c["user"]: [] for c in st.session_state["conversations"]}
    )
    if "active_chat" not in st.session_state:
        st.session_state["active_chat"] = DUMMY_CONVOS[0]["user"] if DUMMY_CONVOS else ""


def _render_tabs() -> tuple[st.container, st.container]:
    """Return message and call tab contexts."""
    tabs = st.tabs(["Messages", "Calls"])
    return tabs[0], tabs[1]


def _render_chat_panel(user: str) -> None:
    header(f"Chat with {user}")
    # Use shared session reference for history syncing
    st.session_state["chat_history"] = st.session_state["messages"].setdefault(user, [])
    
    # Render bubble-style UI
    render_message_bubbles(st.session_state["chat_history"])

    # Input & Send handling
    txt = st.text_input("Message", key="msg_input")
    if st.button("Send", key="send_btn") and txt:
        st.session_state["chat_history"].append({"sender": "You", "text": txt})
        st.session_state["messages"][user] = st.session_state["chat_history"]
        st.session_state.msg_input = ""
        st.experimental_rerun()

    if st.button("Video Call", key="video_call"):
        st.toast("Video call integration pending")



def main(main_container=None) -> None:
    if main_container is None:
        main_container = st
    theme_selector("Theme", key_suffix="messages")
    _init_state()
    container_ctx = safe_container(main_container)
    with container_ctx:
        header("✉️ Messages")
        if not st.session_state["conversations"]:
            st.info("No conversations yet")
            return
        user = st.session_state.get("active_chat")
        messages_tab, calls_tab = _render_tabs()
        with messages_tab:
            if user:
                _render_chat_panel(user)
        with calls_tab:
            st.info("Call history coming soon")


def render() -> None:
    main()


if __name__ == "__main__":
    main()
