"""
Minutes Bot - lightweight minute-by-minute activity logger for DEIA sessions.

Creates a minute-level Markdown diary, emits JSONL telemetry (incl. RSE feed),
and links to the active DEIA session when starting/stopping.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


ISO = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class MinutesState:
    topic: str
    interval: int
    file: str
    start_ts: str
    open_start: Optional[str] = None
    open_text: Optional[str] = None
    pending_text: Optional[str] = None


class MinutesManager:
    def __init__(self, project_root: Optional[Path] = None):
        self.root = Path(project_root) if project_root else Path.cwd()
        self.minutes_dir = self.root / ".deia" / "minutes"
        self.minutes_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.minutes_dir / ".state.json"
        self.index_file = self.minutes_dir / "INDEX.md"
        self.telemetry_dir = self.root / ".deia" / "telemetry"
        self.telemetry_dir.mkdir(parents=True, exist_ok=True)
        self.telemetry_jsonl = self.telemetry_dir / "telemetry.jsonl"
        self.rse_jsonl = self.telemetry_dir / "rse.jsonl"

    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime(ISO)

    def _write_jsonl(self, path: Path, rec: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")

    def _emit_telemetry(self, event: str, ctx: dict | None = None, data: dict | None = None) -> None:
        rec = {
            "ts": self._now(),
            "event": event,
            "ctx": ctx or {},
            "data": data or {},
        }
        self._write_jsonl(self.telemetry_jsonl, rec)
        # Mirror to RSE feed with a lane for Minutes
        rse = {"ts": rec["ts"], "type": event, "lane": "Minutes", "actor": "Edge", "data": rec["data"]}
        self._write_jsonl(self.rse_jsonl, rse)

    def _read_state(self) -> Optional[MinutesState]:
        if not self.state_file.exists():
            return None
        try:
            obj = json.loads(self.state_file.read_text(encoding="utf-8"))
            return MinutesState(**obj)
        except Exception:
            return None

    def _write_state(self, st: MinutesState) -> None:
        self.state_file.write_text(json.dumps(asdict(st), indent=2), encoding="utf-8")

    def _minutes_path(self, topic: str) -> Path:
        stamp = datetime.now().strftime("%Y%m%d-%H%M")
        safe = "".join(c for c in topic if c.isalnum() or c in ("-", "_")).strip() or "session"
        return self.minutes_dir / f"{stamp}-{safe}.md"

    def _append_index(self, path: Path, topic: str) -> None:
        if not self.index_file.exists():
            self.index_file.write_text("# DEIA Minutes Index\n\n", encoding="utf-8")
        with self.index_file.open("a", encoding="utf-8") as f:
            f.write(f"- {datetime.now().strftime('%Y-%m-%d %H:%M')} — {topic} → `{path}`\n")

    def _append_line(self, file: Path, line: str) -> None:
        with file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def start(self, topic: str, interval: int = 60, loop: bool = False) -> Path:
        # Resume if already running
        st = self._read_state()
        if st and st.topic == topic:
            return Path(st.file)
        path = self._minutes_path(topic)
        header = (
            f"# Minutes — {topic}\n\n"
            f"Started: {self._now()}\n\n"
            f"Format: ISO_START — ISO_END — Summary\n\n"
        )
        path.write_text(header, encoding="utf-8")
        self._append_index(path, topic)
        st = MinutesState(topic=topic, interval=interval, file=str(path), start_ts=self._now())
        self._write_state(st)
        self._emit_telemetry("minute_start", {"topic": topic}, {})
        # Link in DEIA session (best-effort)
        try:
            from .logger import ConversationLogger

            logger = ConversationLogger(self.root)
            sess = logger.get_latest_session()
            if sess:
                logger.append_to_session(sess, f"Minutes started for '{topic}': {path}")
        except Exception:
            pass
        if loop:
            try:
                while True:
                    self.tick()
                    time.sleep(max(5, interval))
            except KeyboardInterrupt:
                self.stop()
        return path

    def write(self, text: str) -> None:
        st = self._read_state()
        if not st:
            raise RuntimeError("Minutes not started. Run: deia minutes start --topic <topic>")
        st.pending_text = text.strip()
        self._write_state(st)
        self._emit_telemetry("minute_write", {"topic": st.topic}, {"text": st.pending_text})

    def tick(self) -> None:
        st = self._read_state()
        if not st:
            return
        file = Path(st.file)
        now = self._now()
        # Open a new interval if none, or if pending_text changed
        if not st.open_start:
            st.open_start = now
            st.open_text = st.pending_text or "(unchanged)"
            self._append_line(file, f"{st.open_start} — {now} — {st.open_text}")
        else:
            # Extend or roll
            if (st.pending_text or "(unchanged)") != (st.open_text or ""):
                # Close previous by rewriting last line's end time and append new
                lines = file.read_text(encoding="utf-8").splitlines()
                if lines:
                    last = lines[-1]
                    if " — " in last:
                        parts = last.split(" — ")
                        parts[1] = now
                        lines[-1] = " — ".join(parts)
                        file.write_text("\n".join(lines) + "\n", encoding="utf-8")
                # Open new
                st.open_start = now
                st.open_text = st.pending_text or "(unchanged)"
                self._append_line(file, f"{st.open_start} — {now} — {st.open_text}")
            else:
                # Extend current: update end time of last line
                lines = file.read_text(encoding="utf-8").splitlines()
                if lines:
                    last = lines[-1]
                    if " — " in last:
                        parts = last.split(" — ")
                        parts[1] = now
                        lines[-1] = " — ".join(parts)
                        file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self._write_state(st)
        self._emit_telemetry("minute_tick", {"topic": st.topic, "file": st.file}, {})

    def stop(self) -> Optional[Path]:
        st = self._read_state()
        if not st:
            return None
        path = Path(st.file)
        # Close last interval (already extended to now by tick semantics)
        self._emit_telemetry("minute_stop", {"topic": st.topic, "file": st.file}, {})
        try:
            from .logger import ConversationLogger

            logger = ConversationLogger(self.root)
            sess = logger.get_latest_session()
            if sess:
                logger.append_to_session(sess, f"Minutes stopped for '{st.topic}': {path}")
        except Exception:
            pass
        self.state_file.unlink(missing_ok=True)
        return path

    def report(self) -> Path:
        # For v0.1, emit a one-line JSONL summary event and return path to minutes file
        st = self._read_state()
        minutes_file = Path(st.file) if st else None
        self._emit_telemetry("minute_report", {"topic": st.topic if st else ""}, {"minutes": str(minutes_file) if minutes_file else ""})
        return minutes_file or Path()

