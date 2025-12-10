# Claude Code CLI Adapter - Complete Guide

**Status:** Integration layer complete, waiting for BC subprocess core delivery
**Date:** 2025-10-23
**Author:** BEE-000 (Q33N)

---

## Overview

The Claude Code CLI Adapter enables autonomous bots to execute coding tasks using actual `claude code` CLI processes with full tool access (Read, Write, Edit, Bash).

**Architecture:**

```
┌─────────────────────────────────────────┐
│      BotRunner (Autonomous Loop)        │
│  - Monitors task queue                  │
│  - Executes via adapter                 │
│  - Writes responses                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ClaudeCodeCLIAdapter (Integration)     │
│  - Bot coordination                     │
│  - File tracking                        │
│  - Response formatting                  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ClaudeCodeProcess (Subprocess Core)    │  ← BC BUILDS THIS
│  - Process spawning                     │
│  - Thread management                    │
│  - XML parsing                          │
│  - Signal handling                      │
└─────────────────────────────────────────┘
```

**What we built (BEE-000):**
- `ClaudeCodeCLIAdapter`: Integration layer
- `BotRunner`: Autonomous task execution loop
- `MockClaudeCodeProcess`: Mock subprocess for testing
- Complete test suite (17 tests, all passing)
- Example usage scripts

**What BC will build:**
- `ClaudeCodeProcess`: Real subprocess controller
- Background threading for stream capture
- XML tool use parsing
- Process termination (SIGTERM → SIGKILL)
- Cross-platform support (Windows + Unix)

---

## Current Status

✅ **Working Now (with mock):**
- Bot runner starts and monitors task queue
- Tasks are parsed and executed (mock)
- Responses are written correctly
- File tracking works
- All tests pass

⏳ **Pending BC Delivery:**
- Real `claude code` subprocess spawning
- Actual CLI tool access (Write, Edit, Bash, Read)
- Real XML parsing from Claude Code output
- Production subprocess management

**EGG sent to BC:** `C:/Users/davee/Downloads/uploads/2025-10-23-2345-000-TO-BC-cli-subprocess-core-EGG.md`

---

## Installation

```bash
# Install DEIA with adapters
pip install -e .

# Verify CLI adapter
python -c "from deia.adapters.claude_code_cli_adapter import ClaudeCodeCLIAdapter; print('OK')"

# Run tests
pytest tests/test_cli_adapter.py -v
```

---

## Usage

### Basic CLI Adapter

```python
from pathlib import Path
from deia.adapters.claude_code_cli_adapter import ClaudeCodeCLIAdapter

# Initialize
adapter = ClaudeCodeCLIAdapter(
    bot_id="CLAUDE-CODE-001",
    work_dir=Path.cwd(),
    claude_cli_path="claude",  # Assumes in PATH
    timeout_seconds=300
)

# Start session
adapter.start_session()

# Send task
result = adapter.send_task("""
Create a Python script named hello.py that prints 'Hello World'
""")

print(f"Success: {result['success']}")
print(f"Files modified: {result['files_modified']}")
print(f"Tool uses: {result['tool_uses']}")

# Stop
adapter.stop_session()
```

### Autonomous Bot Runner

```python
from pathlib import Path
from deia.adapters.bot_runner import BotRunner

# Initialize runner
runner = BotRunner(
    bot_id="CLAUDE-CODE-001",
    work_dir=Path.cwd(),
    task_dir=Path(".deia/hive/tasks"),
    response_dir=Path(".deia/tunnel/claude-to-claude"),
    adapter_type="cli",
    platform_config={
        "claude_cli_path": "claude",
        "timeout_seconds": 300
    }
)

# Start
runner.start()

# Run continuous loop
runner.run_continuous(
    poll_interval=5,  # Check every 5 seconds
    on_iteration=lambda i, r: print(f"Iteration {i}: {r}")
)
```

### Complete Example

See: `examples/cli_bot_runner_example.py`

```bash
# Run test mode (single task)
python examples/cli_bot_runner_example.py --test

# Run continuous mode
python examples/cli_bot_runner_example.py
```

---

## API Reference

### ClaudeCodeCLIAdapter

**Constructor:**
```python
ClaudeCodeCLIAdapter(
    bot_id: str,              # Unique bot ID
    work_dir: Path,           # Working directory
    claude_cli_path: str = "claude",
    timeout_seconds: int = 300
)
```

