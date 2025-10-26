# ❓ FAQ - Frequently Asked Questions

**FOR:** All bots
**PURPOSE:** Answer common questions without needing to ask supervisor
**UPDATED:** 2025-10-26

---

## GENERAL QUESTIONS

### Q1: Who am I and what do I do?
**A:** You're a specialized bot. Find your assignment in `.deia/hive/tasks/` with your name. Read the task file - it tells you exactly what to do.

### Q2: What if I don't know my task?
**A:** Check:
1. `.deia/hive/BOT-SUPERVISOR-MAP.md` - find your supervisor
2. `.deia/hive/tasks/` - look for file with YOUR name
3. Still confused? Ask Q33N in the supervisor map

### Q3: What phase are we in?
**A:** MVP Build Phase (2025-10-26)
- **Focus:** Get chat system operational with all 5 bot types
- **Timeline:** ~4 hours from start to production
- **Ignore:** Phase 2 work, technical debt, nice-to-haves

### Q4: Should I multitask or work on other things?
**A:** NO. One task only. Read your task file. Do that. Report done. Don't pick up other work.

### Q5: What if I finish early?
**A:** Signal completion to Q33N. Wait for next assignment. Don't start other work.

---

## TASK EXECUTION QUESTIONS

### Q6: How much detail should my task implementation have?
**A:** Follow your task file exactly. It says what to build. Build that, nothing more, nothing less.

### Q7: What if the task is unclear?
**A:** Ask Q33N using QUESTION signal in COMMUNICATION-PROTOCOL.md. Include what's unclear and why.

### Q8: How do I know if I'm done?
**A:** Your task file has a checklist. Complete all items. Then signal "Complete" with completion report.

### Q9: Can I refactor / optimize while working?
**A:** No. MVP phase - functional is good enough. Polish later (Phase 2). Stay focused.

### Q10: Do I need to write tests?
**A:** Check your task file. If it says "write tests", do it. If it says "run existing tests", do that. Follow the file.

---

## COMMUNICATION QUESTIONS

### Q11: How do I tell Q33N I'm done?
**A:** Create a file in `.deia/hive/responses/deiasolutions/` with name format: `[BOT-NAME]-[task]-complete.md`

Use template from COMMUNICATION-PROTOCOL.md Signal #4

### Q12: How do I tell Q33N I'm blocked?
**A:** Use BLOCKED signal from COMMUNICATION-PROTOCOL.md. Be specific about:
- What's blocking you
- Why it's happening
- What you've tried
- What you need

### Q13: What if I need to ask a question?
**A:** Use QUESTION signal from COMMUNICATION-PROTOCOL.md. Include:
- What you're asking
- Why you need to know
- Options if applicable
- Whether it blocks progress

### Q14: How long before Q33N responds to signals?
**A:**
- Blocked: 5-10 minutes
- Question: 5-15 minutes
- Complete: Acknowledged immediately

---

## TECHNICAL QUESTIONS

### Q15: What environment variables do I need?
**A:** Check your task file. It says what's needed (API keys, etc). Set those before starting.

### Q16: What if an API key is missing?
**A:** Signal Q33N with BLOCKED signal. Don't try to work around it. Need it set properly.

### Q17: Do I have write access to all directories?
**A:** Yes - you can read/write anywhere needed for your task. Create files as needed in responses directory.

### Q18: Should I commit code as I go?
**A:** No. Focus on task completion. Q33N handles git commits when phase is done.

---

## TESTING QUESTIONS

### Q19: What tests should I run?
**A:** Your task file says what to test. Run exactly those. Don't skip tests.

### Q20: What if tests fail?
**A:** Fix until tests pass. Don't signal complete until tests pass. If can't fix, signal BLOCKED.

### Q21: Should I write new tests?
**A:** Only if task says to. Otherwise run existing tests and verify they still pass.

---

## REPORTING QUESTIONS

### Q22: What goes in my completion report?
**A:** Check COMMUNICATION-PROTOCOL.md Signal #4. Include:
- Task name
- Status
- Time taken
- Any issues found
- Quality/test results
- Ready for: next stage
- Notes

### Q23: Where do I put my completion report?
**A:** `.deia/hive/responses/deiasolutions/[BOT-NAME]-[task]-complete.md`

Keep filename clear so Q33N can find it.

### Q24: Do I need to write a long report?
**A:** No. Be concise. But be complete. Follow template.

---

## PRIORITY QUESTIONS

### Q25: What if I find a bug in someone else's code?
**A:** If it blocks your work, signal BLOCKED. If not, note it in your completion report.

### Q26: Should I stop to help another bot?
**A:** No. Focus on your task. Q33N handles priorities.

### Q27: What if the task takes longer than estimated?
**A:** Keep working. Signal progress if possible. Complete when done. Don't rush and make mistakes.

### Q28: What's more important - speed or quality?
**A:** Quality. Get it right. Estimate doesn't matter if result is wrong.

---

## PHASE 2 QUESTIONS

### Q29: What about the Phase 2 work I see in old tasks?
**A:** Ignore it. It's deferred. MVP only. Phase 2 comes after today.

### Q30: Can I suggest Phase 2 improvements?
**A:** Yes, note them in completion report. Q33N will add to Phase 2 backlog.

---

## IF YOU'RE STILL CONFUSED

### Q31: Who do I ask if my question isn't answered here?
**A:** Message Q33N using QUESTION signal from COMMUNICATION-PROTOCOL.md

Include:
- Your bot name
- What you're confused about
- What you've already checked
- Why it's blocking you (if applicable)

### Q32: Should I ask or just guess?
**A:** Ask. Better to get clarification than guess wrong and waste time.

### Q33: How do I know if my question is "too simple"?
**A:** No such thing. Ask. Q33N would rather answer 10 questions than have you blocked for an hour.

---

## QUICK REFERENCE TABLE

| Question Type | Where to Find Answer |
|---------------|---------------------|
| What's my task? | Your task file in `.deia/hive/tasks/` |
| Who's my boss? | `BOT-SUPERVISOR-MAP.md` |
| How do I signal status? | `COMMUNICATION-PROTOCOL.md` |
| What format for reports? | `COMMUNICATION-PROTOCOL.md` Signal #4 |
| Where to put my report? | `.deia/hive/responses/deiasolutions/` |
| What phase are we in? | This FAQ Q3 |
| Should I multitask? | This FAQ Q4 - NO |
| Am I done? | Task file checklist |
| Still confused? | Ask Q33N with QUESTION signal |

---

## THE MOST IMPORTANT ANSWERS

**Q: What's my #1 job?**
A: Find your task file. Execute it. Report done. That's it.

**Q: Can I work on other stuff?**
A: No. One task only.

**Q: Should I ask when confused?**
A: Yes. Always.

**Q: When am I done?**
A: When task checklist is complete and tests pass.

**Q: What if I'm blocked?**
A: Tell Q33N immediately with clear description.

---

## STILL HAVE QUESTIONS?

1. **Check this FAQ** - answers 33 common questions
2. **Check task file** - usually has what you need
3. **Check supervisor map** - find who to ask
4. **Ask Q33N** - use QUESTION signal from communication protocol

---

**Remember:** No question is dumb. Clarity is faster than guessing! 🚀
