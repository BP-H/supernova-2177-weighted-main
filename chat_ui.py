"""Reusable chat interface components with translation and call support."""

from __future__ import annotations
import streamlit as st
from modern_ui import inject_modern_styles

inject_modern_styles()

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


def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate ``text`` to ``target_lang`` if possible."""
    if not text:
        return ""
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception:
        return text


def render_chat_interface() -> None:
    """Display a styled, translatable chat with call controls."""
    st.session_state.setdefault("chat_history", [])
    st.markdown(CHAT_CSS, unsafe_allow_html=True)

    language = st.session_state.get("chat_lang", "en")
    language = st.selectbox("Language", ["en", "es", "ko"], key="chat_lang")

    messages_tab, calls_tab = st.tabs(["Messages", "Calls"])

    with messages_tab:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for entry in st.session_state["chat_history"]:
            sender = entry.get("sender", "")
            text = entry.get("text", "")
            cls = "right" if sender == "You" else "left"
            translated = translate_text(text, language)
            st.markdown(
                f"<div class='chat-bubble {cls}'><strong>{sender}:</strong> {translated}</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns([4, 1])
        with col1:
            msg = st.text_input("Message", key="chat_input")
        with col2:
            if st.button("Send", key="send_chat") and msg:
                st.session_state["chat_history"].append({"sender": "You", "text": msg})
                st.session_state.chat_input = ""
                st.experimental_rerun()

    with calls_tab:
        render_video_call_controls()
        st.divider()
        render_voice_chat_controls()


def render_video_call_controls() -> None:
    """Placeholder video call controls."""
    if st.button("Start Video Call", key="start_video"):
        st.toast("Video call placeholder. Integration with WebRTC pending.")
        st.empty()


def render_voice_chat_controls() -> None:
    """Placeholder voice call controls."""
    if st.button("Start Voice Call", key="start_voice"):
        st.toast("Voice call placeholder. Audio streaming integration pending.")
        st.empty()


__all__ = [
    "translate_text",
    "render_chat_interface",
    "render_video_call_controls",
    "render_voice_chat_controls",
]

