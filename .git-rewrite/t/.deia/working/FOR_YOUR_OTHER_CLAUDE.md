# Instructions for Claude in Other Projects

**From Dave:** Read this to understand how to contribute to DEIA and log conversations.

---

## What is DEIA?

**DEIA = Development Evidence & Insights Automation**

A system for:
1. **Logging conversations** with Claude Code (insurance against crashes)
2. **Capturing patterns** from AI-assisted work
3. **Sharing knowledge** with the community (privacy-preserving)

**Why:** Claude Code doesn't save conversation history. Crashes lose everything. DEIA fixes that.

---

## Priority 1: Log Your Conversations (DO THIS NOW)

### Setup (One-Time)

```bash
# In your project directory
mkdir -p .deia/sessions
touch .deia/sessions/INDEX.md
```

Add to `.gitignore`:
```
.deia/
```

### Every Session: Log It

**Method 1: Copy the logger (fastest)**

Copy from Dave's deiasolutions repo:
```bash
# Copy logger to your project
cp path/to/deiasolutions/src/deia/logger.py .deia/logger.py
```

**Method 2: Use it directly**

```bash
# From your project directory
python -c "
import sys
sys.path.append('path/to/deiasolutions/src')
from deia.logger import quick_log

quick_log(
    context='What you worked on',
    transcript='Your full conversation here',
    decisions=['Decision 1', 'Decision 2'],
    action_items=['Did X', 'Did Y'],
    files_modified=['file1.py', 'file2.md'],
    next_steps='What to do next'
)
"
```

**Method 3: Manual (if Python fails)**

Create: `.deia/sessions/YYYYMMDD-HHMMSS-conversation.md`

```markdown
# Conversation Log

**Date:** 2025-10-06T12:00:00
**Context:** What you worked on

## Transcript
[Paste entire conversation here]

## Key Decisions
- Decision 1
- Decision 2

## Files Modified
- file1.py
- file2.md

## Next Steps
What to do next session
```

### Why This Matters

**Before logging:**
- Computer crashes → lose all context → waste hours

**After logging:**
- Computer crashes → read `.deia/sessions/latest.md` → resume immediately

**Dave's rule:** Log EVERY non-trivial conversation. Claude Code is unusable without this.

---

## How to Contribute to DEIA

### Step 1: Identify Shareable Patterns

**What's shareable:**
- ✅ General patterns ("Test before asking human to test")
- ✅ Platform workarounds (Railway HTTPS redirect fix)
- ✅ Anti-patterns ("Don't auto-deploy to production")
- ✅ Collaboration strategies (AI decision frameworks)

**What's NOT shareable:**
- ❌ Your business logic
- ❌ Client-specific code
- ❌ Proprietary algorithms
- ❌ API keys, secrets, credentials
- ❌ PII (names, emails, personal info)

### Step 2: Extract Pattern from Log

Review your conversation logs:
```bash
ls .deia/sessions/*.md
```

Found something valuable? Extract it.

**Template:**
```markdown
---
id: unique-identifier
date: 2025-10-06
platform: claude-code
category: pattern
confidence: validated
sources: 1
---

# Pattern: [Name]

## Problem
What problem does this solve?

## Solution
How to solve it

## Context
When to use this

## Example
Code or conversation example

## Related
Links to other patterns
```

### Step 3: Sanitize

**Before sharing anything:**

1. **Remove PII:**
   - Names → `[Name]` or `User`
   - Emails → `[email]`
   - Company names → `Company X`
   - Locations → `[City]`

2. **Remove secrets:**
   - API keys → `[REDACTED]`
   - Passwords → `[REDACTED]`
   - Tokens → `[REDACTED]`
   - Internal URLs → `example.com`

3. **Remove IP:**
   - Proprietary algorithms → Describe generally
   - Business logic → Extract universal pattern only
   - Client code → Use generic examples

**Tool (if available):**
```bash
deia sanitize conversation.md
# Manual review still required!
```

### Step 4: Submit to Dave

**Option A: Via intake directory** (preferred if you have access)

```bash
# Copy sanitized pattern to Dave's intake
cp sanitized-pattern.md path/to/deiasolutions/.deia/intake/yourproject_pattern-name_YYYY-MM-DD.md
```

