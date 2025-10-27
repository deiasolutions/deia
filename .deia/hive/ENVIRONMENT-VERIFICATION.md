# Environment Verification Checklist - UAT Readiness

**Purpose:** Verify all prerequisites are met before starting UAT
**Date:** 2025-10-26
**Version:** 1.0
**Prepared By:** BOT-001

---

## Part 1: System Requirements

### Python Environment
```bash
# Verify Python 3.13+
python --version
# Expected: Python 3.13.x or later
```

- [ ] Python 3.13+ installed
- [ ] Python executable in PATH
- [ ] pip available (`pip --version`)
- [ ] virtualenv available (optional)

### Operating System
- [ ] Windows 10/11 OR macOS 11+ OR Linux (Ubuntu 22.04+)
- [ ] Administrator access available (for process management)
- [ ] At least 4GB RAM available
- [ ] At least 1GB free disk space

---

## Part 2: Dependencies Installation

### Step 1: Install Required Packages
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions
pip install -r requirements.txt -q
```

**Expected packages:**
```
fastapi
uvicorn
pydantic
requests
PyJWT
bcrypt
sqlalchemy
```

- [ ] All packages installed without errors
- [ ] No version conflicts reported

### Step 2: Verify Critical Imports
```bash
python -c "
from deia.services.chat_interface_app import app
from deia.services.chat_database import ChatDatabase
from deia.services.auth_service import AuthService
from deia.services.rate_limiter_middleware import rate_limit_middleware
from deia.adapters.bot_runner import BotRunner
from deia.services.service_factory import ServiceFactory
print('✓ All critical imports successful')
"
```

- [ ] All imports successful
- [ ] No ModuleNotFoundError or ImportError

---

## Part 3: File System & Configuration

### Required Directories
```bash
# These should already exist
ls -la .deia/hive/tasks
ls -la .deia/hive/responses/deiasolutions
ls -la src/deia/services
ls -la tests/unit
```

- [ ] `.deia/hive/tasks` exists
- [ ] `.deia/hive/responses/deiasolutions` exists
- [ ] `.deia/config.json` exists with auto_log enabled
- [ ] `src/deia/services/` contains all service files
- [ ] `run_single_bot.py` exists in project root

### Configuration Verification
```bash
# Check config
cat .deia/config.json
```

Expected output:
```json
{
  "project": "deiasolutions",
  "user": "davee",
  "auto_log": true,
  "version": "0.1.0"
}
```

- [ ] `auto_log` is set to `true`
- [ ] Project name is correct
- [ ] User is set correctly

### Database Initialization
```bash
# Chat database should be created on first run
# Verify it can be created
python -c "
from deia.services.chat_database import ChatDatabase
db = ChatDatabase()
print(f'Database path: {db.db_path}')
print(f'Database accessible: {db.db_path.exists()}')
"
```

- [ ] Database file created or exists
- [ ] Database accessible (readable/writable)
- [ ] Schema initialized correctly

---

## Part 4: Port Availability

### Port Range Check
Verify ports 8000-8010 are available:

```bash
# Windows
netstat -ano | findstr "800[0-9]"

# macOS/Linux
lsof -i :8000
lsof -i :8001
```

Expected: No output (ports are free)

- [ ] Port 8000 available (main chat service)
- [ ] Ports 8001-8010 available (for spawned bots)
- [ ] No other services using these ports

### Port Cleanup (if needed)
```bash
# Windows: Kill process on port 8000
taskkill /PID <PID> /F

# macOS/Linux: Kill process on port 8000
kill -9 <PID>
```

- [ ] All target ports freed
- [ ] No zombie processes

---

## Part 5: Network Configuration

### Localhost Resolution
```bash
ping localhost
ping 127.0.0.1
```

Expected: Reply from 127.0.0.1

- [ ] Localhost resolves to 127.0.0.1
- [ ] Can ping localhost
- [ ] Network stack operational

### Firewall Configuration
- [ ] Firewall allows localhost communication
- [ ] Firewall allows port 8000-8010 (internal)
- [ ] If using corporate firewall: ports not blocked

---

## Part 6: Code Quality & Tests

### Syntax Validation
```bash
python -m py_compile src/deia/services/chat_interface_app.py
python -m py_compile src/deia/services/chat_database.py
python -m py_compile src/deia/services/auth_service.py
python -m py_compile src/deia/services/rate_limiter_middleware.py
```

Expected: No output (success)

- [ ] `chat_interface_app.py` valid
- [ ] `chat_database.py` valid
- [ ] `auth_service.py` valid
- [ ] `rate_limiter_middleware.py` valid

### Unit Tests Passing
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions
python -m pytest tests/unit/test_chat_api_endpoints.py::TestLaunchBotEndpoint -v
```

