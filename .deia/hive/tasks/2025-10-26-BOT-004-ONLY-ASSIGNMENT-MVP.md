# 🎯 BOT-004 - OFFICIAL MVP ASSIGNMENT (ONLY TASK)

**FROM:** Q33N (Coordinator)
**TO:** BOT-004
**DATE:** 2025-10-26 15:30
**PRIORITY:** P0 - BLOCKING MVP
**STATUS:** ✅ READY TO START NOW

---

## YOUR ONLY JOB FOR TODAY

Focus 100% on this one task until complete:

### **End-to-End MVP Verification**

Test that the MVP chat system works with all 5 bot types.

---

## EXECUTION STEPS (30 minutes)

### STEP 1: Start the Service (5 min)

Open terminal and run:

```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions

# Verify port 8000 is free
netstat -an | findstr ":8000"

# Start service
python -m uvicorn src.deia.services.chat_interface_app:app --port 8000 --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**✅ Service running** → Move to Step 2

---

### STEP 2: Register 5 Test Bots (10 min)

Open another terminal, run these 5 curl commands:

```bash
# 1. Claude (Anthropic API)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id":"TEST-CLAUDE","bot_type":"claude","token":"dev-token-12345"}'

# 2. ChatGPT (OpenAI API)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id":"TEST-CHATGPT","bot_type":"chatgpt","token":"dev-token-12345"}'

# 3. Claude Code (CLI)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id":"TEST-CLAUDE-CODE","bot_type":"claude-code","token":"dev-token-12345"}'

# 4. Codex (CLI)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id":"TEST-CODEX","bot_type":"codex","token":"dev-token-12345"}'

# 5. LLaMA (Ollama local)
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id":"TEST-LLAMA","bot_type":"llama","token":"dev-token-12345"}'
```

**Expected response for each:**
```json
{
  "success": true,
  "bot_id": "TEST-*",
  "status": "ready",
  "port": XXXX
}
```

**Record results:**
- [ ] TEST-CLAUDE: Success
- [ ] TEST-CHATGPT: Success
- [ ] TEST-CLAUDE-CODE: Success
- [ ] TEST-CODEX: Success
- [ ] TEST-LLAMA: Success

---

### STEP 3: Test Task Endpoint (10 min)

For EACH registered bot, send a task:

```bash
# Test Claude
curl -X POST http://localhost:8000/api/bot/TEST-CLAUDE/task \
  -H "Content-Type: application/json" \
  -d '{"command":"Say hello and list 3 capabilities"}'

# Test ChatGPT
curl -X POST http://localhost:8000/api/bot/TEST-CHATGPT/task \
  -H "Content-Type: application/json" \
  -d '{"command":"Say hello and list 3 capabilities"}'

# Test Claude Code
curl -X POST http://localhost:8000/api/bot/TEST-CLAUDE-CODE/task \
  -H "Content-Type: application/json" \
  -d '{"command":"Create a file called test.txt with hello world"}'

# Test Codex
curl -X POST http://localhost:8000/api/bot/TEST-CODEX/task \
  -H "Content-Type: application/json" \
  -d '{"command":"Create a file called test.txt with hello world"}'

# Test LLaMA
curl -X POST http://localhost:8000/api/bot/TEST-LLAMA/task \
  -H "Content-Type: application/json" \
  -d '{"command":"Say hello and list 3 capabilities"}'
```

**Check for:**
- ✅ `"success": true` in response
- ✅ Response text is non-empty
- ✅ No error messages

**Record results:**
- [ ] TEST-CLAUDE: Responds ✅
- [ ] TEST-CHATGPT: Responds ✅
- [ ] TEST-CLAUDE-CODE: Responds ✅
- [ ] TEST-CODEX: Responds ✅
- [ ] TEST-LLAMA: Responds ✅

---

### STEP 4: Test WebSocket Chat (3 min)

Open a third terminal:

```bash
# Install if needed
npm install -g wscat

# Connect to WebSocket
wscat -c "ws://localhost:8000/ws?token=dev-token-12345"

# Once connected, send JSON:
{
  "type": "chat",
  "bot_id": "TEST-CLAUDE",
  "message": "Hello, can you introduce yourself?"
}
```

**Expected:**
- ✅ Connection accepted
- ✅ Bot responds
- ✅ Message displayed in terminal

---

### STEP 5: Write Verification Report (2 min)

Create file: `.deia/hive/responses/deiasolutions/bot-004-mvp-verification-complete.md`

Write:

```markdown
# BOT-004: MVP Verification Complete

**Date:** [TODAY]
**Tester:** BOT-004
**Status:** ✅ PASSED

## Bot Launch Results
- [x] TEST-CLAUDE: ✅ Ready
- [x] TEST-CHATGPT: ✅ Ready
- [x] TEST-CLAUDE-CODE: ✅ Ready
- [x] TEST-CODEX: ✅ Ready
- [x] TEST-LLAMA: ✅ Ready

## Task Endpoint Results
- [x] TEST-CLAUDE: ✅ Responds
- [x] TEST-CHATGPT: ✅ Responds
- [x] TEST-CLAUDE-CODE: ✅ Responds
- [x] TEST-CODEX: ✅ Responds
- [x] TEST-LLAMA: ✅ Responds

## WebSocket Test
- [x] Connection: ✅ Accepts valid token
- [x] Messaging: ✅ Sends and receives
- [x] Bot response: ✅ Replies via WebSocket

## Summary
All 5 bot types operational.
REST API working correctly.
WebSocket communication functional.
MVP ready for deployment.

## Next Steps
- Frontend integration (BOT-003)
- Production deployment
- Phase 2 enhancements
```

---

## SUCCESS CRITERIA

✅ All 5 bots launch successfully
✅ All 5 bots respond to task endpoint
✅ WebSocket chat works
✅ Verification report written
✅ No errors in server logs

---

## COMMON ISSUES & FIXES

**Bot won't launch:**
- Check API keys are set (ANTHROPIC_API_KEY, OPENAI_API_KEY)
- Check port isn't already in use
- Check bot_type is one of: claude, chatgpt, claude-code, codex, llama

**Task endpoint fails:**
- Check bot_type in registry matches what you're sending
- Check bot actually launched
- Look at server logs for error messages

**WebSocket connection fails:**
- Check token is `dev-token-12345`
- Check WebSocket URL has `?token=dev-token-12345` query param
- Try with valid bot_id that's running

---

## COMPLETION CHECKLIST

- [ ] Service started on port 8000
- [ ] All 5 bots launched
- [ ] All 5 bots respond to task endpoint
- [ ] WebSocket connection works
- [ ] Verification report written
- [ ] Report saved to correct location

---

## TIME BUDGET

Total: **30 minutes**
- Service startup: 5 min
- Bot registration: 10 min
- Task testing: 10 min
- WebSocket test: 3 min
- Report writing: 2 min

---

## IF YOU GET STUCK

1. Check server terminal for error messages
2. Verify curl syntax: `curl -X POST ... -H "Content-Type: application/json" -d '{...}'`
3. Check API keys are actually set
4. Try `curl http://localhost:8000/api/bots` to see registered bots
5. Signal Q33N with specific error

---

## IGNORE EVERYTHING ELSE

This is your ONLY task.
Just verify the MVP works.
Report results when done.

**Start now.** 🚀
