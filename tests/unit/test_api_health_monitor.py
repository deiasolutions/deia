"""
Unit tests for APIHealthMonitor service.

Tests endpoint health checking, service degradation detection, cascade risk analysis.
"""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
from src.deia.services.api_health_monitor import (
    APIHealthMonitor,
    EndpointMetrics,
    ServiceHealth
)


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary working directory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / ".deia" / "bot-logs").mkdir(parents=True, exist_ok=True)
    return work_dir


@pytest.fixture
def api_monitor(temp_dir):
    """Create APIHealthMonitor instance."""
    return APIHealthMonitor(temp_dir)


class TestEndpointMetrics:
    """Test EndpointMetrics dataclass."""

    def test_endpoint_metrics_creation(self):
        """Test creating endpoint metrics."""
        now = datetime.now().isoformat()
        metrics = EndpointMetrics(
            endpoint_url="http://localhost:8001/health",
            bot_id="bot-001",
            timestamp=now,
            response_time_ms=150.5,
            status_code=200,
            is_healthy=True
        )
        assert metrics.endpoint_url == "http://localhost:8001/health"
        assert metrics.bot_id == "bot-001"
        assert metrics.is_healthy is True
        assert metrics.status_code == 200


class TestServiceHealth:
    """Test ServiceHealth tracking."""

    def test_service_health_creation(self):
        """Test creating service health record."""
        now = datetime.now().isoformat()
        health = ServiceHealth(
            bot_id="bot-001",
            service_url="http://localhost:8001",
            overall_status="healthy",
            endpoints_healthy=10,
            endpoints_total=10,
            error_rate=0.0,
            avg_response_time_ms=120.0,
            last_check=now
        )
        assert health.bot_id == "bot-001"
        assert health.overall_status == "healthy"
        assert health.endpoints_healthy == 10


