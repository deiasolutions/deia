# DEIA Multi-Agent Orchestration Architecture

**Built on Claude Agent SDK** - Leverages Anthropic's official SDK with our multi-agent coordination layer.

## Overview

This architecture enables you to run multiple AI agents (Claude Code, Anthropic API, Codex, OpenAI, Llama) coordinated by a Scrum Master, with dual communication channels (file-based + HTTP) and real-time dashboard monitoring.

## What We Built

### Core Components

#### 1. **Claude SDK Adapter** (`src/deia/adapters/claude_sdk_adapter.py`)
- Wraps Anthropic's `claude-agent-sdk` for Claude Code integration
- Provides standardized interface for BotRunner
- Handles async streaming responses
- Supports custom MCP tools
- **RECOMMENDED** for Claude Code bots

#### 2. **Bot Service Layer** (`src/deia/services/bot_service.py`)
- HTTP REST API for each worker bot
- Endpoints: `/health`, `/status`, `/interrupt`, `/terminate`, `/message`
- Runs in background thread alongside task execution
- Enables Scrum Master to control bots directly

#### 3. **Service Registry** (`src/deia/services/registry.py`)
- Central registry at `.deia/hive/registry.json`
- Bot discovery via consistent port hashing (8001-8999)
- Tracks bot metadata: port, PID, status, heartbeat
- Allows Scrum Master to find and communicate with workers

#### 4. **Bot Runner** (`src/deia/adapters/bot_runner.py`)
- Orchestrates bot lifecycle: start, run, stop
- Monitors task queue (`.deia/hive/tasks/{bot-id}/`)
- Executes tasks via platform adapter
- Writes responses to `.deia/hive/responses/`
- Starts HTTP service and registers in registry
- **NOW SUPPORTS SDK ADAPTER** (`adapter_type="sdk"`)

#### 5. **Scrum Master Terminal** (`src/deia/services/scrum_master_terminal.py`)
- Interactive Claude Code wrapper for Scrum Master
- WebSocket streaming of terminal output
- HTTP endpoints for sending commands
- Real-time dashboard integration
- **Alternative to batch task coordination**

### Adapter Types Supported

