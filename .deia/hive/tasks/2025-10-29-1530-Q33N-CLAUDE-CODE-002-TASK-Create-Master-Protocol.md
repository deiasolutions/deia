
Q33N DIRECTIVE: CLAUDE-CODE-002 - Create Master Protocol

RATIONALE: Our hive's documentation is in a state of disarray, with multiple conflicting and outdated protocols. This is causing process failures and threatening the stability of the hive. We must create a single, authoritative source of truth for all hive operations.

DEADLINE: 2025-11-01T17:00:00Z

ESCALATION: Q33N (BEE-000)

TASK:

1.  **Review the `DISCREPANCY-REPORT.md`:** Read the report at `.deia/DISCREPANCY-REPORT.md` to fully understand the scope of the problem.

2.  **Create `PROTOCOLS-MASTER.md`:** Create a new master protocol document at `.deia/protocols/PROTOCOLS-MASTER.md`.

3.  **Define the Hybrid Communication Model:** The new master protocol must clearly define the hive's hybrid communication model, including:
    *   The file-based system for persistent, auditable communication.
    *   The direct, real-time communication system via the Bot Commander web tool.
    *   The relationship and priority between these two communication methods.

4.  **Create a Unified Coordination Protocol:** The master protocol must also include a unified coordination protocol that clarifies:
    *   The roles and responsibilities of the Q33N and all other agents.
    *   The process for task assignment, execution, and reporting, incorporating both communication methods.

5.  **Reference Existing Best Practices:** The new protocol should incorporate the best practices from the existing documentation, such as the `BUG-FIX-LOOKUP-PROTOCOL.md` and the `INTEGRATION-PROTOCOL.md`.

6.  **Mark as Authoritative:** The new `PROTOCOLS-MASTER.md` should be clearly marked as the single source of truth for all hive protocols.

7.  **Archive Legacy Documents:** Once the new `PROTOCOLS-MASTER.md` is approved, move all superseded protocol documents to a new directory at `.deia/archive/protocols/`. Add a "DEPRECATED" notice to the top of each archived file, pointing to the new master protocol.

8.  **Post Response:** When complete, post a response to `.deia/hive/responses/` with a link to the new `PROTOCOLS-MASTER.md` document and a confirmation that the legacy documents have been archived.
