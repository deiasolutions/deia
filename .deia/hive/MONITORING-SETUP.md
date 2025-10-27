# UAT Monitoring & Observability Setup

**Purpose:** Provide visibility into system behavior during UAT testing
**Date:** 2025-10-26
**Version:** 1.0
**Prepared By:** BOT-001

---

## Quick Start

### 1-Minute Setup
Run these 3 commands in separate terminals before starting UAT:

```bash
# Terminal 1: Start service
python -m uvicorn src.deia.services.chat_interface_app:app \
  --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Monitor system resources
watch -n 2 'ps aux | grep python'  # macOS/Linux
# OR
wmic process get name,processid,usermodetime,kerneltime  # Windows

# Terminal 3: Watch logs
tail -f chat.log
```

---

## Monitoring Dashboards & Tools

### Dashboard 1: Service Health (Browser)

Open this URL in browser (keep visible during testing):
```
http://localhost:8000/api/bots
```

**What to observe:**
- Bot count (should increase as you launch bots)
- Bot status (ready, starting, unhealthy)
- Port assignments (8001, 8002, etc.)
- Timestamps (when last updated)

**Warning signs:**
- ❌ Bots stuck in "starting" status (>10 seconds)
- ❌ All bots showing "unhealthy"
- ❌ Port numbers > 8010 (port range exhausted)
- ❌ Timestamps not updating (service hung)

---

### Dashboard 2: System Resources (Terminal)

#### Option A: Real-time Monitor (macOS/Linux)
```bash
watch -n 2 'ps aux | grep -E "python|uvicorn" | grep -v grep'
```

**Columns to watch:**
- `%CPU`: Should stay < 50% at idle, spike to 100% during messages
- `%MEM`: Should stay < 5% at idle, max 20% under load
- `STAT`: Should be `S` (sleeping) or `R` (running), never `Z` (zombie)
- `TIME`: Should increase gradually (not jumping)

#### Option B: Continuous Monitor (Windows)
```bash
# Requires Windows Terminal or PowerShell
Get-Process python | Format-Table -AutoSize -Repeat
# Wait 2-3 seconds between runs
```

#### Option C: Memory Profiler
```bash
pip install psutil
python -c "
import psutil
import time
p = psutil.Process()
while True:
    mem = p.memory_info()
    print(f'Memory: {mem.rss / 1024 / 1024:.1f} MB, CPU: {p.cpu_percent():.1f}%')
    time.sleep(5)
"
```

**Expected baseline:**
- Idle memory: 100-200 MB
- Idle CPU: < 1%
- After 100 messages: 150-300 MB
- After 1 hour: Same as baseline (no leak)

**Warning signs:**
- ❌ Memory > 500 MB at idle
- ❌ CPU > 80% when idle
- ❌ Memory constantly increasing 10MB+/minute
- ❌ Process count growing (zombie processes)

---

### Dashboard 3: Server Logs (Terminal)

```bash
# Watch logs in real-time
tail -f chat.log

# OR search for errors
tail -f chat.log | grep -i error

# OR watch specific pattern
tail -f chat.log | grep -i "bot\|launch\|stop"
```

**Log levels to watch:**

- `INFO`: Normal operations (expected)
- `WARNING`: Degraded state (monitor)
- `ERROR`: Problem occurred (investigate)
- `CRITICAL`: System failure (stop and fix)

**Examples:**
```
✓ INFO: Bot BOT-001 spawned with PID 12345
✓ INFO: Health check passed for BOT-001
⚠ WARNING: Bot BOT-001 health check timeout
❌ ERROR: Failed to spawn bot process
❌ CRITICAL: Database connection lost
```

---

### Dashboard 4: Response Times (Browser Console)

While in browser chat UI, open console (F12) and paste:

```javascript
// Measure response times
const originalFetch = window.fetch;
window.fetch = async function(...args) {
  const start = performance.now();
  const response = await originalFetch(...args);
  const elapsed = performance.now() - start;
  console.log(`${args[0]}: ${elapsed.toFixed(0)}ms`);
  return response;
};
```

**What to watch:**
- Simple queries: < 1000ms (1 second)
- Complex queries: < 2000ms (2 seconds)
- Max allowed: < 5000ms (5 seconds)

