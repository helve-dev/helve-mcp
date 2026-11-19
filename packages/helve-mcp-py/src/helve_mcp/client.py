"""Zero-dependency REST client for Helve's v2 tool gateway (https://helve.dev)."""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

DEFAULT_BASE_URL = "https://helve.dev"


class HelveClient:
    """Minimal Python client for Helve's v2 tool discovery and invocation API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 120.0,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("HELVE_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        if params:
            filtered = {k: v for k, v in params.items() if v is not None}
            if filtered:
                url = f"{url}?{urllib.parse.urlencode(filtered)}"

        headers = {
            "Accept": "application/json",
            "User-Agent": "helve-mcp-py/2.0.2",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def list_tools(self) -> Dict[str, Any]:
        """List Helve's full live tool catalog via GET /v1/tools (no auth required)."""
        return self._request("GET", "/v1/tools")

    def search_tools(
        self,
        query: Optional[str] = None,
        *,
        category: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Search or browse Helve's live tool catalog via POST /v1/tools/search (no auth required)."""
        payload: Dict[str, Any] = {"limit": limit}
        if query is not None:
            payload["query"] = query
        if category is not None:
            payload["category"] = category
        return self._request("POST", "/v1/tools/search", payload=payload)

    def call_tool(
        self,
        tool_id: str,
        arguments: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Invoke any Helve tool by tool_id via POST /v1/tools/call."""
        return self._request(
            "POST",
            "/v1/tools/call",
            payload={"tool_id": tool_id, "arguments": arguments or {}},
        )

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Poll an async job (such as audio transcription) via GET /v1/jobs/{id}."""
        return self._request("GET", f"/v1/jobs/{urllib.parse.quote(job_id, safe='')}")

    def request_tool(
        self,
        tool_name: str,
        use_case: str,
        *,
        category: Optional[str] = None,
        provider_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Log a missing third-party tool or API via POST /v1/tools/request."""
        payload: Dict[str, Any] = {"tool_name": tool_name, "use_case": use_case}
        if category:
            payload["category"] = category
        if provider_url:
            payload["provider_url"] = provider_url
        return self._request("POST", "/v1/tools/request", payload=payload)
