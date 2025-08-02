# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any

import random
import streamlit as st

from frontend.theme import set_theme
from modern_ui import apply_modern_styles

from streamlit_helpers import theme_toggle, safe_container, sanitize_text

from modern_ui_components import st_javascript
from frontend.assets import story_css, story_js, reaction_css, scroll_js

# ──────────────────────────────────────────────────────────────────────────────
# Sample data models
# ──────────────────────────────────────────────────────────────────────────────


@dataclass
class User:
    username: str
    avatar: str
    bio: str
    badges: List[str] = field(default_factory=list)


@dataclass
class Post:
    id: int
    user: User
    media: str
    caption: str
    timestamp: datetime
    reactions: Dict[str, int] = field(
        default_factory=lambda: {"❤️": 0, "🔥": 0, "👍": 0}
    )
    comments: List[Dict[str, str]] = field(default_factory=list)


# ──────────────────────────────────────────────────────────────────────────────
# Demo content generators
# ──────────────────────────────────────────────────────────────────────────────


def _sample_users() -> List[User]:
    """Return three hard-coded demo users."""
    return [
        User("alice", "https://placehold.co/48x48?text=A", "Explorer", ["🌟 super"]),
        User("bob", "https://placehold.co/48x48?text=B", "Creator", ["🥇 pro"]),
        User("carol", "https://placehold.co/48x48?text=C", "Hacker", ["💯 elite"]),
    ]


def _generate_posts(count: int, start: int = 0) -> List[Post]:
    """Generate `count` pseudo-random demo posts."""
    users = _sample_users()
    now = datetime.utcnow()
    posts: List[Post] = []
    for i in range(count):
        u = random.choice(users)
        posts.append(
            Post(
                id=start + i,
                user=u,
                media=f"https://placehold.co/600x400?text=Post+{start+i+1}",
                caption=f"demo caption {start+i+1}",
                timestamp=now - timedelta(minutes=5 * i),
            )
        )
    return posts


# ──────────────────────────────────────────────────────────────────────────────
# Rendering helpers
# ──────────────────────────────────────────────────────────────────────────────