**Track:**
- Average response time
- 95th percentile (95% of requests)
- Max response time (slowest)

---

### Dashboard 5: Database Health (Terminal)

```bash
# Check database size
ls -lah chat.db

# Check database integrity
sqlite3 chat.db "PRAGMA integrity_check;"
# Expected: ok

# Count messages
sqlite3 chat.db "SELECT COUNT(*) FROM messages;"

# Monitor in real-time
watch -n 5 'echo "Message count:"; sqlite3 chat.db "SELECT COUNT(*) FROM messages;"'
```

**Expected:**
- File size grows with messages (~5KB per 100 messages)
- Integrity check always returns "ok"
- Message count increases during tests

**Warning signs:**
- ❌ Integrity check returns error
- ❌ Cannot read database file
- ❌ File size decreasing (data loss)
- ❌ Message count not increasing (not storing)

---

### Dashboard 6: WebSocket Connections (Browser Console)

In browser chat UI console:

```javascript
// Monitor WebSocket connections
const ws = document.querySelector('ws') || window.ws;
console.log('WebSocket state:', {
  readyState: ws?.readyState,  // 0=CONNECTING, 1=OPEN, 2=CLOSING, 3=CLOSED
  url: ws?.url,
  protocol: ws?.protocol,
  bufferedAmount: ws?.bufferedAmount
});

// Monitor connection events
if (ws) {
  ws.addEventListener('open', () => console.log('WS: Connected'));
  ws.addEventListener('close', () => console.log('WS: Closed'));
  ws.addEventListener('error', (e) => console.log('WS: Error', e));
}
```

**Expected:**
- `readyState`: 1 (OPEN)
- `bufferedAmount`: 0 (no queued messages)
- No error events

**Warning signs:**
- ❌ `readyState`: 0 for > 5 seconds (connection stuck)
- ❌ `readyState`: 3 (closed unexpectedly)
- ❌ `bufferedAmount`: Growing continuously
- ❌ Repeated error events

---

## Monitoring Checklist During Testing

### Every 15 Minutes
- [ ] Check bot status in `/api/bots` (should all be "ready")
- [ ] Check memory usage (should be stable)
- [ ] Glance at logs (no error patterns)
- [ ] Verify response times reasonable

### Every 30 Minutes
- [ ] Record memory snapshot
- [ ] Check database integrity (`PRAGMA integrity_check`)
- [ ] Count total messages (`SELECT COUNT(*)`)
- [ ] Review error log summary

### Hourly
- [ ] Full memory profile
- [ ] Database backup
- [ ] Generate resource report
- [ ] Stakeholder check-in

### On Any Error
- [ ] Screenshot the error
- [ ] Save relevant logs
- [ ] Note exact time
- [ ] Reproduce if possible
- [ ] Log in issue tracker

---

## Performance Measurement

### Baseline (Before Testing)
```bash
# Capture baseline metrics
echo "=== BASELINE METRICS ===" > metrics.txt
echo "Time: $(date)" >> metrics.txt
ps aux | grep python >> metrics.txt
echo "" >> metrics.txt
echo "Database: $(ls -lah chat.db)" >> metrics.txt
echo "Messages: $(sqlite3 chat.db 'SELECT COUNT(*) FROM messages;')" >> metrics.txt
```

### During Testing
```bash
# Measure every 30 minutes
echo "=== 30-MIN CHECKPOINT ===" >> metrics.txt
echo "Time: $(date)" >> metrics.txt
ps aux | grep python >> metrics.txt
# ... (same as above)
```

### Response Time Tracking
Create `response-times.csv`:
```
timestamp,endpoint,response_time_ms,status
2025-10-26T09:15:00,/api/bot/launch,450,success
2025-10-26T09:15:05,/api/bot/BOT-001/task,1200,success
2025-10-26T09:15:10,/api/bots,120,success
```

**Track:**
- Minimum time
- Maximum time
- Average time
- P95 (95th percentile)
- P99 (99th percentile)

---

## Alert Conditions

### RED ALERTS (Stop Testing Immediately)
```
[ ] Memory > 1GB
[ ] Process crash/exit
[ ] Database error
[ ] Service unresponsive (> 30s no response)
[ ] WebSocket closes unexpectedly
[ ] Spawn process fails
[ ] Message not stored in database
```