**Methods:**

- `start_session() -> bool`
  Start Claude Code subprocess

- `send_task(task_content: str, timeout: Optional[int] = None) -> Dict`
  Execute task, returns:
  ```python
  {
      "success": bool,
      "output": str,
      "files_modified": List[str],
      "tool_uses": List[dict],
      "error": Optional[str],
      "duration_seconds": float,
      "timed_out": bool
  }
  ```

- `check_health() -> bool`
  Check if subprocess alive

- `stop_session()`
  Graceful termination (SIGTERM)

- `force_kill()`
  Immediate termination (SIGKILL)

- `get_session_info() -> Dict`
  Session metadata

- `get_output_logs() -> List[str]`
  Stdout buffer

- `get_error_logs() -> List[str]`
  Stderr buffer

### BotRunner

**Constructor:**
```python
BotRunner(
    bot_id: str,
    work_dir: Path,
    task_dir: Path,           # Monitor this directory
    response_dir: Path,       # Write responses here
    adapter_type: str = "api",  # "api" or "cli"
    platform_config: Optional[Dict] = None
)
```

**Methods:**

- `start() -> bool`
  Start runner (initializes adapter)

- `run_once() -> Dict`
  Execute one task check cycle

- `run_continuous(poll_interval: int = 5, max_iterations: Optional[int] = None, on_iteration: Optional[Callable] = None)`
  Run persistent monitoring loop

- `stop()`
  Graceful shutdown

- `get_status() -> Dict`
  Runner and adapter status

---

## Task File Format

Tasks are markdown files in `task_dir`:

**Filename:** `{timestamp}-{from}-{to}-TASK-{description}.md`

**Content:**
```markdown
# Task Title

**To:** CLAUDE-CODE-001
**From:** BEE-001
**Priority:** P1

## Task Description

Your task instructions here...
```

**Priority levels:**
- `P0`: Critical (highest)
- `P1`: High
- `P2`: Normal (default)

---

## Response File Format

Responses are written to `response_dir`:

**Filename:** `{timestamp}-{from}-{to}-RESPONSE-{task_short}-{status}.md`

**Content:**
```markdown
# RESPONSE: {task} - Complete

**From:** CLAUDE-CODE-001
**To:** BEE-001
**Task:** {task_id}
**Status:** ✓ SUCCESS
**Duration:** 2.3 seconds

## Output

{adapter output}

## Files Modified

- hello.py
- test.py

---

**Response generated:** 2025-10-23T23:45:00
```

---

## Integration with BC Subprocess Core

When BC delivers `claude_cli_subprocess.py`, integration is simple:

**1. Add BC's file to project:**
```bash
cp {bc_deliverable}/claude_cli_subprocess.py src/deia/adapters/
```

**2. Update CLI adapter:**
```python
# In claude_code_cli_adapter.py, replace mock import:

# OLD (mock):
from .mock_subprocess import MockClaudeCodeProcess

# NEW (real):
from .claude_cli_subprocess import ClaudeCodeProcess
```

**3. Update initialization:**
```python
# In ClaudeCodeCLIAdapter.__init__():

# OLD:
self.process = MockClaudeCodeProcess(...)

# NEW:
self.process = ClaudeCodeProcess(...)
```

**4. Run tests:**
```bash
pytest tests/test_cli_adapter.py -v
```

**That's it.** The integration layer is designed to match BC's spec exactly.

---

## File Tracking

The adapter automatically tracks file modifications from tool uses:

```python
result = adapter.send_task("Create hello.py and goodbye.py")

print(result["files_modified"])
# Output: ["hello.py", "goodbye.py"]

print(adapter.total_files_modified)
# Set of all files modified during session
```

**Extracted from these tools:**
- `Write` (file_path parameter)
- `Edit` (file_path parameter)
- `str_replace` (file_path or path parameter)

---

## Error Handling

### Timeout

```python
result = adapter.send_task("Long task...", timeout=60)

if result["timed_out"]:
    print("Task exceeded timeout, process killed")
    print(result["output"])  # Partial output before timeout
```

### Process Crash

```python
if not adapter.check_health():
    print("Subprocess died, restarting...")
    adapter.stop_session()
    adapter.start_session()
```

