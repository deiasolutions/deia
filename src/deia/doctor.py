"""
DEIA Doctor - Diagnose and fix DEIA installation issues
"""

import sys
from pathlib import Path
from typing import List, Tuple
import json
import subprocess

class DEIADoctor:
    """Diagnose and repair DEIA installations"""

    def __init__(self):
        self.issues: List[Tuple[str, str, str]] = []  # (severity, issue, fix)
        self.warnings: List[str] = []
        self.passed: List[str] = []

    def check_all(self) -> bool:
        """Run all diagnostic checks. Returns True if healthy."""
        from rich.console import Console
        console = Console()
        console.print("[bold cyan]DEIA Doctor - Diagnosing installation...[/bold cyan]\n")

        self.check_python_version()
        self.check_package_installed()
        self.check_import()
        self.check_project_structure()
        self.check_config()
        self.check_claude_integration()

        self.report()

        return len(self.issues) == 0

    def check_python_version(self):
        """Check Python version compatibility"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.issues.append((
                "ERROR",
                f"Python {version.major}.{version.minor} is too old",
                "Install Python 3.8 or newer"
            ))
        else:
            self.passed.append(f"Python {version.major}.{version.minor}.{version.micro}")

    def check_package_installed(self):
        """Check if DEIA package is installed"""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "deia"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            self.issues.append((
                "ERROR",
                "DEIA package not installed",
                "Run: pip install -e /path/to/deia"
            ))
        else:
            # Parse version from output
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    version = line.split(':', 1)[1].strip()
                    self.passed.append(f"DEIA package installed (v{version})")
                    break

    def check_import(self):
        """Check if DEIA can be imported"""
        try:
            from deia.logger import ConversationLogger
            self.passed.append("DEIA imports successfully")
        except ImportError as e:
            self.issues.append((
                "ERROR",
                f"Cannot import DEIA: {e}",
                "Reinstall: pip install -e /path/to/deia"
            ))

    def check_project_structure(self):
        """Check if current directory has DEIA structure"""
        deia_dir = Path('.deia')

        if not deia_dir.exists():
            self.warnings.append(
                "WARNING: Not a DEIA project (.deia/ directory missing)\n"
                "  Run: deia init"
            )
            return

        self.passed.append(".deia/ directory exists")

        # Check subdirectories
        sessions_dir = deia_dir / 'sessions'
        if not sessions_dir.exists():
            self.issues.append((
                "WARNING",
                ".deia/sessions/ directory missing",
                "Run: mkdir .deia/sessions"
            ))
        else:
            self.passed.append(".deia/sessions/ exists")

    def check_config(self):
        """Check if config file exists and is valid"""
        config_file = Path('.deia/config.json')

        if not config_file.exists():
            self.warnings.append(
                "WARNING: .deia/config.json missing\n"
                "  Run: deia init"
            )
            return

        try:
            with open(config_file, 'r') as f:
                config = json.load(f)

            # Check required fields
            required = ['project', 'user']
            missing = [f for f in required if f not in config]

            if missing:
                self.issues.append((
                    "WARNING",
                    f"Config missing fields: {', '.join(missing)}",
                    "Run: deia init --repair"
                ))
            else:
                auto_log = "enabled" if config.get('auto_log') else "disabled"
                self.passed.append(f"config.json valid (auto-log {auto_log})")

        except json.JSONDecodeError:
            self.issues.append((
                "ERROR",
                "config.json is corrupted (invalid JSON)",
                "Run: deia init --repair"
            ))

    def check_claude_integration(self):
        """Check Claude Code integration files"""
        preferences_file = Path('.claude/preferences/deia.md')

        if not preferences_file.exists():
            self.warnings.append(
                "WARNING: Claude Code preferences not set up\n"
                "  File missing: .claude/preferences/deia.md\n"
                "  This file is created by 'deia init'. If it's missing, you may need\n"
                "  to manually copy it from the DEIA repo or reinitialize."
            )
        else:
            self.passed.append("Claude Code preferences exist")

        # Check if user has set # memory
        self.warnings.append(
            "INFO: To enable auto-loading, set Claude Code memory:\n"
            "  Type: # deia-user (for all projects)\n"
            "  or: # deia (for this project only)"
        )

    def report(self):
        """Print diagnostic report"""
        print("\n" + "="*60)
        print("DIAGNOSTIC REPORT")
        print("="*60 + "\n")

        # Passed checks
        if self.passed:
            print("PASSED:\n")
            for item in self.passed:
                print(f"  {item}")
            print()

        # Warnings
        if self.warnings:
            print("WARNINGS:\n")
            for warning in self.warnings:
                print(f"  {warning}")
            print()

        # Issues
        if self.issues:
            print("ISSUES FOUND:\n")
            for severity, issue, fix in self.issues:
                print(f"  [{severity}] {issue}")
                print(f"    -> Fix: {fix}\n")

        # Summary
        print("="*60)
        if not self.issues:
            print("DEIA is healthy!")
        else:
            print(f"Found {len(self.issues)} issue(s) that need attention")
        print("="*60 + "\n")

    def repair(self):
        """Attempt automatic repair of common issues"""
        from rich.console import Console
        console = Console()
        console.print("[bold cyan]DEIA Doctor - Attempting repairs...[/bold cyan]\n")

        repaired = []
        failed = []

        # Repair .deia directory structure
        deia_dir = Path('.deia')
        if not deia_dir.exists():
            try:
                deia_dir.mkdir(parents=True)
                repaired.append("Created .deia/ directory")
            except Exception as e:
                failed.append(f"Could not create .deia/: {e}")

        # Repair sessions directory
        sessions_dir = deia_dir / 'sessions'
        if not sessions_dir.exists():
            try:
                sessions_dir.mkdir(parents=True)
                repaired.append("Created .deia/sessions/ directory")
            except Exception as e:
                failed.append(f"Could not create sessions/: {e}")

        # Repair config.json
        config_file = deia_dir / 'config.json'
        if not config_file.exists() or self._is_config_corrupted(config_file):
            try:
                import getpass
                import os

                default_config = {
                    "project": Path.cwd().name,
                    "user": getpass.getuser(),
                    "auto_log": False,
                    "version": "0.1.0"
                }

                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)

                repaired.append("Repaired config.json")
            except Exception as e:
                failed.append(f"Could not repair config.json: {e}")

        # Report
        print("="*60)
        print("REPAIR REPORT")
        print("="*60 + "\n")

        if repaired:
            print("REPAIRED:\n")
            for item in repaired:
                print(f"  + {item}")
            print()

        if failed:
            print("FAILED:\n")
            for item in failed:
                print(f"  - {item}")
            print()

        print("="*60)
        if failed:
            print("Some repairs failed. Manual intervention needed.")
        else:
            print("Repairs completed successfully!")
        print("="*60 + "\n")

        # Run check again
        print("Running diagnostics again...\n")
        self.check_all()

    def _is_config_corrupted(self, config_file: Path) -> bool:
        """Check if config file is corrupted"""
        try:
            with open(config_file, 'r') as f:
                json.load(f)
            return False
        except (json.JSONDecodeError, IOError):
            return True


def main():
    """CLI entry point for deia doctor"""
    import argparse

    parser = argparse.ArgumentParser(
        description="DEIA Doctor - Diagnose and repair DEIA installations"
    )
    parser.add_argument(
        '--repair',
        action='store_true',
        help='Attempt automatic repair of issues'
    )

    args = parser.parse_args()

    doctor = DEIADoctor()

    if args.repair:
        doctor.repair()
    else:
        doctor.check_all()

        if doctor.issues:
            print("\n💡 TIP: Run 'deia doctor --repair' to attempt automatic fixes")


if __name__ == '__main__':
    main()
