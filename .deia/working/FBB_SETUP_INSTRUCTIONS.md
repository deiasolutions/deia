# FBB Setup Instructions - For Claude Code

**Give this file to Claude in your FBB project**

---

## Instructions for Claude

Dave wants to set up DEIA conversation logging in the Family Bond Bot (FBB) project.

**What to do:**

### Step 1: Find FBB Location

Ask Dave:
```
What's the full path to your Family Bond Bot project?
```

Once you have it (e.g., `C:\Users\davee\...\familybondbot`), proceed.

### Step 2: Create DEIA Workspace

```bash
cd /path/to/familybondbot

# Create DEIA directories
mkdir -p .deia/sessions
mkdir -p .deia/intake
mkdir -p .deia/patterns_drafts

# Confirm to Dave
echo "✓ Created .deia/ workspace structure"
```

### Step 3: Copy DEIA Logger

```bash
# Copy logger from DEIA repo
cp C:/Users/davee/OneDrive/Documents/GitHub/deiasolutions/src/deia/logger.py .deia/logger.py

# Verify it copied
ls -lh .deia/logger.py

echo "✓ Copied DEIA logger (350+ lines)"
```

### Step 4: Update .gitignore

```bash
# Check if .gitignore exists
if [ ! -f .gitignore ]; then
  echo "# FBB gitignore" > .gitignore
fi

# Add DEIA workspace to gitignore
echo "" >> .gitignore
echo "# DEIA workspace (conversation logs, private)" >> .gitignore
echo ".deia/" >> .gitignore

echo "✓ Updated .gitignore to exclude .deia/"
```

### Step 5: Create .claude/START_HERE.md

Ask Dave first:
```
What tech stack does FBB use? (Python/Django? Node/React? Other?)
What are the key files/directories in FBB I should know about?
```

