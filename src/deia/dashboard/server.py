"""
DEIA Hive Monitoring Dashboard - FastAPI Backend

Real-time monitoring of ScrumMaster ↔ Bot communications with human interjection.

Features:
- WebSocket streaming of hive events
- File watcher for .deia/hive/ changes
- REST API for bot status, conversations
- Human interjection (create tasks, pause/resume bots)
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json
import asyncio

from .watcher import HiveWatcher
from .parser import parse_task_file, parse_response_file
from .websocket_manager import ConnectionManager

app = FastAPI(
    title="DEIA Hive Dashboard",
    description="Real-time monitoring of bot communications",
    version="1.0.0"
)

# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
work_dir = Path.cwd()
manager = ConnectionManager()
watcher: Optional[HiveWatcher] = None


@app.on_event("startup")
async def startup_event():
    """Start file watcher on startup."""
    global watcher

    hive_dir = work_dir / ".deia" / "hive"

    if not hive_dir.exists():
        print(f"WARNING: Hive directory not found: {hive_dir}")
        print("Creating directory structure...")
        (hive_dir / "tasks").mkdir(parents=True, exist_ok=True)
        (hive_dir / "responses").mkdir(parents=True, exist_ok=True)
        (hive_dir / "controls").mkdir(parents=True, exist_ok=True)
        (hive_dir / "heartbeats").mkdir(parents=True, exist_ok=True)

    watcher = HiveWatcher(
        hive_dir=hive_dir,
        on_event=lambda event: asyncio.create_task(manager.broadcast(event))
    )

    watcher.start()
    print(f"[OK] File watcher started: {hive_dir}")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop file watcher on shutdown."""
    if watcher:
        watcher.stop()
        print("[OK] File watcher stopped")


