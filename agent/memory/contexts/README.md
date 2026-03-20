# Agent Memory — Specialist Persona Contexts Overview

The `contexts/` directory contains eight specialist persona files loaded based on the task's persona requirement:

| File | Persona | Loaded when |
|---|---|---|
| `bdr.md` | Outbound BDR | persona = bdr |
| `sdr.md` | SDR | persona = sdr |
| `ae-industry.md` | Industry Specialist AE | persona = ae-industry |
| `ae-geography.md` | Geography-Based AE | persona = ae-geography |
| `hiring.md` | Hiring Manager | persona = hiring, task_type = hiring_brief |
| `partner.md` | Partner Manager | persona = partner, task_type = partner_brief |
| `recruiter.md` | Recruiter | persona = recruiter, task_type = hiring_brief |
| `field-marketer.md` | Field Marketer | persona = field-marketer, task_type = field_marketing_brief |

Each file is approximately 40–80 lines. They contain the condensed operating rules, deliverable definition, and hard constraints for each persona. Content is proprietary and not included in this preview.

Each context file is always loaded in combination with `spine.md` and the relevant methodology module(s). Never loaded alone.
