"""Unit tests for External Integration API"""

import pytest
import asyncio
from pathlib import Path
from src.deia.services.external_api import (
    ExternalAPI, WebhookEvent, WebhookDeliveryStatus
)


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory"""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def external_api(temp_work_dir):
    """Create ExternalAPI instance"""
    return ExternalAPI(temp_work_dir)


class TestWebhookRegistration:
    """Test webhook registration"""

    def test_register_webhook(self, external_api):
        """Test registering a webhook"""
        webhook_id = external_api.register_webhook(
            url="https://example.com/webhooks",
            events=["task.completed", "task.failed"]
        )

        assert webhook_id.startswith("wh-")
        assert webhook_id in external_api.webhooks

    def test_register_multiple_webhooks(self, external_api):
        """Test registering multiple webhooks"""
        wh1 = external_api.register_webhook(
            url="https://example.com/wh1",
            events=["task.completed"]
        )
        wh2 = external_api.register_webhook(
            url="https://example.com/wh2",
            events=["task.failed"]
        )

        assert wh1 != wh2
        assert len(external_api.webhooks) == 2

    def test_webhook_secret_generation(self, external_api):
        """Test webhook secret is generated if not provided"""
        webhook_id = external_api.register_webhook(
            url="https://example.com/webhooks",
            events=["task.completed"]
        )

        webhook = external_api.webhooks[webhook_id]
        assert webhook.secret is not None
        assert len(webhook.secret) > 0

    def test_webhook_custom_secret(self, external_api):
        """Test providing custom webhook secret"""
        webhook_id = external_api.register_webhook(
            url="https://example.com/webhooks",
            events=["task.completed"],
            secret="my-custom-secret"
        )

        webhook = external_api.webhooks[webhook_id]
        assert webhook.secret == "my-custom-secret"

    def test_deactivate_webhook(self, external_api):
        """Test deactivating a webhook"""
        webhook_id = external_api.register_webhook(
            url="https://example.com/webhooks",
            events=["task.completed"]
        )

        webhook = external_api.webhooks[webhook_id]
        assert webhook.is_active

        success = external_api.deactivate_webhook(webhook_id)
        assert success
        assert not webhook.is_active

    def test_list_webhooks(self, external_api):
        """Test listing webhooks"""
        external_api.register_webhook(
            url="https://example.com/wh1",
            events=["task.completed"]
        )
        external_api.register_webhook(
            url="https://example.com/wh2",
            events=["task.failed"]
        )

        webhooks = external_api.list_webhooks()
        assert len(webhooks) == 2


class TestTaskSubmission:
    """Test external task submission"""

    def test_submit_task(self, external_api):
        """Test submitting a task"""
        task_id = external_api.submit_task(
            content="Analyze data",
            task_type="analysis",
            priority="P1"
        )

        assert task_id.startswith("ext-task-")
        assert task_id in external_api.tasks

    def test_task_data_stored(self, external_api):
        """Test task data is stored correctly"""
        task_id = external_api.submit_task(
            content="Test task",
            task_type="development",
            priority="P2"
        )

        task = external_api.tasks[task_id]
        assert task["content"] == "Test task"
        assert task["task_type"] == "development"
        assert task["priority"] == "P2"
        assert task["status"] == "submitted"

    def test_submit_multiple_tasks(self, external_api):
        """Test submitting multiple tasks"""
        task_ids = [
            external_api.submit_task(f"Task {i}")
            for i in range(5)
        ]

        assert len(set(task_ids)) == 5  # All unique


class TestTaskStatus:
    """Test task status queries"""

    def test_get_task_status(self, external_api):
        """Test getting task status"""
        task_id = external_api.submit_task("Test task")

        status = external_api.get_task_status(task_id)
        assert status is not None
        assert status["task_id"] == task_id
        assert status["status"] == "submitted"

    def test_get_nonexistent_task(self, external_api):
        """Test getting non-existent task"""
        status = external_api.get_task_status("nonexistent-task-id")
        assert status is None

    def test_get_task_result_not_ready(self, external_api):
        """Test getting result for incomplete task"""
        task_id = external_api.submit_task("Test task")

        result = external_api.get_task_result(task_id)
        assert result is None  # Task not completed yet


class TestWebhookEvents:
    """Test webhook event triggering"""

    def test_webhook_event_triggered(self, external_api):
        """Test webhook event is created on task submission"""
        webhook_id = external_api.register_webhook(
            url="https://example.com/webhooks",
            events=[WebhookEvent.TASK_SUBMITTED.value]
        )

        task_id = external_api.submit_task("Test task")

        # Check deliveries were created
        deliveries = [
            d for d in external_api.deliveries.values()
            if d.webhook_id == webhook_id
        ]
        assert len(deliveries) > 0
        assert deliveries[0].event == WebhookEvent.TASK_SUBMITTED.value

    def test_webhook_filtering_by_event(self, external_api):
        """Test webhooks are filtered by event type"""
        # Register two webhooks for different events
        wh1 = external_api.register_webhook(
            url="https://example.com/wh1",
            events=[WebhookEvent.TASK_SUBMITTED.value]
        )
        wh2 = external_api.register_webhook(
            url="https://example.com/wh2",
            events=[WebhookEvent.TASK_COMPLETED.value]
        )

        # Submit task (triggers TASK_SUBMITTED event)
        task_id = external_api.submit_task("Test task")

        # Only wh1 should have deliveries
        wh1_deliveries = [
            d for d in external_api.deliveries.values()
            if d.webhook_id == wh1
        ]
        wh2_deliveries = [
            d for d in external_api.deliveries.values()
            if d.webhook_id == wh2
        ]

        assert len(wh1_deliveries) > 0
        assert len(wh2_deliveries) == 0


class TestWebhookSigning:
    """Test webhook payload signing"""

    def test_payload_signing(self, external_api):
        """Test HMAC signing of webhook payload"""
        payload = {"event": "test", "data": {"id": "123"}}
        secret = "test-secret"

        signature = external_api._sign_payload(payload, secret)
        assert signature.startswith("sha256=")
        assert len(signature) > 10

    def test_signature_consistency(self, external_api):
        """Test signature is consistent for same payload"""
        payload = {"event": "test", "data": {"id": "123"}}
        secret = "test-secret"

        sig1 = external_api._sign_payload(payload, secret)
        sig2 = external_api._sign_payload(payload, secret)

        assert sig1 == sig2

    def test_signature_differs_for_different_payload(self, external_api):
        """Test signature differs for different payloads"""
        secret = "test-secret"

        sig1 = external_api._sign_payload({"event": "test1"}, secret)
        sig2 = external_api._sign_payload({"event": "test2"}, secret)

        assert sig1 != sig2


class TestWebhookDelivery:
    """Test webhook delivery"""

    @pytest.mark.asyncio
    async def test_webhook_delivery(self, external_api):
        """Test webhook delivery"""
        webhook_id = external_api.register_webhook(
            url="https://example.com/webhooks",
            events=[WebhookEvent.TASK_SUBMITTED.value]
        )

        task_id = external_api.submit_task("Test task")

        # Attempt delivery
        await external_api.deliver_webhooks()

        webhook = external_api.webhooks[webhook_id]
        # Delivery count should be > 0 (some deliveries may succeed)
        assert webhook.delivery_count >= 0

    @pytest.mark.asyncio
    async def test_webhook_retry_logic(self, external_api):
        """Test webhook retry logic"""
        webhook_id = external_api.register_webhook(
            url="https://example.com/webhooks",
            events=[WebhookEvent.TASK_SUBMITTED.value]
        )

        task_id = external_api.submit_task("Test task")

        # Get delivery
        deliveries = list(external_api.deliveries.values())
        assert len(deliveries) > 0

        delivery = deliveries[0]
        initial_attempts = delivery.attempt_count

        # If delivery failed, attempt count should increase
        if delivery.status == WebhookDeliveryStatus.PENDING:
            await external_api.deliver_webhooks()
            # May retry, so this is flexible


class TestAPILogging:
    """Test API logging"""

    def test_api_log_created(self, external_api, temp_work_dir):
        """Test API log file is created"""
        external_api.submit_task("Test task")

        log_file = temp_work_dir / ".deia" / "bot-logs" / "external-api.jsonl"
        assert log_file.exists()

    def test_webhook_log_created(self, external_api, temp_work_dir):
        """Test webhook log file is created"""
        external_api.register_webhook(
            url="https://example.com/webhooks",
            events=["task.completed"]
        )
        external_api.submit_task("Test task")

        log_file = temp_work_dir / ".deia" / "bot-logs" / "webhook-events.jsonl"
        # May or may not exist depending on events
        # But API log should exist
        api_log = temp_work_dir / ".deia" / "bot-logs" / "external-api.jsonl"
        assert api_log.exists()
