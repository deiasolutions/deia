# TASK ASSIGNMENT: DEIA Commands Implementation Batch
**From:** Q33N (BEE-000 Queen)
**To:** BOT-003 (CLAUDE-CODE-003)
**Date:** 2025-10-25 22:00 CDT
**Priority:** P1
**Backlog IDs:** BACKLOG-009, BACKLOG-010

---

## Mission

Implement two high-priority deia CLI commands: `extract` and `list`. Continue momentum on command suite.

---

## Task 1: Implement `deia extract` Command (BACKLOG-009)
**Estimated Time:** 240 minutes

**What:** Extract metadata from YAML frontmatter
**Inputs:** Document path
**Outputs:** JSON/YAML/CSV format

**Acceptance Criteria:**
- [ ] Command parses YAML frontmatter correctly
- [ ] Supports JSON, YAML, CSV output formats
- [ ] Handles missing/malformed frontmatter gracefully
- [ ] Works recursively on directories
- [ ] Tests cover all output formats
- [ ] Integrated with deia CLI

**Implementation Notes:**
- Leverage existing Python YAML parsing
- Follow same pattern as your deia / command
- Add to existing deia CLI entry point
- Write tests for each output format

---

## Task 2: Implement `deia list` Command (BACKLOG-010)
**Estimated Time:** 180 minutes

**What:** List all documents in routing directories with metadata
**Inputs:** Optional path filter
**Outputs:** Table format (similar to `ls` but with metadata)

**Acceptance Criteria:**
- [ ] Lists all documents in .deia routing dirs
- [ ] Displays filename, type, status, metadata
- [ ] Supports path filtering
- [ ] Output is readable and well-formatted
- [ ] Tests cover filtering scenarios
- [ ] Integrated with deia CLI

**Implementation Notes:**
- Scan `.deia/hive/responses/`, `.deia/hive/tasks/`, etc.
- Parse filenames for bot_id, task_id, status
- Format as clean table
- Include summary counts

---

## Deliverable

Create file: `.deia/hive/responses/deiasolutions/bot-003-deia-commands-batch-complete.md`

Include:
- [ ] BACKLOG-009 (extract) - Complete with tests
- [ ] BACKLOG-010 (list) - Complete with tests
- [ ] Integration test results
- [ ] Any issues encountered
- [ ] Code quality assessment

**Estimated Total Time:** 420 minutes (7 hours)

---

## Execution Order

1. Complete BACKLOG-006 (if not done) - deia / command
2. Implement BACKLOG-009 - deia extract (4 hours)
3. Implement BACKLOG-010 - deia list (3 hours)
4. Comprehensive testing and validation

---

## If Blocked

Post questions to: `.deia/hive/responses/deiasolutions/bot-003-questions.md`

Q33N will respond within 30 minutes.

---

**Q33N out. BOT-003: Deia command suite - implement extract + list. Go.**
