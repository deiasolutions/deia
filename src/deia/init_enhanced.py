"""
Enhanced DEIA initialization - Like 'git init' but for DEIA

Creates .deia/ workspace in any project with configuration
"""

from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
import shutil

from .config_schema import DEIAConfig, get_end_user_config, get_dave_config
from .logger import ConversationLogger
from .cli_utils import safe_print

console = Console()


def init_deia_workspace(
    project_path: Path = None,
    project_name: str = None,
    github_username: str = None,
    trusted_submitter: bool = False,
    skip_prompts: bool = False
) -> Path:
    """
    Initialize DEIA workspace in a project (like 'git init')

    Args:
        project_path: Path to project (defaults to current directory)
        project_name: Project name (prompts if not provided)
        github_username: GitHub username for submissions
        trusted_submitter: If True, enables CFRL (Commit First, Review Later)
        skip_prompts: If True, uses defaults for all prompts

    Returns:
        Path to created .deia directory
    """

    # Determine project path
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path).resolve()

    console.print(Panel.fit(
        f"[bold cyan]Initializing DEIA in:[/bold cyan]\n{project_path}",
        border_style="cyan"
    ))

    # Check if already initialized
    deia_dir = project_path / '.deia'
    if deia_dir.exists() and not skip_prompts:
        if not Confirm.ask(f"[yellow].deia/ already exists. Reinitialize?[/yellow]"):
            console.print("[dim]Cancelled.[/dim]")
            return deia_dir

    # Get project name
    if project_name is None and not skip_prompts:
        project_name = Prompt.ask(
            "Project name",
            default=project_path.name
        )
    elif project_name is None:
        project_name = project_path.name

    # Get GitHub username
    if github_username is None and not skip_prompts:
        github_username = Prompt.ask(
            "GitHub username (for submissions)",
            default="anonymous"
        )

    # Create directory structure
    console.print("\n[cyan]Creating directories...[/cyan]")

    directories = [
        deia_dir,
        deia_dir / 'sessions',
        deia_dir / 'intake',
        deia_dir / 'patterns_drafts',
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        safe_print(console, f"  ✓ {directory.relative_to(project_path)}/")

    # Copy logger
    console.print("\n[cyan]Installing conversation logger...[/cyan]")
    logger_source = Path(__file__).parent / 'logger.py'
    logger_dest = deia_dir / 'logger.py'
    shutil.copy(logger_source, logger_dest)
    safe_print(console, f"  ✓ logger.py")

    # Create configuration
    console.print("\n[cyan]Creating configuration...[/cyan]")

    if trusted_submitter:
        config = get_dave_config(project_name)
        safe_print(console, "  ✓ Trusted submitter mode (CFRL enabled)")
    else:
        config = get_end_user_config(project_name, github_username)
        safe_print(console, "  ✓ Standard end-user mode (manual review)")

    config_path = deia_dir / 'config.json'
    config.save(config_path)
    safe_print(console, f"  ✓ config.json")

    # Create .claude/START_HERE.md template
    console.print("\n[cyan]Creating Claude Code integration...[/cyan]")
    claude_dir = project_path / '.claude'
    claude_dir.mkdir(exist_ok=True)

    start_here = claude_dir / 'START_HERE.md'
    if not start_here.exists() or Confirm.ask("Overwrite existing START_HERE.md?", default=False):
        create_start_here_template(start_here, project_name)
        safe_print(console, f"  ✓ .claude/START_HERE.md")

    # Update .gitignore
    console.print("\n[cyan]Updating .gitignore...[/cyan]")
    gitignore = project_path / '.gitignore'
    add_to_gitignore(gitignore)
    safe_print(console, f"  ✓ .gitignore")

    # Create initial session index
    console.print("\n[cyan]Initializing session index...[/cyan]")
    logger = ConversationLogger(project_path)
    # Index file created automatically
    safe_print(console, f"  ✓ sessions/INDEX.md")

    # Create README in .deia
    create_deia_readme(deia_dir, project_name, config)

    # Success message
    success_message = (
        f"[bold green]✓ DEIA initialized successfully![/bold green]\n\n"
        f"[cyan]Project:[/cyan] {project_name}\n"
        f"[cyan]Config:[/cyan] .deia/config.json\n"
        f"[cyan]Logs:[/cyan] .deia/sessions/\n\n"
        f"[bold]Next steps:[/bold]\n"
        f"1. Review .claude/START_HERE.md and customize\n"
        f"2. Start logging: [cyan]deia log conversation[/cyan]\n"
        f"3. Extract patterns: [cyan]deia extract[/cyan]"
    )

    try:
        console.print(Panel.fit(success_message, border_style="green", title="Success"))
    except UnicodeEncodeError:
        # Fallback: Replace Unicode and try again
        from .cli_utils import UNICODE_FALLBACKS
        fallback_message = success_message
        for unicode_char, ascii_replacement in UNICODE_FALLBACKS.items():
            fallback_message = fallback_message.replace(unicode_char, ascii_replacement)
        console.print(Panel.fit(fallback_message, border_style="green", title="Success"))

    return deia_dir


def create_start_here_template(path: Path, project_name: str):
    """Create START_HERE.md template for Claude Code"""

    template = f"""# {project_name} - Instructions for Claude Code

**Project:** {project_name}
**DEIA Enabled:** Yes (conversation logging active)

---

## 🔴 REQUIRED: Log Every Session

**At the end of EVERY conversation, log it:**

```python
import sys
sys.path.insert(0, '.deia')
from logger import quick_log

quick_log(
    context='Brief description of what we worked on',
    transcript='[Full conversation or "See Claude Code history"]',
    decisions=['Key decision 1', 'Key decision 2'],
    action_items=['What was completed', 'What is pending'],
    files_modified=['file1.py', 'file2.md']
)
```

**Why:** Insurance against crashes. Logs stored in `.deia/sessions/` (gitignored).

**Recovery:** If crash, read `.deia/sessions/INDEX.md` to find latest session.

---

## Project Context

### What This Project Does
[Fill in: Brief description]

### Tech Stack
[Fill in: Languages, frameworks, tools]

### Key Architecture Decisions
[Fill in: Major architectural decisions]

---

## Coding Standards

### Code Style
[Fill in: Your style preferences]

### Testing Requirements
[Fill in: When/how to test]

### Git Workflow
[Fill in: Branch strategy, commit messages]

---

## Common Commands

### Run Tests
```bash
[Fill in: How to run tests]
```

### Run Development Server
```bash
[Fill in: How to run locally]
```

### Deploy
```bash
[Fill in: Deployment process]
```

---

## Current Work

### In Progress
[Update this section regularly]

### Known Issues
[Track known issues here]

### Next Priorities
[What to work on next]

---

## DEIA Integration

### Extracting Patterns

If you discover something useful:

```
"Claude, extract that pattern to .deia/intake/ for potential DEIA submission"
```

### Submission Process

1. Pattern extracted to `.deia/intake/`
2. You review and sanitize
3. Submit to DEIA (manual or auto, based on config)

**Config:** `.deia/config.json`

---

**Remember: Log EVERY session. Context is precious.**
"""

    path.write_text(template, encoding='utf-8')


def add_to_gitignore(gitignore_path: Path):
    """Add .deia/ to .gitignore if not already there"""

    if not gitignore_path.exists():
        content = ""
    else:
        content = gitignore_path.read_text(encoding='utf-8')

    if '.deia/' not in content:
        # Add DEIA section
        addition = """
# DEIA workspace (conversation logs, private)
.deia/
"""
        with open(gitignore_path, 'a', encoding='utf-8') as f:
            f.write(addition)


def create_deia_readme(deia_dir: Path, project_name: str, config: DEIAConfig):
    """Create README in .deia/ directory"""

    mode = "Trusted Submitter (CFRL)" if config.submission.auto_submit else "End-User (Manual Review)"

    readme = f"""# DEIA Workspace for {project_name}

**Mode:** {mode}
**Auto-submit:** {'Yes' if config.submission.auto_submit else 'No'}
**Auto-anonymize:** {'Yes' if config.submission.auto_anonymize else 'No'}

---

## What's Here

- `sessions/` - Conversation logs (timestamped)
- `intake/` - Patterns ready for DEIA submission
- `patterns_drafts/` - Work-in-progress patterns
- `logger.py` - Conversation logger
- `config.json` - DEIA configuration

---

## Quick Commands

### Log a conversation
```bash
deia log conversation
```

### Extract pattern
```bash
deia extract sessions/20251006-*.md
```

### Submit to DEIA
```bash
deia submit intake/pattern-name.md
```

---

## Configuration

Edit `config.json` to change settings:
- Auto-submission (opt-in)
- Anonymization preferences
- GitHub username

---

**This directory is gitignored. Never committed to version control.**
"""

    readme_path = deia_dir / 'README.md'
    readme_path.write_text(readme, encoding='utf-8')


if __name__ == '__main__':
    # Test initialization
    init_deia_workspace(
        project_path=Path.cwd(),
        project_name='test-project',
        github_username='testuser',
        skip_prompts=True
    )
