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

**MCP + Code Mode ready — $0/mo subscription & non-expiring $10 / $25 / $100 prepaid packs.** One `HELVE_API_KEY` gives agents 313 tools across 255 providers (LLMs, audio, email, PDF, browser, finance + web) over both **MCP (`https://helve.dev/mcp`)** and **scriptable REST/`fetch` (`https://helve.dev/v1/...`)**, with per-key `spend_limit_usd` caps on every tier and $0 failed-call escrow.

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

## Agent Skills, Marketplaces & Code Mode

### Install Skills & Plugins
```bash
# Install individual Helve skills (Claude Code, Codex, Cursor, etc.)
npx skills add helve-dev/helve-mcp --skill deep-research   # ~$0.02/brief multi-engine search + extract + synthesis
npx skills add helve-dev/helve-mcp --skill batch-crawl     # ~$0.05/10 URLs clean markdown + $0 blocked-page billing
npx skills add helve-dev/helve-mcp --skill audio-brief     # ~$0.08/15 min Deepgram/AssemblyAI transcription + brief
npx skills add helve-dev/helve-mcp --skill get-started     # Core setup, spend_limit_usd caps & tool discovery

# Or add the full plugin marketplace
codex plugin marketplace add helve-dev/helve-mcp
claude plugin marketplace add helve-dev/helve-mcp
```

### Code Mode (Parallel JS `fetch` Scripts)
Running Claude Code's Code Mode or a sandboxed JS/TS script? Helve gives you **one key for 313+ APIs** over scriptable REST/`fetch` with deterministic `spend_limit_usd` caps:
```js
const headers = {
  Authorization: `Bearer ${process.env.HELVE_API_KEY}`,
  "Content-Type": "application/json",
};

const [search, extract] = await Promise.all([
  fetch("https://helve.dev/v1/tools/call", {
    method: "POST",
    headers,
    body: JSON.stringify({ tool_id: "helve.web_search", arguments: { query: "MCP Code Mode" } }),
  }).then((r) => r.json()),
  fetch("https://helve.dev/v1/tools/call", {
    method: "POST",
    headers,
    body: JSON.stringify({ tool_id: "helve.web_extract", arguments: { urls: ["https://docs.helve.dev"] } }),
  }).then((r) => r.json()),
]);
```

## Live Tool Catalog (313 Tools Across 255 Providers & 12 Categories)
- **Search & Extraction:** `helve.web_search` (11 engines + consensus fusion), `helve.web_extract` (9 extractors), `jina.reader`, `microlink.screenshot_metadata`, `exa.find_similar`, `brave.news_search`, `brave.images_search`, `brave.videos_search`
- **Research & LLM/Embeddings:** `perplexity.answer`, `exa.answer`, `tavily.research`, `linkup.sourced_answer`, `valyu.answer`, `firecrawl.map`, `tavily.map`, `openrouter.chat`, `openrouter.embeddings`
- **Audio & Transcription:** `helve.audio_transcribe`, `elevenlabs.tts`, `elevenlabs.sound_effects`, `deepgram.tts`
- **Finance & Regulatory:** `alphavantage.query`, `sec_edgar.search_filings`, `frankfurter.fx_rates`, `open_er.exchange_rates`, `worldbank.indicator`, `us_treasury.debt_to_penny`, `coingecko.price`, `propublica.nonprofits`, `gleif.lei_lookup`, `federal_register.search_documents`, `clearbit.company_autocomplete`
- **Developer & Security Data:** `github.search_repositories`, `gitlab.search_projects`, `hackernews.search`, `stackexchange.search`, `npm.package_info`, `npm.downloads`, `pypi.package_info`, `pypi.downloads`, `crates_io.search_crates`, `packagist.search_packages`, `maven_central.search_artifacts`, `nuget.search_packages`, `go_proxy.module_info`, `docker_hub.repository_info`, `rubygems.gem_info`, `osv.query_vulnerabilities`, `huggingface.search_models`, `judge0.execute_code`, `shodan.internetdb`, `ripestat.network_info`, `hibp.breaches`, `deps_dev.package_insights`, `crt_sh.subdomains`
- **Science, Medical, Geo & Utilities:** `pubmed.search`, `pubmed.article_summaries`, `clinicaltrials.search`, `openfda.drug_events`, `arxiv.search_papers`, `openalex.search_works`, `crossref.search_works`, `osrm.route`, `osrm.matrix`, `nominatim.geocode`, `photon.search_places`, `open_elevation.lookup`, `open_meteo.forecast`, `wikipedia.summary`, `wikimedia.pageviews`, `wikidata.search_entities`, `openlibrary.search_books`, `itunes.search`, `openfoodfacts.lookup_product`, `nager_date.public_holidays`, `zippopotam.postal_lookup`, `timeapi.current_time`, `wayback.available`, `cloudflare.dns_lookup`, `rdap.domain_lookup`, `ipwho.geolocation`, `kickbox.disposable_email`, `kroki.render_diagram`, `quickchart.render_chart`, `qrserver.generate_qr`

## REST API & Official SDKs

- **Python (`helve-mcp` on PyPI):** [`pip install helve-mcp`](https://pypi.org/project/helve-mcp/) or `HELVE_API_KEY=sk_live_... uvx helve-mcp` (zero-dependency stdio MCP bridge + `HelveClient`)
- **Node.js (`helve-mcp` on npm):** [`npx -y helve-mcp`](https://www.npmjs.com/package/helve-mcp) (zero-dependency stdio MCP bridge)
- **Vercel AI SDK (`@helve-dev/ai-sdk` on npm):** [`npm install @helve-dev/ai-sdk`](https://www.npmjs.com/package/@helve-dev/ai-sdk)
- **Catalog & Search (no auth required to browse schemas):** `GET /v1/tools`, `POST /v1/tools/search`
- **Metered Execution & Demand Capture:** `POST /v1/tools/call`, `POST /v1/tools/{id}/call`, `POST /v1/tools/request`
- **TypeScript / Node:** `npm install helve-sdk`
- **Python:** `pip install helve`

## Documentation & Trust
- Docs: https://docs.helve.dev
- MCP Guide: https://docs.helve.dev/mcp-server
- Pricing: https://docs.helve.dev/concepts/pricing
- Terms & Privacy: https://helve.dev/terms | https://helve.dev/privacy
