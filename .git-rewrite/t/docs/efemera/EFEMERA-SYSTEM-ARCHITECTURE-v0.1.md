# Efemera System Architecture (v0.1)

repot_references:
- index: docs/REPOT.md
- process: docs/process/EFEMERA-DEV-PROCESS.md
- telemetry_standard: docs/observability/RSE-0.1.md
- eggs: docs/projects/

## 1) Canon & Glossary
- Queen: Orchestrator of a Hive (team of bots + humans). May coordinate multiple Hives when elevated.
- Queen-of-Queens: Meta-orchestrator coordinating one-to-many Queens across Hives (governed spawn only).
- Leftenant Queen: Ephemeral deputy (TTL-limited). Cannot spawn new Queens unless policy gates pass.
- Hive: Cohesive unit of bots (Nodes) and humans (Edges) managed under a Queen.
- Edge: Human participant (devices, identity, consent, presence).
- Node: Non-human participant (bots, brands, services).
- Egg: Self-contained spec/scaffold that can hatch code, docs, infra, or process.
- NB (Note Bee): Shorthand for important notes; used in docs/chats to flag attention items.

## 2) Governance & Safety
- No Jailbreaker Bakers: Hives must report to the Deia Common Hive (at minimum bugs). Eggs must not permit unreporting hives.
- Leftenant TTL: Leftenant Queens are ephemeral (default TTL=24h) and cannot spawn nested Queens without governance approval and audit logging.
- Reporting Obligations: 1) Bugs to Common Hive, 2) Enhancements encouraged, 3) Shared innovations under MIT.
- Pip Reputation (binary pips):
  - Pip 1: Reports bugs consistently
  - Pip 2: Enhancement suggestions at healthy cadence (e.g., >=1 per 10 bugs)
  - Pip 3: Shares innovations under MIT license
  - Pip 4: Positive social karma (efemera.live)
  - Pip 5: Global council (Dave)

## 3) Runtime Topology
- Single Hive: Queen -> Drones/Services -> Edges/Nodes
- Multi-Hive: Queen-of-Queens -> Queens (per Hive) -> Hives
- Spawning Rules: Only via governed Eggs; Leftenant cannot bypass reporting; all spawns record audit events.
- Observability: All participants emit RSE events; DEIA sessions capture human decisions.

## 4) Observability Baseline (RSE 0.1 + DEIA)
- RSE feed: Append-only JSONL at `.deia/telemetry/rse.jsonl` with fields `{ts,type,lane,actor,data}`.
- DEIA Telemetry: JSONL at `.deia/telemetry/telemetry.jsonl` for system events.
- Minutes Bot: Minute-level Markdown + RSE mirroring for project narrative.
- SSE: Optional `/rse/sse` endpoint for live viewers.

## 5) Identity, Consent, Privacy (v0.1)
- Identity Binding: Edges identified per local project (user/device). Nodes registered per service.
- Consent Defaults: Share-on-consent (recommended). Require explicit flags in Activity payloads.
- Provenance: Activities must include actor, role (Edge/Node), timestamp, and optional signature.

## 6) Eggs & Installers
- Outer/Install Eggs must:
  - Start a DEIA session at hatch (mandatory)
  - Include Repot Pointers
  - Emit telemetry and expose a bot seam (`window.EdgeAPI` or equivalent)
  - Enforce No-Jailbreaker Bakers policy gates

## 7) Initial Sprints & Acceptance
- Sprint 0 (Governance & Observability):
  - Docs: this architecture + RSE 0.1
  - Minutes Bot MVP (done)
  - Acceptance: Minute logs present; RSE feed emitted; DEIA session updated
- Sprint 1 (Queen/Hive + Social Edge Graft skeleton):
  - Hatch Social Edge Graft Install Egg (opt-in LLM OFF by default)
  - Minimal server + EdgeAPI + telemetry wiring
  - Acceptance: Health checks, activity echo, telemetry events, basic viewer
- Sprint 2 (Trust/Moderation):
  - Consent flags, moderation hooks, provenance checks
  - Acceptance: Events flagged/handled; logs recorded; minimal UI

## 8) KPIs (v0.1)
- TTI to first activity: <= 10 minutes from hatch
- Telemetry completeness: >= 95% of core actions reflected in RSE feed
- Reporting: Bugs filed to Common Hive on failures (>= 1 per critical issue)

## 9) Risks
- Decentralized identity assumptions; start local-only then expand
- LLM integration scope creep; keep opt-in and observable
- Cross-hive consistency; use RSE as the lingua franca
