# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""UI Layout Helpers

Reusable Streamlit layout helpers and navigation components for pages.

These functions are lightweight and centralized for easy reuse across modules
without introducing heavy dependencies.

Features:
- `main_container()` – returns a generic container for page content
- `sidebar_container()` – accesses the sidebar container
- `render_sidebar_nav(pages)` – vertical sidebar navigation
- `render_title_bar(icon, label)` – renders a header with an icon

UI Ideas:
- Glassy navbar with icons
- Title bar with emoji label
- Preview badge overlay for unfinished pages
"""

from __future__ import annotations

from typing import Dict, Iterable, Optional
from uuid import uuid4
from pathlib import Path
import os
import importlib
import streamlit as st
from modern_ui_components import SIDEBAR_STYLES
from profile_card import render_profile_card as _render_profile_card

LAYOUT_CSS = """
<style>
.insta-card {
    display: flex;
    flex-direction: column;
    background: var(--card);
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    transition: transform .2s ease, box-shadow .2s ease;
}
.insta-card img {
    width: 100%;
    height: auto;
}
.insta-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
</style>
"""

try:
    _paths = importlib.import_module("utils.paths")
    ROOT_DIR = _paths.ROOT_DIR
    PAGES_DIR = _paths.PAGES_DIR
except Exception:  # pragma: no cover - fallback when utils isn't installed
    ROOT_DIR = Path(__file__).resolve().parents[1]
    PAGES_DIR = ROOT_DIR / "transcendental_resonance_frontend" / "pages"


try:
    from streamlit_option_menu import option_menu
    USE_OPTION_MENU = True
except ImportError:
    USE_OPTION_MENU = False


def main_container() -> st.delta_generator.DeltaGenerator:
    """Return a container for the main content area."""
    st.markdown(LAYOUT_CSS, unsafe_allow_html=True)
    return st.container()



def sidebar_container() -> st.delta_generator.DeltaGenerator:
    """Return the sidebar container."""
    return st.sidebar


def render_profile_card(username: str, avatar_url: str) -> None:
    """Proxy to :func:`profile_card.render_profile_card` using this module's ``st``."""
    import profile_card

    original = profile_card.st
    profile_card.st = st
    try:
        _render_profile_card(username, avatar_url)
    finally:
        profile_card.st = original


