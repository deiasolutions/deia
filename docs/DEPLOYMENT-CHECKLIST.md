# DEIA Production Deployment Checklist

**Version:** 1.0
**Last Updated:** 2025-10-25
**Status:** Production Ready

---

## Pre-Deployment Phase (1-2 hours before launch)

### 1. Environment Setup

- [ ] Verify Python 3.9+ installed: `python --version`
- [ ] Verify Ollama running: `curl http://localhost:11434/api/tags`
- [ ] Check disk space available: `df -h` (recommend 10GB+ free)
- [ ] Check system memory: `free -h` or `vm_stat` (recommend 8GB+ free)
- [ ] Verify network connectivity: `ping -c 3 8.8.8.8`

### 2. Code Preparation

- [ ] Pull latest code: `git pull origin main`
- [ ] Install/update dependencies: `pip install -r requirements.txt`
- [ ] Run pre-deployment tests: `pytest tests/ -v --cov`
- [ ] Check code style: `flake8 src/`
- [ ] Verify imports: `python -c "import deia; print(deia.__version__)"`

### 3. Configuration

- [ ] Copy production config: `cp .deia/config/production.yaml bot-config.yaml`
- [ ] Customize for environment:
  - [ ] Adjust bot_limits (min/max bots)
  - [ ] Set timeout values appropriate for your workload
  - [ ] Configure feature flags (enable/disable as needed)
  - [ ] Set custom application settings
- [ ] Validate config: `python -c "from deia.services.config_manager import ConfigManager; ConfigManager('.').load_config('bot-config')"`
- [ ] No hardcoded secrets in config files

### 4. Data Directory Setup

- [ ] Create state directory: `mkdir -p .deia/state`
- [ ] Create logs directory: `mkdir -p .deia/bot-logs`
- [ ] Create backups directory: `mkdir -p .deia/backups`
- [ ] Set proper permissions: `chmod 750 .deia/`
- [ ] Verify directories exist: `ls -la .deia/`

### 5. Logging Setup

- [ ] Configure log rotation (logrotate or similar)
- [ ] Set up log aggregation if using one
- [ ] Verify log directory is writable: `touch .deia/bot-logs/test.log && rm .deia/bot-logs/test.log`
- [ ] Test audit logging: See DEPLOYMENT-CHECKLIST.md Task 5

---

## Startup Phase (15-30 minutes)

### 6. System Startup

- [ ] Start Ollama (if not already running): `ollama serve`
- [ ] Start bot service: `python run_single_bot.py --bot-id main-bot --port 8001`
- [ ] Wait 10 seconds for service to initialize
- [ ] Verify service is running: `curl http://localhost:8001/health`
- [ ] Check service logs: `tail -f .deia/bot-logs/main-bot-activity.jsonl`

### 7. Health Checks

- [ ] Health endpoint responds: `curl http://localhost:8001/health`
- [ ] Status endpoint responds: `curl http://localhost:8001/status`
- [ ] Messaging endpoint available: `curl http://localhost:8001/api/messaging/inbox`
- [ ] Orchestration endpoint available: `curl http://localhost:8001/api/orchestrate/status`
- [ ] Dashboard endpoint available: `curl http://localhost:8001/api/dashboard/health`

### 8. Configuration Verification

- [ ] Config loaded successfully: Check logs for "Config loaded" message
- [ ] Default values applied: Verify in status endpoint
- [ ] Feature flags active: Check dashboard health endpoint
- [ ] Thresholds configured: Monitor health alerts

### 9. Default Fallbacks

- [ ] Missing config file → Uses defaults: Rename config, restart, verify still works
- [ ] Invalid config value → Uses fallback: Set invalid threshold, verify fallback used
- [ ] Missing directory → Created automatically: Check state/logs/backups created
- [ ] Config hot-reload: Modify config while running, verify updates applied within 5 minutes

---

## Integration Phase (15-30 minutes)

### 10. External Connections

- [ ] Ollama connection works: `curl http://localhost:11434/api/tags`
- [ ] Can list available models: Verify models returned
- [ ] Bot can submit tasks: `curl -X POST http://localhost:8001/api/orchestrate -d '...'`
- [ ] Messages can be sent: `curl -X POST http://localhost:8001/message -d '...'`

### 11. Database/State

- [ ] State files created: `ls -la .deia/state/`
- [ ] Backup created: `ls -la .deia/backups/`
- [ ] No errors in state loading: Check logs
- [ ] Task queue persisted: Verify task files exist

### 12. Monitoring

- [ ] Health monitor activated: Check for "health_check" in logs
- [ ] Resource monitoring active: Check CPU/memory stats in logs
- [ ] Scaling evaluation running: Check for "scaling_evaluation" entries
- [ ] Alert system functional: Set CPU threshold low, verify alert in logs

