# Agent Coordinator

**Service:** `src/deia/services/agent_coordinator.py`
**Purpose:** Multi-agent workflow coordination and intelligent task routing
**Author:** AGENT-005 (Integration Coordinator / BC Liaison)
**Created:** 2025-10-19
**Version:** 3.0
**Test Coverage:** 94%

---

## Overview

The Agent Coordinator is the central coordination layer for DEIA's multi-agent system. It integrates status tracking, message routing, and context loading to enable intelligent delegation and coordination across multiple AI agents (Claude Code, Claude.ai, ChatGPT, etc.).

### Key Features

- **Real-time agent status tracking** - Monitor heartbeats and availability across all agents
- **Intelligent query routing** - BOK-aware classification and delegation
- **Task assignment** - Priority-based task queuing and delegation
- **Multi-agent orchestration** - Coordinate workflows across the hive
- **Health monitoring** - Detect and handle offline/stale agents
- **Dashboard rendering** - Visual coordination dashboard

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Agent Coordinator                      │
│                                                         │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ AgentStatus      │  │ Message      │  │ Context  │ │
│  │ Tracker          │  │ Router       │  │ Loader   │ │
│  └──────────────────┘  └──────────────┘  └──────────┘ │
│                                                         │
│  • Query Classification  • Task Delegation             │
│  • Availability Checking • Workflow Orchestration      │
└─────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌────────┐          ┌────────┐          ┌────────┐
    │Agent 001│          │Agent 002│          │Agent 003│
    └────────┘          └────────┘          └────────┘
```

### Integration Points

- **AgentStatusTracker** - Tracks agent heartbeats and status (idle, busy, waiting, paused, offline)
- **MessageRouter** - Routes messages via file-based messaging system
- **ContextLoader** - Provides BOK search for query classification

---

## Usage

### Basic Initialization

```python
from deia.services.agent_coordinator import AgentCoordinator

# Default initialization (creates dependencies)
coordinator = AgentCoordinator()

# With custom dependencies
from deia.services.agent_status import AgentStatusTracker
from deia.services.context_loader import ContextLoader

status_tracker = AgentStatusTracker(heartbeat_dir="~/.deia/hive/heartbeats")
context_loader = ContextLoader(project_root="/path/to/project")

coordinator = AgentCoordinator(
    status_tracker=status_tracker,
    context_loader=context_loader,
    inbox_dir="~/Downloads/uploads"
)
```

### Agent Registration and Status

```python
# Register new agent
coordinator.register_agent("CLAUDE-CODE-006", "worker")

# Update heartbeat
coordinator.update_agent_heartbeat(
    "CLAUDE-CODE-002",
    "busy",
    "Writing documentation for BOK patterns"
)

# Get agent status
status = coordinator.get_agent_status("CLAUDE-CODE-001")
# {"agent_id": "CLAUDE-CODE-001", "status": "idle", "role": "coordinator"}

# Get all agent statuses
all_status = coordinator.get_agent_status()

# Get available (idle) agents
available = coordinator.get_available_agents()
# ["CLAUDE-CODE-002", "CLAUDE-CODE-004"]

# Check agent health
issues = coordinator.check_agent_health()
# {"CLAUDE-CODE-003": "waiting→idle (timeout)"}
```

### Query Classification and Routing

```python
# Classify query
classification = coordinator.classify_query("Fix authentication bug")
# {
#     "type": "code",
#     "complexity": "medium",
#     "suggested_agent": "CLAUDE_CODE",
#     "can_handle_locally": False,
#     "confidence": 0.8
# }

# Route query (classification + delegation + task creation)
result = coordinator.route_query("Write tests for login.py")
# {
#     "action": "delegate",
#     "agent": "CLAUDE-CODE-003",
#     "classification": {...},
#     "task_file": "/path/to/task.md",
#     "reason": "qa query routed to CLAUDE-CODE-003"
# }
```

### Task Assignment

```python
# Assign task to specific agent
task_file = coordinator.assign_task(
    "CLAUDE-CODE-003",
    "Run comprehensive QA tests on authentication module",
    priority="high"
)

# Broadcast message to all agents
files = coordinator.broadcast_message(
    "Critical security update deployed - all agents verify",
    message_type="ALERT"
)
```

### Dashboard and Monitoring

```python
# Render dashboard
print(coordinator.render_dashboard())
# ┌───────────────────────────────────────────────────────────────┐
# │                  DEIA COORDINATION DASHBOARD                  │
# ├───────────────────────────────────────────────────────────────┤
# │  🟢 AGENT-001       [IDLE    ] No task                        │
# │  🔵 AGENT-002       [BUSY    ] Writing documentation          │
# └───────────────────────────────────────────────────────────────┘

