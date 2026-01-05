from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional


class MessageStore:
    """SQLite-backed message store for local-first persistence."""

    def __init__(self, db_path: Optional[Path] = None) -> None:
        if db_path is None:
            db_path = Path.cwd() / ".deia" / "raqcoon_messages.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT NOT NULL,
                author TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                lane TEXT,
                provider TEXT,
                token_count INTEGER
            )
            """
        )
        self._ensure_columns(
            {
                "lane": "TEXT",
                "provider": "TEXT",
                "token_count": "INTEGER",
            }
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_messages_channel ON messages(channel_id)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_messages_time ON messages(timestamp)"
        )
        self.conn.commit()

    def _ensure_columns(self, columns: Dict[str, str]) -> None:
        cur = self.conn.cursor()
        cur.execute("PRAGMA table_info(messages)")
        existing = {row["name"] for row in cur.fetchall()}
        for name, col_type in columns.items():
            if name not in existing:
                cur.execute(f"ALTER TABLE messages ADD COLUMN {name} {col_type}")
        self.conn.commit()

    def add_message(
        self,
        channel_id: str,
        author: str,
        content: str,
        lane: Optional[str] = None,
        provider: Optional[str] = None,
        token_count: Optional[int] = None,
    ) -> Dict:
        timestamp = datetime.now(timezone.utc).isoformat()
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO messages (channel_id, author, content, timestamp, lane, provider, token_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (channel_id, author, content, timestamp, lane, provider, token_count),
        )
        self.conn.commit()
        return {
            "channel_id": channel_id,
            "author": author,
            "content": content,
            "timestamp": timestamp,
            "lane": lane,
            "provider": provider,
            "token_count": token_count,
        }

    def get_messages(self, channel_id: Optional[str] = None, limit: int = 200) -> List[Dict]:
        cur = self.conn.cursor()
        if channel_id:
            cur.execute(
                """
                SELECT channel_id, author, content, timestamp, lane, provider, token_count
                FROM messages
                WHERE channel_id = ?
                ORDER BY id ASC
                LIMIT ?
                """,
                (channel_id, limit),
            )
        else:
            cur.execute(
                """
                SELECT channel_id, author, content, timestamp, lane, provider, token_count
                FROM messages
                ORDER BY id ASC
                LIMIT ?
                """,
                (limit,),
            )
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def get_summary(self) -> Dict:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT COUNT(*) as total_messages,
                   COALESCE(SUM(token_count), 0) as total_tokens
            FROM messages
            """
        )
        row = cur.fetchone()
        summary = {
            "total_messages": row["total_messages"] if row else 0,
            "total_tokens": row["total_tokens"] if row else 0,
        }
        cur.execute(
            """
            SELECT provider, COUNT(*) as count
            FROM messages
            WHERE provider IS NOT NULL AND provider != ''
            GROUP BY provider
            """
        )
        summary["by_provider"] = {r["provider"]: r["count"] for r in cur.fetchall()}
        cur.execute(
            """
            SELECT lane, COUNT(*) as count
            FROM messages
            WHERE lane IS NOT NULL AND lane != ''
            GROUP BY lane
            """
        )
        summary["by_lane"] = {r["lane"]: r["count"] for r in cur.fetchall()}
        return summary
