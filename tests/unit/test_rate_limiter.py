"""
Tests for Rate Limiter Middleware
"""

import pytest
import time
from deia.services.rate_limiter_middleware import RateLimiter, RateLimitConfig


class TestRateLimitConfig:
    """Test RateLimitConfig class"""

    def test_get_limit_exact_match(self):
        """Test getting limit for exact endpoint match"""
        limit = RateLimitConfig.get_limit("/api/bots")
        assert limit is not None
        assert limit == (30, 60)

    def test_get_limit_auth_login(self):
        """Test auth login has strict limit"""
        limit = RateLimitConfig.get_limit("/api/auth/login")
        assert limit == (5, 300)  # 5 per 5 minutes

    def test_get_limit_auth_register(self):
        """Test auth register has strict limit"""
        limit = RateLimitConfig.get_limit("/api/auth/register")
        assert limit == (3, 300)  # 3 per 5 minutes

    def test_get_limit_parametrized_endpoint(self):
        """Test getting limit for parameterized endpoint"""
        limit = RateLimitConfig.get_limit("/api/bot/BOT-001/task")
        assert limit is not None
        assert limit == (20, 60)

    def test_get_limit_no_limit(self):
        """Test endpoint with no configured limit"""
        limit = RateLimitConfig.get_limit("/api/unknown/endpoint")
        assert limit is None


class TestRateLimiter:
    """Test RateLimiter class"""

    @pytest.fixture
    def limiter(self):
        """Create fresh rate limiter for each test"""
        return RateLimiter()

    def test_initialization(self, limiter):
        """Test rate limiter initializes empty"""
        assert len(limiter.buckets) == 0

    def test_first_request_allowed(self, limiter):
        """Test first request is always allowed"""
        allowed = limiter.is_allowed("user1", "/api/bots", max_requests=5, window_seconds=60)
        assert allowed is True

    def test_multiple_requests_allowed(self, limiter):
        """Test multiple requests allowed within limit"""
        for i in range(5):
            allowed = limiter.is_allowed("user1", "/api/bots", max_requests=5, window_seconds=60)
            assert allowed is True

    def test_request_exceeds_limit(self, limiter):
        """Test request denied when limit exceeded"""
        # Use up all tokens
        for i in range(5):
            limiter.is_allowed("user1", "/api/bots", max_requests=5, window_seconds=60)

        # Next request should be denied
        allowed = limiter.is_allowed("user1", "/api/bots", max_requests=5, window_seconds=60)
        assert allowed is False

    def test_different_users_independent(self, limiter):
        """Test that different users have independent limits"""
        # User1 uses up their quota
        for i in range(5):
            limiter.is_allowed("user1", "/api/bots", max_requests=5, window_seconds=60)

        # User2 should still be allowed
        allowed = limiter.is_allowed("user2", "/api/bots", max_requests=5, window_seconds=60)
        assert allowed is True

    def test_strict_auth_limits(self, limiter):
        """Test strict limits for auth endpoints"""
        # Login limit: 5 per 5 minutes
        auth_limit = RateLimitConfig.get_limit("/api/auth/login")
        assert auth_limit == (5, 300)

        # Try 5 logins quickly - should work
        for i in range(5):
            allowed = limiter.is_allowed("user1", "/api/auth/login", *auth_limit)
            assert allowed is True

        # 6th should fail
        allowed = limiter.is_allowed("user1", "/api/auth/login", *auth_limit)
        assert allowed is False

    def test_register_limit_strict(self, limiter):
        """Test register has stricter limit than login"""
        register_limit = RateLimitConfig.get_limit("/api/auth/register")
        assert register_limit == (3, 300)  # Only 3 per 5 minutes

        # Try 3 registers
        for i in range(3):
            allowed = limiter.is_allowed("user1", "/api/auth/register", *register_limit)
            assert allowed is True

        # 4th should fail
        allowed = limiter.is_allowed("user1", "/api/auth/register", *register_limit)
        assert allowed is False
