"""
Scrum Master Terminal Wrapper - Interactive Claude Code terminal with streaming.

Spawns Claude Code as interactive subprocess, streams output to WebSocket clients,
accepts input from HTTP/WebSocket, provides control endpoints.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Set
from pathlib import Path
from datetime import datetime
import subprocess
import threading
import asyncio
import queue
import os
import uvicorn


class TerminalCommand(BaseModel):
    """Command to send to terminal."""
    command: str


class ScrumMasterTerminal:
    """
    Interactive terminal wrapper for Scrum Master Claude Code.

    Spawns Claude Code as subprocess, streams terminal output to connected
    WebSocket clients, accepts commands via HTTP/WebSocket.

    Architecture:
    - Main thread: Runs FastAPI service
    - Reader thread: Reads stdout/stderr from subprocess, broadcasts to WebSocket clients
    - WebSocket connections: Multiple clients can connect to watch terminal
    - HTTP endpoints: Send commands, get status, terminate
    """

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        port: int = 8000,
        claude_cli_path: str = "claude"
    ):
        """
        Initialize Scrum Master terminal.

        Args:
            bot_id: Full bot ID (e.g., "deiasolutions-SCRUM-MASTER-001")
            work_dir: Working directory for Claude Code
            port: Port to run HTTP/WebSocket service on
            claude_cli_path: Path to claude CLI executable
        """
        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.port = port
        self.claude_cli_path = claude_cli_path

        self.process: Optional[subprocess.Popen] = None
        self.running = False
        self.reader_thread: Optional[threading.Thread] = None

        # Output buffer for new clients
        self.output_buffer: List[str] = []
        self.max_buffer_lines = 1000

        # WebSocket clients
        self.websocket_clients: Set[WebSocket] = set()

        # FastAPI app
        self.app = FastAPI(title=f"Scrum Master Terminal: {bot_id}")
        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes."""

        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {
                "status": "ok",
                "bot_id": self.bot_id,
                "running": self.running,
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/status")
        async def get_status():
            """Get terminal status."""
            return {
                "bot_id": self.bot_id,
                "running": self.running,
                "process_alive": self.process.poll() is None if self.process else False,
                "connected_clients": len(self.websocket_clients),
                "buffer_lines": len(self.output_buffer),
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/send")
        async def send_command(cmd: TerminalCommand):
            """Send command to terminal."""
            if not self.running or not self.process:
                raise HTTPException(status_code=400, detail="Terminal not running")

            try:
                self._send_to_terminal(cmd.command)
                return {"success": True, "message": "Command sent"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/terminate")
        async def terminate():
            """Terminate terminal process."""
            self.stop()
            return {"success": True, "message": "Terminal terminated"}

        @self.app.websocket("/ws/terminal")
        async def websocket_terminal(websocket: WebSocket):
            """WebSocket endpoint for terminal streaming."""
            await websocket.accept()
            self.websocket_clients.add(websocket)

            try:
                # Send buffered output to new client
                for line in self.output_buffer:
                    await websocket.send_text(line)

                # Keep connection open, listen for client messages
                while True:
                    data = await websocket.receive_text()
                    # Client sent a command
                    if self.running and self.process:
                        self._send_to_terminal(data)

            except WebSocketDisconnect:
                self.websocket_clients.discard(websocket)
            except Exception as e:
                print(f"[{self.bot_id}] [TERMINAL] WebSocket error: {e}")
                self.websocket_clients.discard(websocket)

    def start(self) -> bool:
        """
        Start Claude Code terminal.

        Returns:
            True if started successfully

        Raises:
            RuntimeError: If failed to start
        """
        if self.running:
            return True

        # Resolve claude executable path
        claude_cmd = self._resolve_claude_path()

        # Spawn Claude Code process
        try:
            self.process = subprocess.Popen(
                [claude_cmd],
                cwd=str(self.work_dir),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout
                text=True,
                bufsize=1,
                env=os.environ.copy()  # Use full environment (ANTHROPIC_API_KEY if set)
            )

            self.running = True

            # Start reader thread
            self.reader_thread = threading.Thread(target=self._read_output, daemon=True)
            self.reader_thread.start()

            print(f"[{self.bot_id}] [TERMINAL] Started Claude Code on PID {self.process.pid}")
            return True

        except Exception as e:
            print(f"[{self.bot_id}] [TERMINAL] Failed to start: {e}")
            raise RuntimeError(f"Failed to start Claude Code: {e}")

    def stop(self):
        """Stop terminal and cleanup."""
        self.running = False

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

            print(f"[{self.bot_id}] [TERMINAL] Stopped")

    def run_service(self):
        """Run HTTP/WebSocket service (blocking)."""
        uvicorn.run(
            self.app,
            host="0.0.0.0",
            port=self.port,
            log_level="warning"
        )

    def _resolve_claude_path(self) -> str:
        """Resolve path to claude CLI executable."""
        if self.claude_cli_path != "claude":
            return self.claude_cli_path

        # Try npm directory
        npm_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "npm")
        claude_cmd_path = os.path.join(npm_dir, "claude.cmd")

        if os.path.exists(claude_cmd_path):
            return claude_cmd_path

        return "claude"  # Fall back to PATH

    def _read_output(self):
        """Read subprocess output and broadcast to WebSocket clients (runs in thread)."""
        if not self.process or not self.process.stdout:
            return

        try:
            for line in self.process.stdout:
                if not self.running:
                    break

                # Add to buffer
                self.output_buffer.append(line)
                if len(self.output_buffer) > self.max_buffer_lines:
                    self.output_buffer.pop(0)

                # Broadcast to all connected WebSocket clients
                # NOTE: asyncio.run() creates new event loop in thread
                for client in list(self.websocket_clients):
                    try:
                        # Schedule coroutine in client's event loop
                        asyncio.run(client.send_text(line))
                    except Exception as e:
                        print(f"[{self.bot_id}] [TERMINAL] Failed to send to client: {e}")
                        self.websocket_clients.discard(client)

        except Exception as e:
            print(f"[{self.bot_id}] [TERMINAL] Reader thread error: {e}")

    def _send_to_terminal(self, command: str):
        """Send command to terminal stdin."""
        if not self.process or not self.process.stdin:
            raise RuntimeError("Terminal process not running")

        try:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
        except Exception as e:
            raise RuntimeError(f"Failed to send command: {e}")
