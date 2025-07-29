# Codex Dark Theme

The Codex theme provides a minimalist dark appearance inspired by the ChatGPT interface.
It is available through `streamlit_helpers.theme_selector()` and sets the
`Inter` font stack for a clean layout.

### Usage

```python
from streamlit_helpers import theme_selector

# Add a radio selector to switch themes
theme_selector("Theme")
```

To make Codex the default or apply the vibrant cyan palette, update
`.streamlit/config.toml` with the new theme variables:

```toml
[theme]
primaryColor = "#00F0FF"
backgroundColor = "#001E26"
secondaryBackgroundColor = "#002B36"
textColor = "#E0FFFF"
font = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
```
