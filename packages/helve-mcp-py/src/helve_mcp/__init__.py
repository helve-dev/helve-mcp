"""Helve MCP bridge and lightweight REST client."""

from .client import HelveClient
from .cli import DEFAULT_ENDPOINT, extract_json_from_sse, forward_jsonrpc, parse_args

__version__ = "2.0.2"
__all__ = [
    "DEFAULT_ENDPOINT",
    "HelveClient",
    "__version__",
    "extract_json_from_sse",
    "forward_jsonrpc",
    "parse_args",
]
