"""
Unit tests for RequestValidator security service

Tests validation, sanitization, rate limiting, and signature verification
"""

import pytest
import time
from src.deia.services.request_validator import RequestValidator, ValidationResult


class TestRequestValidator:
    """Test suite for RequestValidator"""

    @pytest.fixture
    def validator(self):
        """Create validator instance for each test"""
        return RequestValidator(log_file="/tmp/test-validation.jsonl")

    # Schema Validation Tests
    def test_valid_task(self, validator):
        """Test validation passes for valid task"""
        task = {
            "content": "test task",
            "task_id": "TASK-001",
            "priority": "P1"
        }
        result = validator.validate_task(task, "BOT-001")
        assert result.is_valid
        assert result.error_message is None

    def test_missing_content_field(self, validator):
        """Test validation fails when content is missing"""
        task = {"task_id": "TASK-001"}
        result = validator.validate_task(task, "BOT-001")
        assert not result.is_valid
        assert "content" in result.error_message.lower()

    def test_content_too_long(self, validator):
        """Test validation fails when content exceeds max length"""
        task = {"content": "x" * (validator.MAX_TASK_CONTENT_LENGTH + 1)}
        result = validator.validate_task(task, "BOT-001")
        assert not result.is_valid
        assert "exceeds maximum length" in result.error_message.lower()

    def test_invalid_priority(self, validator):
        """Test validation fails for invalid priority"""
        task = {"content": "test", "priority": "P5"}
        result = validator.validate_task(task, "BOT-001")
        assert not result.is_valid

    def test_non_string_content(self, validator):
        """Test validation fails when content is not string"""
        task = {"content": 123}
        result = validator.validate_task(task, "BOT-001")
        assert not result.is_valid

    # Bot ID Validation Tests
    def test_invalid_bot_id_format(self, validator):
        """Test validation fails for invalid bot ID format"""
        task = {"content": "test"}
        result = validator.validate_task(task, "BOT@@@")
        assert not result.is_valid

    def test_empty_bot_id(self, validator):
        """Test validation fails for empty bot ID"""
        task = {"content": "test"}
        result = validator.validate_task(task, "")
        assert not result.is_valid

    def test_bot_id_too_long(self, validator):
        """Test validation fails for excessively long bot ID"""
        task = {"content": "test"}
        long_id = "BOT-" + "x" * validator.MAX_BOT_ID_LENGTH
        result = validator.validate_task(task, long_id)
        assert not result.is_valid

    # Sanitization Tests
    def test_html_escaping(self, validator):
        """Test HTML special characters are escaped"""
        task = {"content": "<script>alert('xss')</script>"}
        result = validator.validate_task(task, "BOT-001")
        assert result.is_valid
        assert "&lt;script&gt;" in result.sanitized_data["content"]

    def test_quote_escaping(self, validator):
        """Test quotes are properly escaped"""
        task = {"content": 'Test "quoted" text'}
        result = validator.validate_task(task, "BOT-001")
        assert result.is_valid
        assert "&quot;" in result.sanitized_data["content"]

    def test_dangerous_pattern_detection(self, validator):
        """Test dangerous patterns trigger warnings"""
        task = {"content": "rm -rf /"}
        result = validator.validate_task(task, "BOT-001")
        assert result.is_valid  # Still valid (sanitized)
        assert len(result.warnings) > 0
        assert "dangerous" in result.warnings[0].lower()

    def test_sql_injection_detection(self, validator):
        """Test SQL injection patterns detected"""
        task = {"content": "SELECT * FROM users; DROP TABLE users;"}
        result = validator.validate_task(task, "BOT-001")
        assert result.is_valid  # Sanitized
        assert len(result.warnings) > 0

    def test_subprocess_call_detection(self, validator):
        """Test subprocess execution patterns detected"""
        task = {"content": "subprocess.call(['rm', '-rf', '/'])"}
        result = validator.validate_task(task, "BOT-001")
        assert result.is_valid  # Sanitized
        assert len(result.warnings) > 0

    # Rate Limiting Tests
    def test_rate_limit_allows_normal_traffic(self, validator):
        """Test normal request rate is allowed"""
        for i in range(10):
            task = {"content": f"task {i}"}
            result = validator.validate_task(task, "BOT-001")
            assert result.is_valid

    def test_rate_limit_blocks_excessive_traffic(self, validator):
        """Test excessive requests are rate-limited"""
        # Send requests to exceed limit
        for i in range(validator.RATE_LIMIT_REQUESTS_PER_MINUTE + 10):
            task = {"content": f"task {i}"}
            result = validator.validate_task(task, "BOT-002")

        # Next request should be blocked
        task = {"content": "test"}
        result = validator.validate_task(task, "BOT-002")
        assert not result.is_valid
        assert "rate limit" in result.error_message.lower()

    def test_rate_limit_resets_after_window(self, validator):
        """Test rate limit window resets properly"""
        # Send requests to exceed limit (short window for testing)
        validator.RATE_LIMIT_WINDOW = 0.1  # 100ms for testing

        for i in range(validator.RATE_LIMIT_REQUESTS_PER_MINUTE + 1):
            task = {"content": f"task {i}"}
            result = validator.validate_task(task, "BOT-003")

        # Should be blocked now
        result = validator.validate_task({"content": "test"}, "BOT-003")
        assert not result.is_valid

        # Wait for window to reset
        time.sleep(0.2)

        # Should work again
        result = validator.validate_task({"content": "test"}, "BOT-003")
        assert result.is_valid

    def test_per_bot_rate_limiting(self, validator):
        """Test rate limiting is per-bot, not global"""
        # Max out BOT-001
        for i in range(validator.RATE_LIMIT_REQUESTS_PER_MINUTE + 1):
            task = {"content": f"task {i}"}
            validator.validate_task(task, "BOT-001")

        # BOT-001 should be blocked
        result = validator.validate_task({"content": "test"}, "BOT-001")
        assert not result.is_valid

        # BOT-002 should still work
        result = validator.validate_task({"content": "test"}, "BOT-002")
        assert result.is_valid

    # Bot Registration Tests
    def test_register_trusted_bot(self, validator):
        """Test registering a bot as trusted"""
        validator.register_bot("BOT-TRUSTED")
        assert "BOT-TRUSTED" in validator.trusted_bots

    # Status Tests
    def test_get_status(self, validator):
        """Test validator status reporting"""
        # Send some requests
        for i in range(5):
            task = {"content": f"task {i}"}
            validator.validate_task(task, "BOT-001")

        status = validator.get_status()
        assert status["total_requests"] == 5
        assert status["validation_stats"]["passed"] == 5
        assert status["rate_limit_config"]["requests_per_minute"] == validator.RATE_LIMIT_REQUESTS_PER_MINUTE

    # Integration Tests
    def test_complete_validation_workflow(self, validator):
        """Test complete validation workflow"""
        # Valid request
        task = {"content": "Execute analysis", "priority": "P1", "task_id": "TASK-001"}
        result = validator.validate_task(task, "BOT-001")
        assert result.is_valid
        assert result.sanitized_data is not None

        # Invalid request
        task = {"content": "x" * 20000}
        result = validator.validate_task(task, "BOT-002")
        assert not result.is_valid

        # Dangerous content (sanitized but with warnings)
        task = {"content": "eval(user_input)"}
        result = validator.validate_task(task, "BOT-003")
        assert result.is_valid
        assert len(result.warnings) > 0

    def test_validation_count_accuracy(self, validator):
        """Test validation statistics are accurate"""
        # Send mix of valid and invalid requests
        for i in range(3):
            validator.validate_task({"content": f"task {i}"}, "BOT-001")

        validator.validate_task({"missing": "field"}, "BOT-001")

        status = validator.get_status()
        assert status["validation_stats"]["passed"] == 3
        assert status["validation_stats"]["failed"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
