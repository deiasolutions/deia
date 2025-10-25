"""
Task and Response File Parser

Parses markdown task and response files from .deia/hive/
"""

from pathlib import Path
from typing import Dict, Any
import re


def parse_task_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse task markdown file.

    Expected format:
    ```markdown
    # TASK: description

    **To:** BOT-ID
    **From:** SENDER-ID
    **Priority:** P0/P1/P2
    **Created:** ISO timestamp

    Task content here...
    ```

    Returns:
        dict: {
            "from": str,
            "to": str,
            "priority": str,
            "timestamp": str,
            "content": str,
            "task_id": str
        }
    """
    content = file_path.read_text(encoding="utf-8")

    # Extract metadata using regex
    to_match = re.search(r"\*\*To:\*\*\s+(.+)", content)
    from_match = re.search(r"\*\*From:\*\*\s+(.+)", content)
    priority_match = re.search(r"\*\*Priority:\*\*\s+(.+)", content)
    timestamp_match = re.search(r"\*\*Created:\*\*\s+(.+)", content)

    # Extract task ID from filename
    # Format: YYYY-MM-DD-HHMM-FROM-TO-TYPE-desc.md
    parts = file_path.stem.split("-")
    task_id = file_path.stem

    return {
        "from": from_match.group(1).strip() if from_match else "UNKNOWN",
        "to": to_match.group(1).strip() if to_match else "UNKNOWN",
        "priority": priority_match.group(1).strip() if priority_match else "P2",
        "timestamp": timestamp_match.group(1).strip() if timestamp_match else "",
        "content": content,
        "task_id": task_id,
        "file_name": file_path.name
    }


def parse_response_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse response markdown file.

    Expected format:
    ```markdown
    # RESPONSE: description

    **From:** BOT-ID
    **To:** RECIPIENT-ID
    **Task:** task-id
    **Completed:** ISO timestamp

    Response content here...
    ```

    Returns:
        dict: {
            "from": str,
            "to": str,
            "task_id": str,
            "timestamp": str,
            "content": str
        }
    """
    content = file_path.read_text(encoding="utf-8")

    # Extract metadata
    from_match = re.search(r"\*\*From:\*\*\s+(.+)", content)
    to_match = re.search(r"\*\*To:\*\*\s+(.+)", content)
    task_match = re.search(r"\*\*Task:\*\*\s+(.+)", content)
    timestamp_match = re.search(r"\*\*Completed:\*\*\s+(.+)", content)

    return {
        "from": from_match.group(1).strip() if from_match else "UNKNOWN",
        "to": to_match.group(1).strip() if to_match else "UNKNOWN",
        "task_id": task_match.group(1).strip() if task_match else "",
        "timestamp": timestamp_match.group(1).strip() if timestamp_match else "",
        "content": content,
        "file_name": file_path.name
    }


def parse_heartbeat_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse heartbeat YAML file.

    Returns:
        dict: Heartbeat data
    """
    import yaml

    try:
        return yaml.safe_load(file_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Failed to parse heartbeat {file_path.name}: {e}")
        return {}
