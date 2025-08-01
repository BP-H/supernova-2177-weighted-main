# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""UI layout helpers and navigation components.

This module centralises small, **streamlit-only** helpers so that individual
pages stay lean while the overall look & feel remains coherent and modern.
The goal is to achieve a lightweight "LinkedIn × Instagram" vibe: glassy cards,
sleek top-bar, icon-first navigation – all while avoiding heavyweight
frameworks.

Exported helpers
----------------
* ``main_container`` – returns a styled container for primary page content.
* ``sidebar_container`` – thin wrapper around ``st.sidebar``.
* ``render_top_bar`` – translucent sticky header (logo · search · bell ·
  beta-toggle · avatar).
* ``render_sidebar_nav`` – glass-morphic vertical nav (option-menu fallback).
* ``render_title_bar`` – emoji/icon + label heading.
* ``render_profile_card`` – thin proxy around the shared profile-card util.
* ``show_preview_badge`` – overlay badge for WIP pages.
"""

from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Dict, Iterable, Optional
from uuid import uuid4

import streamlit as st
from profile_card import render_profile_card as _render_profile_card
from modern_ui_components import SIDEBAR_STYLES

# -----------------------------------------------------------------------------
# Paths – gracefully fall back if the optional utils module is absent
# -----------------------------------------------------------------------------
try:
    _paths = importlib.import_module("utils.paths")
    ROOT_DIR: Path = _paths.ROOT_DIR  # type: ignore[attr-defined]
    PAGES_DIR: Path = _paths.PAGES_DIR  # type: ignore[attr-defined]
except Exception:  # pragma: no cover – optional dependency
    ROOT_DIR = Path(__file__).resolve().parents[1]
    PAGES_DIR = ROOT_DIR / "transcendental_resonance_frontend" / "pages"

# -----------------------------------------------------------------------------
# Third-party optional helpers (we fail gracefully if absent)
# -----------------------------------------------------------------------------
try:
    from streamlit_option_menu import option_menu  # type: ignore

    USE_OPTION_MENU = True
except ImportError:  # pragma: no cover – optional dependency
    option_menu = None  # type: ignore
    USE_OPTION_MENU = False

# -----------------------------------------------------------------------------
# Re-usable CSS snippets
# -----------------------------------------------------------------------------
LAYOUT_CSS = """
<style>
:root {
  /* these are set globally by modern_ui / theme.py – but we redeclare fallbacks */
  --bg: #001e26;
  --card: #002b36;
  --accent: #00f0ff;
  --radius: 0.75rem;
  --transition: 0.25s ease;
}

html, body {
  scroll-behavior: smooth;
}

/* Generic glass card */
.glass-card {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: var(--radius);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  transition: box-shadow var(--transition), transform var(--transition);
}
.glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(0,0,0,0.25);
}

/* Instagram-like media card */
.insta-card {
  display: flex;
  flex-direction: column;
  background: var(--card);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.12);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.insta-card img { width: 100%; height: auto; }
.insta-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 22px rgba(0,0,0,0.18);
}

