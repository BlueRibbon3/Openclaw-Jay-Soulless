## → [Read the Problem Statement first](./Problem-Statement.md)

# Clawdbot — Jay's AI Sales Agent

**Status:** Live · VM102 · Slack · Claude Sonnet 4.6
**Last updated:** 2026-03-15

---

## What this is

Clawdbot is a personal AI sales agent system built on OpenClaw, running on a Proxmox homelab. It embodies Jay's sales methodology, voice, and approach — capable of handling outbound prospect research, POV generation, and multi-persona sales contexts.

The agent operates through Slack. Jay sends a message. The agent researches, reasons, drafts, and returns output. Nothing is sent to a prospect without Jay reviewing it first.

---

## What it does today

- **Prospect research** — Exa AI semantic search, signal extraction (growth, tech, exec, competitive), structured prospect brief
- **POV drafting** — builds Points of View grounded in Jay's methodology (soul.md §7), provocative question first, red team analysis included
- **Outreach sequences** — subject line, intro email, follow-up using prospect's own vocabulary
- **PDF generation** — research briefs and POVs exported as PDFs, sent directly in Slack
- **Channel creation** — creates a Slack channel per prospect
- **Mission Control** — Kanban pipeline board at `http://192.168.0.120:18790`
- **Lossless context** — lossless-claw plugin prevents conversation memory loss on long sessions

---

## Infrastructure

| VM | Role | IP | Model |
|---|---|---|---|
| VM100 | Personal Assistant (offline) | 192.168.0.100 | Qwen via Ollama |
| VM101 | Ollama inference | 192.168.0.110 | qwen3:14b (CPU phase) |
| VM102 | Sales Agent (OpenClaw) | 192.168.0.120 | Claude Sonnet 4.6 via API |
| VM103 | OpenWebUI (temporary) | 192.168.0.232 | — |

**Host:** Proxmox VE 9.1 · MSI MAG B650 Tomahawk · Ryzen 7 8700G · 64GB DDR5 · Dual RTX 5070 Ti 16GB

**VM102 key services:**
- OpenClaw gateway: port 18789
- Mission Control: port 18790
- Docker Compose: `/opt/clawdbot/`
- Mission Control: `/opt/mission-control/`

---

## How to bring it up from scratch

### Prerequisites
- VM102 running Ubuntu 24, Docker installed
- `/opt/clawdbot/` directory with files from this repository
- API keys in `/opt/clawdbot/.env`

### Required environment variables (`/opt/clawdbot/.env`)

```bash
# Claude API
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-sonnet-4-6

# Ollama fallback (VM101)
OPENAI_API_KEY=local-...
OPENAI_BASE_URL=http://192.168.0.110:11434/v1
OPENAI_MODEL=active-model

# Slack
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

# OpenClaw gateway
CLAWDBOT_GATEWAY_TOKEN=...

# Exa AI (in /opt/clawdbot/workspace/.env also)
EXA_API_KEY=...
```

### Start the agent

```bash
cd /opt/clawdbot
sudo docker compose up -d
```

### Start Mission Control

```bash
cd /opt/mission-control
sudo docker compose up -d
```

### Verify

```bash
# Agent
sudo docker compose -f /opt/clawdbot/docker-compose.yml logs --tail=20 | grep -E "slack|socket|model"

# Mission Control
curl -s http://localhost:18790/health
```

### Pair Slack DM

First time after a fresh start — send any message to the bot in Slack. You'll receive a pairing code. Approve it:

```bash
sudo docker compose -f /opt/clawdbot/docker-compose.yml exec openclaw clawdbot pairing approve slack [CODE]
```

---

## File structure on VM102

```
/opt/clawdbot/
  .env                          ← API keys and tokens (never commit)
  docker-compose.yml            ← OpenClaw container definition
  Dockerfile                    ← OpenClaw image (pinned to openclaw@2026.3.13)
  start-openclaw.sh             ← Startup script (builds config at runtime)
  openclaw.json.template        ← Base config template
  data/                         ← Persistent config (maps to /root/.openclaw)
    clawdbot.json               ← Active OpenClaw config
    agents/main/agent/
      models.json               ← Model definitions
    extensions/
      lossless-claw/            ← Context management plugin
  workspace/                    ← Agent workspace (maps to /root/clawd)
    SOUL.md                     ← Jay's sales identity (loaded every session)
    AGENTS.md                   ← Workspace operating rules
    soul.md                     ← Canonical reference (414 lines)
    .env                        ← Exa API key for skills
    memory/
      README.md                 ← Orchestrator routing rules
      spine.md                  ← Identity core (always loaded)
      modules/                  ← discovery, qualification, pov, sales-cycle, calibration
      contexts/                 ← sdr, bdr, ae-industry, ae-geography, hiring, partner, recruiter, field-marketer
      plays/                    ← expansion plays and sub-vertical packs
    skills/
      exa/                      ← Exa AI research skill
      mission-control/          ← Mission Control queue skill

/opt/mission-control/
  docker-compose.yml
  main.py                       ← FastAPI backend
  schema.sql                    ← SQLite schema
  data/
    mc.db                       ← Mission Control database
  static/
    index.html                  ← Kanban board UI
```

