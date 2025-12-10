"""
Bot Circuit Breaker - Prevents cascading failures by stopping task distribution to failing bots.

Implements circuit breaker pattern:
- CLOSED: Normal operation, tasks flow to bot
- OPEN: Too many failures, tasks rejected to prevent overload
- HALF_OPEN: Testing if bot recovered, limited tasks allowed

Tracks failure rate and recovery indicators.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from pathlib import Path
import json


class CircuitState(Enum):
    """States of circuit breaker."""
    CLOSED = "closed"          # Normal, tasks flowing
    OPEN = "open"              # Failed, rejecting tasks
    HALF_OPEN = "half_open"    # Testing recovery


@dataclass
class FailureMetrics:
    """Tracks failures for a bot."""
    bot_id: str
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[str] = None
    last_success_time: Optional[str] = None
    consecutive_failures: int = 0

    @property
    def failure_rate(self) -> float:
        """Calculate failure rate (0.0 to 1.0)."""
        total = self.failure_count + self.success_count
        if total == 0:
            return 0.0
        return self.failure_count / total

    @property
    def recent_failures(self) -> int:
        """Count failures in last hour."""
        if not self.last_failure_time:
            return 0
        try:
            last_failure = datetime.fromisoformat(self.last_failure_time)
            if datetime.now() - last_failure < timedelta(hours=1):
                return self.failure_count
        except Exception:
            pass
        return 0


class BotCircuitBreaker:
    """
    Circuit breaker for individual bots.

    Monitors failure patterns and switches to OPEN state to prevent
    cascading failures when a bot becomes unhealthy.
    """

    # Configuration thresholds
    FAILURE_RATE_THRESHOLD = 0.5  # 50% failure rate triggers OPEN
    FAILURE_COUNT_THRESHOLD = 5   # 5 consecutive failures triggers OPEN
    RECOVERY_TIMEOUT_SECONDS = 300  # 5 minutes before testing recovery
    HALF_OPEN_SUCCESS_THRESHOLD = 3  # 3 successes to return to CLOSED

    def __init__(
        self,
        bot_id: str,
        failure_rate_threshold: float = FAILURE_RATE_THRESHOLD,
        failure_count_threshold: int = FAILURE_COUNT_THRESHOLD,
        recovery_timeout_seconds: int = RECOVERY_TIMEOUT_SECONDS
    ):
        """
        Initialize circuit breaker for a bot.

        Args:
            bot_id: Bot identifier
            failure_rate_threshold: Open circuit if failure rate exceeds this
            failure_count_threshold: Open circuit if consecutive failures exceed this
            recovery_timeout_seconds: Time to wait before testing recovery
        """
        self.bot_id = bot_id
        self.state = CircuitState.CLOSED
        self.metrics = FailureMetrics(bot_id=bot_id)

        self.failure_rate_threshold = failure_rate_threshold
        self.failure_count_threshold = failure_count_threshold
        self.recovery_timeout = recovery_timeout_seconds

        self.opened_at: Optional[datetime] = None
        self.half_open_successes = 0

    def record_success(self) -> None:
        """Record successful task execution."""
        self.metrics.success_count += 1
        self.metrics.consecutive_failures = 0
        self.metrics.last_success_time = datetime.now().isoformat()

        # If in HALF_OPEN, track recovery
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_successes += 1

            if self.half_open_successes >= self.HALF_OPEN_SUCCESS_THRESHOLD:
                self._close_circuit()

    def record_failure(self) -> None:
        """Record task failure."""
        self.metrics.failure_count += 1
        self.metrics.consecutive_failures += 1
        self.metrics.last_failure_time = datetime.now().isoformat()

        # Check if should open circuit
        if self._should_open_circuit():
            self._open_circuit()

    def can_accept_task(self) -> bool:
        """
        Check if circuit breaker allows task to be sent.

        Returns:
            True if bot is ready to accept task
        """
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self.opened_at:
                elapsed = (datetime.now() - self.opened_at).total_seconds()
                if elapsed >= self.recovery_timeout:
                    self._enter_half_open()
                    return True

            return False

        if self.state == CircuitState.HALF_OPEN:
            # In HALF_OPEN, allow limited tasks
            return True

        return False

    def get_state(self) -> Dict:
        """Get current circuit breaker state."""
        return {
            "bot_id": self.bot_id,
            "state": self.state.value,
            "failure_rate": self.metrics.failure_rate,
            "consecutive_failures": self.metrics.consecutive_failures,
            "total_failures": self.metrics.failure_count,
            "total_successes": self.metrics.success_count,
            "last_failure": self.metrics.last_failure_time,
            "last_success": self.metrics.last_success_time,
            "opened_at": self.opened_at.isoformat() if self.opened_at else None,
            "half_open_successes": self.half_open_successes
        }

    def _should_open_circuit(self) -> bool:
        """Check if circuit should be opened."""
        # Check consecutive failures
        if self.metrics.consecutive_failures >= self.failure_count_threshold:
            return True

        # Check failure rate (only if enough samples)
        if self.metrics.failure_count + self.metrics.success_count >= 10:
            if self.metrics.failure_rate >= self.failure_rate_threshold:
                return True

        return False

    def _open_circuit(self) -> None:
        """Open the circuit, stop accepting tasks."""
        if self.state != CircuitState.OPEN:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()
            print(f"[CIRCUIT-BREAKER] {self.bot_id}: CIRCUIT OPENED")
            print(f"  Failure rate: {self.metrics.failure_rate:.1%}")
            print(f"  Consecutive failures: {self.metrics.consecutive_failures}")

    def _enter_half_open(self) -> None:
        """Enter HALF_OPEN state to test recovery."""
        self.state = CircuitState.HALF_OPEN
        self.half_open_successes = 0
        print(f"[CIRCUIT-BREAKER] {self.bot_id}: HALF_OPEN (testing recovery)")

    def _close_circuit(self) -> None:
        """Close the circuit, resume normal operation."""
        self.state = CircuitState.CLOSED
        self.opened_at = None
        self.half_open_successes = 0
        self.metrics.consecutive_failures = 0
        print(f"[CIRCUIT-BREAKER] {self.bot_id}: CIRCUIT CLOSED (recovered)")


class MultiCircuitBreaker:
    """
    Manages circuit breakers for multiple bots.

    Central management of all bot circuit breakers.
    Provides metrics and visibility into bot health.
    """

    def __init__(self, work_dir: Path):
        """
        Initialize multi-bot circuit breaker.

        Args:
            work_dir: Working directory for logs
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.breakers: Dict[str, BotCircuitBreaker] = {}
        self.event_log_file = self.log_dir / "circuit-breaker-events.jsonl"

    def get_or_create_breaker(self, bot_id: str) -> BotCircuitBreaker:
        """
        Get or create circuit breaker for a bot.

        Args:
            bot_id: Bot identifier

        Returns:
            BotCircuitBreaker instance
        """
        if bot_id not in self.breakers:
            self.breakers[bot_id] = BotCircuitBreaker(bot_id)

        return self.breakers[bot_id]

    def can_send_task(self, bot_id: str) -> bool:
        """
        Check if can send task to bot.

        Args:
            bot_id: Bot identifier

        Returns:
            True if task should be sent
        """
        breaker = self.get_or_create_breaker(bot_id)
        can_send = breaker.can_accept_task()

        if not can_send and breaker.state == CircuitState.OPEN:
            self._log_event("task_rejected", bot_id, {
                "reason": "circuit_open",
                "failure_rate": breaker.metrics.failure_rate
            })

        return can_send

    def record_task_result(self, bot_id: str, success: bool, error: Optional[str] = None) -> None:
        """
        Record task execution result.

        Args:
            bot_id: Bot identifier
            success: Whether task succeeded
            error: Error message if failed
        """
        breaker = self.get_or_create_breaker(bot_id)
        old_state = breaker.state

        if success:
            breaker.record_success()
        else:
            breaker.record_failure()

        # Log state changes
        if old_state != breaker.state:
            self._log_event("state_change", bot_id, {
                "old_state": old_state.value,
                "new_state": breaker.state.value
            })

    def get_bot_health(self, bot_id: str) -> Dict:
        """
        Get health status of a bot.

        Args:
            bot_id: Bot identifier

        Returns:
            Health status dict
        """
        breaker = self.get_or_create_breaker(bot_id)
        return breaker.get_state()

    def get_all_health(self) -> Dict:
        """
        Get health status of all bots.

        Returns:
            Dict mapping bot_id to health status
        """
        return {
            bot_id: breaker.get_state()
            for bot_id, breaker in self.breakers.items()
        }

    def get_healthy_bots(self) -> List[str]:
        """
        Get list of bots in CLOSED state (healthy).

        Returns:
            List of healthy bot IDs
        """
        return [
            bot_id for bot_id, breaker in self.breakers.items()
            if breaker.state == CircuitState.CLOSED
        ]

    def get_unhealthy_bots(self) -> List[str]:
        """
        Get list of bots in OPEN state (unhealthy).

        Returns:
            List of unhealthy bot IDs
        """
        return [
            bot_id for bot_id, breaker in self.breakers.items()
            if breaker.state == CircuitState.OPEN
        ]

    def get_recovering_bots(self) -> List[str]:
        """
        Get list of bots in HALF_OPEN state (recovering).

        Returns:
            List of recovering bot IDs
        """
        return [
            bot_id for bot_id, breaker in self.breakers.items()
            if breaker.state == CircuitState.HALF_OPEN
        ]

    def _log_event(self, event: str, bot_id: str, details: Dict = None) -> None:
        """Log circuit breaker event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "bot_id": bot_id,
            "details": details or {}
        }

        try:
            with open(self.event_log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[CIRCUIT-BREAKER] Failed to log event: {e}")
