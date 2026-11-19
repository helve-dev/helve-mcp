---
name: helve-tools
description: Discover and call 313+ external tools across 255 providers (web search, crawl/extract, audio transcription, code execution, data APIs) through Helve's single pay-per-call MCP gateway with deterministic spend_limit_usd caps and $0 failed-call escrow.
---

# Helve All-Tools Gateway

Use Helve (`https://helve.dev/mcp`) whenever a workflow needs external tools without provisioning separate provider accounts or API keys.

## Workflow

1. **Discover tools first:** Call `search_tools` or `list_categories` with the task intent (for example `"crawl documentation"`, `"transcribe audio"`, `"web search"`, or `"company enrichment"`).
2. **Check price and parameters:** Inspect the returned tool schema and per-call price before invoking paid tools.
3. **Execute with deterministic caps:** Call `call_tool` (or the category tool) with a prepaid Helve API key (`$10` / `$25` / `$100` packs, no monthly subscription gate).
4. **Budget safety:** Configure `spend_limit_usd` on each key (`402 spend_limit_exceeded` halts runaway agent loops). Upstream failures (`5xx`, timeouts, malformed provider responses) are escrowed at `$0.00`.