---

## Architecture overview

```
Jay (Slack)
    ↓
OpenClaw (VM102:18789)
    ↓ loads on every session
SOUL.md → spine.md → relevant modules + context
    ↓ when research needed
Exa AI API → prospect brief
    ↓ queues company
Mission Control API (VM102:18790)
    ↓ when POV needed
POV draft → Critic review → Jay approval
    ↓ when outreach needed
Outreach sequence → Jay sends
```

**Memory architecture (lossless-claw):**
- Session messages persist to SQLite (`lcm.db`)
- Older messages compress into summaries (DAG structure)
- Agent can search compacted history with `lcm_grep`
- Nothing is lost — raw messages always recoverable

---

## Key configuration rules

- **Never edit `clawdbot.json` or `models.json` while the container is running** — the startup script overwrites config on every start. Always `docker compose down` first.
- **`start-openclaw.sh` is the source of truth for runtime config** — many settings are injected by the startup script, not read from the JSON file directly. Changes to the JSON file alone may not take effect.
- **Rebuild required after editing `start-openclaw.sh`** — it's baked into the Docker image. Always use `docker compose up -d --build` after startup script changes.
- **`models.json` is regenerated from `clawdbot.json` on every start** — the Anthropic provider model list in `clawdbot.json` is the authoritative source.
- **Exa API key lives in two places** — `/opt/clawdbot/.env` (for the Docker environment) and `/opt/clawdbot/workspace/.env` (for skills to read at runtime).

---

## Soul.md — the identity document

`soul.md` is the canonical source of truth for Jay's sales methodology. 414 lines. All agent behaviour derives from it.

**Section map:**
- §1 Who I Am As a Seller
- §2 The Motion (expansion + net-new)
- §3 Pre-Call Prep
- §4 Discovery + §4a Question Toolkit + §4b Mutual Success Plan
- §5 Communication Style
- §6 Qualification
- §7 The POV
- §8 Sales Cycle
- §9 Calibration (internal only — never surfaces externally)
- §10a–§10h Specialist personas (BDR, SDR, Industry AE, Geography AE, Hiring Manager, Partner Manager, Recruiter, Field Marketer)
- Appendix A: Email templates

**Runtime loading:** The agent loads `SOUL.md` (uppercase) at session start per `AGENTS.md` instructions. `spine.md` is the condensed identity core (~150 lines) used for task-specific loading. Full soul.md is the human reference — spine.md and modules are what the agent loads at runtime.

---

## Slack app configuration

**Required bot token scopes:**
`chat:write` · `channels:history` · `channels:read` · `channels:manage` · `groups:history` · `groups:read` · `groups:write` · `im:history` · `im:read` · `im:write` · `reactions:write` · `users:read` · `files:write`

**Mode:** Socket Mode (no public URL required)
**Tokens:** `xoxb-` (bot token) + `xapp-` (app-level token for Socket Mode)

---

## Proxmox snapshots (VM102)

| Snapshot | Description |
|---|---|
| `slack-sonnet46-baseline` | Slack connected, claude-sonnet-4-6, Discord removed, soul.md + memory/ loaded |
| `memory-files-confirmed` | memory/ and soul.md confirmed accessible in workspace |
| `exa-skill-working` | Exa skill operational, full agent loop working |
| `full-pipeline-operational` | Full pipeline: identity + Exa research + POV instinct |
| `mission-control-live` | Mission Control deployed port 18790 |
| `pre-openclaw-update` | Before OpenClaw update from 2026.1.24-3 |
| `lossless-claw-installed` | OpenClaw 2026.3.13, lossless-claw 0.3.0 |
| `slack-files-write` | files:write + channels:manage + groups:write scopes |

---

## Open items

- [ ] Mission Control skill — agent not reliably calling it (LAN address resolution issue from inside container)
- [ ] Ralph induction cycle — first formal test of the full pipeline against synthetic prospect
- [ ] Additional sub-vertical packs — healthcare, retail, manufacturing, CPG
- [ ] VM104 — planned loop execution host for Researcher, POV Writer, Critic, Sequencer
- [ ] Second GPU machine — Ryzen 7 5700X3D, AM4 platform (~$590 AUD additional parts)
- [ ] Slash commands — deferred, to be configured in a later session
- [ ] Signal scoring layer — financially material + timely + personally relevant proxy metric
