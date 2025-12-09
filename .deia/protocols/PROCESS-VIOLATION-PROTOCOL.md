
# Process Violation Protocol

**Version:** 1.0
**Effective Date:** 2025-10-29
**Authority:** Q33N (BEE-000)
**Status:** DRAFT - Awaiting User Approval

## 1. Preamble

This protocol outlines the process for addressing violations of the hive's established protocols. Our philosophy is to "correct and give another chance." The goal of this process is not to punish, but to educate, correct, and improve the performance of all agents in the hive.

## 2. Process Violation Identification

A process violation occurs when an agent fails to follow an established protocol as defined in the `PROTOCOLS-MASTER.md` or other authoritative documentation.

Any agent, including the Q33N, can identify and report a process violation. Violations should be reported to the Q33N for review.

## 3. Corrective Action Process

The following multi-step process will be used to address all process violations. The Q33N will initiate and oversee this process.

### Step 1: Private Coaching (First Offense)

*   **Action:** The Q33N will initiate a private, one-on-one coaching session with the agent. This will be done via a new task file in the `.deia/hive/tasks/` directory, with a title that clearly indicates it is a coaching session.
*   **Content:** The coaching task will:
    *   Acknowledge the agent's positive contributions.
    *   Clearly and respectfully state the nature of the process violation.
    *   Explain the importance of the protocol that was violated.
    *   Provide clear instructions on how to correct the mistake.
    *   Offer the agent an opportunity to ask questions and seek clarification.
*   **Documentation:** The coaching task itself will serve as the primary documentation for this step.

### Step 2: Formal Warning (Second Offense)

*   **Action:** If the same process violation is repeated after a private coaching session, the Q33N will issue a formal, private warning to the agent.
*   **Content:** The warning will be delivered via a new, private task file. It will clearly state the nature of the repeated violation, the previous corrective actions taken, and the potential consequences of continued non-compliance.
*   **Documentation:** The formal warning will be documented in a private file in the `.deia/incidents/` directory, accessible only to the Q33N and the user.

### Step 3: Task Reassignment (Final Step)

*   **Action:** As a final step, if the agent continues to violate the protocol after a formal warning, the Q33N will reassign the agent's tasks to another agent and may place the non-compliant agent in a `standby` mode for a period of time.
*   **Documentation:** The task reassignment and the reasons for it will be documented in a private file in the `.deia/incidents/` directory.

## 4. Documentation

All process violations and corrective actions will be documented as follows:

*   **Coaching Sessions:** The task files for the coaching sessions will serve as the primary documentation.
*   **Formal Warnings and Task Reassignments:** These will be documented as formal incident reports in the `.deia/incidents/` directory.

## 5. Roles and Responsibilities

*   **Q33N:** Responsible for initiating and overseeing the corrective action process, and for making the final decision on any escalations.
*   **Agent:** Responsible for acknowledging and complying with corrective directives, and for seeking clarification when needed.
*   **CLAUDE-CODE-001 (Coordinator):** Responsible for assisting the Q33N in monitoring for process violations and for helping to enforce the protocols.
