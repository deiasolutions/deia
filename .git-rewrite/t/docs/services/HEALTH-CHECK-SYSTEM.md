# DEIA Health Check System

**Version:** 1.0
**Author:** CLAUDE-CODE-003 (implementation) + CLAUDE-CODE-004 (documentation)
**Date:** 2025-10-18
**Source:** Agent BC Phase 3

---

## Overview

The DEIA Health Check System provides comprehensive monitoring and diagnostics for your DEIA installation. It verifies that all critical components are functioning correctly, including agent activity, messaging systems, the Body of Knowledge index, filesystem structure, and Python dependencies.

**Key Features:**
- 🤖 **Agent health monitoring** - Track agent activity and detect stale agents
- 📬 **Messaging system verification** - Ensure inter-agent communication is active
- 📚 **BOK index integrity** - Verify Body of Knowledge accessibility
- 📁 **Filesystem structure validation** - Confirm proper `.deia/` setup
- 📦 **Dependency checks** - Validate Python package installations

---

## Quick Start

### Basic Usage

```python
from deia.services.health_check import generate_health_report

# Run all health checks and generate a report
report = generate_health_report()
print(report)
```

### CLI Usage (Future)

```bash
# Run health check from command line
deia health

# Run specific checks only
deia health --agents --messaging

# Output in JSON format
deia health --json
```

---

## Health Metrics Tracked

The system performs five core health checks:

### 1. Agent Health

**What it checks:**
- Agent activity logs exist (`.deia/bot-logs/CLAUDE-CODE-*-activity.jsonl`)
- Agents have recent activity (within last hour)
- Activity log files are readable and valid JSON

**Status meanings:**
- ✅ **PASS** - All agents have recent activity
- ⚠️ **WARNING** - One or more agents have stale activity (>1 hour old)
- ❌ **FAIL** - Agent directory not found

**Example result:**
```
✓ Agent Health: PASS
  All 5 agent(s) have recent activity
```

---

### 2. Messaging Health

**What it checks:**
- Messaging tunnel directory exists (`.deia/tunnel/claude-to-claude/`)
- Recent messages are present (last 24 hours)
- Message volume indicates active communication

**Status meanings:**
- ✅ **PASS** - 5+ messages in last 24 hours
- ⚠️ **WARNING** - Less than 5 messages in last 24 hours
- ❌ **FAIL** - Messaging tunnel directory not found

**Example result:**
```
✓ Messaging Health: PASS
  Messaging system active: 23 messages in last 24 hours
```

---

### 3. BOK Health

**What it checks:**
- Master BOK index file exists (`.deia/index/master-index.yaml` or `bok/master-index.yaml`)
- Index file is readable and non-empty
- Basic YAML structure is valid

**Status meanings:**
- ✅ **PASS** - Index file accessible with valid content
- ⚠️ **WARNING** - Master index file not found (BOK may not be initialized)
- ❌ **FAIL** - Index file exists but is empty or unreadable

**Example result:**
```
✓ BOK Health: PASS
  BOK index accessible with ~47 entries
```

---

### 4. Filesystem Health

**What it checks:**
- `.deia/` directory exists
- Required subdirectories are present:
  - `sessions/`
  - `bok/`
  - `index/`
  - `federalist/`
  - `governance/`
  - `tunnel/claude-to-claude/`
  - `bot-logs/`
  - `observations/`
  - `handoffs/`
  - `intake/`

**Status meanings:**
- ✅ **PASS** - All required directories exist
- ⚠️ **WARNING** - 1-2 optional directories missing
- ❌ **FAIL** - 3+ required directories missing or `.deia/` not found

**Example result:**
```
✓ Filesystem Health: PASS
  All required directories exist
```

---

### 5. Dependencies Health

**What it checks:**
- Required Python packages are installed:
  - `click`
  - `pyyaml`
  - `watchdog`
  - `pytest`
  - `pytest-cov`
- Package versions are retrievable

**Status meanings:**
- ✅ **PASS** - All required packages installed
- ❌ **FAIL** - One or more required packages missing

**Example result:**
```
✓ Dependencies Health: PASS
  All 5 required packages installed
```

---

## Interpreting Results

### Overall Health Status

The system provides three overall health levels:

| Status | Meaning | Exit Code |
|--------|---------|-----------|
| **HEALTHY** | All checks passed | 0 |
| **DEGRADED** | Some warnings present, but no failures | 1 |
| **UNHEALTHY** | One or more critical failures | 2 |

### Understanding Status Levels

**PASS (✓)**
- Component is functioning correctly
- No action required

**WARNING (⚠️)**
- Component is functional but has non-critical issues
- System remains operational
- Review recommended but not urgent

**FAIL (✗)**
- Component has critical issues
- May impact system functionality
- Immediate action recommended

---

## Usage Examples

### Example 1: Full System Check

```python
from deia.services.health_check import HealthCheckSystem

# Initialize health check system
system = HealthCheckSystem()

# Run all checks
results = system.check_system_health()

# Generate formatted report
report = system.generate_health_report(results)
print(report)
```

**Sample Output:**
```
============================================================
DEIA HEALTH CHECK REPORT
============================================================
Timestamp: 2025-10-18 15:30:45
Project Root: /Users/you/projects/deia

SUMMARY
------------------------------------------------------------
Total Checks: 5
Passed:       5 ✓
Warnings:     0 ⚠
Failed:       0 ✗

Overall Status: HEALTHY - All systems operational

DETAILED RESULTS
------------------------------------------------------------
✓ Agent Health: PASS
  All 5 agent(s) have recent activity

✓ Messaging Health: PASS
  Messaging system active: 23 messages in last 24 hours

✓ BOK Health: PASS
  BOK index accessible with ~47 entries

✓ Filesystem Health: PASS
  All required directories exist

✓ Dependencies Health: PASS
  All 5 required packages installed

============================================================
```

---

### Example 2: Individual Health Checks

```python
from deia.services.health_check import (
    check_agent_health,
    check_system_health
)

# Check only agent health
agent_result = check_agent_health()
print(f"{agent_result.status}: {agent_result.message}")

# Check all systems and get results dictionary
all_results = check_system_health()
for name, result in all_results.items():
    print(f"{name}: {result.status}")
```

---

### Example 3: Programmatic Health Monitoring

```python
from deia.services.health_check import HealthCheckSystem

system = HealthCheckSystem()

# Run checks
results = system.check_system_health()

# Get overall status
status, exit_code = system.get_overall_status(results)

if exit_code == 0:
    print("System healthy - proceeding with operations")
elif exit_code == 1:
    print("System degraded - review warnings")
else:
    print("System unhealthy - immediate action required")

# Access specific check details
agent_check = results['agents']
if not agent_check.is_passing():
    print(f"Agent issues: {agent_check.message}")
    print(f"Details: {agent_check.details}")
```

---

### Example 4: Custom Project Root

```python
from pathlib import Path
from deia.services.health_check import HealthCheckSystem

# Check a specific DEIA installation
custom_path = Path("/path/to/deia/project")
system = HealthCheckSystem(project_root=custom_path)

report = system.generate_health_report()
print(report)
```

---

## Common Scenarios

### Scenario 1: Fresh Installation

**Status:** HEALTHY or DEGRADED
**Typical warnings:**
- BOK Health: WARNING (master index not found - BOK not initialized)
- Messaging Health: WARNING (no recent messages - agents not active yet)

**Action:** Normal for new installations. Run `deia init` to initialize BOK structure.

---

### Scenario 2: Stale Agents

**Status:** DEGRADED
**Warning:**
- Agent Health: WARNING (agents with stale activity >1 hour old)

**Action:** Review agent activity logs to determine why agents are inactive. May indicate:
- Agents completed work and stopped (normal)
- Agent crashed or errored (check logs)
- Long-running task in progress (normal)

---

### Scenario 3: Missing Dependencies

**Status:** UNHEALTHY
**Failure:**
- Dependencies Health: FAIL (required packages missing)

**Action:** Install missing packages:
```bash
pip install -e .
# or
pip install click pyyaml watchdog pytest pytest-cov
```

---

### Scenario 4: Corrupted Filesystem

**Status:** UNHEALTHY
**Failure:**
- Filesystem Health: FAIL (required directories missing)

**Action:** Run `deia init` to recreate directory structure:
```bash
deia init
```

---

## API Reference

### Classes

#### `HealthCheckResult`

Represents the result of a single health check.

