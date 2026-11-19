import asyncio
import unittest
from pydantic_ai_helve import HelveCapability, helve_mcp_server


class TestPydanticAIHelve(unittest.TestCase):
    def test_async_capability(self):
        calls = []

        async def fake_transport(method, url, payload, headers):
            calls.append((method, url, payload))
            return {"ok": True}

        cap = HelveCapability(api_key="sk_live_test", transport=fake_transport)
        asyncio.run(cap.search_tools("speech transcription"))
        asyncio.run(cap.call_tool("helve.audio_transcribe", {"audio_url": "https://example.com/a.mp3", "diarize": True}))
        asyncio.run(cap.request_tool("twilio.sms", "Send SMS notifications to leads", provider="twilio"))

        self.assertEqual(calls[0][1], "https://helve.dev/v1/tools/search")
        self.assertEqual(calls[1][2], {"tool_id": "helve.audio_transcribe", "arguments": {"audio_url": "https://example.com/a.mp3", "diarize": True}})
        self.assertEqual(calls[2][1], "https://helve.dev/v1/tools/request")
        self.assertEqual(calls[2][2]["tool_name"], "twilio.sms")
        cfg = helve_mcp_server("sk_live_test")
        self.assertEqual(cfg["url"], "https://helve.dev/mcp")


if __name__ == "__main__":
    unittest.main()
