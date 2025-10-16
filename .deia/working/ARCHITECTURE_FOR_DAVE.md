# DEIA Architecture - How This Actually Works

**Your questions answered with concrete workflows**

---

## The Three Entities (CLARIFIED)

### 1. Public DEIA (github.com/deiasolutions/deia)

**What:** The open-source product for the world
**Location:** GitHub (public repo)
**Contains:**
- Code (`src/deia/`)
- Community BOK (`bok/`)
- Documentation (`docs/`)
- Tools everyone uses

**You are:** Maintainer/Admin (reviews PRs, accepts contributions)

### 2. Dave's Local DEIA Admin Workspace (THIS repo)

**What:** Your private workspace for DEIA administration
**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions`
**Contains:**
- Everything in Public DEIA (your working copy)
- PLUS private areas:
  - `admin/` - Your admin deliberations (gitignored)
  - `.deia/` - Your DEIA usage logs (gitignored)
  - `project_resume.md` - Your session context (gitignored)

**You are:** Admin/Developer (make changes, push to public)

### 3. Dave's FBB Project (Using DEIA as end-user)

**What:** Your day job project (Family Bond Bot)
**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot` (or wherever it is)
**Contains:**
- Your FBB code
- `.deia/` directory with:
  - `sessions/` - FBB conversation logs
  - `logger.py` - Copy of DEIA logger
  - `START_HERE.md` - FBB-specific instructions for Claude
  - `intake/` - Patterns to potentially submit to DEIA

**You are:** End-user (log conversations, extract patterns, submit to DEIA)

---

## The Workflow (CONCRETE)

### Daily Work in FBB

```
┌─────────────────────────────────────┐
│ FBB Project (Day Job)               │
│ C:\...\familybondbot\               │
├─────────────────────────────────────┤
│                                     │
│ Claude Code session starts          │
│ ↓                                   │
│ Reads: .claude/START_HERE.md        │
│ (FBB-specific context)              │
│ ↓                                   │
│ You work on FBB features            │
│ ↓                                   │
│ Claude auto-logs conversation       │
│ → .deia/sessions/YYYYMMDD-*.md      │
│ ↓                                   │
│ Session ends                        │
│                                     │
└─────────────────────────────────────┘
         │
         │ Found something useful?
         ↓
┌─────────────────────────────────────┐
│ Extract Pattern                     │
├─────────────────────────────────────┤
│                                     │
│ You: "Claude, extract that pattern  │
│       to .deia/intake/"             │
│ ↓                                   │
│ Claude creates:                     │
│ .deia/intake/fbb_pattern_X.md       │
│ (sanitized, ready for review)       │
│                                     │
└─────────────────────────────────────┘
         │
         │ Manual copy
         ↓
┌─────────────────────────────────────┐
│ DEIA Admin Workspace                │
│ C:\...\deiasolutions\               │
├─────────────────────────────────────┤
│                                     │
│ You copy:                           │
│ fbb_pattern_X.md                    │
│ → admin/deliberations/              │
│ ↓                                   │
│ You review as DEIA Admin            │
│ ↓                                   │
│ Accept? → Copy to bok/patterns/     │
│ Reject? → Explain why in admin/     │
│ ↓                                   │
│ git add bok/patterns/X.md           │
│ git commit -m "Add pattern: X"      │
│ git push origin master              │
│                                     │
└─────────────────────────────────────┘
         │
         │ Pushed to GitHub
         ↓
┌─────────────────────────────────────┐
│ Public DEIA                         │
│ github.com/deiasolutions/deia       │
├─────────────────────────────────────┤
│                                     │
│ Community can now:                  │
│ - See pattern X                     │
│ - Use pattern X                     │
│ - Submit their own patterns         │
│                                     │
└─────────────────────────────────────┘
```

---

## File Structure (WHERE THINGS GO)

### FBB Project Structure

```
C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\
├── .claude/
│   └── START_HERE.md              # FBB-specific instructions
│                                  # "You're working on Family Bond Bot..."
│                                  # "Use these coding standards..."
│                                  # "Log all conversations to .deia/"
│
├── .deia/                         # FBB's DEIA workspace (gitignored)
│   ├── logger.py                  # Copy of DEIA logger
│   ├── sessions/                  # FBB conversation logs
│   │   ├── INDEX.md
│   │   ├── 20251006-143000-feature-xyz.md
│   │   └── 20251007-091500-bugfix-auth.md
│   └── intake/                    # Patterns ready for DEIA submission
│       ├── fbb_pattern_auth-flow.md
│       └── fbb_pattern_db-migration.md
│
├── src/                           # Your FBB code
├── tests/                         # Your FBB tests
└── README.md                      # FBB project readme
```

