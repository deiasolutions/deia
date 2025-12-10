---
intended_path: docs/specs/pheromone-rsm-protocol-v0.1.md
status: EMBARGOED (ROTG-2 active)
version: 0.1
date: 2025-10-15
authors:
  - OpenAI (Hummingbird Moth, "Whisperwing")
tags: [#protocol, #rse, #rsm, #governance, #embargo]
---

# Pheromone–RSM Protocol (v0.1)

Executive summary: A minimal, lock-aware protocol that turns RSE "pheromone" events into decentralized routing of Markdown envelopes (RSM) for hive coordination. Optimized for local-first operation, additive logging, and strict respect for ROTG-2/DNR policies.

## 0) Scope & Assumptions
- Local-first; no central broker required.
- Observability: RSE JSONL at `.deia/telemetry/rse.jsonl` when permitted; otherwise advisory-only mode.
- Transport: File-based inbox/outbox by default; pluggable to HTTP/SSE/MQTT later.
- Governance: Honor locks — DNR (highest), do-not-alter, do-not-erase (ROTG-2). If uncertain, do not read/write; emit advisory pheromone.
- Embargo note: This spec is staged outside `.deia`; routes point to final locations for when release is authorized.

## 1) Glossary
- Pheromone: An RSE event that signals state/intent (e.g., need, offer, ack).
- RSM Envelope: A Markdown message with a YAML header for routing, consent, and signatures.
- Inbox: A directory watched by a Queen or worker for new envelopes.
- Queen: A coordinating agent (human/AI) that senses pheromones and assigns work.
- Worker/Drone: An execution agent that performs tasks and reports via pheromones/envelopes.

## 2) RSE Event Taxonomy (Minimal Set)
RSE line format: `{ts, type, lane, actor, data}` (JSONL)

- `pheromone_drop` (producer announces something to sense)
  - lane: Governance|Process|Code|Ops|Bugs|Docs|UI
  - data: `{topic, priority, ref?, ttl?, tags?}`
- `pheromone_sense` (consumer observed a signal)
  - data: `{ref, actor_state?}`
- `rsm_envelope_emit` (envelope created and dispatched)
  - data: `{id, to[], priority, ttl, path, hash}`
- `rsm_envelope_recv` (envelope received to inbox)
  - data: `{id, from, inbox, hash}`
- `queen_select` (queen selects next action)
  - data: `{basis: pheromone|inbox, id/ref, rationale}`
- `worker_spawn` (scoped worker created)
  - data: `{name, scope, ttl, parent}`
- `worker_ack` (work acknowledged/done)
  - data: `{ref, status: accepted|done|error, notes?}`
- `backpressure` (queue or rate signal)
  - data: `{inbox_depth, oldest_age_s, action}`
- `policy_guard` (lock detected/honored)
  - data: `{lock: dnr|do-not-erase|do-not-alter, path, mode: advisory|blocked}`

Examples (JSONL):
```
{"ts":"2025-10-15T17:10:00Z","type":"pheromone_drop","lane":"Governance","actor":"Whisperwing","data":{"topic":"pheromone-rsm-v0.1","priority":"P1","ttl":"1h"}}
{"ts":"2025-10-15T17:11:00Z","type":"rsm_envelope_emit","lane":"Process","actor":"Whisperwing","data":{"id":"01JBRM6WQ4...","to":["queen://governance"],"priority":"P1","ttl":"1h","path":".deia/inbox/governance/01JBRM...md","hash":"sha256:..."}}
```

## 3) RSM Envelope Schema (YAML header)
Header fields (minimal, extensible):
```
id: <ULID|UUID>
ts: <ISO8601Z>
from: <actor-id>
to: [<address>, ...]            # e.g., queen://governance, lane://Code
reply_to: <address?>            # optional
correlation_id: <id?>
lane: Governance|Process|Code|Ops|Bugs|Docs|UI
topic: <string>
priority: P0|P1|P2|P3          # P0 highest
ttl: <duration>
scope: <path|resource|capability>
consent: public|team|private   # default team/local
sig: <ed25519|hmac>-<hex>      # provenance
hash: sha256:<hex>             # body checksum
tags: [<str>, ...]
```
Body: Markdown. Keep < 64KB; attach large artifacts by path and include hashes.

Example envelope (Markdown):
```
---
id: 01JBRM7XCN6E9M6KQGM6K3J3E5
ts: 2025-10-15T17:12:03Z
from: Whisperwing
to: ["queen://governance"]
lane: Governance
topic: Pheromone–RSM Protocol v0.1 review
priority: P1
ttl: 1h
scope: docs/specs/pheromone-rsm-protocol-v0.1.md
consent: team
sig: hmac-<hex>
hash: sha256:<hex>
tags: [protocol, review]
---

Please review sections 2–6 for completeness and safety gates.
```

## 4) Routing, Gradients, and Inbox Semantics
- Routing: Addresses use schemes (`queen://<domain>`, `lane://<lane>`, `user://<id>`). Queens resolve to inbox folders.
- Default inbox layout (production): `.deia/inbox/<domain>/`. When locks active, use advisory mode or a safe mirror (e.g., `.embargo/inbox/`).
- Prioritization: `P0..P3` with FIFO within same priority. Age-based decay reduces effective priority over time.
- Decay/TTL: Exponential decay `w(t)=w0*e^{-λt}` with expiry at TTL; expired envelopes are archived, not deleted.
- Dedupe/Idempotency: Maintain a seen-set keyed by `id|hash`. Reprocessing is idempotent; multiple identical envelopes collapse to one effect.
- Backpressure: When `inbox_depth > threshold` or `oldest_age_s > SLO`, emit `backpressure` pheromone and throttle producers.

## 5) Canonical Flows
1) Produce & Dispatch
   - Producer emits `pheromone_drop` → creates envelope → writes to target inbox (or advisory if locked) → emits `rsm_envelope_emit`.
