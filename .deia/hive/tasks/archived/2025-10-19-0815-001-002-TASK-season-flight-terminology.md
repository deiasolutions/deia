# TASK: Flight‑1 Terminology Transition (Docs-first)

Summary
Update DEIA-facing docs to adopt Season/Flight vocabulary and document the work to be done. Do not touch the broader BOK yet. No behavior changes. Prepare a concise plan, proposed edits, and evidence for review.

Context
- We use Seasons (macro) and Flights (execution bursts) instead of sprints/days.
- Old file-drop tunnel is deprecated; coordination happens under `.deia/hive/*`.
- This task is documentation-first; code/CLI strings will be a follow-on flight after review.

Scope (Allowlist)
- In-scope dirs: `.deia/`, `.deia/coordination/`
- Read-only review of `src/deia/` for user-visible strings; propose, don’t patch.
- Out-of-scope: `bok/`, `docs/` outside `.deia/` (note occurrences but don’t edit).

Work Items
- Audit terms in `.deia/` and user-visible CLI help (read-only in `src/deia/`).
  Acceptance: Provide a table of occurrences and recommended replacements.
- Update core `.deia/` docs to Season/Flight language:
  - `.deia/README.md` (overview, heartbeat wording, Integration Protocol refs)
  - `.deia/AGENTS.md` (coordination channels, status/heartbeat language)
  - `.deia/DRONE-START.md` (replace “sprint/day/daily/weekly” where applicable)
  - `.deia/coordination/agent-telemetry.md` (rename “Current Sprint” section; keep history intact)
  Acceptance: No “sprint/day/daily/weekly” remain in `.deia/` except in quoted historical text.
- Propose minimal templates (decision required):
  - `.deia/templates/SEASON-CHARTER.md` (1 page)
  - `.deia/templates/FLIGHT-PLAN.md` (1 page)
  Acceptance: Submit drafts in handoff; 001 will approve before adding files.
- Log change in `.deia/ACCOMPLISHMENTS.md` (as a proposed entry; 001 to append on integrate).

Deliverables
- Handoff doc: `.deia/handoffs/FLIGHT-1-terminology-transition.md`
  - Summary of edits
  - Before/After excerpts (10–20 examples)
  - List of files touched with line anchors
  - Outstanding decisions and risks
- Patch preview: Unified diff blocks in the handoff doc (do not apply changes yourself).
- Response message: SYNC back to 001 with completion link to the handoff.

Acceptance Criteria
- Clear, PR-ready documentation of changes; zero broken paths.
- Occurrence audit attached; replacements maintain meaning and intent.
- No edits outside allowed scope; no CLI or code behavior changes.
- Identity footer present in your SYNC.

Guidance
- Keep historical quotes intact; add a brief glossary to `.deia/README.md` (old → new terms).
- Use Season/Flight vocabulary consistently across headings and prose.
- If a phrasing is ambiguous, propose options in the handoff rather than editing.

How To Respond
- When complete, drop: `.deia/hive/responses/YYYY-MM-DD-HHMM-002-001-SYNC-flight-1-terminology-complete.md` linking to the handoff.
- If blocked, drop a `QUERY` with exact path and question.

References
- Protocols: `.deia/hive/ORDERS-PROTOCOL.md`, `.deia/README.md`, `.deia/AGENTS.md`
- Coordination state: `.deia/coordination/*`

---
Agent ID: CLAUDE-CODE-001
LLH: DEIA Project Hive
Purpose: Strategic planning, orchestration, and agent coordination
