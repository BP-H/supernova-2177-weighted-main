# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

from frontend.profile_card import render_profile_card

def main() -> None:
    # ── fetch / derive your data ──────────────────────────
    current_user  = st.session_state.get("active_user", "guest")
    avatar_url    = f"https://robohash.org/{current_user}.png?size=100x100"
    bio_or_head   = "Default user"
    follower_cnt  = get_followers(current_user)        # replace w/ real fn
    following_cnt = get_following(current_user)
    post_cnt      = get_post_count(current_user)
    is_following  = is_user_followed(current_user)     # bool

    render_profile_card(
        username=current_user,
        avatar_url=avatar_url,
        tagline=bio_or_head,
        stats={
            "Followers": follower_cnt,
            "Following": following_cnt,
            "Posts":     post_cnt,
        },
        actions=[
            "Unfollow" if is_following else "Follow",
            "Message",
        ],
    )

    # …everything else (API-credentials box, model picker, etc) …
