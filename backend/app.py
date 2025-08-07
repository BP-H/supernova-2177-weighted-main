from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI(title="superNova_2177 backend", version="0.2")

# in-memory stores
DB = {"proposals": {}, "votes": [], "decisions": {}, "runs": {}}
C = {"proposal": 0, "decision": 0, "run": 0}

class ProposalIn(BaseModel):
    title: str
    body: str
    author: str

class Proposal(BaseModel):
    id: int
    title: str
    body: str
    author: str

class VoteIn(BaseModel):
    proposal_id: int
    voter: str
    choice: str  # 'up' | 'down'

class Decision(BaseModel):
    id: int
    proposal_id: int
    status: str

class Run(BaseModel):
    id: int
    decision_id: int
    status: str

@app.get("/health")
def health(): return {"ok": True}

@app.get("/profile/{username}")
def profile(username: str):
    return {"username": username, "avatar_url":"", "bio":"Explorer of superNova_2177.", "followers":2315, "following":1523, "status":"online"}

@app.post("/proposals", response_model=Proposal)
def create_proposal(p: ProposalIn):
    C["proposal"] += 1
    pid = C["proposal"]
    DB["proposals"][pid] = {"id":pid, **p.dict()}
    return DB["proposals"][pid]

@app.get("/proposals", response_model=List[Proposal])
def list_proposals():
    return list(sorted(DB["proposals"].values(), key=lambda x: x["id"], reverse=True))

@app.get("/proposals/{pid}/tally")
def tally(pid: int):
    up = sum(1 for v in DB["votes"] if v["proposal_id"]==pid and v["choice"]=="up")
    down = sum(1 for v in DB["votes"] if v["proposal_id"]==pid and v["choice"]=="down")
    return {"up":up,"down":down}

@app.post("/votes")
def add_vote(v: VoteIn):
    DB["votes"].append(v.dict()); return {"ok": True}

@app.post("/decide/{pid}", response_model=Decision)
def decide(pid: int, threshold: float = 0.6):
    t = tally(pid); total = t["up"]+t["down"]
    status = "rejected"
    if total>0 and (t["up"]/total)>=threshold: status = "accepted"
    C["decision"] += 1; did = C["decision"]
    DB["decisions"][did] = {"id":did, "proposal_id":pid, "status":status}
    return DB["decisions"][did]

@app.get("/decisions", response_model=List[Decision])
def list_decisions(): return list(sorted(DB["decisions"].values(), key=lambda x: x["id"], reverse=True))

@app.post("/runs", response_model=Run)
def create_run(decision_id: int):
    C["run"] += 1; rid = C["run"]
    DB["runs"][rid] = {"id":rid, "decision_id":decision_id, "status":"done"}  # simulate instant
    return DB["runs"][rid]

@app.get("/runs", response_model=List[Run])
def list_runs(): return list(sorted(DB["runs"].values(), key=lambda x: x["id"], reverse=True))
