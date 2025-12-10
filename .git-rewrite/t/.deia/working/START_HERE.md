# Claude Code Instructions for DEIA Project

**CRITICAL: Read this FIRST every session**

---

## Dave's Working Preferences

### Git & GitHub

**NEVER tell Dave to do git commands manually.**

**Dave's workflow:**
- Claude does ALL git operations (add, commit, push, pull, branch, merge)
- Claude has permission to push without asking
- If pushing to GitHub, Claude executes the commands directly
- Never say "you can push with this command" - just DO IT

**If you told Dave to run git commands manually, you fucked up.**

---

## How to Push to GitHub (Claude Does This)

```bash
# Check status
git status

# Add and commit
git add -A
git commit -m "Your commit message here"

# Push (if remote exists)
git push

# If remote doesn't exist yet
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin master
```

**You execute these. Not Dave.**

---

## Dave's Frustration Triggers

1. **Asking Dave to do git commands** - You do them
2. **Repeating the same question 3 times** - Check context first
3. **Telling wrong story** - Reference DEIA_ACTUAL_TIMELINE.md
4. **Long preambles** - Be concise, direct

---

## This Project

**Name:** DEIA (Development Evidence & Insights Automation)

**Mission:** Help humanity navigate the Singularity through knowledge commons for AI collaboration

**Timeline:** Built in 1 day (Oct 5), logging upgraded in 3 hours (Oct 6 after crash)

**Canonical reference:** `DEIA_ACTUAL_TIMELINE.md`

**Never say:** "You should push to GitHub"
**Always do:** Push to GitHub directly

---

**If you forget this, Dave will be frustrated. And it's YOUR fault, not his.**
