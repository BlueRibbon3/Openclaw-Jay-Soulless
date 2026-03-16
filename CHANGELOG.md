# CHANGELOG

*Decisions, architecture changes, and significant milestones. Most recent first.*
*Format: date · what changed · why.*

---

## 2026-03-15 — Session 5 (this session)

**OpenClaw updated: 2026.1.24-3 → 2026.3.13**
Required for lossless-claw plugin. Package renamed from `clawdbot` to `openclaw` on npm. Dockerfile updated to `npm install -g openclaw@2026.3.13`. Startup script updated to use `openclaw` binary.

**lossless-claw 0.3.0 installed**
DAG-based lossless context management plugin. Replaces OpenClaw's default sliding-window truncation. Old messages compress to summaries in `lcm.db` (SQLite). Agent can search compacted history with `lcm_grep`. Config: `freshTailCount=32`, `contextThreshold=0.75`, `incrementalMaxDepth=-1`. Addresses the context wall Jay hit in live use.

**Mission Control v1 deployed — VM102 port 18790**
FastAPI + SQLite + single-file HTML Kanban board. Six columns: Queued → Researching → Review → Producing → In Market → Active. Four-table schema: `prospect_run`, `contact`, `relationship`, `event`. Event log captures full provenance — actor, content, quality score, edit delta, Jay's annotation. Competitor auto-queue: when Jay mentions "Zip Money is a competitor to Afterpay", both are queued and linked. Contacts are child cards, not on the card face.

**Slack scopes expanded**
Added: `channels:manage`, `groups:write`, `files:write`. Agent can now create Slack channels and upload PDFs directly in conversation. New bot token generated post-reinstall.

**maxTokens increased: 8192 → 16000**
Previous limit was causing long responses to truncate mid-output, creating the appearance of context loss. Updated in `models.json` Anthropic provider section.

**historyLimit: confirmed at OpenClaw default (50)**
`historyLimit` is a Slack channel config property, not an agent default. OpenClaw default of 50 is sufficient. Previous attempt to set it in `agents.defaults` caused a config crash — invalid key location.

**OpenClaw 2026.3.13 breaking changes handled:**
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback = true` required for non-loopback Control UI (added to `start-openclaw.sh`)
- Volume mount updated: `./data:/root/.clawdbot` → `./data:/root/.openclaw` (new version config dir)
- `plugins.allow` set to `['lossless-claw']` to suppress auto-load warning

**AGENTS.md updated**
Replaced default OpenClaw AGENTS.md with Clawdbot-specific version covering: memory/ directory structure, task routing rules, clarification_request pattern, Exa AI research instructions, and platform formatting rules.

**Exa API key path corrected**
Key lives in two places: `/opt/clawdbot/.env` (Docker env) and `/opt/clawdbot/workspace/.env` (skill runtime). Previous attempts put it only in one location, causing the agent to report it as missing.

**Exa skill updated from JavaScript to SKILL.md**
Original `index.js` approach was incompatible with OpenClaw's skill model (ClawHub markdown-based skills). Replaced with `SKILL.md` containing curl-based Exa API commands the agent executes directly.

**Documentation sweep**
Three HTML documents (agent-loop-guide, sales-proving-ground, task-schema-spec) updated with visible decision log banners noting: Slack replaces Discord, Exa replaces Brave, Claude API primary for all agents, VM104 future state.

**Agent access profiles rebuilt — v3**
Two-part document: pipeline agent profiles (Orchestrator, Researcher, POV Writer, Critic, Sequencer, VM100 PA) and persona context profiles (8 personas). All agents updated to Claude API as starting model. Exa replaces Brave throughout. `clarification_request` added as formal capability.

---

## 2026-03-14 — Session 4 (deployment session)

**Clawdbot deployed to VM102 — first live session**
OpenClaw container up, Slack connected, soul.md loaded, agent responding as Jay.

**Communication layer: Discord → Slack**
Discord was the original interface. Switched to Slack before first live deployment. Reason: Jay uses Slack professionally (AU Sales Team workspace). All config, documentation, and access profiles updated to reflect Slack.

**Model: all pipeline agents → Claude API first**
Decision: run all agents on Claude API (claude-sonnet-4-6) to establish quality baseline before migrating to local LLM (Qwen). Local LLM migration happens per agent after induction cycle confirms output quality. Sequencer was previously planned as Qwen-only — changed.

**Research tool: Brave API → Exa AI**
Exa chosen over Brave for agent use case. Reasons: semantic search vs keyword search, `contents` mode returns full cleaned page text in one call, person-specific and company-specific query modes, `findSimilar` for competitor calibration. Brave is a traditional search API; Exa is purpose-built for LLM agents.

**Gateway 1008 error resolved**
Root cause: dashboard connecting without gateway token. Fix: open `http://192.168.0.120:18789/?token=[gateway-token]` in browser.

