# DEIA Hive Monitoring Dashboard Spec

## Overview

Web-based real-time dashboard for monitoring ScrumMaster ↔ Bot communications with human interjection capability.

## User Story

> "I want a web-based app that listens in on the conversation between the ScrumMaster and the bots. Have the chats listed in the left pane, and in the reading pane show the conversation... and have the ability for me to interject."

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (React/Vue)                      │
│  ┌──────────────┐  ┌────────────────────────────────────┐  │
│  │              │  │                                    │  │
│  │  Chat List   │  │  Conversation View                 │  │
│  │              │  │                                    │  │
│  │ • BOT-002    │  │  [ScrumMaster → BOT-002]          │  │
│  │ • BOT-003    │  │  "Sitting idle violation"         │  │
│  │ • BOT-004    │  │                                    │  │
│  │              │  │  [BOT-002 → ScrumMaster]          │  │
│  │              │  │  "Corrected, waiting for orders"  │  │
│  │              │  │                                    │  │
│  │              │  │  ┌──────────────────────────────┐ │  │
│  │              │  │  │ [Human Input Box]            │ │  │
│  │              │  │  │ "Good job, continue"         │ │  │
│  │              │  │  └──────────────────────────────┘ │  │
│  └──────────────┘  └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ WebSocket
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                       │
│                                                             │
│  • File watcher: .deia/hive/tasks/                         │
│  • File watcher: .deia/hive/responses/                     │
│  • WebSocket broadcast to clients                          │
│  • Human message → task file creation                      │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              File System (.deia/hive/)                      │
│                                                             │
│  tasks/       ← ScrumMaster writes here                    │
│  responses/   ← Bots write here                            │
│  controls/    ← Dashboard can write PAUSE files            │
└─────────────────────────────────────────────────────────────┘
```

## Features

### 1. Chat List (Left Pane)

- List all active bots from `.deia/bot-status-board.json`
- Show bot status indicators:
  - 🟢 Compliant
  - 🟡 Warning (minor violation)
  - 🔴 Violation (major)
  - ⏸️ Paused
  - ❌ Out of Order
- Show unread message count per bot
- Real-time updates via WebSocket

### 2. Conversation View (Right Pane)

- Display chronological conversation between ScrumMaster and selected bot
- Message types:
  - **ScrumMaster → Bot**: Violations, pokes, redirects
  - **Bot → ScrumMaster**: Responses, heartbeats, status updates
  - **Human → Bot/ScrumMaster**: Your interjections
- Color coding:
  - Blue: ScrumMaster messages
  - Gray: Bot messages
  - Green: Human messages
- Auto-scroll to latest message
- Show timestamp for each message

### 3. Human Interjection

**Input Box Features:**
- Text input for your message
- Dropdown to select recipient:
  - Bot directly (writes to `.deia/hive/tasks/{bot_id}`)
  - ScrumMaster (override/directive)
  - Broadcast (all bots)
- Priority selector (P0, P1, P2)
- Quick actions:
  - Pause bot
  - Resume bot
  - Mark out of order
  - Clear violations

**Who to Talk To:**
- **Bot directly**: For specific task assignments, corrections, or overrides
- **ScrumMaster**: For policy changes, protocol updates, or to override violations
- **Orchestrator** (future): For task routing decisions, workload balancing

### 4. Dashboard Features

**Top Bar:**
- Hive health summary:
  - Total bots: X
  - Compliant: Y
  - Violations: Z
  - Out of order: W
- ScrumMaster status indicator
- Refresh button

**Filters:**
- Show only violations
- Show only active conversations
- Show all bots (including idle)

**Search:**
- Search conversation history
- Filter by bot, date, violation type

## Tech Stack

### Backend (Python)
```python
# FastAPI + WebSockets
# File: src/deia/dashboard/server.py

from fastapi import FastAPI, WebSocket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = FastAPI()

class HiveWatcher(FileSystemEventHandler):
    """Watch .deia/hive/ for changes"""
    def on_created(self, event):
        # Parse task/response file
        # Broadcast to WebSocket clients
        pass

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Stream hive events to client

@app.post("/interject")
async def human_interject(bot_id: str, message: str, priority: str):
    # Create task file in .deia/hive/tasks/
    # Broadcast to WebSocket clients
    pass
```

### Frontend (React or Vue)
```javascript
// File: dashboard/src/App.jsx

- React + TailwindCSS
- WebSocket client for real-time updates
- Chat UI components
- Markdown rendering for task/response content
```

## File Structure

```
src/deia/dashboard/
├── server.py           # FastAPI backend
├── watcher.py          # File system watcher
├── parser.py           # Parse task/response files
└── websocket.py        # WebSocket broadcast

dashboard/              # Frontend (separate repo or subdirectory)
├── package.json
├── src/
│   ├── App.jsx
│   ├── ChatList.jsx
│   ├── ConversationView.jsx
│   ├── HumanInput.jsx
│   └── websocket.js
└── public/
```

## API Endpoints

### WebSocket
- `ws://localhost:8000/ws` - Real-time hive events

### REST
- `GET /api/bots` - List all bots
- `GET /api/conversations/{bot_id}` - Get conversation history
- `POST /api/interject` - Human message to bot/ScrumMaster
- `POST /api/pause/{bot_id}` - Pause bot
- `POST /api/resume/{bot_id}` - Resume bot
- `GET /api/status` - Hive health status

## Data Models

### HiveEvent
```json
{
  "type": "task|response|violation|pause|resume",
  "timestamp": "2025-10-23T19:15:00Z",
  "from": "SCRUM-MASTER-001",
  "to": "CLAUDE-CODE-002",
  "content": "Sitting idle violation detected",
  "priority": "P1",
  "file_path": ".deia/hive/tasks/..."
}
```

### Conversation
```json
{
  "bot_id": "CLAUDE-CODE-002",
  "messages": [
    {
      "timestamp": "2025-10-23T19:15:00Z",
      "from": "SCRUM-MASTER-001",
      "to": "CLAUDE-CODE-002",
      "type": "violation",
      "content": "...",
      "severity": "minor"
    }
  ]
}
```

## Implementation Plan

### Phase 1: Backend Foundation
1. FastAPI server with WebSocket support
2. File system watcher for `.deia/hive/`
3. Parser for task/response markdown files
4. WebSocket broadcast for events
5. REST endpoints for bot list, conversations

### Phase 2: Frontend MVP
1. Chat list component
2. Conversation view component
3. WebSocket client integration
4. Basic styling with TailwindCSS

### Phase 3: Human Interjection
1. Input box component
2. POST endpoint for creating task files
3. Quick actions (pause, resume)
4. Priority selector

### Phase 4: Advanced Features
1. Search and filters
2. Violation analytics
3. Export conversation logs
4. Bot performance metrics

## Run Instructions

```bash
# Backend
cd src/deia/dashboard
pip install fastapi uvicorn watchdog websockets
uvicorn server:app --reload --port 8000

# Frontend
cd dashboard
npm install
npm run dev

# Access at http://localhost:3000
```

## Security Considerations

- Read-only by default for most users
- Human interjection requires authentication
- Rate limiting on message creation
- Validate task file content before writing

## Future Enhancements

- Orchestrator integration for task routing decisions
- ML insights: "Bot X performs better on task type Y"
- Historical analytics: violation trends, bot performance over time
- Mobile responsive design
- Multi-user support (team monitoring)

---

**Generated by:** CLAUDE-CODE-001
**Date:** 2025-10-23
**Status:** Specification Ready for Implementation
