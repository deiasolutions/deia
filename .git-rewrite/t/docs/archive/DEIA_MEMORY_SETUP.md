# DEIA Memory Setup Guide

**How to configure Claude Code to remember DEIA behavior**

---

## Two Options: User-level or Project-level

Claude Code allows you to set memories at two levels:
- **User-level**: Applies to ALL projects
- **Project-level**: Applies to THIS project only

**DEIA works with both.** Choose based on your needs.

---

## Option 1: User-Level Memory (Recommended for DEIA users)

**When to use:**
- You use DEIA across multiple projects
- You want automatic detection
- You want "set once, works everywhere"

**Setup:**

1. In Claude Code, type:
   ```
   # deia-user
   ```

2. Claude will create a user-level memory that:
   - Checks for `.deia/` directory at startup
   - Only activates DEIA if present
   - Works across all your projects

**Behavior:**
- In DEIA projects → Auto-logging enabled
- In non-DEIA projects → Skips DEIA behavior
- No manual setup per project

---

## Option 2: Project-Level Memory

**When to use:**
- You only use DEIA on specific projects
- You want explicit opt-in per project
- You want more control

**Setup:**

1. In each DEIA-enabled project, type:
   ```
   # deia
   ```

2. Claude will create a project-level memory for that project only

**Behavior:**
- Must set up in each DEIA project
- Clear separation between projects
- More granular control

---

## How DEIA Memory Works

### Detection (User-level)

When you have user-level `# deia-user` memory:

```python
# Claude checks on startup:
from pathlib import Path

if Path('.deia').exists():
    # This is a DEIA project
    from deia.logger import ConversationLogger
    logger = ConversationLogger()

    # Read project resume
    if Path('project_resume.md').exists():
        # Read to understand context
        pass

    # Check auto-log setting
    import json
    with open('.deia/config.json') as f:
        config = json.load(f)
        auto_log = config.get('auto_log', False)
else:
    # Not a DEIA project, skip
    pass
```

### Project-Specific (Project-level)

When you have project-level `# deia` memory:

```python
# Claude assumes this IS a DEIA project
# No detection needed, directly use DEIA
from deia.logger import ConversationLogger
logger = ConversationLogger()
# ... rest of DEIA behavior
```

---

## Memory Content

The `.claude/preferences/deia.md` file contains the instructions Claude follows.

**Key behaviors:**
1. Check for `.deia/` directory (user-level only)
2. Read `project_resume.md` on startup
3. Check `.deia/config.json` for `auto_log` setting
4. If `auto_log: true`, enable real-time logging
5. Log steps throughout session, not just at end

---

## Verification

### Check if memory is set:

**User-level:**
```
Show me my user-level memories
```

Look for `deia-user` or similar.

**Project-level:**
```
Show me my project memories
```

Look for `deia` or similar.

### Test it works:

Start a new session in a DEIA-enabled project. Claude should:
1. Mention checking for DEIA
2. Read `project_resume.md` automatically
3. Start logging if `auto_log: true`

---

## Updating the Memory

If DEIA behavior changes, update the memory:

**User-level:**
```
# deia-user
[Updated content from .claude/preferences/deia.md]
```

**Project-level:**
```
# deia
[Updated content from .claude/preferences/deia.md]
```

---

## Removing DEIA Memory

**User-level:**
```
Forget my # deia-user memory
```

**Project-level:**
```
Forget my # deia memory for this project
```

---

## Recommendations

### For Individual Developers
**Use user-level** if you:
- Work on multiple DEIA projects
- Want automatic behavior
- Don't want to remember to set it up

### For Teams
**Use project-level** if you:
- Some team members use DEIA, others don't
- Want explicit opt-in
- Need to control which projects have DEIA

### For DEIA Development
**Use project-level** because:
- You're developing DEIA itself
- You want to test different configurations
- You need precise control

---

## Smart Detection (User-Level)

The user-level memory includes detection logic:

```markdown
# DEIA Auto-Logging System

**Check if this project uses DEIA:**
- Look for `.deia/` directory
- If not present, skip all DEIA behavior
- If present, proceed with DEIA startup

**This prevents DEIA from interfering with non-DEIA projects.**
```

---

## Troubleshooting

### User-level memory activating in non-DEIA projects

The detection should prevent this, but if it happens:
1. Check `.claude/preferences/deia.md` includes detection logic
2. Verify the memory starts with "Check if `.deia/` exists"
3. Update memory to include detection

### Project-level memory not activating

1. Verify you set `# deia` in THIS project
2. Check `.claude/preferences/deia.md` exists in project
3. Try setting memory again

### Memory lost after Claude Code update

Memories should persist, but if lost:
1. Re-run `# deia-user` (or `# deia`)
2. Claude will recreate from `.claude/preferences/deia.md`

---

## Best Practices

1. **Choose one approach** (user-level OR project-level, not both)
2. **Test in a safe project first** before relying on it
3. **Keep `.claude/preferences/deia.md` up to date** as DEIA evolves
4. **Document which approach your team uses** for consistency

---

## Summary

| Aspect | User-Level | Project-Level |
|--------|------------|---------------|
| Command | `# deia-user` | `# deia` |
| Scope | All projects | This project only |
| Detection | Checks for `.deia/` | Assumes DEIA present |
| Setup | Once | Per project |
| Best for | DEIA power users | Selective use |

**Both work. Choose what fits your workflow.**
