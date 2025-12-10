"""
Telemetry ETL (Phase 1) - Local-first analytics pipeline for DEIA.

Goals:
- Ensure analytics setup (directories, config, optional DuckDB views)
- Extract session logs (MD), activity events (JSONL), heartbeats (YAML-like)
- Normalize to NDJSON staging (append-only, partitioned by date)
- Optionally initialize DuckDB catalog with views over Parquet (if available)

Note: Parquet writing and full YAML parsing are deferred to Phase 2. This module
works with only the Python standard library (DuckDB optional if installed).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Iterable, Iterator, List, Dict, Any, Optional, Tuple


TABLES = [
    "sessions",
    "session_decisions",
    "session_action_items",
    "session_files_modified",
    "events",
    "heartbeats",
    "hive_tasks",
    "hive_responses",
    "agents",
]


def _ts_iso(dt: Optional[datetime] = None) -> str:
    dt = dt or datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def ensure_setup(project_root: Path) -> Dict[str, Path]:
    """Ensure analytics directory structure and default config.

    Returns a dict of important paths.
    """
    pr = Path(project_root).resolve()
    analytics = pr / ".deia" / "analytics"
    staging = analytics / "staging"
    warehouse = analytics / "warehouse"
    schemas = analytics / "schemas"
    errors = analytics / "errors"
    analytics.mkdir(parents=True, exist_ok=True)
    for p in [staging, warehouse, schemas, errors]:
        p.mkdir(parents=True, exist_ok=True)
    for t in TABLES:
        (staging / t).mkdir(parents=True, exist_ok=True)
        (warehouse / t).mkdir(parents=True, exist_ok=True)

    # Default config
    cfg = analytics / "config.json"
    if not cfg.exists():
        cfg.write_text(
            json.dumps(
                {
                    "targets": ["staging_ndjson"],
                    "transcript_inline": False,
                    "redactions": [],
                    "autorun_on_launch": False,
                    "since": None,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    # Initialize DuckDB file with views if available
    db_path = warehouse / "deia.duckdb"
    _init_duckdb_views_if_available(db_path, warehouse)

    return {
        "analytics": analytics,
        "staging": staging,
        "warehouse": warehouse,
        "schemas": schemas,
        "errors": errors,
        "config": cfg,
        "duckdb": db_path,
    }


def _init_duckdb_views_if_available(db_path: Path, warehouse: Path) -> None:
    try:
        import duckdb  # type: ignore
    except Exception:
        return
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))
    try:
        for t in TABLES:
            # Create view over Parquet partition glob; view works when files exist
            glob_path = str((warehouse / t / "**" / "*.parquet").resolve())
            view_sql = f"CREATE VIEW IF NOT EXISTS {t} AS SELECT * FROM read_parquet('{glob_path}', hive_partitioning=1);"
            con.execute(view_sql)
    finally:
        con.close()


# ------------------------- Extraction helpers -------------------------


def _iter_session_files(project_root: Path) -> Iterator[Path]:
    sessions_dir = project_root / ".deia" / "sessions"
    if sessions_dir.is_dir():
        yield from sessions_dir.glob("*.md")


def _parse_session_md(md_path: Path) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Parse a conversation session markdown into normalized records.

    Returns: (session_row, decisions[], action_items[], files_modified[])
    """
    text = md_path.read_text(encoding="utf-8", errors="replace")
    lines = [ln.rstrip("\n") for ln in text.splitlines()]
    header = {
        "Date": None,
        "Session ID": None,
        "Status": None,
    }
    # Simple header parse
    for i in range(1, min(25, len(lines))):
        ln = lines[i]
        for key in list(header.keys()):
            prefix = f"**{key}:** "
            if ln.startswith(prefix):
                header[key] = ln[len(prefix) :].strip()
    session_id = header.get("Session ID") or md_path.stem
    ts_start = header.get("Date") or datetime.fromtimestamp(md_path.stat().st_mtime, tz=timezone.utc).isoformat()
    status = header.get("Status") or "Unknown"

    # Section extraction by headings
    def extract_section(title: str) -> List[str]:
        start = None
        for idx, ln in enumerate(lines):
            if ln.strip().lower() == f"## {title.lower()}":
                start = idx + 1
                break
        if start is None:
            return []
        out: List[str] = []
        for ln in lines[start:]:
            if ln.startswith("## "):
                break
            out.append(ln)
        return out

    def bullets(sec: List[str]) -> List[str]:
        items: List[str] = []
        for ln in sec:
            s = ln.strip()
            if s.startswith("- "):
                items.append(s[2:].strip())
        return items

    context_lines = extract_section("Context")
    decisions_lines = extract_section("Key Decisions Made")
    action_lines = extract_section("Action Items")
    files_lines = extract_section("Files Modified")
    next_steps_lines = extract_section("Next Steps")

    session_row = {
        "session_id": session_id,
        "ts_start": ts_start,
        "ts_ingested": _ts_iso(),
        "context": "\n".join(context_lines).strip(),
        "transcript_path": str(md_path),
        "status": status,
    }
    decisions = [{"session_id": session_id, "text": t} for t in bullets(decisions_lines)]
    action_items = [{"session_id": session_id, "text": t, "is_done": False} for t in bullets(action_lines)]
    files_modified = []
    for ln in bullets(files_lines):
        # strip backticks and leading path markers
        path = ln.strip().strip("`")
        files_modified.append({"session_id": session_id, "path": path, "repo_relative": not os.path.isabs(path)})

    return session_row, decisions, action_items, files_modified


