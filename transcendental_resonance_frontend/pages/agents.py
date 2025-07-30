import streamlit as st
from agent_ui import render_agent_insights_tab


def main(main_container=None) -> None:
    """Render the full agent insights tab if available."""
    if main_container is None:
        main_container = st

    try:
        render_agent_insights_tab(main_container=main_container)
    except Exception as e:  # pragma: no cover - UI
        st.error(f"Agent page error: {e}")
        if st.button("Reset", key="agent_reset"):
            st.rerun()


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()


if __name__ == "__main__":
    main()
