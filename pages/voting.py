import importlib
import streamlit as st

def main() -> None:
    """Load the real voting page if available or show a placeholder."""
    try:
        mod = importlib.import_module("transcendental_resonance_frontend.pages.voting")
        if hasattr(mod, "main"):
            return mod.main()
        if hasattr(mod, "render"):
            return mod.render()
    except Exception:
        pass

    st.header("Voting")
    st.info("Voting page coming soon.")

def render() -> None:
    """Entry point for the Voting page."""
    main()

if __name__ == "__main__":
    main()
