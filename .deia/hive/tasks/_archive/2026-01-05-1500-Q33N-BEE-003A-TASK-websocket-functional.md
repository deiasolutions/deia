# Task Assignment: TASK-004 - Make WebSocket Functional

**Task ID:** TASK-004
**Assigned to:** BEE-003A
**Assigned by:** Q33N
**Priority:** P0 - Critical (on critical path)
**Sprint:** SPRINT-001 (Integration Wiring)
**Status:** READY - Start Immediately
**Depends On:** None

---

## Task

Transform the current echo-only WebSocket endpoint into a functional broadcast system with channel support. Currently the WebSocket just echoes messages back - it needs connection management and message broadcasting.

---

## Current State

```python
# server.py:424-432
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)  # Just echoes - no broadcast!
    except WebSocketDisconnect:
        return
```

---

## Required Changes

### 1. Create ConnectionManager class

Add before the endpoint definitions (after the global stores around line 30-37):

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel_id: str):
        await websocket.accept()
        if channel_id not in self.active_connections:
            self.active_connections[channel_id] = []
        self.active_connections[channel_id].append(websocket)

    def disconnect(self, websocket: WebSocket, channel_id: str):
        if channel_id in self.active_connections:
            if websocket in self.active_connections[channel_id]:
                self.active_connections[channel_id].remove(websocket)

    async def broadcast(self, channel_id: str, message: dict):
        if channel_id in self.active_connections:
            for connection in self.active_connections[channel_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass  # Handle dead connections gracefully

_ws_manager = ConnectionManager()
```

### 2. Update WebSocket endpoint with channel support

```python
@app.websocket("/api/ws/{channel_id}")
async def websocket_endpoint(websocket: WebSocket, channel_id: str):
    await _ws_manager.connect(websocket, channel_id)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "message":
                msg = _message_store.add_message(
                    channel_id=channel_id,
                    author=data.get("author", "unknown"),
                    content=data.get("content", ""),
                    lane=data.get("lane"),
                    provider=data.get("provider"),
                    token_count=data.get("token_count"),
                )
                await _ws_manager.broadcast(channel_id, {"type": "message", "data": msg})
    except WebSocketDisconnect:
        _ws_manager.disconnect(websocket, channel_id)
```

### 3. Add broadcast hook to post_message() endpoint

Modify the existing `post_message()` to broadcast via WebSocket:

```python
@app.post("/api/messages")
async def post_message(request: MessageRequest) -> Dict:
    item = _message_store.add_message(
        channel_id=request.channel_id,
        author=request.author,
        content=request.content,
        lane=request.lane,
        provider=request.provider,
        token_count=request.token_count,
    )
    # Broadcast to WebSocket clients
    await _ws_manager.broadcast(request.channel_id, {"type": "message", "data": item})
    return {"success": True, "message": item}
```

**Note:** Change `def post_message` to `async def post_message` to support the await.

---

## Files to Modify

| File | Action |
|------|--------|
| `deia_raqcoon/runtime/server.py` | Add ConnectionManager, update WebSocket endpoint, update post_message |

---

## Success Criteria

- [ ] `ConnectionManager` class implemented with connect/disconnect/broadcast methods
- [ ] WebSocket endpoint accepts `channel_id` path parameter (`/api/ws/{channel_id}`)
- [ ] Multiple clients can connect to the same channel
- [ ] Messages broadcast to all clients in the same channel
- [ ] REST `POST /api/messages` triggers WebSocket broadcast to the channel
- [ ] Disconnection handled cleanly (no crashes, connection removed from list)
- [ ] Dead connections handled gracefully in broadcast

---

## Test Approach

1. Start the server
2. Open browser console and connect two WebSocket clients:
```javascript
// Client 1
ws1 = new WebSocket("ws://127.0.0.1:8010/api/ws/test-channel");
ws1.onmessage = (e) => console.log("WS1:", JSON.parse(e.data));

// Client 2
ws2 = new WebSocket("ws://127.0.0.1:8010/api/ws/test-channel");
ws2.onmessage = (e) => console.log("WS2:", JSON.parse(e.data));
```

3. Send message via REST and verify both clients receive it:
```bash
curl -X POST http://127.0.0.1:8010/api/messages \
  -H "Content-Type: application/json" \
  -d '{"channel_id":"test-channel","author":"tester","content":"Hello broadcast!"}'
```

4. Both browser consoles should log the message

---

## Rules

1. Only modify `server.py`
2. Preserve backward compatibility where possible
3. Handle edge cases: empty channels, dead connections, malformed JSON
4. Use existing `_message_store` for persistence
5. Follow async/await patterns correctly

---

## Deliverable

**On Completion:**
1. Create response file: `.deia/hive/responses/2026-01-05-BEE-003A-Q33N-RESPONSE-websocket-functional.md`
2. Include:
   - Summary of changes made
   - Exact lines modified
   - Test results (manual or automated)
   - Any issues encountered
3. Archive this task file to `.deia/hive/tasks/_archive/`
4. **Notify Q33N** that TASK-005 (Minder) can now begin

---

## Working Directory

```
working_dir: C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions
allowed_paths:
  - deia_raqcoon/
  - .deia/hive/
```

---

*Q33N Assignment - SPRINT-001*
