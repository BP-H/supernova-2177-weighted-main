# Universal template for all page files in the 'pages/' directory.
# Example filename: pages/feed.py

import streamlit as st
from pathlib import Path

def main():
    """
    Main function for this page.
    """
    # Automatically display the page title from the filename.
    # e.g., 'video_chat.py' becomes 'Video Chat'
    page_title = Path(__file__).stem.replace('_', ' ').title()
    st.header(page_title)
    
    # --- ADD YOUR PAGE-SPECIFIC UI AND LOGIC BELOW ---
    # This is where you will build the actual content for each page.
    
    st.write(f"Build out the {page_title} page here.")


# This ensures the main function is called when the page is loaded.
if __name__ == "__main__":
    main()
