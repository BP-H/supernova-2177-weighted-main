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

# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

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
import time
from streamlit.errors import StreamlitAPIException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from typing import Optional
from frontend import ui_layout


try:
    from modern_ui_components import (
        render_validation_card,
        render_stats_section,
    )
except Exception:  # pragma: no cover - optional dependency
    def render_validation_card(*_a, **_k):
        st.info("validation card unavailable")

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
from pathlib import Path
import logging
from utils.paths import ROOT_DIR, PAGES_DIR

logger = logging.getLogger(__name__)
logger.propagate = False

try:
    from transcendental_resonance_frontend.src.utils.page_registry import (
        ensure_pages,
        get_pages_dir,
    )
except Exception as import_err:  # pragma: no cover - fallback if absolute import fails
    logger.warning("Primary page_registry import failed: %s", import_err)
    try:
        from utils.page_registry import ensure_pages, get_pages_dir  # type: ignore
    except Exception as fallback_err:  # pragma: no cover - final fallback
        logger.warning("Secondary page_registry import also failed: %s", fallback_err)

        def ensure_pages(*_args, **_kwargs) -> None:
            logger.debug("ensure_pages noop fallback used")
            return None

        def get_pages_dir() -> Path:
            return (
                Path(__file__).resolve().parent
                / "transcendental_resonance_frontend"
                / "pages"
            )



nx = None  # imported lazily in run_analysis
go = None  # imported lazily in run_analysis
# Register fallback watcher for environments that can't use inotify
os.environ["STREAMLIT_WATCHER_TYPE"] = "poll"


# Name of the query parameter used for the CI health check. Adjust here if the
# health check endpoint ever changes.
HEALTH_CHECK_PARAM = "healthz"

# Directory containing Streamlit page modules
ROOT_DIR = Path(__file__).resolve().parent
PAGES_DIR = get_pages_dir()

# Mapping of navigation labels to page module names

PAGES = {
    "Validation": "validation",
    "Voting": "voting",
    "Agents": "agents",
    "Resonance Music": "resonance_music",
    "Chat": "chat",
    "Social": "social",
    "Profile": "profile",
}

# Case-insensitive lookup for labels
_PAGE_LABELS = {label.lower(): label for label in PAGES}


def normalize_choice(choice: str) -> str:
    """Return the canonical label for ``choice`` ignoring case."""
    return _PAGE_LABELS.get(choice.lower(), choice)

# Icons used in the navigation bar. Must be single-character emojis or
# valid Bootstrap icon codes prefixed with ``"bi bi-"``.
NAV_ICONS = ["✅", "📊", "🤖", "🎵", "💬", "👥", "👤"]


# Toggle verbose output via ``UI_DEBUG_PRINTS``
UI_DEBUG = os.getenv("UI_DEBUG_PRINTS", "1") != "0"

# Tracks slugs of fallback pages rendered in this session.
_fallback_rendered: set[str] = set()


def log(msg: str) -> None:
    if UI_DEBUG:
        print(msg, file=sys.stderr)


