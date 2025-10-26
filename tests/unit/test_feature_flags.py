#!/usr/bin/env python3
"""Tests for Feature Flags & A/B Testing."""

import pytest
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.feature_flags import (
    FeatureFlag,
    Variant,
    ABTest,
    RolloutStrategy,
    FeatureFlagManager,
    FeatureFlagService
)


class TestFeatureFlag:
    """Test feature flag."""

    def test_create_flag(self):
        """Test creating flag."""
        flag = FeatureFlag(name="new_ui", enabled=False)
        assert flag.name == "new_ui"
        assert flag.enabled is False

    def test_flag_with_rollout(self):
        """Test flag with rollout."""
        flag = FeatureFlag(
            name="beta_feature",
            enabled=True,
            strategy=RolloutStrategy.GRADUAL,
            rollout_percentage=50.0
        )
        assert flag.rollout_percentage == 50.0


class TestVariant:
    """Test A/B test variant."""

    def test_create_variant(self):
        """Test creating variant."""
        v = Variant(name="control", weight=0.5)
        assert v.name == "control"
        assert v.weight == 0.5

    def test_variant_invalid_weight(self):
        """Test variant with invalid weight."""
        with pytest.raises(ValueError):
            Variant(name="bad", weight=1.5)


class TestABTest:
    """Test A/B test."""

    def test_create_ab_test(self):
        """Test creating A/B test."""
        variants = [
            Variant(name="control", weight=0.5),
            Variant(name="treatment", weight=0.5)
        ]
        test = ABTest(name="ui_test", feature_name="new_ui", variants=variants)
        assert test.name == "ui_test"
        assert len(test.variants) == 2

    def test_ab_test_invalid_weights(self):
        """Test A/B test with invalid weights."""
        variants = [
            Variant(name="control", weight=0.3),
            Variant(name="treatment", weight=0.3)
        ]
        with pytest.raises(ValueError):
            ABTest(name="test", feature_name="feature", variants=variants)


