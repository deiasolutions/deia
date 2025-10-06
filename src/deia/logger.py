"""
DEIA Conversation Logger - Real-time logging of Claude Code sessions
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json


class ConversationLogger:
    """Logs Claude Code conversations to .deia/sessions/"""

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize conversation logger

        Args:
            project_root: Root directory of the project (defaults to current directory)
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.sessions_dir = self.project_root / ".deia" / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.sessions_dir / "INDEX.md"

    def create_session_log(
        self,
        context: str,
        transcript: str,
        decisions: list[str],
        action_items: list[str],
        files_modified: list[str],
        next_steps: str,
        status: str = "Active",
        update_project_resume: bool = True
    ) -> Path:
        """
        Create a new conversation log file

        Args:
            context: What were we working on?
            transcript: Full conversation transcript
            decisions: List of key decisions made
            action_items: What was done, what's pending
            files_modified: List of files created/modified
            next_steps: What should happen next session
            status: Active or Completed

        Returns:
            Path to the created log file
        """
        timestamp = datetime.now()
        filename = timestamp.strftime("%Y%m%d-%H%M%S-conversation.md")
        filepath = self.sessions_dir / filename
        session_id = filename.replace(".md", "")

        # Format decisions
        decisions_text = "\n".join(f"- {d}" for d in decisions) if decisions else "None recorded"

        # Format action items
        action_items_text = "\n".join(f"- {a}" for a in action_items) if action_items else "None recorded"

        # Format files modified
        files_text = "\n".join(f"- `{f}`" for f in files_modified) if files_modified else "None recorded"

        # Create log content
        content = f"""# DEIA Conversation Log

**Date:** {timestamp.isoformat()}
**Session ID:** {session_id}
**Status:** {status}

---

## Context
{context}

---

## Full Transcript
{transcript}

---

## Key Decisions Made
{decisions_text}

---

## Action Items
{action_items_text}

---

## Files Modified
{files_text}

---

## Next Steps
{next_steps}

---

*Logged automatically by DEIA conversation logger*
*This is Dave's insurance against crashes - never lose context again*
"""

        # Write log file
        filepath.write_text(content, encoding='utf-8')

        # Update index
        self._update_index(session_id, timestamp, context, status)

        # Update project_resume.md
        if update_project_resume:
            self._update_project_resume(session_id, timestamp, context, decisions, files_modified)

        return filepath

    def _update_index(self, session_id: str, timestamp: datetime, context: str, status: str):
        """Update the sessions INDEX.md file"""

        # Create index if doesn't exist
        if not self.index_file.exists():
            self.index_file.write_text(
                "# DEIA Session Index\n\n"
                "**All Claude Code conversations logged here**\n\n"
                "---\n\n"
                "## Sessions\n\n",
                encoding='utf-8'
            )

        # Append entry
        entry = (
            f"### {session_id}\n"
            f"- **Date:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"- **Status:** {status}\n"
            f"- **Context:** {context}\n"
            f"- **File:** `.deia/sessions/{session_id}.md`\n\n"
        )

        with open(self.index_file, 'a', encoding='utf-8') as f:
            f.write(entry)

    def append_to_session(self, session_file: Path, new_content: str):
        """
        Append content to an existing session log

        Args:
            session_file: Path to the session log file
            new_content: Content to append
        """
        if not session_file.exists():
            raise FileNotFoundError(f"Session file not found: {session_file}")

        with open(session_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n---\n\n## Update: {datetime.now().isoformat()}\n\n{new_content}\n")

    def get_latest_session(self) -> Optional[Path]:
        """Get the most recent session log file"""
        session_files = sorted(self.sessions_dir.glob("*-conversation.md"), reverse=True)
        return session_files[0] if session_files else None

    def mark_session_complete(self, session_file: Path):
        """Mark a session as completed in the log file"""
        if not session_file.exists():
            raise FileNotFoundError(f"Session file not found: {session_file}")

        content = session_file.read_text(encoding='utf-8')
        updated_content = content.replace("**Status:** Active", "**Status:** Completed")
        session_file.write_text(updated_content, encoding='utf-8')

    def _update_project_resume(self, session_id: str, timestamp: datetime, context: str,
                                decisions: list[str], files_modified: list[str]):
        """
        Update project_resume.md with reference to this conversation log

        Args:
            session_id: Unique session identifier
            timestamp: Session timestamp
            context: Brief description of what was worked on
            decisions: List of key decisions
            files_modified: List of files created/modified
        """
        resume_file = self.project_root / "project_resume.md"

        # Create template if doesn't exist
        if not resume_file.exists():
            template = """# DEIA Project Resume

