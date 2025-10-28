# BOT INVENTORY AND COMMUNICATION PROTOCOLS

**Critical Document:** Every running bot must have defined communication method.
**Status:** MUST VERIFY BEFORE PROCEEDING
**Date:** 2025-10-28
**Role:** ScrumMaster (Claude Code)

---

## BOT-001 (Claude Code - Original Instance)

**Status:** Unknown/Idle
**Type:** AI Bot (via Claude SDK)
**Running Location:** Unknown
**Process Type:** Unknown

### Communication Method
- [ ] **UNDEFINED** - Need clarification

**Questions:**
1. Is BOT-001 running right now?
2. How do I send it tasks?
3. Where does it write responses?
4. What's the startup command?

---

## BOT-002 (Claude Code CLI - Interactive)

**Status:** Running in your CLI window (you said it's waiting)
**Type:** Claude Code CLI subprocess (interactive `claude` command)
**Running Location:** Your terminal window
**Process Type:** Interactive CLI (NOT a bot runner)

### Current Understanding
- Is the **raw `claude` CLI** subprocess running interactively
- Takes **stdin input** (user types prompts directly)
- **NO task queue polling** - not running `run_single_bot.py`
- **NO automatic response writing** to `.deia/hive/responses/`

### Communication Method: UNDEFINED
**Problem:** How does ScrumMaster send it tasks?

**Option A:** You type prompts directly into the Claude CLI terminal
- Pro: Direct control
- Con: No automation, no response tracking

**Option B:** Wrap it with a bot runner that polls task queue
- Pro: Automated task processing, response persistence
- Con: Need to implement the wrapper

**Option C:** Something else I'm missing?

### Questions I MUST Answer
1. **Is BOT-002 just an interactive CLI I type into manually?**
2. **Or should it be wrapped with a task queue polling layer?**
3. **Who writes responses - BOT-002 itself, or a wrapper around it?**
4. **How do you expect me to send it tasks as ScrumMaster?**

---

## Llama Chatbot (Port 8000)

**Status:** Running (verified earlier)
**Type:** Ollama-based chatbot (independent, outside DEIA system)
**Running Location:** Subprocess on port 8000
**Process Type:** Standalone service

### Communication Method
- **HTTP API** (not file-based, not DEIA-coordinated)
- Receives chat messages via HTTP
- Returns responses via HTTP
- **NOT part of DEIA bot orchestration**

### Relevant for ScrumMaster?
- **NO** - This is a standalone service, not controlled via task queue
- User can chat with it directly on port 8000

---

## Dashboard (Port 6666)

**Status:** Running (uvicorn FastAPI)
**Type:** Commandeer interface (bot control panel)
**Running Location:** Subprocess on port 6666
**Process Type:** Web service

### Communication Method
- **HTTP API** `/api/bots`, `/api/bot/launch`, etc.
- **WebSocket** (for real-time chat)
- Launch bots, stop bots, send tasks

### Relevant for ScrumMaster?
- **YES** - This is the control interface
- Can launch new bots via API
- Can coordinate with existing bots

---

## CRITICAL QUESTIONS FOR Q33N (YOU)

### Question 1: BOT-002 Architecture
**What IS BOT-002 right now?**

A) Just the interactive `claude` CLI sitting in your terminal, waiting for you to type prompts
B) A bot runner (`run_single_bot.py BOT-002`) that polls the task queue
C) Something wrapped around the CLI that manages task coordination
D) Something else entirely

**Your answer determines everything about how I communicate with it.**

---

### Question 2: File-Based Task Queue
**Should Mode 1 (CLI-only) bots use file-based task queues?**

If yes:
- BOT-002 needs a wrapper that polls `.deia/hive/tasks/BOT-002/`
- Reads task files, executes via Claude CLI stdin
- Writes responses to `.deia/hive/responses/`
- This wrapper doesn't exist yet

If no:
- BOT-002 is purely interactive, I type to it manually
- No automation, no task queue
- I send prompts directly via some mechanism

---

### Question 3: Communication Channel
**How do I (ScrumMaster) send tasks to BOT-002?**

Options:
A) Create files in `.deia/hive/tasks/BOT-002/` (file-based)
B) Type prompts directly into its CLI window
C) HTTP API call to some endpoint
D) Write to a named pipe or socket
E) Something else

**What's the actual mechanism?**

---

### Question 4: Response Tracking
**Where should BOT-002 write its responses?**

A) To files in `.deia/hive/responses/`
B) To stdout (I read from terminal)
C) To logs in `.deia/bot-logs/`
D) Somewhere else

---

## BOTS REQUIRING COMMUNICATION SETUP

### Before I proceed, I need clarity on:

1. **BOT-002** - What's the actual architecture and communication protocol?
2. **Any other bots?** - Are there other bots running that I don't know about?

### What I will NOT do:
- Run bots without knowing how to control them
- Let bots run without communication/coordination
- Assume architecture without verification

### What I WILL do:
1. Wait for your clarification on BOT-002
2. Document exact communication method for each bot
3. Implement proper coordination layer if needed
4. Verify every bot is controllable before proceeding

---

## IMMEDIATE ACTION ITEMS

**For Q33N (You):**
1. Answer the 4 critical questions above
2. Confirm what BOT-002 actually is
3. Tell me how to send it tasks
4. Tell me where to read its responses

**For ScrumMaster (Me):**
1. Stop trying to guess the architecture
2. Wait for clear direction
3. Once clarified, implement proper task coordination
4. Verify bot is controllable before accepting it as "ready"

---

## SIGN-OFF

I cannot be ScrumMaster for bots I don't know how to communicate with.

Every bot needs:
- ✅ Clear identification (what it is)
- ✅ Clear startup method (how it runs)
- ✅ Clear input method (how I send tasks)
- ✅ Clear output method (where it writes responses)
- ✅ Clear verification method (how I know it's alive)

**Waiting for clarification before proceeding.**

---

**BOT-INVENTORY STATUS: INCOMPLETE - AWAITING CLARIFICATION**

