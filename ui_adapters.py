import logging
import os
from typing import Dict, List, Optional, Tuple

import superNova_2177 as sn_mod


def search_users(query: str) -> Tuple[Optional[List[Dict[str, str]]], Optional[str]]:
    """Search for users via the backend when enabled.

    Parameters
    ----------
    query:
        The raw query string from the UI.

    Returns
    -------
    results, error_message:
        ``results`` is a list of user dictionaries when the backend is
        enabled and the call succeeds. ``None`` indicates that the caller
        should display placeholder content. ``error_message`` contains a
        friendly message for the UI when the backend call fails.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query cannot be empty")

    if os.getenv("ENABLE_SEARCH_BACKEND") != "1":
        return None, None

    try:
        with sn_mod.SessionLocal() as db:
            results = sn_mod.search_users(query, db)
        return results, None
    except Exception:  # pragma: no cover - log the actual backend error
        logging.exception("search_users backend error")
        return None, "Unable to fetch search results. Please try again later."
