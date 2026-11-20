---
name: tool-discovery
description: Discover, inspect schemas, and execute any of Helve's 324+ third-party tools across finance, developer data, knowledge, LLMs, and utilities.
---

Always discover the exact `tool_id` and `input_schema` before calling `call_tool`:

- Use `search_tools(query)` for natural-language capability matching (for example `"sec 10-k xbrl"`, `"pdf convert"`, `"cve score"`, or `"github repos"`).
- Use `list_categories()` when exploring what Helve supports across `search`, `extract`, `crawl_map`, `research_answer`, `llm`, `embeddings`, `audio_tts`, `transcription`, `finance`, `developer_data`, `knowledge_geo`, and `utilities`.
- Prefer `$0.00` public tools when they satisfy the user's request, and use metered tools (`perplexity.answer`, `exa.answer`, `firecrawl.map`, `cohere.chat`, `browserless.scrape`) when deep research, JS-rendered extraction, or LLM synthesis is needed.
- Never invent `tool_id` values or argument names; pass arguments matching the schema returned by `search_tools`.
