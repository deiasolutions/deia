# SERVICE INTEGRATION: BOT-001 & BOT-003 HANDOFF

**Date:** 2025-10-26
**Status:** Ready for Execution
**Scope:** Enable all 5 bot types to be called from chat interface

---

## MISSION

Complete service integration so users can:
1. Launch any of 5 bot types from dropdown (✅ DONE)
2. Send messages/tasks from chat interface (❌ IN PROGRESS)
3. Get responses from appropriate service (❌ NEEDED)
4. See file modifications for CLI bots (❌ NEEDED)

---

## EXECUTION PLAN

### PHASE 1: BOT-001 (45 min)
**Task File:** `.deia/hive/tasks/2025-10-26-BOT-001-SERVICE-FACTORY.md`

**Deliverables:**
1. Create `ServiceFactory` class in new file
2. Update `/api/bot/{bot_id}/task` endpoint to use factory
3. Route to correct service based on bot_type from registry
4. Tests passing

**Success Criteria:**
- ServiceFactory can create all 5 service types
- Task endpoint routes correctly
- Tests pass
- Posts completion report

### PHASE 2: BOT-003 (40 min)
**Task File:** `.deia/hive/tasks/2025-10-26-BOT-003-SERVICE-INTEGRATION.md`

**Deliverables:**
1. Update ChatPanel.js to handle service responses
2. Add `process_task_file()` to API services
3. Create ServiceFactory tests
4. Update bot display to show type

**Success Criteria:**
- API services integrated with FileOperationService
- ChatPanel shows responses correctly
- Files modified by CLI services displayed
- Tests passing
- All services callable from chat

---

## EXECUTION SEQUENCE

```
BOT-001 Starts
    ↓
Create ServiceFactory
    ↓
Update task endpoint
    ↓
Tests pass
    ↓
BOT-001 SIGNALS COMPLETE
    ↓
BOT-003 Starts (waits for signal)
    ↓
Update ChatPanel
    ↓
Integrate API services
    ↓
Tests pass
    ↓
BOT-003 SIGNALS COMPLETE
    ↓
🎯 MISSION COMPLETE: All 5 bot types callable from chat
```

---

## KEY FILES

**To Create:**
- `src/deia/services/service_factory.py` (BOT-001)
- `tests/unit/test_service_factory.py` (BOT-003)

**To Modify:**
- `src/deia/services/chat_interface_app.py` (BOT-001)
- `src/deia/services/static/js/components/ChatPanel.js` (BOT-003)
- `src/deia/services/llm_service.py` (BOT-003)

---

## ARCHITECTURE OVERVIEW

```
User selects bot type & launches
    ↓
Launch endpoint stores bot_type in registry
    ↓
User sends message in chat
    ↓
ChatPanel.js calls /api/bot/{bot_id}/task
    ↓
Task endpoint:
  - Gets bot_type from registry
  - ServiceFactory.get_service(bot_type)
  - Calls service with command
    ↓
Service response:
  - CLI: subprocess output + modified files
  - API: LLM response + optional code extraction
    ↓
ChatPanel.js displays response
    ↓
User sees result
```

---

## SERVICE DETAILS

### Light Services (API-based)
- **Claude (Anthropic)**: chat() method via AnthropicService
- **ChatGPT (OpenAI)**: chat() method via OpenAIService
- **LLaMA (Ollama)**: chat() method via OllamaService

All use FileOperationService for optional markdown task file processing.

### Heavy Services (CLI-based)
- **Claude Code**: ClaudeCodeCLIAdapter spawns `claude code` subprocess
- **Codex**: CodexCLIAdapter spawns `codex` CLI subprocess

Both have full file manipulation capabilities, return tool_uses and modified file list.

---

## CRITICAL POINTS

1. **Service Factory is Single Point of Truth**
   - All service instantiation goes through factory
   - Factory handles API keys, defaults, initialization
   - Easy to add new service types

2. **Bot Type Must Be in Registry Metadata**
   - Launch endpoint stores it ✅
   - Task endpoint retrieves it
   - Display endpoints use it

3. **Two Different Response Patterns**
   - CLI: Returns raw output + modified files
   - API: Returns LLM response text

4. **FileOperationService is Optional**
   - API services CAN use it for task files
   - Not required for basic chat
   - Enables advanced markdown-based workflows

---

## TESTING STRATEGY

**BOT-001:**
- ServiceFactory creates all 5 types
- Task endpoint routes correctly
- No API errors

**BOT-003:**
- ChatPanel handles responses
- Files displayed for CLI bots
- API services integrate with FileOperationService
- All integration tests pass

**Combined:**
- User launches bot → registry has type
- User sends message → service called
- User sees response → chat updates
- Files modified → displayed to user

---

## TIMING

**Total Time:** ~85 minutes
- BOT-001: 45 min (can start immediately)
- BOT-003: 40 min (starts after BOT-001)
- Overlap: None (sequential)

**Target Completion:** ~2 hours from start

---

## SIGNALING

**BOT-001:**
When done, create `.deia/hive/responses/deiasolutions/bot-001-service-factory-done.md`
- Include: Services created, tests passing, ready for BOT-003

**BOT-003:**
When done, create `.deia/hive/responses/deiasolutions/bot-003-service-integration-done.md`
- Include: ChatPanel updated, services integrated, tests passing
- Include: All 5 bot types callable from chat interface

---

## SUCCESS DEFINITION

✅ User can:
1. Select bot type from dropdown
2. Launch bot
3. Send message/task from chat
4. Receive response from ANY of 5 service types
5. See file modifications for CLI bots
6. Use FileOperationService for task files (optional)

✅ System:
- Scales easily to new service types
- Clean separation of concerns
- Tests verify all paths
- No breaking changes to existing code

---

**READY TO EXECUTE**

BOT-001 → Start with ServiceFactory
BOT-003 → Wait for BOT-001 signal, then start

🚀 Let's make all 5 bot types work!
