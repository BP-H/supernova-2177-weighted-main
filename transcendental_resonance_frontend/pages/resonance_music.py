"""Preview resonance metrics as music."""

from __future__ import annotations

import asyncio
import streamlit as st
from utils.api import get_resonance_summary


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
    st.header("Resonance Music")
    options = ["Solar Echoes", "Quantum Drift", "Ether Pulse"]
    choice = st.selectbox(
        "Select a track or resonance profile",
        options,
        index=None,
        placeholder="tracks or resonance profiles",
    )
    if not choice:
        return

    data = _run_async(get_resonance_summary(choice)) or {}
    metrics = data.get("metrics", {})
    if metrics:
        st.subheader("Metrics")
        st.table({"metric": list(metrics.keys()), "value": list(metrics.values())})

    midi = data.get("midi_bytes")
    if isinstance(midi, (bytes, bytearray)):
        st.audio(midi, format="audio/midi")
