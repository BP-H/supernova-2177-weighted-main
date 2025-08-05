# UI Backend Sync Toggle

The Streamlit UI can connect to either a mock backend or the real service. By
default the UI uses the mocked behavior. A toggle allows developers to enable
integration with the real backend when desired.

## Environment Variable

Enable the real backend via an environment variable:

```bash
export USE_REAL_BACKEND=1
streamlit run ui.py
```

Set the variable to `0` or omit it to keep the mock backend.

## Command Line Flags

The toggle can also be controlled with command line flags. CLI options override
the environment variable.

```bash
# Enable the real backend
streamlit run ui.py -- --use-backend

# Explicitly disable it
streamlit run ui.py -- --no-backend
```

## Checking in Code

Use the helper to check the toggle inside your application logic:

```python
from ui import use_real_backend

if use_real_backend():
    connect_to_backend()
else:
    use_stub()
```
