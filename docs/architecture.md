# Clawdbot — Architecture (Current State)

*Last updated: 2026-03-15. Reflects deployed state on VM102.*

---

## System overview

Clawdbot is a single-agent system with a structured memory layer. One OpenClaw instance on VM102 handles all sales agent tasks. The agent operates through Slack. Jay is the only user.

The pipeline is sequential: research → brief review → POV draft → POV review → outreach → Jay sends. No step proceeds without Jay's approval of the previous step's output.

---

## VM topology

```
Proxmox VE 9.1 host (MSI MAG B650, Ryzen 7 8700G, 64GB DDR5)
│
├── VM100 · Agent-100 · 192.168.0.100
│   Role: Personal assistant (offline only)
│   Model: Qwen via Ollama (VM101)
│   Internet: BLOCKED — Proxmox SDN enforced
│   Stack: OpenClaw, FastAPI (Mission Control HUD), SQLite
│   GPU: RTX 5070 Ti (PCIe passthrough — planned)
│   Note: Completely separate from sales agent pipeline
│
├── VM101 · Inference-101 · 192.168.0.110
│   Role: Ollama inference provider
│   Model: qwen3:14b (CPU phase) → qwen3.5:14b (post-passthrough)
│   Internet: BLOCKED — UFW default deny in/out
│   GPU: RTX 5070 Ti (dedicated, no passthrough yet)
│   Ollama: 0.0.0.0:11434
│   Allowed inbound: VM100, VM102, VM103 on port 11434
│
├── VM102 · Sandbox-102 · 192.168.0.120  ← PRIMARY FOCUS
│   Role: Sales agent (OpenClaw) + Mission Control
│   Model: Claude Sonnet 4.6 via Anthropic API
│   Internet: ENABLED (outbound unrestricted)
│   RAM: 24GB · Cores: 10
│   Services:
│     OpenClaw gateway:    port 18789
│     Mission Control:     port 18790
│
└── VM103 · Agent-Interface · 192.168.0.232
    Role: OpenWebUI host (temporary)
    Model: VM101 backend
    Internet: ENABLED
```

---

## VM102 service architecture

```
┌─────────────────────────────────────────────────────────┐
│  VM102 (192.168.0.120)                                  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  OpenClaw container (port 18789)                  │  │
│  │                                                   │  │
│  │  Runtime config:                                  │  │
│  │  - start-openclaw.sh builds config at startup     │  │
│  │  - Reads from clawdbot.json + .env                │  │
│  │                                                   │  │
│  │  Agent workspace (/root/clawd → workspace/)       │  │
│  │  - SOUL.md (loaded every session)                 │  │
│  │  - AGENTS.md (workspace operating rules)          │  │
│  │  - memory/ (17 markdown files)                    │  │
│  │  - skills/ (exa, mission-control)                 │  │
│  │                                                   │  │
│  │  Persistent config (/root/.openclaw → data/)      │  │
│  │  - clawdbot.json                                  │  │
│  │  - lcm.db (lossless-claw context)                 │  │
│  │  - extensions/lossless-claw/                      │  │
│  │                                                   │  │
│  │  Plugins:                                         │  │
│  │  - lossless-claw 0.3.0 (context management)       │  │
│  │  - slack (socket mode)                            │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Mission Control container (port 18790)           │  │
│  │                                                   │  │
│  │  FastAPI backend + SQLite                         │  │
│  │  - prospect_run table                             │  │
│  │  - contact table (child cards)                    │  │
│  │  - relationship table (competitor links)          │  │
│  │  - event table (full provenance log)              │  │
│  │                                                   │  │
│  │  Static HTML Kanban board                         │  │
│  │  6 columns: Queued → Researching → Review →       │  │
│  │             Producing → In Market → Active        │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Agent pipeline (current state)

All agents run as a single OpenClaw instance. The pipeline is task-based, not process-based — the same agent switches persona and loads different memory files depending on the task type.

```
Jay types in Slack
        │
        ▼
OpenClaw receives message
        │
        ├─ Loads SOUL.md (every session)
        ├─ Loads AGENTS.md (workspace rules)
        └─ Loads spine.md (identity core)
                │
                ▼
        Task detection
                │
       ┌────────┴────────┐
       │                 │
  Research task      POV/Outreach task
       │                 │
       ▼                 ▼
  Load calibration.md   Load pov.md + discovery.md
  Call Exa AI API       Load relevant context file
  Extract signals       Load assigned play
  Produce brief         Draft POV / outreach
       │                 │
       └────────┬────────┘
                │
                ▼
        Output to Slack
        Jay reviews
        Jay acts (approves / edits / sends)
