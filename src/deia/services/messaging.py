"""
DEIA Messaging System - File-based Task Queue for Multi-Agent Coordination

This module implements the core messaging infrastructure that enables Queen-Bee
delegation across multiple AI agents (Claude Code, Claude.ai, ChatGPT, etc.)

Based on: b2.py design spec (Message Routing Logic)
Author: Claude (CLAUDE-CODE-001)
Sprint: Week 1 - Foundation
Date: 2025-10-17
"""

import os
import re
import time
from datetime import datetime
from pathlib import Path
from queue import PriorityQueue
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import json


# Message type priority (lower number = higher priority)
MESSAGE_PRIORITY = {
    "ESCALATE": 1,
    "ERROR": 2,
    "REVIEW": 2,
    "TASK": 3,
    "QUERY": 3,
    "RESPONSE": 4,
    "HANDOFF": 4,
    "REPORT": 5,
    "APPROVE": 6,
}

# Valid agent identifiers
VALID_AGENTS = {
    "CLAUDE_CODE",
    "CLAUDE_AI",
    "CLAUDE_WEB",
    "CLAUDE_WEB_BEE_1",
    "CLAUDE_WEB_BEE_2",
    "GPT4",
    "GPT5",
    "CHATGPT",
    "DAVE",
    "BOT_001",
    "ALL",  # Broadcast to all agents
    "ANY",  # First available agent
}

# Valid message types
VALID_MESSAGE_TYPES = {
    "TASK",
    "RESPONSE",
    "HANDOFF",
    "REVIEW",
    "APPROVE",
    "QUERY",
    "REPORT",
    "ERROR",
    "ESCALATE",
}


@dataclass
class Message:
    """Represents a message in the system"""

    filename: str
    timestamp: datetime
    from_agent: str
    to_agent: str
    message_type: str
    subject: str
    priority: int
    filepath: str
    thread_id: Optional[str] = None
    parent_id: Optional[str] = None

    def __lt__(self, other):
        """For priority queue sorting"""
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.timestamp < other.timestamp


class FilenameParser:
    """Parse and validate message filenames"""

    # Pattern: YYYY-MM-DD-HHMM-FROM-TO-TYPE-SUBJECT.md
    FILENAME_PATTERN = re.compile(
        r'^(\d{4})-(\d{2})-(\d{2})-(\d{4})-([A-Z_0-9]+)-([A-Z_0-9]+)-([A-Z]+)-(.+)\.md$'
    )

    @classmethod
    def parse(cls, filename: str) -> Optional[Dict]:
        """
        Parse filename into components

        Returns:
            Dict with parsed components or None if invalid
        """
        match = cls.FILENAME_PATTERN.match(filename)
        if not match:
            return None

        year, month, day, time_str, from_agent, to_agent, msg_type, subject = match.groups()

        # Validate date/time
        try:
            timestamp = datetime(
                int(year), int(month), int(day),
                int(time_str[:2]), int(time_str[2:])
            )
        except ValueError:
            return None

        # Validate agents
        if from_agent not in VALID_AGENTS or to_agent not in VALID_AGENTS:
            return None

        # Validate message type
        if msg_type not in VALID_MESSAGE_TYPES:
            return None

        return {
            "filename": filename,
            "timestamp": timestamp,
            "from_agent": from_agent,
            "to_agent": to_agent,
            "message_type": msg_type,
            "subject": subject,
            "priority": MESSAGE_PRIORITY.get(msg_type, 5),
        }

    @classmethod
    def validate(cls, filename: str) -> Tuple[bool, List[str]]:
        """
        Validate filename and return errors

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        if not filename.endswith('.md'):
            errors.append("Filename must end with .md")
            return False, errors

        parsed = cls.parse(filename)
        if parsed is None:
            errors.append("Filename does not match required pattern: YYYY-MM-DD-HHMM-FROM-TO-TYPE-SUBJECT.md")
            return False, errors

        return True, []


class TaskQueue:
    """Priority queue for agent tasks"""

    def __init__(self, agent_id: str, queue_dir: str = None):
        """
        Initialize task queue for an agent

        Args:
            agent_id: Agent identifier (e.g., "CLAUDE_CODE")
            queue_dir: Directory for queue files (default: ~/.deia/hive/queues/{agent_id})
        """
        self.agent_id = agent_id

        if queue_dir is None:
            home = Path.home()
            queue_dir = home / ".deia" / "hive" / "queues" / agent_id

        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(parents=True, exist_ok=True)

        self._queue: PriorityQueue = PriorityQueue()
        self._pending: Dict[str, Message] = {}

    def enqueue(self, message: Message) -> None:
        """Add message to queue"""
        # Write message file to queue directory
        dest = self.queue_dir / message.filename

        if message.filepath and Path(message.filepath).exists():
            # Copy from source location
            import shutil
            shutil.copy2(message.filepath, dest)

        self._queue.put(message)
        self._pending[message.filename] = message

        self._log_event("ENQUEUE", message)

    def dequeue(self) -> Optional[Message]:
        """Get highest priority message from queue"""
        if self._queue.empty():
            return None

        message = self._queue.get()

        if message.filename in self._pending:
            del self._pending[message.filename]

        self._log_event("DEQUEUE", message)
        return message

    def peek(self) -> Optional[Message]:
        """Look at next message without removing"""
        if self._queue.empty():
            return None

        # Get and put back
        message = self._queue.get()
        self._queue.put(message)
        return message

    def size(self) -> int:
        """Get queue size"""
        return self._queue.qsize()

    def list_pending(self) -> List[Message]:
        """Get all pending messages"""
        return list(self._pending.values())

    def _log_event(self, event: str, message: Message) -> None:
        """Log queue event"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "agent_id": self.agent_id,
            "message_file": message.filename,
            "message_type": message.message_type,
            "priority": message.priority,
        }

        # Append to queue log
        log_file = self.queue_dir / "queue.log.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


