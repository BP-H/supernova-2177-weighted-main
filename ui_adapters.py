import os
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

DUMMY_USERS: List[str] = ["taha_gungor", "artist_dev"]
ERROR_MESSAGE = "Unable to fetch users"


def use_real_backend() -> bool:
    """Return True if the real backend should be used."""
    return os.getenv("USE_REAL_BACKEND", "").lower() in {"1", "true", "yes", "on"}


def search_users_adapter(query: str) -> Tuple[Optional[List[str]], Optional[str]]:
    """Search for users via backend or return stub results.

    Parameters
    ----------
    query:
        The raw query string from the UI.

    Returns
    -------
    usernames, error_message:
        List of usernames if available, or a stub list in fallback mode.
        An error message if the backend call fails.
    """
    if not isinstance(query, str) or not query.strip():
        return None, "Query cannot be empty"

    if not use_real_backend():
        return DUMMY_USERS, None

    try:
        import superNova_2177 as sn_mod
        with sn_mod.SessionLocal() as db:
            results = sn_mod.search_users(query, db)
        return [r.get("username", "") for r in results], None
    except Exception as exc:
        logger.exception("search_users_adapter failed: %s", exc)
        return None, ERROR_MESSAGE

