# Dave Questions - Ongoing Dialog

**Purpose:** This document tracks questions from Dave, answers/discussion, and resulting actions.

**Workflow:**
1. Dave adds questions to `docs/Dave Questions.md`
2. Claude reviews and answers in this dialog doc
3. Questions are removed from Dave Questions.md once reviewed
4. This doc maintains history and tracks outcomes

---

## Session 2025-10-09

### Q1: AI-assisted Review in VS Code Extension

**Question:**
> One of the benefits of using AI to run this process, is that in addition to the py process to generate the docs, we can also use AI to help us generate solutions. I have a thought that while we are in the chat window in VS Code, we have another #deia command that will use the AI to review docs. Is that possible? If so, we can use that to help us generate solutions to submissions. How might that work?
>
> I really like the idea of having the VS Code extension extend the functionality of the deia process. like, upon VS Code launch, it could check for new submissions, and if there are any, it could notify the user. Then, the user could use a command like #deia review to have the AI review the submission and generate a solution.

**Answer:**

Yes, absolutely possible! Here's how it could work:

**Architecture:**

1. **VS Code Extension Features:**
   - Startup hook: Check `.deia/submissions/pending/` for new submissions
   - Notification system: Toast notification "3 new DEIA submissions to review"
   - Chat participant commands:
     - `#deia review <submission-id>` - Review specific submission
     - `#deia review next` - Review next unreviewed submission
     - `#deia generate-solution <submission-id>` - Generate solution
     - `#deia list-submissions` - Show all pending submissions

2. **Implementation Flow:**

```typescript
// On VS Code startup (extension.ts)
async function onStartup() {
  const submissions = await deiaClient.checkSubmissions();

  if (submissions.pending.length > 0) {
    vscode.window.showInformationMessage(
      `📥 ${submissions.pending.length} new DEIA submission(s) to review`,
      'Review Now', 'Later'
    ).then(selection => {
      if (selection === 'Review Now') {
        // Open chat with context
        vscode.commands.executeCommand('workbench.panel.chat.view.copilot.focus');
        // Could auto-inject: "#deia review next"
      }
    });
  }
}

// Chat participant (chatParticipant.ts)
participant.onRequest('#deia review', async (request, context) => {
  const submissionId = request.args[0] || 'next';

  // Call Python: deia admin review <submission-id>
  const submission = await runDeiaCommand(['admin', 'review', submissionId]);

  // AI reviews the submission
  const analysis = await analyzeSubmission(submission);

  // Return in chat
  return {
    markdown: formatReviewForChat(analysis),
    metadata: { submissionId, analysis }
  };
});
```

3. **Python CLI Support:**

```bash
# Extension calls these Python commands
deia admin list-submissions           # Get pending submissions
deia admin review <id>                # Get submission details
deia admin generate-solution <id>     # Generate solution (with AI context)
```

4. **AI Integration Pattern:**

The AI (via chat participant) would:
- Read submission content (bug report, feature request, pattern)
- Analyze against existing codebase
- Generate solution code
- Create explanation/documentation
- Suggest tests (TDD!)
- Highlight potential issues

**Benefits:**
- ✅ Seamless workflow (no leaving VS Code)
- ✅ AI does heavy lifting of review + solution generation
- ✅ User stays in control (reviews AI suggestions)
- ✅ Platform-agnostic (Python CLI can work with any AI/editor)

**Status:** IDEA - Not implemented
**Action Required:** Create feature request for this

---

### Q2: AI-Assisted Documentation Generation

**Question:**
> Another idea is to have the AI assist in generating documentation for the solutions. For example, after the AI generates a solution, it could also create a summary or explanation of the code, which could be included in the documentation.

**Answer:**

Great idea! This fits perfectly with the TDD approach:

**Implementation:**

1. **When AI generates solution:**
   - Write tests first (TDD)
   - Write implementation
   - Auto-generate documentation:
     - Code explanation
     - Usage examples
     - Best practices followed
     - Integration guide

2. **Python CLI:**

```bash
deia admin generate-solution <submission-id> --with-docs
```

Output structure:
```
solutions/
  <submission-id>/
    ├── solution.py          # Implementation
    ├── test_solution.py     # Tests (written FIRST)
    ├── SOLUTION.md          # AI-generated docs
    └── INTEGRATION.md       # How to integrate this
```

3. **AI Prompt Structure:**

