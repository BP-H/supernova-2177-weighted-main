# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Proxy loader for the Agents page."""

from __future__ import annotations

import importlib
import streamlit as st


def _load_real_page() -> bool:
    """Import and invoke the real page if it exists. Return True on success."""
    try:
        mod = importlib.import_module(
            "transcendental_resonance_frontend.pages.agents"
        )
    except ModuleNotFoundError:
        return False

    for fn in ("main", "render"):
        if hasattr(mod, fn):
            getattr(mod, fn)()
            return True
    return False


def _placeholder() -> None:
    st.header("Agents 👥")
    st.info("The full Agents module isn’t installed yet.")


def main() -> None:  # Streamlit runs this when the file is opened
    if not _load_real_page():
        _placeholder()


def render() -> None:  # keep legacy compatibility
    main()


if __name__ == "__main__":  # manual execution
    main()
