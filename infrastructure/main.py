from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import uuid
import json
from datetime import datetime, timezone
import os

DB_PATH = os.environ.get("MC_DB_PATH", "/opt/mission-control/data/mc.db")
STATIC_PATH = os.environ.get("MC_STATIC_PATH", "/opt/mission-control/static")

app = FastAPI(title="Mission Control", version="1.0.0")

VALID_STATUSES = ["queued", "researching", "review", "producing", "in_market", "active", "archived"]
VALID_REL_TYPES = ["competitor", "peer", "parent", "subsidiary"]
VALID_ACTORS = ["agent_researcher", "agent_pov_writer", "agent_critic", "agent_sequencer", "jay", "prospect", "system"]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    schema = open(os.path.join(os.path.dirname(__file__), "schema.sql")).read()
    conn.executescript(schema)
    conn.commit()
    conn.close()

def now():
    return datetime.now(timezone.utc).isoformat()

def new_id():
    return str(uuid.uuid4())

# ── Models ────────────────────────────────────────────────────────────────────

class RunCreate(BaseModel):
    company_name: str
    initial_prompt: Optional[str] = None
    created_via: Optional[str] = "slack"
    play_assigned: Optional[str] = None
    industry_cluster: Optional[str] = None
    flagged: Optional[int] = 0
    ambiguity_note: Optional[str] = None

class RunUpdate(BaseModel):
    status: Optional[str] = None
    play_assigned: Optional[str] = None
    industry_cluster: Optional[str] = None
    flagged: Optional[int] = None
    ambiguity_note: Optional[str] = None

class ContactCreate(BaseModel):
    run_id: str
    name: Optional[str] = None
    role: Optional[str] = None
    seniority: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_primary: Optional[int] = 0

class RelationshipCreate(BaseModel):
    run_id_a: str
    run_id_b: str
    rel_type: Optional[str] = "competitor"
    auto_created: Optional[int] = 1

class EventCreate(BaseModel):
    run_id: str
    event_type: str
    actor: str
    content: Optional[str] = None
    quality_score: Optional[float] = None
    edit_delta: Optional[float] = None
    prompt_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    jay_annotation: Optional[str] = None

class SlackTrigger(BaseModel):
    company_name: str
    initial_prompt: str
    competitor_of: Optional[str] = None
    ambiguous: Optional[bool] = False
    ambiguity_note: Optional[str] = None

# ── Routes ────────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return FileResponse(os.path.join(STATIC_PATH, "index.html"))

@app.get("/health")
def health():
    return {"status": "ok", "time": now()}

# Board — full state for the kanban view
@app.get("/api/board")
def get_board():
    conn = get_db()
    runs = conn.execute("""
        SELECT r.*,
            (SELECT COUNT(*) FROM contact c WHERE c.run_id = r.id AND c.is_active = 1) as contact_count,
            (SELECT COUNT(*) FROM event e WHERE e.run_id = r.id) as event_count,
            (SELECT e.quality_score FROM event e WHERE e.run_id = r.id AND e.quality_score IS NOT NULL ORDER BY e.timestamp DESC LIMIT 1) as last_score,
            (SELECT e.event_type FROM event e WHERE e.run_id = r.id ORDER BY e.timestamp DESC LIMIT 1) as last_event_type,
            (SELECT e.timestamp FROM event e WHERE e.run_id = r.id ORDER BY e.timestamp DESC LIMIT 1) as last_event_at
        FROM prospect_run r
        WHERE r.status != 'archived'
        ORDER BY r.updated_at DESC
    """).fetchall()

    relationships = conn.execute("SELECT * FROM relationship").fetchall()
    conn.close()

    board = {s: [] for s in VALID_STATUSES if s != "archived"}
    rel_map = {}
    for rel in relationships:
        for key in [rel["run_id_a"], rel["run_id_b"]]:
            if key not in rel_map:
                rel_map[key] = []
            other = rel["run_id_b"] if key == rel["run_id_a"] else rel["run_id_a"]
            rel_map[key].append({"run_id": other, "rel_type": rel["rel_type"]})

    for run in runs:
        r = dict(run)
        r["relationships"] = rel_map.get(r["id"], [])
        status = r["status"]
        if status in board:
            board[status].append(r)

    return board

