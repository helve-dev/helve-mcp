#!/usr/bin/env node
import readline from "node:readline";

const DEFAULT_ENDPOINT = process.env.HELVE_MCP_URL || "https://helve.dev/mcp";
export const MISSING_KEY_URL = "https://helve.dev/k/npm";
export const MISSING_KEY_NOTICE = `No HELVE_API_KEY — get one with $1 free credit at ${MISSING_KEY_URL}`;

export function parseArgs(argv) {
  let endpoint = DEFAULT_ENDPOINT;
  let apiKey = process.env.HELVE_API_KEY || "";
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--url" && argv[i + 1]) {
      endpoint = argv[++i];
    } else if (arg === "--api-key" && argv[i + 1]) {
      apiKey = argv[++i];
    } else if (arg === "--help" || arg === "-h") {
      return { help: true, endpoint, apiKey };
    }
  }
  return { help: false, endpoint, apiKey };
}

export function extractJsonFromSse(text) {
  const messages = [];
  for (const line of text.split(/\r?\n/)) {
    if (line.startsWith("data:")) {
      const payload = line.slice(5).trim();
      if (payload && payload !== "[DONE]") {
        messages.push(JSON.parse(payload));
      }
    }
  }
  return messages;
}

export function missingKeyAuthResponse(message) {
  if (!message || message.id === undefined) return [];
  if (message.method === "tools/call") {
    return [
      {
        jsonrpc: "2.0",
        id: message.id,
        result: {
          isError: true,
          content: [
            {
              type: "text",
              text: `${MISSING_KEY_NOTICE} (set HELVE_API_KEY in your MCP client config).`,
            },
          ],
        },
      },
    ];
  }
  return [
    {
      jsonrpc: "2.0",
      id: message.id,
      error: {
        code: -32001,
        message: MISSING_KEY_NOTICE,
      },
    },
  ];
}

export async function forwardJsonRpc(message, { endpoint = DEFAULT_ENDPOINT, apiKey = "", sessionId = "", fetchImpl = fetch } = {}) {
  const headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
  };
  if (apiKey) {
    headers.Authorization = `Bearer ${apiKey}`;
  }
  if (sessionId) {
    headers["mcp-session-id"] = sessionId;
  }

  const res = await fetchImpl(endpoint, {
    method: "POST",
    headers,
    body: JSON.stringify(message),
  });

  const nextSessionId = res.headers?.get?.("mcp-session-id") || sessionId;
  const contentType = res.headers?.get?.("content-type") || "";
  const text = await res.text();

  if (res.status === 401 && !apiKey) {
    return { responses: missingKeyAuthResponse(message), sessionId: nextSessionId };
  }

  if (!text || res.status === 202 || res.status === 204) {
    return { responses: [], sessionId: nextSessionId };
  }

  if (contentType.includes("text/event-stream")) {
    return { responses: extractJsonFromSse(text), sessionId: nextSessionId };
  }

  const parsed = JSON.parse(text);
  return { responses: Array.isArray(parsed) ? parsed : [parsed], sessionId: nextSessionId };
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    process.stderr.write("Usage: helve-mcp [--url https://helve.dev/mcp] [--api-key <HELVE_API_KEY>]\n");
    process.exit(0);
  }

  if (!opts.apiKey) {
    process.stderr.write(`${MISSING_KEY_NOTICE}\n`);
  }

  let sessionId = "";
  const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });

  for await (const line of rl) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    let msg;
    try {
      msg = JSON.parse(trimmed);
    } catch (err) {
      process.stderr.write(`helve-mcp: invalid JSON input: ${err.message}\n`);
      continue;
    }

    try {
      const result = await forwardJsonRpc(msg, {
        endpoint: opts.endpoint,
        apiKey: opts.apiKey,
        sessionId,
      });
      if (result.sessionId) sessionId = result.sessionId;
      for (const resp of result.responses) {
        process.stdout.write(`${JSON.stringify(resp)}\n`);
      }
    } catch (err) {
      if (msg.id !== undefined) {
        process.stdout.write(
          `${JSON.stringify({
            jsonrpc: "2.0",
            id: msg.id,
            error: { code: -32603, message: err.message || "Upstream MCP request failed" },
          })}\n`
        );
      } else {
        process.stderr.write(`helve-mcp: ${err.message}\n`);
      }
    }
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
