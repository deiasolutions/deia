# DEIA Submission Workflow - Implementation Plan

**Complete fix with assurances that Claude will follow the process**

---

## Current Status

✅ **Audit complete** - docs/SUBMISSION_WORKFLOW_AUDIT.md
✅ **Workflow documented** - docs/SUBMISSION_WORKFLOW.md
⏳ **Implementation in progress**

---

## Implementation Phases

### Phase 1: Core Submission Module (HIGH PRIORITY)

**File:** `src/deia/submissions.py`

**Classes:**
- `SubmissionManager` - Handles submission creation, review, sync
- `SubmissionTemplate` - Template system for different submission types
- `SubmissionValidator` - Validates submissions before promotion
- `SubmissionSync` - Syncs between project and user level

**Status:** Need to build (4-6 hours)

### Phase 2: CLI Commands (HIGH PRIORITY)

**File:** `src/deia/cli.py` (add to existing)

**Command groups:**
```python
@main.group()
def submit():
    """Create and manage submissions"""
    pass

@submit.command('create')  # deia submit create
@submit.command('bug-report')  # deia submit bug-report
@submit.command('improvement')  # deia submit improvement
@submit.command('pattern')  # deia submit pattern

@main.command('sync-projects')  # deia sync-projects
@main.command('review-submissions')  # deia review-submissions
@main.command('submit-to-global')  # deia submit-to-global
```

**Status:** Need to build (2-3 hours)

### Phase 3: DEIA Memory Update (HIGH PRIORITY)

**File:** `.claude/preferences/deia.md`

**Add sections:**
- Submission detection during sessions
- Prompt user to create submissions
- Reminder to review submissions periodically
- Verification that workflow is followed

**Status:** Need to build (1 hour)

### Phase 4: Admin Queue Management (MEDIUM PRIORITY)

**File:** `src/deia/admin.py` (extend existing)

**Add commands:**
```python
@admin.command('queue')  # deia admin queue
@admin.command('review-next')  # deia admin review-next
@admin.command('accept')  # deia admin accept <file>
@admin.command('reject')  # deia admin reject <file>
@admin.command('request-changes')  # deia admin request-changes <file>
@admin.command('stats')  # deia admin stats
```

**Status:** Need to build (2-3 hours)

### Phase 5: Verification & Tests (MEDIUM PRIORITY)

**Files:**
- `tests/test_submissions.py` - Unit tests for submission module
- `tests/test_workflow.py` - End-to-end workflow test
- `src/deia/verify.py` - Verification commands

**Commands:**
```python
@main.command('verify-workflow')  # deia verify-workflow
@main.command('test-submission')  # deia test-submission
```

**Status:** Need to build (2-3 hours)

### Phase 6: Documentation Updates (LOW PRIORITY)

**Files to update:**
- `README.md` - Add submission workflow overview
- `CONTRIBUTING.md` - Update with new submission process
- `docs/quickstart.md` - Add submission examples

**Status:** Need to build (1-2 hours)

---

## Detailed Implementation: Phase 1

### src/deia/submissions.py

This is the core module that all other parts depend on.

**Key functions:**

1. **Submission Creation**
```python
def create_submission(
    submission_type: str,  # bug-report, improvement, pattern, etc.
    title: str,
    description: str,
    category: str,
    **kwargs
) -> Path:
    """Create a new submission in .deia/submissions/pending/"""
    pass
```

2. **Project Sync**
```python
def sync_projects() -> dict:
    """
    Scan all projects with .deia/ for pending submissions.
    Aggregate to ~/.deia/submissions/review-queue/
    Returns: {'synced': 4, 'projects': ['fbb', 'other']}
    """
    pass
```

3. **Interactive Review**
```python
def review_submissions_interactive():
    """
    Interactive CLI for reviewing submissions.
    For each submission, prompt: Promote/Keep-local/Discard/Edit/Skip
    """
    pass
```

4. **Global Submission**
```python
def submit_to_global(submission_file: Path) -> dict:
    """
    Submit to global BOK via GitHub PR or issue.
    Returns: {'pr_url': '...', 'tracking_id': '...'}
    """
    pass
```

---

## Detailed Implementation: Phase 3

### Update .claude/preferences/deia.md

Add this section to the DEIA memory:

```markdown
## Submission Workflow

**IMPORTANT: Claude must actively suggest submissions during sessions**

### Detection Rules

While working, watch for:
1. **Patterns worth sharing:**
   - Universal solutions (not project-specific)
   - Validated approaches (proven to work)
   - Time-saving techniques
   - Common pitfalls and how to avoid them

2. **Bugs in DEIA:**
   - Any issues with DEIA itself
   - Documentation inaccuracies
   - Feature gaps

3. **Process improvements:**
   - Better workflows
   - Automation opportunities

### When to Suggest

**Suggest creating submission when:**
- User discovers a useful pattern
- User solves a tricky problem elegantly
- User mentions "this could help others"
- You identify a repeatable solution

**How to suggest:**
```
Claude: "This looks like a useful pattern for other developers.
         Would you like to create a submission for the DEIA BOK?

         I can help you document it now while it's fresh."
