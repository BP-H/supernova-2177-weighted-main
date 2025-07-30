# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Modern UI helpers for Streamlit pages."""

import streamlit as st
import logging
from frontend import theme

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    from streamlit_lottie import st_lottie
    HAS_LOTTIE = True
except Exception:  # pragma: no cover - graceful fallback
    st_lottie = None  # type: ignore
    HAS_LOTTIE = False


def render_lottie_animation(url: str, *, height: int = 200, fallback: str = "🚀") -> None:
    """Display a Lottie animation if available, otherwise show a fallback icon."""
    if HAS_LOTTIE and st_lottie is not None:
        st_lottie(url, height=height)
    else:
        st.markdown(f"<div style='font-size:{height // 4}px'>{fallback}</div>", unsafe_allow_html=True)


logger = logging.getLogger("modern_ui")

def inject_modern_styles() -> None:
    """Inject global CSS for a sleek dark appearance.

    Call this before rendering any UI elements so the styles apply correctly.
    """
    from modern_ui_components import SIDEBAR_STYLES
    from frontend.theme import get_global_css

    if st.session_state.get("modern_styles_injected"):
        logger.debug("Modern styles already injected; skipping")
        return

    st.markdown(get_global_css(True), unsafe_allow_html=True)

    css = """
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
        :root {
            --neon-accent: #00e6ff;
            --bg-start: #0f0c29;
            --bg-end: #302b63;
            --text-color: #f0f4f8;
        }
        body, .stApp {
            background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
            color: var(--text-color);
            font-family: 'Inter', sans-serif;
        }
        .main .block-container {
            padding: 2rem 3rem;
            max-width: 1200px;
        }
        .custom-container,
        .card {
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
            backdrop-filter: blur(8px);

            margin-bottom: 1rem;
            background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            transition: box-shadow 0.3s ease, transform 0.3s ease;
        }
        .card:hover,
        .custom-container:hover {
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
            transform: translateY(-3px);


        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            line-height: 1.3;
            margin: 0 0 0.5rem 0;
        }
        h1 { font-size: clamp(1.8rem, 5vw, 2.4rem); }
        h2 { font-size: clamp(1.5rem, 4vw, 2rem); }
        h3 { font-size: clamp(1.25rem, 3vw, 1.6rem); }
        h4 { font-size: clamp(1.1rem, 2.5vw, 1.3rem); }
        h5 { font-size: clamp(1rem, 2vw, 1.1rem); }
        h6 { font-size: clamp(0.875rem, 1.5vw, 1rem); }
        }
        p, span, div {
            line-height: 1.6;
            font-family: 'Inter', sans-serif;
            margin-bottom: 0.75rem;
        }
        .gradient-btn,
        .stButton > button {
            background: linear-gradient(90deg, var(--neon-accent), #00ffff) !important;
            border: none !important;
            border-radius: 10px !important;
            color: #00111e !important;
            font-weight: 600 !important;
            padding: 0.75rem 2rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.4) !important;
            font-size: 0.95rem !important;
            height: auto !important;
        }
        .gradient-btn:hover,
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(0, 255, 255, 0.6) !important;
            background: linear-gradient(90deg, #00ffff, var(--neon-accent)) !important;
            filter: brightness(1.05);
        }
 
        .stButton>button {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            backdrop-filter: blur(8px) !important;
            border-radius: 12px !important;
            color: var(--text-color) !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.4rem !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
            transition: all 0.2s ease !important;
            font-size: 0.9rem !important;
        }
        .stButton>button:hover {
            box-shadow: 0 4px 10px rgba(0,0,0,0.4) !important, 0 0 6px var(--neon-accent) !important;
            background: rgba(255,255,255,0.08) !important;
            transform: translateY(-1px) scale(1.03) !important;
        }

        input, textarea, select {
            background-color: #1a1a1a !important;
            color: #eee !important;
            border: 1px solid #444 !important;
            border-radius: 8px !important;
        }

        .stButton>button:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.4),0 0 6px var(--neon-accent);
            transform: translateY(-2px) scale(1.03);
        }
        .custom-container, .card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(8px);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            transition: box-shadow 0.3s, transform 0.3s;
        }
        .custom-container:hover, .card:hover {
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            transform: translateY(-3px);
        }


        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }

        @media (max-width: 480px) {
            .main .block-container {
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            .stButton>button {
                width: 100%;
            }
        }

        """
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(SIDEBAR_STYLES, unsafe_allow_html=True)
    st.session_state["modern_styles_injected"] = True


