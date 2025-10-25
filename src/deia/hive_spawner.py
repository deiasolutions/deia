"""
DEIA Hive Bot Spawner

Spawns and manages multiple Claude Code CLI worker bots (002, 003, 004, etc.)
for parallel task execution in the DEIA hive system.

Bot 001 (Queen) uses this to spawn worker bots that monitor .deia/hive/tasks/
"""

from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import json
import time

from .adapters.bot_runner import BotRunner


class HiveSpawner:
    """
    Spawns and manages multiple worker bots for DEIA hive.

    Bot 001 (Queen) uses this to spawn bots 002-006 that:
    - Monitor .deia/hive/tasks/ for assigned work
    - Execute tasks autonomously via Claude Code CLI
    - Write responses to .deia/hive/responses/
    - Update .deia/bot-status-board.json
    """

    def __init__(
        self,
        work_dir: Path,
        queen_id: str = "CLAUDE-CODE-001",
        task_dir: Optional[Path] = None,
        response_dir: Optional[Path] = None,
        status_board: Optional[Path] = None
    ):
        """
        Initialize hive spawner.

        Args:
            work_dir: Root working directory (project root)
            queen_id: Queen bot ID (this session)
            task_dir: Task queue directory (default: .deia/hive/tasks)
            response_dir: Response directory (default: .deia/hive/responses)
            status_board: Status board file (default: .deia/bot-status-board.json)
        """
        self.work_dir = Path(work_dir)
        self.queen_id = queen_id

        self.task_dir = task_dir or (self.work_dir / ".deia" / "hive" / "tasks")
        self.response_dir = response_dir or (self.work_dir / ".deia" / "hive" / "responses")
        self.status_board_path = status_board or (self.work_dir / ".deia" / "bot-status-board.json")

        # Ensure directories exist
        self.task_dir.mkdir(parents=True, exist_ok=True)
        self.response_dir.mkdir(parents=True, exist_ok=True)

        # Track spawned bots
        self.bots: Dict[str, BotRunner] = {}
        self.bot_configs: Dict[str, Dict] = {}

    def spawn_bot(
        self,
        bot_id: str,
        role: str = "Worker",
        start_immediately: bool = True
    ) -> bool:
        """
        Spawn a worker bot.

        Args:
            bot_id: Bot identifier (e.g., "CLAUDE-CODE-002")
            role: Bot role (e.g., "Worker", "Drone-Dev", "Drone-Testing")
            start_immediately: Start monitoring immediately

        Returns:
            True if spawned successfully

        Example:
            spawner.spawn_bot("CLAUDE-CODE-002", role="Drone-Dev")
        """
        if bot_id in self.bots:
            self._log(f"Bot {bot_id} already exists")
            return False

        try:
            # Create bot runner with CLI adapter
            runner = BotRunner(
                bot_id=bot_id,
                work_dir=self.work_dir,
                task_dir=self.task_dir,
                response_dir=self.response_dir,
                adapter_type="cli",
                platform_config={
                    "claude_cli_path": "claude",
                    "timeout_seconds": 300
                }
            )

            # Store bot
            self.bots[bot_id] = runner
            self.bot_configs[bot_id] = {
                "role": role,
                "spawned_at": datetime.now().isoformat(),
                "spawned_by": self.queen_id,
                "status": "spawned"
            }

            self._log(f"Spawned bot: {bot_id} (role: {role})")

            # Start if requested
            if start_immediately:
                success = runner.start()
                if success:
                    self.bot_configs[bot_id]["status"] = "running"
                    self._update_status_board(bot_id, "ACTIVE", role)
                    self._log(f"Bot {bot_id} started successfully")
                else:
                    self._log(f"Failed to start bot {bot_id}")
                    return False

            return True

        except Exception as e:
            self._log(f"Failed to spawn bot {bot_id}: {e}")
            return False

    def spawn_multiple(
        self,
        bot_specs: List[Dict[str, str]]
    ) -> Dict[str, bool]:
        """
        Spawn multiple bots at once.

        Args:
            bot_specs: List of bot specifications
                [{"bot_id": "CLAUDE-CODE-002", "role": "Drone-Dev"}, ...]

        Returns:
            Dict mapping bot_id to success status

        Example:
            results = spawner.spawn_multiple([
                {"bot_id": "CLAUDE-CODE-002", "role": "Drone-Dev"},
                {"bot_id": "CLAUDE-CODE-003", "role": "Drone-Testing"},
                {"bot_id": "CLAUDE-CODE-004", "role": "Worker"}
            ])
        """
        results = {}

        for spec in bot_specs:
            bot_id = spec["bot_id"]
            role = spec.get("role", "Worker")

            results[bot_id] = self.spawn_bot(bot_id, role=role)

        return results

    def assign_task(
        self,
        to_bot: str,
        task_content: str,
        priority: str = "P2",
        task_type: str = "TASK"
    ) -> Path:
        """
        Create task file for a bot.

        Args:
            to_bot: Target bot ID
            task_content: Task markdown content
            priority: Priority (P0, P1, P2)
            task_type: Type (TASK, DELEGATION, QUERY, etc.)

        Returns:
            Path to created task file

        Example:
            task_file = spawner.assign_task(
                to_bot="CLAUDE-CODE-002",
                task_content="Fix bug in session_logger.py",
                priority="P1"
            )
        """
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")

        # Extract short description from content (first line)
        first_line = task_content.split('\n')[0].strip('# ').lower()
        desc = '-'.join(first_line.split()[:4])

        filename = f"{timestamp}-{self.queen_id}-{to_bot}-{task_type}-{desc}.md"
        task_file = self.task_dir / filename

        # Format task
        formatted_task = f"""# {task_type}: {desc}

**To:** {to_bot}
**From:** {self.queen_id}
**Priority:** {priority}
**Created:** {datetime.now().isoformat()}

{task_content}
"""

        task_file.write_text(formatted_task, encoding="utf-8")
        self._log(f"Assigned task to {to_bot}: {filename}")

        return task_file

    def get_bot_status(self, bot_id: str) -> Optional[Dict]:
        """
        Get status of a spawned bot.

        Args:
            bot_id: Bot identifier

        Returns:
            Status dict or None if bot doesn't exist
        """
        if bot_id not in self.bots:
            return None

        runner = self.bots[bot_id]
        config = self.bot_configs[bot_id]

        status = runner.get_status()
        status.update(config)

        return status

    def get_all_statuses(self) -> Dict[str, Dict]:
        """
        Get status of all spawned bots.

        Returns:
            Dict mapping bot_id to status
        """
        return {
            bot_id: self.get_bot_status(bot_id)
            for bot_id in self.bots
        }

    def stop_bot(self, bot_id: str) -> bool:
        """
        Stop a worker bot.

        Args:
            bot_id: Bot to stop

        Returns:
            True if stopped successfully
        """
        if bot_id not in self.bots:
            self._log(f"Bot {bot_id} not found")
            return False

        try:
            runner = self.bots[bot_id]
            runner.stop()

            self.bot_configs[bot_id]["status"] = "stopped"
            self._update_status_board(bot_id, "STOPPED", self.bot_configs[bot_id]["role"])

            self._log(f"Stopped bot: {bot_id}")
            return True

        except Exception as e:
            self._log(f"Failed to stop bot {bot_id}: {e}")
            return False

    def stop_all(self) -> None:
        """Stop all spawned bots."""
        for bot_id in list(self.bots.keys()):
            self.stop_bot(bot_id)

    def _update_status_board(self, bot_id: str, status: str, role: str) -> None:
        """
        Update .deia/bot-status-board.json with bot status.

        Args:
            bot_id: Bot identifier
            status: Bot status (ACTIVE, STOPPED, etc.)
            role: Bot role
        """
        try:
            # Read current status board
            if self.status_board_path.exists():
                board = json.loads(self.status_board_path.read_text(encoding="utf-8"))
            else:
                board = {
                    "version": "1.0",
                    "description": "Shared status board - all bots can read this to see what others are doing",
                    "bots": {}
                }

            # Update bot entry
            if bot_id not in board["bots"]:
                board["bots"][bot_id] = {}

            board["bots"][bot_id].update({
                "role": role,
                "status": status,
                "last_heartbeat": datetime.now().isoformat(),
                "spawned_by": self.queen_id
            })

            board["last_updated"] = datetime.now().isoformat()
            board["updated_by"] = self.queen_id

            # Write back
            self.status_board_path.write_text(
                json.dumps(board, indent=4, ensure_ascii=False),
                encoding="utf-8"
            )

        except Exception as e:
            self._log(f"Failed to update status board: {e}")

    def _log(self, message: str) -> None:
        """
        Log message with timestamp.

        Args:
            message: Log message
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [HiveSpawner] {message}")
