# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""
Streamlit UI helper utilities.

This module provides small helpers used across the Streamlit
applications to keep the UI code concise and consistent.
"""

from __future__ import annotations

import html
from contextlib import nullcontext
from typing import Any, ContextManager, Literal
from frontend.theme import set_theme

_FAKE_SESSION: dict[str, Any] = {}
import inspect
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# UI-backend detection
# ──────────────────────────────────────────────────────────────────────────────
# Prefer streamlit-shadcn-ui and fall back to NiceGUI or plain Streamlit
try:  # streamlit-shadcn-ui available?
    import streamlit_shadcn_ui as ui  # type: ignore
    shadcn = ui
except Exception:  # noqa: BLE001
    try:  # NiceGUI available?
        from nicegui import ui  # type: ignore
        shadcn = None
    except Exception:  # noqa: BLE001
        from contextlib import nullcontext
        import html
        from typing import Any, ContextManager
        import streamlit as st

        class _DummyElement:
            """Gracefully ignore chained style/class calls and context management."""

            def __init__(self, cm: ContextManager | None = None) -> None:
                self._cm = cm or nullcontext()

            def __enter__(self) -> Any:
                return self._cm.__enter__()

            def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
                self._cm.__exit__(exc_type, exc, tb)

            def classes(self, *_a: Any, **_k: Any) -> "_DummyElement":
                return self

            def style(self, *_a: Any, **_k: Any) -> "_DummyElement":
                return self

        class _DummyUI:
            """Fallback UI with minimal Streamlit implementations."""

            def element(self, tag: str, content: str) -> _DummyElement:
                if tag.lower() == "h1":
                    st.header(content)
                else:
                    st.markdown(
                        f"<{tag}>{html.escape(content)}</{tag}>",
                        unsafe_allow_html=True,
                    )
                return _DummyElement()

            def card(self) -> _DummyElement:
                return _DummyElement(st.container())

            def image(self, img: str) -> _DummyElement:
                st.image(img, use_container_width=True, alt="UI image")
                return _DummyElement()



            def badge(self, text: str) -> _DummyElement:
                st.markdown(f"<span>{html.escape(text)}</span>", unsafe_allow_html=True)
                return _DummyElement()

        ui = _DummyUI()  # type: ignore
        shadcn = None




def safe_element(tag: str, content: str) -> Any:
    """Create a UI element with graceful fallback and debug info."""
    clean = sanitize_text(content)
    try:
        return ui.element(tag, clean)
    except TypeError as exc:
        st.toast(f"ui.element signature mismatch: {exc}", icon="⚠️")
        try:
            elem = ui.element(tag)
            if hasattr(elem, "text"):
                elem.text(clean)
                return elem
            if hasattr(elem, "content"):
                setattr(elem, "content", clean)
                return elem
        except Exception as inner_exc:
            st.toast(f"element fallback failed: {inner_exc}", icon="❌")
    except Exception as exc:  # noqa: BLE001
        st.toast(f"ui.element error: {exc}", icon="❌")
    st.markdown(f"<{tag}>{html.escape(clean)}</{tag}>", unsafe_allow_html=True)
    return None


# ──────────────────────────────────────────────────────────────────────────────
# Optional modern-ui styles injector
# ──────────────────────────────────────────────────────────────────────────────

from frontend.theme import inject_modern_styles


# ──────────────────────────────────────────────────────────────────────────────
# Global CSS
# ──────────────────────────────────────────────────────────────────────────────
BOX_CSS = """
<style>
.tab-box {
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #ddd;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
</style>
"""
# Inject immediately so any importing page gets the style
st.markdown(BOX_CSS, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Helper components
# ──────────────────────────────────────────────────────────────────────────────
def sanitize_text(text: Any) -> str:
    """Return ``text`` as a safe string preserving emojis."""
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    return html.escape(text, quote=False)


def sanitize_emoji(text: str) -> str:
    """Return ``text`` with emoji code points HTML-encoded or removed."""
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    out = []
    for ch in text:
        cp = ord(ch)
        if cp in (0xFE0E, 0xFE0F, 0x200D):
            continue  # strip variation selectors and joiners
        if cp > 0xFFFF:
            out.append(f"&#x{cp:X};")
        else:
            out.append(ch)
    return "".join(out)


def _safe_element(tag: str, content: str):
    """Render ``ui.element`` safely across backends."""
    try:
        return ui.element(tag, content)
    except TypeError as exc:
        st.toast(f"ui.element signature mismatch: {exc}", icon="⚠️")
        try:
            elem = ui.element(tag)
            if hasattr(elem, "text"):
                elem.text(content)
            return elem
        except Exception as inner_exc:  # pragma: no cover - fallback
            st.toast(f"ui.element fallback failed: {inner_exc}", icon="⚠️")
    except Exception as exc:  # pragma: no cover - unexpected
        st.toast(f"ui.element failed: {exc}", icon="⚠️")
    # final plain Streamlit fallback
    if tag.lower() == "h1":
        st.header(content)
    else:
        st.markdown(f"<{tag}>{html.escape(content)}</{tag}>", unsafe_allow_html=True)
    return None


def alert(
    message: str,
    level: Literal["warning", "error", "info"] = "info",
    *,
    show_icon: bool = True,
) -> None:
    """Display a minimally intrusive alert box."""
    icons = {"warning": "⚠️", "error": "❌", "info": "ℹ️"}
    colours = {
        "warning": ("#fff7e6", "#f0ad4e"),
        "error": ("#fdecea", "#f44336"),
        "info": ("#e8f4fd", "#1e88e5"),
    }
    bg, border = colours.get(level, colours["info"])
    icon = icons.get(level, "") if show_icon else ""
    # Prefer shadcn-ui components when available
    if ui is not None and hasattr(ui, "card"):
        try:
            text = f"{icon} {message}" if icon else message
            ui.card(content=text)
            if hasattr(ui, "badges"):
                variant_map = {
                    "warning": "secondary",
                    "error": "destructive",
                    "info": "default",
                }
                ui.badges([(level.title(), variant_map.get(level, "default"))])
            return
        except Exception:  # noqa: BLE001 - fallback to Streamlit below
            pass
    st.markdown(
        f"<div style='border-left:4px solid {border};"
        f"background:{bg};padding:.5em 1em;border-radius:4px;"
        f"margin-bottom:1em;display:flex;align-items:center;gap:.5rem;'>"
        f"{f'<span>{html.escape(icon)}</span>' if icon else ''}{html.escape(message)}</div>",
        unsafe_allow_html=True,
    )


def header(title: str, *, layout: str = "centered") -> None:
    """Render a standard page header using the best UI backend available."""
    st.markdown(
        "<style>.app-container{padding:1rem 2rem;}</style>",
        unsafe_allow_html=True,
    )
    safe_title = sanitize_text(title)
    _safe_element("h1", safe_title)


def render_post_card(post_data: dict[str, Any]) -> None:
    """
    Render an Instagram-style post card that works with or without the
    `streamlit-shadcn-ui` / NiceGUI back-end.

    Parameters
    ----------
    post_data
        Dictionary keys that may be present:

        * ``image`` – image URL
        * ``text``  – caption / body text
        * ``user``  / ``username`` – poster’s name
        * ``likes`` – like counter (int, str or anything castable to int)
    """
    # ── Extract & sanitise basic fields ──────────────────────────────────
    img      = sanitize_text(post_data.get("image", "")) if post_data.get("image") else ""
    text     = sanitize_text(post_data.get("text",  ""))
    username = sanitize_text(post_data.get("user") or post_data.get("username", ""))
    likes    = post_data.get("likes", 0)
    try:
        likes = int(likes)
    except Exception:        # leave at 0 on any conversion error
        likes = 0

    if ui is None:
        if hasattr(st, "image") and hasattr(st, "write"):
            if img:
                st.image(
                    img,
                    use_container_width=True,
                    alt=f"Post by {username}" if username else "post image",
                )

            caption_text = f"**{html.escape(username)}**: {text}" if username else text
            st.write(caption_text)
            getattr(st, "caption", st.write)(f"❤️ {likes}")
            getattr(st, "markdown", lambda *a, **k: None)(
                "<div style='color:var(--text-muted);font-size:1.2em;'>❤️ 🔁 💬</div>",

                unsafe_allow_html=True,
            )
        else:
            html_snippet = "<div class='shadcn-card' style='border-radius:12px;padding:8px;'>"
            if img:
                html_snippet += (
                    f"<img src='{html.escape(img)}' alt='' style='width:100%;border-radius:8px;'/>"
                )
            if username:
                html_snippet += f"<div><strong>{html.escape(username)}</strong></div>"
            html_snippet += f"<p>{html.escape(text)}</p>"
            html_snippet += f"<div style='color:var(--text-muted);font-size:1.2em;'>❤️ {likes} 🔁 💬</div>"
            html_snippet += "</div>"
            getattr(st, "markdown", lambda *a, **k: None)(html_snippet, unsafe_allow_html=True)
        return

    try:
        with ui.card().classes("w-full p-4 mb-4"):
            if img:
                ui.image(img).classes("rounded-md mb-2 w-full")
            if hasattr(ui, "element"):
                safe_element("p", text).classes("mb-1")
            else:
                st.markdown(text)
            badge_fn = getattr(ui, "badge", None)
            if badge_fn:
                badge_fn(f"❤️ {likes}").classes("bg-pink-500 mb-1")
                reaction = "❤️ 🔁 💬"
            else:
                reaction = f"❤️ {likes} 🔁 💬"
            if hasattr(ui, "element"):
                ui.element("div", reaction).classes("text-center text-lg")
            else:
                getattr(st, "markdown", lambda *a, **k: None)(
                    f"<div style='color:var(--text-muted);font-size:1.2em;'>{reaction}</div>",
                    unsafe_allow_html=True,
                )
    except Exception as exc:  # noqa: BLE001
        if hasattr(st, "toast"):
            st.toast(f"Post card failed: {exc}", icon="⚠️")
        elif hasattr(st, "warning"):
            st.warning(f"Post card failed: {exc}")
        if img:
            if hasattr(st, "image"):
                st.image(
                    img,
                    use_container_width=True,
                    alt=f"Post by {username}" if username else "post image",
                )
            else:
                getattr(st, "markdown", lambda *a, **k: None)(
                    f"<img src='{html.escape(img)}' alt='post image' style='width:100%'>",
                    unsafe_allow_html=True,
                )

        write_fn = getattr(st, "write", getattr(st, "markdown", lambda x: None))
        write_fn(text)
        getattr(st, "caption", write_fn)(f"❤️ {likes}")
        getattr(st, "markdown", lambda *a, **k: None)(
            "<div style='color:var(--text-muted);font-size:1.2em;'>❤️ 🔁 💬</div>",
            unsafe_allow_html=True,
        )


def render_instagram_grid(posts: list[dict[str, Any]], *, cols: int = 3) -> None:
    """Display posts in a responsive grid using ``render_post_card``."""
    columns = st.columns(cols)
    for i, post in enumerate(posts):
        with columns[i % cols]:
            username = post.get("username") or post.get("user", "")
            caption = post.get("caption") or post.get("text", "")
            if username:
                st.markdown(f"**{html.escape(username)}**")
            render_post_card({
                "image": post.get("image"),
                "text": caption,
                "likes": post.get("likes", 0),
            })


def render_mock_feed() -> None:
    """Render a simple scrolling feed of demo posts."""
    posts = [
        (
            "alice",
            "https://picsum.photos/seed/alice/400/300",
            "Enjoying the sunshine!",
        ),
        (
            "bob",
            "https://picsum.photos/seed/bob/400/300",
            "Hiking adventures today.",
        ),
        (
            "carol",
            "https://picsum.photos/seed/carol/400/300",
            "Coffee time at my favourite spot.",
        ),
    ]

    st.markdown(
        "<div style='max-height: 400px; overflow-y: auto;'>",
        unsafe_allow_html=True,
    )
    with st.container():
        for username, image, caption in posts:
            render_post_card({
                "image": image,
                "text": f"**{html.escape(username)}**: {caption}",
                "likes": 0,
            })
    st.markdown("</div>", unsafe_allow_html=True)



# ──────────────────────────────────────────────────────────────────────────────
# Theme helpers
# ──────────────────────────────────────────────────────────────────────────────


def theme_selector(label: str = "Theme", *, key_suffix: str | None = None) -> str:
    """Render a Light / Dark selector that remembers the choice in session_state
    and mirrors it to the page’s ``?theme=`` query-parameter.

    Returns
    -------
    str
        The currently-selected theme, lower-cased (“light” or “dark”).
    """
    # ------------------------------------------------------------------ #
    # Keys and helpers
    # ------------------------------------------------------------------ #
    if key_suffix is None:
        key_suffix = "default"
    theme_key   = f"theme_{key_suffix}"          # per-caller key
    unique_key  = f"theme_selector_{key_suffix}" # widget key

    def _safe_session_set(k: str, v: str) -> None:
        """Robust setter that also works in test contexts."""
        try:
            st.session_state[k] = v
        except Exception:      # pylint: disable=broad-except
            _FAKE_SESSION[k] = v                     # type: ignore[name-defined]

    def _safe_session_get(k: str, default: str) -> str:
        try:
            return st.session_state.get(k, default)
        except Exception:      # pylint: disable=broad-except
            return _FAKE_SESSION.setdefault(k, default)  # type: ignore[name-defined]

    # ------------------------------------------------------------------ #
    # First-time initialisation: derive default from query-params
    # ------------------------------------------------------------------ #
    if theme_key not in st.session_state:
        try:
            params = st.query_params        # Streamlit ≥1.29
        except AttributeError:
            params = st.experimental_get_query_params()  # Legacy fallback

        param_theme = params.get("theme", None)
        if isinstance(param_theme, list):          # multi-param edge-case
            param_theme = param_theme[0]

        initial = str(param_theme).lower() if param_theme in {"light", "dark"} else "light"
        _safe_session_set(theme_key, initial)
        _safe_session_set("theme",    initial)     # global alias

    current = _safe_session_get(theme_key, "light")

    # ------------------------------------------------------------------ #
    # Render selector – prefer shadcn / NiceGUI where available
    # ------------------------------------------------------------------ #
    if ui is not None and hasattr(ui, "radio_group"):
        # streamlit-shadcn-ui radio buttons
        try:
            choice = ui.radio_group(
                ["Light", "Dark"],
                default_value="Light" if current == "light" else "Dark",
                key=unique_key,
            )
        except Exception:              # fall back to Streamlit
            choice = st.selectbox(
                label, ["Light", "Dark"],
                index=0 if current == "light" else 1,
                key=unique_key,
            )
    else:
        # vanilla Streamlit widget
        choice = st.selectbox(
            label, ["Light", "Dark"],
            index=0 if current == "light" else 1,
            key=unique_key,
        )

    # ------------------------------------------------------------------ #
    # Persist choice, apply CSS, sync query-params
    # ------------------------------------------------------------------ #
    chosen = choice.lower()
    _safe_session_set(theme_key, chosen)
    _safe_session_set("theme",    chosen)          # keep global alias

    set_theme(chosen)

    try:                                           # Streamlit ≥1.29
        st.query_params["theme"] = chosen
    except Exception:                              # noqa: BLE001
        pass

    return chosen


def theme_toggle(label: str = "Dark Mode", *, key_suffix: str | None = None) -> str:
    """Switch between light and dark themes using a toggle widget."""

    inject_modern_styles()

    if key_suffix is None:
        key_suffix = "default"

    theme_key = f"theme_{key_suffix}"
    toggle_key = f"theme_toggle_{key_suffix}"

    current = st.session_state.get(theme_key, "light")
    st.markdown("<div class='fade-in rounded'>", unsafe_allow_html=True)
    is_dark = st.toggle(label, value=current == "dark", key=toggle_key)
    st.markdown("</div>", unsafe_allow_html=True)

    chosen = "dark" if is_dark else "light"
    st.session_state[theme_key] = chosen
    st.session_state["theme"] = chosen

    set_theme(chosen)

    try:
        st.query_params["theme"] = chosen
    except Exception:
        pass

    return chosen

def centered_container(max_width: str = "900px") -> "st.delta_generator.DeltaGenerator":  # type: ignore
    """Return a container with standardized width constraints."""
    st.markdown(
        f"<style>.main .block-container{{max-width:{max_width};margin:auto;}}</style>",
        unsafe_allow_html=True,
    )
    return st.container()


def safe_container(container: Any) -> ContextManager:
    """Return a context manager for *container* or a nullcontext fallback."""
    try:
        candidate = container() if callable(container) else container
        if hasattr(candidate, "__enter__"):
            return candidate  # type: ignore[return-value]
    except Exception:  # noqa: BLE001
        pass
    return nullcontext()


def tabs_nav(labels: list[str], *, key: str = "tabs_nav") -> list[Any]:
    """Render tab navigation using the best available backend."""
    if ui is not None and hasattr(ui, "tabs"):
        try:
            return ui.tabs(labels, key=key)  # type: ignore[return-value]
        except Exception:  # noqa: BLE001
            pass
    return st.tabs(labels, key=key)


def inject_instagram_styles() -> None:
    """Inject lightweight CSS tweaks for an Instagram-like aesthetic."""
    st.markdown(
        """
        <style>
        body { background: #FAFAFA; }
        .shadcn-card {
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            background: #fff;
        }
        .shadcn-badge {
            border-radius: 999px;
            background: #fff;
            padding: 0.25rem 0.5rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .shadcn-btn {
            border-radius: 999px;
            padding: 0.25rem 0.75rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Backwards-compat alias
def inject_global_styles() -> None:
    """Deprecated – prefer *modern_ui.inject_modern_styles*."""
    inject_modern_styles()


def ensure_active_user() -> str:
    """Ensure ``st.session_state['active_user']`` is initialized."""
    return st.session_state.setdefault("active_user", "guest")


def get_active_user() -> str:
    """Return the currently active user from ``st.session_state``."""
    if "active_user" not in st.session_state:
        st.session_state["active_user"] = "guest"
    return st.session_state["active_user"]


# ──────────────────────────────────────────────────────────────────────────────
# Public symbols
# ──────────────────────────────────────────────────────────────────────────────
__all__ = [
    "alert",
    "sanitize_emoji",
    "header",
    "render_post_card",
    "render_instagram_grid",
    "render_mock_feed",
    "sanitize_text",
    "set_theme",
    "theme_selector",
    "theme_toggle",
    "get_active_user",
    "centered_container",
    "safe_container",
    "tabs_nav",
    "inject_global_styles",
    "inject_instagram_styles",
    "ensure_active_user",
    "BOX_CSS",
]
