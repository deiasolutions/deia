"""
Authentication & Authorization Framework for DEIA Bot Infrastructure

Manages user authentication, API keys, roles, and permissions.
Integrates with request_validator for comprehensive request security.
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib
import secrets
from pathlib import Path
import logging


class Permission(Enum):
    """System permissions"""
    # Task management
    TASK_SUBMIT = "task:submit"
    TASK_READ = "task:read"
    TASK_CANCEL = "task:cancel"

    # Bot management
    BOT_LIST = "bot:list"
    BOT_READ = "bot:read"
    BOT_LAUNCH = "bot:launch"
    BOT_STOP = "bot:stop"
    BOT_KILL = "bot:kill"

    # System management
    SYS_CONFIG_READ = "sys:config:read"
    SYS_CONFIG_WRITE = "sys:config:write"
    SYS_LOGS_READ = "sys:logs:read"
    SYS_HEALTH = "sys:health"

    # Admin operations
    ADMIN_USERS = "admin:users"
    ADMIN_KEYS = "admin:keys"
    ADMIN_ROLES = "admin:roles"
    ADMIN_RESTART = "admin:restart"


class Role(Enum):
    """User roles"""
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"
    EXTERNAL = "external"
    BOT = "bot"


# Role -> Permissions mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: set(Permission),  # All permissions
    Role.OPERATOR: {
        Permission.TASK_SUBMIT,
        Permission.TASK_READ,
        Permission.BOT_LIST,
        Permission.BOT_READ,
        Permission.BOT_LAUNCH,
        Permission.BOT_STOP,
        Permission.SYS_LOGS_READ,
        Permission.SYS_HEALTH,
        Permission.SYS_CONFIG_READ,
    },
    Role.VIEWER: {
        Permission.TASK_READ,
        Permission.BOT_LIST,
        Permission.BOT_READ,
        Permission.SYS_LOGS_READ,
        Permission.SYS_HEALTH,
    },
    Role.EXTERNAL: {
        Permission.TASK_SUBMIT,
        Permission.TASK_READ,
    },
    Role.BOT: {
        Permission.TASK_SUBMIT,
        Permission.TASK_READ,
        Permission.BOT_LIST,
        Permission.BOT_READ,
    },
}


@dataclass
class APIKey:
    """API Key for authentication"""
    key_id: str
    key_hash: str  # SHA256 hash of the actual key
    user_id: str
    user_name: str
    role: Role
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    is_active: bool = True
    description: str = ""

    def is_expired(self) -> bool:
        """Check if key is expired"""
        if not self.expires_at:
            return False
        return datetime.now() >= self.expires_at

    def to_dict(self) -> Dict:
        """Convert to dictionary (safe - no actual key)"""
        return {
            "key_id": self.key_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "role": self.role.value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "is_active": self.is_active,
            "description": self.description,
        }


@dataclass
class User:
    """User account"""
    user_id: str
    username: str
    role: Role
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    description: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role.value,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active,
            "description": self.description,
        }


@dataclass
class AuthContext:
    """Authentication context for a request"""
    authenticated: bool
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    role: Optional[Role] = None
    permissions: Set[Permission] = field(default_factory=set)
    api_key_id: Optional[str] = None
    error_message: Optional[str] = None


class AuthManager:
    """
    Manages authentication, authorization, and API key validation.

    Features:
    - User management (create, list, delete)
    - Role-based access control (RBAC)
    - API key generation and validation
    - Permission checking
    - Comprehensive audit logging
    """

    def __init__(self, work_dir: Path):
        """Initialize auth manager"""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.auth_log = self.log_dir / "auth.jsonl"
        self.users_file = self.log_dir / "users.jsonl"
        self.keys_file = self.log_dir / "api-keys.jsonl"

        # In-memory stores
        self.users: Dict[str, User] = {}
        self.api_keys: Dict[str, APIKey] = {}  # key_id -> APIKey
        self.key_lookup: Dict[str, str] = {}  # key_hash -> key_id

        self._load_users()
        self._load_api_keys()

        # Create default admin user if no users exist (not just empty dict after loading)
        if not self.users and not self.users_file.exists():
            self._create_default_admin()

    def validate_api_key(self, api_key: str) -> AuthContext:
        """
        Validate an API key and return authentication context.

        Args:
            api_key: The API key string (from Authorization header)

        Returns:
            AuthContext with user info and permissions
        """
        if not api_key or not api_key.startswith("sk-"):
            self._log_auth("api_key_invalid", {"reason": "invalid_format"}, False)
            return AuthContext(
                authenticated=False,
                error_message="Invalid API key format (must start with 'sk-')"
            )

        # Hash the key to look it up
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        if key_hash not in self.key_lookup:
            self._log_auth("api_key_lookup_failed", {"key_hash": key_hash[:8]}, False)
            return AuthContext(
                authenticated=False,
                error_message="API key not found"
            )

        key_id = self.key_lookup[key_hash]
        api_key_obj = self.api_keys.get(key_id)

        if not api_key_obj:
            self._log_auth("api_key_not_found", {"key_id": key_id}, False)
            return AuthContext(
                authenticated=False,
                error_message="API key not found"
            )

        # Check if active and not expired
        if not api_key_obj.is_active:
            self._log_auth("api_key_inactive", {"key_id": key_id, "user_id": api_key_obj.user_id}, False)
            return AuthContext(
                authenticated=False,
                error_message="API key is inactive"
            )

        if api_key_obj.is_expired():
            self._log_auth("api_key_expired", {"key_id": key_id, "user_id": api_key_obj.user_id}, False)
            return AuthContext(
                authenticated=False,
                error_message="API key has expired"
            )

        # Get user
        user = self.users.get(api_key_obj.user_id)
        if not user or not user.is_active:
            self._log_auth("user_inactive", {"user_id": api_key_obj.user_id}, False)
            return AuthContext(
                authenticated=False,
                error_message="User account is inactive"
            )

        # Update last used
        api_key_obj.last_used = datetime.now()
        user.last_login = datetime.now()
        self._save_api_keys()
        self._save_users()

        # Get permissions for user's role
        permissions = ROLE_PERMISSIONS.get(user.role, set())

        self._log_auth(
            "api_key_validated",
            {
                "key_id": key_id,
                "user_id": user.user_id,
                "username": user.username,
                "role": user.role.value,
                "permissions_count": len(permissions)
            },
            True
        )

        return AuthContext(
            authenticated=True,
            user_id=user.user_id,
            user_name=user.username,
            role=user.role,
            permissions=permissions,
            api_key_id=key_id
        )

    def has_permission(self, auth_ctx: AuthContext, permission: Permission) -> bool:
        """Check if user has a specific permission"""
        if not auth_ctx.authenticated:
            return False
        return permission in auth_ctx.permissions

    def require_permission(self, auth_ctx: AuthContext, permission: Permission) -> Tuple[bool, str]:
        """
        Check if user has permission and return result with message.

        Returns:
            (has_permission, message)
        """
        if not auth_ctx.authenticated:
            return False, "Not authenticated"

        if permission not in auth_ctx.permissions:
            self._log_auth(
                "permission_denied",
                {
                    "user_id": auth_ctx.user_id,
                    "permission": permission.value
                },
                False
            )
            return False, f"Permission denied: {permission.value}"

        return True, "OK"

    def create_api_key(self, user_id: str, description: str = "", days_valid: int = 365) -> Optional[str]:
        """
        Create a new API key for a user.

        Args:
            user_id: User ID
            description: Key description/purpose
            days_valid: Days until key expires

        Returns:
            The actual API key (only returned once, must be saved by caller)
        """
        user = self.users.get(user_id)
        if not user:
            self._log_auth("api_key_create_failed", {"reason": "user_not_found", "user_id": user_id}, False)
            return None

        # Generate new key
        actual_key = f"sk-{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(actual_key.encode()).hexdigest()
        key_id = f"key-{secrets.token_hex(8)}"

        # Create key object
        expires_at = datetime.now() + timedelta(days=days_valid) if days_valid > 0 else None
        api_key = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            user_id=user_id,
            user_name=user.username,
            role=user.role,
            created_at=datetime.now(),
            expires_at=expires_at,
            description=description,
        )

        # Store
        self.api_keys[key_id] = api_key
        self.key_lookup[key_hash] = key_id
        self._save_api_keys()

        self._log_auth(
            "api_key_created",
            {
                "key_id": key_id,
                "user_id": user_id,
                "username": user.username,
                "description": description
            },
            True
        )

        return actual_key  # Return the actual key (only time it's shown)

    def create_user(self, username: str, role: Role, description: str = "") -> Optional[User]:
        """Create a new user"""
        user_id = f"user-{secrets.token_hex(8)}"

        user = User(
            user_id=user_id,
            username=username,
            role=role,
            created_at=datetime.now(),
            description=description,
        )

        self.users[user_id] = user
        self._save_users()

        self._log_auth(
            "user_created",
            {
                "user_id": user_id,
                "username": username,
                "role": role.value
            },
            True
        )

        return user

    def list_users(self) -> List[Dict]:
        """List all active users"""
        return [u.to_dict() for u in self.users.values() if u.is_active]

    def list_api_keys(self, user_id: Optional[str] = None) -> List[Dict]:
        """List API keys (optionally filtered by user)"""
        keys = []
        for key in self.api_keys.values():
            if user_id and key.user_id != user_id:
                continue
            if key.is_active:
                keys.append(key.to_dict())
        return keys

    def deactivate_api_key(self, key_id: str) -> bool:
        """Deactivate an API key"""
        key = self.api_keys.get(key_id)
        if not key:
            return False

        key.is_active = False
        self._save_api_keys()

        self._log_auth(
            "api_key_deactivated",
            {"key_id": key_id, "user_id": key.user_id},
            True
        )

        return True

    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user account"""
        user = self.users.get(user_id)
        if not user:
            return False

        user.is_active = False
        self._save_users()

        # Deactivate all their API keys
        for key in self.api_keys.values():
            if key.user_id == user_id:
                key.is_active = False
        self._save_api_keys()

        self._log_auth(
            "user_deactivated",
            {"user_id": user_id, "username": user.username},
            True
        )

        return True

    def _create_default_admin(self):
        """Create default admin user"""
        admin = User(
            user_id="user-admin",
            username="admin",
            role=Role.ADMIN,
            created_at=datetime.now(),
            description="Default admin user",
        )
        self.users["user-admin"] = admin
        self._save_users()

    def _load_users(self):
        """Load users from disk"""
        if not self.users_file.exists():
            return

        try:
            with open(self.users_file) as f:
                for line in f:
                    data = json.loads(line)
                    user = User(
                        user_id=data["user_id"],
                        username=data["username"],
                        role=Role(data["role"]),
                        created_at=datetime.fromisoformat(data["created_at"]),
                        last_login=datetime.fromisoformat(data["last_login"]) if data.get("last_login") else None,
                        is_active=data["is_active"],
                        description=data.get("description", ""),
                    )
                    self.users[user.user_id] = user
        except Exception as e:
            logging.error(f"Failed to load users: {e}")

    def _save_users(self):
        """Save users to disk"""
        try:
            with open(self.users_file, "w") as f:
                for user in self.users.values():
                    data = user.to_dict()
                    f.write(json.dumps(data) + "\n")
        except Exception as e:
            logging.error(f"Failed to save users: {e}")

    def _load_api_keys(self):
        """Load API keys from disk"""
        if not self.keys_file.exists():
            return

        try:
            with open(self.keys_file) as f:
                for line in f:
                    data = json.loads(line)
                    key = APIKey(
                        key_id=data["key_id"],
                        key_hash=data["key_hash"],
                        user_id=data["user_id"],
                        user_name=data["user_name"],
                        role=Role(data["role"]),
                        created_at=datetime.fromisoformat(data["created_at"]),
                        expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
                        last_used=datetime.fromisoformat(data["last_used"]) if data.get("last_used") else None,
                        is_active=data["is_active"],
                        description=data.get("description", ""),
                    )
                    self.api_keys[key.key_id] = key
                    self.key_lookup[key.key_hash] = key.key_id
        except Exception as e:
            logging.error(f"Failed to load API keys: {e}")

    def _save_api_keys(self):
        """Save API keys to disk"""
        try:
            with open(self.keys_file, "w") as f:
                for key in self.api_keys.values():
                    data = key.to_dict()
                    f.write(json.dumps(data) + "\n")
        except Exception as e:
            logging.error(f"Failed to save API keys: {e}")

    def _log_auth(self, event: str, details: Dict, success: bool):
        """Log authentication event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "success": success,
            "details": details,
        }
        try:
            with open(self.auth_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logging.error(f"Failed to log auth event: {e}")
