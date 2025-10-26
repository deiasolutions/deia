#!/usr/bin/env python3
"""
File Mover Service: Automated file operations based on rules engine.

Watches directories for file changes and applies configured rules:
- Move files to target directories
- Copy files to multiple locations
- Delete files matching criteria
- Create directory structures
- Apply conditional logic (if/else rules)
"""

import json
import logging
import os
import shutil
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import fnmatch
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - FILE-MOVER - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FileRule:
    """Represents a single file operation rule."""

    def __init__(self, rule_dict: dict):
        """Initialize a file rule."""
        self.name = rule_dict.get("name", "unnamed_rule")
        self.enabled = rule_dict.get("enabled", True)
        self.watch_path = Path(rule_dict.get("watch_path", "."))
        self.pattern = rule_dict.get("pattern", "*")
        self.action = rule_dict.get("action", "move")  # move, copy, delete, mkdir
        self.target_path = rule_dict.get("target_path")
        self.condition = rule_dict.get("condition")  # Optional conditional logic
        self.recursive = rule_dict.get("recursive", False)
        self.overwrite = rule_dict.get("overwrite", False)

        # Validation
        if not self.enabled:
            return
        if self.action in ["move", "copy"] and not self.target_path:
            raise ValueError(f"Rule {self.name}: {self.action} requires target_path")

    def matches(self, filepath: Path) -> bool:
        """Check if file matches this rule's pattern."""
        return fnmatch.fnmatch(filepath.name, self.pattern)

    def apply_condition(self, filepath: Path) -> bool:
        """Apply conditional logic if defined."""
        if not self.condition:
            return True

        # Simple condition evaluation
        # Examples: "size > 1000", "extension == .log", "age > 7"
        if "size" in self.condition:
            try:
                file_size = filepath.stat().st_size
                return self._evaluate_expression(self.condition, file_size)
            except Exception as e:
                logger.warning(f"Failed to evaluate size condition: {e}")
                return False

        if "age" in self.condition:
            try:
                import time as time_module
                file_age_days = (time_module.time() - filepath.stat().st_mtime) / (24 * 3600)
                return self._evaluate_expression(self.condition, file_age_days)
            except Exception as e:
                logger.warning(f"Failed to evaluate age condition: {e}")
                return False

        return True

    @staticmethod
    def _evaluate_expression(condition: str, value: Any) -> bool:
        """Evaluate a simple comparison expression."""
        # Very simple evaluator for expressions like "size > 1000"
        for op in [" > ", " < ", " == ", " >= ", " <= ", " != "]:
            if op in condition:
                parts = condition.split(op)
                if len(parts) != 2:
                    return False
                try:
                    threshold = float(parts[1].strip())
                    if op.strip() == ">":
                        return value > threshold
                    elif op.strip() == "<":
                        return value < threshold
                    elif op.strip() == "==":
                        return value == threshold
                    elif op.strip() == ">=":
                        return value >= threshold
                    elif op.strip() == "<=":
                        return value <= threshold
                    elif op.strip() == "!=":
                        return value != threshold
                except (ValueError, TypeError):
                    return False
        return False


