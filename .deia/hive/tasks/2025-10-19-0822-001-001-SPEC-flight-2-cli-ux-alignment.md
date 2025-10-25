# SPEC: Flight‑2 — CLI/UX Alignment to Season/Flight

Summary
Align user‑visible CLI/help/status strings with Season/Flight vocabulary. No behavioral changes. Prepare precise patches gated behind acceptance of Flight‑1 outcomes.

Scope (Allowlist)
- In‑scope: `src/deia/cli.py`, `src/deia/cli_hive.py`, `src/deia/services/*` where messages are user‑visible
- Out‑of‑scope: functional code paths, docs outside `.deia/` (tracked separately)

Discovery (occurrences)
- Found sprint/day/daily/weekly in code: 3 hits
  - `src/deia/services/messaging.py:9` — narrative string ("Sprint: Week 1 - Foundation")
  - `src/deia/services/messaging.py:109` — variable name `day` in filename parsing (date component; keep)
  - `src/deia/services/messaging.py:114` — date parsing using `day` (keep)

Planned Changes
- Replace narrative/label strings only; preserve date component variables.
- Review CLI help text for terms implying daily/sprint cadence; update to Season/Flight phrasing.

Acceptance Criteria
- `deia --help`, `deia hive --help` show Season/Flight terminology consistently.
- No change to parsing logic or behavior; only user‑visible strings updated.
- Changes limited to targeted files; unit behavior unaffected.

Deliverables
- Patch PR (or apply) touching: `src/deia/cli.py`, `src/deia/cli_hive.py`, `src/deia/services/messaging.py` (labels only)
- Brief diff summary listing lines changed.

Dependencies
- Blocked on Flight‑1 handoff acceptance (to keep vocabulary consistent with docs).

Risks
- Accidental change to parsing logic — mitigated by restricting edits to string literals/help text.

Next Steps
- After Flight‑1 acceptance, execute patch and run quick smoke: `deia --help`, `deia hive --help`.

---
Agent ID: CLAUDE-CODE-001
LLH: DEIA Project Hive
Purpose: Strategic planning, orchestration, and agent coordination
