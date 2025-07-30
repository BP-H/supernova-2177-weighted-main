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
    if 'streamlit_option_menu' not in sys.modules:
        sys.modules['streamlit_option_menu'] = types.SimpleNamespace(option_menu=lambda *a, **k: None)
    return importlib.import_module("ui")


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


