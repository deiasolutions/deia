# PATTERN: Pre-Compact Instructions Preparation

**Vendor:** Claude (Claude Code CLI)
**Category:** Event / Context Management
**Status:** Active
**Last Updated:** 2025-11-14

---

## What Is This?

Claude Code CLI has a "pre-compact" event where the context window resets. Before this happens, Claude needs to save critical working state (current task, progress, next steps) in instructions files so that upon restart, Claude can resume immediately without ramp-up time.

---

## Why It Matters

- **Context loss is real:** When Claude Code resets (context window full, session timeout, etc.), all in-memory context is lost
- **Resume friction:** Without prepared instructions, the new session starts cold and needs to re-read all context
- **Efficiency:** Pre-compact instructions allow resume in seconds, not minutes
- **Continuity:** Explicit handoff prevents missed work or duplicate effort

---

## When You Encounter It

- Claude receives notification of pending pre-compact (system message)
- Context window is approaching capacity
- Session is about to reset or has reset unexpectedly
- New session needs to know what was being worked on

---

## How to Respond

### Step 1: Save Working State
Before compact happens:
```
Create/update: .deia/instructions/CLAUDE-CODE-NNN-pre-compact.md
```

**Must include:**
- Current task (filename and line number if in code)
- What was completed in this session
- What's in progress (exact step number)
- What comes next
- Any blockers or context needed for next session

### Step 2: Create Handoff Document
```
Location: .deia/handoffs/CLAUDE-CODE-NNN-pre-compact-YYYY-MM-DD-HHMM.md
Format: Date-timestamped for easy location
```

**Must include:**
- Session summary (what was accomplished)
- Current working directory / project state
- Git branch and any uncommitted changes
- Next immediate action (numbered step)
- Context that might be forgotten

### Step 3: Commit All Work
```bash
git add -A
git commit -m "chore: pre-compact session checkpoint

Current task: [task name]
Status: Step N of M complete
Next: [exactly what to do next]

CLAUDE-CODE-NNN ready for compact"
```

### Step 4: Acknowledge Pre-Compact in .deia/

Create or update status file:
```
.deia/hive/heartbeats/CLAUDE-CODE-NNN.yaml
```

Update with:
```yaml
status: "pre-compact-prepared"
last_update: "YYYY-MM-DD HH:MM"
session_guid: [unique session ID]
task_in_progress: "[task name]"
progress_pct: NN
next_action: "[exactly what to do]"
notes: "[any critical context]"
```

---

## Examples

### Example 1: Mid-Task Compact

**Scenario:** Claude was writing tests for Season 008, context window at 85%

**Pre-compact instructions created:**
```markdown
# Pre-Compact Handoff: Season 008 Tests

**Session:** CLAUDE-CODE-002-2025-11-14-1430
**Current Task:** 2025-11-14-1600-Q33N-CLAUDE-CODE-002-TASK-season-008-tests.md

## Completed This Session
1. ✅ Reviewed Season 008 spec (line 1-45)
2. ✅ Created test file: src/tests/season-008.test.js
3. ✅ Wrote tests 1-8 (basic functionality)

## In Progress
- **Step 3 of 5:** Writing remaining tests (9-15)
- **Location:** src/tests/season-008.test.js, line 150
- **Next line to add:** Test case 9 for feature X

## Blockers
None - on schedule

## Next Session
1. Continue with test case 9 at line 150
2. Complete all 15 test cases
3. Run tests and verify pass
4. Report completion to Q33N
5. Archive task to .deia/hive/tasks/_archive/

## Context Needed
- Season 008 spec is in docs/SEASON-008-SPEC.md
- Test framework: Jest (configured in package.json)
- Acceptance criteria: 80% code coverage, all tests pass
```

**Heartbeat updated:**
```yaml
status: "pre-compact-prepared"
task: "CLAUDE-CODE-002-TASK-season-008-tests"
progress_pct: 53  # 8 of 15 tests done
step: "3 of 5"
next: "Write test case 9 at src/tests/season-008.test.js:150"
blockers: "none"
git_status: "clean (all committed)"
last_commit: "feat: write season 008 tests 1-8"
```

