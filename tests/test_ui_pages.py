# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

import importlib
import contextlib
import types
from pathlib import Path
import sys

import pytest
pytest.importorskip("streamlit")
pytestmark = pytest.mark.requires_streamlit
import streamlit as st

# Ensure repository root is importable
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import frontend.ui_layout as ui_layout
import modern_ui_components as mui
import ui


def test_unknown_page_triggers_fallback(monkeypatch):
    monkeypatch.setenv("UI_DEBUG_PRINTS", "0")
    importlib.reload(ui)

    fallback_called = {}
    monkeypatch.setattr(ui, "_render_fallback", lambda choice: fallback_called.setdefault("choice", choice))
    monkeypatch.setattr(ui, "load_page_with_fallback", lambda choice, paths: ui._render_fallback(choice))
    monkeypatch.setattr(ui, "get_st_secrets", lambda: {})
    monkeypatch.setattr(mui, "render_modern_sidebar", lambda *a, **k: "Ghost")
    monkeypatch.setattr(ui, "render_modern_sidebar", lambda *a, **k: "Ghost")

    class Dummy(contextlib.AbstractContextManager):
        def __enter__(self):
            return self
        def __exit__(self, *exc):
            return False
        def container(self):
            return Dummy()
        def expander(self, *a, **k):
            return Dummy()
        def tabs(self, labels):
            tab_calls.append(labels)
            return [Dummy() for _ in labels]

    tab_calls = []
    monkeypatch.setattr(st, "set_page_config", lambda *a, **k: None)
    monkeypatch.setattr(st, "expander", lambda *a, **k: Dummy())
    monkeypatch.setattr(st, "container", lambda: Dummy())
    monkeypatch.setattr(st, "columns", lambda *a, **k: [Dummy(), Dummy(), Dummy()])
    monkeypatch.setattr(st, "tabs", lambda labels: tab_calls.append(labels) or [Dummy() for _ in labels])
    for fn in [
        "markdown",
        "info",
        "error",
        "warning",
        "write",
        "button",
        "file_uploader",
        "text_input",
        "text_area",
        "divider",
        "progress",
        "json",
        "subheader",
        "radio",
        "toggle",
    ]:
        monkeypatch.setattr(st, fn, lambda *a, **k: None)

    monkeypatch.setattr(st, "session_state", {})
    monkeypatch.setattr(st, "query_params", {})

    for helper in [
        "apply_theme",
        "inject_modern_styles",
        "render_status_icon",
        "render_simulation_stubs",
        "render_stats_section",
    ]:
        monkeypatch.setattr(ui, helper, lambda *a, **k: None)

    monkeypatch.setattr(ui, "render_api_key_ui", lambda *a, **k: {"model": "dummy", "api_key": ""})

    ui.main()

    assert fallback_called.get("choice") == "Ghost"


def test_main_defaults_to_validation(monkeypatch):
    monkeypatch.setenv("UI_DEBUG_PRINTS", "0")
    importlib.reload(ui)

    monkeypatch.setattr(ui, "_render_fallback", lambda choice: None)
    monkeypatch.setattr(ui, "load_page_with_fallback", lambda choice, paths: None)
    monkeypatch.setattr(ui, "get_st_secrets", lambda: {})

    class Dummy(contextlib.AbstractContextManager):
        def __enter__(self):
            return self
        def __exit__(self, *exc):
            return False
        def container(self):
            return Dummy()
        def expander(self, *a, **k):
            return Dummy()
        def tabs(self, labels):
            return [Dummy() for _ in labels]

    monkeypatch.setattr(st, "set_page_config", lambda *a, **k: None)
    monkeypatch.setattr(st, "expander", lambda *a, **k: Dummy())
    monkeypatch.setattr(st, "container", lambda: Dummy())
    monkeypatch.setattr(st, "columns", lambda *a, **k: [Dummy(), Dummy(), Dummy()])
    monkeypatch.setattr(st, "tabs", lambda labels: [Dummy() for _ in labels])
    for fn in [
        "markdown",
        "info",
        "error",
        "warning",
        "write",
        "button",
        "file_uploader",
        "text_input",
        "text_area",
        "divider",
        "progress",
        "json",
        "subheader",
        "radio",
        "toggle",
    ]:
        monkeypatch.setattr(st, fn, lambda *a, **k: None)

    session = {"sidebar_nav": "Ghost"}
    monkeypatch.setattr(st, "session_state", session)
    params = {"page": "Unknown"}
    monkeypatch.setattr(st, "query_params", params)
    monkeypatch.setattr(st, "experimental_get_query_params", lambda: params)
    monkeypatch.setattr(st, "experimental_set_query_params", lambda **k: params.update(k))

    for helper in [
        "apply_theme",
        "inject_modern_styles",
        "render_status_icon",
        "render_simulation_stubs",
        "render_stats_section",
    ]:
        monkeypatch.setattr(ui, helper, lambda *a, **k: None)

    monkeypatch.setattr(ui, "render_api_key_ui", lambda *a, **k: {"model": "dummy", "api_key": ""})
    monkeypatch.setattr(mui, "render_modern_sidebar", lambda *a, **k: session.get("sidebar_nav"))
    monkeypatch.setattr(ui, "render_modern_sidebar", lambda *a, **k: session.get("sidebar_nav"))

    ui.main()

    assert params.get("page") == "Validation"
    assert session.get("sidebar_nav") == "Validation"
