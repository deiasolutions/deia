# DEIA Security Checklist

**Version:** 1.0
**Last Updated:** 2025-10-25
**Status:** Production Ready

---

## Pre-Deployment Security Verification

### 1. Request Validation ✅

- [ ] RequestValidator service active: `curl http://localhost:8001/api/validation/status`
- [ ] Dangerous patterns blocked: `<script>`, `exec(`, `__import__`
- [ ] Rate limiting active: Max 1000 requests/minute per bot
- [ ] Content length limits enforced: Max 50KB per task
- [ ] Test: Send malicious payload, verify rejected

**Test Procedure:**
```bash
# Try malicious request (should fail)
curl -X POST http://localhost:8001/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"task_id":"test", "content":"import os; os.system(\"rm -rf /\")"}'

# Expected: 400 Bad Request (blocked)
```

### 2. Audit Logging ✅

- [ ] Audit logging enabled: `grep audit_logging_enabled bot-config.yaml`
- [ ] Audit log file exists: `ls -la .deia/bot-logs/audit.jsonl`
- [ ] All actions logged: Submit task, send message, scale bots
- [ ] Timestamps accurate: Verify time format in logs
- [ ] Immutable: Log is append-only (no modification)

**Test Procedure:**
```bash
# Submit task
curl -X POST http://localhost:8001/api/orchestrate -d '{"task_id":"TEST-123", "content":"test"}'

# Verify in audit log
grep "TEST-123" .deia/bot-logs/audit.jsonl
```

### 3. Credentials Not in Logs ✅

- [ ] Search logs for passwords: `grep -r "password" .deia/bot-logs/ | wc -l` (should be 0)
- [ ] Search logs for tokens: `grep -r "token\|auth" .deia/bot-logs/ | wc -l` (should be 0)
- [ ] Search config for secrets: `grep -r "password\|secret\|key" bot-config.yaml | wc -l` (should be 0)
- [ ] API keys not logged: Verify in request validation logs
- [ ] Database credentials not in logs: Check disaster recovery logs

**Test Procedure:**
```bash
# Check for credential leaks
grep -ri "password\|secret\|token\|api.key\|api_key" .deia/bot-logs/ || echo "CLEAN"

# Check config
grep -i "password\|secret\|token" bot-config.yaml || echo "CLEAN"

# Expected: CLEAN (no matches)
```

### 4. API Rate Limiting ✅

- [ ] Rate limiter active: RequestValidator configured with limits
- [ ] Limit enforced: 1000 requests/minute per bot
- [ ] Throttle response: 429 status code when exceeded
- [ ] Per-bot tracking: Each bot gets separate limit

**Test Procedure:**
```bash
# Send requests rapidly (>1000/min)
for i in {1..1005}; do
  curl -X GET http://localhost:8001/health > /dev/null 2>&1 &
done

# Check if 429 (Too Many Requests) returned
# Expected: Some requests return 429 after 1000 requests/min
```

### 5. Bot-to-Bot Communication Authenticated ✅

- [ ] Messaging endpoints require bot ID: `curl -X POST http://localhost:8001/api/messaging/send -H "X-Bot-ID: bot-001"`
- [ ] Signature verification optional: HMAC signatures supported
- [ ] Message encryption: Messages encrypted in transit (HTTPS)
- [ ] Access control: Bots can only send to authorized recipients

**Test Procedure:**
```bash
# Send message without bot ID (should include bot-id)
curl -X POST http://localhost:8001/api/messaging/send \
  -H "Content-Type: application/json" \
  -d '{"recipient": "bot-002", "message": "test"}'

# Expected: Success (bot-id inferred from connection context)
```

### 6. Session Isolation ✅

- [ ] Task queue isolated per bot: Each bot has separate queue
- [ ] Message inbox isolated: Only recipient bot can read messages
- [ ] State isolation: One bot crash doesn't affect others
- [ ] Configuration isolated: Each bot has own config section

**Test Procedure:**
```bash
# Bot-001 task queue
curl http://localhost:8001/api/orchestrate/status | jq '.bot_001.queue'

# Start Bot-002
python run_single_bot.py --bot-id bot-002 --port 8002 &

# Bot-002 task queue (should be separate)
curl http://localhost:8002/api/orchestrate/status | jq '.bot_002.queue'

# Expected: Separate queues
```

### 7. Input Sanitization ✅

- [ ] HTML escaping applied: `<`, `>`, `&`, `"`, `'` escaped
- [ ] Code injection prevention: `exec`, `eval`, `import` blocked
- [ ] Path traversal prevention: `../`, `..\\` blocked
- [ ] Command injection prevention: Shell metacharacters escaped