def render_top_bar() -> None:
    """Render the translucent top bar (logo · search with suggestions · notifications · beta toggle · avatar)."""
    if "PYTEST_CURRENT_TEST" in os.environ:
        return
    st.markdown(
        """
        <!-- Font Awesome for the bell icon -->
        <link rel="stylesheet"
              href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />

        <style>
        .sn-topbar{
            position:sticky;top:0;z-index:1000;
            display:flex;align-items:center;gap:1rem;
            padding:.5rem 1rem;
            background:rgba(30,30,30,.6);
            backdrop-filter:blur(8px);
        }
        @media(max-width:600px){
            .sn-topbar{flex-direction:column;align-items:stretch;}
        }

        .sn-topbar input{
            flex:1;padding:.25rem .5rem;
            border-radius:6px;
            border:1px solid rgba(255,255,255,.3);
            background:rgba(255,255,255,.85);
        }

        /* Bell button with badge */
        .sn-bell{
            position:relative;
            background:transparent;border:none;cursor:pointer;
            font-size:1.25rem;color:#fff;
        }
        .sn-bell::before{
            font-family:"Font Awesome 6 Free";font-weight:900;
            content:"\\f0f3";                      /* fa-bell */
        }
        .sn-bell[data-count]::after{
            content:attr(data-count);
            position:absolute;top:-.35rem;right:-.45rem;
            background:red;color:#fff;border-radius:50%;
            padding:0 .3rem;font-size:.6rem;line-height:1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ────────────────────────────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="sn-topbar">', unsafe_allow_html=True)

        # Columns: logo | search | bell | beta | avatar
        cols       = st.columns([1, 4, 1, 2, 1])
        logo_col   = cols[0]
        search_col = cols[1]
        bell_col   = cols[2]
        beta_col   = cols[3]
        avatar_col = cols[4]

        # ── Logo ────────────────────────────────────────────────────────
        logo_col.markdown(
            '<img src="https://placehold.co/32x32?text=SN" width="32" />',
            unsafe_allow_html=True,
        )

        # ── Search box with recent-query suggestions ────────────────────
        page_id   = st.session_state.get("active_page", "global")
        search_key = f"{page_id}_topbar_search"

        query = search_col.text_input(
            "Search",
            placeholder="Search…",
            key=search_key,
            label_visibility="collapsed",
        )

        if query:
            recent = st.session_state.setdefault("recent_searches", [])
            if query not in recent:
                recent.append(query)
                st.session_state["recent_searches"] = recent[-5:]        # keep last 5

        suggestions = st.session_state.get("recent_searches", [])
        if suggestions:
            opts = "".join(f"<option value='{s}'></option>" for s in suggestions)
            search_col.markdown(
                f"""
                <datalist id="recent-searches">{opts}</datalist>
                <script>
                  const inp = window.parent.document.querySelector('.sn-topbar input');
                  if (inp) inp.setAttribute('list','recent-searches');
                </script>
                """,
                unsafe_allow_html=True,
            )

        # ── Notifications bell (popover lists messages) ─────────────────
        note_count = len(st.session_state.get("notifications", []))
        bell_col.markdown(
            f'<button class="sn-bell" data-count="{note_count if note_count else ""}" '
            f'aria-label="Notifications"></button>',
            unsafe_allow_html=True,
        )
        with bell_col.popover("Notifications"):
            notes = st.session_state.get("notifications", [])
            if notes:
                for n in notes:
                    st.write(n)
            else:
                st.write("No notifications")

        # ── Beta mode toggle ────────────────────────────────────────────
        beta_enabled = beta_col.toggle(
            "Beta Mode",
            value=st.session_state.get("beta_mode", False),
        )
        st.session_state["beta_mode"] = beta_enabled
        try:
            st.query_params["beta"] = "1" if beta_enabled else "0"
        except Exception:
            st.experimental_set_query_params(beta="1" if beta_enabled else "0")

        # ── Avatar ──────────────────────────────────────────────────────
        avatar_col.markdown(
            '<img src="https://placehold.co/32x32" width="32" style="border-radius:50%" />',
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # (Optional) JS stub for external suggestion endpoint demonstration
    st.markdown(
        """
        <script>
        document.addEventListener('DOMContentLoaded', () => {
          const inp = document.querySelector('.sn-topbar input');
          if (!inp) return;
          let t;
          inp.addEventListener('input', () => {
            clearTimeout(t);
            const q = inp.value.trim();
            if (!q) return;
            t = setTimeout(async () => {
              try {
                const res = await fetch('/suggest?q=' + encodeURIComponent(q));
                const data = await res.json();
                window.dispatchEvent(new CustomEvent('search-suggestions', {detail: data}));
              } catch(e){ console.error(e); }
            }, 300);
          });
        });
        </script>
        """,
        unsafe_allow_html=True,
    )


def _render_sidebar_nav(
    page_links: Iterable[str] | Dict[str, str],
    icons: Optional[Iterable[str]] = None,
    key: Optional[str] = None,
    default: Optional[str] = None,
    session_key: str = "active_page",
) -> str:
    """Render a vertical sidebar navigation and return the selected label.

    ``page_links`` may be provided as an iterable of page paths/slugs or a
    mapping of labels to those paths. The data is normalized into a
    ``{label: slug}`` dictionary with lowercase slugs. Duplicate slugs are
    ignored and links are sorted alphabetically before rendering.
    The selected page label is also stored in ``st.session_state`` using
    ``session_key`` so other components can react to the active page.
    """

    # Normalize to label -> slug dictionary
    items = list(page_links.items()) if isinstance(page_links, dict) else [
        (None, str(o)) for o in page_links
    ]
    icon_list = list(icons or [None] * len(items))
    key = key or uuid4().hex

    normalized: Dict[str, str] = {}
    seen_slugs: set[str] = set()
    for (label, path), icon in zip(items, icon_list):
        slug = Path(path).stem.lower()
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        if not label:
            label = Path(path).stem.replace("_", " ").title()
        normalized[label] = slug

    # filter out slugs that don't exist and show an error
    valid_opts: list[tuple[str, str]] = []
    valid_icons: list[Optional[str]] = []
    for (label, slug), icon in zip(normalized.items(), icon_list):
        candidates = [ROOT_DIR / slug, PAGES_DIR / slug]
        exists = any(c.with_suffix(".py").exists() for c in candidates)
        if not exists:
            st.sidebar.error(f"Page not found: {slug}")
            continue
        valid_opts.append((label, slug))
        valid_icons.append(icon)

    sorted_pairs = sorted(zip(valid_opts, valid_icons), key=lambda p: p[0][0].lower())
    opts = [p for p, _ in sorted_pairs]
    icon_list = [ico for _, ico in sorted_pairs]
    if not opts:
        return ""

    active = st.session_state.get(session_key, default or opts[0][0])
    if active not in [label for label, _ in opts]:
        active = opts[0][0]
    index = [label for label, _ in opts].index(active)

    choice = active
    container = st.sidebar.container()
    with container:
        st.markdown(SIDEBAR_STYLES, unsafe_allow_html=True)
        st.markdown("<div class='glass-card sidebar-nav'>", unsafe_allow_html=True)
        if hasattr(st.sidebar, "page_link"):
            for (label, slug), icon in zip(opts, icon_list):
                page_path = f"/pages/{slug}.py"
                try:
                    st.sidebar.page_link(page_path, label=label, icon=icon, help=label)
                except Exception:
                    url = f"?page={label}"
                    st.sidebar.link_button(label, url=url, icon=icon)
        elif USE_OPTION_MENU and option_menu is not None:
            choice = option_menu(
                menu_title="Choose",
                options=[label for label, _ in opts],
                icons=[icon or "dot" for icon in icon_list],
                orientation="vertical",
                key=key,
                default_index=index,
            )
        else:
            labels = [f"{icon or ''} {label}".strip() for (label, _), icon in zip(opts, icon_list)]
            choice = st.radio(
                "Navigation",
                labels,
                index=index,
                key=key,
                label_visibility="collapsed",
            )
            choice = opts[labels.index(choice)][0]

        st.markdown("</div>", unsafe_allow_html=True)

    st.session_state[session_key] = choice
    return choice



def render_sidebar_nav(*args, **kwargs):
    """Wrapper to allow legacy patching via ``render_modern_sidebar``."""
    if globals().get("render_modern_sidebar") is not render_sidebar_nav:
        return globals()["render_modern_sidebar"](*args, **kwargs)
    return _render_sidebar_nav(*args, **kwargs)


# Legacy name used in older modules
render_modern_sidebar = render_sidebar_nav


def render_title_bar(icon: str, label: str) -> None:
    """Display a stylized page title with icon."""
    st.markdown(
        f"<h1 style='display:flex;align-items:center;'>"
        f"<span style='margin-right:0.5rem'>{icon}</span>{label}</h1>",
        unsafe_allow_html=True,
    )


def show_preview_badge(text: str = "🚧 Preview Mode") -> None:
    """Overlay a badge used when a fallback or WIP page is shown."""
    st.markdown(
        f"<div style='position:fixed; top:1rem; right:1rem; background:#ffc107; "
        f"color:#000; padding:0.25rem 0.5rem; border-radius:4px; z-index:1000;'>"
        f"{text}</div>",
        unsafe_allow_html=True,
    )


"""\
## UI Ideas

- Glassmorphism cards for data panels
- Sidebar navigation with emoji icons
- Animated progress bars for background tasks
- Reaction badges for interactive elements
"""

__all__ = [
    "main_container",
    "sidebar_container",
    "render_sidebar_nav",
    "render_title_bar",
    "show_preview_badge",
    "render_profile_card",
    "render_top_bar",
]
