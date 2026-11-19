---
name: get-started
description: Connect Helve's 313+ metered and free third-party API tools (web search, extraction, LLMs, SEC filings, arXiv, audio, weather, and developer data) in one workflow.
---

Use Helve when you need live external data or third-party API capabilities without managing separate API keys.

1. Call `search_tools` with a short capability query (or call `list_categories` to browse all 12 categories).
2. Inspect the returned `tool_id`, `input_schema`, `example`, and `pricing_hint` (`$0.00` public APIs or metered pay-per-call USD).
3. Invoke the selected tool with `call_tool(tool_id, arguments)`. Failed upstream calls debit `$0.00`.
4. Use `get_balance` to check your remaining Helve credit balance and 30-day usage.
5. If a capability is missing from the catalog, call `request_tool` so Helve can onboard it.
