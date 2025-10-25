# Session Logger Service

**Status:** Phase 1 Complete (Integrated 2025-10-18)
**Module:** `src/deia/services/session_logger.py`
**Tests:** `tests/unit/test_session_logger.py` (86% coverage, 28 tests)

## Overview

The Session Logger is a production-ready service for tracking and analyzing AI agent activities in real-time. It captures task execution, file operations, and tool usage, providing detailed performance metrics and bottleneck analysis.

**Key Features:**
- **Task Tracking:** Log task start/complete events with metadata
- **File Operations:** Track file reads and writes with size metrics
- **Tool Monitoring:** Monitor tool calls with duration and parameters
- **Session Analysis:** Automated bottleneck detection and velocity metrics
- **Performance Metrics:** Tasks per hour, I/O stats, completion rates
- **JSONL Format:** Industry-standard line-delimited JSON for log storage

## When to Use

Use the Session Logger when you need to:

1. **Monitor AI Agent Performance** - Track multi-agent coordination tasks
2. **Identify Bottlenecks** - Find slow tasks consuming >30% of session time
3. **Measure Velocity** - Calculate tasks/files/tools per hour
4. **Audit Operations** - Maintain detailed records of agent activities
5. **Optimize Workflows** - Use data-driven insights to improve efficiency

## Quick Start

### Basic Usage

```python
from deia.services.session_logger import SessionLogger

# Initialize logger
logger = SessionLogger(agent_id="CLAUDE-CODE-002")

# Log a task
logger.log_task_start("write_documentation")
# ... perform work ...
logger.log_task_complete("write_documentation", duration_ms=1800000)  # 30 min

# Log file operations
logger.log_file_read("/docs/guide.md", size_bytes=4096)
logger.log_file_write("/docs/api.md", size_bytes=8192, lines=200)

# Log tool usage
logger.log_tool_call("pytest", params={"path": "tests/"}, duration_ms=2500)

# Get session summary
summary = logger.get_session_summary()
print(f"Tasks completed: {summary.tasks_completed}")
print(f"Velocity: {summary.velocity:.2f} tasks/hour")

# Save session
logger.save_session(output_dir=".deia/sessions")
```

### Analyzing Sessions

```python
# Analyze a saved session
logger = SessionLogger(agent_id="CLAUDE-CODE-002")
analysis = logger.analyze_session(".deia/sessions/session.jsonl")

# View results
print(f"Task breakdown: {analysis.task_breakdown}")
print(f"Bottlenecks: {analysis.bottlenecks}")
print(f"Velocity: {analysis.velocity_metrics}")
print(f"File I/O: {analysis.file_operation_stats}")
```

## API Reference

### SessionLogger Class

#### `__init__(agent_id: str, session_id: str = None)`

Initialize a new session logger.

**Parameters:**
- `agent_id` (str): Identifier for the agent (e.g., "CLAUDE-CODE-002")
- `session_id` (str, optional): Custom session ID. Auto-generated UUID if not provided.

**Example:**
```python
# Auto-generated session ID
logger = SessionLogger(agent_id="AGENT-001")

# Custom session ID
logger = SessionLogger(agent_id="AGENT-001", session_id="2025-10-18-sprint1")
```

#### `log_task_start(task_name: str, metadata: dict = None)`

Log the start of a task.

**Parameters:**
- `task_name` (str): Descriptive name for the task
- `metadata` (dict, optional): Additional context (priority, tags, etc.)

**Example:**
```python
logger.log_task_start("integrate_health_check", metadata={
    "priority": "P1",
    "estimated_hours": 2.5,
    "assignee": "AGENT-004"
})
```

#### `log_task_complete(task_name: str, duration_ms: int, metadata: dict = None)`

Mark a task as complete.

**Parameters:**
- `task_name` (str): Name matching the task started earlier
- `duration_ms` (int): Total duration in milliseconds
- `metadata` (dict, optional): Additional completion metadata

**Example:**
```python
logger.log_task_complete("integrate_health_check",
    duration_ms=7200000,  # 2 hours
    metadata={"result": "success", "tests_passed": 28}
)
```

**Note:** If no matching task start event is found, a warning is logged.

#### `log_file_read(path: str, size_bytes: int = None)`

Log a file read operation.

**Parameters:**
- `path` (str): File path that was read
- `size_bytes` (int, optional): Size of file in bytes

**Example:**
```python
logger.log_file_read("/src/deia/cli.py", size_bytes=24576)
```

