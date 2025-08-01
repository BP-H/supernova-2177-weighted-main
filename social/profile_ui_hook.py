# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from sqlalchemy.orm import Session
from frontend_bridge import register_route_once

try:  # pragma: no cover - optional when running tests
    from superNova_2177 import (
        get_user_by_username,
        get_user_followers,
        get_user_following,
    )
except Exception:  # pragma: no cover - optional dependency
    get_user_by_username = None  # type: ignore
    get_user_followers = None  # type: ignore
    get_user_following = None  # type: ignore

if TYPE_CHECKING:  # pragma: no cover
    from db_models import Harmonizer


async def get_user_ui(payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Return basic user info for ``payload['username']``."""
    if get_user_by_username is None:
        raise RuntimeError("get_user_by_username unavailable")
    user = get_user_by_username(payload["username"], db=db)
    return {
        "id": user.id,
        "username": user.username,
        "bio": getattr(user, "bio", ""),
    }


async def get_followers_ui(payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Return follower list for ``payload['username']``."""
    if get_user_followers is None:
        raise RuntimeError("get_user_followers unavailable")
    return get_user_followers(payload["username"], db=db)


async def get_following_ui(payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Return following list for ``payload['username']``."""
    if get_user_following is None:
        raise RuntimeError("get_user_following unavailable")
    return get_user_following(payload["username"], db=db)


register_route_once(
    "get_user",
    get_user_ui,
    "Fetch user profile information",
    "social",
)
register_route_once(
    "get_followers",
    get_followers_ui,
    "Retrieve a user's followers",
    "social",
)
register_route_once(
    "get_following",
    get_following_ui,
    "Retrieve who a user follows",
    "social",
)
