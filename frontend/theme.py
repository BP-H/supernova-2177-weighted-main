# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Color theme utilities for Streamlit frontend."""

from __future__ import annotations


def get_global_css(dark: bool) -> str:
    """Return ``:root`` CSS variables for dark or light mode."""
    if dark:
        return (
            "<style>"
            ":root {"
            "--bg:#001E26;"
            "--card:#002B36;"
            "--accent:#00F0FF;"
            "--text-muted:#7e9aaa;"
            "}</style>"
        )
    return (
        "<style>"
        ":root {"
        "--bg:#F0F2F6;"
        "--card:#FFFFFF;"
        "--accent:#0A84FF;"
        "--text-muted:#666666;"
        "}</style>"
    )

