# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
import streamlit as st
from ui_utils import render_modern_layout
from db_models import init_db, seed_default_users


def main() -> None:
    """Launch the Streamlit UI after ensuring the database is ready."""
    init_db()
    seed_default_users()
    render_modern_layout()


if __name__ == "__main__":
    main()
