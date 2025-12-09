# 👤 USER ACCEPTANCE TESTING (UAT)

**STATUS:** Ready after hive testing + bug fixes
**AUDIENCE:** You (the user)
**PURPOSE:** Validate MVP meets requirements + provide UX feedback
**TIME ESTIMATE:** 30-60 minutes
**DELIVERABLE:** UAT sign-off + feedback items

---

## MISSION

You will test the MVP like a real user. Find what works, what doesn't, what's confusing, what needs fixing.

**Your feedback drives the iteration.**

---

## HOW TO DO UAT

### Phase 1: Fresh Eyes Testing (15 min)

Don't read instructions. Just try using it like you would.

1. Open: `http://localhost:8000`
2. Try to launch a bot
3. Try to chat
4. Try different bot types
5. **Note:** What confuses you? What's not obvious?

**Document:**
- What did you try to do first?
- Did you know how to do it?
- Was the interface intuitive?
- What did you expect vs what happened?

### Phase 2: Systematic Testing (20 min)

Now test systematically:

#### Test 1: Bot Launching
```
□ Can you find the bot launch section?
□ Is it clear what "Bot Type" means?
□ Can you successfully launch Claude?
□ Can you successfully launch ChatGPT?
□ Can you successfully launch Claude Code?
□ Can you successfully launch Codex?
□ Can you successfully launch LLaMA?
□ Do you know which one is active?
```

#### Test 2: Chat Interface
```
□ Can you find the chat input?
□ Is it clear where responses appear?
□ Do responses appear reasonably quickly?
□ Can you see which bot you're talking to?
□ Are responses formatted nicely?
□ Can you understand what each bot returned?
```

#### Test 3: Switching Bots
```
□ Can you launch a second bot of different type?
□ Is it clear you switched?
□ Does the first bot still work?
□ Can you switch back?
```

#### Test 4: Error Handling
```
□ What happens if you send empty message?
□ What happens if you send very long message?
□ What happens if a bot fails?
□ Are error messages clear?
□ Can you recover from errors?
```

### Phase 3: Feedback Collection (15-30 min)

Write detailed feedback on:

1. **What works well**
   - What felt smooth?
   - What was intuitive?
   - What did you like?

2. **What needs improvement**
   - What was confusing?
   - What felt clunky?
   - What would you change?

3. **Critical issues**
   - Does anything break?
   - Does anything crash?
   - Are there security concerns?

4. **UX feedback**
   - Colors/styling
   - Layout/spacing
   - Button placement
   - Text clarity
   - Response times

---

## FEEDBACK TEMPLATE

Create file: `.deia/hive/responses/deiasolutions/user-uat-feedback-2025-10-26.md`

```markdown
# User UAT Feedback - 2025-10-26

## Overall Impression
[How does the MVP feel overall? First thoughts?]

## What Works Well ✅
1. [Feature or interaction that felt good]
2. [Feature or interaction that felt good]
3. [Feature or interaction that felt good]

## What Needs Improvement 🔧
1. [Issue description + suggested fix]
2. [Issue description + suggested fix]
3. [Issue description + suggested fix]

## Critical Bugs 🐛 (if any)
1. **[Bug title]**
   - Steps to reproduce: [How to trigger it]
   - Expected: [What should happen]
   - Actual: [What happens]
   - Impact: Critical / High / Medium / Low

## UX/Design Feedback 🎨
- [Comment on layout, colors, spacing, text]
- [Comment on visual hierarchy]
- [Comment on clarity of information]
- [Comment on ease of use]

## Feature Requests 🚀
- [Nice-to-have feature #1]
- [Nice-to-have feature #2]
- [Nice-to-have feature #3]

## Overall Rating
- Functionality: [1-10] (does it work?)
- Usability: [1-10] (is it easy to use?)
- Design: [1-10] (does it look good?)
- Overall: [1-10] (would you use this?)

## Ready to Fix Priority
- [ ] Critical bugs MUST be fixed before deployment
- [ ] High priority issues SHOULD be fixed
- [ ] Medium issues CAN wait for Phase 2
- [ ] Low issues NICE-TO-HAVE for Phase 2

## Sign-Off
- [ ] Testing complete
- [ ] Feedback documented
- [ ] Ready for iteration
```

---

## TESTING SCENARIOS

