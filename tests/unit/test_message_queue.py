#!/usr/bin/env python3
"""Tests for Distributed Message Queue."""

import pytest
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.message_queue import (
    Message,
    MessageStatus,
    Subscriber,
    MessageQueue,
    DistributedMessageQueueService
)


class TestMessage:
    """Test message data structure."""

    def test_create_message(self):
        """Test creating a message."""
        m = Message(
            topic="orders",
            payload={"order_id": "123", "amount": 99.99}
        )

        assert m.topic == "orders"
        assert m.payload["order_id"] == "123"
        assert m.status == MessageStatus.PENDING

    def test_message_serialization(self):
        """Test message to_dict and from_dict."""
        m = Message(
            topic="events",
            payload={"data": "test"}
        )

        data = m.to_dict()
        assert data["topic"] == "events"
        assert data["status"] == "pending"

        m2 = Message.from_dict(data)
        assert m2.topic == m.topic
        assert m2.id == m.id


class TestSubscriber:
    """Test subscriber management."""

    def test_create_subscriber(self):
        """Test creating a subscriber."""
        sub = Subscriber("consumer-1", ["orders", "payments"])

        assert sub.id == "consumer-1"
        assert "orders" in sub.topics
        assert "payments" in sub.topics
        assert sub.active is True

    def test_subscriber_topic_management(self):
        """Test adding/removing topics."""
        sub = Subscriber("consumer-1", ["orders"])

        assert sub.can_handle_topic("orders")
        assert not sub.can_handle_topic("payments")

        sub.add_topic("payments")
        assert sub.can_handle_topic("payments")

        sub.remove_topic("orders")
        assert not sub.can_handle_topic("orders")


