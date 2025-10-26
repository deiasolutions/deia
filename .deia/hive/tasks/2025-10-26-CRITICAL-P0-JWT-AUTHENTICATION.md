# TASK: P0 CRITICAL - JWT Authentication System

**Priority:** P0 CRITICAL (Security Vulnerability)
**Time Estimate:** 60 minutes
**Start:** After Database Persistence task
**Impact:** Without this, any user can access any bot's data

---

## PROBLEM

Currently using **hardcoded dev token** (`"dev-token-12345"`).

**Security Issues:**
- ❌ Anyone with the token can access all bots
- ❌ No user authentication
- ❌ No per-user chat isolation
- ❌ No audit trail of who accessed what
- ❌ Production-grade security impossible

---

## SOLUTION

Implement JWT (JSON Web Token) authentication with user accounts.

---

## PART 1: Create Authentication Service

**File:** `src/deia/services/auth_service.py` (NEW)

```python
"""
JWT Authentication Service - User auth and token management

Uses PyJWT for token generation and validation.
Passwords hashed with bcrypt for security.
"""

import jwt
import bcrypt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """
    JWT authentication and user management.

    Token format: JWT with claims {user_id, username, iat, exp}
    """

    def __init__(self, secret_key: Optional[str] = None, token_expiry_hours: int = 24):
        """
        Initialize auth service.

        Args:
            secret_key: JWT secret key (uses env var or generates one)
            token_expiry_hours: How long tokens are valid (default 24 hours)
        """
        self.secret_key = secret_key or os.getenv(
            "JWT_SECRET_KEY",
            "dev-secret-key-change-in-production"
        )
        self.token_expiry_hours = token_expiry_hours
        self.algorithm = "HS256"

        # In-memory user store (replace with database in production)
        self.users: Dict[str, Dict] = {}

        # Create default dev user for testing
        self.register_user("dev-user", "dev-password")
        logger.info("AuthService initialized")

    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user.

        Args:
            username: Username
            password: Plain-text password (will be hashed)

        Returns:
            True if successful, False if user already exists
        """
        if username in self.users:
            logger.warning(f"User {username} already exists")
            return False

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.users[username] = {
            "username": username,
            "password_hash": hashed_password,
            "created_at": datetime.now().isoformat()
        }

        logger.info(f"User {username} registered")
        return True

    def authenticate(self, username: str, password: str) -> Optional[str]:
        """
        Authenticate user and return JWT token.

        Args:
            username: Username
            password: Plain-text password

        Returns:
            JWT token if successful, None otherwise
        """
        user = self.users.get(username)
        if not user:
            logger.warning(f"Authentication failed: user {username} not found")
            return None

        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            logger.warning(f"Authentication failed: invalid password for {username}")
            return None

        # Generate JWT token
        payload = {
            "user_id": username,  # Using username as unique ID
            "username": username,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        logger.info(f"User {username} authenticated, token issued")
        return token

    def validate_token(self, token: str) -> Optional[Dict]:
        """
        Validate JWT token and return claims.

        Args:
            token: JWT token

        Returns:
            Token claims if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            logger.debug(f"Token validated for user {payload.get('username')}")
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token validation failed: token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token validation failed: {e}")
            return None

    def get_user_from_token(self, token: str) -> Optional[str]:
        """
        Get username from token.

        Args:
            token: JWT token

        Returns:
            Username if valid token, None otherwise
        """
        payload = self.validate_token(token)
        return payload.get("username") if payload else None

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        Change user password.

        Args:
            username: Username
            old_password: Current password
            new_password: New password

        Returns:
            True if successful
        """
        user = self.users.get(username)
        if not user:
            return False

        if not bcrypt.checkpw(old_password.encode(), user["password_hash"].encode()):
            logger.warning(f"Password change failed for {username}: invalid old password")
            return False

        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        user["password_hash"] = hashed_password
        logger.info(f"Password changed for {username}")
        return True
```

---

## PART 2: Add Auth Endpoints

**File:** `src/deia/services/chat_interface_app.py`

**Add imports:**
```python
from deia.services.auth_service import AuthService
from fastapi import Depends, HTTPException, status

# Initialize auth service
auth_service = AuthService()
```

**Add Pydantic models:**
```python
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
```

