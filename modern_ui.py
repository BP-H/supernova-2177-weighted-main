# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Modern UI helpers for Streamlit pages."""

import streamlit as st


def inject_modern_styles() -> None:
    """Inject global CSS for a sleek dark appearance."""
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        :root {
            --neon-accent: #00ffe1;
            --bg-start: #05080f;
            --bg-end: #020409;
            --text-color: #f0f4f8;

        }

        body, .stApp {
            background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
            color: var(--text-color);
            font-family: 'Inter', 'Roboto', 'Urbanist', sans-serif;
        }
        .main .block-container {
            padding-top: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1200px;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(3,6,23,0.95), rgba(10,20,40,0.95));
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        [data-testid="stSidebar"] .stButton>button {
            width: 100%;
        }
        .sidebar-nav label {
            display: flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.25rem;
            transition: background 0.2s;
        }
        .sidebar-nav label:hover {
            background: rgba(255,255,255,0.05);
        }
        .sidebar-nav input:checked + div {
            color: var(--neon-accent);
        }
        .custom-container,
        .card {
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 4px 10px rgba(0,0,0,0.35);
            backdrop-filter: blur(8px);

            margin-bottom: 1rem;
            background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            transition: box-shadow 0.3s ease, transform 0.3s ease;
        }
        .card:hover,
        .custom-container:hover {
            box-shadow: 0 4px 14px rgba(0,0,0,0.4);
            transform: translateY(-3px);

        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            line-height: 1.3 !important;
            margin: 0 0 0.5rem 0 !important;
        }
        h1 { font-size: clamp(1.8rem, 5vw, 2.4rem) !important; }
        h2 { font-size: clamp(1.5rem, 4vw, 2rem) !important; }
        h3 { font-size: clamp(1.25rem, 3vw, 1.6rem) !important; }
        h4 { font-size: clamp(1.1rem, 2.5vw, 1.3rem) !important; }
        h5 { font-size: clamp(1rem, 2vw, 1.1rem) !important; }
        h6 { font-size: clamp(0.875rem, 1.5vw, 1rem) !important; }
        }
        p, span, div {
            line-height: 1.6 !important;
            font-family: 'Inter', sans-serif !important;
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
            box-shadow: 0 4px 10px rgba(0,0,0,0.4) !important;
            background: rgba(255,255,255,0.08) !important;
            transform: translateY(-1px) !important;
        }

        input, textarea, select {
            background-color: #1a1a1a !important;
            color: #eee !important;
            border: 1px solid #444 !important;
            border-radius: 8px !important;
        }

        .sidebar-nav .nav-item {
            padding: 0.4rem 0.8rem;
            border-radius: 8px;
            margin-bottom: 0.25rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: background 0.2s;
        }

        }

        .sidebar-nav .nav-item.active {
            background: rgba(255,255,255,0.1);
            color: var(--neon-accent);
        }

        .sidebar-nav .nav-item:hover {
            background: rgba(255,255,255,0.05);
        }

        .sidebar-nav .icon {
            font-size: 1.2rem;
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
            .gradient-btn,
            .stButton > button {
                width: 100%;
            }
        }

        .profile-card {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 12px;
            padding: 0.5rem 0.75rem;
            margin-bottom: 1rem;
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            [data-testid="stSidebar"] {
                width: 14rem;
            }
        }

        }
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
    "inject_modern_styles",
    "inject_premium_styles",
    "render_modern_header",
    "render_validation_card",
    "render_stats_section",
    "open_card_container",
    "close_card_container",
]