# Root endpoint - serve dashboard
@app.get("/")
async def root():
    """Serve the dashboard HTML."""
    static_file = Path(__file__).parent / "static" / "index.html"
    if static_file.exists():
        return FileResponse(static_file)
    else:
        return {"message": "Dashboard UI not found. Static files may be missing."}


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket for real-time hive events.

    Client receives:
    {
        "type": "task|response|violation|status_update",
        "timestamp": "2025-10-23T19:15:00Z",
        "from": "SCRUM-MASTER-001",
        "to": "CLAUDE-CODE-002",
        "content": "...",
        "file_path": ".deia/hive/tasks/..."
    }
    """
    await manager.connect(websocket)

    try:
        # Send initial state
        initial_state = get_hive_status()
        await websocket.send_json({
            "type": "initial_state",
            "data": initial_state
        })

        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            # Handle client messages if needed (e.g., ping/pong)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


# REST API endpoints

@app.get("/api/status")
async def get_status():
    """
    Get overall hive health status.

    Returns:
    {
        "total_bots": 8,
        "compliant": 5,
        "violations": 2,
        "out_of_order": 1,
        "scrummaster_active": true
    }
    """
    return get_hive_status()


@app.get("/api/bots")
async def get_bots():
    """List all bots from service registry and ping their HTTP status endpoints."""
    try:
        from datetime import timedelta
        import requests
        from deia.services.registry import ServiceRegistry

        # Use explicit path based on work_dir (set at module load time, before uvicorn reload)
        registry_path = work_dir / ".deia" / "hive" / "registry.json"
        registry = ServiceRegistry(registry_path=registry_path)
        all_bots = registry.get_all_bots()

        bots = []
        now = datetime.now()

        for bot_id, bot_info in all_bots.items():
            # NO HEARTBEAT FILTERING - show ALL bots in registry
            # Scrum Master will handle cleanup, not dashboard

            port = bot_info.get("port")
            bot_status = "unknown"
            current_task = None
            last_heartbeat = bot_info.get("last_heartbeat", "never")

            # ALWAYS ping bot HTTP service to check if alive (5 second timeout)
            if port:
                try:
                    resp = requests.get(f"http://localhost:{port}/status", timeout=5)
                    if resp.status_code == 200:
                        data = resp.json()
                        bot_status = data.get("status", "unknown")
                        current_task = data.get("current_task")
                    else:
                        bot_status = "offline"
                except Exception:
                    # Bot not responding to HTTP - mark offline but still show it
                    bot_status = "offline"
            else:
                bot_status = "no_port"

            bots.append({
                "bot_id": bot_id,
                "role": "Scrum Master" if "SCRUM-MASTER" in bot_id else "worker",
                "status": bot_status,
                "platform": "sdk",
                "port": port,
                "pid": bot_info.get("pid"),
                "last_heartbeat": last_heartbeat,
                "current_task": current_task,
                "unread_count": 0
            })

        # Sort: online bots first, then by bot_id
        bots.sort(key=lambda b: (b["status"] == "offline", b["bot_id"]))

        return bots

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read service registry: {e}")

    try:
        from datetime import timedelta

        # Handle UTF-8 BOM
        board = json.loads(status_board_path.read_text(encoding="utf-8-sig"))
        bots = []
        now = datetime.now()

        for bot_id, bot_info in board.get("bots", {}).items():
            # Only include bots with recent heartbeats (last 5 minutes)
            last_heartbeat = bot_info.get("last_heartbeat")

            if not last_heartbeat:
                continue  # Skip bots with no heartbeat

            # Parse heartbeat timestamp
            heartbeat_time = None
            try:
                # Try parsing ISO format with timezone
                heartbeat_str = str(last_heartbeat)
                if not heartbeat_str.endswith("Z") and "+" not in heartbeat_str:
                    # No timezone, skip this bot
                    continue

                heartbeat_time = datetime.fromisoformat(heartbeat_str.replace("Z", "+00:00"))
                # Remove timezone info for comparison
                if heartbeat_time.tzinfo:
                    heartbeat_time = heartbeat_time.replace(tzinfo=None)

            except (ValueError, AttributeError, TypeError):
                continue  # Skip bots with invalid heartbeat format

            # Only include if heartbeat was within last 5 minutes
            if heartbeat_time and (now - heartbeat_time) > timedelta(minutes=5):
                continue  # Skip stale bots

            bots.append({
                "bot_id": bot_id,
                "role": bot_info.get("role", "Unknown"),
                "status": bot_info.get("status", "UNKNOWN"),
                "platform": bot_info.get("platform", "unknown"),
                "last_heartbeat": bot_info.get("last_heartbeat"),
                "current_task": bot_info.get("current_task"),
                "unread_count": 0  # TODO: Calculate from conversation
            })

        return bots

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read status board: {e}")


@app.get("/api/conversations/{bot_id}")
async def get_conversation(bot_id: str):
    """
    Get conversation history for a specific bot.

    Returns:
    {
        "bot_id": "CLAUDE-CODE-002",
        "messages": [
            {
                "timestamp": "2025-10-23T19:15:00Z",
                "from": "SCRUM-MASTER-001",
                "to": "CLAUDE-CODE-002",
                "type": "violation",
                "content": "Sitting idle violation",
                "severity": "minor",
                "file_path": ".deia/hive/tasks/..."
            }
        ]
    }
    """
    tasks_dir = work_dir / ".deia" / "hive" / "tasks"
    responses_dir = work_dir / ".deia" / "hive" / "responses"

    messages = []

    # Collect tasks for this bot
    for task_file in tasks_dir.glob(f"*-{bot_id}-*.md"):
        try:
            task = parse_task_file(task_file)
            messages.append({
                "timestamp": task.get("timestamp", task_file.stat().st_mtime),
                "from": task.get("from", "UNKNOWN"),
                "to": bot_id,
                "type": "task",
                "content": task.get("content", ""),
                "priority": task.get("priority", "P2"),
                "file_path": str(task_file.relative_to(work_dir))
            })
        except Exception as e:
            print(f"Failed to parse task {task_file.name}: {e}")

    # Collect responses from this bot
    for response_file in responses_dir.glob(f"*-{bot_id}-*.md"):
        try:
            response = parse_response_file(response_file)
            messages.append({
                "timestamp": response.get("timestamp", response_file.stat().st_mtime),
                "from": bot_id,
                "to": response.get("to", "UNKNOWN"),
                "type": "response",
                "content": response.get("content", ""),
                "file_path": str(response_file.relative_to(work_dir))
            })
        except Exception as e:
            print(f"Failed to parse response {response_file.name}: {e}")

    # Sort by timestamp
    messages.sort(key=lambda m: m["timestamp"])

    return {
        "bot_id": bot_id,
        "messages": messages
    }


@app.get("/api/all-hive")
async def get_all_hive_messages():
    """
    Get ALL HIVE broadcast channel messages.

    Returns messages that are part of the team broadcast channel:
    - Tasks to ALL_AGENTS or ALL_HIVE
    - SYNC messages from coordination directory
    - SYNC responses

    Returns:
    {
        "messages": [
            {
                "timestamp": "2025-10-23T19:15:00Z",
                "from": "AGENT-001",
                "to": "ALL_AGENTS",
                "type": "task|coordination|sync",
                "content": "...",
                "file_path": "..."
            }
        ]
    }
    """
    tasks_dir = work_dir / ".deia" / "hive" / "tasks"
    responses_dir = work_dir / ".deia" / "hive" / "responses"
    coordination_dir = work_dir / ".deia" / "hive" / "coordination"

    messages = []

    # Collect broadcast tasks (to ALL_AGENTS, ALL_HIVE, etc.)
    for task_file in tasks_dir.glob("*-ALL_*.md"):
        try:
            task = parse_task_file(task_file)
            messages.append({
                "timestamp": task.get("timestamp", task_file.stat().st_mtime),
                "from": task.get("from", "UNKNOWN"),
                "to": task.get("to", "ALL_HIVE"),
                "type": "task",
                "content": task.get("content", ""),
                "priority": task.get("priority", "P2"),
                "file_path": str(task_file.relative_to(work_dir))
            })
        except Exception as e:
            print(f"Failed to parse task {task_file.name}: {e}")

    # Collect SYNC messages from coordination directory
    if coordination_dir.exists():
        for coord_file in coordination_dir.glob("*-SYNC-*.md"):
            try:
                # Coordination files use same format as responses
                sync_msg = parse_response_file(coord_file)
                messages.append({
                    "timestamp": sync_msg.get("timestamp", coord_file.stat().st_mtime),
                    "from": sync_msg.get("from", "UNKNOWN"),
                    "to": sync_msg.get("to", "ALL_HIVE"),
                    "type": "coordination",
                    "content": sync_msg.get("content", ""),
                    "file_path": str(coord_file.relative_to(work_dir))
                })
            except Exception as e:
                print(f"Failed to parse coordination {coord_file.name}: {e}")

    # Collect SYNC responses
    for response_file in responses_dir.glob("*-SYNC-*.md"):
        try:
            response = parse_response_file(response_file)
            messages.append({
                "timestamp": response.get("timestamp", response_file.stat().st_mtime),
                "from": response.get("from", "UNKNOWN"),
                "to": response.get("to", "ALL_HIVE"),
                "type": "sync",
                "content": response.get("content", ""),
                "file_path": str(response_file.relative_to(work_dir))
            })
        except Exception as e:
            print(f"Failed to parse response {response_file.name}: {e}")

    # Sort by timestamp
    messages.sort(key=lambda m: m["timestamp"])

    return {"messages": messages}


from pydantic import BaseModel

class InterjectRequest(BaseModel):
    to_bot: str
    message: str
    priority: str = "P1"
    from_human: str = "HUMAN-DAVE"

@app.post("/api/interject")
async def human_interject(request: InterjectRequest):
    """
    Human interjection - create task for bot.

    Body:
    {
        "to_bot": "CLAUDE-CODE-002",
        "message": "Stop what you're doing and fix bug X",
        "priority": "P0",
        "from_human": "HUMAN-DAVE"
    }
    """
    tasks_dir = work_dir / ".deia" / "hive" / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{timestamp}-{request.from_human}-{request.to_bot}-HUMAN-INTERJECT.md"
    task_file = tasks_dir / filename

    content = f"""# HUMAN INTERJECT

