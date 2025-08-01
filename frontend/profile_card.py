# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""LinkedIn-style profile card component (mobile-first).

Usage
-----
from frontend.profile_card import render_profile_card
render_profile_card(
    username="alice",
    avatar_url="https://robohash.org/alice.png",
    tagline="Senior Cloud Whisperer @ Nebulae Inc.",
    stats={"Followers": 420, "Following": 128, "Posts": 37},
    actions=["Follow", "Message"],
)
"""

from __future__ import annotations

import streamlit as st

_CSS_KEY = "_profile_card_css_injected"

_BASE_CSS = """
<style id="profile-card-css">
/* ---------- Glassy wrapper ---------- */
.pc-wrapper{
  display:flex;flex-direction:column;align-items:center;
  background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.15);
  backdrop-filter:blur(14px) saturate(160%);
  border-radius:1.2rem;
  overflow:hidden;
  padding-bottom:1rem;
  width:100%;
  max-width:360px;
  margin-inline:auto;
  animation:fade-in .35s ease forwards;
}
@keyframes fade-in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

.pc-banner{
  width:100%;height:84px;
  background:linear-gradient(120deg,#0a84ff 0%,#00f0ff 100%);
}
.pc-avatar{
  width:88px;height:88px;border-radius:50%;object-fit:cover;
  border:4px solid var(--card,#001E26);
  margin-top:-46px;
  background:#e5e5e5;
}
.pc-name{font-size:1.15rem;font-weight:600;margin:.4rem 0 .1rem}
.pc-tagline{font-size:.85rem;color:var(--text-muted,#7e9aaa);text-align:center;margin:0 .75rem .6rem}

.pc-stats{display:flex;gap:1.5rem;margin:.4rem 0 .8rem}
.pc-stats div{text-align:center}
.pc-stats .num{font-weight:600;font-size:.95rem}
.pc-stats .lbl{font-size:.75rem;color:var(--text-muted,#7e9aaa)}

.pc-actions{display:flex;gap:.6rem;flex-wrap:wrap;justify-content:center}
.pc-btn{
  flex:1 1 120px;
  padding:.45rem .8rem;border-radius:.65rem;border:none;
  background:rgba(255,255,255,.08);color:#fff;font-size:.85rem;
  cursor:pointer;transition:background .2s ease;
}
.pc-btn:hover{background:rgba(255,255,255,.18)}
@media(max-width:400px){.pc-wrapper{max-width:100%}}
</style>
"""


def _inject_css() -> None:
    if not st.session_state.get(_CSS_KEY):
        st.markdown(_BASE_CSS, unsafe_allow_html=True)
        st.session_state[_CSS_KEY] = True


# ─────────────────────────────────────────────────────────────────────────────
def render_profile_card(
    *,
    username: str,
    avatar_url: str,
    tagline: str | None = None,
    stats: dict[str, int] | None = None,
    actions: list[str] | None = None,
) -> None:
    """Render a responsive profile card.

    Parameters
    ----------
    username : str
        Display name on the card.
    avatar_url : str
        Square avatar image URL.
    tagline : str, optional
        Short descriptive subtitle (role, company, etc.).
    stats : dict[str,int], optional
        KPI counters, e.g. {"Followers": 123,"Following":98}.
        Up to 3 are shown; extra keys are ignored.
    actions : list[str], optional
        Button labels (text only). Buttons return True when clicked.
    """
    _inject_css()

    stats = stats or {"Followers": 0, "Following": 0}
    actions = actions or []

    with st.container():
        st.markdown('<div class="pc-wrapper">', unsafe_allow_html=True)

        # banner & avatar
        st.markdown('<div class="pc-banner"></div>', unsafe_allow_html=True)
        st.markdown(f'<img class="pc-avatar" src="{avatar_url}">', unsafe_allow_html=True)

        # name / tagline
        st.markdown(f'<div class="pc-name">{username}</div>', unsafe_allow_html=True)
        if tagline:
            st.markdown(f'<div class="pc-tagline">{tagline}</div>', unsafe_allow_html=True)

        # stats
        st.markdown('<div class="pc-stats">', unsafe_allow_html=True)
        for (label, value) in list(stats.items())[:3]:
            st.markdown(
                f'<div><div class="num">{value}</div><div class="lbl">{label}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # buttons
        if actions:
            st.markdown('<div class="pc-actions">', unsafe_allow_html=True)
            cols = st.columns(len(actions), gap="small")
            for col, label in zip(cols, actions):
                with col:
                    st.button(label, key=f"{username}_{label}_btn", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


__all__ = ["render_profile_card"]
