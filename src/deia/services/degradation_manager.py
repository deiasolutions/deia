"""
Graceful Degradation Manager - System resilience under partial failures.

When system components fail, degrades gracefully instead of stopping completely.
Maintains core functionality while disabling less critical features.
Transparent to API clients - system responds even when degraded.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum
from datetime import datetime
import json


class DegradationMode(Enum):
    """System operation modes."""
    FULL = "full"              # All features enabled
    DEGRADED = "degraded"      # Core features only, some disabled
    MAINTENANCE = "maintenance"  # System under maintenance


class DegradationCause(Enum):
    """Why system is degraded."""
    BOT_FAILURE = "bot_failure"
    STORAGE_FULL = "storage_full"
    MEMORY_PRESSURE = "memory_pressure"
    HIGH_LOAD = "high_load"
    MANUAL = "manual"
    DEPENDENCY_FAILURE = "dependency_failure"
    NONE = "none"


@dataclass
class DegradationState:
    """Current degradation state."""
    mode: DegradationMode
    cause: DegradationCause
    timestamp: str
    disabled_features: List[str] = field(default_factory=list)
    active_bots: int = 0
    total_bots: int = 0
    queue_capacity_percent: float = 100.0
    estimated_recovery_time_seconds: Optional[int] = None
    message: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            **asdict(self),
            "mode": self.mode.value,
            "cause": self.cause.value
        }


@dataclass
class FeatureStatus:
    """Status of a feature."""
    name: str
    enabled: bool
    reason: str = ""
    criticality: str = "normal"  # critical, important, normal, optional


class DegradationManager:
    """
    Graceful degradation - Keep system running when parts fail.

    Features:
    - 3 operation modes: FULL, DEGRADED, MAINTENANCE
    - Automatic feature disabling when resources constrained
    - Fallback routing to healthy bots
    - Transparent degradation to API clients
    - Recovery detection and re-enablement
    - Comprehensive logging
    """

    # Features that can be disabled
    CRITICAL_FEATURES = [
        "task_orchestration",    # Core task routing
        "message_delivery",      # Bot communication
        "health_monitoring"      # System health tracking
    ]

    IMPORTANT_FEATURES = [
        "adaptive_scheduling",   # ML-based routing
        "auto_scaling"          # Dynamic scaling
    ]

    OPTIONAL_FEATURES = [
        "analytics",            # Advanced analytics
        "predictive_scaling"    # Predictive features
    ]

    def __init__(self, work_dir: Path):
        """Initialize degradation manager."""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.degradation_log = self.log_dir / "degradation-events.jsonl"

        # Current state
        self.mode = DegradationMode.FULL
        self.cause = DegradationCause.NONE
        self.disabled_features: List[str] = []
        self.active_bots = 0
        self.total_bots = 0
        self.queue_capacity_percent = 100.0
        self.last_state_change: Optional[datetime] = None

    def transition_to_degraded(
        self,
        cause: DegradationCause,
        active_bots: int = 0,
        total_bots: int = 0,
        queue_capacity_percent: float = 100.0,
        message: str = ""
    ) -> bool:
        """
        Transition to DEGRADED mode.

        Args:
            cause: Reason for degradation
            active_bots: Number of active bots
            total_bots: Total bots available
            queue_capacity_percent: Queue usage %
            message: Human-readable message

        Returns:
            True if transition successful
        """
        if self.mode == DegradationMode.DEGRADED:
            return False  # Already degraded

        # Determine which features to disable based on cause
        disabled = self._select_features_to_disable(cause)

        self.mode = DegradationMode.DEGRADED
        self.cause = cause
        self.disabled_features = disabled
        self.active_bots = active_bots
        self.total_bots = total_bots
        self.queue_capacity_percent = queue_capacity_percent
        self.last_state_change = datetime.now()

        self._log_event("degraded_mode_entered", {
            "cause": cause.value,
            "disabled_features": disabled,
            "message": message
        })

        return True

    def transition_to_maintenance(self, message: str = "") -> bool:
        """
        Transition to MAINTENANCE mode (all non-critical features disabled).

        Args:
            message: Reason for maintenance
            message: Reason for maintenance

        Returns:
            True if transition successful
        """
        self.mode = DegradationMode.MAINTENANCE
        self.cause = DegradationCause.MANUAL
        self.disabled_features = self.IMPORTANT_FEATURES + self.OPTIONAL_FEATURES
        self.last_state_change = datetime.now()

        self._log_event("maintenance_mode_entered", {
            "message": message
        })

        return True

    def transition_to_full(self) -> bool:
        """
        Transition back to FULL mode (all features enabled).

        Returns:
            True if transition successful
        """
        if self.mode == DegradationMode.FULL:
            return False  # Already full

        self.mode = DegradationMode.FULL
        self.cause = DegradationCause.NONE
        self.disabled_features = []
        self.last_state_change = datetime.now()

        self._log_event("full_mode_restored", {})

        return True

    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if a feature is enabled.

        Args:
            feature_name: Feature to check

        Returns:
            True if feature is enabled
        """
        if self.mode == DegradationMode.FULL:
            return True

        return feature_name not in self.disabled_features

    def get_feature_status(self) -> Dict[str, FeatureStatus]:
        """
        Get status of all features.

        Returns:
            Dict mapping feature names to status
        """
        status = {}

        for feature in self.CRITICAL_FEATURES:
            status[feature] = FeatureStatus(
                name=feature,
                enabled=self.is_feature_enabled(feature),
                criticality="critical"
            )

        for feature in self.IMPORTANT_FEATURES:
            status[feature] = FeatureStatus(
                name=feature,
                enabled=self.is_feature_enabled(feature),
                criticality="important"
            )

        for feature in self.OPTIONAL_FEATURES:
            status[feature] = FeatureStatus(
                name=feature,
                enabled=self.is_feature_enabled(feature),
                criticality="optional"
            )

        return status

    def get_fallback_bot(
        self,
        available_bots: List[str],
        bot_health: Dict[str, Dict]
    ) -> Optional[str]:
        """
        Get healthiest bot to route task to (fallback logic).

        Args:
            available_bots: List of available bot IDs
            bot_health: Dict mapping bot ID to health metrics

        Returns:
            Best bot ID or None
        """
        if not available_bots:
            return None

        # Sort by success rate
        def bot_score(bot_id: str) -> float:
            health = bot_health.get(bot_id, {})
            success_rate = health.get("success_rate", 0.0)
            cpu_percent = health.get("cpu_percent", 1.0)
            # Score = success rate - cpu penalty
            return success_rate - (cpu_percent * 0.1)

        best_bot = max(available_bots, key=bot_score)
        return best_bot

    def should_enable_scaling(self) -> bool:
        """
        Should auto-scaling be enabled?

        In degraded mode, scaling is disabled to reduce complexity.

        Returns:
            True if scaling should be enabled
        """
        return self.mode == DegradationMode.FULL

    def should_enable_analytics(self) -> bool:
        """
        Should analytics be enabled?

        In degraded/maintenance, analytics disabled to save resources.

        Returns:
            True if analytics should be enabled
        """
        return self.mode == DegradationMode.FULL

    def get_state(self) -> DegradationState:
        """
        Get current degradation state.

        Returns:
            DegradationState
        """
        return DegradationState(
            mode=self.mode,
            cause=self.cause,
            timestamp=datetime.now().isoformat(),
            disabled_features=self.disabled_features.copy(),
            active_bots=self.active_bots,
            total_bots=self.total_bots,
            queue_capacity_percent=self.queue_capacity_percent
        )

    def get_status(self) -> Dict[str, Any]:
        """
        Get detailed degradation status.

        Returns:
            Status dictionary
        """
        feature_status = self.get_feature_status()
        state = self.get_state()

        return {
            "timestamp": datetime.now().isoformat(),
            "mode": self.mode.value,
            "cause": self.cause.value,
            "disabled_features": self.disabled_features,
            "feature_status": {
                name: {
                    "enabled": fs.enabled,
                    "criticality": fs.criticality
                }
                for name, fs in feature_status.items()
            },
            "bot_status": {
                "active": self.active_bots,
                "total": self.total_bots,
                "percentage": (self.active_bots / self.total_bots * 100) if self.total_bots > 0 else 0
            },
            "queue_capacity_percent": self.queue_capacity_percent,
            "time_in_mode": self._get_time_in_mode_seconds()
        }

    def apply_resource_constraints(
        self,
        memory_usage_percent: float,
        cpu_usage_percent: float,
        active_bots_count: int,
        total_bots_count: int
    ) -> Optional[DegradationCause]:
        """
        Check resource usage and degrade if needed.

        Call periodically to auto-degrade on resource pressure.

        Args:
            memory_usage_percent: System memory %
            cpu_usage_percent: System CPU %
            active_bots_count: Active bots
            total_bots_count: Total bots

        Returns:
            DegradationCause if degradation triggered, None otherwise
        """
        self.active_bots = active_bots_count
        self.total_bots = total_bots_count

        # Check for resource pressure
        if memory_usage_percent > 85:
            if self.mode != DegradationMode.DEGRADED:
                self.transition_to_degraded(
                    DegradationCause.MEMORY_PRESSURE,
                    active_bots_count,
                    total_bots_count,
                    message=f"Memory usage: {memory_usage_percent:.1f}%"
                )
                return DegradationCause.MEMORY_PRESSURE

        if cpu_usage_percent > 90:
            if self.mode != DegradationMode.DEGRADED:
                self.transition_to_degraded(
                    DegradationCause.HIGH_LOAD,
                    active_bots_count,
                    total_bots_count,
                    message=f"CPU usage: {cpu_usage_percent:.1f}%"
                )
                return DegradationCause.HIGH_LOAD

        # Check for bot failures
        if total_bots_count > 0:
            healthy_percentage = (active_bots_count / total_bots_count) * 100
            if healthy_percentage < 50:
                if self.mode != DegradationMode.DEGRADED:
                    self.transition_to_degraded(
                        DegradationCause.BOT_FAILURE,
                        active_bots_count,
                        total_bots_count,
                        message=f"Only {healthy_percentage:.0f}% of bots healthy"
                    )
                    return DegradationCause.BOT_FAILURE

        # Check if we should recover
        if self.mode == DegradationMode.DEGRADED:
            if (memory_usage_percent < 70 and cpu_usage_percent < 70 and
                healthy_percentage > 80):
                self.transition_to_full()

        return None

    def _select_features_to_disable(self, cause: DegradationCause) -> List[str]:
        """
        Select which features to disable based on cause.

        Args:
            cause: Degradation cause

        Returns:
            List of features to disable
        """
        if cause == DegradationCause.MEMORY_PRESSURE:
            # Disable non-critical features
            return self.IMPORTANT_FEATURES + self.OPTIONAL_FEATURES

        elif cause == DegradationCause.HIGH_LOAD:
            # Disable load-intensive features
            return ["adaptive_scheduling"] + self.OPTIONAL_FEATURES

        elif cause == DegradationCause.BOT_FAILURE:
            # Disable features that require all bots
            return ["auto_scaling"] + self.OPTIONAL_FEATURES

        else:
            # Default: disable optional features
            return self.OPTIONAL_FEATURES

    def _get_time_in_mode_seconds(self) -> int:
        """Get seconds spent in current mode."""
        if not self.last_state_change:
            return 0

        elapsed = datetime.now() - self.last_state_change
        return int(elapsed.total_seconds())

    def _log_event(self, event: str, details: Dict = None) -> None:
        """Log degradation event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "mode": self.mode.value,
            "details": details or {}
        }

        try:
            with open(self.degradation_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[DEGRADATION-MANAGER] Failed to log event: {e}")