### DEIA Admin Workspace Structure

```
C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\
├── bok/                           # PUBLIC: Community patterns
│   ├── patterns/
│   ├── platforms/
│   └── anti-patterns/
│
├── src/deia/                      # PUBLIC: DEIA tools
│   ├── logger.py                  # Source of truth for logger
│   ├── cli.py
│   └── ...
│
├── docs/                          # PUBLIC: Documentation
│
├── admin/                         # PRIVATE: Your admin workspace
│   ├── deliberations/             # Review submissions here
│   │   ├── fbb_pattern_auth-flow.md  (copy from FBB intake)
│   │   └── review-notes.md
│   ├── constitutional-review/     # Big governance decisions
│   └── pending-decisions/         # What you're thinking about
│
├── .deia/                         # PRIVATE: Your DEIA usage
│   ├── sessions/                  # Your DEIA admin conversations
│   └── working/
│       ├── decisions.md
│       ├── ideas.md
│       └── resume-instructions.md
│
├── project_resume.md              # PRIVATE: Your session context
│
└── .gitignore                     # Ignores: admin/, .deia/, project_resume.md
```

---

## The Answer to Your Specific Questions

### Q: "Am I supposed to use deia.py as a service running on my machine?"

**A: NO.** Not a service. Just a Python file you copy to each project.

**In FBB:**
```bash
# One-time setup
cp C:\...\deiasolutions\src\deia\logger.py C:\...\familybondbot\.deia\logger.py
```

**Then in FBB sessions:**
```python
# Claude runs this automatically (or you do manually)
from .deia.logger import quick_log
quick_log('context', 'transcript')
```

### Q: "Am I supposed to have a deia.md file that my FBB claude code references?"

**A: YES.** In FBB's `.claude/START_HERE.md`:

```markdown
# Instructions for Claude Code in FBB Project

You are working on Family Bond Bot.

## Conversation Logging (REQUIRED)

At the end of every session, log the conversation:

```python
from .deia.logger import quick_log
quick_log(
    context='What we worked on',
    transcript='Full conversation',
    decisions=['Key decisions'],
    action_items=['What was done'],
    files_modified=['files.py']
)
```

Logs go to `.deia/sessions/` (private, gitignored).

## Coding Standards

[Your FBB-specific coding standards here]

## Project Context

[FBB-specific project info here]
```

### Q: "Or a .deia directory inside my FBB project that I instruct claude code to run?"

**A: YES.** `.deia/` directory in FBB contains:
- `logger.py` (copied from deiasolutions)
- `sessions/` (conversation logs)
- `intake/` (patterns ready for submission)

**Claude doesn't "run" it automatically.** You (or Claude) explicitly call:
```python
python .deia/logger.py
```

Or better, in `.claude/START_HERE.md`, instruct Claude to log at end of session.

### Q: "Does my LOCAL version of DEIA know about autologging?"

**A: Two separate things:**

1. **FBB's conversation logs** → Stored in `familybondbot/.deia/sessions/`
2. **DEIA admin conversation logs** → Stored in `deiasolutions/.deia/sessions/`

**They don't sync automatically.** They're separate projects.

**If FBB Claude learned about autologging:**
- That knowledge is in FBB's conversation logs
- To share with DEIA: Extract pattern from FBB log → Submit to DEIA

### Q: "Has my LOCAL version of DEIA pushed that as a PR to PUBLIC DEIA?"

**A: NO.** Nothing automatic. Here's the manual workflow:

```bash
# 1. In FBB, find pattern in conversation log
cat familybondbot/.deia/sessions/20251006-*.md

# 2. Extract pattern
# Claude creates: familybondbot/.deia/intake/fbb_pattern_autologging.md

# 3. You (as DEIA admin) copy it
cp familybondbot/.deia/intake/fbb_pattern_autologging.md \
   deiasolutions/admin/deliberations/

# 4. Review in DEIA admin workspace
cd deiasolutions
# Read, sanitize, decide

# 5. Accept → Add to BOK
cp admin/deliberations/fbb_pattern_autologging.md \
   bok/patterns/collaboration/auto-logging.md

# 6. Push to public GitHub
git add bok/patterns/collaboration/auto-logging.md
git commit -m "Add pattern: Automatic conversation logging"
git push origin master
```

**Future:** Could automate this workflow, but for now it's manual.

