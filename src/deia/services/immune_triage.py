#!/usr/bin/env python3
"""
Immune System Triage Agent: Detect anomalies and classify threats.

First line of detection and classification for system anomalies.
Routes threats to cure engine based on classification.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - IMMUNE-TRIAGE - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detects system anomalies from health signals."""

    # Anomaly patterns
    PATTERNS = {
        "scope_violation": {
            "description": "Bot accessed out-of-scope paths",
            "severity": "critical",
            "signal_type": "coordinator_alert"
        },
        "memory_spike": {
            "description": "Unexpected memory usage increase",
            "severity": "high",
            "signal_type": "resource_monitor"
        },
        "connection_exhaustion": {
            "description": "Connection pool nearing capacity",
            "severity": "high",
            "signal_type": "connection_monitor"
        },
        "error_rate_spike": {
            "description": "Error rate above threshold",
            "severity": "high",
            "signal_type": "metrics_monitor"
        },
        "response_time_degradation": {
            "description": "P95 response time elevated",
            "severity": "medium",
            "signal_type": "performance_monitor"
        },
        "repeated_failures": {
            "description": "Same operation failing repeatedly",
            "severity": "medium",
            "signal_type": "operation_monitor"
        },
        "unauthorized_access_attempt": {
            "description": "Non-authenticated access attempt",
            "severity": "critical",
            "signal_type": "security_monitor"
        },
        "configuration_drift": {
            "description": "Config differs from baseline",
            "severity": "medium",
            "signal_type": "config_monitor"
        },
        "resource_exhaustion": {
            "description": "Disk space, CPU, or memory exhausted",
            "severity": "critical",
            "signal_type": "resource_monitor"
        },
        "cascade_failure": {
            "description": "Multiple systems failing in sequence",
            "severity": "critical",
            "signal_type": "dependency_monitor"
        }
    }

    @staticmethod
    def detect(signals: List[Dict]) -> List[Dict]:
        """Detect anomalies from signals."""
        anomalies = []

        for signal in signals:
            signal_type = signal.get("type")
            data = signal.get("data", {})

            # Scope violation detection
            if signal_type == "scope_violation":
                anomalies.append({
                    "pattern": "scope_violation",
                    "severity": "critical",
                    "signal": signal,
                    "details": f"Bot {data.get('bot_id')} accessed {data.get('path')}"
                })

            # Memory spike detection
            elif signal_type == "memory" and data.get("usage_mb", 0) > 1600:
                anomalies.append({
                    "pattern": "memory_spike",
                    "severity": "high",
                    "signal": signal,
                    "details": f"Memory: {data.get('usage_mb')}MB"
                })

            # Error rate detection
            elif signal_type == "error_rate" and data.get("rate", 0) > 0.05:
                anomalies.append({
                    "pattern": "error_rate_spike",
                    "severity": "high",
                    "signal": signal,
                    "details": f"Error rate: {data.get('rate')*100:.1f}%"
                })

            # Response time degradation
            elif signal_type == "response_time" and data.get("p95_ms", 0) > 2000:
                anomalies.append({
                    "pattern": "response_time_degradation",
                    "severity": "medium",
                    "signal": signal,
                    "details": f"P95: {data.get('p95_ms')}ms"
                })

            # Connection exhaustion
            elif signal_type == "connections" and data.get("utilization", 0) > 0.8:
                anomalies.append({
                    "pattern": "connection_exhaustion",
                    "severity": "high",
                    "signal": signal,
                    "details": f"Connection pool: {data.get('utilization')*100:.0f}%"
                })

            # Disk exhaustion
            elif signal_type == "disk" and data.get("usage_percent", 0) > 90:
                anomalies.append({
                    "pattern": "resource_exhaustion",
                    "severity": "critical",
                    "signal": signal,
                    "details": f"Disk: {data.get('usage_percent'):.0f}%"
                })

        return anomalies


class ThreatClassifier:
    """Classify detected anomalies by threat level and category."""

    @staticmethod
    def classify(anomalies: List[Dict]) -> Dict:
        """Classify anomalies and determine response."""
        classified = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_anomalies": len(anomalies),
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "anomalies_by_severity": {},
            "recommended_actions": [],
            "false_positive_likelihood": 0.0
        }

        severity_groups = {}

        for anomaly in anomalies:
            severity = anomaly.get("severity", "unknown")
            pattern = anomaly.get("pattern", "unknown")

            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(anomaly)

            # Count by severity
            if severity == "critical":
                classified["critical_count"] += 1
            elif severity == "high":
                classified["high_count"] += 1
            elif severity == "medium":
                classified["medium_count"] += 1

        classified["anomalies_by_severity"] = severity_groups

        # Determine recommended actions
        if classified["critical_count"] > 0:
            classified["recommended_actions"].append("IMMEDIATE: Freeze all non-critical operations")
            classified["recommended_actions"].append("ESCALATE: Page on-call engineer")
            classified["recommended_actions"].append("ISOLATE: Identify affected components")

        if classified["high_count"] > 2:
            classified["recommended_actions"].append("INVESTIGATE: Multiple high-severity issues detected")
            classified["recommended_actions"].append("PREPARE: Rollback procedures")

        if classified["medium_count"] > 5:
            classified["recommended_actions"].append("MONITOR: High volume of medium-severity issues")

        # Calculate false positive likelihood (simple heuristic)
        # Recent cosmetic errors = higher likelihood
        error_patterns = sum(1 for a in anomalies if "timeout" in a.get("details", "").lower())
        classified["false_positive_likelihood"] = min(0.95, error_patterns * 0.1)

        return classified


class ImmuneTriageAgent:
    """Main triage agent coordinating detection and classification."""

    def __init__(self, project_root: Path = None):
        """Initialize triage agent."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.triage_log = project_root / ".deia" / "logs" / "immune-triage.jsonl"
        self.detector = AnomalyDetector()
        self.classifier = ThreatClassifier()

        # Ensure directories exist
        self.triage_log.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Immune Triage Agent initialized")

    def process_signals(self, signals: List[Dict]) -> Dict:
        """Process signals and return triage result."""
        # Detect anomalies
        anomalies = self.detector.detect(signals)

        # Classify threats
        classification = self.classifier.classify(anomalies)

        # Log triage
        self._log_triage(classification, anomalies)

        return classification

    def _log_triage(self, classification: Dict, anomalies: List[Dict]):
        """Log triage result."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "classification": classification,
            "anomalies_count": len(anomalies)
        }

        try:
            with open(self.triage_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to log triage: {e}")

    def generate_report(self, signals: List[Dict]) -> Dict:
        """Generate comprehensive triage report."""
        anomalies = self.detector.detect(signals)
        classification = self.classifier.classify(anomalies)

        report = {
            "report_time": datetime.utcnow().isoformat() + "Z",
            "signal_count": len(signals),
            "anomaly_count": len(anomalies),
            "classification": classification,
            "actionable_alerts": [
                a for a in anomalies
                if a.get("severity") in ["critical", "high"]
            ]
        }

        return report
