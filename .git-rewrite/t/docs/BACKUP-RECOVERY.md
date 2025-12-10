# DEIA Backup & Recovery Guide

**Version:** 1.0
**Last Updated:** 2025-10-25
**Status:** Production Ready

---

## Overview

DEIA automatically creates backups every 10 minutes. Backups are retained for 7 days. In case of data loss or system failure, you can restore from backup in minutes.

---

## Automatic Backups

### How It Works

Every 10 minutes (configurable), the system creates a backup:

```
Backup Process:
1. Snapshot current state
2. Compress to `.deia/backups/state-{timestamp}.tar.gz`
3. Verify integrity
4. Log backup event
5. Clean old backups (>7 days)
```

### Backup Location

```
.deia/backups/
  ├── state-2025-10-25-16-00-00.tar.gz  (1.2 MB)
  ├── state-2025-10-25-16-10-00.tar.gz  (1.2 MB)
  ├── state-2025-10-25-16-20-00.tar.gz  (1.2 MB)
  └── ...
```

### What's Backed Up

- Task queue and history
- Bot assignments and state
- Chat history
- Audit logs
- Configuration (non-sensitive)
- Performance metrics

### Configuration

In `bot-config.yaml`:

```yaml
persistence:
  backup_enabled: true
  backup_interval_minutes: 10      # Backup every 10 min
  backup_retention_days: 7          # Keep for 7 days
```

---

## Verify Backups Are Working

### Check Backup Directory

```bash
# List backups (should have multiple)
ls -lh .deia/backups/

# Expected output:
# -rw-r--r-- state-2025-10-25-16-00-00.tar.gz  (1.2M)
# -rw-r--r-- state-2025-10-25-16-10-00.tar.gz  (1.2M)
# -rw-r--r-- state-2025-10-25-16-20-00.tar.gz  (1.2M)
```

### Check Backup Logs

```bash
# View backup events
tail -20 .deia/bot-logs/backup.jsonl

# Expected entries:
# {"timestamp": "...", "event": "backup_created", "file": "state-...tar.gz", "size_mb": 1.2}
# {"timestamp": "...", "event": "backup_verified", "file": "state-...tar.gz", "success": true}
```

### Check Backup Frequency

```bash
# Count backups from last hour
ls -l .deia/backups/state-*.tar.gz | wc -l

# Should be 6 (one every 10 minutes)
```

---

## Manual Backup

To create backup on-demand:

```bash
# Trigger backup (if API available)
curl -X POST http://localhost:8001/api/backup/now

# Or manually create backup
tar -czf .deia/backups/state-manual-$(date +%s).tar.gz .deia/state/
```

---

## Restore from Backup

### Quick Restore (No Data Loss)

If system is running and you want to restore to a previous point:

```bash
# 1. List available backups
ls -l .deia/backups/state-*.tar.gz

# 2. Stop system
pkill -f "python run_single_bot.py"

# 3. Backup current state (just in case)
cp -r .deia/state .deia/state.current

# 4. Extract backup
tar -xzf .deia/backups/state-2025-10-25-16-00-00.tar.gz -C .deia/

# 5. Restart system
python run_single_bot.py --bot-id main-bot --port 8001

# 6. Verify restoration
curl http://localhost:8001/status
```

### Full System Restore (From Scratch)

If complete system failure:

```bash
# 1. Ensure you have backup file
ls .deia/backups/state-2025-10-25-16-00-00.tar.gz

# 2. Create fresh state directory
mkdir -p .deia/state
rm -rf .deia/state/*

# 3. Restore from backup
tar -xzf .deia/backups/state-2025-10-25-16-00-00.tar.gz -C .deia/

# 4. Verify files restored
ls -la .deia/state/

# 5. Start fresh system
python run_single_bot.py --bot-id main-bot --port 8001

# 6. Verify system operational
curl http://localhost:8001/health
curl http://localhost:8001/api/dashboard/health
```

---

## Data Persistence Verification

### Task Queue Persistence

**Test:** Kill system, verify tasks reappear on restart

```bash
# 1. Submit tasks
curl -X POST http://localhost:8001/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"task_id": "test-1", "content": "test task"}'

# 2. Verify tasks queued
curl http://localhost:8001/api/orchestrate/status | grep queue_depth

# 3. Kill system (force kill, no shutdown)
pkill -9 -f "python run_single_bot.py"

# 4. Restart system
python run_single_bot.py --bot-id main-bot --port 8001

# 5. Verify tasks still there (PERSISTED)
curl http://localhost:8001/api/orchestrate/status | grep queue_depth
```

**Expected:** Queue depth same before/after restart

### Chat History Persistence

**Test:** Verify chat history survives restart

```bash
# 1. Check initial chat history
curl http://localhost:8000/api/chat/history | jq '.messages | length'

# 2. Kill system
pkill -9 -f "python run_single_bot.py"

# 3. Restart system
python run_single_bot.py --bot-id main-bot --port 8001

# 4. Verify chat history intact (PERSISTED)
curl http://localhost:8000/api/chat/history | jq '.messages | length'
```

**Expected:** Message count same before/after restart

### Bot Assignment Persistence

**Test:** Bot assignments survive restart

```bash
# 1. Check bot assignments
curl http://localhost:8001/api/orchestrate/status | jq '.bots'

# 2. Kill and restart
pkill -9 -f "python run_single_bot.py"
python run_single_bot.py --bot-id main-bot --port 8001

# 3. Verify assignments intact
curl http://localhost:8001/api/orchestrate/status | jq '.bots'
```

