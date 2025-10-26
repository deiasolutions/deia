#!/usr/bin/env python3
"""Database Migration Framework: Version control for schemas.

Supports:
- Schema versioning with up/down migrations
- Atomic migration application with transaction safety
- Rollback capability
- Migration status tracking
- Dry-run mode for testing
- Conflict detection
"""

import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - DATABASE-MIGRATION - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Migration:
    """Represents a single migration."""
    version: str  # e.g., "001"
    description: str
    up_sql: str  # SQL to apply
    down_sql: str  # SQL to rollback
    created_at: str = None
    applied_at: str = None
    status: str = "pending"  # pending, applied, failed, rolled_back

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat() + "Z"


class MigrationRunner:
    """Executes migrations with safety guarantees."""

    def __init__(self, db_path: Path, project_root: Path = None):
        """Initialize migration runner.

        Args:
            db_path: Path to SQLite database
            project_root: Project root for migrations directory
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.db_path = db_path
        self.project_root = project_root
        self.migrations_dir = project_root / ".deia" / "migrations"
        self.migrations_dir.mkdir(parents=True, exist_ok=True)

        # Migration metadata database
        self.metadata_db = project_root / ".deia" / "migration-metadata.db"
        self.migration_log = project_root / ".deia" / "logs" / "migrations.jsonl"
        self.migration_log.parent.mkdir(parents=True, exist_ok=True)

        # Initialize metadata DB
        self._init_metadata_db()
        logger.info(f"MigrationRunner initialized: {db_path}")

    def _init_metadata_db(self):
        """Initialize metadata database for tracking migrations."""
        try:
            conn = sqlite3.connect(str(self.metadata_db))
            cursor = conn.cursor()

            # Create migrations table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version TEXT UNIQUE NOT NULL,
                    description TEXT,
                    up_sql TEXT,
                    down_sql TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT,
                    applied_at TEXT,
                    rolled_back_at TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to initialize metadata DB: {e}")
            raise

    def register_migration(self, migration: Migration) -> bool:
        """Register a migration in the system.

        Args:
            migration: Migration object to register

        Returns:
            True if registered successfully
        """
        try:
            conn = sqlite3.connect(str(self.metadata_db))
            cursor = conn.cursor()

            # Check if already exists
            cursor.execute("SELECT id FROM migrations WHERE version = ?", (migration.version,))
            if cursor.fetchone():
                logger.warning(f"Migration {migration.version} already exists")
                conn.close()
                return False

            cursor.execute("""
                INSERT INTO migrations
                (version, description, up_sql, down_sql, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                migration.version,
                migration.description,
                migration.up_sql,
                migration.down_sql,
                migration.status,
                migration.created_at
            ))
            conn.commit()
            conn.close()

            logger.info(f"Migration {migration.version} registered")
            return True
        except Exception as e:
            logger.error(f"Failed to register migration: {e}")
            return False

    def get_applied_versions(self) -> List[str]:
        """Get list of applied migration versions."""
        try:
            conn = sqlite3.connect(str(self.metadata_db))
            cursor = conn.cursor()

            cursor.execute(
                "SELECT version FROM migrations WHERE status = 'applied' ORDER BY version"
            )
            versions = [row[0] for row in cursor.fetchall()]
            conn.close()

            return versions
        except Exception as e:
            logger.error(f"Failed to get applied versions: {e}")
            return []

    def get_pending_migrations(self) -> List[Migration]:
        """Get list of pending migrations."""
        try:
            conn = sqlite3.connect(str(self.metadata_db))
            cursor = conn.cursor()

            cursor.execute(
                "SELECT version, description, up_sql, down_sql, created_at, status "
                "FROM migrations WHERE status = 'pending' ORDER BY version"
            )

            migrations = []
            for row in cursor.fetchall():
                m = Migration(
                    version=row[0],
                    description=row[1],
                    up_sql=row[2],
                    down_sql=row[3],
                    created_at=row[4],
                    status=row[5]
                )
                migrations.append(m)

            conn.close()
            return migrations
        except Exception as e:
            logger.error(f"Failed to get pending migrations: {e}")
            return []

    def apply_migration(self, migration: Migration, dry_run: bool = False) -> Tuple[bool, str]:
        """Apply a single migration.

        Args:
            migration: Migration to apply
            dry_run: If True, don't persist changes

        Returns:
            Tuple of (success, message)
        """
        if dry_run:
            logger.info(f"[DRY-RUN] Would apply migration {migration.version}")
            try:
                conn = sqlite3.connect(":memory:")
                cursor = conn.cursor()
                cursor.execute(migration.up_sql)
                conn.close()
                return True, f"Dry-run successful for {migration.version}"
            except Exception as e:
                return False, f"Dry-run failed: {str(e)}"

        try:
            # Apply to main database with transaction
            conn = sqlite3.connect(str(self.db_path))
            conn.isolation_level = None  # Autocommit off
            cursor = conn.cursor()

            try:
                cursor.execute("BEGIN TRANSACTION")
                cursor.execute(migration.up_sql)
                cursor.execute("COMMIT")

                # Update metadata
                metadata_conn = sqlite3.connect(str(self.metadata_db))
                metadata_cursor = metadata_conn.cursor()
                metadata_cursor.execute(
                    "UPDATE migrations SET status = 'applied', applied_at = ? WHERE version = ?",
                    (datetime.utcnow().isoformat() + "Z", migration.version)
                )
                metadata_conn.commit()
                metadata_conn.close()

                # Log migration
                self._log_migration(migration, "applied", None)
                logger.info(f"Migration {migration.version} applied successfully")
                return True, f"Applied {migration.version}"

            except Exception as e:
                cursor.execute("ROLLBACK")
                metadata_conn = sqlite3.connect(str(self.metadata_db))
                metadata_cursor = metadata_conn.cursor()
                metadata_cursor.execute(
                    "UPDATE migrations SET status = 'failed' WHERE version = ?",
                    (migration.version,)
                )
                metadata_conn.commit()
                metadata_conn.close()

                self._log_migration(migration, "failed", str(e))
                logger.error(f"Migration {migration.version} failed: {e}")
                return False, f"Failed: {str(e)}"

            finally:
                conn.close()

        except Exception as e:
            logger.error(f"Database error: {e}")
            return False, f"Database error: {str(e)}"

    def rollback_migration(self, version: str, dry_run: bool = False) -> Tuple[bool, str]:
        """Rollback a migration.

        Args:
            version: Migration version to rollback
            dry_run: If True, don't persist changes

        Returns:
            Tuple of (success, message)
        """
        # Get migration details
        try:
            conn = sqlite3.connect(str(self.metadata_db))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT down_sql, status FROM migrations WHERE version = ?",
                (version,)
            )
            row = cursor.fetchone()
            conn.close()

            if not row:
                return False, f"Migration {version} not found"

            down_sql, status = row

            if status != "applied":
                return False, f"Cannot rollback: migration {version} is {status}"

            if dry_run:
                logger.info(f"[DRY-RUN] Would rollback migration {version}")
                try:
                    conn = sqlite3.connect(":memory:")
                    cursor = conn.cursor()
                    cursor.execute(down_sql)
                    conn.close()
                    return True, f"Dry-run rollback successful for {version}"
                except Exception as e:
                    return False, f"Dry-run rollback failed: {str(e)}"

            # Execute rollback with transaction
            conn = sqlite3.connect(str(self.db_path))
            conn.isolation_level = None
            cursor = conn.cursor()

            try:
                cursor.execute("BEGIN TRANSACTION")
                cursor.execute(down_sql)
                cursor.execute("COMMIT")

                # Update metadata
                metadata_conn = sqlite3.connect(str(self.metadata_db))
                metadata_cursor = metadata_conn.cursor()
                metadata_cursor.execute(
                    "UPDATE migrations SET status = 'rolled_back', rolled_back_at = ? WHERE version = ?",
                    (datetime.utcnow().isoformat() + "Z", version)
                )
                metadata_conn.commit()
                metadata_conn.close()

                logger.info(f"Migration {version} rolled back successfully")
                return True, f"Rolled back {version}"

            except Exception as e:
                cursor.execute("ROLLBACK")
                logger.error(f"Rollback failed: {e}")
                return False, f"Rollback failed: {str(e)}"

            finally:
                conn.close()

        except Exception as e:
            logger.error(f"Error during rollback: {e}")
            return False, f"Error: {str(e)}"

    def apply_all_pending(self, dry_run: bool = False) -> Dict:
        """Apply all pending migrations in order.

        Args:
            dry_run: If True, don't persist changes

        Returns:
            Dict with results
        """
        pending = self.get_pending_migrations()

        if not pending:
            return {
                "total": 0,
                "applied": 0,
                "failed": 0,
                "results": []
            }

        results = []
        applied_count = 0
        failed_count = 0

        for migration in pending:
            success, message = self.apply_migration(migration, dry_run)
            results.append({
                "version": migration.version,
                "success": success,
                "message": message
            })

            if success:
                applied_count += 1
            else:
                failed_count += 1
                # Stop on first failure to maintain consistency
                break

        return {
            "total": len(pending),
            "applied": applied_count,
            "failed": failed_count,
            "dry_run": dry_run,
            "results": results
        }

    def detect_conflicts(self) -> List[str]:
        """Detect migration conflicts (e.g., overlapping versions).

        Returns:
            List of conflict descriptions
        """
        try:
            conn = sqlite3.connect(str(self.metadata_db))
            cursor = conn.cursor()

            conflicts = []

            # Check for duplicate versions
            cursor.execute(
                "SELECT version, COUNT(*) as count FROM migrations GROUP BY version HAVING count > 1"
            )

            for row in cursor.fetchall():
                conflicts.append(f"Duplicate migration version: {row[0]}")

            # Check for out-of-order applied migrations
            cursor.execute(
                "SELECT version FROM migrations WHERE status = 'applied' ORDER BY version"
            )
            applied = [row[0] for row in cursor.fetchall()]

            # Simple version ordering check
            for i in range(len(applied) - 1):
                if applied[i] >= applied[i+1]:
                    conflicts.append(f"Out-of-order migrations: {applied[i]} >= {applied[i+1]}")

            conn.close()
            return conflicts

        except Exception as e:
            logger.error(f"Error detecting conflicts: {e}")
            return []

    def get_migration_status(self) -> Dict:
        """Get overall migration status.

        Returns:
            Dict with migration counts and history
        """
        try:
            conn = sqlite3.connect(str(self.metadata_db))
            cursor = conn.cursor()

            cursor.execute("SELECT status, COUNT(*) FROM migrations GROUP BY status")
            status_counts = {row[0]: row[1] for row in cursor.fetchall()}

            cursor.execute("SELECT version, status, applied_at FROM migrations ORDER BY version")
            history = [
                {
                    "version": row[0],
                    "status": row[1],
                    "applied_at": row[2]
                }
                for row in cursor.fetchall()
            ]

            conn.close()

            return {
                "pending": status_counts.get("pending", 0),
                "applied": status_counts.get("applied", 0),
                "failed": status_counts.get("failed", 0),
                "rolled_back": status_counts.get("rolled_back", 0),
                "total": sum(status_counts.values()),
                "history": history
            }
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return {}

    def _log_migration(self, migration: Migration, status: str, error: Optional[str]):
        """Log migration event."""
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "version": migration.version,
                "description": migration.description,
                "status": status,
                "error": error
            }

            with open(self.migration_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to log migration: {e}")


class DatabaseMigrationService:
    """High-level service for managing database migrations."""

    def __init__(self, db_path: Path, project_root: Path = None):
        """Initialize migration service."""
        self.runner = MigrationRunner(db_path, project_root)
        logger.info("DatabaseMigrationService initialized")

    def create_migration(self, version: str, description: str, up_sql: str, down_sql: str) -> bool:
        """Create and register a new migration.

        Args:
            version: Semantic version (e.g., "001", "002")
            description: Migration description
            up_sql: SQL to apply
            down_sql: SQL to rollback

        Returns:
            True if created successfully
        """
        migration = Migration(
            version=version,
            description=description,
            up_sql=up_sql,
            down_sql=down_sql
        )
        return self.runner.register_migration(migration)

    def migrate(self, dry_run: bool = False) -> Dict:
        """Run all pending migrations."""
        return self.runner.apply_all_pending(dry_run)

    def rollback(self, version: str, dry_run: bool = False) -> Tuple[bool, str]:
        """Rollback a specific migration."""
        return self.runner.rollback_migration(version, dry_run)

    def status(self) -> Dict:
        """Get migration status."""
        return self.runner.get_migration_status()

    def validate(self) -> List[str]:
        """Check for conflicts and issues."""
        return self.runner.detect_conflicts()
