"""Streamlit entry point for the Validation page."""

import streamlit as st
from transcendental_resonance_frontend.pages.validation import (
    main as _frontend_main,
)


def render() -> None:
    """Render the validation dashboard."""
    _frontend_main()


if __name__ == "__main__":  # pragma: no cover - manual execution
    render()