# Get coordination summary
summary = coordinator.get_coordination_summary()
# {
#     "total_agents": 5,
#     "online_agents": 4,
#     "idle_agents": 2,
#     "busy_agents": 2,
#     "offline_agents": 1,
#     "last_check": "2025-10-19T00:40:00"
# }
```

---

## Query Classification

The Agent Coordinator uses a multi-layered classification system:

### 1. BOK Search (Highest Priority)

If the ContextLoader finds relevant patterns in the Body of Knowledge, the query is classified as **"bok"** type and handled locally with 95% confidence.

### 2. Keyword-Based Classification

Queries are classified based on keyword matching (in priority order):

| Type | Keywords | Suggested Agent | Confidence |
|------|----------|----------------|------------|
| **QA** | test, coverage, qa, verify, validate, pytest, unittest | CLAUDE-CODE-003 | 0.85 |
| **Documentation** | document, docs, readme, guide, manual, documentation | CLAUDE-CODE-002 | 0.85 |
| **Engineering** | design, architecture, system, api, interface, protocol | CLAUDE_CODE | 0.9 |
| **Code** | error, bug, debug, fix, implement, code, function, class | CLAUDE_CODE | 0.8 |
| **Creative** | write, poem, story, summarize, explain, describe | CLAUDE | 0.7 |
| **General** | (fallback) | local | 0.6 |

### 3. Delegation Decision

Queries are delegated if:
- Cannot be handled locally (confidence < 0.8 OR can_handle_locally = False)
- Suggested agent is not "local"
- Suggested agent is registered and available (idle status)

Otherwise, queries are handled locally.

---

## Agent Roles

The coordinator supports 4 agent roles:

| Role | Description | Example |
|------|-------------|---------|
| **coordinator** | Strategic planning and orchestration | CLAUDE-CODE-001 |
| **queen** | Specialized lead agents | CLAUDE-CODE-002 (Documentation Lead) |
| **worker** | General-purpose agents | CLAUDE-CODE-003, CLAUDE-CODE-004 |
| **drone** | Task-specific agents | Pattern extractors, sanitizers |

---

## Agent Statuses

| Status | Description | Timeout |
|--------|-------------|---------|
| **idle** | Available for tasks | - |
| **busy** | Currently working | 30 min → offline |
| **waiting** | Waiting for input | 15 min → idle |
| **paused** | Temporarily paused | - |
| **offline** | No heartbeat | Detected after 5 min |

---

## Message Types and Priorities

| Message Type | Priority | Use Case |
|--------------|----------|----------|
| **ESCALATE** | 1 (Highest) | Critical issues requiring immediate attention |
| **ERROR** | 2 | Error reports |
| **REVIEW** | 2 | Code/documentation review requests |
| **TASK** | 3 | Standard task assignments |
| **QUERY** | 3 | User queries requiring delegation |
| **RESPONSE** | 4 | Responses to queries/tasks |
| **HANDOFF** | 4 | Session handoffs between agents |
| **REPORT** | 5 | Status reports and updates |
| **APPROVE** | 6 (Lowest) | Approval requests |

---

## Error Handling

### Context Loader Failures

If the ContextLoader cannot be initialized or BOK search fails, the coordinator falls back to keyword-based classification:

```python
# Graceful degradation when BOK unavailable
try:
    bok_results = self.context_loader.search_bok(query)
except Exception as e:
    logger.warning(f"BOK search failed: {e}")
    bok_results = []  # Fall back to keywords
```

### Delegation Failures

If task creation fails during delegation, the coordinator falls back to local handling:

```python
result = coordinator.route_query("Fix authentication bug")
# If delegation fails:
# {
#     "action": "local",
#     "agent": "local",
#     "reason": "Delegation failed: Permission denied, handling locally"
# }
```

### Task Assignment Errors

```python
# Unknown agent
coordinator.assign_task("UNKNOWN-AGENT", "Task")
# Raises: ValueError: Agent UNKNOWN-AGENT not registered

# Task creation failure
coordinator.assign_task("AGENT-001", "Task")
# Raises: RuntimeError: Task assignment failed: Permission denied
```

---

## Thread Safety

The Agent Coordinator is thread-safe for concurrent operations:

- **Agent registration** - Uses AgentStatusTracker's RLock
- **Heartbeat updates** - Thread-safe via RLock
- **Status queries** - Returns copies, not references
- **Task creation** - Atomic file operations

```python
import threading

def update_agent(agent_id):
    for i in range(10):
        coordinator.update_agent_heartbeat(agent_id, "busy", f"Task {i}")

# Safe concurrent updates
threads = [
    threading.Thread(target=update_agent, args=("AGENT-001",)),
    threading.Thread(target=update_agent, args=("AGENT-002",))
]

for thread in threads:
    thread.start()
```

---

## Testing

Comprehensive test suite with 94% coverage:

```bash
# Run tests
pytest tests/unit/test_agent_coordinator.py -v

