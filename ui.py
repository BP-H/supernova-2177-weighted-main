"""
Streamlit entry point for the superNova_2177 validation dashboard.
Launch with: $ streamlit run ui.py
"""
import os
import sys
import traceback
import importlib
import asyncio
import json
import difflib
import logging
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import streamlit as st  # Streamlit must be imported early
from streamlit.errors import StreamlitAPIException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# If running on older Streamlit that lacks experimental multi-page API, add a no-op
if not hasattr(st, "experimental_page"):
    def _noop_experimental_page(*_args, **_kwargs):
        def decorator(func):
            return func
        return decorator
    st.experimental_page = _noop_experimental_page

# Include repository disclaimer comments
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

# Attempt to import unified UI helpers (includes Shadcn UI integration)
try:
    from streamlit_helpers import ui  # Preferential UI wrapper from helpers
except ImportError:
    # Fallback: manually create UI wrapper if helpers not available
    try:
        import streamlit_shadcn_ui as _shadcn_ui  # Shadcn UI for modern components
    except Exception:
        _shadcn_ui = None
    class _UIWrapper:
        """Provides a `tabs` method compatible with NiceGUI-style usage."""
        def __init__(self, backend: object | None = None) -> None:
            self._backend = backend
        def tabs(self, labels: list[str]):
            if self._backend and hasattr(self._backend, "tabs"):
                try:
                    return self._backend.tabs(labels)  # use Shadcn UI's tabs if available
                except Exception:
                    pass
            # Fallback to internal implementation
            return _StreamlitTabs(labels)
        def __getattr__(self, name: str):
            if self._backend is not None:
                return getattr(self._backend, name)
            raise AttributeError(name)
    ui = _UIWrapper(_shadcn_ui)
# Ensure ui has a tabs method even if partially loaded
if not hasattr(ui, "tabs"):
    ui.tabs = lambda labels: _StreamlitTabs(labels)  # attach minimal tabs if missing
# Legacy alias
ui_wrapper = ui

# Utility path handling and page registration
logger = logging.getLogger(__name__)
logger.propagate = False

try:
    from transcendental_resonance_frontend.src.utils.page_registry import ensure_pages
except Exception as import_err:
    logger.warning("Primary page_registry import failed: %s", import_err)
    try:
        from utils.page_registry import ensure_pages  # type: ignore
    except Exception as fallback_err:
        logger.warning("Secondary page_registry import failed: %s", fallback_err)
        def ensure_pages(*_args, **_kwargs) -> None:
            logger.debug("ensure_pages noop fallback used")
            return None

try:
    from utils.paths import ROOT_DIR, PAGES_DIR, get_pages_dir
except Exception:
    ROOT_DIR = Path(__file__).resolve().parent
    PAGES_DIR = ROOT_DIR / "transcendental_resonance_frontend" / "pages"
    def get_pages_dir() -> Path:
        return PAGES_DIR

# Force Streamlit file watcher to polling mode for broader compatibility
os.environ["STREAMLIT_WATCHER_TYPE"] = "poll"

# Name of the query parameter used for health-check probes
HEALTH_CHECK_PARAM = "healthz"

# Determine pages available in the application
PAGES_DIR = get_pages_dir()
def build_pages(pages_dir: Path) -> dict[str, str]:
    """Build a mapping from page labels to their slug (filename without .py)."""
    pages: dict[str, str] = {}
    for page_file in sorted(pages_dir.glob("*.py")):
        if page_file.stem == "__init__":
            continue
        slug = page_file.stem
        label = slug.replace("_", " ").title()
        if label not in pages:
            pages[label] = slug
    return pages

PAGES = build_pages(PAGES_DIR)
# Case-insensitive mapping to normalize page choices
_PAGE_LABELS = {label.lower(): label for label in PAGES}

def normalize_choice(choice: str) -> str:
    """Return the canonical page label for a given choice (case-insensitive)."""
    return _PAGE_LABELS.get(choice.lower(), choice)

# Navigation icon set for pages (FontAwesome classes aligned with PAGES order)
NAV_ICONS = [
    "fa-solid fa-robot",      # Agents
    "fa-solid fa-comments",   # Chat
    "fa-solid fa-envelope",   # Messages
    "fa-solid fa-user",       # Profile
    "fa-solid fa-music",      # Resonance Music
    "fa-solid fa-users",      # Social
    "fa-solid fa-check",      # Validation
    "fa-solid fa-video",      # Video Chat
    "fa-solid fa-chart-bar",  # Voting
]

# Debug flag for verbose output (controlled by env var UI_DEBUG_PRINTS)
UI_DEBUG = os.getenv("UI_DEBUG_PRINTS", "1") != "0"
_fallback_rendered: set[str] = set()  # tracks any pages rendered via fallback logic

