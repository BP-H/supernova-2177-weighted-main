# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""User identity hub with profile and activity overview."""

import asyncio
from typing import Any, Dict
import streamlit as st
from frontend.theme import apply_theme
from streamlit_helpers import (
    safe_container,
    header,
    theme_toggle,
    get_active_user,
    ensure_active_user,
    inject_global_styles,


from status_indicator import render_status_icon



try:
    from social_tabs import _load_profile
    from frontend_bridge import dispatch_route
except Exception:  # pragma: no cover - optional dependencies
    _load_profile = None  # type: ignore
    dispatch_route = None  # type: ignore

try:  # Optional DB access for follow/unfollow
    from db_models import (
        SessionLocal,
        Harmonizer,
        init_db,
        seed_default_users,
    )
except Exception:  # pragma: no cover - optional dependency
    SessionLocal = None  # type: ignore
    Harmonizer = None  # type: ignore

    def init_db() -> None:  # type: ignore
        pass

    def seed_default_users() -> None:  # type: ignore
        pass


)
from frontend.profile_card import (
    DEFAULT_USER,
    render_profile_card as _render_profile_card,  # keep this alias
)



# --- SAFE WRAPPER FOR PROFILE CARD ---
from inspect import signature, Parameter

def render_profile_card(data=None):
    """
    Calls the real profile card function no matter its signature:
    - If it takes 0 args -> call without args
    - If it takes 1 positional arg (a dict) -> pass merged dict
    - If it takes keyword-only args (e.g., username, avatar_url) -> pass **kwargs
    """
    merged = {**DEFAULT_USER, **(data or {})}

    try:
        sig = signature(_render_profile_card)
    except Exception:
        # Unknown signature; best attempt with dict, else no-arg
        try:
            return _render_profile_card(merged)
        except TypeError:
            return _render_profile_card()

    params = list(sig.parameters.values())

    # 0 parameters → just call it
    if not params:
        return _render_profile_card()

    # 1 positional parameter → likely expects a dict
    first = params[0]
    if first.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD) and first.default is Parameter.empty:
        try:
            return _render_profile_card(merged)
        except TypeError:
            pass  # fall through to kwargs path

    # Build kwargs for whatever names it wants
    kwargs = {}
    for name, p in sig.parameters.items():
        if name == "self":
            continue
        if p.kind in (Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
            if name in merged:
                kwargs[name] = merged[name]

    try:
        return _render_profile_card(**kwargs)
    except TypeError:
        # last resort
        try:
            return _render_profile_card(merged)
        except TypeError:
            return _render_profile_card()
# --- END WRAPPER ---



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


# Initialize theme & global styles once, then ensure a user is set
apply_theme("light")
inject_global_styles()
ensure_active_user()


def _render_profile(username: str) -> None:
    data = {**DEFAULT_USER, "username": username}
    followers: Dict[str, Any] = {"followers": []}
    following: Dict[str, Any] = {"following": []}
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
    # Display follower/following lists below the card
    st.markdown("**Followers**")
    st.write(followers.get("followers", []))
    st.markdown("**Following**")
    st.write(following.get("following", []))


def main(main_container=None) -> None:
    if main_container is None:
        main_container = st
    init_db()
    seed_default_users()
    theme_toggle("Dark Mode", key_suffix="profile")

    with safe_container(main_container):
        # Header with status icon
        header_col, status_col = st.columns([8, 1])
        with header_col:
            header("ðŸ‘¤ Profile")
        with status_col:
            render_status_icon()

        # Active user editable section
        current = get_active_user()
        current = st.text_input("Username", value=current, key="profile_user")
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
        followers = st.session_state.get(
            "profile_followers", {"count": 0, "followers": []}
        )
        following = st.session_state.get(
            "profile_following", {"count": 0, "following": []}
        )
        st.markdown("**Followers**")
        st.write(followers.get("followers", []))
        st.markdown("**Following**")
        st.write(following.get("following", []))


def render() -> None:
    main()


if __name__ == "__main__":
    main()
