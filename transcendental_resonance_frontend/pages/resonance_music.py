# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Resonance music player and summary viewer."""

from __future__ import annotations

import asyncio
import base64
import os
from typing import Any

from streamlit_autorefresh import st_autorefresh

import requests
import streamlit as st
from streamlit_helpers import alert, centered_container
from streamlit_autorefresh import st_autorefresh
from status_indicator import render_status_icon

try:
    from frontend_bridge import dispatch_route
except Exception:  # pragma: no cover - optional dependency
    dispatch_route = None  # type: ignore

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def _check_backend() -> bool:
    """Return ``True`` if the backend is reachable."""
    try:
        resp = requests.get(f"{BACKEND_URL}/healthz", timeout=3)
        resp.raise_for_status() # This is generally more robust than checking for status_code == 200
    except Exception:
        return False
    return True


def _run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        return loop.run_until_complete(coro)


def main(main_container=None) -> None:
    """Render music generation and summary widgets."""
    st_autorefresh(interval=30000, key="status_ping")

    if main_container is None:
        main_container = st

    # Auto-refresh for backend health check
    st_autorefresh(interval=5000, key="health-ping")

    with st.sidebar:
        # Render the global backend status indicator using the modular component
        render_status_icon(endpoint="/healthz") # Assuming /healthz is the correct health check endpoint for your backend

    # The general page-level backend check and alert should come after the sidebar rendering,
    # as they are not part of the sidebar's content but rather overall page status.
    # This part is not in the provided diff, but is crucial for the overall logic.
    # Example (from previous full resolve):
    # backend_ok = check_backend(endpoint="/healthz")
    # if not backend_ok:
    #     alert(
    #         f"Backend service unreachable. Please ensure it is running at {BACKEND_URL}.",
    #         "error",
    #     )

    profile = st.selectbox(
        "Select resonance profile",
        ["default", "high_harmony", "high_entropy"],
    )

    # Display alert if backend is not reachable
    if not backend_ok:
        alert(
            f"Backend service unreachable. Please ensure it is running at {BACKEND_URL}.",
            "error",
        )

    with main_container:
        st.subheader("Resonance Music")
        centered_container()

        profile = st.selectbox(
            "Select resonance profile",
            ["default", "high_harmony", "high_entropy"],
        )
        midi_placeholder = st.empty()

        if st.button("Generate music") and dispatch_route:
            with st.spinner("Generating..."):
                try:
                    result = _run_async(
                        dispatch_route("generate_midi", {"profile": profile})
                    )
                except Exception:  # Catch all exceptions for feedback
                    alert(
                        f"Generation failed: Backend service unreachable. Please ensure it is running at {BACKEND_URL}.",
                        "error",
                    )
                else:
                    midi_b64 = (
                        result.get("midi_base64") if isinstance(result, dict) else None
                    )
                    if midi_b64:
                        midi_bytes = base64.b64decode(midi_b64)
                        midi_placeholder.audio(midi_bytes, format="audio/midi")
                        st.toast("Music generated!") # Success toast
                    else:
                        alert("No MIDI data returned", "warning")

        if st.button("Fetch resonance summary"):
            try:
                resp = requests.get(f"{BACKEND_URL}/resonance-summary", timeout=5)
                resp.raise_for_status()
                data = resp.json()
                st.json(data.get("metrics", {}))
                st.write(f"MIDI bytes: {data.get('midi_bytes', 0)}")
                st.toast("Summary loaded!") # Success toast
            except Exception:  # Catch all exceptions for feedback
                alert(
                    f"Failed to load summary: Backend service unreachable. Please ensure it is running at {BACKEND_URL}.",
                    "error",
                )
                if midi_b64:
                    midi_bytes = base64.b64decode(midi_b64)
                    midi_placeholder.audio(midi_bytes, format="audio/midi")
                else:
                    alert("No MIDI data returned", "warning")

    if st.button("Fetch resonance summary"):
        try:
            resp = requests.get(f"{BACKEND_URL}/resonance-summary", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            st.json(data.get("metrics", {}))
            st.write(f"MIDI bytes: {data.get('midi_bytes', 0)}")
        except Exception as exc:  # pragma: no cover - best effort
            alert(f"Failed to load summary: {exc}", "error")