from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import json


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")


def task_dir(repo_root: Path, bot_id: str) -> Path:
    return repo_root / ".deia" / "hive" / "tasks" / bot_id


def response_dir(repo_root: Path) -> Path:
    return repo_root / ".deia" / "hive" / "responses"


def archive_dir(repo_root: Path, bot_id: Optional[str] = None) -> Path:
    base = repo_root / ".deia" / "hive" / "archive"
    return base / bot_id if bot_id else base


def _infer_bot_id(task_path: Path) -> Optional[str]:
    parts = task_path.parts
    if "tasks" in parts:
        idx = parts.index("tasks")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None


def write_task(repo_root: Path, bot_id: str, payload: Dict) -> Path:
    tdir = task_dir(repo_root, bot_id)
    tdir.mkdir(parents=True, exist_ok=True)
    payload.setdefault("status", "queued")
    payload.setdefault("created_at", datetime.now().isoformat())
    filename = f"{_timestamp()}-TASK-{payload.get('task_id', 'NEW')}.json"
    path = tdir / filename
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def complete_task(repo_root: Path, task_path: Path, completion_note: Optional[str] = None) -> Optional[Path]:
    if not task_path.exists():
        return None

    data = json.loads(task_path.read_text(encoding="utf-8"))
    data["status"] = "completed"
    data["completed_at"] = datetime.now().isoformat()
    if completion_note:
        data["completion_note"] = completion_note
    task_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    bot_id = _infer_bot_id(task_path) or "unassigned"
    adir = archive_dir(repo_root, bot_id)
    adir.mkdir(parents=True, exist_ok=True)
    archived = adir / f"{_timestamp()}-COMPLETED-{task_path.name}"
    task_path.replace(archived)
    return archived


def latest_response(repo_root: Path, task_id: Optional[str] = None) -> Optional[Path]:
    rdir = response_dir(repo_root)
    if not rdir.exists():
        return None

    files = sorted(rdir.glob("*.md"), reverse=True)
    if task_id:
        files = [f for f in files if task_id in f.name]
    return files[0] if files else None
