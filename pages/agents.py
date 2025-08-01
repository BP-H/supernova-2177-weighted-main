# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Proxy loader for the Agents page."""

from __future__ import annotations

from transcendental_resonance_frontend.pages import agents as real_page


def main() -> None:  # Streamlit runs this when the file is opened
    real_page.main()


def render() -> None:  # keep legacy compatibility
    real_page.main()


if __name__ == "__main__":  # manual execution
    main()
