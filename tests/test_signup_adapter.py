import importlib
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))


def test_stub_signup(monkeypatch):
    monkeypatch.setenv("OFFLINE_MODE", "1")
    import signup_adapter
    importlib.reload(signup_adapter)
    signup_adapter.reset_stub()

    ok, _ = signup_adapter.register_user("alice", "a@example.com", "password123")
    assert ok
    ok, msg = signup_adapter.register_user("alice", "b@example.com", "password123")
    assert not ok and "exists" in msg.lower()
    ok, msg = signup_adapter.register_user("bob", "a@example.com", "password123")
    assert not ok and "exists" in msg.lower()


def test_backend_signup(tmp_path, monkeypatch):
    monkeypatch.setenv("OFFLINE_MODE", "0")
    monkeypatch.setenv("DB_MODE", "central")
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SECRET_KEY", "testsecret")

    import db_models
    import superNova_2177
    import signup_adapter

    importlib.reload(db_models)
    importlib.reload(superNova_2177)
    superNova_2177.create_database()
    superNova_2177.Base.metadata.drop_all(bind=superNova_2177.engine)
    superNova_2177.Base.metadata.create_all(bind=superNova_2177.engine)
    importlib.reload(signup_adapter)

    ok, _ = signup_adapter.register_user("carol", "c@example.com", "password123")
    assert ok
    ok, msg = signup_adapter.register_user("carol", "d@example.com", "password123")
    assert not ok and "exists" in msg.lower()
    ok, msg = signup_adapter.register_user("dave", "c@example.com", "password123")
    assert not ok and "exists" in msg.lower()
