# TASK: P0 CRITICAL - Rate Limiting Integration

**Priority:** P0 CRITICAL (DoS Vulnerability)
**Time Estimate:** 30 minutes
**Start:** After JWT Authentication task
**Impact:** Without this, anyone can overwhelm the server with requests

---

## PROBLEM

Rate limiter service exists but **isn't wired to API endpoints**.

**Consequences:**
- ❌ Users can spam endpoints without limit
- ❌ No protection against brute force attacks
- ❌ No protection against accidental abuse
- ❌ Server can be overwhelmed by single user
- ❌ Production-grade reliability impossible

---

## SOLUTION

Wire existing `RateLimiter` service to all public endpoints.

**Note:** The rate limiter already exists in codebase (`src/deia/services/rate_limiter.py`). We just need to integrate it.

---

## PART 1: Create Rate Limiter Middleware

**File:** `src/deia/services/rate_limiter_middleware.py` (NEW)

```python
"""
Rate Limiter Middleware - Apply rate limits to endpoints

Uses the existing RateLimiter service configured per endpoint.
"""

from fastapi import Request, HTTPException, status
from functools import wraps
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)


class RateLimitConfig:
    """Configuration for rate limiting"""

    # Define limits per endpoint
    LIMITS = {
        "/api/auth/login": (5, 300),           # 5 per 5 minutes
        "/api/auth/register": (3, 300),        # 3 per 5 minutes
        "/api/bot/launch": (10, 60),           # 10 per minute
        "/api/bot/stop": (10, 60),             # 10 per minute
        "/api/bot/{bot_id}/task": (20, 60),    # 20 per minute
        "/api/bots/status": (30, 60),          # 30 per minute (frequent polling)
        "/api/chat/history": (30, 60),         # 30 per minute
        "/ws": (5, 60),                        # 5 connections per minute
    }

    @staticmethod
    def get_limit(endpoint: str) -> Optional[tuple]:
        """Get rate limit for endpoint (requests, seconds)"""
        return RateLimitConfig.LIMITS.get(endpoint)


class RateLimiter:
    """
    In-memory rate limiter using token bucket algorithm.

    Tracks requests per user/IP and enforces limits.
    """

    def __init__(self):
        self.buckets = {}  # {user_id: {endpoint: (tokens, last_refill)}}

    def is_allowed(self, user_id: str, endpoint: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if request is allowed under rate limit.

        Args:
            user_id: User identifier (username or IP)
            endpoint: API endpoint
            max_requests: Max requests allowed
            window_seconds: Time window in seconds

        Returns:
            True if request allowed, False if rate limit exceeded
        """
        import time

        now = time.time()
        key = f"{user_id}:{endpoint}"

        if key not in self.buckets:
            self.buckets[key] = {"tokens": max_requests, "last_refill": now}

        bucket = self.buckets[key]

        # Refill tokens based on time elapsed
        time_passed = now - bucket["last_refill"]
        tokens_to_add = (time_passed / window_seconds) * max_requests
        bucket["tokens"] = min(max_requests, bucket["tokens"] + tokens_to_add)
        bucket["last_refill"] = now

        # Check if request allowed
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        else:
            return False

    def get_retry_after(self, user_id: str, endpoint: str, max_requests: int, window_seconds: int) -> int:
        """Get seconds to wait before next request is allowed"""
        import time

        key = f"{user_id}:{endpoint}"
        if key in self.buckets:
            bucket = self.buckets[key]
            time_since_refill = time.time() - bucket["last_refill"]
            return max(0, int(window_seconds - time_since_refill))
        return window_seconds


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """
    FastAPI middleware for rate limiting.

    Checks rate limit before processing request.
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

    # Try to get username from query token
    token = request.query_params.get("token")
    if token:
        try:
            from deia.services.auth_service import AuthService
            from deia.services.chat_interface_app import auth_service
            user_id = auth_service.get_user_from_token(token)
        except:
            pass

    # Fallback to IP address
    if not user_id:
        user_id = request.client.host if request.client else "unknown"

    # Check rate limit
    if not rate_limiter.is_allowed(user_id, endpoint, max_requests, window_seconds):
        retry_after = rate_limiter.get_retry_after(user_id, endpoint, max_requests, window_seconds)
        logger.warning(f"Rate limit exceeded for {user_id} on {endpoint}")

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Retry after {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)}
        )

    response = await call_next(request)

    # Add rate limit headers to response
    response.headers["X-RateLimit-Limit"] = str(max_requests)
    response.headers["X-RateLimit-Window"] = str(window_seconds)

    key = f"{user_id}:{endpoint}"
    remaining = max(0, int(rate_limiter.buckets.get(key, {}).get("tokens", max_requests)))
    response.headers["X-RateLimit-Remaining"] = str(remaining)

    return response
```

---

## PART 2: Add Middleware to FastAPI App

**File:** `src/deia/services/chat_interface_app.py`

**Add imports:**
```python
from deia.services.rate_limiter_middleware import rate_limit_middleware
```

**Add middleware to app (right after creating FastAPI app):**
```python
app = FastAPI(title="Chat Interface")

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# ... rest of app setup
```

---

## PART 3: Add Rate Limit Response Headers

**Update all endpoints to include rate limit info** (the middleware handles this automatically, but we can enhance responses)

When returning rate limit errors, the middleware adds:
- `X-RateLimit-Limit`: Max requests allowed
- `X-RateLimit-Window`: Time window in seconds
- `X-RateLimit-Remaining`: Requests remaining
- `Retry-After`: Seconds until rate limit resets

These help clients know when they can retry.

