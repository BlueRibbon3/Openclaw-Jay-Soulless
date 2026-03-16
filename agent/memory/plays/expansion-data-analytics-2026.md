---
title:      Data and Analytics Drag — Expansion Play
type:       play
industries: all
use_cases:  data-analytics, ai-readiness, crm-expansion, platform-adoption
personas:   ae-industry, ae-geography, orchestrator
signals:    snowflake, databricks, microsoft-fabric, azure, power-bi, tableau, looker, data-engineer, bi-developer, analytics-engineer, cdo, chief-data-officer, data-driven, reporting-lag, data-latency, warehouse, agentforce
updated:    2026-03
review:     2026-09
---

# Play: Expansion — Data and Analytics Drag

**orchestrator_note:** Use when Researcher identifies external data warehouse dependency, BI tooling friction, or data latency as a prospect pain signal. Override if a stronger unlock is apparent from the brief. Applicable to all industries — the warehouse drag pattern exists regardless of sector.

---

## The Core Insight

Most Salesforce expansion accounts have built a side quest into their workflow. Data flows out of Salesforce into an external warehouse — Snowflake, Microsoft Fabric, Azure, Databricks — where it gets processed by data engineers and analysts, and comes back as a report that is already stale by the time anyone reads it.

That architecture is expensive in ways organisations often don't fully see. The visible cost is the warehouse and BI tooling licences. The invisible cost is larger: the data engineers required to keep the pipeline alive, the analysts interpreting outputs that nobody acts on, the latency baked into every decision made from a report that reflects last week's reality. And in any fast-moving sales or service environment, timing is everything. A rep who gets context thirty seconds before a call makes a different decision than one who gets it three days after.

The unlock is not replacing the warehouse. It is making the insights available inside the flow of work — inside the tools people are already using, at the moment they need them — instead of making data a destination people have to seek out.

---

## The Conversation Frame

The opening question is not about data. It is about where work happens.

*"What is the most widely used application in your business?"*

The answer is almost always Teams or Slack. Follow with:

*"What are you delivering inside it — text and file sharing, or process and decision-making?"*

If it is decision-making, that needs data. If it is process, that process should be informed by the insights the organisation has already decided are most valuable. The question becomes: are those insights reaching the people who need them, inside the tool where they are already working — or are they sitting in a dashboard somewhere that requires a separate login and a reason to go looking?

The value proposition is not replacement. It is: keep your external BI for looking backwards — for audit, for compliance, for the CFO's quarterly review. But if you want to influence what your people do right now, in this call, in this deal, in this service interaction, the insights need to be where those people are. Don't make data a destination. Make it part of the flow.

When you do that, the CRM stops being an administrative burden and becomes the place where useful things happen. That shift changes adoption, which changes data quality, which improves every downstream decision. It compounds.

---

## The Semantic Layer Angle

Agents — and this matters for any account where Agentforce is in scope — do best with curated, correlated data. Not mass data dumps. The organisations that will get the most from AI-assisted workflows are the ones that define their semantic layer first: their language, their process definitions, their business terms, codified so that every system — and every agent — is working from the same dictionary.

Just as onboarding a new employee requires learning the language of the business before anything else, agents need that same grounding. The organisations that build this foundation first will have a compounding advantage — every capability they deploy gets more effective faster, because the context is already right.

This is a natural bridge from a data and analytics conversation into a longer-term platform vision. It does not need to be introduced early. It surfaces when the prospect is already thinking about what comes after solving the immediate data friction problem.

---

## Signal Indicators (for Researcher)

Recommend this play when the prospect brief surfaces one or more of the following:

- Job postings or LinkedIn presence showing data engineers, BI developers, or analytics engineers as significant headcount
- Technology stack references to Snowflake, Databricks, Microsoft Fabric, Power BI, Tableau (standalone), Looker, or similar
- Executive commentary about "data-driven decision-making" without specifics — often signals aspiration without execution
- Salesforce instance present but service or sales teams showing low CRM adoption or data quality complaints
- Recent investment in cloud infrastructure suggesting active modernisation
- Org structure showing a CDO, Chief Data Officer, or Head of Analytics as a separate function from IT

Do not recommend this play if:

- The account is net-new to Salesforce — data and analytics expansion requires an existing platform foundation
- The prospect's primary pain signals are in a different domain — a more targeted play will be more relevant

---

## Recommended Provocative Question (for POV Writer)

*"Your team generates more data about your customers today than at any point in your history. How much of that reaches the people who need it, at the moment they need it — and how much arrives too late to change anything?"*

---

## Related Plays

- `expansion-agentforce-semantic-layer-2026.md` — natural progression if data foundation conversation goes well
- `pov-example-dominos.md` — structural reference for framing just-in-time insights without naming a product
