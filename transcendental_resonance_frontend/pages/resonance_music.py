# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Resonance music player and summary viewer."""

from __future__ import annotations

import asyncio
import base64
import os
from typing import Any, Optional, Dict

import requests
import streamlit as st
from streamlit_helpers import alert, centered_container
from streamlit_autorefresh import st_autorefresh
from status_indicator import render_status_icon, check_backend # Ensure check_backend is imported
from utils.api import get_resonance_summary, dispatch_route # Import get_resonance_summary and dispatch_route from utils.api

# BACKEND_URL is defined in utils.api, but we keep it here for direct requests calls if needed
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


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


def main(main_container=None, status_container=None) -> None:
    """Render music generation and summary widgets."""

    if main_container is None:
        main_container = st
    if status_container is None:
        status_container = st

    # Auto-refresh for backend health check (global, outside main_container)
    st_autorefresh(interval=30000, key="status_ping")

    # Render global backend status indicator in the provided container
    with status_container:
        render_status_icon(endpoint="/healthz")

    # Display alert if backend is not reachable (check once per rerun)
    backend_ok = check_backend(endpoint="/healthz") # Use the modular check_backend
    if not backend_ok:
        alert(
            f"Backend service unreachable. Please ensure it is running at {BACKEND_URL}.",
            "error",
        )

    with main_container:
        st.subheader("Resonance Music")
        centered_container()

        profile_options = ["default", "high_harmony", "high_entropy"]
        # Also include the "Solar Echoes", "Quantum Drift", "Ether Pulse" from the other branch
        track_options = ["Solar Echoes", "Quantum Drift", "Ether Pulse"]
        combined_options = list(set(profile_options + track_options)) # Remove duplicates

        choice = st.selectbox(
            "Select a track or resonance profile",
            combined_options,
            index=0, # Default to first option
            placeholder="tracks or resonance profiles",
            key="resonance_profile_select"
        )
        
        midi_placeholder = st.empty() # Placeholder for MIDI audio player

        # --- Generate Music Section ---
        if st.button("Generate music", key="generate_music_btn"):
            if not backend_ok: # Check backend status before attempting generation
                alert(f"Cannot generate music: Backend service unreachable at {BACKEND_URL}.", "error")
                return

            with st.spinner("Generating..."):
                try:
                    # Use dispatch_route for consistency with other backend calls
                    result = _run_async(
                        dispatch_route("generate_midi", {"profile": choice}) # Use 'choice' for profile/track
                    )
                    midi_b64 = result.get("midi_base64") if isinstance(result, dict) else None
                    
                    if midi_b64:
                        midi_bytes = base64.b64decode(midi_b64)
                        midi_placeholder.audio(midi_bytes, format="audio/midi")
                        st.toast("Music generated!")
                    else:
                        alert("No MIDI data returned from generation.", "warning")
                except Exception as exc:
                    alert(f"Music generation failed: {exc}. Ensure backend is running and 'generate_midi' route is available.", "error")

        # --- Fetch Resonance Summary Section ---
        if st.button("Fetch resonance summary", key="fetch_summary_btn"):
            if not backend_ok: # Check backend status before attempting fetch
                alert(f"Cannot fetch summary: Backend service unreachable at {BACKEND_URL}.", "error")
                return

            with st.spinner("Fetching summary..."):
                try:
                    # Use the modular get_resonance_summary from utils.api
                    data = _run_async(get_resonance_summary(choice)) # Use 'choice' for summary
                    
                    if data:
                        metrics = data.get("metrics", {})
                        midi_bytes_count = data.get("midi_bytes", 0) # Assuming this is a count, not actual bytes here
                        
                        st.subheader("Metrics")
                        # Display metrics in a table for better readability
                        if metrics:
                            st.table({"metric": list(metrics.keys()), "value": list(metrics.values())})
                        else:
                            st.info("No metrics available for this profile.")
                        
                        st.write(f"Associated MIDI bytes (count/size): {midi_bytes_count}")

                        # If the summary also returns MIDI bytes (e.g., for preview), play it
                        summary_midi_b64 = data.get("midi_base64")
                        if summary_midi_b64:
                            summary_midi_bytes = base64.b64decode(summary_midi_b64)
                            st.audio(summary_midi_bytes, format="audio/midi", key="summary_audio_player")
                            st.info("Playing associated MIDI from summary.")

                        st.toast("Summary loaded!")
                    else:
                        alert("No summary data returned for this profile.", "warning")

                except Exception as exc:
                    alert(f"Failed to load summary: {exc}. Ensure backend is running and 'resonance-summary' route is available.", "error")
