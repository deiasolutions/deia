# Multi-Agent Architecture UAT Test Plan

**Date:** 2025-10-24
**Tester:** Claude Code (automated)
**Status:** IN PROGRESS

## Test Environment
- ✅ Claude Code CLI: `/c/Users/davee/AppData/Roaming/npm/claude`
- ✅ Claude Agent SDK: v0.1.4
- ✅ Python dependencies: FastAPI, uvicorn, etc.
- ✅ ANTHROPIC_API_KEY: Available

## Test Suite

### Test 1: Service Registry ⏳
**Purpose:** Verify bot discovery and port assignment
**Duration:** 2 min
**Status:** PENDING

**Steps:**
1. Import ServiceRegistry
2. Assign port to test bot
3. Register bot in registry
4. Retrieve bot info
5. Verify registry file created

**Expected Results:**
- Port assigned in range 8001-8999
- Bot registered in `.deia/hive/registry.json`
- Can retrieve bot URL

**Actual Results:**

---

### Test 2: Bot Service HTTP API ⏳
**Purpose:** Verify bot HTTP service endpoints
**Duration:** 5 min
**Status:** PENDING

**Steps:**
1. Create BotService instance
2. Start service on port 8050
3. Test /health endpoint
4. Test /status endpoint
5. Test /interrupt endpoint
6. Stop service

**Expected Results:**
- Service starts without errors
- All endpoints return 200 OK
- Status shows bot info

**Actual Results:**

---

### Test 3: Mock Bot with Service Integration ⏳
**Purpose:** Verify BotRunner + Service integration
**Duration:** 10 min
**Status:** PENDING

**Steps:**
1. Create task/response directories
2. Initialize BotRunner with mock adapter
3. Start bot (should auto-register)
4. Check registry.json has entry
5. Test HTTP endpoints
6. Run one task iteration
7. Verify bot status updates

**Expected Results:**
- Bot starts successfully
- Registers in service registry
- HTTP service responds
- Can execute mock tasks

**Actual Results:**

---

### Test 4: Claude SDK Adapter ⏳
**Purpose:** Verify official SDK integration
**Duration:** 15 min
**Status:** PENDING

**Steps:**
1. Create BotRunner with adapter_type='sdk'
2. Start bot (should initialize SDK client)
3. Check session started
4. Verify no errors in SDK initialization
5. Test adapter health check

**Expected Results:**
- SDK adapter initializes
- Session starts without errors
- Health check passes

**Actual Results:**

---

### Test 5: File-Based Task Assignment ⏳
**Purpose:** Verify file-based task queue
**Duration:** 10 min
**Status:** PENDING

**Steps:**
1. Create task file in bot's task directory
2. Run bot.run_once()
3. Verify task picked up
4. Check response file created
5. Verify task marked as processed

**Expected Results:**
- Bot finds task file
- Processes task
- Writes response file
- Task not re-processed

**Actual Results:**

---

### Test 6: HTTP Control Endpoints ⏳
**Purpose:** Verify real-time bot control
**Duration:** 5 min
**Status:** PENDING

**Steps:**
1. Start bot with service
2. Send interrupt via POST /interrupt
3. Verify bot receives signal
4. Send direct message via POST /message
5. Check bot receives message

**Expected Results:**
- Interrupt signal received
- Direct message queued
- Bot can check and clear messages

**Actual Results:**

---

## Summary

**Total Tests:** 6
**Passed:** 0
**Failed:** 0
**Pending:** 6

**Overall Status:** NOT STARTED

## Issues Found

(None yet)

## Notes

(Test execution notes here)
