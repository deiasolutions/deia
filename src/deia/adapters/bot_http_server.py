"""
Bot HTTP Server - FastAPI server for HTTP/WebSocket communication with bots.

Provides REST API and WebSocket endpoints for:
- Bot health checks (/status)
- Task submission via HTTP (POST /api/task)
- Real-time interaction via WebSocket (/ws)
- Priority queue management (WebSocket > file queue)
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import JSONResponse
import asyncio
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

logger = logging.getLogger(__name__)


class BotHTTPServer:
    """
    Lightweight FastAPI server for bot HTTP/WebSocket communication.
    """

    def __init__(self, bot_id: str, port: int, bot_runner=None):
        self.bot_id = bot_id
        self.port = port
        self.bot_runner = bot_runner
        self.app = FastAPI(title=f"Bot {bot_id} Server")
        self.websocket_queue = asyncio.Queue(maxsize=100)
        self.startup_time = datetime.utcnow()
        self.tasks_processed = 0
        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes."""

        @self.app.get("/status")
        async def get_status():
            """Get bot health and status."""
            uptime = (datetime.utcnow() - self.startup_time).total_seconds()
            status_data = {
                "bot_id": self.bot_id,
                "status": "running" if self.bot_runner and self.bot_runner.running else "idle",
                "port": self.port,
                "uptime_seconds": int(uptime),
                "tasks_processed": self.tasks_processed,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            return JSONResponse(content=status_data)

        @self.app.post("/api/task")
        async def submit_task(body: Dict = None):
            """Submit a task via HTTP."""
            if not body or not body.get("command"):
                raise HTTPException(status_code=400, detail="command is required")

            command = body.get("command")
            task_id = body.get("task_id") or f"HTTP-{uuid.uuid4().hex[:8]}"

            try:
                task = {
                    "task_id": task_id,
                    "command": command,
                    "source": "websocket",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
                self.websocket_queue.put_nowait(task)
                logger.info(f"[{self.bot_id}] Task queued via HTTP: {task_id}")

                return JSONResponse(content={
                    "status": "queued",
                    "task_id": task_id,
                    "message": f"Task {task_id} queued for execution",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }, status_code=202)

            except asyncio.QueueFull:
                raise HTTPException(status_code=429, detail="Task queue full - too many pending tasks")

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time bot interaction."""
            await websocket.accept()
            logger.info(f"[{self.bot_id}] WebSocket client connected")

            try:
                while True:
                    try:
                        data = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)
                        message = json.loads(data)
                    except asyncio.TimeoutError:
                        await websocket.send_json({
                            "type": "ping",
                            "timestamp": datetime.utcnow().isoformat() + "Z"
                        })
                        continue
                    except json.JSONDecodeError:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Invalid JSON format"
                        })
                        continue

                    if message.get("type") == "task":
                        command = message.get("command")
                        if not command:
                            await websocket.send_json({
                                "type": "error",
                                "message": "Missing 'command' field"
                            })
                            continue

                        task_id = f"WS-{uuid.uuid4().hex[:8]}"
                        task = {
                            "task_id": task_id,
                            "command": command,
                            "source": "websocket",
                            "timestamp": datetime.utcnow().isoformat() + "Z"
                        }

                        try:
                            self.websocket_queue.put_nowait(task)
                            await websocket.send_json({
                                "type": "ack",
                                "status": "queued",
                                "task_id": task_id,
                                "timestamp": datetime.utcnow().isoformat() + "Z"
                            })
                            logger.info(f"[{self.bot_id}] Task queued via WebSocket: {task_id}")

                        except asyncio.QueueFull:
                            await websocket.send_json({
                                "type": "error",
                                "message": "Task queue full - too many pending tasks",
                                "status_code": 429
                            })

                    elif message.get("type") == "ping":
                        await websocket.send_json({
                            "type": "pong",
                            "timestamp": datetime.utcnow().isoformat() + "Z"
                        })

                    else:
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Unknown message type: {message.get('type')}"
                        })

            except Exception as e:
                logger.error(f"[{self.bot_id}] WebSocket error: {e}")

    async def get_next_websocket_task(self) -> Optional[Dict[str, Any]]:
        """Get next task from WebSocket queue (non-blocking)."""
        try:
            task = await asyncio.wait_for(
                self.websocket_queue.get(),
                timeout=0.1
            )
            return task
        except asyncio.TimeoutError:
            return None

    def get_next_websocket_task_sync(self) -> Optional[Dict[str, Any]]:
        """Get next task from WebSocket queue (non-blocking, synchronous).

        This is a synchronous wrapper for calling from sync code.
        Uses get_nowait() for true non-blocking behavior.
        """
        try:
            task = self.websocket_queue.get_nowait()
            return task
        except asyncio.QueueEmpty:
            return None


def create_bot_http_server(bot_id: str, port: int, bot_runner=None):
    """Create FastAPI app for bot HTTP server."""
    server = BotHTTPServer(bot_id=bot_id, port=port, bot_runner=bot_runner)
    return server.app, server
