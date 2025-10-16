# Hive Backlog

- Use this as a shared queue if needed.

## Human Review Queue

- [P0] HUMAN_REVIEW: Postmortem — Escaped Bot to Non-Scoped Repo
  - Review: `.deia/review-requests/INCIDENT-P0-ESCAPED-BOT-POSTMORTEM.md`
  - Draft: `.deia/incidents/P0-ESCAPED-BOT-POSTMORTEM.md`
  - Decision: Approve / Approve with edits / Request changes / Reject
  - Owner: Dave
  - Requested by: BOT-00001

## Queued — Monitor→Action

- [P0] Monitor→Action Coordinator Spec (BACKLOG-026)
  - Define event→action coordinator replacing output-only monitoring
  - Triggers: scope_drift, BUG-001 signals; Actions: freeze/notify/log
  - Acceptance: state machine, test plan, rollout, ownership
  - Owner: BOT-00001; Related: `.deia/telemetry/PATH-CAPTURE-SPEC.md`

- [P1] Coordinator MVP Implementation (BACKLOG-027)
  - Listen to `.deia/telemetry/path-events.jsonl`; enforce freeze/notify
  - Acceptance: listens, freezes on drift, manual test, nightly zero-drift
  - Owner: BOT-00006; Depends on: BACKLOG-026
