#!/usr/bin/env python3
"""Audit Logging: Track all user actions, system changes, compliance."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - AUDIT - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Audit event types."""
    USER_ACTION = "user_action"
    SYSTEM_CHANGE = "system_change"
    SECURITY_EVENT = "security_event"
    CONFIG_CHANGE = "config_change"
    DATA_ACCESS = "data_access"
    ERROR = "error"


class EventSeverity(Enum):
    """Event severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Single audit event."""
    id: str = field(default_factory=lambda: __import__('uuid').uuid4().__str__()[:8])
    event_type: EventType = EventType.USER_ACTION
    severity: EventSeverity = EventSeverity.INFO
    actor: str = ""
    action: str = ""
    resource: str = ""
    changes: Dict = field(default_factory=dict)
    result: str = "success"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['event_type'] = self.event_type.value
        data['severity'] = self.severity.value
        return data


class AuditLogger:
    """Core audit logging system."""

    def __init__(self, project_root: Path = None):
        """Initialize audit logger."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.audit_dir = project_root / ".deia" / "audit"
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        self.events_log = self.audit_dir / "events.jsonl"
        self.changes_log = self.audit_dir / "changes.jsonl"
        self.events: List[AuditEvent] = []
        self.lock = threading.RLock()

    def log_event(self, event_type: EventType, actor: str, action: str,
                 resource: str = "", changes: Optional[Dict] = None,
                 severity: EventSeverity = EventSeverity.INFO) -> AuditEvent:
        """Log an audit event."""
        with self.lock:
            event = AuditEvent(
                event_type=event_type,
                actor=actor,
                action=action,
                resource=resource,
                changes=changes or {},
                severity=severity
            )
            self.events.append(event)
            self._persist_event(event)
            logger.info(f"Event: {actor} {action} {resource}")
            return event

    def log_change(self, actor: str, resource: str, before: Dict, after: Dict):
        """Log a configuration/data change."""
        changes = self._compute_changes(before, after)
        self.log_event(
            EventType.SYSTEM_CHANGE,
            actor,
            "modify",
            resource,
            changes,
            EventSeverity.WARNING
        )

    def log_security_event(self, actor: str, action: str, success: bool):
        """Log security event."""
        self.log_event(
            EventType.SECURITY_EVENT,
            actor,
            action,
            severity=EventSeverity.CRITICAL if not success else EventSeverity.INFO
        )

    def log_data_access(self, actor: str, resource: str, operation: str):
        """Log data access."""
        self.log_event(EventType.DATA_ACCESS, actor, operation, resource)

    def get_events_by_actor(self, actor: str) -> List[AuditEvent]:
        """Get all events by actor."""
        with self.lock:
            return [e for e in self.events if e.actor == actor]

    def get_events_by_resource(self, resource: str) -> List[AuditEvent]:
        """Get all events for resource."""
        with self.lock:
            return [e for e in self.events if e.resource == resource]

    def get_events_by_type(self, event_type: EventType) -> List[AuditEvent]:
        """Get events by type."""
        with self.lock:
            return [e for e in self.events if e.event_type == event_type]

    def query(self, actor: Optional[str] = None, resource: Optional[str] = None,
             event_type: Optional[EventType] = None) -> List[AuditEvent]:
        """Query audit trail."""
        with self.lock:
            results = self.events
            if actor:
                results = [e for e in results if e.actor == actor]
            if resource:
                results = [e for e in results if e.resource == resource]
            if event_type:
                results = [e for e in results if e.event_type == event_type]
            return results

    def get_stats(self) -> Dict:
        """Get audit statistics."""
        with self.lock:
            total = len(self.events)
            by_type = {}
            by_actor = {}
            by_severity = {}

            for event in self.events:
                by_type[event.event_type.value] = by_type.get(event.event_type.value, 0) + 1
                by_actor[event.actor] = by_actor.get(event.actor, 0) + 1
                by_severity[event.severity.value] = by_severity.get(event.severity.value, 0) + 1

            return {
                "total_events": total,
                "by_type": by_type,
                "by_actor": by_actor,
                "by_severity": by_severity
            }

    def _persist_event(self, event: AuditEvent):
        """Persist event to log."""
        try:
            with open(self.events_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event.to_dict()) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist event: {e}")

    @staticmethod
    def _compute_changes(before: Dict, after: Dict) -> Dict:
        """Compute before/after changes."""
        changes = {}
        for key in set(list(before.keys()) + list(after.keys())):
            before_val = before.get(key)
            after_val = after.get(key)
            if before_val != after_val:
                changes[key] = {"before": before_val, "after": after_val}
        return changes


class ComplianceReporter:
    """Generate compliance reports."""

    def __init__(self, audit_logger: AuditLogger):
        """Initialize compliance reporter."""
        self.logger = audit_logger

    def get_user_activity_report(self, actor: str) -> Dict:
        """Get user activity report."""
        events = self.logger.get_events_by_actor(actor)
        return {
            "actor": actor,
            "total_events": len(events),
            "actions": [e.action for e in events],
            "last_activity": events[-1].timestamp if events else None
        }

    def get_change_history(self, resource: str) -> List[Dict]:
        """Get change history for resource."""
        events = self.logger.get_events_by_resource(resource)
        return [{
            "timestamp": e.timestamp,
            "actor": e.actor,
            "changes": e.changes
        } for e in events if e.event_type == EventType.SYSTEM_CHANGE]

    def generate_compliance_report(self) -> Dict:
        """Generate comprehensive compliance report."""
        stats = self.logger.get_stats()
        return {
            "report_date": datetime.utcnow().isoformat() + "Z",
            "audit_stats": stats,
            "security_events": len(self.logger.get_events_by_type(EventType.SECURITY_EVENT)),
            "critical_events": len([e for e in self.logger.events if e.severity == EventSeverity.CRITICAL])
        }


class AuditService:
    """High-level audit service."""

    def __init__(self, project_root: Path = None):
        """Initialize audit service."""
        self.logger = AuditLogger(project_root)
        self.reporter = ComplianceReporter(self.logger)

    def log(self, event_type: EventType, actor: str, action: str,
           resource: str = "") -> AuditEvent:
        """Log event."""
        return self.logger.log_event(event_type, actor, action, resource)

    def log_change(self, actor: str, resource: str, before: Dict, after: Dict):
        """Log change."""
        self.logger.log_change(actor, resource, before, after)

    def log_security(self, actor: str, action: str, success: bool):
        """Log security event."""
        self.logger.log_security_event(actor, action, success)

    def query(self, actor: Optional[str] = None, resource: Optional[str] = None) -> List[AuditEvent]:
        """Query audit trail."""
        return self.logger.query(actor, resource)

    def user_report(self, actor: str) -> Dict:
        """Get user activity report."""
        return self.reporter.get_user_activity_report(actor)

    def compliance_report(self) -> Dict:
        """Get compliance report."""
        return self.reporter.generate_compliance_report()

    def stats(self) -> Dict:
        """Get audit statistics."""
        return self.logger.get_stats()