**To:** {request.to_bot}
**From:** {request.from_human}
**Priority:** {request.priority}
**Created:** {datetime.now().isoformat()}

{request.message}

---
Human interjection via dashboard
"""

    task_file.write_text(content, encoding="utf-8")

    # Broadcast to WebSocket clients
    await manager.broadcast({
        "type": "human_interject",
        "timestamp": datetime.now().isoformat(),
        "from": request.from_human,
        "to": request.to_bot,
        "content": request.message,
        "priority": request.priority,
        "file_path": str(task_file.relative_to(work_dir))
    })

    return JSONResponse({
        "success": True,
        "file": str(task_file.relative_to(work_dir))
    })


@app.post("/api/pause/{bot_id}")
async def pause_bot(bot_id: str):
    """
    Pause a bot (create PAUSE file).

    ScrumMaster will detect and halt the bot.
    """
    controls_dir = work_dir / ".deia" / "hive" / "controls"
    controls_dir.mkdir(parents=True, exist_ok=True)

    pause_file = controls_dir / f"{bot_id}-PAUSE"

    pause_content = f"""# BOT PAUSED

**Bot:** {bot_id}
**Time:** {datetime.now().isoformat()}
**Paused By:** Human via Dashboard

Bot has been PAUSED.
To resume: Delete this file.
"""

    pause_file.write_text(pause_content, encoding="utf-8")

    await manager.broadcast({
        "type": "bot_paused",
        "timestamp": datetime.now().isoformat(),
        "bot_id": bot_id,
        "paused_by": "HUMAN"
    })

    return JSONResponse({"success": True, "bot_id": bot_id, "paused": True})


@app.post("/api/resume/{bot_id}")
async def resume_bot(bot_id: str):
    """
    Resume a paused bot (delete PAUSE file).
    """
    pause_file = work_dir / ".deia" / "hive" / "controls" / f"{bot_id}-PAUSE"

    if pause_file.exists():
        pause_file.unlink()

        await manager.broadcast({
            "type": "bot_resumed",
            "timestamp": datetime.now().isoformat(),
            "bot_id": bot_id,
            "resumed_by": "HUMAN"
        })

        return JSONResponse({"success": True, "bot_id": bot_id, "resumed": True})
    else:
        return JSONResponse({
            "success": False,
            "error": f"Bot {bot_id} is not paused"
        }, status_code=404)


@app.post("/api/interrupt/{bot_id}")
async def interrupt_bot(bot_id: str):
    """
    Send interrupt signal (Ctrl+C) to bot.

    NOTE: This requires access to bot process - may need bot runner integration.
    """
    # TODO: Integrate with HiveSpawner to send interrupt to bot process
    # For now, create an INTERRUPT task

    tasks_dir = work_dir / ".deia" / "hive" / "tasks"
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{timestamp}-SCRUM-MASTER-001-{bot_id}-INTERRUPT.md"
    task_file = tasks_dir / filename

    content = f"""# INTERRUPT

