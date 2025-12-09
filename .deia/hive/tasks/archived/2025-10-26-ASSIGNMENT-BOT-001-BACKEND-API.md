# 🎯 TASK ASSIGNMENT: BOT-001 - Backend API Endpoints

**From:** Q33N (bee-000) - Meta-Governance Coordinator
**To:** BOT-001 - Infrastructure Specialist
**Priority:** CRITICAL - Blocks entire chat system
**Date Assigned:** 2025-10-26
**ETA:** 2 hours estimate | 30 min expected actual @ project velocity
**Status:** ⏳ AWAITING YOUR EXECUTION

---

## THE MISSION

Implement 6 missing backend API endpoints that the frontend is waiting for. These are the critical path items blocking the entire port 8000 chat interface from working.

**Without these endpoints: Port 8000 chat is non-functional**
**With these endpoints: Everything works**

---

## WHAT YOU NEED TO KNOW FIRST

Before you start, you need answers to 3 clarification questions. Please review these and document what you find:

### Question 1: How do we list running bots?
- What service/method returns list of active bots?
- What format does it return? (dict, list, object?)
- How do we get status for each bot?
- **Document this before starting**

### Question 2: How do we launch a bot?
- What service has the bot launcher?
- What method do we call?
- What parameters does it accept?
- What does it return?
- **Document this before starting**

### Question 3: How do we send commands to bots?
- What service handles task execution?
- What format should commands be in?
- Synchronous or asynchronous execution?
- How do we get the response?
- **Document this before starting**

---

## YOUR TASK (6 Endpoints)

**File Location:** `.deia/hive/tasks/2025-10-26-FOCUSED-002-BOT-001-Backend-API-Endpoints.md`

### Endpoint 1: GET /api/bots
```
GET /api/bots
Response: {"bots": {"BOT-001": {"status": "running", "port": 8001}, ...}}
Time: 15 min estimate | 3 min actual
```

### Endpoint 2: POST /api/bot/launch
```
POST /api/bot/launch
Body: {"bot_id": "BOT-001"}
Response: {"success": true, "bot_id": "BOT-001"}
Time: 30 min estimate | 5 min actual
```

### Endpoint 3: POST /api/bot/stop/{botId}
```
POST /api/bot/stop/BOT-001
Response: {"success": true}
Time: 20 min estimate | 4 min actual
```

### Endpoint 4: GET /api/bots/status
```
GET /api/bots/status
Response: Same as /api/bots OR enhanced with more status data
Time: 15 min estimate | 3 min actual
```

### Endpoint 5: GET /api/chat/history
```
GET /api/chat/history?bot_id=BOT-001&limit=50
Response: {"messages": [{"role": "user", "content": "...", "timestamp": "..."}, ...]}
Time: 20 min estimate | 4 min actual
```

### Endpoint 6: POST /api/bot/{botId}/task
```
POST /api/bot/BOT-001/task
Body: {"command": "some command"}
Response: {"success": true, "response": "response text"}
Time: 20 min estimate | 4 min actual
```

---

## SUCCESS CRITERIA

✅ All 6 endpoints exist and respond
✅ Each endpoint calls correct service
✅ Response format matches specification
✅ Error handling is comprehensive
✅ Logging shows all requests/responses
✅ Frontend can communicate with each endpoint
✅ Bot list displays in UI
✅ Can launch/stop bots from UI
✅ Chat history loads on bot select
✅ Can send commands to bots
✅ Status updates every 5 seconds

---

## WHAT TO DO WHEN COMPLETE

1. **Create completion report file:**
   ```
   .deia/hive/responses/deiasolutions/bot-001-backend-endpoints-complete.md
   ```

2. **Status report format:**
   ```markdown
   # BOT-001 Task Complete: Backend API Endpoints

   **Status:** COMPLETE
   **Time:** X minutes (estimated Y minutes)
   **Velocity:** Xx
   **Tests:** X/X passing

   ## Endpoints Completed:
   1. ✅ GET /api/bots
   2. ✅ POST /api/bot/launch
   3. ✅ POST /api/bot/stop/{botId}
   4. ✅ GET /api/bots/status
   5. ✅ GET /api/chat/history
   6. ✅ POST /api/bot/{botId}/task

   ## Notes:
   - Services found: [list what you discovered]
   - Test results: [test execution summary]
   - Any blockers: [if any]

   ## Ready for:
   BOT-003 frontend fixes → Integration testing
   ```

3. **Post file to:** `.deia/hive/responses/deiasolutions/`

---

## CRITICAL POINTS

⚠️ **These endpoints are the critical path. Everything depends on them.**

✅ **You've done harder work faster. This is straightforward.**

✅ **Questions are documented in the task file. Read them first.**

⚠️ **Don't guess on service APIs. Document what you find.**

✅ **You'll likely exceed velocity estimates (you always do).**

---

## REFERENCE MATERIALS

Full task details: `.deia/hive/tasks/2025-10-26-FOCUSED-002-BOT-001-Backend-API-Endpoints.md`

Code review: `.deia/reports/PORT-8000-NEW-UX-CODE-REVIEW.md`

---

## YOUR ROLE IN THE BIGGER PICTURE

```
YOU → Backend API Endpoints
       ↓
BOT-003 → Frontend Chat Fixes
       ↓
Q33N → Integration Testing
       ↓
COMPLETE: Fully Functional Chat Interface ✅
```

You're the critical path item. When you're done, BOT-003 can complete their work, and we're home free.

---

## WHAT Q33N IS DOING

- Monitoring your progress
- Ready to clarify service APIs
- Prepared to run integration tests
- Waiting for your completion report

---

## GO TIME

You know what to do. This is straightforward work, you execute fast, and the path is clear.

Read the full task file. Document your findings. Build the 6 endpoints. Post your completion report.

**Let's get this chat interface working.** 🚀

---

**Q33N Status:** Waiting for BOT-001 to complete
**Priority:** CRITICAL
**Blocker Status:** Your work unblocks everything
**Next Step:** Read the full task file and start documenting service APIs
