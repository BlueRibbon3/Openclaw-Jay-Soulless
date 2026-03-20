# CHANGELOG

*Architecture decisions, methodology decisions, and significant milestones.*
*Proprietary methodology content and internal calibration decisions are not included in this preview.*
*Most recent first.*

---

## 2026-03-16 — System prompt generation

**Eight persona system prompts generated** from soul.md. Self-contained format (Option A) — each prompt works as a standalone system prompt without requiring the memory directory. Covers: BDR, SDR, Industry AE, Geography AE, Hiring Manager, Partner Manager, Recruiter, Field Marketer.

**Triangulation posture added** to all eight system prompts and soul.md §5. Core principle: before producing any output, answer two questions — what is this for, and who is the primary audience and what frame are they bringing? This principle is the root of the product-name discipline, language extraction methodology, and upfront contract. It is encoded in every persona.

---

## 2026-03-15 — Infrastructure, context management, repository

**OpenClaw updated: 2026.1.24-3 → 2026.3.13**
Package renamed from `clawdbot` to `openclaw` on npm. Dockerfile updated. Breaking changes handled: new config directory (`/root/.openclaw`), Control UI origin policy, startup script updates.

**lossless-claw 0.3.0 installed**
DAG-based lossless context management. Replaces OpenClaw's default sliding-window truncation. Old messages compress to summaries in `lcm.db` (SQLite). Agent can search compacted history with `lcm_grep`. Config: `freshTailCount=32`, `contextThreshold=0.75`, `incrementalMaxDepth=-1`. In the OOLONG benchmark, lossless-claw scored 74.8 vs Claude Code's 70.3 on long-context tasks — and the gap widens as context length increases.

**Mission Control v1 deployed — port 18790**
FastAPI + SQLite + single-file HTML Kanban board. Six columns: Queued → Researching → Review → Producing → In Market → Active. Four-table schema: `prospect_run`, `contact`, `relationship`, `event`. Event log captures full provenance — actor, content, quality score, edit delta, Jay's annotation. Competitor auto-queue: when a prospect is mentioned as a competitor, both are queued and linked automatically. Contacts are child cards per company.

**Slack scopes expanded**
Added: `channels:manage`, `groups:write`, `files:write`. Agent creates Slack channels and uploads PDFs directly in conversation.

**maxTokens increased: 8192 → 16000**
Previous limit was truncating long outputs.

**Private GitHub repository created**
All agent files, infrastructure, and documentation version-controlled. Two-machine access: VM102 (push/pull) and MacBook (clone).

**README, architecture.md, CHANGELOG written**
Documentation baseline established.

---

## 2026-03-14 — First live deployment

**Sales agent deployed to VM102 — first live session**
OpenClaw container up, Slack connected, sales identity loaded, agent responding correctly.

**Communication layer: Discord → Slack**
Switched before first live deployment. Reason: Slack is the professional default for the target use case. All config and documentation updated.

**Model: all pipeline agents → Claude API first**
Decision: run all agents on Claude API (claude-sonnet-4-6) to establish a quality baseline before migrating individual agents to local LLM. Local LLM migration happens per agent after the induction cycle confirms output quality.

**Research tool: Brave API → Exa AI**
Exa chosen for agent research use case. Reasons: semantic search vs keyword search, `contents` mode returns full cleaned page text in one call, person-specific and company-specific query modes, `findSimilar` for competitor research. Brave is a traditional search API. Exa is purpose-built for LLM agents.

**Config management discipline established**
The startup script (`start-openclaw.sh`) rewrites config on every container start. Editing `clawdbot.json` alone does not persist some settings. Correct workflow: edit `.env` for runtime-injected values, edit `start-openclaw.sh` for structural config, use Python scripts for JSON edits to avoid syntax errors.

**Memory directory deployed**
17 markdown files in `/opt/clawdbot/workspace/memory/`. Routing rules in `memory/README.md`. OpenClaw's own `memory/main.sqlite` coexists without conflict.

