import os
import subprocess
import sys
import unittest
from helve_mcp import HelveClient, extract_json_from_sse, forward_jsonrpc, parse_args
from helve_mcp.cli import MISSING_KEY_NOTICE, MISSING_KEY_URL


class TestHelveMcp(unittest.TestCase):
    def test_parse_args(self):
        opts = parse_args(["--url", "https://example.com/mcp", "--api-key", "sk_test"])
        self.assertEqual(opts["endpoint"], "https://example.com/mcp")
        self.assertEqual(opts["api_key"], "sk_test")
        self.assertFalse(opts["help"])

    def test_extract_json_from_sse(self):
        sse = 'event: message\ndata: {"jsonrpc":"2.0","id":1,"result":{"ok":true}}\n\ndata: [DONE]\n'
        msgs = extract_json_from_sse(sse)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]["id"], 1)

    def test_live_mcp_initialize_and_tools_list(self):
        res, sid = forward_jsonrpc(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "helve-mcp-py-test", "version": "2.0.6"},
                },
            }
        )
        self.assertTrue(len(res) >= 1)
        self.assertIn("result", res[0])

        tools_res, _ = forward_jsonrpc(
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            session_id=sid,
        )
        self.assertTrue(len(tools_res) >= 1)
        tools = tools_res[0]["result"]["tools"]
        names = {t["name"] for t in tools}
        self.assertIn("search_tools", names)
        self.assertIn("call_tool", names)
        self.assertIn("list_categories", names)

    def test_live_call_tool_missing_key_returns_pypi_url(self):
        res, _ = forward_jsonrpc(
            {
                "jsonrpc": "2.0",
                "id": 9,
                "method": "tools/call",
                "params": {"name": "call_tool", "arguments": {"tool_id": "serper.search", "arguments": {"q": "test"}}},
            },
            api_key="",
        )
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["id"], 9)
        self.assertTrue(res[0]["result"]["isError"])
        self.assertIn(MISSING_KEY_URL, res[0]["result"]["content"][0]["text"])

    def test_cli_missing_key_writes_only_stderr(self):
        env = dict(os.environ)
        env.pop("HELVE_API_KEY", None)
        env["PYTHONPATH"] = os.path.join(os.path.dirname(__file__), "..", "src")
        proc = subprocess.run(
            [sys.executable, "-c", "from helve_mcp.cli import main; raise SystemExit(main())"],
            input="",
            text=True,
            capture_output=True,
            env=env,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(proc.stderr.strip(), MISSING_KEY_NOTICE)

    def test_cli_with_key_stays_silent(self):
        env = dict(os.environ)
        env["HELVE_API_KEY"] = "sk_live_test"
        env["PYTHONPATH"] = os.path.join(os.path.dirname(__file__), "..", "src")
        proc = subprocess.run(
            [sys.executable, "-c", "from helve_mcp.cli import main; raise SystemExit(main())"],
            input="",
            text=True,
            capture_output=True,
            env=env,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(proc.stderr, "")

    def test_live_rest_search_tools(self):
        client = HelveClient(api_key="")
        data = client.search_tools("web extract", limit=3)
        self.assertIn("tools", data)
        self.assertTrue(len(data["tools"]) >= 1)


if __name__ == "__main__":
    unittest.main()
