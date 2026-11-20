---
name: deep-research
description: Run a multi-engine deep research brief (~$0.02/brief) using Helve fusion search, clean page extraction, and LLM synthesis.
---

# Helve Deep Research Skill (~$0.02 / brief)

Run a complete multi-source research brief across parallel search engines, clean markdown extraction, and LLM synthesis with one `HELVE_API_KEY` (`sk_live_...`).

## Cost Breakdown (`usage.cost_usd`)

| Step | Tool | Est. Cost |
| --- | --- | --- |
| 1. Multi-engine consensus search | `helve.web_search` (`provider: "fusion"`) | `~$0.014` |
| 2. Clean markdown extract (top 3 URLs) | `helve.web_extract` (`provider: "auto"`) | `~$0.006` |
| 3. Executive synthesis | `cohere.chat` (`command-a-03-2025`, trial tier) | `$0.000` |
| **Total per brief** | **1 key · `$1.00` free = ~50 briefs** | **`~$0.020`** |

Failed or empty/WAF-blocked upstream responses debit **$0.00**.

## Quickstart (`curl`)

```bash
curl -sS -X POST https://helve.dev/v1/tools/call \
  -H "Authorization: Bearer $HELVE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "helve.web_search",
    "arguments": {
      "query": "AI agent payment protocols 2026 comparison",
      "provider": "fusion",
      "max_results": 8
    }
  }'
```

## MCP Workflow (`https://helve.dev/mcp`)

1. Call `search(query, provider="fusion", max_results=8)` for consensus results.
2. Call `extract(urls=[...top_3_urls], max_chars=8000)` to pull clean markdown.
3. Call `call_tool(tool_id="cohere.chat", arguments={...})` to synthesize a cited brief.
