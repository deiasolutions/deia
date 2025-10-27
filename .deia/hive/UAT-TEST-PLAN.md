# UAT Test Plan - DEIA Multi-Bot Chat System

**Date Created:** 2025-10-26
**Version:** 1.0
**Status:** Ready for Review
**Prepared By:** BOT-001

---

## Executive Summary

Comprehensive User Acceptance Testing plan for the DEIA MVP chat system with 5 bot types. This document defines all test scenarios, success criteria, and acceptance thresholds required before production deployment.

---

## Test Scope

### In Scope
- ✅ All 5 bot types (Claude, ChatGPT, Claude Code, Codex, Llama)
- ✅ Bot launch/stop lifecycle
- ✅ Chat message flow end-to-end
- ✅ Chat history persistence
- ✅ User authentication (login/register)
- ✅ Rate limiting enforcement
- ✅ WebSocket real-time communication
- ✅ Bot switching during conversation
- ✅ Error handling and graceful degradation
- ✅ Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- ✅ Multi-user concurrent sessions
- ✅ Performance under load (50+ concurrent users)

### Out of Scope
- ❌ Advanced analytics or reporting
- ❌ User management (admin panel)
- ❌ Monitoring dashboard (will be Phase 2)
- ❌ Mobile app testing
- ❌ Accessibility compliance (WCAG - Phase 2)
- ❌ Disaster recovery procedures

---

## Acceptance Criteria

### Must Pass (Critical)
- [  ] All 5 bot types launch successfully
- [  ] Chat messages send and receive correctly
- [  ] No "Operation was aborted" errors
- [  ] Authentication (login/register) functional
- [  ] Rate limiting enforced correctly
- [  ] No data loss on server restart
- [  ] WebSocket reconnection works after disconnect
- [  ] Bot process termination clean and complete

### Should Pass (Important)
- [  ] Response times < 2 seconds (95th percentile)
- [  ] Handle 50+ concurrent users without degradation
- [  ] All error messages clear and actionable
- [  ] Chat history retrieved correctly
- [  ] Bot switching doesn't lose context
- [  ] No memory leaks after 1 hour runtime

### Nice to Have (Enhancement)
- [  ] Sub-500ms response times for simple queries
- [  ] Handle 100+ concurrent users
- [  ] Graceful degradation under extreme load

---

## Pre-UAT Verification

### Environment Readiness
Before starting UAT, verify all prerequisites:

```
[ ] Database initialized (SQLite chat.db exists)
[ ] All dependencies installed (pip freeze shows all required packages)
[ ] Python 3.13+ running
[ ] Ports 8000-8010 available
[ ] run_single_bot.py executable
[ ] Service Factory working (test endpoint exists)
[ ] File paths correctly configured
```

### Service Health Check
```bash
# Start chat interface on port 8000
python -m uvicorn src.deia.services.chat_interface_app:app --host 0.0.0.0 --port 8000

# In another terminal, verify endpoints
curl http://localhost:8000/api/bots                    # Should return empty list
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"dev-user","password":"dev-password"}'  # Should return JWT token
```

---

## Test Scenarios

### Category 1: Bot Lifecycle Management

#### Test 1.1: Launch Bot - Claude (API-based)
```
GIVEN: Chat system is running
WHEN: User clicks "Launch Claude"
THEN:
  - Bot appears in bot list
  - Status shows "ready"
  - Assigned port visible (e.g., 8001)
  - No errors in console/logs
  - Process PID stored in registry
ACCEPTANCE: Success response with port and PID
```

#### Test 1.2: Launch Bot - Claude Code (CLI-based)
```
GIVEN: Chat system is running
WHEN: User clicks "Launch Claude Code"
THEN:
  - Bot appears in bot list
  - Status shows "ready"
  - Spawned Python process visible in task manager
  - Health check passes
  - Adapter type shows "cli"
ACCEPTANCE: Success response with PID and adapter_type
```