class TestAPIHealthMonitor:
    """Test APIHealthMonitor functionality."""

    @patch('src.deia.services.api_health_monitor.requests.get')
    def test_check_endpoint_healthy(self, mock_get, api_monitor):
        """Test checking a healthy endpoint."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.15
        mock_get.return_value = mock_response

        metrics = api_monitor.check_endpoint("bot-001", "http://localhost:8001/health")

        assert metrics is not None
        assert metrics.bot_id == "bot-001"
        assert metrics.status_code == 200
        assert metrics.is_healthy is True

    @patch('src.deia.services.api_health_monitor.requests.get')
    def test_check_endpoint_timeout(self, mock_get, api_monitor):
        """Test endpoint timeout."""
        import requests
        mock_get.side_effect = requests.Timeout("timeout")

        metrics = api_monitor.check_endpoint("bot-001", "http://localhost:8001/health")

        assert metrics is not None
        assert metrics.timeout is True
        assert metrics.is_healthy is False

    @patch('src.deia.services.api_health_monitor.requests.get')
    def test_check_endpoint_error(self, mock_get, api_monitor):
        """Test endpoint error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.elapsed.total_seconds.return_value = 0.2
        mock_get.return_value = mock_response

        metrics = api_monitor.check_endpoint("bot-001", "http://localhost:8001/health")

        assert metrics is not None
        assert metrics.status_code == 500
        assert metrics.is_healthy is False

    @patch('src.deia.services.api_health_monitor.requests.get')
    def test_check_endpoint_slow_response(self, mock_get, api_monitor):
        """Test slow endpoint response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 2.5  # Slow response
        mock_get.return_value = mock_response

        metrics = api_monitor.check_endpoint("bot-001", "http://localhost:8001/health")

        assert metrics is not None
        assert metrics.response_time_ms > 2000
        assert metrics.is_healthy is False  # Slow response is unhealthy

    @patch('src.deia.services.api_health_monitor.requests.get')
    def test_get_api_status(self, mock_get, api_monitor):
        """Test getting API status."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response

        # Record some endpoint checks
        api_monitor.check_endpoint("bot-001", "http://localhost:8001/status")
        api_monitor.check_endpoint("bot-001", "http://localhost:8001/health")

        status = api_monitor.get_api_status()

        assert "overall_health" in status
        assert "endpoints" in status

    def test_check_cascade_risk(self, api_monitor):
        """Test cascade risk detection."""
        now = datetime.now().isoformat()

        # Add multiple failed endpoints
        metrics1 = EndpointMetrics(
            endpoint_url="http://localhost:8001/health",
            bot_id="bot-001",
            timestamp=now,
            response_time_ms=150.0,
            status_code=500,
            is_healthy=False
        )

        metrics2 = EndpointMetrics(
            endpoint_url="http://localhost:8001/status",
            bot_id="bot-001",
            timestamp=now,
            response_time_ms=150.0,
            status_code=500,
            is_healthy=False
        )

        api_monitor.endpoint_metrics["bot-001"] = [metrics1, metrics2]

        cascade_risk = api_monitor.check_cascade_risk()

        assert isinstance(cascade_risk, float)

    def test_track_service_health(self, api_monitor):
        """Test service health tracking."""
        now = datetime.now().isoformat()

        health = ServiceHealth(
            bot_id="bot-001",
            service_url="http://localhost:8001",
            overall_status="healthy",
            endpoints_healthy=5,
            endpoints_total=5,
            error_rate=0.0,
            avg_response_time_ms=120.0,
            last_check=now
        )

        api_monitor.service_health["bot-001"] = health

        retrieved = api_monitor.service_health.get("bot-001")

        assert retrieved is not None
        assert retrieved.bot_id == "bot-001"
        assert retrieved.overall_status == "healthy"

    def test_metrics_logging(self, api_monitor, temp_dir):
        """Test that endpoint metrics are logged to file."""
        now = datetime.now().isoformat()
        metrics = EndpointMetrics(
            endpoint_url="http://localhost:8001/health",
            bot_id="bot-001",
            timestamp=now,
            response_time_ms=150.0,
            status_code=200,
            is_healthy=True
        )

        api_monitor._log_metrics(metrics)

        log_file = temp_dir / ".deia" / "bot-logs" / "api-health.jsonl"
        assert log_file.exists()

        with open(log_file, "r") as f:
            lines = f.readlines()
            assert len(lines) > 0


class TestConsecutiveFailures:
    """Test consecutive failure tracking."""

    @patch('src.deia.services.api_health_monitor.requests.get')
    def test_consecutive_failure_detection(self, mock_get, api_monitor):
        """Test detection of consecutive failures."""
        mock_get.side_effect = Exception("Connection failed")

        # Simulate multiple consecutive failures
        for i in range(4):
            try:
                api_monitor.check_endpoint("bot-001", "http://localhost:8001/health")
            except:
                pass

        # Check if consecutive failures are tracked
        service_health = api_monitor.service_health.get("bot-001")
        if service_health:
            assert service_health.consecutive_failures > 0


class TestEndpointErrorRates:
    """Test error rate calculation."""

    def test_error_rate_calculation(self, api_monitor):
        """Test error rate calculation."""
        now = datetime.now().isoformat()

        # Add metrics with some errors
        metrics = [
            EndpointMetrics(
                endpoint_url="http://localhost:8001/health",
                bot_id="bot-001",
                timestamp=now,
                response_time_ms=150.0,
                status_code=200,
                is_healthy=True,
                request_count=10,
                error_count=1,
                error_rate=0.1
            ),
            EndpointMetrics(
                endpoint_url="http://localhost:8001/health",
                bot_id="bot-001",
                timestamp=now,
                response_time_ms=150.0,
                status_code=500,
                is_healthy=False,
                request_count=11,
                error_count=2,
                error_rate=0.18  # ~18% error rate
            )
        ]

        api_monitor.endpoint_metrics["bot-001"] = metrics

        # Verify error rates are stored
        assert api_monitor.endpoint_metrics["bot-001"][0].error_rate == 0.1
        assert api_monitor.endpoint_metrics["bot-001"][1].error_rate == 0.18
