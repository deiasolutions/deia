"""Unit tests for AuthManager service"""

import pytest
from pathlib import Path
from src.deia.services.auth_manager import (
    AuthManager, Permission, Role, User, APIKey, AuthContext
)


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory"""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def auth_manager(temp_work_dir):
    """Create AuthManager instance"""
    return AuthManager(temp_work_dir)


class TestUserManagement:
    """Test user creation and management"""

    def test_default_admin_created(self, auth_manager):
        """Test default admin user created"""
        users = auth_manager.list_users()
        assert len(users) > 0
        admin = [u for u in users if u["username"] == "admin"]
        assert len(admin) == 1
        assert admin[0]["role"] == "admin"

    def test_create_user(self, auth_manager):
        """Test creating a new user"""
        user = auth_manager.create_user("operator1", Role.OPERATOR, "Test operator")
        assert user is not None
        assert user.username == "operator1"
        assert user.role == Role.OPERATOR
        assert user.is_active

    def test_create_multiple_users(self, auth_manager):
        """Test creating multiple users"""
        auth_manager.create_user("op1", Role.OPERATOR)
        auth_manager.create_user("op2", Role.OPERATOR)
        auth_manager.create_user("viewer1", Role.VIEWER)

        users = auth_manager.list_users()
        assert len(users) >= 3

    def test_deactivate_user(self, auth_manager):
        """Test deactivating a user"""
        user = auth_manager.create_user("temp_user", Role.VIEWER)
        assert user.is_active

        success = auth_manager.deactivate_user(user.user_id)
        assert success

        users = auth_manager.list_users()
        inactive_users = [u for u in users if u["username"] == "temp_user"]
        assert len(inactive_users) == 0


class TestAPIKeyGeneration:
    """Test API key generation and management"""

    def test_create_api_key(self, auth_manager):
        """Test creating an API key"""
        user = auth_manager.create_user("keytest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id, "Test key")

        assert actual_key is not None
        assert actual_key.startswith("sk-")

    def test_list_api_keys(self, auth_manager):
        """Test listing API keys"""
        user = auth_manager.create_user("keyuser", Role.OPERATOR)
        auth_manager.create_api_key(user.user_id, "Key 1")
        auth_manager.create_api_key(user.user_id, "Key 2")

        keys = auth_manager.list_api_keys(user.user_id)
        assert len(keys) >= 2

    def test_api_key_format(self, auth_manager):
        """Test API key has correct format"""
        user = auth_manager.create_user("formattest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)

        assert actual_key.startswith("sk-")
        assert len(actual_key) > 10

    def test_deactivate_api_key(self, auth_manager):
        """Test deactivating an API key"""
        user = auth_manager.create_user("deactivate_test", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id, "To deactivate")

        # Find the key ID
        keys = auth_manager.list_api_keys(user.user_id)
        assert len(keys) > 0
        key_id = keys[0]["key_id"]

        # Deactivate it
        success = auth_manager.deactivate_api_key(key_id)
        assert success

        # Try to use it - should fail
        auth_ctx = auth_manager.validate_api_key(actual_key)
        assert not auth_ctx.authenticated


class TestAPIKeyValidation:
    """Test API key validation and authentication"""

    def test_valid_api_key(self, auth_manager):
        """Test validating a valid API key"""
        user = auth_manager.create_user("validtest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)

        assert auth_ctx.authenticated
        assert auth_ctx.user_id == user.user_id
        assert auth_ctx.user_name == "validtest"
        assert auth_ctx.role == Role.OPERATOR

    def test_invalid_api_key_format(self, auth_manager):
        """Test rejecting invalid format"""
        auth_ctx = auth_manager.validate_api_key("invalid-format")
        assert not auth_ctx.authenticated

    def test_invalid_api_key(self, auth_manager):
        """Test rejecting non-existent API key"""
        auth_ctx = auth_manager.validate_api_key("sk-nonexistent1234567890123456789")
        assert not auth_ctx.authenticated

    def test_expired_api_key(self, auth_manager):
        """Test expired key is rejected"""
        from datetime import datetime, timedelta

        user = auth_manager.create_user("expiredtest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id, days_valid=0)

        # Manually expire the key
        keys = auth_manager.list_api_keys(user.user_id)
        key_id = keys[0]["key_id"]
        api_key_obj = auth_manager.api_keys[key_id]
        api_key_obj.expires_at = datetime.now() - timedelta(seconds=1)

        auth_ctx = auth_manager.validate_api_key(actual_key)
        assert not auth_ctx.authenticated

    def test_inactive_api_key(self, auth_manager):
        """Test inactive key is rejected"""
        user = auth_manager.create_user("inactivetest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)

        # Deactivate and try to use
        keys = auth_manager.list_api_keys(user.user_id)
        key_id = keys[0]["key_id"]
        auth_manager.deactivate_api_key(key_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)
        assert not auth_ctx.authenticated

    def test_inactive_user(self, auth_manager):
        """Test key from inactive user is rejected"""
        user = auth_manager.create_user("inactiveuser", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)

        # Deactivate user and try to use key
        auth_manager.deactivate_user(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)
        assert not auth_ctx.authenticated

    def test_last_used_updated(self, auth_manager):
        """Test last_used timestamp is updated"""
        user = auth_manager.create_user("lastusedtest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)

        keys_before = auth_manager.list_api_keys(user.user_id)
        assert keys_before[0]["last_used"] is None

        # Use the key
        auth_manager.validate_api_key(actual_key)

        keys_after = auth_manager.list_api_keys(user.user_id)
        assert keys_after[0]["last_used"] is not None


class TestRolePermissions:
    """Test role-based permissions"""

    def test_admin_has_all_permissions(self, auth_manager):
        """Test admin role has all permissions"""
        user = auth_manager.create_user("admin2", Role.ADMIN)
        actual_key = auth_manager.create_api_key(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)

        # Admin should have all permissions
        for permission in Permission:
            assert permission in auth_ctx.permissions

    def test_operator_limited_permissions(self, auth_manager):
        """Test operator role has limited permissions"""
        user = auth_manager.create_user("op", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)

        # Operator should not have all admin permissions
        assert Permission.ADMIN_USERS not in auth_ctx.permissions
        assert Permission.ADMIN_KEYS not in auth_ctx.permissions

        # But should have some task permissions
        assert Permission.TASK_SUBMIT in auth_ctx.permissions
        assert Permission.TASK_READ in auth_ctx.permissions

    def test_viewer_read_only(self, auth_manager):
        """Test viewer role is read-only"""
        user = auth_manager.create_user("viewer", Role.VIEWER)
        actual_key = auth_manager.create_api_key(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)

        # Viewer should have read permissions
        assert Permission.TASK_READ in auth_ctx.permissions
        assert Permission.BOT_READ in auth_ctx.permissions

        # But not write/admin permissions
        assert Permission.TASK_SUBMIT not in auth_ctx.permissions
        assert Permission.ADMIN_USERS not in auth_ctx.permissions

    def test_external_limited(self, auth_manager):
        """Test external role has limited task permissions"""
        user = auth_manager.create_user("external", Role.EXTERNAL)
        actual_key = auth_manager.create_api_key(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)

        # External should only have task permissions
        assert Permission.TASK_SUBMIT in auth_ctx.permissions
        assert Permission.TASK_READ in auth_ctx.permissions

        # No bot or system permissions
        assert Permission.BOT_LIST not in auth_ctx.permissions
        assert Permission.SYS_CONFIG_READ not in auth_ctx.permissions

    def test_bot_role(self, auth_manager):
        """Test bot role permissions"""
        user = auth_manager.create_user("bot1", Role.BOT)
        actual_key = auth_manager.create_api_key(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)

        # Bot should have task and bot listing permissions
        assert Permission.TASK_SUBMIT in auth_ctx.permissions
        assert Permission.BOT_LIST in auth_ctx.permissions

        # But not admin permissions
        assert Permission.ADMIN_USERS not in auth_ctx.permissions


class TestPermissionChecking:
    """Test permission checking methods"""

    def test_has_permission(self, auth_manager):
        """Test has_permission check"""
        user = auth_manager.create_user("permtest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)

        assert auth_manager.has_permission(auth_ctx, Permission.TASK_SUBMIT)
        assert not auth_manager.has_permission(auth_ctx, Permission.ADMIN_USERS)

    def test_require_permission_granted(self, auth_manager):
        """Test require_permission with granted permission"""
        user = auth_manager.create_user("reqtest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)

        success, message = auth_manager.require_permission(auth_ctx, Permission.TASK_SUBMIT)
        assert success
        assert message == "OK"

    def test_require_permission_denied(self, auth_manager):
        """Test require_permission with denied permission"""
        user = auth_manager.create_user("denytest", Role.VIEWER)
        actual_key = auth_manager.create_api_key(user.user_id)

        auth_ctx = auth_manager.validate_api_key(actual_key)

        success, message = auth_manager.require_permission(auth_ctx, Permission.TASK_SUBMIT)
        assert not success
        assert "Permission denied" in message

    def test_require_permission_not_authenticated(self, auth_manager):
        """Test require_permission on unauthenticated context"""
        auth_ctx = AuthContext(authenticated=False)

        success, message = auth_manager.require_permission(auth_ctx, Permission.TASK_SUBMIT)
        assert not success
        assert "Not authenticated" in message


class TestPersistence:
    """Test user and key persistence"""

    def test_users_persisted(self, temp_work_dir):
        """Test users are persisted to disk"""
        auth1 = AuthManager(temp_work_dir)
        auth1.create_user("persist_user", Role.OPERATOR)

        # Create new instance - should load from disk
        auth2 = AuthManager(temp_work_dir)
        users = auth2.list_users()

        persist_users = [u for u in users if u["username"] == "persist_user"]
        assert len(persist_users) == 1

    def test_api_keys_persisted(self, temp_work_dir):
        """Test API keys are persisted to disk"""
        auth1 = AuthManager(temp_work_dir)
        user = auth1.create_user("key_persist_user", Role.OPERATOR)
        actual_key = auth1.create_api_key(user.user_id, "Persistent key")

        # Verify key file exists
        key_file = temp_work_dir / ".deia" / "bot-logs" / "api-keys.jsonl"
        assert key_file.exists()

        # Verify key data was written
        with open(key_file) as f:
            lines = f.readlines()
        assert len(lines) > 0


class TestAuthLogging:
    """Test authentication logging"""

    def test_auth_log_created(self, auth_manager, temp_work_dir):
        """Test auth log file is created"""
        user = auth_manager.create_user("logtest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)
        auth_manager.validate_api_key(actual_key)

        log_file = temp_work_dir / ".deia" / "bot-logs" / "auth.jsonl"
        assert log_file.exists()

    def test_auth_events_logged(self, auth_manager, temp_work_dir):
        """Test auth events are logged"""
        user = auth_manager.create_user("eventtest", Role.OPERATOR)
        actual_key = auth_manager.create_api_key(user.user_id)
        auth_manager.validate_api_key(actual_key)

        log_file = temp_work_dir / ".deia" / "bot-logs" / "auth.jsonl"
        with open(log_file) as f:
            lines = f.readlines()

        # Should have multiple log entries
        assert len(lines) >= 2
        assert "user_created" in lines[0] or "api_key_created" in lines[0]


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_create_key_nonexistent_user(self, auth_manager):
        """Test creating key for non-existent user"""
        key = auth_manager.create_api_key("nonexistent_user")
        assert key is None

    def test_deactivate_nonexistent_user(self, auth_manager):
        """Test deactivating non-existent user"""
        success = auth_manager.deactivate_user("nonexistent")
        assert not success

    def test_deactivate_nonexistent_key(self, auth_manager):
        """Test deactivating non-existent key"""
        success = auth_manager.deactivate_api_key("nonexistent_key")
        assert not success

    def test_empty_api_key(self, auth_manager):
        """Test validating empty API key"""
        auth_ctx = auth_manager.validate_api_key("")
        assert not auth_ctx.authenticated

    def test_none_api_key(self, auth_manager):
        """Test validating None API key"""
        auth_ctx = auth_manager.validate_api_key(None)
        assert not auth_ctx.authenticated