# Run with coverage report
pytest tests/unit/test_agent_coordinator.py --cov=src/deia/services/agent_coordinator --cov-report=term-missing
```

**Test Categories:**
- Initialization and configuration (2 tests)
- Agent status and availability (11 tests)
- Query classification (8 tests)
- Delegation decisions (5 tests)
- Query routing (3 tests)
- Task creation and assignment (7 tests)
- Broadcasting (2 tests)
- Dashboard and monitoring (5 tests)
- Integration workflows (2 tests)
- Error handling and edge cases (4 tests)

---

## Performance Considerations

### BOK Search

BOK search adds latency to classification but improves accuracy:

```python
# Typical classification time:
# - Without BOK: ~1ms (keyword matching only)
# - With BOK hit: ~50-100ms (includes search)
# - With BOK miss: ~50-100ms + fallback to keywords
```

**Recommendation:** For latency-sensitive applications, consider:
- Caching BOK search results
- Running BOK search asynchronously
- Disabling BOK search and using keywords only

### Heartbeat Checking

Heartbeat checking scans all agent files:

```python
# Check interval recommendations:
# - Development: 60 seconds
# - Production: 120-300 seconds
# - High-frequency: Use monitor_loop with custom interval
```

---

## Migration from Previous Versions

### From v2.0 (Agent006's Implementation)

The v3.0 implementation is a complete rewrite with:

**Added:**
- Full BOK integration
- Enhanced error handling
- Comprehensive documentation
- 94% test coverage
- Thread safety guarantees
- Query routing workflow

**Changed:**
- ContextLoader now required (gracefully degrades if unavailable)
- Query classification order (QA/Doc before Engineering)
- Default initialization creates dependencies

**Migration Example:**

```python
# v2.0 (stub)
coordinator = AgentCoordinator()
coordinator.get_agent_status()  # Not implemented

# v3.0 (full implementation)
coordinator = AgentCoordinator()
status = coordinator.get_agent_status("AGENT-001")
# {"agent_id": "AGENT-001", "status": "idle", "role": "worker"}
```

---

## Future Enhancements

Planned improvements for future versions:

1. **Async Support** - Async/await for non-blocking operations
2. **Load Balancing** - Round-robin or weighted task distribution
3. **Task Queuing** - Per-agent task queues with priorities
4. **Health Checks** - Proactive health monitoring
5. **Metrics Collection** - Task completion times, delegation rates
6. **Policy Configuration** - Customizable routing rules
7. **Agent Capabilities** - Declare and match agent capabilities
8. **Workflow Templates** - Pre-defined multi-agent workflows

---

## Related Documentation

- [Agent Status Tracker](./AGENT-STATUS.md) - Agent heartbeat and status management
- [Message Router](./MESSAGE-ROUTER.md) - File-based messaging system
- [Context Loader](./CONTEXT-LOADER.md) - BOK search and context assembly
- [BC Liaison Protocol](../process/BC-LIAISON-WORK-PACKET-PROTOCOL.md) - External agent coordination

---

## Troubleshooting

### Agent not receiving tasks

**Check:**
1. Agent is registered: `coordinator.get_agent_status("AGENT-ID")`
2. Agent is idle: `coordinator.get_available_agents()`
3. Message router inbox directory exists
4. Task files are being created in correct location

### Classification not matching expectations

**Check:**
1. BOK search is working: Enable debug logging
2. Keyword order: More specific keywords checked first
3. Query wording: Keywords are case-insensitive

### Heartbeat timeout issues

**Check:**
1. Heartbeat directory permissions
2. System clock synchronization
3. Timeout settings (5 min for offline, 15 min for waiting→idle, 30 min for busy→offline)

---

## Examples

### Complete Coordination Workflow

```python
from deia.services.agent_coordinator import AgentCoordinator

# 1. Initialize
coordinator = AgentCoordinator()

# 2. Register agents
coordinator.register_agent("WORKER-001", "worker")
coordinator.register_agent("QA-SPECIALIST", "queen")

# 3. Update heartbeats
coordinator.update_agent_heartbeat("WORKER-001", "idle")
coordinator.update_agent_heartbeat("QA-SPECIALIST", "idle")

# 4. Route user query
result = coordinator.route_query("Write tests for authentication module")

if result["action"] == "delegate":
    print(f"Task delegated to {result['agent']}")
    print(f"Task file: {result['task_file']}")
else:
    print(f"Handling locally: {result['reason']}")

# 5. Check coordination status
summary = coordinator.get_coordination_summary()
print(f"Online agents: {summary['online_agents']}")
print(f"Idle agents: {summary['idle_agents']}")

# 6. Render dashboard
print(coordinator.render_dashboard())
```

### Health Monitoring Loop

```python
import time

coordinator = AgentCoordinator()

while True:
    # Check for issues
    issues = coordinator.check_agent_health()

    if issues:
        print("Agent health issues detected:")
        for agent_id, issue in issues.items():
            print(f"  {agent_id}: {issue}")

            # Take action based on issue
            if "offline" in issue:
                print(f"  → Agent {agent_id} went offline, alerting team...")
            elif "timeout" in issue:
                print(f"  → Agent {agent_id} timed out, resetting status...")

    # Sleep before next check
    time.sleep(120)  # Check every 2 minutes
```

---

**Last Updated:** 2025-10-19 00:40 CDT
**Maintainer:** AGENT-005 (Integration Coordinator)
**Status:** Production Ready (v3.0)
