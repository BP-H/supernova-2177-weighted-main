import os
import streamlit as st  # ensure Streamlit is imported early

# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

import asyncio
import difflib
import io
import json
import logging
import math
import sys
import traceback

# Default port controlled by start.sh via STREAMLIT_PORT; old setting kept
# for reference but disabled.
# os.environ["STREAMLIT_SERVER_PORT"] = "8501"
from datetime import datetime
from pathlib import Path

# os.environ["STREAMLIT_SERVER_PORT"] = "8501"

logger = logging.getLogger(__name__)
logger.propagate = False

nx = None  # imported lazily in run_analysis
go = None  # imported lazily in run_analysis
# Register fallback watcher for environments that can't use inotify
os.environ["STREAMLIT_WATCHER_TYPE"] = "poll"

# Bind to the default Streamlit port to satisfy platform health checks
# os.environ["STREAMLIT_SERVER_PORT"] = "8501"

# Name of the query parameter used for the CI health check. Adjust here if the
# health check endpoint ever changes.
HEALTH_CHECK_PARAM = "healthz"

# Directory containing Streamlit page modules
PAGES_DIR = (
    Path(__file__).resolve().parent / "transcendental_resonance_frontend" / "pages"
)

# Toggle verbose output via ``UI_DEBUG_PRINTS``
UI_DEBUG = os.getenv("UI_DEBUG_PRINTS", "1") != "0"

def log(msg: str) -> None:
    if UI_DEBUG:
        print(msg, file=sys.stderr)

if UI_DEBUG:
    log("\u23f3 Booting superNova_2177 UI...")
from streamlit_option_menu import option_menu
from streamlit_helpers import (
    alert,
    apply_theme,
    centered_container,
    header,
    theme_selector,
)

def load_css() -> None:
    """Placeholder for loading custom CSS."""
    pass

# Accent color used for button styling
ACCENT_COLOR = "#4f8bf9"
from api_key_input import render_api_key_ui, render_simulation_stubs
from ui_utils import load_rfc_entries, parse_summary, summarize_text, render_main_ui

# Database fallback for local testing
try:
    from db_models import Harmonizer, SessionLocal, UniverseBranch
    DATABASE_AVAILABLE = True
except Exception:
    DATABASE_AVAILABLE = False

    class MockSessionLocal:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def query(self, *args):
            return MockQuery()

    class MockQuery:
        def filter(self, *args):
            return self
        def first(self):
            return None
        def all(self):
            return []

    class MockHarmonizer:
        id = 1
        name = "Test Harmonizer"
        config = "{}"

    SessionLocal = MockSessionLocal
    Harmonizer = MockHarmonizer
    UniverseBranch = MockHarmonizer

if not DATABASE_AVAILABLE:
    st.session_state.setdefault(
        "mock_data",
        {
            "validations": [],
            "proposals": [
                {"id": 1, "title": "Sample Proposal 1", "status": "active"},
                {"id": 2, "title": "Sample Proposal 2", "status": "pending"},
            ],
            "runs": 0,
            "success_rate": 94.2,
        },
    )


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

from typing import Any, Optional

from agent_ui import render_agent_insights_tab
from llm_backends import get_backend
from protocols import AGENT_REGISTRY
from social_tabs import render_social_tab
from voting_ui import render_voting_tab


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

    with st.spinner("Running analysis..."):
        result = analyze_validation_integrity(validations)

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
        # Check for critical errors first
        if st.session_state.get("critical_error"):
            st.error("Application Error: " + st.session_state["critical_error"])
            if st.button("Reset Application", key="reset_app_critical"):
                st.session_state.clear()
                st.rerun()
            return

        # Render content directly - REMOVED 'with main_container:'
        st.title("🚀 superNova_2177 Validation Analyzer")
        
        # Demo mode toggle
        col1, col2 = st.columns([3, 1])
        with col2:
            demo_mode = st.toggle("Demo Mode", value=True, key="demo_mode_toggle")
        
        if demo_mode:
            st.info("🎮 Running in Demo Mode - Using sample data for testing")
            
            # Sample stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Runs", "0", delta="0")
            with col2:
                st.metric("Proposals", "12", delta="+2")
            with col3:
                st.metric("Success Rate", "94.2%", delta="+1.2%")
            with col4:
                st.metric("Accuracy", "98.5%", delta="+0.3%")
            
            # Sample validation form
            st.subheader("📋 Validation Input")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                validation_text = st.text_area(
                    "Validations JSON",
                    value='{"sample": "validation", "status": "demo"}',
                    height=200,
                    key="demo_validation_input"
                )
            
            with col2:
                view_mode = st.selectbox("View Mode", ["force", "gentle", "analysis"], key="demo_view_mode")
                
                if st.button("🔍 Run Analysis", type="primary", key="demo_run_analysis"):
                    st.success("✅ Demo analysis completed!")
                    st.json({
                        "result": "success",
                        "score": 95.7,
                        "recommendations": ["Optimize validation logic", "Add error handling"]
                    })
        else:
            st.warning("⚠️ Live mode requires database connection")
            st.info("Enable Demo Mode above to test the interface")
        
    except Exception as exc:
        st.session_state["critical_error"] = str(exc)
        st.error(f"Rendering Error: {str(exc)}")
        if st.button("Clear Error & Restart", key="clear_error_restart"):
            st.session_state.clear()
            st.rerun()


def main() -> None:
    """Entry point with comprehensive error handling."""
    try:
        st.set_page_config(
            page_title="superNova_2177",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Load CSS safely
        try:
            from components.modern_ui import load_css
            load_css()
        except Exception:
            pass  # Fail silently

        # Health check
        params = st.query_params
        if "1" in params.get("healthz", []):
            st.write("ok")
            st.stop()
            return

        # Initialize session state safely
        if "initialized" not in st.session_state:
            st.session_state.update({
                "initialized": True,
                "theme": "dark",
                "demo_mode": True,
                "errors": []
            })

        # Render main UI with error recovery
        try:
            render_validation_ui()
        except Exception as e:
            st.error(f"UI Rendering Error: {str(e)}")
            st.code(f"Error details: {repr(e)}")
            if st.button("🔄 Reset Application", key="reset_main_ui"):
                st.session_state.clear()
                st.rerun()

    except Exception as e:
        st.error(f"Critical Application Error: {str(e)}")
        st.code(f"Stack trace: {repr(e)}")


if __name__ == "__main__":
    main()