### Example 2: Exploring New Process

**Scenario:** Claude was discovering how process contribution works, getting ready to document it

**Pre-compact instructions created:**
```markdown
# Pre-Compact Handoff: Process Documentation Discovery

**Session:** CLAUDE-CODE-003-2025-11-14-1530
**Task:** Self-directed - discovering DEIA process patterns

## Completed This Session
1. ✅ Read PROCESS-0001 and PROCESS-0002
2. ✅ Reviewed FamilyBondBot communication system
3. ✅ Drafted outline for PROCESS-0003 (process contribution)
4. ✅ Identified 3 key gaps to address

## In Progress
- Drafting PROCESS-0003 documentation
- 40% complete (120 of 300 lines)
- Current section: "Steps" (Step 4 of 6)

## Next Session
1. Complete "Steps" section (steps 4-6)
2. Add "Success Criteria" section
3. Add "Rollback" section
4. Review and test against PROCESS-0001 pattern
5. File submission note
6. Commit to git

## Critical Context
- Reference files: .deia/processes/PROCESS-0001.md, PROCESS-0002.md
- FamilyBondBot master reference: familybondbot/.deia/MASTER-DEIA-REFERENCE.md
- Draft location: .deia/processes/PROCESS-0003-process-discovery-and-contribution.md (in progress, not yet committed)
- Gaps found: vendor-specific patterns not documented, global/local hierarchy not explicit

## Unsaved Work
- Current draft in working memory (150 lines written but not yet committed)
- Outline and notes in `.deia/working/process-0003-notes.md`
```

---

## How to Avoid Problems

### DO
- ✅ Save pre-compact instructions BEFORE compact happens
- ✅ Be specific about line numbers and file locations
- ✅ Commit all work immediately after completing each task step
- ✅ Create timestamped handoff documents
- ✅ Update heartbeat with exact next action

### DON'T
- ❌ Wait until last minute to save state
- ❌ Leave uncommitted changes ("I'll commit after I'm done")
- ❌ Use vague instructions ("continue with the work")
- ❌ Assume context will be remembered across compact
- ❌ Skip the pre-compact handoff and rely on task file alone

---

## If Compact Happens Without Preparation

**Recovery steps:**
1. Read git log to see last commit message and what was done
2. Read active task file (`.deia/hive/tasks/YYYY-MM-DD-HHMM-*TASK*.md`)
3. Read all coordination messages in `.deia/hive/coordination/` (latest first)
4. Read heartbeat (`.deia/hive/heartbeats/CLAUDE-CODE-NNN.yaml`)
5. If pre-compact handoff exists, read that
6. Piece together what was being done
7. Create new pre-compact handoff for THIS session if needed

**This is slower (5-10 min) than having prepared instructions (30 seconds), so always prepare.**

---

## Related Patterns

- **Checkpointing:** Save state at clear milestones, not just at compact
- **Progress Saving (vendor-agnostic):** Continually save work, don't wait for completion
- **Git Commits:** Frequent, meaningful commits are essential for recovery
- **Heartbeat Status:** Keep `.deia/hive/heartbeats/` updated continuously

---

## Implementation Checklist

- [ ] Pre-compact instructions file created
- [ ] Handoff document created and timestamped
- [ ] All work committed to git
- [ ] Heartbeat updated with current status
- [ ] Next action is specific and clear
- [ ] No uncommitted changes remain
- [ ] All context is documented somewhere discoverable

---

## Notes

**Why this matters:** In a multi-vendor world where different LLMs might pick up work from each other, explicit handoff documents become a lingua franca. Codex, GPT-5, or another Claude instance can resume work if the handoff is explicit enough.

**Scalability:** As DEIA projects scale to multiple concurrent bees of different vendors, clear pre-compact handoffs ensure no work is lost and any vendor can resume any task.
