from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional


class FlightStore:
    """SQLite-backed store for flights and recaps."""

    def __init__(self, db_path: Optional[Path] = None) -> None:
        if db_path is None:
            db_path = Path.cwd() / ".deia" / "raqcoon_flights.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS flights (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS recaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id TEXT NOT NULL,
                recap_text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def start_flight(self, flight_id: str, title: str) -> Dict:
        started_at = datetime.now(timezone.utc).isoformat()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO flights (id, title, started_at, ended_at) VALUES (?, ?, ?, ?)",
            (flight_id, title, started_at, None),
        )
        self.conn.commit()
        return {"flight_id": flight_id, "title": title, "started_at": started_at}

    def end_flight(self, flight_id: str) -> Dict:
        ended_at = datetime.now(timezone.utc).isoformat()
        cur = self.conn.cursor()
        cur.execute("UPDATE flights SET ended_at = ? WHERE id = ?", (ended_at, flight_id))
        self.conn.commit()
        return {"flight_id": flight_id, "ended_at": ended_at}

    def add_recap(self, flight_id: str, recap_text: str) -> Dict:
        created_at = datetime.now(timezone.utc).isoformat()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO recaps (flight_id, recap_text, created_at) VALUES (?, ?, ?)",
            (flight_id, recap_text, created_at),
        )
        self.conn.commit()
        return {"flight_id": flight_id, "created_at": created_at}

    def list_flights(self) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, started_at, ended_at FROM flights ORDER BY started_at DESC")
        return [dict(row) for row in cur.fetchall()]

    def list_recaps(self, flight_id: Optional[str] = None) -> List[Dict]:
        cur = self.conn.cursor()
        if flight_id:
            cur.execute(
                "SELECT flight_id, recap_text, created_at FROM recaps WHERE flight_id = ? ORDER BY created_at DESC",
                (flight_id,),
            )
        else:
            cur.execute(
                "SELECT flight_id, recap_text, created_at FROM recaps ORDER BY created_at DESC"
            )
        return [dict(row) for row in cur.fetchall()]