Expected: 3 passed

- [ ] `test_launch_bot_success` - PASS
- [ ] `test_launch_bot_duplicate` - PASS
- [ ] `test_launch_bot_empty_id` - PASS

### Chat Database Tests
```bash
python -m pytest tests/unit/test_chat_database.py -v
```

Expected: 14/14 passed

- [ ] All database tests passing
- [ ] No schema issues

### Auth Service Tests
```bash
python -m pytest tests/unit/test_auth_service.py -v
```

Expected: 19/19 passed

- [ ] All authentication tests passing
- [ ] No JWT issues

### Rate Limiter Tests
```bash
python -m pytest tests/unit/test_rate_limiter.py -v
```

Expected: 12/12 passed

- [ ] All rate limiting tests passing

---

## Part 7: Service Startup Test

### Start Chat Interface Service
```bash
python -m uvicorn src.deia.services.chat_interface_app:app \
  --host 0.0.0.0 --port 8000 --reload
```

Expected: Service starts, listens on 0.0.0.0:8000

- [ ] Service starts without errors
- [ ] Listens on port 8000
- [ ] No import errors on startup
- [ ] No database errors on startup

### Keep terminal open and proceed to Part 8

---

## Part 8: API Health Checks

### In another terminal, run these checks:

#### Check 1: Service is responding
```bash
curl http://localhost:8000/api/bots
```

Expected:
```json
{
  "success": true,
  "bots": {},
  "timestamp": "2025-10-26T..."
}
```

- [ ] Service responds to HTTP
- [ ] Returns valid JSON
- [ ] No connection refused errors

#### Check 2: Authentication endpoint available
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"dev-user","password":"dev-password"}'
```

Expected:
```json
{
  "success": true,
  "token": "eyJ0eXAi...",
  "timestamp": "2025-10-26T..."
}
```

- [ ] Authentication endpoint responds
- [ ] Returns JWT token
- [ ] Token is valid format

#### Check 3: Bot launch endpoint available
```bash
curl -X POST http://localhost:8000/api/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"bot_id":"TEST-LAUNCH","bot_type":"claude"}'
```

Expected: Success response with port and PID

- [ ] Launch endpoint responds
- [ ] Returns port assignment
- [ ] Returns process PID

#### Check 4: Verify bot list updated
```bash
curl http://localhost:8000/api/bots
```

Expected: TEST-LAUNCH bot in list

- [ ] Bot appears in list
- [ ] Port assigned correctly
- [ ] Status is "starting" or "ready"

#### Check 5: Stop bot
```bash
curl -X POST http://localhost:8000/api/bot/stop/TEST-LAUNCH
```

Expected: Success response

- [ ] Bot removal succeeds
- [ ] No errors in stopping

---

## Part 9: Database Persistence

### Verify database file exists
```bash
# Windows
dir | find "chat.db"

# macOS/Linux
ls -la | grep chat.db
```

- [ ] `chat.db` file exists
- [ ] File is readable/writable
- [ ] File size > 0 KB

### Verify table schema
```bash
# Install sqlite3 if needed
pip install sqlite3

# Check schema
sqlite3 chat.db ".schema"
```

Expected output includes:
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    bot_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
```

- [ ] `messages` table exists
- [ ] `sessions` table exists (if present)
- [ ] Schema matches expected

---

## Part 10: Process Management

### Verify run_single_bot.py is executable
```bash
python run_single_bot.py --help
```

Expected: Help output with arguments

- [ ] Script is executable
- [ ] Help text displays
- [ ] Arguments documented

