"""
Tests for AuthService JWT authentication module
"""

import pytest
import jwt
from datetime import datetime, timedelta
from deia.services.auth_service import AuthService


class TestAuthService:
    """Test AuthService class"""

    @pytest.fixture
    def auth_service_instance(self):
        """Create a fresh AuthService instance for testing"""
        return AuthService(secret_key="test-secret-key", token_expiry_hours=24)

    def test_initialization(self, auth_service_instance):
        """Test AuthService initializes with default user"""
        assert auth_service_instance.secret_key == "test-secret-key"
        assert auth_service_instance.token_expiry_hours == 24
        assert auth_service_instance.algorithm == "HS256"
        # Should have dev-user created by default
        assert "dev-user" in auth_service_instance.users

    def test_register_new_user(self, auth_service_instance):
        """Test registering a new user"""
        success = auth_service_instance.register_user("testuser", "password123")
        assert success is True
        assert "testuser" in auth_service_instance.users

    def test_register_duplicate_user_fails(self, auth_service_instance):
        """Test that registering duplicate username fails"""
        auth_service_instance.register_user("testuser", "password123")
        success = auth_service_instance.register_user("testuser", "password456")
        assert success is False

    def test_authenticate_valid_credentials(self, auth_service_instance):
        """Test authentication with valid credentials"""
        auth_service_instance.register_user("testuser", "password123")
        token = auth_service_instance.authenticate("testuser", "password123")
        assert token is not None
        assert isinstance(token, str)

    def test_authenticate_invalid_password(self, auth_service_instance):
        """Test authentication fails with wrong password"""
        auth_service_instance.register_user("testuser", "password123")
        token = auth_service_instance.authenticate("testuser", "wrongpassword")
        assert token is None

    def test_authenticate_nonexistent_user(self, auth_service_instance):
        """Test authentication fails for nonexistent user"""
        token = auth_service_instance.authenticate("nonexistent", "password")
        assert token is None

    def test_authenticate_default_user(self, auth_service_instance):
        """Test authenticating with default dev-user"""
        token = auth_service_instance.authenticate("dev-user", "dev-password")
        assert token is not None
        assert isinstance(token, str)

    def test_validate_token_valid(self, auth_service_instance):
        """Test validating a valid JWT token"""
        auth_service_instance.register_user("testuser", "password123")
        token = auth_service_instance.authenticate("testuser", "password123")

        claims = auth_service_instance.validate_token(token)
        assert claims is not None
        assert claims["username"] == "testuser"
        assert claims["user_id"] == "testuser"
        assert "iat" in claims
        assert "exp" in claims

    def test_validate_token_invalid(self, auth_service_instance):
        """Test validating an invalid token"""
        claims = auth_service_instance.validate_token("invalid.token.here")
        assert claims is None

    def test_validate_token_empty(self, auth_service_instance):
        """Test validating empty token"""
        claims = auth_service_instance.validate_token("")
        assert claims is None

    def test_token_expiry(self, auth_service_instance):
        """Test that tokens include expiry time"""
        token = auth_service_instance.authenticate("dev-user", "dev-password")
        claims = auth_service_instance.validate_token(token)

        assert "exp" in claims
        # Token should be valid for 24 hours (86400 seconds)
        # JWT timestamps are integers (Unix time), not datetime objects
        exp_time = claims["exp"] if isinstance(claims["exp"], int) else int(claims["exp"].timestamp())
        iat_time = claims["iat"] if isinstance(claims["iat"], int) else int(claims["iat"].timestamp())
        duration = exp_time - iat_time
        # Allow 5 second margin
        assert 86395 <= duration <= 86405

    def test_get_user_existing(self, auth_service_instance):
        """Test getting existing user info"""
        auth_service_instance.register_user("testuser", "password123")
        user = auth_service_instance.get_user("testuser")

        assert user is not None
        assert user["username"] == "testuser"
        assert "created_at" in user
        # Password hash should not be returned
        assert "password_hash" not in user

    def test_get_user_nonexistent(self, auth_service_instance):
        """Test getting nonexistent user returns None"""
        user = auth_service_instance.get_user("nonexistent")
        assert user is None

    def test_change_password_valid(self, auth_service_instance):
        """Test changing user password"""
        auth_service_instance.register_user("testuser", "oldpassword")

        # Old password should work
        token1 = auth_service_instance.authenticate("testuser", "oldpassword")
        assert token1 is not None

        # Change password
        success = auth_service_instance.change_password(
            "testuser", "oldpassword", "newpassword"
        )
        assert success is True

        # Old password should not work
        token2 = auth_service_instance.authenticate("testuser", "oldpassword")
        assert token2 is None

        # New password should work
        token3 = auth_service_instance.authenticate("testuser", "newpassword")
        assert token3 is not None

    def test_change_password_invalid_old(self, auth_service_instance):
        """Test changing password fails with wrong old password"""
        auth_service_instance.register_user("testuser", "correctpassword")

        success = auth_service_instance.change_password(
            "testuser", "wrongpassword", "newpassword"
        )
        assert success is False

    def test_change_password_nonexistent_user(self, auth_service_instance):
        """Test changing password for nonexistent user fails"""
        success = auth_service_instance.change_password(
            "nonexistent", "oldpass", "newpass"
        )
        assert success is False

    def test_list_users(self, auth_service_instance):
        """Test listing all users"""
        auth_service_instance.register_user("user1", "pass1")
        auth_service_instance.register_user("user2", "pass2")

        users = auth_service_instance.list_users()
        usernames = [u["username"] for u in users]

        # Should have dev-user + user1 + user2
        assert "dev-user" in usernames
        assert "user1" in usernames
        assert "user2" in usernames

        # No password hashes should be in returned list
        for user in users:
            assert "password_hash" not in user
            assert "created_at" in user

    def test_token_contains_correct_claims(self, auth_service_instance):
        """Test that JWT token contains correct claims"""
        auth_service_instance.register_user("testuser", "password123")
        token = auth_service_instance.authenticate("testuser", "password123")

        # Decode without verification to check claims
        decoded = jwt.decode(
            token,
            auth_service_instance.secret_key,
            algorithms=[auth_service_instance.algorithm]
        )

        assert decoded["username"] == "testuser"
        assert decoded["user_id"] == "testuser"
        assert "iat" in decoded
        assert "exp" in decoded

    def test_multiple_users_isolated(self, auth_service_instance):
        """Test that multiple users don't interfere with each other"""
        auth_service_instance.register_user("user1", "pass1")
        auth_service_instance.register_user("user2", "pass2")

        token1 = auth_service_instance.authenticate("user1", "pass1")
        token2 = auth_service_instance.authenticate("user2", "pass2")

        claims1 = auth_service_instance.validate_token(token1)
        claims2 = auth_service_instance.validate_token(token2)

        assert claims1["username"] == "user1"
        assert claims2["username"] == "user2"
        assert claims1["user_id"] != claims2["user_id"]
