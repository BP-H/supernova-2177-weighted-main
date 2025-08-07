import os, json, urllib.request
import streamlit as st

def _use_backend(): return os.getenv("USE_REAL_BACKEND","0").lower() in {"1","true","yes"}
def _burl(): return os.getenv("BACKEND_URL","http://127.0.0.1:8000")
def _get(path):
    with urllib.request.urlopen(_burl()+path) as r:
        import json; return json.loads(r.read().decode("utf-8"))
def _post(path, payload):
    import json; data=json.dumps(payload).encode("utf-8")
    import urllib.request as ur; req=ur.Request(_burl()+path, data=data, headers={"Content-Type":"application/json"})
    with ur.urlopen(req) as r: return json.loads(r.read().decode("utf-8"))

try:
    from external_services.fake_api import list_proposals, tally_proposal, decide, list_decisions
except Exception:
    def list_proposals(): return []
    def tally_proposal(pid): return {"up":0,"down":0}
    def decide(pid, threshold=0.6): return {"proposal_id":pid, "status":"rejected"}
    def list_decisions(): return []

def main():
    st.subheader("Decisions")
    st.caption("Rule: accept when 👍 / (👍+👎) ≥ 60% (and at least 1 vote).")

    if _use_backend():
        proposals = _get("/proposals")
    else:
        proposals = list_proposals()

    for p in proposals:
        pid = p["id"]
        tally = (_get(f"/proposals/{pid}/tally") if _use_backend() else tally_proposal(pid))
        up, down = tally.get("up",0), tally.get("down",0)
        total = up+down
        pct = (up/total*100) if total else 0
        st.write(f"**{p['title']}** — {up} 👍 / {down} 👎  ({pct:.0f}%)")
        if st.button(f"Compute decision for #{pid}", key=f"dec_{pid}"):
            res = (_post(f"/decide/{pid}", {}) if _use_backend() else decide(pid))
            st.success(f"Decision: {res.get('status').upper()}")

    st.divider()
    st.markdown("### Decisions log")
    out = (_get("/decisions") if _use_backend() else list_decisions())
    for d in out:
        st.write(f"#{d['id']} — proposal {d['proposal_id']} → **{d['status']}**")

def render(): main()
