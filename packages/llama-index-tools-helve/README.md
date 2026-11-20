# llama-index-tools-helve

LlamaIndex `BaseToolSpec` integration for [Helve](https://helve.dev) — a pay-per-call AI tool gateway exposing 324 live tools across 257 providers (0% per-call markup, USD 1.00 free starter credit) (web search, batch extraction, audio transcription, PDFs, LLMs, finance, email, and more) behind one API key.

- **No monthly subscriptions:** Prepaid USD 10, USD 25, or USD 100 credit packs that never expire.
- **Deterministic spend caps:** Set per-key `spend_limit_usd` limits (`402 spend_limit_exceeded` before overspend).
- **Zero charge on failed calls:** Upstream errors or timeouts are refunded automatically.
- **MCP + REST / Code Mode ready:** Works directly via `HelveToolSpec` (`search_tools`, `call_tool`, `request_tool`) or via `https://helve.dev/mcp`.

## Installation

```bash
pip install llama-index-tools-helve
```

## Quickstart

```python
from llama_index.tools.helve import HelveToolSpec

spec = HelveToolSpec()  # reads HELVE_API_KEY from environment

# 1. Discover matching tools, schemas, and pricing hints (no auth required)
results = spec.search_tools("web page extraction", limit=3)
print(results)

# 2. Call any discovered tool_id with its native input_schema
extracted = spec.call_tool(
    "helve.web_extract",
    {
        "urls": ["https://docs.helve.dev"],
        "content": {"max_chars": 4000},
    },
)
print(extracted)

# 3. Pass directly as LlamaIndex FunctionTools
tools = spec.to_tool_list()
```

## Links

- Website: https://helve.dev
- Docs: https://docs.helve.dev
- MCP Guide: https://docs.helve.dev/mcp-server
- Source: https://github.com/helve-dev/helve-mcp
