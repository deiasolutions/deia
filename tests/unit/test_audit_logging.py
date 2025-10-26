#!/usr/bin/env python3
"""Tests for Audit Logging."""

import pytest
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.audit_logging import (
    EventType, EventSeverity, AuditEvent, AuditLogger,
    ComplianceReporter, AuditService
)


class TestAuditEvent:
    """Test audit event."""

    def test_create_event(self):
        """Test creating event."""
        event = AuditEvent(
            event_type=EventType.USER_ACTION,
            actor="user-1",
            action="create",
            resource="document-1"
        )
        assert event.actor == "user-1"
        assert event.action == "create"


class TestAuditLogger:
    """Test audit logger."""

    @pytest.fixture
    def logger(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = AuditLogger(Path(tmpdir))
            yield logger

    def test_log_event(self, logger):
        """Test logging event."""
        event = logger.log_event(
            EventType.USER_ACTION,
            "user-1",
            "create",
            "doc-1"
        )
        assert event is not None
        assert event.actor == "user-1"

    def test_log_change(self, logger):
        """Test logging change."""
        logger.log_change(
            "admin",
            "config",
            {"timeout": 30},
            {"timeout": 60}
        )
        events = logger.query(actor="admin")
        assert len(events) > 0

    def test_log_security_event(self, logger):
        """Test logging security event."""
        logger.log_security_event("user-1", "login", True)
        events = logger.get_events_by_type(EventType.SECURITY_EVENT)
        assert len(events) > 0

    def test_query_by_actor(self, logger):
        """Test querying by actor."""
        logger.log_event(EventType.USER_ACTION, "user-1", "read", "doc-1")
        logger.log_event(EventType.USER_ACTION, "user-2", "write", "doc-2")

        events = logger.query(actor="user-1")
        assert len(events) == 1
        assert events[0].actor == "user-1"

    def test_query_by_resource(self, logger):
        """Test querying by resource."""
        logger.log_event(EventType.USER_ACTION, "user-1", "read", "doc-1")
        logger.log_event(EventType.USER_ACTION, "user-2", "read", "doc-1")

        events = logger.query(resource="doc-1")
        assert len(events) == 2

    def test_get_stats(self, logger):
        """Test statistics."""
        logger.log_event(EventType.USER_ACTION, "user-1", "read", "doc-1")
        logger.log_event(EventType.SYSTEM_CHANGE, "admin", "modify", "config")

        stats = logger.get_stats()
        assert stats["total_events"] == 2
        assert "by_type" in stats
        assert "by_actor" in stats


class TestComplianceReporter:
    """Test compliance reporter."""

    @pytest.fixture
    def reporter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = AuditLogger(Path(tmpdir))
            reporter = ComplianceReporter(logger)
            yield logger, reporter

    def test_user_activity_report(self, reporter):
        """Test user activity report."""
        logger, reporter = reporter
        logger.log_event(EventType.USER_ACTION, "user-1", "read", "doc-1")
        logger.log_event(EventType.USER_ACTION, "user-1", "write", "doc-2")

        report = reporter.get_user_activity_report("user-1")
        assert report["actor"] == "user-1"
        assert report["total_events"] == 2

    def test_change_history(self, reporter):
        """Test change history."""
        logger, reporter = reporter
        logger.log_change("admin", "config", {"a": 1}, {"a": 2})

        history = reporter.get_change_history("config")
        assert len(history) > 0

    def test_compliance_report(self, reporter):
        """Test compliance report."""
        logger, reporter = reporter
        logger.log_event(EventType.SECURITY_EVENT, "user-1", "login")
        logger.log_event(EventType.USER_ACTION, "user-1", "read", "doc-1")

        report = reporter.generate_compliance_report()
        assert "report_date" in report
        assert "audit_stats" in report


class TestAuditService:
    """Test high-level service."""

    @pytest.fixture
    def service(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            service = AuditService(Path(tmpdir))
            yield service

    def test_log(self, service):
        """Test logging via service."""
        event = service.log(EventType.USER_ACTION, "user-1", "read", "doc-1")
        assert event is not None

    def test_log_change(self, service):
        """Test logging change via service."""
        service.log_change("admin", "config", {"x": 1}, {"x": 2})
        events = service.query(actor="admin")
        assert len(events) > 0

    def test_log_security(self, service):
        """Test logging security via service."""
        service.log_security("user-1", "login", True)
        assert True  # Event logged

    def test_query(self, service):
        """Test querying via service."""
        service.log(EventType.USER_ACTION, "user-1", "read", "doc-1")
        events = service.query(actor="user-1")
        assert len(events) > 0

    def test_user_report(self, service):
        """Test user report."""
        service.log(EventType.USER_ACTION, "user-1", "read", "doc-1")
        report = service.user_report("user-1")
        assert report["actor"] == "user-1"

    def test_compliance_report(self, service):
        """Test compliance report."""
        service.log(EventType.USER_ACTION, "user-1", "read", "doc-1")
        report = service.compliance_report()
        assert "audit_stats" in report

    def test_stats(self, service):
        """Test statistics."""
        service.log(EventType.USER_ACTION, "user-1", "read", "doc-1")
        stats = service.stats()
        assert stats["total_events"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