**First real prospect brief produced**
TLC (The Living Company). Agent: disambiguated two TLC entities, ran Exa research, identified Aveo acquisition ($3.85B), CIO departure post-acquisition as timing signal, tech stack inferred from job listings. Correct why-now framing generated without prompting.

---

## 2026-03-13 — Memory architecture and induction system

**Memory refactor — spine/modules/contexts architecture**
soul.md preserved as canonical reference. Three derived layers: `spine.md` (always loaded), `modules/` (by task type), `contexts/` (by persona).

**Plays directory: flat structure with frontmatter tagging**
All plays visible to all agents. Relevance determined by YAML tag matching, not folder location. Signal matching is semantic proximity, not exact string match.

**`clarification_request` formalised as task type**
Sub-agents raise structured clarification requests rather than guessing when context is insufficient. Orchestrator resolves or escalates.

**Agent induction system built**
Three documents: operational checklist (5 stages), prompt library (24 reusable test prompts with 0/1/2 scoring), synthetic prospect scenario (Meridian Fleet Solutions, 3-session mock cycle). The induction cycle is the mechanism for validating agent behaviour before live use.

---

## 2026-03-12 — Methodology documentation

**soul.md core sections drafted**
§1 Identity, §2 Motion, §3 Pre-call, §4 Discovery, §4a Question Toolkit, §4b Mutual Success Plan, §5 Communication Style, §6 Qualification, §7 POV, §8 Sales Cycle.

**POV methodology defined**
Build backwards from the provocative question. Five-point structure: customer's world → validate existing → gap as opportunity → concrete and specific → aspiration not ask. What a POV must never do: name product before problem, tell customer what is wrong with their business, use generic language, end with a feature list.

**Expansion play created**
`expansion-data-analytics-2026.md` — data and analytics drag pattern. In scope for all industries. Opening question, Agentforce angle, signal indicators for Researcher, provocative question for POV Writer.

**Financial Planning / Wealth Management sub-vertical pack**
First industry pack created. 12 sections covering regulatory environment, consolidation dynamics, demographic tailwind, key personas and language.

---

## 2026-03-10 — Architecture and initial infrastructure

**VM topology confirmed**
- VM101 (192.168.0.110): Ollama inference, internet-blocked by UFW, GPU passthrough active
- VM102 (192.168.0.120): Sales agent (OpenClaw), web-enabled, Claude API primary

**OpenClaw on VM102 — first working pipeline**
Root cause of initial failure: API type mismatch (`openai-responses` → `openai`). Fixed by switching to correct API type and Qwen 14B via active-model alias.

**Agent loop task schema v1**
Task object fields: `task_type`, `prospect_id`, `persona`, `context` (modules, context_file, play), `review_required`. Task type taxonomy: `prospect_research`, `pov_draft`, `pov_critique`, `outreach_sequence`, `discovery_prep`, `qualification_review`, `stage_progression`.

**Primary model decision: Claude API for reasoning-intensive tasks**
POV generation and critique require sophisticated reasoning. Local LLM handles structured extraction (Researcher) and templated outbound (Sequencer) after quality baseline is established.

**Agent architecture: single agent on VM102, VM104 future state**
All pipeline functions (Orchestrator, Researcher, POV Writer, Critic, Sequencer) run as a single OpenClaw instance on VM102. VM104 is planned as a dedicated loop execution host — migration after VM102 pipeline is stable and proven.

---

## Ongoing principles

- **The methodology document is the dependency.** Everything downstream is blocked until it is complete.
- **No agent sends externally without seller review.** All outreach is reviewed and sent manually.
- **Calibration content is internal only.** Never surfaces in any customer-facing output.
- **Qualify out fast.** Time is the resource most protected.
- **Problem first, never product first.** No product named before the problem is established.
- **Config editing discipline on VM102.** Always edit config only when the container is down.
