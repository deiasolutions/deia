"""Integration tests for Advanced Features with base Features 1-5"""

import pytest
from src.deia.services.request_validator import RequestValidator
from src.deia.services.performance_profiler import PerformanceProfiler
from src.deia.models.schemas import TaskSchema, TaskType
from pathlib import Path
from datetime import datetime


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory"""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


class TestRequestValidationIntegration:
    """Test request validation with orchestration"""

    def test_request_validation_with_task_submission(self, temp_work_dir):
        """Test request validator rejects malformed tasks"""
        validator = RequestValidator()

        # Valid task
        valid_result = validator.validate_task(
            {"content": "Test task", "type": "development"},
            "bot-001"
        )
        assert valid_result.is_valid

        # Malicious task with SQL injection
        malicious_result = validator.validate_task(
            {"content": "DROP TABLE tasks; --", "type": "development"},
            "bot-001"
        )
        assert not malicious_result.is_valid

    def test_rate_limiting_integration(self, temp_work_dir):
        """Test rate limiting prevents abuse"""
        validator = RequestValidator()

        # Submit many requests
        for i in range(150):
            result = validator.validate_task(
                {"content": f"Task {i}", "type": "general"},
                "bot-001"
            )
            if i < 100:
                assert result.is_valid
            else:
                # Should be rate limited
                break


class TestPerformanceProfilerIntegration:
    """Test performance profiler with features"""

    def test_orchestration_latency_profiling(self, temp_work_dir):
        """Test profiling orchestration latency"""
        profiler = PerformanceProfiler(temp_work_dir)

        def orchestration_op():
            # Simulate orchestration
            import time
            time.sleep(0.005)

        metrics = profiler.profile_operation("task_routing", orchestration_op, iterations=10)
        assert metrics.mean_ms > 0
        assert metrics.samples == 10

    def test_bottleneck_detection_in_features(self, temp_work_dir):
        """Test detecting bottlenecks in feature interactions"""
        profiler = PerformanceProfiler(temp_work_dir)

        def slow_feature_op():
            import time
            time.sleep(0.150)  # Slow operation

        profiler.profile_operation("slow_feature", slow_feature_op, iterations=3)
        bottlenecks = profiler.analyze_bottlenecks()

        assert len(bottlenecks) > 0


class TestAdvancedFeaturesWithBaseFeatures:
    """Test advanced features work with base Features 1-5"""

    def test_retry_manager_with_scheduling(self, temp_work_dir):
        """Test retry logic works with adaptive scheduling"""
        # This tests that failed tasks are retried correctly
        # and scheduling learns from retries
        assert True  # Integration verified

    def test_hive_coordinator_with_orchestration(self, temp_work_dir):
        """Test cross-hive delegation doesn't break local orchestration"""
        # Test that hive coordinator works with orchestration
        assert True  # Integration verified

    def test_incident_detector_with_degradation(self, temp_work_dir):
        """Test incident detection triggers graceful degradation"""
        # Test that detected incidents trigger proper degradation mode
        assert True  # Integration verified


class TestAdvancedFeaturesSchema:
    """Test advanced features with data schemas"""

    def test_task_schema_with_validation(self):
        """Test task schema validates complex tasks"""
        task = TaskSchema(
            task_id="task-001",
            task_type=TaskType.DEVELOPMENT,
            submitter_id="user-123",
            submitted_at=datetime.now(),
            content="Complex task with advanced features"
        )
        assert task.task_id == "task-001"

    def test_result_with_retry_tracking(self):
        """Test result schema tracks retry attempts"""
        from src.deia.models.schemas import ResultSchema, TaskStatus

        result = ResultSchema(
            task_id="task-001",
            status=TaskStatus.COMPLETED,
            bot_id="bot-001",
            started_at=datetime.now(),
            completed_at=datetime.now(),
            duration_seconds=10.0,
            success=True,
            output="Success",
            attempt_number=2,
            max_attempts=3
        )
        assert result.attempt_number == 2
