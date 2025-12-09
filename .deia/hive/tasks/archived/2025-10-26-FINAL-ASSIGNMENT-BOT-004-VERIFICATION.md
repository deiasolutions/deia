# FINAL ASSIGNMENT: BOT-004 - MVP E2E Verification

**Priority:** P0 (MVP-blocking)
**Time Estimate:** 30 minutes
**Status:** READY
**Depends On:** BOT-003 Service Integration completion

---

## CONTEXT

ServiceFactory work completed and consolidated. Task endpoint now uses existing `create_llm_service()` factory.

**Your job:** Verify all 5 bot types work end-to-end through the chat interface.

---

## OBJECTIVE

Test that users can successfully chat with ALL 5 bot types:
1. Claude (Anthropic API)
2. ChatGPT (OpenAI API)
3. Claude Code (CLI subprocess)
4. Codex (CLI subprocess)
5. LLaMA (Ollama local)

---

## PART 1: Launch Bot Registry (5 min)

Start the service in development mode:

```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions

# Make sure port 8000 is free
lsof -i :8000  # or: netstat -an | findstr :8000

# Start the chat interface service
python -m uvicorn src.deia.services.chat_interface_app:app --port 8000 --reload
```

Verify output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## PART 2: Register Test Bots (5 min)

Open new terminal, run these curl commands:

```bash
# Claude (API)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "TEST-CLAUDE",
    "bot_type": "claude",
    "token": "dev-token-12345"
  }'

# ChatGPT (API)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "TEST-CHATGPT",
    "bot_type": "chatgpt",
    "token": "dev-token-12345"
  }'

# Claude Code (CLI)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "TEST-CLAUDE-CODE",
    "bot_type": "claude-code",
    "token": "dev-token-12345"
  }'

# Codex (CLI)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "TEST-CODEX",
    "bot_type": "codex",
    "token": "dev-token-12345"
  }'

# LLaMA (Ollama)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "TEST-LLAMA",
    "bot_type": "llama",
    "token": "dev-token-12345"
  }'
```

Expected response for each:
```json
{
  "success": true,
  "bot_id": "TEST-*",
  "status": "ready",
  "port": XXXX
}
```

**Record which bots launched successfully:**
- [ ] Claude
- [ ] ChatGPT
- [ ] Claude Code
- [ ] Codex
- [ ] LLaMA

---

## PART 3: Test Chat Endpoint (10 min)

For each registered bot, send a task:

```bash
# Claude
curl -X POST http://localhost:8000/api/bot/TEST-CLAUDE/task \
  -H "Content-Type: application/json" \
  -d '{"command": "Say hello and list your capabilities"}'

# ChatGPT
curl -X POST http://localhost:8000/api/bot/TEST-CHATGPT/task \
  -H "Content-Type: application/json" \
  -d '{"command": "Say hello and list your capabilities"}'

# Claude Code
curl -X POST http://localhost:8000/api/bot/TEST-CLAUDE-CODE/task \
  -H "Content-Type: application/json" \
  -d '{"command": "Create a simple Python hello.py file"}'

# Codex
curl -X POST http://localhost:8000/api/bot/TEST-CODEX/task \
  -H "Content-Type: application/json" \
  -d '{"command": "Create a simple Python hello.py file"}'

# LLaMA
curl -X POST http://localhost:8000/api/bot/TEST-LLAMA/task \
  -H "Content-Type: application/json" \
  -d '{"command": "Say hello and list your capabilities"}'
```

**Check for:**
- ✅ `"success": true` in response
- ✅ Bot returns non-empty response
- ✅ No errors in console

**Record results:**
- [ ] Claude responds
- [ ] ChatGPT responds
- [ ] Claude Code responds
- [ ] Codex responds
- [ ] LLaMA responds

---

## PART 4: Test WebSocket Chat (5 min)

Connect via WebSocket (using curl or wscat):

```bash
# Install wscat if needed
npm install -g wscat

# Connect to WebSocket
wscat -c "ws://localhost:8000/ws?token=dev-token-12345"

# Once connected, send JSON message:
{
  "type": "chat",
  "bot_id": "TEST-CLAUDE",
  "message": "Hello, how are you?"
}
```

Expected:
- ✅ Connection accepted
- ✅ Bot responds via WebSocket
- ✅ Response shows in terminal

---

## PART 5: Create Verification Report

Create file: `.deia/hive/responses/deiasolutions/BOT-004-E2E-VERIFICATION-REPORT.md`

Write:

```markdown
# BOT-004 E2E Verification Report

**Date:** [TODAY]
**Tester:** BOT-004
**Status:** ✅ PASSED

## Bot Launch Results
- [x] Claude: ✅ Ready
- [x] ChatGPT: ✅ Ready
- [x] Claude Code: ✅ Ready
- [x] Codex: ✅ Ready
- [x] LLaMA: ✅ Ready

## Chat Task Results
- [x] Claude: ✅ Responds
- [x] ChatGPT: ✅ Responds
- [x] Claude Code: ✅ Responds
- [x] Codex: ✅ Responds
- [x] LLaMA: ✅ Responds

## WebSocket Results
- [x] Connection: ✅ Accepts token
- [x] Messaging: ✅ Sends/receives
- [x] All bot types: ✅ Respond via WebSocket

## Failures (if any)
None. All 5 bot types working end-to-end.

## Ready for Production
✅ YES - MVP is operational.
```

---

## SUCCESS CRITERIA

- ✅ All 5 bots launch without error
- ✅ All 5 bots respond to task endpoint
- ✅ WebSocket chat works with at least one bot
- ✅ Verification report written
- ✅ No errors in server console

---

## IF SOMETHING FAILS

**Bot won't launch:**
- Check API key is set (ANTHROPIC_API_KEY, OPENAI_API_KEY)
- Check port is available
- Check bot_type matches enum values (claude, chatgpt, claude-code, codex, llama)

**Bot won't respond to task:**
- Check bot_type in registry matches request
- Check service factory is receiving correct provider name
- Check logs for error messages

**WebSocket fails:**
- Verify token is `dev-token-12345`
- Check WebSocket connection accepts before sending message
- Try different bot_id that successfully launched

---

## DELIVERABLES

When done, create completion file:

`.deia/hive/responses/deiasolutions/bot-004-mvp-verification-complete.md`

---

## NEXT STEP

After verification, system is OPERATIONAL. Ready to deploy or add P0 features.
