"""
Claude Code Adapter - Autonomous Claude Code Session Controller

Enables programmatic control of Claude Code sessions for autonomous bot task execution.
Supports both API and CLI-based implementations.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import subprocess
import time
import json
import os
import re


class ClaudeCodeAdapter:
    """
    Autonomous Claude Code session controller.

    Spawns Claude Code sessions, sends prompts, captures responses, handles tasks.
    Implementation uses Anthropic API for maximum reliability and control.
    """

    def __init__(
        self,
        bot_id: str,
        work_dir: Path,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4.5"
    ):
        """
        Initialize Claude Code adapter.

        Args:
            bot_id: Unique bot identifier (e.g., "FBB-002", "CLAUDE-CODE-001")
            work_dir: Working directory for bot (e.g., Path("/path/to/project"))
            api_key: Anthropic API key (optional, reads from env if not provided)
            model: Claude model to use

        Raises:
            ValueError: If bot_id is empty or work_dir doesn't exist
            EnvironmentError: If API key not found
        """
        if not bot_id:
            raise ValueError("bot_id cannot be empty")

        if not work_dir.exists():
            raise ValueError(f"work_dir does not exist: {work_dir}")

        self.bot_id = bot_id
        self.work_dir = Path(work_dir)
        self.model = model

        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise EnvironmentError(
                "API key not provided and ANTHROPIC_API_KEY environment variable not set"
            )

        self.session_active = False
        self.started_at = None
        self.tasks_completed = 0
        self.conversation_history = []

        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "anthropic package required. Install with: pip install anthropic"
            )

    def start_session(self) -> bool:
        """
        Start a new Claude Code session.

        Returns:
            bool: True if session started successfully

        Raises:
            RuntimeError: If session fails to start
        """
        if self.session_active:
            return True

        try:
            test_response = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[{
                    "role": "user",
                    "content": "Respond with 'ready' if you can read this."
                }]
            )

            response_text = test_response.content[0].text.lower()
            if "ready" in response_text:
                self.session_active = True
                self.started_at = datetime.now().isoformat()
                self.conversation_history = []
                return True
            else:
                raise RuntimeError("Claude did not respond with expected ready signal")

        except Exception as e:
            raise RuntimeError(f"Failed to start session: {str(e)}")

    def send_task(self, task_content: str) -> Dict[str, Any]:
        """
        Send a task to Claude Code and get response.

        Args:
            task_content: Full task specification (markdown text)

        Returns:
            dict: {
                "success": bool,
                "output": str,
                "files_modified": List[str],
                "error": Optional[str],
                "duration_seconds": float
            }
        """
        if not self.session_active:
            return {
                "success": False,
                "output": "",
                "files_modified": [],
                "error": "Session not active. Call start_session() first.",
                "duration_seconds": 0.0
            }

        start_time = time.time()

        try:
            system_prompt = f"""You are an autonomous coding assistant working as bot {self.bot_id}.
Working directory: {self.work_dir}

When you complete tasks:
1. Execute all requested operations
2. Report results clearly
3. List any files you modified
4. Use ✓ for success, ✗ for failure

