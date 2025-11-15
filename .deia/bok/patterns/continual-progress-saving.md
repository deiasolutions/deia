# PATTERN: Continual Progress Saving

**Category:** Work Execution / Reliability
**Applies to:** All LLM vendors (Claude, Codex, etc.)
**Status:** Active
**Last Updated:** 2025-11-14

---

## What Is This?

Never wait for a task to be fully complete before saving progress. Save intermediate work at every logical step, every file creation, every test run, every decision point. This is the opposite of "I'll commit when I'm done."

---

## Why It Matters

- **Resilience:** If the vendor crashes, context resets, or session ends unexpectedly, you only lose work since the last save
- **Visibility:** Q33N and other bees can see progress in real-time via git commits and heartbeat updates
- **Trust:** Frequent commits build confidence that work is actually happening
- **Parallelization:** Other bees can start dependent work once early stages are saved
- **Recovery:** New sessions can resume from saved state, not from task start

---

## When to Apply

- Every time you complete a numbered step in a task
- Every time you create or modify a file
- Every time you finish a logical unit of work
- Before taking a risky action
- At natural checkpoints in your work

---

## Core Practice

### Pattern 1: Commit After Every Step

**Structure:**
```bash
# Step 1: Do something
# ... work ...

# Save step 1
git add src/file1.js
git commit -m "feat: implement feature step 1

- Description of what was done
- Acceptance criteria met: [list]
- Status: Ready for next step / Blocked on [X]"

# Step 2: Do next thing
# ... work ...

# Save step 2
git add src/file2.js tests/file2.test.js
git commit -m "feat: implement feature step 2 with tests"

# Continue...
```

**Why:** Each commit is a savepoint. If something breaks, you only roll back to that point.

### Pattern 2: Update Heartbeat After Each Step

**Every vendor should:**
1. Complete a step
2. Update `.deia/hive/heartbeats/[VENDOR-ID].yaml`
3. Commit the heartbeat update

**Example:**
```yaml
status: "working"
task: "2025-11-14-1600-Q33N-BOT-00002-TASK-season-008-tests"
progress_pct: 33  # Step 1 of 3 complete
step: "1 of 3"
last_save: "2025-11-14 14:30"
last_commit: "tests: add basic functionality tests"
blockers: "none"
next: "Add edge case tests (step 2)"
```

### Pattern 3: Create Intermediate Responses Before Final Response

**Progression:**
```
Step 1 complete → Commit
Step 2 complete → Commit + brief status message in coordination
Step 3 complete → Commit + fuller update
Task complete → Create final response file (.deia/hive/responses/)
```

**Example coordination file during work (optional):**
```
.deia/hive/coordination/2025-11-14-1445-BOT-00002-Q33N-SYNC-season-008-progress.md

Task: Season 008 Tests
Status: In Progress (Step 2 of 3)
Progress: 66% - Tests 1-10 written and passing
Next: Edge case tests (step 3)
ETA: 30 minutes
No blockers
```

---

## Examples

### Example 1: Multi-Step Feature Implementation

**Task:** Write 15 unit tests (broken into 5 chunks of 3 tests each)

**Bad approach (waiting until done):**
```
Start → Write all 15 tests (2 hours) → Commit all at once → Report done
```
Problem: If crash at test 14, all 2 hours lost.

**Good approach (saving at every checkpoint):**
```
Start → Write tests 1-3 → Commit
       → Write tests 4-6 → Commit
       → Write tests 7-9 → Commit
       → Write tests 10-12 → Commit
       → Write tests 13-15 → Commit
       → Run all tests & verify passing → Commit
       → Report done in response file
```

Each commit is a savepoint. If crash at test 14, only last 10 minutes lost (since commit 4).

### Example 2: Multi-File Feature

**Task:** Create authentication system (3 files)

**Bad:**
```
Start → Write auth.js (30 min) → Write tests (30 min) → Write config (20 min)
     → Run test suite (10 min) → Commit all → Report done
```
Problem: Entire 90 minutes can be lost if something goes wrong.

**Good:**
```
Start → Write auth.js skeleton → Commit "feat: auth skeleton"
     → Write auth.js implementation → Commit "feat: auth implementation"
     → Write auth.test.js → Commit "tests: auth unit tests"
     → Write auth.config.js → Commit "config: auth configuration"
     → Run full test suite → Commit "tests: all auth tests passing"
     → Report done in response file
```

Each of 5 commits is safe. Maximum loss is ~15 minutes between commits.

