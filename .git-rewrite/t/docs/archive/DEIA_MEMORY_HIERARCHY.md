# DEIA Memory Hierarchy Guide

**How DEIA works with Claude Code's four memory levels**

---

## Claude Code Memory Hierarchy

Claude Code loads memories in this order (lowest to highest precedence):

1. **Enterprise** - Organization-wide (managed by IT)
2. **User** - Personal (all your projects)
3. **Team** - Shared with team (committed to repo)
4. **Project** - Project-specific (`.claude/`)

**Higher levels override lower levels.**

---

## DEIA at Each Level

### 1. Enterprise Level (Organization-Wide)

**Location:**
- macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
- Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md` (likely)
- Linux: `/etc/ClaudeCode/CLAUDE.md` (likely)

**When to use:**
- Organization mandates DEIA usage
- Centrally managed by IT/admin
- Applies to all users

**Setup (Admin only):**
```bash
# Copy DEIA memory to enterprise location
sudo cp .claude/preferences/deia.md "/Library/Application Support/ClaudeCode/CLAUDE.md"
```

**Behavior:**
- ALL users in organization get DEIA
- Users can override with personal/project settings
- Lowest precedence (easily overridden)

---

### 2. User Level (Personal - Recommended for Individuals)

**Location:** `~/.claude/CLAUDE.md`

**When to use:**
- You use DEIA across multiple personal projects
- Want automatic detection
- Don't want to set up per-project

**Setup:**
```bash
# Copy DEIA memory to user location
mkdir -p ~/.claude
cp .claude/preferences/deia.md ~/.claude/CLAUDE.md
```

**Or use # memory:**
```
# deia-user
[Paste content from .claude/preferences/deia.md]
```

**Behavior:**
- Applies to ALL your projects
- Checks for `.deia/` directory (only activates if present)
- Overrides enterprise settings
- Can be overridden by team/project settings

---

### 3. Team Level (Shared - Recommended for Teams)

**Location:** `./CLAUDE.md` (project root, committed to git)

**When to use:**
- Team uses DEIA on shared projects
- Want DEIA behavior committed to repo
- New team members automatically get DEIA

**Setup:**
```bash
# Create team-level DEIA memory
cp .claude/preferences/deia.md CLAUDE.md

# Commit to repo
git add CLAUDE.md
git commit -m "Add DEIA team memory"
git push
```

**Behavior:**
- Committed to git (everyone gets it)
- Overrides user-level settings
- All team members have consistent DEIA behavior
- Can be overridden by project-level settings

---

### 4. Project Level (Project-Specific)

**Location:** `./.claude/preferences/deia.md` or `./.claude/CLAUDE.md`

**When to use:**
- Want DEIA only on specific projects
- Need project-specific configuration
- Don't want team-wide DEIA

**Setup:**

Already exists: `.claude/preferences/deia.md`

**Or use # memory:**
```
# deia
[Paste content from .claude/preferences/deia.md]
```

**Behavior:**
- Only applies to THIS project
- Highest precedence (overrides all others)
- Not committed to git (in `.gitignore`)

---

## Comparison Table

| Aspect | Enterprise | User | Team | Project |
|--------|------------|------|------|---------|
| **Location** | `/Library/Application Support/` | `~/.claude/` | `./CLAUDE.md` | `./.claude/` |
| **File** | `CLAUDE.md` | `CLAUDE.md` | `CLAUDE.md` | `preferences/deia.md` |
| **Scope** | All users in org | All your projects | This repo (team) | This project only |
| **Committed** | N/A | No | **Yes** | No (gitignored) |
| **Detection** | **Required** | **Required** | **Required** | Optional |
| **Setup** | IT/Admin | Once | Per repo | Per project |
| **Precedence** | 1 (Lowest) | 2 | 3 | 4 (Highest) |
| **Best for** | Mandatory org-wide | Individual devs | Team projects | Project-specific |

---

## Which Level Should You Use?

### For Individual Developers
→ **User-level** (`~/.claude/CLAUDE.md`)
- Set once, works everywhere
- Auto-detects DEIA projects

### For Teams
→ **Team-level** (`./CLAUDE.md`)
- Commit to repo
- Everyone gets DEIA automatically
- New contributors onboard instantly

### For Organizations
→ **Enterprise-level** (managed by IT)
- Mandatory DEIA usage
- Centrally controlled
- Users can customize with user/project levels

### For Specific Projects Only
→ **Project-level** (`./.claude/preferences/deia.md`)
- Explicit opt-in
- Fine-grained control
- Overrides everything else

---

## Detection Logic (Required for Enterprise/User/Team)

At Enterprise, User, and Team levels, DEIA **must** check if `.deia/` exists:

```python
from pathlib import Path