def inject_premium_styles() -> None:
    """Backward compatible alias for :func:`inject_modern_styles`."""
    inject_modern_styles()


def render_modern_header() -> None:
    """Render the premium glassy header."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(24, 24, 24, 0.95), rgba(36, 36, 36, 0.95));
            backdrop-filter: blur(20px);
            padding: 1.5rem 2rem;
            margin: -2rem -3rem 3rem -3rem;
            border-bottom: 1px solid rgba(74, 144, 226, 0.2);
            border-radius: 0 0 16px 16px;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="
                        background: linear-gradient(135deg, #4a90e2, #5ba0f2);
                        border-radius: 12px;
                        padding: 0.75rem;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        <span style="font-size: 1.5rem;">🚀</span>
                    </div>
                    <div>
                        <h1 style="margin: 0; color: #ffffff; font-size: 1.75rem; font-weight: 700;">
                            superNova_2177
                        </h1>
                        <p style="margin: 0; color: #888; font-size: 0.9rem;">Validation Analyzer</p>
                    </div>
                </div>
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <div style="
                        background: rgba(74, 144, 226, 0.1);
                        border: 1px solid rgba(74, 144, 226, 0.3);
                        border-radius: 8px;
                        padding: 0.5rem 1rem;
                        color: #4a90e2;
                        font-size: 0.85rem;
                        font-weight: 500;
                    ">
                        ✓ Online
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_validation_card() -> None:
    """Render the main validation card container."""
    st.markdown(
        """
        <div style="
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 12px 40px rgba(0,0,0,0.3)'"
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
    """,
        unsafe_allow_html=True,
    )

def render_stats_section() -> None:
    """Display quick stats using a responsive flexbox layout."""

    accent = theme.get_accent_color()

    st.markdown(
        f"""
        <style>
        .stats-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: space-between;
        }}
        .stats-card {{
            flex: 1 1 calc(25% - 1rem);
            min-width: 120px;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            transition: transform 0.3s ease;
        }}
        .stats-card:hover {{
            transform: scale(1.02);
        }}
        .stats-value {{
            color: {accent};
            font-size: calc(1.5rem + 0.3vw);
            font-weight: 700;
            margin-bottom: 0.25rem;
        }}
        .stats-label {{
            color: #888;
            font-size: calc(0.8rem + 0.2vw);
            font-weight: 500;
        }}
        @media (max-width: 768px) {{
            .stats-card {{
                flex: 1 1 calc(50% - 1rem);
            }}
        }}
        @media (max-width: 480px) {{
            .stats-card {{
                flex: 1 1 100%;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    stats = [
        ("🏃‍♂️", "Runs", "0"),
        ("📝", "Proposals", "12"),
        ("⚡", "Success Rate", "94%"),
        ("🎯", "Accuracy", "98.2%"),
    ]

    st.markdown("<div class='stats-container'>", unsafe_allow_html=True)
    for icon, label, value in stats:
        st.markdown(
            f"""
            <div class='stats-card'>
                <div style='font-size:2rem;margin-bottom:0.5rem;'>{icon}</div>
                <div class='stats-value'>{value}</div>
                <div class='stats-label'>{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def open_card_container() -> None:
    """Start a card container for custom content."""
    render_validation_card()


def close_card_container() -> None:
    """Close the validation card container div."""
    st.markdown("</div>", unsafe_allow_html=True)


__all__ = [
    "render_lottie_animation",
    "inject_modern_styles",
    "inject_premium_styles",
    "render_modern_header",
    "render_validation_card",
    "render_stats_section",
    "open_card_container",
    "close_card_container",
]
