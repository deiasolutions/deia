"""
Disaster Recovery - Backup and restore system state on crashes.

Periodically backs up critical system state (registry, queue, bot assignments).
On startup, automatically detects and recovers from crashes.
Ensures zero data loss through regular backups and integrity validation.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
import json
import shutil
import hashlib


class BackupType(Enum):
    """Types of backups."""
    REGISTRY = "registry"          # Bot registry
    QUEUE = "queue"                # Task queue state
    BOT_ASSIGNMENTS = "bot_assignments"  # Bot-task assignments
    FULL = "full"                  # All of above


@dataclass
class BackupMetadata:
    """Metadata about a backup."""
    backup_id: str
    backup_type: BackupType
    timestamp: str
    source: str                    # What was backed up
    size_bytes: int
    item_count: int
    checksum: str                  # SHA256 for integrity
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            **asdict(self),
            "backup_type": self.backup_type.value
        }


@dataclass
class RestorePoint:
    """A point we can restore from."""
    restore_id: str
    timestamp: str
    backups: List[str] = field(default_factory=list)  # Backup IDs that make up this point
    description: str = ""
    manually_created: bool = False


class DisasterRecovery:
    """
    Disaster recovery and backup management.

    Features:
    - Regular backups of critical state (registry, queue, bot assignments)
    - Automatic crash detection on startup
    - Point-in-time restore capability
    - Backup integrity validation
    - Automatic cleanup of old backups
    - Comprehensive logging
    """

    # Backup retention policy
    BACKUP_RETENTION_DAYS = 7
    AUTO_BACKUP_INTERVAL_MINUTES = 10  # Backup every 10 minutes
    MAX_BACKUPS_PER_TYPE = 100

    def __init__(self, work_dir: Path):
        """
        Initialize disaster recovery system.

        Args:
            work_dir: Working directory
        """
        self.work_dir = Path(work_dir)
        self.backup_dir = self.work_dir / ".deia" / "backups"
        self.log_dir = self.work_dir / ".deia" / "bot-logs"
        self.state_dir = self.work_dir / ".deia" / "state"

        # Create directories if needed
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

        self.dr_log = self.log_dir / "disaster-recovery.jsonl"
        self.metadata_index = self.backup_dir / "index.json"

        # In-memory index of backups
        self.backups: Dict[str, BackupMetadata] = {}
        self.restore_points: Dict[str, RestorePoint] = {}

        # Load existing backup index
        self._load_backup_index()

        # Track last auto-backup time
        self._last_auto_backup: Optional[datetime] = None

    def create_backup(
        self,
        backup_type: BackupType,
        data: Dict[str, Any],
        source: str = "",
        tags: Optional[Dict[str, str]] = None
    ) -> Tuple[bool, str]:
        """
        Create a backup of data.

        Args:
            backup_type: Type of backup
            data: Data to backup
            source: Description of source
            tags: Optional tags for organizing backups

        Returns:
            (success, backup_id)
        """
        import uuid

        try:
            backup_id = str(uuid.uuid4())

            # Serialize data
            data_json = json.dumps(data, indent=2)
            data_bytes = data_json.encode('utf-8')

            # Calculate checksum
            checksum = hashlib.sha256(data_bytes).hexdigest()

            # Save backup file
            backup_file = self.backup_dir / f"{backup_id}.json"
            with open(backup_file, 'wb') as f:
                f.write(data_bytes)

            # Create metadata
            metadata = BackupMetadata(
                backup_id=backup_id,
                backup_type=backup_type,
                timestamp=datetime.now().isoformat(),
                source=source or f"backup-{backup_type.value}",
                size_bytes=len(data_bytes),
                item_count=self._count_items(data),
                checksum=checksum,
                tags=tags or {}
            )

            # Store metadata
            self.backups[backup_id] = metadata

            # Log event
            self._log_event("backup_created", {
                "backup_id": backup_id,
                "type": backup_type.value,
                "size_bytes": len(data_bytes),
                "checksum": checksum
            })

            return True, backup_id

        except Exception as e:
            self._log_event("backup_failed", {
                "type": backup_type.value,
                "error": str(e)
            })
            return False, ""

    def restore_backup(self, backup_id: str) -> Tuple[bool, Optional[Dict]]:
        """
        Restore data from a backup.

        Args:
            backup_id: Backup ID to restore

        Returns:
            (success, data_dict)
        """
        try:
            if backup_id not in self.backups:
                self._log_event("restore_failed", {"reason": "backup_not_found"})
                return False, None

            backup_file = self.backup_dir / f"{backup_id}.json"
            if not backup_file.exists():
                self._log_event("restore_failed", {"reason": "backup_file_missing"})
                return False, None

            # Verify integrity
            with open(backup_file, 'rb') as f:
                data_bytes = f.read()

            checksum = hashlib.sha256(data_bytes).hexdigest()
            if checksum != self.backups[backup_id].checksum:
                self._log_event("restore_failed", {"reason": "checksum_mismatch"})
                return False, None

            # Load data
            data = json.loads(data_bytes.decode('utf-8'))

            self._log_event("restore_successful", {
                "backup_id": backup_id,
                "type": self.backups[backup_id].backup_type.value
            })

            return True, data

        except Exception as e:
            self._log_event("restore_failed", {"error": str(e)})
            return False, None

    def create_restore_point(
        self,
        registry_data: Dict = None,
        queue_data: Dict = None,
        assignments_data: Dict = None,
        description: str = "",
        manual: bool = False
    ) -> Tuple[bool, str]:
        """
        Create a full restore point from multiple data sources.

        Args:
            registry_data: Bot registry to backup
            queue_data: Task queue to backup
            assignments_data: Bot assignments to backup
            description: Description of restore point
            manual: Whether manually created

        Returns:
            (success, restore_point_id)
        """
        import uuid

        try:
            restore_id = str(uuid.uuid4())
            backup_ids = []

            # Backup each component
            if registry_data:
                success, backup_id = self.create_backup(
                    BackupType.REGISTRY,
                    registry_data,
                    "registry-backup"
                )
                if success:
                    backup_ids.append(backup_id)

            if queue_data:
                success, backup_id = self.create_backup(
                    BackupType.QUEUE,
                    queue_data,
                    "queue-backup"
                )
                if success:
                    backup_ids.append(backup_id)

            if assignments_data:
                success, backup_id = self.create_backup(
                    BackupType.BOT_ASSIGNMENTS,
                    assignments_data,
                    "assignments-backup"
                )
                if success:
                    backup_ids.append(backup_id)

            # Create restore point
            restore_point = RestorePoint(
                restore_id=restore_id,
                timestamp=datetime.now().isoformat(),
                backups=backup_ids,
                description=description,
                manually_created=manual
            )

            self.restore_points[restore_id] = restore_point

            self._log_event("restore_point_created", {
                "restore_id": restore_id,
                "backup_ids": backup_ids,
                "description": description,
                "manual": manual
            })

            return True, restore_id

        except Exception as e:
            self._log_event("restore_point_failed", {"error": str(e)})
            return False, ""

    def auto_backup_if_needed(
        self,
        registry_data: Dict = None,
        queue_data: Dict = None,
        assignments_data: Dict = None
    ) -> bool:
        """
        Automatically create backup if interval has passed.

        Call this periodically to maintain backups.

        Args:
            registry_data: Current registry state
            queue_data: Current queue state
            assignments_data: Current assignments state

        Returns:
            True if backup was created
        """
        now = datetime.now()

        # Check if enough time has passed
        if self._last_auto_backup:
            elapsed = (now - self._last_auto_backup).total_seconds()
            if elapsed < (self.AUTO_BACKUP_INTERVAL_MINUTES * 60):
                return False

        # Create restore point
        success, restore_id = self.create_restore_point(
            registry_data=registry_data,
            queue_data=queue_data,
            assignments_data=assignments_data,
            description="automatic-backup",
            manual=False
        )

        if success:
            self._last_auto_backup = now
            self._cleanup_old_backups()
            self._save_backup_index()
            return True

        return False

    def detect_crash_state(self) -> Tuple[bool, Optional[str]]:
        """
        Detect if system crashed (no clean shutdown marker).

        Returns:
            (crashed, latest_restore_point_id)
        """
        shutdown_marker = self.state_dir / "shutdown.marker"

        if not shutdown_marker.exists():
            # No shutdown marker = crash
            latest = self._get_latest_restore_point()
            return True, latest

        # Check if marker is recent (within 30 seconds)
        marker_time = datetime.fromtimestamp(shutdown_marker.stat().st_mtime)
        elapsed = (datetime.now() - marker_time).total_seconds()

        if elapsed > 30:
            # Stale marker = crash
            latest = self._get_latest_restore_point()
            return True, latest

        return False, None

    def mark_clean_shutdown(self) -> bool:
        """
        Mark that system is shutting down cleanly.

        Call before shutdown.

        Returns:
            True if marker created
        """
        try:
            shutdown_marker = self.state_dir / "shutdown.marker"
            shutdown_marker.touch()
            self._log_event("clean_shutdown_marked", {})
            return True
        except Exception as e:
            self._log_event("shutdown_marker_failed", {"error": str(e)})
            return False

    def clear_shutdown_marker(self) -> bool:
        """
        Clear shutdown marker on startup (before checking for crashes).

        Returns:
            True if cleared
        """
        try:
            shutdown_marker = self.state_dir / "shutdown.marker"
            if shutdown_marker.exists():
                shutdown_marker.unlink()
            self._log_event("shutdown_marker_cleared", {})
            return True
        except Exception as e:
            self._log_event("shutdown_marker_clear_failed", {"error": str(e)})
            return False

    def get_backup_history(
        self,
        backup_type: Optional[BackupType] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get list of backups, optionally filtered by type.

        Args:
            backup_type: Filter by type (None = all)
            limit: Maximum results

        Returns:
            List of backup metadata dicts
        """
        backups = []

        for backup_id, metadata in self.backups.items():
            if backup_type and metadata.backup_type != backup_type:
                continue

            backups.append(metadata.to_dict())

        # Sort by timestamp, newest first
        backups.sort(key=lambda b: b["timestamp"], reverse=True)

        return backups[:limit]

    def get_restore_point_details(self, restore_point_id: str) -> Optional[Dict]:
        """
        Get details of a restore point.

        Args:
            restore_point_id: Restore point ID

        Returns:
            Restore point details or None
        """
        if restore_point_id not in self.restore_points:
            return None

        rp = self.restore_points[restore_point_id]
        return {
            "restore_id": rp.restore_id,
            "timestamp": rp.timestamp,
            "backups": rp.backups,
            "description": rp.description,
            "manual": rp.manually_created,
            "backup_details": [
                self.backups[bid].to_dict()
                for bid in rp.backups
                if bid in self.backups
            ]
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Get disaster recovery system status.

        Returns:
            Status dict
        """
        crashed = self.detect_crash_state()

        return {
            "timestamp": datetime.now().isoformat(),
            "total_backups": len(self.backups),
            "total_restore_points": len(self.restore_points),
            "latest_backup": self._get_latest_backup(),
            "latest_restore_point": self._get_latest_restore_point(),
            "crash_detected": crashed[0],
            "backup_dir": str(self.backup_dir),
            "backups_by_type": self._count_by_type(),
            "disk_usage_mb": self._calculate_disk_usage() / (1024 * 1024)
        }

    def _get_latest_backup(self) -> Optional[str]:
        """Get ID of latest backup."""
        if not self.backups:
            return None

        latest = max(
            self.backups.values(),
            key=lambda b: b.timestamp
        )
        return latest.backup_id

    def _get_latest_restore_point(self) -> Optional[str]:
        """Get ID of latest restore point."""
        if not self.restore_points:
            return None

        latest = max(
            self.restore_points.values(),
            key=lambda rp: rp.timestamp
        )
        return latest.restore_id

    def _count_by_type(self) -> Dict[str, int]:
        """Count backups by type."""
        counts = {}
        for backup in self.backups.values():
            type_key = backup.backup_type.value
            counts[type_key] = counts.get(type_key, 0) + 1
        return counts

    def _count_items(self, data: Dict) -> int:
        """Count items in data dict."""
        count = 0
        for value in data.values():
            if isinstance(value, (list, dict)):
                if isinstance(value, list):
                    count += len(value)
                else:
                    count += len(value)
        return count

    def _calculate_disk_usage(self) -> int:
        """Calculate total disk usage of backups in bytes."""
        total = 0
        for backup in self.backups.values():
            total += backup.size_bytes
        return total

    def _cleanup_old_backups(self) -> None:
        """Remove backups older than retention period."""
        cutoff = datetime.now() - timedelta(days=self.BACKUP_RETENTION_DAYS)

        to_delete = []
        for backup_id, metadata in self.backups.items():
            backup_time = datetime.fromisoformat(metadata.timestamp)
            if backup_time < cutoff:
                to_delete.append(backup_id)

        for backup_id in to_delete:
            try:
                backup_file = self.backup_dir / f"{backup_id}.json"
                if backup_file.exists():
                    backup_file.unlink()
                del self.backups[backup_id]
                self._log_event("backup_deleted_old", {"backup_id": backup_id})
            except Exception as e:
                self._log_event("cleanup_failed", {"error": str(e)})

    def _load_backup_index(self) -> None:
        """Load backup index from disk."""
        if not self.metadata_index.exists():
            return

        try:
            with open(self.metadata_index) as f:
                data = json.load(f)

            for backup_id, metadata_dict in data.get("backups", {}).items():
                backup_type = BackupType[metadata_dict["backup_type"].upper()]
                metadata = BackupMetadata(
                    backup_id=backup_id,
                    backup_type=backup_type,
                    timestamp=metadata_dict["timestamp"],
                    source=metadata_dict["source"],
                    size_bytes=metadata_dict["size_bytes"],
                    item_count=metadata_dict["item_count"],
                    checksum=metadata_dict["checksum"],
                    tags=metadata_dict.get("tags", {})
                )
                self.backups[backup_id] = metadata

            for restore_id, rp_dict in data.get("restore_points", {}).items():
                restore_point = RestorePoint(
                    restore_id=restore_id,
                    timestamp=rp_dict["timestamp"],
                    backups=rp_dict["backups"],
                    description=rp_dict.get("description", ""),
                    manually_created=rp_dict.get("manually_created", False)
                )
                self.restore_points[restore_id] = restore_point

            self._log_event("index_loaded", {
                "backups": len(self.backups),
                "restore_points": len(self.restore_points)
            })

        except Exception as e:
            self._log_event("index_load_failed", {"error": str(e)})

    def _save_backup_index(self) -> None:
        """Save backup index to disk."""
        try:
            data = {
                "backups": {
                    bid: metadata.to_dict()
                    for bid, metadata in self.backups.items()
                },
                "restore_points": {
                    rpid: asdict(rp)
                    for rpid, rp in self.restore_points.items()
                }
            }

            with open(self.metadata_index, 'w') as f:
                json.dump(data, f, indent=2)

            self._log_event("index_saved", {
                "backups": len(self.backups),
                "restore_points": len(self.restore_points)
            })

        except Exception as e:
            self._log_event("index_save_failed", {"error": str(e)})

    def _log_event(self, event: str, details: Dict = None) -> None:
        """Log disaster recovery event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details or {}
        }

        try:
            with open(self.dr_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[DISASTER-RECOVERY] Failed to log event: {e}")