---

## Validation Phase (10-15 minutes)

### 13. Critical Path Testing

- [ ] Task submission works: POST `/api/orchestrate` with sample task
- [ ] Task routing works: Verify task routed to bot
- [ ] Message delivery works: Send bot-to-bot message
- [ ] Health monitoring works: Check `/api/dashboard/health` endpoint
- [ ] Adaptive scheduling works: Submit multiple similar tasks, verify routing

### 14. Error Handling

- [ ] Invalid request rejected: POST malformed JSON to `/api/orchestrate`
- [ ] Rate limiting works: Send 1000+ requests/min, verify throttled
- [ ] Graceful degradation: Stop Ollama, verify system degrades gracefully
- [ ] Recovery from failure: Restart Ollama, verify system recovers

### 15. Audit & Security

- [ ] Audit logging active: Check `.deia/bot-logs/audit.jsonl`
- [ ] No credentials in logs: `grep -r "password\|token\|key" .deia/bot-logs/ | wc -l` (should be 0)
- [ ] Request validation active: Verify dangerous patterns blocked
- [ ] Bot authentication working: Verify bot signatures validated

---

## Production Handoff Phase (5-10 minutes)

### 16. Documentation

- [ ] Deployment checklist completed (this document)
- [ ] Configuration guide reviewed: See CONFIGURATION-GUIDE.md
- [ ] Troubleshooting guide available: See TROUBLESHOOTING.md
- [ ] Runbooks documented: See RUNBOOKS.md
- [ ] Team trained on deployment: All operators know this checklist

### 17. Monitoring Setup

- [ ] Alerts configured: CPU, memory, queue depth, failure rate
- [ ] Log aggregation active: Logs flowing to central system
- [ ] Dashboard accessible: Status visible to team
- [ ] On-call rotation: Team knows escalation path

### 18. Backup & Recovery

- [ ] Backups running automatically: Verify backup files created every 10 min
- [ ] Backup restore tested: Restore from backup, verify data integrity
- [ ] Recovery time documented: Note RTO/RPO
- [ ] Disaster recovery plan: Team reviewed recovery procedures

### 19. Final Checks

- [ ] All tests passing: `pytest tests/ -v`
- [ ] No errors in logs: `grep ERROR .deia/bot-logs/*.jsonl | wc -l` (should be 0)
- [ ] System under steady load: Monitor CPU, memory, queue depth
- [ ] Team ready to support: On-call team briefed and ready
- [ ] Sign-off obtained: Approver confirms readiness

### 20. Launch

- [ ] Green light received from team lead
- [ ] System monitoring active: Dashboard watched
- [ ] On-call team standing by: Ready for issues
- [ ] Deployment logged: Document timestamp, who deployed, what version
- [ ] Success notification: Team notified of go-live

---

## Post-Deployment Phase (Ongoing)

### 21. First 24 Hours

- [ ] Monitor error rates: Should be <0.1%
- [ ] Monitor latency: Task routing should be <10ms
- [ ] Monitor throughput: System at expected load
- [ ] Monitor resource usage: CPU/memory stable
- [ ] Review logs hourly: Catch any issues early

### 22. First Week

- [ ] No unplanned restarts: System stability verified
- [ ] Backups verified: Restore tests successful
- [ ] Monitoring dashboards useful: Team comfortable with tools
- [ ] Performance stable: No degradation over time
- [ ] Team competency verified: Operators can handle issues

---

## Rollback Procedures

If critical issues occur:

1. **Stop new task submission:** Set scaling.max_bots = 0
2. **Wait for in-flight tasks:** Monitor orchestration status
3. **Shut down system:** `pkill -f "python run_single_bot.py"`
4. **Restore from backup:** `cp .deia/backups/state-{timestamp}.tar.gz .deia/ && tar -xzf`
5. **Restart with previous version:** `git checkout previous-version && python run_single_bot.py`
6. **Verify recovery:** Run health checks from section 7
7. **Notify team:** Document incident and recovery time

---

## Success Criteria

System is production-ready when:

- ✅ All pre-deployment checks pass
- ✅ All startup health checks pass
- ✅ All integration tests pass
- ✅ All critical path tests pass
- ✅ Error handling tested and verified
- ✅ Audit logging verified
- ✅ Backups verified
- ✅ Monitoring active
- ✅ Team trained and ready
- ✅ Sign-off obtained

---

**Status:** ✅ PRODUCTION READY

**Last Verified:** 2025-10-25 16:19 CDT
**Verified By:** BOT-001 (Infrastructure Lead)

For questions or issues, see TROUBLESHOOTING.md or contact the on-call engineer.
