# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Common path constants for the Streamlit frontend."""

from __future__ import annotations

from pathlib import Path

# Repository root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Default directory where Streamlit pages are located
PAGES_DIR = ROOT_DIR / "transcendental_resonance_frontend" / "pages"


def get_pages_dir() -> Path:
    """Return the canonical directory for Streamlit page modules."""
    return PAGES_DIR


__all__ = ["ROOT_DIR", "PAGES_DIR", "get_pages_dir"]