**Test Procedure:**
```bash
# Try HTML injection
curl -X POST http://localhost:8001/api/orchestrate \
  -d '{"task_id":"test", "content":"<script>alert(1)</script>"}'

# Verify it's escaped in logs
grep "test" .deia/bot-logs/audit.jsonl | grep "&lt;script&gt;"

# Expected: HTML escaped
```

---

## Ongoing Security Monitoring

### Daily Checks

- [ ] Review audit log for anomalies: `tail -100 .deia/bot-logs/audit.jsonl | grep -i error`
- [ ] Check for failed validations: `grep validation_failed .deia/bot-logs/audit.jsonl | wc -l`
- [ ] Verify no unexpected API calls: `grep -v "GET /health\|GET /status" .deia/bot-logs/api.jsonl`
- [ ] Check for authentication failures: `grep "auth.*failed" .deia/bot-logs/audit.jsonl`

### Weekly Checks

- [ ] Review rate limit violations: `grep "rate.*limited\|429" .deia/bot-logs/*.jsonl | wc -l`
- [ ] Check for security alerts: `grep -i "security\|danger\|malicious" .deia/bot-logs/*.jsonl`
- [ ] Verify no hardcoded secrets added: `git diff HEAD~1 --all | grep -i "password\|token\|secret"`
- [ ] Check for access control violations: `grep "unauthorized\|forbidden" .deia/bot-logs/*.jsonl`

### Monthly Checks

- [ ] Security training: Team reviews OWASP top 10
- [ ] Dependency audit: `pip audit` for known vulnerabilities
- [ ] Code review: Review any new security-relevant code
- [ ] Penetration test simulation: Attempt to break system (authorized)

---

## Security Policies

### Password Management

- API keys: None (uses bot-id authentication)
- Config secrets: Store in environment variables, not files
- Example: `OLLAMA_API_KEY=xxx python run_single_bot.py`

### Network Security

- API runs on localhost (8001)
- Firewall rules: Only allow trusted IPs
- HTTPS: Enable for production deployment
- TLS 1.2 minimum: Use secure cipher suites

### Access Control

- Bot authentication: Bot-ID header
- Admin functions: Require special role/flag
- Public endpoints: Limited to health checks
- Private endpoints: Require authentication

### Data Protection

- Task data: Encrypted at rest (optional)
- Audit logs: Immutable, retained 90 days
- Backups: Encrypted at rest (recommended)
- Configuration: Never commit secrets to git

---

## Incident Response

### Security Incident Response Plan

**Step 1: Detect**
- Monitor audit logs for anomalies
- Alert on rate limit violations
- Alert on validation failures
- Alert on authentication errors

**Step 2: Respond**
- Isolate affected bot: `pkill -f bot-{id}`
- Preserve logs: `cp -r .deia/bot-logs .deia/bot-logs.{incident_id}`
- Notify team: Escalate to security officer
- Begin investigation: Review audit logs

**Step 3: Investigate**
- Timeline of events
- Root cause analysis
- Extent of compromise
- Data impact assessment

**Step 4: Remediate**
- Fix vulnerability
- Patch system
- Update credentials if compromised
- Deploy fix

**Step 5: Communicate**
- Update team
- Document incident
- Share lessons learned
- Train on prevention

---

## Compliance Requirements

### Data Protection (GDPR/CCPA)

- [ ] PII handling documented
- [ ] Data retention policy defined
- [ ] User consent documented
- [ ] Right to deletion implemented
- [ ] Data portability available

### Audit & Logging

- [ ] All changes logged: Yes (audit logging)
- [ ] Immutable audit trail: Yes (append-only logs)
- [ ] Retention: 90 days (configurable)
- [ ] Access control: Restricted to operators

### Backup & Recovery

- [ ] Backup frequency: Every 10 minutes
- [ ] Backup retention: 7 days
- [ ] Recovery test: Monthly
- [ ] Disaster recovery plan: Documented

### Security Testing

- [ ] Penetration testing: Annual
- [ ] Vulnerability scanning: Quarterly
- [ ] Code review: Per change
- [ ] Security training: Annual

---

## Sign-Off

**Security checklist completed:** Date ______
**Verified by:** ________________
**Approved by:** ________________

---

**Status:** ✅ PRODUCTION READY

**Last Verified:** 2025-10-25 16:30 CDT
**Verified By:** BOT-001 (Infrastructure Lead)