---

## PART 4: Create Tests

**File:** `tests/unit/test_rate_limiter_middleware.py` (NEW)

```python
"""Tests for Rate Limiter Middleware"""

import pytest
import asyncio
from deia.services.rate_limiter_middleware import RateLimiter, RateLimitConfig


def test_rate_limiter_init():
    """Test rate limiter initialization"""
    limiter = RateLimiter()
    assert limiter.buckets == {}


def test_rate_limiter_allows_requests():
    """Test rate limiter allows requests within limit"""
    limiter = RateLimiter()

    # Should allow 3 requests
    assert limiter.is_allowed("user-1", "/endpoint", 3, 60) == True
    assert limiter.is_allowed("user-1", "/endpoint", 3, 60) == True
    assert limiter.is_allowed("user-1", "/endpoint", 3, 60) == True

    # 4th should be blocked
    assert limiter.is_allowed("user-1", "/endpoint", 3, 60) == False


def test_rate_limiter_per_user():
    """Test rate limiter isolates per user"""
    limiter = RateLimiter()

    # User 1 uses 2/3 requests
    assert limiter.is_allowed("user-1", "/endpoint", 3, 60) == True
    assert limiter.is_allowed("user-1", "/endpoint", 3, 60) == True

    # User 2 should still have 3/3
    assert limiter.is_allowed("user-2", "/endpoint", 3, 60) == True
    assert limiter.is_allowed("user-2", "/endpoint", 3, 60) == True
    assert limiter.is_allowed("user-2", "/endpoint", 3, 60) == True


def test_rate_limiter_per_endpoint():
    """Test rate limiter isolates per endpoint"""
    limiter = RateLimiter()

    # User 1 at endpoint A
    assert limiter.is_allowed("user-1", "/endpoint-a", 2, 60) == True
    assert limiter.is_allowed("user-1", "/endpoint-a", 2, 60) == True

    # Same user at endpoint B should have fresh limit
    assert limiter.is_allowed("user-1", "/endpoint-b", 2, 60) == True
    assert limiter.is_allowed("user-1", "/endpoint-b", 2, 60) == True


def test_rate_limit_config():
    """Test rate limit configuration"""
    # Login should have strict limit
    assert RateLimitConfig.get_limit("/api/auth/login") == (5, 300)

    # Task endpoint should have looser limit
    assert RateLimitConfig.get_limit("/api/bot/{bot_id}/task") == (20, 60)

    # Unconfigured endpoint
    assert RateLimitConfig.get_limit("/unknown") is None


def test_rate_limiter_retry_after():
    """Test retry-after calculation"""
    limiter = RateLimiter()

    # Use all tokens
    limiter.is_allowed("user-1", "/endpoint", 1, 60)
    limiter.is_allowed("user-1", "/endpoint", 1, 60)  # Blocked

    # Get retry-after
    retry_after = limiter.get_retry_after("user-1", "/endpoint", 1, 60)
    assert 0 <= retry_after <= 60


@pytest.mark.asyncio
async def test_rate_limiter_middleware(client):
    """Test rate limiter middleware on actual endpoint"""
    # This would require a test client, implementation depends on test setup
    pass
```

---

## PART 5: Update Frontend to Handle Rate Limits

**File:** `src/deia/services/static/js/utils/toast.js` or `app.js`

**Add error handling for 429 responses:**

```javascript
async function makeApiCall(endpoint, options = {}) {
  try {
    const response = await fetch(endpoint, options);

    // Check for rate limit
    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After');
      Toast.warning(`⏱️ Rate limit exceeded. Retry after ${retryAfter} seconds.`);
      return { success: false, error: 'rate_limit' };
    }

    // Log rate limit headers
    const remaining = response.headers.get('X-RateLimit-Remaining');
    if (remaining && parseInt(remaining) < 5) {
      Toast.warning(`⚠️ Only ${remaining} requests remaining`);
    }

    return await response.json();
  } catch (error) {
    Toast.error(`Error: ${error.message}`);
    return { success: false, error: error.message };
  }
}
```

---

## TESTING

```bash
# Test rate limiter logic
pytest tests/unit/test_rate_limiter_middleware.py -v

# Test with actual API calls
pytest tests/integration/test_rate_limiting.py -v
```

---

## CHECKLIST

- [ ] Create `rate_limiter_middleware.py` with rate limiting logic
- [ ] Add rate limiter configuration for all endpoints
- [ ] Add middleware to FastAPI app in chat_interface_app.py
- [ ] Update frontend to handle 429 responses
- [ ] Create tests in `test_rate_limiter_middleware.py`
- [ ] Tests passing
- [ ] Verify rate limit headers in responses
- [ ] Verify 429 errors when limits exceeded
- [ ] Create completion report

---

## LIMITS

Default limits (configurable):

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/auth/login` | 5 | 5 min |
| `/api/auth/register` | 3 | 5 min |
| `/api/bot/launch` | 10 | 1 min |
| `/api/bot/stop` | 10 | 1 min |
| `/api/bot/{bot_id}/task` | 20 | 1 min |
| `/api/bots/status` | 30 | 1 min |
| `/api/chat/history` | 30 | 1 min |
| `/ws` | 5 | 1 min |

---

## COMPLETION

When finished, create: `.deia/hive/responses/deiasolutions/p0-rate-limiting-complete.md`

Write:
- Rate limiter integrated into all endpoints
- Token bucket algorithm implemented
- 429 responses with Retry-After header
- Rate limit headers in responses
- Frontend handles rate limits gracefully
- Tests passing
- Production-ready rate limiting active
