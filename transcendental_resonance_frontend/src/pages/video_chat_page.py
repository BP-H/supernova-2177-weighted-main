# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Experimental video chat page."""

from __future__ import annotations

import json

from nicegui import ui

from utils import ErrorOverlay
from utils.api import TOKEN, WS_CONNECTION, listen_ws
from utils.layout import navigation_bar, page_container
from utils.styles import get_theme

from .login_page import login_page


@ui.page("/video-chat")
async def video_chat_page() -> None:
    """Simple camera demo with WebSocket signaling."""
    if not TOKEN:
        ui.open(login_page)
        return

    THEME = get_theme()
    with page_container(THEME):
        if TOKEN:
            navigation_bar()
        ui.label("Video Chat").classes("text-2xl font-bold mb-4").style(
            f'color: {THEME["accent"]};'
        )

        error_overlay = ErrorOverlay()

        local_cam = ui.camera().classes("w-full mb-4")
        remote_view = ui.video().props("autoplay playsinline").classes("w-full mb-4")
        caption = ui.label().classes("text-sm mb-2")
        translate_input = ui.input("Text to translate").classes("w-full mb-2")
        translate_lang = ui.input("Target language code", value="en").classes("w-full mb-4")

        async def handle_event(event: dict) -> None:
            if event.get("type") == "frame":
                remote_view.source = event.get("data")
            if event.get("type") == "translation":
                caption.text = event.get("translation")
            if event.get("type") == "screen_share":
                remote_view.source = event.get("data")

        join_button = ui.button("Join Call")
        share_button = ui.button("Share Screen")

        async def join_call() -> None:
            try:
                ws_task = listen_ws(handle_event)
                await ws_task
            except Exception:  # pragma: no cover - network issues
                ui.notify("Realtime updates unavailable", color="warning")
                join_button.disable()
                local_cam.disable()
                error_overlay.show("Realtime updates unavailable")

        join_button.on_click(lambda: ui.run_async(join_call()))
        share_button.on_click(lambda: WS_CONNECTION and WS_CONNECTION.send_text(json.dumps({"type": "screen_share"})))


        async def send_frame() -> None:
            if WS_CONNECTION and local_cam.value:
                await WS_CONNECTION.send_text(
                    json.dumps({"type": "frame", "data": local_cam.value})
                )

        async def send_translation() -> None:
            if WS_CONNECTION and translate_input.value:
                await WS_CONNECTION.send_text(
                    json.dumps(
                        {
                            "type": "translate",
                            "user": "local-user",
                            "lang": translate_lang.value or "en",
                            "text": translate_input.value,
                        }
                    )
                )
                translate_input.value = ""

        local_cam.on("capture", lambda _: ui.run_async(send_frame()))
        translate_input.on("submit", lambda _: ui.run_async(send_translation()))
        ui.label("Note: Video chat is unavailable when offline.").classes(
            "text-xs opacity-75 mt-2"
        )

