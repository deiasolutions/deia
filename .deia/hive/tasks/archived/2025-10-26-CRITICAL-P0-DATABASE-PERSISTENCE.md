# TASK: P0 CRITICAL - Database Persistence for Chat History

**Priority:** P0 CRITICAL (Data Loss Risk)
**Time Estimate:** 60 minutes
**Start:** After BOT-004 completes ServiceFactory
**Impact:** Without this, all chat history lost on server restart

---

## PROBLEM

Currently chat history is **in-memory only** (`dict chat_history = {}`).

**Consequences:**
- ❌ All conversations lost when server restarts
- ❌ No chat history persistence across sessions
- ❌ No way to retrieve old conversations
- ❌ Production-grade reliability impossible

---

## SOLUTION

Replace in-memory `chat_history` with SQLite database.

---

## PART 1: Create Database Models

**File:** `src/deia/services/chat_database.py` (NEW)

```python
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
        logger.debug(f"Message added to {bot_id}: {role}")

    def get_messages(self, bot_id: str, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Get chat messages for a bot.

        Args:
            bot_id: Bot ID
            limit: Max messages to return (default 100)
            offset: Pagination offset (default 0)

        Returns:
            List of messages in format: [{"role": "...", "content": "...", "timestamp": "..."}]
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT role, content, timestamp
            FROM messages
            WHERE bot_id = ?
            ORDER BY timestamp ASC
            LIMIT ? OFFSET ?
        """, (bot_id, limit, offset))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def clear_messages(self, bot_id: str):
        """Clear all messages for a bot"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM messages WHERE bot_id = ?", (bot_id,))
        self.conn.commit()
        logger.info(f"Cleared messages for {bot_id}")

    def get_message_count(self, bot_id: str) -> int:
        """Get number of messages for a bot"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM messages WHERE bot_id = ?", (bot_id,))
        return cursor.fetchone()["count"]

    def close(self):
        """Close database connection"""
        self.conn.close()
        logger.info("ChatDatabase connection closed")
```

---

## PART 2: Update chat_interface_app.py

**Location:** Top of `src/deia/services/chat_interface_app.py`

**Add imports:**
```python
from deia.services.chat_database import ChatDatabase
```

**Replace this line:**
```python
# OLD:
chat_history = {}

# NEW:
chat_database = ChatDatabase(".deia/chat_history.db")
```

---

## PART 3: Update History Retrieval Endpoint

**Location:** Find `@app.get("/api/chat/history")` (around line ~500)

**Replace with:**

```python
@app.get("/api/chat/history")
async def get_chat_history(bot_id: str = None, limit: int = 100, offset: int = 0):
    """
    Get chat history for a bot from database.

    Args:
        bot_id: Bot ID (required)
        limit: Max messages (default 100)
        offset: Pagination offset (default 0)

    Returns:
        {"messages": [...], "total": N, "limit": L, "offset": O}
    """
    try:
        if not bot_id:
            return {
                "success": False,
                "error": "bot_id is required",
                "timestamp": datetime.now().isoformat()
            }

        bot_id = bot_id.strip()

        # Get messages from database
        messages = chat_database.get_messages(bot_id, limit=limit, offset=offset)
        total = chat_database.get_message_count(bot_id)

        return {
            "success": True,
            "messages": messages,
            "total": total,
            "limit": limit,
            "offset": offset,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

---

## PART 4: Update WebSocket Message Handling

**Location:** Find the WebSocket message handling in `@app.websocket("/ws")` (around line ~200)

**Update the message storage section:**

```python
# OLD CODE (REMOVE):
# chat_history.setdefault(bot_id, []).append({"role": "assistant", "content": response})

# NEW CODE (ADD):
chat_database.add_message(bot_id, "assistant", response)
```

Also update where user messages are stored:

```python
# OLD CODE (REMOVE):
# chat_history.setdefault(bot_id, []).append({"role": "user", "content": user_input})

