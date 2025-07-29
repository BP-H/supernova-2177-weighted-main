# Codex Dark Theme

The Codex theme provides a minimalist dark appearance inspired by the ChatGPT interface.
It is available through `streamlit_helpers.theme_selector()` and sets a monospace
Iosevka font for a clean layout.

### Usage

```python
from streamlit_helpers import theme_selector

# Add a radio selector to switch themes
theme_selector("Theme")
```

To make Codex the default, update `.streamlit/config.toml` with the included palette.
