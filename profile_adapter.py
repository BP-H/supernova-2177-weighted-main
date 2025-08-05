"""Profile update adapter handling backend/stub flows."""

from __future__ import annotations

import os
from typing import Dict, List

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def update_profile_adapter(bio: str, cultural_preferences: List[str]) -> Dict[str, str]:
    """Update the user's profile.

    Checks the ``use_backend`` toggle in ``st.session_state``. When disabled,
    returns a stubbed response. When enabled, it attempts to call the backend's
    ``update_profile`` endpoint and captures errors.
    """

    if not bio.strip():
        return {"status": "error", "error": "Bio is required"}

    if not st.session_state.get("use_backend", False):
        return {
            "status": "stubbed",
            "bio": bio,
            "cultural_preferences": cultural_preferences,
        }

    payload = {"bio": bio, "cultural_preferences": cultural_preferences}
    try:
        resp = requests.put(f"{BACKEND_URL}/users/me", json=payload, timeout=5)
        resp.raise_for_status()
    except Exception as exc:
        return {"status": "error", "error": str(exc)}
    return {"status": "ok"}
