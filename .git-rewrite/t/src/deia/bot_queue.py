#!/usr/bin/env python3
"""
DEIA Bot Queue Service

FIFO queue with skill tracking for optimal bot selection in multi-bot coordination.

Features:
- FIFO check-in tracking
- Skill and context profile per bot
- Best available bot selection (skill + context matching)
- Idle bot management (assign prep tasks)
- Persistence to JSON

Usage:
    from deia.bot_queue import BotQueue

    queue = BotQueue()
    queue.add_bot("BOT-00002", skills=["testing", "python"], context_history=[])
    next_bot = queue.get_next_available(required_skills=["testing"])
    queue.mark_busy(next_bot, "Running tests")
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict


class BotQueue:
    """
    Manages FIFO queue of bots with skill tracking for optimal selection.
    """

    def __init__(self, queue_file: Optional[Path] = None):
        """
        Initialize bot queue.

        Args:
            queue_file: Path to queue JSON file. Defaults to ~/.deia/bot-queue.json
        """
        if queue_file is None:
            queue_file = Path.home() / ".deia" / "bot-queue.json"

        self.queue_file = Path(queue_file)
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)

        self.data = self._load_queue()

    def _load_queue(self) -> Dict:
        """Load queue from disk, create if doesn't exist."""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        # Default queue structure
        return {
            "queue": [],
            "profiles": {},
            "version": "1.0"
        }

    def _save_queue(self):
        """Save queue to disk."""
        with open(self.queue_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_bot(
        self,
        bot_id: str,
        skills: List[str],
        context_history: List[str]
    ) -> None:
        """
        Add bot to queue with profile.

        Args:
            bot_id: Bot ID (e.g., "BOT-00002")
            skills: List of skills (e.g., ["testing", "python"])
            context_history: Recent work context (e.g., ["worked on sync"])
        """
        now = datetime.now().isoformat()

        # Add to queue if not already there
        if bot_id not in self.data["queue"]:
            self.data["queue"].append(bot_id)

        # Create/update profile
        self.data["profiles"][bot_id] = {
            "bot_id": bot_id,
            "skills": skills,
            "context_history": context_history.copy(),
            "status": "available",
            "current_task": None,
            "idle_prep": None,
            "added_at": now,
            "last_updated": now
        }

        self._save_queue()

    def remove_bot(self, bot_id: str) -> None:
        """
        Remove bot from queue.

        Args:
            bot_id: Bot ID to remove
        """
        if bot_id in self.data["queue"]:
            self.data["queue"].remove(bot_id)

        if bot_id in self.data["profiles"]:
            del self.data["profiles"][bot_id]

        self._save_queue()

    def get_next_available(
        self,
        required_skills: Optional[List[str]] = None,
        context_keywords: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Get best available bot from queue.

        Selection algorithm:
        1. Filter to available bots (not busy, no idle prep)
        2. If required_skills provided, prefer bots with matching skills
        3. If context_keywords provided, prefer bots with relevant context
        4. Return first match in FIFO order

        Args:
            required_skills: List of required skills (optional)
            context_keywords: Context keywords to match (optional)

        Returns:
            Bot ID of best available bot, or None if queue empty
        """
        # Get available bots (not busy, no idle prep)
        available = []
        for bot_id in self.data["queue"]:
            profile = self.data["profiles"].get(bot_id)
            if profile and profile["status"] == "available" and profile["idle_prep"] is None:
                available.append(bot_id)

        if not available:
            return None

        # No skill requirements - return first available
        if not required_skills and not context_keywords:
            return available[0]

        # Score bots based on skill and context match
        scored_bots = []
        for bot_id in available:
            profile = self.data["profiles"][bot_id]
            score = 0

            # Skill matching
            if required_skills:
                matching_skills = set(required_skills) & set(profile["skills"])
                score += len(matching_skills) * 10

            # Context matching
            if context_keywords:
                context_text = " ".join(profile["context_history"]).lower()
                for keyword in context_keywords:
                    if keyword.lower() in context_text:
                        score += 5

            scored_bots.append((bot_id, score))

        # Sort by score (descending), then by queue position (ascending)
        scored_bots.sort(key=lambda x: (-x[1], available.index(x[0])))

        return scored_bots[0][0] if scored_bots else available[0]

    def update_context(self, bot_id: str, recent_work: str) -> None:
        """
        Update bot's context history.

        Args:
            bot_id: Bot ID
            recent_work: Description of recent work
        """
        if bot_id in self.data["profiles"]:
            self.data["profiles"][bot_id]["context_history"].append(recent_work)
            self.data["profiles"][bot_id]["last_updated"] = datetime.now().isoformat()
            self._save_queue()

    def assign_idle_prep(self, bot_id: str, prep_task: str) -> None:
        """
        Assign preparation task to idle bot.

        Args:
            bot_id: Bot ID
            prep_task: Preparation task (e.g., "Read BOK INDEX")
        """
        if bot_id in self.data["profiles"]:
            self.data["profiles"][bot_id]["idle_prep"] = prep_task
            self.data["profiles"][bot_id]["last_updated"] = datetime.now().isoformat()
            self._save_queue()

    def mark_busy(self, bot_id: str, task: str) -> None:
        """
        Mark bot as busy with a task.

        Args:
            bot_id: Bot ID
            task: Task description
        """
        if bot_id in self.data["profiles"]:
            self.data["profiles"][bot_id]["status"] = "busy"
            self.data["profiles"][bot_id]["current_task"] = task
            self.data["profiles"][bot_id]["idle_prep"] = None  # Clear idle prep
            self.data["profiles"][bot_id]["last_updated"] = datetime.now().isoformat()
            self._save_queue()

    def mark_available(self, bot_id: str) -> None:
        """
        Mark bot as available.

        Args:
            bot_id: Bot ID
        """
        if bot_id in self.data["profiles"]:
            self.data["profiles"][bot_id]["status"] = "available"
            self.data["profiles"][bot_id]["current_task"] = None
            self.data["profiles"][bot_id]["last_updated"] = datetime.now().isoformat()
            self._save_queue()

    def get_bot_profile(self, bot_id: str) -> Optional[Dict]:
        """
        Get bot's profile.

        Args:
            bot_id: Bot ID

        Returns:
            Bot profile dict, or None if not found
        """
        return self.data["profiles"].get(bot_id)

    def list_available_bots(self) -> List[str]:
        """
        List all available bots in queue order.

        Returns:
            List of bot IDs
        """
        available = []
        for bot_id in self.data["queue"]:
            profile = self.data["profiles"].get(bot_id)
            if profile and profile["status"] == "available" and profile["idle_prep"] is None:
                available.append(bot_id)
        return available


def main():
    """CLI interface for bot queue management."""
    import argparse

    parser = argparse.ArgumentParser(description="DEIA Bot Queue Service")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add bot to queue')
    add_parser.add_argument('bot_id', help='Bot ID (e.g., BOT-00002)')
    add_parser.add_argument('--skills', nargs='+', required=True, help='Skills')
    add_parser.add_argument('--context', nargs='*', default=[], help='Context history')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove bot from queue')
    remove_parser.add_argument('bot_id', help='Bot ID')

    # Next command
    next_parser = subparsers.add_parser('next', help='Get next available bot')
    next_parser.add_argument('--skills', nargs='*', help='Required skills')
    next_parser.add_argument('--context', nargs='*', help='Context keywords')

    # Busy command
    busy_parser = subparsers.add_parser('busy', help='Mark bot as busy')
    busy_parser.add_argument('bot_id', help='Bot ID')
    busy_parser.add_argument('task', help='Task description')

    # Available command
    available_parser = subparsers.add_parser('available', help='Mark bot as available')
    available_parser.add_argument('bot_id', help='Bot ID')

    # Context command
    context_parser = subparsers.add_parser('update-context', help='Update bot context')
    context_parser.add_argument('bot_id', help='Bot ID')
    context_parser.add_argument('work', help='Recent work description')

    # Idle prep command
    idle_parser = subparsers.add_parser('idle-prep', help='Assign idle prep task')
    idle_parser.add_argument('bot_id', help='Bot ID')
    idle_parser.add_argument('task', help='Prep task')

    # List command
    subparsers.add_parser('list', help='List available bots')

    # Profile command
    profile_parser = subparsers.add_parser('profile', help='Get bot profile')
    profile_parser.add_argument('bot_id', help='Bot ID')

    args = parser.parse_args()
    queue = BotQueue()

    if args.command == 'add':
        queue.add_bot(args.bot_id, args.skills, args.context)
        print(f"Added {args.bot_id} to queue")
        print(f"Skills: {', '.join(args.skills)}")

    elif args.command == 'remove':
        queue.remove_bot(args.bot_id)
        print(f"Removed {args.bot_id} from queue")

    elif args.command == 'next':
        next_bot = queue.get_next_available(args.skills, args.context)
        if next_bot:
            print(f"Next available bot: {next_bot}")
            profile = queue.get_bot_profile(next_bot)
            print(f"Skills: {', '.join(profile['skills'])}")
        else:
            print("No available bots in queue")

    elif args.command == 'busy':
        queue.mark_busy(args.bot_id, args.task)
        print(f"Marked {args.bot_id} as busy: {args.task}")

    elif args.command == 'available':
        queue.mark_available(args.bot_id)
        print(f"Marked {args.bot_id} as available")

    elif args.command == 'update-context':
        queue.update_context(args.bot_id, args.work)
        print(f"Updated context for {args.bot_id}")

    elif args.command == 'idle-prep':
        queue.assign_idle_prep(args.bot_id, args.task)
        print(f"Assigned idle prep to {args.bot_id}: {args.task}")

    elif args.command == 'list':
        available = queue.list_available_bots()
        if available:
            print(f"Available bots ({len(available)}):\n")
            for bot_id in available:
                profile = queue.get_bot_profile(bot_id)
                print(f"{bot_id}")
                print(f"  Skills: {', '.join(profile['skills'])}")
                print(f"  Status: {profile['status']}")
                print()
        else:
            print("No available bots")

    elif args.command == 'profile':
        profile = queue.get_bot_profile(args.bot_id)
        if profile:
            print(json.dumps(profile, indent=2))
        else:
            print(f"Bot {args.bot_id} not found")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
