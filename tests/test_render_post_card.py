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
    """Card renders correctly when a UI backend is present."""
    card_called: dict = {}
    captured: list = []  # collect (tag, content) tuples from ui.element / ui.image

    class DummyCard:
        def __enter__(self):
            card_called["entered"] = True
            return self

        def __exit__(self, *exc):
            card_called["exited"] = True

        def classes(self, cls):
            card_called["cls"] = cls
            return self

    dummy_ui = types.SimpleNamespace(
        card=lambda: DummyCard(),
        image=lambda img, **k: types.SimpleNamespace(
            classes=lambda cls: captured.append(("img", img))
        ),
        element=lambda tag, content: types.SimpleNamespace(
            classes=lambda cls: captured.append((tag, content))
        ),
    )

    monkeypatch.setattr(sh, "ui", dummy_ui)
    monkeypatch.setattr(sh, "st", types.SimpleNamespace())  # stub Streamlit

    sh.render_post_card(
        {"image": "pic.png", "text": "Hello", "likes": 4, "user": "alice"}
    )

    assert card_called.get("entered")
    assert ("img", "pic.png") in captured
    # the final element should be the reactions line
    assert ("div", "❤️ 4 🔁 💬") in captured


def test_render_post_card_plain_streamlit(monkeypatch):
    """Card renders correctly when *ui* is absent (pure Streamlit fallback)."""
    captured: dict = {}

    dummy_st = types.SimpleNamespace(
        # only markdown output is used by the fallback HTML renderer
        markdown=lambda html, unsafe_allow_html=True: captured.setdefault("html", html),
    )

    monkeypatch.setattr(sh, "ui", None)  # force fallback mode
    monkeypatch.setattr(sh, "st", dummy_st)

    sh.render_post_card(
        {"image": "img.png", "text": "Hi", "likes": 7, "user": "bob"}
    )

    html_out = captured["html"]
    assert "img.png" in html_out  # image rendered
    assert "Hi" in html_out       # caption rendered
    assert "bob" in html_out      # username rendered
    assert "❤️ 7" in html_out     # like count rendered
    # style hints present
    assert "border-radius" in html_out

