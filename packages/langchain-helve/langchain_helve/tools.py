from __future__ import annotations

import json
import os
from typing import Any, Callable, Dict, List, Optional, Type

try:
    from langchain_core.tools import BaseTool, BaseToolkit
except ImportError:
    class BaseTool:  # type: ignore
        name: str = ""
        description: str = ""
        def __init__(self, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)
        def invoke(self, input_data: Dict[str, Any]) -> Any:
            return self._run(**input_data)

    class BaseToolkit:  # type: ignore
        def __init__(self, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)

try:
    from pydantic import BaseModel, ConfigDict, Field
except ImportError:
    class BaseModel:  # type: ignore
        pass
    def ConfigDict(**kwargs: Any) -> Dict[str, Any]:  # type: ignore
        return kwargs
    def Field(*args: Any, **kwargs: Any) -> Any:  # type: ignore
        return None


class HelveGatewayClient:
    """HTTP client targeting Helve v2 gateway endpoints (/v1/tools, /search, /call, /request)."""

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

    def list_tools(self, category: Optional[str] = None, include_unavailable: bool = False) -> Dict[str, Any]:
        params = []
        if category:
            params.append(f"category={category}")
        if include_unavailable:
            params.append("include_unavailable=true")
        suffix = f"?{'&'.join(params)}" if params else ""
        return self._request("GET", f"/v1/tools{suffix}", require_auth=False)

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


class _SearchToolsInput(BaseModel):
    query: str = Field(..., description="Capability, API, or task description to search on Helve.")
    category: Optional[str] = Field(default=None, description="Optional category filter.")
    limit: int = Field(default=10, description="Maximum number of matching tools to return (1-30).")


class _CallToolInput(BaseModel):
    tool_id: str = Field(..., description="Exact tool_id returned by helve_search_tools.")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Native JSON arguments for the tool.")


class _RequestToolInput(BaseModel):
    tool_name: str = Field(..., description="Missing API or tool name.")
    use_case: str = Field(..., description="Concrete description of what the agent needs to accomplish.")
    provider: Optional[str] = Field(default=None, description="Optional upstream provider name.")
    category: Optional[str] = Field(default=None, description="Optional tool category.")
    docs_url: Optional[str] = Field(default=None, description="Optional link to provider API docs.")


class HelveSearchTools(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = "helve_search_tools"
    description: str = (
        "Search Helve's pay-per-call AI tool gateway for available third-party APIs and free public utilities, "
        "returning tool_id, native input_schema, example, and pricing_hint."
    )
    args_schema: Type[BaseModel] = _SearchToolsInput
    client: Any = None

    def _run(self, query: str, category: Optional[str] = None, limit: int = 10) -> str:
        return json.dumps(self.client.search_tools(query=query, category=category, limit=limit))


class HelveCallTool(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = "helve_call_tool"
    description: str = (
        "Execute any tool_id discovered via helve_search_tools on Helve's metered gateway. "
        "0% per-call markup (exact upstream provider rates); zero charge on free public tools and failed upstream calls."
    )
    args_schema: Type[BaseModel] = _CallToolInput
    client: Any = None

    def _run(self, tool_id: str, arguments: Optional[Dict[str, Any]] = None) -> str:
        return json.dumps(self.client.call_tool(tool_id=tool_id, arguments=arguments or {}))


class HelveRequestTool(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = "helve_request_tool"
    description: str = "Log a missing API or capability on Helve when helve_search_tools returns no match."
    args_schema: Type[BaseModel] = _RequestToolInput
    client: Any = None

    def _run(
        self,
        tool_name: str,
        use_case: str,
        provider: Optional[str] = None,
        category: Optional[str] = None,
        docs_url: Optional[str] = None,
    ) -> str:
        return json.dumps(
            self.client.request_tool(
                tool_name=tool_name,
                use_case=use_case,
                provider=provider,
                category=category,
                docs_url=docs_url,
            )
        )


class HelveToolkit(BaseToolkit):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    client: HelveGatewayClient

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://helve.dev", client: Optional[HelveGatewayClient] = None) -> None:
        resolved_client = client or HelveGatewayClient(api_key=api_key, base_url=base_url)
        super().__init__(client=resolved_client)

    def get_tools(self) -> List[BaseTool]:
        return [
            HelveSearchTools(client=self.client),
            HelveCallTool(client=self.client),
            HelveRequestTool(client=self.client),
        ]