```
You are reviewing a DEIA submission for [bug/feature/pattern].

Submission: [content]

Generate:
1. Tests (TDD - write these FIRST)
2. Implementation
3. Documentation including:
   - What the solution does
   - Why this approach was chosen
   - Best practices applied
   - How to integrate
   - Potential edge cases
```

**Status:** IDEA - Not implemented
**Action Required:** Add to feature backlog

---

### Q3: Protecting Against AI Hallucinations

**Question:**
> I really want to protect against AI hallucinations. How might we do that?

**Answer:**

Excellent concern! Here's a comprehensive strategy:

**1. Data Validation:**
- Before accepting AI output, validate against:
  - Existing code patterns (does this code actually exist?)
  - File paths (does this file exist?)
  - Function signatures (does this API match reality?)

**2. Contextual Awareness:**
- Provide AI with rich context:
  - Actual codebase snippets (via file reads)
  - Git history (what changed recently)
  - Test results (does this actually work?)

**3. AI Self-Check (Before Human Review):**

```bash
deia admin review <id> --with-validation
```

AI process:
1. Generate solution
2. **Self-check phase:**
   - "Does this code reference files that exist?" → Check via file system
   - "Are these function signatures correct?" → Check via code analysis
   - "Does this match the codebase style?" → Check via linting
   - "Would this break existing tests?" → Run tests
3. Report uncertainties:
   ```
   ⚠️  Uncertainties detected:
   - Uncertain if function `processSubmission()` exists in src/deia/core.py
   - Could not verify that this pattern matches codebase style
   ```

**4. Human-in-the-Loop:**
- After AI self-check, human reviews
- Focus review on areas AI flagged as uncertain

**5. Continuous Monitoring & Reporting:**

**THIS IS HUGE - I LOVE YOUR IDEA:**

```bash
deia admin report-hallucination <submission-id> --details "AI suggested function that doesn't exist"
```

This would:
- Log to `.deia/hallucinations/`
- Optionally sync to DEIA Global (if user opts in)
- Build dataset of hallucinations
- Share with AI platforms (OpenAI, Anthropic, etc.) to improve models

**Implementation:**

```python
# src/deia/admin.py
class HallucinationReporter:
    def report(self, submission_id: str, hallucination_type: str, details: str):
        """Report AI hallucination for tracking and improvement"""

        report = {
            "submission_id": submission_id,
            "timestamp": datetime.now().isoformat(),
            "type": hallucination_type,
            "details": details,
            "ai_platform": detect_ai_platform(),  # Claude, GPT-4, etc.
            "model_version": detect_model_version()
        }

        # Save locally
        self._save_local(report)

        # Optionally sync to global
        if user_opted_in():
            self._sync_to_global(report)
```

**Status:** CRITICAL - Should implement before AI review features
**Action Required:** Create ADR + implementation plan

---

### Q4: Protecting Confidential Information

**Question:**
> I also really want to protect against confidential information being shared with the AI. I realize that we might have included some confidential information in the logs, so it would be good to have a way to scrub that information before sending it to the AI for review.

**Answer:**

Great catch! We already have sanitization, but need to enhance it for AI review:

**Current State:**
- `deia sanitize` already removes PII, secrets, API keys
- BUT: It's designed for public sharing, not AI review

**Enhanced Approach for AI Review:**

**1. Two-Tier Sanitization:**

```bash
# Tier 1: For AI review (keeps more context, but removes secrets)
deia sanitize --for-ai <file>

# Tier 2: For public sharing (removes everything sensitive)
deia sanitize --for-public <file>
```

**2. AI-Tier Sanitization Rules:**

**Keep (AI needs this):**
- File structure and names
- Function/variable names (non-sensitive)
- Code logic and patterns
- Error messages (sanitized)
- Workflow descriptions

**Remove (Confidential):**
- API keys, tokens, passwords
- Real customer/user names
- Internal IP addresses
- Proprietary algorithms (mark as [PROPRIETARY])
- Database connection strings
- Email addresses
- Phone numbers
- Anything marked `# CONFIDENTIAL`

**3. Validation Before AI Review:**

```python
def prepare_for_ai_review(submission_path: str) -> str:
    """Sanitize submission for AI review"""

    # Run sanitization
    sanitized = sanitize_for_ai(submission_path)

    # Validate: Check for remaining secrets
    secrets = scan_for_secrets(sanitized)
    if secrets:
        raise ValueError(f"Still contains secrets: {secrets}")

    # Validate: Check information is sufficient
    if not has_sufficient_context(sanitized):
        raise ValueError("Too much removed - AI won't have enough context")

    return sanitized
```

