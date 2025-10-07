"""
DEIA Installation Module - Sets up global and project-level DEIA infrastructure
"""

from pathlib import Path
from typing import Optional
import json
import sys
import os


class DeiaInstaller:
    """Handles DEIA installation for users"""

    def __init__(self):
        self.home = Path.home()
        self.global_deia = self.home / ".deia-global"

    def install_global(self, username: Optional[str] = None, auto_log: bool = True) -> bool:
        """
        Install global DEIA infrastructure

        Args:
            username: User's name (defaults to system username)
            auto_log: Enable auto-logging by default

        Returns:
            True if successful, False otherwise
        """
        print("Installing DEIA globally...")

        # Get username
        if not username:
            username = os.getenv("USER") or os.getenv("USERNAME") or "user"

        # Create global directory
        self.global_deia.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Created {self.global_deia}")

        # Create global config
        config_file = self.global_deia / "config.json"
        if not config_file.exists():
            config = {
                "version": "1.0",
                "user": username,
                "auto_log_default": auto_log,
                "projects": []
            }
            config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
            print(f"[OK] Created global config: {config_file}")
        else:
            print(f"[SKIP] Global config already exists: {config_file}")

        # Create global preferences
        prefs_file = self.global_deia / "preferences.md"
        if not prefs_file.exists():
            prefs_content = """# Global DEIA Preferences for Claude Code

**Auto-load behavior:**

When Claude Code starts in a DEIA-enabled project, automatically:
1. Read `project_resume.md` if it exists (get context from last session)
2. Check `.deia/config.json` for project-specific settings
3. If `auto_log: true`, start logging this conversation
4. Read `.claude/INSTRUCTIONS.md` for project-specific instructions

**During session:**

5. Log at natural breakpoints:
   - After completing major tasks
   - When user asks "where were we?"
   - When user indicates end of session

**End-of-session behavior:**

6. If auto-log enabled, create session log with:
   - Full conversation transcript (prompts + responses)
   - Key decisions made
   - Action items (completed and pending)
   - Files modified
   - Next steps

7. Update `project_resume.md` with reference to this session

**Privacy:**

- Conversation logs are stored locally only (`.deia/sessions/`)
- No data sent to external servers
- User controls what gets logged
- Can disable auto-log anytime: `deia config set auto_log false`

**This ensures context is never lost, even after crashes.**
"""
            prefs_file.write_text(prefs_content, encoding='utf-8')
            print(f"[OK] Created global preferences: {prefs_file}")
        else:
            print(f"[SKIP] Global preferences already exist: {prefs_file}")

        # Create Claude Code integration instructions
        integration_file = self.global_deia / "CLAUDE_CODE_INTEGRATION.md"
        if not integration_file.exists():
            integration_content = """# How DEIA Integrates with Claude Code

## Project-Level Integration

When you run `deia init` in a project, DEIA creates `.claude/INSTRUCTIONS.md`.

**Claude Code automatically reads this file** and follows the instructions:
- Check `.deia/config.json` for `auto_log` setting
- Read `project_resume.md` on startup
- Log conversations at appropriate breakpoints
- Follow project-specific preferences

## Manual Setup (if needed)

If `.claude/INSTRUCTIONS.md` isn't being read automatically:

1. Start Claude Code in your project
2. Type: "Read .claude/INSTRUCTIONS.md and follow those instructions"
3. Claude will read the file and start following DEIA preferences

## Verification

To verify DEIA is active:
1. Start new Claude Code session in your project
2. Ask: "Is DEIA auto-logging enabled?"
3. Claude should respond with current config status

## Disabling Auto-Log

Per project:
```bash
cd your-project
deia config set auto_log false
```

Globally (for new projects):
```bash
deia config set auto_log_default false --global
```

## Support

If DEIA isn't working as expected, file a bug report:
https://github.com/deiasolutions/deia/issues
"""
            integration_file.write_text(integration_content, encoding='utf-8')
            print(f"[OK] Created integration guide: {integration_file}")
        else:
            print(f"[SKIP] Integration guide already exists: {integration_file}")

        print("\nGlobal DEIA installation complete!")
        print(f"\nGlobal DEIA directory: {self.global_deia}")
        print(f"Config: {config_file}")
        print(f"Preferences: {prefs_file}")
        print(f"\nNext: Run 'deia init' in your project directory to enable DEIA for that project.")

        return True

    def init_project(
        self,
        project_path: Optional[Path] = None,
        project_name: Optional[str] = None,
        auto_log: Optional[bool] = None
    ) -> bool:
        """
        Initialize DEIA for a project

        Args:
            project_path: Path to project (defaults to current directory)
            project_name: Project name (defaults to directory name)
            auto_log: Enable auto-logging (defaults to global setting)

        Returns:
            True if successful, False otherwise
        """
        # Ensure global DEIA exists
        if not self.global_deia.exists():
            print("❌ Global DEIA not installed. Run 'deia install' first.")
            return False

        # Get project path
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path).resolve()

        # Get project name
        if project_name is None:
            project_name = project_path.name

        # Get auto_log setting
        if auto_log is None:
            global_config = json.loads((self.global_deia / "config.json").read_text())
            auto_log = global_config.get("auto_log_default", True)

        print(f"Initializing DEIA for project: {project_name}")
        print(f"   Path: {project_path}")

        # Create .deia directory
        deia_dir = project_path / ".deia"
        deia_dir.mkdir(exist_ok=True)
        print(f"[OK] Created {deia_dir}")

        # Create sessions directory
        sessions_dir = deia_dir / "sessions"
        sessions_dir.mkdir(exist_ok=True)
        print(f"[OK] Created {sessions_dir}")

        # Create project config
        config_file = deia_dir / "config.json"
        username = json.loads((self.global_deia / "config.json").read_text()).get("user", "user")

        config = {
            "mode": "end-user",
            "global_deia_path": str(self.global_deia),
            "project": project_name,
            "user": username,
            "auto_log": auto_log
        }
        config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
        print(f"[OK] Created project config: {config_file}")

        # Create .claude directory
        claude_dir = project_path / ".claude"
        claude_dir.mkdir(exist_ok=True)
        print(f"[OK] Created {claude_dir}")

        # Create .claude/INSTRUCTIONS.md
        instructions_file = claude_dir / "INSTRUCTIONS.md"
        instructions_content = f"""# DEIA Auto-Logging Instructions

**Read this file at the start of every conversation.**

## Check Auto-Log Status

```python
import json
from pathlib import Path

config = Path(".deia/config.json")
if config.exists():
    auto_log = json.loads(config.read_text()).get("auto_log", False)
    if auto_log:
        # Auto-logging is ENABLED for this project
        pass
```

## When Auto-Log is Enabled

Proactively log conversations at these breakpoints:

### 1. Session Start
- Read `project_resume.md` if it exists (recover context from last session)
- Mention to user: "📋 Continuing from last session: [brief context]"

### 2. User Asks "Where Were We?"
- BEFORE responding, check `.deia/sessions/` for recent logs
- Read latest session log to recover context
- Summarize what was happening

### 3. After Major Task Completion
- Feature implementation complete
- Bug fix complete
- Documentation written
- Proactively log without asking

### 4. User Ends Session
- User says "that's it", "done for now", "thanks", "good night"
- Log session before they go

### 5. Crash Recovery
- User references work you don't see in context
- Immediately check `.deia/sessions/` for recent logs
- Read latest log to recover context

## How to Log

Use the ConversationLogger:

```python
import sys
sys.path.insert(0, 'src')
from deia.logger import ConversationLogger

logger = ConversationLogger()
log_file = logger.create_session_log(
    context="Brief description of what we worked on",
    transcript="FULL conversation - include both user prompts AND your responses",
    decisions=["Key decision 1", "Key decision 2"],
    action_items=["[OK] Completed item", "[PENDING] Pending item"],
    files_modified=["path/to/file1.py", "path/to/file2.md"],
    next_steps="What should happen in the next session"
)
print(f"[OK] Logged to: {{log_file}}")
```

## CRITICAL: Full Transcript

The `transcript` field must contain the COMPLETE conversation:
- Every user prompt
- Every response you gave
- Code you wrote
- Explanations you provided

You have this in your context window - use it.

## Silent Operation

- Don't announce "checking auto-log config"
- Don't mention this file unless user asks
- Just log at appropriate times
- Confirm briefly: "[OK] Session logged"

## User Can Disable

If user says "stop auto-logging" or "disable auto-log":
```bash
deia config set auto_log false
```

## This Prevents Data Loss

Crashes happen. Logs persist. This is the user's insurance policy.

---

**Project:** {project_name}
**Auto-log:** {'Enabled' if auto_log else 'Disabled'}
"""
        instructions_file.write_text(instructions_content, encoding='utf-8')
        print(f"[OK] Created Claude Code instructions: {instructions_file}")

        # Create /log slash command
        commands_dir = claude_dir / "commands"
        commands_dir.mkdir(exist_ok=True)
        log_command = commands_dir / "log.md"
        if not log_command.exists():
            log_content = """# Log This Conversation

Save the current conversation as a session log.

## Instructions:

Extract key information from the conversation and call the logger:

```python
import sys
sys.path.insert(0, 'src')
from deia.logger import ConversationLogger

logger = ConversationLogger()
log_file = logger.create_session_log(
    context="What we worked on",
    transcript="Full conversation text from your context",
    decisions=["Key decisions"],
    action_items=["Completed and pending items"],
    files_modified=["files changed"],
    next_steps="What's next"
)
print(f"[OK] Logged to: {log_file}")
```

This uses your API tokens but ensures you never lose context from crashes.
"""
            log_command.write_text(log_content, encoding='utf-8')
            print(f"[OK] Created /log command: {log_command}")

        # Create .claude/preferences/deia.md
        preferences_dir = claude_dir / "preferences"
        preferences_dir.mkdir(exist_ok=True)
        preferences_file = preferences_dir / "deia.md"
        if not preferences_file.exists():
            # Read the template from the DEIA repo
            deia_repo_prefs = Path(__file__).parent.parent.parent / ".claude" / "preferences" / "deia.md"
            if deia_repo_prefs.exists():
                preferences_content = deia_repo_prefs.read_text(encoding='utf-8')
                preferences_file.write_text(preferences_content, encoding='utf-8')
                print(f"[OK] Created Claude preferences: {preferences_file}")
            else:
                # Fallback: create basic preferences
                preferences_content = """# DEIA Auto-Logging System

**DEIA enables conversation logging and knowledge capture.**

## Startup Behavior

**IMPORTANT: Only activate DEIA if `.deia/` directory exists in the project.**

When you start a session, first check if DEIA is present:

1. **Check if `.deia/` directory exists:**
   ```python
   from pathlib import Path
   if not Path('.deia').exists():
       # Not a DEIA project, skip all DEIA behavior
       pass
   ```

2. **If DEIA exists, check installation:**
   ```python
   from deia.logger import ConversationLogger
   ```

3. **Read project resume:**
   - Check if `project_resume.md` exists
   - If yes, read it to understand context from previous sessions
   - If no, this is a fresh project

4. **Check auto-log setting:**
   - Read `.deia/config.json`
   - If `auto_log: true`, enable real-time logging

## Real-Time Logging (when auto_log = true)

**Log after each significant step:**
- File creation/modification
- Key decision made
- Problem solved
- Error fixed
- Task completed

**What to log:**
```python
logger = ConversationLogger()
logger.log_step(
    action="what was done",
    files_modified=["list", "of", "files"],
    decision="key decision if any",
    next_step="what comes next"
)
```

## End of Session

**Always do this before conversation ends:**
1. Create final session log with full context
2. Update `project_resume.md` with current state
3. Note any pending tasks

## Manual Fallback

If auto-logging isn't working:
- User can say "read project_resume.md" to load context
- User can say "log this chat" to manually trigger logging

## Important

**Real-time logging means DURING the session, not just at the end.**

When `auto_log: true`:
- Log after each meaningful action
- Don't wait until the end
- Keep project_resume.md current throughout
"""
                preferences_file.write_text(preferences_content, encoding='utf-8')
                print(f"[OK] Created Claude preferences: {preferences_file}")
        else:
            print(f"[SKIP] Claude preferences already exist: {preferences_file}")

        # Create project_resume.md if it doesn't exist
        resume_file = project_path / "project_resume.md"
        if not resume_file.exists():
            resume_content = f"""# {project_name} - Project Resume

**Quick Start for Claude Code:** Read the latest session log below to see what happened in the last conversation.

**Last Updated:** Not yet

---

## Latest Session Logs

**📋 Read these in reverse chronological order to catch up on recent work.**

(No sessions logged yet. Run `/log` or wait for auto-logging to create first session.)
"""
            resume_file.write_text(resume_content, encoding='utf-8')
            print(f"[OK] Created project resume: {resume_file}")
        else:
            print(f"[SKIP] Project resume already exists: {resume_file}")

        # Register project with global DEIA
        global_config_file = self.global_deia / "config.json"
        global_config = json.loads(global_config_file.read_text())

        # Check if project already registered
        project_exists = any(
            p.get("path") == str(project_path)
            for p in global_config.get("projects", [])
        )

        if not project_exists:
            if "projects" not in global_config:
                global_config["projects"] = []

            global_config["projects"].append({
                "name": project_name,
                "path": str(project_path),
                "auto_log": auto_log,
                "initialized": "2025-10-06"
            })

            global_config_file.write_text(json.dumps(global_config, indent=2), encoding='utf-8')
            print(f"[OK] Registered project with global DEIA")

        print(f"\n{'='*60}")
        print(f"DEIA initialized for {project_name}!")
        print(f"{'='*60}\n")

        print(f"Project structure:")
        print(f"   .deia/config.json - Project config")
        print(f"   .deia/sessions/ - Conversation logs")
        print(f"   .claude/preferences/deia.md - Claude startup instructions")
        print(f"   .claude/commands/log.md - Manual /log command")
        print(f"   project_resume.md - Quick context recovery")
        print(f"\n   Auto-logging: {'ON' if auto_log else 'OFF'}\n")

        print(f"{'='*60}")
        print(f"IMPORTANT: Claude Code Integration Setup")
        print(f"{'='*60}\n")

        print(f"Claude Code doesn't automatically read files on startup.")
        print(f"You need to set up a memory so Claude knows about DEIA.\n")

        print(f"Choose ONE of these options:\n")

        print(f"Option 1 - Project-level (just this project):")
        print(f"   1. In Claude Code, type: # deia")
        print(f"   2. Paste the content from: .claude/preferences/deia.md")
        print(f"   3. Save the memory\n")

        print(f"Option 2 - User-level (all your DEIA projects):")
        print(f"   1. In Claude Code, type: # deia-user")
        print(f"   2. Paste the content from: .claude/preferences/deia.md")
        print(f"   3. Save the memory\n")

        print(f"After setting up memory, Claude will:")
        print(f"   - Auto-detect DEIA in any project with .deia/")
        print(f"   - Read project_resume.md on startup")
        print(f"   - {'Log conversations automatically' if auto_log else 'Wait for manual /log command'}\n")

        print(f"{'='*60}")
        print(f"Quick Test:")
        print(f"{'='*60}\n")

        print(f"1. Set up the memory (above)")
        print(f"2. Start a new Claude Code conversation")
        print(f"3. Claude should mention: 'I see this is a DEIA-enabled project'")
        print(f"\nIf Claude doesn't mention DEIA, run: deia doctor\n")

        return True


def install_global(username: Optional[str] = None, auto_log: bool = True):
    """Install global DEIA infrastructure"""
    installer = DeiaInstaller()
    return installer.install_global(username, auto_log)


def init_project(
    project_path: Optional[Path] = None,
    project_name: Optional[str] = None,
    auto_log: Optional[bool] = None
):
    """Initialize DEIA for a project"""
    installer = DeiaInstaller()
    return installer.init_project(project_path, project_name, auto_log)
