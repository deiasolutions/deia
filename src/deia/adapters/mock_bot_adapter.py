"""
Mock Bot Adapter - Simple file-based bot for testing coordination.

Implements basic file-watching bot behavior without Claude Code CLI dependency.
Used for testing dashboard and coordination flow.
"""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json


class MockBotAdapter:
    """
    Mock bot adapter for testing file-based coordination.

    Implements the same interface as ClaudeCodeAdapter and ClaudeCodeCLIAdapter,
    but generates simple canned responses instead of using AI.

    Purpose: Unblock dashboard testing while CLI adapter issues are debugged.
    """

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        **kwargs
    ):
        """
        Initialize mock bot adapter.

        Args:
            bot_id: Unique bot identifier (e.g., "CLAUDE-CODE-TEST-001")
            work_dir: Working directory for bot operations
            **kwargs: Ignored (for compatibility with other adapters)
        """
        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.session_active = False
        self.task_count = 0

    def start_session(self) -> bool:
        """
        Start mock bot session.

        Returns:
            True (mock always succeeds)
        """
        if self.session_active:
            return True

        print(f"[{self.bot_id}] [MOCK] Starting mock bot session")
        self.session_active = True
        self.task_count = 0
        return True

    def stop_session(self) -> None:
        """Stop mock bot session."""
        if not self.session_active:
            return

        print(f"[{self.bot_id}] [MOCK] Stopping mock bot session")
        print(f"[{self.bot_id}] [MOCK] Processed {self.task_count} tasks")
        self.session_active = False

    def send_task(self, task_content: str) -> Dict[str, Any]:
        """
        Process task and generate mock response.

        Args:
            task_content: Task content from markdown file

        Returns:
            dict: {
                "success": bool,
                "response": str,
                "duration_seconds": float,
                "error": Optional[str]
            }
        """
        if not self.session_active:
            return {
                "success": False,
                "response": "",
                "duration_seconds": 0.0,
                "error": "Session not started"
            }

        self.task_count += 1
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Extract first line or heading from task as title
        lines = task_content.strip().split('\n')
        title = "Untitled Task"
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                break
            elif line and not line.startswith('**'):
                title = line[:50] + ("..." if len(line) > 50 else "")
                break

        # Generate mock response
        response = f"""# MOCK RESPONSE: {title}

**From:** {self.bot_id} (Mock Bot)
**Task Number:** {self.task_count}
**Timestamp:** {timestamp}

## Response

This is a mock bot response for testing purposes.

### Task Summary
Received task with {len(lines)} lines, {len(task_content)} characters.

### Mock Actions Taken
1. [OK] Task parsed successfully
2. [OK] Mock processing completed
3. [OK] Response generated

### Task Content Preview
```
{task_content[:300]}{'...' if len(task_content) > 300 else ''}
```

### Notes
- This is a MOCK bot for testing dashboard coordination
- Real bot would execute actual work here
- Mock responses are generic and not intelligent

**Status:** [OK] Task acknowledged and processed (mock)
"""

        print(f"[{self.bot_id}] [MOCK] Processed task #{self.task_count}: {title}")

        return {
            "success": True,
            "response": response,
            "duration_seconds": 0.1,  # Instant mock response
            "error": None
        }

    def check_health(self) -> bool:
        """
        Check adapter health.

        Returns:
            True if session active (mock always healthy)
        """
        return self.session_active

    def get_session_info(self) -> Dict[str, Any]:
        """
        Get session information.

        Returns:
            dict: Session metadata
        """
        return {
            "bot_id": self.bot_id,
            "adapter_type": "mock",
            "session_active": self.session_active,
            "tasks_processed": self.task_count,
            "started_at": datetime.utcnow().isoformat() + "Z" if self.session_active else None
        }
