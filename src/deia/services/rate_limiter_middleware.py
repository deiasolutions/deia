"""
Rate Limiter Middleware - Apply rate limits to endpoints

Uses token bucket algorithm for efficient rate limiting.
"""

from fastapi import Request, HTTPException, status
from typing import Optional, Tuple, Dict
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


class RateLimitConfig:
    """Configuration for rate limiting per endpoint"""

    # Define limits per endpoint: (max_requests, window_seconds)
    LIMITS = {
        "/api/auth/login": (5, 300),           # 5 per 5 minutes (prevent brute force)
        "/api/auth/register": (3, 300),        # 3 per 5 minutes (prevent spam)
        "/api/bot/launch": (10, 60),           # 10 per minute
        "/api/bot/stop": (10, 60),             # 10 per minute
        "/api/bot/{bot_id}/task": (20, 60),    # 20 per minute
        "/api/bots": (30, 60),                 # 30 per minute (frequent polling)
        "/api/bots/status": (30, 60),          # 30 per minute
        "/api/chat/history": (30, 60),         # 30 per minute
        "/ws": (5, 60),                        # 5 connections per minute
    }

    @staticmethod
    def get_limit(endpoint: str) -> Optional[Tuple[int, int]]:
        """
        Get rate limit for endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Tuple of (max_requests, window_seconds) or None if no limit
        """
        # Try exact match first
        if endpoint in RateLimitConfig.LIMITS:
            return RateLimitConfig.LIMITS[endpoint]

        # Try pattern matching for parameterized endpoints
        for pattern, limit in RateLimitConfig.LIMITS.items():
            if "{" in pattern:
                # Convert pattern to regex-like matching
                pattern_parts = pattern.split("{")
                if endpoint.startswith(pattern_parts[0]):
                    return limit

        return None


class RateLimiter:
    """
    Token bucket rate limiter for in-memory rate limiting.

    Tracks requests per user/IP and enforces limits.
    """

    def __init__(self):
        """Initialize rate limiter"""
        # {user_id:endpoint: {"tokens": float, "last_refill": float}}
        self.buckets: Dict[str, Dict] = {}

    def is_allowed(
        self,
        user_id: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int
    ) -> bool:
        """
        Check if request is allowed under rate limit using token bucket algorithm.

        Args:
            user_id: User identifier (username or IP)
            endpoint: API endpoint
            max_requests: Max requests allowed
            window_seconds: Time window in seconds

        Returns:
            True if request allowed, False if rate limit exceeded
        """
        now = time.time()
        key = f"{user_id}:{endpoint}"

        # Initialize bucket if not exists
        if key not in self.buckets:
            self.buckets[key] = {
                "tokens": float(max_requests),
                "last_refill": now
            }

        bucket = self.buckets[key]

        # Refill tokens based on time elapsed
        time_passed = now - bucket["last_refill"]
        tokens_to_add = (time_passed / window_seconds) * max_requests
        bucket["tokens"] = min(float(max_requests), bucket["tokens"] + tokens_to_add)
        bucket["last_refill"] = now

        # Check if request allowed
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        else:
            return False

    def get_retry_after(
        self,
        user_id: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int
    ) -> int:
        """
        Get seconds to wait before next request is allowed.

        Args:
            user_id: User identifier
            endpoint: API endpoint
            max_requests: Max requests allowed
            window_seconds: Time window in seconds

        Returns:
            Seconds to wait (0 if request is allowed)
        """
        key = f"{user_id}:{endpoint}"
        if key in self.buckets:
            bucket = self.buckets[key]
            time_since_refill = time.time() - bucket["last_refill"]
            return max(0, int(window_seconds - time_since_refill))
        return 0

    def cleanup_expired(self, ttl_seconds: int = 3600):
        """
        Remove expired rate limit entries (cleanup old buckets).

        Args:
            ttl_seconds: Time to live for a bucket (default 1 hour)
        """
        now = time.time()
        expired_keys = [
            key for key, bucket in self.buckets.items()
            if (now - bucket["last_refill"]) > ttl_seconds
        ]
        for key in expired_keys:
            del self.buckets[key]
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired rate limit buckets")


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """
    FastAPI middleware for rate limiting.

    Checks rate limit before processing request.
    Returns 429 if limit exceeded.
    """
    endpoint = request.url.path

    # Get limit for this endpoint
    limit = RateLimitConfig.get_limit(endpoint)
    if not limit:
        # No limit configured for this endpoint
        return await call_next(request)

    max_requests, window_seconds = limit

    # Get user identifier
    # Priority: authenticated user > client IP
    user_id = None

    # Try to get user from Authorization header (JWT)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        user_id = auth_header[7:]  # Extract token

    # Fallback to client IP
    if not user_id:
        client_ip = request.client.host if request.client else "unknown"
        user_id = client_ip

    # Check rate limit
    if not rate_limiter.is_allowed(user_id, endpoint, max_requests, window_seconds):
        retry_after = rate_limiter.get_retry_after(user_id, endpoint, max_requests, window_seconds)
        logger.warning(
            f"Rate limit exceeded for {user_id} on {endpoint} "
            f"(limit: {max_requests}/{window_seconds}s, retry after: {retry_after}s)"
        )
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )

    # Process request
    return await call_next(request)
