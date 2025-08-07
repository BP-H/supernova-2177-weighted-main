import streamlit as st

def main():
    st.title("Proposals")
    st.caption("Draft a proposal → save it to session for review.")
    with st.form("proposal"):
        goal = st.text_area("Goal", "Launch pilot campaign")
        constraints = st.text_input("Constraints", "Budget $1k, safe content only")
        metrics = st.text_input("KPIs", "CTR, conversions")
        submitted = st.form_submit_button("Save Proposal")
    if submitted:
        st.session_state["proposal"] = dict(goal=goal, constraints=constraints, metrics=metrics, status="Draft")
        st.success("Saved to session. Go to Decisions →")
        st.session_state["nav_hint"] = "Decisions"

if __name__ == "__main__":
    main()