### Task Failure

```python
result = adapter.send_task("Invalid task")

if not result["success"]:
    print(f"Error: {result['error']}")
    print(f"Stderr: {adapter.get_error_logs()}")
```

---

## Testing

**Run all adapter tests:**
```bash
pytest tests/test_cli_adapter.py -v
```

**Run specific test:**
```bash
pytest tests/test_cli_adapter.py::TestClaudeCodeCLIAdapter::test_send_task_with_session -v
```

**Test with real BC subprocess:**
(After BC delivers)
```bash
# Update adapter to use real subprocess
# Tests will run against actual claude code CLI
pytest tests/test_cli_adapter.py -v --real-cli
```

---

## Comparison: API vs CLI Adapter

| Feature | API Adapter | CLI Adapter |
|---------|-------------|-------------|
| **Implementation** | Anthropic Messages API | Claude Code CLI subprocess |
| **Tool Access** | ❌ No (text only) | ✅ Yes (Write, Edit, Bash, Read) |
| **File Operations** | ❌ No | ✅ Yes |
| **Bash Execution** | ❌ No | ✅ Yes |
| **Conversation History** | ✅ Yes | ⚠️ Via file context |
| **Error Handling** | ✅ Structured | ⚠️ Parse stderr |
| **Reliability** | ✅ High | ⚠️ Subprocess complexity |
| **Speed** | ✅ Fast | ⚠️ Slower (process startup) |
| **Testing** | ✅ Easy (mockable) | ⚠️ Harder (subprocess mocks) |
| **Use Case** | Chat, simple tasks | **Autonomous coding** |

**Recommendation:**
- **API adapter:** Questions, analysis, simple responses
- **CLI adapter:** File edits, test execution, multi-step coding

---

## Production Deployment

### Running as Service

```python
# service.py
from deia.adapters.bot_runner import BotRunner
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

runner = BotRunner(
    bot_id="CLAUDE-CODE-001",
    work_dir=Path.cwd(),
    task_dir=Path(".deia/hive/tasks"),
    response_dir=Path(".deia/tunnel/claude-to-claude"),
    adapter_type="cli"
)

runner.start()
runner.run_continuous(poll_interval=5)
```

**Run:**
```bash
# Development
python service.py

# Production (with restart on crash)
while true; do python service.py; sleep 5; done
```

### Monitoring

```python
# Check status endpoint
status = runner.get_status()

print(f"Bot: {status['bot_id']}")
print(f"Status: {status['status']}")
print(f"Tasks completed: {status['session_info']['tasks_completed']}")
print(f"Queue size: {status['task_queue_size']}")
```

---

## Troubleshooting

**Problem:** `ImportError: cannot import ClaudeCodeCLIAdapter`
**Solution:** `pip install -e .` from project root

**Problem:** `ValueError: work_dir does not exist`
**Solution:** Ensure working directory exists before initializing

**Problem:** Tests fail with "Session not active"
**Solution:** Call `adapter.start_session()` before `send_task()`

**Problem:** Mock subprocess always returns same result
**Solution:** Expected until BC delivers real subprocess. Check `result["output"]` contains "[MOCK]"

---

## Next Steps

1. ⏳ **Wait for BC deliverable** (`claude_cli_subprocess.py`)
2. 🔧 **Integrate BC subprocess** (swap mock for real)
3. ✅ **Test with real CLI** (verify actual file operations)
4. 🚀 **Deploy autonomous bots** (persistent task execution)
5. 📊 **Monitor production** (task completion rates, errors)

---

## Files

**Core Implementation:**
- `src/deia/adapters/claude_code_cli_adapter.py` (Integration layer + mock)
- `src/deia/adapters/bot_runner.py` (Autonomous runner)
- `src/deia/adapters/claude_code_adapter.py` (API adapter for comparison)

**Testing:**
- `tests/test_cli_adapter.py` (17 tests, all passing)

**Examples:**
- `examples/cli_bot_runner_example.py` (Complete working example)

**Documentation:**
- This file

**BC Work Packet:**
- `C:/Users/davee/Downloads/uploads/2025-10-23-2345-000-TO-BC-cli-subprocess-core-EGG.md`

---

**Author:** BEE-000 (Q33N)
**Date:** 2025-10-23
**Status:** Integration complete, awaiting BC subprocess core
