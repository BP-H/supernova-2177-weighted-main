import types
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import modern_ui_components as mui


def test_render_modern_sidebar_default_container(monkeypatch):
    dummy_st = types.SimpleNamespace(
        markdown=lambda *a, **k: None,
        radio=lambda label, opts: opts[0],
    )
    monkeypatch.setattr(mui, "st", dummy_st)
    pages = {"A": "a", "B": "b"}
    assert mui.render_modern_sidebar(pages) == "A"

