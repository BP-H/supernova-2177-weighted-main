# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Simple sticky top bar component for Streamlit UIs."""

from __future__ import annotations

import streamlit as st


def render_topbar() -> None:
    """Render a translucent top navigation bar."""
    st.markdown(
        """
        <style>
        .sn-topbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.5rem 1rem;
            background: rgba(30, 30, 30, 0.6);
            backdrop-filter: blur(8px);
        }
        .sn-topbar input {
            flex: 1;
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.85);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="sn-topbar">
            <img src="https://placehold.co/32x32?text=SN" width="32" />
            <input type="text" placeholder="Search..." />
            <img src="https://placehold.co/32x32" width="32" style="border-radius:50%" />
        </div>
        """,
        unsafe_allow_html=True,
    )

__all__ = ["render_topbar"]