# Prospect runs
@app.get("/api/runs")
def list_runs(status: Optional[str] = None):
    conn = get_db()
    if status:
        runs = conn.execute("SELECT * FROM prospect_run WHERE status = ? ORDER BY updated_at DESC", (status,)).fetchall()
    else:
        runs = conn.execute("SELECT * FROM prospect_run ORDER BY updated_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in runs]

@app.post("/api/runs")
def create_run(body: RunCreate):
    conn = get_db()
    run_id = new_id()
    ts = now()
    conn.execute("""
        INSERT INTO prospect_run (id, company_name, status, play_assigned, created_via, initial_prompt,
            industry_cluster, flagged, ambiguity_note, created_at, updated_at)
        VALUES (?, ?, 'queued', ?, ?, ?, ?, ?, ?, ?, ?)
    """, (run_id, body.company_name, body.play_assigned, body.created_via, body.initial_prompt,
          body.industry_cluster, body.flagged, body.ambiguity_note, ts, ts))

    conn.execute("""
        INSERT INTO event (id, run_id, event_type, actor, timestamp, content)
        VALUES (?, ?, 'queued', 'system', ?, ?)
    """, (new_id(), run_id, ts, json.dumps({"initial_prompt": body.initial_prompt, "created_via": body.created_via})))

    conn.commit()
    conn.close()
    return {"id": run_id, "status": "queued"}

@app.get("/api/runs/{run_id}")
def get_run(run_id: str):
    conn = get_db()
    run = conn.execute("SELECT * FROM prospect_run WHERE id = ?", (run_id,)).fetchone()
    if not run:
        raise HTTPException(404, "Run not found")
    contacts = conn.execute("SELECT * FROM contact WHERE run_id = ? ORDER BY is_primary DESC", (run_id,)).fetchall()
    events = conn.execute("SELECT * FROM event WHERE run_id = ? ORDER BY timestamp ASC", (run_id,)).fetchall()
    rels = conn.execute("""
        SELECT r.*, p.company_name as other_company
        FROM relationship r
        JOIN prospect_run p ON (
            CASE WHEN r.run_id_a = ? THEN r.run_id_b ELSE r.run_id_a END = p.id
        )
        WHERE r.run_id_a = ? OR r.run_id_b = ?
    """, (run_id, run_id, run_id)).fetchall()
    conn.close()
    return {
        **dict(run),
        "contacts": [dict(c) for c in contacts],
        "events": [dict(e) for e in events],
        "relationships": [dict(r) for r in rels]
    }

@app.patch("/api/runs/{run_id}")
def update_run(run_id: str, body: RunUpdate):
    conn = get_db()
    run = conn.execute("SELECT id FROM prospect_run WHERE id = ?", (run_id,)).fetchone()
    if not run:
        raise HTTPException(404, "Run not found")
    if body.status and body.status not in VALID_STATUSES:
        raise HTTPException(400, f"Invalid status. Must be one of: {VALID_STATUSES}")
    fields = []
    values = []
    if body.status is not None:
        fields.append("status = ?")
        values.append(body.status)
    if body.play_assigned is not None:
        fields.append("play_assigned = ?")
        values.append(body.play_assigned)
    if body.industry_cluster is not None:
        fields.append("industry_cluster = ?")
        values.append(body.industry_cluster)
    if body.flagged is not None:
        fields.append("flagged = ?")
        values.append(body.flagged)
    if body.ambiguity_note is not None:
        fields.append("ambiguity_note = ?")
        values.append(body.ambiguity_note)
    if not fields:
        return {"status": "no changes"}
    fields.append("updated_at = ?")
    values.append(now())
    values.append(run_id)
    conn.execute(f"UPDATE prospect_run SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return {"status": "updated"}

# Contacts
@app.post("/api/contacts")
def create_contact(body: ContactCreate):
    conn = get_db()
    contact_id = new_id()
    conn.execute("""
        INSERT INTO contact (id, run_id, name, role, seniority, linkedin_url, is_primary, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
    """, (contact_id, body.run_id, body.name, body.role, body.seniority, body.linkedin_url, body.is_primary, now()))
    conn.commit()
    conn.close()
    return {"id": contact_id}

# Relationships
@app.post("/api/relationships")
def create_relationship(body: RelationshipCreate):
    conn = get_db()
    existing = conn.execute("""
        SELECT id FROM relationship
        WHERE (run_id_a = ? AND run_id_b = ?) OR (run_id_a = ? AND run_id_b = ?)
    """, (body.run_id_a, body.run_id_b, body.run_id_b, body.run_id_a)).fetchone()
    if existing:
        conn.close()
        return {"id": existing["id"], "status": "already_exists"}
    rel_id = new_id()
    conn.execute("""
        INSERT INTO relationship (id, run_id_a, run_id_b, rel_type, auto_created, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (rel_id, body.run_id_a, body.run_id_b, body.rel_type, body.auto_created, now()))
    conn.commit()
    conn.close()
    return {"id": rel_id}

# Events
@app.post("/api/events")
def create_event(body: EventCreate):
    conn = get_db()
    event_id = new_id()
    ts = now()
    conn.execute("""
        INSERT INTO event (id, run_id, event_type, actor, timestamp, content,
            quality_score, edit_delta, prompt_tokens, output_tokens, jay_annotation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (event_id, body.run_id, body.event_type, body.actor, ts,
          body.content, body.quality_score, body.edit_delta,
          body.prompt_tokens, body.output_tokens, body.jay_annotation))
    conn.execute("UPDATE prospect_run SET updated_at = ? WHERE id = ?", (ts, body.run_id))
    conn.commit()
    conn.close()
    return {"id": event_id}

# Slack trigger endpoint — called by the agent when it detects a company mention
@app.post("/api/slack/trigger")
def slack_trigger(body: SlackTrigger):
    conn = get_db()
    ts = now()

    # Check if company already exists
    existing = conn.execute(
        "SELECT id, status FROM prospect_run WHERE LOWER(company_name) = LOWER(?)",
        (body.company_name,)
    ).fetchone()

    if existing:
        conn.close()
        run_id = existing["id"]
        result = {"run_id": run_id, "status": "already_exists", "current_status": existing["status"]}
    else:
        run_id = new_id()
        conn.execute("""
            INSERT INTO prospect_run (id, company_name, status, created_via, initial_prompt,
                flagged, ambiguity_note, created_at, updated_at)
            VALUES (?, ?, 'queued', 'slack', ?, ?, ?, ?, ?)
        """, (run_id, body.company_name, body.initial_prompt,
              1 if body.ambiguous else 0, body.ambiguity_note, ts, ts))
        conn.execute("""
            INSERT INTO event (id, run_id, event_type, actor, timestamp, content)
            VALUES (?, ?, 'queued', 'system', ?, ?)
        """, (new_id(), run_id, ts, json.dumps({
            "initial_prompt": body.initial_prompt,
            "created_via": "slack",
            "ambiguous": body.ambiguous
        })))
        result = {"run_id": run_id, "status": "created"}

    # If this company is a competitor of another, create the relationship
    if body.competitor_of:
        parent = conn.execute(
            "SELECT id FROM prospect_run WHERE LOWER(company_name) = LOWER(?)",
            (body.competitor_of,)
        ).fetchone()

        if not parent:
            # Auto-create the parent company too
            parent_id = new_id()
            conn.execute("""
                INSERT INTO prospect_run (id, company_name, status, created_via, initial_prompt, created_at, updated_at)
                VALUES (?, ?, 'queued', 'slack', ?, ?, ?)
            """, (parent_id, body.competitor_of,
                  f"Auto-queued: competitor of {body.company_name}", ts, ts))
            conn.execute("""
                INSERT INTO event (id, run_id, event_type, actor, timestamp, content)
                VALUES (?, ?, 'queued', 'system', ?, ?)
            """, (new_id(), parent_id, ts, json.dumps({
                "auto_created": True,
                "reason": f"competitor of {body.company_name}"
            })))
            parent_id_val = parent_id
            result["parent_auto_created"] = body.competitor_of
        else:
            parent_id_val = parent["id"]

        # Create relationship (deduplicated)
        existing_rel = conn.execute("""
            SELECT id FROM relationship
            WHERE (run_id_a = ? AND run_id_b = ?) OR (run_id_a = ? AND run_id_b = ?)
        """, (run_id, parent_id_val, parent_id_val, run_id)).fetchone()

        if not existing_rel:
            conn.execute("""
                INSERT INTO relationship (id, run_id_a, run_id_b, rel_type, auto_created, created_at)
                VALUES (?, ?, ?, 'competitor', 1, ?)
            """, (new_id(), run_id, parent_id_val, ts))
            result["relationship_created"] = True

    conn.commit()
    conn.close()
    return result

# Stats for header
@app.get("/api/stats")
def get_stats():
    conn = get_db()
    counts = {}
    for status in VALID_STATUSES:
        if status != "archived":
            row = conn.execute(
                "SELECT COUNT(*) as c FROM prospect_run WHERE status = ?", (status,)
            ).fetchone()
            counts[status] = row["c"]
    review_count = counts.get("review", 0)
    total_active = sum(v for k, v in counts.items() if k != "archived")
    conn.close()
    return {"by_status": counts, "total_active": total_active, "review_pending": review_count}
