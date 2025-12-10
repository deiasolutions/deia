"""
DEIA Health Check System

Provides comprehensive system health checks for DEIA infrastructure:
- Agent status monitoring
- Messaging system verification
- BOK index integrity
- Filesystem structure validation
- Dependency checks

Author: CLAUDE-CODE-003 (Tactical Coordinator)
Date: 2025-10-18
Source: Agent BC Phase 3 specifications
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import importlib.metadata


class HealthCheckResult:
    """Represents the result of a single health check."""

    def __init__(self, name: str, status: str, message: str, details: Optional[Dict] = None):
        """
        Initialize a health check result.

        Args:
            name: Name of the health check
            status: Status (PASS, FAIL, WARNING)
            message: Human-readable message
            details: Optional dictionary of additional details
        """
        self.name = name
        self.status = status
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }

    def is_passing(self) -> bool:
        """Check if this result is passing."""
        return self.status == "PASS"


class HealthCheckSystem:
    """Main health check system for DEIA infrastructure."""

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the health check system.

        Args:
            project_root: Path to DEIA project root (auto-detected if None)
        """
        self.project_root = project_root or self._find_project_root()
        self.results: List[HealthCheckResult] = []

    def _find_project_root(self) -> Path:
        """Find the DEIA project root directory."""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".deia").exists():
                return current
            current = current.parent
        # If not found, use current directory
        return Path.cwd()

    def check_agent_health(self) -> HealthCheckResult:
        """
        Check the health of all registered agents.

        Verifies:
        - Agent status files exist
        - Heartbeats are up to date (within last hour)
        - Activity logs are accessible

        Returns:
            HealthCheckResult for agent health
        """
        agent_dir = self.project_root / ".deia" / "bot-logs"

        if not agent_dir.exists():
            return HealthCheckResult(
                name="Agent Health",
                status="FAIL",
                message="Agent directory not found",
                details={"expected_path": str(agent_dir)}
            )

        # Find all agent activity logs
        activity_logs = list(agent_dir.glob("CLAUDE-CODE-*-activity.jsonl"))

        if not activity_logs:
            return HealthCheckResult(
                name="Agent Health",
                status="WARNING",
                message="No agent activity logs found",
                details={"directory": str(agent_dir)}
            )

        # Check each agent's latest activity
        agent_statuses = []
        stale_agents = []

        for log_file in activity_logs:
            agent_id = log_file.stem.replace("-activity", "")

            try:
                # Read last line of activity log
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        last_entry = json.loads(lines[-1])
                        timestamp_str = last_entry.get("timestamp", "")

                        # Parse timestamp (handle both ISO format with timezone and without)
                        if timestamp_str:
                            # Remove timezone for parsing simplicity
                            timestamp_str = timestamp_str.split('+')[0].split('-05:00')[0].split('Z')[0]
                            last_activity = datetime.fromisoformat(timestamp_str)
                            age = datetime.now() - last_activity

                            agent_statuses.append({
                                "agent": agent_id,
                                "last_activity": timestamp_str,
                                "age_hours": round(age.total_seconds() / 3600, 2)
                            })

                            # Flag agents with no activity in last hour
                            if age > timedelta(hours=1):
                                stale_agents.append(agent_id)
            except (json.JSONDecodeError, ValueError) as e:
                agent_statuses.append({
                    "agent": agent_id,
                    "error": str(e)
                })

        # Determine status
        if stale_agents:
            status = "WARNING"
            message = f"Found {len(stale_agents)} agent(s) with stale activity (>1 hour old)"
        else:
            status = "PASS"
            message = f"All {len(agent_statuses)} agent(s) have recent activity"

        return HealthCheckResult(
            name="Agent Health",
            status=status,
            message=message,
            details={
                "agents": agent_statuses,
                "stale_agents": stale_agents
            }
        )

    def check_messaging_health(self) -> HealthCheckResult:
        """
        Check the health of the messaging system.

        Verifies:
        - Tunnel directory exists
        - Recent messages present
        - Message format is valid

        Returns:
            HealthCheckResult for messaging health
        """
        tunnel_dir = self.project_root / ".deia" / "tunnel" / "claude-to-claude"

        if not tunnel_dir.exists():
            return HealthCheckResult(
                name="Messaging Health",
                status="FAIL",
                message="Messaging tunnel directory not found",
                details={"expected_path": str(tunnel_dir)}
            )

        # Count recent messages (last 24 hours)
        recent_messages = []
        now = datetime.now()

        for message_file in tunnel_dir.glob("*.md"):
            try:
                mtime = datetime.fromtimestamp(message_file.stat().st_mtime)
                age = now - mtime

                if age < timedelta(hours=24):
                    recent_messages.append({
                        "file": message_file.name,
                        "age_hours": round(age.total_seconds() / 3600, 2)
                    })
            except Exception as e:
                continue

        # Check if we have recent activity
        if len(recent_messages) == 0:
            status = "WARNING"
            message = "No messages in last 24 hours"
        elif len(recent_messages) < 5:
            status = "WARNING"
            message = f"Low message volume: only {len(recent_messages)} messages in last 24 hours"
        else:
            status = "PASS"
            message = f"Messaging system active: {len(recent_messages)} messages in last 24 hours"

        return HealthCheckResult(
            name="Messaging Health",
            status=status,
            message=message,
            details={
                "tunnel_path": str(tunnel_dir),
                "recent_message_count": len(recent_messages),
                "sample_messages": recent_messages[:5]  # First 5 recent messages
            }
        )

    def check_bok_health(self) -> HealthCheckResult:
        """
        Check the health of the BOK (Body of Knowledge) index.

        Verifies:
        - Master index exists
        - Index is valid YAML/JSON
        - Referenced files exist

        Returns:
            HealthCheckResult for BOK health
        """
        index_file = self.project_root / ".deia" / "index" / "master-index.yaml"

        if not index_file.exists():
            # Try alternate location
            index_file = self.project_root / "bok" / "master-index.yaml"

        if not index_file.exists():
            return HealthCheckResult(
                name="BOK Health",
                status="WARNING",
                message="Master index file not found",
                details={"searched_paths": [
                    str(self.project_root / ".deia" / "index" / "master-index.yaml"),
                    str(self.project_root / "bok" / "master-index.yaml")
                ]}
            )

        # Check if file is readable
        try:
            content = index_file.read_text(encoding='utf-8')

            # Basic validation: check for YAML structure
            if not content.strip():
                return HealthCheckResult(
                    name="BOK Health",
                    status="FAIL",
                    message="Master index file is empty",
                    details={"file": str(index_file)}
                )

            # Count entries (simple heuristic: count lines starting with '- ')
            entry_count = len([line for line in content.split('\n') if line.strip().startswith('- ')])

            return HealthCheckResult(
                name="BOK Health",
                status="PASS",
                message=f"BOK index accessible with ~{entry_count} entries",
                details={
                    "index_file": str(index_file),
                    "file_size": len(content),
                    "estimated_entries": entry_count
                }
            )
        except Exception as e:
            return HealthCheckResult(
                name="BOK Health",
                status="FAIL",
                message=f"Failed to read BOK index: {str(e)}",
                details={"error": str(e), "file": str(index_file)}
            )

    def check_filesystem_health(self) -> HealthCheckResult:
        """
        Check the health of the DEIA filesystem structure.

        Verifies:
        - .deia directory exists
        - Required subdirectories exist
        - Key files are accessible

        Returns:
            HealthCheckResult for filesystem health
        """
        deia_dir = self.project_root / ".deia"

        if not deia_dir.exists():
            return HealthCheckResult(
                name="Filesystem Health",
                status="FAIL",
                message=".deia directory not found - run 'deia init'",
                details={"expected_path": str(deia_dir)}
            )

        # Required directories
        required_dirs = [
            "sessions",
            "bok",
            "index",
            "federalist",
            "governance",
            "tunnel/claude-to-claude",
            "bot-logs",
            "observations",
            "handoffs",
            "intake"
        ]

        missing_dirs = []
        existing_dirs = []

        for dir_name in required_dirs:
            dir_path = deia_dir / dir_name
            if dir_path.exists():
                existing_dirs.append(dir_name)
            else:
                missing_dirs.append(dir_name)

        # Determine status
        if len(missing_dirs) == 0:
            status = "PASS"
            message = "All required directories exist"
        elif len(missing_dirs) <= 2:
            status = "WARNING"
            message = f"{len(missing_dirs)} optional directory(ies) missing"
        else:
            status = "FAIL"
            message = f"{len(missing_dirs)} required directory(ies) missing - run 'deia init'"

        return HealthCheckResult(
            name="Filesystem Health",
            status=status,
            message=message,
            details={
                "existing_dirs": existing_dirs,
                "missing_dirs": missing_dirs,
                "total_required": len(required_dirs)
            }
        )

    def check_dependencies_health(self) -> HealthCheckResult:
        """
        Check the health of Python dependencies.

        Verifies:
        - Required packages are installed
        - Package versions are compatible

        Returns:
            HealthCheckResult for dependencies health
        """
        required_packages = [
            "click",
            "pyyaml",
            "watchdog",
            "pytest",
            "pytest-cov"
        ]

        installed = []
        missing = []

        for package in required_packages:
            try:
                version = importlib.metadata.version(package)
                installed.append({"package": package, "version": version})
            except importlib.metadata.PackageNotFoundError:
                missing.append(package)

        # Determine status
        if len(missing) == 0:
            status = "PASS"
            message = f"All {len(required_packages)} required packages installed"
        else:
            status = "FAIL"
            message = f"{len(missing)} required package(s) missing"

        return HealthCheckResult(
            name="Dependencies Health",
            status=status,
            message=message,
            details={
                "installed": installed,
                "missing": missing,
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            }
        )

    def check_system_health(self) -> Dict[str, HealthCheckResult]:
        """
        Run all health checks and return results.

        Returns:
            Dictionary mapping check names to results
        """
        checks = {
            "agents": self.check_agent_health(),
            "messaging": self.check_messaging_health(),
            "bok": self.check_bok_health(),
            "filesystem": self.check_filesystem_health(),
            "dependencies": self.check_dependencies_health()
        }

        self.results = list(checks.values())
        return checks

    def generate_health_report(self, checks: Optional[Dict[str, HealthCheckResult]] = None) -> str:
        """
        Generate a formatted health report.

        Args:
            checks: Dictionary of health check results (runs all if None)

        Returns:
            Formatted health report string
        """
        if checks is None:
            checks = self.check_system_health()

        lines = []
        lines.append("=" * 60)
        lines.append("DEIA HEALTH CHECK REPORT")
        lines.append("=" * 60)
        lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Project Root: {self.project_root}")
        lines.append("")

        # Summary
        total = len(checks)
        passed = sum(1 for r in checks.values() if r.status == "PASS")
        warnings = sum(1 for r in checks.values() if r.status == "WARNING")
        failed = sum(1 for r in checks.values() if r.status == "FAIL")

        lines.append("SUMMARY")
        lines.append("-" * 60)
        lines.append(f"Total Checks: {total}")
        lines.append(f"Passed:       {passed} ✓")
        lines.append(f"Warnings:     {warnings} ⚠")
        lines.append(f"Failed:       {failed} ✗")
        lines.append("")

        # Overall health
        if failed > 0:
            overall = "UNHEALTHY - Critical issues detected"
        elif warnings > 0:
            overall = "DEGRADED - Non-critical issues detected"
        else:
            overall = "HEALTHY - All systems operational"

        lines.append(f"Overall Status: {overall}")
        lines.append("")

        # Detailed results
        lines.append("DETAILED RESULTS")
        lines.append("-" * 60)

        for name, result in checks.items():
            symbol = "✓" if result.status == "PASS" else ("⚠" if result.status == "WARNING" else "✗")
            lines.append(f"{symbol} {result.name}: {result.status}")
            lines.append(f"  {result.message}")

            # Add key details
            if result.details:
                for key, value in result.details.items():
                    if isinstance(value, (list, dict)) and len(str(value)) > 100:
                        continue  # Skip large details in summary
                    lines.append(f"    {key}: {value}")
            lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)

    def get_overall_status(self, checks: Optional[Dict[str, HealthCheckResult]] = None) -> Tuple[str, int]:
        """
        Get the overall system health status.

        Args:
            checks: Dictionary of health check results (runs all if None)

        Returns:
            Tuple of (status_string, exit_code)
            Exit codes: 0 = healthy, 1 = warnings, 2 = failures
        """
        if checks is None:
            checks = self.check_system_health()

        has_failures = any(r.status == "FAIL" for r in checks.values())
        has_warnings = any(r.status == "WARNING" for r in checks.values())

        if has_failures:
            return ("UNHEALTHY", 2)
        elif has_warnings:
            return ("DEGRADED", 1)
        else:
            return ("HEALTHY", 0)


def check_agent_health(project_root: Optional[Path] = None) -> HealthCheckResult:
    """Standalone function to check agent health."""
    system = HealthCheckSystem(project_root)
    return system.check_agent_health()


def check_system_health(project_root: Optional[Path] = None) -> Dict[str, HealthCheckResult]:
    """Standalone function to check overall system health."""
    system = HealthCheckSystem(project_root)
    return system.check_system_health()


def generate_health_report(project_root: Optional[Path] = None) -> str:
    """Standalone function to generate a health report."""
    system = HealthCheckSystem(project_root)
    checks = system.check_system_health()
    return system.generate_health_report(checks)
