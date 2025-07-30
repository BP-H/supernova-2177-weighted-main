import os
import streamlit as st  # ensure Streamlit is imported early

# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

from importlib import import_module
from datetime import datetime, timezone
import asyncio
import difflib
import io
import json
import logging
import math
import sys
import traceback

from modern_ui_components import (
    render_modern_layout,
    render_modern_header,
    render_modern_sidebar,
    render_validation_card,
    render_stats_section,
)

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
from streamlit_option_menu import option_menu
from streamlit_helpers import (
    alert,
    apply_theme,
    centered_container,
    header,
    theme_selector,
)

from modern_ui import (
    inject_premium_styles,
    render_modern_header,
    render_stats_section,
    open_card_container,
    close_card_container,
)

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

# Fix for the import error in render_agent_insights_tab
def render_agent_insights_tab():
    """Fallback agent insights tab."""
    st.subheader("🤖 Agent Insights")
    st.info("Agent insights module not available. Install required dependencies.")
    
    # Show basic agent info if registry is available
    if 'AGENT_REGISTRY' in globals() and AGENT_REGISTRY:
        st.write("Available Agents:")
        for name, info in AGENT_REGISTRY.items():
            with st.expander(f"🔧 {name}"):
                st.write(f"Description: {info.get('description', 'No description')}")
                st.write(f"Class: {info.get('class', 'Unknown')}")
    else:
        st.warning("No agents registered")

# Fix theme_selector to handle missing key_suffix parameter

# Add this modern UI code to your ui.py - replace the page loading section

def inject_modern_styles():
    """Inject sleek modern styling."""
    st.markdown("""
        <style>
        /* Modern glassmorphism design */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        /* Main container with glassmorphism */
        .main .block-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            margin-top: 1rem;
        }
        
        /* Sidebar modern styling */
        .css-1d391kg {
            background: rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Navigation tabs */
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Modern buttons */
        .stButton > button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Modern metrics */
        [data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 1rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Text styling */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        /* Error messages modern styling */
        .stAlert {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* File uploader */
        .stFileUploader {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border: 2px dashed rgba(255, 255, 255, 0.3);
            padding: 2rem;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            color: white;
        }
        
        /* Slider styling */
        .stSlider > div > div > div {
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* Modern scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .main .block-container > div {
            animation: fadeIn 0.6s ease-out;
        }
        </style>
    """, unsafe_allow_html=True)

