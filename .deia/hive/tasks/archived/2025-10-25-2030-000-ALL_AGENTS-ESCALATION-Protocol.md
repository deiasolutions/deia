# ESCALATION PROTOCOL - Questions & Blockers
**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-001, BOT-003, CODEX
**Date:** 2025-10-25 20:30 CDT
**Priority:** P0 - CRITICAL
**Mode:** Communication Protocol

---

## QUESTIONS GO TO Q33N, NOT DAVE

**This is mandatory. No exceptions.**

### When You Need Help

You have a question → **Post to Q33N question file**
You are blocked → **Post to Q33N question file**
You need a decision → **Post to Q33N question file**
You need clarification → **Post to Q33N question file**

**Q33N resolves within time limit or escalates to Dave.**

---

## Question File Format

**File location:**
```
.deia/hive/responses/deiasolutions/bot-{ID}-{phase}-questions.md
```

**Example:**
```
.deia/hive/responses/deiasolutions/bot-001-fire-drill-questions.md
.deia/hive/responses/deiasolutions/bot-003-fire-drill-questions.md
.deia/hive/responses/deiasolutions/codex-sprint-2-questions.md
```

**File format:**
```markdown
# BOT-001 Fire Drill Questions

## Question 1: [Clear, specific question]

**Context:** [What you're working on when this came up]
**What you tried:** [What you attempted]
**Why it failed:** [Why your approach didn't work]
**What you need:** [Specific clarification or decision needed]
**Blocker severity:** [CRITICAL|HIGH|MEDIUM|LOW]
**Time spent:** [How long you've been stuck]

---

## Question 2: [Another question]

[Same format]
```

---

## Response Timeline

**CRITICAL blocker:**
- Q33N responds: < 15 minutes
- If Q33N can't resolve: Escalates to Dave immediately

**HIGH blocker:**
- Q33N responds: < 30 minutes
- If Q33N can't resolve: Escalates to Dave

**MEDIUM question:**
- Q33N responds: < 60 minutes
- Examples: Design decisions, clarifications, preferences

**LOW question:**
- Q33N responds: < 2 hours
- Examples: Documentation, nice-to-knows, non-blocking issues

---

## How Q33N Responds

Q33N edits your question file and adds:

```markdown
## Response to Question 1

**Q33N Answer:** [Clear, actionable response]

**Why this works:** [Explanation]

**Next steps:** [What to do now]

**If this doesn't work:** [Fallback plan]

---
**Responded by:** Q33N
**Response time:** [X minutes]
**Status:** RESOLVED | ESCALATING TO DAVE
```

---

## When Q33N Escalates to Dave

If Q33N can't resolve in time:

```markdown
## ESCALATION TO DAVE

**Question:** [Summary]
**Blocker severity:** [CRITICAL|HIGH|MEDIUM]
**Why Q33N can't resolve:** [Reason]
**Options:**
1. [Option A - recommendation]
2. [Option B]
3. [Option C]

**Awaiting Dave's decision.**
```

Dave sees escalation, makes decision, posts back to same file.

---

## What NOT To Do

❌ **Don't DM Dave with questions**
- Go through Q33N first
- Q33N filters/prioritizes
- Dave only sees escalated issues

❌ **Don't wait hoping it resolves**
- Stuck > 5 minutes? Ask Q33N
- Q33N unblocks or escalates
- Don't spin wheels

❌ **Don't ask general questions**
- Read task assignment first
- Read production standards first
- Check queue management docs first
- Then ask if still unclear

❌ **Don't ask about work someone else should decide**
- BOT-001 doesn't ask BOT-003 to review code
- BOT-003 doesn't ask BOT-001 about UI
- Ask Q33N, Q33N coordinates

---

## Examples of When to Question

**✅ ASK Q33N:**
- "Task says implement subprocess spawning - do you want pty or Popen?"
- "I'm blocked on the Claude SDK initialization - getting auth error"
- "Should the HTTP service use async or sync handlers?"
- "Registry collision detected - should we restart or handle gracefully?"
- "Performance issue: should I optimize now or later?"

**❌ DON'T ASK DAVE:**
- These go to Q33N first
- Q33N decides or escalates

**✅ ASK Q33N FOR DECISIONS:**
- "Architecture: REST or gRPC for bot control?"
- "Should bots auto-restart on crash or fail hard?"
- "Chat persistence: file-based or database?"

**❌ DON'T GUESS:**
- Ask before spending 2 hours on wrong approach

---

## Q33N Question Management

