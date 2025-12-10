# Real Simple Efemera (RSE) v0.1

Purpose: A tiny, append-only timeline format and transport so tools (Minutes Bot, apps, hive servers, viewers) can interoperate.

## 1) Event Shape (JSON Lines)
- File: `.deia/telemetry/rse.jsonl`
- Each line is a single JSON object:
  - `ts` (string, ISO8601, UTC) — timestamp
  - `type` (string) — e.g., minute_start, minute_tick, activity_post, bug_report
  - `lane` (string) — e.g., Minutes, Code, Docs, Bugs, CI, Ops, UI
  - `actor` (string) — Edge | Node | Queen | System
  - `data` (object) — free-form payload

Example:
```
{"ts":"2025-10-14T21:15:00Z","type":"minute_tick","lane":"Minutes","actor":"Edge","data":{"topic":"sprint-14"}}
{"ts":"2025-10-14T21:15:08Z","type":"activity_post","lane":"Code","actor":"Node","data":{"path":"apps/server/src/index.ts"}}
```

## 2) Lanes (recommended)
- Minutes — minute-level narrative from Minutes Bot
- Code — changes, builds, deploys
- Docs — specs, eggs, process updates
- Bugs — bug filed/fixed/verified
- CI — pipeline/health
- Ops — infra events (db/mqtt/server)
- UI — user-facing interactions, demos

## 3) Transport
- File: append-only JSONL as above
- SSE (optional): `/rse/sse` (server-sent events) — sends lines as `data: <json>`
- HTTP (optional): `/rse/feed` — returns newline-delimited JSON

## 4) Producers
- Minutes Bot: emits minute_start, minute_write, minute_tick, minute_stop, minute_report
- Apps/Game: emit domain events (frame/activity_post/etc.)
- DEIA tools: may mirror key actions (session_start, sanitize, submit)

## 5) Consumers
- Local Viewer: reads `.deia/telemetry/rse.jsonl` and animates swimlanes
- Hive Telemetry Server: accepts SSE connections; optional aggregation

## 6) Conventions
- UTC timestamps; ISO8601 with Z
- Do not mutate history; corrections are new events
- Keep `data` small; put large artifacts in docs and reference by path

## 7) Security & Privacy
- Local-first by default; do not transmit without consent
- Redaction step required before sharing publicly

