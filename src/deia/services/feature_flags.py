#!/usr/bin/env python3
"""Feature Flags & A/B Testing: Enable/disable features, gradual rollouts."""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import threading
import hashlib

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - FEATURE-FLAGS - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RolloutStrategy(Enum):
    """Rollout strategies."""
    IMMEDIATE = "immediate"
    CANARY = "canary"
    BLUE_GREEN = "blue_green"
    GRADUAL = "gradual"


@dataclass
class FeatureFlag:
    """Feature flag configuration."""
    name: str
    enabled: bool = False
    strategy: RolloutStrategy = RolloutStrategy.IMMEDIATE
    rollout_percentage: float = 100.0  # 0-100, defaults to 100% if enabled
    target_users: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.strategy, str):
            self.strategy = RolloutStrategy(self.strategy)


@dataclass
class Variant:
    """A/B test variant."""
    name: str
    weight: float = 0.5  # 0-1
    config: Dict = field(default_factory=dict)

    def __post_init__(self):
        if self.weight < 0 or self.weight > 1:
            raise ValueError("Weight must be between 0 and 1")


@dataclass
class ABTest:
    """A/B test configuration."""
    name: str
    feature_name: str
    variants: List[Variant] = field(default_factory=list)
    enabled: bool = False
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def __post_init__(self):
        # Validate weights sum to 1.0
        total_weight = sum(v.weight for v in self.variants)
        if abs(total_weight - 1.0) > 0.001:
            raise ValueError(f"Variant weights must sum to 1.0, got {total_weight}")


