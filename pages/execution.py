import streamlit as st

def main():
    st.title("Execution")
    p = st.session_state.get("proposal")
    d = st.session_state.get("decision")
    if not p or not d or not d.get("approved"):
        st.warning("Need an approved proposal first.")
        return
    st.write("**Running**:", p)
    phase = st.radio("Phase", ["Dry-run", "Canary", "Full"], index=0)
    if st.button("Start"):
        st.info(f"Started {phase}. (Demo mode)")
        st.session_state.setdefault("runs", []).append(dict(phase=phase, proposal=p))
    st.subheader("History")
    for i, r in enumerate(reversed(st.session_state.get("runs", [])), 1):
        st.write(f"{i}. {r['phase']} – {r['proposal']['goal']}")

if __name__ == "__main__":
    main()
