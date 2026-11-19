import unittest
from llama_index.tools.helve import HelveToolSpec


class TestLlamaIndexHelve(unittest.TestCase):
    def test_spec_functions(self):
        calls = []

        def fake_transport(method, url, payload, headers):
            calls.append((method, url, payload))
            return {"ok": True}

        spec = HelveToolSpec(api_key="sk_live_test", transport=fake_transport)
        self.assertEqual(spec.spec_functions, ["search_tools", "call_tool", "request_tool"])
        spec.search_tools("web search", limit=5)
        spec.call_tool("perplexity.answer", {"query": "What is MCP?", "model": "sonar", "max_tokens": 250})
        spec.request_tool("browserbase.session", "Run headless browser sessions for JS-heavy pages", provider="browserbase")
        self.assertEqual([c[1] for c in calls], [
            "https://helve.dev/v1/tools/search",
            "https://helve.dev/v1/tools/call",
            "https://helve.dev/v1/tools/request",
        ])
        self.assertEqual(calls[1][2], {"tool_id": "perplexity.answer", "arguments": {"query": "What is MCP?", "model": "sonar", "max_tokens": 250}})
        self.assertEqual(calls[2][2]["tool_name"], "browserbase.session")
        self.assertEqual(calls[2][2]["use_case"], "Run headless browser sessions for JS-heavy pages")


if __name__ == "__main__":
    unittest.main()