### YELLOW ALERTS (Monitor Closely)
```
[ ] Memory > 500MB
[ ] Response time > 5 seconds
[ ] CPU > 80% sustained
[ ] Multiple timeouts
[ ] Health check failing intermittently
[ ] WebSocket disconnects (with reconnect)
```

### GREEN ALERTS (Normal Operations)
```
[ ] Memory 150-300MB
[ ] Response time < 2 seconds
[ ] CPU < 50%
[ ] All services responding
[ ] Health checks passing
[ ] Database stable
```

---

## Real-Time Monitoring Dashboard (Advanced)

If you have `watch` command available, use this:

```bash
watch -n 3 '
echo "=== SYSTEM STATUS ===" ;
echo "Time: $(date)" ;
echo "" ;
echo "=== PROCESSES ===" ;
ps aux | grep python | grep -v grep | awk "{print \$2, \$3\"%CPU\", \$4\"%MEM\", \$11}" ;
echo "" ;
echo "=== DATABASE ===" ;
echo "Messages: $(sqlite3 chat.db \"SELECT COUNT(*) FROM messages;\")" ;
echo "Size: $(ls -lh chat.db | awk \"{print \$5}\")" ;
echo "" ;
echo "=== BOTS ===" ;
curl -s http://localhost:8000/api/bots | jq ".bots | length" ;
'
```

---

## Log Analysis Tips

### Find patterns
```bash
# Find all errors
grep ERROR chat.log

# Find bot launch events
grep "spawn\|launch\|ready" chat.log

# Find timeouts
grep -i "timeout\|500\|504" chat.log

# Find by time
grep "09:15" chat.log
```

### Count occurrences
```bash
# How many errors?
grep ERROR chat.log | wc -l

# How many bots launched?
grep "spawned" chat.log | wc -l

# How many messages?
sqlite3 chat.db "SELECT COUNT(*) FROM messages;"
```

---

## Creating a Monitoring Report

At end of each testing phase, generate:

```bash
# System resources report
echo "=== PHASE X MONITORING REPORT ===" > phase_X_report.txt
echo "Duration: [start time] to [end time]" >> phase_X_report.txt
echo "Messages processed: $(sqlite3 chat.db 'SELECT COUNT(*) FROM messages;')" >> phase_X_report.txt
echo "Memory peak: [highest MB observed]" >> phase_X_report.txt
echo "Response time (avg/p95/max): [values]" >> phase_X_report.txt
echo "Errors encountered: [count]" >> phase_X_report.txt
echo "Database integrity: OK" >> phase_X_report.txt
```

---

## Troubleshooting Monitoring Issues

### "Cannot open logs"
```bash
# Ensure logs are being written
ls -la chat.log
# If missing, create it
touch chat.log

# Redirect service output
python -m uvicorn ... > chat.log 2>&1
```

### "Database locked"
```bash
# Close other connections
# Check what's using it
lsof | grep chat.db
kill -9 <pid>
```

### "Port already in use"
```bash
# Find what's using it
lsof -i :8000
netstat -ano | findstr :8000
# Kill it
kill -9 <pid>
```

### "Cannot connect to service"
```bash
# Verify service is running
curl http://localhost:8000/api/bots

# Check if port is open
telnet localhost 8000
# OR
nc -zv localhost 8000
```

---

## Monitoring Checklist

Before starting UAT, ensure:

- [ ] Logging configured and working
- [ ] Database monitoring tools ready
- [ ] System monitoring active
- [ ] Response time tracking set up
- [ ] All dashboards tested and accessible
- [ ] Team knows how to read metrics
- [ ] Alert procedures defined
- [ ] Escalation contacts documented

---

## Document Management

**Pre-UAT:**
- Save this document
- Share with monitoring team
- Conduct walkthrough
- Practice 1-2 times

**During UAT:**
- Keep terminals visible
- Take screenshots of metrics
- Save logs/database periodically
- Document all observations

**Post-UAT:**
- Archive metrics
- Analyze trends
- Generate final report
- Identify optimization opportunities

---

**Document Version:** 1.0
**Last Updated:** 2025-10-26
**Distribution:** QA/Testing Team, DevOps, Development
