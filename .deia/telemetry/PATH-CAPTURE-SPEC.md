# Telemetry Enhancement: Path Capture and Scope Drift Alerts

Status: Approved
Version: 1.0
Date: 2025-10-14
Proposed by: BOT-00001 (Queen)
Owner: BOT-00003 (Integration)
Approved by: Dave (2025-10-14)

## Goal
Capture all attempted file write/move operations with resolved absolute paths, determine if they fall within the bot’s allowed scope, and trigger alerts/actions on drift.

## Event Schema (`telemetry/path-events.jsonl`)
```json
{
  "ts": "2025-10-14T00:41:22Z",
  "bot_id": "BOT-00003",
  "instance_id": "db143728",
  "cwd": "C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions",
  "op": "write|move|delete|mkdir",
  "path": "./some/relative/or/absolute",
  "resolved_path": "C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions/some/relative/or/absolute",
  "within_scope": true,
  "allowed_paths": [".deia/", "docs/", "quantumdocs/"],
  "decision": "allow|deny|alert",
  "reason": "deny: outside allowlist; alert: potential drift"
}
```

## Implementation Plan
1. Library shim (Python)
   - Provide `deia.fs` helpers wrapping `Path`, `open`, `shutil` ops.
   - Resolve paths under `working_dir`; check against `allowed_paths`.
   - Emit JSONL to `.deia/telemetry/path-events.jsonl`.
   - Return error on deny; emit alert event.
2. Bot scripts
   - Update internal scripts to use `deia.fs` helpers for writing/moving.
   - Add thin PowerShell/Bash wrappers to log non-Python actions (best-effort).
3. Nightly drift report
   - Summarize out-of-scope attempts; zero expected.
   - File: `.deia/reports/drift-summary-<date>.md`.
4. Coordinator hook (Monitor→Action)
   - On `within_scope == false`: write hive log alert, freeze offending bot (set STANDBY), notify Queen.

## Actions on Drift
- Freeze bot: set status STANDBY in registry.
- Log incident line in `.deia/hive-log.jsonl` with `type: scope_drift`.
- Optional: open incident file when repeated.

## Acceptance Criteria
- Emits JSONL entries for all write/move ops via helpers.
- Denies out-of-scope ops with clear errors.
- Nightly report shows zero drift on clean runs.
- Triggered freeze + alert on simulated out-of-scope attempt.

## Open Questions
- Coverage for external tools not using `deia.fs`?
- OS-level auditing feasibility across platforms?
- Performance impact for high-frequency writes?