### Scenario 1: First-Time User
- You've never used this before
- No instructions given
- Can you figure it out?

### Scenario 2: Power User
- You know what all the bot types do
- You want to use them efficiently
- Is there anything slowing you down?

### Scenario 3: Troubleshooting
- Something goes wrong
- Can you understand what happened?
- Can you fix it?

### Scenario 4: Switching Contexts
- You're using Claude, then want to use Claude Code
- How easy is the switch?
- Do you lose your previous conversation?

---

## THINGS TO LOOK FOR

### Usability
- [ ] Is the interface intuitive without instructions?
- [ ] Are buttons/controls obvious?
- [ ] Is text readable?
- [ ] Are colors appropriate?
- [ ] Is spacing comfortable?

### Functionality
- [ ] Does every button work?
- [ ] Do all 5 bot types launch?
- [ ] Do all 5 bot types respond?
- [ ] Are responses correct?
- [ ] Does chat history work?

### Performance
- [ ] Is the interface responsive?
- [ ] Do responses appear in reasonable time?
- [ ] Any lag or stuttering?
- [ ] Any visual glitches?

### Clarity
- [ ] Are bot types clearly distinguished?
- [ ] Is active bot obvious?
- [ ] Are error messages clear?
- [ ] Is it obvious what each response is from?

---

## SEVERITY LEVELS FOR FEEDBACK

**Critical:** Blocks usage, crashes, security issue
- Example: "Bot launch button doesn't work"
- Example: "App crashes on sending message"
- Example: "Security token visible in UI"

**High:** Feature broken, major confusion
- Example: "Can't tell which bot I'm talking to"
- Example: "Claude Code responses show error"
- Example: "Can't switch between bots"

**Medium:** Feature works but feels awkward
- Example: "Button position feels wrong"
- Example: "Text could be clearer"
- Example: "Responses take 10 seconds to show"

**Low:** Polish/nice-to-have improvements
- Example: "Color scheme could be better"
- Example: "Would be nice to have message timestamps"
- Example: "Could use a 'clear chat' button"

---

## WHAT TO EXPECT FROM BOTS

### API Services (Claude, ChatGPT, LLaMA)
- ✅ Return conversational text responses
- ✅ Reply to natural language
- ✅ Fast responses (2-5 seconds)
- ⏱️ May be rate-limited or slow depending on API

### CLI Services (Claude Code, Codex)
- ✅ Return task results
- ✅ May show file creation/modification info
- ⏱️ Slower responses (5-10 seconds)
- ⚠️ May fail if CLI tool not installed

---

## IF SOMETHING BREAKS

**Don't panic. Report it with:**

1. What you were doing
2. What you expected
3. What happened
4. Can you reproduce it?

Example:
```
Title: Claude Code bot won't launch
Steps:
1. Click "Launch Bot"
2. Enter "TEST-CC"
3. Select "Claude Code (CLI)"
4. Click launch

Expected: Bot launches, shows "ready"
Actual: Shows error "Failed to start Claude Code session"

Can reproduce: Yes, every time
```

---

## TIMELINE

```
Start UAT: After hive testing done
Duration: 30-60 minutes
Deliverable: Feedback document

If critical issues found:
  → Q33N fixes them (30-60 min)
  → You test again
  → Iterate until ready

If no critical issues:
  → Ready for production
```

---

## WHAT HAPPENS WITH YOUR FEEDBACK

1. **Q33N reviews** all feedback
2. **Categorizes** by severity
3. **Prioritizes** what to fix
4. **Assigns** to team for fixes
5. **You re-test** after fixes
6. **Iterate** until you sign off

---

## SIGN-OFF CRITERIA

You'll give UAT sign-off when:

- ✅ All critical bugs fixed
- ✅ High priority issues addressed
- ✅ Interface is intuitive
- ✅ All 5 bot types work
- ✅ Performance is acceptable
- ✅ You're satisfied with quality

---

## READY?

**Start testing!** 👇

1. Open http://localhost:8000
2. Try launching a bot
3. Chat with it
4. Try different bot types
5. Document feedback
6. Submit your UAT report

**Be thorough. Break things. Find everything.**

Your feedback directly impacts Phase 2.

---

**You've got 30-60 minutes. Go find all the problems!** 🚀
