import types
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import modern_ui_components as mui


def test_render_modern_sidebar_default_container(monkeypatch):
    calls = []
    def dummy_radio(label, options, key=None, index=0):
        calls.append(options)
        return options[index]

    dummy_st = types.SimpleNamespace(
        markdown=lambda *a, **k: None,
        radio=dummy_radio,
        sidebar=types.SimpleNamespace(markdown=lambda *a, **k: None, radio=dummy_radio),
        session_state={},
    )
    monkeypatch.setattr(mui, "USE_OPTION_MENU", False)
    monkeypatch.setattr(mui, "st", dummy_st)
    pages = {"A": "a", "B": "b"}
    assert mui.render_modern_sidebar(pages) == "A"
    assert calls, "buttons rendered"

