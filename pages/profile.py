# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Profile page — standalone + works with fake backend."""

import streamlit as st

# --- fake backend (Option C). If not present, use safe fallbacks ---
try:
    from external_services.fake_api import get_profile, save_profile  # C step
except Exception:
    def get_profile(username: str):
        return {"username": username, "avatar_url": "", "bio": "", "location": "", "website": ""}
    def save_profile(data: dict):
        return True

DEFAULT_USER = {
    "username": "guest",
    "avatar_url": "",
    "bio": "This is a demo profile.",
    "location": "Earth",
    "website": "https://example.com",
}

def render_profile_card_ui(profile: dict) -> None:
    """Local UI renderer so we never crash on imports/signatures."""
    st.markdown(f"### @{profile.get('username','guest')}")
    col1, col2 = st.columns([1, 3])
    with col1:
        url = profile.get("avatar_url") or ""
        if url:
            st.image(url, width=96)
        else:
            st.write("🧑‍🚀")
    with col2:
        st.write(profile.get("bio", ""))
        loc = profile.get("location", "")
        web = profile.get("website", "")
        if loc: st.write(f"📍 {loc}")
        if web: st.write(f"🔗 {web}")

def main():
    st.title("superNova_2177")
    st.subheader("Profile")

    # --- Username INPUT FIRST (so it's defined) ---
    username = st.text_input("Username", st.session_state.get("profile_username", "guest"))
    st.session_state["profile_username"] = username

    # --- Load from fake backend, then merge defaults ---
    loaded = get_profile(username) or {}
    profile = {**DEFAULT_USER, **loaded, "username": username}

    # --- Edit fields (simple) ---
    with st.expander("Edit", expanded=False):
        profile["avatar_url"] = st.text_input("Avatar URL", profile.get("avatar_url", ""))
        profile["bio"] = st.text_area("Bio", profile.get("bio", ""))
        profile["location"] = st.text_input("Location", profile.get("location", ""))
        profile["website"] = st.text_input("Website", profile.get("website", ""))

        if st.button("Save Profile"):
            if save_profile(profile):
                st.success("Saved (fake API, in-memory).")
            else:
                st.error("Could not save profile.")

    # --- Render the card ---
    try:
        render_profile_card_ui(profile)
    except Exception as e:
        st.error(f"Render error: {e}")

def render() -> None:
    main()

if __name__ == "__main__":
    main()
