"""
DEIA CLI - Command-line interface for the DEIA toolkit
"""

import click
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.markdown import Markdown
import sys

from .core import init_project, create_session_log, sanitize_file, validate_file
from .bok import search_bok, sync_bok
from .config import load_config, save_config
from .logger import ConversationLogger
from .installer import install_global, init_project as installer_init_project

console = Console()


@click.group()
@click.version_option()
def main():
    """
    DEIA - Development Evidence & Insights Automation

    Learn from every AI-assisted development session. Build better with AI.
    """
    pass


@main.command()
@click.option('--username', help='Your username (defaults to system username)')
@click.option('--auto-log/--no-auto-log', default=True,
              help='Enable auto-logging by default (default: enabled)')
def install(username, auto_log):
    """Install DEIA globally (run once per user)"""

    console.print(Panel.fit(
        "[bold cyan]Installing DEIA[/bold cyan]\n"
        "Setting up global DEIA infrastructure...",
        border_style="cyan"
    ))

    try:
        success = install_global(username, auto_log)
        if success:
            console.print("\n[bold green]Installation complete![/bold green]")
            console.print("\n[bold]Next:[/bold] Run [cyan]deia init[/cyan] in your project directory")
        else:
            console.print("\n[red]Installation failed.[/red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option('--project-name', help='Project name (defaults to directory name)')
@click.option('--auto-log/--no-auto-log', default=None,
              help='Enable auto-logging for this project (defaults to global setting)')
@click.option('--path',
              type=click.Path(),
              default='.',
              help='Project directory (default: current directory)')
def init(project_name, auto_log, path):
    """Initialize DEIA for a project"""

    console.print(Panel.fit(
        "[bold cyan]Initializing DEIA[/bold cyan]\n"
        "Setting up project-level DEIA...",
        border_style="cyan"
    ))

    target_path = Path(path).resolve()

    # Check if global DEIA exists
    global_deia = Path.home() / ".deia-global"
    if not global_deia.exists():
        console.print("[yellow]⚠ Global DEIA not found.[/yellow]")
        console.print("Run [cyan]deia install[/cyan] first to set up global DEIA.")
        if Confirm.ask("Install global DEIA now?", default=True):
            try:
                install_global()
            except Exception as e:
                console.print(f"[red]Error installing global DEIA:[/red] {e}")
                sys.exit(1)
        else:
            console.print("[dim]Cancelled.[/dim]")
            sys.exit(0)

    # Check if already initialized
    if (target_path / '.deia').exists():
        console.print("[yellow]DEIA is already initialized in this directory.[/yellow]")
        if not Confirm.ask("Reinitialize?"):
            console.print("[dim]Cancelled.[/dim]")
            sys.exit(0)

    # Run initialization
    try:
        success = installer_init_project(target_path, project_name, auto_log)
        if not success:
            console.print("\n[red]Initialization failed.[/red]")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.group()
def log():
    """Manage session logs"""
    pass


@log.command('create')
@click.option('--topic', prompt='Session topic (brief description)',
              help='Brief topic slug (e.g., "https-redirects")')
@click.option('--type',
              type=click.Choice(['feature', 'bug-fix', 'refactor', 'architecture', 'other']),
              default='feature',
              help='Type of session')
def log_create(topic, type):
    """Create a new session log from template"""

    try:
        log_path = create_session_log(topic, type)

        console.print(f"\n[green]✓[/green] Session log created: [cyan]{log_path}[/cyan]")
        console.print("\n[bold]Fill in the template and save when done.[/bold]")

        # Offer to open in editor
        if Confirm.ask("Open in your default editor?", default=True):
            import subprocess
            subprocess.run([get_editor(), str(log_path)])

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@log.command('conversation')
@click.option('--context', help='Brief description of what you worked on')
@click.option('--transcript', type=click.Path(exists=True), help='Path to conversation transcript file')
def log_conversation(context, transcript):
    """
    Log a Claude Code conversation (insurance against crashes)

    This saves your conversation to .deia/sessions/ so you never lose context.
    """

    logger = ConversationLogger()

    # Prompt for context if not provided
    if not context:
        context = Prompt.ask("What were you working on?")

    # Get transcript
    transcript_text = ""
    if transcript:
        transcript_path = Path(transcript)
        transcript_text = transcript_path.read_text(encoding='utf-8')
    else:
        console.print("[yellow]Note: No transcript provided. Paste it in the log file manually.[/yellow]")
        transcript_text = "(Transcript to be added manually - see log file)"

    # Prompt for key info
    console.print("\n[cyan]Optional details (press Enter to skip):[/cyan]")

    decisions_input = Prompt.ask("Key decisions (comma-separated)", default="")
    decisions = [d.strip() for d in decisions_input.split(",")] if decisions_input else []

    action_items_input = Prompt.ask("Action items (comma-separated)", default="")
    action_items = [a.strip() for a in action_items_input.split(",")] if action_items_input else []

    files_input = Prompt.ask("Files modified (comma-separated)", default="")
    files_modified = [f.strip() for f in files_input.split(",")] if files_input else []

    next_steps = Prompt.ask("Next steps", default="Continue from this conversation")

    # Create log
    try:
        log_file = logger.create_session_log(
            context=context,
            transcript=transcript_text,
            decisions=decisions,
            action_items=action_items,
            files_modified=files_modified,
            next_steps=next_steps,
            status="Completed"
        )

        console.print(Panel.fit(
            f"[bold green]✓ Conversation logged successfully[/bold green]\n\n"
            f"[cyan]Location:[/cyan] {log_file}\n"
            f"[cyan]Session ID:[/cyan] {log_file.stem}\n\n"
            f"[dim]Your conversation is safe. View the index:[/dim]\n"
            f"[dim]{logger.index_file}[/dim]",
            border_style="green",
            title="Success"
        ))

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o',
              help='Output file path (default: <input>_SANITIZED.md)')