2) Sense & Select
   - Queen watches RSE/inbox → emits `pheromone_sense` → selects work (`queen_select`).
3) Act & Ack
   - Worker spawns (`worker_spawn`) → performs work → acknowledges (`worker_ack`) → optional reply envelope.
4) Error & Retry
   - On failure, keep envelope, annotate status, re-emit `pheromone_drop` with downgraded priority or increased context.
5) Backpressure & Drain
   - Emit `backpressure` when thresholds triggered; selection algorithm favors high-priority and oldest items.

## 6) Safety Gates (Governance Compliance)
- Lock checks: Before read/write, call local policy guard (e.g., `.deia/tools/policy_guard.*`). If DNR or ROTG-2 is active, do not read/write; emit `policy_guard` pheromone.
- Consent: Use `consent` header; default to team/local. Public requires explicit flag.
- Audit: RSE-only append; never rewrite history. Corrections are new events.
- Redaction: Provide a redaction step for envelopes moving from local to public contexts.
- Attestation (DNR): Future-proof hook to check `.deia/do-not-read/` lists before reading.

## 7) Minimal Adapter Interfaces

TypeScript pseudo-interface:
```
interface RSEEmitter { emit(e: {ts?: string; type: string; lane: string; actor: string; data: any}): Promise<void>; }
interface RSMTransport {
  send(env: Envelope, bodyMd: string): Promise<{path?: string; hash: string}>;
  recv(inbox: string): AsyncIterable<{env: Envelope; bodyMd: string; path: string}>;
}
```

Python (using existing helper):
```
from src.efemera.rse import log_rse
log_rse(type="pheromone_drop", lane="Governance", actor="Whisperwing", data={"topic":"pheromone-rsm-v0.1","priority":"P1"})
```

## 8) Metrics & SLOs
- E2E latency (emit→ack): P50 ≤ 2m, P95 ≤ 10m (local)
- Delivery ratio: ≥ 99% within TTL
- Duplicates: ≤ 0.5%
- Observability coverage: ≥ 95% of core actions reflected in RSE
- Policy violations: 0 (hard requirement)
- Backpressure recovery: queue drains to target within 30m under normal load

## 9) Reference Implementation Plan
- Sprint 0: Spec + local file inbox watcher (read-only dry run) + RSE emitters.
- Sprint 1: Write-capable file transport with policy guard integration; dedupe set; CLI tools.
- Sprint 2: Pluggable transports (HTTP/SSE/MQTT) behind same interface; tests; docs.

## 10) Test Plan (Local)
- Lock compliance: With ROTG-2 active, attempts to write/read `.deia` result in advisory-only behavior and `policy_guard` events.
- Inbox cycle: Create N envelopes, verify sense/select/ack order and metrics.
- Dedupe/idempotency: Re-inject identical envelope; ensure single effect.
- TTL/decay: Expire envelopes; verify archival and no processing.
- Backpressure: Simulate queue growth; verify `backpressure` and throttling.

## 11) Release Criteria
- All safety gates validated; no policy violations.
- Metrics within SLO for local file transport.
- Clear docs and examples; adapters for Python/TS stubs.

## 12) Risks & Mitigations
- Misrouted writes under locks → Strict guard; embargo mirrors.
- Envelope sprawl → TTL + archival + dedupe.
- Human/AI coordination drift → Pheromone taxonomy + dashboards (later).

---
Appendix A: Example Artifacts

1) RSE JSONL lines
```
{"ts":"2025-10-15T17:30:00Z","type":"queen_select","lane":"Governance","actor":"Whisperwing","data":{"basis":"inbox","id":"01J...","rationale":"P1 and oldest"}}
{"ts":"2025-10-15T17:32:00Z","type":"worker_ack","lane":"Governance","actor":"Whisperwing","data":{"ref":"01J...","status":"done"}}
```

2) Envelope header template (copy/paste)
```
---
id: <ULID>
ts: <ISO8601Z>
from: <actor>
to: ["queen://<domain>"]
lane: <lane>
topic: <string>
priority: P0|P1|P2|P3
ttl: <duration>
scope: <path|capability>
consent: team
sig: hmac-<hex>
hash: sha256-<hex>
tags: []
---

<markdown body>
```

