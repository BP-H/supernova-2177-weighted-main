"""
Streamlit entry point for the validation dashboard.

Example:
    $ streamlit run ui.py
"""

import os
import time
import streamlit as st  # ensure Streamlit is imported early
if not hasattr(st, "experimental_page"):
    def _noop_experimental_page(*_args, **_kwargs):
        def decorator(func):
            return func
        return decorator
    st.experimental_page = _noop_experimental_page

from datetime import datetime, timezone
import asyncio
import difflib
import io
import json
import logging
import math
import sys
import traceback
import sqlite3
import importlib
from streamlit.errors import StreamlitAPIException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from typing import Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.propagate = False

try:
    from modern_ui_components import (
        render_validation_card,
        render_post_card,
        render_stats_section,
    )
except Exception:  # pragma: no cover - optional dependency
    def render_validation_card(*_a, **_k):
        st.info("validation card unavailable")
    def render_post_card(*_a, **_k):
        st.info("post card unavailable")
    def render_stats_section(*_a, **_k):
        st.info("stats section unavailable")

# Prefer modern sidebar render if available
try:
    from modern_ui_components import render_modern_sidebar as _modern_sidebar_impl
except ImportError:  # pragma: no cover - optional dependency
    _modern_sidebar_impl = None

from frontend.ui_layout import (
    main_container,
    render_title_bar,
    show_preview_badge,
    render_profile_card,
    render_top_bar,
    render_sidebar_nav as _base_render_sidebar_nav,
)

def render_sidebar_nav(*args, **kwargs):
    """Proxy to allow monkeypatching via `render_modern_sidebar` if available."""
    if _modern_sidebar_impl and _modern_sidebar_impl is not render_sidebar_nav:
        return _modern_sidebar_impl(*args, **kwargs)
    return _base_render_sidebar_nav(*args, **kwargs)

# Backwards compatibility alias
render_modern_sidebar = render_sidebar_nav

# Utility path handling
try:
    from transcendental_resonance_frontend.src.utils.page_registry import ensure_pages
except Exception as import_err:  # pragma: no cover - fallback if absolute import fails
    logger.warning("Primary page_registry import failed: %s", import_err)
    try:
        from utils.page_registry import ensure_pages  # type: ignore
    except Exception as fallback_err:  # pragma: no cover - final fallback
        logger.warning("Secondary page_registry import also failed: %s", fallback_err)
        def ensure_pages(*_args, **_kwargs) -> None:
            logger.debug("ensure_pages noop fallback used")
            return None

try:
    from utils.paths import ROOT_DIR, PAGES_DIR, get_pages_dir
except Exception:  # pragma: no cover - fallback when utils.paths is missing
    ROOT_DIR = Path(__file__).resolve().parent
    PAGES_DIR = ROOT_DIR / "transcendental_resonance_frontend" / "pages"
    def get_pages_dir() -> Path:
        return PAGES_DIR

nx = None  # imported lazily in run_analysis
go = None  # imported lazily in run_analysis

# Register fallback watcher for environments that can't use inotify
os.environ["STREAMLIT_WATCHER_TYPE"] = "poll"

# Name of the query parameter used for the CI health check. Adjust here if the
# health check endpoint ever changes.
HEALTH_CHECK_PARAM = "healthz"

# Directory containing Streamlit page modules
PAGES_DIR = get_pages_dir()

def build_pages(pages_dir: Path) -> dict[str, str]:
    """Return a mapping of sidebar labels to page slugs."""
    pages: dict[str, str] = {}
    for page_file in sorted(pages_dir.glob("*.py")):
        if page_file.stem == "__init__":
            continue
        slug = page_file.stem
        label = slug.replace("_", " ").title()
        if label not in pages:
            pages[label] = slug
    return pages

# Mapping of navigation labels to page module names
PAGES = build_pages(PAGES_DIR)

# Case-insensitive lookup for labels
_PAGE_LABELS = {label.lower(): label for label in PAGES}

def normalize_choice(choice: str) -> str:
    """Return the canonical label for ``choice`` ignoring case."""
    return _PAGE_LABELS.get(choice.lower(), choice)

NAV_ICONS = [
    "fa-solid fa-robot",
    "fa-solid fa-comments",
    "fa-solid fa-envelope",
    "fa-solid fa-user",
    "fa-solid fa-music",
    "fa-solid fa-users",
    "fa-solid fa-check",
    "fa-solid fa-video",
    "fa-solid fa-chart-bar",
]

UI_DEBUG = os.getenv("UI_DEBUG_PRINTS", "1") != "0"

_fallback_rendered: set[str] = set()

