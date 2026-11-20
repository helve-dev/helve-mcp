from __future__ import annotations

import os
from typing import Any, Callable, Dict, List, Optional

try:
    from llama_index.core.tools.tool_spec.base import BaseToolSpec
except ImportError:
    class BaseToolSpec:  # type: ignore
        spec_functions: List[str] = []


class HelveToolSpec(BaseToolSpec):
    """LlamaIndex ToolSpec for Helve's metered pay-per-call all-tools gateway."""

    spec_functions = ["search_tools", "call_tool", "request_tool"]

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
        """Search Helve's catalog for available third-party tools, native input_schema, and pricing_hint."""
        body: Dict[str, Any] = {"query": query, "limit": limit}
        if category is not None:
            body["category"] = category
        if include_unavailable:
            body["include_unavailable"] = True
        return self._request("POST", "/v1/tools/search", body, require_auth=False)

    def call_tool(self, tool_id: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a discovered Helve tool_id per-call (0% per-call markup — exact upstream provider rates; $0.00 on failed calls)."""
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
        """Request a missing tool or API to be onboarded onto Helve."""
        body: Dict[str, Any] = {"tool_name": tool_name, "use_case": use_case}
        if provider is not None:
            body["provider"] = provider
        if category is not None:
            body["category"] = category
        if docs_url is not None:
            body["docs_url"] = docs_url
        return self._request("POST", "/v1/tools/request", body, require_auth=False)
