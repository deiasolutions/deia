# ⚠️ DEPRECATED PROTOCOL

**THIS DOCUMENT IS DEPRECATED AND ARCHIVED**

**Reason for deprecation:** This protocol has been superseded by the comprehensive master protocol.

**See instead:**  (the authoritative source of truth)

**Archive date:** 2025-10-29
**Archived by:** CLAUDE-CODE-002 (Documentation Systems Lead)

---

# 📢 COMMUNICATION PROTOCOL - How Bots Signal Status

**FOR:** All bots
**PURPOSE:** Standard way to communicate task status, blockers, completions
**SYSTEM:** Autologging captures all signals automatically

---

## COMMUNICATION TEMPLATES

### Signal #1: Task Started

**When:** You begin a task
**Format:**
```
# [BOT-NAME] Started: [Task Name]

Task: [Full name of task]
Assigned by: [Q33N or supervisor]
Estimated time: X minutes
Starting: [timestamp]
```

**Example:**
```
# BOT-003 Started: Frontend Service Integration

Task: Service Integration & Frontend Chat
Assigned by: Q33N
Estimated time: 50 minutes
Starting: 2025-10-26 15:35
```

---

### Signal #2: Progress Update (Optional)

**When:** Major milestones (if needed)
**Format:**
```
# [BOT-NAME] Progress: [Task Name]

Task: [Task name]
Progress: [% complete or milestone]
Completed: [What's done]
Remaining: [What's left]
ETA: [New estimate]
Issues: [None / describe]
```

**Example:**
```
# BOT-003 Progress: Frontend Integration

Task: Service Integration & Frontend Chat
Progress: 40% (bot selector added)
Completed: HTML form, JavaScript launch handler
Remaining: Response handling, badges, tests
ETA: 30 minutes remaining
Issues: None
```

---

### Signal #3: Blocked (Critical)

**When:** You're stuck and can't proceed
**Format:**
```
# [BOT-NAME] BLOCKED: [Task Name]

Task: [Task name]
Issue: [What's blocking you]
Root cause: [Why it's happening]
Attempted fixes: [What you've tried]
Need: [What's required to unblock]
Waiting on: [Person/action needed]
Time blocked: X minutes
```

**Example:**
```
# BOT-004 BLOCKED: E2E Verification

Task: E2E Verification Testing
Issue: Claude API not responding to requests
Root cause: ANTHROPIC_API_KEY environment variable not set
Attempted fixes: Checked variable, restarted service
Need: ANTHROPIC_API_KEY value set in environment
Waiting on: Q33N to set API key
Time blocked: 5 minutes
```

**ACTION:** Q33N will respond immediately with fix or workaround

---

### Signal #4: Task Complete (Required)

**When:** You finish the task
**Format:**
```
# [BOT-NAME] Complete: [Task Name]

Task: [Full task name]
Status: ✅ COMPLETE
Time: [Actual time taken]
Issues: [None / list any issues found]
Quality: [Passes requirements / Notes]
Test results: [Summary]
Ready for: [Next stage or who to handoff to]
Notes: [Anything noteworthy]
```

**Example:**
```
# BOT-003 Complete: Service Integration & Frontend

Task: Service Integration & Frontend Chat
Status: ✅ COMPLETE
Time: 48 minutes
Issues: None
Quality: All requirements met, tests passing
Test results: 5/5 functional tests pass
Ready for: Q33N final verification
Notes: Frontend is responsive, bot type selector working, all service types handled

Deliverable: .deia/hive/responses/deiasolutions/bot-003-mvp-complete.md
```

---

### Signal #5: Critical Issue Found

**When:** You discover a critical bug or security issue
**Format:**
```
# [BOT-NAME] CRITICAL: [Issue Name]

Severity: CRITICAL
Issue: [Description]
Impact: [What breaks]
Reproduction: [Steps to reproduce]
Needs fix: [Yes/No]
Can continue: [Yes/No - can you keep working?]
```

**Example:**
```
# BOT-004 CRITICAL: Security Issue

Severity: CRITICAL
Issue: API token visible in browser console
Impact: Security risk - token exposed
Reproduction: Open DevTools, check Network tab, see token in requests
Needs fix: Yes
Can continue: No - need to fix before deployment
```

---

