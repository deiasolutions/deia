# DEIA Submission Workflow - Current State Audit

**Date:** 2025-10-09
**Purpose:** Document what exists, what's missing, and what needs to be built

---

## What We Have (Existing)

### 1. Directory Structure
✅ `.deia/submissions/` - Exists in deiasolutions repo
✅ `.deia/intake/` - Exists for incoming submissions
✅ `.deia/reviewed/` - Exists for reviewed items
✅ `.deia/sessions/` - Exists for session logs

### 2. Admin Tools (src/deia/admin.py)
✅ `SecurityScanner` - Scans for secrets, API keys, malicious code
✅ `QualityChecker` - Validates submission structure and formatting
✅ `UserManager` - Ban/flag/unban users
✅ `AIReviewer` - Combined security + quality analysis

### 3. CLI Commands (Admin-facing)
✅ `deia admin scan <file>` - Security scan
✅ `deia admin quality <file>` - Quality check
✅ `deia admin review <file>` - Full review
✅ `deia admin ban-user <username>` - Ban user
✅ `deia admin unban-user <username>` - Unban user
✅ `deia admin flag-user <username>` - Flag user
✅ `deia admin list-banned` - List banned users
✅ `deia admin list-flagged` - List flagged users

### 4. Documentation
✅ `docs/sanitization-workflow.md` - Sanitization process
✅ `CONTRIBUTING.md` - Manual PR/issue submission process
✅ `DEIA_MEMORY_HIERARCHY.md` - Claude Code memory levels

### 5. Examples
✅ Two submission files from FBB in `.deia/submissions/`

---

## What's Missing (Critical Gaps)

### 1. Multi-Tier Submission Workflow Documentation
❌ **No documentation** of the complete flow:
   - Project level → User level → Global level
   - What stays local vs. what goes global
   - How decisions propagate between levels

### 2. User-Facing CLI Commands
❌ `deia submit` - Create submission from current project
❌ `deia submit bug-report` - Create bug report
❌ `deia submit improvement` - Create improvement suggestion
❌ `deia submit pattern` - Submit BOK pattern
❌ `deia review-submissions` - Review your pending submissions
❌ `deia promote <submission>` - Promote local → global
❌ `deia keep-local <submission>` - Mark as local-only

### 3. Automated Submission Creation
❌ No automation to detect submittable content in projects
❌ No templates for different submission types
❌ No guided submission creation workflow

### 4. User-Level Review Workflow
❌ No process for user to review their submissions
❌ No filtering mechanism (local vs. global)
❌ No user-level BOK separate from global

### 5. Propagation Mechanism
❌ No automation to move submissions between levels
❌ No sync between project `.deia/` and user `~/.deia/`
❌ No process to submit from user level to global

### 6. Admin Review Queue
❌ No batch review interface for admins
❌ No priority/categorization system
❌ No dashboard or summary view
❌ No workflow to accept/reject/request-changes

### 7. Claude Integration
❌ DEIA memory doesn't enforce submission workflow
❌ No prompts to create submissions during work
❌ No automatic detection of submittable patterns
❌ No verification that Claude follows the process

---

## The Complete Workflow (Desired State)

### Level 1: Project Level (e.g., FBB)

**Location:** `familybondbot/.deia/submissions/`

**What happens:**
1. During Claude Code session in FBB, patterns/bugs/improvements are identified
2. Claude suggests: "This looks like a submittable pattern. Create submission?"
3. User approves → Claude runs `deia submit pattern`
4. Submission created in `familybondbot/.deia/submissions/pending/`
5. File includes metadata: project, date, type, sanitization status

**Submission types:**
- Bug reports
- Improvement suggestions
- BOK patterns
- Processes/workflows
- Anti-patterns

### Level 2: User Level (Dave's machine)

**Location:** `~/.deia/submissions/`

**What happens:**
1. Periodically, user runs `deia sync-projects`
2. DEIA scans all projects with `.deia/submissions/pending/`
3. Aggregates submissions to `~/.deia/submissions/review-queue/`
4. User runs `deia review-submissions`
5. For each submission:
   - ✅ Approve → Move to `~/.deia/submissions/to-global/`
   - 🏠 Keep local → Move to `~/.deia/local-bok/`
   - ❌ Discard → Delete
   - ✏️ Edit → Open for modification

**Local BOK:**
- Patterns specific to Dave's workflow
- Client-specific patterns (sanitized but not universal)
- Experimental patterns not ready for global

### Level 3: Global BOK (GitHub)

**Location:** `github.com/deiasolutions/deia` (or `deia-bok` repo)

**What happens:**
1. User runs `deia submit-to-global`
2. DEIA creates PR or issue in global repo
3. Submission goes to admin review queue
4. Admin (Dave or others) reviews:
   - Run `deia admin review <file>`
   - Check security, quality, universality
   - Accept → Merge to BOK
   - Request changes → Comment on PR
   - Reject → Close with explanation

