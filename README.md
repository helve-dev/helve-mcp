# Helve MCP — The Metered "All Tools" Gateway for AI Agents

<p align="center">
  <a href="https://helve.dev">
    <img src="https://helve.dev/og.png" alt="Helve — The Metered All-Tools Gateway for AI Agents" width="600" />
  </a>
</p>

[![MCP Streamable HTTP](https://img.shields.io/badge/MCP-Streamable%20HTTP-blue)](https://helve.dev/mcp)
[![Website](https://img.shields.io/badge/web-helve.dev-green)](https://helve.dev)
[![Docs](https://img.shields.io/badge/docs-helve.dev-black)](https://docs.helve.dev)
[![llms.txt](https://img.shields.io/badge/llms.txt-helve.dev-purple)](https://helve.dev/llms.txt)

**Run high-frequency paid multi-provider AI agent workflows (deep research, multi-engine search/crawl/extract, audio transcription, LLMs & TTS) with one key, deterministic `spend_limit_usd` caps, and $0 failed-call escrow.**

Helve is a metered, pay-per-call **all-tools gateway and tool-search MCP server** at `https://helve.dev/mcp` (313 live tools today across 255 providers and 12 categories — 291 free public/finance/dev data tools + 22 metered paid tools spanning search, extraction, transcription, research Q&A, TTS/audio, crawl/mapping, code execution, security/DNS, finance, developer data, and knowledge/geo):
- **`search_tools`**: Search Helve's catalog by capability or intent (or omit `query` to browse live tools), inspect native JSON schemas, and see upfront `pricing_hint`s.
- **`list_categories`**: Browse Helve's live tool catalog by category with tool counts and sample `tool_id`s.
- **`get_balance`**: Check your USD credit balance, 30-day usage summary, and active API key `spend_limit_usd` budget cap.
- **`call_tool`**: Execute any discovered `tool_id` with `arguments` under one prepaid USD balance ($0.50 free signup credit, no credit card required; upstream cost + 15% Helve fee; $0.00 on zero-auth public utilities).
- **`request_tool`**: Report a missing API or capability (`tool_name`, `use_case`) when your agent hits a blocker so Helve can prioritize onboarding it.
- **Direct & Async Convenience Tools (11 MCP tools total)**: `search`, `extract`, `transcribe`, `transcription_status`, `list_transcriptions`, and `cancel_transcription`.
- **Zero-Debit Failed-Call Protection**: Failed upstream calls debit **$0.00** (transcription debits only on completion).

## Quick Connect (`https://helve.dev/mcp`)

### Claude Code
```bash
claude mcp add --transport http helve https://helve.dev/mcp \
  --header "Authorization: Bearer sk_live_..."
```

### Cursor (`~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "helve": {
      "url": "https://helve.dev/mcp",
      "headers": {
        "Authorization": "Bearer sk_live_..."
      }
    }
  }
}
```

### Codex
```bash
export HELVE_API_KEY="sk_live_..."
codex mcp add helve --url https://helve.dev/mcp --bearer-token-env-var HELVE_API_KEY
```

### Gemini CLI
```bash
gemini mcp add --transport http \
  --header "Authorization: Bearer sk_live_..." helve https://helve.dev/mcp
```

### VS Code (`settings.json`)
```json
"mcp": {
  "servers": {
    "helve": {
      "type": "http",
      "url": "https://helve.dev/mcp",
      "headers": {
        "Authorization": "Bearer sk_live_..."
      }
    }
  }
}
```

## Live Tool Catalog (193 Tools Across 161 Providers & 12 Categories)
- **Search & Extraction:** `helve.web_search` (11 engines + consensus fusion), `helve.web_extract` (9 extractors), `jina.reader`, `microlink.screenshot_metadata`, `exa.find_similar`, `brave.news_search`, `brave.images_search`, `brave.videos_search`
- **Research & LLM/Embeddings:** `perplexity.answer`, `exa.answer`, `tavily.research`, `linkup.sourced_answer`, `valyu.answer`, `firecrawl.map`, `tavily.map`, `openrouter.chat`, `openrouter.embeddings`
- **Audio & Transcription:** `helve.audio_transcribe`, `elevenlabs.tts`, `elevenlabs.sound_effects`, `deepgram.tts`
- **Finance & Regulatory:** `alphavantage.query`, `sec_edgar.search_filings`, `frankfurter.fx_rates`, `open_er.exchange_rates`, `worldbank.indicator`, `us_treasury.debt_to_penny`, `coingecko.price`, `propublica.nonprofits`, `gleif.lei_lookup`, `federal_register.search_documents`, `clearbit.company_autocomplete`
- **Developer & Security Data:** `github.search_repositories`, `gitlab.search_projects`, `hackernews.search`, `stackexchange.search`, `npm.package_info`, `npm.downloads`, `pypi.package_info`, `pypi.downloads`, `crates_io.search_crates`, `packagist.search_packages`, `maven_central.search_artifacts`, `nuget.search_packages`, `go_proxy.module_info`, `docker_hub.repository_info`, `rubygems.gem_info`, `osv.query_vulnerabilities`, `huggingface.search_models`, `judge0.execute_code`, `shodan.internetdb`, `ripestat.network_info`, `hibp.breaches`, `deps_dev.package_insights`, `crt_sh.subdomains`
- **Science, Medical, Geo & Utilities:** `pubmed.search`, `pubmed.article_summaries`, `clinicaltrials.search`, `openfda.drug_events`, `arxiv.search_papers`, `openalex.search_works`, `crossref.search_works`, `osrm.route`, `osrm.matrix`, `nominatim.geocode`, `photon.search_places`, `open_elevation.lookup`, `open_meteo.forecast`, `wikipedia.summary`, `wikimedia.pageviews`, `wikidata.search_entities`, `openlibrary.search_books`, `itunes.search`, `openfoodfacts.lookup_product`, `nager_date.public_holidays`, `zippopotam.postal_lookup`, `timeapi.current_time`, `wayback.available`, `cloudflare.dns_lookup`, `rdap.domain_lookup`, `ipwho.geolocation`, `kickbox.disposable_email`, `kroki.render_diagram`, `quickchart.render_chart`, `qrserver.generate_qr`

## REST API & Official SDKs
- **Catalog & Search (no auth required to browse schemas):** `GET /v1/tools`, `POST /v1/tools/search`
- **Metered Execution & Demand Capture:** `POST /v1/tools/call`, `POST /v1/tools/{id}/call`, `POST /v1/tools/request`
- **TypeScript / Node:** `npm install helve-sdk`
- **Python:** `pip install helve`

## Documentation & Trust
- Docs: https://docs.helve.dev
- MCP Guide: https://docs.helve.dev/mcp
- Pricing: https://docs.helve.dev/concepts/pricing
- Terms & Privacy: https://helve.dev/terms | https://helve.dev/privacy