#### Test 1.3: Launch Bot - All 5 Types in Sequence
```
GIVEN: Chat system is running
WHEN: Launch Claude, ChatGPT, Claude Code, Codex, Llama (in order)
THEN:
  - All 5 bots appear in list
  - Each has unique port (8001-8005)
  - All show "ready" status
  - No port conflicts
  - No process conflicts
ACCEPTANCE: All 5 bots running concurrently
```

#### Test 1.4: Stop Bot
```
GIVEN: Bot is running with PID=12345
WHEN: User clicks "Stop Bot"
THEN:
  - Bot removed from list
  - Process terminates cleanly
  - Port released
  - No zombie processes
ACCEPTANCE: Bot fully unregistered and process killed
```

#### Test 1.5: Launch Duplicate Bot
```
GIVEN: BOT-001 is already running
WHEN: User tries to launch BOT-001 again
THEN:
  - Error: "Bot already running"
  - Original bot still running
  - No duplicate spawned
ACCEPTANCE: Error response with clear message
```

---

### Category 2: Chat Message Flow

#### Test 2.1: Send Message to Claude
```
GIVEN: Claude bot is running and selected
WHEN: User types message and hits Enter
THEN:
  - Message appears in chat (user side)
  - Request sent to /api/bot/{bot_id}/task
  - Bot processes on port 8001
  - Response received within 2 seconds
  - Response appears in chat (assistant side)
  - Message stored in database
ACCEPTANCE: Full round-trip < 2 seconds, message in database
```

#### Test 2.2: Message to Different Bot Types
```
GIVEN: All 5 bots running
WHEN: Send identical message to each bot type
THEN:
  - Each bot receives message
  - Each bot responds correctly
  - Responses differ per bot type (Claude vs GPT vs Code)
  - No cross-contamination between bots
ACCEPTANCE: All 5 bots respond correctly and independently
```

#### Test 2.3: Rapid Message Sending
```
GIVEN: Claude bot running
WHEN: User sends 10 messages in quick succession
THEN:
  - All messages queued properly
  - All responses received (some may queue)
  - No messages lost
  - Rate limiting triggered after limit (if enforced)
ACCEPTANCE: All messages processed, none lost
```

#### Test 2.4: Large Message Content
```
GIVEN: Claude bot running
WHEN: Send 10KB+ message to bot
THEN:
  - Message transmitted successfully
  - Bot processes without truncation
  - Response received fully
ACCEPTANCE: No truncation or message loss
```

---

### Category 3: Authentication & Security

#### Test 3.1: Login with Valid Credentials
```
GIVEN: User account "test-user" exists
WHEN: POST /api/auth/login with correct password
THEN:
  - Returns JWT token
  - Token valid for 24 hours
  - Token contains user_id claim
ACCEPTANCE: JWT token returned and valid
```

#### Test 3.2: Login with Invalid Password
```
GIVEN: User account "test-user" exists
WHEN: POST /api/auth/login with wrong password
THEN:
  - Returns error: "Invalid credentials"
  - No token issued
  - No account locked
ACCEPTANCE: Clear error, no token issued
```

#### Test 3.3: Register New User
```
GIVEN: Username "newuser" doesn't exist
WHEN: POST /api/auth/register with valid credentials
THEN:
  - User created
  - Can login immediately
  - Password hashed (bcrypt)
ACCEPTANCE: User registered and can authenticate
```

#### Test 3.4: WebSocket Requires Authentication
```
GIVEN: WebSocket /ws endpoint
WHEN: Connect without token
THEN:
  - Connection rejected
  - Error: "Authentication required"
ACCEPTANCE: WebSocket requires valid token
```

---

### Category 4: Data Persistence

#### Test 4.1: Chat History Persists Across Restart
```
GIVEN: 10 messages exchanged with Claude
WHEN: Restart server
THEN:
  - Database still contains 10 messages
  - Chat history API returns all 10 messages
  - No data lost
ACCEPTANCE: Messages persist across restart
```

#### Test 4.2: Per-Bot Message Isolation
```
GIVEN: 5 messages to Claude, 3 to ChatGPT
WHEN: Query /api/chat/history for Claude bot
THEN:
  - Returns 5 messages (Claude only)
  - ChatGPT messages excluded
ACCEPTANCE: Message isolation works correctly
```

