# Signal Quality Framework
*Version 1.0 — Blank framework for Ralph induction cycle.*
*Source classification and calibration data populated post-Ralph.*
*Do not edit composite_score or validation_delta — agent calculates these.*

---

## Purpose

This framework gives the Researcher a structured output format for every signal found during prospect research. It separates observable facts (agent fills in) from quality judgments (Jay scores). The gap between the agent's composite score and Jay's validation score is the training signal that improves the Researcher over time.

---

## Scoring model

Signal strength is multiplicative across three dimensions:

```
composite_score = timeliness_score × financial_score × personal_score
```

**Timeliness:**
| Bucket | Days | Score |
|---|---|---|
| Hot | 0–30 | 1.5 |
| Current | 31–90 | 1.2 |
| Stale | 91–180 | 0.8 |
| Historical | 180+ | 0.5 |

**Financial materiality:**
| Assessment | Score |
|---|---|
| Yes | 1.5 |
| Unclear | 1.0 |
| No | 0.5 |

**Personal relevance (derived from name fields):**
| Condition | Score |
|---|---|
| Exec mentioned by name | 1.5 |
| Prospect mentioned by name only | 1.2 |
| Neither | 0.8 |

**Score range:**
- Maximum: 1.5 × 1.5 × 1.5 = **3.375** — timely, financially material, exec named
- Minimum: 0.5 × 0.5 × 0.8 = **0.200** — historical, not material, not personal
- One-dimensional: 1.5 × 0.5 × 0.8 = **0.600** — timely only

---

## Signal type taxonomy

Every signal belongs to one of six types:

| Type | What it covers |
|---|---|
| **Leadership & Talent** | Executive appointments, departures, restructures, new hires in key roles, promotions, team expansions |
| **Financial & Commercial** | Earnings, revenue announcements, funding rounds, M&A, investor statements, cost reduction programs, budget cycles |
| **Strategic & Operational** | New business units, market entries or exits, partnerships, technology decisions, digital transformation, infrastructure changes |
| **Market & Competitive** | Competitor moves, industry disruption, regulatory changes, market share shifts, new entrants, category creation |
| **Customer & Reputation** | Customer wins or losses, product reviews, NPS signals, community sentiment, analyst ratings, brand moments |
| **Regulatory & Compliance** | Government announcements, industry body rulings, compliance obligations, licensing changes, audit findings |

---

## Source type taxonomy

Every signal has a producer type. The agent identifies this from the URL and content. The producer type is the primary input to credibility scoring — Jay assigns credibility, not the agent.

| Producer type | What it means |
|---|---|
| **Subject-produced** | The company or executive themselves — announcements, reports, job postings, exec statements, investor presentations |
| **Market-produced** | Financial markets, regulators, exchanges — market announcements, regulatory filings, exchange notices |
| **Media-produced** | Journalists and analysts — industry press, analyst reports, general news coverage |
| **Community-produced** | Peers, practitioners, aggregators — forums, LinkedIn posts, review sites, Reddit |
| **Vendor-produced** | Your company or competitors — case studies, press releases, partner announcements |

---

## Signal card template

One card per signal found. Agent fills in all fields above the divider. Jay fills in all fields below the divider after reviewing.

```yaml
---
# ── AGENT FILLS IN ──────────────────────────────────────────
signal_id:               # SIG-001, SIG-002 etc — sequential per research run
run_id:                  # Mission Control prospect_run ID
prospect_name:           # Company name
signal_type:             # One of the six taxonomy types above
description:             # 1-2 sentences — what was found, no interpretation
source_url:              # Exact URL
source_type:             # One of the five producer types above
published_date:          # YYYY-MM-DD
days_since_published:    # Integer — calculated from published_date to today
timeliness:              # Hot / Current / Stale / Historical
timeliness_score:        # 1.5 / 1.2 / 0.8 / 0.5
prospect_mentioned_by_name:  # yes / no
exec_mentioned_by_name:      # yes / no
financially_material:        # yes / no / unclear
financial_score:         # 1.5 / 1.0 / 0.5
personal_relevance:      # Exec named / Prospect named / Neither
personal_score:          # 1.5 / 1.2 / 0.8
composite_score:         # timeliness_score × financial_score × personal_score
research_purpose:        # outreach_trigger / pov_research / account_background / competitive_context

# ── JAY FILLS IN ─────────────────────────────────────────────
jay_validation_score:    # Jay's score 0.2–3.375 — overall signal strength judgment
validation_delta:        # composite_score minus jay_validation_score (agent calculates after Jay scores)
outreach_utility:        # high / medium / low — is this a compelling reason to make contact?
pov_utility:             # high / medium / low — does this strengthen a POV?
credibility:             # high / medium / low — how much do you trust this source?
jay_notes:               # Why the delta exists. What this signal means in context.
                         # What you would tell an AE about this signal.
---
```

---

## Example card (blank — Ralph Session 1 template)

```yaml
---
signal_id: SIG-001
run_id:
prospect_name: Meridian Fleet Solutions
signal_type:
description:
source_url:
source_type:
published_date:
days_since_published:
timeliness:
timeliness_score:
prospect_mentioned_by_name:
exec_mentioned_by_name:
financially_material:
financial_score:
personal_relevance:
personal_score:
composite_score:
research_purpose:

jay_validation_score:
validation_delta:
outreach_utility:
pov_utility:
credibility:
jay_notes:
---
```

---

## Researcher instructions

At the end of every research run, produce one signal card per signal found. Follow these rules:

**What counts as a signal:**
- Any piece of information that could change how you approach this prospect
- Minimum threshold: the signal must be specific to this company, this industry, or this executive — not generic market commentary

**What does not count as a signal:**
- General industry trend articles with no prospect-specific connection
- Company website boilerplate (about us, mission statement, product descriptions)
- Undated content — if no publication date can be found, note it in description and set timeliness to Historical

**Filling in the card:**
- `description` — what was found, not what it means. Save interpretation for the brief.
- `financially_material` — mark yes if the signal explicitly references revenue, cost, investment, funding, headcount changes, or contract value. Mark unclear if financial implications are implied but not stated. Mark no if purely operational or reputational.
- `personal_relevance` — check for the prospect company name and the target executive's name explicitly. Do not infer.
- `composite_score` — multiply the three scores. Round to two decimal places.

**Output format:**
- List signal cards after the research brief, under the heading `## Signal Cards`
- Order by composite_score descending — highest scoring signals first
- Minimum 3 cards per research run, maximum 10
- If fewer than 3 signals found, flag this explicitly: `⚠ Low signal density — only N signals found`

**After Jay scores:**
- Calculate `validation_delta` = composite_score − jay_validation_score
- A positive delta means the agent over-scored. A negative delta means the agent under-scored.
- Both are learning signals. The direction and magnitude of the delta, combined with jay_notes, is what calibrates the model over time.

---

## Calibration log (populated post-Ralph)

*Empty until first Ralph cycle completes. Calibration entries are added here after Jay validates signal cards.*

| Pattern | Observed delta | Calibration rule | Added |
|---|---|---|---|
| — | — | — | — |

---

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-03-21 | Initial framework — blank card template, scoring model, researcher instructions |
