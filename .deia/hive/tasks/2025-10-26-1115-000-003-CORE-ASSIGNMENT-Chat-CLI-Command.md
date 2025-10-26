# CORE MISSION TASK: deia chat Command + Bot Selector
**From:** Q33N (BEE-000 Queen)
**To:** BOT-003 (CLAUDE-CODE-003)
**Date:** 2025-10-26 11:15 AM CDT
**Priority:** P0 - CORE MISSION
**Status:** BLOCKING - Waits for BOT-001 Anthropic service

---

## MISSION CRITICAL

Build CLI `deia chat` command to launch chat interface with bot selector.

**User experience:** `deia chat` → launches browser on port 8000 → chat window opens with bot selector dropdown.

---

## Task Requirements

**Create 3 main components:**

### 1. CLI Command: `deia chat`
**File:** Add to `src/deia/cli.py`

```
@main.command()
@click.option('--port', default=8000, help='Port to run chat server (default: 8000)')
@click.option('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
@click.option('--open-browser/--no-open-browser', default=True, help='Open browser on startup')
def chat(port, host, open_browser):
    """Start chat interface with bot selector"""
    # Launch FastAPI app on specified port
    # Optionally open browser to http://localhost:{port}
```

**Features:**
- ✅ Launches `src/deia/services/chat_interface_app.py` on specified port
- ✅ Opens browser automatically (or --no-open-browser flag)
- ✅ Graceful shutdown (Ctrl+C)
- ✅ Port checking (fail if already in use)

### 2. HTML Bot Selector UI
**File:** Enhance existing `chat_interface.html`

**Add to UI:**
- Bot selector dropdown (OpenAI / Anthropic)
- Show current bot in title/header
- Switch bot in dropdown → maintains chat history per bot
- Bot status indicator (e.g., "Connected to OpenAI")

**JavaScript:**
- Track selected bot in session
- Send bot preference with each message
- Maintain separate history per bot
- Switch bot button/dropdown

### 3. Backend Bot Routing
**File:** Enhance `src/deia/services/chat_interface_app.py`

**Modifications:**
- Accept bot selection from frontend
- Route messages to correct LLM service (OpenAI or Anthropic)
- Maintain per-bot conversation history
- Return bot info in message responses

---

## Acceptance Criteria

- [ ] `deia chat` command exists and launches app
- [ ] Browser opens on port 8000
- [ ] Bot selector dropdown visible in UI
- [ ] OpenAI bot works via dropdown
- [ ] Anthropic bot works via dropdown
- [ ] Bot switching maintains history
- [ ] Chat messages route to correct bot
- [ ] Error handling (missing API keys, timeouts)
- [ ] 20+ unit tests, 100% passing
- [ ] No breaking changes to existing chat app

---

## Tests Required

- ✅ CLI command launches successfully
- ✅ Server starts on specified port
- ✅ Browser opens (or --no-open-browser respected)
- ✅ Bot selector UI renders
- ✅ OpenAI bot selection works
- ✅ Anthropic bot selection works
- ✅ Bot switching preserves history
- ✅ Message routing to correct service
- ✅ API key validation
- ✅ Port already in use error handling
- ✅ Graceful shutdown
- ✅+ 8 more (20 total)

---

## Deliverable

`.deia/hive/responses/deiasolutions/bot-003-chat-command-complete.md`

**Estimated Time:** 180 minutes

---

## DEPENDENCIES

- **Waits for:** BOT-001 Anthropic service completion
- **Then:** Start this task

---

## CRITICAL NOTES

1. **Do NOT** start until BOT-001 Anthropic service is complete
2. **Reuse existing chat interface app** - don't rewrite, enhance
3. **Keep bot switching simple** - dropdown, not complex UI
4. **All tests must pass** before completion
5. **Test end-to-end:** Launch `deia chat` → select bots → chat works

---

**WAIT for BOT-001, then GO. CORE MISSION.**
