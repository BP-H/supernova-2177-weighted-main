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
                st.image(img, use_column_width=True)
                return _DummyElement()

            def badge(self, text: str) -> _DummyElement:
                st.markdown(f"<span>{html.escape(text)}</span>", unsafe_allow_html=True)
                return _DummyElement()

        ui = _DummyUI()  # type: ignore
        shadcn = None


def sanitize_text(text: Any) -> str:
    """Return ``text`` as a safe UTF-8 string."""
    if not isinstance(text, str):
        text = str(text)
    return text.encode("utf-8", "ignore").decode("utf-8")


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

try:
    from modern_ui import inject_modern_styles  # type: ignore
except Exception:  # noqa: BLE001

    def inject_modern_styles(*_a: Any, **_kw: Any) -> None:  # type: ignore
        """No-op when *modern_ui* is absent."""
        return None


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
    """Instagram-style post card that degrades gracefully."""
    img = sanitize_text(post_data.get("image", "")) if post_data.get("image") else ""
    text = sanitize_text(post_data.get("text", ""))
    likes = post_data.get("likes", 0)
    try:
        likes = int(likes)
    except Exception:
        likes = 0

    if ui is None:
        if img:
            st.image(img, use_column_width=True)
        st.write(text)
        st.caption(f"❤️ {likes}")
        st.markdown(
            "<div style='color:var(--text-color);font-size:1.2em;'>❤️ 🔁 💬</div>",
            unsafe_allow_html=True,
        )
        return

    try:
        with ui.card().classes("w-full p-4 mb-4"):
            if img:
                ui.image(img).classes("rounded-md mb-2 w-full")
            safe_element("p", text).classes("mb-1") if hasattr(ui, "element") else st.markdown(text)
            ui.badge(f"❤️ {likes}").classes("bg-pink-500 mb-1")
            ui.element("div", "❤️ 🔁 💬").classes("text-center text-lg")
    except Exception as exc:  # noqa: BLE001
        st.toast(f"Post card failed: {exc}", icon="⚠️")
        if img:
            st.image(img, use_column_width=True)
        st.write(text)
        st.caption(f"❤️ {likes}")
        st.markdown(
            "<div style='color:var(--text-color);font-size:1.2em;'>❤️ 🔁 💬</div>",
            unsafe_allow_html=True,
        )


import html  # Ensure this is imported at the top if not already

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
def _apply_theme_css(theme: str) -> None:
    """Inject CSS for the selected theme."""
    if theme.lower() == "dark":
        css = """
        <style>
        :root {
            --background: #1e1e1e;
            --secondary-bg: #252525;
            --text-color: #d4d4d4;
            --primary-color: #4f8bf9;
            --font-family: 'Inter', sans-serif;
        }
        .stApp {
            background: var(--background);
            color: var(--text-color);
            font-family: var(--font-family);
        }
        a { color: var(--primary-color); }
        </style>
        """
    elif theme.lower() == "codex":
        css = """
        <style>
        :root {
            --background: #202123;
            --secondary-bg: #343541;
            --text-color: #ECECF1;
            --primary-color: #19C37D;
            --font-family: 'Iosevka', monospace;
        }
        .stApp {
            background: var(--background);
            color: var(--text-color);
            font-family: var(--font-family);
        }
        a { color: var(--primary-color); }
        </style>
        """
    else:  # light default
        css = """
        <style>
        :root {
            --background: #F0F2F6;
            --secondary-bg: #FFFFFF;
            --text-color: #333333;
            --primary-color: #0A84FF;
            --font-family: 'Inter', sans-serif;
        }
        .stApp {
            background: var(--background);
            color: var(--text-color);
            font-family: var(--font-family);
        }
        a { color: var(--primary-color); }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)


def apply_theme(theme: str) -> None:
    """Public wrapper around the internal CSS injector."""
    try:
        _apply_theme_css(theme)
    except Exception as exc:  # noqa: BLE001
        st.warning(f"Theme application failed: {exc}")


def theme_selector(label: str = "Theme", *, key_suffix: str | None = None) -> str:
    """Render a Light/Dark selector that remembers the choice in session_state."""
    if key_suffix is None:
        key_suffix = "default"

    theme_key = f"theme_{key_suffix}"
    if theme_key not in st.session_state:
        st.session_state[theme_key] = "light"

    unique_key = f"theme_selector_{key_suffix}"
    current = st.session_state[theme_key]

    if ui is not None and hasattr(ui, "radio_group"):
        try:
            choice = ui.radio_group(
                ["Light", "Dark"],
                default_value="Light" if current == "light" else "Dark",
                key=unique_key,
            )
        except Exception:  # fallback to Streamlit
            choice = st.selectbox(
                label,
                ["Light", "Dark"],
                index=0 if current == "light" else 1,
                key=unique_key,
            )
    else:
        choice = st.selectbox(
            label,
            ["Light", "Dark"],
            index=0 if current == "light" else 1,
            key=unique_key,
        )

    st.session_state[theme_key] = choice.lower()
    apply_theme(st.session_state[theme_key])
    return st.session_state[theme_key]

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


# ──────────────────────────────────────────────────────────────────────────────
# Public symbols
# ──────────────────────────────────────────────────────────────────────────────
__all__ = [
    "alert",
    "header",
    "render_post_card",
    "render_instagram_grid",
    "render_mock_feed",
    "sanitize_text",
    "apply_theme",
    "theme_selector",
    "get_active_user",
    "centered_container",
    "safe_container",
    "tabs_nav",
    "inject_global_styles",
    "inject_instagram_styles",
    "ensure_active_user",
    "BOX_CSS",
]
