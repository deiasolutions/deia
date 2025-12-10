"""
DEIA Slash Command - Claude Code CLI Integration

Provides bot coordination through slash command interface.
Supports targeting specific bots, broadcasting, and instruction file updates.
"""

import os
import json
import time
import glob
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict


class SlashCommandHandler:
    """Handles slash commands with bot coordination capabilities."""

    def __init__(self, deia_root: Optional[str] = None):
        """
        Initialize slash command handler.

        Args:
            deia_root: Path to .deia directory. Defaults to ~/.deia
        """
        if deia_root is None:
            deia_root = os.path.join(os.path.expanduser("~"), ".deia")

        self.deia_root = Path(deia_root)
        self.instructions_dir = self.deia_root / "instructions"
        self.history_file = self.deia_root / "slash-history.json"

        # Ensure directories exist
        self.instructions_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(__name__)

    def list_active_bots(self) -> List[str]:
        """
        Get list of all active bots from instruction files.

        Returns:
            List of bot IDs (e.g., ['BOT-00001', 'BOT-00002'])
        """
        if not self.instructions_dir.exists():
            return []

        bot_files = glob.glob(str(self.instructions_dir / "BOT-*-instructions.md"))
        bot_ids = []

        for file_path in bot_files:
            filename = os.path.basename(file_path)
            # Extract BOT-NNNNN from filename
            if filename.startswith("BOT-") and filename.endswith("-instructions.md"):
                bot_id = filename.replace("-instructions.md", "")
                bot_ids.append(bot_id)

        return sorted(bot_ids)

    def send_to_bot(self, bot_id: str, command: str, wait: bool = False, timeout: int = 30) -> Dict:
        """
        Send command to specific bot via instruction file.

        Args:
            bot_id: Target bot ID (e.g., 'BOT-00002')
            command: Command text to send
            wait: Whether to wait for bot response
            timeout: Response timeout in seconds

        Returns:
            Dict with status and response info
        """
        instruction_file = self.instructions_dir / f"{bot_id}-instructions.md"

        if not instruction_file.exists():
            return {
                "success": False,
                "error": f"Bot {bot_id} not found (no instruction file)",
                "bot_id": bot_id
            }

        # Update instruction file with command
        success = self.update_instruction_file(bot_id, command)

        result = {
            "success": success,
            "bot_id": bot_id,
            "command": command,
            "timestamp": datetime.now().isoformat()
        }

        # Record to history
        self._add_to_history(result)

        if wait and success:
            # Wait for bot response (check for report file or status change)
            response = self.wait_for_response(bot_id, timeout)
            result["response"] = response

        return result

    def broadcast_to_all(self, command: str) -> Dict:
        """
        Broadcast command to all active bots.

        Args:
            command: Command text to broadcast

        Returns:
            Dict with broadcast results
        """
        active_bots = self.list_active_bots()

        if not active_bots:
            return {
                "success": False,
                "error": "No active bots found",
                "command": command
            }

        results = []
        for bot_id in active_bots:
            result = self.send_to_bot(bot_id, command, wait=False)
            results.append(result)

        broadcast_result = {
            "success": True,
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "bot_count": len(active_bots),
            "bots": active_bots,
            "results": results
        }

        # Record broadcast to history
        self._add_to_history(broadcast_result)

        return broadcast_result

    def update_instruction_file(self, bot_id: str, command: str) -> bool:
        """
        Append command to bot's instruction file.

        Args:
            bot_id: Target bot ID
            command: Command text to append

        Returns:
            True if successful, False otherwise
        """
        instruction_file = self.instructions_dir / f"{bot_id}-instructions.md"

        if not instruction_file.exists():
            self.logger.error(f"Instruction file not found for {bot_id}")
            return False

        try:
            # Append command as a new section at the end
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(instruction_file, 'a', encoding='utf-8') as f:
                f.write(f"\n\n---\n\n")
                f.write(f"## COMMAND FROM DEIA / ({timestamp})\n\n")
                f.write(f"```\n{command}\n```\n\n")
                f.write(f"**Action:** Read and execute the command above.\n\n")

            self.logger.info(f"Command sent to {bot_id}: {command}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating instruction file for {bot_id}: {e}")
            return False

    def wait_for_response(self, bot_id: str, timeout: int = 30) -> Optional[str]:
        """
        Wait for bot to respond (check for report file or status change).

        Args:
            bot_id: Bot ID to wait for
            timeout: Maximum wait time in seconds

        Returns:
            Response text if found, None otherwise
        """
        start_time = time.time()
        reports_dir = self.deia_root / "reports"

        # Look for recent report files from this bot
        while time.time() - start_time < timeout:
            if reports_dir.exists():
                # Find most recent report from this bot
                pattern = str(reports_dir / f"{bot_id}-*.md")
                reports = glob.glob(pattern)

                if reports:
                    # Get most recent report
                    latest_report = max(reports, key=os.path.getmtime)

                    # Check if it's recent (created after command sent)
                    mtime = os.path.getmtime(latest_report)
                    if mtime > start_time:
                        return f"Report filed: {os.path.basename(latest_report)}"

            time.sleep(1)

        return None

    def _add_to_history(self, entry: Dict):
        """
        Add command/broadcast to history file.

        Args:
            entry: History entry dict
        """
        try:
            history = []

            # Load existing history
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)

            # Append new entry
            history.append(entry)

            # Keep last 1000 entries
            if len(history) > 1000:
                history = history[-1000:]

            # Save history
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            self.logger.error(f"Error updating history: {e}")

    def get_history(self, limit: int = 10) -> List[Dict]:
        """
        Get recent command history.

        Args:
            limit: Number of entries to return

        Returns:
            List of history entries
        """
        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                return history[-limit:]
        except Exception as e:
            self.logger.error(f"Error reading history: {e}")
            return []