# NEW CODE (ADD):
chat_database.add_message(bot_id, "user", user_input)
```

---

## PART 5: Create Tests

**File:** `tests/unit/test_chat_database.py` (NEW)

```python
"""Tests for ChatDatabase"""

import pytest
import tempfile
from pathlib import Path
from deia.services.chat_database import ChatDatabase, ChatMessage


def test_chat_database_init():
    """Test database initialization"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = f"{tmpdir}/test.db"
        db = ChatDatabase(db_path)
        assert Path(db_path).exists()
        db.close()


def test_add_message():
    """Test adding messages"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = ChatDatabase(f"{tmpdir}/test.db")

        db.add_message("BOT-001", "user", "Hello")
        db.add_message("BOT-001", "assistant", "Hi there!")

        count = db.get_message_count("BOT-001")
        assert count == 2
        db.close()


def test_get_messages():
    """Test retrieving messages"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = ChatDatabase(f"{tmpdir}/test.db")

        db.add_message("BOT-001", "user", "Hello")
        db.add_message("BOT-001", "assistant", "Hi there!")

        messages = db.get_messages("BOT-001")
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"
        db.close()


def test_clear_messages():
    """Test clearing messages"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = ChatDatabase(f"{tmpdir}/test.db")

        db.add_message("BOT-001", "user", "Hello")
        db.add_message("BOT-001", "assistant", "Hi")

        db.clear_messages("BOT-001")
        count = db.get_message_count("BOT-001")
        assert count == 0
        db.close()


def test_pagination():
    """Test message pagination"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = ChatDatabase(f"{tmpdir}/test.db")

        # Add 10 messages
        for i in range(10):
            db.add_message("BOT-001", "user", f"Message {i}")

        # Get first 5
        messages = db.get_messages("BOT-001", limit=5, offset=0)
        assert len(messages) == 5

        # Get next 5
        messages = db.get_messages("BOT-001", limit=5, offset=5)
        assert len(messages) == 5
        db.close()


def test_multiple_bots():
    """Test isolation between bots"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = ChatDatabase(f"{tmpdir}/test.db")

        db.add_message("BOT-001", "user", "Hello")
        db.add_message("BOT-002", "user", "Hi")

        count_001 = db.get_message_count("BOT-001")
        count_002 = db.get_message_count("BOT-002")

        assert count_001 == 1
        assert count_002 == 1
        db.close()
```

---

## TESTING

```bash
# Test database functionality
pytest tests/unit/test_chat_database.py -v

# Test updated endpoints
pytest tests/unit/test_chat_api_endpoints.py::TestChatHistory -v
```

---

## MIGRATION FROM IN-MEMORY

**Optional: Migrate existing in-memory history to database**

Add this helper (use once if needed):

```python
def migrate_to_database(old_chat_history: dict, db: ChatDatabase):
    """Migrate in-memory chat_history to database"""
    for bot_id, messages in old_chat_history.items():
        for msg in messages:
            db.add_message(
                bot_id,
                msg.get("role", "assistant"),
                msg.get("content", ""),
                msg.get("timestamp")
            )
    logger.info(f"Migrated {len(old_chat_history)} bots to database")
```

---

## CHECKLIST

- [ ] Create `chat_database.py` with ChatDatabase class
- [ ] Update chat_interface_app.py imports
- [ ] Replace in-memory dict with database
- [ ] Update WebSocket message storage
- [ ] Update `/api/chat/history` endpoint
- [ ] Create tests in `test_chat_database.py`
- [ ] Tests passing
- [ ] Verify chat history persists across restarts
- [ ] Create completion report

---

## COMPLETION

When finished, create: `.deia/hive/responses/deiasolutions/p0-database-persistence-complete.md`

Write:
- SQLite database implemented
- All messages now persistent
- Tests passing
- Server restarts no longer lose chat history
- Ready for authentication work
