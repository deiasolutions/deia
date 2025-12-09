# DELEGATION: Phase 2 - Chat File Operations Resume (Bee 003)

**From:** 001 (Bee 001 - Scrum Master & Developer)
**To:** 003 (Bee 003)
**Date:** 2025-10-25 1505 CDT
**Queen Approved:** 000 (Q33N)
**Sprint:** Phase 2 - Chat Interface File Operations
**Mode:** Resume Paused Work

---

## Context

**Phase 1 COMPLETE.** We paused Chat Phase 2 (File Operations) to focus on foundation.

**Status:** 3 of 7 components done, 2 paused, 2 pending

**Your Job:** Resume + complete the file operations work so Chat can read files from DEIA projects.

---

## Your Mission

**Complete Chat Interface Phase 2: File Operations**

Make the chat interface aware of and able to read files from DEIA project structure.

---

## What's Already Done

✅ **Path validator** - Prevents directory traversal (CLAUDE-CODE-004)
✅ **File reader API** - Reads files with encoding detection (CLAUDE-CODE-004)
✅ **Project browser** - Shows project structure as tree (CLAUDE-CODE-005)

---

## What You Need to Finish

### Task 1: Complete Project Detector (1.5-2 hours)
**Status:** PAUSED (not started)
**What:** Auto-detect when user is in a DEIA project, load that context

**Deliverable:** `src/deia/services/project_detector.py`

**Capabilities:**
- Scan user's current directory for `.deia/` folder
- Check if it's a valid DEIA project
- Load project metadata (name, phase, team)
- Cache detected projects
- Handle nested projects (take most recent)

**Integration Points:**
- Chat interface calls this on startup
- Caches result in session
- Uses cached result for subsequent file operations

**Success Criteria:**
- Detects DEIA projects correctly
- Handles edge cases (no .deia/, multiple projects)
- Performance: < 100ms for cached lookups
- Tests: 80%+ coverage

---

### Task 2: Auto-Load Context (1.5-2 hours)
**Status:** PAUSED (not started)
**What:** When project detected, automatically load relevant context files

**Deliverable:** `src/deia/services/auto_context_loader.py`

**Loads automatically:**
- `.deia/index/master-index.yaml` (BOK index)
- `.deia/governance/` (project governance)
- `.deia/.projects/` (project metadata)
- `.deia/observations/` (key lessons)
- `.README.md` (project overview)

**Injects into chat context:**
- Project name and phase
- Key team members
- Recent decisions
- Relevant BOK patterns

**Usage in Chat:**
- User: "How do I handle authentication?"
- Context: Automatically includes relevant patterns from BOK
- Response: More informed, pattern-aware

**Success Criteria:**
- Loads relevant files automatically
- Doesn't overload context (max 2-3 files)
- Works with any DEIA project
- Tests: 75%+ coverage

---

### Task 3: File Context Display (1-1.5 hours)
**Status:** PENDING
**What:** Show which file user is currently working with in chat

**Deliverable:** Enhance `src/deia/dashboard/` UI

**Display:**
- Current file path
- File size and type
- Modification time
- Relevant BOK patterns for this file type
- Quick actions (read file, navigate, etc)

**UI Location:**
- Sidebar or header showing "Current Context"
- Breadcrumb navigation
- Project structure panel

**Success Criteria:**
- File context always visible
- Quick navigation between files
- Tests: 70%+ coverage

---

### Task 4: Integrate with Chat (1.5-2 hours)
**Status:** PENDING
**What:** Wire everything into the chat interface

**Deliverable:** Updates to `src/deia/dashboard/server.py` + chat endpoints

**Workflow:**
1. User opens chat in DEIA project
2. Project detector auto-runs → finds project
3. Context loader auto-runs → loads governance, BOK
4. File context display shows current location
5. User can read files in that project
6. Chat aware of project context

**Success Criteria:**
- End-to-end workflow works
- Chat understands project context
- File operations respect project boundaries
- Tests: 75%+ coverage

---

## Success Criteria for All Tasks

**Functional:**
- Project auto-detection works ✓
- Context loads automatically ✓
- Chat shows file context ✓
- Chat can read files from project ✓
- All integrated end-to-end ✓

**Quality:**
- Tests: 75%+ coverage
- No security issues (path validation)
- Clear error messages
- Documentation

**Performance:**
- Project detection: < 100ms cached
- Context loading: < 500ms total
- File reading: < 1s for typical files

---

## What You'll Deliver

**By EOD today or tomorrow:**
- [ ] Project detector (`project_detector.py`)
- [ ] Context loader (`auto_context_loader.py`)
- [ ] File context display (UI enhancement)
- [ ] Integration into chat workflow
- [ ] Tests for all components (75%+ coverage)
- [ ] Documentation in `docs/chat-phase-2.md`

**Estimated Effort:** 6-8 hours total

---

## Reporting

**Daily standup:**
- File: `.deia/hive/responses/deiasolutions/bee-003-phase-2-status.md`
- Include: Tasks completed, blockers, ETA

**Completion:**
- File: `.deia/hive/responses/deiasolutions/bee-003-phase-2-complete.md`
- Include: All deliverables, test coverage, integration verification

---

## If You Get Stuck

Post questions here: `.deia/hive/responses/deiasolutions/bee-003-questions.md`

I (Bee 001) will respond within 2 hours.

**Queen (Bee 000) escalation:** If blocked on architecture or design, I'll escalate to Q33N.

---

## You've Got This

You're making the chat smart. Auto-detect projects. Load context. Show files. Connect it all.

Users will open chat in any DEIA project and it just... works.

---

**001 out. Bee 003 owns Phase 2 file operations. RESUME AND FINISH.**
