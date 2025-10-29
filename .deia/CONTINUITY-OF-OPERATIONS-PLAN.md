# DEIA Continuity of Operations Plan (COOP)

**Document Type:** Operational Procedure
**Authority:** Q33N / ScrumMaster
**Effective Date:** 2025-10-28
**Status:** ACTIVE
**Classification:** Operational / Recovery Playbook

---

## Purpose

Define how to resume DEIA operations after any interruption:
- Session crashes or timeouts
- Context limit reached (autocompact)
- System reboot or shutdown
- Emergency pause/stop
- Planned maintenance

This document ensures **zero loss of operational continuity** and **complete recovery of work state**.

---

## Quick Start (5 Minutes)

If you're resuming after interruption:

1. **Read this section** (you're doing it now) - 1 min
2. **Follow the Checkpoint Recovery sequence** below - 2 min
3. **Review In-Progress Work** - 2 min
4. **Resume execution** - See "Resuming Work" section

---

## Core Principle

**Every work session creates a checkpoint.** On resumption, you read the checkpoint, understand where you left off, and continue from that exact point.

---

## Part 1: Session Checkpointing (What To Do DURING Work)

### The Three Types of Checkpoints

#### Type 1: Continuous Logging (Automatic)
- **What:** Activity logs written as work happens
- **Where:** `.deia/bot-logs/[BOT-ID]-activity.jsonl`
- **Format:** JSONL, one event per line
- **Frequency:** Every 5-15 minutes minimum
- **Your job:** Ensure logging is ON

**Verify logging is active:**
```bash
# Check recent activity log entries
tail -20 .deia/bot-logs/CLAUDE-CODE-001-activity.jsonl | jq .

# Should show recent timestamps
# If timestamps are old (>1 hour), logging is stale
```

#### Type 2: Session Handoff (Manual, At End of Session)
- **What:** Document of what you completed and what's next
- **Where:** `.deia/handoffs/CLAUDE-CODE-SESSION-[DATE]-[TIME]-handoff.md`
- **Format:** Markdown with structured sections
- **Frequency:** At end of every session or when stopping work
- **Your job:** Create this before disconnecting

**Required sections in handoff:**
```markdown
# Session Handoff - [Date] [Time]

## What Was Completed
- [List completed items with commit refs]

## What Was Started But Not Finished
- [List in-progress items with exact state]

## Next Steps (For Resumption)
- [Ordered list of what to do next]
- [Exact files to read/modify]
- [Tests to run]

## Cookie Trail / Debugging Notes
- [Anything that would help next session debug issues]
- [Known quirks or gotchas]
- [Debug checklist if something goes wrong]

## Git Status
- Branch: [current branch]
- Uncommitted changes: [list or "none"]
- Latest commits: [last 3 commit hashes/messages]
```

#### Type 3: Work-in-Progress Markers (Structural)
- **What:** Files/dirs that mark incomplete work
- **Where:** Various (task files, .deia/hive/tasks/, response files, etc.)
- **Format:** File existence indicates state
- **Your job:** Leave them in place if work incomplete

**Examples:**
- Task file still in `.deia/hive/tasks/BOT-ID/` = Not yet processed
- Response file in `.deia/hive/responses/` = Work was completed
- `.deia/IN-PROGRESS/` = Work started
- Staged git changes = Not yet committed

---

## Part 2: Checkpoint Recovery (What To Do ON RESUMPTION)

### Recovery Sequence (Must Follow In Order)

#### Step 1: Understand What Happened (2 min)
```bash
# Check git status - what changed?
git status

# Check recent commits - what was last completed?
git log --oneline -10

# Check handoff document - what was the plan?
ls -lt .deia/handoffs/ | head -5
cat .deia/handoffs/[LATEST-HANDOFF]
```

**What you learn:**
- What code was last committed
- What was still in progress
- What the next step should have been

#### Step 2: Review Activity Logs (2 min)
```bash
# Check when work last happened
tail -50 .deia/bot-logs/CLAUDE-CODE-001-activity.jsonl | jq .

# Look for:
# - Timestamps (how long ago?)
# - Last event type (what was happening?)
# - Any errors recorded?
```

**What you learn:**
- Exact point work stopped
- Any errors that occurred
- How long ago work was active

#### Step 3: Review Task Queue (1 min)
```bash
# Check what's still waiting
ls .deia/hive/tasks/BOT-001/

# Check what was completed
ls .deia/hive/responses/ | grep BOT-001 | tail -20
```

**What you learn:**
- Pending work that needs to be done
- Last task that was completed
- Any failed tasks

#### Step 4: Check Git Changes (1 min)
```bash
# What's staged?
git diff --cached --name-only

# What's unstaged?
git diff --name-only

# Any uncommitted work?
git status
```

**What you learn:**
- If there are uncommitted code changes
- What files were being modified
- Whether changes are safe to commit

#### Step 5: Re-establish Context (2 min)
Read in this order:
1. The session handoff document (`.deia/handoffs/latest-handoff.md`)
2. The last 3 commit messages (`git log --oneline -3`)
3. Any debug notes in the handoff's "Cookie Trail" section

**At this point you should be able to answer:**
- What was I working on?
- What did I complete?
- What's the next thing to do?
- Are there any gotchas I should know about?

---

## Part 3: Resuming Work (What To Do AFTER Recovery)

### Resume Sequence

#### Step 1: Commit Any Staged Changes
```bash
# If there are staged changes from before interruption
git status

# If changes are safe (review them first!)
git add [remaining-files]
git commit -m "Resume session: [brief description of what was added]"
```

**Only commit if:**
- You understand what the changes are
- They were intentionally staged
- Tests pass (if applicable)
- The handoff says it's safe to commit

#### Step 2: Run Tests (If Applicable)
```bash
# Run unit tests for modified files
pytest tests/unit/test_[module].py -v

# Check for regressions
pytest tests/ -v --tb=short
```

**Only continue if:**
- Tests pass
- No new failures
- Coverage maintained

#### Step 3: Continue From Handoff Plan
Follow the "Next Steps" section of your handoff document exactly:
- Read the files it says to read
- Modify the files it says to modify
- Run the tests it says to run

#### Step 4: Create New Session Log
```bash
# Start by documenting this resumption
cat >> .deia/bot-logs/CLAUDE-CODE-001-activity.jsonl << 'EOF'
{
  "ts": "2025-10-28T14:00:00Z",
  "agent_id": "CLAUDE-CODE-001",
  "event": "session_resumed",
  "message": "Resuming after [reason: crash/context-limit/planned-stop/etc]",
  "resumed_from_handoff": ".deia/handoffs/[HANDOFF-FILE]",
  "next_action": "[What you're about to do]"
}
EOF
```

This creates an audit trail showing continuity.

#### Step 5: Execute Planned Work
Now proceed with the work outlined in the handoff's "Next Steps" section.

---

## Part 4: In-Progress Work Tracking

### How To Mark Work As In-Progress

Use `.deia/IN-PROGRESS/` directory to track work that's started but not finished:

```bash
# When starting a task that will take multiple sessions
touch .deia/IN-PROGRESS/BOT-001-TASK-implement-feature-x

# File contents (optional but recommended)
cat > .deia/IN-PROGRESS/BOT-001-TASK-implement-feature-x.md << 'EOF'
# In-Progress: Feature X Implementation

**Started:** 2025-10-28 13:00
**Last Updated:** 2025-10-28 14:30
**Expected Completion:** 2025-10-29

## Current State
- Step 1: Design complete ✅
- Step 2: Skeleton code written ✅
- Step 3: Core logic in progress 🔄 (50% done)
- Step 4: Testing - not started

## Files Being Modified
- src/deia/features/feature_x.py
- tests/unit/test_feature_x.py

## Next Action
Complete core logic implementation in feature_x.py, then run tests.

## Notes
- Need to handle edge case with empty input
- Performance might be issue with large datasets
EOF

# On resumption, read this file to understand state
cat .deia/IN-PROGRESS/BOT-001-TASK-implement-feature-x.md

# When work is complete
rm .deia/IN-PROGRESS/BOT-001-TASK-implement-feature-x.md
git add src/deia/features/feature_x.py tests/unit/test_feature_x.py
git commit -m "feat: Complete Feature X implementation"
```

### How To Find In-Progress Work On Resumption

```bash
# List all in-progress work
ls .deia/IN-PROGRESS/

# Read the status of each
for file in .deia/IN-PROGRESS/*.md; do
  echo "=== $(basename $file) ==="
  head -20 "$file"
done
```

---

## Part 5: Session Handoff Template

Use this template when ending a session:

```markdown
# Session Handoff - [Date] [Time to Time]

**Session Duration:** [hours:minutes]
**Status:** [COMPLETE / IN-PROGRESS]
**Last Commit:** [commit-hash - commit-message]

---

## What Was Completed This Session

### Deliverables
- [Specific thing 1] - File: path/to/file.py
- [Specific thing 2] - Files: multiple-files
- [Specific thing 3] - Commit: abc1234

### Tests Added/Modified
- [Test suite 1]: X/Y tests passing
- [Test suite 2]: Coverage now at Z%

### Documentation
- [Docs updated]: path/to/doc.md
- [Comments added]: In files: ...

### Commits Made
```
abc1234 - commit message 1
def5678 - commit message 2
ghi9012 - commit message 3
```

---

## What Was Started But Not Finished

### In-Progress Work
1. **Feature: [Name]**
   - Status: [0-100%] complete
   - Files: src/deia/module/file.py
   - Last change: [brief description]
   - Blocker: [If blocked, what's blocking?]

2. **Bug Fix: [Description]**
   - Status: [0-100%] complete
   - Root cause: [What's the issue?]
   - Solution approach: [How will it be fixed?]
   - Files touched: ...

### Staged Changes (In Git)
[If any - list them]

### Uncommitted Changes
[If any - describe what's not staged and why]

---

## Next Steps (For Resumption)

**In order:**

1. Read this handoff completely
2. Read `.deia/DEBUG-TRAIL-*.md` if any (investigation notes)
3. Check git log: `git log --oneline -5`
4. Check git status: `git status`
5. Review activity log: `tail -30 .deia/bot-logs/CLAUDE-CODE-001-activity.jsonl`
6. [SPECIFIC STEP 1]: [Exact action to take]
   - Read file: [path/to/file]
   - Verify: [what to check]
   - Run: [exact command]
7. [SPECIFIC STEP 2]: [Next action]
   - Continue from: [exact line/function in code]
   - Complete: [what needs to be done]
   - Test with: [exact test command]
8. [SPECIFIC STEP 3]: [Final steps]
   - Commit with message: "[Suggested commit message]"
   - Run full test suite: `pytest tests/ -v`

---

## Cookie Trail / Debugging Notes

### Known Issues
- [Issue 1]: [Symptom], [Root cause], [Workaround]
- [Issue 2]: ...

### Gotchas to Watch For
- [Gotcha 1]: [Why it's tricky], [How to avoid]
- [Gotcha 2]: ...

### Performance Notes
- [What's slow]: [Why], [Possible optimization]

### Test Failures (If Any)
- [Test name]: [Why it fails], [How to fix]

### Things That Might Break Next Session
- [Potential issue 1]: [Watch for symptom X], [Check file Y]
- [Potential issue 2]: ...

### Debug Checklist (If Something Goes Wrong)
- [ ] Check git log for unexpected changes
- [ ] Check activity log for errors (grep error .deia/bot-logs/...)
- [ ] Run tests to find what broke
- [ ] Check if dependencies changed
- [ ] Verify no staged changes conflict with new work

---

## Git Status at End of Session

**Current Branch:** [branch-name]

**Latest Commits:**
```
[hash] - [message]
[hash] - [message]
[hash] - [message]
```

**Staged Changes:** [None / List files]

**Uncommitted Changes:** [None / List files]

**Status:**
```
[Output of: git status]
```

---

## Session Summary

**Time Spent:** [X hours Y minutes]
**Most Time On:** [Task/area that consumed most time]
**Blockers Encountered:** [List or "None"]
**Quality Issues Found:** [List or "None"]
**Tests Written:** [X new, Y modified]
**Documentation Updated:** [Y/N, specifics]

---

## Recommendations for Next Session

- [Recommendation 1]: [Why, and action to take]
- [Recommendation 2]: ...

---

**Handoff Complete - Ready for Resumption**

---

```

---

## Part 6: Implementation Checklist

### For Every Session, You Must:

**During Work:**
- [ ] Keep logging ON (verify every 30 minutes)
- [ ] Commit work regularly (every major feature/fix)
- [ ] Update activity logs (events every 10-15 min)

**At End of Session (Before Disconnecting):**
- [ ] Create session handoff document in `.deia/handoffs/`
- [ ] Include all required sections (completion, in-progress, next steps)
- [ ] Add cookie trail and debugging notes
- [ ] Commit any final staged changes
- [ ] Verify latest commit has clear message
- [ ] Run test suite one final time
- [ ] Update `.deia/IN-PROGRESS/` markers if work incomplete

**On Resumption (Before Continuing):**
- [ ] Read session handoff
- [ ] Check git log and status
- [ ] Review activity logs for errors
- [ ] Follow "Next Steps" in handoff exactly
- [ ] Run tests to verify no regressions
- [ ] Log resumption event to activity log
- [ ] Continue from exact point handoff indicates

---

## Part 7: Special Cases

### Case 1: Crash/Unexpected Interruption

**Recovery:**
1. Check if there's a session handoff from last time
2. If no handoff: reconstruct from git log + activity log
3. Check for uncommitted changes: `git status`
4. Decide: commit, discard, or investigate further?
5. Follow "Checkpoint Recovery" sequence

**Prevention:**
Create handoff before every planned stop.

### Case 2: Context Limit Hit (Autocompact)

**Recovery:**
1. Handoff document MUST exist (created before hitting limit)
2. Read it to understand where you left off
3. Follow "Resume Sequence" exactly
4. Note: You lost context, so follow steps carefully

**Prevention:**
Save handoff proactively when approaching context limit.

### Case 3: Merged Commits From Other Agents

**Recovery:**
1. Pull latest: `git pull`
2. Check for merge conflicts: `git status`
3. If conflicts: resolve them before continuing
4. Run tests to verify integration
5. Continue with handoff plan

**Prevention:**
Pull before creating handoff. Note any recent merges in handoff.

### Case 4: Multi-Day Work (Task Spans Sessions)

**Procedure:**
1. Create `.deia/IN-PROGRESS/` marker file
2. Create detailed handoff at end of each session
3. Each session starts by reading IN-PROGRESS marker
4. Update IN-PROGRESS marker with new status
5. When complete, remove marker and commit

**Example:**
```bash
# Session 1
touch .deia/IN-PROGRESS/feature-x-implementation.md
# Do 50% of work
# Create handoff with current status

# Session 2 (resumption)
cat .deia/IN-PROGRESS/feature-x-implementation.md
# Update status
# Complete remaining 50%
# Remove marker, commit, delete marker file
rm .deia/IN-PROGRESS/feature-x-implementation.md
```

---

## Part 8: References & Related Documents

**Read these if you need more detail on specific areas:**

- **TESTING-PROTOCOL.md** - How to run tests on resumption
- **INTEGRATION-PROTOCOL.md** - How to integrate completed work
- **AGENT-COMMUNICATION-CADENCE-v1.0.md** - How to log and communicate
- **BEE-000-Q33N-BOOT-PROTOCOL.md** - Q33N governance and reporting
- **SCRUMMASTER-PROTOCOL.md** - Task queue management

---

## Part 9: Success Criteria

You are maintaining continuity of operations successfully when:

✅ **Checkpointing:**
- Activity logs updated every 10-15 minutes
- Session handoffs created at end of each session
- All sessions have clear commit messages

✅ **Recovery:**
- After any interruption, you can resume in <5 minutes
- Zero loss of work or context
- Previous session's handoff clearly shows next steps

✅ **Quality:**
- Tests pass after resumption
- No regressions introduced
- Code is clean and ready to merge

✅ **Traceability:**
- Git history shows clear progression
- Activity logs show when work happened
- Handoffs document all decisions

---

## Violations / Red Flags

🚩 **Sessions with no handoff** - Can't resume easily
🚩 **Uncommitted work left in progress** - Lost if crash happens
🚩 **No activity log entries** - Can't audit what happened
🚩 **Unclear commit messages** - Others can't understand changes
🚩 **Tests failing after resumption** - Indicates lost context

---

## Summary

**Continuity of Operations = Checkpoints + Recovery Procedures**

1. **Create checkpoints constantly** (logging, commits, handoffs)
2. **Follow recovery procedure on resumption** (read, understand, continue)
3. **Leave clear breadcrumbs** (comments, notes, structured handoff)
4. **Test everything** before and after resumption
5. **Document decisions** so others can understand and continue

**The next session will thank you for the work you document today.**

---

**Document Version:** 1.0
**Effective:** 2025-10-28
**Authority:** Q33N
**Maintained By:** All agents
**Review Cycle:** Quarterly or as processes change
