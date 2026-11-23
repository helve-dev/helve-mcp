import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { parseArgs, extractJsonFromSse, forwardJsonRpc, MISSING_KEY_NOTICE, MISSING_KEY_URL } from "../bin/helve-mcp.mjs";

const BIN_PATH = fileURLToPath(new URL("../bin/helve-mcp.mjs", import.meta.url));

test("parseArgs parses url and api-key flags", () => {
  const opts = parseArgs(["--url", "https://example.com/mcp", "--api-key", "sk_live_test"]);
  assert.equal(opts.endpoint, "https://example.com/mcp");
  assert.equal(opts.apiKey, "sk_live_test");
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
    { endpoint: "https://helve.dev/mcp", apiKey: "sk_live_abc", fetchImpl: fakeFetch }
  );
  assert.equal(captured.url, "https://helve.dev/mcp");
  assert.equal(captured.init.headers.Authorization, "Bearer sk_live_abc");
  assert.equal(res.sessionId, "sess_123");
  assert.equal(res.responses[0].id, 1);
});

test("forwardJsonRpc returns missing-key /k/npm error on 401 call_tool", async () => {
  const fakeFetch = async () =>
    new Response(JSON.stringify({ error: { type: "unauthorized", message: "missing key" } }), {
      status: 401,
      headers: { "content-type": "application/json" },
    });
  const res = await forwardJsonRpc(
    { jsonrpc: "2.0", id: 7, method: "tools/call", params: { name: "call_tool", arguments: { tool_id: "serper.search" } } },
    { endpoint: "https://helve.dev/mcp", apiKey: "", fetchImpl: fakeFetch }
  );
  assert.equal(res.responses.length, 1);
  assert.equal(res.responses[0].id, 7);
  assert.equal(res.responses[0].result.isError, true);
  assert.ok(res.responses[0].result.content[0].text.includes(MISSING_KEY_URL));
});

test("CLI writes missing-key notice strictly to stderr and never stdout", () => {
  const env = { ...process.env };
  delete env.HELVE_API_KEY;
  const proc = spawnSync(process.execPath, [BIN_PATH], { input: "", encoding: "utf8", env });
  assert.equal(proc.status, 0);
  assert.equal(proc.stdout, "");
  assert.equal(proc.stderr.trim(), MISSING_KEY_NOTICE);
});

test("CLI stays silent on stderr when HELVE_API_KEY is set", () => {
  const env = { ...process.env, HELVE_API_KEY: "sk_live_test" };
  const proc = spawnSync(process.execPath, [BIN_PATH], { input: "", encoding: "utf8", env });
  assert.equal(proc.status, 0);
  assert.equal(proc.stdout, "");
  assert.equal(proc.stderr, "");
});
