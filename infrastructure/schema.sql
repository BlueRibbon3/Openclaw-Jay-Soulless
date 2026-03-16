CREATE TABLE IF NOT EXISTS prospect_run (
    id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued',
    play_assigned TEXT,
    created_via TEXT DEFAULT 'slack',
    initial_prompt TEXT,
    industry_cluster TEXT,
    flagged INTEGER DEFAULT 0,
    ambiguity_note TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS contact (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES prospect_run(id),
    name TEXT,
    role TEXT,
    seniority TEXT,
    linkedin_url TEXT,
    is_primary INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS relationship (
    id TEXT PRIMARY KEY,
    run_id_a TEXT NOT NULL REFERENCES prospect_run(id),
    run_id_b TEXT NOT NULL REFERENCES prospect_run(id),
    rel_type TEXT NOT NULL DEFAULT 'competitor',
    auto_created INTEGER DEFAULT 1,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS event (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES prospect_run(id),
    event_type TEXT NOT NULL,
    actor TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    content TEXT,
    quality_score REAL,
    edit_delta REAL,
    prompt_tokens INTEGER,
    output_tokens INTEGER,
    jay_annotation TEXT
);

CREATE INDEX IF NOT EXISTS idx_event_run ON event(run_id);
CREATE INDEX IF NOT EXISTS idx_contact_run ON contact(run_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationship(run_id_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationship(run_id_b);
CREATE INDEX IF NOT EXISTS idx_run_status ON prospect_run(status);
