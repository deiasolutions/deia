# FLIGHT-1 Terminology Transition (Docs-first) — Handoff

Summary
- Adopt Season/Flight vocabulary across DEIA-facing docs under `.deia/`.
- Do not modify historical quotes or logs; propose edits via unified diff previews.
- No code/CLI behavior changes; src review is read-only.

Scope
- In-scope: `.deia/`, `.deia/coordination/` docs.
- Read-only review: `src/deia/` for user-visible strings.
- Out-of-scope (note only): `bok/`, general `docs/` outside `.deia/`.

Occurrence Audit (sample)
- .deia/AGENTS.md: line 259 — "tasks & sprints" → "tasks & flights" (propose)
- .deia/coordination/agent-telemetry.md: line 11 — "Current Sprint" → "Current Flight" (propose)
- .deia/coordination/agent-telemetry.md: line 14 — "Sprint Priorities" → "Flight Priorities" (propose)
- .deia/coordination/agent-telemetry.md: line 58 — "Sprint coordination" → "Flight coordination" (propose)
- .deia/coordination/agent-telemetry.md: section — "Sprint Velocity Metrics" → "Flight Velocity Metrics" (propose)
- .deia/PHASE-2-STRATEGIC-PRIORITIES.md: multiple — sprint references (propose update to season/flight)
- .deia/ACCOMPLISHMENTS.md: "16 Hour Sprint" (historical — leave)
- .deia/CHANGELOG.md: "weekly limit" (external context — leave)

Before/After Excerpts
1) .deia/AGENTS.md
   - Before: Task Tracking: `BACKLOG.md` (tasks & sprints)
   - After:  Task Tracking: `BACKLOG.md` (tasks & flights)

2) .deia/coordination/agent-telemetry.md
   - Before: ## Current Sprint: Phase 2 - Documentation & Integration
   - After:  ## Current Flight: Phase 2 - Documentation & Integration

3) .deia/coordination/agent-telemetry.md
   - Before: **Sprint Priorities:**
   - After:  **Flight Priorities:**

4) .deia/coordination/agent-telemetry.md
   - Before: **Role:** Sprint coordination, agent management, task routing
   - After:  **Role:** Flight coordination, agent management, task routing

5) .deia/coordination/agent-telemetry.md
   - Before: ## Sprint Velocity Metrics
   - After:  ## Flight Velocity Metrics

6) .deia/coordination/PHASE-2-STRATEGIC-PRIORITIES.md
   - Before: "Phase 2 mid-sprint assessment"
   - After:  "Phase 2 mid-flight assessment"

7) .deia/coordination/PHASE-2-STRATEGIC-PRIORITIES.md
   - Before: "Next Review: 2025-10-25 (mid-sprint)"
   - After:  "Next Review: 2025-10-25 (mid-flight)"

8) .deia/README.md (add glossary)
   - Before: (no glossary)
   - After:  Add "Glossary: Seasons & Flights" with mappings.

9) .deia/coordination/agent-telemetry.md
   - Before: "sent daily status report"
   - After:  "sent flight status update" (option A) or "sent end-of-session report" (option B)

10) .deia/AGENTS.md
   - Before: "tasks & sprints, ROADMAP.md (phases & milestones)"
   - After:  "tasks & flights, ROADMAP.md (seasons & milestones)"

Proposed Unified Diffs (previews only)

---
--- a/.deia/AGENTS.md
+++ b/.deia/AGENTS.md
@@
- **Task Tracking:** `BACKLOG.md` (tasks & sprints), `ROADMAP.md` (phases & milestones)
+ **Task Tracking:** `BACKLOG.md` (tasks & flights), `ROADMAP.md` (seasons & milestones)

---
--- a/.deia/coordination/agent-telemetry.md
+++ b/.deia/coordination/agent-telemetry.md
@@
-## Current Sprint: Phase 2 - Documentation & Integration
+## Current Flight: Phase 2 - Documentation & Integration
@@
-**Sprint Priorities:**
+**Flight Priorities:**
@@
-**Role:** Sprint coordination, agent management, task routing
+**Role:** Flight coordination, agent management, task routing
@@
-## Sprint Velocity Metrics
+## Flight Velocity Metrics
@@
-**1700 CDT:** AGENT-003 sent daily status report
+**1700 CDT:** AGENT-003 sent flight status update

---
--- a/.deia/coordination/PHASE-2-STRATEGIC-PRIORITIES.md
+++ b/.deia/coordination/PHASE-2-STRATEGIC-PRIORITIES.md
@@
- Phase 2 mid-sprint assessment
+ Phase 2 mid-flight assessment
@@
-**Next Review:** 2025-10-25 (mid-sprint)
+**Next Review:** 2025-10-25 (mid-flight)

---
--- a/.deia/README.md
+++ b/.deia/README.md
@@
 ## Workflow
@@
 4) Queen reviews handoff and assigns next task
+
+## Glossary: Seasons & Flights
+
+- Season: Planning period (macro cadence). Set goals and milestones.
+- Flight: Execution burst within a Season. Deliver concrete outcomes.
+- Replacements:
+  - Sprint → Flight
+  - Weekly cadence/summary → Season summary (or Flight rollup, context-dependent)
+  - Daily status report → Flight status update (or end-of-session report)
+
+Notes
+- Do not alter historical quotes or logs; use Season/Flight for new and current docs.

List of Files Touched (proposed)
- .deia/AGENTS.md: tasks & sprints → tasks & flights
- .deia/coordination/agent-telemetry.md: Sprint→Flight; daily→flight update
- .deia/coordination/PHASE-2-STRATEGIC-PRIORITIES.md: mid-sprint→mid-flight; next review note
- .deia/README.md: add Seasons & Flights glossary

Outstanding Decisions
- Decision RESOLVED: Use "flight status update" (Option A) consistently in current docs.
- Whether to update backlog.json sprint fields in a follow-on flight (data vs docs)

Risks
- Over-replacing legitimate historical contexts; mitigation: exempt quotes/logs.
- Ambiguity around "daily" phrasing; propose explicit guidance above.

Acceptance Checklist Mapping
- Occurrence audit included (sample + references)
- Proposed unified diffs provided (no direct changes applied)
- Handoff location present with link and file list

Generated by BOT-00002
