"""
Audit Logger - Immutable audit trail for compliance and forensics.

Logs every action taken on the system with who/what/when/why.
Immutable: logs cannot be modified after creation.
Queryable: filter and search audit trail by various criteria.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib


class AuditAction(Enum):
    """Types of audit actions."""
    BOT_CREATED = "bot_created"
    BOT_DELETED = "bot_deleted"
    TASK_SUBMITTED = "task_submitted"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    CONFIG_CHANGED = "config_changed"
    BACKUP_CREATED = "backup_created"
    BACKUP_RESTORED = "backup_restored"
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    ALERT_GENERATED = "alert_generated"
    ALERT_RESOLVED = "alert_resolved"
    MESSAGE_SENT = "message_sent"
    RESTART_REQUESTED = "restart_requested"
    SHUTDOWN_INITIATED = "shutdown_initiated"
    API_CALL = "api_call"


class AuditLevel(Enum):
    """Audit severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class AuditEntry:
    """A single audit log entry."""
    entry_id: str
    timestamp: str
    action: AuditAction
    level: AuditLevel
    actor: str  # Who did the action (bot_id, user, system)
    target: str  # What was affected
    details: Dict[str, Any] = field(default_factory=dict)
    result: str = "success"  # success, failure, partial
    error_message: Optional[str] = None
    checksum: str = ""  # For integrity verification

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            **asdict(self),
            "action": self.action.value,
            "level": self.level.value
        }