### Verify subprocess spawning works
```bash
# Windows: Check if process can be spawned
python -c "
import subprocess
import sys

cmd = [sys.executable, 'run_single_bot.py', 'TEST-BOT', '--adapter-type', 'api']
print(f'Command: {\" \".join(cmd)}')
print(f'Would execute from: {os.getcwd()}')
"
```

- [ ] Subprocess spawning should work
- [ ] Path to run_single_bot.py correct
- [ ] Command syntax valid

---

## Part 11: Cross-Platform Verification

### If on Windows
```bash
# Verify subprocess.CREATE_NEW_PROCESS_GROUP available
python -c "import subprocess; print(subprocess.CREATE_NEW_PROCESS_GROUP)"
```

Expected: Integer constant

- [ ] Windows process group support available
- [ ] taskkill command available
- [ ] SIGABRT handling available

### If on macOS/Linux
```bash
# Verify signal handling
python -c "import signal; print(signal.SIGTERM, signal.SIGTERM)"
```

Expected: Signal constants

- [ ] SIGTERM available
- [ ] Signal handling works
- [ ] Process termination works

---

## Part 12: Performance Baseline

### Memory usage at startup
```bash
# Start service and check
# On Windows:
tasklist | findstr python

# On macOS/Linux:
ps aux | grep python
```

- [ ] Python process using < 500MB RAM
- [ ] Baseline documented

### CPU usage at startup
- [ ] CPU usage < 10% at idle
- [ ] Service responds within 500ms

---

## Part 13: Logging & Monitoring

### Verify logging is working
```bash
# Check that logs are being written
# Service should have created logs with recent timestamps
```

- [ ] Service logs created
- [ ] Logs show recent timestamps
- [ ] No ERROR level logs at startup

### Verify auto-logging
```bash
# Check if auto-log is creating session files
ls -lt .deia/sessions | head -5
```

- [ ] Session files being created
- [ ] Timestamps recent
- [ ] Auto-log is active

---

## Part 14: Stop Services

Stop the running chat interface service (Ctrl+C in terminal)

Expected: Service stops cleanly, no errors

- [ ] Service stops without errors
- [ ] Database connection closes properly
- [ ] Processes terminate cleanly

---

## Summary Checklist

### Critical (Must Have)
- [ ] Python 3.13+ installed
- [ ] All dependencies installed
- [ ] All imports successful
- [ ] Ports 8000-8010 available
- [ ] Chat service starts without errors
- [ ] API endpoints respond
- [ ] Database initialized
- [ ] Unit tests passing
- [ ] Auto-logging enabled

### Important (Should Have)
- [ ] Cross-platform verified
- [ ] Memory baseline < 500MB
- [ ] Response time < 1s
- [ ] Bot launch works
- [ ] Bot stop works
- [ ] Database persistence works

### Nice to Have
- [ ] Performance baseline documented
- [ ] Logging setup verified
- [ ] Error messages clear

---

## Sign-Off

**Environment Ready for UAT?**

- [ ] **YES** - All critical items checked, proceed with UAT
- [ ] **NO** - Resolve outstanding items before UAT

**Verified By:** _________________
**Date/Time:** _________________
**Issues Found:**
```
1. ________________________________
2. ________________________________
3. ________________________________
```

**Resolution Plan:**
```
[Describe how issues will be resolved]
```

**Estimated Resolution Time:** ___ hours

---

## Troubleshooting Guide

### Issue: "ModuleNotFoundError: No module named 'deia'"
**Solution:**
```bash
pip install -e .
# OR add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Kill process on port 8000
netstat -ano | findstr ":8000"
taskkill /PID <PID> /F
```

### Issue: "Permission denied" on database file
**Solution:**
```bash
# Fix permissions
chmod 644 chat.db
# OR delete and recreate
rm chat.db
python -c "from deia.services.chat_database import ChatDatabase; ChatDatabase()"
```

### Issue: "Failed to import auth_service"
**Solution:**
```bash
pip install PyJWT bcrypt --upgrade
python -m py_compile src/deia/services/auth_service.py
```

### Issue: "WebSocket connection refused"
**Solution:**
- Verify service is running: `curl http://localhost:8000/api/bots`
- Verify no firewall blocking
- Check browser console for errors

---

**Document Version:** 1.0
**Last Updated:** 2025-10-26
**Next Review:** After UAT Phase 1
