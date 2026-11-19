from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, Optional

try:
    from pydantic_ai.capabilities import AbstractCapability
except ImportError:
    class AbstractCapability:  # type: ignore
        pass


@dataclass
class HelveCapability(AbstractCapability):
    """PydanticAI capability exposing Helve's search_tools, call_tool, and request_tool."""

    api_key: str = field(default_factory=lambda: os.environ.get("HELVE_API_KEY", ""))
    base_url: str = "https://helve.dev"
    transport: Optional[Callable[[str, str, Optional[Dict[str, Any]], Dict[str, str]], Awaitable[Dict[str, Any]]]] = None

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")

    async def _request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None, require_auth: bool = True) -> Dict[str, Any]:
        if require_auth and not self.api_key:
            raise ValueError("Helve API key is required (pass api_key or set HELVE_API_KEY).")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        url = f"{self.base_url}{path}"
        if self.transport is not None:
            return await self.transport(method, url, payload, headers)
        import httpx
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.request(method, url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()

    async def search_tools(self, query: str, category: Optional[str] = None, limit: int = 10, include_unavailable: bool = False) -> Dict[str, Any]:
        body: Dict[str, Any] = {"query": query, "limit": limit}
        if category is not None:
            body["category"] = category
        if include_unavailable:
            body["include_unavailable"] = True
        return await self._request("POST", "/v1/tools/search", body, require_auth=False)

    async def call_tool(self, tool_id: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"tool_id": tool_id, "arguments": arguments or {}}
        return await self._request("POST", "/v1/tools/call", body, require_auth=True)

    async def request_tool(
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
        return await self._request("POST", "/v1/tools/request", body, require_auth=False)

    def get_instructions(self) -> str:
        return (
            "You have access to Helve, a metered pay-per-call all-tools gateway. "
            "Always call search_tools first to discover tool_id, native input_schema, and pricing_hint. "
            "Then invoke call_tool with {tool_id, arguments}. If no tool fits, log the gap with request_tool."
        )


def helve_mcp_server(api_key: Optional[str] = None, url: str = "https://helve.dev/mcp") -> Dict[str, Any]:
    """Return connection config for PydanticAI's MCPServerStreamableHTTP."""
    resolved = api_key or os.environ.get("HELVE_API_KEY", "")
    if not resolved:
        raise ValueError("Helve API key is required.")
    return {
        "url": url,
        "headers": {"Authorization": f"Bearer {resolved}"},
    }