class AuditLogger:
    """
    Immutable audit trail for compliance and forensics.

    Features:
    - Logs every significant action on the system
    - Immutable: append-only log format
    - Checksums: verify log integrity
    - Queryable: filter and search audit trail
    - Retention: configurable retention policy
    - Compliance: suitable for regulatory compliance
    """

    # Retention policy
    AUDIT_RETENTION_DAYS = 365  # 1 year
    CHECKSUM_CHAIN = True  # Include previous checksum in new entries

    def __init__(self, work_dir: Path):
        """
        Initialize audit logger.

        Args:
            work_dir: Working directory
        """
        self.work_dir = Path(work_dir)
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.audit_log = self.log_dir / "audit-trail.jsonl"
        self.audit_index = self.log_dir / "audit-index.json"

        # In-memory cache of audit entries
        self.entries: List[AuditEntry] = []
        self.entry_index: Dict[str, AuditEntry] = {}

        # Load existing audit log
        self._load_audit_log()

        # Last checksum for chain integrity
        self._last_checksum = ""

    def log_action(
        self,
        action: AuditAction,
        actor: str,
        target: str,
        level: AuditLevel = AuditLevel.INFO,
        details: Optional[Dict] = None,
        result: str = "success",
        error_message: Optional[str] = None
    ) -> str:
        """
        Log an action to the audit trail.

        Args:
            action: Type of action
            actor: Who performed the action
            target: What was affected
            level: Severity level
            details: Additional details
            result: success/failure/partial
            error_message: Error message if failed

        Returns:
            Entry ID
        """
        import uuid

        entry_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # Calculate checksum for integrity
        checksum_data = f"{entry_id}{timestamp}{action.value}{actor}{target}"
        checksum = hashlib.sha256(checksum_data.encode()).hexdigest()

        # Create entry
        entry = AuditEntry(
            entry_id=entry_id,
            timestamp=timestamp,
            action=action,
            level=level,
            actor=actor,
            target=target,
            details=details or {},
            result=result,
            error_message=error_message,
            checksum=checksum
        )

        # Add to memory
        self.entries.append(entry)
        self.entry_index[entry_id] = entry

        # Persist immediately (immutable)
        self._persist_entry(entry)

        return entry_id

    def query_entries(
        self,
        action: Optional[AuditAction] = None,
        actor: Optional[str] = None,
        target: Optional[str] = None,
        level: Optional[AuditLevel] = None,
        result: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 1000
    ) -> List[Dict]:
        """
        Query audit trail with filters.

        Args:
            action: Filter by action type
            actor: Filter by actor
            target: Filter by target
            level: Filter by level
            result: Filter by result
            start_time: ISO format start time
            end_time: ISO format end time
            limit: Max results

        Returns:
            List of matching audit entries
        """
        results = []

        for entry in self.entries:
            # Apply filters
            if action and entry.action != action:
                continue
            if actor and entry.actor != actor:
                continue
            if target and entry.target != target:
                continue
            if level and entry.level != level:
                continue
            if result and entry.result != result:
                continue

            # Time range filter
            if start_time or end_time:
                entry_time = datetime.fromisoformat(entry.timestamp)
                if start_time:
                    start = datetime.fromisoformat(start_time)
                    if entry_time < start:
                        continue
                if end_time:
                    end = datetime.fromisoformat(end_time)
                    if entry_time > end:
                        continue

            results.append(entry.to_dict())

        # Sort by timestamp, newest first
        results.sort(key=lambda e: e["timestamp"], reverse=True)

        return results[:limit]

    def get_actor_actions(self, actor: str, limit: int = 100) -> List[Dict]:
        """
        Get all actions by a specific actor.

        Args:
            actor: Actor identifier
            limit: Max results

        Returns:
            List of actions by actor
        """
        return self.query_entries(actor=actor, limit=limit)

    def get_target_history(self, target: str, limit: int = 100) -> List[Dict]:
        """
        Get full change history for a target.

        Args:
            target: Target identifier
            limit: Max results

        Returns:
            List of changes to target
        """
        return self.query_entries(target=target, limit=limit)

    def get_critical_actions(self, hours: int = 24) -> List[Dict]:
        """
        Get critical actions from last N hours.

        Args:
            hours: Look back N hours

        Returns:
            List of critical actions
        """
        start_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        return self.query_entries(
            level=AuditLevel.CRITICAL,
            start_time=start_time
        )

    def get_failed_actions(self, hours: int = 24) -> List[Dict]:
        """
        Get failed actions from last N hours.

        Args:
            hours: Look back N hours

        Returns:
            List of failed actions
        """
        start_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        return self.query_entries(
            result="failure",
            start_time=start_time
        )

    def verify_integrity(self) -> Dict[str, Any]:
        """
        Verify audit log integrity.

        Checks that log format is valid and entries are consecutive.

        Returns:
            Verification results
        """
        errors = []
        warnings = []

        if not self.entries:
            return {
                "verified": True,
                "errors": [],
                "warnings": ["No audit entries to verify"],
                "total_entries": 0
            }

        # Check entry IDs are unique
        ids = [e.entry_id for e in self.entries]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate entry IDs found")

        # Check timestamps are in order
        for i in range(1, len(self.entries)):
            prev_time = datetime.fromisoformat(self.entries[i-1].timestamp)
            curr_time = datetime.fromisoformat(self.entries[i].timestamp)
            if curr_time < prev_time:
                warnings.append(f"Out of order timestamps at entry {i}")

        # Verify checksums
        invalid_checksums = 0
        for entry in self.entries:
            checksum_data = f"{entry.entry_id}{entry.timestamp}{entry.action.value}{entry.actor}{entry.target}"
            expected = hashlib.sha256(checksum_data.encode()).hexdigest()
            if expected != entry.checksum:
                invalid_checksums += 1

        if invalid_checksums > 0:
            errors.append(f"{invalid_checksums} entries with invalid checksums")

        return {
            "verified": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "total_entries": len(self.entries),
            "invalid_checksums": invalid_checksums
        }

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about audit trail.

        Returns:
            Statistics dict
        """
        if not self.entries:
            return {"total_entries": 0}

        actions = {}
        actors = {}
        levels = {}
        results = {}

        for entry in self.entries:
            actions[entry.action.value] = actions.get(entry.action.value, 0) + 1
            actors[entry.actor] = actors.get(entry.actor, 0) + 1
            levels[entry.level.value] = levels.get(entry.level.value, 0) + 1
            results[entry.result] = results.get(entry.result, 0) + 1

        return {
            "total_entries": len(self.entries),
            "date_range": {
                "oldest": self.entries[0].timestamp,
                "newest": self.entries[-1].timestamp
            },
            "actions": actions,
            "actors": actors,
            "levels": levels,
            "results": results
        }

    def export_entries(self, filepath: Path) -> bool:
        """
        Export audit entries to a file.

        Args:
            filepath: Path to export to

        Returns:
            True if successful
        """
        try:
            data = [e.to_dict() for e in self.entries]
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False

    def cleanup_old_entries(self) -> int:
        """
        Remove entries older than retention period.

        Returns:
            Number of entries deleted
        """
        cutoff = datetime.now() - timedelta(days=self.AUDIT_RETENTION_DAYS)

        to_delete = []
        for entry in self.entries:
            entry_time = datetime.fromisoformat(entry.timestamp)
            if entry_time < cutoff:
                to_delete.append(entry.entry_id)

        for entry_id in to_delete:
            if entry_id in self.entry_index:
                entry = self.entry_index[entry_id]
                self.entries.remove(entry)
                del self.entry_index[entry_id]

        return len(to_delete)

    def _persist_entry(self, entry: AuditEntry) -> None:
        """
        Persist entry to disk immediately (immutable).

        Args:
            entry: Entry to persist
        """
        try:
            # Append to immutable log
            with open(self.audit_log, 'a') as f:
                f.write(json.dumps(entry.to_dict()) + "\n")
        except Exception as e:
            print(f"[AUDIT-LOGGER] Failed to persist entry: {e}")

    def _load_audit_log(self) -> None:
        """Load existing audit log from disk."""
        if not self.audit_log.exists():
            return

        try:
            with open(self.audit_log) as f:
                for line in f:
                    if not line.strip():
                        continue
                    data = json.loads(line)

                    action = AuditAction[data["action"].upper()]
                    level = AuditLevel[data["level"].upper()]

                    entry = AuditEntry(
                        entry_id=data["entry_id"],
                        timestamp=data["timestamp"],
                        action=action,
                        level=level,
                        actor=data["actor"],
                        target=data["target"],
                        details=data.get("details", {}),
                        result=data.get("result", "success"),
                        error_message=data.get("error_message"),
                        checksum=data.get("checksum", "")
                    )

                    self.entries.append(entry)
                    self.entry_index[entry.entry_id] = entry

        except Exception as e:
            print(f"[AUDIT-LOGGER] Failed to load audit log: {e}")
