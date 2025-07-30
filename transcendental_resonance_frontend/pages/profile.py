# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""User profile and API configuration page."""

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container
from api_key_input import render_api_key_ui
from social_tabs import _load_profile

inject_modern_styles()


def main(main_container=None) -> None:
    """Render the user profile page."""
    if main_container is None:
        main_container = st

    container_ctx = safe_container(main_container)
    with container_ctx:
        st.subheader("👤 Profile")
        st.info("Manage API credentials for advanced features.")
        render_api_key_ui(key_prefix="profile")

        st.divider()
        username = st.text_input(
            "View Profile",
            value=st.session_state.get("profile_username", "demo_user"),
            key="profile_username",
        )
        if st.button("Load Profile", key="load_profile"):
            try:
                user, followers, following = _load_profile(username)
                st.session_state["profile_data"] = user
                st.session_state["profile_followers"] = followers
                st.session_state["profile_following"] = following
            except Exception:
                st.warning("Profile data unavailable, using placeholder")
                st.session_state["profile_data"] = {
                    "username": username,
                    "bio": "Exploring the cosmos.",
                    "avatar": "https://placehold.co/100",
                    "interests": ["science", "art"],
                }
                st.session_state["profile_followers"] = {"count": 0, "followers": []}
                st.session_state["profile_following"] = {"count": 0, "following": []}

        data = st.session_state.get(
            "profile_data",
            {
                "username": username,
                "bio": "Exploring the cosmos.",
                "avatar": "https://placehold.co/100",
                "interests": ["science", "art"],
            },
        )
        st.image(data.get("avatar", "https://placehold.co/100"), width=100)
        st.write(f"**{data.get('username', username)}**")
        st.write(data.get("bio", ""))
        st.write(
            "Interests:",
            ", ".join(data.get("interests", [])),
        )

        cols = st.columns(3)
        with cols[0]:
            st.button("Follow", key="follow_btn")
        with cols[1]:
            st.button("Message", key="dm_btn")
        with cols[2]:
            st.button("Video Chat", key="video_btn")

        st.markdown("**Badges**: *(coming soon)*")
        st.markdown("**Portfolio**: *(coming soon)*")


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()


if __name__ == "__main__":
    main()