Respond concisely but completely."""

            self.conversation_history.append({
                "role": "user",
                "content": task_content
            })

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=self.conversation_history
            )

            response_text = ""
            for block in response.content:
                if block.type == "text":
                    response_text += block.text

            self.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })

            files_modified = self._extract_file_paths(response_text)

            success = self._detect_success(response_text)

            duration = time.time() - start_time
            self.tasks_completed += 1

            return {
                "success": success,
                "output": response_text,
                "files_modified": files_modified,
                "error": None if success else "Task may have failed - check output",
                "duration_seconds": round(duration, 1)
            }

        except Exception as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "output": "",
                "files_modified": [],
                "error": f"Exception during task execution: {str(e)}",
                "duration_seconds": round(duration, 1)
            }

    def check_health(self) -> bool:
        """
        Check if Claude Code session is still alive.

        Returns:
            bool: True if session responding, False if dead
        """
        if not self.session_active:
            return False

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=50,
                messages=[{
                    "role": "user",
                    "content": "Respond with 'ok'"
                }]
            )

            response_text = response.content[0].text.lower()
            return "ok" in response_text

        except Exception:
            return False

    def stop_session(self) -> None:
        """
        Gracefully stop Claude Code session.
        """
        self.session_active = False
        self.conversation_history = []

    def get_session_info(self) -> Dict[str, Any]:
        """
        Get current session metadata.

        Returns:
            dict: {
                "bot_id": str,
                "model": str,
                "started_at": str,
                "tasks_completed": int,
                "status": str
            }
        """
        status = "active" if self.session_active else "stopped"

        return {
            "bot_id": self.bot_id,
            "model": self.model,
            "started_at": self.started_at or "not started",
            "tasks_completed": self.tasks_completed,
            "status": status
        }

    def _extract_file_paths(self, text: str) -> List[str]:
        """
        Extract file paths from Claude's response.

        Args:
            text: Response text to parse

        Returns:
            List of file paths found
        """
        patterns = [
            r'(?:modified|created|updated|changed):\s*([^\s\n]+\.[a-zA-Z]+)',
            r'(?:file|path):\s*([^\s\n]+\.[a-zA-Z]+)',
            r'`([^\s`]+\.[a-zA-Z]+)`',
        ]

        files = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            files.extend(matches)

        return list(set(files))

    def _detect_success(self, text: str) -> bool:
        """
        Detect if task completed successfully.

        Args:
            text: Response text to analyze

        Returns:
            bool: True if success indicators found
        """
        success_indicators = [
            "✓", "✔", "success", "complete", "done", "finished"
        ]
        failure_indicators = [
            "✗", "✘", "failed", "error", "exception", "could not", "unable"
        ]

        text_lower = text.lower()

        has_failure = any(indicator in text_lower for indicator in failure_indicators)
        has_success = any(indicator in text_lower for indicator in success_indicators)

        if has_failure:
            return False
        if has_success:
            return True

        return True


def parse_task_file(task_path: Path) -> Dict[str, Any]:
    """
    Parse a task file from filesystem.

    Args:
        task_path: Path to task markdown file

    Returns:
        dict: {
            "task_id": str,
            "to": str,
            "from": str,
            "priority": str,
            "content": str,
            "created_at": str
        }
    """
    if not task_path.exists():
        raise FileNotFoundError(f"Task file not found: {task_path}")

    content = task_path.read_text(encoding="utf-8")

    # Try YAML frontmatter first
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if yaml_match:
        frontmatter = yaml_match.group(1)
        body = yaml_match.group(2)

        # Parse YAML frontmatter
        task_id_match = re.search(r'task_id:\s*([^\n]+)', frontmatter)
        to_match = re.search(r'to:\s*([^\n]+)', frontmatter)
        from_match = re.search(r'from:\s*([^\n]+)', frontmatter)
        priority_match = re.search(r'priority:\s*([^\n]+)', frontmatter)
        created_match = re.search(r'created_at:\s*([^\n]+)', frontmatter)

        task_id = task_id_match.group(1).strip() if task_id_match else task_path.stem
        to_bot = to_match.group(1).strip() if to_match else "unknown"
        from_bot = from_match.group(1).strip() if from_match else "unknown"
        priority = priority_match.group(1).strip() if priority_match else "P2"
        created_at = created_match.group(1).strip() if created_match else datetime.now().isoformat()
        content_body = body.strip()
    else:
        # Fallback to markdown-style parsing
        task_id = task_path.stem
        to_match = re.search(r'\*\*To:\*\*\s*([^\n]+)', content, re.IGNORECASE)
        from_match = re.search(r'\*\*From:\*\*\s*([^\n]+)', content, re.IGNORECASE)
        priority_match = re.search(r'\*\*Priority:\*\*\s*([^\n]+)', content, re.IGNORECASE)

        to_bot = to_match.group(1).strip() if to_match else "unknown"
        from_bot = from_match.group(1).strip() if from_match else "unknown"
        priority = priority_match.group(1).strip() if priority_match else "P2"

        mtime = task_path.stat().st_mtime
        created_at = datetime.fromtimestamp(mtime).isoformat()
        content_body = content

    return {
        "task_id": task_id,
        "to": to_bot,
        "from": from_bot,
        "priority": priority,
        "content": content_body,
        "created_at": created_at
    }


def write_response_file(
    response_dir: Path,
    from_bot: str,
    to_bot: str,
    task_id: str,
    result: Dict[str, Any]
) -> Path:
    """
    Write task completion response to filesystem.

    Args:
        response_dir: Directory to write response
        from_bot: Bot completing task
        to_bot: Bot that assigned task
        task_id: Original task identifier
        result: Task execution result

    Returns:
        Path: Path to created response file
    """
    response_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")

    task_short = task_id.split("-")[-1] if "-" in task_id else task_id
    task_short = task_short[:20]

    status_word = "complete" if result["success"] else "failed"
    filename = f"{timestamp}-{from_bot}-{to_bot}-RESPONSE-{task_short}-{status_word}.md"

    response_path = response_dir / filename

    status_symbol = "✓ SUCCESS" if result["success"] else "✗ FAILED"

    files_section = "- None"
    if result.get("files_modified"):
        files_section = "\n".join(f"- {f}" for f in result["files_modified"])

    error_section = ""
    if result.get("error"):
        error_section = f"\n## Error\n\n{result['error']}\n"

    output_text = result.get("output") or result.get("response", "No output")

    content = f"""# RESPONSE: {task_short} - {status_word.title()}

**From:** {from_bot}
**To:** {to_bot}
**Task:** {task_id}
**Status:** {status_symbol}
**Duration:** {result.get('duration_seconds', 0)} seconds

## Output

{output_text}

## Files Modified

{files_section}
{error_section}
---

**Response generated:** {datetime.now().isoformat()}
"""

    response_path.write_text(content, encoding="utf-8")

    return response_path
