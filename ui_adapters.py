# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Adapters bridging UI events to backend services.

Currently provides :func:`follow_adapter` which mirrors the toggle style of
search related adapters.  The function attempts to use the real backend via the
``utils.api`` module but falls back to a lightweight in-memory stub when the
backend is unavailable.  All outcomes are logged and a concise status message is
returned for display in the UI.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Tuple, Dict, Any

try:  # pragma: no cover - optional backend
    from utils.api import toggle_follow  # type: ignore
except Exception:  # pragma: no cover - backend not available
    toggle_follow = None  # type: ignore

logger = logging.getLogger(__name__)

# Simple in-memory follow set used when ``toggle_follow`` is unavailable.
_STUB_FOLLOWING: set[str] = set()


def _run_async(coro):
    """Execute ``coro`` whether or not an event loop is running."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        return loop.run_until_complete(coro)


def follow_adapter(target_username: str) -> Tuple[bool, str]:
    """Toggle following ``target_username``.

    Returns a ``(success, message)`` tuple. Success is ``True`` when the follow
    state was toggled either via the backend or the local stub. When the backend
    is unavailable a lightweight in-memory toggle is used instead.
    """

    if not target_username:
        logger.warning("follow_adapter called without a username")
        return False, "No username provided"

    if toggle_follow is None:
        # Fallback stub path
        if target_username in _STUB_FOLLOWING:
            _STUB_FOLLOWING.remove(target_username)
            message = "Unfollowed"
        else:
            _STUB_FOLLOWING.add(target_username)
            message = "Followed"
        logger.info("Stub follow toggle for %s: %s", target_username, message)
        return True, message

    try:
        resp: Dict[str, Any] | None = _run_async(toggle_follow(target_username))
        message = (resp or {}).get("message", "Updated")
        logger.info("Follow toggle for %s succeeded: %s", target_username, message)
        return True, message
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.exception("Follow toggle failed for %s", target_username)
        return False, f"Follow failed: {exc}"


__all__ = ["follow_adapter"]