**To:** {bot_id}
**From:** SCRUM-MASTER-001 (via Human)
**Priority:** P0

STOP CURRENT OPERATION IMMEDIATELY.

Interrupted by human via dashboard at {datetime.now().isoformat()}.

Await new instructions.
"""

    task_file.write_text(content, encoding="utf-8")

    return JSONResponse({"success": True, "bot_id": bot_id, "interrupted": True})


# Helper functions

def get_hive_status() -> Dict[str, Any]:
    """Get overall hive health status."""
    status_board_path = work_dir / ".deia" / "bot-status-board.json"

    if not status_board_path.exists():
        return {
            "total_bots": 0,
            "compliant": 0,
            "violations": 0,
            "out_of_order": 0,
            "scrummaster_active": False
        }

    try:
        # Handle UTF-8 BOM
        board = json.loads(status_board_path.read_text(encoding="utf-8-sig"))
        bots = board.get("bots", {})

        # Count statuses
        total = len(bots)
        active = sum(1 for b in bots.values() if b.get("status") == "ACTIVE")
        violations = sum(1 for b in bots.values() if b.get("status") in ["VIOLATION", "WARNING"])
        out_of_order = sum(1 for b in bots.values() if b.get("status") == "OUT_OF_ORDER")

        return {
            "total_bots": total,
            "compliant": active,
            "violations": violations,
            "out_of_order": out_of_order,
            "scrummaster_active": True  # TODO: Check if ScrumMaster is running
        }

    except Exception as e:
        print(f"Failed to read status board: {e}")
        return {
            "total_bots": 0,
            "compliant": 0,
            "violations": 0,
            "out_of_order": 0,
            "scrummaster_active": False
        }


if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("DEIA Hive Monitoring Dashboard")
    print("=" * 70)
    print(f"Work Dir: {work_dir}")
    print(f"Hive Dir: {work_dir / '.deia' / 'hive'}")
    print()
    print("Starting server...")
    print("Access dashboard at: http://localhost:8000")
    print("=" * 70)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