# Global exception handler for Streamlit UI
def global_exception_handler(exc_type, exc_value, exc_traceback) -> None:
    """Handle all uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    st.error("Critical Application Error")
    st.code(f"Error: {exc_value}")

    if st.button("Emergency Reset"):
        st.session_state.clear()
        st.rerun()


# Install global handler
sys.excepthook = global_exception_handler

if UI_DEBUG:
    log("\u23f3 Booting superNova_2177 UI...")
from streamlit_helpers import (
    alert,
    apply_theme,
    header,
    theme_selector,
    safe_container,
)

try:
    from modern_ui import (
        inject_modern_styles,
        render_stats_section,
    )
except Exception:  # pragma: no cover - gracefully handle missing/invalid module
    def inject_modern_styles(*_a, **_k):
        return None

    def render_stats_section(*_a, **_k):
        st.info("stats section unavailable")


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


# Optional modules used throughout the UI. Provide simple fallbacks
# when the associated packages are not available.
try:
    from protocols import AGENT_REGISTRY
except ImportError:  # pragma: no cover - optional dependency
    AGENT_REGISTRY = {}

try:
    from social_tabs import render_social_tab
except ImportError:  # pragma: no cover - optional dependency

    def render_social_tab() -> None:
        st.subheader("👥 Social Features")
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
        st.subheader("🤖 Agent Insights")
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
    """Render fallback landing page when pages directory is missing."""
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
        ```
        transcendental_resonance_frontend/pages/
        ```
        """
    )

    # Show diagnostic information
    st.subheader("🔧 System Diagnostics")
    col1, col2 = st.columns(2)

    with col1:
        st.info("📁 Expected Pages Directory")
        st.code(str(PAGES_DIR))

    with col2:
        st.info("🔍 Directory Status")
        if PAGES_DIR.exists():
            st.success("Directory exists")
        else:
            st.error("Directory missing")

    # Show available fallback features
    st.subheader("🎮 Available Features")
    if st.button("Run Validation Analysis"):
        run_analysis([], layout="force")

    if st.button("Show Boot Diagnostics"):
        boot_diagnostic_ui()

    # Overlay with quick start actions when no page modules are present
    st.markdown(
        """
        <style>
        .landing-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        .landing-overlay-content {
            background: rgba(30, 30, 30, 0.85);
            backdrop-filter: blur(6px);
            padding: 2rem 3rem;
            border-radius: 12px;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    overlay = st.container()
    with overlay:
        st.markdown(
            "<div class='landing-overlay'><div class='landing-overlay-content'>",
            unsafe_allow_html=True,
        )
        st.markdown("### Quick Actions", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create Proposal", key="landing_create_proposal"):
                load_page_with_fallback(
                    "Voting",
                    [
                        f"transcendental_resonance_frontend.pages.{PAGES['Voting']}",
                        f"pages.{PAGES['Voting']}",
                    ],
                )
        with col2:
            if st.button("Run Validation", key="landing_run_validation"):
                run_analysis([], layout="force")
        st.markdown("</div></div>", unsafe_allow_html=True)


def inject_modern_styles() -> None:
    """Backward compatible alias for modern theme injection."""
    from frontend.theme import inject_modern_styles as _impl

    _impl()


# Backward compatibility alias
def inject_dark_theme() -> None:
    """Legacy alias for inject_modern_styles()."""
    inject_modern_styles()


def load_page_with_fallback(choice: str, module_paths: list[str] | None = None) -> None:
    """Load a page via ``st.switch_page`` or fall back to importing the module with graceful handling."""
    # Normalize choice label for slug-based matching
    choice = normalize_choice(choice)

    if module_paths is None:
        module = PAGES.get(choice)
        if not module and choice.lower() in PAGES.values():
            module = choice.lower()

        if not module:
            st.error(f"Unknown page: {choice}")
            if "_render_fallback" in globals():
                _render_fallback(choice)
            return

        module_paths = [
            f"transcendental_resonance_frontend.pages.{module}",
            f"pages.{module}",
        ]


    # Validate PAGES_DIR existence
    PAGES_DIR = get_pages_dir()
    if not PAGES_DIR.exists():
        st.error(f"Pages directory not found: {PAGES_DIR}")
        if "_render_fallback" in globals():
            _render_fallback(choice)
        return

    # Track the last exception for reporting
    last_exc: Exception | None = None
    attempted_paths = set()  # Track attempted paths to avoid infinite loops

    # First try switching pages using Streamlit's multipage support
    for module_path in module_paths:
        if module_path in attempted_paths:
            continue
        attempted_paths.add(module_path)
        filename = module_path.rsplit(".", 1)[-1] + ".py"
        candidate_files = [
            ROOT_DIR / "pages" / filename,
            PAGES_DIR / filename,
        ]

        for page_file in candidate_files:
            if page_file.exists():
                rel_path = f"pages/{page_file.stem}"  # ✅ no .py extension for st.switch_page
                try:
                    st.switch_page(rel_path)
                    _fallback_rendered.clear()
                    return
                except StreamlitAPIException as exc:
                    st.toast(f"Switch failed for {choice}: {exc}", icon="⚠️")
                    logger.debug("File exists but switch failed: %s", page_file)
                    break
                except Exception as exc:
                    logging.error(
                        "switch_page failed for %s: %s", rel_path, exc, exc_info=True
                    )
                    logger.debug("File exists but switch failed: %s", page_file)
                    last_exc = exc
                    break


        # Fallback: import the module directly and call ``render`` or ``main``
        try:
            page_mod = importlib.import_module(module_path)
            for method_name in ("render", "main"):
                if hasattr(page_mod, method_name):
                    getattr(page_mod, method_name)()
                    _fallback_rendered.clear()
                    return
        except ImportError:
            continue
        except Exception as exc:  # Unexpected failure
            last_exc = exc
            logging.error("Error executing %s: %s", module_path, exc, exc_info=True)
            break

    st.toast("Unable to load page. Showing preview.", icon="⚠️")
    if choice == "Validation":
        st.error("Validation page failed to load")
    if "_render_fallback" in globals():
        _render_fallback(choice)
    if last_exc:
        with st.expander("Show error details"):
            st.exception(last_exc)


def _render_fallback(choice: str) -> None:
    """Render built-in fallback if module is missing or errors out."""
    # Normalize and derive slug/module name
    normalized = normalize_choice(choice)
    slug = PAGES.get(normalized, str(normalized)).lower()

    # Prevent rendering the same fallback repeatedly.
    if slug in _fallback_rendered:
        return
    _fallback_rendered.add(slug)

    try:
        from transcendental_resonance_frontend.src.utils.api import OFFLINE_MODE
    except Exception:
        OFFLINE_MODE = False

    # Candidate paths to try loading from
    page_candidates = [
        ROOT_DIR / "pages" / f"{slug}.py",
        get_pages_dir() / f"{slug}.py",
        Path.cwd() / "pages" / f"{slug}.py",
    ]

    loaded = False
    if hasattr(st, "experimental_page"):
        for page_file in page_candidates:
            if not page_file.exists():
                continue

            logger.debug("Attempting to load %s from %s", slug, page_file)

            try:
                spec = importlib.util.spec_from_file_location(
                    f"_page_{slug}", page_file
                )
                if not spec or not spec.loader:
                    continue

                mod = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = mod
                spec.loader.exec_module(mod)

                # Call either `render` or `main` once imported
                for fn in ("render", "main"):
                    if hasattr(mod, fn):
                        try:
                            getattr(mod, fn)()      # run the page
                            loaded = True
                            break
                        except Exception as exc:
                            logger.error(
                                "Error running %s.%s: %s",
                                slug, fn, exc, exc_info=True,
                            )
                if loaded:
                    break     # page loaded successfully → stop loop

            except Exception as exc:
                logger.error(
                    "Error loading page candidate %s: %s",
                    page_file, exc, exc_info=True,
                )

    # If we managed to render a page above, simply return
    if loaded:
        return


    # Map to fallback UI stubs
    fallback_pages = {
        "validation": render_modern_validation_page,
        "voting": render_modern_voting_page,
        "agents": render_modern_agents_page,
        "resonance music": render_modern_music_page,
        "chat": render_modern_chat_page,
        "social": render_modern_social_page,
        "profile": render_modern_profile_page,
    }
    fallback_fn = fallback_pages.get(slug)
    if fallback_fn:
        logger.debug("Rendering fallback for %s", slug)
        if OFFLINE_MODE:
            st.toast("Offline mode: using mock services", icon="⚠️")
        show_preview_badge("🚧 Preview Mode")
        fallback_fn()

    else:
        st.toast(f"No fallback available for page: {choice}", icon="⚠️")

def render_modern_validation_page():
    render_title_bar("✅", "Validation Console")
    st.markdown("**Timeline**")
    st.markdown("- Task queued\n- Running analysis\n- Completed")
    progress = st.progress(0)
    for i in range(5):
        time.sleep(0.1)
        progress.progress((i + 1) / 5)
    st.success("Status: OK")


def render_modern_voting_page():
    render_title_bar("🗳️", "Voting Dashboard")
    votes = {"Proposal A": 3, "Proposal B": 5}
    total = sum(votes.values()) or 1
    for label, count in votes.items():
        st.write(f"{label}: {count} votes")
        st.progress(count / total)


def render_modern_agents_page():
    render_title_bar("🤖", "AI Agents")
    agents = ["Guardian", "Oracle", "Resonance"]
    cols = st.columns(len(agents))
    for col, name in zip(cols, agents):
        with col:
            st.image("https://via.placeholder.com/80", width=80)
            st.write(name)
            st.line_chart([1, 3, 2, 4])


def render_modern_music_page():
    render_title_bar("🎵", "Resonance Music")
    st.line_chart([0, 1, 0, -1, 0])
    st.caption("Harmonic signature: A# minor")


def render_modern_social_page():
    render_title_bar("👥", "Social Network")
    st.markdown("😀 @alice #hello")
    st.markdown("🔥 Trending: #resonance #ai")
    st.success("Social feed placeholder loaded")


def render_modern_chat_page() -> None:
    """Simple placeholder page for the Chat section."""
    render_title_bar("💬", "Chat")
    st.toast("Chat module not yet implemented.")


def render_modern_profile_page() -> None:
    """Placeholder profile page."""
    render_title_bar("👤", "Profile")
    st.toast("Profile management pending implementation.")


def render_sidebar() -> str:
    """Render the left sidebar with navigation and quick actions."""
    user = safe_get_user()
    avatar = getattr(user, "profile_pic", "https://via.placeholder.com/64")
    username = getattr(user, "username", "Guest")

    render_profile_card(username, avatar)

    # Actions in a cleaner expander format
    with st.sidebar.expander("Create Proposal"):
        st.button("Create Proposal")
    with st.sidebar.expander("Run Validation"):
        st.button("Run Validation")

    # Theme toggle
    dark = st.sidebar.toggle("Dark Mode", value=st.session_state.get("theme") == "dark")
    st.session_state["theme"] = "dark" if dark else "light"

    # Environment tag
    env = os.getenv("ENV", "development").lower()
    env_tag = "🚀 Production" if env.startswith("prod") else "🧪 Development"
    st.sidebar.markdown(env_tag)

    # Navigation
    icon_map = dict(zip(PAGES.keys(), NAV_ICONS))
    if "render_modern_sidebar" in globals():
        choice_label = render_modern_sidebar(
            PAGES,
            container=st.sidebar,
            icons=icon_map,
            session_key="active_page",
        )
    else:
        choice_label = render_sidebar_nav(PAGES, icons=NAV_ICONS, session_key="active_page")

    # Normalize and convert label to lowercase slug
    return normalize_choice(PAGES.get(choice_label, choice_label))



def load_css() -> None:
    """Placeholder for loading custom CSS."""
    pass


# Accent color used for button styling
ACCENT_COLOR = "#4f8bf9"
from api_key_input import render_api_key_ui, render_simulation_stubs
from status_indicator import render_status_icon

# Optional UI utilities - provide fallbacks if not available
try:
    from ui_utils import load_rfc_entries, parse_summary, summarize_text, render_main_ui
except ImportError:  # pragma: no cover - optional dependency

    def load_rfc_entries():
        return []

    def parse_summary(text):
        return {"summary": text[:100] + "..." if len(text) > 100 else text}

    def summarize_text(text):
        return text[:200] + "..." if len(text) > 200 else text

    def render_main_ui():
        st.info("Main UI utilities not available")


# Database fallback for local testing
try:
    from db_models import Harmonizer, SessionLocal, UniverseBranch

    DATABASE_AVAILABLE = True
except Exception:  # pragma: no cover - missing ORM
    DATABASE_AVAILABLE = False
    from stubs.mock_db import Harmonizer, SessionLocal, UniverseBranch


def _run_async(coro):
    """Execute ``coro`` regardless of event loop state."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        return loop.run_until_complete(coro)


try:
    from frontend_bridge import dispatch_route
except Exception:  # pragma: no cover - optional dependency
    dispatch_route = None

try:
    from introspection.introspection_pipeline import run_full_audit
except Exception:  # pragma: no cover - optional module
    run_full_audit = None  # type: ignore

try:
    from superNova_2177 import InMemoryStorage, agent, cosmic_nexus
except Exception:  # pragma: no cover - optional runtime globals
    cosmic_nexus = None  # type: ignore
    agent = None  # type: ignore
    InMemoryStorage = None  # type: ignore


try:
    from network.network_coordination_detector import build_validation_graph
    from validation_integrity_pipeline import analyze_validation_integrity
except ImportError as exc:  # pragma: no cover - optional dependency
    logger.warning("Analysis modules unavailable: %s", exc)
    build_validation_graph = None  # type: ignore
    analyze_validation_integrity = None  # type: ignore

try:
    from validator_reputation_tracker import update_validator_reputations
except Exception:  # pragma: no cover - optional dependency
    update_validator_reputations = None


def get_st_secrets() -> dict:
    """Return Streamlit secrets with a fallback for development."""
    try:
        return st.secrets  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover - optional in dev/CI
        return {
            "SECRET_KEY": "dev",
            "DATABASE_URL": "sqlite:///:memory:",
        }


sample_path = Path(__file__).resolve().parent / "sample_validations.json"

try:
    from validation_certifier import Config as VCConfig
except Exception:  # pragma: no cover - optional debug dependencies
    VCConfig = None  # type: ignore

try:
    from config import Config
    from superNova_2177 import HarmonyScanner
except Exception:  # pragma: no cover - optional debug dependencies
    HarmonyScanner = None  # type: ignore
    Config = None  # type: ignore

if Config is None:

    class Config:  # type: ignore[no-redef]
        METRICS_PORT = 1234


if VCConfig is None:

    class VCConfig:  # type: ignore[no-redef]
        HIGH_RISK_THRESHOLD = 0.7
        MEDIUM_RISK_THRESHOLD = 0.4


if HarmonyScanner is None:

    class HarmonyScanner:  # type: ignore[no-redef]
        def __init__(self, *_a, **_k):
            pass

        def scan(self, _data):
            return {"dummy": True}


def clear_memory(state: dict) -> None:
    """Reset analysis tracking state."""
    state["analysis_diary"] = []
    state["run_count"] = 0
    state["last_result"] = None
    state["last_run"] = None


def export_latest_result(state: dict) -> str:
    """Return the latest result as a JSON blob."""
    return json.dumps(state.get("last_result", {}), indent=2)


def diff_results(old: dict | None, new: dict) -> str:
    """Return a unified diff between two result dictionaries."""
    if not old:
        return ""
    old_txt = json.dumps(old, indent=2, sort_keys=True).splitlines()
    new_txt = json.dumps(new, indent=2, sort_keys=True).splitlines()
    diff = difflib.unified_diff(
        old_txt,
        new_txt,
        fromfile="previous",
        tofile="new",
        lineterm="",
    )
    return "\n".join(diff)


def generate_explanation(result: dict) -> str:
    """Generate a human readable integrity summary."""
    integrity = result.get("integrity_analysis", {})
    if not integrity:
        return "No integrity analysis available."
    risk = integrity.get("risk_level", "unknown")
    score = integrity.get("overall_integrity_score", "N/A")
    lines = [f"Risk level: {risk}", f"Integrity score: {score}"]
    recs = result.get("recommendations") or []
    if recs:
        lines.append("Recommendations:")
        for r in recs:
            lines.append(f"- {r}")
    return "\n".join(lines)


def run_analysis(validations, *, layout: str = "force"):
    """Execute the validation integrity pipeline and display results."""
    global nx, go
    if nx is None:
        try:
            import networkx as nx  # type: ignore
        except ImportError:
            nx = None
    if go is None:
        try:
            import plotly.graph_objects as go  # type: ignore
        except ImportError:
            go = None
    if analyze_validation_integrity is None or build_validation_graph is None:
        st.error(
            "Required analysis modules are missing. Please install optional dependencies."
        )
        return {}
    if not validations:
        try:
            with open(sample_path) as f:
                sample = json.load(f)
                validations = sample.get("validations", [])
        except Exception:
            validations = [{"validator": "A", "target": "B", "score": 0.5}]
        alert("No validations provided – using fallback data.", "warning")
        if os.getenv("UI_DEBUG_PRINTS", "1") != "0":
            print("✅ UI diagnostic agent active")

    with st.spinner("Loading..."):
        result = analyze_validation_integrity(validations)

    st.subheader("Validations")
    for entry in validations:
        render_validation_card(entry)

    consensus = result.get("consensus_score")
    if consensus is not None:
        st.metric("Consensus Score", round(consensus, 3))

    integrity = result.get("integrity_analysis", {})
    score = integrity.get("overall_integrity_score")
    if score is not None:
        color = "green"
        if score < VCConfig.MEDIUM_RISK_THRESHOLD:
            color = "red"
        elif score < VCConfig.HIGH_RISK_THRESHOLD:
            color = "yellow"
        tooltip = (
            f"Green \u2265 {VCConfig.HIGH_RISK_THRESHOLD}, "
            f"Yellow \u2265 {VCConfig.MEDIUM_RISK_THRESHOLD}, "
            f"Red < {VCConfig.MEDIUM_RISK_THRESHOLD}"
        )
        st.markdown(
            f"<span title='{tooltip}' "
            f"style='background-color:{color};color:white;"
            f"padding:0.25em 0.5em;border-radius:0.25em;'>"
            f"Integrity Score: {score:.2f}</span>",
            unsafe_allow_html=True,
        )

    st.subheader("Analysis Result")
    st.json(result)

    graph_data = build_validation_graph(validations)
    edges = graph_data.get("edges", [])
    if edges and nx is not None:
        G = nx.Graph()

        # Collect voter metadata from the validations
        voter_meta: dict[str, dict[str, str]] = {}
        for entry in validations:
            vid = entry.get("validator_id")
            if not vid:
                continue
            meta = voter_meta.setdefault(vid, {})
            cls = (
                entry.get("validator_class")
                or entry.get("class")
                or entry.get("affiliation")
                or entry.get("specialty")
            )
            species = entry.get("species") or entry.get("validator_species")
            if cls and "voter_class" not in meta:
                meta["voter_class"] = str(cls)
            if species and "species" not in meta:
                meta["species"] = str(species)

        # Add nodes with metadata and default fallbacks
        for node in graph_data.get("nodes", []):
            meta = voter_meta.get(node, {})
            G.add_node(
                node,
                voter_class=meta.get("voter_class", "unknown"),
                species=meta.get("species", "unknown"),
            )

        for v1, v2, w in edges:
            G.add_edge(v1, v2, weight=w)

        # Offer GraphML download of the constructed graph including metadata
        gm_buf = io.BytesIO()
        try:
            nx.write_graphml(G, gm_buf)
            gm_buf.seek(0)
            st.download_button(
                "Download GraphML",
                gm_buf.getvalue(),
                file_name="graph.graphml",
            )
        except Exception as exc:  # pragma: no cover - optional
            logger.warning(f"GraphML export failed: {exc}")

        # Determine layout
        if layout == "circular":
            pos = nx.circular_layout(G)
        elif layout == "grid":
            side = math.ceil(math.sqrt(len(G)))
            pos = {n: (i % side, i // side) for i, n in enumerate(G.nodes())}
        else:
            pos = nx.spring_layout(G, seed=42)

        # Load validator reputations if available
        reputations = {}
        if update_validator_reputations:
            try:
                rep_result = update_validator_reputations(validations)
                if isinstance(rep_result, dict):
                    reputations = rep_result.get("reputations", {})
            except Exception as exc:  # pragma: no cover - optional
                logger.warning(f"Reputation calc failed: {exc}")

        if go is not None:
            edge_x = []
            edge_y = []
            for u, v in G.edges():
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]
            edge_trace = go.Scatter(
                x=edge_x,
                y=edge_y,
                line=dict(width=0.5, color="#888"),
                hoverinfo="none",
                mode="lines",
            )

            node_x = []
            node_y = []
            texts = []
            node_sizes = []
            node_colors = []
            max_rep = max(reputations.values()) if reputations else 1.0
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                texts.append(str(node))
                rep = reputations.get(node)
                node_sizes.append(10 + (rep or 0) * 20)
                node_colors.append(rep if rep is not None else 0.5)

            node_trace = go.Scatter(
                x=node_x,
                y=node_y,
                mode="markers+text",
                text=texts,
                hoverinfo="text",
                marker=dict(
                    size=node_sizes,
                    color=node_colors,
                    colorscale="Viridis",
                    cmin=0,
                    cmax=max_rep,
                    showscale=bool(reputations),
                ),
            )

            fig = go.Figure(data=[edge_trace, node_trace])
            st.subheader("Validator Coordination Graph")
            st.plotly_chart(fig, use_container_width=True)

            img_buf = io.BytesIO()
            try:
                fig.write_image(img_buf, format="png")
                img_buf.seek(0)
                st.download_button(
                    "Download Graph Image",
                    img_buf.getvalue(),
                    file_name="graph.png",
                )
            except Exception as exc:  # pragma: no cover - optional
                logger.warning(f"Image export failed: {exc}")
        else:
            st.info("Install plotly for graph visualization")
    elif edges:
        st.info("Install networkx for graph visualization")

    if st.button("Explain This Score"):
        explanation = generate_explanation(result)
        with st.expander("Score Explanation"):
            st.markdown(explanation)

    return result


def boot_diagnostic_ui():
    """Render a simple diagnostics UI used during boot."""
    header("Boot Diagnostic", layout="centered")

    st.subheader("Config Test")
    if Config is not None:
        st.success("Config import succeeded")
        st.write({"METRICS_PORT": Config.METRICS_PORT})
    else:
        alert("Config import failed", "error")

    st.subheader("Harmony Scanner Check")
    scanner = HarmonyScanner(Config()) if Config and HarmonyScanner else None
    if scanner:
        st.success("HarmonyScanner instantiated")
    else:
        alert("HarmonyScanner init failed", "error")

    if st.button("Run Dummy Scan") and scanner:
        try:
            scanner.scan("hello world")
            st.success("Dummy scan completed")
        except Exception as exc:  # pragma: no cover - debug only
            alert(f"Dummy scan error: {exc}", "error")

    st.subheader("Validation Analysis")
    run_analysis([], layout="force")


def render_validation_ui(
    sidebar: Optional[st.delta_generator.DeltaGenerator] = None,
    main_container: Optional[st.delta_generator.DeltaGenerator] = None,
) -> None:
    """Main entry point for the validation analysis UI with error handling."""
    if sidebar is None:
        sidebar = st.sidebar
    if main_container is None:
        main_container = st

    try:
        page_paths = {
            label: f"/pages/{mod}.py" for label, mod in PAGES.items()
        }
        NAV_ICONS = ["✅", "📊", "🤖", "🎵", "💬", "👥", "👤"]

        # ...

        choice_label = render_sidebar_nav(
            page_paths,
            icons=["✅", "📊", "🤖", "🎵", "💬", "👥", "👤"],
            session_key="active_page",
        )
        choice = PAGES.get(choice_label, str(choice_label)).lower()

        # Use 3-column layout for cleaner modern UX
        left_col, center_col, _ = main_container.columns(
            [1, 3, 1]
        )  # omit right_col for simplicity

        with center_col:
            st.info("Select a page above to continue.")

        with left_col:
            render_status_icon()
            render_developer_tools()

    except Exception as exc:
        st.error("Failed to load validation UI")
        st.code(str(exc))


def render_developer_tools() -> None:
    """Display debugging utilities grouped in a single expander."""
    st.markdown(
        """
        <style>
        .dev-tabs [data-testid="stTab"] button {padding:0.25rem 1rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Developer Tools"):
        # Frequently used action
        if "cosmic_nexus" in globals() and "Harmonizer" in globals():
            try:
                user = safe_get_user()
                if user and st.button("Fork with Mock Config"):
                    try:
                        fork_id = cosmic_nexus.fork_universe(
                            user, {"entropy_threshold": 0.5}
                        )
                        st.success(f"Forked universe {fork_id}")
                    except Exception as exc:
                        st.error(f"Fork failed: {exc}")
                elif not user:
                    st.toast("No users available to fork")
            except Exception as exc:
                st.error(f"Database error: {exc}")
        else:
            st.toast("Fork operation unavailable", icon="⚠️")

        # Less common diagnostics
        with st.expander("Diagnostics & Logs"):
            # Universe state viewer
            if "SessionLocal" in globals() and "UniverseBranch" in globals():
                try:
                    with SessionLocal() as db:
                        records = (
                            db.query(UniverseBranch)
                            .order_by(UniverseBranch.timestamp.desc())
                            .limit(5)
                            .all()
                        )
                        if records:
                            for r in records:
                                st.write(
                                    {
                                        "id": r.id,
                                        "status": r.status,
                                        "timestamp": r.timestamp,
                                    }
                                )
                        else:
                            st.write("No forks recorded")
                except Exception as exc:
                    st.error(f"Database error: {exc}")
            else:
                st.toast("Database unavailable", icon="⚠️")

            # Run introspection audit
            hid = st.text_input("Hypothesis ID", key="audit_id")
            if st.button("Run Audit") and hid:
                if "dispatch_route" in globals() and "SessionLocal" in globals():
                    try:
                        with SessionLocal() as db:
                            with st.spinner("Working on it..."):
                                try:
                                    result = _run_async(
                                        dispatch_route(
                                            "trigger_full_audit",
                                            {"hypothesis_id": hid},
                                            db=db,
                                        )
                                    )
                                    st.json(result)
                                    st.toast("Success!")
                                except Exception as exc:
                                    st.error(f"Audit failed: {exc}")
                    except Exception as exc:
                        st.error(f"Database error: {exc}")
                elif "run_full_audit" in globals() and "SessionLocal" in globals():
                    try:
                        with SessionLocal() as db:
                            with st.spinner("Working on it..."):
                                try:
                                    result = run_full_audit(hid, db)
                                    st.json(result)
                                    st.toast("Success!")
                                except Exception as exc:
                                    st.error(f"Audit failed: {exc}")
                    except Exception as exc:
                        st.error(f"Database error: {exc}")
                else:
                    st.toast("Audit functionality unavailable", icon="⚠️")

            # Agent logs
            log_candidates = [
                Path("logchain_main.log"),
                Path("remix_logchain.log"),
                Path("transcendental_resonance.log"),
            ]
            log_path = next((p for p in log_candidates if p.exists()), None)
            searched_msg = ", ".join(p.name for p in log_candidates)
            if log_path is not None:
                try:
                    lines = log_path.read_text(errors="ignore").splitlines()[-100:]
                    st.text("\n".join(lines))
                except Exception:
                    st.toast(f"Unable to read log file {log_path.name}", icon="⚠️")
                st.caption(f"Searched: {searched_msg}")
            else:
                st.toast(f"No log file found. Searched: {searched_msg}", icon="⚠️")

            # Inject event
            with st.expander("Inject Event", expanded=False):
                event_json = st.text_area(
                    "Event JSON", value="{}", height=150, key="inject_event"
                )
                if st.button("Process Event"):
                    agent_obj = st.session_state.get("agent_instance") or globals().get(
                        "agent"
                    )
                    if agent_obj is not None:
                        try:
                            event = json.loads(event_json or "{}")
                            agent_obj.process_event(event)
                            st.success("Event processed")
                        except Exception as exc:
                            st.error(f"Event failed: {exc}")
                    else:
                        st.toast("Agent unavailable")

            # Session inspector
            if "AGENT_REGISTRY" in globals():
                st.write("Available agents:", list(AGENT_REGISTRY.keys()))
            if "cosmic_nexus" in globals():
                st.write(
                    "Sub universes:",
                    list(getattr(cosmic_nexus, "sub_universes", {}).keys()),
                )
            agent_obj = st.session_state.get("agent_instance") or globals().get("agent")
            if agent_obj is not None and "InMemoryStorage" in globals():
                try:
                    if isinstance(agent_obj.storage, InMemoryStorage):
                        st.write(
                            f"Users: {len(agent_obj.storage.users)} / Coins: {len(agent_obj.storage.coins)}"
                        )
                    else:
                        user_count = len(agent_obj.storage.get_all_users())
                        st.write(f"User count: {user_count}")
                except Exception:
                    st.toast("Inspection failed", icon="⚠️")

        # Playground for quick flows
        with st.expander("Playground"):
            flow_txt = st.text_area(
                "Agent Flow JSON", "[]", height=150, key="flow_json"
            )
            if st.button("Run Flow"):
                if "AGENT_REGISTRY" in globals():
                    try:
                        steps = json.loads(flow_txt or "[]")
                        results = []
                        for step in steps:
                            a_name = step.get("agent")
                            agent_cls = AGENT_REGISTRY.get(a_name, {}).get("class")
                            evt = step.get("event", {})
                            if agent_cls:
                                backend_fn = get_backend("dummy")
                                a = agent_cls(llm_backend=backend_fn)
                                results.append(a.process_event(evt))
                        st.json(results)
                    except Exception as exc:
                        st.error(f"Flow execution failed: {exc}")
                else:
                    st.toast("Agent registry unavailable", icon="⚠️")


def main() -> None:
    """Entry point with comprehensive error handling and modern UI."""
    ensure_pages(PAGES, PAGES_DIR)
    # Initialize database BEFORE anything else
    try:
        db_ready = ensure_database_exists()
        if not db_ready:
            st.warning("Database initialization failed. Running in fallback mode")
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        st.info("Running in fallback mode")

    # Respond to lightweight health-check probes
    try:
        params = st.query_params
    except AttributeError:
        # Fallback for older Streamlit versions
        params = st.experimental_get_query_params()

    value = params.get(HEALTH_CHECK_PARAM)

    path_info = os.environ.get("PATH_INFO", "").rstrip("/")
    if (
        value == "1"
        or (isinstance(value, list) and "1" in value)
        or path_info == f"/{HEALTH_CHECK_PARAM}"
    ):

        st.write("ok")
        st.stop()
        return

    try:
        st.set_page_config(
            page_title="superNova_2177",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
        render_top_bar()
        # Inject keyboard shortcuts for quick navigation
        st.markdown(
            """
            <script>
            document.addEventListener('keydown', function(e) {
              const tag = document.activeElement.tagName;
              if (tag === 'INPUT' || tag === 'TEXTAREA') { return; }
              const params = new URLSearchParams(window.location.search);
              if (e.key === 'N' || e.key === 'n') {
                params.set('page', 'Voting');
                window.location.search = params.toString();
              }
              if (e.key === 'V' || e.key === 'v') {
                params.set('page', 'Validation');
                window.location.search = params.toString();
              }
            });
            </script>
            """,
            unsafe_allow_html=True,
        )
        if not st.session_state.get("modern_styles_injected"):
            try:
                inject_modern_styles()
            except Exception as exc:
                logger.warning("CSS load failed: %s", exc)

        # Initialize session state
        defaults = {
            "session_start_ts": datetime.now(timezone.utc).isoformat(
                timespec="seconds"
            ),
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
        for k, v in defaults.items():
            st.session_state.setdefault(k, v)
        st.session_state.setdefault("users", [])
        st.session_state.setdefault("logs", [])

        if st.session_state.get("critical_error"):
            st.error("Application Error: " + st.session_state.get("critical_error", ""))
            if st.button("Reset Application", key="reset_app_critical"):
                st.session_state.clear()
                st.rerun()
            return

        try:
            apply_theme(st.session_state.get("theme", "light"))
        except Exception as exc:
            st.warning(f"Theme load failed: {exc}")

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

        render_topbar()  # sticky top bar

        page_paths: dict[str, str] = {}
        missing_pages: list[str] = []

        for label, slug in PAGES.items():
            candidate_files = [
                PAGES_DIR / f"{slug}.py",
                ROOT_DIR / "pages" / f"{slug}.py",
            ]
            if any(path.exists() for path in candidate_files):
                # Streamlit links expect paths like "/pages/validation.py"
                page_paths[label] = f"/pages/{slug}.py"
            else:
                missing_pages.append(label)

        if missing_pages:
            st.warning("Missing pages: " + ", ".join(missing_pages))


        # Determine page from query params and sidebar selection
        try:
            query = st.query_params
        except AttributeError:
            # Fallback for legacy versions
            query = st.experimental_get_query_params()

        param = query.get("page")
        forced_page = param[0] if isinstance(param, list) else param

        # Normalize and resolve forced page from query params to display label
        if forced_page:
            forced_slug = normalize_choice(forced_page)
            forced_page = next(
                (label for label, slug in PAGES.items() if normalize_choice(slug) == forced_slug),
                None,
            )

        # Ensure session state defaults are valid
        if st.session_state.get("sidebar_nav") not in PAGES.values():
            st.session_state["sidebar_nav"] = "validation"

        if forced_page not in PAGES:
            forced_page = None

        # Determine selected label from sidebar or fallback
        choice_label = forced_page or render_modern_sidebar(
            page_paths,
            icons=NAV_ICONS,
            session_key="active_page",
        )

        if not choice_label:
            choice_label = "Validation"

        # Normalize and extract slug for loading
        display_choice = PAGES.get(choice_label, choice_label)
        choice = normalize_choice(display_choice)

        try:
            st.query_params["page"] = display_choice
        except AttributeError:
            st.experimental_set_query_params(page=display_choice)


        # Page layout: left for tools, center for content
        left_col, center_col, _ = st.columns([1, 3, 1])

        # Sidebar functionality (left column)
        with left_col:
            render_status_icon()

            with st.expander("Environment Details"):
                secrets = get_st_secrets()
                info_text = (
                    f"DB: {secrets.get('DATABASE_URL', 'not set')} | "
                    f"ENV: {os.getenv('ENV', 'dev')} | "
                    f"Session: {st.session_state.get('session_start_ts', '')} UTC"
                )
                st.info(info_text)

            with st.expander("Application Settings"):
                demo_mode = st.radio("Mode", ["Normal", "Demo"], horizontal=True)
                theme_selector("Theme")

            with st.expander("Data Management"):
                uploaded_file = st.file_uploader("Upload JSON", type="json")
                if st.button("Run Analysis"):
                    st.success("Analysis complete!")

            with st.expander("Agent Configuration"):
                api_info = render_api_key_ui(key_prefix="devtools")
                backend_choice = api_info.get("model", "dummy")
                api_key = api_info.get("api_key", "") or ""

                if AGENT_REGISTRY:
                    agent_choice = st.selectbox(
                        "Agent",
                        sorted(AGENT_REGISTRY.keys()),
                        key="devtools_agent_select",
                    )
                else:
                    agent_choice = None
                    st.info("No agents registered")

                event_type = st.text_input("Event", value="LLM_INCOMING")
                payload_txt = st.text_area("Payload JSON", value="{}", height=100)
                run_agent_clicked = st.button("Run Agent")

            with st.expander("Simulation Tools"):
                render_simulation_stubs()

            st.divider()
            governance_view = st.toggle(
                "Governance View",
                value=st.session_state.get("governance_view", False),
            )
            st.session_state["governance_view"] = governance_view

            render_developer_tools()

        # Center content area — dynamic page loading
        with center_col:
            # Resolve page module
            # Normalize input and resolve page key
            label = normalize_choice(choice)
            page_key = PAGES.get(label, label.lower())

            if page_key:
                module_paths = [
                    f"transcendental_resonance_frontend.pages.{page_key}",
                    f"pages.{page_key}",
                ]
                try:
                    load_page_with_fallback(display_choice, module_paths)
                except Exception:
                    st.toast(f"Page not found: {display_choice}", icon="⚠️")
                    _render_fallback(display_choice)
            else:
                st.toast("Select a page above to continue.")
                _render_fallback("Validation")



            # Run agent logic if triggered
            if run_agent_clicked and "AGENT_REGISTRY" in globals():
                try:
                    payload = json.loads(payload_txt or "{}")
                except Exception as exc:
                    alert(f"Invalid payload: {exc}", "error")
                else:
                    try:
                        backend_fn = get_backend(
                            backend_choice.lower(), api_key or None
                        )
                        if backend_fn is None:
                            raise KeyError("backend")

                        agent_cls = AGENT_REGISTRY.get(agent_choice, {}).get("class")
                        if agent_cls is None:
                            raise KeyError("agent")

                        if agent_choice == "CI_PRProtectorAgent":
                            talker = backend_fn or (lambda p: p)
                            selected_agent = agent_cls(talker, llm_backend=backend_fn)
                        elif agent_choice == "MetaValidatorAgent":
                            selected_agent = agent_cls({}, llm_backend=backend_fn)
                        elif agent_choice == "GuardianInterceptorAgent":
                            selected_agent = agent_cls(llm_backend=backend_fn)
                        else:
                            selected_agent = agent_cls(llm_backend=backend_fn)

                        st.session_state["agent_instance"] = selected_agent
                        result = selected_agent.process_event(
                            {"event": event_type, "payload": payload}
                        )
                        st.session_state["agent_output"] = result
                        st.success("Agent executed")
                    except KeyError as missing:
                        if str(missing) == "'backend'":
                            st.warning("No backend available")
                        else:
                            st.warning("No agents available")
                        st.session_state["agent_output"] = None
                        _render_fallback("Agents")
                    except Exception as exc:
                        st.session_state["agent_output"] = {"error": str(exc)}
                        alert(f"Agent error: {exc}", "error")

            # Show agent output
            if st.session_state.get("agent_output") is not None:
                st.subheader("Agent Output")
                st.json(st.session_state.get("agent_output"))

            stats = {
                "runs": st.session_state.get("run_count", 0),
                "proposals": st.session_state.get("proposal_count", "N/A"),
                "success_rate": st.session_state.get("success_rate", "N/A"),
                "accuracy": st.session_state.get("accuracy", "N/A"),
            }
            render_stats_section(stats)

    except Exception as exc:
        logger.critical("Unhandled error in main: %s", exc, exc_info=True)
        st.error("Critical Application Error")
        st.code(traceback.format_exc())
        if st.button("Reset Application"):
            st.session_state.clear()
            st.rerun()


def ensure_database_exists() -> bool:
    """Ensure harmonizers table exists and insert default admin if necessary."""
    try:
        secrets = get_st_secrets()
        db_url = secrets.get("DATABASE_URL", "sqlite:///harmonizers.db")
        engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False} if "sqlite" in db_url else {},
        )
    except Exception as exc:
        logger.error("Failed to configure DB engine: %s", exc)
        return False

    try:
        with engine.begin() as conn:
            # Create table if missing
            conn.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS harmonizers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        hashed_password VARCHAR(255) NOT NULL,
                        bio TEXT,
                        profile_pic VARCHAR(255),
                        is_active BOOLEAN DEFAULT 1,
                        is_admin BOOLEAN DEFAULT 0,
                        is_genesis BOOLEAN DEFAULT 0,
                        consent_given BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_passive_aura_timestamp TIMESTAMP,
                        species VARCHAR(50) DEFAULT 'human',
                        cultural_preferences TEXT,
                        harmony_score FLOAT DEFAULT 0.0,
                        creative_spark FLOAT DEFAULT 0.0,
                        network_centrality FLOAT DEFAULT 0.0,
                        karma_score FLOAT DEFAULT 0.0,
                        engagement_streaks INTEGER DEFAULT 0
                    );
                    """
                )
            )

            # Check if any user exists
            res = conn.execute(text("SELECT COUNT(*) FROM harmonizers"))
            count = res.scalar() or 0
            if count == 0:
                conn.execute(
                    text(
                        """
                        INSERT INTO harmonizers
                            (username, email, hashed_password, bio,
                             is_active, is_admin, is_genesis, consent_given)
                        VALUES
                            ('admin', 'admin@supernova.dev', 'hashed_password_here',
                             'Default admin user for superNova_2177',
                             1, 1, 1, 1);
                        """
                    )
                )
        return True
    except (OperationalError, sqlite3.Error) as exc:
        logger.error("Database initialization failed: %s", exc)
        return False
    except Exception as exc:
        logger.error("Unexpected DB init error: %s", exc)
        return False


def safe_get_user():
    """Get the first user with proper error handling."""
    try:
        if not ensure_database_exists():
            return None
        with SessionLocal() as db:
            return db.query(Harmonizer).first()
    except Exception as exc:
        logger.warning("Failed to fetch user: %s", exc)

    users = st.session_state.get("users")
    if users:
        return users[0]
    return None


if __name__ == "__main__":
    main()
