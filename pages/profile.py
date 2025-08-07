# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""User profile page (safe, standalone)."""

from inspect import signature, Parameter
import streamlit as st

# --- Try to import the real profile card renderer ---
try:
    from frontend.profile_card import (
        DEFAULT_USER,
        render_profile_card as _render_profile_card,  # alias the real function
    )
except Exception:
    # Fallbacks if that module isn't available
    DEFAULT_USER = {"username": "guest", "avatar_url": "", "bio": "", "location": "", "website": ""}
    def _render_profile_card(**kwargs):
        st.info(f"[placeholder] profile for {kwargs.get('username','guest')}")

# Optional: status icon; safe no-op if missing
try:
    from status_indicator import render_status_icon
except Exception:
    def render_status_icon(*args, **kwargs):
        return

# --- Safe caller: works whether the real function wants kwargs or a dict or nothing ---
def _call_profile_card(data=None):
    merged = {**DEFAULT_USER, **(data or {})}

    # Try to understand the real function's signature
    try:
        sig = signature(_render_profile_card)
    except Exception:
        # unknown signature; try dict then no-arg
        try:
            return _render_profile_card(merged)
        except TypeError:
            return _render_profile_card()

    params = list(sig.parameters.values())
    if not params:
        # takes no args
        return _render_profile_card()

    # If first parameter is a required positional arg, assume it's a dict
    first = params[0]
    if first.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD) and first.default is Parameter.empty:
        try:
            return _render_profile_card(merged)
        except TypeError:
            pass  # fall through

    # Build kwargs for whatever names the function wants
    kwargs = {}
    for name, p in sig.parameters.items():
        if name == "self":
            continue
        if p.kind in (Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
            if name in merged:
                kwargs[name] = merged[name]

    # Prefer kwargs; fall back to dict; then no-arg
    try:
        return _render_profile_card(**kwargs)
    except TypeError:
        try:
            return _render_profile_card(merged)
        except TypeError:
            return _render_profile_card()

# --- Streamlit page ---
def main() -> None:
    st.title("superNova_2177")
    st.subheader("Profile")

    username = st.text_input("Username", st.session_state.get("profile_username", "guest"))
    st.session_state["profile_username"] = username

    demo_data = {
        "username": username,
        "avatar_url": "",                     # add URLs/fields here as you wire real data
        "bio": "This is a demo profile.",
        "location": "Earth",
        "website": "https://example.com",
    }

    try:
        _call_profile_card(demo_data)
    except Exception as e:
        st.error(f"Could not render profile card: {e}")

def render() -> None:
    main()

if __name__ == "__main__":
    main()