class _StreamlitTabs:
    """Simple context manager to mimic ``ui.tabs`` using Streamlit widgets."""
    def __init__(self, labels: list[str], key: str = "_main_tabs") -> None:
        self.labels = labels
        self.key = key
        self.active = labels[0]

    def __enter__(self) -> "_StreamlitTabs":
        index = 0
        current = st.session_state.get(self.key)
        if isinstance(current, str) and current not in self.labels:
            self.active = current
            return self
        if isinstance(current, str) and current in self.labels:
            index = self.labels.index(current)
        self.active = st.radio(
            "",
            self.labels,
            horizontal=True,
            index=index,
            key=self.key,
        )
        if self.active is None:
            self.active = current if isinstance(current, str) else self.labels[index]
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        st.session_state[self.key] = self.active
        return False

# If `ui` not already defined, create it
try:
    from streamlit_helpers import ui
except ImportError:
    try:
        import streamlit_shadcn_ui as _shadcn_ui  # type: ignore
    except Exception:
        _shadcn_ui = None
    class _UIWrapper:
        def __init__(self, backend: object | None = None) -> None:
            self._backend = backend

        def tabs(self, labels: list[str]) -> _StreamlitTabs:
            if self._backend and hasattr(self._backend, "tabs"):
                try:
                    return self._backend.tabs(labels)  # type: ignore[return-value]
                except Exception:
                    pass
            return _StreamlitTabs(labels)

        def __getattr__(self, name: str):
            if self._backend is not None:
                return getattr(self._backend, name)
            raise AttributeError(name)

    ui = _UIWrapper(_shadcn_ui)

# Ensure `ui.tabs` is present
if not hasattr(ui, "tabs"):
    ui.tabs = _UIWrapper().tabs  # type: ignore[attr-defined]

ui_wrapper = ui

def log(msg: str) -> None:
    if UI_DEBUG:
        print(msg, file=sys.stderr)

# Global exception handler for Streamlit UI
def global_exception_handler(exc_type, exc_value, exc_traceback) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    st.error("Critical Application Error")
    st.code(f"Error: {exc_value}")
    if st.button("Emergency Reset"):
        st.session_state.clear()
        st.rerun()

sys.excepthook = global_exception_handler

if UI_DEBUG:
    log("\u23f3 Booting superNova_2177 UI...")

from streamlit_helpers import (
    alert,
    header,
    theme_selector,
    safe_container,
    render_post_card,
    render_instagram_grid,
)

from frontend.theme import initialize_theme

try:
    from frontend.ui_layout import overlay_badge, render_title_bar
except ImportError:  # optional dependency fallback
    try:
        from frontend.ui_layout import render_title_bar
    except ImportError:
        def render_title_bar(*args, **kwargs):
            st.warning("⚠️ render_title_bar is unavailable.")
            return None
    def overlay_badge(*args, **kwargs):
        st.warning("⚠️ overlay_badge is unavailable.")
        return None

# Optional modules with fallbacks
try:
    from protocols import AGENT_REGISTRY
except ImportError:  # pragma: no cover - optional dependency
    AGENT_REGISTRY = {}

try:
    from social_tabs import render_social_tab
except Exception:  # pragma: no cover - optional dependency or invalid module
    def render_social_tab() -> None:
        header("👥 Social Features")
        st.info("Social features module not available")

try:
    from voting_ui import render_voting_tab
except ImportError:  # pragma: no cover - optional dependency
    def render_voting_tab() -> None:
        st.info("Voting module not available")

try:
    from agent_ui import render_agent_insights_tab
except ImportError:  # pragma: no cover - optional dependency
    def render_agent_insights_tab() -> None:
        header("🤖 Agent Insights")
        st.info("Agent insights module not available. Install required dependencies.")
        if AGENT_REGISTRY:
            st.write("Available Agents:")
            for name, info in AGENT_REGISTRY.items():
                with st.expander(f"🔧 {name}"):
                    st.write(
                        f"Description: {info.get('description', 'No description')}"
                    )
                    st.write(f"Class: {info.get('class', 'Unknown')}")
        else:
            st.warning("No agents registered")

try:
    from llm_backends import get_backend
except ImportError:  # pragma: no cover - optional dependency
    def get_backend(name, api_key=None):
        return lambda x: {"response": "dummy backend"}

def render_landing_page():
    st.title("🚀 superNova_2177")
    st.markdown(
        """
        ### Advanced Validation Analysis Platform
        
        Welcome to the superNova_2177 validation analyzer. This platform provides:
        
        - **Validation Analysis** - Comprehensive validation pipeline analysis
        - **Agent Playground** - Test and interact with AI agents
        - **Network Coordination** - Advanced network analysis tools
        - **Developer Tools** - Debug and monitoring capabilities
        
        **Demo Mode Available** - Try the platform with sample data.
        
        ---
        
        **Note:** Pages directory not found. Please ensure the following directory exists:
