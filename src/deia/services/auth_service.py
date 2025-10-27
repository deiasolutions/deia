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
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None

    def get_user(self, username: str) -> Optional[Dict]:
        """
        Get user information (without password hash).

        Args:
            username: Username

        Returns:
            User info dict if exists, None otherwise
        """
        user = self.users.get(username)
        if user:
            # Don't return password hash
            return {
                "username": user["username"],
                "created_at": user["created_at"]
            }
        return None

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        Change user password.

        Args:
            username: Username
            old_password: Current password
            new_password: New password

        Returns:
            True if successful, False otherwise
        """
        user = self.users.get(username)
        if not user:
            logger.warning(f"User {username} not found for password change")
            return False

        # Verify old password
        if not bcrypt.checkpw(old_password.encode(), user["password_hash"].encode()):
            logger.warning(f"Password change failed: invalid old password for {username}")
            return False

        # Hash and update new password
        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        user["password_hash"] = new_hash

        logger.info(f"Password changed for user {username}")
        return True

    def list_users(self) -> list:
        """
        List all users (without password hashes).

        Returns:
            List of user dicts
        """
        return [
            {
                "username": user["username"],
                "created_at": user["created_at"]
            }
            for user in self.users.values()
        ]