**4. User Control:**

```bash
# Config option
deia config set ai_review_enabled true
deia config set ai_review_auto_sanitize true

# Or prompt before each review
$ deia admin review <id>
⚠️  This will send sanitized content to AI for review.
   Confidential info will be removed automatically.

   Review sanitized version? [Y/n]
```

**Status:** HIGH PRIORITY - Needed before AI review features
**Action Required:** Enhance existing sanitization code

---

### Q5: Token Usage Tracking

**Question:**
> I want to have a way for deia to track the token overhead that it is using so we can make sure its efficient and the user knows how much it's costing them. I would also like token overhead to be reported with submissions to deia global (if people opt in to sharing that info).

**Answer:**

Excellent idea for transparency and efficiency tracking!

**Implementation:**

**1. Token Tracking in Python:**

```python
# src/deia/telemetry.py
class TokenTracker:
    def __init__(self):
        self.session_tokens = 0
        self.total_tokens = self._load_total()

    def track_ai_request(self, prompt: str, response: str, metadata: dict):
        """Track tokens for AI interaction"""

        # Estimate tokens (or get from API response)
        prompt_tokens = estimate_tokens(prompt)
        completion_tokens = estimate_tokens(response)
        total = prompt_tokens + completion_tokens

        # Log
        self._log_usage({
            "timestamp": datetime.now().isoformat(),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total,
            "operation": metadata.get("operation"),  # "review", "generate-solution", etc.
            "submission_id": metadata.get("submission_id"),
            "cost_estimate": self._estimate_cost(total, metadata.get("model"))
        })

        # Update totals
        self.session_tokens += total
        self.total_tokens += total
        self._save_total()
```

**2. CLI Commands:**

```bash
# Show token usage
deia usage
deia usage --session           # This session only
deia usage --by-operation      # Group by operation type
deia usage --cost-estimate     # Show estimated cost

# Output:
Token Usage Summary
-------------------
Session:  1,234 tokens ($0.002)
Today:    12,456 tokens ($0.020)
This Week: 45,678 tokens ($0.075)
Total:    123,456 tokens ($0.200)

By Operation:
  review:           45,000 tokens (36%)
  generate-solution: 35,000 tokens (28%)
  sanitize:         25,000 tokens (20%)
  other:            18,456 tokens (16%)
```

**3. User Notifications:**

```bash
# After expensive operation
$ deia admin generate-solution submission-123

✓ Solution generated!
📊 Token usage: 5,234 tokens (~$0.008)
```

**4. Opt-in Telemetry to DEIA Global:**

```bash
deia config set telemetry_enabled true
deia config set share_token_usage true  # Opt-in
```

Shared data (anonymized):
```json
{
  "user_id": "hash(username)",  // Anonymized
  "operation": "review",
  "tokens": 1234,
  "timestamp": "2025-10-09T10:00:00Z",
  "model": "claude-sonnet-4",
  "success": true
}
```

**5. Efficiency Monitoring:**

```bash
# Admin dashboard
deia admin dashboard

Token Efficiency Metrics
------------------------
Average tokens per review: 1,234
Average tokens per solution: 5,678

Trend: ↓ 15% more efficient than last week
```

**Status:** FEATURE REQUEST - Not implemented
**Action Required:** Create feature spec + implementation plan

---

### Q6: Admin Dashboard

**Question:**
> I want to have a dashboard that shows submissions, findings, solutions, and token usage over time. This dashboard could be part of the VS Code extension for users, and we could also have a web-based dashboard for deia global.

**Answer:**

Love this! Two-tier dashboard approach:

**1. Local Dashboard (VS Code Extension):**

**User View:**
```
╔════════════════════════════════════════════════════════════╗
║               DEIA Personal Dashboard                      ║
╠════════════════════════════════════════════════════════════╣
║ Submissions                                                ║
║   • Pending:    3                                          ║
║   • Reviewed:   12                                         ║
║   • Accepted:   8                                          ║
║                                                            ║
║ Token Usage (This Week)                                    ║
║   • Total: 45,678 tokens (~$0.075)                         ║
║   • Avg per day: 6,525 tokens                              ║
║   • Most expensive: generate-solution (28%)                ║
║                                                            ║
║ Sessions Logged: 24                                        ║
║ Patterns Contributed: 5                                    ║
╚════════════════════════════════════════════════════════════╝
```

**Implementation:**
- VS Code Webview panel
- Calls `deia dashboard --json` to get data
- Charts: submissions over time, token usage trends
- Quick actions: "Review next submission", "View token breakdown"