class MessageRouter:
    """Routes messages between agents based on availability and rules"""

    def __init__(self, inbox_dir: str = None, status_tracker=None):
        """
        Initialize message router

        Args:
            inbox_dir: Directory to watch for incoming messages
            status_tracker: AgentStatusTracker instance (optional, for availability checks)
        """
        if inbox_dir is None:
            home = Path.home()
            inbox_dir = home / "Downloads" / "uploads"

        self.inbox_dir = Path(inbox_dir)
        self.inbox_dir.mkdir(parents=True, exist_ok=True)

        self.status_tracker = status_tracker
        self._queues: Dict[str, TaskQueue] = {}
        self._seen_files: set = set()

    def get_queue(self, agent_id: str) -> TaskQueue:
        """Get or create queue for agent"""
        if agent_id not in self._queues:
            self._queues[agent_id] = TaskQueue(agent_id)
        return self._queues[agent_id]

    def route_message(self, filename: str, filepath: str) -> bool:
        """
        Route a message to appropriate agent queue

        Returns:
            True if routed successfully, False otherwise
        """
        # Parse filename
        parsed = FilenameParser.parse(filename)
        if not parsed:
            self._log_error("INVALID_FILENAME", filename)
            return False

        # Create message object
        message = Message(filepath=filepath, **parsed)

        target = message.to_agent

        # Handle broadcast
        if target == "ALL":
            return self._broadcast_message(message)

        # Handle any-available routing
        elif target == "ANY":
            return self._route_to_available(message)

        # Direct routing
        else:
            return self._route_to_agent(message, target)

    def _broadcast_message(self, message: Message) -> bool:
        """Broadcast message to all agents"""
        success = True
        for agent_id in VALID_AGENTS:
            if agent_id not in ["ALL", "ANY"]:
                queue = self.get_queue(agent_id)
                try:
                    queue.enqueue(message)
                except Exception as e:
                    self._log_error("BROADCAST_FAILED", message.filename, str(e))
                    success = False
        return success

    def _route_to_available(self, message: Message) -> bool:
        """Route to first available agent"""
        if self.status_tracker:
            available = self.status_tracker.get_available_agents()
            if available:
                target = available[0]
                return self._route_to_agent(message, target)

        # Fallback: queue for manual assignment
        queue = self.get_queue("PENDING_ANY")
        queue.enqueue(message)
        self._log_event("QUEUED_FOR_ASSIGNMENT", message.filename)
        return True

    def _route_to_agent(self, message: Message, agent_id: str) -> bool:
        """Route to specific agent"""
        queue = self.get_queue(agent_id)
        try:
            queue.enqueue(message)
            self._log_event("ROUTED", message.filename, agent_id)
            return True
        except Exception as e:
            self._log_error("ROUTING_FAILED", message.filename, str(e))
            return False

    def process_inbox(self) -> int:
        """
        Process all new files in inbox directory

        Returns:
            Number of messages processed
        """
        processed = 0

        for filepath in self.inbox_dir.glob("*.md"):
            filename = filepath.name

            if filename in self._seen_files:
                continue

            self._seen_files.add(filename)

            if self.route_message(filename, str(filepath)):
                processed += 1

        return processed

    def watch_inbox(self, interval: int = 2, callback=None):
        """
        Watch inbox directory for new messages (blocking)

        Args:
            interval: Check interval in seconds
            callback: Optional callback function(message) for each new message
        """
        print(f"[MessageRouter] Watching {self.inbox_dir} every {interval}s...")

        while True:
            count = self.process_inbox()
            if count > 0:
                print(f"[MessageRouter] Processed {count} new messages")

                if callback:
                    for agent_id, queue in self._queues.items():
                        while queue.size() > 0:
                            message = queue.dequeue()
                            callback(message)

            time.sleep(interval)

    def _log_event(self, event: str, filename: str, details: str = ""):
        """Log routing event"""
        print(f"[MessageRouter] {event}: {filename} {details}")

    def _log_error(self, error: str, filename: str, details: str = ""):
        """Log routing error"""
        print(f"[MessageRouter] ERROR {error}: {filename} {details}")


# Convenience functions

def create_task_file(
    from_agent: str,
    to_agent: str,
    task_type: str,
    subject: str,
    content: str,
    output_dir: str = None
) -> str:
    """
    Create a properly formatted task file

    Returns:
        Path to created file
    """
    if output_dir is None:
        output_dir = Path.home() / "Downloads" / "uploads"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    now = datetime.now()
    filename = (
        f"{now.strftime('%Y-%m-%d-%H%M')}-"
        f"{from_agent}-{to_agent}-{task_type}-{subject}.md"
    )

    filepath = output_dir / filename

    with open(filepath, 'w') as f:
        f.write(content)

    return str(filepath)


def get_agent_queue_status(agent_id: str) -> Dict:
    """Get status of agent's queue"""
    queue = TaskQueue(agent_id)

    # Scan queue directory
    pending_files = list(queue.queue_dir.glob("*.md"))

    return {
        "agent_id": agent_id,
        "queue_size": len(pending_files),
        "queue_dir": str(queue.queue_dir),
        "pending_files": [f.name for f in pending_files],
    }
