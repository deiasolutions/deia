# DEIA Multi-Tier Submission Workflow

**The complete process for submitting patterns, bugs, and improvements from projects to the global BOK**

---

## Overview

DEIA uses a **three-tier submission system**:

1. **Project Level** - Where patterns are identified during work
2. **User Level** - Where you review and filter what to share
3. **Global Level** - Community-wide BOK on GitHub

This ensures:
- ✅ No accidental sharing of sensitive/project-specific info
- ✅ You control what goes public vs. stays private
- ✅ Quality submissions through review at each level

---

## The Three Tiers

### Tier 1: Project Level

**Location:** `<project>/.deia/submissions/`

**Purpose:** Capture submittable content during project work

**Who:** You (as developer/user) + Claude

**Process:**
1. While working in a project, Claude identifies submittable content:
   - Patterns that could help others
   - Bugs in DEIA itself
   - Process improvements
   - Anti-patterns to avoid

2. Claude suggests: "This looks submittable. Create a submission?"

3. You approve → Claude creates submission file in `.deia/submissions/pending/`

4. Submission stays in project until you review it

### Tier 2: User Level

**Location:** `~/.deia/submissions/`

**Purpose:** Aggregate, review, and filter submissions from all your projects

**Who:** You (as DEIA user)

**Process:**
1. Run `deia sync-projects` to aggregate submissions from all projects

2. Run `deia review-submissions` to see what's pending

3. For each submission, decide:
   - **Promote to global:** Useful for everyone → Goes to global BOK
   - **Keep local:** Useful only for you → Goes to your private BOK
   - **Discard:** Not useful → Delete

4. Run `deia submit-to-global` to submit approved items

### Tier 3: Global Level

**Location:** `github.com/deiasolutions/deia-bok` (or issues/PRs in main repo)

**Purpose:** Community-wide Body of Knowledge

**Who:** DEIA admins (Dave + others)

**Process:**
1. Submission arrives as PR or issue

2. Admin reviews:
   - Security scan (no secrets/malicious code)
   - Quality check (well-structured, universal)
   - Sanitization check (no PII/proprietary info)

3. Admin decides:
   - **Accept:** Merge to BOK
   - **Request changes:** Comment with required improvements
   - **Reject:** Close with explanation

---

## Detailed Workflows

### For Users: Creating Submissions

#### During Project Work (Automatic)

**Claude will:**
1. Monitor conversation for submittable patterns
2. Suggest when something is worth submitting
3. Create submission file with metadata
4. Place in `.deia/submissions/pending/`

**You can:**
- Accept Claude's suggestion → Submission created
- Decline → No submission created
- Manually run `deia submit` → Guided submission creation

#### Manual Submission Creation

```bash
# Generic submission (guided prompts)
deia submit

# Specific submission types
deia submit bug-report
deia submit improvement
deia submit pattern
deia submit process
deia submit anti-pattern
```

**What happens:**
1. DEIA asks for required info (title, description, category, etc.)
2. Creates submission file in `.deia/submissions/pending/`
3. Opens file for you to add details
4. Automatically runs sanitization check
5. Warns if potential PII/secrets detected

#### Submission File Structure

```markdown
---
type: pattern  # or bug-report, improvement, process, anti-pattern
project: familybondbot
created: 2025-10-09
status: pending
sanitized: true
---

# [Title]

## Summary
Brief description

## Details
Full explanation

## Category
Where this belongs in BOK

## Validation
How you know it works

## Tags
Relevant keywords
```

---

### For Users: Reviewing Submissions

#### Sync from Projects

```bash
# Aggregate submissions from all projects
deia sync-projects

# Output:
# ✓ Found 3 submissions in familybondbot
# ✓ Found 1 submission in otherperoject
# ✓ Synced 4 submissions to ~/.deia/submissions/review-queue/
```

#### Review Queue

```bash
# Interactive review
deia review-submissions

# Shows each submission:
# 1. pattern-002.md (from familybondbot)
#    "Architecture Review Template for AI Projects"
#    [P]romote to global | [K]eep local | [D]iscard | [E]dit | [S]kip
```

**For each submission:**

**P - Promote to global:**
- Moves to `~/.deia/submissions/to-global/`
- Will be submitted to GitHub when you run `deia submit-to-global`

**K - Keep local:**
- Moves to `~/.deia/local-bok/`
- Usable by you, not shared publicly
- Still available for future promotion if you change your mind