class FeatureFlagManager:
    """Feature flag management."""

    def __init__(self, project_root: Path = None):
        """Initialize feature flag manager."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.flags_dir = project_root / ".deia" / "feature-flags"
        self.flags_dir.mkdir(parents=True, exist_ok=True)

        self.flags_log = self.flags_dir / "flags.jsonl"
        self.evaluations_log = project_root / ".deia" / "logs" / "flag-evaluations.jsonl"
        self.evaluations_log.parent.mkdir(parents=True, exist_ok=True)

        self.flags: Dict[str, FeatureFlag] = {}
        self.ab_tests: Dict[str, ABTest] = {}
        self.lock = threading.RLock()

        logger.info("FeatureFlagManager initialized")

    def create_flag(self, name: str, enabled: bool = False,
                   strategy: RolloutStrategy = RolloutStrategy.IMMEDIATE,
                   rollout_percentage: float = 0.0) -> FeatureFlag:
        """Create a feature flag."""
        with self.lock:
            flag = FeatureFlag(
                name=name,
                enabled=enabled,
                strategy=strategy,
                rollout_percentage=rollout_percentage
            )
            self.flags[name] = flag
            self._persist_flag(flag)
            logger.info(f"Flag '{name}' created")
            return flag

    def evaluate(self, flag_name: str, user_id: Optional[str] = None,
                context: Optional[Dict] = None) -> bool:
        """Evaluate feature flag for user."""
        with self.lock:
            if flag_name not in self.flags:
                logger.warning(f"Flag '{flag_name}' not found")
                return False

            flag = self.flags[flag_name]

            # Check if globally disabled
            if not flag.enabled:
                self._log_evaluation(flag_name, user_id, False)
                return False

            # Check user targeting
            if flag.target_users and user_id and user_id not in flag.target_users:
                self._log_evaluation(flag_name, user_id, False)
                return False

            # Check rollout percentage
            if flag.rollout_percentage < 100:
                if user_id:
                    # Consistent hashing for user
                    user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
                    user_percentage = (user_hash % 100) / 100.0
                    if user_percentage > flag.rollout_percentage / 100.0:
                        self._log_evaluation(flag_name, user_id, False)
                        return False

            self._log_evaluation(flag_name, user_id, True)
            return True

    def enable_flag(self, name: str) -> bool:
        """Enable a flag."""
        with self.lock:
            if name not in self.flags:
                return False
            self.flags[name].enabled = True
            self.flags[name].updated_at = datetime.utcnow().isoformat() + "Z"
            self._persist_flag(self.flags[name])
            logger.info(f"Flag '{name}' enabled")
            return True

    def disable_flag(self, name: str) -> bool:
        """Disable a flag."""
        with self.lock:
            if name not in self.flags:
                return False
            self.flags[name].enabled = False
            self.flags[name].updated_at = datetime.utcnow().isoformat() + "Z"
            self._persist_flag(self.flags[name])
            logger.info(f"Flag '{name}' disabled")
            return True

    def set_rollout(self, name: str, percentage: float) -> bool:
        """Set rollout percentage."""
        if percentage < 0 or percentage > 100:
            return False
        with self.lock:
            if name not in self.flags:
                return False
            self.flags[name].rollout_percentage = percentage
            self.flags[name].updated_at = datetime.utcnow().isoformat() + "Z"
            self._persist_flag(self.flags[name])
            logger.info(f"Flag '{name}' rollout set to {percentage}%")
            return True

    def create_ab_test(self, name: str, feature_name: str, variants: List[Variant]) -> ABTest:
        """Create A/B test."""
        with self.lock:
            test = ABTest(name=name, feature_name=feature_name, variants=variants)
            self.ab_tests[name] = test
            logger.info(f"A/B test '{name}' created")
            return test

    def get_variant(self, test_name: str, user_id: str) -> Optional[Variant]:
        """Get variant for user in A/B test."""
        with self.lock:
            if test_name not in self.ab_tests:
                return None

            test = self.ab_tests[test_name]
            if not test.enabled:
                return None

            # Consistent hashing for variant assignment
            user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
            user_value = (user_hash % 100) / 100.0

            cumulative = 0.0
            for variant in test.variants:
                cumulative += variant.weight
                if user_value <= cumulative:
                    logger.debug(f"User {user_id} assigned to variant '{variant.name}' in test '{test_name}'")
                    return variant

            return test.variants[-1]  # Fallback

    def get_flag(self, name: str) -> Optional[FeatureFlag]:
        """Get flag by name."""
        with self.lock:
            return self.flags.get(name)

    def list_flags(self) -> List[FeatureFlag]:
        """List all flags."""
        with self.lock:
            return list(self.flags.values())

    def _persist_flag(self, flag: FeatureFlag):
        """Persist flag to log."""
        try:
            with open(self.flags_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(flag)) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist flag: {e}")

    def _log_evaluation(self, flag_name: str, user_id: Optional[str], result: bool):
        """Log flag evaluation."""
        try:
            entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "flag": flag_name,
                "user_id": user_id,
                "result": result
            }
            with open(self.evaluations_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to log evaluation: {e}")


class FeatureFlagService:
    """High-level feature flag service."""

    def __init__(self, project_root: Path = None):
        """Initialize service."""
        self.manager = FeatureFlagManager(project_root)

    def create(self, name: str, enabled: bool = False) -> FeatureFlag:
        """Create flag."""
        return self.manager.create_flag(name, enabled)

    def is_enabled(self, name: str, user_id: Optional[str] = None) -> bool:
        """Check if flag is enabled."""
        return self.manager.evaluate(name, user_id)

    def enable(self, name: str) -> bool:
        """Enable flag."""
        return self.manager.enable_flag(name)

    def disable(self, name: str) -> bool:
        """Disable flag."""
        return self.manager.disable_flag(name)

    def set_rollout(self, name: str, percentage: float) -> bool:
        """Set rollout percentage."""
        return self.manager.set_rollout(name, percentage)

    def create_ab_test(self, name: str, feature: str, variants: List[Variant]) -> ABTest:
        """Create A/B test."""
        return self.manager.create_ab_test(name, feature, variants)

    def get_variant(self, test_name: str, user_id: str) -> Optional[Variant]:
        """Get variant for user."""
        return self.manager.get_variant(test_name, user_id)

    def list_flags(self) -> List[FeatureFlag]:
        """List all flags."""
        return self.manager.list_flags()
