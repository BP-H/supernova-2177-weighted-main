import importlib
import streamlit as st


def main() -> None:
    """Load the real validation page if present or show a placeholder."""
    try:
        mod = importlib.import_module(
            "transcendental_resonance_frontend.pages.validation"
        )
        if hasattr(mod, "main"):
            return mod.main()
        if hasattr(mod, "render"):
            return mod.render()
    except Exception:
        pass
    st.header("Validation")
    st.info("Validation page not available.")


def render() -> None:
    main()


if __name__ == "__main__":
    main()