**Expected:** Bot assignments same before/after restart

### Audit Log Persistence

**Test:** Audit logs survive restart

```bash
# 1. Count audit log entries
wc -l .deia/bot-logs/audit.jsonl

# 2. Kill and restart system
pkill -9 -f "python run_single_bot.py"
python run_single_bot.py --bot-id main-bot --port 8001

# 3. Count audit entries again (should have more from restart)
wc -l .deia/bot-logs/audit.jsonl
```

**Expected:** Audit log entries increase (persist through restart)

---

## Crash Recovery Test

**Scenario:** System crashes, verify automatic recovery

```bash
# 1. Start system
python run_single_bot.py --bot-id main-bot --port 8001

# 2. Verify running
ps aux | grep "python run_single_bot"

# 3. Simulate crash (kill -9 = force kill)
pkill -9 -f "python run_single_bot.py"

# 4. Verify process gone
sleep 2
ps aux | grep "python run_single_bot" | grep -v grep || echo "Process killed"

# 5. Restart system
python run_single_bot.py --bot-id main-bot --port 8001

# 6. Verify recovery
# a. Service responds to health check
curl http://localhost:8001/health
# b. State recovered
curl http://localhost:8001/api/orchestrate/status | jq '.state_recovered'
# c. In-flight tasks resumed
curl http://localhost:8001/api/orchestrate/status | jq '.queue_depth'

# 7. Check logs for recovery events
tail -20 .deia/bot-logs/system.jsonl | grep -i "recovery\|restored"
```

**Expected:** System recovers automatically, state preserved, no data loss

---

## Recovery Time Objectives

| Scenario | RTO | RPO | Status |
|----------|-----|-----|--------|
| Single bot crash | <1 min | <1 min | ✅ Automated |
| Partial data loss | <5 min | <10 min | ✅ Restore from backup |
| Full system failure | <10 min | <10 min | ✅ Full restore possible |
| Disk corruption | <15 min | <10 min | ✅ Restore from backup |
| Data center failure | <30 min | Custom | Manual (plan ahead) |

**RTO = Recovery Time Objective (how fast can we restore)**
**RPO = Recovery Point Objective (how much data can we lose)**

---

## Backup Storage & Cleanup

### Storage Usage

```bash
# Check backup storage
du -sh .deia/backups/

# Typical: 50-100 MB for 7 days of hourly backups
```

### Retention Policy

- Keep backups for 7 days
- Clean up automatically (no manual action needed)
- Old backups deleted on next backup cycle
- Can configure in `bot-config.yaml`:

```yaml
persistence:
  backup_retention_days: 7    # Change to 30 for longer retention
```

### Manual Cleanup

To free space, delete old backups:

```bash
# Find backups older than 7 days
find .deia/backups/ -name "state-*.tar.gz" -mtime +7

# Delete them
find .deia/backups/ -name "state-*.tar.gz" -mtime +7 -delete

# Verify
ls -lh .deia/backups/ | tail -5
```

---

## Disaster Recovery Checklist

Before production deployment, verify:

- [ ] Backups created automatically (check last 10 minutes)
- [ ] Backup files valid (can extract without error)
- [ ] Restore procedure tested (full restore works)
- [ ] Task queue persists across restart
- [ ] Chat history persists across restart
- [ ] Audit logs persist across restart
- [ ] Recovery from crash automatic
- [ ] Backup storage adequate (>500MB free)
- [ ] Retention policy understood (7 days default)
- [ ] Team trained on manual recovery

---

## Troubleshooting

### No Backups Being Created

**Symptom:** No backup files in `.deia/backups/`

**Solution:**
1. Check if backup enabled: `grep backup_enabled bot-config.yaml`
2. Check for errors: `tail -f .deia/bot-logs/system.jsonl | grep -i backup`
3. Verify directory writable: `touch .deia/backups/test.txt && rm .deia/backups/test.txt`
4. Check disk space: `df -h .deia/`
5. Manual backup: `tar -czf .deia/backups/state-manual.tar.gz .deia/state/`

### Restore Fails with "Checksum Error"

**Symptom:** Error extracting backup (corrupted file)

**Solution:**
1. Verify backup integrity: `tar -tzf state-*.tar.gz >/dev/null && echo "OK" || echo "CORRUPT"`
2. Use older backup: `ls -lt .deia/backups/ | head -5` (choose older file)
3. Try restore with older backup
4. If all backups corrupt, restore from external backup

### Restore Successful But Data Missing

**Symptom:** Tasks/messages missing after restore

**Solution:**
1. Verify restore point is recent enough
2. Check backup timestamp vs data needed
3. Use backup from right after data was created
4. Review what point-in-time you need to restore to
5. Use most recent backup that still has your data

---

## Best Practices

1. **Test backups regularly:** Monthly full restore test
2. **Monitor backup success:** Check logs daily
3. **Document RTO/RPO:** Know your recovery objectives
4. **Store backups securely:** Access controls, encryption optional
5. **External backups:** Consider copying to external storage weekly
6. **Document procedures:** Keep this guide accessible to team
7. **Automate testing:** Write script to verify backups weekly
8. **Alert on backup failure:** Monitor backup logs for errors

---

**Status:** ✅ PRODUCTION READY

**Last Verified:** 2025-10-25 16:27 CDT
**Verified By:** BOT-001 (Infrastructure Lead)

For more information, see TROUBLESHOOTING.md or contact the on-call engineer.
