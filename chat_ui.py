# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Reusable chat interface components with translation and call support."""

from __future__ import annotations
import asyncio
import threading
from typing import Optional
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx
from modern_ui import inject_modern_styles
from realtime_comm import ChatWebSocketManager

try:
    import websockets
except Exception:  # pragma: no cover - optional dependency
    websockets = None

inject_modern_styles()


def _run_async(coro):
    """Execute ``coro`` regardless of event loop state."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        return loop.run_until_complete(coro)


EMOJI_OPTIONS = ["😀", "😂", "😍", "👍", "🎉"]

CHAT_CSS = """
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
}
.chat-message {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
}
.chat-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}
.chat-bubble {
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    max-width: 80%;
    word-wrap: break-word;
}
.chat-bubble.left {
    align-self: flex-start;
    background: var(--card);
    color: var(--text-muted);
}
.chat-bubble.right {
    align-self: flex-end;
    background: var(--accent);
    color: #fff;
}
.chat-input-row .stTextInput input {
    border-radius: 1.5rem;
    padding: 0.5rem 1rem;
}
.chat-input-row .stButton>button {
    background: var(--accent);
    color: #fff;
    border-radius: 1.5rem;
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


def _start_ws_listener(url: str = "ws://localhost:8765") -> None:
    """Connect to the broadcast WebSocket server in a background thread."""
    if websockets is None or st.session_state.get("_ws_thread"):
        return

    async def _listen() -> None:
        try:
            async with websockets.connect(url) as ws:
                st.session_state["_ws"] = ws
                async for message in ws:
                    st.session_state["chat_history"].append({
                        "sender": "Peer",
                        "text": message,
                    })
                    st.rerun()
        except Exception:
            st.session_state["_ws"] = None

    loop = asyncio.new_event_loop()

    def _run() -> None:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_listen())

    thread = threading.Thread(target=_run, daemon=True)
    add_script_run_ctx(thread)
    thread.start()
    st.session_state["_ws_thread"] = thread
    st.session_state["_ws_loop"] = loop


def _send_ws(message: str) -> bool:
    """Send ``message`` through the WebSocket if connected."""
    ws = st.session_state.get("_ws")
    loop: Optional[asyncio.AbstractEventLoop] = st.session_state.get("_ws_loop")
    if ws and loop:
        loop.call_soon_threadsafe(asyncio.create_task, ws.send(message))
        return True
    return False


def render_chat_interface() -> None:
    """Display a styled, translatable chat with call controls."""
    st.session_state.setdefault("chat_history", [])
    if "chat_ws" not in st.session_state:
        manager = ChatWebSocketManager()

        async def handle_msg(payload: dict) -> None:
            st.session_state.chat_history.append(
                {
                    "sender": payload.get("sender", "Anon"),
                    "text": payload.get("text", ""),
                    "avatar": payload.get("avatar", "https://via.placeholder.com/32"),
                }
            )
            st.rerun()

        manager.add_listener(handle_msg)
        manager.start()
        st.session_state["chat_ws"] = manager
    else:
        manager = st.session_state["chat_ws"]

    st.markdown(CHAT_CSS, unsafe_allow_html=True)

    page_prefix = f"{st.session_state.get('active_page', 'global')}_"
    language = st.session_state.get("chat_lang", "en")
    language = st.selectbox(
        "Language",
        ["en", "es", "ko"],
        key=f"{page_prefix}chat_lang",
    )

    messages_tab, calls_tab = st.tabs(["Messages", "Calls"])

    with messages_tab:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for entry in st.session_state["chat_history"]:
            sender = entry.get("sender", "")
            text = entry.get("text", "")
            avatar = entry.get("avatar", "https://via.placeholder.com/32")
            cls = "right" if sender == "You" else "left"
            translated = translate_text(text, language)
            cols = st.columns([1, 9]) if cls == "left" else st.columns([9, 1])
            avatar_col, msg_col = cols if cls == "left" else reversed(cols)
            with avatar_col:
                st.image(avatar, width=32)
            with msg_col:
                st.markdown(
                    f"<div class='chat-message'><div class='chat-bubble {cls}'><strong>{sender}:</strong> {translated}</div></div>",
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='chat-input-row'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            msg = st.text_input(
                "Message",
                key=f"{page_prefix}chat_input",
                label_visibility="collapsed",
                placeholder="Type a message...",
            )
        with col2:
            emoji = st.selectbox(
                "",
                EMOJI_OPTIONS,
                label_visibility="collapsed",
                key=f"{page_prefix}emoji_picker",
            )
            if st.button("+", key=f"{page_prefix}add_emoji"):
                st.session_state[f"{page_prefix}chat_input"] = (msg or "") + emoji
                st.rerun()
        with col3:
            if st.button("Send", key=f"{page_prefix}send_chat") and msg:
                payload = {"sender": "You", "text": msg}
                st.session_state["chat_history"].append({"sender": "You", "text": msg, "avatar": "https://via.placeholder.com/32"})
                _run_async(manager.send(payload))
                st.session_state[f"{page_prefix}chat_input"] = ""
        st.markdown("</div>", unsafe_allow_html=True)

    with calls_tab:
        render_video_call_controls(key_prefix=page_prefix)
        st.divider()
        render_voice_chat_controls(key_prefix=page_prefix)


def render_video_call_controls(key_prefix: str | None = None) -> None:
    """Placeholder video call controls."""
    if key_prefix is None:
        page = st.session_state.get("active_page", "")
        key_prefix = f"{page}_" if page else ""
    if st.button("Start Video Call", key=f"{key_prefix}start_video"):
        st.toast("Video call placeholder. Integration with WebRTC pending.")
        st.empty()


def render_voice_chat_controls(key_prefix: str | None = None) -> None:
    """Placeholder voice call controls."""
    if key_prefix is None:
        page = st.session_state.get("active_page", "")
        key_prefix = f"{page}_" if page else ""
    if st.button("Start Voice Call", key=f"{key_prefix}start_voice"):
        st.toast("Voice call placeholder. Audio streaming integration pending.")
        st.empty()

__all__ = [
    "translate_text",
    "render_chat_interface",
    "render_video_call_controls",
    "render_voice_chat_controls",
]
