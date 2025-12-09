# 🧪 MVP HIVE TESTING - Community Validation

**STATUS:** Ready after BOT-003 & BOT-004 completion
**TRIGGER:** When Q33N declares MVP OPERATIONAL
**AUDIENCE:** All hive agents (test in parallel)
**TIME ESTIMATE:** 30 minutes (hive testing)
**DELIVERABLE:** Issue list + sign-off

---

## MISSION

Test the MVP chat interface with all 5 bot types. Find bugs, UX issues, edge cases.

**This is NOT polished testing - it's rapid feedback.**

---

## HOW TO PARTICIPATE (For Any Hive Agent)

### Step 1: Read This Document (2 min)
You're doing it now ✅

### Step 2: Access MVP (2 min)
```
Service running at: http://localhost:8000
Token: dev-token-12345 (hardcoded for MVP)
```

Open in browser: `http://localhost:8000`

### Step 3: Test One Bot Type (10 min each)

**Pick ONE bot type and test thoroughly:**

#### If you choose CLAUDE (Anthropic API):
```
1. Click "Launch Bot"
2. Enter: BOT-ID = "HIVE-CLAUDE-[YOUR-NAME]"
3. Select: "Claude (Anthropic API)"
4. Click launch
5. Send messages and verify responses
6. Check bot type shows in header
7. Try edge cases (empty input, long text, special chars)
```

#### If you choose CHATGPT (OpenAI API):
```
Same process but select "ChatGPT (OpenAI API)"
```

#### If you choose CLAUDE-CODE (CLI):
```
Same process but select "Claude Code (CLI)"
Try: "Create a test.py file"
Check if file operations work
```

#### If you choose CODEX (CLI):
```
Same process but select "Codex (CLI)"
Try: "Create a test.js file"
```

#### If you choose LLAMA (Ollama):
```
Same process but select "LLaMA (Ollama)"
Verify responses (may be slower)
```

### Step 4: Report Issues (5 min)

Create a file: `.deia/hive/responses/deiasolutions/hive-testing-[YOUR-NAME]-[BOT-TYPE].md`

**Template:**
```markdown
# Hive Testing: [YOUR-NAME] Testing [BOT-TYPE]

**Date:** 2025-10-26
**Tester:** [YOUR-NAME]
**Bot Type:** [claude/chatgpt/claude-code/codex/llama]
**Status:** ✅ Tested

## What Worked
- [ ] Bot launched successfully
- [ ] Bot type displays in header
- [ ] Messages send and receive
- [ ] Responses appear in chat
- [ ] Bot type badge shows on responses

## Issues Found
### Issue #1 (if any)
- **Description:** [What happened]
- **Steps to reproduce:** [How to repeat]
- **Expected:** [What should happen]
- **Actual:** [What actually happened]
- **Severity:** Critical / High / Medium / Low

### Issue #2 (if any)
[Same format]

## UX Feedback
- [Note anything confusing about UI/UX]
- [Note anything that felt clunky]
- [Note suggestions for improvement]

## General Notes
[Anything else worth noting]

## Sign-Off
✅ Testing complete for [BOT-TYPE]
```

---

## WHAT TO TEST

### Functional Tests (Does it work?)

- [ ] **Bot Launch**
  - Can I select bot type?
  - Can I enter bot ID?
  - Does bot launch without error?
  - Does it show in header?

- [ ] **Chat**
  - Can I send a message?
  - Does bot respond?
  - Does response appear in chat window?
  - Does bot type badge show?

- [ ] **Different Bot Types**
  - Claude responds with text
  - ChatGPT responds with text
  - Claude Code shows file operations
  - Codex shows file operations
  - LLaMA responds with text

### Edge Cases (Does it break?)

- [ ] Empty input
- [ ] Very long text (1000+ chars)
- [ ] Special characters (!@#$%^&*)
- [ ] Unicode/emoji
- [ ] Multiple rapid messages
- [ ] Reconnect after disconnect

### UX Tests (Does it feel good?)

- [ ] Is bot type selector obvious?
- [ ] Is active bot info clear?
- [ ] Are chat messages readable?
- [ ] Do responses appear quickly?
- [ ] Are errors clear?
- [ ] Can you easily switch bots?

---

## BUG SEVERITY LEVELS

**Critical:** Crashes, data loss, security issue, blocks usage
**High:** Feature broken, prevents normal workflow
**Medium:** Feature works but with friction, minor confusion
**Low:** Polish, nice-to-have improvements, wording

---

## QUICK TESTING CHECKLIST

```
□ Bot launches
□ Bot type shows in header
□ Message sends
□ Response appears
□ Badge shows bot type
□ Can switch to another bot
□ No crashes/errors
□ Responses are reasonable
```

---

## PARTICIPATION GUIDE

**If you're a hive agent and want to help:**

1. Pick a bot type that hasn't been tested yet
2. Test it for 10 minutes
3. Report issues using the template
4. Mark your file with bot type you tested

**All agents can test simultaneously** - no conflicts.

---

## EXPECTED RESULT

After hive testing (30 min with multiple testers):

- ✅ All 5 bot types confirmed working
- ✅ Bug list created (if any)
- ✅ UX feedback collected
- ✅ Ready for user UAT

---

## NEXT STEPS

After all hive testing complete:

1. Q33N collects all issue reports
2. User does UAT on working system
3. User prioritizes feedback
4. Team fixes critical issues
5. Iterate until UAT passes

---

## QUESTIONS?

- Is bot not launching? Check API keys are set
- Is response slow? Normal for some services
- Is UI confusing? Report it - that's what we're testing
- Anything else? Note it in your report

---

**READY? Start testing!** 🧪

You've got 30 minutes to find all the problems. Be creative. Break things. Report what you find.
