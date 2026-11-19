import test from "node:test";
import assert from "node:assert/strict";
import { parseArgs, extractJsonFromSse, forwardJsonRpc } from "../bin/helve-mcp.mjs";

test("parseArgs parses url and api-key flags", () => {
  const opts = parseArgs(["--url", "https://example.com/mcp", "--api-key", "hlv_test"]);
  assert.equal(opts.endpoint, "https://example.com/mcp");
  assert.equal(opts.apiKey, "hlv_test");
  assert.equal(opts.help, false);
});

test("extractJsonFromSse extracts data payloads", () => {
  const sse = 'event: message\ndata: {"jsonrpc":"2.0","id":1,"result":{"ok":true}}\n\n';
  const msgs = extractJsonFromSse(sse);
  assert.equal(msgs.length, 1);
  assert.equal(msgs[0].id, 1);
  assert.equal(msgs[0].result.ok, true);
});

test("forwardJsonRpc sends Authorization and mcp-session-id headers", async () => {
  let captured = null;
  const fakeFetch = async (url, init) => {
    captured = { url, init };
    return new Response(JSON.stringify({ jsonrpc: "2.0", id: 1, result: { tools: [] } }), {
      status: 200,
      headers: { "content-type": "application/json", "mcp-session-id": "sess_123" },
    });
  };
  const res = await forwardJsonRpc(
    { jsonrpc: "2.0", id: 1, method: "tools/list" },
    { endpoint: "https://helve.dev/mcp", apiKey: "hlv_abc", fetchImpl: fakeFetch }
  );
  assert.equal(captured.url, "https://helve.dev/mcp");
  assert.equal(captured.init.headers.Authorization, "Bearer hlv_abc");
  assert.equal(res.sessionId, "sess_123");
  assert.equal(res.responses[0].id, 1);
});
