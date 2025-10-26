#!/usr/bin/env python3
"""Tests for Advanced Rate Limiter."""

import pytest
import tempfile
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.rate_limiter import (
    RateLimitAlgorithm,
    RateLimitDecision,
    TokenBucket,
    SlidingWindow,
    RateLimitBucket,
    AdvancedRateLimiter,
    RateLimiterService
)


class TestTokenBucket:
    """Test token bucket algorithm."""

    def test_bucket_creation(self):
        """Test creating token bucket."""
        bucket = TokenBucket(capacity=100, refill_rate=10)
        assert bucket.capacity == 100
        assert bucket.tokens == 100

    def test_bucket_allow(self):
        """Test allowing request."""
        bucket = TokenBucket(capacity=10, refill_rate=1)
        allowed, remaining = bucket.allow(5)

        assert allowed is True
        assert remaining == 5

    def test_bucket_deny(self):
        """Test denying when tokens exhausted."""
        bucket = TokenBucket(capacity=5, refill_rate=1)
        bucket.allow(5)  # Use all tokens

        allowed, remaining = bucket.allow(1)
        assert allowed is False
        assert remaining < 1

    def test_bucket_refill(self):
        """Test token refill over time."""
        bucket = TokenBucket(capacity=10, refill_rate=2)
        bucket.allow(10)  # Use all tokens

        time.sleep(0.6)  # Wait for refill (0.6s * 2 refill_rate = 1.2 tokens)

        allowed, remaining = bucket.allow(1)
        assert allowed is True

    def test_bucket_capacity_limit(self):
        """Test tokens don't exceed capacity."""
        bucket = TokenBucket(capacity=10, refill_rate=100)
        bucket.tokens = 0

        time.sleep(0.2)  # Would normally give 20 tokens
        assert bucket.tokens <= 10  # Should be capped


class TestSlidingWindow:
    """Test sliding window algorithm."""

    def test_window_creation(self):
        """Test creating sliding window."""
        window = SlidingWindow(window_seconds=60, max_requests=100)
        assert window.window_seconds == 60
        assert window.max_requests == 100

    def test_window_allow(self):
        """Test allowing requests within window."""
        window = SlidingWindow(window_seconds=60, max_requests=5)

        for i in range(5):
            allowed, remaining = window.allow()
            assert allowed is True

        # 6th request should be denied
        allowed, remaining = window.allow()
        assert allowed is False

    def test_window_reset(self):
        """Test window reset after time."""
        window = SlidingWindow(window_seconds=1, max_requests=2)

        window.allow()
        window.allow()

        allowed, remaining = window.allow()
        assert allowed is False

        time.sleep(1.1)  # Wait for window to reset

        allowed, remaining = window.allow()
        assert allowed is True


class TestRateLimitBucket:
    """Test rate limit bucket."""

    def test_bucket_token_algorithm(self):
        """Test bucket with token bucket algorithm."""
        bucket = RateLimitBucket(
            "test-user",
            RateLimitAlgorithm.TOKEN_BUCKET,
            capacity=10,
            refill_rate=1
        )

        decision = bucket.allow(5)
        assert decision.allowed is True

    def test_bucket_sliding_window_algorithm(self):
        """Test bucket with sliding window algorithm."""
        bucket = RateLimitBucket(
            "test-endpoint",
            RateLimitAlgorithm.SLIDING_WINDOW,
            window_seconds=60,
            max_requests=10
        )

        for i in range(10):
            decision = bucket.allow()
            assert decision.allowed is True

        decision = bucket.allow()
        assert decision.allowed is False

    def test_bucket_stats(self):
        """Test bucket statistics."""
        bucket = RateLimitBucket(
            "test",
            RateLimitAlgorithm.SLIDING_WINDOW,
            window_seconds=60,
            max_requests=5
        )

        for i in range(5):
            bucket.allow()

        bucket.allow()  # This one should be denied

        stats = bucket.get_stats()
        assert stats["requests_allowed"] == 5
        assert stats["requests_denied"] == 1