**2. Global Dashboard (Web-based):**

**Admin View (deiasolutions.com/admin or similar):**

```
DEIA Global Dashboard
=====================

User Activity
-------------
Total Users:              1,234
Active (Last 7 days):     456
New This Week:            23

Extension Downloads
-------------------
Total:                    5,678
This Week:                123
Growth Rate:              +15%

Package Installs (PyPI)
-----------------------
Total:                    12,345
This Week:                234
Version 0.1.0:            98%

Submissions
-----------
Total:                    567
Pending Review:           34
Reviewed This Week:       45

Quality Metrics
---------------
Avg Quality Score:        78/100
Avg Review Time:          2.3 days
Acceptance Rate:          68%

Token Efficiency
----------------
Avg Tokens/Review:        1,234
Avg Tokens/Solution:      5,678
Total Tokens (All Users): 2.3M
Trend:                    ↓ 12% improvement
```

**Technology Stack:**

**Local (VS Code):**
- TypeScript + Webview
- Charts: Chart.js or D3.js
- Data: Local `.deia/` directory

**Global (Web):**
- Backend: Python (FastAPI or Django)
- Frontend: React or Vue.js
- Database: PostgreSQL
- Analytics: Track submissions, downloads, usage
- Authentication: GitHub OAuth (for admins)

**Implementation Steps:**

1. **Phase 1: Local Dashboard (VS Code)**
   - Add webview panel to extension
   - `deia dashboard` CLI command
   - Basic charts (submissions, tokens)

2. **Phase 2: Telemetry Sync**
   - Optional sync to DEIA Global
   - Anonymized data collection
   - Privacy controls

3. **Phase 3: Web Dashboard**
   - Build web backend (FastAPI)
   - Admin authentication
   - Real-time metrics
   - Public stats page

**Status:** FEATURE REQUEST - Long-term
**Action Required:** Create roadmap + phased implementation plan

---

### Q7: TDD as Standard

**Question:**
> Make sure TDD is noted as a Dave standard and a DEIA standard for when we are working on the deia project itself, and also for solutions we generate for submissions.

**Answer:**

Absolutely! Let's document this formally:

**Implementation:**

**1. Document in Project Standards:**

File: `CONTRIBUTING.md`
```markdown
## Development Standards

### Test-Driven Development (TDD)

DEIA uses Test-Driven Development for all code changes:

1. **Write tests FIRST**
2. Run tests (they should fail)
3. Write minimal code to pass tests
4. Refactor
5. Repeat

This applies to:
- ✅ DEIA core functionality
- ✅ CLI commands
- ✅ VS Code extension features
- ✅ Solutions generated for submissions
- ✅ Bug fixes
- ✅ New features

**No exceptions.**
```

**2. Add to Dave's Preferences:**

File: `~/.deia/dave/preferences.md`
```markdown
## Dave's Development Standards

### TDD Always
- Write tests FIRST, implementation second
- No code without tests
- No excuses
```

**3. Add to DEIA Principles:**

File: `PRINCIPLES.md` (new or existing)
```markdown
# DEIA Development Principles

## 1. Test-Driven Development (TDD)

Tests are written BEFORE implementation. Always.

**Why:**
- Ensures code correctness
- Documents expected behavior
- Prevents regressions
- Forces good design

**How:**
1. Write failing test
2. Write minimal code to pass
3. Refactor
4. Commit

## 2. [Other principles...]
```

**4. Enforce in AI Review:**

When AI generates solutions:
```
AI Review Checklist:
☐ Tests written FIRST
☐ Tests cover edge cases
☐ Implementation passes tests
☐ Code is documented
☐ Follows TDD pattern
```

**5. Add Pre-commit Hook:**

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Ensure tests exist for modified code

modified_py_files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | grep -v '^tests/')

if [ -n "$modified_py_files" ]; then
    echo "⚠️  Python files modified:"
    echo "$modified_py_files"
    echo ""
    echo "Did you write tests first? (TDD)"
    read -p "Confirm tests exist [y/N]: " confirm

    if [ "$confirm" != "y" ]; then
        echo "❌ Commit aborted. Write tests first!"
        exit 1
    fi
