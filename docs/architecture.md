# Clawdbot — Architecture (Current State)

*Last updated: 2026-03-16. Reflects deployed state on VM102.*
*Engineering preview — personal assistant infrastructure not included.*

---

## System overview

A single-agent system with a structured memory layer. One OpenClaw instance on VM102 handles all sales agent tasks. The agent operates through Slack. All outreach is reviewed and sent by the seller — the agent does the preparation, the seller exercises the judgment.

The pipeline is sequential: research → brief review → POV draft → POV review → outreach → seller sends. No step proceeds without the seller's approval of the previous step's output.

---

## Infrastructure

```
┌─────────────────────────────────────────────────────────┐
│  VM101 · Inference-101 · 192.168.0.110                  │
│                                                         │
│  Role: Ollama inference provider (local LLM)            │
│  Model: qwen3:14b → qwen3.5:14b (post-GPU)             │
│  Internet: BLOCKED — UFW default deny in/out            │
│  GPU: RTX 5070 Ti 16GB (dedicated)                      │
│  Ollama: 0.0.0.0:11434                                  │
│  Allowed inbound: VM102 only on port 11434              │
│                                                         │
│  Security note: internet-blocked by design.             │
│  Model ingestion: pull on VM102, scp to VM101 over LAN. │
│  No exceptions.                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  VM102 · Sandbox-102 · 192.168.0.120  ← PRIMARY        │
│                                                         │
│  Role: Sales agent + Mission Control                    │
│  Model: Claude Sonnet 4.6 (Anthropic API) primary       │
│         Ollama/Qwen (VM101) fallback                    │
│  Internet: ENABLED (outbound unrestricted)              │
│  RAM: 24GB · Cores: 10                                  │
│                                                         │
│  Services:                                              │
│    OpenClaw gateway:    port 18789                      │
│    Mission Control:     port 18790                      │
└─────────────────────────────────────────────────────────┘
```

---

## VM102 service architecture

```
┌───────────────────────────────────────────────────────┐
│  OpenClaw container (port 18789)                      │
│                                                       │
│  Runtime: start-openclaw.sh builds config at startup  │
│  Config: clawdbot.json + .env                         │
│                                                       │
│  Agent workspace (/root/clawd → workspace/)           │
│  - SOUL.md (loaded every session)                     │
│  - AGENTS.md (workspace operating rules)              │
│  - memory/ (spine + modules + contexts + plays)       │
│  - skills/ (exa, mission-control)                     │
│                                                       │
│  Persistent config (/root/.openclaw → data/)          │
│  - clawdbot.json                                      │
│  - lcm.db (lossless-claw context — SQLite)            │
│  - extensions/lossless-claw/                          │
│                                                       │
│  Plugins:                                             │
│  - lossless-claw 0.3.0 (context management)           │
│  - slack (socket mode)                                │
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│  Mission Control container (port 18790)               │
│                                                       │
│  FastAPI backend + SQLite                             │
│  - prospect_run table                                 │
│  - contact table (child cards per company)            │
│  - relationship table (competitor/peer links)         │
│  - event table (full provenance log)                  │
│                                                       │
│  Static HTML Kanban board                             │
│  Columns: Queued → Researching → Review →             │
│           Producing → In Market → Active              │
└───────────────────────────────────────────────────────┘
```

---

## Agent pipeline

All pipeline functions run as a single OpenClaw instance. The pipeline is task-based — the same agent switches persona and loads different memory files depending on the task type.

```
Seller types in Slack
        │
        ▼
OpenClaw receives message
        │
        ├─ Loads SOUL.md (every session)
        ├─ Loads AGENTS.md (workspace rules)
        └─ Loads spine.md (identity core)
                │
                ▼
        Task detection + purpose clarification
        (if purpose not stated, agent asks)
                │
       ┌────────┴────────┐
       │                 │
  Research task      POV/Outreach task
       │                 │
       ▼                 ▼
  Load calibration.md   Load pov.md + discovery.md
  Run Exa AI queries    Load relevant context file
  Score signals         Load assigned play
  Produce brief         Draft POV / outreach
       │                 │
       └────────┬────────┘
                │
                ▼
        Output to Slack
        Seller reviews
        Seller acts (approves / edits / sends)
```

---

## Memory architecture

```
workspace/memory/
│
├── README.md          ← Orchestrator routing rules
├── spine.md           ← Identity core (~150 lines, always loaded)
│
├── modules/           ← Methodology — loaded by task type
│   ├── discovery.md
│   ├── qualification.md
│   ├── pov.md
│   ├── sales-cycle.md
│   └── calibration.md    ← internal only, never surfaces externally
│
├── contexts/          ← Specialist personas — loaded by persona
│   ├── bdr.md, sdr.md, ae-industry.md, ae-geography.md
│   └── hiring.md, partner.md, recruiter.md, field-marketer.md
│
└── plays/             ← Expansion plays and sub-vertical packs
    └── [tagged with YAML frontmatter, flat structure]
```

