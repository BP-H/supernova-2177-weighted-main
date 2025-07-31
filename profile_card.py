"""Minimal profile card component used across pages."""

import os
import streamlit as st


def render_profile_card(username: str, avatar_url: str) -> None:
    """Render a compact profile card with an environment badge."""
    env = os.getenv("APP_ENV", "development").lower()
    badge = "🚀 Production" if env.startswith("prod") else "🧪 Development"
    st.markdown(
        f"""
        <div class='glass-card' style='display:flex;align-items:center;gap:0.5rem;'>
            <img src="{avatar_url}" alt="avatar" width="48" style="border-radius:50%;" />
            <div>
                <strong>{username}</strong><br/>
                <span style='font-size:0.85rem'>{badge}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


__all__ = ["render_profile_card"]
