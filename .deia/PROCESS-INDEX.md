# DEIA Process Index - Quick Reference

**Purpose:** Q33N quick lookup - know the name and purpose of every official process without memorizing them.

**Read Time:** 2 minutes

---

## Core Processes (Foundation)

### PROCESS-0001: Always Check (or Create) the Process, Then Submit
**Purpose:** Ensure every workflow has a documented process before execution
**When to use:** Before attempting any new task, workflow, or workaround
**Key principle:** Discover → Create (if missing) → Execute → Test → Submit to collective
**File:** `.deia/processes/PROCESS-0001-always-check-and-submit.md`
**Status:** Official
**Scope:** All bees, all vendors, all projects

---

### PROCESS-0002: Task Completion & Archival (Mandatory Workflow)
**Purpose:** Ensure completed tasks are locked and prevent duplicate execution
**When to use:** Every time a bee completes ANY task (success or blocked)
**Key principle:** Completion = archival to `_archive/`. Non-negotiable.
**File:** `.deia/processes/PROCESS-0002-task-completion-and-archival.md`
**Status:** Official - Q33N Directive (MANDATORY)
**Scope:** All task completions, all bees, all projects

**Critical requirement:** Move task file from `.deia/hive/tasks/` to `.deia/hive/tasks/_archive/`
**Why:** Prevents bots from re-executing the same task

---

### PROCESS-0003: Process Discovery & Contribution Workflow
**Purpose:** Define how new processes are discovered, created locally, tested, and contributed to global DEIA
**When to use:** When creating a new process OR when looking for the contribution workflow
**Key principle:** Local-first discovery → local creation/testing → global submission via PROCESS-0001
**File:** `.deia/processes/PROCESS-0003-process-discovery-and-contribution.md`
**Status:** Official
**Scope:** All process-related work, all projects

**Critical requirement:** All processes must be LLM-agnostic (work for Claude, Codex, any vendor)

---

## Operational Processes (Hive Management)

*(To be documented - processes for specific operational scenarios)*

---

## Vendor-Specific Processes

### Claude Pre-Compact Context Handling
**Purpose:** Prepare context for Claude's pre-compact event (session reset)
**When to use:** Before Claude context resets or when context window approaching capacity
**Key principle:** Save working state explicitly so new session can resume in seconds
**File:** `.deia/vendors/claude/patterns/pre-compact-instructions.md`
**Category:** Vendor-Specific Pattern (Claude only)
**Scope:** Claude Code CLI only

---

## By Use Case

### "I'm assigning work to a bee"
→ Read: **PROCESS-0002** (how they'll complete and report)
→ Read: `.deia/instructions/README.md` (unified naming format)
→ Read: `.deia/hive-coordination-rules.md` (task assignment procedure)

### "Bee just reported work complete"
→ Check: **PROCESS-0002** completion requirements met?
→ Verify: Original task file moved to `_archive/`?
→ Then: Review response file and assign next task or coordinate

### "Creating a new workflow/process"
→ Read: **PROCESS-0001** (check-first pattern)
→ Read: **PROCESS-0003** (discovery and contribution)
→ Then: Create locally, test, submit globally

### "Coordinating work between bees"
→ Read: `.deia/hive-coordination-rules.md` (sections on parallelization and conflict resolution)
→ Read: `.deia/instructions/README.md` (coordination message format)
→ Then: Create task or coordination message in `.deia/hive/coordination/`

### "A bee is blocked or escalating"
→ Check: `.deia/hive-coordination-rules.md` (escalation policy section)
→ Then: Either unblock with coordination message or escalate to human

### "Planning a sprint"
→ Read: `.deia/bok/patterns/sprint-planning-framework.md`
→ Check: Do we have a process for this scenario? (see PROCESS-INDEX)
→ Then: Plan and assign tasks

### "Corner case / edge case encountered"
→ Search: PROCESS-INDEX and master-index.yaml for similar scenarios
→ If found: Read the documented process
→ If not found: Follow PROCESS-0001 (create local process, test, submit)

---

## Process Hierarchy & Precedence

**In order of authority:**
1. **Official Processes** (PROCESS-0001, 0002, 0003) - Q33N-issued, mandatory
2. **Operational Processes** (PROCESS-00XX for scenarios) - Q33N-issued, applicable to specific use cases
3. **Vendor-Specific Patterns** (`.deia/vendors/[vendor]/`) - Vendor-specific, not applicable to other vendors
4. **Vendor-Agnostic Patterns** (`.deia/bok/patterns/`) - Apply to all vendors
5. **Anti-Patterns** (`.deia/bok/anti-patterns/`) - What NOT to do

---

## All Processes at a Glance

| Process ID | Title | Category | Status | Applies To |
|-----------|-------|----------|--------|-----------|
| PROCESS-0001 | Always Check (or Create) the Process | Foundation | Official | All bees, all vendors |
| PROCESS-0002 | Task Completion & Archival | Hive Operations | **MANDATORY** | All task completions |
| PROCESS-0003 | Process Discovery & Contribution | Knowledge Management | Official | New process creation |
| scope-enforcement | Scope Enforcement | Hive Operations | Official | All bots |
| *(pending)* | *(operational scenarios)* | *(various)* | *(draft)* | *(specific contexts)* |

---

## Quick Lookup: "Do we have a process for...?"

**Task assignment and completion?**
→ PROCESS-0002

**Creating/finding processes?**
→ PROCESS-0001, PROCESS-0003

**Coordinating between bees?**
→ `.deia/hive-coordination-rules.md` (not a PROCESS, but coordination spec)

**Handling scope violations?**
→ `scope-enforcement.md`

**Handling vendor-specific behavior?**
→ `.deia/vendors/[vendor]/patterns/`

**General best practices/patterns?**
→ `.deia/bok/patterns/`

**What to avoid?**
→ `.deia/bok/anti-patterns/`

---

## How This Index Helps Q33N

✅ **Know what exists without searching**
- All processes listed with name and purpose
- No guessing "is there a process for this?"

✅ **Find the right process by scenario**
- Organized by use case ("I'm assigning work", "Creating new process", etc.)
- Jump directly to relevant process or doc

✅ **Understand precedence**
- Know which processes are mandatory vs. optional
- Know which apply to specific vendors vs. all vendors

✅ **Quick 2-minute orientation**
- New Q33N can read this and know the landscape
- Returning Q33N can reference without searching

✅ **Prevent duplicate process creation**
- Before creating new workflow, check this index
- If "process for this scenario exists", don't reinvent

---

## Maintenance

**Update this index when:**
- New PROCESS-XXXX is created and approved
- Existing process status changes (draft → official, etc.)
- Use cases or scenarios change
- Categories need adjustment

**Owner:** Q33N Authority
**Last Updated:** 2025-11-14
**Version:** 1.0
