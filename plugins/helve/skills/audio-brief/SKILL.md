---
name: audio-brief
description: Transcribe prerecorded audio or video (~$0.08/15 min) via Deepgram/AssemblyAI and summarize into an executive brief.
---

# Helve Audio Brief Skill (~$0.08 / 15-min recording)

Transcribe podcasts, earnings calls, or meetings via Deepgram Nova / AssemblyAI and generate a structured summary with one `HELVE_API_KEY` (`sk_live_...`).

## Cost Breakdown (`usage.cost_usd`)

| Step | Tool | Est. Cost |
| --- | --- | --- |
| 1. Audio transcription (15 min) | `transcribe` (`POST /v1/transcriptions`) | `~$0.075` |
| 2. Structured summary brief | `openrouter.chat` (`openai/gpt-4o-mini`) | `~$0.005` |
| **Total per 15-min brief** | **1 key · `$0.50` free = ~6 briefs** | **`~$0.080`** |

## Quickstart (`curl`)

```bash
# 1. Queue transcription job
curl -sS -X POST https://helve.dev/v1/transcriptions \
  -H "Authorization: Bearer $HELVE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "https://example.com/earnings-call.mp3"}'

# 2. Poll GET /v1/jobs/{id}, then summarize via cohere.chat or openrouter.chat
```

## MCP Workflow (`https://helve.dev/mcp`)

1. Call `transcribe(audio_url="https://...")` to get a durable `job_id`.
2. Poll `transcription_status(id=job_id)` until `status === "completed"`.
3. Call `call_tool(tool_id="cohere.chat", arguments={...})` to produce action items and key quotes.
