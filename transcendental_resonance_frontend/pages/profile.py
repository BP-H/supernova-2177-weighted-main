# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""User identity hub with profile and activity overview."""

import streamlit as st
from modern_ui import inject_modern_styles
from streamlit_helpers import safe_container
from api_key_input import render_api_key_ui

try:
    from social_tabs import _load_profile
    from frontend_bridge import dispatch_route
except Exception:  # pragma: no cover - optional dependencies
    _load_profile = None  # type: ignore
    dispatch_route = None  # type: ignore

inject_modern_styles()


def _render_profile(username: str) -> None:
    if _load_profile is None:
        st.error("Profile services unavailable")
        return
    try:
        user, followers, following = _load_profile(username)
    except Exception as exc:
        st.error(f"Profile fetch failed: {exc}")
        return
    st.image("https://placehold.co/120x120", width=120)
    st.markdown(f"### {user.get('username', username)}")
    st.write(user.get("bio", ""))
    st.markdown(
        f"**Followers:** {len(followers.get('followers', []))}  \
        **Following:** {len(following.get('following', []))}"
    )
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
    container_ctx = safe_container(main_container)
    with container_ctx:
        st.subheader("👤 Profile")
        current = st.session_state.get("active_user", "guest")
        current = st.text_input("Username", value=current, key="profile_user")
        st.session_state["active_user"] = current
        _render_profile(current)
        st.divider()
        st.info("Manage API credentials for advanced features.")
        render_api_key_ui(key_prefix="profile")


def render() -> None:
    main()


if __name__ == "__main__":
    main()
