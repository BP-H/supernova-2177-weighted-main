# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
import asyncio
import json
import streamlit as st
from streamlit_helpers import safe_container, alert
import pandas as pd
try:
    from st_aggrid import AgGrid, GridOptionsBuilder
except Exception:
    # pragma: no cover - optional dependency
    AgGrid = None
    GridOptionsBuilder = None
try:
    from frontend_bridge import dispatch_route
except Exception:
    # pragma: no cover - optional dependency
    dispatch_route = None

def _sanitize_markdown(text: str) -> str:
    """Return a UTF-8 safe string for ``st.markdown``."""
    if isinstance(text, bytes):
        return text.decode("utf-8", "ignore")
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")

def safe_markdown(text: str, **kwargs) -> None:
    """Render markdown after sanitizing the input text."""
    st.markdown(_sanitize_markdown(text), **kwargs)

def _run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        return loop.run_until_complete(coro)

def render_proposals_tab(main_container=None) -> None:
    """Display proposal creation, listing and voting controls."""
    if main_container is None:
        main_container = st
    container_ctx = safe_container(main_container)
    with container_ctx:
        if AgGrid is None or GridOptionsBuilder is None:
            alert(
                "st_aggrid is not installed – proposal features unavailable.", "warning"
            )
            return
        if dispatch_route is None:
            alert(
                "Governance routes not enabled—enable them in config.", "warning"
            )
            return
        col1, col2 = st.columns([1, 1])
        with col1:
            with st.form("create_proposal_form"):
                st.write("Create Proposal")
                title = st.text_input("Title")
                description = st.text_area("Description")
                author_id = st.number_input("Author ID", value=1, step=1)
                group_id = st.text_input("Group ID")
                voting_deadline = st.date_input("Voting Deadline")
                submitted = st.form_submit_button("Create")
        with col2:
            if st.button("Refresh Proposals", key="refresh_proposals"):
                with st.spinner("Working on it..."):
                    try:
                        res = _run_async(dispatch_route("list_proposals", {}))
                        st.session_state["proposals_cache"] = res.get("proposals", [])
                        st.toast("Success!")
                    except Exception as exc:
                        alert(f"Failed to load proposals: {exc}", "error")
        proposals = st.session_state.get("proposals_cache", [])
        if proposals:
            simple = [
                {
                    "id": p.get("id"),
                    "title": p.get("title"),
                    "status": p.get("status"),
                    "deadline": p.get("voting_deadline"),
                }
                for p in proposals
            ]
            df = pd.DataFrame(simple)
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(filter=True, sortable=True, resizable=True)
            AgGrid(
                df,
                gridOptions=gb.build(),
                theme="streamlit",
                fit_columns_on_grid_load=True,
            )
        with st.form("vote_proposal_form"):
            st.write("Vote on Proposal")
            ids = [p.get("id") for p in proposals]
            prop_id = (
                st.selectbox("Proposal", ids)
                if ids
                else st.number_input("Proposal ID", value=1, step=1)
            )
            harmonizer_id = st.number_input(
                "Harmonizer ID", value=1, step=1, key="harmonizer_id_vote"
            )
            vote_choice = st.selectbox("Vote", ["yes", "no", "abstain"])
            vote_sub = st.form_submit_button("Submit Vote")
        if submitted:
            payload = {
                "title": title,
                "description": description,
                "author_id": int(author_id),
                "group_id": group_id or None,
                "voting_deadline": voting_deadline.isoformat(),
            }
            with st.spinner("Working on it..."):
                try:
                    res = _run_async(dispatch_route("create_proposal", payload))
                    alert(f"Proposal {res.get('id')} created!", "info")
                except Exception as exc:
                    alert(f"Failed to create proposal: {exc}", "error")



def main():
    st.write("Voting content (placeholder - add your code).")  # Low numbers as placeholder

if __name__ == "__main__":
    main()
