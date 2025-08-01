# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Central UI-layout helpers.

Key helpers
-----------
main_container()            – main page container
sidebar_container()         – Streamlit sidebar wrapper
render_top_bar()            – sticky translucent navbar (logo · search · bell · beta · avatar)
render_sidebar_nav(...)     – vertical nav (option-menu or radio fallback)
render_title_bar(icon,txt)  – page H1 with emoji / icon
show_preview_badge(text)    – floating “Preview” badge
render_profile_card(user)   – proxy around profile_card.render_profile_card
"""

from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Dict, Iterable, Optional
from uuid import uuid4

import streamlit as st
from modern_ui_components import SIDEBAR_STYLES
from profile_card import render_profile_card as _render_profile_card

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════════
_EMOJI_FALLBACK = "🔖"
LAYOUT_CSS = """
<style>
.glass-card{
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.10);
  backdrop-filter:blur(14px);
  border-radius:1rem;
  padding:1rem;
}
.insta-card{
  display:flex;flex-direction:column;
  background:var(--card);
  border-radius:1rem;
  overflow:hidden;
  box-shadow:0 2px 6px rgba(0,0,0,.1);
  transition:transform .25s ease,box-shadow .25s ease;
}
.insta-card:hover{
  transform:translateY(-4px);
  box-shadow:0 8px 22px rgba(0,0,0,.18);
}
</style>
"""

# ─────────────────────────────  repo paths (fallback if utils.paths missing)
try:
    _paths = importlib.import_module("utils.paths")
    ROOT_DIR: Path = _paths.ROOT_DIR
    PAGES_DIR: Path = _paths.PAGES_DIR
except Exception:  # pragma: no cover
    ROOT_DIR = Path(__file__).resolve().parents[1]
    PAGES_DIR = ROOT_DIR / "transcendental_resonance_frontend" / "pages"

# optional pretty-sidebar package
try:
    from streamlit_option_menu import option_menu
    USE_OPTION_MENU = True
except ImportError:  # pragma: no cover
    USE_OPTION_MENU = False

# ═══════════════════════════════════════════════════════════════════════════════
# BASIC CONTAINERS
# ═══════════════════════════════════════════════════════════════════════════════
def main_container() -> st.delta_generator.DeltaGenerator:
    """Main content container (injects base CSS once)."""
    if "_layout_css_injected" not in st.session_state:
        st.markdown(LAYOUT_CSS, unsafe_allow_html=True)
        st.session_state["_layout_css_injected"] = True
    return st.container()


def sidebar_container() -> st.delta_generator.DeltaGenerator:
    """Thin wrapper around *st.sidebar* for consistency."""
    return st.sidebar


# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE CARD PROXY
# ═══════════════════════════════════════════════════════════════════════════════
def render_profile_card(username: str, avatar_url: str) -> None:
    """Call *profile_card.render_profile_card* with the current Streamlit ctx."""
    import profile_card as _pc

    original_st = _pc.st
    _pc.st = st
    try:
        _render_profile_card(username, avatar_url)
    finally:
        _pc.st = original_st


# ═══════════════════════════════════════════════════════════════════════════════
# TOP BAR (mobile-friendly)
# ═══════════════════════════════════════════════════════════════════════════════
def render_top_bar() -> None:
    if "PYTEST_CURRENT_TEST" in os.environ:  # unit-test stub safety
        return

    # inject styles & FA icons once
    st.markdown(
        """
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
.sn-topbar{
  position:sticky;top:0;inset-inline:0;z-index:1001;
  display:flex;align-items:center;gap:.75rem;
  padding:.6rem 1rem;backdrop-filter:blur(10px);
  background:rgba(18,18,18,.65);
}
@media(max-width:600px){.sn-topbar{flex-wrap:wrap}}
.sn-topbar input{
  flex:1;padding:.45rem .7rem;border-radius:8px;
  border:1px solid rgba(255,255,255,.25);min-width:140px;
  background:rgba(255,255,255,.90);font-size:.9rem;
}
.sn-bell{position:relative;background:none;border:none;font-size:1.3rem;color:#fff;cursor:pointer}
.sn-bell::before{font-family:"Font Awesome 6 Free";font-weight:900;content:"\\f0f3"}
.sn-bell[data-count]::after{
  content:attr(data-count);position:absolute;top:-.35rem;right:-.45rem;
  background:#ff4757;color:#fff;border-radius:999px;padding:0 .33rem;
  font-size:.62rem;line-height:1;
}
</style>
<div class="sn-topbar">
""",
        unsafe_allow_html=True,
    )

    # layout: logo | search | bell | beta | avatar
    cols = st.columns([1, 4, 1, 2, 1])
    if len(cols) < 5:  # mocked st.columns
        st.markdown("</div>", unsafe_allow_html=True)
        return
    logo_col, search_col, bell_col, beta_col, avatar_col = cols

    logo_col.markdown('<i class="fa-solid fa-rocket fa-lg"></i>', unsafe_allow_html=True)

    # search box with suggestions
    pid = st.session_state.get("active_page", "global")
    q_key = f"{pid}_search"
    q = search_col.text_input("", placeholder="Search…", key=q_key, label_visibility="collapsed")
    if q:
        recent = st.session_state.setdefault("_recent_q", [])
        if q not in recent:
            recent.append(q)
            st.session_state["_recent_q"] = recent[-6:]

    if (sugs := st.session_state.get("_recent_q")):
        options = "".join(f"<option value='{s}'></option>" for s in sugs)
        search_col.markdown(
            f"<datalist id='recent-sugs'>{options}</datalist>"
            "<script>window.parent.document.querySelector('.sn-topbar input')?.setAttribute('list','recent-sugs');</script>",
            unsafe_allow_html=True,
        )

    # notifications bell
    n_notes = len(st.session_state.get("notifications", []))
    bell_col.markdown(
        f'<button class="sn-bell" data-count="{n_notes or ""}" aria-label="Notifications"></button>',
        unsafe_allow_html=True,
    )
    with bell_col.popover("Notifications"):
        if n_notes:
            for note in st.session_state["notifications"]:
                st.write(note)
        else:
            st.write("No notifications")

    # beta toggle
    beta = beta_col.toggle("Beta", value=st.session_state.get("beta_mode", False))
    st.session_state["beta_mode"] = beta
    try:
        st.query_params["beta"] = "1" if beta else "0"
    except Exception:
        st.experimental_set_query_params(beta="1" if beta else "0")

    # avatar placeholder
    avatar_col.markdown('<i class="fa-regular fa-circle-user fa-lg"></i>', unsafe_allow_html=True)

    # close .sn-topbar
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAV
# ═══════════════════════════════════════════════════════════════════════════════
def _render_sidebar_nav(
    page_links: Iterable[str] | Dict[str, str],
    icons: Optional[Iterable[str]] = None,
    *,
    key: Optional[str] = None,
    default: Optional[str] = None,
    session_key: str = "active_page",
) -> str:
    """Vertical sidebar nav; returns the *label* of the chosen page."""
    raw_pairs = (
        list(page_links.items()) if isinstance(page_links, dict)
        else [(None, p) for p in page_links]
    )
    icons = list(icons or [None] * len(raw_pairs))
    key = key or f"nav_{uuid4().hex}"

    mapping: Dict[str, str] = {}
    icon_map: Dict[str, Optional[str]] = {}
    for (lbl, path), ico in zip(raw_pairs, icons):
        slug = Path(path).stem.lower()
        lbl = lbl or Path(path).stem.replace("_", " ").title()
        if lbl in mapping:  # de-dupe – keep first
            continue
        mapping[lbl] = slug
        icon_map[lbl] = ico

    # keep only pages that actually exist
    choices: list[tuple[str, str]] = []
    for lbl, slug in mapping.items():
        page_ok = any(
            (ROOT_DIR / slug).with_suffix(".py").exists()
            or (PAGES_DIR / slug).with_suffix(".py").exists()
        )
        if page_ok:
            choices.append((lbl, slug))

    if not choices:
        return ""

    default_lbl = default or choices[0][0]
    active_lbl = st.session_state.get(session_key, default_lbl)
    if active_lbl not in [l for l, _ in choices]:
        active_lbl = default_lbl
    default_idx = [l for l, _ in choices].index(active_lbl)

    with st.sidebar:
        st.markdown(SIDEBAR_STYLES, unsafe_allow_html=True)
        st.markdown("<div class='glass-card sidebar-nav'>", unsafe_allow_html=True)

        # 1️⃣ native page_link if available (Streamlit 1.29+)
        if hasattr(st.sidebar, "page_link"):
            for lbl, slug in choices:
                ico = icon_map.get(lbl) or _EMOJI_FALLBACK
                st.sidebar.page_link(f"/pages/{slug}.py", label=lbl, icon=ico, help=lbl)
            chosen = active_lbl

        # 2️⃣ pretty option-menu
        elif USE_OPTION_MENU:
            chosen = option_menu(
                menu_title="",
                options=[l for l, _ in choices],
                icons=[icon_map.get(l) or "dot" for l, _ in choices],
                orientation="vertical",
                key=key,
                default_index=default_idx,
            )

        # 3️⃣ fallback radio
        else:
            radio_labels = [
                f"{icon_map.get(lbl) or ''} {lbl}".strip() for lbl, _ in choices
            ]
            picked = st.radio(
                "Navigation", radio_labels,
                index=default_idx, key=key, label_visibility="collapsed"
            )
            chosen = choices[radio_labels.index(picked)][0]

        st.markdown("</div>", unsafe_allow_html=True)

    st.session_state[session_key] = chosen
    return chosen


# public alias (+ legacy compat)
def render_sidebar_nav(*a, **kw):
    """Wrapper so legacy code using *render_modern_sidebar* keeps working."""
    if globals().get("render_modern_sidebar") is not render_sidebar_nav:
        return globals()["render_modern_sidebar"](*a, **kw)
    return _render_sidebar_nav(*a, **kw)


render_modern_sidebar = render_sidebar_nav  # legacy alias

# ═══════════════════════════════════════════════════════════════════════════════
# TITLE & BADGE
# ═══════════════════════════════════════════════════════════════════════════════
def render_title_bar(icon: str, label: str) -> None:
    """Large H1 with emoji/icon."""
    st.markdown(
        f"<h1 style='display:flex;align-items:center;gap:.6rem;margin-bottom:1rem'>"
        f"<span>{icon}</span><span>{label}</span></h1>",
        unsafe_allow_html=True,
    )


def show_preview_badge(text: str = "Preview") -> None:
    """Floating badge in the top-right corner."""
    st.markdown(
        f"<div style='position:fixed;top:1.1rem;right:1.1rem;"
        f"background:#ffc107;color:#000;padding:.28rem .6rem;border-radius:6px;"
        f"box-shadow:0 2px 6px rgba(0,0,0,.15);z-index:999'>"
        f"<i class='fa-solid fa-triangle-exclamation'></i>&nbsp;{text}</div>",
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
__all__ = [
    "main_container",
    "sidebar_container",
    "render_sidebar_nav",
    "render_title_bar",
    "show_preview_badge",
    "render_profile_card",
    "render_top_bar",
]