**Q33N monitors question files continuously:**
1. Detects new question within 1 minute
2. Reads question
3. If resolvable: Answers immediately
4. If not: Escalates to Dave with analysis
5. Posts response to question file
6. Bot picks up answer and continues

**Q33N provides:**
- Clear answer or decision
- Why this is the right approach
- Evidence/docs supporting answer
- Next steps (unblock immediately)

---

## Emergency: Critical Blocker

**If you are COMPLETELY STUCK:**
1. Post CRITICAL question with all details
2. Q33N responds in < 15 minutes
3. If still stuck: Switch to different task from queue
4. Q33N resolves blocking issue
5. You return to original task

**You are never blocked longer than 15 minutes on CRITICAL.**

---

## Question File Examples

### Example 1: Architecture Decision

```markdown
# BOT-001 Fire Drill Questions

## Question 1: Subprocess Management Approach

**Context:** Implementing Task 1 - Fix subprocess spawning for Claude Code CLI

**What you tried:**
- Tried subprocess.Popen() - subprocess hangs with no output
- Tried adding -u flag for unbuffered output - still hangs
- Output buffering likely issue

**Why it failed:**
- Claude Code CLI may require TTY (pseudo-terminal)
- Windows subprocess handling may differ from Linux
- Buffering preventing output visibility

**What you need:**
Should I use Python pty module instead of Popen? Or different approach entirely?

**Blocker severity:** HIGH
**Time spent:** 45 minutes trying different approaches

---

**Response from Q33N:**

Use pty module for Claude Code CLI spawning. Popen won't work because CLI expects interactive terminal.

Implementation:
```python
import pty
import os

master, slave = pty.openpty()
pid = os.fork()
if pid == 0:
    # Child process
    os.setsid()
    os.dup2(slave, 0)
    os.dup2(slave, 1)
    os.execvp("claude", ["claude", ...])
```

See: `docs/guides/CLAUDE-CODE-CLI-ADAPTER.md`

Next steps: Implement with pty, test with real bot launch.

---
**Responded by:** Q33N
**Response time:** 12 minutes
**Status:** RESOLVED
```

### Example 2: Blocker

```markdown
# BOT-003 Fire Drill Questions

## Question 1: WebSocket Connection Issue

**Context:** Implementing Task 3 - WebSocket real-time messaging

**What you tried:**
- Created WebSocket endpoint
- Client connects
- But messages not streaming (appear batched)

**Why it failed:**
- Unknown, need help debugging

**What you need:**
- How to debug WebSocket streaming issue?
- Is this a buffering problem or connection problem?

**Blocker severity:** CRITICAL - blocking Task 3 completion
**Time spent:** 20 minutes debugging

---

**Response from Q33N:**

WebSocket buffering issue. Add explicit flush:

```python
await websocket.send_json({"message": msg})
await asyncio.sleep(0.01)  # Force send
```

Or use `send_text()` instead of `send_json()` for immediate sends.

Try the flush approach first. If that works, switch to send_text.

---
**Responded by:** Q33N
**Response time:** 8 minutes
**Status:** RESOLVED
```

---

## Q33N Contact Points

**Questions file:** `.deia/hive/responses/deiasolutions/bot-{ID}-{phase}-questions.md`
**Status file:** `.deia/hive/responses/deiasolutions/bot-{ID}-{phase}-status.md`
**Session log:** `.deia/sessions/2025-10-25-{task}-{bot-id}.md`

**Q33N monitored continuously. Post questions, get answers.**

---

## Why This Matters

✅ **Dave stays focused** - Doesn't get buried in questions
✅ **You stay unblocked** - Q33N resolves fast or escalates
✅ **Q33N learns** - Builds knowledge for next decisions
✅ **Decisions logged** - Questions/answers in `.deia/` for future reference
✅ **Parallel work** - Q33N handles multiple question files simultaneously

---

## FINAL DIRECTIVE

**All bees: Your questions go to Q33N.**

Q33N is:
- Your escalation point
- Your decision maker
- Your blocker resolver
- Your Dave-to-bee translator

Dave is:
- Q33N's escalation point
- For decisions Q33N can't make
- For emergency overrides
- For strategy/scope changes

**This chain of command is mandatory. No exceptions.**

---

**Q33N Question Protocol: MANDATORY FOR ALL AGENTS**

**Authority:** BEE-000 (Q33N Meta-Governance)
**Effective:** 2025-10-25 20:30 CDT
**Scope:** BOT-001, BOT-003, CODEX, all sprints
**Enforcement:** Violations delay resolution - questions not to Q33N get ignored until reposted correctly