#### `log_file_write(path: str, size_bytes: int, lines: int = None)`

Log a file write operation.

**Parameters:**
- `path` (str): File path that was written
- `size_bytes` (int): Size of written data in bytes
- `lines` (int, optional): Number of lines written

**Example:**
```python
logger.log_file_write("/docs/API.md", size_bytes=8192, lines=200)
```

#### `log_tool_call(tool_name: str, params: dict, duration_ms: int)`

Log a tool or function call.

**Parameters:**
- `tool_name` (str): Name of tool (bash, pytest, grep, etc.)
- `params` (dict): Parameters passed to tool
- `duration_ms` (int): Tool execution time in milliseconds

**Example:**
```python
logger.log_tool_call("pytest",
    params={"path": "tests/unit", "verbose": True},
    duration_ms=2500
)
```

#### `get_session_summary() -> SessionSummary`

Generate summary statistics for current session.

**Returns:** `SessionSummary` object with:
- `total_duration_ms` (int): Total session duration
- `tasks_completed` (int): Number of completed tasks
- `files_read` (int): Number of files read
- `files_written` (int): Number of files written
- `tool_calls_count` (int): Number of tool calls
- `velocity` (float): Tasks completed per hour

**Example:**
```python
summary = logger.get_session_summary()
print(f"Session duration: {summary.total_duration_ms / 1000 / 60:.1f} min")
print(f"Productivity: {summary.velocity:.2f} tasks/hour")
```

#### `analyze_session(session_path: str) -> SessionAnalysis`

Analyze a saved session log file.

**Parameters:**
- `session_path` (str): Path to .jsonl session log file

**Returns:** `SessionAnalysis` object with:
- `task_breakdown` (Dict[str, int]): Task durations in ms
- `bottlenecks` (List[str]): Tasks taking >30% of total time
- `velocity_metrics` (Dict[str, float]): Per-hour metrics
- `file_operation_stats` (Dict[str, int]): Read/write counts

**Example:**
```python
analysis = logger.analyze_session(".deia/sessions/2025-10-18_session.jsonl")

# Identify slow tasks
for task in analysis.bottlenecks:
    duration = analysis.task_breakdown[task]
    print(f"Bottleneck: {task} took {duration/1000:.1f}s")
```

#### `save_session(output_dir: str)`

Save session events to JSONL file.

**Parameters:**
- `output_dir` (str): Directory to save session log

**Output Format:** `{agent_id}_{session_id}.jsonl`

**Example:**
```python
logger.save_session(".deia/sessions")
# Creates: .deia/sessions/CLAUDE-CODE-002_abc123.jsonl
```

## Data Structures

### TaskEvent

```python
@dataclass
class TaskEvent:
    name: str                       # Task name
    start_time: float               # Unix timestamp
    end_time: Optional[float]       # Unix timestamp (None if not complete)
    metadata: Dict                  # Additional context
```

### FileEvent

```python
@dataclass
class FileEvent:
    path: str                       # File path
    operation: str                  # "read" or "write"
    size_bytes: Optional[int]       # File size
    lines: Optional[int]            # Line count (write only)
```

### ToolEvent

```python
@dataclass
class ToolEvent:
    name: str                       # Tool name
    params: Dict                    # Tool parameters
    duration_ms: int                # Execution time
```

### SessionSummary

```python
@dataclass
class SessionSummary:
    total_duration_ms: int          # Total session time
    tasks_completed: int            # Completed task count
    files_read: int                 # File read count
    files_written: int              # File write count
    tool_calls_count: int           # Tool call count
    velocity: float                 # Tasks per hour
```

### SessionAnalysis

```python
@dataclass
class SessionAnalysis:
    task_breakdown: Dict[str, int]          # Task name -> duration (ms)
    bottlenecks: List[str]                  # Slow tasks (>30% total time)
    velocity_metrics: Dict[str, float]      # Per-hour metrics
    file_operation_stats: Dict[str, int]    # Operation type -> count
```

## File Format

Session logs are saved in JSONL (JSON Lines) format - one JSON object per line.

**Example:**
```jsonl
{"name":"write_tests","start_time":1697654400.123,"end_time":1697656200.456,"metadata":{"priority":"P1"}}
{"path":"/tests/test_logger.py","operation":"read","size_bytes":4096,"lines":null}
{"name":"pytest","params":{"path":"tests/"},"duration_ms":2500}
{"path":"/tests/test_logger.py","operation":"write","size_bytes":8192,"lines":200}
```

## Usage Examples

