# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Unified messages and chat center."""

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container

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


def _render_conversation_list() -> None:
    users = [c["user"] for c in st.session_state["conversations"]]
    active = st.session_state.get("active_chat")
    if active not in users and users:
        active = users[0]
    col1, col2 = st.columns([1, 3])
    with col1:
        selected = st.radio("", users, index=users.index(active)) if users else ""
        st.session_state["active_chat"] = selected
    with col2:
        st.write("Recent")
        if users:
            st.write(st.session_state["conversations"][users.index(selected)]["preview"])


def _render_chat_panel(user: str) -> None:
    st.subheader(f"Chat with {user}")
    msgs = st.session_state["messages"].setdefault(user, [])
    for msg in msgs:
        st.write(f"{msg['sender']}: {msg['text']}")
    txt = st.text_input("Message", key="msg_input")
    if st.button("Send", key="send_btn") and txt:
        msgs.append({"sender": "You", "text": txt})
        st.session_state.msg_input = ""
        st.experimental_rerun()
    if st.button("Start Video Call", key="video_call"):
        st.toast("Video call integration pending")


def main(main_container=None) -> None:
    if main_container is None:
        main_container = st
    _init_state()
    container_ctx = safe_container(main_container)
    with container_ctx:
        st.subheader("✉️ Messages")
        if not st.session_state["conversations"]:
            st.info("No conversations yet")
            return
        user = st.session_state.get("active_chat")
        _render_conversation_list()
        st.divider()
        if user:
            _render_chat_panel(user)


def render() -> None:
    main()


if __name__ == "__main__":
    main()
