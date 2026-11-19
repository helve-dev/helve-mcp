---
name: web-research
description: Run multi-provider web search, clean page extraction, and deep research workflows with Helve.
---

For web research and fact-finding tasks:

1. Use `search(query)` for fast multi-provider web search (`provider: "auto"` or `"fusion"` to merge top engines) or `search_tools(query="research answer")` for Perplexity/Exa answer tools.
2. Use `extract(urls)` to pull clean markdown from specific pages (default `max_chars: 8000`, raise up to `50000` when full text is needed).
3. For JS-rendered pages or screenshots, discover `browserless.content` / `browserless.scrape` via `search_tools`.
4. Summarize findings concisely with source URLs and report the call cost when relevant.