### Level 4: Admin Operations

**Tools needed:**
1. `deia admin queue` - Show pending submissions
2. `deia admin review-next` - Review next in queue
3. `deia admin accept <submission>` - Accept and merge
4. `deia admin reject <submission> --reason "..."` - Reject
5. `deia admin request-changes <submission> --comment "..."` - Request changes
6. `deia admin stats` - Show submission stats

---

## Directory Structure (Complete)

### Project Level
```
familybondbot/
├── .deia/
│   ├── config.json
│   ├── sessions/
│   └── submissions/
│       ├── pending/          # New submissions awaiting user review
│       │   ├── bug-report-001.md
│       │   └── pattern-002.md
│       └── submitted/        # Submissions sent to user level
│           └── pattern-002.md
```

### User Level
```
~/.deia/
├── config.json
├── submissions/
│   ├── review-queue/         # Aggregated from all projects
│   │   ├── fbb/
│   │   │   ├── bug-report-001.md
│   │   │   └── pattern-002.md
│   │   └── otherperoject/
│   ├── to-global/            # Approved for global submission
│   │   └── pattern-002.md
│   ├── submitted-to-global/  # Already submitted (tracking)
│   │   └── pattern-002-submitted-2025-10-09.json
│   └── archived/             # Old submissions
├── local-bok/                # User's private patterns
│   ├── patterns/
│   ├── processes/
│   └── anti-patterns/
└── templates/                # Custom submission templates
```

### Global Level (GitHub Repo)
```
deia/ (or deia-bok/)
├── submissions/
│   ├── pending/              # PRs/issues awaiting review
│   ├── accepted/             # Accepted, ready to merge to BOK
│   └── rejected/             # Rejected submissions (for reference)
├── bok/
│   ├── patterns/
│   ├── platforms/
│   └── anti-patterns/
└── .deia-admin/
    ├── banned-users.json
    ├── flagged-users.json
    └── submission-stats.json
```

---

## Enforcement Mechanisms

### 1. DEIA Memory Update
Update `.claude/preferences/deia.md` to include:
- Check for submittable content during sessions
- Prompt user to create submissions
- Automatically run submission workflow
- Verify submissions are reviewed

### 2. Git Hooks
- Pre-commit: Check for unsubmitted patterns in `.deia/submissions/pending/`
- Post-commit: Remind to run `deia sync-projects`

### 3. Periodic Reminders
- `deia doctor` checks for:
  - Unreviewed submissions
  - Stale submissions (>7 days)
  - Projects not synced in >14 days

### 4. Verification Commands
- `deia verify-workflow` - Check if workflow is functioning
- `deia test-submission` - Test submission creation end-to-end

---

## Implementation Plan

### Phase 1: Core User Commands (High Priority)
1. `deia submit` - Create submissions
2. `deia review-submissions` - Review queue
3. `deia promote`/`deia keep-local` - Filtering
4. `deia sync-projects` - Aggregate submissions

### Phase 2: Global Submission (High Priority)
1. `deia submit-to-global` - Submit to GitHub
2. `deia track-submission` - Track status
3. Templates and metadata

### Phase 3: Admin Queue (Medium Priority)
1. `deia admin queue` - Show pending
2. `deia admin review-next` - Batch review
3. `deia admin accept`/`reject` - Actions

### Phase 4: Automation (Medium Priority)
1. Update DEIA memory for enforcement
2. Add suggestions during sessions
3. Periodic reminders

### Phase 5: Verification (Low Priority)
1. `deia verify-workflow` - Verification
2. End-to-end tests
3. Documentation updates

---

## Success Criteria

**The workflow is complete when:**
1. ✅ User can create submission from any project with `deia submit`
2. ✅ Submissions automatically aggregate to user level
3. ✅ User can review and filter (local vs. global)
4. ✅ User can submit to global with one command
5. ✅ Admin can batch-review submissions efficiently
6. ✅ Claude prompts for submissions during sessions
7. ✅ Documentation is complete and clear
8. ✅ End-to-end test passes

**Assurance that Claude follows the process:**
1. ✅ DEIA memory includes submission workflow
2. ✅ Claude checks for submittable content automatically
3. ✅ Claude prompts user to create submissions
4. ✅ Verification commands confirm workflow works
5. ✅ Process is documented in `.claude/CLAUDE.md` at all levels

---

## Next Steps

1. Build Phase 1 commands (user submissions)
2. Create submission templates
3. Update DEIA memory
4. Build Phase 2 (global submission)
5. Build Phase 3 (admin queue)
6. Test end-to-end
7. Deploy and verify

---

**Status:** Audit complete. Ready to build missing components.
