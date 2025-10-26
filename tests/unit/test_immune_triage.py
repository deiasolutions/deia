#!/usr/bin/env python3
"""Tests for Immune System Triage Agent."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.immune_triage import AnomalyDetector, ThreatClassifier, ImmuneTriageAgent


class TestAnomalyDetector:
    """Test anomaly detection."""

    def test_detect_scope_violation(self):
        """Test scope violation detection."""
        signals = [{
            "type": "scope_violation",
            "data": {"bot_id": "BOT-001", "path": "/external/repo"}
        }]

        anomalies = AnomalyDetector.detect(signals)
        assert len(anomalies) == 1
        assert anomalies[0]["pattern"] == "scope_violation"
        assert anomalies[0]["severity"] == "critical"

    def test_detect_memory_spike(self):
        """Test memory spike detection."""
        signals = [{
            "type": "memory",
            "data": {"usage_mb": 1800}
        }]

        anomalies = AnomalyDetector.detect(signals)
        assert len(anomalies) == 1
        assert anomalies[0]["pattern"] == "memory_spike"

    def test_detect_error_rate_spike(self):
        """Test error rate spike detection."""
        signals = [{
            "type": "error_rate",
            "data": {"rate": 0.10}
        }]

        anomalies = AnomalyDetector.detect(signals)
        assert len(anomalies) == 1
        assert anomalies[0]["pattern"] == "error_rate_spike"

    def test_detect_connection_exhaustion(self):
        """Test connection pool exhaustion detection."""
        signals = [{
            "type": "connections",
            "data": {"utilization": 0.95}
        }]

        anomalies = AnomalyDetector.detect(signals)
        assert len(anomalies) == 1
        assert anomalies[0]["pattern"] == "connection_exhaustion"

    def test_detect_multiple_anomalies(self):
        """Test detecting multiple anomalies."""
        signals = [
            {"type": "memory", "data": {"usage_mb": 1800}},
            {"type": "error_rate", "data": {"rate": 0.10}},
            {"type": "disk", "data": {"usage_percent": 95}}
        ]

        anomalies = AnomalyDetector.detect(signals)
        assert len(anomalies) == 3


class TestThreatClassifier:
    """Test threat classification."""

    def test_classify_critical_threats(self):
        """Test classifying critical threats."""
        anomalies = [
            {"pattern": "scope_violation", "severity": "critical", "signal": {}, "details": "Bot escaped"},
            {"pattern": "resource_exhaustion", "severity": "critical", "signal": {}, "details": "Disk full"}
        ]

        classification = ThreatClassifier.classify(anomalies)
        assert classification["critical_count"] == 2
        assert classification["total_anomalies"] == 2
        assert "IMMEDIATE" in str(classification["recommended_actions"])

    def test_classify_mixed_severity(self):
        """Test classifying mixed severity anomalies."""
        anomalies = [
            {"pattern": "scope_violation", "severity": "critical", "signal": {}, "details": ""},
            {"pattern": "memory_spike", "severity": "high", "signal": {}, "details": ""},
            {"pattern": "response_time_degradation", "severity": "medium", "signal": {}, "details": ""}
        ]

        classification = ThreatClassifier.classify(anomalies)
        assert classification["critical_count"] == 1
        assert classification["high_count"] == 1
        assert classification["medium_count"] == 1

    def test_empty_anomalies(self):
        """Test classifying with no anomalies."""
        classification = ThreatClassifier.classify([])
        assert classification["total_anomalies"] == 0
        assert classification["critical_count"] == 0
        assert len(classification["recommended_actions"]) == 0


class TestImmuneTriageAgent:
    """Test triage agent."""

    def test_agent_initialization(self):
        """Test agent initialization."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            agent = ImmuneTriageAgent(Path(tmpdir))
            assert agent.detector is not None
            assert agent.classifier is not None

    def test_process_signals(self):
        """Test processing signals."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            agent = ImmuneTriageAgent(Path(tmpdir))

            signals = [
                {"type": "scope_violation", "data": {"bot_id": "BOT-001", "path": "/ext"}},
                {"type": "memory", "data": {"usage_mb": 1800}}
            ]

            result = agent.process_signals(signals)
            assert result["total_anomalies"] == 2
            assert result["critical_count"] == 1
            assert result["high_count"] == 1

    def test_generate_report(self):
        """Test report generation."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            agent = ImmuneTriageAgent(Path(tmpdir))

            signals = [
                {"type": "error_rate", "data": {"rate": 0.10}},
                {"type": "response_time", "data": {"p95_ms": 3000}}
            ]

            report = agent.generate_report(signals)
            assert report["signal_count"] == 2
            assert report["anomaly_count"] == 2
            assert "actionable_alerts" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
