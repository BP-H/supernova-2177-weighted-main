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
    
    st.write(f"Welcome to the {page_title} page.")
    st.info("This content is a placeholder. You can now build out the specific functionality for this page.")
    
    # --- ADD YOUR PAGE-SPECIFIC CODE BELOW ---
    
    # Example:
    if st.button("Click me for a surprise!"):
        st.balloons()

# This ensures the main function is called when the page is loaded.
if __name__ == "__main__":
    main()