### Example 3: Research / Exploration Task

**Task:** Discover and document a new process

**Bad:**
```
Start → Read 3 files (1 hour) → Draft outline (30 min) → Write full doc (1.5 hours)
     → Review & finalize (30 min) → Commit all → Submit
```
Problem: 3.5 hours of work in a single commit. If writing is lost, so is all context.

**Good:**
```
Start → Read file 1 & notes → Commit "docs: process discovery notes part 1"
     → Read file 2 & notes → Commit "docs: process discovery notes part 2"
     → Read file 3 & notes → Commit "docs: process discovery notes part 3"
     → Draft outline → Commit "docs: process outline"
     → Write sections 1-3 → Commit "docs: process sections 1-3"
     → Write sections 4-6 → Commit "docs: process sections 4-6"
     → Review & finalize → Commit "docs: process complete and reviewed"
     → Submit via submission file
```

Each step is saved. Discovery notes are safe even if writing fails. Outline is safe. Etc.

---

## How to Implement

### 1. Break Tasks Into Steps

Before starting, look at the task and identify logical save points:
```
Task: "Write Season 008 Tests"

Steps (natural breaking points):
1. Read Season 008 spec → Save (commit)
2. Create test file & scaffold → Save (commit)
3. Write tests 1-5 → Save (commit)
4. Write tests 6-10 → Save (commit)
5. Write tests 11-15 → Save (commit)
6. Run tests & verify all pass → Save (commit)
7. Report completion → Create response file, archive task
```

### 2. Complete Each Step, Then Immediately Save

```
Do step 1
↓
Save/Commit
↓
Do step 2
↓
Save/Commit
↓
(repeat)
```

Never `Do step 1` → `Do step 2` → `Do step 3` → `Save all`

### 3. Use Clear Commit Messages

Each commit should say what was done:
```
Good: "feat: write unit tests for season 008 features 1-5"
Bad:  "work in progress"

Good: "docs: process outline and initial draft"
Bad:  "updates"

Good: "fix: edge case handling in auth validator"
Bad:  "fix"
```

### 4. Update Heartbeat Between Commits

Let Q33N know you're alive and making progress:
```yaml
last_update: "2025-11-14 14:35"
progress_pct: 50
last_commit: "tests: write unit tests 1-10"
next: "write unit tests 11-15 and run full test suite"
```

---

## How to Verify You're Following This Pattern

- [ ] You have 5+ commits in the last hour (shows frequent saves)
- [ ] Each commit message describes what was done
- [ ] Heartbeat file is updated after each logical step
- [ ] No single commit is more than 30-45 minutes of work
- [ ] If session crashed right now, you'd only lose work since last commit
- [ ] Q33N can see progress in real-time via git log and heartbeat

---

## What Gets Saved Where

| What | Where | When |
|------|-------|------|
| Code changes | Git commit | After each logical step |
| Status update | `.deia/hive/heartbeats/[ID].yaml` | Every 15-30 min or step |
| Task response | `.deia/hive/responses/` | When task is complete |
| Work progress | Coordination message (optional) | If blocked or need feedback |

---

## Avoiding Common Mistakes

### ❌ DON'T: Batch All Work Then Commit

```bash
# BAD - 90 minutes of work, one commit
[write tests 1-15]
git commit -m "add tests"
```

### ✅ DO: Commit at Natural Checkpoints

```bash
# GOOD - 15 min per step, 6 commits
[write tests 1-5]
git commit -m "tests: write unit tests 1-5"

[write tests 6-10]
git commit -m "tests: write unit tests 6-10"

[write tests 11-15]
git commit -m "tests: write unit tests 11-15"

[run and verify]
git commit -m "tests: all 15 tests passing"
```

### ❌ DON'T: Create Response File Only When Done

### ✅ DO: Update Heartbeat During Work

```yaml
# Updated after each step
last_commit: "tests: 1-5 complete"
progress_pct: 33

# Later
last_commit: "tests: 1-10 complete"
progress_pct: 66

# Finally
last_commit: "tests: all 15 complete and passing"
progress_pct: 100
```

---

## Related Patterns

- **Checkpointing:** Save state at clear milestones
- **Pre-Compact Instructions (Claude):** Vendor-specific way to save state before context reset
- **Task Archival (PROCESS-0002):** Final save and archival when task is complete

---

## Authority

This is a fundamental DEIA principle that applies to all vendors equally. Non-negotiable.
