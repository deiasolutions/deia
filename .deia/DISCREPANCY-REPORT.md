# Discrepancy Report: DEIA Hive Process Documentation

**Report Date:** 2025-10-29
**Prepared By:** Q33N (BEE-000)

## 1. Executive Summary

A comprehensive review of all process and protocol documentation has revealed a critical state of disarray. The documentation is a patchwork of conflicting, outdated, and incomplete information, leading to process confusion and the re-emergence of "zombie processes".

The root cause is the lack of a single, authoritative source of truth for hive operations. Multiple, overlapping, and contradictory protocols exist, and key documents are either empty or refer to deprecated systems.

This report details all identified discrepancies and proposes a path to rectify the situation.

## 2. Key Findings

### 2.1. Hybrid Communication Model

The hive operates on a hybrid communication model:

*   **File-Based (Persistent):** The original system of using files in `.deia/hive/tasks/` and `.deia/hive/responses/` for asynchronous, auditable communication.
*   **Direct (Real-Time):** A new, WIP "Bot Commander" web tool (`chat_interface_app.py`) that allows for direct, real-time communication with bots via HTTP and WebSockets.

**Discrepancy:** The documentation does not clearly describe this hybrid model. The relationship and priority between the two communication methods are undefined.


### 2.1. Conflicting Communication Protocols

There are at least three different communication protocols described in the documentation:

*   **Corpus Callosum:** Described in `AGENTS.md`, this protocol uses a `YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md` file naming convention for inter-agent messaging in the `.deia/tunnel/claude-to-claude/` directory.
*   **Queen-Drone Instruction Files:** Described in `hive-coordination-rules.md`, this protocol involves the Queen updating instruction files in `.deia/instructions/`.
*   **Pheromone-RSM Protocol:** Described in `docs/coordination/PHEROMONE-RSM-PROTOCOL-v0.1.md`, this is an embargoed proposal for a new communication system based on "pheromones" and "RSM envelopes".

**Discrepancy:** These protocols are mutually exclusive and create confusion about how bots should communicate.

### 2.2. Deprecated `tunnel` System

The `.deia/tunnel/` directory and its associated communication protocol are deprecated, but are still referenced in the following key documents:

*   `AGENTS.md`
*   `.deia/protocols/BEE-000-Q33N-BOOT-PROTOCOL.md`

**Discrepancy:** Core operational documents refer to a defunct system.

### 2.3. Outdated `hive-coordination-rules.md`

This document is severely outdated and contains numerous contradictions with other documents:

*   It describes the old Queen-Drone instruction file communication method.
*   It refers to a `bot_coordinator.py` script that is not mentioned elsewhere.
*   Its "Current Hive Status" section lists an incorrect set of active agents.

**Discrepancy:** A core protocol document is no longer a reliable source of truth.

### 2.4. Empty and Incomplete Protocol Documents

Several key protocol documents are either empty or exist only as "TODO" notes:

*   `docs/process/BC-LIAISON-WORK-PACKET-PROTOCOL.md` is empty.
*   `.deia/hive/coordination/TODO-TACTICAL-COORDINATION-PROTOCOL.md` is a placeholder for a critical protocol that was never written.

**Discrepancy:** Key processes are undefined, leaving a gap in the hive's operational procedures.

### 2.5. Multiple "Queen" Personas

The documentation refers to two different "Queen" personas:

*   **Q33N (BEE-000):** The meta-governance authority for the DEIA hive.
*   **Q88N:** The "Queen of All Queens" and "The Great I Am", introduced in `HIVE-NOTICE-PROCESS-CREATION-MODE.md`.

**Discrepancy:** The existence of multiple, seemingly overlapping high-level authorities creates confusion about the hive's governance structure.

## 3. Detailed List of Discrepancies

| File | Discrepancy |
| --- | --- |
| `.deia/AGENTS.md` | References the deprecated `.deia/tunnel/` communication system. |
| `.deia/hive-coordination-rules.md` | Describes an outdated communication protocol and contains an incorrect list of active agents. |
| `.deia/hive/COMMUNICATION-PROTOCOL.md` | Conflicts with other communication protocols. |
| `.deia/tunnel/COMMUNICATION-PROTOCOL.md` | Located in a deprecated directory and conflicts with other protocols. |
| `.deia/protocols/BEE-000-Q33N-BOOT-PROTOCOL.md` | References the deprecated `.deia/tunnel/` communication system. |
| `docs/process/BC-LIAISON-WORK-PACKET-PROTOCOL.md` | Empty file. |
| `.deia/hive/coordination/TODO-TACTICAL-COORDINATION-PROTOCOL.md` | Placeholder for an unwritten protocol. |
| `HIVE-NOTICE-PROCESS-CREATION-MODE.md` | Introduces a conflicting "Q88N" persona. |
| `.deia/hive/ORDERS-PROTOCOL.md` | Describes yet another task assignment mechanism via `bot-status-board.json`, conflicting with other protocols. |

## 4. Proposed Resolution

To restore order and create a single source of truth, I propose the following plan:

1.  **Establish Authoritative Protocols:** Create a new, unified set of core protocol documents:
    *   `PROTOCOLS-MASTER.md`: A master document that will serve as the single source of truth for all hive protocols.
    *   `COMMUNICATION-PROTOCOL.md`: A new, unified communication protocol based on the most recent and effective method (likely the file-based system described in `BOT-ASSIGNMENT-PROTOCOL-v2.md`).
    *   `COORDINATION-PROTOCOL.md`: A new, unified coordination protocol that clarifies the roles of the Q33N and the other agents.

2.  **Update All Documentation:** Create a task to systematically review and update all other documents to reference the new, authoritative protocols. This will involve removing all references to the `tunnel` system, outdated communication methods, and the "Q88N" persona.

3.  **Complete Missing Protocols:** Create tasks to write the content for the empty and "TODO" protocol documents, including the `BC-LIAISON-WORK-PACKET-PROTOCOL.md` and the `TACTICAL-COORDINATION-PROTOCOL.md`.

4.  **Update `AGENTS.md`:** Create a task to update `AGENTS.md` to reflect the current agent roster and the new, unified communication protocol.

**Execution:**

I will now create a task to begin this process, starting with the creation of the `PROTOCOLS-MASTER.md` document. This will be a high-priority task assigned to the most appropriate agent (likely `CLAUDE-CODE-002`, the Documentation Systems Lead).
