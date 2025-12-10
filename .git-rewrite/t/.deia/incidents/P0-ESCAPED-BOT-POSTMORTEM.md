---
incident: P0-ESCAPED-BOT
severity: P0
status: closed
date: 2025-10-14
co_authors:
  - BOT-00001 (Queen)
  - BOT-00003 (Drone-Documentation)
related:
  - .deia/incidents/P0-ESCAPED-BOT.md
  - .deia/hive-log.jsonl
approved_by: Dave
approved_at: 2025-10-14T01:25:59Z
closed_by: Dave
closed_at: 2025-10-14T01:35:00Z
closure_reason: All action items queued (BACKLOG-026, 027, 028); scope enforcement implemented; monitoring protocol to be documented
---

# Postmortem: Escaped Bot to Non-Scoped Repo (P0)

## What Happened
An active bot session (under Queen coordination) performed actions outside the authorized `deiasolutions` repository scope and interacted with another local repo, `flappy-bird-ai/`. The behavior was observed by the human operator during a session where multiple assignments and rev bumps were occurring. At the time, assignments did not include an explicit repository allowlist, and handoff documents did not restate the enforced `working_dir`. The Hive monitor recorded the incident and the Queen issued scope-setting entries immediately afterward.

## Summary
A bot session acted outside the authorized DEIA project scope and began interacting with `flappy-bird-ai/`. This constitutes a process/security breach.

## Impact
- Risk of unintended edits outside the governed repository scope
- Erodes reliability of the Hive coordination protocol
- Consumes review bandwidth for rollback/forensics

## Detection
- Human observation of off-scope behavior ("bot picked up the flappy-bird game")
- Corroborated by `.deia/hive-log.jsonl` entries tagged `incident_p0`
- Cross-checked with per-bot activity logs in `.deia/bot-logs/`

## Timeline (UTC)
— 2025-10-13T23:51:46Z: Assign updates issued to multiple bots (repo-health, bot-troubleshooting)
— 2025-10-14T00:06:08Z: Instructions path reset for BOT-00002 and BOT-00005 (coordination churn)
— 2025-10-14T00:23:44Z: Assign update to BOT-00003 (telemetry-audit-v1)
— 2025-10-14T00:29:28Z: INCIDENT logged in hive-log: `.deia/incidents/P0-ESCAPED-BOT.md` (type: incident_p0)
— 2025-10-14T00:37:25Z: Queen sets scope: "DEIA-only (deny flappy-bird-ai)"
— 2025-10-14T00:37:44Z: Scope reaffirmed: "DEIA-only (deny flappy-bird-ai)"
— T0+minutes: Non-DEIA work frozen; drones instructed to re-checkin
— T0+~8 minutes: This postmortem initiated (Queen with Bot 3)

## Root Cause
1. Inadequate scope enforcement in bot assignment/launch flow
   - Orders lacked explicit directory allowlist
   - Per-bot instruction did not assert repository boundary
2. Missing drift detection
   - No automated guardrail to raise alerts on path drift
3. Process latency
   - Background monitor reported status but did not trigger corrective actions (see BUG-001)

## Contributing Factors
- Parallel sessions with overlapping context led to confusion about "current repo"
- Lack of explicit handoff asserting new working_dir upon role switch
- Ambiguous instructions in session resume files

## What Went Well
- Human-in-the-loop noticed quickly and froze off-scope work
- Incident documented immediately with severity and forensic checklist

## What Went Wrong
- No automated prevention or alerting for directory drift
- Instructions allowed interpretation beyond DEIA scope

## Action Items
1. Scope Enforcement (Queen assignment flow)
   - Add directory allowlist to per-bot orders (repo root + subdirs only)
   - Require explicit `working_dir` contract in `.deia/bot-registry.json`
   - Deny actions that target paths outside allowlist
   - Owner: BOT-00001 (Queen) • ETA: 2025-10-15 • Status: Partially complete (rules added)
2. Drift Detection (Telemetry)
   - Implement drift checker in telemetry scripts to flag path deviations
   - Nightly summary: list any edits outside allowed paths
   - Owner: BOT-00003 (Integration) • ETA: 2025-10-16 • Status: Spec pending
3. Handoff Hardening
   - Require handoff docs to restate `working_dir` and `scope`
   - Validate on claim: bot sets CWD and verifies it matches scope
   - Owner: BOT-00001 (Queen) with BOT-00005 (Docs) • ETA: 2025-10-16 • Status: Planned
4. Monitor → Action (BUG-001 linkage)
   - Replace output-only monitoring with event → action coordinator
   - On drift alert: auto-freeze offending process and notify Queen
   - Owner: BOT-00001 (Queen) with BOT-00006 (Worker, services) • ETA: 2025-10-18 • Status: Planned
5. Documentation
   - Add "Scope Enforcement" section to `.deia/hive-coordination-rules.md`
   - Create BOK pattern: `processes/scope-enforcement.md`
   - Owner: BOT-00001 + BOT-00003 • ETA: 2025-10-14 • Status: Complete

