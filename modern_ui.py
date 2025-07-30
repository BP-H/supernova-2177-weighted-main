# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Modern UI helpers for Streamlit pages."""

import streamlit as st

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


def inject_modern_styles() -> None:
    """Inject global CSS for a sleek dark appearance."""
    st.markdown(
        """
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
        [data-testid="stSidebar"] {
            background: rgba(20,25,40,0.9);
            border-right: 1px solid rgba(255,255,255,0.1);
            transition: width 0.3s ease;
        }
        [data-testid="stSidebar"] .stButton>button {width: 100%;}
        .stButton>button {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(6px);
            border-radius: 10px;
            color: var(--text-color);
            padding: 0.6rem 1.2rem;
            transition: transform 0.2s, box-shadow 0.2s;
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
        .sidebar-nav .nav-item {
            padding:0.5rem 1rem;
            border-radius:8px;
            display:flex;
            align-items:center;
            gap:0.5rem;
            transition:background 0.2s;
        }
        .sidebar-nav .nav-item:hover {background: rgba(255,255,255,0.05);}
        .sidebar-nav .nav-item.active {background: rgba(255,255,255,0.1); color: var(--neon-accent);}
        @media (max-width:768px){.main .block-container{padding:1rem;}}
        @media (max-width:480px){.main .block-container{padding:0.5rem;} .stButton>button{width:100%;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


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
    """Display quick stats in four columns."""
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("🏃‍♂️", "Runs", "0", "#4a90e2"),
        ("📝", "Proposals", "12", "#10b981"),
        ("⚡", "Success Rate", "94%", "#f59e0b"),
        ("🎯", "Accuracy", "98.2%", "#8b5cf6"),
    ]
    for col, (icon, label, value, color) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: rgba(255, 255, 255, 0.03);
                    backdrop-filter: blur(15px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                    transition: all 0.3s ease;
                " onmouseover="this.style.transform='scale(1.02)'"
                   onmouseout="this.style.transform='scale(1)'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="color: {color}; font-size: 1.75rem; font-weight: 700; margin-bottom: 0.25rem;">
                        {value}
                    </div>
                    <div style="color: #888; font-size: 0.85rem; font-weight: 500;">
                        {label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


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
