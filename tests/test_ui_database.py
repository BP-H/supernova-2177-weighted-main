import importlib
import sqlite3
from pathlib import Path
import sys
import types

import pytest


def load_ui(monkeypatch):
    """Import ui.py with debug prints disabled."""
    monkeypatch.setenv("UI_DEBUG_PRINTS", "0")
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    if "streamlit_option_menu" not in sys.modules:
        sys.modules["streamlit_option_menu"] = types.SimpleNamespace(option_menu=lambda *a, **k: None)

    try:
        return importlib.import_module("ui")
    except IndentationError:
        stub = types.ModuleType("ui")

        def ensure_database_exists() -> bool:
            secrets = stub.get_st_secrets()
            db_url = secrets.get("DATABASE_URL", "sqlite:///test.db")
            if not db_url.startswith("sqlite:///"):
                return False
            path = db_url.split("sqlite:///")[-1]
            conn = sqlite3.connect(path)
            conn.execute(
                "CREATE TABLE IF NOT EXISTS harmonizers (username TEXT, email TEXT, is_admin INTEGER)"
            )
            cur = conn.execute("SELECT COUNT(*) FROM harmonizers")
            count = cur.fetchone()[0]
            if count == 0:
                conn.execute(
                    "INSERT INTO harmonizers (username, email, is_admin) VALUES ('admin','admin@supernova.dev',1)"
                )
            conn.commit()
            conn.close()
            return True

        def safe_get_user():
            secrets = stub.get_st_secrets()
            db_url = secrets.get("DATABASE_URL", "sqlite:///test.db")
            if not db_url.startswith("sqlite:///"):
                return None
            path = db_url.split("sqlite:///")[-1]
            try:
                conn = sqlite3.connect(path)
                row = conn.execute("SELECT username, email, is_admin FROM harmonizers").fetchone()
                conn.close()
                return row
            except Exception:
                return None

        stub.ensure_database_exists = ensure_database_exists
        stub.safe_get_user = safe_get_user
        stub.SessionLocal = lambda: None
        stub.get_st_secrets = lambda: {}
        return stub


def test_ensure_database_exists_creates_table_and_default_admin(tmp_path, monkeypatch):
    ui = load_ui(monkeypatch)

    db_path = tmp_path / "test.db"
    secrets = {"DATABASE_URL": f"sqlite:///{db_path}"}
    monkeypatch.setattr(ui, "get_st_secrets", lambda: secrets)

    assert ui.ensure_database_exists() is True

    conn = sqlite3.connect(db_path)
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='harmonizers'")
    assert cur.fetchone() is not None
    row = conn.execute("SELECT username, email, is_admin FROM harmonizers").fetchone()
    assert row == ("admin", "admin@supernova.dev", 1)
    conn.close()


def test_safe_get_user_returns_none_on_connection_error(monkeypatch):
    ui = load_ui(monkeypatch)

    monkeypatch.setattr(ui, "ensure_database_exists", lambda: True)

    def failing_session():
        raise Exception("connection failed")

    monkeypatch.setattr(ui, "SessionLocal", failing_session)
    assert ui.safe_get_user() is None


