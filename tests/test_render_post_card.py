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
    captured = []

    class DummyCard:
        def __enter__(self):
            card_called['entered'] = True
            return self
        def __exit__(self, *exc):
            card_called['exited'] = True
        def classes(self, cls):
            card_called['cls'] = cls
            return self

    dummy_ui = types.SimpleNamespace(
        card=lambda: DummyCard(),
        image=lambda img, **k: types.SimpleNamespace(classes=lambda cls: captured.append(("img", img))),
        element=lambda tag, content: types.SimpleNamespace(classes=lambda cls: captured.append((tag, content))),
    )

    monkeypatch.setattr(sh, "ui", dummy_ui)
    monkeypatch.setattr(sh, "st", types.SimpleNamespace())

    sh.render_post_card({"image": "pic.png", "text": "Hello", "likes": 4, "user": "alice"})

    assert card_called.get('entered')
    assert ("img", "pic.png") in captured
    assert ("div", "❤️ 4 🔁 💬") in captured


def test_render_post_card_plain_streamlit(monkeypatch):
    captured = {}
    dummy_st = types.SimpleNamespace(
        markdown=lambda html, unsafe_allow_html=True: captured.setdefault("html", html),
    )

    monkeypatch.setattr(sh, "ui", None)
    monkeypatch.setattr(sh, "st", dummy_st)

    sh.render_post_card({"image": "img.png", "text": "Hi", "likes": 7, "user": "bob"})

    html_out = captured["html"]
    assert "img.png" in html_out
    assert "Hi" in html_out
    assert "bob" in html_out
    assert "❤️ 7" in html_out
    assert "border-radius" in html_out
