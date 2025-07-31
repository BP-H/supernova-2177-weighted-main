# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

import types
import sys
from pathlib import Path
import pytest
pytest.importorskip("streamlit")
pytestmark = pytest.mark.requires_streamlit

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import streamlit_helpers as sh


def test_render_post_card_uses_ui_components(monkeypatch):
    card_called = {}
    badge_called = {}

    class DummyCard:
        def __enter__(self):
            card_called['entered'] = True
            return self
        def __exit__(self, *exc):
            card_called['exited'] = True
        def classes(self, cls):
            card_called['cls'] = cls
            return self

    def dummy_badge(text):
        badge_called['text'] = text
        return types.SimpleNamespace(classes=lambda cls: badge_called.setdefault('cls', cls))

    dummy_ui = types.SimpleNamespace(
        card=lambda: DummyCard(),
        image=lambda *a, **k: types.SimpleNamespace(classes=lambda *b, **c: None),
        element=lambda *a, **k: types.SimpleNamespace(classes=lambda *b, **c: None),
        badge=dummy_badge,
    )

    monkeypatch.setattr(sh, "ui", dummy_ui)
    monkeypatch.setattr(sh, "st", types.SimpleNamespace())

    sh.render_post_card({"text": "Hello", "likes": 4})

    assert card_called.get('entered')
    assert badge_called.get('text') == "❤️ 4"


def test_render_post_card_plain_streamlit(monkeypatch):
    captured = {}
    dummy_st = types.SimpleNamespace(
        image=lambda img, use_column_width=True: captured.setdefault("image", img),
        write=lambda text: captured.setdefault("write", text),
        caption=lambda text: captured.setdefault("caption", text),
    )

    monkeypatch.setattr(sh, "ui", None)
    monkeypatch.setattr(sh, "st", dummy_st)

    sh.render_post_card({"image": "img.png", "text": "Hi", "likes": 7})

    assert captured["image"] == "img.png"
    assert captured["write"] == "Hi"
    assert captured["caption"] == "❤️ 7"