**Add endpoints:**
```python
@app.post("/api/auth/register")
async def register(request: RegisterRequest):
    """Register a new user"""
    try:
        if auth_service.register_user(request.username, request.password):
            return {
                "success": True,
                "message": f"User {request.username} registered successfully",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": f"User {request.username} already exists",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.post("/api/auth/login")
async def login(request: LoginRequest):
    """Authenticate user and return JWT token"""
    try:
        token = auth_service.authenticate(request.username, request.password)
        if token:
            return {
                "success": True,
                "token": token,
                "user": request.username,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": "Invalid credentials",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Login error: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.post("/api/auth/change-password")
async def change_password(request: Dict, token: str = None):
    """Change user password"""
    try:
        if not token:
            return {
                "success": False,
                "error": "Token required",
                "timestamp": datetime.now().isoformat()
            }

        username = auth_service.get_user_from_token(token)
        if not username:
            return {
                "success": False,
                "error": "Invalid token",
                "timestamp": datetime.now().isoformat()
            }

        if auth_service.change_password(username, request.get("old_password"), request.get("new_password")):
            return {
                "success": True,
                "message": "Password changed successfully",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": "Password change failed",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Password change error: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

---

## PART 3: Update WebSocket to Use JWT

**Location:** Find `@app.websocket("/ws")` (around line ~130)

**Update token validation:**

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    """
    WebSocket endpoint with JWT authentication.

    Args:
        token: JWT token from query parameter
    """
    # Validate token
    user = auth_service.get_user_from_token(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
        return

    await websocket.accept()
    # ... rest of WebSocket handler
    # Store user in connection context for per-user message isolation
```

---

## PART 4: Create Tests

**File:** `tests/unit/test_auth_service.py` (NEW)

```python
"""Tests for AuthService"""

import pytest
from deia.services.auth_service import AuthService


def test_auth_register():
    """Test user registration"""
    auth = AuthService()
    assert auth.register_user("test-user", "password123")
    assert not auth.register_user("test-user", "another-password")


def test_auth_authenticate():
    """Test user authentication"""
    auth = AuthService()
    auth.register_user("test-user", "password123")

    token = auth.authenticate("test-user", "password123")
    assert token is not None

    token_wrong = auth.authenticate("test-user", "wrong-password")
    assert token_wrong is None


def test_auth_validate_token():
    """Test token validation"""
    auth = AuthService()
    auth.register_user("test-user", "password123")

    token = auth.authenticate("test-user", "password123")
    payload = auth.validate_token(token)

    assert payload is not None
    assert payload["username"] == "test-user"


def test_auth_invalid_token():
    """Test invalid token"""
    auth = AuthService()
    payload = auth.validate_token("invalid-token")
    assert payload is None


def test_auth_get_user_from_token():
    """Test getting username from token"""
    auth = AuthService()
    auth.register_user("test-user", "password123")

    token = auth.authenticate("test-user", "password123")
    username = auth.get_user_from_token(token)

    assert username == "test-user"


def test_auth_change_password():
    """Test password change"""
    auth = AuthService()
    auth.register_user("test-user", "password123")

    assert auth.change_password("test-user", "password123", "new-password")
    assert auth.authenticate("test-user", "new-password") is not None
    assert auth.authenticate("test-user", "password123") is None
```

---

## PART 5: Update Existing Endpoints for User Context

**Update `/api/bot/launch`:**
```python
@app.post("/api/bot/launch")
async def launch_bot(request: BotLaunchRequest, token: str = Query(...)):
    """
    Launch bot (requires authentication)

    Bots are now isolated per user
    """
    user = auth_service.get_user_from_token(token)
    if not user:
        return {"success": False, "error": "Invalid token"}

    # Store user as owner of bot in metadata
    # Bot now scoped to this user
    ...
```

---

## TESTING

```bash
# Test auth service
pytest tests/unit/test_auth_service.py -v

# Test JWT in endpoints
pytest tests/unit/test_chat_api_endpoints.py -v -k auth
```

---

## REQUIREMENTS

Install if not already installed:
```bash
pip install pyjwt bcrypt
```

---

## CHECKLIST

- [ ] Create `auth_service.py` with AuthService class
- [ ] Add imports and models to chat_interface_app.py
- [ ] Add `/api/auth/register` endpoint
- [ ] Add `/api/auth/login` endpoint
- [ ] Add `/api/auth/change-password` endpoint
- [ ] Update WebSocket to validate JWT tokens
- [ ] Update endpoints to use user context
- [ ] Create tests in `test_auth_service.py`
- [ ] Tests passing
- [ ] Replace hardcoded token throughout
- [ ] Create completion report

---

## COMPLETION

When finished, create: `.deia/hive/responses/deiasolutions/p0-jwt-authentication-complete.md`

Write:
- JWT authentication implemented
- Users can register and login
- All endpoints now require valid token
- Per-user bot isolation working
- Tests passing
- Ready for rate limiting
