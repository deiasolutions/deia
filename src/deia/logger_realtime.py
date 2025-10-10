"""
Real-time logging extension for DEIA

Add this to logger.py:

1. In __init__, add:
   self.current_session_file = None

2. Add this method to ConversationLogger class:
"""

from datetime import datetime
from pathlib import Path
from typing import Optional


def log_step(self, action: str, files_modified: Optional[list[str]] = None,
             decision: Optional[str] = None, next_step: Optional[str] = None):
    """
    Log a single step in real-time (for auto_log mode)

    Usage:
        logger = ConversationLogger()
        logger.log_step(
            action="Created authentication module",
            files_modified=["src/auth.py"],
            decision="Using JWT tokens instead of sessions",
            next_step="Add rate limiting"
        )

    Args:
        action: What was done in this step
        files_modified: Files created/modified in this step
        decision: Key decision made (if any)
        next_step: What comes next (if known)
    """
    timestamp = datetime.now()

    # Create a session file if we don't have one yet
    if self.current_session_file is None or not self.current_session_file.exists():
        filename = timestamp.strftime("%Y%m%d-%H%M%S-realtime.md")
        self.current_session_file = self.sessions_dir / filename

        # Initialize the session file
        header = f"""# DEIA Real-Time Session Log

**Started:** {timestamp.isoformat()}
**Status:** Active (real-time logging)

---

## Session Steps

"""
        self.current_session_file.write_text(header, encoding='utf-8')

    # Append this step
    files_text = ", ".join(f"`{f}`" for f in files_modified) if files_modified else "None"

    step_content = f"""### [{timestamp.strftime('%H:%M:%S')}] {action}

"""
    if files_modified:
        step_content += f"**Files:** {files_text}\n\n"
    if decision:
        step_content += f"**Decision:** {decision}\n\n"
    if next_step:
        step_content += f"**Next:** {next_step}\n\n"

    step_content += "---\n\n"

    # Append to session file
    with open(self.current_session_file, 'a', encoding='utf-8') as f:
        f.write(step_content)

    # Also update project_resume in real-time
    self._update_resume_with_step(action, files_modified, decision)


def _update_resume_with_step(self, action: str, files_modified: Optional[list[str]],
                              decision: Optional[str]):
    """Update project_resume.md with the latest step"""
    resume_file = self.project_root / "project_resume.md"
    timestamp = datetime.now()

    # Create if doesn't exist
    if not resume_file.exists():
        template = f"""# DEIA Project Resume

**Quick Start for Claude Code:** This file tracks the most recent work in real-time.

**Last Updated:** {timestamp.isoformat()}

---

## Current Session (Real-Time)

"""
        resume_file.write_text(template, encoding='utf-8')

    # Read current content
    content = resume_file.read_text(encoding='utf-8')

    # Update timestamp
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('**Last Updated:**'):
            lines[i] = f'**Last Updated:** {timestamp.isoformat()}'
            break

    # Find where to insert (after "## Current Session" header)
    current_session_idx = None
    for i, line in enumerate(lines):
        if '## Current Session' in line:
            current_session_idx = i + 1
            break

    if current_session_idx is not None:
        # Build step summary
        step_line = f"- **[{timestamp.strftime('%H:%M')}]** {action}"
        if decision:
            step_line += f" → *{decision}*"
        if files_modified:
            step_line += f" ({', '.join(f'`{f}`' for f in files_modified)})"

        # Insert after the header (but skip blank line if present)
        insert_idx = current_session_idx
        if insert_idx < len(lines) and lines[insert_idx].strip() == '':
            insert_idx += 1

        lines.insert(insert_idx, step_line)

    # Write back
    resume_file.write_text('\n'.join(lines), encoding='utf-8')
