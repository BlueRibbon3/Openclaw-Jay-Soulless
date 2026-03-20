# Soul.md — Sales Identity Document
*[REDACTED — Engineering Preview]*

---

This document is the canonical source of truth for the agent's sales identity, methodology, and operating principles. It is 414 lines across 10 sections and 8 specialist persona contexts. All agent behaviour derives from it.

**This file is not included in the engineering preview.** The content represents proprietary sales methodology and is not shared outside the organisation.

---

## What this document contains

| Section | Content | Lines (approx) |
|---|---|---|
| §1 Who I Am As a Seller | Sales identity, operating principles, calibrated scepticism posture | ~35 |
| §2 The Motion | Expansion and net-new motion, OS framing, Agentforce and Data 360 plays | ~40 |
| §3 Pre-Call Prep | Power map, language extraction, discovery sequence (11 steps) | ~35 |
| §4 Discovery | Sandler pain funnel (L1/L2/L3), upfront contract, qualification through discovery | ~45 |
| §5 Communication Style | Product name discipline, CBUS principle, triangulation posture, language extraction methodology | ~30 |
| §6 Qualification | Continuous qualification, disqualification filters, political account plays | ~40 |
| §7 The POV | POV structure, provocative question methodology, Domino's annotated example | ~45 |
| §8 Commercial | [Not started] | — |
| §9 Calibration | Internal-only. Agent reasoning patterns and signal weighting heuristics. Never surfaces in external output. | ~25 |
| §10a–10h Specialist contexts | BDR, SDR, Industry AE, Geography AE, Hiring Manager, Partner Manager, Recruiter, Field Marketer | ~100 |
| Appendix A | Email templates (pre-call intro, post-discovery next steps, low-interest redirect) | ~60 |

---

## How it is used at runtime

The agent does not load the full document on every request. Instead, a condensed identity core (`spine.md`, ~150 lines) is always loaded, and methodology modules and persona contexts are loaded on demand based on task type.

The routing logic lives in `agent/memory/README.md`.

---

## Derived artifacts

Eight self-contained persona system prompts are generated from this document. Each encodes the relevant sections for a specific persona (BDR, SDR, AE, etc.) and can be used as a standalone system prompt in any LLM API call.

System prompts are in `agent/system-prompts/` — content is redacted in this preview but the structure and format are visible.
