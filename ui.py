# ui.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Main Streamlit UI entry point for superNova_2177."""
import sys
from pathlib import Path
import streamlit as st

# Path setup for Cloud mount
sys.path.insert(0, str(Path("/mount/src").resolve() if 'mount' in str(Path(__file__)) else Path(__file__).parent))

# Imports (same as before)
# ... (keep your existing imports and dummies)

# Loader (fixed for Cloud /mount/src/pages/)
def load_page(page_name: str):
    try:
        base_paths = [Path("/mount/src/pages"), Path(__file__).parent / "pages"]
        for base in base_paths:
            module_path = base / f"{page_name}.py"
            if module_path.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location(page_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'main'):
                    module.main()
                elif hasattr(module, 'render'):
                    module.render()
                return
        st.error(f"Page file missing for {page_name}. Check /pages/ folder.")
    except Exception as e:
        st.error(f"Error loading {page_name}: {e}")

# Main (collapsed sidebar confirmed)
def main() -> None:
    st.set_page_config(
        page_title="superNova_2177",
        layout="wide",
        initial_sidebar_state="collapsed"  # Hides default
    )
    st.session_state.setdefault("theme", "light")
    initialize_theme(st.session_state["theme"])

    with st.sidebar:
        st.title("🌌 superNova")
        PAGES = {
            "Feed": "feed",
            "Chat": "chat",
            "Messages": "messages",
            "Agents": "agents",
            "Voting": "voting",
            "Profile": "profile",
            "Music": "music",
        }
        page_selection = st.radio("Navigation", list(PAGES.keys()))
        theme_selector()

    page_to_load = PAGES.get(page_selection)
    if page_to_load:
        load_page(page_to_load)
    else:
        st.write("Select a page.")

if __name__ == "__main__":
    main()