**D - Discard:**
- Deletes the submission
- Permanently removed (can't be recovered)

**E - Edit:**
- Opens in your editor
- Make changes, then review again

**S - Skip:**
- Leaves in review queue
- Review later

#### Submit to Global

```bash
# Submit all approved items
deia submit-to-global

# Or submit specific item
deia submit-to-global pattern-002.md
```

**What happens:**
1. DEIA runs final sanitization check
2. Creates PR or issue in global repo
3. Tracks submission status
4. Moves to `~/.deia/submissions/submitted-to-global/`
5. You can check status with `deia submissions status`

---

### For Admins: Reviewing Submissions

#### View Queue

```bash
# Show all pending submissions
deia admin queue

# Output:
# Pending Submissions (12):
#
# HIGH PRIORITY (3):
#   1. Bug: Logger not capturing conversations (#45)
#   2. Security: Sanitization bypass found (#46)
#   3. Breaking: API change needed (#47)
#
# NORMAL (8):
#   4. Pattern: Architecture Review Template (#48)
#   5. Pattern: Test before asking human (#49)
#   ...
#
# LOW (1):
#   12. Improvement: Better CLI help text (#50)
```

#### Review Submission

```bash
# Review next in queue
deia admin review-next

# Or review specific submission
deia admin review submissions/pending/pattern-002.md
```

**DEIA runs:**
1. Security scan (secrets, malicious code)
2. Quality check (structure, completeness)
3. Sanitization check (PII, proprietary info)
4. Shows results + recommendation

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Submission Review: pattern-002.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: Architecture Review Template
Type: Pattern
Submitter: daveeichler
Project: familybondbot

━━━━ Security Scan ━━━━
✓ No secrets found
✓ No malicious patterns

━━━━ Quality Check ━━━━
✓ All required sections present
✓ Code blocks properly labeled
✓ Sufficient detail

━━━━ Sanitization ━━━━
⚠ 1 potential issue:
  Line 45: Possible internal URL "mycompany.internal"

━━━━ Overall ━━━━
Risk Score: 15/100 (LOW)
Recommendation: APPROVE (after fixing sanitization warning)

Actions:
[A]ccept | [R]eject | [C]hanges needed | [F]lag user | [S]kip
```

#### Admin Actions

**Accept:**
```bash
deia admin accept pattern-002.md

# Optional: Add to specific BOK location
deia admin accept pattern-002.md --to bok/patterns/development/
```

**Request Changes:**
```bash
deia admin request-changes pattern-002.md \
  --comment "Please remove internal URL on line 45"
```

**Reject:**
```bash
deia admin reject pattern-002.md \
  --reason "Too project-specific. Not universal enough for BOK."
```

**Flag User:**
```bash
deia admin flag-user daveeichler \
  --reason "Multiple sanitization issues"
```

---

## Directory Structure Reference

### Project Level
```
familybondbot/
└── .deia/
    ├── config.json
    ├── sessions/
    └── submissions/
        ├── pending/              # Awaiting user review
        │   ├── bug-001.md
        │   └── pattern-002.md
        └── submitted/            # Sent to user level
```

### User Level
```
~/.deia/
├── config.json
├── submissions/
│   ├── review-queue/             # From all projects
│   │   ├── fbb/
│   │   │   ├── bug-001.md
│   │   │   └── pattern-002.md
│   │   └── otherproject/
│   ├── to-global/                # Approved for submission
│   │   └── pattern-002.md
│   ├── submitted-to-global/      # Tracking
│   │   └── pattern-002.json
│   └── archived/                 # Old submissions
├── local-bok/                    # Private patterns
│   ├── patterns/
│   │   └── my-workflow.md
│   ├── processes/
│   └── anti-patterns/
└── templates/                    # Custom templates
```

### Global Level
```
deia-bok/  (GitHub repo)
├── submissions/
│   ├── pending/                  # PRs awaiting review
│   ├── accepted/                 # Ready to merge
│   └── rejected/                 # For reference
├── bok/
│   ├── patterns/
│   │   ├── collaboration/
│   │   ├── development/
│   │   └── ...
│   ├── platforms/
│   └── anti-patterns/
└── .deia-admin/
    ├── banned-users.json
    ├── flagged-users.json
    └── stats.json
```

---

## Configuration

### Project Level Config

`.deia/config.json`:
```json
{
  "auto_log": true,
  "project": "familybondbot",
  "user": "daveeichler",
  "submissions": {
    "auto_suggest": true,
    "require_sanitization": true,
    "default_type": "pattern"
  }
}
```

### User Level Config

`~/.deia/config.json`:
```json
{
  "user": "daveeichler",
  "email": "dave@deiasolutions.org",
  "github_username": "daveeichler",
  "submissions": {
    "auto_sync": false,
    "sync_interval_days": 7,
    "require_review": true,
    "default_action": "prompt"
  },
  "local_bok": {
    "enabled": true,
    "path": "~/.deia/local-bok"
  }
}
```

---

## Command Reference

### User Commands

**Submission Creation:**
- `deia submit` - Create submission (guided)
- `deia submit bug-report` - Create bug report
- `deia submit improvement` - Create improvement suggestion
- `deia submit pattern` - Submit pattern
- `deia submit process` - Submit process/workflow
- `deia submit anti-pattern` - Submit anti-pattern

**Review & Sync:**
- `deia sync-projects` - Aggregate submissions from projects
- `deia review-submissions` - Interactive review queue
- `deia promote <file>` - Promote specific submission to global
- `deia keep-local <file>` - Keep submission in local BOK
- `deia discard <file>` - Delete submission

**Global Submission:**
- `deia submit-to-global` - Submit all approved items
- `deia submit-to-global <file>` - Submit specific item
- `deia submissions status` - Check status of submitted items
- `deia submissions list` - List all submissions

**Local BOK:**
- `deia local-bok list` - List your private patterns
- `deia local-bok search <query>` - Search local BOK
- `deia local-bok show <file>` - Show specific pattern

### Admin Commands

**Review Queue:**
- `deia admin queue` - Show pending submissions
- `deia admin review-next` - Review next in queue
- `deia admin review <file>` - Review specific submission

**Actions:**
- `deia admin accept <file>` - Accept and merge
- `deia admin accept <file> --to <path>` - Accept to specific location
- `deia admin reject <file> --reason "..."` - Reject
- `deia admin request-changes <file> --comment "..."` - Request changes

**User Management:**
- `deia admin ban-user <username>` - Ban user
- `deia admin unban-user <username>` - Unban user
- `deia admin flag-user <username>` - Flag for review
- `deia admin list-banned` - List banned users
- `deia admin list-flagged` - List flagged users

**Analysis:**
- `deia admin scan <file>` - Security scan only
- `deia admin quality <file>` - Quality check only
- `deia admin stats` - Submission statistics

---

## Automation & Enforcement

### Claude Integration

DEIA memory (`.claude/preferences/deia.md`) includes:

1. **Pattern Detection:** Claude watches for submittable content
2. **Suggestion Prompts:** Claude asks if you want to create submission
3. **Auto-creation:** With permission, Claude creates submission files
4. **Reminder:** Claude reminds to review submissions periodically

### Periodic Checks

```bash
# Check for unreviewed submissions
deia doctor

# Output:
# ⚠ Unreviewed Submissions:
#   3 submissions in review queue (oldest: 12 days)
#   Run: deia review-submissions
#
# ⚠ Projects Not Synced:
#   familybondbot: last synced 15 days ago
#   Run: deia sync-projects
```

### Git Hooks (Optional)

**Pre-commit:** Warn if unsubmitted patterns
**Post-commit:** Remind to sync projects

---

## Best Practices

### For Submitters

**DO:**
- ✅ Review submissions before promoting to global
- ✅ Sanitize thoroughly (no PII, secrets, proprietary info)
- ✅ Make patterns universal (not project-specific)
- ✅ Provide validation (how you know it works)
- ✅ Use descriptive titles and tags

**DON'T:**
- ❌ Skip sanitization checks
- ❌ Submit untested ideas
- ❌ Include client/company names
- ❌ Share proprietary code
- ❌ Submit without reviewing

### For Admins

**DO:**
- ✅ Run full review (`deia admin review`)
- ✅ Check sanitization carefully
- ✅ Verify pattern is universal
- ✅ Provide constructive feedback
- ✅ Be consistent with decisions

**DON'T:**
- ❌ Accept without security scan
- ❌ Skip quality checks
- ❌ Reject without explanation
- ❌ Let queue grow stale (>7 days)

---

## Troubleshooting

### "No submissions found"

**Cause:** No pending submissions in projects

**Fix:** Create a submission first:
```bash
deia submit
```

### "Sync failed"

**Cause:** Project not DEIA-enabled

**Fix:** Initialize DEIA in project:
```bash
cd /path/to/project
deia init
```

### "Sanitization warnings"

**Cause:** Potential PII/secrets detected

**Fix:** Review file manually:
```bash
deia sanitize <file> --review
```

Then edit file to remove sensitive info.

### "Submission rejected"

**Cause:** Failed security/quality checks

**Fix:** Check rejection reason:
```bash
deia submissions status <submission-id>
```

Address issues and resubmit.

---

## Summary

**The complete flow:**

1. **Work** → Claude identifies submittable content
2. **Create** → Submission file created in project
3. **Sync** → Aggregate to user level (`deia sync-projects`)
4. **Review** → Filter local vs. global (`deia review-submissions`)
5. **Submit** → Send to global BOK (`deia submit-to-global`)
6. **Admin Review** → Admin accepts/rejects/requests-changes
7. **Merge** → Pattern added to global BOK

**Key principles:**
- ✅ You control what's shared
- ✅ Multiple review stages catch issues
- ✅ Automation reduces friction
- ✅ Quality and security enforced

---

**Ready to start?**

```bash
# First time setup
deia init

# Create your first submission
deia submit pattern

# Review your submissions
deia review-submissions

# Submit to global BOK
deia submit-to-global
```

---

**Questions?** See [CONTRIBUTING.md](../CONTRIBUTING.md) or run `deia help submissions`
