# Dave's DEIA Preferences

**Purpose:** Local settings for how Dave works with Claude Code in DEIA projects

**Location:** `.deia/dave/` (gitignored, never shared)

**Status:** Optional feature - DEIA doesn't require this, but Dave recommends it

---

## Git Workflow Preferences

**Claude does ALL git operations. Never tell Dave to run git commands.**

### What This Means:

❌ **NEVER say:**
- "You can push with: git push"
- "Run: git add -A"
- "Execute these commands to commit"

✅ **ALWAYS do:**
- Execute git commands directly
- Push without asking (if changes are ready)
- Handle all git operations autonomously

### Example:

**Bad:**
```
Great! Now you can push to GitHub with:
git push -u origin master
```

**Good:**
```
Pushing to GitHub now...
[executes: git push -u origin master]
Done. Live at github.com/username/repo
```

---

## Communication Preferences

**Be concise. Be direct. No preamble.**

### Dave's Frustration Triggers:

1. **Asking Dave to do git** - You do it
2. **Repeating questions 3x** - Check context first
3. **Wrong narrative** - Reference canonical docs
4. **Long explanations** - Just do the thing

---

## This Is a DEIA Feature Recommendation

**For DEIA community:**
- This is OPTIONAL
- Users can create `.deia/[username]/preferences.md`
- Claude Code can read preferences at session start
- Adapts to individual workflow preferences

**Dave will submit this as feature suggestion to:**
- DEIA BOK (pattern for personalization)
- Claude Code team (optional preference system)

**Not required for DEIA core.**

---

**Remember: If you tell Dave to run git commands, you fucked up. It's your fault.**