if not Path('.deia').exists():
    # Not a DEIA project, skip all DEIA behavior
    pass
else:
    # This is a DEIA project, proceed
    from deia.logger import ConversationLogger
    # ... DEIA behavior
```

**Why?**
- Enterprise/User/Team levels apply to ALL projects
- Not every project uses DEIA
- Detection prevents DEIA from interfering with non-DEIA projects

**Project-level doesn't need detection** (you explicitly set DEIA for that project).

---

## Precedence in Action

**Example: User has User-level, project has Team-level**

1. Claude loads Enterprise memory (if exists)
2. Claude loads User memory (overrides enterprise)
3. Claude loads Team memory (overrides user) ← **This wins**
4. Claude loads Project memory (if exists, would override team)

**Result:** Team-level DEIA behavior applies.

---

## Setup Instructions

### Enterprise (Admin)

```bash
# macOS
sudo mkdir -p "/Library/Application Support/ClaudeCode"
sudo cp .claude/preferences/deia.md "/Library/Application Support/ClaudeCode/CLAUDE.md"

# Windows (as admin)
mkdir "C:\ProgramData\ClaudeCode"
copy .claude\preferences\deia.md "C:\ProgramData\ClaudeCode\CLAUDE.md"
```

### User (Individual)

```bash
mkdir -p ~/.claude
cp .claude/preferences/deia.md ~/.claude/CLAUDE.md
```

### Team (Shared Repo)

```bash
cp .claude/preferences/deia.md CLAUDE.md
git add CLAUDE.md
git commit -m "Add DEIA team memory"
```

### Project (This Project Only)

Already set up: `.claude/preferences/deia.md`

---

## Verification

Check which levels are active:

```bash
# Enterprise
ls "/Library/Application Support/ClaudeCode/CLAUDE.md"

# User
ls ~/.claude/CLAUDE.md

# Team
ls CLAUDE.md

# Project
ls .claude/preferences/deia.md
```

In Claude Code:
```
Show me all my active memories
```

Claude will list Enterprise → User → Team → Project in order.

---

## Troubleshooting

### DEIA activating in non-DEIA projects

**Cause:** Missing detection logic at Enterprise/User/Team level

**Fix:** Ensure memory starts with:
```python
from pathlib import Path
if not Path('.deia').exists():
    pass  # Skip DEIA
```

### Team member not getting DEIA

**Cause:** `CLAUDE.md` not committed to repo

**Fix:**
```bash
git add CLAUDE.md
git commit -m "Add DEIA team memory"
git push
```

Team member pulls:
```bash
git pull
```

### Project-level overriding team settings unexpectedly

**Cause:** Project-level has highest precedence

**Solution:** Remove project-level if you want team-level to apply:
```bash
rm .claude/preferences/deia.md
# Or remove # deia project memory
```

---

## Best Practices

1. **Choose one primary level** (don't mix unnecessarily)
2. **Use detection at Enterprise/User/Team** (required)
3. **Document your team's approach** (in README)
4. **Test in non-DEIA project** (ensure detection works)
5. **Keep memories in sync** (if using multiple levels)

---

## Migration Path

### From Manual to User-Level

```bash
# Set up user-level memory
mkdir -p ~/.claude
cp .claude/preferences/deia.md ~/.claude/CLAUDE.md

# Now works in all DEIA projects automatically
```

### From User to Team-Level

```bash
# Create team memory
cp ~/.claude/CLAUDE.md CLAUDE.md

# Commit for team
git add CLAUDE.md
git commit -m "Migrate DEIA to team-level"
```

### From Team to Enterprise

```bash
# Admin migrates
sudo cp CLAUDE.md "/Library/Application Support/ClaudeCode/CLAUDE.md"

# Team can remove team-level
git rm CLAUDE.md
git commit -m "Migrated DEIA to enterprise-level"
```

---

## Summary

**DEIA respects all four Claude Code memory levels:**

✅ Enterprise (org-wide)
✅ User (personal)
✅ Team (shared repo)
✅ Project (specific project)

**Detection is built-in** - Only activates in projects with `.deia/` directory.

**Choose the level that fits your workflow.**
