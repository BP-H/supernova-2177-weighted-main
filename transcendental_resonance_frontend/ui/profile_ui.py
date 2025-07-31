"""Backwards compatibility wrapper for profile card UI."""
from __future__ import annotations

from .profile_card import (
    DEFAULT_USER,
    inject_profile_styles,
    render_profile_card,
)

# Alias for old function name
render_profile = render_profile_card

__all__ = [
    "render_profile_card",
    "render_profile",
    "inject_profile_styles",
    "DEFAULT_USER",
]
