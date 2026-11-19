import json
import unittest
from langchain_helve import HelveGatewayClient, HelveToolkit


class TestLangChainHelve(unittest.TestCase):
    def test_toolkit_routing(self):
        recorded = []

        def fake_transport(method, url, payload, headers):
            recorded.append((method, url, payload, headers))
            return {"ok": True, "url": url}

        client = HelveGatewayClient(api_key="sk_live_test", transport=fake_transport)
        toolkit = HelveToolkit(client=client)
        tools = {t.name: t for t in toolkit.get_tools()}

        self.assertEqual(set(tools.keys()), {"helve_search_tools", "helve_call_tool", "helve_request_tool"})

        res1 = json.loads(tools["helve_search_tools"]._run(query="enrichment", limit=3))
        res2 = json.loads(tools["helve_call_tool"]._run(tool_id="exa.answer", arguments={"query": "helve", "text": True}))
        res3 = json.loads(tools["helve_request_tool"]._run(tool_name="lob.postcards", use_case="Send direct mail to leads", provider="lob"))

        self.assertTrue(res1["ok"])
        self.assertTrue(res2["ok"])
        self.assertTrue(res3["ok"])
        self.assertEqual(recorded[0][1], "https://helve.dev/v1/tools/search")
        self.assertEqual(recorded[1][1], "https://helve.dev/v1/tools/call")
        self.assertEqual(recorded[1][2], {"tool_id": "exa.answer", "arguments": {"query": "helve", "text": True}})
        self.assertEqual(recorded[2][1], "https://helve.dev/v1/tools/request")
        self.assertEqual(recorded[2][2], {"tool_name": "lob.postcards", "use_case": "Send direct mail to leads", "provider": "lob"})


if __name__ == "__main__":
    unittest.main()