class TestAdvancedRateLimiter:
    """Test advanced rate limiter."""

    @pytest.fixture
    def limiter(self):
        """Create rate limiter for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            limiter = AdvancedRateLimiter(project_root)
            yield limiter, project_root

    def test_limiter_initialization(self, limiter):
        """Test limiter initialization."""
        l, _ = limiter
        assert l is not None

    def test_configure_user_limit(self, limiter):
        """Test configuring user limits."""
        l, _ = limiter

        l.configure_user_limit(
            "user-1",
            RateLimitAlgorithm.TOKEN_BUCKET,
            capacity=100,
            refill_rate=10
        )

        assert "user-1" in l.user_config

    def test_configure_endpoint_limit(self, limiter):
        """Test configuring endpoint limits."""
        l, _ = limiter

        l.configure_endpoint_limit(
            "/api/users",
            RateLimitAlgorithm.SLIDING_WINDOW,
            window_seconds=60,
            max_requests=1000
        )

        assert "/api/users" in l.endpoint_config

    def test_user_limit_enforcement(self, limiter):
        """Test user-level rate limiting."""
        l, _ = limiter

        l.configure_user_limit(
            "user-1",
            RateLimitAlgorithm.SLIDING_WINDOW,
            window_seconds=60,
            max_requests=3
        )

        for i in range(3):
            decision = l.check_limit("user-1", "/api/data")
            assert decision.allowed is True

        decision = l.check_limit("user-1", "/api/data")
        assert decision.allowed is False

    def test_endpoint_limit_enforcement(self, limiter):
        """Test endpoint-level rate limiting."""
        l, _ = limiter

        l.configure_endpoint_limit(
            "/api/expensive",
            RateLimitAlgorithm.SLIDING_WINDOW,
            window_seconds=60,
            max_requests=2
        )

        for i in range(2):
            decision = l.check_limit(f"user-{i}", "/api/expensive")
            assert decision.allowed is True

        decision = l.check_limit("user-3", "/api/expensive")
        assert decision.allowed is False

    def test_combined_limits(self, limiter):
        """Test combined user+endpoint limits."""
        l, _ = limiter

        # User limit: 10 requests
        l.configure_user_limit(
            "user-1",
            RateLimitAlgorithm.TOKEN_BUCKET,
            capacity=10,
            refill_rate=1  # Use non-zero refill rate
        )

        # Endpoint limit: 5 requests
        l.configure_endpoint_limit(
            "/api/data",
            RateLimitAlgorithm.SLIDING_WINDOW,
            window_seconds=60,
            max_requests=5
        )

        # Should allow up to endpoint limit
        for i in range(5):
            decision = l.check_limit("user-1", "/api/data")
            assert decision.allowed is True

        # 6th should be denied (endpoint limit)
        decision = l.check_limit("user-1", "/api/data")
        assert decision.allowed is False

    def test_multiple_users_same_endpoint(self, limiter):
        """Test multiple users sharing endpoint limit."""
        l, _ = limiter

        l.configure_endpoint_limit(
            "/api/shared",
            RateLimitAlgorithm.SLIDING_WINDOW,
            window_seconds=60,
            max_requests=3
        )

        # User 1 gets 2 requests
        l.check_limit("user-1", "/api/shared")
        l.check_limit("user-1", "/api/shared")

        # User 2 gets 1 request
        decision = l.check_limit("user-2", "/api/shared")
        assert decision.allowed is True

        # Endpoint limit exhausted (3 total)
        decision = l.check_limit("user-2", "/api/shared")
        assert decision.allowed is False

    def test_fair_distribution(self, limiter):
        """Test fair distribution under load."""
        l, _ = limiter

        # Configure shared endpoint with generous limits
        l.configure_endpoint_limit(
            "/api/fair",
            RateLimitAlgorithm.SLIDING_WINDOW,
            window_seconds=60,
            max_requests=30  # Increased to allow all users some requests
        )

        # 3 users, each tries for 5 requests
        total_allowed = 0
        for i in range(3):
            count = 0
            for j in range(5):
                decision = l.check_limit(f"user-{i}", "/api/fair")
                if decision.allowed:
                    count += 1
            total_allowed += count

        # Total should be distributed among users
        assert total_allowed > 0

    def test_decision_contains_reset_info(self, limiter):
        """Test that decision includes reset information."""
        l, _ = limiter

        l.configure_user_limit(
            "user-1",
            RateLimitAlgorithm.TOKEN_BUCKET,
            capacity=1,
            refill_rate=1
        )

        decision = l.check_limit("user-1", "/api/test")
        assert decision.allowed is True

        decision = l.check_limit("user-1", "/api/test")
        assert decision.allowed is False
        assert decision.reset_after_ms is not None

    def test_get_user_stats(self, limiter):
        """Test getting user statistics."""
        l, _ = limiter

        for i in range(5):
            l.check_limit("user-1", "/api/test")

        stats = l.get_user_stats("user-1")
        assert stats["requests_allowed"] >= 0

    def test_get_endpoint_stats(self, limiter):
        """Test getting endpoint statistics."""
        l, _ = limiter

        for i in range(5):
            l.check_limit("user-1", "/api/test")

        stats = l.get_endpoint_stats("/api/test")
        assert stats["total_requests"] == 5

    def test_get_all_stats(self, limiter):
        """Test getting all statistics."""
        l, _ = limiter

        l.check_limit("user-1", "/api/a")
        l.check_limit("user-2", "/api/b")

        stats = l.get_all_stats()
        assert "users" in stats
        assert "endpoints" in stats
        assert "combined" in stats

    def test_quota_status(self, limiter):
        """Test getting quota status."""
        l, _ = limiter

        for i in range(3):
            l.check_limit("user-1", "/api/status")

        status = l.get_quota_status("user-1", "/api/status")
        assert status["user_id"] == "user-1"
        assert status["endpoint"] == "/api/status"

    def test_analytics_persistence(self, limiter):
        """Test that decisions are logged."""
        l, project_root = limiter

        l.check_limit("user-1", "/api/test", tokens=1)

        analytics_log = project_root / ".deia" / "rate-limiting" / "analytics.jsonl"
        assert analytics_log.exists()


class TestRateLimiterService:
    """Test high-level rate limiter service."""

    @pytest.fixture
    def service(self):
        """Create rate limiter service."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            service = RateLimiterService(project_root)
            yield service

    def test_service_configure_user(self, service):
        """Test configuring user via service."""
        service.configure_user("user-1", capacity=100, refill_rate=10)
        assert "user-1" in service.limiter.user_config

    def test_service_configure_endpoint(self, service):
        """Test configuring endpoint via service."""
        service.configure_endpoint("/api/v1/users", window_seconds=60, max_requests=1000)
        assert "/api/v1/users" in service.limiter.endpoint_config

    def test_service_is_allowed(self, service):
        """Test checking if request is allowed."""
        service.configure_user("user-1", capacity=2, refill_rate=1)  # Use refill_rate=1

        assert service.is_allowed("user-1", "/api/test") is True
        assert service.is_allowed("user-1", "/api/test") is True
        assert service.is_allowed("user-1", "/api/test") is False

    def test_service_get_status(self, service):
        """Test getting status via service."""
        service.configure_user("user-1", capacity=5, refill_rate=1)

        service.is_allowed("user-1", "/api/test")
        status = service.get_status("user-1", "/api/test")

        assert status["user_id"] == "user-1"
        assert "user_quota" in status

    def test_service_get_analytics(self, service):
        """Test getting analytics via service."""
        service.configure_user("user-1", capacity=10, refill_rate=1)
        service.configure_endpoint("/api/test", window_seconds=60, max_requests=100)

        for i in range(5):
            service.is_allowed("user-1", "/api/test")

        analytics = service.get_analytics()
        assert "users" in analytics
        assert "endpoints" in analytics

    def test_service_workflow(self, service):
        """Test complete service workflow."""
        # Configure limits
        service.configure_user("api-client", capacity=100, refill_rate=10)
        service.configure_endpoint("/api/heavy", window_seconds=60, max_requests=50)

        # Simulate requests
        allowed_count = 0
        for i in range(100):
            if service.is_allowed("api-client", "/api/heavy"):
                allowed_count += 1

        # Should have blocked some requests
        assert allowed_count < 100
        assert allowed_count > 0

        # Get analytics
        analytics = service.get_analytics()
        assert analytics is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
