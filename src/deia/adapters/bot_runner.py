"""
Autonomous Bot Runner - Persistent bot task execution system

Monitors task queues, executes tasks via platform adapters, reports results.
Designed to run as persistent background process communicating with lead bot.
"""

from typing import Dict, Any, Optional, Callable
from pathlib import Path
from datetime import datetime
import time
import json

from .claude_code_adapter import ClaudeCodeAdapter, parse_task_file, write_response_file
from .claude_code_cli_adapter import ClaudeCodeCLIAdapter
from .claude_sdk_adapter import ClaudeSDKAdapter
from .mock_bot_adapter import MockBotAdapter
from ..services.bot_service import BotService
from ..services.registry import ServiceRegistry


class BotRunner:
    """
    Autonomous bot runner for persistent task execution.

    Monitors task queue directory, executes tasks via platform adapter,
    writes responses, communicates with lead bot.

    Supports multiple platform adapters:
    - ClaudeSDKAdapter: Official Claude Agent SDK (recommended)
    - ClaudeCodeAdapter: Anthropic Messages API
    - ClaudeCodeCLIAdapter: True Claude Code CLI subprocess
    - MockBotAdapter: Testing/demo
    - (Future: LlamaAdapter, CodexAdapter, OpenAIAdapter, etc.)
    """

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        task_dir: Path,
        response_dir: Path,
        adapter_type: str = "api",
        platform_config: Optional[Dict[str, Any]] = None,
        task_cooldown_seconds: int = 10
    ):
        """
        Initialize bot runner.

        Args:
            bot_id: Unique bot identifier (e.g., "CLAUDE-CODE-001")
            work_dir: Working directory for bot operations
            task_dir: Directory to monitor for incoming tasks
            response_dir: Directory to write response files
            adapter_type: Platform adapter ("api" or "cli")
            platform_config: Platform-specific configuration
            task_cooldown_seconds: Seconds to wait after task (0 = no limit, configurable by governance)

        Raises:
            ValueError: If directories don't exist or adapter_type invalid
        """
        if not work_dir.exists():
            raise ValueError(f"work_dir does not exist: {work_dir}")
        if not task_dir.exists():
            raise ValueError(f"task_dir does not exist: {task_dir}")

        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.task_dir = Path(task_dir)
        self.response_dir = Path(response_dir)
        self.response_dir.mkdir(parents=True, exist_ok=True)
        self.task_cooldown_seconds = task_cooldown_seconds
        self.pause_file = self.work_dir / ".deia" / "hive" / "controls" / f"{bot_id}-PAUSE"

        platform_config = platform_config or {}

        # Initialize platform adapter
        if adapter_type == "api":
            self.adapter = ClaudeCodeAdapter(
                bot_id=bot_id,
                work_dir=work_dir,
                **platform_config
            )
        elif adapter_type == "cli":
            self.adapter = ClaudeCodeCLIAdapter(
                bot_id=bot_id,
                work_dir=work_dir,
                **platform_config
            )
        elif adapter_type == "sdk":
            self.adapter = ClaudeSDKAdapter(
                bot_id=bot_id,
                work_dir=work_dir,
                **platform_config
            )
        elif adapter_type == "mock":
            self.adapter = MockBotAdapter(
                bot_id=bot_id,
                work_dir=work_dir,
                **platform_config
            )
        else:
            raise ValueError(f"Unknown adapter_type: {adapter_type}")

        self.adapter_type = adapter_type
        self.running = False
        self.session_started = False
        self.processed_tasks = set()

        # Initialize service layer
        self.registry = ServiceRegistry()
        self.port = self.registry.assign_port(bot_id)
        self.service = BotService(bot_id=bot_id, port=self.port, work_dir=work_dir)
        self.service_started = False

    def start(self) -> bool:
        """
        Start the bot runner (start adapter session and HTTP service).

        Returns:
            True if started successfully

        Raises:
            RuntimeError: If adapter fails to start
        """
        if self.session_started:
            return True

        success = self.adapter.start_session()

        if success:
            self.session_started = True

            # Start HTTP service
            self.service.start()
            self.service_started = True

            # Register in service registry
            self.registry.register(self.bot_id, self.port)

            self._log(f"Bot runner started: {self.bot_id} ({self.adapter_type}) on port {self.port}")
            return True
        else:
            raise RuntimeError("Failed to start adapter session")

    def run_once(self) -> Dict[str, Any]:
        """
        Execute one iteration of task monitoring loop.

        Checks for new tasks, executes highest priority, writes response.

        Returns:
            dict: {
                "task_found": bool,
                "task_executed": bool,
                "task_id": Optional[str],
                "success": Optional[bool],
                "error": Optional[str]
            }
        """
        if not self.session_started:
            return {
                "task_found": False,
                "task_executed": False,
                "task_id": None,
                "success": False,
                "error": "Session not started. Call start() first."
            }

        # Check for service interrupts/termination
        if self.service_started:
            if self.service.check_terminate():
                self._log("Terminate signal received from service")
                self.stop()
                return {
                    "task_found": False,
                    "task_executed": False,
                    "task_id": None,
                    "success": None,
                    "error": "Bot terminated by service request"
                }

            if self.service.check_interrupt():
                self._log("Interrupt signal received from service")
                # Skip current iteration, return to idle
                self.service.update_status("idle")
                return {
                    "task_found": False,
                    "task_executed": False,
                    "task_id": None,
                    "success": None,
                    "error": "Task interrupted by service request"
                }

        # Check adapter health
        if not self.adapter.check_health():
            self._log("Adapter health check failed - attempting restart")
            self.adapter.stop_session()
            self.session_started = False
            self.start()

        # Update service status to idle (waiting for tasks)
        if self.service_started:
            self.service.update_status("idle")

        # Find next task
        task_file = self._find_next_task()

        if not task_file:
            return {
                "task_found": False,
                "task_executed": False,
                "task_id": None,
                "success": None,
                "error": None
            }

        # Parse task
        try:
            task = parse_task_file(task_file)
        except Exception as e:
            self._log(f"Failed to parse task {task_file.name}: {e}")
            return {
                "task_found": True,
                "task_executed": False,
                "task_id": task_file.stem,
                "success": False,
                "error": f"Task parse error: {str(e)}"
            }

        # Execute task
        self._log(f"Executing task: {task['task_id']}")

        # Update service status to working
        if self.service_started:
            self.service.update_status("working", task["task_id"])

        result = self.adapter.send_task(task["content"])

        # Write response
        try:
            response_file = write_response_file(
                response_dir=self.response_dir,
                from_bot=self.bot_id,
                to_bot=task["from"],
                task_id=task["task_id"],
                result=result
            )
            self._log(f"Response written: {response_file.name}")
        except Exception as e:
            self._log(f"Failed to write response: {e}")

        # Mark task as processed
        self.processed_tasks.add(task_file.name)

        # Safety countdown: configurable wait before next task
        # Gives ScrumMaster time to check compliance and intervene
        # 0 = no limit (governed by protocol layer)
        if self.task_cooldown_seconds > 0:
            self._countdown_with_pause(self.task_cooldown_seconds)

        return {
            "task_found": True,
            "task_executed": True,
            "task_id": task["task_id"],
            "success": result["success"],
            "error": result.get("error"),
            "duration": result.get("duration_seconds")
        }

    def run_continuous(
        self,
        poll_interval: int = 5,
        max_iterations: Optional[int] = None,
        on_iteration: Optional[Callable] = None
    ) -> None:
        """
        Run continuous task monitoring loop.

        Args:
            poll_interval: Seconds between task checks
            max_iterations: Stop after N iterations (None = infinite)
            on_iteration: Callback after each iteration: fn(iteration_num, result)

        Raises:
            KeyboardInterrupt: Graceful shutdown on Ctrl+C
        """
        self.running = True
        iteration = 0

        self._log(f"Starting continuous run (poll_interval={poll_interval}s)")

        try:
            while self.running:
                iteration += 1

                result = self.run_once()

                if on_iteration:
                    on_iteration(iteration, result)

                if max_iterations and iteration >= max_iterations:
                    self._log(f"Reached max_iterations ({max_iterations}), stopping")
                    break

                time.sleep(poll_interval)

        except KeyboardInterrupt:
            self._log("Received interrupt, shutting down gracefully")
            self.stop()

    def stop(self) -> None:
        """Stop bot runner, cleanup adapter session, and unregister from registry."""
        self.running = False

        if self.session_started:
            self.adapter.stop_session()
            self.session_started = False

        # Stop HTTP service and unregister from registry
        if self.service_started:
            self.service.stop()
            self.service_started = False
            self.registry.unregister(self.bot_id)

        self._log(f"Bot runner stopped: {self.bot_id}")

    def get_status(self) -> Dict[str, Any]:
        """
        Get current runner status.

        Returns:
            dict: {
                "bot_id": str,
                "adapter_type": str,
                "running": bool,
                "session_started": bool,
                "session_info": dict,
                "processed_tasks": int,
                "task_queue_size": int
            }
        """
        session_info = self.adapter.get_session_info() if self.session_started else {}

        task_queue_size = len([
            f for f in self.task_dir.glob("*.md")
            if f.name not in self.processed_tasks
        ])

        return {
            "bot_id": self.bot_id,
            "adapter_type": self.adapter_type,
            "running": self.running,
            "session_started": self.session_started,
            "session_info": session_info,
            "processed_tasks": len(self.processed_tasks),
            "task_queue_size": task_queue_size
        }

    def _find_next_task(self) -> Optional[Path]:
        """
        Find next task to execute (highest priority, oldest first).

        Returns:
            Path to task file, or None if no tasks
        """
        task_files = [
            f for f in self.task_dir.glob("*.md")
            if f.name not in self.processed_tasks
        ]

        if not task_files:
            return None

        # Sort by priority (P0, P1, P2) then by timestamp (oldest first)
        def priority_key(task_file):
            try:
                task = parse_task_file(task_file)
                priority = task.get("priority", "P2")
                # Extract priority number (P0 -> 0, P1 -> 1, etc.)
                priority_num = int(priority[1]) if len(priority) > 1 else 2
                # Lower number = higher priority
                return (priority_num, task_file.stat().st_mtime)
            except:
                # Fallback: lowest priority, oldest first
                return (99, task_file.stat().st_mtime)

        task_files.sort(key=priority_key)

        return task_files[0]

    def _countdown_with_pause(self, seconds: int) -> None:
        """
        Countdown before next task with pause capability.

        ScrumMaster can pause bot by creating .deia/hive/controls/{bot_id}-PAUSE file.
        Bot will wait until file is removed.

        Args:
            seconds: Seconds to countdown
        """
        for remaining in range(seconds, 0, -1):
            # Check for pause file every second
            if self.pause_file.exists():
                self._log(f"PAUSED by ScrumMaster - waiting for resume")
                while self.pause_file.exists():
                    time.sleep(1)
                self._log(f"RESUMED by ScrumMaster")

            print(f"[{self.bot_id}] Next task in {remaining}s...", end='\r')
            time.sleep(1)

        print(f"[{self.bot_id}] Proceeding to next task" + " " * 20)

    def _log(self, message: str) -> None:
        """
        Log message with timestamp.

        Args:
            message: Log message
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.bot_id}] {message}")
