# pages/agents.py
from __future__ import annotations
import asyncio
import streamlit as st
from typing import Any, Dict

# Your async bridge
from frontend_bridge import dispatch_route

st.header("🤖 Agents")

def call(route: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    # Streamlit is sync; wrap the async bridge call
    return asyncio.run(dispatch_route(route, payload))

# --- API key (session only; no persistence yet) -------------------------------
st.subheader("API key")
st.caption("Paste your OpenAI key once; we pass it to the launcher for this session.")

openai_key = st.text_input(
    "OPENAI_API_KEY",
    type="password",
    value=st.session_state.get("openai_key", ""),
    key="agents_openai_key_input_v1_v2",       # <-- UNIQUE KEY
)

if st.button("Save key (session)", key="agents_save_key_btn_v2"):
    st.session_state["openai_key"] = openai_key
    st.success("Saved to this session.")

# --- discover agents ----------------------------------------------------------
st.subheader("Available agents")
resp = call("protocol_agents_list", {})  # or "list_agents"
agents = resp.get("agents", []) if isinstance(resp, dict) else []
chosen = st.multiselect(
    "Pick agents to run",
    options=agents,
    default=agents[:1],
    key="agents_pick_multiselect_v1_v2",       # <-- UNIQUE KEY
)

# --- pick backend -------------------------------------------------------------
st.subheader("Backend (optional)")
st.caption("Leave empty to use the agent default. Example: openai:gpt-4o-mini")
llm_backend = st.text_input(
    "LLM backend",
    value="openai:gpt-4o-mini",
    key="agents_backend_input_v1_v2",          # <-- UNIQUE KEY
)

c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 Launch", key="agents_launch_btn_v2"):
        payload = {
            "provider": "openai",
            "api_key": st.session_state.get("openai_key", ""),
            "agents": chosen,
            "llm_backend": llm_backend.strip() or None,
        }
        out = call("protocol_agents_launch", payload)  # or "launch_agents"
        st.success(f"Launched: {out.get('launched', [])}")

with c2:
    if st.button("⏭️ Step all", key="agents_step_btn_v2"):
        out = call("protocol_agents_step", {})  # or "step_agents"
        st.info(f"Stepped: {out.get('stepped', [])}")
