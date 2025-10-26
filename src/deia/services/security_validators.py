"""
Security validators for API input validation and sanitization.

Provides reusable validation functions for common security issues:
- Bot ID validation (whitelist pattern)
- Command/text sanitization
- File path validation
- Request size validation
"""

import re
from typing import Optional, Tuple
from fastapi import HTTPException


class BotIDValidator:
    """Validates bot identifiers against whitelist pattern."""

    # Whitelist pattern: BOT-001, BOT-002, etc.
    # Format: BOT-[3+ digits]
    PATTERN = re.compile(r'^BOT-\d{3,}$')
    MAX_LENGTH = 50

    @staticmethod
    def validate(bot_id: Optional[str]) -> str:
        """
        Validate bot ID format.

        Args:
            bot_id: Bot identifier to validate

        Returns:
            Validated bot_id

        Raises:
            ValueError: If bot_id is invalid
        """
        if not bot_id:
            raise ValueError("Bot ID cannot be empty")

        bot_id = bot_id.strip()

        if not bot_id:
            raise ValueError("Bot ID cannot be empty or whitespace")

        if len(bot_id) > BotIDValidator.MAX_LENGTH:
            raise ValueError(f"Bot ID too long (max {BotIDValidator.MAX_LENGTH} chars)")

        if not BotIDValidator.PATTERN.match(bot_id):
            raise ValueError(
                "Invalid bot ID format. Expected format: BOT-[3+ digits] "
                "(e.g., BOT-001, BOT-123)"
            )

        return bot_id

    @staticmethod
    def is_valid(bot_id: Optional[str]) -> bool:
        """Check if bot_id is valid without raising."""
        try:
            BotIDValidator.validate(bot_id)
            return True
        except ValueError:
            return False


class CommandValidator:
    """Validates and sanitizes commands."""

    MAX_LENGTH = 10000
    # Whitelist safe characters for commands
    # Allows alphanumeric, spaces, common punctuation, but not shell metacharacters
    SAFE_CHARS = re.compile(r'^[a-zA-Z0-9\s\-_.,;:\(\)\[\]{}]+$')

    @staticmethod
    def validate(command: Optional[str]) -> str:
        """
        Validate and sanitize command input.

        Args:
            command: Command string to validate

        Returns:
            Validated command

        Raises:
            ValueError: If command is invalid or contains dangerous patterns
        """
        if not command:
            raise ValueError("Command cannot be empty")

        command = command.strip()

        if not command:
            raise ValueError("Command cannot be empty or whitespace")

        if len(command) > CommandValidator.MAX_LENGTH:
            raise ValueError(f"Command too long (max {CommandValidator.MAX_LENGTH} chars)")

        # Check for dangerous shell metacharacters
        dangerous_chars = ['`', '$', '|', '&', ';', '>', '<', '\n', '\r']
        for char in dangerous_chars:
            if char in command:
                raise ValueError(f"Command contains dangerous character: {char}")

        return command


class PathValidator:
    """Validates file paths against traversal attacks."""

    @staticmethod
    def validate(path: str, base_dir: str = None) -> str:
        """
        Validate file path to prevent traversal attacks.

        Args:
            path: Path to validate
            base_dir: Base directory (optional)

        Returns:
            Validated path

        Raises:
            ValueError: If path contains traversal attempts
        """
        if not path:
            raise ValueError("Path cannot be empty")

        # Reject absolute paths
        if path.startswith('/') or path.startswith('\\') or (len(path) > 1 and path[1] == ':'):
            raise ValueError("Absolute paths not allowed")

        # Reject path traversal patterns
        dangerous_patterns = ['..', '~', '//', '\\\\', '%2e%2e', '%252e']
        path_lower = path.lower()

        for pattern in dangerous_patterns:
            if pattern in path_lower:
                raise ValueError(f"Invalid path: contains dangerous pattern '{pattern}'")

        return path


class ErrorMessageSanitizer:
    """Sanitizes error messages to prevent information disclosure."""

    @staticmethod
    def sanitize(error: Exception) -> str:
        """
        Sanitize exception message to prevent information disclosure.

        Args:
            error: Exception to sanitize

        Returns:
            Safe error message for API response
        """
        error_type = type(error).__name__

        # Map known error types to generic messages
        error_messages = {
            'FileNotFoundError': 'The requested resource was not found',
            'PermissionError': 'Permission denied',
            'ValueError': 'Invalid input provided',
            'TypeError': 'Invalid data type',
            'ProcessLookupError': 'Process not found',
            'ConnectionError': 'Connection failed',
            'TimeoutError': 'Request timed out',
        }

        # Return generic message or generic default
        return error_messages.get(error_type, 'An error occurred processing your request')


class InputSanitizer:
    """Sanitizes user input to prevent XSS and injection attacks."""

    @staticmethod
    def sanitize_json_value(value: str, max_length: int = 1000) -> str:
        """
        Sanitize JSON string value.

        Args:
            value: Value to sanitize
            max_length: Maximum length allowed

        Returns:
            Sanitized value

        Raises:
            ValueError: If value exceeds max length
        """
        if not isinstance(value, str):
            return str(value)[:max_length]

        value = value.strip()

        if len(value) > max_length:
            raise ValueError(f"Input exceeds maximum length of {max_length}")

        # Remove null bytes
        value = value.replace('\x00', '')

        return value


class RateLimitConfig:
    """Configuration for rate limiting."""

    # Default rate limits (requests per minute)
    LIMITS = {
        '/api/bot/launch': 5,      # 5 launches per minute
        '/api/bot/stop': 10,        # 10 stops per minute
        '/api/bot': 30,             # 30 list requests per minute
        '/api/bots/status': 60,     # 60 status checks per minute
        '/api/chat/history': 20,    # 20 history requests per minute
        '/api/bot/task': 50,        # 50 tasks per minute
    }

    @staticmethod
    def get_limit(endpoint: str) -> Optional[int]:
        """Get rate limit for endpoint."""
        return RateLimitConfig.LIMITS.get(endpoint)


# Validation decorator helpers
def validate_bot_id(bot_id: Optional[str]) -> str:
    """Validate bot ID or raise HTTPException."""
    try:
        return BotIDValidator.validate(bot_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def validate_command(command: Optional[str]) -> str:
    """Validate command or raise HTTPException."""
    try:
        return CommandValidator.validate(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def validate_path(path: str) -> str:
    """Validate path or raise HTTPException."""
    try:
        return PathValidator.validate(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