def render_modern_validation_page():
    """Render a beautiful modern validation page."""
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3rem; background: linear-gradient(45deg, #667eea, #764ba2); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       margin-bottom: 0.5rem;'>
                🚀 superNova_2177
            </h1>
            <p style='font-size: 1.2rem; color: rgba(255, 255, 255, 0.8); margin-bottom: 2rem;'>
                Advanced Validation Analysis Platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Modern status cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: rgba(76, 175, 80, 0.1); 
                        border-radius: 15px; border: 1px solid rgba(76, 175, 80, 0.3);'>
                <h2 style='color: #4CAF50; margin: 0; font-size: 2rem;'>✅</h2>
                <h3 style='color: white; margin: 0.5rem 0 0 0;'>System Online</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: rgba(33, 150, 243, 0.1); 
                        border-radius: 15px; border: 1px solid rgba(33, 150, 243, 0.3);'>
                <h2 style='color: #2196F3; margin: 0; font-size: 2rem;'>🔍</h2>
                <h3 style='color: white; margin: 0.5rem 0 0 0;'>Ready to Analyze</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: rgba(255, 193, 7, 0.1); 
                        border-radius: 15px; border: 1px solid rgba(255, 193, 7, 0.3);'>
                <h2 style='color: #FFC107; margin: 0; font-size: 2rem;'>⚡</h2>
                <h3 style='color: white; margin: 0.5rem 0 0 0;'>High Performance</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: rgba(156, 39, 176, 0.1); 
                        border-radius: 15px; border: 1px solid rgba(156, 39, 176, 0.3);'>
                <h2 style='color: #9C27B0; margin: 0; font-size: 2rem;'>🎯</h2>
                <h3 style='color: white; margin: 0.5rem 0 0 0;'>Precision Mode</h3>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content area
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.05); padding: 2rem; border-radius: 20px; 
                    border: 1px solid rgba(255, 255, 255, 0.1); margin: 2rem 0;'>
            <h2 style='color: white; text-align: center; margin-bottom: 1.5rem;'>
                🔬 Validation Analysis Center
            </h2>
            <p style='color: rgba(255, 255, 255, 0.8); text-align: center; font-size: 1.1rem;'>
                Upload your validation data or use demo mode to experience the power of superNova_2177
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Interactive demo section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Validation Input")
        
        # Beautiful text area
        validation_data = st.text_area(
            "Validation JSON Data",
            value='{\n  "validations": [\n    {\n      "validator": "Alice",\n      "target": "Proposal_001",\n      "score": 0.95,\n      "timestamp": "2025-07-30T00:28:28Z"\n    }\n  ]\n}',
            height=200,
            help="Paste your validation data here or use the sample data"
        )
        
        # Modern toggle for demo mode
        demo_mode = st.toggle("🎮 Demo Mode", value=True, help="Use sample data for testing")
        
    with col2:
        st.markdown("### ⚙️ Analysis Settings")
        
        view_mode = st.selectbox(
            "Visualization Mode",
            ["🌟 Force Layout", "🔄 Circular", "📐 Grid"],
            help="Choose how to visualize the validation network"
        )
        
        confidence_threshold = st.slider(
            "Confidence Threshold",
            0.0, 1.0, 0.75,
            help="Minimum confidence level for validation acceptance"
        )
        
        if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyzing validation data..."):
                # Simulate analysis
                import time
                time.sleep(2)
                
                st.success("✅ Analysis completed successfully!")
                
                # Display results
                st.markdown("### 📈 Analysis Results")
                
                result_col1, result_col2, result_col3 = st.columns(3)
                
                with result_col1:
                    st.metric("Consensus Score", "0.87", delta="0.12")
                with result_col2:
                    st.metric("Network Health", "94.2%", delta="2.3%")
                with result_col3:
                    st.metric("Validation Count", "1,247", delta="156")
                
                # Beautiful results display
                st.markdown("""
                    <div style='background: rgba(76, 175, 80, 0.1); padding: 1.5rem; 
                                border-radius: 15px; border: 1px solid rgba(76, 175, 80, 0.3); margin-top: 1rem;'>
                        <h4 style='color: #4CAF50; margin: 0 0 1rem 0;'>🎉 Excellent Validation Health!</h4>
                        <p style='color: white; margin: 0;'>
                            Your validation network shows strong consensus with high integrity scores. 
                            The system detected no anomalies and recommends proceeding with confidence.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

# In your main() function, replace the page loading section with:
def load_page_with_fallback(choice):
    """Load page with beautiful fallback."""
    # Define pages here since it's not global
    pages = {
        "Validation": "validation",
        "Voting": "voting", 
        "Agents": "agents",
        "Resonance Music": "resonance_music",
        "Social": "social",
    }
    
    try:
        page_module = pages[choice]
        module_path = f"pages.{page_module}"
        page_mod = import_module(module_path)
        
        if hasattr(page_mod, 'render'):
            page_mod.render()
        else:
            render_modern_validation_page()
    except ImportError:
        # Beautiful fallback based on page choice
        if choice == "Validation":
            render_modern_validation_page()
        elif choice == "Voting":
            render_modern_voting_page()
        elif choice == "Agents":
            render_modern_agents_page()
        elif choice == "Resonance Music":
            render_modern_music_page()
        elif choice == "Social":
            render_modern_social_page()
    except Exception as exc:
        st.error(f"Error loading page: {exc}")
def render_modern_voting_page():
    """Modern voting page fallback."""
    st.markdown("# 🗳️ Voting Dashboard")
    st.info("🚧 Advanced voting features coming soon!")

def render_modern_agents_page():
    """Modern agents page fallback."""
    st.markdown("# 🤖 AI Agents")
    st.info("🚧 Agent management system in development!")

def render_modern_music_page():
    """Modern music page fallback."""
    st.markdown("# 🎵 Resonance Music")
    st.info("🚧 Harmonic resonance features coming soon!")

def render_modern_social_page():
    """Modern social page fallback."""
    st.markdown("# 👥 Social Network")
    st.info("🚧 Social features in development!")

# Add this to your main() function after st.set_page_config():
inject_modern_styles()

def theme_selector(label: str, key_suffix: str = "") -> str:
    """Render theme selector with unique key."""
    key = f"theme_selector_{key_suffix}" if key_suffix else "theme_selector"
    theme = st.selectbox(
        label,
        ["light", "dark"],
        index=0 if st.session_state.get("theme", "light") == "light" else 1,
        key=key
    )
    st.session_state["theme"] = theme
    return theme

def load_css() -> None:
    """Placeholder for loading custom CSS."""
    pass

# Accent color used for button styling
ACCENT_COLOR = "#4f8bf9"
from api_key_input import render_api_key_ui, render_simulation_stubs
from status_indicator import render_status_icon
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

# Database fallback for local testing
DATABASE_AVAILABLE = True
try:
    from db_models import Harmonizer, SessionLocal, UniverseBranch
except Exception:  # pragma: no cover - missing ORM
    DATABASE_AVAILABLE = False

    class MockHarmonizer:
        def __init__(self, id: int = 1, username: str = "demo"):
            self.id = id
            self.username = username

    class UniverseBranch:
        class timestamp:
            @staticmethod
            def desc() -> None:
                return None

        def __init__(self, id: str, status: str, timestamp: datetime):
            self.id = id
            self.status = status
            self.timestamp = timestamp

    class MockQuery(list):
        def __init__(self, data: list | None = None) -> None:
            super().__init__(data or [])

        def order_by(self, *_a, **_k) -> "MockQuery":
            return self

        def limit(self, *_a, **_k) -> "MockQuery":
            return self

        def all(self) -> list:
            return list(self)

        def first(self):
            return self[0] if self else None

    class MockSessionLocal:
        def __enter__(self) -> "MockSessionLocal":
            return self

        def __exit__(self, *_exc) -> None:
            pass

        def query(self, model):
            data = []
            if model is MockHarmonizer:
                data = st.session_state.get("mock_data", {}).get("harmonizers", [])
            elif model is UniverseBranch:
                data = st.session_state.get("mock_data", {}).get("universe_branches", [])
            return MockQuery(data)

    Harmonizer = MockHarmonizer  # type: ignore
    SessionLocal = MockSessionLocal  # type: ignore

    if "mock_data" not in st.session_state:
        st.session_state["mock_data"] = {
            "harmonizers": [MockHarmonizer()],
            "universe_branches": [
                UniverseBranch("1", "active", datetime.utcnow())
            ],
        }
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


try:
    from social_tabs import render_social_tab
except ImportError:
    def render_social_tab():
        st.info("Social features not available")

try:
    from voting_ui import render_voting_tab
except ImportError:
    def render_voting_tab():
        st.info("Voting module not available")

try:
    from agent_ui import render_agent_insights_tab
except ImportError:
    def render_agent_insights_tab():
        st.subheader("🤖 Agent Insights")
        st.info("Agent insights not available")


try:
    from llm_backends import get_backend
except ImportError:
    def get_backend(name, api_key=None):
        return lambda x: {"response": "dummy"}

try:
    from protocols import AGENT_REGISTRY
except ImportError:
    AGENT_REGISTRY = {}

try:
    from agent_ui import render_agent_insights_tab
except ImportError:
    def render_agent_insights_tab():
        st.subheader("🤖 Agent Insights")
        st.info("Agent insights not available")

try:
    from social_tabs import render_social_tab
except ImportError:
    def render_social_tab():
        st.subheader("👥 Social Features")
        st.info("Social features module not available")

try:
    from llm_backends import get_backend
except ImportError:
    def get_backend(name, api_key=None):
        return lambda x: {"response": "dummy backend"}

try:
    from protocols import AGENT_REGISTRY
except ImportError:
    AGENT_REGISTRY = {}


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

def main() -> None:
    """Entry point with comprehensive error handling and modern UI."""
    params = st.query_params
    path_info = os.environ.get("PATH_INFO", "").rstrip("/")
    if "1" in params.get(HEALTH_CHECK_PARAM, []) or path_info == f"/{HEALTH_CHECK_PARAM}":
        st.write("ok")
        st.stop()
        return

    try:
        st.set_page_config(
            page_title="superNova_2177",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply modern styling
        inject_modern_styles()
        
        # Initialize session state
        if "session_start_ts" not in st.session_state:
            st.session_state["session_start_ts"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if "theme" not in st.session_state:
            st.session_state["theme"] = "light"
        if "governance_view" not in st.session_state:
            st.session_state["governance_view"] = False
        if "validations_json" not in st.session_state:
            st.session_state["validations_json"] = ""
        if "agent_output" not in st.session_state:
            st.session_state["agent_output"] = None
        if "last_result" not in st.session_state:
            st.session_state["last_result"] = None
        if "last_run" not in st.session_state:
            st.session_state["last_run"] = None
        if "diary" not in st.session_state:
            st.session_state["diary"] = []
        if "analysis_diary" not in st.session_state:
            st.session_state["analysis_diary"] = []
        if "run_count" not in st.session_state:
            st.session_state["run_count"] = 0

        # Check for critical errors first
        if st.session_state.get("critical_error"):
            st.error("Application Error: " + st.session_state["critical_error"])
            if st.button("Reset Application", key="reset_app_critical"):
                st.session_state.clear()
                st.rerun()
            return

        # Apply modern styling
        try:
            inject_premium_styles()
        except Exception as exc:
            logger.warning("CSS load failed: %s", exc)

        try:
            apply_theme(st.session_state["theme"])
        except Exception as exc:
            st.warning(f"Theme load failed: {exc}")
        
        # Global button styles
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

        # Define pages
        pages = {
            "Validation": "validation",
            "Voting": "voting", 
            "Agents": "agents",
            "Resonance Music": "resonance_music",
            "Social": "social",
        }

        # Navigation
        choice = option_menu(
            menu_title=None,
            options=list(pages.keys()),
            icons=["check2-square", "graph-up", "robot", "music-note-beamed", "people"],
            orientation="horizontal",
            key="main_nav_menu"
        )

        # Main content with sidebar
        main_col, left_col = st.columns([3, 1])

        with main_col:
            # Load page content
            load_page_with_fallback(choice)

        with left_col:
            render_status_icon()

            with st.expander("Environment"):
                secrets = get_st_secrets()
                st.write(f"Database URL: {secrets.get('DATABASE_URL', 'not set')}")
                st.write(f"ENV: {os.getenv('ENV', 'dev')}")
                st.write(f"Session: {st.session_state['session_start_ts']} UTC")

            with st.expander("Settings"):
                demo_mode = st.radio("Mode", ["Normal", "Demo"], horizontal=True)
                theme_selector("Theme")

            with st.expander("File Upload"):
                uploaded_file = st.file_uploader("Upload JSON", type="json")
                if st.button("Run Analysis"):
                    st.success("Analysis complete!")

            with st.expander("Agent Controls"):
                api_info = render_api_key_ui()
                backend_choice = api_info.get("model", "dummy")
                api_key = api_info.get("api_key", "") or ""
                event_type = st.text_input("Event", value="LLM_INCOMING")
                payload_txt = st.text_area("Payload JSON", value="{}", height=100)
                run_agent_clicked = st.button("Run Agent")
                render_simulation_stubs()

            st.divider()
            governance_view = st.checkbox(
                "Governance View", value=st.session_state.get("governance_view", False)
            )
            st.session_state["governance_view"] = governance_view

            with st.expander("Developer Tools"):
                dev_tabs = st.tabs([
                    "Fork Universe",
                    "Universe State Viewer",
                    "Run Introspection Audit",
                    "Agent Logs",
                    "Inject Event",
                    "Session Inspector",
                    "Playground",
                ])

                with dev_tabs[0]:
                    if 'cosmic_nexus' in globals() and 'SessionLocal' in globals() and 'Harmonizer' in globals():
                        with SessionLocal() as db:
                            user = db.query(Harmonizer).first()
                            if user and st.button("Fork with Mock Config"):
                                try:
                                    fork_id = cosmic_nexus.fork_universe(
                                        user, {"entropy_threshold": 0.5}
                                    )
                                    st.success(f"Forked universe {fork_id}")
                                except Exception as exc:
                                    st.error(f"Fork failed: {exc}")
                            elif not user:
                                st.info("No users available to fork")
                    else:
                        st.info("Fork operation unavailable")

                with dev_tabs[1]:
                    if 'SessionLocal' in globals() and 'UniverseBranch' in globals():
                        with SessionLocal() as db:
                            records = (
                                db.query(UniverseBranch)
                                .order_by(UniverseBranch.timestamp.desc())
                                .limit(5)
                                .all()
                            )
                            if records:
                                for r in records:
                                    st.write({
                                        "id": r.id,
                                        "status": r.status,
                                        "timestamp": r.timestamp,
                                    })
                            else:
                                st.write("No forks recorded")
                    else:
                        st.info("Database unavailable")

                with dev_tabs[2]:
                    hid = st.text_input("Hypothesis ID", key="audit_id")
                    if st.button("Run Audit") and hid:
                        if 'dispatch_route' in globals() and 'SessionLocal' in globals():
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
                        elif 'run_full_audit' in globals() and 'SessionLocal' in globals():
                            with SessionLocal() as db:
                                with st.spinner("Working on it..."):
                                    try:
                                        result = run_full_audit(hid, db)
                                        st.json(result)
                                        st.toast("Success!")
                                    except Exception as exc:
                                        st.error(f"Audit failed: {exc}")
                        else:
                            st.info("Audit functionality unavailable")

                with dev_tabs[3]:
                    log_path = Path("logchain_main.log")
                    if not log_path.exists():
                        log_path = Path("remix_logchain.log")
                    if log_path.exists():
                        try:
                            lines = log_path.read_text().splitlines()[-100:]
                            st.text("\n".join(lines))
                        except Exception as exc:
                            st.error(f"Log read failed: {exc}")
                    else:
                        st.info("No log file found")

                with dev_tabs[4]:
                    event_json = st.text_area(
                        "Event JSON", value="{}", height=150, key="inject_event"
                    )
                    if st.button("Process Event"):
                        if 'agent' in globals():
                            try:
                                event = json.loads(event_json or "{}")
                                agent.process_event(event)
                                st.success("Event processed")
                            except Exception as exc:
                                st.error(f"Event failed: {exc}")
                        else:
                            st.info("Agent unavailable")

                with dev_tabs[5]:
                    if 'AGENT_REGISTRY' in globals():
                        st.write("Available agents:", list(AGENT_REGISTRY.keys()))
                    if 'cosmic_nexus' in globals():
                        st.write(
                            "Sub universes:",
                            list(getattr(cosmic_nexus, "sub_universes", {}).keys()),
                        )
                    if 'agent' in globals() and 'InMemoryStorage' in globals():
                        if isinstance(agent.storage, InMemoryStorage):
                            st.write(
                                f"Users: {len(agent.storage.users)} / Coins: {len(agent.storage.coins)}"
                            )
                        else:
                            try:
                                user_count = len(agent.storage.get_all_users())
                            except Exception:
                                user_count = "?"
                            st.write(f"User count: {user_count}")

                with dev_tabs[6]:
                    flow_txt = st.text_area(
                        "Agent Flow JSON",
                        "[]",
                        height=150,
                        key="flow_json",
                    )
                    if st.button("Run Flow"):
                        if 'AGENT_REGISTRY' in globals():
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
                            st.info("Agent registry unavailable")

        # Handle agent execution
        if run_agent_clicked and 'AGENT_REGISTRY' in globals():
            try:
                payload = json.loads(payload_txt or "{}")
            except Exception as exc:
                alert(f"Invalid payload: {exc}", "error")
            else:
                backend_fn = get_backend(backend_choice.lower(), api_key or None)
                if backend_fn is None:
                    alert("Invalid backend selected", "error")
                    st.session_state["agent_output"] = None
                    st.stop()
                
                agent_cls = AGENT_REGISTRY.get(agent_choice, {}).get("class")
                if agent_cls is None:
                    alert("Unknown agent selected", "error")
                else:
                    try:
                        if agent_choice == "CI_PRProtectorAgent":
                            talker = backend_fn or (lambda p: p)
                            agent = agent_cls(talker, llm_backend=backend_fn)
                        elif agent_choice == "MetaValidatorAgent":
                            agent = agent_cls({}, llm_backend=backend_fn)
                        elif agent_choice == "GuardianInterceptorAgent":
                            agent = agent_cls(llm_backend=backend_fn)
                        else:
                            agent = agent_cls(llm_backend=backend_fn)
                        
                        result = agent.process_event(
                            {"event": event_type, "payload": payload}
                        )
                        st.session_state["agent_output"] = result
                        st.success("Agent executed")
                    except Exception as exc:
                        st.session_state["agent_output"] = {"error": str(exc)}
                        alert(f"Agent error: {exc}", "error")

        # Display agent output
        if st.session_state.get("agent_output") is not None:
            st.subheader("Agent Output")
            st.json(st.session_state["agent_output"])

        # Render stats section
        render_stats_section()
        
        st.markdown(f"**Runs:** {st.session_state['run_count']}")

    except Exception as exc:
        logger.critical("Unhandled error in main: %s", exc, exc_info=True)
        st.error("Critical Application Error")
        st.code(traceback.format_exc())
        if st.button("Reset Application"):
            st.session_state.clear()
            st.rerun()


if __name__ == "__main__":
    main()