class FileMoverService:
    """Service for automating file operations based on rules."""

    def __init__(self, rules_file: Path, project_root: Path = None):
        """Initialize file mover service."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.rules_file = rules_file
        self.rules: List[FileRule] = []
        self.operations_log = project_root / ".deia" / "logs" / "file-mover-operations.jsonl"
        self.errors_log = project_root / ".deia" / "logs" / "file-mover-errors.jsonl"
        self.running = True
        self.lock = threading.Lock()

        # Ensure directories exist
        self.operations_log.parent.mkdir(parents=True, exist_ok=True)

        # Load rules
        self.load_rules()

        logger.info(f"File Mover initialized with {len(self.rules)} rules")

    def load_rules(self):
        """Load rules from configuration file."""
        if not self.rules_file.exists():
            logger.warning(f"Rules file not found: {self.rules_file}")
            return

        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)

            self.rules = []
            for rule_dict in rules_data.get("rules", []):
                try:
                    rule = FileRule(rule_dict)
                    if rule.enabled:
                        self.rules.append(rule)
                        logger.info(f"Loaded rule: {rule.name}")
                except ValueError as e:
                    logger.error(f"Invalid rule: {e}")

            logger.info(f"Loaded {len(self.rules)} enabled rules")

        except Exception as e:
            logger.error(f"Failed to load rules: {e}")

    def log_operation(self, operation: str, source: Path, target: Optional[Path], success: bool, details: str = ""):
        """Log a file operation."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "operation": operation,
            "source": str(source),
            "target": str(target) if target else None,
            "success": success,
            "details": details
        }

        with open(self.operations_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

    def log_error(self, rule_name: str, filepath: Path, error: str):
        """Log an error during file operation."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "rule": rule_name,
            "file": str(filepath),
            "error": error
        }

        with open(self.errors_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

    def apply_move(self, source: Path, rule: FileRule) -> bool:
        """Move file to target location."""
        try:
            target = Path(rule.target_path) / source.name

            # Create parent directories if needed
            target.parent.mkdir(parents=True, exist_ok=True)

            # Check if target exists
            if target.exists() and not rule.overwrite:
                logger.warning(f"Target exists and overwrite disabled: {target}")
                return False

            shutil.move(str(source), str(target))
            self.log_operation("move", source, target, True)
            logger.info(f"Moved: {source} → {target}")
            return True

        except Exception as e:
            logger.error(f"Failed to move {source}: {e}")
            self.log_error(rule.name, source, str(e))
            return False

    def apply_copy(self, source: Path, rule: FileRule) -> bool:
        """Copy file to target location."""
        try:
            target = Path(rule.target_path) / source.name

            # Create parent directories if needed
            target.parent.mkdir(parents=True, exist_ok=True)

            # Check if target exists
            if target.exists() and not rule.overwrite:
                logger.warning(f"Target exists and overwrite disabled: {target}")
                return False

            shutil.copy2(str(source), str(target))
            self.log_operation("copy", source, target, True)
            logger.info(f"Copied: {source} → {target}")
            return True

        except Exception as e:
            logger.error(f"Failed to copy {source}: {e}")
            self.log_error(rule.name, source, str(e))
            return False

    def apply_delete(self, filepath: Path, rule: FileRule) -> bool:
        """Delete a file safely."""
        try:
            # Safety check: don't delete if path looks suspicious
            if ".deia" in filepath.parts or ".git" in filepath.parts:
                logger.warning(f"Refusing to delete protected path: {filepath}")
                return False

            os.remove(str(filepath))
            self.log_operation("delete", filepath, None, True)
            logger.info(f"Deleted: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete {filepath}: {e}")
            self.log_error(rule.name, filepath, str(e))
            return False

    def apply_mkdir(self, filepath: Path, rule: FileRule) -> bool:
        """Create directory structure."""
        try:
            # For mkdir action, target_path is the directory to create
            target_dir = Path(rule.target_path)
            target_dir.mkdir(parents=True, exist_ok=True)
            self.log_operation("mkdir", filepath, target_dir, True)
            logger.info(f"Created directory: {target_dir}")
            return True

        except Exception as e:
            logger.error(f"Failed to create directory: {e}")
            self.log_error(rule.name, filepath, str(e))
            return False

    def process_file(self, filepath: Path, rule: FileRule) -> bool:
        """Apply a rule to a file."""
        # Check if file matches pattern
        if not rule.matches(filepath):
            return False

        # Apply condition if defined
        if not rule.apply_condition(filepath):
            return False

        # Apply action
        logger.info(f"Applying rule '{rule.name}' to {filepath}")

        if rule.action == "move":
            return self.apply_move(filepath, rule)
        elif rule.action == "copy":
            return self.apply_copy(filepath, rule)
        elif rule.action == "delete":
            return self.apply_delete(filepath, rule)
        elif rule.action == "mkdir":
            return self.apply_mkdir(filepath, rule)
        else:
            logger.warning(f"Unknown action: {rule.action}")
            return False

    def scan_directory(self, rule: FileRule):
        """Scan directory and apply rule to matching files."""
        if not rule.watch_path.exists():
            logger.warning(f"Watch path does not exist: {rule.watch_path}")
            return

        try:
            if rule.recursive:
                # Recursive scan
                for filepath in rule.watch_path.rglob("*"):
                    if filepath.is_file():
                        self.process_file(filepath, rule)
            else:
                # Non-recursive scan
                for filepath in rule.watch_path.iterdir():
                    if filepath.is_file():
                        self.process_file(filepath, rule)

        except Exception as e:
            logger.error(f"Error scanning directory {rule.watch_path}: {e}")

    def run_once(self):
        """Execute all rules once."""
        with self.lock:
            for rule in self.rules:
                if rule.enabled:
                    logger.info(f"Executing rule: {rule.name}")
                    self.scan_directory(rule)

    def monitor(self, interval: int = 60):
        """Continuous monitoring loop."""
        logger.info(f"Starting file mover monitoring (interval: {interval}s)")

        while self.running:
            try:
                self.run_once()
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")

            time.sleep(interval)

    def stop(self):
        """Stop the service."""
        logger.info("Stopping file mover service")
        self.running = False


def main():
    """Entry point for file mover service."""
    # Default rules file location
    rules_file = Path(__file__).parent.parent.parent.parent / ".deia" / "file-mover-rules.json"

    try:
        service = FileMoverService(rules_file)
        service.monitor()
    except KeyboardInterrupt:
        logger.info("File mover interrupted")
    except Exception as e:
        logger.error(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
