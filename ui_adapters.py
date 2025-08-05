import os
import logging
from typing import List

DUMMY_USERS: List[str] = ["taha_gungor", "artist_dev"]
ERROR_MESSAGE = "Unable to fetch users"

logger = logging.getLogger(__name__)

def use_real_backend() -> bool:
    """Return True if the real backend should be used."""
    return os.getenv("USE_REAL_BACKEND", "").lower() in {"1", "true", "yes"}


def search_users_adapter(query: str) -> List[str]:
    """Search for users by ``query`` using real backend when available.

    Falls back to a static dummy list when ``use_real_backend`` is ``False``.
    On failure, logs the error and returns a friendly message.
    """
    if not use_real_backend():
        return DUMMY_USERS
    try:
        import superNova_2177 as sn  # Local import to avoid heavy cost when unused
        with sn.SessionLocal() as db:
            results = sn.search_users(query, db)
        return [r.get("username", "") for r in results]
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("search_users_adapter failed: %s", exc)
        return [ERROR_MESSAGE]
