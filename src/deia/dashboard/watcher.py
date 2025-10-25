"""
Hive File Watcher

Watches .deia/hive/ directory for changes and emits events.
Uses watchdog for cross-platform file system monitoring.
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent
from pathlib import Path
from typing import Callable, Dict, Any, Optional
from datetime import datetime
import time

from .parser import parse_task_file, parse_response_file


class HiveFileHandler(FileSystemEventHandler):
    """Handle file system events in .deia/hive/"""

    def __init__(self, hive_dir: Path, on_event: Callable[[Dict[str, Any]], None]):
        """
        Initialize handler.

        Args:
            hive_dir: Path to .deia/hive/ directory
            on_event: Callback for events: on_event(event_dict)
        """
        self.hive_dir = Path(hive_dir)
        self.on_event = on_event

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Only process markdown files
        if file_path.suffix != ".md":
            return

        # Determine event type based on directory
        if "tasks" in file_path.parts:
            self._handle_task_created(file_path)
        elif "responses" in file_path.parts:
            self._handle_response_created(file_path)
        elif "coordination" in file_path.parts:
            self._handle_coordination_created(file_path)

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Handle status board updates
        if file_path.name == "bot-status-board.json":
            self._handle_status_update(file_path)

    def _handle_task_created(self, file_path: Path):
        """Handle new task file."""
        try:
            task = parse_task_file(file_path)

            # Determine task type
            task_type = "task"
            if "VIOLATION" in file_path.name:
                task_type = "violation"
            elif "HUMAN" in file_path.name:
                task_type = "human_interject"
            elif "INTERRUPT" in file_path.name:
                task_type = "interrupt"

            event = {
                "type": task_type,
                "timestamp": datetime.now().isoformat(),
                "from": task.get("from", "UNKNOWN"),
                "to": task.get("to", "UNKNOWN"),
                "content": task.get("content", "")[:200],  # First 200 chars
                "priority": task.get("priority", "P2"),
                "file_path": str(file_path.relative_to(self.hive_dir.parent.parent))
            }

            self.on_event(event)
            print(f"[Watcher] Task created: {file_path.name}")

        except Exception as e:
            print(f"[Watcher] Failed to parse task {file_path.name}: {e}")

    def _handle_response_created(self, file_path: Path):
        """Handle new response file."""
        try:
            response = parse_response_file(file_path)

            event = {
                "type": "response",
                "timestamp": datetime.now().isoformat(),
                "from": response.get("from", "UNKNOWN"),
                "to": response.get("to", "UNKNOWN"),
                "content": response.get("content", "")[:200],  # First 200 chars
                "file_path": str(file_path.relative_to(self.hive_dir.parent.parent))
            }

            self.on_event(event)
            print(f"[Watcher] Response created: {file_path.name}")

        except Exception as e:
            print(f"[Watcher] Failed to parse response {file_path.name}: {e}")

    def _handle_coordination_created(self, file_path: Path):
        """Handle new coordination/SYNC file."""
        try:
            sync_msg = parse_response_file(file_path)  # Same format as responses

            event = {
                "type": "coordination",
                "timestamp": datetime.now().isoformat(),
                "from": sync_msg.get("from", "UNKNOWN"),
                "to": sync_msg.get("to", "ALL_HIVE"),
                "content": sync_msg.get("content", "")[:200],  # First 200 chars
                "file_path": str(file_path.relative_to(self.hive_dir.parent.parent))
            }

            self.on_event(event)
            print(f"[Watcher] Coordination message created: {file_path.name}")

        except Exception as e:
            print(f"[Watcher] Failed to parse coordination {file_path.name}: {e}")

    def _handle_status_update(self, file_path: Path):
        """Handle status board update."""
        try:
            import json

            # Handle UTF-8 BOM
            board = json.loads(file_path.read_text(encoding="utf-8-sig"))

            event = {
                "type": "status_update",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "total_bots": len(board.get("bots", {})),
                    "last_updated": board.get("last_updated"),
                    "updated_by": board.get("updated_by")
                }
            }

            self.on_event(event)
            print(f"[Watcher] Status board updated")

        except Exception as e:
            print(f"[Watcher] Failed to parse status board: {e}")


class HiveWatcher:
    """Watcher for .deia/hive/ directory."""

    def __init__(self, hive_dir: Path, on_event: Callable[[Dict[str, Any]], None]):
        """
        Initialize watcher.

        Args:
            hive_dir: Path to .deia/hive/ directory
            on_event: Callback for events
        """
        self.hive_dir = Path(hive_dir)
        self.on_event = on_event
        self.observer: Optional[Observer] = None

    def start(self):
        """Start watching for file changes."""
        if self.observer:
            print("[Watcher] Already running")
            return

        handler = HiveFileHandler(self.hive_dir, self.on_event)
        self.observer = Observer()

        # Watch tasks, responses, coordination, and parent directory (for status board)
        self.observer.schedule(handler, str(self.hive_dir / "tasks"), recursive=False)
        self.observer.schedule(handler, str(self.hive_dir / "responses"), recursive=False)

        # Watch coordination if it exists
        coordination_dir = self.hive_dir / "coordination"
        if coordination_dir.exists():
            self.observer.schedule(handler, str(coordination_dir), recursive=False)

        self.observer.schedule(handler, str(self.hive_dir.parent), recursive=False)  # For status board

        self.observer.start()
        print(f"[Watcher] Started monitoring: {self.hive_dir}")

    def stop(self):
        """Stop watching."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            print("[Watcher] Stopped")

    def is_running(self) -> bool:
        """Check if watcher is running."""
        return self.observer is not None and self.observer.is_alive()
