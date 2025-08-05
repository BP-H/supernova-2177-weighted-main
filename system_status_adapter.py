# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Adapter for retrieving system status metrics from the backend."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "0") == "1"


def get_status() -> Optional[Dict[str, Any]]:
    """Fetch system status data from the backend API.

    Returns ``None`` if offline mode is enabled or the request fails.
    """
    if OFFLINE_MODE:
        return None
    try:
        resp = requests.get(f"{BACKEND_URL}/status", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None
