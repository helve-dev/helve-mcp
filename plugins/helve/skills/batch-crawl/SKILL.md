---
name: batch-crawl
description: Cleanly extract markdown from up to 10 URLs (~$0.05/batch) with automatic multi-provider fallback and $0 billing on blocked/empty 200-OK pages.
---

# Helve Batch Crawl & Extract Skill (~$0.05 / 10 URLs)

Extract clean, LLM-ready markdown from up to 10 URLs in one call with automatic provider fallback (`exa` → `tavily` → `parallel` → `firecrawl`) and `$0.00` charged on empty or Cloudflare/CAPTCHA 200-OK challenge pages.

## Cost Breakdown (`usage.cost_usd`)

| Step | Tool | Est. Cost |
| --- | --- | --- |
| 1. Batch extract (10 URLs) | `helve.web_extract` (`provider: "auto"`) | `~$0.050` |
| 2. JS-rendered fallback (optional) | `browserless.content` | `~$0.005 / page` |
| **Total per 10-URL batch** | **1 key · `$0.50` free = ~100 pages** | **`~$0.050`** |

## Quickstart (`curl`)

```bash
curl -sS -X POST https://helve.dev/v1/tools/call \
  -H "Authorization: Bearer $HELVE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "helve.web_extract",
    "arguments": {
      "urls": ["https://helve.dev/pricing", "https://docs.helve.dev/quickstart"],
      "max_chars": 8000
    }
  }'
```

## MCP Workflow (`https://helve.dev/mcp`)

1. Call `extract(urls=[...], max_chars=8000)` — Helve automatically skips empty/WAF-blocked responses and falls back to the next healthy provider.
2. For heavy client-side SPAs, call `call_tool(tool_id="browserless.content", arguments={"url": "..."})`.
