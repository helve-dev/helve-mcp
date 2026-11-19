import test from "node:test";
import assert from "node:assert/strict";
import { HelveGatewayClient, createHelveGateway } from "../src/index.mjs";

test("HelveGatewayClient routes listTools, searchTools, callTool, and requestTool to live v2 schema", async () => {
  const calls = [];
  const mockFetch = async (url, init) => {
    calls.push({ url, method: init.method, headers: init.headers, body: init.body ? JSON.parse(init.body) : null });
    return {
      ok: true,
      status: 200,
      text: async () => JSON.stringify({ ok: true, usage: { cost_usd: 0.00575 } }),
    };
  };

  const client = new HelveGatewayClient({ apiKey: "sk_live_test", fetchImpl: mockFetch });
  await client.listTools({ category: "search" });
  await client.searchTools({ query: "company filings", limit: 5 });
  await client.callTool({ toolId: "exa.answer", arguments: { query: "When was Stripe founded?", text: true } });
  await client.requestTool({ toolName: "easypost.labels", useCase: "Create shipping labels for customer orders", provider: "easypost" });

  assert.equal(calls.length, 4);
  assert.equal(calls[0].url, "https://helve.dev/v1/tools?category=search");
  assert.equal(calls[0].method, "GET");
  assert.equal(calls[1].url, "https://helve.dev/v1/tools/search");
  assert.deepEqual(calls[1].body, { query: "company filings", limit: 5 });
  assert.equal(calls[2].url, "https://helve.dev/v1/tools/call");
  assert.deepEqual(calls[2].body, { tool_id: "exa.answer", arguments: { query: "When was Stripe founded?", text: true } });
  assert.equal(calls[2].headers.Authorization, "Bearer sk_live_test");
  assert.equal(calls[3].url, "https://helve.dev/v1/tools/request");
  assert.deepEqual(calls[3].body, {
    tool_name: "easypost.labels",
    use_case: "Create shipping labels for customer orders",
    provider: "easypost",
  });
});

test("createHelveGateway builds tool definitions when toolFn and z are provided", async () => {
  const fakeZ = {
    string: () => ({ describe: () => ({}), optional: () => ({ describe: () => ({}) }) }),
    number: () => ({
      int: () => ({ min: () => ({ max: () => ({ optional: () => ({ default: () => ({}) }) }) }) }),
    }),
    record: () => ({ describe: () => ({}) }),
    unknown: () => ({}),
    object: (shape) => shape,
  };
  const tools = createHelveGateway({
    apiKey: "sk_live_test",
    fetchImpl: async () => ({ ok: true, status: 200, text: async () => "{}" }),
    toolFn: (def) => def,
    z: fakeZ,
  });

  assert.ok(tools.helve_search_tools);
  assert.ok(tools.helve_call_tool);
  assert.ok(tools.helve_request_tool);
});