def _iter_events_jsonl(project_root: Path) -> Iterator[Dict[str, Any]]:
    log_dir = project_root / ".deia" / "bot-logs"
    if not log_dir.is_dir():
        return
    for fp in sorted(log_dir.glob("*.jsonl")):
        with fp.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                try:
                    obj = json.loads(s)
                except Exception:
                    continue
                ev: Dict[str, Any] = {
                    "ts": obj.get("timestamp") or obj.get("time") or _ts_iso(),
                    "bot_id": obj.get("bot_id") or obj.get("agent") or "unknown",
                    "event_type": str(obj.get("event_type") or obj.get("event") or "unknown").lower(),
                    "message": obj.get("message") or obj.get("details") or "",
                    "raw": obj,
                    "source_path": str(fp),
                }
                yield ev


def _iter_heartbeats(project_root: Path) -> Iterator[Dict[str, Any]]:
    hb_dir = project_root / ".deia" / "hive" / "heartbeats"
    if not hb_dir.is_dir():
        return
    for fp in sorted(hb_dir.glob("*.yaml")):
        # Light-weight YAML reader: key: value pairs per line
        data: Dict[str, Any] = {}
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for ln in text.splitlines():
            if not ln.strip() or ln.strip().startswith("#"):
                continue
            if ":" in ln:
                k, v = ln.split(":", 1)
                data[k.strip()] = v.strip().strip("'\"")
        if not data:
            continue
        yield {
            "ts": data.get("timestamp") or _ts_iso(),
            "bot_id": data.get("bot") or data.get("agent") or "unknown",
            "instance": data.get("instance") or "",
            "status": data.get("status") or "",
            "flight": data.get("flight") or "",
            "message": data.get("message") or "",
            "raw": data,
            "source_path": str(fp),
        }


# ---------------------- Hive tasks/responses ingest ----------------------

import re

_HIVE_FILE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(\d{4})-([A-Z0-9_]+)-([A-Z0-9_\-]+)-([A-Z]+)-(.+)\.md$", re.IGNORECASE)


def _parse_hive_body(fp: Path) -> Dict[str, Any]:
    """Parse key fields from hive message body.

    Looks for markdown lines like:
      To: X  From: Y  Subject: Z
      or a title starting with '# TYPE: Subject'
    """
    out: Dict[str, Any] = {}
    try:
        text = fp.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return out
    # split lines and scan
    lines = text.splitlines()
    # Title
    for ln in lines[:5]:
        s = ln.strip()
        if s.startswith("# "):
            out["title"] = s[2:].strip()
            # try TYPE from title prefix before ':'
            if ":" in out["title"]:
                out["title_type"] = out["title"].split(":", 1)[0].strip().upper()
            break
    # Header key-value
    for ln in lines[:40]:
        s = ln.strip()
        for key in ("To:", "From:", "Subject:"):
            if s.lower().startswith(key.lower()):
                val = s[len(key):].strip()
                k = key[:-1].lower()  # to, from, subject
                out[k] = val
    return out