**Attributes:**
- `name` (str): Name of the health check
- `status` (str): Status - "PASS", "WARNING", or "FAIL"
- `message` (str): Human-readable description
- `details` (dict): Additional diagnostic information
- `timestamp` (str): ISO-formatted timestamp

**Methods:**
- `to_dict()`: Convert to dictionary for serialization
- `is_passing()`: Returns True if status is "PASS"

---

#### `HealthCheckSystem`

Main health check system for DEIA infrastructure.

**Constructor:**
```python
HealthCheckSystem(project_root: Optional[Path] = None)
```

**Methods:**

**`check_agent_health() -> HealthCheckResult`**
- Checks agent activity and heartbeats
- Returns HealthCheckResult for agent health

**`check_messaging_health() -> HealthCheckResult`**
- Checks messaging tunnel activity
- Returns HealthCheckResult for messaging health

**`check_bok_health() -> HealthCheckResult`**
- Checks BOK index accessibility
- Returns HealthCheckResult for BOK health

**`check_filesystem_health() -> HealthCheckResult`**
- Checks `.deia/` directory structure
- Returns HealthCheckResult for filesystem health

**`check_dependencies_health() -> HealthCheckResult`**
- Checks Python package installations
- Returns HealthCheckResult for dependencies health

**`check_system_health() -> Dict[str, HealthCheckResult]`**
- Runs all health checks
- Returns dictionary mapping check names to results

**`generate_health_report(checks: Optional[Dict] = None) -> str`**
- Generates formatted health report
- If checks is None, runs all checks first
- Returns formatted report string

**`get_overall_status(checks: Optional[Dict] = None) -> Tuple[str, int]`**
- Gets overall system health status
- Returns tuple of (status_string, exit_code)
- Exit codes: 0 = healthy, 1 = warnings, 2 = failures

---

### Standalone Functions

```python
from deia.services.health_check import (
    check_agent_health,
    check_system_health,
    generate_health_report
)

# Check agent health only
result = check_agent_health(project_root=None)

# Check all systems
results = check_system_health(project_root=None)

# Generate full report
report = generate_health_report(project_root=None)
```

---

## Testing

The health check system includes comprehensive test coverage (93%):

```bash
# Run health check tests
pytest tests/unit/test_health_check.py -v

# Run with coverage
pytest tests/unit/test_health_check.py --cov=src/deia/services/health_check
```

**Test coverage includes:**
- All five health check functions
- Edge cases (missing directories, stale agents, corrupted files)
- Overall status calculations
- Report generation
- Standalone utility functions

---

## Future Enhancements

**Planned features:**
- CLI integration (`deia health` command)
- Auto-fix functionality for common issues
- Scheduled health checks
- Health check history tracking
- Email/Slack notifications for failures
- Web dashboard for real-time monitoring

---

## Troubleshooting

### "Agent directory not found"

**Cause:** `.deia/bot-logs/` directory missing
**Solution:** Run `deia init` to create directory structure

### "No agent activity logs found"

**Cause:** No agents have been active yet
**Solution:** Normal for fresh installations. Agents create logs on first activity.

### "BOK index file not found"

**Cause:** BOK not initialized yet
**Solution:** Normal for fresh installations. Initialize BOK when ready.

### "Required directories missing"

**Cause:** `.deia/` structure incomplete
**Solution:** Run `deia init` to recreate directory structure

### "Required packages missing"

**Cause:** Python dependencies not installed
**Solution:** Run `pip install -e .` from project root

---

## Implementation Details

**File:** `src/deia/services/health_check.py` (536 lines)
**Tests:** `tests/unit/test_health_check.py` (539 lines, 39 tests)
**Coverage:** 93%
**Status:** Production-ready

**Dependencies:**
- Python 3.8+
- Standard library only (json, pathlib, datetime, importlib)

**Performance:**
- Full system check: <100ms typical
- Individual checks: <20ms typical
- Safe for frequent execution (no side effects)

---

## Related Documentation

- [BOK Pattern Validator](./BOK-PATTERN-VALIDATOR.md)
- [Agent Coordination Protocol](../.deia/tunnel/COMMUNICATION-PROTOCOL.md)
- [DEIA CLI Reference](../README.md)

---

**Questions or issues? File a bug report in `.deia/observations/` or contact the agent team.**