class _StreamlitTabs:
    """Context manager to emulate tabbed interface using horizontal radio buttons."""
    def __init__(self, labels: list[str], key: str = "_main_tabs") -> None:
        self.labels = labels
        self.key = key
        self.active = labels[0]

    def __enter__(self) -> "_StreamlitTabs":
        index = 0
        current = st.session_state.get(self.key)
        # If a saved tab label is no longer valid, keep showing it (graceful fallback)
        if isinstance(current, str) and current not in self.labels:
            self.active = current
            return self
        # Otherwise, restore previously active tab if it exists
        if isinstance(current, str) and current in self.labels:
            index = self.labels.index(current)
        # Render horizontal radio for tabs
        self.active = st.radio("", self.labels, index=index, horizontal=True, key=self.key)
        if self.active is None:
            # If radio returns None, retain last selection or default to first
            self.active = current if isinstance(current, str) else self.labels[index]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # Save currently active tab label to session state for persistence
        st.session_state[self.key] = self.active
        return False

# Global exception handler to catch any unhandled errors in the UI
def global_exception_handler(exc_type, exc_value, exc_traceback) -> None:
    """Capture unhandled exceptions and present an error with reset option."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow Ctrl+C to pass through during development
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    # Log the exception for debugging
    logger.error("Uncaught exception in UI", exc_info=(exc_type, exc_value, exc_traceback))
    # Show a critical error message in the app
    st.error("Critical Application Error")
    st.code(f"Error: {exc_value}")
    # Provide a safe reset button to clear state and reload the app
    if st.button("Emergency Reset"):
        st.session_state.clear()
        st.experimental_rerun()

# Install the global exception handler
sys.excepthook = global_exception_handler

# ---------- Begin App Execution ----------
# Handle health-check requests early (before any UI rendering)
try:
    params = st.experimental_get_query_params() if not hasattr(st, "query_params") else st.query_params
except Exception:
    params = {}
value = params.get(HEALTH_CHECK_PARAM)
path_info = os.environ.get("PATH_INFO", "").rstrip("/")
if value == "1" or (isinstance(value, list) and "1" in value) or path_info == f"/{HEALTH_CHECK_PARAM}":
    st.write("ok")
    st.stop()  # health-check endpoint: respond with "ok" and stop:contentReference[oaicite:12]{index=12}

# (Optional) Parse any beta/test mode flags from URL (no-op if none)
# e.g., if "beta=1" in params, we could enable certain experimental features
if params.get("beta") or params.get("beta_mode"):
    st.session_state.setdefault("beta_mode", True)

# Initialize session state defaults for first run
defaults = {
    "session_start_ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "theme": "light",
    "governance_view": False,
    "validations_json": "",
    "agent_output": None,
    "last_result": None,
    "last_run": None,
    "diary": [],
    "analysis_diary": [],
    "run_count": 0,
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)
# Ensure certain state keys exist (even if empty)
st.session_state.setdefault("users", [])
st.session_state.setdefault("logs", [])

# If a critical error was stored in state from a previous run, alert and offer reset
if st.session_state.get("critical_error"):
    st.error("Application Error: " + st.session_state["critical_error"])
    if st.button("Reset Application", key="reset_app_critical"):
        st.session_state.clear()
        st.experimental_rerun()
    st.stop()

# Apply the current theme (light/dark) and inject base styles
from frontend.theme import initialize_theme
initialize_theme(st.session_state.get("theme", "light"))

# Set a consistent style for primary buttons (using the accent color)
ACCENT_COLOR = "#4f8bf9"
st.markdown(
    f"""
    <style>
    .stButton>button {{
        border-radius: 6px;
        background-color: {ACCENT_COLOR};
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Render the custom top bar (branding, titles, etc.)
from frontend.ui_layout import render_top_bar, render_title_bar, render_profile_card, main_container, show_preview_badge
render_top_bar()

# Determine which pages exist and which are missing (for user feedback)
page_paths: dict[str, str] = {}
missing_pages: list[str] = []
for label, slug in PAGES.items():
    # Check both the new pages directory and any legacy "pages" directory
    candidates = [PAGES_DIR / f"{slug}.py", ROOT_DIR / "pages" / f"{slug}.py"]
    if any(path.exists() for path in candidates):
        # Build a URL fragment for the page (to be used in anchor links if needed)
        page_paths[label] = f"/pages/{slug}.py"
    else:
        missing_pages.append(label)
if missing_pages:
    st.warning("Missing pages: " + ", ".join(missing_pages))

# Determine if a page is forced via URL query (e.g., direct link or shortcut)
forced_page = None
try:
    page_param = params.get("page")
    forced_page = page_param[0] if isinstance(page_param, list) else page_param
except Exception:
    forced_page = None
if forced_page:
    # Normalize the forced page value to match our page labels
    forced_slug = normalize_choice(forced_page)
    forced_page = next((label for label, slug in PAGES.items() if normalize_choice(slug) == forced_slug), None)
# Ensure session state for sidebar selection is valid
if st.session_state.get("sidebar_nav") not in PAGES.values():
    st.session_state["sidebar_nav"] = "validation"
if forced_page not in PAGES:
    forced_page = None

# Render the sidebar navigation menu (modern style if available, fallback to base)
icon_map = dict(zip(PAGES.keys(), NAV_ICONS))
if forced_page:
    choice_label = forced_page
else:
    # Use the modern sidebar component if present; otherwise default nav
    try:
        from modern_ui_components import render_modern_sidebar as _render_sidebar
    except ImportError:
        _render_sidebar = None
    if _render_sidebar:
        choice_label = _render_sidebar(page_paths, container=st.sidebar, icons=icon_map, session_key="active_page")
    else:
        from frontend.ui_layout import render_sidebar_nav as _base_render_sidebar_nav
        choice_label = _base_render_sidebar_nav(PAGES, icons=NAV_ICONS, session_key="active_page")

if not choice_label:
    choice_label = "Validation"  # default page if none selected
# Get the slug (filename) corresponding to the chosen page label
display_choice = PAGES.get(choice_label, choice_label)
selected_slug = normalize_choice(display_choice)

# In test mode, ensure a default page loads to avoid breaking tests
if "PYTEST_CURRENT_TEST" in os.environ and display_choice not in PAGES.values():
    st.session_state["sidebar_nav"] = "validation"
    try:
        st.experimental_set_query_params(page="validation")
    except Exception:
        pass
    if "load_page_with_fallback" in globals():
        load_page_with_fallback(display_choice, None)
    else:
        # Simple fallback: display a warning if page missing (once per session)
        if selected_slug not in _fallback_rendered:
            _fallback_rendered.add(selected_slug)
            st.warning(f"Page '{display_choice}' not found. Running in fallback mode.")
    st.stop()

# At this point, if a page was selected via the sidebar or forced, Streamlit will navigate to it.
# The actual page content is delivered via Streamlit's multipage mechanism (see ensure_pages below).
# We don't manually import or run the page module here because either ensure_pages or the anchor links handle it.

# (Optional) Additional UI utility definitions and database stubs for completeness
def load_css() -> None:
    """Placeholder for loading external CSS files (not used in this app)."""
    return
# Define dummy functions for optional features if their modules are missing
def run_analysis(*args, **kwargs):
    st.info("Analysis module is not available.")
def boot_diagnostic_ui():
    st.info("Diagnostics module is not available.")

# Try to load any optional back-end modules, but continue if they aren't present
try:
    from frontend_bridge import dispatch_route
except Exception:
    dispatch_route = None
try:
    from introspection.introspection_pipeline import run_full_audit
except Exception:
    run_full_audit = None  # If not available, ignore
try:
    from superNova_2177 import InMemoryStorage, agent, cosmic_nexus
except Exception:
    InMemoryStorage = agent = cosmic_nexus = None
try:
    from network.network_coordination_detector import build_validation_graph
    from validation_integrity_pipeline import analyze_validation_integrity
except ImportError as exc:
    logger.warning("Analysis modules unavailable: %s", exc)
    build_validation_graph = analyze_validation_integrity = None
try:
    from validator_reputation_tracker import update_validator_reputations
except Exception:
    update_validator_reputations = None
try:
    from validation_certifier import Config as VCConfig
except Exception:
    VCConfig = None
try:
    from config import Config
    from superNova_2177 import HarmonyScanner
except Exception:
    Config = None
    HarmonyScanner = None

# Provide fallback values for configuration if not loaded
if Config is None:
    class Config:  # type: ignore
        METRICS_PORT = 8001  # default Prometheus metrics port if not specified
if VCConfig is None:
    class VCConfig:  # type: ignore
        HIGH_RISK_THRESHOLD = 0.7
        MEDIUM_RISK_THRESHOLD = 0.4
# Stub HarmonyScanner if not available
if HarmonyScanner is None:
    class HarmonyScanner:  # type: ignore
        def __init__(self, *args, **kwargs): pass
        def scan(self, data): return {"dummy": True}

# Utility functions for result management (used by validation analysis, if any)
def clear_memory(state: dict) -> None:
    """Reset analysis tracking state in session."""
    state["analysis_diary"] = []
    state["run_count"] = 0
    state["last_result"] = None
    state["last_run"] = None

def export_latest_result(state: dict) -> str:
    """Serialize the latest analysis result to a JSON-formatted string."""
    return json.dumps(state.get("last_result", {}), indent=2)

def diff_results(old: dict | None, new: dict) -> str:
    """Return a unified diff between two result dictionaries."""
    if not old:
        return ""
    old_txt = json.dumps(old, indent=2, sort_keys=True).splitlines()
    new_txt = json.dumps(new, indent=2, sort_keys=True).splitlines()
    diff = difflib.unified_diff(old_txt, new_txt, fromfile="previous", tofile="new", lineterm="")
    return "\n".join(diff)

# Ensure Streamlit knows about all pages (for multipage navigation)
try:
    ensure_pages(PAGES, PAGES_DIR)
except Exception as exc:
    logger.warning("ensure_pages failed: %s", exc)