def _iter_hive_messages(project_root: Path, box: str) -> Iterator[Dict[str, Any]]:
    """Iterate hive tasks or responses directory and parse filenames.

    box: 'tasks' or 'responses'
    """
    hive_dir = project_root / ".deia" / "hive" / box
    if not hive_dir.is_dir():
        return
    for fp in sorted(hive_dir.glob("*.md")):
        name = fp.name
        m = _HIVE_FILE_RE.match(name)
        if not m:
            # fallback: parse body only
            body = _parse_hive_body(fp)
            yield {
                "ts": _ts_iso(),
                "from": body.get("from"),
                "to": body.get("to"),
                "type": body.get("title_type"),
                "subject": body.get("subject") or body.get("title") or name,
                "path": str(fp),
                "box": box,
            }
            continue
        year, month, day, hhmm, frm, to, typ, subject = m.groups()
        # Build timestamp in local naive; mark as ISO
        try:
            ts = datetime(int(year), int(month), int(day), int(hhmm[:2]), int(hhmm[2:]), tzinfo=timezone.utc).isoformat()
        except Exception:
            ts = _ts_iso()
        body = _parse_hive_body(fp)
        yield {
            "ts": ts,
            "from": frm,
            "to": to,
            "type": typ.upper(),
            "subject": body.get("subject") or body.get("title") or subject,
            "path": str(fp),
            "box": box,
        }


# --------------------------- Writers & ETL ---------------------------


def _partition_dir(base: Path, table: str, dt: Optional[str] = None) -> Path:
    dt = dt or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    p = base / table / f"dt={dt}"
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_ndjson(table: str, rows: Iterable[Dict[str, Any]], staging_root: Path, dt: Optional[str] = None) -> Path:
    target_dir = _partition_dir(staging_root, table, dt)
    out_path = target_dir / f"{table}-{datetime.now(timezone.utc).strftime('%H%M%S')}.ndjson"
    count = 0
    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return out_path


def write_parquet_if_available(table: str, rows: Iterable[Dict[str, Any]], warehouse_root: Path, dt: Optional[str] = None) -> Optional[Path]:
    """Write rows to Parquet if pyarrow is available. Returns path or None.

    Notes:
      - Converts any 'raw' field to JSON string 'raw_json' for Parquet friendliness.
    """
    try:
        import pyarrow as pa  # type: ignore
        import pyarrow.parquet as pq  # type: ignore
    except Exception:
        return None
    dt = dt or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    target_dir = warehouse_root / table / f"dt={dt}"
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / f"{table}-{datetime.now(timezone.utc).strftime('%H%M%S')}.parquet"
    # materialize rows and transform
    material: List[Dict[str, Any]] = []
    for row in rows:
        r = dict(row)
        if "raw" in r:
            try:
                r["raw_json"] = json.dumps(r["raw"], ensure_ascii=False)
            except Exception:
                r["raw_json"] = None
            del r["raw"]
        material.append(r)
    if not material:
        return None
    table_pa = pa.Table.from_pylist(material)
    pq.write_table(table_pa, out_path)
    return out_path


def extract_sessions(project_root: Path) -> Dict[str, List[Dict[str, Any]]]:
    sessions: List[Dict[str, Any]] = []
    decisions: List[Dict[str, Any]] = []
    action_items: List[Dict[str, Any]] = []
    files_modified: List[Dict[str, Any]] = []
    for md in _iter_session_files(project_root):
        try:
            s, d, a, fm = _parse_session_md(md)
            sessions.append(s)
            decisions.extend(d)
            action_items.extend(a)
            files_modified.extend(fm)
        except Exception:
            continue
    return {
        "sessions": sessions,
        "session_decisions": decisions,
        "session_action_items": action_items,
        "session_files_modified": files_modified,
    }


