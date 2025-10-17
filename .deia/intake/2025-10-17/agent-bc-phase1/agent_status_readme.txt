# Agent Status Tracker

The `AgentStatusTracker` class provides a way to track the status and availability of agents in the DEIA system. It uses heartbeat files to monitor when agents are online, what they're working on, and manages state transitions.

## Installation

The `AgentStatusTracker` is part of the `deia` package. Install it with:

```bash
pip install deia
```

## Usage

### Importing

```python
from deia.services.agent_status import AgentStatusTracker
```

### Initialization

```python
tracker = AgentStatusTracker(heartbeat_dir="~/.deia/hive/heartbeats/")
```

The `heartbeat_dir` argument specifies where the heartbeat YAML files will be stored. Defaults to `~/.deia/hive/heartbeats/`.

### Registering Agents

```python
tracker.register_agent(agent_id="agent1", role="worker")
```

Register a new agent with the given `agent_id` and `role`. Role must be one of `{"coordinator", "queen", "worker", "drone"}`.

### Updating Heartbeats

```python
tracker.update_heartbeat(agent_id="agent1", status="busy", current_task="task123")
```

Agents should call `update_heartbeat` periodically to indicate they are still online and what they're currently working on. Status must be one of `{"idle", "busy", "waiting", "paused", "offline"}`.

### Checking Heartbeats

```python
offline_agents = tracker.check_heartbeats()
```

`check_heartbeats` scans all registered agents and returns a dictionary of agents that have gone offline (no heartbeat for 5+ minutes). It also automatically transitions agents to "offline" status.

Additionally, it checks for agents stuck in "waiting" or "busy" status for too long and transitions them to "idle" or "offline" respectively.

### Getting Agent Status

```python
status = tracker.get_agent_status(agent_id="agent1")
```

Returns a dictionary with the current status information for the given `agent_id`, e.g.:

```python
{
    "agent_id": "agent1",
    "status": "busy",
    "current_task": "task123",
    "role": "worker",
    "last_heartbeat": "2023-06-08T15:30:00.000000"
}
```

If the agent is not registered, returns:

```python
{
    "agent_id": "agent1", 
    "status": "unknown",
    "error": "not_registered"
}
```

### Getting All Agent Statuses

```python
all_statuses = tracker.get_all_agents()
```

Returns a dictionary with the current status of all registered agents, keyed by `agent_id`.

### Getting Available Agents

```python
available = tracker.get_available_agents()
```

Returns a list of `agent_id`s for all agents currently in "idle" status, i.e. available for new tasks.

### Starting Monitor Loop

```python
tracker.start_monitor_loop(interval=60)
```

Starts a background thread that periodically (every `interval` seconds) calls `check_heartbeats` to monitor for offline/stuck agents.

## CLI Integration

The `AgentStatusTracker` integrates with the `deia` CLI tool:

- `deia hive status`: Show status of all agents
- `deia hive agents`: List all registered agents 
- `deia hive heartbeat AGENT_ID`: Manually trigger a heartbeat for an agent
- `deia hive monitor`: Start the background monitor loop

Run `deia hive --help` for more details and options.

## Dashboard

The `AgentStatusTracker` provides an ASCII dashboard of the current agent status accessible via `deia hive status`:

```
┌───────────────────────────────────────────────────────────────┐
│                  DEIA COORDINATION DASHBOARD                  │
├───────────────────────────────────────────────────────────────┤
│  🟢 CLAUDE_CODE    [IDLE]     Ready for tasks                 │
│  🟡 CLAUDE_WEB     [WAITING]  Waiting for CLAUDE_DB           │
│  🟢 CLAUDE_DB      [BUSY]     Processing request ID:abc123    │
│  🔴 CLAUDE_MATH    [OFFLINE]  Last seen: 2023-06-08 15:30:00  │
├───────────────────────────────────────────────────────────────┤
│   Online: 3  │  Offline: 1  │  Idle: 1  │  Busy: 1  │  Avg:2m  │
└───────────────────────────────────────────────────────────────┘
```

## Logging

The `AgentStatusTracker` logs all important events (registrations, heartbeats, state transitions, errors) to the `deia.agent_status` logger.

You can configure logging in your application:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

## Error Handling

The `AgentStatusTracker` is designed to never raise exceptions during normal usage. All methods handle potential errors gracefully:

- If an agent is not registered, `get_agent_status` returns a dictionary with `status="unknown"` and `error="not_registered"` rather than raising a `KeyError`.

- If an invalid `agent_id`, `role`, or `status` is passed to `register_agent`, `update_heartbeat`, etc., the method will raise a `ValueError` with a descriptive message. 

- If heartbeat file I/O or YAML parsing fails, the error is logged and the agent is marked offline, but no exception is raised to the caller.

This allows other DEIA components to use the `AgentStatusTracker` without having to wrap every call in `try/except` blocks.

## Testing

The `AgentStatusTracker` has a comprehensive test suite in `tests/unit/test_agent_status.py`. 

To run the tests:

```bash
pytest tests/unit/test_agent_status.py
```

The tests cover all key functionality, edge cases, error handling, concurrency, and time-based transitions.

## Contributing

The `AgentStatusTracker` is part of the core DEIA codebase. To contribute:

1. Open an issue describing the feature/bug
2. Fork the repository and open a pull request with your changes
3. Ensure all tests pass and the code meets the DEIA style guide
4. Request review from the DEIA maintainers

We welcome contributions to improve the functionality, performance, and reliability of the agent status tracking system. 

If you have any questions or feedback, please open an issue or join the DEIA community chat.

Happy tracking!
