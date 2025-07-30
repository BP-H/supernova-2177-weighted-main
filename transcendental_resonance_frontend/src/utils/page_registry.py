# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Utility helpers for managing Streamlit page modules."""

from __future__ import annotations

from pathlib import Path
import logging
import streamlit as st

# Track which slugs have already triggered a missing-page warning.
_warned_slugs: set[str] = set()

logger = logging.getLogger(__name__)
logger.propagate = False



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
            logger.info("Created placeholder page module %s", file_path.name)

            # Warn in Streamlit contexts that the slug was missing, but only once per slug.
            if hasattr(st, "warning") and slug not in _warned_slugs:
                st.warning(f"Placeholder page created for missing slug '{slug}'.")
                _warned_slugs.add(slug)

__all__ = ["ensure_pages"]
