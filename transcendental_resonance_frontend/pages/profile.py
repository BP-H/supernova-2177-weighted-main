# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""User profile and API configuration page."""

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container
from api_key_input import render_api_key_ui

try:  # Optional social features
    from frontend_bridge import dispatch_route
except Exception:  # pragma: no cover - optional dependency
    dispatch_route = None  # type: ignore

try:  # Optional DB access for follow/unfollow
    from db_models import SessionLocal, Harmonizer
except Exception:  # pragma: no cover - optional dependency
    SessionLocal = None  # type: ignore
    Harmonizer = None  # type: ignore

import asyncio


def _run_async(coro):
    """Execute ``coro`` whether or not an event loop is running."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        return loop.run_until_complete(coro)


def _fetch_social(username: str) -> tuple[dict, dict]:
    """Return follower and following data for ``username`` via routes."""
    if dispatch_route is None or SessionLocal is None:
        return {}, {}
    with SessionLocal() as db:
        followers = _run_async(
            dispatch_route("get_followers", {"username": username}, db=db)
        )
        following = _run_async(
            dispatch_route("get_following", {"username": username}, db=db)
        )
    return followers or {}, following or {}

inject_modern_styles()


def main(main_container=None) -> None:
    """Render the user profile page."""
    if main_container is None:
        main_container = st

    container_ctx = safe_container(main_container)
    with container_ctx:
        st.subheader("👤 Profile")

        username = st.session_state.get("active_user", "demo_user")
        avatar_url = "https://placekitten.com/200/200"
        bio = "Exploring the frontiers of resonance."
        interests = ["Music", "Physics", "Art"]

        st.image(avatar_url, width=120)
        st.markdown(f"### {username}")
        st.write(bio)
        st.markdown(f"**Interests:** {', '.join(interests)}")

        followers, following = _fetch_social(username)
        st.write(f"Followers: {followers.get('count', 0)}")
        st.write(f"Following: {following.get('count', 0)}")

        cols = st.columns(3)
        follow_label = "Follow"
        if followers.get("followers") and username in followers.get("followers", []):
            follow_label = "Unfollow"

        with cols[0]:
            if st.button(follow_label, use_container_width=True):
                if dispatch_route and SessionLocal and Harmonizer:
                    with SessionLocal() as db:
                        user_obj = (
                            db.query(Harmonizer)
                            .filter(Harmonizer.username == username)
                            .first()
                        )
                        if user_obj:
                            _run_async(
                                dispatch_route(
                                    "follow_user",
                                    {"username": username},
                                    db=db,
                                    current_user=user_obj,
                                )
                            )
                            followers, following = _fetch_social(username)
                            st.experimental_rerun()
                else:
                    st.info("Follow service unavailable")

        with cols[1]:
            if st.button("Message", use_container_width=True):
                try:
                    st.switch_page("pages/messages")
                except Exception:
                    st.error("Messages page not available.")

        with cols[2]:
            if st.button("Video Chat", use_container_width=True):
                try:
                    st.switch_page("pages/video_chat")
                except Exception:
                    st.error("Video chat page not available.")

        # st.markdown("### Badges")  # Placeholder for future badge display
        # st.markdown("### Portfolio")  # Placeholder for portfolio section

        st.divider()
        st.info("Manage API credentials for advanced features.")
        render_api_key_ui(key_prefix="profile")


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()


if __name__ == "__main__":
    main()