### Example 1: Track Integration Task

```python
from deia.services.session_logger import SessionLogger

logger = SessionLogger(agent_id="AGENT-004")

# Start integration task
logger.log_task_start("integrate_health_check", metadata={
    "priority": "P1",
    "estimated_hours": 2.5
})

# Track file operations
logger.log_file_read("intake/health_check.txt", size_bytes=3200)
logger.log_file_write("src/deia/services/health_check.py", size_bytes=7700, lines=150)
logger.log_file_write("tests/unit/test_health_check.py", size_bytes=9220, lines=250)

# Track test execution
logger.log_tool_call("pytest",
    params={"path": "tests/unit/test_health_check.py", "coverage": True},
    duration_ms=3500
)

# Complete task
logger.log_task_complete("integrate_health_check",
    duration_ms=7200000,  # 2 hours
    metadata={"coverage": 82, "tests_passed": 28}
)

# Save and summarize
logger.save_session(".deia/sessions")
summary = logger.get_session_summary()
print(f"Completed in {summary.total_duration_ms/1000/60:.1f} minutes")
print(f"Files created: {summary.files_written}")
print(f"Test coverage: 82%")
```

### Example 2: Multi-Task Session

```python
logger = SessionLogger(agent_id="AGENT-002")

# Documentation task
logger.log_task_start("write_api_docs")
logger.log_file_read("src/deia/services/session_logger.py", size_bytes=12300)
logger.log_file_write("docs/services/SESSION-LOGGER.md", size_bytes=15000, lines=300)
logger.log_task_complete("write_api_docs", duration_ms=3600000)  # 1 hour

# Review task
logger.log_task_start("review_tests")
logger.log_file_read("tests/unit/test_session_logger.py", size_bytes=18000)
logger.log_task_complete("review_tests", duration_ms=900000)  # 15 min

# Summary
summary = logger.get_session_summary()
print(f"Tasks completed: {summary.tasks_completed}")
print(f"Velocity: {summary.velocity:.2f} tasks/hour")
```

### Example 3: Analyze Past Performance

```python
logger = SessionLogger(agent_id="AGENT-001")
analysis = logger.analyze_session(".deia/sessions/2025-10-17_sprint.jsonl")

# Find bottlenecks
print("=== Bottlenecks ===")
for task in analysis.bottlenecks:
    duration_min = analysis.task_breakdown[task] / 1000 / 60
    print(f"- {task}: {duration_min:.1f} min")

# Show velocity
print("\n=== Velocity Metrics ===")
print(f"Tasks/hour: {analysis.velocity_metrics['tasks_per_hour']:.2f}")
print(f"Files read/hour: {analysis.velocity_metrics['files_read_per_hour']:.2f}")
print(f"Files written/hour: {analysis.velocity_metrics['files_written_per_hour']:.2f}")

# I/O stats
print("\n=== File I/O ===")
print(f"Reads: {analysis.file_operation_stats.get('read', 0)}")
print(f"Writes: {analysis.file_operation_stats.get('write', 0)}")
```

## Integration with DEIA

### Multi-Agent Coordination

```python
# In agent coordination workflows
from deia.services.session_logger import SessionLogger

class DEIAAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = SessionLogger(agent_id=agent_id)

    def execute_task(self, task_name: str, task_func):
        """Execute task with automatic logging."""
        self.logger.log_task_start(task_name)
        start_time = time.time()

        try:
            result = task_func()
            duration_ms = int((time.time() - start_time) * 1000)
            self.logger.log_task_complete(task_name, duration_ms,
                metadata={"result": "success"})
            return result
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            self.logger.log_task_complete(task_name, duration_ms,
                metadata={"result": "failed", "error": str(e)})
            raise
        finally:
            self.logger.save_session(".deia/sessions")
```

### Comparison with ConversationLogger

| Feature | SessionLogger | ConversationLogger |
|---------|--------------|-------------------|
| **Purpose** | Performance metrics | Conversation history |
| **Format** | JSONL (structured) | Markdown + YAML |
| **Granularity** | Task/file/tool events | Full conversation text |
| **Analysis** | Automated bottleneck detection | Manual review |
| **Use Case** | AI agent monitoring | Human-readable logs |
| **Real-time** | Yes | Yes |
| **Storage** | `.deia/sessions/` | `.deia/sessions/` |

**Use both together:** SessionLogger tracks performance metrics while ConversationLogger maintains human-readable conversation history.

## Best Practices

### 1. Consistent Event Logging