### Signal #6: Question / Need Clarification

**When:** You need clarification from supervisor
**Format:**
```
# [BOT-NAME] Question: [Topic]

Question: [What you're asking]
Context: [Why you need to know]
Options: [If applicable, what are options?]
Blocking: [Yes/No - does this block progress?]
Waiting on: [Q33N response needed]
```

**Example:**
```
# BOT-003 Question: Frontend Framework

Question: Should I use Vue, React, or vanilla JS for bot selector?
Context: Task doesn't specify, want to match existing code style
Options: Vue (if used elsewhere), React (more powerful), Vanilla (simplest)
Blocking: Yes
Waiting on: Q33N guidance
```

---

## WHERE TO SEND SIGNALS

### Option 1: Message in Task File Comment
Add comments at bottom of your task file with signals

### Option 2: Create Response File
Create markdown file in `.deia/hive/responses/deiasolutions/`
**Format:** `[BOT-NAME]-[task]-[signal].md`

**Examples:**
```
bot-003-frontend-integration-complete.md
bot-004-e2e-verification-complete.md
bot-003-frontend-integration-blocked.md
bot-004-e2e-verification-progress.md
```

### Option 3: Direct Message
If extremely urgent, signal Q33N directly with clear format

---

## RESPONSE TIME EXPECTATIONS

| Signal Type | Expected Response |
|------------|-------------------|
| Task Complete | Acknowledged immediately |
| Blocked | 5-10 minutes |
| Progress Update | Acknowledged if needed |
| Critical Issue | 2-5 minutes |
| Question | 5-15 minutes |

---

## AUTOLOGGING

**What it captures:**
- ✅ All task signals
- ✅ Status updates
- ✅ Completions
- ✅ Issues reported
- ✅ Time tracking
- ✅ Questions & answers

**What you do:**
- Nothing extra - just follow templates above
- System captures everything automatically
- No manual logging required

**Where logs go:**
- `.deia/hive/logs/` (auto-generated)
- `.deia/bot-logs/` (activity log)

---

## STANDARD COMPLETION CHECKLIST

Before you signal "Complete", verify:

```
[ ] Task requirements met
[ ] Tests passing (if applicable)
[ ] Code quality acceptable
[ ] No debug code left
[ ] Error handling in place
[ ] Documentation done
[ ] Report file created
[ ] Status signal ready
```

---

## ESCALATION SIGNALS

If you need escalation:

**For issues that affect timeline:**
```
# [BOT-NAME] ESCALATION: [Issue Name]

Issue: [What's wrong]
Impact on timeline: [How much delay]
Needs: [What's needed to resolve]
Recommend: [Your suggestion]
```

**Q33N escalates to USER if needed**

---

## QUICK REFERENCE

| Event | Signal | File | Template |
|-------|--------|------|----------|
| Start work | "Started" | Task file | See Signal #1 |
| Making progress | "Progress" | Response file | See Signal #2 |
| Stuck | "BLOCKED" | Response file | See Signal #3 |
| Finish work | "Complete" | Response file | See Signal #4 |
| Big problem | "CRITICAL" | Response file | See Signal #5 |
| Need help | "Question" | Response file | See Signal #6 |

---

## EXAMPLES OF GOOD SIGNALS

**Good:**
```
# BOT-003 Complete: Frontend Integration

Status: ✅ COMPLETE
Time: 48 minutes
Issues: None
Quality: All requirements met
Test results: 28/30 passing (acceptable for MVP)
Ready for: Q33N verification
```

**Bad:**
```
done
```

**Good:**
```
# BOT-004 BLOCKED: E2E Tests

Issue: Ollama service not responding
Root cause: Service on port 11434 not running
Need: Ollama service started or alternative for testing
Waiting on: Q33N guidance
```

**Bad:**
```
stuck lol
```

---

## KEY POINTS

- ✅ Use templates provided
- ✅ Be specific and clear
- ✅ Include time estimate/actual
- ✅ Note any issues found
- ✅ Signal immediately when blocked
- ✅ Complete signals are critical for handoff
- ✅ System logs everything - don't worry about format details

---

## QUESTIONS ABOUT COMMUNICATION?

Check `FAQ.md` or ask Q33N in supervisor map

---

**Remember:** Clear communication keeps the MVP moving! 🚀
