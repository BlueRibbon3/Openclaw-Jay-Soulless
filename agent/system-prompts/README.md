# Agent Persona System Prompts — Structure and Design

Eight self-contained persona system prompts generated from `soul.md`. Each is designed to work as a standalone system prompt in any OpenClaw agent instance or any LLM API call — no external file loading required.

| File | Persona | Approx lines |
|---|---|---|
| `system-prompt-bdr.md` | Outbound BDR | ~120 |
| `system-prompt-sdr.md` | SDR | ~100 |
| `system-prompt-ae-industry.md` | Industry Specialist AE | ~150 |
| `system-prompt-ae-geography.md` | Geography-Based AE | ~140 |
| `system-prompt-hiring.md` | Hiring Manager | ~110 |
| `system-prompt-partner.md` | Partner Manager | ~120 |
| `system-prompt-recruiter.md` | Recruiter | ~115 |
| `system-prompt-field-marketer.md` | Field Marketer | ~110 |

---

## Structure of each system prompt

Every prompt follows the same structure:

1. **Identity header** — who this persona is, which Jay traits they carry
2. **Deliverable** — what closed looks like for this persona specifically
3. **Operating posture** — how they think and approach their work
4. **Methodology** — relevant sections from soul.md in condensed form
5. **Triangulation posture** — the two questions that must be answered before any output is produced: *what is this for?* and *who is the primary audience and what frame are they bringing?*
6. **What they never do** — hard negative constraints
7. **Hard rules** — non-negotiable operating principles

---

## The triangulation posture

Every system prompt encodes the same core communication principle: before producing any output, the agent answers two questions.

**First — what is this for?** The purpose determines scope, depth, and output format. If purpose is not stated, the agent asks before running.

**Second — who is the primary audience, and what frame are they bringing?** A POV written for a CFO is not the same document as a POV written for a CTO. An outreach email read by a prospect is not the same document handed to an AE. The audience determines the language, the structure, and what gets left unsaid.

This principle — triangulate, do not guess — is the root of the product-name discipline, the language extraction methodology, and the upfront contract. It is not a rule about communication style. It is a rule about respect for the receiver.

---

## How these prompts would scale

At organisational scale, each of these eight prompts becomes the foundation for a dedicated agent instance:

- A BDR agent that runs research and drafts outreach for every BDR in the team
- An Industry AE agent that builds POVs for FSI, Healthcare, Retail accounts
- A Geography AE agent that handles cross-vertical accounts
- A Hiring Manager agent that generates role briefs and interview frameworks

The prompts are portable. They do not depend on the homelab infrastructure. They can run on any LLM API with any agent framework.
