#!/usr/bin/env python3
"""Tests for Database Migration Framework."""

import pytest
import tempfile
import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from deia.services.database_migration import (
    Migration,
    MigrationRunner,
    DatabaseMigrationService
)


class TestMigration:
    """Test Migration dataclass."""

    def test_create_migration(self):
        """Test creating a migration."""
        m = Migration(
            version="001",
            description="Create users table",
            up_sql="CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)",
            down_sql="DROP TABLE users"
        )

        assert m.version == "001"
        assert m.description == "Create users table"
        assert m.status == "pending"
        assert m.created_at is not None

    def test_migration_with_applied_state(self):
        """Test migration with applied state."""
        m = Migration(
            version="001",
            description="Create table",
            up_sql="CREATE TABLE test (id INTEGER)",
            down_sql="DROP TABLE test",
            status="applied"
        )

        assert m.status == "applied"


class TestMigrationRunner:
    """Test migration execution."""

    @pytest.fixture
    def runner(self):
        """Create temporary database and runner."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            project_root.mkdir(exist_ok=True)
            deia_dir = project_root / ".deia"
            deia_dir.mkdir(exist_ok=True)
            (project_root / ".deia" / "logs").mkdir(exist_ok=True)

            db_path = project_root / "test.db"
            runner = MigrationRunner(db_path, project_root)

            yield runner, project_root, db_path

    def test_runner_initialization(self, runner):
        """Test runner initializes correctly."""
        runner_obj, project_root, db_path = runner

        assert runner_obj.db_path == db_path
        assert (project_root / ".deia" / "migration-metadata.db").exists()

    def test_register_migration(self, runner):
        """Test registering a migration."""
        runner_obj, _, _ = runner

        m = Migration(
            version="001",
            description="Create users",
            up_sql="CREATE TABLE users (id INTEGER, name TEXT)",
            down_sql="DROP TABLE users"
        )

        success = runner_obj.register_migration(m)
        assert success is True

    def test_register_duplicate_migration(self, runner):
        """Test duplicate migration registration."""
        runner_obj, _, _ = runner

        m = Migration(
            version="001",
            description="Create users",
            up_sql="CREATE TABLE users (id INTEGER)",
            down_sql="DROP TABLE users"
        )

        assert runner_obj.register_migration(m) is True
        # Duplicate should fail silently
        assert runner_obj.register_migration(m) is False

    def test_get_applied_versions(self, runner):
        """Test getting applied versions."""
        runner_obj, _, _ = runner

        # Register migrations
        m1 = Migration("001", "Create users", "CREATE TABLE users (id INTEGER)", "DROP TABLE users")
        m2 = Migration("002", "Create posts", "CREATE TABLE posts (id INTEGER)", "DROP TABLE posts")

        runner_obj.register_migration(m1)
        runner_obj.register_migration(m2)

        # Initially no applied versions
        assert len(runner_obj.get_applied_versions()) == 0

    def test_get_pending_migrations(self, runner):
        """Test getting pending migrations."""
        runner_obj, _, _ = runner

        m1 = Migration("001", "Create users", "CREATE TABLE users (id INTEGER)", "DROP TABLE users")
        m2 = Migration("002", "Create posts", "CREATE TABLE posts (id INTEGER)", "DROP TABLE posts")

        runner_obj.register_migration(m1)
        runner_obj.register_migration(m2)

        pending = runner_obj.get_pending_migrations()
        assert len(pending) == 2
        assert pending[0].version == "001"
        assert pending[1].version == "002"

    def test_apply_migration(self, runner):
        """Test applying a migration."""
        runner_obj, _, db_path = runner

        m = Migration(
            version="001",
            description="Create users",
            up_sql="CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)",
            down_sql="DROP TABLE users"
        )

        runner_obj.register_migration(m)
        success, message = runner_obj.apply_migration(m)

        assert success is True
        assert "applied" in message.lower()

        # Verify table exists
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None
        conn.close()

    def test_apply_migration_dry_run(self, runner):
        """Test dry-run migration."""
        runner_obj, _, _ = runner

        m = Migration(
            version="001",
            description="Create users",
            up_sql="CREATE TABLE users (id INTEGER)",
            down_sql="DROP TABLE users"
        )

        success, message = runner_obj.apply_migration(m, dry_run=True)
        assert success is True
        assert "dry-run" in message.lower()

    def test_apply_invalid_migration(self, runner):
        """Test applying invalid SQL migration."""
        runner_obj, _, _ = runner

        m = Migration(
            version="001",
            description="Invalid SQL",
            up_sql="INVALID SQL SYNTAX ;;;",
            down_sql="DROP TABLE test"
        )

        success, message = runner_obj.apply_migration(m)
        assert success is False
        assert "failed" in message.lower() or "error" in message.lower()

    def test_rollback_migration(self, runner):
        """Test rolling back a migration."""
        runner_obj, _, db_path = runner

        m = Migration(
            version="001",
            description="Create users",
            up_sql="CREATE TABLE users (id INTEGER)",
            down_sql="DROP TABLE users"
        )

        runner_obj.register_migration(m)
        runner_obj.apply_migration(m)

        # Rollback
        success, message = runner_obj.rollback_migration("001")
        assert success is True

        # Verify table no longer exists
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is None
        conn.close()

    def test_rollback_pending_migration(self, runner):
        """Test rollback of pending migration fails."""
        runner_obj, _, _ = runner

        m = Migration(
            version="001",
            description="Create table",
            up_sql="CREATE TABLE test (id INTEGER)",
            down_sql="DROP TABLE test"
        )

        runner_obj.register_migration(m)

        # Try to rollback pending migration
        success, message = runner_obj.rollback_migration("001")
        assert success is False

    def test_rollback_dry_run(self, runner):
        """Test dry-run rollback with simple schema."""
        runner_obj, _, db_path = runner

        # Use simple SQL that works on empty in-memory DB for dry-run
        m = Migration(
            version="001",
            description="Create table",
            up_sql="CREATE TABLE test (id INTEGER)",
            down_sql="DROP TABLE IF EXISTS test"  # IF EXISTS allows dry-run on empty DB
        )

        runner_obj.register_migration(m)
        success, msg = runner_obj.apply_migration(m)
        assert success is True, f"Migration apply failed: {msg}"

        # Verify status in metadata
        conn = sqlite3.connect(str(runner_obj.metadata_db))
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM migrations WHERE version = '001'")
        status = cursor.fetchone()[0]
        conn.close()
        assert status == "applied", f"Migration status is {status}, expected 'applied'"

        # Dry-run rollback (tests on empty in-memory DB)
        success, message = runner_obj.rollback_migration("001", dry_run=True)
        assert success is True, f"Dry-run rollback failed: {message}"
        assert "dry-run" in message.lower()

    def test_apply_all_pending(self, runner):
        """Test applying all pending migrations."""
        runner_obj, _, db_path = runner

        m1 = Migration("001", "Create users", "CREATE TABLE users (id INTEGER)", "DROP TABLE users")
        m2 = Migration("002", "Create posts", "CREATE TABLE posts (id INTEGER)", "DROP TABLE posts")

        runner_obj.register_migration(m1)
        runner_obj.register_migration(m2)

        result = runner_obj.apply_all_pending()

        assert result["total"] == 2
        assert result["applied"] == 2
        assert result["failed"] == 0

        # Verify tables exist
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        count = cursor.fetchone()[0]
        conn.close()

        assert count >= 2

    def test_apply_all_pending_with_failure(self, runner):
        """Test apply all stops on first failure."""
        runner_obj, _, _ = runner

        m1 = Migration("001", "Create users", "CREATE TABLE users (id INTEGER)", "DROP TABLE users")
        m2 = Migration("002", "Invalid", "INVALID SQL ;;;", "DROP TABLE test")

        runner_obj.register_migration(m1)
        runner_obj.register_migration(m2)

        result = runner_obj.apply_all_pending()

        assert result["total"] == 2
        assert result["applied"] == 1
        assert result["failed"] == 1

    def test_detect_conflicts(self, runner):
        """Test conflict detection."""
        runner_obj, _, _ = runner

        # Register two migrations
        m1 = Migration("001", "Create users", "CREATE TABLE users (id INTEGER)", "DROP TABLE users")
        m2 = Migration("002", "Create posts", "CREATE TABLE posts (id INTEGER)", "DROP TABLE posts")

        runner_obj.register_migration(m1)
        runner_obj.register_migration(m2)

        conflicts = runner_obj.detect_conflicts()
        assert isinstance(conflicts, list)

    def test_get_migration_status(self, runner):
        """Test getting migration status."""
        runner_obj, _, _ = runner

        m1 = Migration("001", "Create users", "CREATE TABLE users (id INTEGER)", "DROP TABLE users")
        m2 = Migration("002", "Create posts", "CREATE TABLE posts (id INTEGER)", "DROP TABLE posts")

        runner_obj.register_migration(m1)
        runner_obj.register_migration(m2)

        status = runner_obj.get_migration_status()

        assert status["pending"] == 2
        assert status["applied"] == 0
        assert status["total"] == 2
        assert len(status["history"]) == 2


class TestDatabaseMigrationService:
    """Test high-level migration service."""

    @pytest.fixture
    def service(self):
        """Create migration service."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".deia").mkdir()
            (project_root / ".deia" / "logs").mkdir()

            db_path = project_root / "test.db"
            service = DatabaseMigrationService(db_path, project_root)

            yield service, db_path

    def test_create_migration(self, service):
        """Test creating migration via service."""
        svc, _ = service

        success = svc.create_migration(
            version="001",
            description="Create users",
            up_sql="CREATE TABLE users (id INTEGER)",
            down_sql="DROP TABLE users"
        )

        assert success is True

    def test_migrate_workflow(self, service):
        """Test full migration workflow."""
        svc, db_path = service

        # Create migrations
        svc.create_migration(
            "001",
            "Create users",
            "CREATE TABLE users (id INTEGER, name TEXT)",
            "DROP TABLE users"
        )

        svc.create_migration(
            "002",
            "Create posts",
            "CREATE TABLE posts (id INTEGER, user_id INTEGER)",
            "DROP TABLE posts"
        )

        # Run migrations
        result = svc.migrate()
        assert result["applied"] == 2
        assert result["failed"] == 0

        # Check status
        status = svc.status()
        assert status["applied"] == 2
        assert status["pending"] == 0

    def test_rollback_workflow(self, service):
        """Test rollback workflow."""
        svc, db_path = service

        svc.create_migration(
            "001",
            "Create users",
            "CREATE TABLE users (id INTEGER)",
            "DROP TABLE users"
        )

        svc.migrate()
        success, msg = svc.rollback("001")

        assert success is True

    def test_dry_run_workflow(self, service):
        """Test dry-run workflow."""
        svc, _ = service

        svc.create_migration(
            "001",
            "Create table",
            "CREATE TABLE test (id INTEGER)",
            "DROP TABLE test"
        )

        result = svc.migrate(dry_run=True)
        assert result["dry_run"] is True
        assert result["applied"] == 1

        # Verify not actually applied
        status = svc.status()
        assert status["pending"] == 1

    def test_validate_migrations(self, service):
        """Test validation."""
        svc, _ = service

        svc.create_migration(
            "001",
            "Create table",
            "CREATE TABLE test (id INTEGER)",
            "DROP TABLE test"
        )

        conflicts = svc.validate()
        assert isinstance(conflicts, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
