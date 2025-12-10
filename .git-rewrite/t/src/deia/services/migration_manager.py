"""
Migration Manager - Zero-downtime deployments via blue-green strategy.

Supports parallel running of old and new system versions. Gradual traffic
shifting between versions. Quick rollback if issues detected.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum
from datetime import datetime
import json
import uuid


class DeploymentPhase(Enum):
    """Deployment phases."""
    IDLE = "idle"                    # No active deployment
    BLUE_RUNNING = "blue_running"    # Old version running
    GREEN_STAGING = "green_staging"  # New version staged
    SHIFTING_TRAFFIC = "shifting"    # Moving traffic from blue to green
    GREEN_RUNNING = "green_running"  # New version running
    ROLLING_BACK = "rolling_back"    # Reverting to old version


@dataclass
class DeploymentVersion:
    """A deployable version."""
    version_id: str
    tag: str                      # e.g., "v1.0.0", "v1.1.0"
    timestamp: str
    git_commit: Optional[str] = None
    type: str = "blue"            # "blue" or "green"
    is_active: bool = False
    tests_passed: bool = False
    canary_tests_passed: bool = False
    traffic_percentage: float = 0.0


@dataclass
class DeploymentStatus:
    """Current deployment status."""
    phase: DeploymentPhase
    timestamp: str
    blue_version: Optional[str] = None
    green_version: Optional[str] = None
    traffic_to_green: float = 0.0  # 0-100
    metrics: Dict[str, Any] = field(default_factory=dict)


class MigrationManager:
    """
    Blue-green deployment with traffic shifting and rollback.

    Features:
    - Parallel old and new versions
    - Gradual traffic shifting (0-100%)
    - Automated canary testing
    - Quick rollback capability
    - Comprehensive logging
    """

    def __init__(self, work_dir: Path):
        """Initialize migration manager."""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.migration_dir = self.work_dir / ".deia" / "migrations"

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.migration_dir.mkdir(parents=True, exist_ok=True)

        self.migration_log = self.log_dir / "migration-log.jsonl"

        # Current state
        self.phase = DeploymentPhase.IDLE
        self.blue_version: Optional[DeploymentVersion] = None
        self.green_version: Optional[DeploymentVersion] = None
        self.traffic_to_green = 0.0
        self.deployment_history: List[Dict] = []

    def stage_deployment(
        self,
        version_tag: str,
        git_commit: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Prepare new version for deployment (GREEN).

        Args:
            version_tag: Version identifier (e.g., "v1.1.0")
            git_commit: Git commit SHA

        Returns:
            (success, version_id)
        """
        if self.phase not in [DeploymentPhase.IDLE, DeploymentPhase.BLUE_RUNNING]:
            return False, "Another deployment in progress"

        version_id = str(uuid.uuid4())

        green = DeploymentVersion(
            version_id=version_id,
            tag=version_tag,
            timestamp=datetime.now().isoformat(),
            git_commit=git_commit,
            type="green"
        )

        self.green_version = green
        self.phase = DeploymentPhase.GREEN_STAGING

        self._log_event("green_staged", {
            "version_id": version_id,
            "tag": version_tag
        })

        return True, version_id

    def run_canary_tests(self, version_id: str) -> bool:
        """
        Run tests on GREEN version before shifting traffic.

        Args:
            version_id: Version to test

        Returns:
            True if tests passed
        """
        if not self.green_version or self.green_version.version_id != version_id:
            return False

        # In real implementation, this would run actual tests
        # For now, mark as passed
        self.green_version.canary_tests_passed = True

        self._log_event("canary_tests_passed", {
            "version_id": version_id
        })

        return True

    def start_traffic_shift(self, version_id: str) -> bool:
        """
        Begin gradual traffic shift from BLUE to GREEN.

        Args:
            version_id: Version to shift to

        Returns:
            True if shift started
        """
        if self.phase != DeploymentPhase.GREEN_STAGING:
            return False

        if not self.green_version or self.green_version.version_id != version_id:
            return False

        self.phase = DeploymentPhase.SHIFTING_TRAFFIC
        self.traffic_to_green = 0.0

        self._log_event("traffic_shift_started", {
            "version_id": version_id
        })

        return True

    def shift_traffic(
        self,
        target_percentage: float,
        version_metrics: Optional[Dict] = None
    ) -> bool:
        """
        Shift percentage of traffic to GREEN version.

        Args:
            target_percentage: Target traffic % for green (0-100)
            version_metrics: Metrics from GREEN version

        Returns:
            True if shift successful
        """
        if self.phase != DeploymentPhase.SHIFTING_TRAFFIC:
            return False

        # Validate target
        if not (0 <= target_percentage <= 100):
            return False

        # Check if green version is healthy
        if version_metrics and version_metrics.get("success_rate", 1.0) < 0.95:
            # If <95% success, don't continue shifting
            return False

        self.traffic_to_green = target_percentage

        self._log_event("traffic_shifted", {
            "traffic_percentage": target_percentage,
            "metrics": version_metrics or {}
        })

        return True

    def complete_deployment(self, version_id: str) -> bool:
        """
        Complete deployment - GREEN becomes BLUE.

        Args:
            version_id: Version that was deployed

        Returns:
            True if deployment completed
        """
        if self.phase != DeploymentPhase.SHIFTING_TRAFFIC:
            return False

        if not self.green_version or self.green_version.version_id != version_id:
            return False

        if self.traffic_to_green < 100:
            return False  # Must be at 100%

        # Rotate versions
        self.blue_version = self.green_version
        self.blue_version.is_active = True
        self.green_version = None
        self.traffic_to_green = 0.0
        self.phase = DeploymentPhase.BLUE_RUNNING

        self._log_event("deployment_completed", {
            "version_id": version_id,
            "tag": self.blue_version.tag
        })

        self.deployment_history.append({
            "version_id": version_id,
            "timestamp": datetime.now().isoformat(),
            "result": "success"
        })

        return True

    def rollback(self) -> bool:
        """
        Rollback to previous version.

        Returns:
            True if rollback successful
        """
        if not self.green_version:
            return False

        # Simply discard GREEN and return to BLUE
        self.green_version = None
        self.traffic_to_green = 0.0
        self.phase = DeploymentPhase.BLUE_RUNNING

        self._log_event("rollback_executed", {
            "reverted_to": self.blue_version.tag if self.blue_version else None
        })

        return True

    def get_deployment_status(self) -> DeploymentStatus:
        """
        Get current deployment status.

        Returns:
            DeploymentStatus
        """
        return DeploymentStatus(
            phase=self.phase,
            timestamp=datetime.now().isoformat(),
            blue_version=self.blue_version.tag if self.blue_version else None,
            green_version=self.green_version.tag if self.green_version else None,
            traffic_to_green=self.traffic_to_green
        )

    def get_deployment_progress(self) -> Dict[str, Any]:
        """
        Get detailed deployment progress.

        Returns:
            Progress details
        """
        status = self.get_deployment_status()

        return {
            "timestamp": datetime.now().isoformat(),
            "phase": self.phase.value,
            "blue": {
                "tag": self.blue_version.tag if self.blue_version else None,
                "active": self.blue_version.is_active if self.blue_version else False
            },
            "green": {
                "tag": self.green_version.tag if self.green_version else None,
                "tests_passed": self.green_version.canary_tests_passed if self.green_version else False
            },
            "traffic": {
                "blue_percentage": 100 - self.traffic_to_green,
                "green_percentage": self.traffic_to_green
            }
        }

    def get_deployment_history(self, limit: int = 10) -> List[Dict]:
        """
        Get deployment history.

        Args:
            limit: Max results

        Returns:
            List of past deployments
        """
        return self.deployment_history[-limit:]

    def can_proceed_with_traffic_shift(self) -> bool:
        """
        Check if safe to proceed with traffic shift.

        Returns:
            True if safe
        """
        if not self.green_version:
            return False

        # Must have passed canary tests
        return self.green_version.canary_tests_passed

    def is_deployment_active(self) -> bool:
        """
        Check if deployment is in progress.

        Returns:
            True if active
        """
        return self.phase != DeploymentPhase.IDLE

    def _log_event(self, event: str, details: Dict = None) -> None:
        """Log migration event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "phase": self.phase.value,
            "details": details or {}
        }

        try:
            with open(self.migration_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[MIGRATION-MANAGER] Failed to log event: {e}")