class TestMessageQueue:
    """Test message queue operations."""

    @pytest.fixture
    def queue(self):
        """Create temporary queue."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            queue = MessageQueue(project_root)
            yield queue, project_root

    def test_publish_message(self, queue):
        """Test publishing a message."""
        mq, _ = queue

        msg_id = mq.publish("orders", {"order_id": "123"})
        assert msg_id is not None
        assert mq.get_queue_size("orders") == 1

    def test_publish_multiple_topics(self, queue):
        """Test publishing to different topics."""
        mq, _ = queue

        mq.publish("orders", {"id": "1"})
        mq.publish("payments", {"id": "2"})
        mq.publish("orders", {"id": "3"})

        assert mq.get_queue_size("orders") == 2
        assert mq.get_queue_size("payments") == 1
        assert mq.get_queue_size() == 3

    def test_subscribe(self, queue):
        """Test subscribing to topics."""
        mq, _ = queue

        sub = mq.subscribe("consumer-1", ["orders", "payments"])
        assert "consumer-1" in mq.subscribers
        assert sub.can_handle_topic("orders")

    def test_unsubscribe_topic(self, queue):
        """Test unsubscribing from a topic."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders", "payments"])
        assert mq.unsubscribe("consumer-1", "orders")
        assert "consumer-1" in mq.subscribers

    def test_unsubscribe_all(self, queue):
        """Test unsubscribing from all topics."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])
        assert mq.unsubscribe("consumer-1")
        assert "consumer-1" not in mq.subscribers

    def test_consume_message(self, queue):
        """Test consuming a message."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])
        mq.publish("orders", {"order_id": "123"})

        message = mq.consume("consumer-1")
        assert message is not None
        assert message.topic == "orders"
        assert message.status == MessageStatus.PROCESSING

    def test_consume_no_messages(self, queue):
        """Test consuming when queue is empty."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])
        message = mq.consume("consumer-1")
        assert message is None

    def test_acknowledge_message(self, queue):
        """Test acknowledging a message."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])
        msg_id = mq.publish("orders", {"id": "1"})
        message = mq.consume("consumer-1")

        assert mq.ack(message.id)
        assert message.status == MessageStatus.DELIVERED

    def test_negative_acknowledge_retry(self, queue):
        """Test negative acknowledge with retry."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])
        msg_id = mq.publish("orders", {"id": "1"}, max_retries=3)
        message = mq.consume("consumer-1")

        # First nack - should retry
        assert mq.nack(message.id, "Processing failed")
        assert message.status == MessageStatus.PENDING
        assert message.delivery_attempts == 1

        # Try consuming again
        message2 = mq.consume("consumer-1")
        assert message2 is not None
        assert message2.id == message.id

    def test_dead_letter_queue(self, queue):
        """Test moving to dead-letter queue."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])
        mq.publish("orders", {"id": "1"}, max_retries=2)

        # First attempt
        msg = mq.consume("consumer-1")
        mq.nack(msg.id, "Error 1")

        # Second attempt
        msg = mq.consume("consumer-1")
        assert msg is not None
        assert msg.delivery_attempts == 2

        # Third nack moves to DLQ
        mq.nack(msg.id, "Error 2")

        assert mq.get_dlq_size() == 1
        assert msg.status == MessageStatus.DEAD_LETTER

    def test_message_ordering_per_topic(self, queue):
        """Test message ordering is maintained per topic."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])

        ids = []
        for i in range(5):
            msg_id = mq.publish("orders", {"seq": i})
            ids.append(msg_id)

        # Consume in order
        for i in range(5):
            msg = mq.consume("consumer-1")
            assert msg.payload["seq"] == i

    def test_multiple_subscribers_same_topic(self, queue):
        """Test multiple subscribers on same topic."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])
        mq.subscribe("consumer-2", ["orders"])
        mq.publish("orders", {"id": "1"})
        mq.publish("orders", {"id": "2"})

        # In a queue-based system, each message is consumed by one subscriber
        msg1_c1 = mq.consume("consumer-1")
        msg1_c2 = mq.consume("consumer-2")

        # They should get different messages (queue pops first in, first out)
        assert msg1_c1.payload["id"] == "1"
        assert msg1_c2.payload["id"] == "2"
        assert mq.get_queue_size("orders") == 0

    def test_get_queue_info(self, queue):
        """Test getting queue information."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])
        mq.subscribe("consumer-2", ["orders"])
        mq.subscribe("consumer-3", ["payments"])

        mq.publish("orders", {"id": "1"})
        mq.publish("payments", {"id": "2"})

        info = mq.get_topic_info()

        assert info["orders"]["pending"] == 1
        assert info["orders"]["subscribers"] == 2
        assert info["payments"]["pending"] == 1
        assert info["payments"]["subscribers"] == 1

    def test_get_metrics(self, queue):
        """Test getting queue metrics."""
        mq, _ = queue

        mq.subscribe("consumer-1", ["orders"])
        mq.publish("orders", {"id": "1"})
        mq.publish("orders", {"id": "2"})

        msg = mq.consume("consumer-1")
        mq.ack(msg.id)

        metrics = mq.get_metrics()
        assert metrics["metrics"]["published"] == 2
        assert metrics["metrics"]["delivered"] == 1
        assert metrics["topics"] == 1

    def test_message_persistence(self, queue):
        """Test message persistence to log."""
        mq, project_root = queue

        mq.publish("orders", {"id": "1"})

        # Check message log exists
        messages_log = project_root / ".deia" / "queue" / "messages.jsonl"
        assert messages_log.exists()

    def test_dlq_persistence(self, queue):
        """Test DLQ persistence to log."""
        mq, project_root = queue

        mq.subscribe("consumer-1", ["orders"])
        mq.publish("orders", {"id": "1"}, max_retries=1)

        msg = mq.consume("consumer-1")
        mq.nack(msg.id, "Error")

        # Check DLQ log exists
        dlq_log = project_root / ".deia" / "queue" / "dead-letter-queue.jsonl"
        assert dlq_log.exists()


class TestDistributedMessageQueueService:
    """Test high-level message queue service."""

    @pytest.fixture
    def service(self):
        """Create message queue service."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            service = DistributedMessageQueueService(project_root)
            yield service

    def test_publish_consume_workflow(self, service):
        """Test basic pub/sub workflow."""
        # Publish
        msg_id = service.publish("orders", {"order_id": "123"})
        assert msg_id is not None

        # Subscribe and consume
        service.subscribe("consumer-1", ["orders"])
        msg = service.consume("consumer-1")
        assert msg is not None
        assert msg.payload["order_id"] == "123"

        # Acknowledge
        assert service.ack(msg.id)

    def test_error_handling_workflow(self, service):
        """Test error handling and DLQ."""
        service.subscribe("consumer-1", ["orders"])
        service.publish("orders", {"id": "1"}, max_retries=2)

        # Consume, fail multiple times
        msg = service.consume("consumer-1")
        service.nack(msg.id, "Error 1")

        msg = service.consume("consumer-1")
        service.nack(msg.id, "Error 2")

        # Should be in DLQ now
        dlq = service.get_dlq_messages()
        assert len(dlq) == 1
        assert dlq[0]["id"] == msg.id

    def test_status_endpoint(self, service):
        """Test getting status."""
        service.subscribe("consumer-1", ["orders"])
        service.publish("orders", {"id": "1"})

        status = service.status()
        assert "metrics" in status
        assert "topics" in status
        assert "dlq_size" in status

    def test_multiple_topic_subscription(self, service):
        """Test subscribing to multiple topics."""
        service.subscribe("consumer-1", ["orders", "payments", "shipping"])
        service.publish("orders", {"id": "1"})
        service.publish("payments", {"id": "2"})
        service.publish("shipping", {"id": "3"})

        # Consume from multiple topics
        msg1 = service.consume("consumer-1")
        msg2 = service.consume("consumer-1")
        msg3 = service.consume("consumer-1")

        topics = {msg1.topic, msg2.topic, msg3.topic}
        assert topics == {"orders", "payments", "shipping"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
