# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Reusable chat interface components."""

from __future__ import annotations

import streamlit as st


CHAT_CSS = """
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.chat-bubble {
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    max-width: 80%;
    word-wrap: break-word;
}
.chat-bubble.left {
    align-self: flex-start;
    background: #eee;
}
.chat-bubble.right {
    align-self: flex-end;
    background: #DCF8C6;
}
</style>
"""


def render_chat() -> None:
    """Display a simple chat with messages and call controls."""
    st.session_state.setdefault("chat_history", [])

    st.markdown(CHAT_CSS, unsafe_allow_html=True)

    messages_tab, calls_tab = st.tabs(["Messages", "Calls"])

    with messages_tab:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for entry in st.session_state["chat_history"]:
            sender = entry.get("sender", "")
            text = entry.get("text", "")
            cls = "right" if sender == "You" else "left"
            st.markdown(
                f"<div class='chat-bubble {cls}'><strong>{sender}:</strong> {text}</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns([4, 1])
        with col1:
            msg = st.text_input("Message", key="chat_msg")
        with col2:
            if st.button("Send", key="chat_send") and msg:
                st.session_state["chat_history"].append({"sender": "You", "text": msg})
                st.session_state.chat_msg = ""
                st.experimental_rerun()

    with calls_tab:
        if st.button("Start Video Call", key="chat_video"):
            st.toast("Video call integration pending")
