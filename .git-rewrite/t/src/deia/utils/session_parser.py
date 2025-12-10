"""
Parse DEIA session log format.

Extracts structured data from session markdown files.
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Message:
    """Represents a single message in a session."""

    speaker: str  # "User", "Assistant", "System"
    content: str
    line_number: int
    is_code_block: bool = False


@dataclass
class SessionMetadata:
    """Metadata extracted from session."""

    session_id: str
    date: str
    duration: Optional[str] = None
    participant_count: int = 2
    tools_used: List[str] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tools_used is None:
            self.tools_used = []
        if self.tags is None:
            self.tags = []


class SessionParser:
    """Parse DEIA session log markdown files."""

    # Session header patterns
    SESSION_ID_PATTERN = r"session[-_](\w+)"
    DATE_PATTERN = r"(\d{4}-\d{2}-\d{2})"
    SPEAKER_PATTERN = r"^### (.+?)[\s\n]"  # ### Speaker format

    @staticmethod
    def parse_file(file_path: str) -> Tuple[SessionMetadata, List[Message]]:
        """
        Parse a session log file.

        Args:
            file_path: Path to session markdown file

        Returns:
            Tuple of (metadata, messages)
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return SessionParser.parse_content(content, file_path)

    @staticmethod
    def parse_content(content: str, source_id: str = "unknown") -> Tuple[SessionMetadata, List[Message]]:
        """
        Parse session content.

        Args:
            content: Full session markdown content
            source_id: Source identifier (filename, ID, etc)

        Returns:
            Tuple of (metadata, messages)
        """
        metadata = SessionParser._extract_metadata(content, source_id)
        messages = SessionParser._extract_messages(content)

        return metadata, messages

    @staticmethod
    def _extract_metadata(content: str, source_id: str) -> SessionMetadata:
        """Extract metadata from session content."""
        # Extract session ID from filename or content
        session_id_match = re.search(SessionParser.SESSION_ID_PATTERN, source_id)
        session_id = session_id_match.group(1) if session_id_match else source_id

        # Extract date
        date_match = re.search(SessionParser.DATE_PATTERN, content)
        date = date_match.group(1) if date_match else "unknown"

        # Extract tools mentioned
        tools = SessionParser._extract_tools_mentioned(content)

        # Extract tags from metadata blocks
        tags = SessionParser._extract_tags(content)

        return SessionMetadata(
            session_id=session_id,
            date=date,
            tools_used=tools,
            tags=tags,
        )

    @staticmethod
    def _extract_messages(content: str) -> List[Message]:
        """Extract individual messages from session."""
        messages = []
        lines = content.split("\n")
        current_speaker = None
        current_content = []
        current_line = 0
        in_code_block = False

        for i, line in enumerate(lines):
            # Track code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block

            # Check for speaker markers (### Speaker:)
            speaker_match = re.match(r"^### (.+?)(?::|\s|$)", line)

            if speaker_match:
                # Save previous message if exists
                if current_speaker and current_content:
                    messages.append(
                        Message(
                            speaker=current_speaker,
                            content="\n".join(current_content).strip(),
                            line_number=current_line,
                            is_code_block=in_code_block,
                        )
                    )

                current_speaker = speaker_match.group(1).strip()
                current_content = []
                current_line = i
            elif current_speaker:
                # Accumulate content
                current_content.append(line)

        # Save final message
        if current_speaker and current_content:
            messages.append(
                Message(
                    speaker=current_speaker,
                    content="\n".join(current_content).strip(),
                    line_number=current_line,
                    is_code_block=in_code_block,
                )
            )

        return messages

    @staticmethod
    def _extract_tools_mentioned(content: str) -> List[str]:
        """Extract tool names mentioned in session."""
        tools = []

        # Common DEIA tools
        tool_patterns = [
            r"\b(Read|Write|Edit|Bash|Glob|Grep|WebFetch|Task)\b",
            r"(pytest|pip|docker|git|npm|yarn)",
        ]

        for pattern in tool_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            tools.extend([m for m in matches if m])

        # Return unique, normalized
        return list(set([t.lower() for t in tools]))

    @staticmethod
    def _extract_tags(content: str) -> List[str]:
        """Extract tags from session metadata."""
        tags = []

        # Look for tags in metadata blocks
        tag_patterns = [
            r"tags?:\s*(.+?)(?:\n|$)",  # tags: ...
            r"#(\w+)",  # #tag format
        ]

        for pattern in tag_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Split on comma/space if multiple
                if isinstance(match, str):
                    tag_list = [t.strip() for t in re.split(r"[,\s]+", match)]
                    tags.extend(tag_list)

        return list(set([t for t in tags if t]))  # Unique, non-empty

    @staticmethod
    def segment_by_topic(messages: List[Message]) -> Dict[str, List[Message]]:
        """
        Segment messages by potential topics.

        Uses heuristics to identify major topic shifts in conversation.
        """
        segments = {}
        current_topic = "general"
        current_messages = []

        for msg in messages:
            # Simple heuristic: speaker change or long gap might indicate new topic
            if msg.speaker == "User":
                # Check if this looks like a new topic
                if "?" in msg.content and len(current_messages) > 5:
                    # Start new segment
                    if current_messages:
                        segments[current_topic] = current_messages
                    current_topic = f"topic_{len(segments)}"
                    current_messages = [msg]
                else:
                    current_messages.append(msg)
            else:
                current_messages.append(msg)

        # Save final segment
        if current_messages:
            segments[current_topic] = current_messages

        return segments

    @staticmethod
    def get_conversation_summary(messages: List[Message]) -> str:
        """Get a brief summary of the conversation."""
        if not messages:
            return "Empty conversation"

        user_turns = len([m for m in messages if m.speaker == "User"])
        assistant_turns = len([m for m in messages if m.speaker == "Assistant"])
        total_words = sum(len(m.content.split()) for m in messages)

        summary = (
            f"{user_turns} user messages, {assistant_turns} assistant responses, "
            f"~{total_words} words total"
        )

        return summary