**clawdbot.json source of truth established**
The startup script (`start-openclaw.sh`) rewrites config on every container start from `.env` variables. Editing `clawdbot.json` alone does not persist for some settings. The correct workflow: edit `.env` for runtime-injected values; edit `start-openclaw.sh` for structural config; use Python scripts (not nano) for JSON edits to avoid syntax errors.

**models.json rewrite pattern established**
`models.json` gets regenerated from `clawdbot.json`'s models provider section on every start. To change models: update `clawdbot.json` providers section. `models.json` edits alone do not survive restart.

**Memory directory structure deployed**
17 markdown files placed in `/opt/clawdbot/workspace/memory/`. Initial placement error: files went to `./data/` (config mount) instead of `./workspace/` (workspace mount). Corrected. OpenClaw's own `memory/main.sqlite` coexists in the same directory without conflict.

**soul.md deployed as SOUL.md**
AGENTS.md instructs the agent to load `SOUL.md` (uppercase) at session start. Our `soul.md` was renamed to match. Default OpenClaw `SOUL.md` renamed to `SOUL-default.md`.

**Exa live search confirmed working**
Agent researched The Living Company (TLC), Nearmap, and REST Super without explicit bash command prompting. Auto-runs Exa via `AGENTS.md` instruction. Research quality confirmed — CIO departure signal identified for TLC/Aveo, correct why-now framing generated.

**First real prospect brief produced**
TLC (The Living Company) research session. Agent: disambiguated two TLC entities and flagged for Jay, ran Exa research, identified Aveo acquisition ($3.85B), CIO departure post-acquisition as timing signal, tech stack inferred from job listings. Ended with correct POV instinct.

**Mission Control skill installed**
`/opt/clawdbot/workspace/skills/mission-control/SKILL.md` installed. LAN address corrected from `localhost:18790` to `192.168.0.120:18790`. Agent confirmed able to reach Mission Control from inside container via LAN IP.

---

## 2026-03-13 — Session 3 (soul.md completion + memory refactor)

**soul.md completed — all sections**
Sections 10f (SDR), 10g (Field Marketer), 10h (Geography AE) drafted. §9 reframed as internal agent calibration material — not customer-facing stories but internal reasoning patterns and signal-weighting heuristics. First calibration entry: "Not every dollar is equal" (Prospa story).

**memory/ refactor — Option B directory structure**
soul.md preserved as complete canonical reference. Three derived layers created: `spine.md` (identity core, always loaded), `modules/` (methodology by task type), `contexts/` (personas). All 17 files built and validated.

**Plays directory: flat structure, no subdirectories**
Original design had `plays/sub-vertical/` subdirectory. Changed to flat `plays/` directory with frontmatter tagging schema. Reason: sub-vertical packs are not a separate category from plays — they are reference context loaded alongside plays. All plays visible to all agents; relevance determined by tags, not folder location.

**Play frontmatter tagging schema defined**
Fields: `title`, `type` (play|sub-vertical-pack), `industries` (all|list), `use_cases`, `personas`, `signals`, `updated`, `review`. Signal matching is semantic proximity not exact match. `industries: all` means in-scope for every account.

**`clarification_request` formalised as task type**
Sub-agents do not guess when context is insufficient. They raise a structured `clarification_request` object. Orchestrator resolves or escalates to Jay via Slack. If Jay's answer requires new research, Orchestrator dispatches scoped `prospect_research` task to Researcher. Added to README.md routing table, induction checklist (item 0.12), and prompt library (IP-2d.5).

**memory/README.md — Orchestrator routing reference**
Single file containing: directory structure, what each bucket contains, plays tagging schema, routing table (task_type → files to load), play selection rules, clarification_request section, what agents must never do, portability note.

**Agent induction system built**
Three documents: `agent-induction-checklist.md` (5-stage operational checklist), `agent-induction-prompt-library.md` (24 reusable test prompts, 0/1/2 scoring), `agent-induction-ralph-scenario.md` (synthetic prospect Meridian Fleet Solutions, 3-session mock cycle).

**Agent access profiles v1 built**
Pipeline agents (Orchestrator, Researcher, POV Writer, Critic, Sequencer) with internet access, model, file access, tool capabilities documented. Confirmed: Researcher is the only agent with internet access.

**Customer stories retrieval instruction added**
§2 and §3 updated: `salesforce.com/customer-stories` as canonical entry point, resilient retrieval via `site:salesforce.com customer stories [industry]`. Do not hardcode deep links — sub-paths change.

---

## 2026-03-12 — Session 2 (soul.md core sections)

