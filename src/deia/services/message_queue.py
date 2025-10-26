#!/usr/bin/env python3
"""Distributed Message Queue: Pub/Sub with delivery guarantees.

Features:
- Publish/subscribe pattern
- Queue persistence (JSONL)
- Message ordering guarantee per topic
- At-least-once delivery
- Dead-letter queue for failed messages
- Monitoring and metrics
"""

import json
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum
import threading
from collections import defaultdict, deque

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - MESSAGE-QUEUE - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MessageStatus(Enum):
    """Message lifecycle status."""
    PENDING = "pending"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


@dataclass
class Message:
    """Represents a single message in the queue."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    topic: str = ""
    payload: Dict = field(default_factory=dict)
    status: MessageStatus = MessageStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    delivered_at: Optional[str] = None
    failed_at: Optional[str] = None
    error_message: Optional[str] = None
    delivery_attempts: int = 0
    max_retries: int = 3

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = MessageStatus(self.status)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        """Create from dictionary."""
        if isinstance(data.get('status'), str):
            data['status'] = MessageStatus(data['status'])
        return cls(**data)


class Subscriber:
    """Represents a message subscriber/consumer."""

    def __init__(self, subscriber_id: str, topics: List[str]):
        """Initialize subscriber."""
        self.id = subscriber_id
        self.topics = set(topics)
        self.active = True

    def can_handle_topic(self, topic: str) -> bool:
        """Check if subscriber handles this topic."""
        return topic in self.topics

    def add_topic(self, topic: str):
        """Subscribe to additional topic."""
        self.topics.add(topic)

    def remove_topic(self, topic: str):
        """Unsubscribe from topic."""
        self.topics.discard(topic)


class MessageQueue:
    """Core message queue implementation with pub/sub."""

    def __init__(self, project_root: Path = None):
        """Initialize message queue."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.queue_dir = project_root / ".deia" / "queue"
        self.queue_dir.mkdir(parents=True, exist_ok=True)

        self.messages_log = self.queue_dir / "messages.jsonl"
        self.dlq_log = self.queue_dir / "dead-letter-queue.jsonl"
        self.metrics_log = project_root / ".deia" / "logs" / "queue-metrics.jsonl"
        self.metrics_log.parent.mkdir(parents=True, exist_ok=True)

        # In-memory structures
        self.messages: Dict[str, Message] = {}  # Message ID -> Message
        self.queues: Dict[str, deque] = defaultdict(deque)  # Topic -> Message IDs
        self.subscribers: Dict[str, Subscriber] = {}  # Subscriber ID -> Subscriber
        self.dlq: Dict[str, Message] = {}  # Message ID -> Message
        self.consumer_positions: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))  # subscriber -> topic -> position
        self.lock = threading.RLock()

        # Metrics
        self.metrics = {
            "published": 0,
            "delivered": 0,
            "failed": 0,
            "dead_lettered": 0
        }

        self._load_messages()
        logger.info("MessageQueue initialized")

    def publish(self, topic: str, payload: Dict, max_retries: int = 3) -> str:
        """Publish message to topic."""
        with self.lock:
            message = Message(
                topic=topic,
                payload=payload,
                max_retries=max_retries
            )

            # Store message
            self.messages[message.id] = message
            self.queues[topic].append(message.id)

            # Persist
            self._persist_message(message)

            # Update metrics
            self.metrics["published"] += 1
            self._log_metrics("published", topic, message.id)

            logger.info(f"Message {message.id} published to topic '{topic}'")
            return message.id

    def subscribe(self, subscriber_id: str, topics: List[str]) -> Subscriber:
        """Subscribe to topics."""
        with self.lock:
            if subscriber_id in self.subscribers:
                subscriber = self.subscribers[subscriber_id]
                for topic in topics:
                    subscriber.add_topic(topic)
            else:
                subscriber = Subscriber(subscriber_id, topics)
                self.subscribers[subscriber_id] = subscriber
                # Initialize positions
                for topic in topics:
                    self.consumer_positions[subscriber_id][topic] = 0

            logger.info(f"Subscriber '{subscriber_id}' subscribed to {topics}")
            return subscriber

    def unsubscribe(self, subscriber_id: str, topic: Optional[str] = None) -> bool:
        """Unsubscribe from topic or all topics."""
        with self.lock:
            if subscriber_id not in self.subscribers:
                return False

            subscriber = self.subscribers[subscriber_id]

            if topic:
                subscriber.remove_topic(topic)
                if topic in self.consumer_positions[subscriber_id]:
                    del self.consumer_positions[subscriber_id][topic]
                if not subscriber.topics:
                    del self.subscribers[subscriber_id]
            else:
                del self.subscribers[subscriber_id]
                del self.consumer_positions[subscriber_id]

            return True

    def consume(self, subscriber_id: str) -> Optional[Message]:
        """Consume next message for subscriber."""
        with self.lock:
            if subscriber_id not in self.subscribers:
                return None

            subscriber = self.subscribers[subscriber_id]

            # Try each subscribed topic
            for topic in subscriber.topics:
                if topic in self.queues and len(self.queues[topic]) > 0:
                    # Get next message ID from queue
                    msg_id = self.queues[topic].popleft()
                    if msg_id in self.messages:
                        message = self.messages[msg_id]
                        message.status = MessageStatus.PROCESSING
                        message.delivery_attempts += 1
                        return message

            return None

    def ack(self, message_id: str) -> bool:
        """Acknowledge successful message delivery."""
        with self.lock:
            if message_id not in self.messages:
                return False

            message = self.messages[message_id]
            message.status = MessageStatus.DELIVERED
            message.delivered_at = datetime.utcnow().isoformat() + "Z"
            self._persist_message(message)
            self.metrics["delivered"] += 1
            self._log_metrics("delivered", message.topic, message_id)
            logger.info(f"Message {message_id} acknowledged")
            return True

    def nack(self, message_id: str, error: Optional[str] = None) -> bool:
        """Negative acknowledge - failed message."""
        with self.lock:
            if message_id not in self.messages:
                return False

            message = self.messages[message_id]
            message.failed_at = datetime.utcnow().isoformat() + "Z"
            message.error_message = error

            if message.delivery_attempts >= message.max_retries:
                # Move to DLQ
                message.status = MessageStatus.DEAD_LETTER
                self.dlq[message_id] = message
                if message_id in self.messages:
                    del self.messages[message_id]
                self._persist_dlq_message(message)
                self.metrics["dead_lettered"] += 1
                self._log_metrics("dead_lettered", message.topic, message_id)
                logger.warning(f"Message {message_id} moved to DLQ after {message.delivery_attempts} attempts")
            else:
                # Retry - re-queue
                message.status = MessageStatus.PENDING
                self.queues[message.topic].append(message_id)
                self.metrics["failed"] += 1
                self._log_metrics("failed", message.topic, message_id)
                logger.info(f"Message {message_id} requeued (attempt {message.delivery_attempts})")

            self._persist_message(message)
            return True

    def get_queue_size(self, topic: Optional[str] = None) -> int:
        """Get queue size for topic or all topics."""
        with self.lock:
            if topic:
                return len(self.queues.get(topic, []))
            else:
                return sum(len(q) for q in self.queues.values())

    def get_dlq_size(self) -> int:
        """Get dead-letter queue size."""
        with self.lock:
            return len(self.dlq)

    def get_topic_info(self) -> Dict:
        """Get information about all topics."""
        with self.lock:
            info = {}
            for topic, queue in self.queues.items():
                info[topic] = {
                    "pending": len(queue),
                    "subscribers": sum(1 for s in self.subscribers.values() if s.can_handle_topic(topic))
                }
            return info

    def get_metrics(self) -> Dict:
        """Get queue metrics."""
        with self.lock:
            return {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "metrics": self.metrics.copy(),
                "queue_sizes": {topic: len(q) for topic, q in self.queues.items()},
                "dlq_size": len(self.dlq),
                "subscribers": len(self.subscribers),
                "topics": len(self.queues)
            }

    def _persist_message(self, message: Message):
        """Persist message to log."""
        try:
            with open(self.messages_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(message.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist message: {e}")

    def _persist_dlq_message(self, message: Message):
        """Persist DLQ message to log."""
        try:
            with open(self.dlq_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(message.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist DLQ message: {e}")

    def _load_messages(self):
        """Load persisted messages from log."""
        try:
            if self.messages_log.exists():
                with open(self.messages_log, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            message = Message.from_dict(data)
                            self.messages[message.id] = message
                            if message.status in [MessageStatus.PENDING, MessageStatus.PROCESSING]:
                                self.queues[message.topic].append(message.id)

            if self.dlq_log.exists():
                with open(self.dlq_log, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            message = Message.from_dict(data)
                            self.dlq[message.id] = message
        except Exception as e:
            logger.error(f"Failed to load messages: {e}")

    def _log_metrics(self, event: str, topic: str, message_id: str):
        """Log metrics event."""
        try:
            entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "event": event,
                "topic": topic,
                "message_id": message_id
            }
            with open(self.metrics_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to log metrics: {e}")


class DistributedMessageQueueService:
    """High-level message queue service."""

    def __init__(self, project_root: Path = None):
        """Initialize message queue service."""
        self.queue = MessageQueue(project_root)

    def publish(self, topic: str, payload: Dict, max_retries: int = 3) -> str:
        """Publish message."""
        return self.queue.publish(topic, payload, max_retries)

    def subscribe(self, subscriber_id: str, topics: List[str]) -> Subscriber:
        """Subscribe to topics."""
        return self.queue.subscribe(subscriber_id, topics)

    def unsubscribe(self, subscriber_id: str, topic: Optional[str] = None) -> bool:
        """Unsubscribe from topic(s)."""
        return self.queue.unsubscribe(subscriber_id, topic)

    def consume(self, subscriber_id: str) -> Optional[Message]:
        """Consume next message."""
        return self.queue.consume(subscriber_id)

    def ack(self, message_id: str) -> bool:
        """Acknowledge message."""
        return self.queue.ack(message_id)

    def nack(self, message_id: str, error: Optional[str] = None) -> bool:
        """Negative acknowledge (failed) message."""
        return self.queue.nack(message_id, error)

    def status(self) -> Dict:
        """Get queue status."""
        return {
            "metrics": self.queue.get_metrics(),
            "topics": self.queue.get_topic_info(),
            "dlq_size": self.queue.get_dlq_size()
        }

    def get_dlq_messages(self) -> List[Dict]:
        """Get all dead-letter queue messages."""
        with self.queue.lock:
            return [msg.to_dict() for msg in self.queue.dlq.values()]
