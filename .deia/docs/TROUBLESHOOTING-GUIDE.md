# Troubleshooting Guide
**Created by:** BOT-001
**Date:** 2025-10-25
**Status:** QUICK REFERENCE

---

## Common Issues & Solutions

### Application Won't Start

**Problem:** Application crashes immediately on startup

**Solution:**
1. Check environment variables: `env | grep APP`
2. Check logs: `tail -f /var/log/app.log`
3. Verify database connection: `psql $DATABASE_URL -c "SELECT 1"`
4. Check port not in use: `lsof -i :8000`
5. Check file permissions: `ls -la` on working directory

---

### Database Connection Failed

**Problem:** "Cannot connect to database" error

**Symptoms:**
```
psycopg2.OperationalError: could not connect to server
```

**Solution:**
1. Verify DATABASE_URL is correct format:
   ```
   postgresql://user:password@host:5432/dbname
   ```
2. Test connectivity: `psql postgresql://...`
3. Check database is running: `pg_isready -h localhost`
4. Check firewall: `telnet localhost 5432`
5. Check network: `ping db.server.com`

---

### High Memory Usage

**Problem:** Application memory grows over time

**Symptoms:**
```
RSS: 500MB → 2GB over 24 hours
```

**Diagnosis:**
1. Check for memory leaks: `ps aux | grep python`
2. Monitor over time: `watch -n 5 'ps aux | grep python'`
3. Check for circular references
4. Check database connection pool

**Solution:**
1. Restart application (temporary): `systemctl restart deia`
2. Optimize queries (permanent)
3. Add connection pooling limits
4. Investigate memory profiling

---

### Slow API Responses

**Problem:** API endpoints taking > 1 second

**Symptoms:**
```
response time: 2.5s (expected: <500ms)
```

**Diagnosis:**
1. Check logs for slow queries: `grep "duration=" app.log`
2. Monitor database: `SELECT query_start, query FROM pg_stat_activity`
3. Check network latency: `ping -c 10 database`
4. Monitor CPU: `top`

**Solution:**
1. Add database indexes
2. Optimize queries
3. Implement caching
4. Scale horizontally (add more workers)

---

### High CPU Usage

**Problem:** Application using 100% CPU

**Solution:**
1. Check running processes: `top`
2. Identify hot spots: `python -m cProfile app.py`
3. Check for infinite loops
4. Check for N+1 queries
5. Scale horizontally (add more workers)

---

### WebSocket Connection Issues

**Problem:** WebSocket connections timing out or dropping

**Symptoms:**
```
WebSocket closed: Code 1006 (abnormal closure)
```

**Solution:**
1. Check WebSocket URL: `ws://localhost:8001`
2. Check firewall allows WebSocket: `lsof -i :8001`
3. Check proxy config (if behind proxy)
4. Increase timeout: `WS_TIMEOUT=300`
5. Enable heartbeat: `WS_HEARTBEAT=true`

---

### Authentication Failures

**Problem:** JWT token validation failing

**Symptoms:**
```
401 Unauthorized: Invalid token
```

**Solution:**
1. Verify JWT_SECRET matches across instances
2. Check token expiration: `jwt.decode(token, verify=False)`
3. Check CORS configuration
4. Verify client is sending Authorization header

---

### Disk Space Issues

**Problem:** "No space left on device" errors

**Solution:**
1. Check disk usage: `df -h`
2. Find large files: `du -sh /* | sort -rh`
3. Clear logs: `truncate -s 0 /var/log/app.log`
4. Clear temp files: `rm -rf /tmp/*`
5. Archive old logs: `gzip /var/log/app.log.*`

---

### SSL/TLS Certificate Issues

**Problem:** "Certificate verification failed"

**Solution:**
1. Check certificate: `openssl s_client -connect host:443`
2. Verify expiration: `date -d "cert_date"`
3. Check certificate chain
4. Update certificates: `certbot renew`

---

## Debug Mode

Enable detailed logging for troubleshooting:

```bash
DEBUG=true
LOG_LEVEL=debug
APP_ENV=development
```

Then:
```bash
tail -f /var/log/app.log | grep -i error
```

## Performance Tuning

- Increase workers: `WORKERS=8`
- Adjust pool size: `DATABASE_POOL_SIZE=30`
- Enable caching: `REDIS_ENABLED=true`
- Add monitoring: `PROMETHEUS_ENABLED=true`

---

## Getting Help

If you can't resolve the issue:
1. Check logs: `tail -100 /var/log/app.log`
2. Check status: `systemctl status deia`
3. Check recent changes: `git log --oneline -10`
4. File an issue with logs attached
