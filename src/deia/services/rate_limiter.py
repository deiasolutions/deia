#!/usr/bin/env python3
"""Advanced Rate Limiting: Multiple algorithms with fair allocation.

Algorithms:
- Token Bucket: Smooth burst handling
- Sliding Window: Precise rate limiting

Features:
- Per-user rate limits
- Per-endpoint rate limits
- Fair distribution under load
- Graceful degradation
- Client quota tracking
- Analytics and reporting
"""

import time
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple
from enum import Enum
from collections import defaultdict, deque
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - RATE-LIMITER - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RateLimitAlgorithm(Enum):
    """Rate limiting algorithms."""
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"


class RateLimitDecision:
    """Decision result for rate limit check."""

    def __init__(self, allowed: bool, tokens_remaining: float, reset_after_ms: Optional[float] = None):
        """Initialize decision.

        Args:
            allowed: Whether request is allowed
            tokens_remaining: Tokens left in quota
            reset_after_ms: Time until quota reset (milliseconds)
        """
        self.allowed = allowed
        self.tokens_remaining = tokens_remaining
        self.reset_after_ms = reset_after_ms
        self.timestamp = datetime.utcnow().isoformat() + "Z"


class TokenBucket:
    """Token bucket rate limiter."""

    def __init__(self, capacity: float, refill_rate: float):
        """Initialize token bucket.

        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def allow(self, tokens: float = 1.0) -> Tuple[bool, float]:
        """Check if tokens available.

        Args:
            tokens: Number of tokens needed

        Returns:
            Tuple of (allowed, tokens_remaining)
        """
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time (only if refill_rate > 0)
            if self.refill_rate > 0:
                refilled = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + refilled)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True, self.tokens

            return False, self.tokens


class SlidingWindow:
    """Sliding window rate limiter."""

    def __init__(self, window_seconds: int, max_requests: int):
        """Initialize sliding window.

        Args:
            window_seconds: Time window in seconds
            max_requests: Max requests in window
        """
        self.window_seconds = window_seconds
        self.max_requests = max_requests
        self.requests = deque()  # (timestamp) tuples
        self.lock = threading.Lock()

    def allow(self) -> Tuple[bool, int]:
        """Check if request allowed.

        Returns:
            Tuple of (allowed, remaining_in_window)
        """
        with self.lock:
            now = time.time()
            window_start = now - self.window_seconds

            # Remove old requests outside window
            while self.requests and self.requests[0] < window_start:
                self.requests.popleft()

            remaining = self.max_requests - len(self.requests)

            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True, remaining

            return False, remaining


class RateLimitBucket:
    """Rate limit bucket for single entity (user/endpoint/combo)."""

    def __init__(self, identifier: str, algorithm: RateLimitAlgorithm, **kwargs):
        """Initialize rate limit bucket.

        Args:
            identifier: Unique identifier (user, endpoint, etc)
            algorithm: Algorithm to use
            **kwargs: Algorithm-specific parameters
        """
        self.identifier = identifier
        self.algorithm = algorithm
        self.created_at = time.time()
        self.requests_allowed = 0
        self.requests_denied = 0
        self.lock = threading.Lock()

        if algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
            self.limiter = TokenBucket(**kwargs)
        elif algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
            self.limiter = SlidingWindow(**kwargs)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def allow(self, tokens: float = 1.0) -> RateLimitDecision:
        """Check if request allowed.

        Args:
            tokens: Tokens needed (for token bucket)

        Returns:
            RateLimitDecision
        """
        with self.lock:
            if self.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
                allowed, remaining = self.limiter.allow(tokens)
                if self.limiter.refill_rate > 0:
                    reset_after = (self.limiter.capacity - remaining) / self.limiter.refill_rate * 1000
                else:
                    reset_after = float('inf')  # No refill, tokens never replenish
            else:  # SLIDING_WINDOW
                allowed, remaining = self.limiter.allow()
                reset_after = self.limiter.window_seconds * 1000

            if allowed:
                self.requests_allowed += 1
            else:
                self.requests_denied += 1

            return RateLimitDecision(allowed, remaining, reset_after if not allowed else None)

    def get_stats(self) -> Dict:
        """Get bucket statistics."""
        with self.lock:
            total = self.requests_allowed + self.requests_denied
            return {
                "identifier": self.identifier,
                "algorithm": self.algorithm.value,
                "requests_allowed": self.requests_allowed,
                "requests_denied": self.requests_denied,
                "total_requests": total,
                "allow_rate": self.requests_allowed / total if total > 0 else 0,
                "uptime_seconds": time.time() - self.created_at
            }


class AdvancedRateLimiter:
    """Advanced rate limiter with multi-level limiting."""

    def __init__(self, project_root: Path = None):
        """Initialize rate limiter.

        Args:
            project_root: Project root for analytics storage
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.analytics_dir = project_root / ".deia" / "rate-limiting"
        self.analytics_dir.mkdir(parents=True, exist_ok=True)

        self.analytics_log = self.analytics_dir / "analytics.jsonl"
        self.metrics_log = project_root / ".deia" / "logs" / "rate-limiter-metrics.jsonl"
        self.metrics_log.parent.mkdir(parents=True, exist_ok=True)

        # Rate limit buckets
        self.user_limits: Dict[str, RateLimitBucket] = {}  # user_id -> bucket
        self.endpoint_limits: Dict[str, RateLimitBucket] = {}  # endpoint -> bucket
        self.combined_limits: Dict[str, RateLimitBucket] = {}  # user_id:endpoint -> bucket

        # Configuration
        self.user_config = {}  # user_id -> {limit_config}
        self.endpoint_config = {}  # endpoint -> {limit_config}

        self.lock = threading.RLock()

        logger.info("AdvancedRateLimiter initialized")

    def configure_user_limit(self, user_id: str, algorithm: RateLimitAlgorithm = RateLimitAlgorithm.TOKEN_BUCKET, **kwargs):
        """Configure rate limit for user.

        Args:
            user_id: User ID
            algorithm: Algorithm to use
            **kwargs: Algorithm parameters
        """
        with self.lock:
            self.user_config[user_id] = {
                "algorithm": algorithm,
                "params": kwargs
            }
            logger.info(f"User limit configured for '{user_id}': {algorithm.value}")

    def configure_endpoint_limit(self, endpoint: str, algorithm: RateLimitAlgorithm = RateLimitAlgorithm.SLIDING_WINDOW, **kwargs):
        """Configure rate limit for endpoint.

        Args:
            endpoint: Endpoint path (e.g., "/api/users")
            algorithm: Algorithm to use
            **kwargs: Algorithm parameters
        """
        with self.lock:
            self.endpoint_config[endpoint] = {
                "algorithm": algorithm,
                "params": kwargs
            }
            logger.info(f"Endpoint limit configured for '{endpoint}': {algorithm.value}")

    def check_limit(self, user_id: str, endpoint: str, tokens: float = 1.0) -> RateLimitDecision:
        """Check rate limit for user+endpoint.

        Multi-level check: user limit AND endpoint limit AND combined limit

        Args:
            user_id: User ID
            endpoint: Endpoint path
            tokens: Tokens needed

        Returns:
            RateLimitDecision (denied if any level rejects)
        """
        with self.lock:
            # Get user bucket
            user_key = user_id
            if user_key not in self.user_limits:
                config = self.user_config.get(user_id, {})
                algo = config.get("algorithm", RateLimitAlgorithm.TOKEN_BUCKET)
                params = config.get("params", {"capacity": 1000, "refill_rate": 100})
                self.user_limits[user_key] = RateLimitBucket(user_key, algo, **params)

            # Get endpoint bucket
            endpoint_key = endpoint
            if endpoint_key not in self.endpoint_limits:
                config = self.endpoint_config.get(endpoint, {})
                algo = config.get("algorithm", RateLimitAlgorithm.SLIDING_WINDOW)
                params = config.get("params", {"window_seconds": 60, "max_requests": 1000})
                self.endpoint_limits[endpoint_key] = RateLimitBucket(endpoint_key, algo, **params)

            # Get combined bucket (user + endpoint)
            combined_key = f"{user_id}:{endpoint}"
            if combined_key not in self.combined_limits:
                # Use stricter limits for combined
                self.combined_limits[combined_key] = RateLimitBucket(
                    combined_key,
                    RateLimitAlgorithm.TOKEN_BUCKET,
                    capacity=500,
                    refill_rate=50
                )

            # Check all levels
            user_decision = self.user_limits[user_key].allow(tokens)
            endpoint_decision = self.endpoint_limits[endpoint_key].allow()
            combined_decision = self.combined_limits[combined_key].allow(tokens)

            # Allow only if all levels allow
            allowed = user_decision.allowed and endpoint_decision.allowed and combined_decision.allowed

            # Determine reset time (maximum of all)
            reset_times = [d.reset_after_ms for d in [user_decision, endpoint_decision, combined_decision] if d.reset_after_ms]
            reset_after = max(reset_times) if reset_times else None

            decision = RateLimitDecision(
                allowed,
                min(user_decision.tokens_remaining, endpoint_decision.tokens_remaining, combined_decision.tokens_remaining),
                reset_after
            )

            # Log decision
            self._log_decision(user_id, endpoint, allowed)

            logger.debug(f"Rate limit check for {user_id}@{endpoint}: {'ALLOWED' if allowed else 'DENIED'}")
            return decision

    def get_user_stats(self, user_id: str) -> Dict:
        """Get statistics for user."""
        with self.lock:
            if user_id not in self.user_limits:
                return {}
            return self.user_limits[user_id].get_stats()

    def get_endpoint_stats(self, endpoint: str) -> Dict:
        """Get statistics for endpoint."""
        with self.lock:
            if endpoint not in self.endpoint_limits:
                return {}
            return self.endpoint_limits[endpoint].get_stats()

    def get_all_stats(self) -> Dict:
        """Get statistics for all buckets."""
        with self.lock:
            return {
                "users": {k: v.get_stats() for k, v in self.user_limits.items()},
                "endpoints": {k: v.get_stats() for k, v in self.endpoint_limits.items()},
                "combined": {k: v.get_stats() for k, v in self.combined_limits.items()}
            }

    def get_quota_status(self, user_id: str, endpoint: str) -> Dict:
        """Get current quota status."""
        with self.lock:
            user_stats = self.get_user_stats(user_id)
            endpoint_stats = self.get_endpoint_stats(endpoint)

            return {
                "user_id": user_id,
                "endpoint": endpoint,
                "user_quota": user_stats,
                "endpoint_quota": endpoint_stats
            }

    def _log_decision(self, user_id: str, endpoint: str, allowed: bool):
        """Log rate limiting decision."""
        try:
            entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "user_id": user_id,
                "endpoint": endpoint,
                "allowed": allowed
            }
            with open(self.analytics_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to log decision: {e}")


class RateLimiterService:
    """High-level rate limiter service for applications."""

    def __init__(self, project_root: Path = None):
        """Initialize rate limiter service."""
        self.limiter = AdvancedRateLimiter(project_root)

    def configure_user(self, user_id: str, capacity: float = 1000, refill_rate: float = 100):
        """Configure token bucket for user."""
        self.limiter.configure_user_limit(
            user_id,
            RateLimitAlgorithm.TOKEN_BUCKET,
            capacity=capacity,
            refill_rate=refill_rate
        )

    def configure_endpoint(self, endpoint: str, window_seconds: int = 60, max_requests: int = 1000):
        """Configure sliding window for endpoint."""
        self.limiter.configure_endpoint_limit(
            endpoint,
            RateLimitAlgorithm.SLIDING_WINDOW,
            window_seconds=window_seconds,
            max_requests=max_requests
        )

    def is_allowed(self, user_id: str, endpoint: str, tokens: float = 1.0) -> bool:
        """Check if request is allowed."""
        decision = self.limiter.check_limit(user_id, endpoint, tokens)
        return decision.allowed

    def get_status(self, user_id: str, endpoint: str) -> Dict:
        """Get quota status."""
        return self.limiter.get_quota_status(user_id, endpoint)

    def get_analytics(self) -> Dict:
        """Get all analytics."""
        return self.limiter.get_all_stats()