**Option B: Via email/message**

Send sanitized pattern to Dave with:
- Subject: "DEIA Submission: [Pattern Name]"
- Attachment: Sanitized markdown file
- Note: Which project it's from

**Option C: GitHub PR** (once public repo exists)

```bash
# Fork deiasolutions/deia
# Add pattern to bok/patterns/[category]/
# Create PR
```

### Step 5: Dave Reviews

Dave will:
1. Review for privacy/security
2. Verify pattern is universal
3. Accept → add to BOK
4. Reject → explain why (might need more sanitization)

---

## Submission Naming Convention

**Format:** `projectname_type_brief-description_YYYY-MM-DD.md`

**Examples:**
- `familybondbot_pattern_test-before-asking_2025-10-06.md`
- `familybondbot_antipattern_autonomous-deployment_2025-10-06.md`
- `myapp_platform-railway_https-redirect_2025-10-06.md`

**Types:**
- `pattern` - General best practice
- `antipattern` - What NOT to do
- `platform-[name]` - Platform-specific workaround
- `session-log` - Full conversation log (for review, not BOK)

---

## Current DEIA Status

**What works now:**
- ✅ Conversation logging (fully functional)
- ✅ Manual submission via intake directory
- ✅ BOK structure defined
- ✅ Sanitization guide available

**Coming soon:**
- 🔄 Public GitHub repo
- 🔄 Automated sanitization tool
- 🔄 Direct PR submission workflow
- 🔄 Community BOK search

---

## Quick Reference Commands

### Log Conversation (Python)
```python
from deia.logger import quick_log
quick_log('context', 'transcript', decisions=[], action_items=[], files_modified=[])
```

### Log Conversation (Bash)
```bash
python path/to/deiasolutions/src/deia/logger.py
# Follow prompts
```

### Check Logs
```bash
cat .deia/sessions/INDEX.md
```

### Latest Log
```bash
ls -t .deia/sessions/*.md | head -1 | xargs cat
```

---

## Files You Need

**Essential:**
1. `path/to/deiasolutions/src/deia/logger.py` - Copy to your project
2. `path/to/deiasolutions/docs/conversation-logging.md` - Full logging guide
3. `path/to/deiasolutions/docs/sanitization-guide.md` - Sanitization rules
4. This file - Keep as reference

**Optional:**
- `CONVERSATION_LOGGING_QUICKSTART.md` - Quick logging reference
- `docs/sanitization-workflow.md` - Step-by-step sanitization

---

## Emergency: Computer About to Crash

**SAVE NOW:**

```bash
# Quick log current conversation
python -c "from deia.logger import quick_log; quick_log('CRASH IMMINENT', 'SEE RAW LOGS', decisions=['None'], action_items=['Log before crash'], files_modified=['None'])"

# Or just dump to file
echo "[CONVERSATION TRANSCRIPT PASTE HERE]" > .deia/sessions/emergency-$(date +%Y%m%d-%H%M%S).md
```

**Then:** Copy `.deia/sessions/` to safe location (USB, cloud, etc.)

---

## Philosophy

**Dave's perspective:**

> "I'm paying $100/month for Claude Code and it can't remember context session to session. Crashes happen. Claude Code is UNUSABLE without conversation logging. This isn't optional - it's a requirement for the tool to be viable."

**DEIA's purpose:**

1. **Primary:** Insurance against data loss (conversation logging)
2. **Secondary:** Share what we learn (BOK contributions)
3. **Long-term:** Build collective intelligence for AI collaboration

**Your responsibility:**

- Log your conversations (for yourself)
- Share patterns (for community)
- Protect privacy (for everyone)

---

## Questions?

**Check:**
1. `docs/conversation-logging.md` - Logging details
2. `docs/sanitization-guide.md` - Privacy rules
3. `.deia/working/decisions.md` - Open questions (Dave's workspace)

**Or:** Ask Dave directly

---

## Status of Public DEIA

**Current:** Local repo only (Dave's machine)
**Next:** Public GitHub repo (coming soon)
**Future:** pip install deia, full automation

**For now:** Manual process, Dave reviews everything

---

**Your mission:**
1. Log every conversation
2. Extract valuable patterns
3. Sanitize and submit
4. Help build the BOK

**Never lose context again.**
