"""
Mock data and fixtures for DEIA testing.
"""

import json
from pathlib import Path
from typing import Dict, List, Any


class MockBOKData:
    """Mock BOK data for testing."""

    SAMPLE_INDEX = {
        "patterns": [
            {
                "id": "bug-fix-001",
                "category": "bug_fixes",
                "title": "Database timeout issue",
                "type": "bug_fix",
                "urgency": "high",
            },
            {
                "id": "best-practice-001",
                "category": "best_practices",
                "title": "Query optimization",
                "type": "best_practice",
                "urgency": "medium",
            },
            {
                "id": "gotcha-001",
                "category": "gotchas",
                "title": "N+1 query problem",
                "type": "gotcha",
                "urgency": "medium",
            },
        ]
    }

    SAMPLE_PATTERN = {
        "title": "How to optimize database queries",
        "pattern_type": "best_practice",
        "problem": "Database queries were slow and causing timeouts in production environments",
        "solution": "Added proper indexing and optimized query execution plans with connection pooling",
        "reasoning": "Indexes speed up lookups, query optimization reduces unnecessary scans, pooling reduces overhead",
        "tags": ["database", "performance", "optimization"],
        "urgency": "medium",
        "when_to_use": "When dealing with slow database performance issues",
        "gotchas": "Indexes slow down writes, so balance read/write patterns carefully",
        "related_patterns": ["index-design", "connection-pooling"],
    }


class MockSessionData:
    """Mock session data for testing."""

    SAMPLE_LOG = """# Session Log - 2025-10-25

### User
What's the best way to optimize database queries?

### Assistant
Database optimization involves several strategies:
1. Proper indexing on frequently queried columns
2. Query execution plan analysis
3. Connection pooling for performance

### User
How do I implement indexing?

### Assistant
Here's a practical approach to database indexing:

```sql
CREATE INDEX idx_name ON table_name(column_name);
```

This creates a B-tree index by default.

### User
Thanks, this is helpful.

### Assistant
You're welcome! Feel free to ask more questions.
"""

    SAMPLE_METADATA = {
        "session_id": "session-001",
        "date": "2025-10-25",
        "duration": "45 minutes",
        "participants": ["User", "Assistant"],
        "tools_used": ["Read", "Write", "Bash"],
        "tags": ["development", "debugging"],
    }


class MockFileStructure:
    """Mock file system structures."""

    @staticmethod
    def create_in_directory(base_path: Path) -> None:
        """Create a mock file structure."""
        # Create directories
        (base_path / "src").mkdir(exist_ok=True)
        (base_path / "docs").mkdir(exist_ok=True)
        (base_path / "tests").mkdir(exist_ok=True)
        (base_path / "config").mkdir(exist_ok=True)

        # Create files
        (base_path / "src" / "main.py").write_text("# Main module\n")
        (base_path / "src" / "utils.py").write_text("# Utils module\n")
        (base_path / "docs" / "guide.md").write_text("# Guide\n")
        (base_path / "config" / "settings.json").write_text('{"key": "value"}')
        (base_path / "README.md").write_text("# Project\n")
        (base_path / ".env").write_text("SECRET=hidden\n")

    FILES = {
        "src/main.py": "# Main module\n",
        "src/utils.py": "# Utils module\n",
        "docs/guide.md": "# Guide\n",
        "config/settings.json": '{"key": "value"}\n',
        "README.md": "# Project\n",
        ".env": "SECRET=hidden\n",
    }


class MockProjectStructure:
    """Mock DEIA project structure."""

    @staticmethod
    def create_deia_project(base_path: Path) -> None:
        """Create a mock DEIA project."""
        deia = base_path / ".deia"
        deia.mkdir(exist_ok=True)

        # Create subdirectories
        directories = [
            "hive/tasks",
            "hive/responses",
            "bok/patterns",
            "index",
            "governance",
            "observations",
            "sessions",
        ]

        for dir_path in directories:
            (deia / dir_path).mkdir(parents=True, exist_ok=True)

        # Create metadata
        metadata = {
            "project_name": "test-project",
            "phase": "Phase 1",
            "team_members": ["Alice", "Bob"],
            "created_date": "2025-10-25",
        }
        (deia / "metadata.json").write_text(json.dumps(metadata, indent=2))

        # Create README
        (base_path / "README.md").write_text("# Test DEIA Project\n")

        # Create mock BOK index
        (deia / "index" / "master-index.yaml").write_text(
            "patterns:\n"
            "  - id: pattern-001\n"
            "    category: best_practices\n"
            "    title: Test Pattern\n"
        )
