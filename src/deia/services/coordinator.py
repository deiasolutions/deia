#!/usr/bin/env python3
"""
Coordinator MVP: Scope Enforcement Daemon

Monitors path events and automatically freezes bots that violate their scope.
Critical for hive governance and preventing escaped bots.

Responds to P0 incident: https://github.com/deiasolutions/deiasolutions/issues/P0
"""

import json
import logging
import signal
import sys
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - COORDINATOR - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScopeEnforcer:
    """Monitors path events and enforces bot scope boundaries."""

    def __init__(self, project_root: Path = None):
        """Initialize scope enforcer."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.path_events_file = project_root / ".deia" / "telemetry" / "path-events.jsonl"
        self.hive_log = project_root / ".deia" / "hive-log.jsonl"
        self.violations_log = project_root / ".deia" / "hive" / "logs" / "scope-violations.log"
        self.bot_registry = project_root / ".deia" / "bot-registry.json"

        # Ensure directories exist
        self.violations_log.parent.mkdir(parents=True, exist_ok=True)

        # Track last processed line to avoid reprocessing
        self.last_processed_line = 0
        self.violating_bots: Dict[str, int] = {}  # Track violation counts per bot
        self.running = True
        self.lock = threading.Lock()

        logger.info(f"Coordinator initialized (project root: {self.project_root})")

    def log_violation(self, bot_id: str, event: dict, reason: str):
        """Log a scope violation."""
        timestamp = datetime.utcnow().isoformat() + "Z"

        violation_entry = {
            "timestamp": timestamp,
            "bot_id": bot_id,
            "violation_type": "scope_drift",
            "attempted_path": event.get("resolved_path"),
            "allowed_paths": event.get("allowed_paths"),
            "current_cwd": event.get("cwd"),
            "operation": event.get("op"),
            "reason": reason,
            "action_taken": "STANDBY"
        }

        # Write to violations log
        with open(self.violations_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(violation_entry) + '\n')

        # Write to hive log
        hive_entry = {
            "timestamp": timestamp,
            "type": "scope_drift_detected",
            "bot_id": bot_id,
            "message": f"Bot {bot_id} attempted to access {event.get('resolved_path')} - outside allowed scope",
            "severity": "critical",
            "action": "bot_frozen_to_standby"
        }

        with open(self.hive_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(hive_entry) + '\n')

        logger.warning(f"VIOLATION LOGGED: {bot_id} - {reason}")

    def freeze_bot(self, bot_id: str) -> bool:
        """Freeze a bot by setting its status to STANDBY."""
        try:
            if not self.bot_registry.exists():
                logger.warning(f"Bot registry not found: {self.bot_registry}")
                return False

            with open(self.bot_registry, 'r', encoding='utf-8') as f:
                registry = json.load(f)

            if bot_id not in registry:
                logger.warning(f"Bot {bot_id} not in registry")
                return False

            # Set status to STANDBY
            registry[bot_id]["status"] = "STANDBY"
            registry[bot_id]["frozen_at"] = datetime.utcnow().isoformat() + "Z"
            registry[bot_id]["freeze_reason"] = "scope_drift_detected"

            with open(self.bot_registry, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2)

            logger.info(f"BOT FROZEN: {bot_id} status set to STANDBY")
            return True

        except Exception as e:
            logger.error(f"Failed to freeze bot {bot_id}: {e}")
            return False

    def process_path_event(self, event: dict):
        """Process a path event and take action if needed."""
        bot_id = event.get("bot_id")
        within_scope = event.get("within_scope", True)
        decision = event.get("decision", "allow")
        reason = event.get("reason", "")

        if within_scope and decision != "deny":
            # Normal operation - scope is good
            return

        # SCOPE VIOLATION DETECTED
        logger.critical(f"SCOPE VIOLATION: {bot_id} - {reason}")

        with self.lock:
            # Increment violation count
            self.violating_bots[bot_id] = self.violating_bots.get(bot_id, 0) + 1

            # Log the violation
            self.log_violation(bot_id, event, reason)

            # Freeze the bot
            if self.freeze_bot(bot_id):
                logger.critical(f"COORDINATOR ACTION: {bot_id} frozen to STANDBY")
            else:
                logger.error(f"COORDINATOR FAILED: Could not freeze {bot_id}")

    def monitor_path_events(self):
        """Main monitoring loop - watches path-events.jsonl for violations."""
        logger.info(f"Starting path event monitoring (file: {self.path_events_file})")

        if not self.path_events_file.exists():
            logger.info(f"Path events file not yet created: {self.path_events_file}")

        while self.running:
            try:
                if not self.path_events_file.exists():
                    # File not created yet - wait
                    time.sleep(5)
                    continue

                with open(self.path_events_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Process new lines
                for line_num, line in enumerate(lines[self.last_processed_line:], start=self.last_processed_line):
                    if not line.strip():
                        continue

                    try:
                        event = json.loads(line)
                        self.process_path_event(event)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse path event line {line_num}: {e}")
                    except Exception as e:
                        logger.error(f"Error processing path event: {e}")

                # Update last processed line
                self.last_processed_line = len(lines)

                # Sleep before next check
                time.sleep(5)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)

    def generate_summary(self) -> dict:
        """Generate summary of violations."""
        try:
            if not self.violations_log.exists():
                return {"total_violations": 0, "bots_frozen": [], "clean_run": True}

            with open(self.violations_log, 'r', encoding='utf-8') as f:
                violations = [json.loads(line) for line in f if line.strip()]

            bots_frozen = list(self.violating_bots.keys())

            return {
                "total_violations": len(violations),
                "bots_frozen": bots_frozen,
                "clean_run": len(violations) == 0,
                "last_violation": violations[-1] if violations else None
            }

        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return {"error": str(e)}

    def start(self):
        """Start the coordinator daemon."""
        logger.info("Starting Coordinator daemon...")

        # Set up signal handlers for graceful shutdown
        def signal_handler(sig, frame):
            logger.info("Shutting down gracefully...")
            self.running = False

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # Start monitoring in main thread
        self.monitor_path_events()

    def stop(self):
        """Stop the coordinator daemon."""
        logger.info("Stopping Coordinator daemon...")
        self.running = False


def main():
    """Entry point for coordinator daemon."""
    try:
        coordinator = ScopeEnforcer()
        coordinator.start()
    except KeyboardInterrupt:
        logger.info("Coordinator interrupted")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error in coordinator: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
