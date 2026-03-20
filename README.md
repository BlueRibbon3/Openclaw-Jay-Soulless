# Agent Memory — Task Routing Architecture
*This file is not redacted. It shows the routing architecture without revealing methodology content.*

---

## Directory structure

```
memory/
├── README.md          ← this file — routing rules and load instructions
├── spine.md           ← identity core, always loaded [CONTENT REDACTED]
├── modules/           ← methodology by task type [CONTENT REDACTED]
│   ├── discovery.md
│   ├── qualification.md
│   ├── pov.md
│   ├── sales-cycle.md
│   └── calibration.md
├── contexts/          ← specialist personas, loaded by task [CONTENT REDACTED]
│   ├── bdr.md
│   ├── sdr.md
│   ├── ae-industry.md
│   ├── ae-geography.md
│   ├── hiring.md
│   ├── partner.md
│   ├── recruiter.md
│   └── field-marketer.md
└── plays/             ← expansion plays and sub-vertical packs [CONTENT REDACTED]
    ├── expansion-data-analytics-2026.md
    └── financial-planning-wealth-management.md
```

---

## Routing table

The Orchestrator loads files based on task type. This table is the routing reference.

| Task type | Always load | Also load |
|---|---|---|
| `prospect_research` | spine.md | modules/calibration.md |
| `pov_generation` | spine.md | modules/pov.md + modules/discovery.md + relevant context + relevant play |
| `discovery_prep` | spine.md | modules/discovery.md + modules/qualification.md + relevant context |
| `outreach_sequence` | spine.md | modules/pov.md + relevant context |
| `qualification_review` | spine.md | modules/qualification.md + modules/sales-cycle.md |
| `hiring_brief` | spine.md | contexts/hiring.md |
| `partner_brief` | spine.md | contexts/partner.md |
| `field_marketing_brief` | spine.md | contexts/field-marketer.md |

---

## Play selection rules

1. Check the prospect's industry against play frontmatter `industries` field
2. Check use cases against play frontmatter `use_cases` field
3. Match is semantic proximity, not exact string match
4. `industries: all` means in scope for every account
5. Maximum one play per POV generation task
6. If no play matches — proceed without one, do not force a match

---

## Plays frontmatter schema

Every play file carries YAML frontmatter:

```yaml
---
title: [play name]
type: play | sub-vertical-pack
industries: all | [list]
use_cases: [list]
personas: [list]
signals: [list of signal types that trigger this play]
updated: [date]
review: [date — when statistics should be re-verified]
---
```

---

## clarification_request

When a sub-agent cannot resolve a gap from available context, it raises a `clarification_request` rather than guessing.

```json
{
  "type": "clarification_request",
  "raised_by": "agent_id",
  "task_id": "task_id",
  "gap": "description of what is missing",
  "options": ["option A", "option B"],
  "escalate_to": "orchestrator"
}
```

Flow: sub-agent → Orchestrator → Jay via Slack → optional Researcher re-dispatch.

---

## What agents must never do

- Surface calibration.md content in any external output
- Load a play without verifying statistics are current (Researcher responsibility)
- Guess when a clarification_request is the correct action
- Load contexts/ files for personas not relevant to the current task
- Name a product before establishing a shared problem definition