| Adapter Type | Description | Use Case | Status |
|--------------|-------------|----------|--------|
| `sdk` | **Official Claude Agent SDK** | Claude Code (recommended) | ✅ Ready |
| `api` | Anthropic Messages API | API-based bots (no credits) | ✅ Ready |
| `cli` | Raw subprocess Claude Code | Legacy/testing | ✅ Ready |
| `mock` | Mock bot for testing | Development/demo | ✅ Ready |
| `codex` | OpenAI Codex | Future | 🔜 Planned |
| `openai` | OpenAI GPT-4 | Future | 🔜 Planned |
| `llama` | LLaMA/local models | Future | 🔜 Planned |

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         DASHBOARD                                │
│                     (http://localhost:8000)                      │
│  - WebSocket: real-time hive events                             │
│  - WebSocket: Scrum Master terminal streaming                   │
│  - REST API: bot status, task creation                          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ HTTP/WebSocket
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                   SCRUM MASTER                                   │
│              (deiasolutions-SCRUM-MASTER-001)                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Claude Agent SDK (interactive)                             ││
│  │  - Terminal wrapper with WebSocket streaming                ││
│  │  - HTTP endpoints: /send, /health, /status, /terminate      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Coordinates via:                                                │
│  1. File-based tasks → .deia/hive/tasks/{bot-id}/               │
│  2. HTTP service calls → http://localhost:{bot-port}/           │
│  3. Service registry → .deia/hive/registry.json                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┬───────────────┐
         │                           │               │
         ▼                           ▼               ▼
┌────────────────┐         ┌────────────────┐  ┌────────────────┐
│  WORKER BOT 001│         │  WORKER BOT 002│  │  WORKER BOT 003│
│  (Claude SDK)  │         │  (Anthropic API│  │  (Future: Llama│
│  Port: 8xxx    │         │   Port: 8yyy   │  │   Port: 8zzz)  │
├────────────────┤         ├────────────────┤  ├────────────────┤
│ BotRunner      │         │ BotRunner      │  │ BotRunner      │
│ + BotService   │         │ + BotService   │  │ + BotService   │
│ + Adapter(SDK) │         │ + Adapter(API) │  │ + Adapter(???) │
└────────────────┘         └────────────────┘  └────────────────┘
         │                           │               │
         │ Monitors tasks            │               │
         │ Writes responses          │               │
         ▼                           ▼               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FILE SYSTEM COMMUNICATION                      │
│  .deia/hive/                                                     │
│    ├── tasks/         # Task assignments (by bot ID)            │
│    ├── responses/     # Task completion responses               │
│    ├── registry.json  # Bot discovery registry                  │
│    ├── controls/      # Pause/resume signals                    │
│    └── heartbeats/    # Bot health monitoring                   │
└─────────────────────────────────────────────────────────────────┘
```

## Dual Communication Channels

### 1. File-Based (Async, Durable)
**Use for:** Task assignments, responses, documentation

- **Tasks:** `.deia/hive/tasks/{bot-id}/{timestamp}-{priority}-{task-id}.md`
- **Responses:** `.deia/hive/responses/{timestamp}-{from-bot}-to-{to-bot}-{task-id}.md`
- **Format:** Markdown with YAML frontmatter

**Example Task File:**
```markdown
---
from: deiasolutions-SCRUM-MASTER-001
to: deiasolutions-CLAUDE-CODE-001
task_id: task_20251024_001
priority: P1
created_at: 2025-10-24T10:00:00Z
---

# Task: Implement user authentication

Please implement JWT-based authentication with the following requirements:
- Login endpoint
- Token validation middleware
- Refresh token rotation
```

### 2. HTTP Service (Sync, Real-Time)
**Use for:** Control signals, status queries, interrupts

Each bot runs FastAPI service on assigned port.

**Endpoints:**
```bash
GET  /health                # Health check
GET  /status                # Current status
POST /interrupt             # Stop current task
POST /terminate             # Shutdown bot
POST /message               # Direct message
GET  /messages              # Get queued messages
```

**Example:**
```bash
# Get bot status
curl http://localhost:8001/status

# Interrupt current task
curl -X POST http://localhost:8001/interrupt

# Send direct message
curl -X POST http://localhost:8001/message \
  -H "Content-Type: application/json" \
  -d '{"from_bot": "SCRUM-MASTER-001", "content": "Pause and wait for review", "priority": "P0"}'
```

## Bot ID Format

Human-readable format: `{repo}-{role}-{number}`

**Examples:**
- `deiasolutions-SCRUM-MASTER-001`
- `deiasolutions-CLAUDE-CODE-001`
- `deiasolutions-CLAUDE-CODE-002`
- `familybondbot-SCRUM-MASTER-001`
- `familybondbot-LLAMA-001`

## Usage Examples

### Example 1: Launch Scrum Master with Interactive Terminal

```bash
# Start Scrum Master with terminal streaming to dashboard
python run_scrum_master_terminal.py \
  --repo deiasolutions \
  --port 8000

# Open dashboard in browser
# Navigate to: http://localhost:8000
# Watch real-time terminal output
# Send commands via WebSocket or HTTP POST /send
```

### Example 2: Launch Worker Bot (Claude SDK)

```python
from pathlib import Path
from src.deia.adapters.bot_runner import BotRunner

# Create task directories
work_dir = Path.cwd()
task_dir = work_dir / ".deia" / "hive" / "tasks" / "deiasolutions-CLAUDE-CODE-001"
response_dir = work_dir / ".deia" / "hive" / "responses"
task_dir.mkdir(parents=True, exist_ok=True)
response_dir.mkdir(parents=True, exist_ok=True)

# Initialize bot with SDK adapter
bot = BotRunner(
    bot_id="deiasolutions-CLAUDE-CODE-001",
    work_dir=work_dir,
    task_dir=task_dir,
    response_dir=response_dir,
    adapter_type="sdk",  # Use official Claude Agent SDK
    platform_config={
        "model": "claude-sonnet-4.5",
        "max_iterations": 50
    }
)

# Start bot
bot.start()

# Run continuous monitoring
bot.run_continuous(poll_interval=5)
```

### Example 3: Launch Mock Bot for Testing

```python
from pathlib import Path
from src.deia.adapters.bot_runner import BotRunner

bot = BotRunner(
    bot_id="deiasolutions-MOCK-001",
    work_dir=Path.cwd(),
    task_dir=Path(".deia/hive/tasks/deiasolutions-MOCK-001"),
    response_dir=Path(".deia/hive/responses"),
    adapter_type="mock"
)

bot.start()
bot.run_continuous(max_iterations=10)  # Run 10 iterations for testing
```

### Example 4: Scrum Master Assigns Task via Files

```python
from pathlib import Path
from datetime import datetime

# Create task file
task_dir = Path(".deia/hive/tasks/deiasolutions-CLAUDE-CODE-001")
task_file = task_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}-P1-refactor-auth.md"

task_content = """---
from: deiasolutions-SCRUM-MASTER-001
to: deiasolutions-CLAUDE-CODE-001
task_id: refactor-auth-001
priority: P1
created_at: {timestamp}
---

# Task: Refactor Authentication Module

Refactor the authentication module to use dependency injection:
1. Extract auth logic from routes
2. Create AuthService class
3. Add unit tests
4. Update documentation

Please complete within 30 minutes.
""".format(timestamp=datetime.now().isoformat())

task_file.write_text(task_content, encoding='utf-8')
print(f"Task created: {task_file}")
```

### Example 5: Scrum Master Controls Bot via HTTP

```python
import requests

bot_url = "http://localhost:8001"  # Bot's service port from registry

# Get status
status = requests.get(f"{bot_url}/status").json()
print(f"Bot status: {status}")

# Send direct message
response = requests.post(
    f"{bot_url}/message",
    json={
        "from_bot": "deiasolutions-SCRUM-MASTER-001",
        "content": "Please prioritize bug fixes over new features",
        "priority": "P0"
    }
)
print(f"Message sent: {response.json()}")

# Interrupt current task
interrupt = requests.post(f"{bot_url}/interrupt")
print(f"Interrupt sent: {interrupt.json()}")
```

### Example 6: Query Service Registry

```python
from src.deia.services.registry import ServiceRegistry

registry = ServiceRegistry()

# Get all bots
all_bots = registry.get_all_bots()
print(f"Registered bots: {list(all_bots.keys())}")

# Get specific bot
bot = registry.get_bot("deiasolutions-CLAUDE-CODE-001")
print(f"Bot info: {bot}")

# Get bot service URL
url = registry.get_bot_url("deiasolutions-CLAUDE-CODE-001")
print(f"Bot URL: {url}")

# Get all bots for a repo
repo_bots = registry.get_bots_by_repo("deiasolutions")
print(f"Repo bots: {list(repo_bots.keys())}")
```

## Dependencies

```bash
# Install dependencies
pip install claude-agent-sdk  # Official Claude SDK
pip install fastapi uvicorn   # HTTP services
pip install python-multipart  # Form data
pip install websockets         # Real-time streaming

# Required external tools
npm install -g @anthropic-ai/claude-code  # Claude Code CLI
```

## Configuration

### Environment Variables

```bash
# For API-based bots
export ANTHROPIC_API_KEY="sk-ant-..."

# For Claude Code (claude.ai auth)
# Just run: claude login
```

### Bot Configuration

```python
# SDK adapter (recommended for Claude Code)
platform_config = {
    "model": "claude-sonnet-4.5",
    "max_iterations": 50,
    "custom_tools": []  # MCP tools
}

# API adapter
platform_config = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 4096
}