---

## Proposed Workflow (SIMPLIFIED)

### Setup (One-Time Per Project)

**In each project (FBB, future projects):**

```bash
cd /path/to/project
mkdir -p .deia/sessions .deia/intake
cp /path/to/deiasolutions/src/deia/logger.py .deia/logger.py
echo ".deia/" >> .gitignore
```

**Create `.claude/START_HERE.md`:**
```markdown
# [Project Name] - Instructions for Claude Code

## Required: Log Every Session

At end of session:
```python
from .deia.logger import quick_log
quick_log('what we did', 'conversation transcript')
```

## Project-Specific Instructions
[Your stuff here]
```

### Daily Work

**1. Work in FBB with Claude Code**
- Claude reads `.claude/START_HERE.md` on startup
- You work on features
- At end of session, log conversation (manually or via START_HERE instruction)

**2. Review logs occasionally**
```bash
# In FBB
cat .deia/sessions/INDEX.md
```

**3. Extract useful patterns**
```
You: "Claude, that authentication pattern is useful. Extract it to .deia/intake/fbb_pattern_auth.md"
Claude: Creates sanitized pattern file
```

**4. Submit to DEIA (weekly? monthly?)**
```bash
# Switch to DEIA admin workspace
cd deiasolutions

# Copy pattern from FBB
cp ../familybondbot/.deia/intake/fbb_pattern_auth.md \
   admin/deliberations/

# Review as admin
# Accept → Copy to bok/
# Push to GitHub
```

---

## What Needs to Happen Right Now

### 1. Push DEIA to GitHub (PUBLIC)

```bash
cd deiasolutions
git status  # Verify only public files
git add -A
git commit -m "Initial public release: Conversation logging + BOK"
git remote add origin https://github.com/deiasolutions/deia.git
git push -u origin master
```

### 2. Set Up FBB with DEIA (YOUR END-USER INSTANCE)

```bash
cd /path/to/familybondbot

# Create DEIA workspace
mkdir -p .deia/sessions .deia/intake

# Copy logger
cp /path/to/deiasolutions/src/deia/logger.py .deia/logger.py

# Add to gitignore
echo ".deia/" >> .gitignore

# Create START_HERE for FBB Claude
cat > .claude/START_HERE.md << 'EOF'
# Family Bond Bot - Instructions for Claude Code

You are working on Family Bond Bot, a visitation scheduling platform.

## REQUIRED: Log Every Session

At the end of EVERY session, log the conversation:

```python
import sys
sys.path.insert(0, '.deia')
from logger import quick_log

quick_log(
    context='Brief description of what we worked on',
    transcript='[Full conversation - paste or reference]',
    decisions=['Key decision 1', 'Key decision 2'],
    action_items=['What was completed', 'What is pending'],
    files_modified=['file1.py', 'file2.md']
)
```

This creates: `.deia/sessions/YYYYMMDD-HHMMSS-conversation.md`

## FBB Coding Standards
[Your coding standards here]

## Project Context
[FBB-specific context here]
EOF
```

### 3. Test Logging in FBB

Open Claude Code in FBB project:
```
Claude, read .claude/START_HERE.md and log this conversation.
```

Verify:
```bash
ls .deia/sessions/
cat .deia/sessions/INDEX.md
```

---

## Future Automation (v2.0)

**What could be automated:**
1. Auto-log every conversation (no manual trigger)
2. Auto-extract patterns (Claude suggests, you approve)
3. Auto-submit to DEIA (creates PR automatically)
4. Sync `.claude/START_HERE.md` across projects

**For now:** Manual workflow. Proven first, automate later.

---

## Summary

**Three separate repos:**
1. **Public DEIA** (GitHub) - Community uses
2. **DEIA Admin** (local deiasolutions) - You develop/maintain
3. **FBB Project** (local familybondbot) - You use as end-user

**Workflow:**
1. Work in FBB → Log conversations → Extract patterns
2. Switch to DEIA admin → Review → Accept → Push to GitHub
3. Community pulls → Uses patterns → Submits their own

**No service running. No automatic syncing. Manual workflow. Simple.**

---

## Next Steps

1. ✅ Push deiasolutions to GitHub (makes Public DEIA)
2. ✅ Set up FBB with `.deia/` and `.claude/START_HERE.md`
3. ✅ Test logging in FBB
4. ⏸️ Continue FBB work (logs accumulate)
5. ⏸️ Weekly: Review FBB logs, extract patterns, submit to DEIA

**Want me to create the FBB setup files now?**
