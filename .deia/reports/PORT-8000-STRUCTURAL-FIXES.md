# Port 8000 Chat Controller - Structural Fixes Specification
**Date:** 2025-10-25
**Reviewer:** BOT-00004
**Target Architecture:** Professional, scalable, maintainable

---

## Current Structure Issues

### Problem 1: All HTML/CSS/JS in Single app.py File
**Current:** 2586 lines of HTML/CSS/JS mixed with Python backend
**Issue:**
- Hard to maintain (CSS changes require restart)
- No hot reload
- Coupling between front/back too tight
- Difficult to test UI separately

**Solution:** Separate into static files

---

### Problem 2: Flat Component Architecture
**Current:** One monolithic interface with 3 panels (bot list, chat, status)
**Issue:**
- Panels can't be reused independently
- State management scattered
- Hard to add new features

**Solution:** Component-based architecture with clear separation

---

### Problem 3: Chat History Stored in Single JSON File
**Current:** All messages appended to `chat_history.jsonl`, filtered in memory
**Issue:**
- Loads entire history (crashes at scale)
- Linear search is slow
- No indexing
- Pagination is custom and buggy

**Solution:** Session-based storage with proper schema

---

## Recommended New Architecture

### 1. File Structure

```
llama-chatbot/
├── app.py                          # FastAPI server (core logic only)
├── static/
│   ├── index.html                  # Single-page app
│   ├── css/
│   │   ├── layout.css              # Main grid layout
│   │   ├── components.css          # Reusable component styles
│   │   ├── dark-theme.css          # Dark mode variables
│   │   └── responsive.css          # Mobile breakpoints
│   └── js/
│       ├── app.js                  # App initialization
│       ├── components/
│       │   ├── BotLauncher.js      # Launch modal component
│       │   ├── BotList.js          # Bot list panel
│       │   ├── ChatPanel.js        # Chat display & input
│       │   └── StatusBoard.js      # Status dashboard
│       ├── services/
│       │   ├── api.js              # REST API calls
│       │   ├── ws.js               # WebSocket manager
│       │   └── store.js            # State management
│       └── utils/
│           ├── formatters.js       # Message formatting
│           └── validators.js       # Input validation
├── services/
│   ├── bot_manager.py              # Bot lifecycle (launch, stop)
│   ├── message_handler.py          # Message routing logic
│   └── history_store.py            # Chat history persistence
├── models/
│   ├── bot.py                      # Bot data model
│   ├── message.py                  # Message data model
│   └── session.py                  # Session data model
├── config.py                       # Configuration (ports, settings)
└── requirements.txt
```

### 2. Component Hierarchy

**Layout Components (Top-level)**
```
AppLayout
  ├── BotListPanel
  │   ├── PanelHeader
  │   ├── LaunchButton
  │   └── BotList
  │       └── BotItem (x N)
  │           ├── BotStatus
  │           └── BotActions
  ├── ChatPanel
  │   ├── ChatHeader
  │   ├── MessageList
  │   │   └── Message (x N)
  │   ├── TypingIndicator
  │   └── ChatInputGroup
  │       ├── ChatInput
  │       └── SendButton
  └── StatusPanel
      ├── PanelHeader
      └── StatusList
          └── StatusItem (x N)
```

### 3. Data Flow Pattern

```
User Interaction
    ↓
Component Event Handler
    ↓
Store Action (update state)
    ↓
API Service (if needed)
    ↓
Backend Route
    ↓
Business Logic (bot_manager, message_handler)
    ↓
Database/File System
    ↓
Response → Store → Component Re-render
```

### 4. Code Organization by Responsibility

**app.py (FastAPI)**
- Route definitions only
- Delegate to service layer

Example:
```python
@app.post("/api/bot/launch")
async def launch_bot(request: BotLaunchRequest):
    # Delegate to service
    result = await bot_manager.launch(request.bot_id)
    return {"success": result.success, "error": result.error}
```

**services/bot_manager.py**
- Bot lifecycle (launch, stop, status)
- Process management
- Port allocation

**services/message_handler.py**
- Route message to correct bot
- Handle offline bots
- Add message metadata (timestamp, session_id)

**services/history_store.py**
- Session-based storage
- Query by bot_id, session_id
- Pagination support

### 5. Chat History Schema

**From:** All messages in one file (flat)
**To:** Sessions with structured storage

```
Sessions Table:
  ├── session_id (primary key)
  ├── bot_id
  ├── created_at
  ├── updated_at
  └── metadata (JSON)

Messages Table:
  ├── message_id
  ├── session_id (foreign key)
  ├── role (user|assistant)
  ├── content
  ├── timestamp
  └── metadata
```

Query examples:
```python
# Get messages for a session
messages = history_store.get_messages(
    session_id="sess-123",
    limit=100,
    offset=0
)

# Get recent sessions for a bot
sessions = history_store.get_sessions(
    bot_id="BOT-001",
    limit=10
)
```

### 6. State Management

**From:** Scattered global variables
**To:** Centralized store

```javascript
// store.js
const store = {
  state: {
    selectedBotId: null,
    activeBots: {},
    messages: [],
    isLoading: false,
    error: null,
    wsConnected: false
  },

  actions: {
    selectBot(botId) { /* update state */ },
    addMessage(message) { /* update state */ },
    setLoading(value) { /* update state */ },
    setError(error) { /* update state */ }
  },

  subscribe(listener) { /* notify on changes */ }
};

// Usage in components
store.subscribe((newState) => {
  component.render(newState);
});
```

### 7. WebSocket Architecture

**From:** Connected but unused
**To:** Proper real-time manager

```javascript
// services/ws.js
class WebSocketManager {
  constructor(store) {
    this.store = store;
    this.ws = null;
  }

  connect() {
    this.ws = new WebSocket("ws://localhost:8000/ws");
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.store.actions.addMessage(data);
    };
    this.ws.onerror = () => this.store.actions.setError("Connection lost");
  }

  send(message) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }
}
```

### 8. Error Handling Pattern

**From:** Returns success: true even on errors
**To:** Explicit error responses

```python
class ApiResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    data: Optional[dict] = None

# Usage
if bot_not_found:
    return ApiResponse(
        success=False,
        error=f"Bot {bot_id} not found. Available: {available_ids}"
    )
```

---

## Implementation Roadmap

### Week 1: Structural Foundation
- [ ] Extract static files (HTML, CSS, JS)
- [ ] Create component structure
- [ ] Set up state management
- [ ] Refactor Python services layer

### Week 2: Feature Implementation
- [ ] Implement BotLauncher component
- [ ] Implement WebSocket manager
- [ ] Migrate history to session-based storage
- [ ] Fix message routing logic

### Week 3: Polish & Testing
- [ ] Unit tests for services
- [ ] Integration tests for workflows
- [ ] Visual design refinement
- [ ] Performance optimization

---

## Benefits of New Structure

| Current | New |
|---------|-----|
| 2586 lines in one file | 500 lines app.py + modular files |
| No code reuse | Components reusable |
| Hard to test | Unit testable services |
| Tight coupling | Loose coupling via store |
| Single point of failure | Layered architecture |
| No hot reload | Development fast feedback |

---

Generated by BOT-00004
