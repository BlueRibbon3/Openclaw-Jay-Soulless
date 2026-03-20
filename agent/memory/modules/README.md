# Agent Memory — Methodology Modules Overview

The `modules/` directory contains five methodology files loaded by task type:

| File | Source | Loaded for |
|---|---|---|
| `discovery.md` | soul.md §3, §4, §4a, §4b | discovery_prep, pov_generation |
| `qualification.md` | soul.md §6 | qualification_review, discovery_prep |
| `pov.md` | soul.md §7 | pov_generation, outreach_sequence |
| `sales-cycle.md` | soul.md §8 | qualification_review, stage_progression |
| `calibration.md` | soul.md §9 | prospect_research only — internal agent reasoning heuristics, never surfaces in external output |

Each file is approximately 60–120 lines. Content is proprietary methodology and is not included in this preview.

The routing table in `memory/README.md` shows which modules are loaded for each task type.
