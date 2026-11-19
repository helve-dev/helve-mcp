from __future__ import annotations

import os
from typing import Any, Callable, Dict, List, Optional


class HelveToolsGateway:
    """Framework-agnostic Python gateway client & tool definitions for Microsoft Agent Framework, CrewAI, Agno, and Smolagents."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://helve.dev",
        transport: Optional[Callable[[str, str, Optional[Dict[str, Any]], Dict[str, str]], Dict[str, Any]]] = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("HELVE_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self._transport = transport

    def _request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None, require_auth: bool = True) -> Dict[str, Any]:
        if require_auth and not self.api_key:
            raise ValueError("Helve API key is required (pass api_key or set HELVE_API_KEY).")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        url = f"{self.base_url}{path}"
        if self._transport is not None:
            return self._transport(method, url, payload, headers)
        import httpx
        with httpx.Client(timeout=60.0) as client:
            resp = client.request(method, url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()

    def search_tools(self, query: str, category: Optional[str] = None, limit: int = 10, include_unavailable: bool = False) -> Dict[str, Any]:
        body: Dict[str, Any] = {"query": query, "limit": limit}
        if category is not None:
            body["category"] = category
        if include_unavailable:
            body["include_unavailable"] = True
        return self._request("POST", "/v1/tools/search", body, require_auth=False)

    def call_tool(self, tool_id: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"tool_id": tool_id, "arguments": arguments or {}}
        return self._request("POST", "/v1/tools/call", body, require_auth=True)

    def request_tool(
        self,
        tool_name: str,
        use_case: str,
        provider: Optional[str] = None,
        category: Optional[str] = None,
        docs_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {"tool_name": tool_name, "use_case": use_case}
        if provider is not None:
            body["provider"] = provider
        if category is not None:
            body["category"] = category
        if docs_url is not None:
            body["docs_url"] = docs_url
        return self._request("POST", "/v1/tools/request", body, require_auth=False)

    def as_callables(self) -> List[Callable[..., Dict[str, Any]]]:
        return [self.search_tools, self.call_tool, self.request_tool]


def smolagents_tool_specs() -> Dict[str, Dict[str, Any]]:
    """Metadata specs for publishing `helve/tool-search`, `helve/call-tool`, and `helve/request-tool` on Hugging Face Hub."""
    return {
        "helve/tool-search": {
            "name": "helve_search_tools",
            "description": "Search Helve's metered all-tools gateway for third-party APIs, native input_schema, and pricing_hint.",
            "inputs": {
                "query": {"type": "string", "description": "Capability or API to search"},
                "limit": {"type": "integer", "description": "Max tools to return (1-30)", "nullable": True},
            },
            "output_type": "object",
        },
        "helve/call-tool": {
            "name": "helve_call_tool",
            "description": "Call any discovered tool_id on Helve's metered gateway with $0 debit on failed calls.",
            "inputs": {
                "tool_id": {"type": "string", "description": "Exact tool_id from helve_search_tools"},
                "arguments": {"type": "object", "description": "Native arguments matching the tool's input_schema"},
            },
            "output_type": "object",
        },
        "helve/request-tool": {
            "name": "helve_request_tool",
            "description": "Request a missing tool or API when helve_search_tools has no match.",
            "inputs": {
                "tool_name": {"type": "string", "description": "Missing tool or API name"},
                "use_case": {"type": "string", "description": "Use case details"},
            },
            "output_type": "object",
        },
    }