```

---

## Memory architecture

```
workspace/memory/
│
├── README.md          ← Orchestrator routing rules (task_type → files to load)
├── spine.md           ← Identity core, always loaded (~150 lines, <6k chars)
│
├── modules/           ← Methodology — loaded by task type
│   ├── discovery.md        §3, §4, §4a, §4b
│   ├── qualification.md    §6
│   ├── pov.md              §7
│   ├── sales-cycle.md      §8
│   └── calibration.md      §9 — INTERNAL ONLY, never surfaces externally
│
├── contexts/          ← Specialist personas — loaded by persona
│   ├── sdr.md              §10f
│   ├── bdr.md              §10a
│   ├── ae-industry.md      §10b
│   ├── ae-geography.md     §10h
│   ├── hiring.md           §10c
│   ├── partner.md          §10d
│   ├── recruiter.md        §10e
│   └── field-marketer.md   §10g
│
└── plays/             ← Expansion plays and sub-vertical packs (flat, tagged)
    ├── expansion-data-analytics-2026.md      industries: all
    └── financial-planning-wealth-management.md  industries: fsi, fintech
```

**Loading rules:**
- `spine.md` — always loaded for any sales task
- `modules/` — loaded based on task type (see README.md routing table)
- `contexts/` — loaded based on persona (one per task)
- `plays/` — loaded based on Researcher signal match (Orchestrator selects)
- `calibration.md` — loaded for research tasks only, never surfaces in external output

---

## Lossless context management

```
Before lossless-claw (default OpenClaw):
Message 1, 2, 3 ... [context fills up] ... old messages DROPPED

After lossless-claw:
Message 1, 2, 3 ... [context threshold 75%] ... compress to summaries
Summaries stored in lcm.db (SQLite)
Agent can lcm_grep / lcm_describe / lcm_expand to recover detail
Nothing is lost
```

Config: `freshTailCount=32` · `contextThreshold=0.75` · `incrementalMaxDepth=-1`

---

## External integrations

| Service | Purpose | Access |
|---|---|---|
| Anthropic API | Claude Sonnet 4.6 — primary inference | VM102 outbound |
| Exa AI API | Prospect research — semantic search + full content | VM102 outbound |
| Slack | Primary interface — Jay ↔ agent | Socket Mode, xoxb + xapp tokens |
| Ollama (VM101) | Local inference fallback | LAN only, port 11434 |

**Exa API key locations:**
- `/opt/clawdbot/.env` — Docker environment variable
- `/opt/clawdbot/workspace/.env` — Read by Exa skill at runtime

---

## Mission Control data model

```
prospect_run          ← one row per company
  id, company_name, status, play_assigned
  created_via, initial_prompt (verbatim)
  flagged, ambiguity_note
  created_at, updated_at

contact               ← child of prospect_run, many per company
  id, run_id, name, role, seniority
  is_primary, is_active

relationship          ← many:many between prospect_runs
  id, run_id_a, run_id_b
  rel_type (competitor | peer | parent)
  auto_created

event                 ← append-only log, every action
  id, run_id, event_type, actor
  timestamp, content
  quality_score, edit_delta
  prompt_tokens, output_tokens
  jay_annotation
```

**Status flow:** queued → researching → review → producing → in_market → active

**Event actors:** agent_researcher · agent_pov_writer · agent_critic · agent_sequencer · jay · prospect · system

---

## Security posture

| Rule | Enforcement |
|---|---|
| VM100 internet blocked | Proxmox SDN firewall (not just UFW) |
| VM101 internet blocked | UFW default deny in/out |
| VM101 Ollama access | Allowlist: VM100, VM102, VM103 only |
| VM102 internet | Outbound unrestricted (web sandbox by design) |
| No agent sends email | Jay reviews all outreach, sends manually |
| No agent modifies soul.md or AGENTS.md | Read-only at runtime |
| Calibration content (§9) | Never surfaces in external output |
| API keys | `.env` files, not committed |
| Gateway token | Required for Control UI access |

---

## Planned — not yet built

**VM104 — Loop execution host**
Planned separate VM for Researcher, POV Writer, Critic, Sequencer. Currently all agents run on VM102. Migration happens after VM102 pipeline is stable and proven.

**Second GPU machine**
Ryzen 7 5700X3D (already owned), AM4 platform, ~$590 AUD additional parts. Second RTX 5070 Ti will run here. Enables dedicated GPU inference for both VMs simultaneously.

**Signal scoring layer**
Coverage × specificity scoring (financially material + timely + personally relevant) as a fast, auditable proxy metric for research quality. Multiplicative signal hypothesis: 1.5 × 1.5 = 2.25 > 1 + 1. To be instrumented once pipeline is running at volume.

**Additional sub-vertical packs**
Healthcare/life sciences, retail, manufacturing, CPG, tech. Financial Planning/Wealth Management pack exists. Template exists.
