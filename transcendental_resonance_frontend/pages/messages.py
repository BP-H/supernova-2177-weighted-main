# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Messages page – delegates to the reusable chat UI."""

from __future__ import annotations

from frontend.theme import set_theme, inject_global_styles, apply_theme
from modern_ui import apply_modern_styles
from streamlit_helpers import theme_toggle
from transcendental_resonance_frontend.ui.chat_ui import render_chat_ui

set_theme("light")
apply_modern_styles()


def main(main_container=None) -> None:
    """Render the chat interface inside the given container (or the page itself)."""
    apply_theme("light")
    inject_global_styles()

    theme_toggle("Dark Mode", key_suffix="messages")
    render_chat_ui(main_container)


def render() -> None:  # for multipage apps that expect a `render` symbol
    main()


if __name__ == "__main__":
    main()
