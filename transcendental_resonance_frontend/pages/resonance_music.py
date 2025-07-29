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

try:
    from frontend_bridge import dispatch_route
except Exception:  # pragma: no cover - optional dependency
    dispatch_route = None  # type: ignore

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def backend_online() -> bool:
    """Return True if the backend health check succeeds."""
    try:
        resp = requests.get(f"{BACKEND_URL}/healthz", timeout=2)
        return resp.status_code == 200
    except Exception:
        return False


def _run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        return loop.run_until_complete(coro)


def main() -> None:
    """Render music generation and summary widgets."""

    st_autorefresh(interval=5000, key="health-ping")
    indicator_color = "green" if backend_online() else "red"
    st.markdown(
        f"Backend: <span style='color:{indicator_color};font-size:1.2rem;'>\u25CF</span>",
        unsafe_allow_html=True,
    )

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
            except Exception as exc:  # pragma: no cover - feedback
                alert(f"Generation failed: {exc}", "error")
            else:
                midi_b64 = (
                    result.get("midi_base64") if isinstance(result, dict) else None
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
        except Exception:  # pragma: no cover - best effort
            alert(
                "Backend service unreachable. Please ensure the backend server is running at http://localhost:8000.",
                "error",
            )
