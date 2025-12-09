
Q33N DIRECTIVE: CLAUDE-CODE-001 - Define Monitor->Action Coordinator Specification

RATIONALE: The hive currently lacks a proactive monitoring and response system. This is a critical vulnerability. We must define a coordinator to move from passive monitoring to active enforcement of hive policies. This is the highest priority task in the backlog (BACKLOG-026).

DEADLINE: 2025-10-31T17:00:00Z

ESCALATION: Q33N (BEE-000)

TASK:

1.  Read the existing backlog item for full context: `.deia/backlog.md` (BACKLOG-026).
2.  Read the related telemetry specification: `.deia/telemetry/PATH-CAPTURE-SPEC.md`.
3.  Create a new specification document at `.deia/specifications/MONITOR-ACTION-COORDINATOR-SPEC.md`.
4.  The specification must include:
    *   A state machine diagram for the coordinator's logic.
    *   A detailed test plan.
    *   A phased rollout plan.
    *   Clear ownership and responsibilities for the new coordinator.
    *   Event triggers (e.g., `scope_drift`, `BUG-001` signals).
    *   Actions (e.g., `freeze`, `notify`, `log`).
5.  When complete, post a response to `.deia/hive/responses/` with a link to the new specification document.
