import unittest
from helve_mcp import HelveClient, extract_json_from_sse, forward_jsonrpc, parse_args


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
                    "clientInfo": {"name": "helve-mcp-py-test", "version": "2.0.2"},
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

    def test_live_rest_search_tools(self):
        client = HelveClient(api_key="")
        data = client.search_tools("web extract", limit=3)
        self.assertIn("tools", data)
        self.assertTrue(len(data["tools"]) >= 1)


if __name__ == "__main__":
    unittest.main()
