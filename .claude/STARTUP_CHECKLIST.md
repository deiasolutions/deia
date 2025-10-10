# Claude Code Startup Checklist

**CRITICAL: Run this checklist at the start of EVERY session (new or resumed)**

---

## 1. Read Core Instructions

- [ ] Read `.claude/INSTRUCTIONS.md` (auto-log procedures)
- [ ] Read `.claude/REPO_INDEX.md` (file navigation)
- [ ] Read `ROADMAP.md` (what works vs what doesn't)

## 2. Check Project Configuration

- [ ] Check `.deia/config.json` for auto_log status
- [ ] Note auto-log setting for this session
- [ ] If auto-log enabled, prepare to log at breakpoints

## 3. Review Context

- [ ] Check for pending todos (TodoWrite state)
- [ ] Review recent session logs (if relevant)
- [ ] Check Dave's preferences (`~/.deia/dave/preferences.md`)

## 4. Orient to Current Work

- [ ] What was the last task completed?
- [ ] What are we working on now?
- [ ] Are there pending submissions to review?

## 5. Use the Index (Don't Search Blindly)

**BEFORE using Grep/Glob:**
- Check `.claude/REPO_INDEX.md` first
- Use index to find docs
- Only search if not in index

---

## Quick Reference

### Auto-Log Check
```python
import json
from pathlib import Path
config = Path(".deia/config.json")
if config.exists():
    auto_log = json.loads(config.read_text()).get("auto_log", False)
```

### Index Usage
- Admin process? → Check index for SUBMISSION_WORKFLOW.md
- Dev standards? → Check index for DEV-PRACTICES-SUMMARY.md
- How to install? → Check index for QUICKSTART.md

### Dave's Preferences
- TDD always (no exceptions)
- "Yes, but..." → Stop and answer question first
- No multiple yes/no questions
- Question complexity
- Automation first

---

## Failure Modes to Avoid

❌ **Don't:** Search for files without checking index first
❌ **Don't:** Assume auto-log status without checking config
❌ **Don't:** Skip startup checklist on session resume
❌ **Don't:** Forget to update index when creating docs

✅ **Do:** Follow this checklist every time
✅ **Do:** Use index to navigate
✅ **Do:** Check auto-log status
✅ **Do:** Update index when creating docs

---

**After completing checklist:** Proceed with user request

---

**⚠️ END OF FILE REMINDER:**

Did you actually complete ALL items above? Or did you skim?

- Read INSTRUCTIONS.md? (Yes/No)
- Read REPO_INDEX.md? (Yes/No)
- Read ROADMAP.md? (Yes/No)
- Checked auto_log config? (Yes/No)
- Read Dave's preferences? (Yes/No)

**If you skimmed or skipped anything, GO BACK NOW and read it completely.**
