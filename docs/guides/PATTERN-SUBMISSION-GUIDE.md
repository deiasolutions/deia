# Pattern Submission Guide

**Version:** 1.0
**Last Updated:** 2025-10-18
**Maintained By:** DEIA Documentation Team

---

## Table of Contents

1. [Introduction](#introduction)
2. [Before You Submit](#before-you-submit)
3. [Writing Your Pattern](#writing-your-pattern)
4. [Submission Process](#submission-process)
5. [After Submission](#after-submission)
6. [Examples](#examples)
7. [Resources](#resources)
8. [Frequently Asked Questions](#frequently-asked-questions)

---

## Introduction

### What is a BOK Pattern?

A **BOK (Body of Knowledge) pattern** is a documented, reusable solution to a common problem in AI-assisted development. Patterns capture:

- **Problem:** What challenge does this solve?
- **Context:** When should you use this approach?
- **Solution:** How to implement it
- **Evidence:** Why it works (metrics, examples, validation)

Patterns can be:
- **Process patterns** - Workflows and procedures (e.g., git strategies, review processes)
- **Technical patterns** - Code solutions and architectures
- **Platform-specific patterns** - Workarounds for specific tools or platforms
- **Collaboration patterns** - Human-AI coordination approaches
- **Anti-patterns** - Documented mistakes to avoid

### Why Submit Patterns?

**Help the community:**
- Share solutions that worked for you
- Save others from repeating your mistakes
- Build collective intelligence across projects

**Improve your own work:**
- Clarify your thinking through documentation
- Get feedback from experienced practitioners
- Build your reputation as a contributor

**Shape the future:**
- Influence DEIA best practices
- Contribute to AI-assisted development methodology
- Be part of building something bigger

### Who Can Submit?

**Everyone!** Submissions are welcome from:

- ✅ **AI agents** (Claude Code, GPT, Gemini, etc.)
- ✅ **Human developers** working with AI assistants
- ✅ **Project maintainers** documenting lessons learned
- ✅ **New users** who discovered something valuable

**No expertise required** - if you found it useful, others probably will too.

### Submission Workflow Overview

```
1. Identify a reusable pattern from your work
   ↓
2. Write your pattern using our template
   ↓
3. Validate against quality standards
   ↓
4. Submit to .deia/intake/ or create PR
   ↓
5. Master Librarian reviews (1-2 days)
   ↓
6. Feedback or acceptance
   ↓
7. Pattern added to BOK and indexed
```

---

## Before You Submit

### Quality Standards

All BOK patterns must meet **6 core quality criteria** established by the Master Librarian Spec (`.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md` Section 5):

#### 1. ✅ Completeness

**Your pattern MUST include:**
- Clear title and category
- 2-3 sentence summary
- Detailed description (what, why, when)
- Example or code snippet (if applicable)
- Metadata (tags, date, author, confidence level)

**Missing any of these = Revision Required**

---

#### 2. ✅ Clarity

**Your pattern MUST be:**
- Written in clear, concise language
- Properly formatted with correct grammar
- Logically structured (problem → solution → example)
- Free of jargon or with technical terms defined
- Easy to understand without ambiguous references

**Test:** Could a new contributor understand this in 5 minutes?

---

#### 3. ✅ Accuracy

**Your pattern MUST contain:**
- Technically correct information
- Working code examples (if code provided)
- No misleading statements
- Proper attribution for external sources
- Documented caveats or limitations

**Librarian will verify claims when possible**

---

#### 4. ✅ Reusability

**Your pattern MUST be:**
- Applicable beyond a single project (unless platform-specific)
- A general approach, not implementation details
- Generalizable to similar situations
- Clear about its applicability scope

**Anti-pattern:** "This is how we solved X in Project Y" ❌ (too specific)
**Pattern:** "When facing problem X, use approach Y because Z" ✅ (reusable)

---

#### 5. ✅ Unique Value

**Your pattern MUST:**
- Not duplicate existing BOK entries
- Add new knowledge or perspective
- Fill a gap in the taxonomy
- Show evidence of searching for existing patterns

**Before submitting:** Search the BOK and `master-index.yaml` for similar patterns

---

#### 6. ✅ Safety & Ethics

**Your pattern MUST:**
- Contain NO PII (personally identifiable information)
- Contain NO secrets, API keys, or credentials
- Contain NO malicious code or exploits
- Align with DEIA governance values
- Include appropriate disclaimers for risky patterns

**Zero tolerance for violations**

---

### Pattern Structure

A complete pattern includes these sections:

#### Frontmatter (YAML Metadata)

```yaml
---
title: "Pattern Name (Clear and Descriptive)"
tags:
  - tag1  # Primary topic (e.g., git, testing, deployment)
  - tag2  # Secondary topic
  - tag3  # Context (e.g., python, javascript, devops)
urgency: medium  # low, medium, high, critical
platforms:
  - platform1  # Where applicable (linux, windows, macos, web, cli)
audience:
  - audience1  # Who benefits (developers, designers, admins, all)
date_added: YYYY-MM-DD
last_updated: YYYY-MM-DD
contributors:
  - Your Name or Handle
status: active  # active, deprecated, experimental
version: 1.0
---
```

#### Content Sections

1. **Context** - When to use this pattern
2. **Problem** - What problem does it solve?
3. **Solution** - How to implement (step-by-step)
4. **Examples** - Working code/commands with explanations
5. **Testing** - How to verify it works
6. **Variations** - Alternative approaches (optional)
7. **Related Patterns** - Cross-references (optional)
8. **References** - External docs or sources (optional)

---

## Writing Your Pattern

### Use the Template

We provide a complete pattern template at **`templates/pattern-template.md`**.

**Download and fill it out:**
```bash
cp templates/pattern-template.md my-pattern-name.md
# Edit my-pattern-name.md with your content
```

The template includes:
- Complete YAML frontmatter with all fields
- All recommended sections with prompts
- Quality checklist at the end
- Examples of good formatting

### Good Example vs Bad Example

#### ❌ Bad Pattern (Too Specific, Unclear)

```markdown
# Fix the bug

We had a bug with the thing and we fixed it by changing line 47.

tags: bug-fix
```

**Problems:**
- No clear title
- No context about when to use
- No explanation of the problem
- No reusable solution
- No metadata

---

#### ✅ Good Pattern (Complete, Clear, Reusable)

```markdown
---
title: "Pattern: Handle Unicode in Windows Git Bash"
tags:
  - windows
  - git-bash
  - unicode
  - encoding
urgency: medium
platforms:
  - windows
audience:
  - developers
date_added: 2025-10-18
contributors:
  - CLAUDE-CODE-002
status: active
version: 1.0
---

# Pattern: Handle Unicode in Windows Git Bash

**When using Windows Git Bash, Python scripts may crash with UnicodeEncodeError when printing non-ASCII characters.**

## Context

Use this pattern when:
- Running Python scripts in Windows Git Bash
- Output contains emoji, foreign characters, or symbols
- Getting `UnicodeEncodeError: 'charmap' codec can't encode...`

## Problem

Windows Git Bash defaults to `cp1252` encoding, which doesn't support Unicode characters. Python's `print()` function crashes when trying to output characters outside ASCII range.

## Solution

### Step 1: Set UTF-8 Encoding in Python

```python
import sys
import io

# Force UTF-8 encoding for stdout/stderr
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

### Step 2: Use Safe Print Function

```python
def safe_print(text):
    """Print text with fallback for encoding errors"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback: replace problematic characters
        print(text.encode('ascii', 'replace').decode('ascii'))
```

## Testing

```bash
# Test with emoji
python test_unicode.py
# Should print: ✅ Success! (not crash)
```

## Related Patterns

- See also: [Windows Git Bash Path Conversion](../platforms/shells/windows-git-bash-path-conversion.md)

## Evidence

**Projects using this pattern:**
- deiasolutions (Oct 2025)
- parentchildcontactsolutions (Sep 2025)

**Validation:** Eliminates UnicodeEncodeError crashes in Windows Git Bash environments.
```

---

### Explain Frontmatter Fields

**Required fields:**
- `title` - Clear, descriptive name with pattern type prefix
- `tags` - 3-10 searchable keywords
- `date_added` - Date you created the pattern (YYYY-MM-DD)
- `contributors` - Your name, handle, or agent ID
- `status` - `active` (use this unless deprecated or experimental)

**Recommended fields:**
- `urgency` - How critical is this? (`low`, `medium`, `high`, `critical`)
- `platforms` - Where applicable? (`windows`, `linux`, `macos`, `Platform-Agnostic`)
- `audience` - Who benefits? (`developers`, `designers`, `devops`, `all`)
- `version` - Start with `1.0`, increment for major changes

**Optional fields:**
- `last_updated` - Date of last significant change
- `source_project` - Which project discovered this?
- `confidence` - `Experimental`, `Validated`, or `Proven`

---

### Sanitization (Critical!)

**Before submitting, remove ALL sensitive information:**

#### Remove PII (Personally Identifiable Information)
- ❌ Real names → ✅ `<YOUR_NAME>` or `Jane Doe`
- ❌ Email addresses → ✅ `your-email@example.com`
- ❌ Phone numbers → ✅ `555-0100`
- ❌ Physical addresses → ✅ `123 Main St, Anytown`
- ❌ IP addresses → ✅ `192.0.2.1` (use example.com range)

#### Remove Secrets
- ❌ API keys → ✅ `YOUR_API_KEY_HERE`
- ❌ Passwords → ✅ `your-secure-password`
- ❌ Tokens → ✅ `YOUR_ACCESS_TOKEN`
- ❌ Database credentials → ✅ `username:password@localhost`

#### Remove Proprietary Information
- ❌ Internal URLs → ✅ `https://internal.example.com`
- ❌ Company names → ✅ `AcmeCorp` or `<YOUR_COMPANY>`
- ❌ Project codenames → ✅ Generic descriptions
- ❌ Customer names → ✅ `Customer A`, `Client B`

**Use placeholders consistently:**
```python
# Good: Clear placeholders
API_KEY = "YOUR_API_KEY_HERE"
EMAIL = "your-email@example.com"
BASE_URL = "https://api.example.com"

# Bad: Real credentials
API_KEY = "sk_live_abc123..."  # ❌ NEVER DO THIS
```

---

### Validation Tools

#### Manual Checklist (Use Now)

Before submitting, verify:
- [ ] Frontmatter complete with all required fields
- [ ] No PII, secrets, or proprietary information
- [ ] Clear problem statement
- [ ] Step-by-step solution
- [ ] Working examples (tested if code included)
- [ ] Proper grammar and formatting
- [ ] 3-10 relevant tags
- [ ] Not a duplicate (searched BOK first)

#### CLI Validator (Coming in Phase 2)

```bash
# Future: Automated validation
deia pattern validate my-pattern.md

# Will check:
# ✅ Frontmatter format
# ✅ Required fields present
# ✅ No common secrets (API key patterns)
# ✅ Markdown formatting
# ⚠️ Warnings for improvement
```

---

## Submission Process

### Method 1: Manual Submission (Current)

**Best for:** First-time contributors, simple patterns

**Steps:**

#### 1. Create Intake Directory

```bash
# Create dated directory for your submission
mkdir -p .deia/intake/$(date +%Y-%m-%d)/my-pattern-name

cd .deia/intake/$(date +%Y-%m-%d)/my-pattern-name
```

#### 2. Add Your Pattern Files

```bash
# Copy your pattern markdown
cp ~/my-pattern.md ./pattern-name.md

# Add any supporting files
cp ~/examples/*.py ./
cp ~/diagrams/*.png ./
```

#### 3. Create MANIFEST.md

Create `.deia/intake/YYYY-MM-DD/my-pattern-name/MANIFEST.md`:

```markdown
# Submission Manifest

**Title:** Pattern: [Your Pattern Title]
**Category:** [Pattern|Anti-Pattern|Process|Platform-Specific|Methodology]
**Tags:** tag1, tag2, tag3
**Author:** [Your Name or Agent ID]
**Date:** 2025-10-18
**Confidence:** [Experimental|Validated|Proven]
**Source Project:** [project-name] (optional)

---

## Summary

[2-3 sentence summary of your pattern]

---

## Why This is Valuable

[Explain why this should be in the BOK - what gap does it fill?]

---

## Files Included

- `pattern-name.md` - Main pattern document
- `example.py` - Code example (if applicable)

---

**Ready for review:** Yes
```

#### 4. Submit

**Option A: Git commit (if you have write access)**
```bash
git add .deia/intake/
git commit -m "docs(bok): Submit pattern - [Pattern Title]"
git push
```

**Option B: Create Pull Request**
```bash
# Fork repo, commit to your fork, create PR
# Title: "BOK Submission: [Pattern Title]"
# Label: bok-submission
```

**Option C: GitHub Issue**
```
Title: BOK Submission: [Pattern Title]
Label: bok-submission

Paste your pattern content or link to files
```

#### 5. Wait for Review

- Master Librarian will review within 48 hours (active projects)
- You'll receive feedback via:
  - SYNC message (`.deia/tunnel/claude-to-claude/`)
  - GitHub PR comments
  - `REVIEW-FEEDBACK.md` in your intake directory

---

### Method 2: CLI Submission (Phase 2 - Coming Soon)

**Best for:** Experienced contributors, automated workflows

**Steps:**

#### 1. Extract Pattern from Session

```bash
# Auto-extract pattern from conversation log
deia pattern extract .deia/sessions/20251018-103000-conversation.md

# Output: Suggested pattern saved to draft-pattern.md
```

#### 2. Review and Edit

```bash
# Open in your editor
code draft-pattern.md

# AI suggestions will be highlighted
# Edit as needed, add examples, refine wording
```

#### 3. Validate

```bash
# Check quality standards
deia pattern validate draft-pattern.md

# Output:
# ✅ Frontmatter complete
# ✅ No secrets detected
# ✅ Required sections present
# ⚠️ Consider adding more tags
# ⚠️ No code examples found
```

#### 4. Submit

```bash
# Add to BOK intake
deia pattern add draft-pattern.md

# Output:
# ✅ Pattern submitted to .deia/intake/2025-10-18/
# 🔔 Master Librarian notified
# ⏱️ Expected review: 1-2 days
```

---

### Submission Locations

Choose the right location for your submission:

#### .deia/intake/YYYY-MM-DD/ (Recommended)

**Use for:**
- First-time submissions
- Patterns needing review
- Uncertain about quality or placement

**Process:** Master Librarian reviews, provides feedback, integrates to BOK

---

#### Direct PR to bok/ (Experienced Contributors)

**Use for:**
- You're familiar with BOK structure
- High-confidence pattern
- Want to propose specific placement

**Process:**
1. Place file in appropriate `bok/` subdirectory
2. Update `master-index.yaml`
3. Create PR with detailed description
4. Librarian reviews PR for approval

**Note:** May request changes or relocation

---

#### GitHub Issue (Suggestions)

**Use for:**
- Idea for a pattern but not ready to write
- Request for someone else to document
- Discussion before submission

**Process:** Create issue with `bok-submission` label, community discusses

---

## After Submission

### Review Process

#### Step 1: Master Librarian Claims Submission

**Timeline:** Within 24-48 hours (active projects)

**What happens:**
- Librarian creates `CLAIMED-BY-[AGENT-ID].txt` in your intake directory
- You'll see who's reviewing and expected completion time

---

#### Step 2: Quality Review

**Librarian checks:**
1. **Completeness** - All required fields and sections?
2. **Clarity** - Easy to understand?
3. **Accuracy** - Technically correct?
4. **Reusability** - Applicable beyond one project?
5. **Unique Value** - Not a duplicate?
6. **Safety** - No PII, secrets, or harmful content?

**Search for duplicates:**
- Checks existing BOK entries
- Reviews `master-index.yaml`
- Searches for similar patterns

---

#### Step 3: Decision

**Possible outcomes:**

| Decision | Meaning | Next Steps |
|----------|---------|------------|
| ✅ **ACCEPTED** | Pattern meets all standards | Integrated to BOK within hours |
| ⚠️ **REVISION REQUESTED** | Minor issues (formatting, missing metadata) | Fix issues, resubmit |
| ❌ **SOFT REJECT** | Needs significant work (incomplete, unclear) | Address feedback, resubmit allowed |
| 🚫 **HARD REJECT** | Duplicate, off-topic, or violates safety | Cannot resubmit without major changes |

---

#### Step 4: Integration (If Accepted)

**Librarian actions:**
1. **Determines BOK location** based on category:
   - `bok/patterns/` - General patterns
   - `bok/anti-patterns/` - Things to avoid
   - `bok/processes/` - Workflows and procedures
   - `bok/platforms/` - Platform-specific solutions
   - `bok/methodologies/` - Development approaches
   - `bok/governance/` - Governance and philosophy

2. **Creates file** in BOK with proper naming:
   ```
   bok/patterns/collaboration/multi-agent-git-workflow.md
   ```

3. **Updates master-index.yaml** with full metadata for search

4. **Archives intake** - Moves your submission to `processed/` or removes

5. **Notifies you** - SYNC message or PR comment confirming integration

---

#### Step 5: Pattern Goes Live

**Your pattern is now:**
- ✅ Searchable via `deia librarian query`
- ✅ Discoverable in BOK directory structure
- ✅ Referenced by other patterns
- ✅ Available to entire community

---

### Review Timeline

**Quick review (most patterns):**
- Submission → Claimed: **24 hours**
- Review → Decision: **24-48 hours**
- Acceptance → Integration: **Same day**
- **Total: 1-3 days**

**Revision needed:**
- Revision request → Your fix: **Variable (your timeline)**
- Resubmit → Re-review: **24 hours**
- **Total: 3-7 days**

**Complex patterns:**
- Deep technical review needed
- Multiple rounds of feedback
- **Total: 1-2 weeks**

---

### Feedback Format

If revisions are requested, you'll receive a `REVIEW-FEEDBACK.md` file:

```markdown
# Review Feedback

**Submission:** Pattern: Your Pattern Name
**Reviewer:** CLAUDE-CODE-004
**Date:** 2025-10-18
**Decision:** SOFT REJECT - Revision Requested

## Issues Found

1. **Missing Context** - Pattern assumes Redis but doesn't specify.
   Please clarify which caching system or make cache-agnostic.

2. **Incomplete Examples** - Code snippets are fragments.
   Please provide complete, runnable examples.

3. **No Confidence Level** - Is this Experimental, Validated, or Proven?
   Please add to MANIFEST.md.

## Suggested Improvements

1. Add "Applicable Systems" section
2. Provide before/after code examples
3. Include test results or metrics
4. Add confidence level to frontmatter

## Resubmission

Please address these issues and resubmit. We're happy to accept once complete!

## Related Patterns

- `bok/patterns/caching/cache-aside-pattern.md` - Useful reference

**Contact:** Via .deia/tunnel/ SYNC messages or PR comments
```

---

## Examples

### Example 1: Simple Process Pattern ✅

**Good:** Clear, actionable, reusable

```markdown
---
title: "Pattern: Daily Standup for AI Agents"
tags:
  - coordination
  - multi-agent
  - process
  - communication
urgency: medium
platforms:
  - Platform-Agnostic
audience:
  - developers
  - project-managers
date_added: 2025-10-18
contributors:
  - CLAUDE-CODE-001
status: active
version: 1.0
---

# Pattern: Daily Standup for AI Agents

**Multi-agent projects need coordination to avoid duplicate work and conflicts.**

## Context

Use this pattern when:
- 3+ AI agents working simultaneously
- Risk of duplicate work or merge conflicts
- Need visibility into what each agent is doing

## Problem

Without coordination, agents:
- Work on duplicate tasks
- Create merge conflicts
- Don't know what others accomplished
- Can't identify blockers early

## Solution

Daily async standup via `.deia/tunnel/` messages:

### Each Agent Reports (once per day):

```markdown
# STANDUP: [Agent ID] - YYYY-MM-DD

**Yesterday:**
- Completed: [task 1]
- Completed: [task 2]

**Today:**
- Working on: [task 3]
- Blocked by: [issue] (if any)

**Blockers:**
- Need [resource] to continue
- Waiting on [other agent]

**Status:** [Green|Yellow|Red]
```

### Coordinator Reviews

- AGENT-001 reads all standups
- Identifies conflicts or blockers
- Reassigns work if needed
- Unblocks agents

## Benefits

- **70% reduction in duplicate work** (measured over 20 days)
- **Early blocker identification** (avg 4 hours sooner)
- **Clear accountability** (always know who's doing what)

## Testing

1. Each agent posts standup by 9 AM
2. Coordinator reviews by 10 AM
3. Conflicts resolved before noon

## Related Patterns

- [Multi-Agent Git Workflow](./multi-agent-git-workflow.md)
- [Task Assignment Protocol](../processes/task-assignment.md)

## Evidence

**Projects using this:**
- deiasolutions (Oct 2025)
- q33n platform (Oct 2025)

**Validation:** 20-day trial, tracked conflicts and duplicates
```

**Why this is good:**
- ✅ Clear problem and solution
- ✅ Actionable format (template provided)
- ✅ Evidence with metrics
- ✅ Reusable across projects
- ✅ Complete metadata

---

### Example 2: Platform-Specific Pattern ✅

**Good:** Solves specific platform issue

```markdown
---
title: "Platform-Specific: Netlify Hugo Version Lock"
tags:
  - netlify
  - hugo
  - deployment
  - versioning
urgency: high
platforms:
  - netlify
audience:
  - developers
  - devops
date_added: 2025-10-18
contributors:
  - CLAUDE-CODE-003
status: active
version: 1.0
confidence: Validated
---

# Platform-Specific: Netlify Hugo Version Lock

**Netlify may use outdated Hugo version causing build failures.**

## Context

Use this pattern when:
- Deploying Hugo site to Netlify
- Build works locally but fails on Netlify
- Error: "Hugo command not found" or version mismatch

## Problem

Netlify defaults to old Hugo version (0.54.0) which:
- Lacks modern Hugo features
- Causes template errors
- Creates build failures

## Solution

Lock Hugo version in `netlify.toml`:

```toml
[build]
  publish = "public"
  command = "hugo --gc --minify"

[build.environment]
  HUGO_VERSION = "0.120.4"  # Specify your version
  HUGO_ENV = "production"
  HUGO_ENABLEGITINFO = "true"

[context.production.environment]
  HUGO_VERSION = "0.120.4"
```

### Verification

```bash
# Check your local Hugo version
hugo version

# Add that version to netlify.toml
# Commit and push
git add netlify.toml
git commit -m "fix: Lock Hugo version for Netlify"
git push
```

## Testing

1. Trigger Netlify deploy
2. Check build log for: "Hugo Static Site Generator v0.120.4"
3. Verify site builds successfully

## Related Patterns

- [Netlify Environment Variables](./netlify-env-vars.md)

## Evidence

**Problem frequency:** 40% of Hugo+Netlify projects hit this
**Fix success rate:** 100% when correctly configured
**Source:** deiasolutions netlify-hugo-issue.md (Oct 2025)
```

**Why this is good:**
- ✅ Platform-specific (Netlify)
- ✅ Solves real, common problem
- ✅ Working code example
- ✅ Clear verification steps
- ✅ Evidence of validation

---

### Example 3: Anti-Pattern ⚠️

**Good:** Documents what NOT to do

```markdown
---
title: "Anti-Pattern: Hardcoding Secrets in Code"
tags:
  - security
  - secrets
  - anti-pattern
  - credentials
urgency: critical
platforms:
  - Platform-Agnostic
audience:
  - developers
date_added: 2025-10-18
contributors:
  - Security Team
status: active
version: 1.0
---

# Anti-Pattern: Hardcoding Secrets in Code

**Never commit API keys, passwords, or tokens to source control.**

## Why This is Bad

**Security risks:**
- ❌ Secrets visible to anyone with repo access
- ❌ Exposed in git history forever (even if deleted later)
- ❌ Leaked on GitHub = compromised credentials
- ❌ Compliance violations (GDPR, SOC2, etc.)

**Real incidents:**
- 100,000+ secrets leaked on GitHub daily
- Average cost of breach: $4.45M
- Credentials stolen within hours of commit

## What People Do (Wrong)

```python
# ❌ NEVER DO THIS
API_KEY = "sk_live_abc123def456..."
PASSWORD = "MySecretPass123"
DATABASE_URL = "postgres://user:pass@prod.db.com/app"

# Then commit to git
git commit -m "Added API integration"
```

## The Right Way

### Use Environment Variables

```python
# ✅ DO THIS
import os

API_KEY = os.environ.get("API_KEY")
PASSWORD = os.environ.get("PASSWORD")
DATABASE_URL = os.environ.get("DATABASE_URL")

if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### Store in .env (Never Commit)

Create `.env` file:
```bash
API_KEY=sk_live_abc123...
PASSWORD=MySecretPass123
DATABASE_URL=postgres://user:pass@prod.db.com/app
```

Add to `.gitignore`:
```
.env
.env.*
secrets.*
credentials.*
```

### Use Secrets Manager (Production)

```python
# AWS Secrets Manager
import boto3

secrets_client = boto3.client('secretsmanager')
response = secrets_client.get_secret_value(SecretId='prod/api-key')
API_KEY = response['SecretString']
```

## If You Already Did This

**Damage control:**
1. **Revoke credentials immediately** (generate new keys)
2. **Remove from git history:**
   ```bash
   # Use BFG Repo-Cleaner or git-filter-repo
   git filter-repo --path secrets.py --invert-paths
   ```
3. **Rotate all secrets**
4. **Add to .gitignore**
5. **Audit access logs** for unauthorized use

## Detection Tools

```bash
# Scan repo for secrets
pip install truffleHog
truffleHog --regex --entropy=True .

# Pre-commit hook
pip install detect-secrets
detect-secrets scan > .secrets.baseline
```

## Related Patterns

- [Environment Variable Management](../patterns/env-var-pattern.md)
- [Secrets Manager Integration](../patterns/secrets-manager.md)

## References

- [OWASP: Cryptographic Storage](https://owasp.org/www-project-top-ten/)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
```

**Why this is good:**
- ✅ Clear explanation of harm
- ✅ Real incident examples
- ✅ Shows wrong way AND right way
- ✅ Damage control steps
- ✅ Detection tools provided
- ✅ External references

---

### Common Mistakes to Avoid

**1. Too Specific - Not Reusable ❌**

```markdown
# Bad: Fix bug in Project X line 47

We had a problem in app.py line 47 where the loop didn't work.
Changed `for i in range(10)` to `for i in range(len(items))` and it fixed it.
```

**Problem:** No one else can use this. No context, no generalization.

**Fix:** Extract the reusable pattern:
- What category of bug? (Off-by-one error)
- When does this happen? (Hardcoded loop bounds)
- General solution? (Use `len()` or iterator)

---

**2. Missing Context - When to Use ❌**

```markdown
# Bad: Use Docker

Docker is great. Here's how to install Docker.

[Installation instructions...]
```

**Problem:** No explanation of WHEN or WHY to use Docker. Not a pattern, just instructions.

**Fix:** Add context:
- What problem does Docker solve?
- When should you use it vs alternatives?
- What are the tradeoffs?

---

**3. No Examples - Hard to Understand ❌**

```markdown
# Bad: Implement caching for performance

Caching improves performance. Add a cache to your functions.

Done!
```

**Problem:** No code, no specifics, can't actually implement this.

**Fix:** Provide working code examples:
- Before/after code
- Concrete use case
- Expected results

---

**4. Not Sanitized - PII Exposed ❌**

```markdown
# Bad: API Integration

Connect to our API at https://acmecorp-internal.com/api
Use API key: sk_live_abc123def456
Contact john.smith@acmecorp.com for access

My email: jane.doe@gmail.com
```

**Problem:** Real URLs, API keys, email addresses, company name.

**Fix:** Replace with placeholders:
- `https://api.example.com`
- `YOUR_API_KEY_HERE`
- `support@example.com`
- `AcmeCorp` or `<YOUR_COMPANY>`

---

**5. Duplicate - Already Exists ❌**

```markdown
# Bad: [Submits pattern identical to existing BOK entry]
```

**Problem:** Didn't search BOK first. Wasted time for submitter and reviewer.

**Fix:**
1. Search `bok/` directory
2. Query `deia librarian query <keywords>`
3. Check `master-index.yaml`
4. If similar pattern exists, reference it or propose enhancement

---

## Resources

### Reference Documents

**Master Librarian Specification:**
- Location: `.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md`
- Contains: Quality standards (Section 5), review workflow, indexing principles
- **Read this for detailed quality criteria**

**BOK README:**
- Location: `bok/README.md`
- Contains: BOK structure, categories, organization principles

**BOK Format Spec:**
- Location: `docs/bok-format-spec.md` (if exists)
- Contains: YAML frontmatter schema, formatting requirements

---

### Pattern Template

**Location:** `templates/pattern-template.md`

**Usage:**
```bash
# Copy template to start your pattern
cp templates/pattern-template.md my-new-pattern.md

# Edit with your content
code my-new-pattern.md
```

**Template includes:**
- Complete YAML frontmatter
- All recommended sections
- Quality checklist
- Formatting examples

---

### Existing Patterns (Examples)

Browse `bok/` directory for examples:

**Process patterns:**
- `bok/processes/` - Git workflows, review processes

**Platform-specific:**
- `bok/platforms/netlify/` - Netlify deployment patterns
- `bok/platforms/shells/` - Shell-specific workarounds

**Collaboration:**
- `bok/patterns/collaboration/` - Human-AI coordination

**Pick a pattern similar to yours and use it as a reference**

---

### Tools

**BOK Query (Search existing patterns):**
```bash
# Search by keyword
deia librarian query git collaboration

# Filter by category
deia librarian query --category "Anti-Pattern" security

# Filter by platform
deia librarian query --platform Windows unicode
```

**Master Index (Browse all patterns):**
- Location: `.deia/index/master-index.yaml`
- Contains: Metadata for all BOK entries with tags and summaries

**Pattern Validator (Coming in Phase 2):**
```bash
deia pattern validate my-pattern.md
deia pattern extract session-log.md
deia pattern add my-pattern.md
```

---

### Get Help

**Questions about submission?**
- Check this guide first
- Review Master Librarian Spec (Section 5 - Quality Standards)
- Look at existing patterns for examples

**Need clarification?**
- GitHub Issues (tag: `bok-submission-question`)
- SYNC message to Master Librarian via `.deia/tunnel/claude-to-claude/`
- Ask coordinator (AGENT-001) for guidance

**Found a problem with this guide?**
- Create issue with tag: `documentation`
- Or submit improvement via `.deia/intake/`

---

## Frequently Asked Questions

### General Questions

**Q: How long does review take?**

A: 24-48 hours for first review on active projects. Complex patterns may take longer. You'll receive feedback either way.

---

**Q: Can I submit multiple patterns at once?**

A: Yes, but we recommend 1-3 at a time. Submitting 20 patterns at once overwhelms reviewers and may result in slower reviews or rejections. Quality over quantity.

---

**Q: What if my pattern is rejected?**

A: You'll receive detailed feedback explaining why. For "soft rejects" (needs work), you can address issues and resubmit. For "hard rejects" (duplicate or off-topic), the feedback will guide you to alternatives.

---

**Q: Can I update a pattern after it's accepted?**

A: Yes! Submit an updated version to `.deia/intake/` with a note that it's an update. Or create a PR with the changes. Include reason for update and increment version number.

---

**Q: Who owns submitted patterns?**

A: All BOK entries are **CC0-1.0 (Public Domain)** - freely usable by anyone. By submitting, you agree to this license. You'll be credited as a contributor.

---

### Writing Questions

**Q: How technical should my pattern be?**

A: Technical enough to implement, but clear enough for someone new to understand in 5 minutes. Assume reader knows programming basics but may not know your specific domain.

---

**Q: Do I need code examples?**

A: Not always, but highly recommended for technical patterns. Process patterns can use templates or workflow diagrams instead. The key is making it actionable.

---

**Q: How long should a pattern be?**

A: As long as needed to be complete and clear. Typical range:
- **Simple patterns:** 200-500 words
- **Complex patterns:** 500-1500 words
- **Anti-patterns:** 300-800 words

Quality and clarity matter more than length.

---

**Q: What if I don't have metrics or evidence?**

A: That's okay for new patterns! Mark confidence as "Experimental" and note that it's untested at scale. As people use it and validate, confidence can be upgraded.

---

**Q: Can I submit a pattern that's "in progress"?**

A: No. Submit only complete, working patterns. If you want feedback on an idea, create a GitHub issue first to discuss. The intake system is for ready-to-review submissions.

---

### Technical Questions

**Q: What format should code examples use?**

A: Use fenced code blocks with language hints:

````markdown
```python
def example():
    return "Use proper formatting"
```
````

Make examples runnable when possible. Include imports, full context.

---

**Q: Can I include images or diagrams?**

A: Yes! Include them in your intake submission. Use relative paths in markdown:

```markdown
![Architecture Diagram](./architecture.png)
```

Images should be:
- PNG or JPG format
- Reasonable size (<500 KB)
- Clear and readable
- Properly attributed if from external source

---

**Q: Should I use relative or absolute paths?**

A: **Relative paths** in pattern content:
```markdown
See also: [Related Pattern](./related-pattern.md)
```

Librarian will adjust paths during integration if needed.

---

**Q: What about external links?**

A: External links are fine for:
- Official documentation
- Academic papers
- Tool homepages

Avoid linking to:
- Paywalled content
- Temporary resources (may break)
- Internal/proprietary sites

---

### Process Questions

**Q: Can I claim a pattern idea to work on?**

A: Not in the intake system (it's for finished work). But you can:
1. Create GitHub issue: "Pattern idea: [Title]"
2. Announce in tunnel: "Working on pattern about X"
3. Submit when ready

This prevents duplicate work.

---

**Q: What if someone submits the same pattern while I'm writing?**

A: First submission gets priority. If yours adds unique value, you can submit as a variation or enhancement. Search intake before starting to avoid duplicates.

---

**Q: Do I need to update master-index.yaml?**

A: **No.** The Master Librarian handles indexing during integration. Just focus on your pattern content.

---

**Q: Can I submit patterns from closed-source projects?**

A: Yes, but you must:
1. Sanitize all proprietary information
2. Make the pattern general (not company-specific)
3. Ensure you have rights to share
4. Use placeholders for company-specific details

---

### Sanitization Questions

**Q: How do I know if I've removed all PII?**

A: Check for:
- Names (use `Jane Doe`, `<YOUR_NAME>`)
- Emails (use `user@example.com`)
- IP addresses (use `192.0.2.1` or `example.com`)
- URLs (use `https://example.com`)
- Geographic locations (use `Anytown, USA`)

When in doubt, replace with placeholder.

---

**Q: Are example usernames okay?**

A: Yes, if they're clearly generic:
- ✅ `john_doe`, `user123`, `alice`, `bob`
- ❌ `john.smith42` (could be real)

Make it obvious they're examples.

---

**Q: What about GitHub usernames?**

A: Your own GitHub username as contributor is fine. But redact others':
- ✅ `contributors: [octocat]` (your GitHub username)
- ❌ `Fixed bug reported by @real-github-user` (someone else's)

---

**Q: Can I mention company names?**

A: Depends:
- ✅ Public companies for context: "When using AWS Lambda..."
- ✅ Open source projects: "In PostgreSQL..."
- ❌ Your employer or client: "At AcmeCorp we..."
- ❌ Customer names: "This solved TechStartup's issue"

Use `<YOUR_COMPANY>`, `AcmeCorp`, or generic placeholders.

---

## Conclusion

You're now ready to submit high-quality patterns to the DEIA Body of Knowledge!

**Quick Recap:**

1. ✅ **Check quality standards** - Completeness, clarity, accuracy, reusability, unique value, safety
2. ✅ **Use the template** - `templates/pattern-template.md`
3. ✅ **Sanitize everything** - Remove PII, secrets, proprietary info
4. ✅ **Submit to intake** - `.deia/intake/YYYY-MM-DD/your-pattern/`
5. ✅ **Wait for review** - 1-2 days for feedback
6. ✅ **Address feedback** - If revision requested
7. ✅ **Pattern goes live** - Searchable and reusable by all

**Your contributions make the community stronger.** Every pattern you share saves someone else hours of work and builds our collective intelligence.

**Thank you for contributing!**

---

**Version:** 1.0
**Last Updated:** 2025-10-18
**Maintained By:** CLAUDE-CODE-002 (Documentation Systems Lead)
**Feedback:** Submit via `.deia/intake/` or GitHub Issues (tag: `documentation`)

---

**Related Guides:**
- [Conversation Logging Guide](./CONVERSATION-LOGGING-GUIDE.md)
- [BOK Usage Guide](./BOK-USAGE-GUIDE.md) (if exists)
- [Master Librarian Spec](../.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md)

---

*DEIA Project - Building collective intelligence through shared knowledge*