#### Test 4.3: Database Integrity
```
GIVEN: 100 messages in database
WHEN: Check database file directly (sqlite3)
THEN:
  - messages table has correct schema
  - All 100 rows present
  - Timestamps correct
  - No corrupted data
ACCEPTANCE: Database integrity verified
```

---

### Category 5: Rate Limiting

#### Test 5.1: Rate Limit Enforcement
```
GIVEN: Rate limit = 20 messages/minute per user
WHEN: Send 25 messages rapidly
THEN:
  - First 20 accepted
  - 21st message rejected with 429 Too Many Requests
  - Retry-After header present
ACCEPTANCE: Rate limit enforced at correct threshold
```

#### Test 5.2: Rate Limit Reset
```
GIVEN: User hit rate limit
WHEN: Wait 60 seconds
THEN:
  - New messages accepted
  - Counter reset
ACCEPTANCE: Rate limit resets per time window
```

---

### Category 6: Error Handling

#### Test 6.1: Bot Process Crash
```
GIVEN: Bot process running
WHEN: Bot process crashes (simulated or actual)
THEN:
  - Request to bot returns error
  - User sees "Bot offline" message
  - Can attempt reconnect
  - Can stop/restart bot
ACCEPTANCE: Graceful error handling, user can recover
```

#### Test 6.2: Network Disconnect
```
GIVEN: Active chat with bot
WHEN: Network disconnected
THEN:
  - WebSocket detects disconnect
  - UI shows "Reconnecting..."
  - Auto-reconnect within 5 seconds (if network restored)
ACCEPTANCE: Graceful disconnect handling
```

#### Test 6.3: Invalid Bot ID
```
GIVEN: Chat system running
WHEN: Try to send message to non-existent bot
THEN:
  - Error: "Bot not found"
  - No crash
  - Clear error message
ACCEPTANCE: Safe error handling
```

---

### Category 7: Performance & Load

#### Test 7.1: Sub-2-Second Response Times
```
GIVEN: Simple queries (< 50 chars)
WHEN: Send 20 simple messages to Claude
THEN:
  - 95% of responses < 2 seconds
  - No responses > 5 seconds
ACCEPTANCE: 95th percentile < 2s, max < 5s
```

#### Test 7.2: Concurrent Users (50)
```
GIVEN: 50 simulated concurrent users
WHEN: Each sends 5 messages simultaneously
THEN:
  - All 250 messages processed
  - No dropped connections
  - Response times degraded < 20% vs single user
  - Server memory stable (no leak)
ACCEPTANCE: 50 concurrent users handled
```

#### Test 7.3: Memory Leak Detection
```
GIVEN: Chat system running
WHEN: Monitor memory for 1 hour, 100+ messages
THEN:
  - Memory stable or decreasing
  - No gradual increase
  - No leaked file handles
ACCEPTANCE: No memory leaks detected
```

---

### Category 8: Cross-Browser Compatibility

#### Test 8.1: Chrome/Chromium
```
GIVEN: Latest Chrome browser
WHEN: Use chat interface normally
THEN:
  - WebSocket connects
  - Messages send/receive
  - UI responsive
ACCEPTANCE: Full functionality in Chrome
```

#### Test 8.2: Firefox
```
GIVEN: Latest Firefox browser
WHEN: Use chat interface normally
THEN:
  - WebSocket connects
  - Messages send/receive
  - UI responsive
ACCEPTANCE: Full functionality in Firefox
```

#### Test 8.3: Safari
```
GIVEN: Latest Safari browser
WHEN: Use chat interface normally
THEN:
  - WebSocket connects
  - Messages send/receive
  - UI responsive
ACCEPTANCE: Full functionality in Safari
```

#### Test 8.4: Edge
```
GIVEN: Latest Edge browser
WHEN: Use chat interface normally
THEN:
  - WebSocket connects
  - Messages send/receive
  - UI responsive
ACCEPTANCE: Full functionality in Edge
```