def _render_stories(users: List[User]) -> None:
    """Render the horizontal story-strip."""
    st.markdown(story_css(), unsafe_allow_html=True)
    html = "<div class='story-strip' id='story-strip'>"
    for u in users:
        avatar = sanitize_text(u.avatar)
        username = sanitize_text(u.username)
        html += (
            f"<div class='story-item'><img src='{avatar}' width='60' alt='avatar'/><br>{username}</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    st_javascript(story_js(), key="story_carousel")


def _render_post(post: Post) -> None:
    """Render an individual post card with reactions & comments."""
    reactions = st.session_state.setdefault("reactions", {}).setdefault(
        post.id, post.reactions.copy()
    )
    comments = st.session_state.setdefault("comments", {}).setdefault(
        post.id, post.comments.copy()
    )

    with st.container():
        st.markdown("<div class='post-card'>", unsafe_allow_html=True)
        # Header
        avatar = sanitize_text(post.user.avatar)
        username = sanitize_text(post.user.username)
        st.markdown(
            f"<div class='post-header'><img src='{avatar}' alt='avatar'/>"
            f"<strong>{username}</strong> "
            f"<span>{' '.join(post.user.badges)}</span>"
            f"<span style='margin-left:auto;font-size:0.75rem;'>{post.timestamp:%H:%M}</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        # Media with alt text
        caption = sanitize_text(post.caption)
        st.image(
            post.media,
            use_container_width=True,
            output_format="JPEG",
            alt=caption,
        )
        # Caption
        st.markdown(f"<div class='post-caption'>{caption}</div>", unsafe_allow_html=True)

        # Reactions & comments
        cols = st.columns(len(reactions) + 1)
        icon_map = {"❤️": "fa-heart", "🔥": "fa-fire", "👍": "fa-thumbs-up"}
        for idx, (emoji, count) in enumerate(reactions.items()):
            btn_key = f"react_{post.id}_{emoji}"
            if cols[idx].button(str(count), key=btn_key):
                reactions[emoji] += 1
                st.session_state["reactions"][post.id] = reactions
                st.rerun()
            cols[idx].markdown(
                f"""
                <script>
                const btns = document.querySelectorAll('button[data-testid="widget-button"]');
                const btn = btns[btns.length-1];
                if(btn){{btn.id='{btn_key}';btn.classList.add('reaction-btn','fa-solid','{icon_map.get(emoji, 'fa-heart')}');
                if(!btn.querySelector('i'))btn.insertAdjacentHTML('afterbegin','<i class="fa-solid {icon_map.get(emoji, 'fa-heart')}"></i> ');}}
                </script>
                """,
                unsafe_allow_html=True,
            )

        # Pop-over for comments
        with cols[-1]:
            with st.popover("💬"):
                st.markdown("### comments")
                for c in comments:
                    user = sanitize_text(c['user'])
                    text = sanitize_text(c['text'])
                    st.write(f"**{user}**: {text}")
                new = st.text_input("Add a comment", key=f"c_{post.id}")
                if st.button("post", key=f"cbtn_{post.id}") and new:
                    comments.append({"user": "you", "text": sanitize_text(new)})
                    st.session_state["comments"][post.id] = comments

                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Page-state helpers
# ──────────────────────────────────────────────────────────────────────────────


def _init_state() -> None:
    if "posts" not in st.session_state:
        st.session_state["posts"] = _generate_posts(6)
    st.session_state.setdefault("post_offset", 3)
    if "reactions" not in st.session_state:
        st.session_state["reactions"] = {
            p.id: p.reactions.copy() for p in st.session_state["posts"]
        }
    if "comments" not in st.session_state:
        st.session_state["comments"] = {
            p.id: p.comments.copy() for p in st.session_state["posts"]
        }


def _load_more_posts() -> None:
    posts: List[Post] = st.session_state["posts"]
    offset = st.session_state["post_offset"]
    if offset < len(posts):
        st.session_state["post_offset"] += 3
        return

    start = len(posts)
    new_posts = _generate_posts(3, start=start)
    posts.extend(new_posts)
    st.session_state["post_offset"] += 3
    for p in new_posts:
        st.session_state["reactions"][p.id] = p.reactions.copy()
        st.session_state["comments"][p.id] = p.comments.copy()


# ──────────────────────────────────────────────────────────────────────────────
# Page entrypoints
# ──────────────────────────────────────────────────────────────────────────────

set_theme("light")
apply_modern_styles()


def _page_body() -> None:
    """Render the main feed inside the current container."""
    _init_state()

    theme_toggle("Dark Mode", key_suffix="feed")
    st.toggle("beta mode", key="beta_mode")

    posts: List[Post] = st.session_state["posts"]
    users = _sample_users()

    _render_stories(users)
    st.markdown(reaction_css(), unsafe_allow_html=True)

    offset = st.session_state["post_offset"]
    for p in posts[:offset]:
        _render_post(p)

    # ── Infinite scroll sentinel ───────────────────────────────────────
    st.markdown("<div id='feed-sentinel'></div>", unsafe_allow_html=True)
    triggered = st_javascript(
        """
        (() => {
          const sent = document.getElementById('feed-sentinel');
          if (!sent || window.feedObserverAttached) return false;
          window.feedObserverAttached = true;
          return new Promise(resolve => {
            const obs = new IntersectionObserver(entries => {
              if (entries[0].isIntersecting) {
                obs.disconnect();
                resolve(true);
              }
            });
            obs.observe(sent);
          });
        })();
        """,
        key="feed_observer",
    )

    if triggered:
        # load more posts when sentinel comes into view
        if offset >= len(posts):
            posts.extend(_generate_posts(3, start=len(posts)))
        st.session_state["post_offset"] += 3
        st.rerun()



def main(main_container=None) -> None:
    """Render the feed inside ``main_container`` (or root Streamlit)."""
    apply_theme("light")
    inject_modern_styles()

    container = main_container or st
    with safe_container(container):
        _page_body()


def render() -> None:
    """Wrapper for Streamlit multipage routing."""
    main()


if __name__ == "__main__":
    render()

