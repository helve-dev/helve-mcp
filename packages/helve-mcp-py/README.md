# helve-mcp (Python)

Zero-dependency stdio-to-Streamable-HTTP MCP bridge and lightweight Python client for **[Helve](https://helve.dev)** — one pay-per-call API & MCP gateway for **313 live tools across 255 providers** (web search, crawl/extract, deep research, audio transcription, LLMs, SEC filings, GitHub, PDFs, finance, and utilities).

- **No monthly subscriptions:** Zero base fee with non-expiring prepaid credit packs (USD 10 / 25 / 100; USD 0.50 free signup credit).
- **Deterministic budget caps:** Per-key `spend_limit_usd` hard ceiling (`402 spend_limit_exceeded`).
- **Zero-cost failed-call escrow:** Failed upstream calls automatically debit USD 0.
- **MCP + REST / Code Mode ready:** Works over Streamable HTTP MCP, stdio MCP via `uvx helve-mcp`, or direct Python/REST calls.

## Quickstart (MCP stdio bridge)

Run directly with `uvx` (no global install):

```bash
HELVE_API_KEY=sk_live_... uvx helve-mcp
```

Or install with `pip`:

```bash
pip install helve-mcp
HELVE_API_KEY=sk_live_... helve-mcp
```

### Claude Desktop / Cursor / Windsurf MCP config

```json
{
  "mcpServers": {
    "helve": {
      "command": "uvx",
      "args": ["helve-mcp"],
      "env": {
        "HELVE_API_KEY": "sk_live_..."
      }
    }
  }
}
```

> If your MCP client supports remote Streamable HTTP directly, you can also connect to `https://helve.dev/mcp` with `Authorization: Bearer sk_live_...` (or OAuth 2.1).

## Quickstart (Python REST client)

```python
from helve_mcp import HelveClient

client = HelveClient()  # reads HELVE_API_KEY from environment

# 1. Discover tools (no API key required)
tools = client.search_tools("web extract", limit=5)

# 2. Invoke any tool by tool_id (requires HELVE_API_KEY)
result = client.call_tool(
    "helve.web_extract",
    {"urls": ["https://docs.helve.dev"], "content": {"max_chars": 4000}},
)
print(result)
```

## Links

- Website: https://helve.dev
- MCP Guide: https://docs.helve.dev/mcp-server
- Source & Agent Skills: https://github.com/helve-dev/helve-mcp
