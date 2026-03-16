---
name: mission-control
description: "Queue companies for sales research via Mission Control. Use when a company name is mentioned in a research or sales context. Automatically handles competitor relationships, deduplication, and ambiguity flagging. Always call this before starting Exa research on a new company."
---

# Mission Control Skill

Queue companies for research and track the full pipeline via Mission Control at http://192.168.0.120:18790.

## When to use this skill

Use when Jay mentions a company in a research or sales context:
- "Research Afterpay" → queue it
- "Look into Zip Money — they're a competitor to Afterpay" → queue both, create competitor relationship
- "What do we know about Nearmap?" → queue if not already in board

Do NOT queue companies mentioned casually with no research intent:
- "Salesforce announced..." → not a queue trigger (unless Jay says "research Salesforce")
- "Their competitor is Xero" → flag for context but confirm intent before queuing

## Step 1 — Queue the company

```bash
export MC_URL="http://192.168.0.120:18790"

curl -s -X POST "$MC_URL/api/slack/trigger" \
  -H "Content-Type: application/json" \
  -d "{
    \"company_name\": \"COMPANY_NAME\",
    \"initial_prompt\": \"JAYS_EXACT_MESSAGE\",
    \"competitor_of\": \"PARENT_COMPANY_OR_NULL\",
    \"ambiguous\": false,
    \"ambiguity_note\": null
  }" | python3 -m json.tool
```

Replace:
- `COMPANY_NAME` with the company name exactly as Jay said it
- `JAYS_EXACT_MESSAGE` with Jay's full message (verbatim — this is the training signal)
- `PARENT_COMPANY_OR_NULL` with the parent company name if Jay mentioned a competitor relationship, otherwise omit the field
- Set `ambiguous: true` and add `ambiguity_note` if there are multiple companies with the same name

## Step 2 — Handle ambiguity

If two companies match (e.g. "TLC" could be The Living Company or The Lottery Corporation):

```bash
curl -s -X POST "$MC_URL/api/slack/trigger" \
  -H "Content-Type: application/json" \
  -d "{
    \"company_name\": \"TLC\",
    \"initial_prompt\": \"JAYS_MESSAGE\",
    \"ambiguous\": true,
    \"ambiguity_note\": \"2 matches: The Living Company (retirement) or The Lottery Corporation (ASX:TLC)\"
  }" | python3 -m json.tool
```

Then ask Jay in Slack: "Which TLC — The Living Company (retirement sector) or The Lottery Corporation (ASX:TLC)?"

## Step 3 — Update status when research starts

When you begin Exa research on a company, update its status:

```bash
# Get the run_id from the queue response, then:
curl -s -X PATCH "$MC_URL/api/runs/RUN_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "researching"}' | python3 -m json.tool
```

## Step 4 — Log research completion

After Exa research is complete, log the event:

```bash
curl -s -X POST "$MC_URL/api/events" \
  -H "Content-Type: application/json" \
  -d "{
    \"run_id\": \"RUN_ID\",
    \"event_type\": \"research_complete\",
    \"actor\": \"agent_researcher\",
    \"content\": \"Brief summary of key signals found\",
    \"prompt_tokens\": PROMPT_TOKENS,
    \"output_tokens\": OUTPUT_TOKENS
  }" | python3 -m json.tool

# Then set status to review
curl -s -X PATCH "$MC_URL/api/runs/RUN_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "review"}' | python3 -m json.tool
```

## Check board state

```bash
curl -s http://192.168.0.120:18790/api/stats | python3 -m json.tool
```

## Key rules

- Always capture Jay's exact message as `initial_prompt` — it is the training signal
- If a company is already in the board (response shows `"status": "already_exists"`), do not re-queue — log a new event instead
- When queuing a competitor, if the parent company is not already in the board, Mission Control auto-creates it
- After every agent action (research complete, POV drafted, outreach generated), log an event
- Set `review` status whenever human input is needed
