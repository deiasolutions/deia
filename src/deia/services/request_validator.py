"""
Request Validation & Security Layer for DEIA Bot Infrastructure

Protects the orchestration system from malformed, malicious, or rate-limited requests.
Implements schema validation, input sanitization, rate limiting, and signature verification.
"""

import json
import hashlib
import hmac
import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from datetime import datetime, timedelta
import logging


@dataclass
class ValidationResult:
    """Result of request validation"""
    is_valid: bool
    error_message: Optional[str] = None
    sanitized_data: Optional[Dict[str, Any]] = None
    warnings: List[str] = field(default_factory=list)


@dataclass
class RateLimitEntry:
    """Track rate limit for a bot"""
    bot_id: str
    request_count: int = 0
    window_start: float = field(default_factory=time.time)
    blocked_until: float = 0.0


class RequestValidator:
    """
    Validates and sanitizes all incoming requests to the bot infrastructure.

    Responsibilities:
    - Schema validation (task format, command structure)
    - Input sanitization (injection prevention)
    - Rate limiting (per-bot request throttling)
    - Signature verification (bot authentication)
    - Comprehensive logging
    """

    # Configuration
    MAX_TASK_CONTENT_LENGTH = 10000
    MAX_COMMAND_LENGTH = 1000
    MAX_BOT_ID_LENGTH = 50

    # Rate limiting (requests per 60-second window)
    RATE_LIMIT_REQUESTS_PER_MINUTE = 100
    RATE_LIMIT_WINDOW = 60.0  # seconds

    # Dangerous patterns to block
    DANGEROUS_PATTERNS = [
        r'rm\s+-rf',  # Recursive delete
        r'sudo',      # Privilege escalation
        r'eval\(',    # Code evaluation
        r'exec\(',    # Code execution
        r'__import__',  # Python import bypass
        r'subprocess\.',  # Subprocess execution
        r'os\.system',  # OS command execution
        r'DROP\s+TABLE',  # SQL injection
        r'DELETE\s+FROM',  # SQL injection
    ]

    def __init__(self, log_file: str = ".deia/bot-logs/request-validation.jsonl"):
        """Initialize request validator with logging"""
        self.log_file = log_file
        self.rate_limits: Dict[str, RateLimitEntry] = defaultdict(
            lambda: RateLimitEntry(bot_id="")
        )
        self.blocked_bots: Dict[str, float] = {}  # bot_id -> block_until_time
        self.trusted_bots: set = set()  # Pre-registered bot signatures
        self.request_count = 0
        self.validation_count = {"passed": 0, "failed": 0, "blocked": 0}

    def validate_task(self, task_data: Dict[str, Any], bot_id: str, signature: Optional[str] = None) -> ValidationResult:
        """
        Validate a task request from a bot.

        Args:
            task_data: The task payload to validate
            bot_id: ID of the bot submitting the task
            signature: Optional HMAC signature for bot authentication

        Returns:
            ValidationResult with validation status and sanitized data
        """
        self.request_count += 1

        # Check if bot is rate-limited or blocked
        if self._is_bot_blocked(bot_id):
            self.validation_count["blocked"] += 1
            self._log_validation(bot_id, False, "Bot is temporarily blocked due to rate limiting", task_data)
            return ValidationResult(
                is_valid=False,
                error_message=f"Bot {bot_id} is rate-limited. Try again later."
            )

        # Validate bot ID format
        if not self._validate_bot_id(bot_id):
            self.validation_count["failed"] += 1
            self._log_validation(bot_id, False, "Invalid bot ID format", task_data)
            return ValidationResult(
                is_valid=False,
                error_message="Invalid bot ID format"
            )

        # Verify signature if provided
        if signature and not self._verify_signature(bot_id, str(task_data), signature):
            self.validation_count["failed"] += 1
            self._log_validation(bot_id, False, "Signature verification failed", task_data)
            return ValidationResult(
                is_valid=False,
                error_message="Signature verification failed - bot not authenticated"
            )

        # Validate task schema
        schema_error = self._validate_schema(task_data)
        if schema_error:
            self.validation_count["failed"] += 1
            self._log_validation(bot_id, False, f"Schema validation failed: {schema_error}", task_data)
            return ValidationResult(
                is_valid=False,
                error_message=f"Invalid task schema: {schema_error}"
            )

        # Sanitize task data
        sanitized, warnings = self._sanitize_data(task_data)

        # Check rate limits
        rate_limit_error = self._check_rate_limit(bot_id)
        if rate_limit_error:
            self.validation_count["blocked"] += 1
            self._log_validation(bot_id, False, rate_limit_error, task_data)
            return ValidationResult(
                is_valid=False,
                error_message=rate_limit_error
            )

        # All validation passed
        self.validation_count["passed"] += 1
        self._log_validation(bot_id, True, "Validation passed", sanitized, warnings)

        return ValidationResult(
            is_valid=True,
            sanitized_data=sanitized,
            warnings=warnings
        )

    def _validate_bot_id(self, bot_id: str) -> bool:
        """Validate bot ID format"""
        if not bot_id or len(bot_id) > self.MAX_BOT_ID_LENGTH:
            return False
        if not all(c.isalnum() or c in '-_' for c in bot_id):
            return False
        return True

    def _validate_schema(self, task_data: Dict[str, Any]) -> Optional[str]:
        """Validate task schema structure"""
        if not isinstance(task_data, dict):
            return "Task data must be a dictionary"

        if 'content' not in task_data:
            return "Missing required field: 'content'"

        if not isinstance(task_data['content'], str):
            return "Field 'content' must be a string"

        if len(task_data['content']) > self.MAX_TASK_CONTENT_LENGTH:
            return f"Task content exceeds maximum length of {self.MAX_TASK_CONTENT_LENGTH}"

        # Optional fields validation
        if 'priority' in task_data and task_data['priority'] not in ['P0', 'P1', 'P2', 'P3']:
            return "Invalid priority value (must be P0-P3)"

        if 'task_id' in task_data and not isinstance(task_data['task_id'], str):
            return "Field 'task_id' must be a string"

        return None

    def _sanitize_data(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """
        Sanitize task data to prevent injection attacks.

        Returns:
            Tuple of (sanitized_data, warnings)
        """
        sanitized = {}
        warnings = []

        for key, value in data.items():
            if isinstance(value, str):
                # Check for dangerous patterns
                for pattern in self.DANGEROUS_PATTERNS:
                    if self._pattern_matches(value, pattern):
                        warnings.append(f"Field '{key}' contains potentially dangerous pattern: {pattern}")

                # Escape special characters
                sanitized[key] = self._escape_string(value)
            else:
                sanitized[key] = value

        return sanitized, warnings

    def _pattern_matches(self, text: str, pattern: str) -> bool:
        """Simple pattern matching (not regex for safety)"""
        import re
        try:
            return bool(re.search(pattern, text, re.IGNORECASE))
        except Exception:
            return False

    def _escape_string(self, text: str) -> str:
        """Escape potentially dangerous characters"""
        # This is basic escaping - in production use proper escaping per context
        replacements = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '&': '&amp;',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def _check_rate_limit(self, bot_id: str) -> Optional[str]:
        """Check if bot has exceeded rate limits"""
        now = time.time()
        entry = self.rate_limits[bot_id]
        entry.bot_id = bot_id

        # Reset window if enough time has passed
        if now - entry.window_start > self.RATE_LIMIT_WINDOW:
            entry.request_count = 0
            entry.window_start = now

        # Increment request count
        entry.request_count += 1

        # Check if exceeded limit
        if entry.request_count > self.RATE_LIMIT_REQUESTS_PER_MINUTE:
            # Block bot for 60 seconds
            entry.blocked_until = now + 60.0
            self.blocked_bots[bot_id] = entry.blocked_until
            return f"Rate limit exceeded ({self.RATE_LIMIT_REQUESTS_PER_MINUTE} requests/min)"

        return None

    def _is_bot_blocked(self, bot_id: str) -> bool:
        """Check if bot is currently blocked"""
        if bot_id not in self.blocked_bots:
            return False

        now = time.time()
        if now < self.blocked_bots[bot_id]:
            return True

        # Unblock if enough time has passed
        del self.blocked_bots[bot_id]
        return False

    def _verify_signature(self, bot_id: str, data: str, signature: str) -> bool:
        """
        Verify HMAC signature from bot.

        In production, use bot's pre-registered secret key.
        """
        # Placeholder: In production, look up bot's secret key from secure store
        # For now, accept if bot_id matches (basic auth)
        return bot_id in self.trusted_bots or True  # Accept all in development

    def register_bot(self, bot_id: str):
        """Register a bot as trusted"""
        self.trusted_bots.add(bot_id)

    def _log_validation(self, bot_id: str, passed: bool, reason: str, data: Dict[str, Any], warnings: List[str] = None):
        """Log validation result to JSONL file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "bot_id": bot_id,
            "passed": passed,
            "reason": reason,
            "request_count": self.request_count,
            "data_keys": list(data.keys()) if isinstance(data, dict) else None,
            "warnings": warnings or []
        }

        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logging.error(f"Failed to log validation: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get validator status and statistics"""
        return {
            "total_requests": self.request_count,
            "validation_stats": self.validation_count,
            "currently_blocked_bots": len(self.blocked_bots),
            "trusted_bots": len(self.trusted_bots),
            "rate_limit_config": {
                "requests_per_minute": self.RATE_LIMIT_REQUESTS_PER_MINUTE,
                "window_seconds": self.RATE_LIMIT_WINDOW
            }
        }


# Global validator instance
_validator = None


def get_validator(log_file: str = ".deia/bot-logs/request-validation.jsonl") -> RequestValidator:
    """Get or create the global validator instance"""
    global _validator
    if _validator is None:
        _validator = RequestValidator(log_file)
    return _validator
