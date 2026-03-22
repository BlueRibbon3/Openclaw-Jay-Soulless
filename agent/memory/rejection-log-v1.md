# Rejection Log
*Training corpus for Critic 1. Every rejection is a labelled training example.*
*Version 1.0 — introduced at Ralph Loop 1.*
*The `would_never` field is the primary training signal. Be specific.*

---

## Purpose

This log captures every output Jay rejects during Ralph loops and live prospect runs. The rejection reason and `would_never` annotation are the inputs that train Critic 1 over time — teaching it the boundary between what Jay would send and what Jay would never send.

Soul.md captures what Jay does and why. This log captures what Jay would never do — extracted from actual rejections, not stated upfront. The two documents together form the complete policy definition.

---

## How to use this log

After reviewing any agent output — signal cards, outreach draft, POV, discovery prep — if you would not send it or use it as-is, log the rejection here before editing.

Do not log edits. Log rejections. An edit means the output was close enough to fix. A rejection means it failed at a level that requires understanding why, not just fixing what.

---

## Rejection entry template

```yaml
---
rejection_id:          # REJ-001, REJ-002 etc — sequential
run_id:                # Mission Control prospect_run ID
loop:                  # Loop 1 / Loop 2 / Loop 3 / Loop 4 / Loop 5 / Live
output_type:           # signal_cards / outreach / pov_initial / pov_mid_cycle / discovery_prep / brief
date:                  # YYYY-MM-DD
prospect_name:         # Company name

# ── WHAT FAILED ──────────────────────────────────────────────
rejection_reason:      # 1-2 sentences — why this output was rejected
violation_category:    # Which soul.md principle was violated — see taxonomy below
would_never:           # The specific thing Jay would never do that appeared here
                       # This is the primary training signal — be precise
evidence:              # The exact line, phrase, or element from the output that caused the rejection

# ── CRITIC CALIBRATION ────────────────────────────────────────
critic_missed_it:      # yes / no — did the agentic Critic fail to flag this?
critic_dimension:      # Which Critic dimension should have caught this (if critic_missed_it = yes)
calibration_note:      # What rule should be added to the Critic to catch this next time
---
```

---

## Violation category taxonomy

Every rejection maps to one of these categories. Use the most specific one that applies.

| Code | Category | Description |
|---|---|---|
| V01 | Product before problem | Product name or capability introduced before a shared problem is established |
| V02 | Vendor language | Agent's language or marketing language used instead of prospect's own words |
| V03 | Generic opener | Outreach opens without a traceable signal — could be sent to anyone |
| V04 | Wrong signal used | Signal used in outreach is stale, low credibility, or not specific to this prospect |
| V05 | Assumed pain | Agent assumed L2 or L3 pain without discovery evidence |
| V06 | Told customer what's wrong | POV or outreach diagnoses the customer's problem rather than inviting them to identify it |
| V07 | Feature list | Output ends with or includes a feature list rather than aspiration or outcome |
| V08 | Closed question | Outreach or discovery closes with a yes/no question |
| V09 | Too long | First contact exceeds five sentences, or POV section exceeds appropriate length |
| V10 | Multiple signals | More than one signal used in a single outreach — dilutes the angle |
| V11 | Missing upfront contract | Discovery prep omits the upfront contract or sets wrong expectations |
| V12 | Calibration surfaced | Internal calibration reasoning appeared in customer-facing output |
| V13 | Thread broken | Output does not connect to or reference prior context from earlier in the pursuit |
| V14 | Wrong persona | Output does not match the stated persona — BDR acting like AE, AE acting like SDR |
| V15 | Triangulation failure | Output produced for the wrong audience frame — written for sender not receiver |
| V16 | Other | Does not fit above — describe fully in rejection_reason and would_never |

---

## Example entry (illustrative — not from a real run)

```yaml
---
rejection_id: REJ-001
run_id: mc-run-001
loop: Loop 1
output_type: outreach
date: 2026-03-22
prospect_name: Meridian Fleet Solutions

rejection_reason: >
  The outreach opened with a reference to Salesforce Data Cloud before
  establishing any shared problem. The prospect has no reason to care
  about the product name at this stage.
violation_category: V01
would_never: >
  I would never name a product in the first sentence of a cold outreach.
  The product name belongs to us. The problem belongs to them. Lead with
  theirs, not ours.
evidence: >
  "I wanted to reach out about how Salesforce Data Cloud could help
  Meridian Fleet with their data strategy..."

critic_missed_it: yes
critic_dimension: Dimension 3 — Hard rules adherence
calibration_note: >
  Add explicit check: does the subject line or first sentence contain
  any Salesforce product name? If yes, automatic violation V01 regardless
  of context.
---
```

---

## Rejection log (append entries below)

*Empty — first entry added during Ralph Loop 1.*

---

## Would-never index (populated from entries above)

*A running list of specific things Jay would never do, extracted from rejections. Updated after each Ralph session.*
*This index becomes the negative training corpus for Critic 1.*

| REJ-ID | Would never | Violation | Loop |
|---|---|---|---|
| — | — | — | — |

---

## Calibration rules extracted (populated post-Ralph)

*Rules added to Critic 1 based on rejections where `critic_missed_it = yes`.*

| Rule | Added from | Critic dimension | Date |
|---|---|---|---|
| — | — | — | — |