**soul.md sections 1–8 drafted**
§1 Who I Am, §2 The Motion, §3 Pre-Call Prep, §4 Discovery, §4a Question Toolkit, §4b Mutual Success Plan, §5 Communication Style, §6 Qualification, §7 The POV, §8 Sales Cycle. 1,048 lines total.

**§8 Sales Cycle — eight stages defined**
Stage 1 Identifying Opportunity through Stage 8 Closed Won. Dead outcomes: Lost, No Decision, No Opportunity. BANT as Stage 1 threshold only — not a replacement for MSP.

**§7 The POV — provocative question first principle**
Every POV built backwards from the provocative question. Five-point structure: customer's world → validate existing → gap as opportunity → concrete and specific → aspiration not ask. What a POV must never do: name product before problem, list features, end with a close.

**§6 Qualification — continuous, not a gate**
Primary disqualification filters documented. Two political account plays: find the next necessary project, find someone senior and make them a hero. Qualifying out language defined.

**§5 CBUS principle established**
Single correct word — *members* not *customers* — established credibility that no slide deck could manufacture. Language extraction before first meeting is non-negotiable.

**First expansion play created**
`expansion-data-analytics-2026.md` — data and analytics drag pattern. `industries: all`. Opening question: "What is the most widely used application in your business?" Semantic layer angle for Agentforce. Signal indicators for Researcher. Provocative question for POV Writer.

**Financial Planning / Wealth Management sub-vertical pack**
12-section pack covering FOFA reforms, consolidation, demographic tailwind, trust deficit. Personas: CEO/MD, Operations/COO, Revenue/BD. Statistics sourced from 2018–2019 materials — flagged for verification before live use.

---

## 2026-03-10 — Session 1 (architecture and infrastructure)

**VM topology confirmed**
Four VMs: VM100 (local assistant), VM101 (Ollama inference), VM102 (sales agent/web), VM103 (OpenWebUI). VM101 internet-blocked by design — only correct workflow is pull models on VM102, scp to VM101 over LAN.

**OpenClaw on VM102 — first working pipeline**
Discord ↔ Clawdbot ↔ Ollama pipeline working. Root cause of initial failure: API type mismatch (`openai-responses` → `openai`), model tool-calling issues with qwen2.5:7b, session history accumulation. Fixed by switching to qwen2.5:14b via active-model alias.

**Dual RTX 5070 Ti installation complete**
PCIe lane limitation identified: Ryzen 7 8700G has 16 CPU PCIe lanes, M2_2/PCIE2 lane sharing prevents second GPU passthrough on current machine. Decision: single GPU passthrough to VM101 on current machine; second GPU planned for a second machine built around Ryzen 7 5700X3D (AM4, already owned).

**Three-tier memory architecture established**
Tier 1: Session RAM (historyLimit:5 — later revised). Tier 2: Compressed session summaries (recent-context.md, 14-day TTL). Tier 3: Long-term facts (/memory/facts/, no TTL, promoted nightly). SQLite backend until ~200 entities.

**Agent loop task schema v1**
Task object fields: task_type, prospect_id, persona, context (modules, context_file, play), review_required, few_shot_ref. task_type taxonomy: prospect_research, pov_draft, pov_critique, outreach_sequence, discovery_prep, qualification_review, stage_progression.

**Primary model decision: Claude API for POV Writer and Critic**
Soul.md makes clear POV generation requires sophisticated reasoning. Qwen2.5-coder:32b cannot reliably execute the provocative question structure, red-team analysis, language extraction, and five-point structure. Claude API confirmed for POV Writer and Critic. Qwen handles Researcher (structured extraction) and Sequencer (templated outbound) — later revised to Claude API for all agents initially.

**Sales agent architecture — four sub-agents on VM104**
Orchestrator (Jay/Claude API/VM102), Researcher (Qwen/VM104), POV Writer (Claude API/VM104), Critic (Claude API/VM104), Sequencer (Qwen/VM104). Later revised: all on VM102 for initial deployment, VM104 as future migration target.

**No Industry Specialist sub-agent at this stage**
Researcher validates sub-vertical pack statistics at start of any run that loads a pack. Industry depth comes from the pack + AE context file, not a dedicated specialist agent.

---

## Ongoing principles (never overridden)

- **soul.md is the dependency.** Everything downstream is blocked until soul.md is complete.
- **VM separation is non-negotiable.** VM100 offline. VM101 offline. VM102 web-enabled. VM100 and VM102 never share data.
- **No agent sends externally without Jay review.** All outreach Jay reviews and sends manually.
- **Calibration (§9) is internal only.** Never surfaces in any customer-facing output.
- **Qualify out fast.** Time is the resource most protected. Willingness to solve is the primary filter.
- **Problem first, never product first.** No product named before the problem is established.
- **config editing discipline on VM102.** Always edit `clawdbot.json` and `models.json` only when the container is DOWN. Use Python scripts, not nano, for JSON edits.
