<!--
STRICTLY A SOCIAL MEDIA PLATFORM
Intellectual Property & Artistic Inspiration
Legal & Ethical Safeguards
-->
# UI Backend Sync Toggle

`ui.py` now supports an optional connection to the real backend. By default,
it uses local stubs to preserve existing behaviour.

Enable the backend by setting an environment variable or passing a CLI flag:

```bash
USE_REAL_BACKEND=1 streamlit run ui.py
# or
streamlit run ui.py -- --real-backend
# start script examples
USE_REAL_BACKEND=1 ./start.sh
./start.sh --real-backend
```

Call the `use_backend()` helper within `ui.py` to check whether the real
backend is active. When enabled, the module imports functions from
`superNova_2177`.
