# Flights and Recaps (Lean Mode)

## Terms
- **Sprint**: Longer planning window (multi-day or multi-week).
- **Flight**: Short execution burst (hours). Ends with a recap.

## Why
We need durable memory to extract patterns and anti-patterns across hive comms.
Flights provide a lightweight cadence without bloating the system.

## What We Store
### Message Log (raw)
- timestamp
- channel_id
- author
- lane (llm | terminal | local | task_file)
- provider (claude, codex, llama, etc.)
- content
- kb_entities_injected

### Flight Recap (summary)
- flight_id
- start_time / end_time
- goals
- decisions
- tasks completed / open
- bugs found
- patterns / anti-patterns discovered
- costs (optional, if available)

## Capture Flow
1. Flight starts (manual or auto).
2. Messages stream into local log.
3. Flight ends → recap written.
4. Patterns and anti-patterns promoted into RAQCOON KB.

## Embeddings
Optional: add embeddings later for search and pattern detection.
Default: text-only indexing to stay lean.
