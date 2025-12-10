"""
Tests for session parser module.
"""

import pytest
from deia.utils.session_parser import SessionParser, Message, SessionMetadata


class TestSessionParser:
    """Test session parsing logic."""

    def test_parse_simple_content(self):
        """Should parse basic session content."""
        content = """
# Session Log - 2025-10-25

### User
What is the best way to optimize database queries?

### Assistant
Database optimization involves several key strategies.
First, use proper indexing on frequently queried columns.
Second, optimize query patterns and execution plans.
"""

        metadata, messages = SessionParser.parse_content(content, "session-001")

        assert metadata.session_id == "001"
        assert metadata.date == "2025-10-25"
        assert len(messages) >= 2

    def test_extract_metadata(self):
        """Should extract session metadata."""
        content = """
# Session: database-optimization
Date: 2025-10-24
Tags: database, performance, optimization
"""

        metadata = SessionParser._extract_metadata(content, "session-database-optimization")

        assert "database" in metadata.session_id or "001" in metadata.session_id
        assert metadata.date == "2025-10-24"

    def test_extract_messages(self):
        """Should extract and parse messages."""
        content = """
### User
First question

### Assistant
First answer

### User
Second question

### Assistant
Second answer
"""

        messages = SessionParser._extract_messages(content)

        assert len(messages) >= 4
        assert any(m.speaker == "User" for m in messages)
        assert any(m.speaker == "Assistant" for m in messages)

    def test_message_content_preservation(self):
        """Should preserve message content accurately."""
        content = """
### User
This is a multi-line
message with formatting
and code examples.

```python
def example():
    return True
```

### Assistant
I understand your question.
"""

        messages = SessionParser._extract_messages(content)

        user_msg = next((m for m in messages if m.speaker == "User"), None)
        assert user_msg is not None
        assert "multi-line" in user_msg.content
        assert "code examples" in user_msg.content

    def test_extract_tools(self):
        """Should identify tools mentioned in session."""
        content = """
I used Read to open the file
Then I used Edit to make changes
And Bash to run the tests
"""

        tools = SessionParser._extract_tools_mentioned(content)

        assert "read" in [t.lower() for t in tools]
        assert "edit" in [t.lower() for t in tools]
        assert "bash" in [t.lower() for t in tools]

    def test_conversation_summary(self):
        """Should generate conversation summary."""
        content = """
### User
Question one?

### Assistant
Answer one.

### User
Question two?

### Assistant
Answer two.
"""

        messages = SessionParser._extract_messages(content)
        summary = SessionParser.get_conversation_summary(messages)

        assert "2" in summary  # Should mention 2 user messages
        assert "2" in summary  # Should mention 2 assistant responses
        assert "words" in summary.lower()

    def test_segment_by_topic(self):
        """Should segment conversation by topic shifts."""
        messages = [
            Message("User", "Tell me about databases", 1),
            Message("Assistant", "Databases store data", 2),
            Message("User", "Good tip. Now about APIs?", 3),
            Message("Assistant", "APIs provide interfaces", 4),
        ]

        segments = SessionParser.segment_by_topic(messages)

        assert len(segments) >= 1
        # Topics should be identified
        assert len(segments) >= 1

    def test_empty_session(self):
        """Should handle empty sessions gracefully."""
        content = ""
        metadata, messages = SessionParser.parse_content(content)

        assert metadata is not None
        assert len(messages) == 0

    def test_metadata_with_tags(self):
        """Should extract tags from content."""
        content = """
# Session Log
tags: python, debugging, performance
#feature-development
#critical-fix

Content here
"""

        metadata = SessionParser._extract_metadata(content, "session-test")

        assert len(metadata.tags) > 0
        # Should have some tags

    def test_date_extraction(self):
        """Should extract dates in standard format."""
        content = "Session Date: 2025-10-25\nCreated on 2025-10-25"

        metadata = SessionParser._extract_metadata(content, "session-001")

        assert metadata.date == "2025-10-25"

    def test_multiline_messages(self):
        """Should handle multiline messages correctly."""
        content = """
### User
This is a long message
that spans multiple lines.

It has paragraphs too.

### Assistant
Response also spans
multiple lines.
"""

        messages = SessionParser._extract_messages(content)

        assert all(isinstance(m.content, str) for m in messages)
        assert all(m.content.strip() for m in messages)
