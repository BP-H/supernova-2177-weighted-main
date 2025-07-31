# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""User identity hub with profile and activity overview."""

import streamlit as st
from frontend.light_theme import inject_light_theme
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container, header, theme_selector, get_active_user
from api_key_input import render_api_key_ui
from social_tabs import _load_profile
from transcendental_resonance_frontend.ui.profile_card import (
    DEFAULT_USER,
    render_profile_card,
)
from status_indicator import render_status_icon
from feed_renderer import render_mock_feed, DEMO_POSTS


try:
    from social_tabs import _load_profile
    from frontend_bridge import dispatch_route
except Exception:  # pragma: no cover - optional dependencies
    _load_profile = None  # type: ignore
    dispatch_route = None  # type: ignore

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

inject_light_theme()
inject_modern_styles()
ensure_active_user()


def _render_profile(username: str) -> None:
    data = {**DEFAULT_USER, "username": username}
    if _load_profile is None:
        st.error("Profile services unavailable")
    else:
        try:
            user, followers, following = _load_profile(username)
            data = {
                **user,
                "followers": len(followers.get("followers", [])),
                "following": len(following.get("following", [])),
            }
        except Exception as exc:  # pragma: no cover - runtime fetch may fail
            st.warning(f"Profile fetch failed: {exc}, using placeholder")
    render_profile_card(data)
    if dispatch_route is not None and st.button("Follow/Unfollow", key="follow"):
        with st.spinner("Updating..."):
            try:
                dispatch_route("follow_user", {"username": username})
                st.success("Updated")
            except Exception as exc:
                st.error(f"Failed: {exc}")
    if st.button("Message", key="dm"):
        st.switch_page("pages/messages.py")
    if st.button("Video Chat", key="vc"):
        st.switch_page("pages/video_chat.py")


def main(main_container=None) -> None:
    if main_container is None:
        main_container = st
    theme_selector("Theme", key_suffix="profile")

    st.session_state.setdefault("active_user", "guest")
    container_ctx = safe_container(main_container)
    with container_ctx:
        if "active_user" not in st.session_state:
            st.session_state["active_user"] = "guest"
        # Header with status icon
        header_col, status_col = st.columns([8, 1])
        with header_col:
            header("👤 Profile")
        with status_col:
            render_status_icon()

        # Active user editable section
        current = st.session_state.get("active_user", "guest")
        current = st.text_input("Username", value=current, key="profile_user")
        st.session_state["active_user"] = current
        _render_profile(current)

        # Divider + API Keys
        st.divider()
        st.info("Manage API credentials for advanced features.")
        render_api_key_ui(key_prefix="profile")

        # Divider + external profile lookup
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
                    **DEFAULT_USER,
                    "username": username,
                }
                st.session_state["profile_followers"] = {"count": 0, "followers": []}
                st.session_state["profile_following"] = {"count": 0, "following": []}

        # Display fallback/default profile
        data = st.session_state.get(
            "profile_data",
            {**DEFAULT_USER, "username": username},
        )
        render_profile_card(data)




def render() -> None:
    main()


if __name__ == "__main__":
    main()
