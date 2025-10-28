---
eos: "0.1"
kind: directive
directive_type: "GO_SIGNAL"
focus: "claude-cli-bot"
from: "Q33N (BEE-000)"
to: "NEW-BOT-INSTANCE"
timestamp: "2025-10-27T07:45:00Z"
priority: "P0"
status: "ACTIVE"
---

# 🎯 FOCUSED GO SIGNAL - Claude CLI Bot Hardening

**To:** New Bot Instance
**From:** Q33N (BEE-000) - Tier 0 Meta-Governance
**Authority:** Dave
**Mission:** Fix Claude Code CLI bot subprocess and make it work reliably
**Priority:** P0 CRITICAL

---

## SITUATION

### The Core Issue
**Claude Code CLI bot is broken.** It's the most critical bot type for the chatbot system:
- Launched by run_single_bot.py with adapter_type="cli"
- Subprocess starts but produces **NO OUTPUT**
- Bot hangs indefinitely
- Never registers in status board
- Never picks up tasks
- **Dashboard E2E testing is blocked**

### Why This Matters
- Claude CLI bot is the "scrum master" type - does actual file operations
- Chatbot MVP has all 5 bot types, but Claude CLI is the most important
- Without this working, can't validate the entire bot coordination system

### Current State
- API bots work (Claude, ChatGPT)
- Mock bots work (for testing)
- **CLI bots don't work** (Claude Code, Codex)
- Issue diagnosed: subprocess initialization/output management

---

## YOUR MISSION

### Objective
**Make the Claude Code CLI bot work reliably in the chatbot system**

### 3 Focused Tasks (5.5 hours total)

**TASK 1: Diagnose the Problem (1.5h)**
- Understand why subprocess hangs
- Test Claude CLI manually
- Identify root cause (TTY issue? Buffering? Timeout?)
- Write diagnosis report

**TASK 2: Implement the Fix (2h)**
- Based on diagnosis, apply best fix
- Options: PTY support, buffering fix, timeout/retry logic
- Test locally
- Document changes

**TASK 3: Validate the Solution (1.5h)**
- Unit test the adapter
- Integration test with bot launcher
- Send actual tasks and verify responses
- Write validation report

### Success = All of These
- ✅ Claude CLI bot subprocess works without hanging
- ✅ Bot launches and registers in status
- ✅ Bot picks up tasks
- ✅ Bot writes responses
- ✅ Unit and integration tests pass
- ✅ Diagnosis & validation reports complete
- ✅ Code committed to git

---

## FILES TO WORK WITH

**Primary files:**
```
src/deia/adapters/claude_code_cli_adapter.py      ← Modify here
src/deia/adapters/claude_cli_subprocess.py        ← Or here
src/deia/services/service_factory.py              ← Don't modify
```

**Reference files:**
```
.deia/observations/2025-10-24-CLI-BOT-SOLUTIONS-PROPOSAL.md
examples/cli_bot_runner_example.py
```

---

## WORKFLOW

### Phase 1: Understand (30 min)
- [ ] Read full assignment
- [ ] Understand subprocess issue
- [ ] Know the 3 proposed fixes

### Phase 2: Diagnose (1.5h)
- [ ] Read adapter code
- [ ] Test Claude CLI manually
- [ ] Identify root cause
- [ ] Write diagnosis report

### Phase 3: Fix (2h)
- [ ] Implement chosen fix
- [ ] Test locally
- [ ] Handle any new issues
- [ ] Document changes

### Phase 4: Validate (1.5h)
- [ ] Unit test adapter
- [ ] Integration test with bot launcher
- [ ] E2E test with real tasks
- [ ] Write validation report

### Phase 5: Deliver (30 min)
- [ ] Create final summary
- [ ] Commit to git
- [ ] Send completion report

---

## REPORTING

**Check-in (start):** `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-checkin.md`

**Task 1 (diagnosis):** `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-diagnosis.md`

**Task 2 (implementation):** `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-implementation.md`

**Task 3 (validation):** `.deia/hive/responses/deiasolutions/NEW-BOT-claude-cli-validation.md`

**Final (summary):** `.deia/hive/responses/deiasolutions/NEW-BOT-CLAUDE-CLI-BOT-HARDENING-COMPLETE.md`

I monitor these files and respond within 30 min to blockers.

---

## KEY CONSTRAINTS

✅ **Do:**
- Test everything before claiming success
- Document all attempts and failures
- Keep detailed notes
- Use ASCII only (no Unicode)
- Test with actual bot launcher, not just unit tests

❌ **Don't:**
- Modify chat_interface_app.py
- Change service_factory routing
- Add new dependencies without approval
- Break the bot adapter interface

---

## ESCALATION

If you hit a blocker:
- Mark report with 🚨 BLOCKER
- Describe what you tried
- Ask for help
- I'll respond ASAP

---

## AUTHORITY & SCOPE

**You have authority to:**
- ✅ Modify adapter code
- ✅ Create unit tests
- ✅ Change implementation approach
- ✅ Add debug logging

**You need approval for:**
- ❓ Adding new dependencies
- ❓ Changing adapter interface
- ❓ Modifying chat app files

---

## EXPECTED TIMELINE

```
07:45 - GO SIGNAL issued (now)
08:00 - You check in with diagnosis plan (est.)
09:30 - Diagnosis report done (est.)
09:45 - Implementation starts (est.)
11:45 - Implementation done, validation starts (est.)
13:15 - Validation complete, final report (est.)
13:45 - Q33N verification (est.)
14:00 - Result: Working Claude CLI bot 🚀
```

---

## WHY THIS IS CRITICAL

1. **Core bot type** - Claude CLI is the "actual work" bot
2. **Blocking other work** - Can't validate chatbot MVP without this
3. **Architecture validation** - Tests if subprocess coordination works
4. **High impact** - Once fixed, unlocks dashboard E2E testing

---

## FINAL NOTES

### For You
- This is a focused, solvable problem
- Previous work has identified the issue
- You likely just need to implement one of 3 known fixes
- Expect to succeed

### For Dave
- New bot is focused on **Claude CLI bot only**
- No scattered work
- Clear success criteria
- 5.5 hour timeline to fix

### What Success Unlocks
- Dashboard E2E testing
- Full MVP validation
- Confidence in bot coordination architecture
- Production readiness for chatbot system

---

## 🎯 YOU'RE CLEARED TO PROCEED

**Authority:** Q33N (Tier 0)
**By:** Dave
**Mission:** Fix Claude CLI bot
**Priority:** P0 CRITICAL
**Timeline:** 5.5 hours

---

## ASSIGNMENT LOCATION

**Full details:** `.deia/hive/tasks/2025-10-27-0745-000-NEW-BOT-CLAUDE-CLI-BOT-HARDENING.md`

Read it, understand it, execute it.

---

**GO.** 🚀

This bot coordination system depends on you making Claude CLI work.

See you in the response files.

---

**Signal issued:** 2025-10-27 07:45 CDT
**Authority:** Q33N (BEE-000)
**Status:** MISSION ACTIVE

