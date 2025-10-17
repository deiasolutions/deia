"""
State persistence for sync operations.

Manages state tracking across sync runs including processed files,
timestamps, and error counts.
"""

import os
import json
import logging
from typing import Dict, Optional
from datetime import datetime, timezone


class StateManager:
    """Manages state persistence across sync runs."""

    def __init__(self, state_file: Optional[str] = None):
        """
        Initialize state manager.

        Args:
            state_file: Path to state file. Defaults to ~/.deia/sync/state.json
        """
        if state_file is None:
            state_file = os.path.join(
                os.path.expanduser("~"),
                ".deia",
                "sync",
                "state.json"
            )

        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load state from file, or create default state."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass  # Fall through to default state

        # Default state
        return {
            "last_run": None,
            "last_processed_files": [],
            "processed_count": 0,
            "errors_count": 0
        }

    def save_state(self):
        """Persist state to disk."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)

            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving state: {e}")

    def update_last_run(self):
        """Update last run timestamp to current time."""
        self.state['last_run'] = datetime.now(timezone.utc).isoformat()
        self.save_state()

    def add_processed_file(self, filename: str):
        """Record a successfully processed file."""
        if filename not in self.state['last_processed_files']:
            self.state['last_processed_files'].append(filename)
        self.state['processed_count'] += 1
        self.save_state()

    def increment_error_count(self):
        """Increment error counter."""
        self.state['errors_count'] += 1
        self.save_state()

    def get_last_run_datetime(self) -> Optional[datetime]:
        """Get last run as datetime object."""
        if not self.state['last_run']:
            return None
        return datetime.fromisoformat(self.state['last_run'])

    def was_file_processed(self, filename: str) -> bool:
        """Check if file was successfully processed before."""
        return filename in self.state['last_processed_files']