fi
```

**Status:** ACTION REQUIRED - Document and enforce
**Action Required:**
1. Update CONTRIBUTING.md
2. Create/update PRINCIPLES.md
3. Update Dave's preferences
4. Add to AI review checklist

---

### Q8: Numbering and Tracking System

**Question:**
> Should we start numbering bug reports and feature requests and things coming from this doc, and from submissions? I'd like to have a way to track them, and make sure we are addressing them, and also to make sure we are prioritizing them correctly. How might we do that? What are dev best practices for that?

**Answer:**

Great question! Let's implement a proper issue tracking system.

**Best Practices:**

**Option 1: GitHub Issues (Recommended)**
- ✅ Industry standard
- ✅ Free
- ✅ Integrated with repo
- ✅ Labels, milestones, projects
- ✅ Can reference in commits: "Fixes #123"

**Option 2: Custom DEIA Tracking**
- ✅ Offline-first
- ✅ Integrated with DEIA workflow
- ❌ More work to build
- ❌ Less standard

**Recommendation: Hybrid Approach**

**1. Use GitHub Issues for DEIA Project:**

```bash
# Create issue from CLI
deia admin create-issue --type bug --title "Unicode error on Windows" --from-submission <id>

# Or use gh CLI directly
gh issue create --title "Feature: AI review command" --label enhancement
```

**2. DEIA Submission IDs:**

Format: `DEIA-YYYY-NNN-TYPE`

Examples:
- `DEIA-2025-001-BUG` - First bug report of 2025
- `DEIA-2025-002-FEAT` - Second item, feature request
- `DEIA-2025-003-PAT` - Third item, pattern submission

**3. Automatic ID Assignment:**

```python
# src/deia/submissions.py
def assign_submission_id(submission_type: str) -> str:
    """Assign unique ID to submission"""

    year = datetime.now().year
    next_num = get_next_number(year)

    type_code = {
        'bug': 'BUG',
        'feature': 'FEAT',
        'pattern': 'PAT',
        'improvement': 'IMP'
    }[submission_type]

    return f"DEIA-{year}-{next_num:03d}-{type_code}"
```

**4. Tracking File:**

`.deia/submissions/INDEX.md`
```markdown
# DEIA Submissions Index

| ID | Type | Title | Status | Assigned | Priority |
|----|------|-------|--------|----------|----------|
| DEIA-2025-001-BUG | Bug | Unicode error on Windows | ✅ Resolved | @claude | High |
| DEIA-2025-002-FEAT | Feature | AI review command | 🔄 In Progress | @dave | High |
| DEIA-2025-003-PAT | Pattern | Yes-but handling | ⏳ Pending | - | Medium |
```

**5. Link to GitHub Issues:**

```bash
# Create GitHub issue from DEIA submission
deia admin sync-to-github DEIA-2025-002-FEAT

# Creates issue:
# Title: [DEIA-2025-002-FEAT] AI review command
# Body: [submission content]
# Labels: feature, deia-submission
```

**6. Priority System:**

```
P0 - Critical (security, data loss)
P1 - High (blocks users, major bugs)
P2 - Medium (important features, minor bugs)
P3 - Low (nice-to-have, polish)
```

**7. Status Workflow:**

```
Pending → Triaged → In Progress → Review → Done → Closed
```

**8. CLI Commands:**

```bash
# List all submissions
deia admin list --status pending --priority high

# Show submission details
deia admin show DEIA-2025-001-BUG

# Update status
deia admin update DEIA-2025-002-FEAT --status "in-progress" --assign dave

# Link to GitHub issue
deia admin link DEIA-2025-002-FEAT --github-issue 456
```

**Status:** SHOULD IMPLEMENT - Before we get too many submissions
**Action Required:**
1. Design ID format
2. Create index/tracking system
3. GitHub integration
4. Add CLI commands

---

## Summary of Actions Required

### Immediate (This Session)
1. ✅ Review Dave's questions
2. ⏳ Create this dialog document
3. ⏳ Clear Dave Questions.md
4. ⏳ Create tracking issues for new features

### High Priority (Next Sprint)
1. Document TDD as standard (CONTRIBUTING.md, PRINCIPLES.md)
2. Implement submission ID system
3. Enhance sanitization for AI review
4. Create hallucination reporting system

### Medium Priority (Future)
1. Token tracking system
2. Local dashboard (VS Code)
3. AI review commands (#deia review)
4. GitHub integration

### Long-term
1. Web-based admin dashboard
2. Telemetry sync to global
3. AI-assisted documentation generation

---

## Questions Waiting for Dave

None currently - all questions answered above.

---

**Last Updated:** 2025-10-09
**Next Review:** When Dave adds new questions to Dave Questions.md
