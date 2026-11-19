# @helve-dev/ai-sdk

**MCP + Code Mode ready** — Vercel AI SDK tool definitions and gateway client for **Helve** (`https://helve.dev`). Give your agents one `HELVE_API_KEY` for 313+ APIs across 255 providers over both **MCP (`https://helve.dev/mcp`)** and **scriptable REST/`fetch`**, with deterministic `spend_limit_usd` caps and `$0` failed-call escrow.

## Quickstart

```js
import { generateText } from "ai";
import { tool } from "ai";
import { z } from "zod";
import { createHelveGateway } from "@helve-dev/ai-sdk";

const helve = createHelveGateway({
  apiKey: process.env.HELVE_API_KEY,
  toolFn: tool,
  z,
});

const { text } = await generateText({
  model: yourModel,
  tools: helve,
  prompt: "Search for live web extraction tools on Helve and run one.",
});
```

## Links
- Live Gateway & Docs: https://docs.helve.dev/sdks
- MCP Server Guide: https://docs.helve.dev/mcp-server
- GitHub: https://github.com/helve-dev/helve-mcp
