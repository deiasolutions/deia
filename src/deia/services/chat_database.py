"""
Chat Database - Persistent storage for chat history

Uses SQLite for simple deployment, but architecture supports PostgreSQL/MySQL.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json
import logging

logger = logging.getLogger(__name__)


class ChatMessage:
    """Represents a single chat message"""
    def __init__(self, bot_id: str, role: str, content: str, timestamp: Optional[str] = None):
        self.bot_id = bot_id
        self.role = role  # "user" or "assistant"
        self.content = content
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        }


class ChatDatabase:
    """
    SQLite database for chat history persistence.

    Schema:
    - messages: bot_id, role, content, timestamp, created_at
    - sessions: bot_id, started_at, ended_at, message_count
    """

    def __init__(self, db_path: str = ".deia/chat_history.db"):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create connection
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        # Initialize schema
        self._init_schema()
        logger.info(f"ChatDatabase initialized at {self.db_path}")

    def _init_schema(self):
        """Create tables if they don't exist"""
        cursor = self.conn.cursor()

        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_id TEXT NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                message_count INTEGER DEFAULT 0
            )
        """)

        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_bot_id
            ON messages(bot_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_timestamp
            ON messages(timestamp)
        """)

        self.conn.commit()
        logger.info("Database schema initialized")

    def add_message(self, bot_id: str, role: str, content: str, timestamp: Optional[str] = None):
        """
        Add a message to chat history.

        Args:
            bot_id: Bot ID
            role: "user" or "assistant"
            content: Message content
            timestamp: ISO timestamp (optional, uses now if not provided)
        """
        if role not in ["user", "assistant"]:
            raise ValueError("role must be 'user' or 'assistant'")

        timestamp = timestamp or datetime.now().isoformat()

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO messages (bot_id, role, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (bot_id, role, content, timestamp))
        self.conn.commit()
        logger.debug(f"Added message for {bot_id}: {role}")

    def get_messages(self, bot_id: str, limit: int = 100) -> List[Dict]:
        """
        Get messages for a bot.

        Args:
            bot_id: Bot ID
            limit: Max messages to return

        Returns:
            List of message dicts with role, content, timestamp
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT role, content, timestamp FROM messages
            WHERE bot_id = ?
            ORDER BY timestamp ASC
            LIMIT ?
        """, (bot_id, limit))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def clear_messages(self, bot_id: str):
        """
        Clear all messages for a bot.

        Args:
            bot_id: Bot ID
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM messages WHERE bot_id = ?", (bot_id,))
        self.conn.commit()
        logger.info(f"Cleared messages for {bot_id}")

    def get_session_count(self, bot_id: str) -> int:
        """Get number of sessions for a bot"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM messages WHERE bot_id = ?
        """, (bot_id,))
        result = cursor.fetchone()
        return result["count"] if result else 0

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
