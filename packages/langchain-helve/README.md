# langchain-helve

LangChain and LangGraph toolkit for [Helve](https://helve.dev) — one API key and one prepaid balance for 324 tools across 257 providers (0% per-call markup, USD 1.00 free starter credit) (web search, crawling/extraction, LLMs, audio transcription, PDFs, email, browser automation, finance, and free public utilities).

- **No monthly subscriptions:** start with prepaid credit packs (10 / 25 / 100 USD, never expire).
- **Deterministic spend caps:** per-key `spend_limit_usd` enforcement (`402 spend_limit_exceeded`).
- **Failed-call escrow:** upstream 5xx errors and timeouts automatically refund to 0 USD.
- **Free tool discovery:** `helve_search_tools` works without authentication so agents can discover `tool_id`, `input_schema`, and pricing before calling.

## Installation

```bash
pip install langchain-helve
```

## Quickstart

```python
import os
from langchain_helve import HelveToolkit

toolkit = HelveToolkit(api_key=os.environ.get("HELVE_API_KEY"))
tools = toolkit.get_tools()
# [HelveSearchTools, HelveCallTool, HelveRequestTool]

# 1. Discover tools dynamically (no auth required)
search_tool = tools[0]
print(search_tool.invoke({"query": "web extraction", "limit": 3}))

# 2. Bind to any LangChain / LangGraph agent
# agent = create_react_agent(model, tools)
```

## Direct Client Usage

```python
from langchain_helve import HelveGatewayClient

client = HelveGatewayClient(api_key="sk_live_...")

# Search available tools
matches = client.search_tools("web extraction", limit=5)

# Execute any discovered tool_id with its native arguments
result = client.call_tool(
    "helve.web_extract",
    {"urls": ["https://docs.helve.dev"], "content": {"max_chars": 4000}},
)
```

## Links

- Website: https://helve.dev
- Documentation: https://docs.helve.dev
- MCP Server & Skills: https://github.com/helve-dev/helve-mcp
- OpenAPI 3.1 Spec: https://helve.dev/openapi.json
