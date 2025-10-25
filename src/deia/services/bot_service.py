"""
Bot HTTP Service - Provides REST API for bot control.

Each bot runs a FastAPI service that Scrum Master can call for:
- Status queries
- Interrupts
- Direct messages
- Health checks
- Termination
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import threading
import uvicorn
import os


class DirectMessage(BaseModel):
    """Direct message from Scrum Master to bot."""
    from_bot: str
    content: str
    priority: str = "P2"


class BotServiceConfig(BaseModel):
    """Configuration for bot service."""
    bot_id: str
    port: int
    work_dir: Path


class BotService:
    """
    HTTP service for bot control and status.

    Runs in background thread alongside bot's task execution loop.
    Provides endpoints for Scrum Master to interact with bot directly.
    """

    def __init__(self, bot_id: str, port: int, work_dir: Path):
        """
        Initialize bot service.

        Args:
            bot_id: Full bot ID (e.g., "deiasolutions-CLAUDE-CODE-001")
            port: Port to run service on
            work_dir: Bot working directory
        """
        self.bot_id = bot_id
        self.port = port
        self.work_dir = Path(work_dir)
        self.app = FastAPI(title=f"Bot Service: {bot_id}")
        self.running = False
        self.server_thread: Optional[threading.Thread] = None

        # Shared state (thread-safe via simple assignment)
        self.current_status = "idle"
        self.current_task: Optional[str] = None
        self.interrupt_requested = False
        self.terminate_requested = False
        self.direct_messages: list = []

        # Setup routes
        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes."""

        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {"status": "ok", "bot_id": self.bot_id, "timestamp": datetime.now().isoformat()}

        @self.app.get("/status")
        async def get_status():
            """
            Get current bot status.

            Returns:
            {
                "bot_id": "deiasolutions-CLAUDE-CODE-001",
                "status": "working|idle|paused",
                "current_task": "task-id or null",
                "port": 8001,
                "pid": 12345
            }
            """
            return {
                "bot_id": self.bot_id,
                "status": self.current_status,
                "current_task": self.current_task,
                "port": self.port,
                "pid": os.getpid(),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/interrupt")
        async def interrupt():
            """
            Interrupt current task.

            Bot will stop current work and return to idle state.
            """
            print(f"[{self.bot_id}] [SERVICE] Interrupt requested")
            self.interrupt_requested = True
            return {"success": True, "message": "Interrupt signal sent"}

        @self.app.post("/terminate")
        async def terminate():
            """
            Request bot termination.

            Bot will finish current task and shut down gracefully.
            """
            print(f"[{self.bot_id}] [SERVICE] Terminate requested")
            self.terminate_requested = True
            return {"success": True, "message": "Terminate signal sent"}

        @self.app.post("/message")
        async def direct_message(msg: DirectMessage):
            """
            Send direct message to bot.

            For urgent communications that don't need full task file.
            Bot should check this periodically.
            """
            print(f"[{self.bot_id}] [SERVICE] Direct message from {msg.from_bot}: {msg.content[:50]}...")

            self.direct_messages.append({
                "from": msg.from_bot,
                "content": msg.content,
                "priority": msg.priority,
                "timestamp": datetime.now().isoformat()
            })

            return {"success": True, "message": "Message queued"}

        @self.app.get("/messages")
        async def get_messages():
            """
            Get queued direct messages.

            Bot calls this to check for urgent messages from Scrum Master.
            """
            messages = self.direct_messages.copy()
            self.direct_messages.clear()  # Clear after reading
            return {"messages": messages}

    def start(self):
        """Start service in background thread."""
        if self.running:
            return

        self.running = True

        def run_server():
            uvicorn.run(
                self.app,
                host="0.0.0.0",
                port=self.port,
                log_level="warning"  # Reduce noise
            )

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

        print(f"[{self.bot_id}] [SERVICE] Started on port {self.port}")

    def stop(self):
        """Stop service."""
        self.running = False
        # Note: uvicorn doesn't have easy programmatic shutdown
        # In production, use process management
        print(f"[{self.bot_id}] [SERVICE] Stopped")

    def update_status(self, status: str, task: Optional[str] = None):
        """Update bot status (called by bot task loop)."""
        self.current_status = status
        self.current_task = task

    def check_interrupt(self) -> bool:
        """Check if interrupt was requested. Clears flag after reading."""
        if self.interrupt_requested:
            self.interrupt_requested = False
            return True
        return False

    def check_terminate(self) -> bool:
        """Check if terminate was requested."""
        return self.terminate_requested
