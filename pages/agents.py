import importlib
import streamlit as st

def main() -> None:
    """Load the real agents page if present, otherwise show a placeholder."""
    try:
        mod = importlib.import_module("transcendental_resonance_frontend.pages.agents")
        if hasattr(mod, "main"):
            return mod.main()
        if hasattr(mod, "render"):
            return mod.render()
    except Exception:
        pass

    st.header("Agents")
    st.info("Agents page coming soon.")

def render() -> None:
    """Entry point for the Agents page."""
    main()

if __name__ == "__main__":
    main()
