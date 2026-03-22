---
name: exa
description: "Prospect research using Exa AI semantic search. Use for company news, executive statements, funding signals, tech stack research, and full page content retrieval. Always use this before drafting a POV or outreach sequence."
---

# Exa Research Skill

Use the Exa AI API for prospect research. The API key is stored in `/root/clawd/.env`.

## Setup — Load the API Key
```bash
export EXA_API_KEY=$(grep EXA_API_KEY /root/clawd/.env | cut -d= -f2)
```

## Search — News and Company Signals
```bash
curl -s https://api.exa.ai/search \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "QUERY_HERE",
    "numResults": 5,
    "type": "neural",
    "contents": {
      "summary": {"query": "QUERY_HERE"}
    }
  }' | python3 -m json.tool
```

Replace `QUERY_HERE` with the actual search query. Examples:
- `"Nearmap Australia executive news 2026"`
- `"Afterpay CRO strategic priorities"`
- `"[Company] funding round announcement"`
- `"[Company] technology stack data platform"`

## Search with Date Filter — Recent News Only
```bash
curl -s https://api.exa.ai/search \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "QUERY_HERE",
    "numResults": 5,
    "type": "neural",
    "startPublishedDate": "2025-01-01",
    "contents": {
      "summary": {"query": "QUERY_HERE"}
    }
  }' | python3 -m json.tool
```

## Full Page Content — Retrieve Article Text
```bash
curl -s https://api.exa.ai/search \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "QUERY_HERE",
    "numResults": 3,
    "type": "neural",
    "contents": {
      "text": {"maxCharacters": 3000},
      "summary": {"query": "QUERY_HERE"}
    }
  }' | python3 -m json.tool
```

## Find Similar Companies
```bash
curl -s https://api.exa.ai/findSimilar \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.COMPANY_WEBSITE.com",
    "numResults": 5,
    "contents": {
      "summary": {"query": "company overview business model"}
    }
  }' | python3 -m json.tool
```

## Research Workflow for Prospect Brief

1. Search for recent company news: `"[Company] news 2025 2026"`
2. Search for executive statements: `"[Company] CEO OR CRO OR CDO statement strategy"`
3. Search for technology signals: `"[Company] data platform OR CRM OR Salesforce"`
4. Search for growth signals: `"[Company] funding OR hiring OR expansion"`
5. Find similar companies for calibration: use `findSimilar` with company URL

Always extract:
- Growth signals (hiring pace, funding, market expansion)
- Technology stack signals (tools, platforms, vendors)
- Executive signals (recent statements, LinkedIn posts, press)
- Competitive signals (what vendors are mentioned, recent wins/losses)
- Timing signals (mandated projects, regulatory changes, new executive hires)

## Signal Cards — Required Output After Every Research Run

After completing research, produce signal cards using the framework at `/root/clawd/memory/signal-quality-framework-v1.md`.

Read the framework before producing cards. One card per signal found.

**Rules:**
- Minimum 3 cards per run, maximum 10
- Order cards by composite_score descending — highest first
- If fewer than 3 signals found, flag: `⚠ Low signal density — only N signals found`
- Do not interpret signals in the card — description is facts only
- Calculate composite_score = timeliness_score × financial_score × personal_score

**Output structure — append after the research brief:**
```
## Signal Cards

### SIG-001
signal_type: [type]
description: [1-2 sentences — what was found]
source_url: [URL]
source_type: [producer type]
published_date: [YYYY-MM-DD]
days_since_published: [integer]
timeliness: [Hot/Current/Stale/Historical]
timeliness_score: [1.5/1.2/0.8/0.5]
prospect_mentioned_by_name: [yes/no]
exec_mentioned_by_name: [yes/no]
financially_material: [yes/no/unclear]
financial_score: [1.5/1.0/0.5]
personal_relevance: [Exec named/Prospect named/Neither]
personal_score: [1.5/1.2/0.8]
composite_score: [calculated]
research_purpose: [outreach_trigger/pov_research/account_background/competitive_context]

jay_validation_score: [blank]
validation_delta: [blank]
outreach_utility: [blank]
pov_utility: [blank]
credibility: [blank]
jay_notes: [blank]
```

Repeat for each signal found, incrementing signal_id.