/* Sidebar nav tweaks */
.sidebar-nav a:hover { filter: brightness(1.2); }
</style>
"""

# -----------------------------------------------------------------------------
# Public helpers
# -----------------------------------------------------------------------------

def main_container() -> st.delta_generator.DeltaGenerator:  # noqa: D401 – we want a short description
    """Return the standard page container and inject global CSS once."""
    if not st.session_state.get("_layout_css_injected"):
        st.markdown(LAYOUT_CSS, unsafe_allow_html=True)
        st.session_state["_layout_css_injected"] = True
    return st.container()


def sidebar_container() -> st.delta_generator.DeltaGenerator:
    """Shorthand alias for ``st.sidebar`` (symmetry with *main_container*)."""
    return st.sidebar


# -----------------------------------------------------------------------------
# Profile card proxy (avoids circular streamlit import clashes)
# -----------------------------------------------------------------------------

def render_profile_card(username: str, avatar_url: str) -> None:
    """Render the shared profile card, temporarily monkey-patching *st*."""
    import profile_card  # local import to avoid optional dep on import

    original = profile_card.st
    profile_card.st = st  # type: ignore[assignment]
    try:
        _render_profile_card(username, avatar_url)
    finally:
        profile_card.st = original  # type: ignore[assignment]


# -----------------------------------------------------------------------------
# Top bar (sticky, translucent, minimal)
# -----------------------------------------------------------------------------

def render_top_bar() -> None:
    """Glassy top bar with search, notifications and beta toggle."""
    if "PYTEST_CURRENT_TEST" in os.environ:
        return  # skip during unit tests

    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
        <style>
        .sn-topbar{
            position:sticky; top:0; z-index:1020;
            display:flex; align-items:center; gap:1rem;
            padding:.5rem 1rem; background:rgba(20,20,20,.55);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        @media(max-width:600px){ .sn-topbar{flex-direction:column; align-items:stretch;} }
        .sn-topbar input{
            flex:1 1 auto; padding:.35rem .6rem; border-radius:var(--radius);
            border:1px solid rgba(255,255,255,.2); background:rgba(255,255,255,.9);
        }
        .sn-bell{ position:relative; background:transparent; border:none; cursor:pointer; font-size:1.25rem; color:#fff; }
        .sn-bell::before{ font-family:"Font Awesome 6 Free"; font-weight:900; content:"\f0f3"; }
        .sn-bell[data-count]::after{
            content:attr(data-count); position:absolute; top:-.35rem; right:-.45rem;
            background:crimson; color:#fff; border-radius:50%; padding:0 .3rem;
            font-size:.55rem; line-height:1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -------------------- layout columns --------------------
    with st.container():
        st.markdown("<div class='sn-topbar'>", unsafe_allow_html=True)
        cols = st.columns([1, 4, 1, 2, 1])  # logo · search · bell · beta · avatar
        if len(cols) < 5:
            st.markdown("</div>", unsafe_allow_html=True)
            return

        logo_col, search_col, bell_col, beta_col, avatar_col = cols

        # Logo (could be an SVG later)
        logo_col.markdown("<i class='fa-solid fa-user-astronaut fa-lg'></i>", unsafe_allow_html=True)

        # Search field with simple recent-query suggestions
        page_id = st.session_state.get("active_page", "global")
        search_key = f"{page_id}_search"
        query = search_col.text_input("search", placeholder="Search…", key=search_key, label_visibility="collapsed")
        if query:
            hist = st.session_state.setdefault("recent_searches", [])
            if query not in hist:
                hist.append(query)
                st.session_state["recent_searches"] = hist[-6:]

        if (suggest := st.session_state.get("recent_searches")):
            datalist = "".join(f"<option value='{s}'></option>" for s in suggest)
            search_col.markdown(
                f"<datalist id='recent-searches'>{datalist}</datalist><script>const i=document.querySelector('.sn-topbar input');if(i)i.setAttribute('list','recent-searches');</script>",
                unsafe_allow_html=True,
            )

        # Notifications bell
        notif_cnt = len(st.session_state.get("notifications", []))
        bell_col.markdown(
            f"<button class='sn-bell' data-count='{notif_cnt if notif_cnt else ''}'></button>",
            unsafe_allow_html=True,
        )
        with bell_col.popover("Notifications"):
            notes = st.session_state.get("notifications", [])
            if not notes:
                st.write("No notifications ✨")
            for n in notes:
                st.write(n)

        # Beta toggle
        beta = beta_col.toggle("β Beta", value=st.session_state.get("beta_mode", False))
        st.session_state["beta_mode"] = beta

        # Avatar placeholder (would switch to profile pic)
        avatar_col.markdown("<i class='fa-solid fa-circle-user fa-lg'></i>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Sidebar navigation
# -----------------------------------------------------------------------------

def _render_sidebar_nav(
    page_links: Iterable[str] | Dict[str, str],
    icons: Optional[Iterable[str]] = None,
    key: Optional[str] = None,
    default: Optional[str] = None,
    session_key: str = "active_page",
) -> str:
    """Render a vertical nav and return the selected label."""

    # 1. Normalise {label: slug}
    pairs = (
        list(page_links.items()) if isinstance(page_links, dict) else [(None, str(p)) for p in page_links]
    )
    icons = list(icons or [None] * len(pairs))
    mapping: Dict[str, str] = {}
    for (label, path), ico in zip(pairs, icons):
        slug = Path(path).stem.lower()
        if slug in mapping.values():
            continue
        mapping[label or slug.replace("_", " ").title()] = slug

    # 2. Filter out non-existent pages, warn user
    valid: list[tuple[str, str]] = []
    valid_icons: list[Optional[str]] = []
    for (label, slug), ico in zip(mapping.items(), icons):
        candidates = [ROOT_DIR / slug, PAGES_DIR / slug]
        if any((c.with_suffix(".py").exists() for c in candidates)):
            valid.append((label, slug))
            valid_icons.append(ico)
        else:
            st.sidebar.error(f"Page not found: {slug}")

    if not valid:
        return ""

    valid.sort(key=lambda p: p[0].lower())
    labels = [l for l, _ in valid]
    slugs = [s for _, s in valid]
    valid_icons = valid_icons[: len(valid)]

    key = key or uuid4().hex
    active_label = st.session_state.get(session_key, default or labels[0])
    if active_label not in labels:
        active_label = labels[0]
    default_idx = labels.index(active_label)

    with st.sidebar.container():
        st.markdown(SIDEBAR_STYLES, unsafe_allow_html=True)
        st.markdown("<div class='glass-card sidebar-nav'>", unsafe_allow_html=True)

        if hasattr(st.sidebar, "page_link"):
            for lbl, slug, ico in zip(labels, slugs, valid_icons):
                st.sidebar.page_link(f"/pages/{slug}.py", label=lbl, icon=ico or "circle")
            choice = active_label  # page_link handles nav behind the scenes
        elif USE_OPTION_MENU and option_menu:
            choice = option_menu(
                menu_title="Navigation",
                options=labels,
                icons=[ico or "dot" for ico in valid_icons],
                orientation="vertical",
                key=key,
                default_index=default_idx,
            )
        else:
            decorated = [f"{ico or ''} {lbl}".strip() for lbl, ico in zip(labels, valid_icons)]
            selected = st.radio("Navigation", decorated, index=default_idx, key=key, label_visibility="collapsed")
            choice = labels[decorated.index(selected)]

        st.markdown("</div>", unsafe_allow_html=True)

    st.session_state[session_key] = choice
    return choice


def render_sidebar_nav(*args, **kwargs):  # noqa: D401 – keep legacy name
    """Public wrapper (keeps older modules functional)."""
    if globals().get("render_modern_sidebar") is not render_sidebar_nav:
        # someone monkey-patched the legacy alias – defer to that
        return globals()["render_modern_sidebar"](*args, **kwargs)
    return _render_sidebar_nav(*args, **kwargs)

# maintain older alias
render_modern_sidebar = render_sidebar_nav


# -----------------------------------------------------------------------------
# Misc helpers
# -----------------------------------------------------------------------------

def render_title_bar(icon: str, label: str) -> None:
    """Large heading with icon/emoji and subtle fade-in."""
    st.markdown(
        f"""
        <h1 style='display:flex; gap:.5rem; align-items:center;' class='fade-in'>
            <span>{icon}</span>
            <span>{label}</span>
        </h1>
        """,
        unsafe_allow_html=True,
    )


def show_preview_badge(text: str = "Preview") -> None:
    """Fixed corner badge signalling WIP / fallback mode."""
    st.markdown(
        f"""
        <div style='position:fixed; top:1rem; right:1rem; background:#ffc107; color:#000;
                    padding:0.35rem 0.6rem; border-radius:6px; font-weight:600; z-index:1040;'
             class='fade-in'>
             <i class='fa-solid fa-triangle-exclamation' style='margin-right:.4rem'></i>{text}
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Re-export list
# -----------------------------------------------------------------------------
__all__ = [
    "main_container",
    "sidebar_container",
    "render_sidebar_nav",
    "render_title_bar",
    "show_preview_badge",
    "render_profile_card",
    "render_top_bar",
]