```

### Creating Submissions

**When user agrees:**
```python
from deia.submissions import create_submission

# Get details from conversation context
title = "Architecture Review Template"
description = "Systematic process for reviewing project architecture..."
category = "patterns/development"

# Create submission
submission_file = create_submission(
    submission_type="pattern",
    title=title,
    description=description,
    category=category
)

# Inform user
print(f"✓ Submission created: {submission_file}")
print("Review later with: deia review-submissions")
```

### Periodic Reminders

**At end of session:**
- Check if .deia/submissions/pending/ has items
- If yes, remind user: "You have N pending submissions to review"

**Weekly:**
- Check if ~/.deia/submissions/review-queue/ has old items (>7 days)
- Suggest: "Run 'deia review-submissions' to clear your queue"

### Verification

**Before ending session, verify:**
1. Did we identify any submittable content?
2. If yes, did we create submissions?
3. If submissions created, did we remind user to review?

**This ensures the workflow is actually followed.**
```

---

## Assurances for Dave

### 1. Documentation is Complete
✅ Full workflow documented in `docs/SUBMISSION_WORKFLOW.md`
✅ Current state audit in `docs/SUBMISSION_WORKFLOW_AUDIT.md`
✅ Implementation plan in `docs/IMPLEMENTATION_PLAN.md`

### 2. Claude Will Follow the Process

**Enforcement mechanisms:**
1. **Memory Integration:** `.claude/preferences/deia.md` includes submission workflow
2. **Detection Rules:** Claude checks for submittable content automatically
3. **Prompts:** Claude suggests submissions during work
4. **Reminders:** Claude reminds at end of session
5. **Verification:** Claude verifies workflow was followed

**Testing:**
1. End-to-end test simulates full workflow
2. Verification command checks all steps
3. Doctor command diagnoses issues

### 3. Gaps Are Filled

**Before this fix:**
❌ No submission creation commands
❌ No user-level review workflow
❌ No sync between project and user level
❌ No global submission automation
❌ No admin batch review
❌ No verification/testing

**After this fix:**
✅ Complete CLI command set
✅ Interactive review workflow
✅ Auto-sync from projects
✅ One-command global submission
✅ Admin queue management
✅ Verification tests pass

### 4. Backwards Compatible

**Existing functionality preserved:**
- All current CLI commands still work
- Admin tools unchanged (only extended)
- Existing .deia/ directories compatible
- No breaking changes

### 5. Measurable Success

**You can verify the fix works by:**

```bash
# 1. Create a test submission
cd familybondbot
deia submit pattern --title "Test Pattern"

# 2. Sync to user level
deia sync-projects
# Expected: "Synced 1 submission from familybondbot"

# 3. Review submissions
deia review-submissions
# Expected: Interactive prompt showing test submission

# 4. Verify workflow
deia verify-workflow
# Expected: "✓ All workflow checks passed"

# 5. Check Claude follows process
# Start Claude Code session, identify a pattern
# Expected: Claude suggests creating submission
```

---

## Time Estimate

**Total implementation time:** 12-17 hours

**Breakdown:**
- Phase 1 (Core module): 4-6 hours
- Phase 2 (CLI commands): 2-3 hours
- Phase 3 (DEIA memory): 1 hour
- Phase 4 (Admin queue): 2-3 hours
- Phase 5 (Verification): 2-3 hours
- Phase 6 (Docs): 1-2 hours

**Can be done in phases:**
- Phases 1-3 = Minimum viable (7-10 hours)
- Phases 4-5 = Full featured (11-16 hours)
- Phase 6 = Polish (12-17 hours)

---

## Next Steps

**Immediate (this session):**
1. ✅ Complete audit
2. ✅ Document workflow
3. ✅ Create implementation plan
4. ⏳ Build Phase 1 (core submission module)
5. ⏳ Build Phase 2 (CLI commands)
6. ⏳ Update Phase 3 (DEIA memory)

**Follow-up (next session):**
1. Test end-to-end workflow
2. Build Phase 4 (admin queue)
3. Build Phase 5 (verification)
4. Update Phase 6 (documentation)

**Verification (final session):**
1. Run `deia verify-workflow` → Pass
2. Test with real submission → Success
3. Confirm Claude suggests submissions → Working
4. Sign off: Gaps filled, assurances met

---

## Dave's Approval Checklist

Before marking this as "complete", verify:

- [ ] Documentation is clear and comprehensive
- [ ] CLI commands exist and work
- [ ] Claude memory enforces workflow
- [ ] End-to-end test passes
- [ ] Can create submission in project
- [ ] Can sync to user level
- [ ] Can review submissions
- [ ] Can submit to global
- [ ] Admin can review queue
- [ ] Verification tests pass
- [ ] Claude actively suggests submissions during work

**When all boxes checked:** Workflow is complete and Claude will follow it.

---

**Status:** Ready to implement Phase 1-3
**ETA for MVP:** 7-10 hours of work
**ETA for complete:** 12-17 hours of work
