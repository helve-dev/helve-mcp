"""Zero-dependency stdio-to-Streamable-HTTP MCP bridge for https://helve.dev/mcp."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_ENDPOINT = os.environ.get("HELVE_MCP_URL", "https://helve.dev/mcp")
VERSION = "2.0.2"


def parse_args(argv: List[str]) -> Dict[str, Any]:
    endpoint = os.environ.get("HELVE_MCP_URL", "https://helve.dev/mcp")
    api_key = os.environ.get("HELVE_API_KEY", "")
    show_help = False
    show_version = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--url" and i + 1 < len(argv):
            endpoint = argv[i + 1]
            i += 2
        elif arg == "--api-key" and i + 1 < len(argv):
            api_key = argv[i + 1]
            i += 2
        elif arg in ("--help", "-h"):
            show_help = True
            i += 1
        elif arg in ("--version", "-v"):
            show_version = True
            i += 1
        else:
            i += 1

    return {
        "help": show_help,
        "version": show_version,
        "endpoint": endpoint,
        "api_key": api_key,
    }


def extract_json_from_sse(text: str) -> List[Dict[str, Any]]:
    messages: List[Dict[str, Any]] = []
    for line in text.splitlines():
        if line.startswith("data:"):
            payload = line[5:].strip()
            if payload and payload != "[DONE]":
                messages.append(json.loads(payload))
    return messages


def forward_jsonrpc(
    message: Dict[str, Any],
    *,
    endpoint: str = DEFAULT_ENDPOINT,
    api_key: str = "",
    session_id: str = "",
    timeout: float = 120.0,
) -> Tuple[List[Dict[str, Any]], str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": f"helve-mcp-py/{VERSION}",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if session_id:
        headers["mcp-session-id"] = session_id

    data = json.dumps(message).encode("utf-8")
    req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            next_session_id = resp.headers.get("mcp-session-id") or session_id
            content_type = resp.headers.get("content-type", "")
            text = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        next_session_id = exc.headers.get("mcp-session-id") if exc.headers else session_id
        body = exc.read().decode("utf-8", errors="replace")
        if "id" in message:
            return (
                [
                    {
                        "jsonrpc": "2.0",
                        "id": message["id"],
                        "error": {
                            "code": -32000,
                            "message": f"HTTP {exc.code}: {body[:500]}",
                        },
                    }
                ],
                next_session_id or session_id,
            )
        return [], next_session_id or session_id

    if not text or status in (202, 204):
        return [], next_session_id

    if "text/event-stream" in content_type or text.lstrip().startswith("event:") or text.lstrip().startswith("data:"):
        return extract_json_from_sse(text), next_session_id

    parsed = json.loads(text)
    if isinstance(parsed, list):
        return parsed, next_session_id
    return [parsed], next_session_id


def main(argv: Optional[List[str]] = None) -> int:
    opts = parse_args(sys.argv[1:] if argv is None else argv)
    if opts["version"]:
        sys.stdout.write(f"helve-mcp {VERSION}\n")
        return 0
    if opts["help"]:
        sys.stdout.write(
            "helve-mcp - stdio-to-Streamable-HTTP MCP bridge for Helve (https://helve.dev/mcp)\n\n"
            "Usage:\n"
            "  HELVE_API_KEY=sk_live_... helve-mcp [--url https://helve.dev/mcp] [--api-key KEY]\n\n"
            "Options:\n"
            "  --url URL        Remote MCP endpoint (default: https://helve.dev/mcp)\n"
            "  --api-key KEY    Helve API key (default: $HELVE_API_KEY)\n"
            "  -v, --version    Show version and exit\n"
            "  -h, --help       Show this help message and exit\n"
        )
        return 0

    endpoint = opts["endpoint"]
    api_key = opts["api_key"]
    session_id = ""

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            sys.stderr.write(f"helve-mcp: invalid JSON on stdin: {exc}\n")
            continue

        try:
            responses, session_id = forward_jsonrpc(
                message,
                endpoint=endpoint,
                api_key=api_key,
                session_id=session_id,
            )
            for response in responses:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
        except Exception as exc:  # noqa: BLE001
            if isinstance(message, dict) and "id" in message:
                err = {
                    "jsonrpc": "2.0",
                    "id": message["id"],
                    "error": {"code": -32603, "message": str(exc)},
                }
                sys.stdout.write(json.dumps(err) + "\n")
                sys.stdout.flush()
            else:
                sys.stderr.write(f"helve-mcp: bridge error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
