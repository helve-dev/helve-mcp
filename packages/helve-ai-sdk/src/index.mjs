/**
 * Helve Gateway Client & Tool Definitions for Vercel AI SDK (v4–v7+).
 * Matches live Helve v2 endpoints:
 * - GET  /v1/tools
 * - POST /v1/tools/search   { query, category?, limit?, include_unavailable? }
 * - POST /v1/tools/call     { tool_id, arguments }
 * - POST /v1/tools/request  { tool_name, use_case, provider?, category?, docs_url? }
 */

const DEFAULT_BASE_URL = "https://helve.dev";

export class HelveGatewayClient {
  constructor({ apiKey = process.env.HELVE_API_KEY, baseUrl = DEFAULT_BASE_URL, fetchImpl = fetch } = {}) {
    this.apiKey = apiKey || undefined;
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.fetch = fetchImpl;
  }

  async _request(method, path, body, { requireAuth = true } = {}) {
    if (requireAuth && !this.apiKey) {
      throw new Error("Helve API key is required (pass apiKey or set HELVE_API_KEY).");
    }
    const headers = {
      "Content-Type": "application/json",
    };
    if (this.apiKey) {
      headers.Authorization = `Bearer ${this.apiKey}`;
    }
    const res = await this.fetch(`${this.baseUrl}${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    const text = await res.text();
    let data;
    try {
      data = text ? JSON.parse(text) : {};
    } catch {
      data = { raw: text };
    }
    if (!res.ok) {
      const msg = data?.error?.message || data?.message || `Helve HTTP ${res.status}`;
      const err = new Error(msg);
      err.status = res.status;
      err.data = data;
      throw err;
    }
    return data;
  }

  listTools({ category, includeUnavailable } = {}) {
    const qs = new URLSearchParams();
    if (category !== undefined) qs.set("category", String(category));
    if (includeUnavailable !== undefined) qs.set("include_unavailable", String(Boolean(includeUnavailable)));
    const suffix = qs.toString() ? `?${qs.toString()}` : "";
    return this._request("GET", `/v1/tools${suffix}`, undefined, { requireAuth: false });
  }

  searchTools({ query, category, limit = 10, includeUnavailable } = {}) {
    const payload = { query, limit };
    if (category !== undefined) payload.category = category;
    if (includeUnavailable !== undefined) payload.include_unavailable = Boolean(includeUnavailable);
    return this._request("POST", "/v1/tools/search", payload, { requireAuth: false });
  }

  callTool({ toolId, tool, args, arguments: toolArguments, params, input } = {}) {
    const resolvedToolId = toolId ?? tool;
    if (!resolvedToolId) {
      throw new Error("toolId is required.");
    }
    const resolvedArgs = toolArguments ?? args ?? input ?? params ?? {};
    return this._request("POST", "/v1/tools/call", {
      tool_id: resolvedToolId,
      arguments: resolvedArgs,
    });
  }

  requestTool({ toolName, capability, useCase, description, exampleUseCase, provider, category, docsUrl } = {}) {
    const resolvedToolName = toolName ?? capability;
    const resolvedUseCase = useCase ?? exampleUseCase ?? description;
    if (!resolvedToolName || !resolvedUseCase) {
      throw new Error("toolName and useCase are required.");
    }
    const payload = {
      tool_name: resolvedToolName,
      use_case: resolvedUseCase,
    };
    if (provider !== undefined) payload.provider = provider;
    if (category !== undefined) payload.category = category;
    if (docsUrl !== undefined) payload.docs_url = docsUrl;
    return this._request("POST", "/v1/tools/request", payload, { requireAuth: false });
  }
}

export function createHelveGateway({ apiKey, baseUrl, fetchImpl, toolFn, z } = {}) {
  const client = new HelveGatewayClient({ apiKey, baseUrl, fetchImpl });

  if (toolFn && z) {
    return {
      helve_search_tools: toolFn({
        description:
          "Search Helve's metered pay-per-call tool gateway for available third-party APIs and free public utilities, returning tool_id, native input_schema, example, and pricing_hint.",
        inputSchema: z.object({
          query: z.string().describe("What capability, API, or task you need (e.g. 'sec filings', 'perplexity answer', 'web search')"),
          category: z.string().optional().describe("Optional category filter"),
          limit: z.number().int().min(1).max(30).optional().default(10),
        }),
        execute: async ({ query, category, limit }) => client.searchTools({ query, category, limit }),
      }),
      helve_call_tool: toolFn({
        description:
          "Call any tool_id discovered via helve_search_tools on Helve's metered gateway. 0% per-call markup — exact upstream provider rates ($0.00 on 302 free public tools and failed calls).",
        inputSchema: z.object({
          tool_id: z.string().describe("Exact tool_id returned by helve_search_tools"),
          arguments: z.record(z.unknown()).describe("Native JSON arguments matching the tool's input_schema"),
        }),
        execute: async ({ tool_id, arguments: toolArgs }) =>
          client.callTool({ toolId: tool_id, arguments: toolArgs }),
      }),
      helve_request_tool: toolFn({
        description:
          "Log an unfulfilled tool or API request when helve_search_tools has no matching capability yet.",
        inputSchema: z.object({
          tool_name: z.string().describe("Short name of missing API or tool"),
          use_case: z.string().describe("What the agent needs to accomplish with this tool"),
          provider: z.string().optional(),
          category: z.string().optional(),
          docs_url: z.string().optional(),
        }),
        execute: async (args) => client.requestTool({
          toolName: args.tool_name,
          useCase: args.use_case,
          provider: args.provider,
          category: args.category,
          docsUrl: args.docs_url,
        }),
      }),
    };
  }

  return { client };
}
