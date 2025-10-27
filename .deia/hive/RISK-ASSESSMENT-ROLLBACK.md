# Risk Assessment & Rollback Procedures

**Purpose:** Identify risks during UAT and define recovery procedures
**Date:** 2025-10-26
**Version:** 1.0
**Prepared By:** BOT-001

---

## Executive Summary

This document identifies potential failures during UAT and provides rollback/recovery procedures for each risk. The goal is to ensure UAT can proceed safely with clear mitigation strategies.

---

## Risk Categories & Assessment

### Critical Risks (Abort UAT if occurs)

#### Risk CR-1: Bot Process Spawning Fails

**Description:** `/api/bot/launch` fails to spawn actual bot process

**Probability:** Medium (code is new)
**Impact:** Critical (core functionality broken)
**Severity:** P0 - Abort UAT

**Symptoms:**
- Bot appears in list but status is "unhealthy"
- Requests to bot endpoint timeout
- "Operation was aborted" error appears
- Process PID is -1 or missing

**Root Causes:**
1. `run_single_bot.py` not found in expected path
2. Python subprocess.Popen fails (permissions, environment)
3. Bot adapter fails to initialize
4. Port assignment conflict

**Detection:**
```bash
# Check if process spawned
ps aux | grep run_single_bot  # macOS/Linux
tasklist | findstr python      # Windows

# Check registry for PID
# If PID is null or -1, spawn failed
```

**Immediate Recovery:**
1. Stop UAT immediately
2. Check logs for spawn error
3. Verify `run_single_bot.py` exists
4. Check permissions on script
5. Verify PYTHONPATH includes project root

**Rollback Procedure:**
```bash
# 1. Revert to previous version (if exists)
git checkout HEAD~1 src/deia/services/chat_interface_app.py

# 2. Restart service
# Kill running service (Ctrl+C or taskkill)
python -m uvicorn src.deia.services.chat_interface_app:app --port 8000

# 3. Verify bots work with old code
curl http://localhost:8000/api/bots
```

---

#### Risk CR-2: Database Corruption

**Description:** Chat history database becomes corrupted or unreadable

**Probability:** Low (SQLite is robust)
**Impact:** Critical (data loss)
**Severity:** P0 - Abort UAT

**Symptoms:**
- "Database is locked" error
- "Disk I/O error" messages
- Chat history endpoint returns 500 error
- Messages disappear from history

**Root Causes:**
1. Multiple processes writing simultaneously (race condition)
2. Disk full condition
3. File permissions changed
4. Corrupted database file

**Detection:**
```bash
# Check database integrity
sqlite3 chat.db "PRAGMA integrity_check;"
# Expected: ok

# Check disk space
df -h | grep -E "/$|dev"
```

**Immediate Recovery:**
1. Stop service immediately
2. Backup corrupted database
3. Delete chat.db file
4. Restart service (recreates clean database)
5. Inform users: "Chat history was reset"

**Detailed Steps:**
```bash
# 1. Stop service
# Kill the running uvicorn process

# 2. Backup corrupted database
cp chat.db chat.db.corrupted.backup

# 3. Remove corrupted file
rm chat.db

# 4. Restart service
python -m uvicorn src.deia.services.chat_interface_app:app --port 8000

# 5. Verify database recreated
ls -la chat.db
sqlite3 chat.db ".schema"
```

---

#### Risk CR-3: All 5 Bots Cannot Run Concurrently

**Description:** System fails when multiple bots spawn simultaneously

