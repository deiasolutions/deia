"""Tests for MessageValidator service."""

import pytest
from pathlib import Path
from datetime import datetime
import sys
import time

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.deia.services.message_validator import MessageValidator


@pytest.fixture
def validator(tmp_path):
    """Provide MessageValidator instance."""
    return MessageValidator(tmp_path, max_messages_per_minute=5)


class TestDangerousPatterns:
    """Tests for dangerous pattern detection."""

    def test_block_rm_rf(self, validator):
        """Test blocking rm -rf command."""
        result = validator.validate_message("rm -rf /", "user1")

        assert not result.valid
        assert len(result.reasons) > 0

    def test_block_fork_bomb(self, validator):
        """Test blocking fork bomb."""
        result = validator.validate_message(":() { :| : & }; :", "user1")

        assert not result.valid

    def test_block_sql_injection(self, validator):
        """Test blocking SQL injection."""
        result = validator.validate_message("DROP TABLE users;", "user1")

        assert not result.valid

    def test_block_code_execution(self, validator):
        """Test blocking code execution."""
        result = validator.validate_message("exec(malicious_code)", "user1")

        assert not result.valid

    def test_allow_safe_message(self, validator):
        """Test allowing safe message."""
        result = validator.validate_message("Hello, how can I help?", "user1")

        assert result.valid
        assert len(result.reasons) == 0


class TestWarningPatterns:
    """Tests for warning pattern detection."""

    def test_warn_curl_request(self, validator):
        """Test warning for curl command."""
        result = validator.validate_message("curl https://example.com", "user1")

        assert result.valid  # Warning but not blocked
        assert len(result.warnings) > 0

    def test_warn_kill_9(self, validator):
        """Test warning for kill -9."""
        result = validator.validate_message("kill -9 12345", "user1")

        assert result.valid
        assert len(result.warnings) > 0


class TestRateLimiting:
    """Tests for rate limiting."""

    def test_allow_messages_within_limit(self, validator):
        """Test allowing messages within rate limit."""
        for i in range(5):
            result = validator.validate_message(f"Message {i}", "user1")
            assert result.rate_limit_ok

    def test_block_messages_over_limit(self, validator):
        """Test blocking messages over rate limit."""
        # Send 5 messages (at limit)
        for i in range(5):
            validator.validate_message(f"Message {i}", "user1")

        # 6th message should be blocked
        result = validator.validate_message("Message 6", "user1")
        assert not result.rate_limit_ok
        assert not result.valid

    def test_rate_limit_per_user(self, validator):
        """Test rate limiting is per-user."""
        # User1 at limit
        for i in range(5):
            validator.validate_message(f"Message {i}", "user1")

        # User2 should not be limited
        result = validator.validate_message("Message", "user2")
        assert result.rate_limit_ok

    def test_reset_rate_limit(self, validator):
        """Test resetting rate limit."""
        # Fill user1 limit
        for i in range(5):
            validator.validate_message(f"Message {i}", "user1")

        # Next message blocked
        result = validator.validate_message("Message", "user1")
        assert not result.rate_limit_ok

        # Reset and try again
        validator.reset_rate_limit("user1")
        result = validator.validate_message("Message", "user1")
        assert result.rate_limit_ok


class TestMessageLength:
    """Tests for message length warnings."""

    def test_warn_long_message(self, validator):
        """Test warning for very long message."""
        long_msg = "a" * 15000
        result = validator.validate_message(long_msg, "user1")

        assert result.valid
        assert len(result.warnings) > 0


class TestAuditTrail:
    """Tests for audit trail."""

    def test_get_audit_trail(self, validator):
        """Test retrieving audit trail."""
        validator.validate_message("Test message", "user1")
        validator.validate_message("rm -rf /", "user1")

        audit = validator.get_audit_trail()
        assert len(audit) >= 2

    def test_filter_audit_by_user(self, validator):
        """Test filtering audit by user."""
        validator.validate_message("Message 1", "user1")
        validator.validate_message("Message 2", "user2")

        user1_audit = validator.get_audit_trail("user1")
        assert all(e["user_id"] == "user1" for e in user1_audit)

    def test_get_user_stats(self, validator):
        """Test getting user statistics."""
        validator.validate_message("Safe message", "user1")
        validator.validate_message("rm -rf /", "user1")

        stats = validator.get_user_stats("user1")

        assert stats["user_id"] == "user1"
        assert stats["total_messages"] == 2
        assert stats["blocked"] == 1


class TestEdgeCases:
    """Tests for edge cases."""

    def test_case_insensitive_blocking(self, validator):
        """Test blocking is case-insensitive."""
        result = validator.validate_message("RM -RF /", "user1")

        assert not result.valid

    def test_empty_message(self, validator):
        """Test handling empty message."""
        result = validator.validate_message("", "user1")

        assert result.valid

    def test_multiple_violations(self, validator):
        """Test detecting multiple violations."""
        result = validator.validate_message("rm -rf / && DROP TABLE;", "user1")

        assert not result.valid
        assert len(result.reasons) >= 2


# Coverage targets
COVERAGE_TARGETS = {
    "Dangerous Patterns": "✅ 5 tests",
    "Warning Patterns": "✅ 2 tests",
    "Rate Limiting": "✅ 4 tests",
    "Message Length": "✅ 1 test",
    "Audit Trail": "✅ 3 tests",
    "Edge Cases": "✅ 3 tests",
    "Total Tests": "18 tests",
    "Target Coverage": "70%+"
}

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
