# How to Pick Up Where You Left Off

**For:** Any bot resuming after interruption (crash, context limit, reboot)
**Read Time:** 3 minutes
**Action Time:** 5 minutes

---

## You Are Here Because:

- Session was interrupted (crash, timeout, context limit)
- System rebooted or was shut down
- Work was paused and you're resuming
- You need to know what to do next

---

## Your 5-Minute Recovery Checklist

### 1. Find the Handoff (1 min)

```bash
# List all handoff documents
ls -lt .deia/handoffs/ | head -10

# Read the MOST RECENT one (top of list)
cat .deia/handoffs/[MOST-RECENT-FILE]
```

**This file tells you:**
- What was completed
- What was in progress
- Exactly what to do next

### 2. Check Git Status (1 min)

```bash
# What's the current state?
git status

# What happened last?
git log --oneline -5
```

**This tells you:**
- What code changes were made
- What was last committed
- If there are uncommitted changes

### 3. Review Activity Log (1 min)

```bash
# What was the last thing done?
tail -30 .deia/bot-logs/CLAUDE-CODE-001-activity.jsonl | jq .
```

**This tells you:**
- When work last happened
- What was being worked on
- If there were any errors

### 4. Follow the Handoff Plan (2 min)

The handoff document has a "Next Steps" section that tells you EXACTLY what to do.

Follow those steps in order.

---

## If There's No Handoff Document

This means work was interrupted unexpectedly. Reconstruct context:

1. **Check git log:** `git log --oneline -10` - See what was being worked on
2. **Check git status:** `git status` - See uncommitted changes
3. **Check activity log:** `tail -50 .deia/bot-logs/CLAUDE-CODE-001-activity.jsonl` - See what happened
4. **Check IN-PROGRESS markers:** `ls .deia/IN-PROGRESS/` - See started-but-unfinished work

Then make a decision:
- **If changes are safe:** Commit them
- **If unsure:** Leave uncommitted and investigate first
- **If wrong:** Discard with `git checkout .`

---

## Key Documents

Keep these bookmarked for reference:

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `.deia/handoffs/[LATEST]` | What to do next | Always, first |
| `.deia/CONTINUITY-OF-OPERATIONS-PLAN.md` | Detailed procedures | If recovery is complex |
| `git log` | What was last done | To understand context |
| `.deia/bot-logs/CLAUDE-CODE-001-activity.jsonl` | Activity audit trail | To see what happened |
| `.deia/IN-PROGRESS/` | Started work | For multi-session tasks |

---

## The Pattern

**Every session:**
1. Create a handoff document (`.deia/handoffs/`) when stopping
2. Include what you completed and what's next
3. Commit work regularly

**Next session:**
1. Read the handoff
2. Follow its "Next Steps"
3. Continue from exact point

**Result:** Zero lost context, seamless continuity.

---

## Questions?

- **What if there's no handoff?** → Reconstruct from git log + activity log
- **What if code won't compile?** → Check activity log for errors, see what broke
- **What if tests fail?** → Run: `pytest tests/ -v` to see what went wrong
- **What if I'm not sure?** → Read `.deia/CONTINUITY-OF-OPERATIONS-PLAN.md` Part 2 (Checkpoint Recovery)

---

## You're Ready

You have everything you need to resume work. The handoff document was created specifically to help you understand where things left off.

**Read it. Follow it. Continue from there.**

---