# CLI adapter
platform_config = {
    "claude_cli_path": "claude",  # or full path
    "ready_signal": "✓",
    "completion_signal": "Done"
}
```

## Multi-Auth Support

**Problem:** Can't run both claude.ai-auth Claude Code AND API-key Claude Code simultaneously.

**Solution:** Environment isolation per bot type.

- **Claude Code bots (SDK/CLI):** Uses claude.ai authentication (no ANTHROPIC_API_KEY)
- **API bots:** Uses ANTHROPIC_API_KEY environment variable
- **Subprocess isolation:** SDK/CLI adapters remove API key from subprocess environment

This allows mixing:
- Scrum Master: Claude Code (claude.ai auth)
- Worker 001: Claude Code SDK (claude.ai auth)
- Worker 002: Anthropic API (API key auth)
- Worker 003: Llama (no auth)

## Next Steps

1. **Test end-to-end:** Launch Scrum Master + 2 workers, assign tasks
2. **Dashboard integration:** Add terminal streaming to existing dashboard
3. **Add more adapters:** OpenAI, Codex, Llama
4. **Bot identity/context:** Load bot-specific instructions and context
5. **Advanced coordination:** Task dependencies, parallel execution, error recovery

## Files Created/Modified

**New Files:**
- `src/deia/adapters/claude_sdk_adapter.py` - SDK-based adapter
- `src/deia/services/bot_service.py` - HTTP service for bots
- `src/deia/services/registry.py` - Service registry
- `src/deia/services/scrum_master_terminal.py` - Interactive terminal wrapper
- `run_scrum_master_terminal.py` - Scrum Master launcher

**Modified Files:**
- `src/deia/adapters/bot_runner.py` - Added service integration, SDK adapter support
- `src/deia/adapters/claude_cli_subprocess.py` - Environment isolation for multi-auth

## Architecture Benefits

✅ **Multi-platform:** Run Claude Code, Anthropic API, Codex, OpenAI, Llama together
✅ **Dual channels:** File-based (async) + HTTP (sync) communication
✅ **Discovery:** Service registry for bot coordination
✅ **Control:** Direct bot control via HTTP endpoints
✅ **Monitoring:** Dashboard with real-time WebSocket streaming
✅ **Isolation:** Multi-auth support via environment isolation
✅ **Official SDK:** Leverages Anthropic's claude-agent-sdk
✅ **Extensible:** Easy to add new adapter types

## Troubleshooting

### Bot won't start with SDK adapter

```bash
# Check Claude Code is installed
npm list -g @anthropic-ai/claude-code

# Install if missing
npm install -g @anthropic-ai/claude-code

# Check Python package
python -c "import claude_agent_sdk; print('OK')"
```

### Port conflicts

```bash
# Check registry
cat .deia/hive/registry.json

# Manually assign port
platform_config = {"port": 8050}
```

### Dashboard not showing terminal

```bash
# Check WebSocket connection
# Browser console should show: "WebSocket connected"

# Check Scrum Master is running
curl http://localhost:8000/health
```

## Summary

You now have a complete multi-agent orchestration system built on Claude Agent SDK that supports:
- Multiple AI platforms (Claude Code, API, future: Codex, Llama, OpenAI)
- Dual communication (files + HTTP)
- Service discovery and control
- Real-time monitoring
- Multi-auth isolation

Ready to coordinate AI agents at scale!
