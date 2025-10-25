"""
Message Validator - Validate and sanitize user messages before sending.

Blocks dangerous patterns, enforces rate limiting, maintains audit trail.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json
import re
from collections import defaultdict


@dataclass
class ValidationResult:
    """Result of message validation."""
    message: str
    valid: bool
    reasons: List[str]
    warnings: List[str]
    rate_limit_ok: bool
    user_id: str
    timestamp: str


class MessageValidator:
    """Validate messages for safety and compliance."""

    def __init__(self, work_dir: Path, max_messages_per_minute: int = 10):
        """Initialize message validator."""
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.audit_log = self.log_dir / "message-validation-audit.jsonl"
        self.max_messages_per_minute = max_messages_per_minute

        # Rate limiting: user_id -> list of (timestamp, message) tuples
        self.user_messages: Dict[str, List[datetime]] = defaultdict(list)

        # Dangerous patterns to block
        self.dangerous_patterns = [
            r"rm\s+-rf",  # Recursive delete
            r":\(\)",  # Unix fork bomb
            r"sudo\s+.*\bpasswd\b",  # Password change via sudo
            r"chmod\s+777",  # World-writable permissions
            r"dd\s+if=",  # Low-level disk operations
            r"--force.*--hard",  # Force destructive operations
            r"DROP\s+TABLE",  # SQL injection
            r"DELETE\s+FROM",  # SQL deletion
            r"exec\(",  # Code execution
            r"eval\(",  # Dynamic code execution
            r"system\(",  # System command execution
        ]

        # Warning patterns (suspicious but not blocked)
        self.warning_patterns = [
            r"curl\s+",  # External network requests
            r"wget\s+",  # Download commands
            r"kill\s+-9",  # Force kill
            r"truncate",  # Destructive operations
            r"shred",  # Secure deletion
        ]

    def validate_message(self, message: str, user_id: str) -> ValidationResult:
        """
        Validate a message for safety.

        Args:
            message: Message to validate
            user_id: User sending message

        Returns:
            ValidationResult with validation details
        """
        reasons = []
        warnings = []
        valid = True

        # Check dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                reasons.append(f"Blocked: {pattern}")
                valid = False

        # Check warning patterns
        for pattern in self.warning_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                warnings.append(f"Warning: {pattern}")

        # Check rate limiting
        rate_limit_ok = self._check_rate_limit(user_id)
        if not rate_limit_ok:
            reasons.append(f"Rate limit exceeded: {self.max_messages_per_minute} messages/minute")
            valid = False

        # Check message length
        if len(message) > 10000:
            warnings.append(f"Message very long: {len(message)} characters")

        result = ValidationResult(
            message=message,
            valid=valid,
            reasons=reasons,
            warnings=warnings,
            rate_limit_ok=rate_limit_ok,
            user_id=user_id,
            timestamp=datetime.now().isoformat()
        )

        self._log_validation(result)
        return result

    def get_audit_trail(self, user_id: Optional[str] = None, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get audit trail of message validation.

        Args:
            user_id: Filter by user (None for all)
            hours: Hours of history

        Returns:
            List of audit entries
        """
        entries = []
        cutoff = datetime.now() - timedelta(hours=hours)

        try:
            with open(self.audit_log, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    if datetime.fromisoformat(entry["timestamp"]) < cutoff:
                        continue
                    if user_id and entry.get("user_id") != user_id:
                        continue
                    entries.append(entry)
        except FileNotFoundError:
            pass

        return entries

    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get validation statistics for a user."""
        audit = self.get_audit_trail(user_id)

        total = len(audit)
        blocked = sum(1 for e in audit if not e.get("valid"))
        warnings = sum(1 for e in audit if e.get("warnings"))
        rate_limited = sum(1 for e in audit if not e.get("rate_limit_ok"))

        return {
            "user_id": user_id,
            "total_messages": total,
            "blocked": blocked,
            "with_warnings": warnings,
            "rate_limited": rate_limited,
            "block_rate": blocked / total if total > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }

    def reset_rate_limit(self, user_id: str) -> None:
        """Reset rate limit for a user."""
        self.user_messages[user_id] = []

    def _check_rate_limit(self, user_id: str) -> bool:
        """Check if user is within rate limit."""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Remove old messages
        self.user_messages[user_id] = [
            ts for ts in self.user_messages[user_id]
            if ts > minute_ago
        ]

        # Check if at limit
        if len(self.user_messages[user_id]) >= self.max_messages_per_minute:
            return False

        # Add current message
        self.user_messages[user_id].append(now)
        return True

    def _log_validation(self, result: ValidationResult) -> None:
        """Log validation result."""
        entry = {
            "timestamp": result.timestamp,
            "user_id": result.user_id,
            "valid": result.valid,
            "blocked_reasons": result.reasons,
            "warnings": result.warnings,
            "rate_limit_ok": result.rate_limit_ok,
            "message_length": len(result.message)
        }

        try:
            with open(self.audit_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[MESSAGE-VALIDATOR] Failed to log: {e}")