---

## Test Execution Schedule

### Phase 1: Pre-Flight Checks (30 min)
- Verify environment readiness
- Run smoke tests
- Check all services start

### Phase 2: Bot Lifecycle (45 min)
- Tests 1.1 through 1.5
- Verify all bot types launch/stop correctly

### Phase 3: Core Chat Flow (60 min)
- Tests 2.1 through 2.4
- Verify messages send/receive correctly

### Phase 4: Security & Auth (30 min)
- Tests 3.1 through 3.4
- Verify authentication works

### Phase 5: Data Persistence (30 min)
- Tests 4.1 through 4.3
- Verify data survives restarts

### Phase 6: Rate Limiting & Error Handling (30 min)
- Tests 5.1, 5.2, 6.1, 6.2, 6.3
- Verify limits and error handling

### Phase 7: Performance Testing (60 min)
- Tests 7.1 through 7.3
- Load test and monitor performance

### Phase 8: Browser Compatibility (30 min)
- Tests 8.1 through 8.4
- Test across 4 browsers

**Total Time:** ~4 hours

---

## Success/Failure Criteria

### Overall Success
- ✅ 100% of "Must Pass" tests passing
- ✅ 80% of "Should Pass" tests passing
- ✅ No unresolved blockers
- ✅ All critical paths tested

### Acceptable to Deploy
- ✅ All Must Pass tests: PASS
- ✅ Should Pass tests: ≥ 80%
- ✅ Known issues documented and acceptable
- ✅ Rollback plan in place

### Abort Criteria (Do Not Deploy)
- ❌ Any "Must Pass" test failing
- ❌ "Operation was aborted" error appears
- ❌ Message data loss detected
- ❌ All 5 bot types cannot run concurrently
- ❌ Security vulnerability discovered
- ❌ Memory leak confirmed

---

## Test Execution Record

### Pre-Flight Checks
```
Environment Ready:        [ ] Yes [ ] No
All services start:       [ ] Yes [ ] No
Database initialized:     [ ] Yes [ ] No
Ports available:          [ ] Yes [ ] No
Smoke test passed:        [ ] Yes [ ] No

Tester: _________________ Date: _________ Time: _________
```

### Test Results Template
```
Test 1.1: Launch Bot - Claude
Result:   [ ] PASS [ ] FAIL [ ] BLOCKED
Time:     _____ seconds
Notes:    _________________________________

Test 1.2: Launch Bot - Claude Code
Result:   [ ] PASS [ ] FAIL [ ] BLOCKED
Time:     _____ seconds
Notes:    _________________________________

[... continue for all tests ...]
```

---

## Known Issues & Workarounds

*To be populated during UAT*

| Issue | Severity | Workaround | Status |
|-------|----------|-----------|--------|
| (Example) WebSocket lag on slow connection | Low | Increase timeout threshold | Documented |
| | | | |

---

## Sign-Off

For UAT to proceed, this plan must be reviewed and approved by:

- [ ] User/Product Owner - Confirms scope and acceptance criteria
- [ ] QA Lead - Confirms test coverage and feasibility
- [ ] DevOps/Infra - Confirms environment readiness
- [ ] Development - Confirms known limitations

---

## Appendix: Test Environment Setup

### Required Tools
- Python 3.13+
- pytest (for unit tests)
- curl (for API testing)
- Browser (Chrome/Firefox/Safari/Edge)
- Database browser (optional, for SQLite inspection)

### Sample Test Scripts
```bash
# Test bot launch
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id":"TEST-BOT","bot_type":"claude"}'

# Test authentication
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"dev-user","password":"dev-password"}'

# Test rate limiting
for i in {1..25}; do
  curl -X POST http://localhost:8001/api/bot/TEST-BOT/task \
    -H "Content-Type: application/json" \
    -d "{\"command\":\"test $i\"}"
done
```

---

**Document Version:** 1.0
**Last Updated:** 2025-10-26
**Next Review:** After Phase 1 completion
