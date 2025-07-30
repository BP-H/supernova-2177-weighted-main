# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Utility helpers for managing Streamlit page modules."""

from __future__ import annotations

from pathlib import Path
import logging
import streamlit as st

logger = logging.getLogger(__name__)


def ensure_pages(pages: dict[str, str], pages_dir: Path) -> None:
    """Ensure placeholder page modules exist for each slug.

    Parameters
    ----------
    pages:
        Mapping of display labels to page slugs.
    pages_dir:
        Directory where page modules are stored.
    """
    pages_dir.mkdir(parents=True, exist_ok=True)

    for slug in pages.values():
        file_path = pages_dir / f"{slug}.py"
        if not file_path.exists():
            file_path.write_text(
                "import streamlit as st\n\n"
                "def main():\n"
                "    st.write('Placeholder')\n"
            )
            logger.debug("Created placeholder page module: %s", file_path)

__all__ = ["ensure_pages"]
