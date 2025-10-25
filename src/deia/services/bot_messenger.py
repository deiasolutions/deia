"""
Bot Messenger - Inter-bot direct messaging system.

Enables bots to communicate directly with priority queuing, delivery tracking,
and retry logic. Supports both synchronous and asynchronous messaging patterns.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
import json
import uuid


class MessagePriority(Enum):
    """Message priority levels."""
    P0 = "P0"  # Critical - urgent
    P1 = "P1"  # High - important
    P2 = "P2"  # Normal - standard
    P3 = "P3"  # Low - can wait


class MessageStatus(Enum):
    """Message delivery status."""
    PENDING = "pending"        # Queued, not yet delivered
    DELIVERED = "delivered"    # Successfully delivered
    READ = "read"              # Recipient read message
    FAILED = "failed"          # Delivery failed
    EXPIRED = "expired"        # TTL exceeded


@dataclass
class Message:
    """Inter-bot message."""
    message_id: str
    from_bot: str
    to_bot: str
    content: str
    priority: MessagePriority = MessagePriority.P2
    status: MessageStatus = MessageStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    delivered_at: Optional[str] = None
    read_at: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    ttl_seconds: int = 3600  # 1 hour default
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            **asdict(self),
            "priority": self.priority.value,
            "status": self.status.value
        }

    def is_expired(self) -> bool:
        """Check if message has expired."""
        if not self.created_at:
            return False
        created = datetime.fromisoformat(self.created_at)
        return (datetime.now() - created).total_seconds() > self.ttl_seconds

    def is_deliverable(self) -> bool:
        """Check if message can be delivered (not expired, hasn't exceeded retries)."""
        return not self.is_expired() and self.retry_count < self.max_retries


@dataclass
class MessageBox:
    """Message inbox for a bot."""
    bot_id: str
    messages: List[Message] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        """Add message to inbox."""
        self.messages.append(message)

    def get_unread(self) -> List[Message]:
        """Get all unread messages."""
        return [m for m in self.messages if m.status == MessageStatus.PENDING]

    def get_by_priority(self, priority: MessagePriority) -> List[Message]:
        """Get messages by priority."""
        return [m for m in self.messages if m.priority == priority]

    def mark_read(self, message_id: str) -> bool:
        """Mark message as read."""
        for msg in self.messages:
            if msg.message_id == message_id:
                msg.status = MessageStatus.READ
                msg.read_at = datetime.now().isoformat()
                return True
        return False

    def remove_expired(self) -> List[str]:
        """Remove expired messages. Returns list of removed message IDs."""
        removed = []
        self.messages = [
            m for m in self.messages
            if not m.is_expired() or m.status in [MessageStatus.READ, MessageStatus.DELIVERED]
        ]
        return removed


class BotMessenger:
    """
    Inter-bot messaging system.

    Features:
    - Direct messaging between bots
    - Priority-based message queuing
    - Delivery tracking and retry logic
    - Message expiration (TTL)
    - Per-bot inboxes
    - JSON logging of all message events
    """

    def __init__(self, work_dir: Path):
        """
        Initialize bot messenger.

        Args:
            work_dir: Working directory for logs and state
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.messaging_log = self.log_dir / "bot-messaging.jsonl"

        # Message store: bot_id -> MessageBox
        self.inboxes: Dict[str, MessageBox] = {}

        # Outgoing message queue (pending delivery)
        self.outgoing_queue: List[Message] = []

        # Message history (all messages ever sent/received)
        self.message_history: Dict[str, Message] = {}

    def send_message(
        self,
        from_bot: str,
        to_bot: str,
        content: str,
        priority: str = "P2",
        ttl_seconds: int = 3600,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Send a message from one bot to another.

        Args:
            from_bot: Sender bot ID
            to_bot: Recipient bot ID
            content: Message content
            priority: Message priority (P0-P3)
            ttl_seconds: Time to live in seconds
            metadata: Optional metadata dict

        Returns:
            Message ID
        """
        try:
            priority_enum = MessagePriority[priority.upper()]
        except (KeyError, AttributeError):
            priority_enum = MessagePriority.P2

        # Create message
        message_id = str(uuid.uuid4())
        message = Message(
            message_id=message_id,
            from_bot=from_bot,
            to_bot=to_bot,
            content=content,
            priority=priority_enum,
            ttl_seconds=ttl_seconds,
            metadata=metadata or {}
        )

        # Add to outgoing queue
        self.outgoing_queue.append(message)

        # Store in history
        self.message_history[message_id] = message

        # Log event
        self._log_event("message_queued", message)

        return message_id

    def get_inbox(self, bot_id: str) -> MessageBox:
        """
        Get inbox for a bot, creating if necessary.

        Args:
            bot_id: Bot identifier

        Returns:
            MessageBox
        """
        if bot_id not in self.inboxes:
            self.inboxes[bot_id] = MessageBox(bot_id=bot_id)
        return self.inboxes[bot_id]

    def retrieve_messages(self, bot_id: str, priority: Optional[str] = None) -> List[Dict]:
        """
        Retrieve messages for a bot.

        Args:
            bot_id: Bot identifier
            priority: Optional priority filter (P0-P3)

        Returns:
            List of message dicts
        """
        inbox = self.get_inbox(bot_id)

        # Clean up expired messages
        inbox.remove_expired()

        # Get messages
        messages = inbox.messages
        if priority:
            try:
                priority_enum = MessagePriority[priority.upper()]
                messages = inbox.get_by_priority(priority_enum)
            except (KeyError, AttributeError):
                pass

        # Mark as delivered
        for msg in messages:
            if msg.status == MessageStatus.PENDING:
                msg.status = MessageStatus.DELIVERED
                msg.delivered_at = datetime.now().isoformat()
                self._log_event("message_delivered", msg)

        return [m.to_dict() for m in messages]

    def mark_as_read(self, bot_id: str, message_id: str) -> bool:
        """
        Mark a message as read.

        Args:
            bot_id: Bot identifier
            message_id: Message ID

        Returns:
            True if marked successfully
        """
        inbox = self.get_inbox(bot_id)
        success = inbox.mark_read(message_id)

        if success and message_id in self.message_history:
            self._log_event("message_read", self.message_history[message_id])

        return success

    def process_outgoing_queue(self) -> Dict[str, Any]:
        """
        Process outgoing message queue, delivering to inboxes.

        Handles retries for failed deliveries.

        Returns:
            Summary of delivery results
        """
        delivered = []
        failed = []
        retried = []

        for message in self.outgoing_queue[:]:
            # Check expiration
            if message.is_expired():
                message.status = MessageStatus.EXPIRED
                self._log_event("message_expired", message)
                self.outgoing_queue.remove(message)
                continue

            # Deliver to recipient inbox
            try:
                recipient_inbox = self.get_inbox(message.to_bot)
                recipient_inbox.add_message(message)
                message.status = MessageStatus.DELIVERED
                message.delivered_at = datetime.now().isoformat()
                delivered.append(message.message_id)

                self._log_event("message_delivered", message)
                self.outgoing_queue.remove(message)

            except Exception as e:
                # Retry logic
                if message.retry_count < message.max_retries:
                    message.retry_count += 1
                    retried.append(message.message_id)
                    self._log_event("message_retry", message, {
                        "attempt": message.retry_count,
                        "error": str(e)
                    })
                else:
                    message.status = MessageStatus.FAILED
                    failed.append(message.message_id)
                    self._log_event("message_failed", message, {"error": str(e)})
                    self.outgoing_queue.remove(message)

        return {
            "delivered": delivered,
            "failed": failed,
            "retried": retried,
            "pending": len(self.outgoing_queue)
        }

    def get_messaging_status(self) -> Dict[str, Any]:
        """
        Get overall messaging system status.

        Returns:
            Status dict
        """
        # Count messages by status
        status_counts = {
            MessageStatus.PENDING.value: 0,
            MessageStatus.DELIVERED.value: 0,
            MessageStatus.READ.value: 0,
            MessageStatus.FAILED.value: 0,
            MessageStatus.EXPIRED.value: 0
        }

        for message in self.message_history.values():
            status_counts[message.status.value] += 1

        # Count by priority
        priority_counts = {p.value: 0 for p in MessagePriority}
        for message in self.message_history.values():
            priority_counts[message.priority.value] += 1

        return {
            "timestamp": datetime.now().isoformat(),
            "total_bots": len(self.inboxes),
            "total_messages": len(self.message_history),
            "pending_delivery": len(self.outgoing_queue),
            "status_breakdown": status_counts,
            "priority_breakdown": priority_counts,
            "bots": {
                bot_id: {
                    "total_messages": len(inbox.messages),
                    "unread": len(inbox.get_unread())
                }
                for bot_id, inbox in self.inboxes.items()
            }
        }

    def get_bot_conversation(self, bot_id_1: str, bot_id_2: str) -> List[Dict]:
        """
        Get all messages between two bots.

        Args:
            bot_id_1: First bot
            bot_id_2: Second bot

        Returns:
            List of messages (both directions, sorted by time)
        """
        conversation = [
            msg.to_dict()
            for msg in self.message_history.values()
            if (msg.from_bot == bot_id_1 and msg.to_bot == bot_id_2) or
               (msg.from_bot == bot_id_2 and msg.to_bot == bot_id_1)
        ]
        # Sort by creation time
        conversation.sort(key=lambda m: m["created_at"])
        return conversation

    def cleanup_expired(self) -> Dict[str, int]:
        """
        Clean up expired messages from all inboxes.

        Returns:
            Count of removed messages per bot
        """
        cleanup_stats = {}

        for bot_id, inbox in self.inboxes.items():
            # Remove all expired messages (regardless of read status)
            initial_count = len(inbox.messages)
            inbox.messages = [m for m in inbox.messages if not m.is_expired()]
            removed_count = initial_count - len(inbox.messages)

            if removed_count > 0:
                cleanup_stats[bot_id] = removed_count

        self._log_event("cleanup_completed", None, {"stats": cleanup_stats})
        return cleanup_stats

    def _log_event(
        self,
        event: str,
        message: Optional[Message] = None,
        details: Optional[Dict] = None
    ) -> None:
        """
        Log messaging event.

        Args:
            event: Event type
            message: Associated message (if any)
            details: Additional details
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "message_id": message.message_id if message else None,
            "from_bot": message.from_bot if message else None,
            "to_bot": message.to_bot if message else None,
            "priority": message.priority.value if message else None,
            "status": message.status.value if message else None,
            "details": details or {}
        }

        try:
            with open(self.messaging_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[BOT-MESSENGER] Failed to log event: {e}")
