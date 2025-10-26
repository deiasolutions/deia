# 🐝 BOT SUPERVISOR MAP - Chain of Command

**PURPOSE:** Know who to report to, who reports to you
**CURRENT SPRINT:** MVP Build (2025-10-26)
**COORDINATOR:** Q33N

---

## SUPERVISOR HIERARCHY

```
USER (you)
    ↓
Q33N (Coordinator)
    ├─ BOT-001 (Codex specialist)
    ├─ BOT-003 (Frontend specialist)
    └─ BOT-004 (Testing specialist)
```

---

## WHO REPORTS TO WHOM

| Bot | Supervisor | Role | Current Assignment |
|-----|-----------|------|-------------------|
| **BOT-001** | Q33N | Codex/CLI specialist | Standby (backup) |
| **BOT-003** | Q33N | Frontend/CLI specialist | Frontend integration |
| **BOT-004** | Q33N | Testing/Verification | E2E verification |
| **Q33N** | USER | Coordinator | MVP orchestration |
| **USER** | - | Project owner | UAT + feedback |

---

## COMMUNICATION LINES

### BOT-003 or BOT-004 Get Blocked?
→ **Tell Q33N immediately**

**Message format:**
```
# [BOT-NAME] Blocked

Issue: [What's blocking you]
Root cause: [Why it's happening]
Need: [What you need to unblock]
```

### BOT-003 or BOT-004 Complete?
→ **Tell Q33N with completion report**

**Message format:**
```
# [BOT-NAME] Complete

Task: [Task name]
Status: ✅ COMPLETE
Time: X minutes
Issues: [None / describe]
Ready for: [Next stage]
```

### Q33N Gets Stuck?
→ **Tell USER (you) with status update**

### USER (You) Needs Something?
→ **Tell Q33N in UAT phase**

---

## FOR THIS MVP SPRINT

| Who | Reporting To | About What | When |
|-----|-------------|-----------|------|
| BOT-003 | Q33N | Progress on frontend | Every 15 min (self-directed) |
| BOT-004 | Q33N | Progress on E2E tests | Every 15 min (self-directed) |
| Q33N | USER | MVP status, ready for UAT? | At 16:50 |
| USER | (Self) | UAT feedback | At 18:00 |
| Q33N | USER | Fixes ready, re-test? | At 18:30 |
| USER | (Self) | Re-test results | At 19:00 |
| Q33N | USER | Deployed to production | At 19:30 |

---

## IF YOU'RE A BOT AND DON'T KNOW YOUR SUPERVISOR

**Ask here:**

1. Check your task file - it should say who to report to
2. Check this map - find yourself and see "Supervisor" column
3. If still unclear, **add a comment to this file** with your bot ID
4. **Q33N will respond** with your assignment

**Format:**
```markdown
### [BOT-NAME] - Asking

I don't know my supervisor or assignment. What should I do?

→ [Q33N will respond here]
```

---

## BOT-001 STATUS

**BOT-001:** Now online, available for backup
- If BOT-003 or BOT-004 need help: Can assist
- If critical blocker: Can take over task
- Otherwise: Standby

---

## Q33N AUTHORITY

Q33N (me) can:
- ✅ Assign tasks
- ✅ Clarify requirements
- ✅ Unblock bots
- ✅ Make priority calls
- ✅ Report to USER
- ✅ Make final deployment decision

---

## USER AUTHORITY

You (USER) can:
- ✅ Give feedback
- ✅ Reject MVP if quality insufficient
- ✅ Prioritize issues
- ✅ Approve for production
- ✅ Make Phase 2 decisions
- ✅ Adjust timelines if needed

---

## ESCALATION PATH

**If stuck:** Bot → Q33N → USER

**If disagreement:** Q33N mediates, USER has final say

**If timeline threatened:** Q33N adjusts approach, consults USER

---

## CURRENT SPRINT FOCUS

Everyone is focused on:
- **MVP build & test (TODAY)**
- Ignore Phase 2 work
- Ignore technical debt
- Ignore nice-to-haves
- **Just operational today**

---

## Questions?

If you're a bot and your supervisor isn't clear:
1. Read this file again
2. Check your task assignment
3. Ask in comment section below

---

## Acknowledgments

- Q33N: Coordinator
- BOT-001: Backup/specialist
- BOT-003: Frontend
- BOT-004: Testing
- USER: Owner/tester

**Let's ship the MVP!** 🚀
