import unittest
from agent_framework_helve import HelveToolsGateway, smolagents_tool_specs


class TestAgentFrameworkHelve(unittest.TestCase):
    def test_gateway_and_smolagents_specs(self):
        calls = []

        def fake_transport(method, url, payload, headers):
            calls.append((method, url, payload))
            return {"ok": True}

        gw = HelveToolsGateway(api_key="sk_live_test", transport=fake_transport)
        self.assertEqual(len(gw.as_callables()), 3)
        gw.search_tools("browser")
        gw.call_tool("firecrawl.map", {"url": "https://helve.dev", "limit": 20})
        gw.request_tool("e2b.sandbox", "Execute untrusted Python code in cloud sandbox", provider="e2b")
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[1][2], {"tool_id": "firecrawl.map", "arguments": {"url": "https://helve.dev", "limit": 20}})
        self.assertEqual(calls[2][2]["tool_name"], "e2b.sandbox")
        self.assertEqual(calls[2][2]["use_case"], "Execute untrusted Python code in cloud sandbox")
        specs = smolagents_tool_specs()
        self.assertIn("helve/tool-search", specs)
        self.assertIn("helve/call-tool", specs)
        self.assertIn("helve/request-tool", specs)


if __name__ == "__main__":
    unittest.main()