Then create `.claude/START_HERE.md` with this template (customize based on Dave's answers):

```markdown
# Family Bond Bot - Instructions for Claude Code

**Project:** Family Bond Bot - Visitation scheduling platform
**Tech Stack:** [FILL IN FROM DAVE: Python/Django? Node/React?]
**Purpose:** Help parents coordinate child visitation schedules

---

## 🔴 REQUIRED: Log Every Session

**At the end of EVERY conversation, run:**

```python
import sys
sys.path.insert(0, '.deia')
from logger import quick_log

quick_log(
    context='Brief description of what we worked on',
    transcript='Key decisions and work done this session',
    decisions=['Decision 1', 'Decision 2'],
    action_items=['Completed: X', 'Pending: Y'],
    files_modified=['file1.py', 'file2.js']
)
```

**Or use the slash command (if available):**
```
/log-conversation
```

**Result:**
- Log saved to `.deia/sessions/YYYYMMDD-HHMMSS-conversation.md`
- Index updated in `.deia/sessions/INDEX.md`
- If crash: Read latest log to recover context

---

## Project Context

### What FBB Does
[FILL IN: Brief description of FBB's purpose and features]

### Key Directories
[FILL IN FROM DAVE:
- src/ - ?
- tests/ - ?
- frontend/ - ?
- etc.]

### Important Files
[FILL IN:
- Key configuration files
- Entry points
- Important modules]

---

## Coding Standards

### Style
[FILL IN FROM DAVE:
- Python: PEP 8? Black? Ruff?
- JavaScript: ESLint? Prettier?
- Other preferences?]

### Testing
[FILL IN:
- Test framework (pytest? jest? other?)
- When to write tests
- How to run tests]

### Git Workflow
[FILL IN:
- Branch naming
- Commit message format
- PR process]

---

## Common Commands

### Development
```bash
[FILL IN: How to run dev server]
```

### Testing
```bash
[FILL IN: How to run tests]
```

### Database
```bash
[FILL IN: Migrations, seeds, etc.]
```

---

## Current Work

### Active Features
[Dave will update this as work progresses]

### Known Issues
[Track issues here]

### Next Priorities
[What to work on next]

---

## DEIA Integration

### Conversation Logging
- Logs stored in `.deia/sessions/` (gitignored, private)
- Use `/log-conversation` or Python API
- Recovery: Read `.deia/sessions/INDEX.md` after crash

### Pattern Extraction
If you discover something worth sharing with DEIA community:

```
"Claude, that pattern looks useful. Extract it to .deia/intake/ for potential DEIA submission"
```

You'll create a sanitized pattern file that Dave can review and submit.

---

**Remember: Log EVERY session. Context is precious. Never lose work again.**
```

Save this to: `.claude/START_HERE.md`

### Step 6: Create Initial Session Index

```bash
cd .deia/sessions

# Create initial INDEX.md
cat > INDEX.md << 'EOF'
# FBB Session Index

**All Claude Code conversations logged here**

---

## Sessions

[Sessions will be added automatically when you log conversations]
EOF

echo "✓ Created .deia/sessions/INDEX.md"
```

### Step 7: Test Logging

```python
# Test the logger
import sys
sys.path.insert(0, '.deia')
from logger import quick_log

log_file = quick_log(
    context='DEIA setup in FBB project',
    transcript='Set up DEIA conversation logging in Family Bond Bot',
    decisions=['Use DEIA for conversation logging', 'Store logs in .deia/sessions/'],
    action_items=[
        'Created .deia/ workspace structure',
        'Copied logger.py from DEIA repo',
        'Created .claude/START_HERE.md',
        'Updated .gitignore'
    ],
    files_modified=[
        '.deia/logger.py (copied from DEIA)',
        '.claude/START_HERE.md (created)',
        '.gitignore (updated)'
    ]
)

print(f"✓ Test log created: {log_file}")
print(f"✓ Check .deia/sessions/INDEX.md to verify")
```

### Step 8: Verify Setup

```bash
# Check everything was created
ls -la .deia/
ls -la .deia/sessions/
ls -la .claude/

# Verify .gitignore
cat .gitignore | grep ".deia"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ DEIA Setup Complete in FBB"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "What was created:"
echo "  • .deia/ workspace (gitignored)"
echo "  • .deia/logger.py (conversation logger)"
echo "  • .deia/sessions/ (log storage)"
echo "  • .claude/START_HERE.md (Claude instructions)"
echo ""
echo "Next steps:"
echo "  1. Customize .claude/START_HERE.md with FBB details"
echo "  2. Start working on FBB features"
echo "  3. Log every session with /log-conversation"
echo ""
echo "If crash: cat .deia/sessions/INDEX.md → read latest log"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

### Step 9: Tell Dave

```
Dave, DEIA is set up in FBB!

Created:
  ✓ .deia/ workspace (gitignored)
  ✓ .deia/logger.py (copied from DEIA repo)
  ✓ .deia/sessions/ (for conversation logs)
  ✓ .claude/START_HERE.md (needs customization)
  ✓ .gitignore updated

Next:
  1. Review and customize .claude/START_HERE.md with FBB-specific info
  2. Start working on FBB features
  3. Use /log-conversation at end of every session

Your conversations will be logged automatically. If computer crashes, read .deia/sessions/INDEX.md to find and resume from latest log.

Ready to continue FBB work?
```

---

## GLOBAL vs LOCAL DEIA

### What This Setup Does

**GLOBAL DEIA (from GitHub):**
- `logger.py` is copied from `deiasolutions/src/deia/logger.py`
- This is the "latest version" from the public repo
- When DEIA updates, you copy the new version to FBB

**LOCAL OPTIONS (FBB-specific):**
- `.claude/START_HERE.md` - Your FBB-specific instructions
- `.deia/sessions/` - Your FBB conversation logs (private)
- `.deia/intake/` - FBB patterns ready for submission to DEIA
- `.deia/config.json` - FBB-specific DEIA settings (future)

**How updates work:**
```bash
# When DEIA releases new logger version:
cd /path/to/familybondbot
cp /path/to/deiasolutions/src/deia/logger.py .deia/logger.py

# Your local logs/config stay intact
# Only the logger code updates
```

### Future: `deia init` Command

Eventually, Dave will implement:
```bash
cd /path/to/any-project
deia init --from-github deiasolutions/deia

# This will:
# - Download latest DEIA tools
# - Create .deia/ structure
# - Create .claude/START_HERE.md template
# - Configure .gitignore
# - One command, automatic
```

But for now, manual setup as described above works perfectly.

---

## Notes for Dave

**To give this to FBB Claude:**

1. Open Claude Code in FBB project
2. Paste this message:

```
Read this file and execute the setup:
C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\FBB_SETUP_INSTRUCTIONS.md

After setup, ask me for FBB-specific details to customize .claude/START_HERE.md
```

3. Claude will execute all steps
4. Claude will ask you for FBB details (tech stack, directories, etc.)
5. Claude will customize START_HERE.md
6. Test logging
7. Done!

**Time:** 5-10 minutes total

---

## Troubleshooting

**If logger.py copy fails:**
```bash
# Find DEIA repo location
find ~ -name "deiasolutions" -type d 2>/dev/null

# Or manually specify path:
cp /full/path/to/deiasolutions/src/deia/logger.py .deia/logger.py
```

**If import fails:**
```python
# Make sure path is correct:
import sys
sys.path.insert(0, '.deia')  # Relative to project root
from logger import quick_log
```

**If .gitignore append duplicates:**
```bash
# Check if already there:
grep ".deia" .gitignore

# If yes, don't append again
```

---

**This setup gives FBB the GLOBAL DEIA logger + LOCAL customization.**
