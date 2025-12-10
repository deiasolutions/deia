"""RSE logging helper (Python).

Writes append-only events to `.deia/telemetry/rse.jsonl`.
Event shape: { ts, type, lane, actor, data }
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_rse(event_type: str, lane: str, actor: str, data: Dict[str, Any] | None = None, root: Path | None = None) -> None:
    root = root or Path.cwd()
    rse_path = root / ".deia" / "telemetry" / "rse.jsonl"
    rse_path.parent.mkdir(parents=True, exist_ok=True)
    rec = {
        "ts": _now_iso(),
        "type": event_type,
        "lane": lane,
        "actor": actor,
        "data": data or {},
    }
    with rse_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")

