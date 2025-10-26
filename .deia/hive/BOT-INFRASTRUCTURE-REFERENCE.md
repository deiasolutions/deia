# 🏗️ BOT INFRASTRUCTURE REFERENCE

**PURPOSE:** Understand the bot coordination system
**CREATED:** 2025-10-26
**LOCATION:** `.deia/hive/`

---

## DOCUMENTS CREATED FOR BOT COORDINATION

### 1. BOT-BOOT-DOC.md (10 lines)
**What it is:** Quick orientation guide for any new bot
**Contains:**
- Where to find tasks
- Where to find supervisor
- Where to report work
- Overview of autologging
- Quick 3-step next actions

**For:** Every bot, every time they activate
**Read time:** 2 minutes

**Key info:**
```
1. Find Your Orders: .deia/hive/tasks/
2. Know Your Supervisor: .deia/hive/BOT-SUPERVISOR-MAP.md
3. Report Output: .deia/hive/responses/deiasolutions/
4. Communication: .deia/hive/COMMUNICATION-PROTOCOL.md
5. Help: .deia/hive/FAQ.md
```

---

### 2. BOT-SUPERVISOR-MAP.md
**What it is:** Organizational chart - who reports to whom
**Contains:**
- Hierarchy of bots and supervisors
- Current sprint assignments
- Communication lines
- Escalation paths
- Authority of each role

**For:** Understanding chain of command, finding supervisor
**Use when:** Don't know who to report to, or who reports to you
**Key info:**
```
BOT-001 → Reports to Q33N
BOT-003 → Reports to Q33N
BOT-004 → Reports to Q33N
Q33N → Reports to USER
```

---

### 3. COMMUNICATION-PROTOCOL.md
**What it is:** Standard templates and format for bot signals
**Contains:**
- 6 signal types (Started, Progress, Blocked, Complete, Critical, Question)
- Template for each signal type
- Where to send signals
- Expected response times
- Autologging info
- Examples of good/bad signals

**For:** All bot-to-supervisor communication
**Use when:** You need to report status, ask question, signal completion
**Key signals:**
```
Signal #1: Task Started
Signal #2: Progress Update
Signal #3: Blocked (Critical)
Signal #4: Task Complete (Required)
Signal #5: Critical Issue Found
Signal #6: Question / Need Clarification
```

---

### 4. FAQ.md
**What it is:** Answers to 33 common questions
**Contains:**
- General questions (what am I, what phase, etc)
- Task execution questions
- Communication questions
- Technical questions
- Testing questions
- Reporting questions
- Priority questions
- What to do if still confused

**For:** Quick answers without asking supervisor
**Use before:** You ask Q33N a question
**Read time:** 5-10 minutes

---

## HOW IT ALL WORKS TOGETHER

### When a Bot Activates:
```
1. Read BOT-BOOT-DOC.md (2 min)
2. Find task in .deia/hive/tasks/
3. Find supervisor in BOT-SUPERVISOR-MAP.md
4. Read task file completely
5. Execute task
```

### When a Bot Needs to Communicate:
```
1. Determine signal type (started, blocked, complete, etc)
2. Go to COMMUNICATION-PROTOCOL.md
3. Find your signal type
4. Use template provided
5. Create response file or message
6. System autologs everything
```

### When a Bot Has Questions:
```
1. Check FAQ.md - answer might be there
2. If FAQ doesn't answer it, create QUESTION signal
3. Use COMMUNICATION-PROTOCOL.md template
4. Wait for Q33N response (5-15 min)
```

### When a Bot Gets Stuck:
```
1. Create BLOCKED signal from COMMUNICATION-PROTOCOL.md
2. Be specific about what's blocking
3. Q33N responds within 5-10 minutes
4. Continue work when unblocked
```

---

## FILE LOCATIONS

```
🏗️ BOT INFRASTRUCTURE:
├─ BOT-BOOT-DOC.md                    ← START HERE (any bot, any time)
├─ BOT-SUPERVISOR-MAP.md              ← Know your supervisor
├─ COMMUNICATION-PROTOCOL.md          ← How to communicate
├─ FAQ.md                             ← Common questions
└─ BOT-INFRASTRUCTURE-REFERENCE.md    ← This file

📋 TASK ASSIGNMENTS:
└─ tasks/
   ├─ 2025-10-26-BOT-003-ONLY-ASSIGNMENT-MVP.md
   ├─ 2025-10-26-BOT-004-ONLY-ASSIGNMENT-MVP.md
   ├─ 2025-10-26-BOT-EXECUTION-SEQUENCE.md
   └─ [Many other task files]

📝 BOT RESPONSES:
└─ responses/deiasolutions/
   ├─ bot-003-mvp-complete.md
   ├─ bot-004-e2e-verification-complete.md
   ├─ feedback-triaged-2025-10-26.md
   └─ [Other completion reports]

📊 LOGS:
└─ logs/
   └─ [Auto-generated activity logs]
```

---

## FOR FUTURE SPRINTS

When you run the next sprint (Phase 2, future features, etc):

1. **Create task files** in `.deia/hive/tasks/` with clear names
2. **Assign to bots** - specify supervisor in task file
3. **Point bots to BOT-BOOT-DOC.md** - they'll know what to do
4. **Use COMMUNICATION-PROTOCOL templates** - consistent signaling
5. **Monitor responses** in `.deia/hive/responses/deiasolutions/`
6. **Check FAQ if bots ask questions** - many are pre-answered

---

## ADVANTAGES OF THIS SYSTEM

✅ **Clear orientation:** Any bot can get oriented in 2 minutes
✅ **No ambiguity:** Supervisor map shows reporting lines
✅ **Standard signals:** Everyone uses same templates
✅ **Self-service help:** FAQ answers most questions
✅ **Autologging:** All activity captured automatically
✅ **Scalable:** Works with 2 bots or 20 bots
✅ **Focused:** One task per bot, no context switching
✅ **Transparent:** Clear chain of command
✅ **Fast:** No time wasted on clarifications

---

## CUSTOMIZATION FOR YOUR WORKFLOW

If you want to adapt this for your system:

1. **Update BOT-SUPERVISOR-MAP.md**
   - Change bot names
   - Change supervisor assignments
   - Add new roles if needed

2. **Update BOT-BOOT-DOC.md**
   - Customize file locations if different
   - Add links to your specific systems
   - Update context about current sprint

3. **Extend COMMUNICATION-PROTOCOL.md**
   - Add new signal types if needed
   - Customize template fields
   - Add role-specific signals

4. **Keep FAQ updated**
   - Add answers to questions that come up
   - Remove answers that become outdated

---

## METRICS THIS SYSTEM PROVIDES

Because of autologging and standard signals, you can track:

- ✅ When each bot started their task
- ✅ How long each task took
- ✅ Which bots got blocked and why
- ✅ Response times from supervisors
- ✅ Quality of completions
- ✅ Issues discovered during execution
- ✅ Timeline accuracy
- ✅ Bot reliability

---

## NEXT STEPS IF YOU LIKE THIS

1. **For today:** Bots use system for MVP work
2. **For Phase 2:** Reuse system with new task assignments
3. **For production:** Document any changes you make
4. **For scaling:** System works with unlimited bots

---

## QUESTIONS ABOUT THE INFRASTRUCTURE?

Check FAQ.md or document issues here for improvement next sprint.

---

**This system keeps bots focused, supervisors informed, and work flowing.** 🚀