**Quick Start for Claude Code:** Read the latest session log below to see what happened in the last conversation.

**Last Updated:** {timestamp}

---

## Latest Session Logs

**📋 Read these in reverse chronological order to catch up on recent work.**

""".format(timestamp=timestamp.isoformat())
            resume_file.write_text(template, encoding='utf-8')

        # Read current content
        content = resume_file.read_text(encoding='utf-8')

        # Format decisions summary
        decisions_summary = decisions[:3] if decisions else []  # First 3 decisions only
        decisions_text = "\n".join(f"- {d}" for d in decisions_summary)
        if len(decisions) > 3:
            decisions_text += f"\n- ... and {len(decisions) - 3} more"

        # Format files summary
        files_summary = files_modified[:5] if files_modified else []  # First 5 files only
        files_text = "\n".join(f"- {f}" for f in files_summary)
        if len(files_modified) > 5:
            files_text += f"\n- ... and {len(files_modified) - 5} more"

        # Create entry
        entry = f"""### [{timestamp.strftime('%Y-%m-%d %H:%M')}] {session_id}
**Context:** {context}

**Key decisions:**
{decisions_text if decisions_text else "None recorded"}

**Files modified:**
{files_text if files_text else "None"}

**Full log:** `.deia/sessions/{session_id}.md`

---

"""

        # Update "Last Updated" timestamp
        content = content.replace(
            f"**Last Updated:** {content.split('**Last Updated:** ')[1].split('\\n')[0]}",
            f"**Last Updated:** {timestamp.isoformat()}"
        )

        # Insert after "## Latest Session Logs" header
        if "## Latest Session Logs" in content:
            # Find the position after the header and introductory text
            parts = content.split("**📋 Read these in reverse chronological order to catch up on recent work.**\n\n")
            if len(parts) == 2:
                # Insert new entry at the top of the list
                updated_content = parts[0] + "**📋 Read these in reverse chronological order to catch up on recent work.**\n\n" + entry + parts[1]
                resume_file.write_text(updated_content, encoding='utf-8')
            else:
                # Fallback: append at end
                resume_file.write_text(content + "\n" + entry, encoding='utf-8')
        else:
            # Fallback: append at end
            resume_file.write_text(content + "\n" + entry, encoding='utf-8')


def quick_log(context: str, transcript: str, **kwargs) -> Path:
    """
    Quick helper function to log a conversation

    Args:
        context: Brief description of what was worked on
        transcript: Full conversation text
        **kwargs: Additional optional parameters (decisions, action_items, files_modified, next_steps)

    Returns:
        Path to created log file
    """
    logger = ConversationLogger()
    return logger.create_session_log(
        context=context,
        transcript=transcript,
        decisions=kwargs.get('decisions', []),
        action_items=kwargs.get('action_items', []),
        files_modified=kwargs.get('files_modified', []),
        next_steps=kwargs.get('next_steps', "Continue from this conversation"),
        status=kwargs.get('status', 'Active')
    )


if __name__ == "__main__":
    # Example usage
    logger = ConversationLogger()
    log_file = logger.create_session_log(
        context="Building automated conversation logging system",
        transcript="[Full conversation would go here]",
        decisions=["Create real-time logging", "Use Python + slash command approach"],
        action_items=["Build logger.py", "Create slash command", "Test logging"],
        files_modified=["src/deia/logger.py", ".claude/commands/log-conversation.md"],
        next_steps="Test the logging system with a real conversation"
    )
    print(f"Created log: {log_file}")
