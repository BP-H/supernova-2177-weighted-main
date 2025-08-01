# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Central UI-layout helpers.

Key helpers
-----------
main_container()            → returns the main content container
sidebar_container()         → returns the sidebar container
render_top_bar()            → sticky translucent navbar (logo · search · bell · beta · avatar)
render_sidebar_nav(...)     → vertical nav (option-menu or radio fallback)
render_title_bar(icon,txt)  → page H1 with emoji / icon
show_preview_badge(text)    → floating “Preview” badge
render_profile_card(user)   → tiny proxy around profile_card.render_profile_card
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

# ─────────────────────────────────────────  CONST / GLOBALS  ─────────────────────────────────────────
_EMOJI_FALLBACK = "🔖"
LAYOUT_CSS = """
<style>
/* glassy card utility */
.glass-card{
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.10);
  backdrop-filter:blur(14px);
  border-radius:1rem;
  padding:1rem;
}
/* generic insta-card demo class */
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

# Resolve repo roots even if utils.paths is unavailable during tests
try:
    _paths = importlib.import_module("utils.paths")
    ROOT_DIR: Path = _paths.ROOT_DIR
    PAGES_DIR: Path = _paths.PAGES_DIR
except Exception:  # pragma: no cover – tests or missing helper
    ROOT_DIR = Path(__file__).resolve().parents[1]
    PAGES_DIR = ROOT_DIR / "transcendental_resonance_frontend" / "pages"

# Optional pretty-sidebar lib
try:
    from streamlit_option_menu import option_menu

    USE_OPTION_MENU = True
except ImportError:
    USE_OPTION_MENU = False

# ─────────────────────────────────────────  BASIC CONTAINERS  ─────────────────────────────────────────
def main_container() -> st.delta_generator.DeltaGenerator:
    """Return a main content container with base layout CSS injected once."""
    if "_layout_css_injected" not in st.session_state:
        st.markdown(LAYOUT_CSS, unsafe_allow_html=True)
        st.session_state["_layout_css_injected"] = True
    return st.container()


def sidebar_container() -> st.delta_generator.DeltaGenerator:  # noqa: D401
    """The Streamlit sidebar (thin wrapper for consistency)."""
    return st.sidebar


# ─────────────────────────────────────────  PROFILE CARD PROXY  ──────────────────────────────────────
def render_profile_card(username: str, avatar_url: str) -> None:
    """Thin proxy so profile_card can temporarily use this module’s st."""
    import profile_card as _pc  # local import to avoid circular deps

    original_st = _pc.st
    _pc.st = st
    try:
        _render_profile_card(username, avatar_url)
    finally:
        _pc.st = original_st


# ─────────────────────────────────────────────  TOP BAR  ─────────────────────────────────────────────
def render_top_bar() -> None:
    """Sticky translucent top-navigation bar (mobile-friendly)."""
    if "PYTEST_CURRENT_TEST" in os.environ:  # tests stub out st.columns
        return

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
    flex:1;padding:.45rem .7rem;border-radius:8px;border:1px solid rgba(255,255,255,.25);
    background:rgba(255,255,255,.90);min-width:140px;font-size:.9rem;
}
.sn-bell{position:relative;background:none;border:none;color:#fff;font-size:1.3rem;cursor:pointer}
.sn-bell::before{font-family:"Font Awesome 6 Free";font-weight:900;content:"\\f0f3"}
.sn-bell[data-count]::after{
   content:attr(data-count);position:absolute;top:-.35rem;right:-.45rem;
   background:#ff4757;color:#fff;border-radius:999px;padding:0 .33rem;
   font-size:.62rem;line-height:1
}
</style>
""",
        unsafe_allow_html=True,
    )

    # -- layout columns ------------------------------------------------
    cols = st.columns([1, 4, 1, 2, 1])  # logo | search | bell | beta | avatar
    if len(cols) < 5:  # safety for mocked st.columns in unit tests
        return
    logo_col, search_col, bell_col, beta_col, avatar_col = cols

    # Logo
    logo_col.markdown('<i class="fa-solid fa-rocket fa-lg"></i>', unsafe_allow_html=True)

    # Search with datalist suggestions
    page_id = st.session_state.get("active_page", "global")
    key_search = f"{page_id}_search"
    query = search_col.text_input("", placeholder="Search…", key=key_search, label_visibility="collapsed")
    if query:
        recent = st.session_state.setdefault("_recent_q", [])
        if query not in recent:
            recent.append(query)
            st.session_state["_recent_q"] = recent[-6:]  # keep last 6

    if (sugs := st.session_state.get("_recent_q")):
        opts = "".join(f"<option value='{s}'></option>" for s in sugs)
        search_col.markdown(
            f"<datalist id='recent-sugs'>{opts}</datalist>"
            "<script>window.parent.document.querySelector('.sn-topbar input')?.setAttribute('list','recent-sugs');</script>",
            unsafe_allow_html=True,
        )

    # Notifications
    n_notes = len(st.session_state.get("notifications", []))
    bell_col.markdown(
        f'<button class="sn-bell" data-count="{n_notes or ""}" aria-label="Notifications"></button>',
        unsafe_allow_html=True,
    )
    with bell_col.popover("Notifications"):
        if n_notes:
            for nt in st.session_state["notifications"]:
                st.write(nt)
        else:
            st.write("No notifications")

    # Beta toggle (persists into query params)
    beta = beta_col.toggle("Beta", value=st.session_state.get("beta_mode", False))
    st.session_state["beta_mode"] = beta
    try:
        st.query_params["beta"] = "1" if beta else "0"
    except Exception:
        st.experimental_set_query_params(beta="1" if beta else "0")

    # Avatar placeholder
    avatar_col.markdown('<i class="fa-regular fa-circle-user fa-lg"></i>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)  # close .sn-topbar


# ─────────────────────────────────────────  SIDEBAR NAV  ────────────────────────────────────────────
def _render_sidebar_nav(
    page_links: Iterable[str] | Dict[str, str],
    icons: Optional[Iterable[str]] = None,
    key: Optional[str] = None,
    default: Optional[str] = None,
    session_key: str = "active_page",
) -> str:
    """Render vertical nav & return selected label (option-menu on mobile)."""
    # --- normalize {label:slug} -------------------------------------
    pairs = list(page_links.items()) if isinstance(page_links, dict) else [(None, p) for p in page_links]
    icons = list(icons or [None] * len(pairs))
    key = key or f"nav_{uuid4().hex}"

    mapping: Dict[str, str] = {}
    for (lbl, path), ico in zip(pairs, icons):
        slug = Path(path).stem.lower()
        lbl = lbl or Path(path).stem.replace("_", " ").title()
        mapping[lbl] = slug  # last wins – duplicates ignored gracefully

    # --- ensure page exists -----------------------------------------
    choices, icon_list = [], []
    for lbl, slug in mapping.items():
        exists = any((ROOT_DIR / slug).with_suffix(".py").exists() or (PAGES_DIR / slug).with_suffix(".py").exists())
        if exists:
            choices.append((lbl, slug))
            icon_list.append(icon_list.append or None)  # placeholder to align, will re-assign next
    # real icon assignment after validation
    icon_list = [ico for (_, _), ico in zip(pairs, icons) if _ in mapping]

    if not choices:  # nothing valid
        return ""

    default_lbl = default or choices[0][0]
    active_lbl = st.session_state.get(session_key, default_lbl)
    if active_lbl not in [lbl for lbl, _ in choices]:
        active_lbl = default_lbl
    idx_default = [lbl for lbl, _ in choices].index(active_lbl)

    # --- render ------------------------------------------------------
    with st.sidebar:
        st.markdown(SIDEBAR_STYLES, unsafe_allow_html=True)
        st.markdown("<div class='glass-card sidebar-nav'>", unsafe_allow_html=True)

        if hasattr(st.sidebar, "page_link"):  # native linking (Streamlit ≥v1.29)
            for (lbl, slug), ico in zip(choices, icon_list):
                st.sidebar.page_link(f"/pages/{slug}.py", label=lbl, icon=ico or _EMOJI_FALLBACK, help=lbl)
            chosen = active_lbl
        elif USE_OPTION_MENU:
            chosen = option_menu(
                menu_title="",
                options=[lbl for lbl, _ in choices],
                icons=[ico or "dot" for ico in icon_list],
                orientation="vertical",
                key=key,
                default_index=idx_default,
            )
        else:  # final fallback: radio
            radio_labels = [f"{ico or ''} {lbl}".strip() for (lbl, _), ico in zip(choices, icon_list)]
            chosen_radio = st.radio("Navigation", radio_labels, index=idx_default, key=key, label_visibility="collapsed")
            chosen = choices[radio_labels.index(chosen_radio)][0]

        st.markdown("</div>", unsafe_allow_html=True)

    st.session_state[session_key] = chosen
    return chosen


# Public alias (+ legacy compatibility)
def render_sidebar_nav(*a, **kw):  # noqa: D401
    """Wrapper so old code using render_modern_sidebar keeps working."""
    if globals().get("render_modern_sidebar") is not render_sidebar_nav:
        return globals()["render_modern_sidebar"](*a, **kw)
    return _render_sidebar_nav(*a, **kw)


render_modern_sidebar = render_sidebar_nav  # legacy alias

# ─────────────────────────────────────────  TITLE & BADGE  ──────────────────────────────────────────
def render_title_bar(icon: str, label: str) -> None:  # noqa: D401
    """Large H1 with emoji/icon."""
    st.markdown(
        f"<h1 style='display:flex;align-items:center;gap:.6rem;margin-bottom:1rem'>"
        f"<span>{icon}</span><span>{label}</span></h1>",
        unsafe_allow_html=True,
    )


def show_preview_badge(text: str = "Preview") -> None:
    """Floating  badge in upper-right corner."""
    st.markdown(
        f"<div style='position:fixed;top:1.1rem;right:1.1rem;"
        f"background:#ffc107;color:#000;padding:.28rem .6rem;border-radius:6px;"
        f"box-shadow:0 2px 6px rgba(0,0,0,.15);z-index:999'>"
        f"<i class='fa-solid fa-triangle-exclamation'></i>&nbsp;{text}</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────  EXPORTED NAMES  ─────────────────────────────────────────
__all__ = [
    "main_container",
    "sidebar_container",
    "render_sidebar_nav",
    "render_title_bar",
    "show_preview_badge",
    "render_profile_card",
    "render_top_bar",
]
