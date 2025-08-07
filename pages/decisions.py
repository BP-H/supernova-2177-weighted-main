import streamlit as st

def main():
    st.title("Decisions")
    p = st.session_state.get("proposal")
    if not p:
        st.warning("No proposal found. Go to Proposals first.")
        return
    st.write("**Proposal**", p)
    st.subheader("Voting (⅓ Human, ⅓ Safety, ⅓ Ops)")
    human = st.slider("Human Council", 0, 100, 80)
    safety = st.slider("Safety Council", 0, 100, 90)
    ops = st.slider("Ops Council", 0, 100, 75)
    weighted = round((human + safety + ops) / 3)
    st.metric("Weighted approval", f"{weighted}%")
    if weighted >= 70:
        if st.button("Approve"):
            p["status"] = "Approved"
            st.session_state["decision"] = dict(approved=True, score=weighted)
            st.success("Approved. Head to Execution →")
            st.session_state["nav_hint"] = "Execution"
    else:
        st.error("Below threshold; adjust or reject.")
        if st.button("Reject"):
            p["status"] = "Rejected"
            st.session_state["decision"] = dict(approved=False, score=weighted)

if __name__ == "__main__":
    main()