@click.option('--auto-open/--no-auto-open',
              default=True,
              help='Open sanitized file for manual review')
def sanitize(file_path, output, auto_open):
    """Sanitize a session log for public sharing"""

    console.print(Panel.fit(
        "[bold]Sanitization Process[/bold]\n\n"
        "1. Automated detection (PII, secrets, IP)\n"
        "2. Manual review required\n"
        "3. Validation before submit",
        border_style="yellow"
    ))

    try:
        sanitized_path = sanitize_file(file_path, output)

        console.print(f"\n[green]✓[/green] Automated sanitization complete")
        console.print(f"[cyan]{sanitized_path}[/cyan]")

        console.print("\n[yellow]⚠ MANUAL REVIEW REQUIRED[/yellow]")
        console.print("Automated tools can't catch everything.")
        console.print("Review the sanitized file carefully before sharing.\n")

        if auto_open:
            import subprocess
            subprocess.run([get_editor(), str(sanitized_path)])

        console.print("\n[bold]Next step:[/bold] [cyan]deia validate <file>[/cyan]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.argument('file_path', type=click.Path(exists=True))
def validate(file_path):
    """Validate a sanitized file is ready for submission"""

    console.print("[bold]Validating...[/bold]\n")

    try:
        issues = validate_file(file_path)

        if not issues:
            console.print("[green]✓ All checks passed![/green]")
            console.print("\n[bold]Ready to submit:[/bold] [cyan]deia submit <file>[/cyan]")
        else:
            console.print("[red]✗ Validation failed:[/red]\n")
            for issue in issues:
                console.print(f"  • {issue}")
            console.print("\n[yellow]Fix these issues before submitting.[/yellow]")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--skip-validation', is_flag=True, help='Skip validation (not recommended)')
def submit(file_path, skip_validation):
    """Submit a sanitized session to the DEIA community"""

    if not skip_validation:
        console.print("[dim]Running validation...[/dim]")
        issues = validate_file(file_path)
        if issues:
            console.print("[red]Validation failed. Fix issues first.[/red]")
            console.print("Or use --skip-validation (not recommended)")
            sys.exit(1)

    console.print(Panel.fit(
        "[bold]Submit to DEIA Community[/bold]\n\n"
        "This will:\n"
        "1. Fork the DEIA repository (if needed)\n"
        "2. Create a new branch\n"
        "3. Add your sanitized file\n"
        "4. Create a Pull Request\n\n"
        "[yellow]Make sure you've reviewed the file carefully![/yellow]",
        border_style="green"
    ))

    if not Confirm.ask("\nProceed with submission?"):
        console.print("[dim]Cancelled.[/dim]")
        sys.exit(0)

    try:
        # TODO: Implement GitHub PR creation
        console.print("[yellow]PR creation coming in next version[/yellow]")
        console.print("For now, manually submit a PR to github.com/deiasolutions/deia")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.group()
def bok():
    """Query the Book of Knowledge"""
    pass


@bok.command('search')
@click.argument('query')
@click.option('--platform', help='Filter by platform (claude-code, cursor, etc.)')
@click.option('--category', help='Filter by category (pattern, anti-pattern, etc.)')
def bok_search(query, platform, category):
    """Search the community Book of Knowledge"""

    try:
        results = search_bok(query, platform=platform, category=category)

        if not results:
            console.print(f"[yellow]No results found for:[/yellow] {query}")
            sys.exit(0)

        console.print(f"\n[bold]Found {len(results)} result(s):[/bold]\n")

        for result in results:
            console.print(Panel(
                f"[bold cyan]{result['title']}[/bold cyan]\n\n"
                f"{result['description']}\n\n"
                f"[dim]Platform: {result['platform']} | Category: {result['category']}[/dim]",
                border_style="cyan"
            ))
            console.print()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@bok.command('sync')
def bok_sync():
    """Sync latest community Book of Knowledge"""

    console.print("[bold]Syncing BOK from community...[/bold]")

    try:
        stats = sync_bok()

        console.print(f"\n[green]✓[/green] Sync complete!")
        console.print(f"  • {stats['new']} new entries")
        console.print(f"  • {stats['updated']} updated entries")
        console.print(f"  • {stats['total']} total entries")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option('--repair', is_flag=True, help='Attempt automatic repair of issues')
def doctor(repair):
    """Diagnose and repair DEIA installation"""
    from .doctor import DEIADoctor

    doctor = DEIADoctor()

    if repair:
        doctor.repair()
    else:
        doctor.check_all()

        if doctor.issues:
            console.print("\n[bold]TIP:[/bold] Run [cyan]deia doctor --repair[/cyan] to attempt automatic fixes")


def get_editor():
    """Get system default editor"""
    import os
    return os.environ.get('EDITOR', 'notepad' if sys.platform == 'win32' else 'nano')


if __name__ == '__main__':
    main()