**Loading principle:** spine.md always loads. Modules load by task type. Contexts load by persona. Plays load by signal match. Calibration loads for research tasks only and never surfaces in external output.

---

## Lossless context management

```
Default OpenClaw (before lossless-claw):
Messages 1–N ... [context fills] ... old messages DROPPED

With lossless-claw:
Messages 1–N ... [75% threshold] ... compress to summaries → lcm.db
Agent can lcm_grep / lcm_describe / lcm_expand to recover detail
Nothing is lost. Raw messages always recoverable.
```

OOLONG benchmark: lossless-claw 74.8 vs Claude Code 70.3. Gap widens with context length.

Config: `freshTailCount=32` · `contextThreshold=0.75` · `incrementalMaxDepth=-1`

---

## Mission Control data model

```
prospect_run          ← one row per company
  id, company_name, status, play_assigned
  created_via, initial_prompt (verbatim — training signal)
  flagged, ambiguity_note

contact               ← child of prospect_run, many per company
  id, run_id, name, role, seniority, is_primary

relationship          ← many:many between prospect_runs
  id, run_id_a, run_id_b
  rel_type (competitor | peer | parent)
  auto_created

event                 ← append-only log, every action
  id, run_id, event_type, actor
  timestamp, content
  quality_score       ← Critic score where applicable
  edit_delta          ← % of output seller changed
  prompt_tokens, output_tokens
  jay_annotation      ← seller's qualitative note
```

**Status flow:** queued → researching → review → producing → in_market → active

**The event log is the training dataset.** Every research run, every POV draft, every edit the seller makes is captured. Over time this answers: does initial prompt quality correlate with brief quality? Does edit delta trend down as the agent improves? Which signal types produce the most engagement?

---

## External integrations

| Service | Purpose | Direction |
|---|---|---|
| Anthropic API | Claude Sonnet 4.6 — primary inference | VM102 outbound |
| Exa AI | Prospect research — semantic search + full content | VM102 outbound |
| Slack | Primary interface — seller ↔ agent | Socket Mode |
| Ollama (VM101) | Local inference fallback | LAN only |

---

## Signal quality system (in progress)

A structured framework for classifying every source the Researcher touches.

**Six signal types:**
1. Leadership & Talent
2. Financial & Commercial
3. Strategic & Operational
4. Market & Competitive
5. Customer & Reputation
6. Regulatory & Compliance

**Four research purposes:**
1. Outreach trigger — find one timely reason to make contact
2. POV research — full six-signal sweep, language extraction, provocative question hypothesis
3. Account background — orient before a meeting or handoff
4. Competitive context — understand the landscape around a prospect

**Scoring model:**
```
Signal value = Credibility × Timeliness × Personal relevance
```
A signal that is financially material (High) + timely (0-30 days) + personally relevant (mentions the exec you're meeting) scores 1.5 × 1.5 × 1.5 = 3.375 vs a one-dimensional signal scoring 1.5 × 1.0 × 1.0 = 1.5. The difference between a brief built on three-dimensional signals and one built on one-dimensional signals is the thing worth instrumenting.

**Purpose-first protocol:** the agent always clarifies research purpose before running. If purpose is not stated, the agent asks. Scope, depth, and token budget are set by purpose declaration.

---

## Security posture

| Rule | Enforcement |
|---|---|
| VM101 internet blocked | UFW default deny in/out |
| VM101 Ollama access | VM102 only on port 11434 |
| VM102 internet | Outbound unrestricted (web sandbox by design) |
| No agent sends externally | Seller reviews all outreach, sends manually |
| Calibration content | Never surfaces in external output |
| API keys | `.env` files only, never committed |

---

## Planned — not yet built

**VM104 — Loop execution host**
Planned separate VM for dedicated pipeline agent instances (Researcher, POV Writer, Critic, Sequencer). Currently all on VM102. Migration after VM102 pipeline is stable and proven at volume.

**Signal scoring instrumentation**
Coverage × specificity scoring built into Mission Control event log. Fast auditable proxy metric: financially material + timely + personally relevant. Multiplicative hypothesis: 1.5 × 1.5 = 2.25 > 1 + 1 = 2.

**Additional sub-vertical packs**
Healthcare/Life Sciences, Retail, Manufacturing, CPG, Technology. Financial Planning/Wealth Management exists. Template exists.
