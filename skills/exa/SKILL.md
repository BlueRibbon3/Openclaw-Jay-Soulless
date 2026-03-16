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