class TestFeatureFlagManager:
    """Test feature flag manager."""

    @pytest.fixture
    def manager(self):
        """Create manager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = FeatureFlagManager(Path(tmpdir))
            yield manager

    def test_create_flag(self, manager):
        """Test creating flag."""
        flag = manager.create_flag("feature1", enabled=False)
        assert flag.name == "feature1"
        assert "feature1" in manager.flags

    def test_evaluate_disabled_flag(self, manager):
        """Test evaluating disabled flag."""
        manager.create_flag("feature1", enabled=False)
        result = manager.evaluate("feature1", "user-1")
        assert result is False

    def test_evaluate_enabled_flag(self, manager):
        """Test evaluating enabled flag."""
        manager.create_flag("feature1", enabled=True, rollout_percentage=100)
        result = manager.evaluate("feature1", "user-1")
        assert result is True

    def test_evaluate_nonexistent_flag(self, manager):
        """Test evaluating nonexistent flag."""
        result = manager.evaluate("missing", "user-1")
        assert result is False

    def test_target_users(self, manager):
        """Test flag targeting specific users."""
        manager.create_flag("beta", enabled=True, rollout_percentage=100)
        # Update the flag in the manager's dictionary
        manager.flags["beta"].target_users = ["user-1", "user-2"]

        assert manager.evaluate("beta", "user-1") is True
        assert manager.evaluate("beta", "user-3") is False

    def test_rollout_percentage(self, manager):
        """Test gradual rollout."""
        manager.create_flag("feature1", enabled=True, rollout_percentage=0)
        assert manager.evaluate("feature1", "user-1") is False

        manager.set_rollout("feature1", 100)
        assert manager.evaluate("feature1", "user-1") is True

    def test_enable_disable(self, manager):
        """Test enabling/disabling."""
        manager.create_flag("feature1", enabled=False)
        assert manager.evaluate("feature1") is False

        manager.enable_flag("feature1")
        assert manager.evaluate("feature1") is True

        manager.disable_flag("feature1")
        assert manager.evaluate("feature1") is False

    def test_consistent_rollout(self, manager):
        """Test consistent rollout assignment."""
        manager.create_flag("feature1", enabled=True, rollout_percentage=50)

        # Same user should get same result
        result1 = manager.evaluate("feature1", "user-123")
        result2 = manager.evaluate("feature1", "user-123")
        assert result1 == result2

    def test_ab_test_creation(self, manager):
        """Test creating A/B test."""
        variants = [
            Variant(name="control", weight=0.5),
            Variant(name="treatment", weight=0.5, config={"color": "blue"})
        ]
        test = manager.create_ab_test("test1", "feature1", variants)
        assert test.name == "test1"

    def test_ab_test_variant_assignment(self, manager):
        """Test A/B test variant assignment."""
        variants = [
            Variant(name="control", weight=0.5),
            Variant(name="treatment", weight=0.5)
        ]
        test = manager.create_ab_test("test1", "feature1", variants)
        test.enabled = True

        # Same user gets same variant
        v1 = manager.get_variant("test1", "user-1")
        v2 = manager.get_variant("test1", "user-1")
        assert v1.name == v2.name

    def test_variant_distribution(self, manager):
        """Test variant distribution is roughly even."""
        variants = [
            Variant(name="control", weight=0.5),
            Variant(name="treatment", weight=0.5)
        ]
        test = manager.create_ab_test("test1", "feature1", variants)
        test.enabled = True

        control_count = 0
        treatment_count = 0

        for i in range(100):
            user_id = f"user-{i}"
            variant = manager.get_variant("test1", user_id)
            if variant.name == "control":
                control_count += 1
            else:
                treatment_count += 1

        # Should be roughly balanced (40-60 each)
        assert 30 < control_count < 70
        assert 30 < treatment_count < 70

    def test_list_flags(self, manager):
        """Test listing flags."""
        manager.create_flag("feature1")
        manager.create_flag("feature2")

        flags = manager.list_flags()
        assert len(flags) == 2

    def test_get_flag(self, manager):
        """Test getting flag."""
        manager.create_flag("feature1", enabled=True)
        flag = manager.get_flag("feature1")

        assert flag is not None
        assert flag.enabled is True


class TestFeatureFlagService:
    """Test high-level service."""

    @pytest.fixture
    def service(self):
        """Create service."""
        with tempfile.TemporaryDirectory() as tmpdir:
            service = FeatureFlagService(Path(tmpdir))
            yield service

    def test_create_and_check(self, service):
        """Test creating and checking flag."""
        service.create("feature1", enabled=True)
        assert service.is_enabled("feature1") is True

    def test_enable_disable_service(self, service):
        """Test enable/disable via service."""
        service.create("feature1", enabled=False)
        assert service.is_enabled("feature1") is False

        service.enable("feature1")
        assert service.is_enabled("feature1") is True

        service.disable("feature1")
        assert service.is_enabled("feature1") is False

    def test_rollout_via_service(self, service):
        """Test rollout via service."""
        service.create("feature1", enabled=True)
        service.set_rollout("feature1", 0)
        assert service.is_enabled("feature1", "user-1") is False

        service.set_rollout("feature1", 100)
        assert service.is_enabled("feature1", "user-1") is True

    def test_ab_test_via_service(self, service):
        """Test A/B test via service."""
        variants = [
            Variant(name="A", weight=0.5),
            Variant(name="B", weight=0.5)
        ]
        test = service.create_ab_test("test1", "feature1", variants)
        test.enabled = True

        variant = service.get_variant("test1", "user-1")
        assert variant is not None
        assert variant.name in ["A", "B"]

    def test_list_flags_service(self, service):
        """Test listing flags."""
        service.create("feature1")
        service.create("feature2")

        flags = service.list_flags()
        assert len(flags) == 2


class TestRolloutStrategies:
    """Test different rollout strategies."""

    def test_immediate_rollout(self):
        """Test immediate rollout."""
        flag = FeatureFlag(
            name="immediate",
            enabled=True,
            strategy=RolloutStrategy.IMMEDIATE,
            rollout_percentage=100
        )
        assert flag.rollout_percentage == 100

    def test_canary_rollout(self):
        """Test canary rollout."""
        flag = FeatureFlag(
            name="canary",
            enabled=True,
            strategy=RolloutStrategy.CANARY,
            rollout_percentage=5  # Start with 5%
        )
        assert flag.rollout_percentage == 5

    def test_gradual_rollout(self):
        """Test gradual rollout."""
        flag = FeatureFlag(
            name="gradual",
            enabled=True,
            strategy=RolloutStrategy.GRADUAL,
            rollout_percentage=25  # Quarter rollout
        )
        assert flag.rollout_percentage == 25


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
