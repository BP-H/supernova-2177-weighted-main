"""Common chat UI helpers."""

import streamlit as st
from modern_ui import inject_modern_styles

inject_modern_styles()


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
    """Simple real-time chat using session state."""
    st.session_state.setdefault("chat_messages", [])
    language = st.session_state.get("chat_lang", "en")
    language = st.selectbox("Language", ["en", "es", "ko"], key="chat_lang")

    chat_container = st.container()
    for entry in st.session_state.chat_messages:
        chat_container.markdown(
            f"**{entry['user']}**: {translate_text(entry['text'], language)}"
        )

    cols = st.columns([4, 1])
    with cols[0]:
        msg = st.text_input("Message", key="chat_input")
    with cols[1]:
        if st.button("Send", key="send_chat") and msg:
            st.session_state.chat_messages.append({"user": "You", "text": msg})
            st.session_state.chat_input = ""
            st.experimental_rerun()


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
