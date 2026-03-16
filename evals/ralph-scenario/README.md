# memory/ — Directory Guide and Agent Routing Rules

*Last updated: 2026-03. Maintained by: Jay / Orchestrator.*
*This file is loaded by the Orchestrator at task intake. It is the authoritative routing reference.*
*Do not hardcode file paths in sub-agent system prompts — derive them from this document.*

---

## Directory structure

```
memory/
  README.md                          ← this file. Orchestrator loads always.
  spine.md                           ← identity core. All agents load always.
  modules/
    discovery.md                     ← §3, §4, §4a, §4b
    qualification.md                 ← §6
    pov.md                           ← §7
    sales-cycle.md                   ← §8
    calibration.md                   ← §9 (internal only — never surfaces externally)
  contexts/
    sdr.md                           ← §10f
    bdr.md                           ← §10a
    ae-industry.md                   ← §10b
    ae-geography.md                  ← §10h
    hiring.md                        ← §10c
    partner.md                       ← §10d
    recruiter.md                     ← §10e
    field-marketer.md                ← §10g
  plays/
    [all plays and sub-vertical packs — flat, tagged]
```

**Source of truth:** All content derives from soul.md (preserved separately as the complete reference document). Do not edit module or context files directly — edit soul.md and regenerate.

---

## What each bucket contains

**spine.md** — Who Jay is, core operating principles, 80/20 posture, upfront contract, POV philosophy in brief, customer stories retrieval instruction, agent loading rules. Under 150 lines. The identity that persists across every task.

