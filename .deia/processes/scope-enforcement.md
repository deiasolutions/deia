# Process Pattern: Scope Enforcement for Hive Bots

Status: Adopted (local policy)
Version: 1.0
Date: 2025-10-14
Owners: BOT-00001 (Queen), BOT-00003 (Documentation)

## Problem
Bots can drift outside the intended repository or directory scope, causing off-scope edits and process risk.

## Solution
Explicitly define and enforce scope for each bot: a `working_dir` plus an allowlist of subpaths. Validate on claim, enforce on file operations, detect drift in telemetry, and freeze on violations.

## Implementation
1. Define scope in assignments/instructions
   - working_dir: absolute repo root
   - allowed_paths: relative subdirectories (minimal set)
2. Claim-time validation
   - Bot sets CWD to working_dir; error if missing
   - Verify allowed_paths exist (create only if policy allows)
3. Operation guardrails
   - Resolve target paths → ensure within allowed_paths under working_dir
   - Deny and log on escape attempts (e.g., `..` traversal)
4. Handoffs restate scope
   - Include working_dir, allowed_paths, branch
   - Note any scope deltas vs prior handoff
5. Drift detection
   - Telemetry nightly summary flags any out-of-scope edits
   - Zero-drift target; alerts to Queen on violations
6. Emergency freeze
   - On drift: set affected bots to STANDBY, open/append incident, review

## Example (Instruction Snippet)
```json
{
  "bot_id": "BOT-00003",
  "role": "Drone-Documentation",
  "working_dir": "C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions",
  "allowed_paths": [".deia/", "quantumdocs/", "docs/"]
}
```

## Checklist
- [ ] working_dir is the correct repo root
- [ ] allowed_paths are minimal and exist
- [ ] Bot verified CWD and scope on claim
- [ ] Handoff restates scope and branch
- [ ] Telemetry report shows no drift
- [ ] Incident documented for any violation

## Notes
- Start strict; broaden allowed_paths only with justification.
- Pair with monitor→action coordinator to auto-freeze on violations.

## References
- .deia/hive-coordination-rules.md (Scope Enforcement)
- .deia/incidents/P0-ESCAPED-BOT.md
- .deia/incidents/P0-ESCAPED-BOT-POSTMORTEM.md