**Probability:** Low (architecture tested)
**Impact:** Critical (core feature doesn't work)
**Severity:** P0 - Abort UAT

**Symptoms:**
- Launch 2nd bot hangs or fails
- Port assignment conflicts
- Process spawn fails with "Resource exhausted"
- Memory usage spikes to 100%

**Root Causes:**
1. Port range exhausted (8000-8010 insufficient)
2. Memory insufficient for 5 processes
3. File descriptor limit exceeded
4. OS process limit reached

**Detection:**
```bash
# Check available ports
netstat -ano | findstr "800[0-9]"

# Check process count
wmic process list | wc -l  # Windows
ps aux | wc -l             # macOS/Linux

# Check memory
free -h                    # Linux
vm_stat                    # macOS
```

**Immediate Recovery:**
1. Stop all launched bots
2. Stop service
3. Increase port range or process limits
4. Restart service
5. Gradually launch bots (1 at a time)

**Configuration Fix:**
```bash
# Windows: Increase process limits (if needed)
# macOS/Linux: Increase ulimits
ulimit -u 1024  # max processes
ulimit -n 4096  # max file descriptors

# Edit port configuration (if needed)
# Increase port range from 8001-8010 to 8001-8100
```

---

### High Risks (Pause UAT, fix, continue)

#### Risk HR-1: Authentication Token Expires During Test

**Description:** JWT token expires mid-UAT, breaking WebSocket connections

**Probability:** Medium (24-hour expiry, UAT < 4 hours normally)
**Impact:** High (affects all test scenarios)
**Severity:** P1 - Pause UAT

**Symptoms:**
- WebSocket connection closes with "Authentication required"
- POST requests return 401 Unauthorized
- Need to re-login

**Root Causes:**
1. Token expiry during long test session
2. System clock skew
3. Token validation too strict

**Detection:**
```bash
# Check token validity
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"dev-user","password":"dev-password"}'

# Response includes expiry time - check if < 30 min
```

**Immediate Recovery:**
1. Re-authenticate as test user
2. Get new token
3. Continue UAT
4. Consider extending token TTL for test environment

**Fix:**
```python
# In auth_service.py, increase token expiry for UAT
TOKEN_EXPIRY_HOURS = 24  # Change to 48 or 72 for UAT
```

---

#### Risk HR-2: Rate Limiting Too Strict

**Description:** Rate limiter blocks legitimate test traffic

**Probability:** Medium (limits not tuned for test scenarios)
**Impact:** High (cannot test message volume)
**Severity:** P1 - Pause UAT

**Symptoms:**
- After ~20 messages, get "429 Too Many Requests"
- Cannot send rapid test messages
- Blocking "should pass" test scenarios

**Root Causes:**
1. Rate limits set for production, not testing
2. Shared rate limit counter across test users
3. Test harness exceeds per-minute limits

**Detection:**
```bash
# Send test messages and watch for 429
for i in {1..30}; do
  curl -X POST http://localhost:8001/api/bot/TEST/task \
    -H "Content-Type: application/json" \
    -d "{\"command\":\"test $i\"}"
  echo "Message $i sent"
done
# Look for 429 responses
```

**Immediate Recovery:**
1. Wait for rate limit window to reset (1-5 minutes)
2. Continue testing with longer delays between messages
3. Or: temporarily disable rate limiting for UAT

**Fix:**
```python
# In rate_limiter_middleware.py
# For UAT, increase limits temporarily:
ENDPOINT_LIMITS = {
    "/api/bot/{bot_id}/task": (100, 60),  # 100/min instead of 20/min
    # ...
}
```

---

#### Risk HR-3: WebSocket Connection Drops

**Description:** WebSocket connections drop unexpectedly during chat

**Probability:** Medium (network/load dependent)
**Impact:** High (affects user experience)
**Severity:** P1 - Pause UAT

**Symptoms:**
- Chat UI shows "Disconnected"
- Messages not sent
- Manual reconnect required
- Intermittent failures

**Root Causes:**
1. Network instability
2. Firewall timeout
3. Server load too high
4. Client timeout configured too short

**Detection:**
```bash
# Monitor WebSocket connections
# In browser console:
console.log('WebSocket state:', ws.readyState);
// 0=CONNECTING, 1=OPEN, 2=CLOSING, 3=CLOSED
```

**Immediate Recovery:**
1. Check network connectivity
2. Refresh browser page (forces reconnect)
3. Check server load (memory/CPU)
4. Restart service if hanging

**Configuration Fix:**
```python
# In chat_interface_app.py
# Increase WebSocket keepalive timeout
WEBSOCKET_TIMEOUT = 60  # seconds (increase from 30)
```

---

#### Risk HR-4: Memory Leak Under Load

**Description:** Memory usage increases during UAT without decreasing

**Probability:** Low (code reviewed)
**Impact:** High (system becomes unstable)
**Severity:** P1 - Pause UAT

**Symptoms:**
- Memory usage steadily increases (100MB → 500MB → 1GB)
- System becomes sluggish
- Eventually runs out of memory (OOM killer)
- Service crashes

**Root Causes:**
1. Unclosed database connections
2. WebSocket handlers not cleaning up
3. Message buffers accumulating
4. Event listeners not unregistered

**Detection:**
```bash
# Monitor memory during 1-hour test
watch -n 5 'ps aux | grep python | grep chat_interface'

# Expected: stable or slightly decreasing
# Bad: steadily increasing 50MB+ per hour
```

**Immediate Recovery:**
1. Stop service and restart
2. Run garbage collection in monitoring
3. Investigate memory profiler output
4. Review recent code changes

**Profiling:**
```bash
# Run with memory profiler
pip install memory-profiler
python -m memory_profiler src/deia/services/chat_interface_app.py
```

---

### Medium Risks (Monitor, log, continue)

#### Risk MR-1: Bot Process Hangs (Doesn't Respond)

**Description:** Bot process starts but doesn't respond to requests

**Probability:** Low-Medium (adapter initialization issues)
**Impact:** Medium (affects specific bot type)
**Severity:** P2 - Monitor

**Symptoms:**
- Bot appears "ready" but requests timeout
- `/api/bot/{id}/task` returns 504 Gateway Timeout
- Process visible but consuming CPU
- Logs show adapter waiting for something

**Root Causes:**
1. Adapter initialization blocking on I/O
2. External service (LLM) unavailable
3. Deadlock in bot code
4. Infinite loop in startup

**Detection:**
```bash
# Check if process responsive
curl http://localhost:8001/health
# Should return quickly

# Check logs for errors
tail -f chat.db.log
```

**Recovery:**
1. Stop the hung bot: `POST /api/bot/stop/{bot_id}`
2. Check bot process terminated
3. Restart bot
4. If persistent, skip that bot type in UAT

---

#### Risk MR-2: Cross-Browser Incompatibility

**Description:** Chat UI doesn't work in one or more browsers

**Probability:** Medium (WebSocket support varies)
**Impact:** Medium (affects some users)
**Severity:** P2 - Monitor

**Symptoms:**
- Page loads but WebSocket fails to connect
- Chat input doesn't work
- Bot dropdown broken
- Console shows JavaScript errors

**Root Causes:**
1. WebSocket not supported in older browsers
2. CORS headers missing
3. JavaScript syntax incompatible
4. Missing polyfills

**Detection:**
```bash
# Test in Chrome, Firefox, Safari, Edge
# Open browser console (F12)
# Check for errors
# Try sending message
```

**Recovery:**
1. Document incompatible browser
2. Mark as "use Chrome" requirement
3. Or: Add polyfills if time permits
4. Continue testing with compatible browser

---

#### Risk MR-3: Performance Below Threshold

**Description:** Response times exceed 2-second target

**Probability:** Medium (depends on system load)
**Impact:** Medium (poor UX)
**Severity:** P2 - Monitor

**Symptoms:**
- Messages take 3-5 seconds to respond
- UI feels sluggish
- Users see "thinking..." for long time
- Performance degrades over time

**Root Causes:**
1. Slow LLM service
2. Database queries slow
3. Network latency
4. CPU/memory constrained

**Detection:**
```bash
# Measure response times
import time
start = time.time()
response = await call_bot_task(bot_id, command)
elapsed = time.time() - start
print(f"Response time: {elapsed:.2f}s")
```

**Recovery:**
1. Check external service performance (LLM/API)
2. Profile database queries
3. Check system resources
4. Document as known limitation
5. Optimize if time permits

---

### Low Risks (Log, acknowledge, continue)

#### Risk LR-1: Typos in Error Messages

**Description:** Error messages have spelling/grammar errors

**Probability:** High (human-written)
**Impact:** Low (cosmetic)
**Severity:** P3 - Nice to have

**Recovery:** Fix typos post-UAT

#### Risk LR-2: Missing Documentation

**Description:** Some endpoints not documented

**Probability:** Medium
**Impact:** Low (code works)
**Severity:** P3 - Nice to have

**Recovery:** Document post-UAT

#### Risk LR-3: UI Layout Issues

**Description:** Chat UI elements misaligned on some screen sizes

**Probability:** Low
**Impact:** Low (doesn't affect function)
**Severity:** P3 - Nice to have

**Recovery:** Fix styling post-UAT

---

## Abort Criteria

**STOP UAT immediately if:**

1. ❌ **CR-1 occurs:** Bot spawning completely broken
2. ❌ **CR-2 occurs:** Database corrupted and unrecoverable
3. ❌ **CR-3 occurs:** Cannot run 5 bots concurrently
4. ❌ **Multiple P1 risks** occurring simultaneously
5. ❌ **Security vulnerability** discovered
6. ❌ **Data loss** confirmed
7. ❌ **Service cannot start** after restart

**Action on Abort:**
1. Stop all testing immediately
2. Preserve logs/database for analysis
3. Revert to previous stable version
4. File incident report
5. Hold debriefing to identify root cause
6. Fix issues and restart UAT

---

## Risk Mitigation Strategies

### Before UAT
- [ ] Verify bot process spawning works (smoke test)
- [ ] Check database integrity (PRAGMA integrity_check)
- [ ] Monitor memory baseline
- [ ] Verify all 5 bots can start sequentially
- [ ] Test rate limiting with expected load
- [ ] Verify authentication tokens
- [ ] Test WebSocket reconnection

### During UAT
- [ ] Monitor memory every 30 minutes
- [ ] Monitor response times continuously
- [ ] Keep logs on screen for error visibility
- [ ] Have "stop service" procedure ready (kill switch)
- [ ] Document all issues as they occur
- [ ] Take screenshots of errors
- [ ] Record timing of failures

### Communication
- [ ] Notify stakeholders of abort decision immediately
- [ ] Provide root cause analysis
- [ ] Provide estimated time to fix
- [ ] Provide revised UAT schedule

---

## Escalation Path

**If Critical Risk Occurs:**

1. **Immediate (First 5 minutes):**
   - Stop UAT
   - Alert test coordinator
   - Preserve all logs/data

2. **Short-term (First 30 minutes):**
   - Notify BOT-001 (infrastructure lead)
   - Notify Q33N (decision maker)
   - Begin root cause analysis

3. **Medium-term (First 2 hours):**
   - Develop fix or workaround
   - Estimate resolution time
   - Decide: Fix & Retry or Abort?

4. **Long-term:**
   - Execute fix
   - Verify fix with smoke tests
   - Schedule UAT restart
   - Document lessons learned

---

## Known Limitations

*To be populated during UAT*

| Limitation | Workaround | Severity |
|------------|-----------|----------|
| (Example) Claude Code adapter requires claude CLI | Use api adapters for testing | Low |
| | | |

---

## Recovery Procedures Summary

| Risk | Detection Time | Recovery Time | Data Loss | Abort |
|------|---|---|---|---|
| CR-1: Bot spawn fails | <2 min | 15 min | No | Maybe |
| CR-2: Database corrupt | <2 min | 30 min | Yes | Yes |
| CR-3: 5 bots won't run | 10 min | 30 min | No | Yes |
| HR-1: Token expires | Variable | 2 min | No | No |
| HR-2: Rate limit strict | <5 min | 5 min | No | No |
| HR-3: WebSocket drops | Immediate | 5 min | No | No |
| HR-4: Memory leak | 30 min | 15 min | No | Maybe |
| MR-1: Bot hangs | 5 min | 10 min | No | No |

---

## Checklist Before Approval

- [ ] All risk assessment items reviewed
- [ ] Recovery procedures understood
- [ ] Abort criteria clear
- [ ] Team trained on procedures
- [ ] Logs/monitoring in place
- [ ] Kill switches documented
- [ ] Escalation contacts confirmed
- [ ] Ready to proceed with UAT

---

## Sign-Off

**Risk Assessment Approved:**
- [ ] **YES** - Proceed with UAT
- [ ] **NO** - Address risks before UAT

**Reviewed By:** _________________
**Date/Time:** _________________

---

**Document Version:** 1.0
**Last Updated:** 2025-10-26
**Next Review:** After UAT Phase 1