**modules/** — Methodology. How to do the work. Loaded based on what the task requires, not what the persona is.

**contexts/** — Specialist personas. How to think and operate from a specific role. Loaded based on who the agent is acting as for this task.

**plays/** — All plays and sub-vertical packs in a single flat directory. Tagged for relevance. Loaded based on signal match from the Researcher's brief. Every play is visible to every agent — relevance is determined by tags, not by folder location. Plays evolve continuously as technology, markets, and sentiment shift.

---

## The plays/ tagging schema

Every file in plays/ carries a frontmatter header using this schema:

```yaml
---
title:        [human-readable title]
type:         play | sub-vertical-pack
industries:   all | [comma-separated list: fsi, healthcare, retail, manufacturing, cpg, tech, fintech, superannuation, insurance, ...]
use_cases:    [comma-separated list: data-analytics, ai-readiness, crm-expansion, personalisation, field-service, ...]
personas:     [comma-separated list: ae-industry, ae-geography, bdr, sdr, orchestrator, ...]
signals:      [comma-separated list of Researcher signal keywords]
updated:      YYYY-MM
review:       YYYY-MM
---
```

**industries: all** means the play is applicable to any organisation regardless of sector. The Orchestrator considers it in scope for every account. This is the default for plays built around use cases rather than industry-specific dynamics.

**industries: [list]** means the play is most relevant to those sectors. The Orchestrator still considers other plays for those accounts, but this one is weighted up.

**type: sub-vertical-pack** files are reference context loaded alongside a play when the industry is known — not a motion to run, but knowledge to ground the motion.

**Signal matching:** The Researcher surfaces signals in the prospect brief using keywords. The Orchestrator matches those keywords against each play's signals: field to rank play relevance. Exact match is not required — semantic proximity is sufficient.

---

## Routing table — what to load for each task type

The Orchestrator resolves the context manifest before passing any task to a sub-agent. Use this table.

| task_type            | modules/                          | contexts/       | plays/                              |
|----------------------|-----------------------------------|-----------------|-------------------------------------|
| prospect_research    | calibration.md                    | (none)          | (none at research stage) |                    | (none)          | (none at research stage)            |
| pov_draft            | pov.md, discovery.md              | persona match   | Orchestrator-selected play          |
| pov_critique         | pov.md, qualification.md          | (none)          | play loaded for draft               |
| outreach_sequence    | discovery.md                      | persona match   | play if relevant                    |
| discovery_prep       | discovery.md, qualification.md    | persona match   | sub-vertical-pack if industry known |
| qualification_review | qualification.md, sales-cycle.md  | (none)          | (none)                              |
| stage_progression    | sales-cycle.md                    | (none)          | (none)                              |
| hiring_brief         | (none)                            | hiring.md, recruiter.md | (none)                      |
| partner_brief        | (none)                            | partner.md      | sub-vertical-pack if relevant       |
| field_marketing_brief| (none)                            | field-marketer.md | sub-vertical-pack if relevant     |

**Persona match rule:** Load the context file that matches the role perspective the task requires. Default to no context file if the task is not persona-specific. Never load more than one context file per task unless the task explicitly involves two personas interacting (e.g. a BDR-to-AE handoff brief).

---

## Play selection rules

Play selection is the Orchestrator's responsibility, informed by the Researcher's signal summary. Sub-agents never browse plays/ independently.

**Selection sequence:**
1. Researcher produces prospect brief with signal summary.
2. Orchestrator reads all play frontmatter tags in plays/.
3. Orchestrator scores each play: signal keyword matches + industry tag match + persona relevance.
4. Orchestrator selects the highest-scoring play, or overrides if context warrants.
5. If a sub-vertical-pack exists for the prospect's industry, load it alongside the selected play.
6. Selected play path(s) written into the task context manifest.
7. Sub-agent loads from the manifest. It does not select.

**If no play matches well:** Do not force a fit. Note in the task output that no strong match was found and flag for play creation. A missing play is a gap in the system, not a reason to use an ill-fitting one.

**If multiple plays match:** Load the strongest single match. Note other candidates in the task output for Orchestrator consideration.

---

## Clarification requests

When a sub-agent encounters a gap it cannot resolve from its loaded context, it raises a `clarification_request` rather than guessing. This is a formal task type, not an ad-hoc behaviour.

**Raising a clarification_request:**
Any sub-agent (Researcher, POV Writer, Critic, Sequencer) may raise a clarification_request when it encounters:
- Ambiguous industry or persona match (e.g. signals suggest both FSI and fintech)
- No strong play match in plays/ — gap flagged, not forced
- Missing critical prospect data that research did not surface
- Conflicting signals that cannot be resolved from loaded context
- Output boundary question (e.g. what level of detail is appropriate for this recipient)

**Format:**
```json
{
  "type": "clarification_request",
  "raised_by": "pov-writer",
  "task_id": "pov-draft-acme-001",
  "gap": "Prospect industry unclear — signals suggest both FSI and fintech. Which sub-vertical pack should be loaded?",
  "options": ["Load financial-planning-wealth-management.md", "Load fintech signals only", "Proceed without pack — flag in output"],
  "escalate_to": "orchestrator"
}
```

**Resolution flow:**
1. Sub-agent writes clarification_request to output directory
2. Orchestrator reads it — resolves if the answer is clear from existing context
3. If not resolvable: Orchestrator posts to Jay via Slack with specific question and options
4. Jay responds with a choice or free-text instruction
5. If Jay's answer requires new research: Orchestrator dispatches a scoped `prospect_research` task to Researcher
6. Orchestrator updates the task manifest and re-dispatches the original task

**Sub-agents never guess.** A clarification_request is not a failure — it is the correct behaviour when context is insufficient.

---

## What agents must never do

- Browse memory/ independently to decide what to load.
- Load a context file not specified in the task manifest.
- Surface content from modules/calibration.md externally. Calibration is internal reasoning only.
- Force-load a sub-vertical pack when no matching industry pack exists.
- Hardcode play file paths — filenames include dates and will change. Always resolve from the manifest.
- Load soul.md directly — it is the source document. Use spine.md and the relevant modules.

---

## Adding new files

**New play:** Add to plays/ with format [topic]-[year].md. Include the full frontmatter tag block.

**New sub-vertical pack:** Add to plays/ with format [industry-segment].md. Set type: sub-vertical-pack in frontmatter. Use the standard 12-section template.

**New module:** Add to modules/ and update the routing table above.

**New context:** Add to contexts/ and update the routing table's persona match rule.

**Retiring a play:** Do not delete — rename with -archived suffix. Keeps history intact.

---

## Portability note

This directory has no dependency on any specific VM or agent framework. The structure is plain text files in a directory. To move it: copy the directory, update the base path reference in each sub-agent system prompt. The routing logic lives here, not in the framework.