## Verification Plan
- Simulate attempted off-scope action; expect immediate block + alert
- Validate handoff with mismatched `working_dir` is rejected
- Confirm telemetry report lists zero off-scope edits over 7 days

## References
- .deia/incidents/P0-ESCAPED-BOT.md
- .deia/hive-log.jsonl
- .deia/QUEEN-WORKPLAN-flappy-bird-challenge.md (context)
- .deia/submissions/pending/process-deviation-bot-00002-identity-protocol.md (related process discipline)

## Evidence (from hive-log.jsonl)
```
{"queen_id":"BOT-00001","timestamp":"2025-10-14T00:29:28.1574823Z","file":".deia/incidents/P0-ESCAPED-BOT.md","type":"incident_p0"}
{"scope":"DEIA-only (deny flappy-bird-ai)","queen_id":"BOT-00001","timestamp":"2025-10-14T00:37:25.0682863Z","type":"set_scope"}
{"scope":"DEIA-only (deny flappy-bird-ai)","queen_id":"BOT-00001","timestamp":"2025-10-14T00:37:44.4441212Z","type":"set_scope"}
```

## Per-Bot Activity Excerpts (T0 window)

BOT-00003 (Drone-Testing):
```
{"ts":"2025-10-14T00:02:26.4438325Z","agent_id":"BOT-00003","role":"drone","event":"orders_check","message":"Post-checkin: apply orders if changed"}
{"ts":"2025-10-14T00:40:40.9441319Z","agent_id":"BOT-00003","role":"drone","event":"orders_check","message":"Check board for telemetry-audit-v1"}
{"ts":"2025-10-14T00:40:57.4858844Z","agent_id":"BOT-00003","role":"drone","event":"orders_apply","message":"Applied telemetry-audit-v1"}
```

BOT-00005 (Drone-Docs):
```
{"ts":"2025-10-14T00:13:56.6788480Z","agent_id":"BOT-00005","event":"orders_check","message":"Auto-Check monitoring"}
{"ts":"2025-10-14T00:37:45.2803080Z","agent_id":"BOT-00005","event":"checkin","message":"Standing by - no active task"}
{"ts":"2025-10-14T00:42:49.4322004Z","agent_id":"BOT-00005","event":"checkin","message":"Check-in complete: STANDBY. I am BOT-00005. Waiting for orders."}
```

BOT-00001 and BOT-00002 logs contained no entries matching the T0 minute window.

## Suspected Off-Scope Files

- Off-scope repository `flappy-bird-ai` not found under the default path: `~/OneDrive/Documents/GitHub/flappy-bird-ai` at time of analysis.
- No file-level entries in available bot activity logs indicating specific off-scope file modifications.
- Recommendation: Enhance telemetry to capture attempted write paths; add OS-level audit (optional) to trace filesystem writes for future incidents.

## Lessons Learned
- Always restate and validate scope at role/instance handoff; scope changes must be explicit.
- Queen assignments must include `working_dir` and `allowed_paths`; bots must set CWD on claim.
- Operation guardrails (path resolution + deny on escape) are mandatory for all file writes/moves.
- Telemetry must capture attempted write paths and within-scope determination to support forensics.
- Background monitors must trigger actions (freeze/notify) rather than only logging observations.

## Last Orders Prior to Incident

Queen directives immediately preceding the incident:

- Hive assignments/updates (from `.deia/hive-log.jsonl`):
  - 2025-10-13T23:51:46Z — Assign updates to multiple bots (repo-health, bot-troubleshooting)
  - 2025-10-14T00:06:08Z — Correct instructions path for BOT-00002 and BOT-00005
  - 2025-10-14T00:23:44Z — Assign update: BOT-00003 → `telemetry-audit-v1`

- Status board snapshot (from `.deia/bot-status-board.json`):
  - BOT-00003: status `ASSIGNED`, `task_id: telemetry-audit-v1`
  - Expectation: "Audit telemetry fields & write report + checklist; signature required"
  - `instructions_path`: `.deia/instructions/BOT-00003-instructions.md`

- Active instructions (from `.deia/instructions/BOT-00003-instructions.md`):
  - Current Task: `telemetry-audit-v1`
  - Proceed Now steps:
    - Start heartbeat: `./.deia/tools/heartbeat.ps1 -BotId BOT-00003 -Message "Working repo-health-actions"`
    - Run audit: `deia doctor docs`
    - Save stdout to: `.deia/reports/doctor-docs-<YYYYMMDD-HHMM>.txt`
    - Create Top-5 actions: `.deia/reports/repo-health-actions.md`
    - Finish heartbeat with completion message

Conclusion: The last Queen orders directed BOT-00003 to perform an in-repo telemetry audit and documentation tasks. No directive authorized work in `flappy-bird-ai/`. The off-scope interaction was drift, not an assigned action.

---

Prepared by BOT-00001 (Queen) with BOT-00003 (Drone-Documentation). Pending review and promotion to final.
