# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

import pytest
pytest.importorskip("streamlit")
pytestmark = pytest.mark.requires_streamlit

import types
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import modern_ui_components as mui


def test_render_modern_sidebar_default_container(monkeypatch):
    calls = []
    def dummy_button(label, key=None, help=None):
        calls.append(label)
        return False

    dummy_st = types.SimpleNamespace(
        markdown=lambda *a, **k: None,
        button=dummy_button,
        sidebar=types.SimpleNamespace(markdown=lambda *a, **k: None, button=dummy_button),
        session_state={},
    )
    monkeypatch.setattr(mui, "st", dummy_st)
    pages = {"A": "a", "B": "b"}
    assert mui.render_modern_sidebar(pages) == "A"
    assert calls, "buttons rendered"

