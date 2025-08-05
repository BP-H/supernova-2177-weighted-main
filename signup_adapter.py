import os
from typing import Tuple

OFFLINE_MODE = os.getenv("OFFLINE_MODE", "0") == "1"

# simple in-memory store for stubbed mode
_stub_users: list[dict] = []


def register_user(username: str, email: str, password: str) -> Tuple[bool, str]:
    """Register a user against the backend or an in-memory stub.

    Returns a tuple ``(success, message)`` where ``success`` indicates whether
    the registration succeeded. ``message`` contains either ``"ok"`` or a
    human-readable error description.
    """
    if OFFLINE_MODE:
        if any(u["username"] == username or u["email"] == email for u in _stub_users):
            return False, "Username or email already exists"
        _stub_users.append({"username": username, "email": email, "password": password})
        return True, "ok"
    else:
        from fastapi import HTTPException
        from superNova_2177 import HarmonizerCreate, SessionLocal, register_harmonizer

        try:
            with SessionLocal() as db:
                user = HarmonizerCreate(username=username, email=email, password=password)
                register_harmonizer(user, db)
            return True, "ok"
        except HTTPException as exc:  # duplicate or other HTTP errors
            if exc.status_code == 400:
                return False, exc.detail
            return False, "Registration failed"
        except Exception as exc:  # pragma: no cover - unexpected failures
            return False, str(exc)


def reset_stub() -> None:
    """Clear stubbed users (testing helper)."""
    _stub_users.clear()
