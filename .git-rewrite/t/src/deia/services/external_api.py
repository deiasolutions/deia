"""
External Integration API for DEIA

Provides REST API for external systems to:
- Submit tasks to the DEIA system
- Query task status and results
- Register webhooks for event notifications
- Receive webhook deliveries with retry logic
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import json
import uuid
import hashlib
import hmac
import asyncio
from enum import Enum


class WebhookEvent(str, Enum):
    """Webhook event types"""
    TASK_SUBMITTED = "task.submitted"
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    SYSTEM_ERROR = "system.error"


class WebhookDeliveryStatus(str, Enum):
    """Webhook delivery status"""
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass
class WebhookRegistration:
    """Webhook registration"""
    webhook_id: str
    url: str
    events: List[str]
    secret: str
    created_at: datetime
    is_active: bool = True
    delivery_count: int = 0
    failure_count: int = 0
    last_delivery: Optional[datetime] = None


@dataclass
class WebhookDelivery:
    """Webhook delivery attempt"""
    delivery_id: str
    webhook_id: str
    event: str
    payload: Dict[str, Any]
    status: WebhookDeliveryStatus
    attempt_count: int = 1
    next_retry: Optional[datetime] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def should_retry(self) -> bool:
        """Check if delivery should be retried"""
        if self.status == WebhookDeliveryStatus.DELIVERED:
            return False
        if self.attempt_count >= 5:  # Max 5 attempts
            return False
        if self.next_retry and datetime.now() < self.next_retry:
            return False
        return True

    def calculate_next_retry(self):
        """Calculate exponential backoff for next retry"""
        delay_seconds = 60 * (2 ** (self.attempt_count - 1))  # 1min, 2min, 4min, 8min, 16min
        self.next_retry = datetime.now() + timedelta(seconds=delay_seconds)


class ExternalAPI:
    """
    External Integration API for task submission and webhooks.

    Features:
    - Task submission from external systems
    - Task status and result queries
    - Webhook registration and delivery
    - Retry logic with exponential backoff
    - HMAC-based webhook signing
    """

    def __init__(self, work_dir: Path):
        """Initialize external API"""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.api_log = self.log_dir / "external-api.jsonl"
        self.webhook_log = self.log_dir / "webhook-events.jsonl"

        # Storage
        self.webhooks: Dict[str, WebhookRegistration] = {}
        self.deliveries: Dict[str, WebhookDelivery] = {}
        self.tasks: Dict[str, Dict[str, Any]] = {}

    def register_webhook(
        self,
        url: str,
        events: List[str],
        secret: str = None,
    ) -> str:
        """
        Register a webhook for event notifications.

        Args:
            url: Webhook URL to deliver events to
            events: List of event types to subscribe to
            secret: Optional secret for HMAC signing

        Returns:
            Webhook ID for future reference
        """
        webhook_id = f"wh-{str(uuid.uuid4())[:8]}"

        if secret is None:
            secret = str(uuid.uuid4())

        webhook = WebhookRegistration(
            webhook_id=webhook_id,
            url=url,
            events=events,
            secret=secret,
            created_at=datetime.now(),
        )

        self.webhooks[webhook_id] = webhook

        self._log_api("webhook_registered", {
            "webhook_id": webhook_id,
            "url": url,
            "events": events,
        })

        return webhook_id

    def submit_task(
        self,
        content: str,
        task_type: str = "general",
        priority: str = "P2",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Submit a task from external system.

        Args:
            content: Task description
            task_type: Type of task
            priority: Task priority (P0-P3)
            metadata: Optional metadata

        Returns:
            Task ID for future reference
        """
        task_id = f"ext-task-{str(uuid.uuid4())[:8]}"

        task_data = {
            "task_id": task_id,
            "content": content,
            "task_type": task_type,
            "priority": priority,
            "status": "submitted",
            "submitted_at": datetime.now().isoformat(),
            "metadata": metadata or {},
        }

        self.tasks[task_id] = task_data

        self._log_api("task_submitted", {
            "task_id": task_id,
            "task_type": task_type,
            "priority": priority,
        })

        # Trigger webhook event
        self._trigger_webhook_event(
            WebhookEvent.TASK_SUBMITTED,
            {"task_id": task_id, "task_type": task_type}
        )

        return task_id

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status and result"""
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        self._log_api("task_status_queried", {"task_id": task_id})
        return task

    def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task result (only if completed)"""
        task = self.get_task_status(task_id)
        if not task:
            return None

        if task["status"] not in ["completed", "failed"]:
            return None

        return {
            "task_id": task_id,
            "status": task["status"],
            "result": task.get("result"),
            "error": task.get("error"),
        }

    async def deliver_webhooks(self):
        """
        Deliver pending webhooks with retry logic.
        Should be called periodically (e.g., every 30 seconds).
        """
        pending_deliveries = [
            d for d in self.deliveries.values()
            if d.should_retry()
        ]

        for delivery in pending_deliveries:
            await self._deliver_webhook(delivery)

    async def _deliver_webhook(self, delivery: WebhookDelivery):
        """Attempt to deliver a single webhook"""
        webhook = self.webhooks.get(delivery.webhook_id)
        if not webhook or not webhook.is_active:
            delivery.status = WebhookDeliveryStatus.EXPIRED
            return

        try:
            # Sign payload with HMAC
            signature = self._sign_payload(delivery.payload, webhook.secret)

            # In real implementation, would make HTTP request
            # For now, simulate success
            success = await self._simulate_http_post(webhook.url, delivery.payload, signature)

            if success:
                delivery.status = WebhookDeliveryStatus.DELIVERED
                webhook.delivery_count += 1
                webhook.last_delivery = datetime.now()

                self._log_webhook("delivery_success", {
                    "delivery_id": delivery.delivery_id,
                    "webhook_id": delivery.webhook_id,
                    "attempts": delivery.attempt_count,
                })
            else:
                delivery.attempt_count += 1
                delivery.calculate_next_retry()
                delivery.status = WebhookDeliveryStatus.PENDING
                webhook.failure_count += 1

                self._log_webhook("delivery_failed", {
                    "delivery_id": delivery.delivery_id,
                    "webhook_id": delivery.webhook_id,
                    "attempt": delivery.attempt_count,
                    "next_retry": delivery.next_retry.isoformat() if delivery.next_retry else None,
                })

        except Exception as e:
            delivery.attempt_count += 1
            delivery.error = str(e)
            delivery.calculate_next_retry()
            delivery.status = WebhookDeliveryStatus.PENDING

            self._log_webhook("delivery_error", {
                "delivery_id": delivery.delivery_id,
                "webhook_id": delivery.webhook_id,
                "error": str(e),
            })

    def deactivate_webhook(self, webhook_id: str) -> bool:
        """Deactivate a webhook"""
        if webhook_id not in self.webhooks:
            return False

        webhook = self.webhooks[webhook_id]
        webhook.is_active = False

        self._log_api("webhook_deactivated", {"webhook_id": webhook_id})
        return True

    def list_webhooks(self) -> List[Dict[str, Any]]:
        """List all active webhooks"""
        return [
            {
                "webhook_id": w.webhook_id,
                "url": w.url,
                "events": w.events,
                "active": w.is_active,
                "deliveries": w.delivery_count,
                "failures": w.failure_count,
                "last_delivery": w.last_delivery.isoformat() if w.last_delivery else None,
            }
            for w in self.webhooks.values()
            if w.is_active
        ]

    def _trigger_webhook_event(self, event: WebhookEvent, data: Dict[str, Any]):
        """Trigger a webhook event for matching subscriptions"""
        payload = {
            "event": event.value,
            "timestamp": datetime.now().isoformat(),
            "data": data,
        }

        for webhook in self.webhooks.values():
            if not webhook.is_active:
                continue
            if event.value not in webhook.events:
                continue

            delivery = WebhookDelivery(
                delivery_id=f"del-{str(uuid.uuid4())[:8]}",
                webhook_id=webhook.webhook_id,
                event=event.value,
                payload=payload,
                status=WebhookDeliveryStatus.PENDING,
            )

            self.deliveries[delivery.delivery_id] = delivery

    def _sign_payload(self, payload: Dict[str, Any], secret: str) -> str:
        """Create HMAC signature for webhook payload"""
        json_str = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            secret.encode(),
            json_str.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"

    async def _simulate_http_post(
        self,
        url: str,
        payload: Dict[str, Any],
        signature: str
    ) -> bool:
        """Simulate HTTP POST to webhook (in production would use httpx/requests)"""
        # For testing, randomly succeed/fail
        import random
        await asyncio.sleep(0.01)  # Simulate network latency
        return random.random() < 0.8  # 80% success rate in simulation

    def _log_api(self, event: str, details: Dict):
        """Log API event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details,
        }
        try:
            with open(self.api_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    def _log_webhook(self, event: str, details: Dict):
        """Log webhook event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details,
        }
        try:
            with open(self.webhook_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
