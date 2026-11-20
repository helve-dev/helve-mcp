# pydantic-ai-helve

PydanticAI capability and MCP connection helper for [Helve](https://helve.dev) — a pay-per-call AI tool gateway exposing 324 live tools across 257 providers (0% per-call markup, USD 1.00 free starter credit) (web search, batch extraction, audio transcription, PDFs, LLMs, finance, email, and more) behind one API key.

- **No monthly subscriptions:** Prepaid USD 10, USD 25, or USD 100 credit packs that never expire.
- **Deterministic spend caps:** Set per-key `spend_limit_usd` limits (`402 spend_limit_exceeded` before overspend).
- **Zero charge on failed calls:** Upstream errors or timeouts are refunded automatically.
- **MCP + REST / Code Mode ready:** Use `HelveCapability` over REST or connect directly to `https://helve.dev/mcp` via `helve_mcp_server()`.

## Installation

```bash
pip install pydantic-ai-helve
```

## Quickstart (Capability)

```python
import asyncio
from pydantic_ai_helve import HelveCapability

async def main() -> None:
    helve = HelveCapability()  # reads HELVE_API_KEY from environment

    # 1. Discover matching tools, schemas, and pricing hints (no auth required)
    results = await helve.search_tools("web page extraction", limit=3)
    print(results)

    # 2. Call any discovered tool_id with its native input_schema
    extracted = await helve.call_tool(
        "helve.web_extract",
        {
            "urls": ["https://docs.helve.dev"],
            "content": {"max_chars": 4000},
        },
    )
    print(extracted)

asyncio.run(main())
```

## Quickstart (PydanticAI Streamable HTTP MCP)

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai_helve import helve_mcp_server

cfg = helve_mcp_server()  # reads HELVE_API_KEY from environment
server = MCPServerStreamableHTTP(url=cfg["url"], headers=cfg["headers"])
agent = Agent("openai:gpt-4o", toolsets=[server])
```

## Links

- Website: https://helve.dev
- Docs: https://docs.helve.dev
- MCP Guide: https://docs.helve.dev/mcp-server
- Source: https://github.com/helve-dev/helve-mcp