def extract_events(project_root: Path) -> List[Dict[str, Any]]:
    return list(_iter_events_jsonl(project_root))


def extract_heartbeats(project_root: Path) -> List[Dict[str, Any]]:
    return list(_iter_heartbeats(project_root))


def extract_hive_boxes(project_root: Path) -> Dict[str, List[Dict[str, Any]]]:
    tasks = list(_iter_hive_messages(project_root, "tasks"))
    responses = list(_iter_hive_messages(project_root, "responses"))
    return {"hive_tasks": tasks, "hive_responses": responses}


def derive_agents(events: List[Dict[str, Any]], heartbeats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Build bot_id -> [timestamps]
    from collections import defaultdict
    times = defaultdict(list)
    for ev in events:
        bid = ev.get("bot_id") or "unknown"
        ts = ev.get("ts")
        if ts:
            times[bid].append(ts)
    for hb in heartbeats:
        bid = hb.get("bot_id") or "unknown"
        ts = hb.get("ts")
        if ts:
            times[bid].append(ts)
    out: List[Dict[str, Any]] = []
    for bid, tss in times.items():
        # normalize ISO parse
        def parse_iso(s: str) -> datetime:
            try:
                return datetime.fromisoformat(s.replace("Z", "+00:00"))
            except Exception:
                return datetime.now(timezone.utc)
        parsed = [parse_iso(s) for s in tss]
        if not parsed:
            continue
        first = min(parsed)
        last = max(parsed)
        out.append({
            "bot_id": bid,
            "first_seen": first.isoformat(),
            "last_seen": last.isoformat(),
            "active": True,
        })
    return out


def autorun(project_root: Path) -> Dict[str, Any]:
    """Ensure setup and run a lightweight incremental ETL into staging NDJSON.

    Returns summary dict with written files.
    """
    paths = ensure_setup(project_root)
    staging_root: Path = paths["staging"]
    warehouse_root: Path = paths["warehouse"]

    # Load analytics config for targets
    cfg = {}
    cfg_path = Path(project_root) / ".deia" / "analytics" / "config.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            cfg = {}
    targets = cfg.get("targets", ["staging_ndjson"]) or ["staging_ndjson"]

    # For autorun, just write a daily partition with current snapshots
    sess = extract_sessions(project_root)
    events = extract_events(project_root)
    heartbeats = extract_heartbeats(project_root)
    hive_boxes = extract_hive_boxes(project_root)
    agents = derive_agents(events, heartbeats)

    dt = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    written: Dict[str, str] = {}
    # helper to fan-out to targets
    def emit(table: str, rows: List[Dict[str, Any]]):
        if not rows:
            return
        if "staging_ndjson" in targets:
            nd = write_ndjson(table, rows, staging_root, dt)
            written[table] = str(nd)
        if "parquet" in targets:
            pqpath = write_parquet_if_available(table, rows, warehouse_root, dt)
            if pqpath:
                written[f"{table}_parquet"] = str(pqpath)

    for table, rows in sess.items():
        emit(table, rows)
    emit("events", events)
    emit("heartbeats", heartbeats)
    for table, rows in hive_boxes.items():
        emit(table, rows)
    emit("agents", agents)

    # Update manifest
    manifest = (paths["analytics"]) / "manifest.json"
    run_entry = {
        "run_id": _ts_iso(),
        "project_root": str(project_root),
        "dt": dt,
        "written": written,
        "schema_version": 1,
        "targets": targets,
    }
    try:
        if manifest.exists():
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if isinstance(data, list):
                data.append(run_entry)
            else:
                data = [data, run_entry]
        else:
            data = [run_entry]
        manifest.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass

    return {"paths": {k: str(v) for k, v in paths.items()}, "written": written}


def maybe_autorun_on_launch(project_root: Path) -> Optional[Dict[str, Any]]:
    """Check analytics config and run autorun if enabled.

    Safe no-op if config missing or disabled.
    """
    cfg_path = Path(project_root) / ".deia" / "analytics" / "config.json"
    try:
        if not cfg_path.exists():
            return None
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        if not cfg.get("autorun_on_launch"):
            return None
        return autorun(project_root)
    except Exception:
        return None