```python
# ✅ GOOD: Log both start and complete
logger.log_task_start("refactor_module")
# ... do work ...
logger.log_task_complete("refactor_module", duration_ms=1800000)

# ❌ BAD: Only log start (incomplete data)
logger.log_task_start("refactor_module")
# ... forgot to log complete ...
```

### 2. Meaningful Task Names

```python
# ✅ GOOD: Descriptive names
logger.log_task_start("integrate_health_check_system")
logger.log_task_start("write_api_documentation")
logger.log_task_start("run_integration_tests")

# ❌ BAD: Generic names
logger.log_task_start("task1")
logger.log_task_start("work")
logger.log_task_start("stuff")
```

### 3. Rich Metadata

```python
# ✅ GOOD: Context-rich metadata
logger.log_task_start("code_review", metadata={
    "pull_request": "#123",
    "author": "AGENT-004",
    "lines_changed": 450,
    "priority": "P1"
})

# ❌ BAD: No metadata (lost context)
logger.log_task_start("code_review")
```

### 4. Regular Session Saves

```python
# ✅ GOOD: Save after major milestones
logger.log_task_complete("integration", duration_ms=3600000)
logger.save_session(".deia/sessions")  # Save after task

logger.log_task_complete("documentation", duration_ms=1800000)
logger.save_session(".deia/sessions")  # Save again

# ❌ BAD: Only save at end (risk data loss)
# ... many tasks ...
logger.save_session(".deia/sessions")  # Only one save at end
```

### 5. Analyze for Optimization

```python
# Weekly sprint retrospective
analysis = logger.analyze_session(".deia/sessions/week42.jsonl")

# Identify areas for improvement
if len(analysis.bottlenecks) > 0:
    print("Tasks to optimize:")
    for task in analysis.bottlenecks:
        print(f"  - {task}: {analysis.task_breakdown[task]/1000:.1f}s")

# Compare velocity to goals
target_velocity = 8.0  # tasks per hour
if analysis.velocity_metrics['tasks_per_hour'] < target_velocity:
    print(f"Below target velocity: {analysis.velocity_metrics['tasks_per_hour']:.2f} < {target_velocity}")
```

## Troubleshooting

### Issue: "Task complete event logged without corresponding start event"

**Cause:** Called `log_task_complete()` without prior `log_task_start()`

**Solution:**
```python
# Make sure task names match exactly
logger.log_task_start("write_documentation")
# ... work ...
logger.log_task_complete("write_documentation", duration_ms=3600000)  # Same name
```

### Issue: Division by zero / velocity = 0.0

**Cause:** Session duration is extremely short (< 1ms)

**Solution:** This is expected for very fast operations. The code handles this gracefully by returning velocity = 0.0.

### Issue: Session file not created

**Cause:** Output directory doesn't exist

**Solution:**
```python
import os
output_dir = ".deia/sessions"
os.makedirs(output_dir, exist_ok=True)
logger.save_session(output_dir)
```

### Issue: Empty bottlenecks list

**Cause:** No single task consumed >30% of total session time

**Solution:** This is expected for well-balanced sessions. If you want to see all tasks ranked by duration:
```python
sorted_tasks = sorted(analysis.task_breakdown.items(), key=lambda x: x[1], reverse=True)
for task, duration in sorted_tasks:
    print(f"{task}: {duration/1000:.1f}s")
```

## Performance Considerations

- **Memory:** Events stored in memory until `save_session()` called
- **I/O:** Single write operation per `save_session()` call
- **Overhead:** Minimal (~0.1ms per event logged)
- **File Size:** ~100-200 bytes per event in JSONL format

**Recommendation:** Save sessions every 30-60 minutes or after major milestones to prevent excessive memory use in long-running sessions.

## Related Documentation

- [Conversation Logging Guide](../guides/CONVERSATION-LOGGING-GUIDE.md) - Human-readable session logs
- [Pattern Submission Guide](../guides/PATTERN-SUBMISSION-GUIDE.md) - Contributing performance patterns
- [Multi-Agent Coordination](../../.deia/AGENTS.md) - Agent coordination workflows

## Testing

**Test Suite:** `tests/unit/test_session_logger.py`
**Coverage:** 86% (123 statements, 20 branches)
**Tests:** 28 passing

Run tests:
```bash
pytest tests/unit/test_session_logger.py -v --cov=src/deia/services/session_logger
```

---

**Last Updated:** 2025-10-18
**Maintainer:** AGENT-002 (Documentation Expert)
**Status:** Production Ready ✅
