# Soul Builder — Product Documentation
*Version 1.0 · Part of the Seller Onboarding Program*
*Last updated: 2026-03-25*

---

## What it is

Soul Builder is a Claude-powered interactive interview that turns a seller's experience, stories, and instincts into a personalised sales identity document — the foundation their AI agent is built on.

A 60-minute conversation. One output: `soul.md`.

---

## How it works

**Screen 1 — Profile selection**
Four cards: Charlie Challenger, Dan Driver, Cathy Consultant, Jay Strategist. Each pre-loads a different interview context that adjusts the depth, tone, and starting questions. Editorial aesthetic — cream paper, gold accents, serif headings.

**Screen 2 — The interview**
Six sections, one at a time. The agent asks one question, listens, extracts the principle, plays it back. Progress dots at the top. The agent knows when to move sections and signals completion with a hidden tag. The opening question adapts to the selected profile.

**Screen 3 — Soul.md output**
Generated from the full conversation. First person, seller's own language, six sections. Download as `.md` or copy to clipboard.

**The agent rules baked in:**
- Never asks multiple questions at once
- Always probes for stories not statements
- Plays back what it heard before moving on
- Never adds principles the seller didn't demonstrate
- Never names products unless the seller does first

---

## The four profiles

| Profile | Experience | Who they are |
|---|---|---|
| **Charlie Challenger** | 1–3 years | High energy, building methodology. Strong on activity, developing judgment. |
| **Dan Driver** | 3–7 years | Consistent performer with a developing methodology. Knows what works, wants to sharpen the edges. |
| **Cathy Consultant** | 5–10 years | Solution-seller background. Strong on discovery and relationships, developing outbound motion. |
| **Jay Strategist** | 10+ years | Developed methodology, sharp instincts. Needs codification more than education. |

---

## The six interview sections

| Section | Focus | What gets extracted |
|---|---|---|
| 1 — Identity | Who you are as a seller | Core identity, what drives them, defining win or loss |
| 2 — Opening | How you open a conversation | Upfront contract, word-for-word opening, expectation setting |
| 3 — Discovery | How you find the real problem | Question approach, L1/L2/L3 instincts, curiosity posture |
| 4 — Qualification | How you protect your time | Disqualification filters, walk-away triggers, time discipline |
| 5 — Communication | How you make things land | Language discipline, triangulation posture, product-name discipline |
| 6 — The POV | How you earn the right to a view | POV instinct, provocative question approach, what makes it land |

---

## The soul.md output

Generated from the full conversation. Six sections. First person. Seller's own language and vocabulary throughout. Every principle traceable to something said in the interview — nothing invented, nothing generic.

Downloadable as `.md`. Ready to load into the agent architecture.

---

## The 201 and 301 sessions (planned)

**201 — Specialisation**
Draws out industry depth, competitive knowledge, calibration on what good signals look like in the seller's vertical. Produces the contexts and plays sections of soul.md.

**301 — Calibration**
The hardest session. Focuses on what the seller would never do — the negative policy. Draws out the stories behind the hard rules. Produces the calibration section and seeds the rejection log with the seller's own `would_never` entries.

---

## Voice (future)

The interview questions are currently delivered as text. The vision is audio — a recognised voice asking the questions, creating a more immersive and memorable onboarding experience.

---

## Technical notes

- Built as a single HTML file with embedded CSS and JavaScript
- Powered by Claude Sonnet 4.6 via Anthropic API
- No backend required — runs entirely in the browser
- Conversation history maintained in memory for the session
- soul.md generated in a separate API call after the interview completes
- Designed to migrate to Slack (Socket Mode) for deployment across the sales organisation

---

## Status

| Component | Status |
|---|---|
| Profile selection | ✅ Live |
| Six-section interview | ✅ Live |
| soul.md generation | ✅ Live |
| Download / copy | ✅ Live |
| 201 Specialisation session | ⬜ Planned |
| 301 Calibration session | ⬜ Planned |
| Audio / voice delivery | ⬜ Future |
| Slack deployment | ⬜ Future |
| Admin dashboard (org-wide view) | ⬜ Future |
