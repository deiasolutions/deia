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
import stat
import textwrap
import time
import socket
import webbrowser
from typing import Optional

from .core import (
    init_project,
    create_session_log,
    sanitize_file,
    validate_file,
    find_project_root,
)
from .bok import search_bok, sync_bok
from .config import load_config, save_config
from .logger import ConversationLogger
from .installer import install_global, init_project as installer_init_project
from .cli_utils import safe_print
from .minutes import MinutesManager
from .services.telemetry_etl import maybe_autorun_on_launch, autorun as analytics_autorun

console = Console()


@click.group()
@click.version_option()
def main():
    """
    DEIA - Development Evidence & Insights Automation

    Learn from every AI-assisted development session. Build better with AI.
    Planning cadence uses Seasons (macro) and Flights (execution bursts).
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
        safe_print(console, "[yellow]⚠ Global DEIA not found.[/yellow]")
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
def session():
    """Manage session logs"""
    pass


@main.group()
def minutes():
    """Minute-by-minute team log (DEIA Minutes Bot)"""
    pass


@minutes.command('start')
@click.option('--topic', required=True, help='Topic/name for this minutes file')
@click.option('--interval', type=int, default=60, help='Tick interval in seconds (default: 60)')
@click.option('--loop/--no-loop', default=False, help='Run a ticking loop until Ctrl+C')
def minutes_start(topic, interval, loop):
    mgr = MinutesManager()
    path = mgr.start(topic=topic, interval=interval, loop=loop)
    safe_print(console, f"[green]Minutes started[/green]: {path}")
    # Optional analytics autorun on launch (controlled by .deia/analytics/config.json)
    try:
        res = maybe_autorun_on_launch(Path.cwd())
        if res:
            safe_print(console, "[dim]Analytics ETL autorun completed (staging).[/dim]")
    except Exception:
        pass


@minutes.command('write')
@click.argument('text', nargs=-1)
def minutes_write(text):
    mgr = MinutesManager()
    msg = " ".join(text).strip()
    if not msg:
        console.print("[yellow]Nothing to write. Provide text.[/yellow]")
        return
    try:
        mgr.write(msg)
        safe_print(console, f"[green]Minutes updated[/green]: {msg}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@minutes.command('tick')
def minutes_tick():
    mgr = MinutesManager()
    mgr.tick()
    safe_print(console, "[green]Tick recorded[/green]")


@minutes.command('stop')
def minutes_stop():
    mgr = MinutesManager()
    path = mgr.stop()
    safe_print(console, f"[green]Minutes stopped[/green]: {path}")


@minutes.command('report')
def minutes_report():
    mgr = MinutesManager()
    path = mgr.report()
    safe_print(console, f"[green]Report event emitted[/green]; minutes file: {path}")
@main.group()
def analytics():
    """Analytics ETL utilities (staging NDJSON; optional DuckDB views)."""
    pass


@analytics.command("autorun")
def analytics_run_autorun():
    """Ensure analytics setup and run a lightweight ETL into staging."""
    try:
        res = analytics_autorun(Path.cwd())
        count = len(res.get("written", {}))
        safe_print(console, f"[green]Analytics ETL wrote[/green] {count} tables (staging).")
    except Exception as e:
        console.print(f"[red]Analytics ETL failed:[/red] {e}")
@session.command('create')
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

        safe_print(console, f"\n[green]✓[/green] Session log created: [cyan]{log_path}[/cyan]")
        console.print("\n[bold]Fill in the template and save when done.[/bold]")

        # Offer to open in editor
        if Confirm.ask("Open in your default editor?", default=True):
            import subprocess
            subprocess.run([get_editor(), str(log_path)])

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@session.command('log')
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
@click.option('--from-clipboard', is_flag=True, help='Log conversation from clipboard')
@click.option('--from-file', type=click.Path(exists=True), help='Log conversation from file')
def log(from_clipboard, from_file):
    """Log a conversation to DEIA sessions"""
    from .logger import ConversationLogger
    import pyperclip

    # Check if DEIA is initialized
    if not Path('.deia').exists():
        console.print("[red]Error:[/red] DEIA not initialized in this directory")
        console.print("Run [cyan]deia init[/cyan] first")
        sys.exit(1)

    # Get conversation content
    conversation_text = None

    if from_clipboard:
        try:
            conversation_text = pyperclip.paste()
            if not conversation_text or len(conversation_text.strip()) < 10:
                console.print("[red]Error:[/red] Clipboard is empty or too short")
                sys.exit(1)
        except Exception as e:
            console.print(f"[red]Error reading clipboard:[/red] {e}")
            console.print("\n[yellow]Tip:[/yellow] Install pyperclip: pip install pyperclip")
            sys.exit(1)

    elif from_file:
        try:
            with open(from_file, 'r', encoding='utf-8') as f:
                conversation_text = f.read()
        except Exception as e:
            console.print(f"[red]Error reading file:[/red] {e}")
            sys.exit(1)

    else:
        console.print("[red]Error:[/red] Must specify --from-clipboard or --from-file")
        console.print("\nUsage:")
        console.print("  deia log --from-clipboard")
        console.print("  deia log --from-file conversation.txt")
        sys.exit(1)

    # Parse conversation
    console.print("[cyan]Parsing conversation...[/cyan]")
    parsed = _parse_conversation(conversation_text)

    # Show preview and confirm
    console.print(f"\n[bold]Detected:[/bold]")
    console.print(f"  Context: {parsed['context'][:80]}..." if len(parsed['context']) > 80 else f"  Context: {parsed['context']}")
    console.print(f"  Messages: {parsed['message_count']}")
    console.print(f"  Decisions: {len(parsed['decisions'])}")
    console.print(f"  Files: {len(parsed['files_modified'])}")

    if not Confirm.ask("\n[bold]Log this conversation?[/bold]"):
        console.print("Cancelled")
        return

    # Create log
    logger = ConversationLogger()

    try:
        log_file = logger.create_session_log(
            context=parsed['context'],
            transcript=conversation_text,
            decisions=parsed['decisions'],
            action_items=parsed['action_items'],
            files_modified=parsed['files_modified'],
            next_steps=parsed['next_steps'],
            status="Completed"
        )

        console.print(Panel.fit(
            f"[bold green]Conversation logged successfully[/bold green]\n\n"
            f"[cyan]Location:[/cyan] {log_file}\n"
            f"[cyan]Session ID:[/cyan] {log_file.stem}\n\n"
            f"[dim]Your conversation is safe.[/dim]",
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

        safe_print(console, f"\n[green]✓[/green] Automated sanitization complete")
        console.print(f"[cyan]{sanitized_path}[/cyan]")

        safe_print(console, "\n[yellow]⚠ MANUAL REVIEW REQUIRED[/yellow]")
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
            safe_print(console, "[green]✓ All checks passed![/green]")
            console.print("\n[bold]Ready to submit:[/bold] [cyan]deia submit <file>[/cyan]")
        else:
            safe_print(console, "[red]✗ Validation failed:[/red]\n")
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

        safe_print(console, f"\n[green]✓[/green] Sync complete!")
        console.print(f"  • {stats['new']} new entries")
        console.print(f"  • {stats['updated']} updated entries")
        console.print(f"  • {stats['total']} total entries")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.group()
def doctor():
    """Diagnose and repair DEIA installation and documentation"""
    pass


@doctor.command('install')
@click.option('--repair', is_flag=True, help='Attempt automatic repair of issues')
def doctor_install(repair):
    """Diagnose and repair DEIA installation"""
    from .doctor import DEIADoctor

    doctor_instance = DEIADoctor()

    if repair:
        doctor_instance.repair()
    else:
        doctor_instance.check_all()

        if doctor_instance.issues:
            console.print("\n[bold]TIP:[/bold] Run [cyan]deia doctor install --repair[/cyan] to attempt automatic fixes")


@doctor.command('docs')
@click.option('--fix', is_flag=True, help='Apply recommended fixes automatically')
@click.option('--save-report', is_flag=True, default=True, help='Save audit report to docs/audits/')
def doctor_docs(fix, save_report):
    """Audit documentation for accuracy and redundancy"""
    import subprocess
    from pathlib import Path
    from datetime import datetime

    console.print(Panel.fit(
        "[bold cyan]Documentation Audit[/bold cyan]\n"
        "Verifying accuracy and identifying redundancies...",
        border_style="cyan"
    ))

    # Phase 1: Inventory
    console.print("\n[bold]Phase 1: Inventory[/bold]")

    try:
        result = subprocess.run(
            ['find', '.', '-name', '*.md', '-not', '-path', '*/node_modules/*',
             '-not', '-path', '*/.git/*', '-not', '-path', '*/.deia/*'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            md_files = [f for f in result.stdout.strip().split('\n') if f]
            console.print(f"Found {len(md_files)} markdown files")

            # Categorize
            core = [f for f in md_files if '/' not in f[2:] and any(x in f.lower() for x in ['readme', 'quickstart', 'roadmap'])]
            setup = [f for f in md_files if any(x in f.lower() for x in ['setup', 'install', 'integration', 'memory'])]
            reference = [f for f in md_files if '/docs/' in f or '/bok/' in f]

            console.print(f"  • Core: {len(core)} files")
            console.print(f"  • Setup: {len(setup)} files")
            console.print(f"  • Reference: {len(reference)} files")
        else:
            console.print("[yellow]Could not enumerate files (using fallback)[/yellow]")
            md_files = []
    except Exception as e:
        console.print(f"[yellow]Inventory failed: {e}[/yellow]")
        md_files = []

    # Phase 2: Verification
    console.print("\n[bold]Phase 2: Verification[/bold]")

    issues = []

    # Check if CLI commands in docs exist
    console.print("Checking CLI command references...")
    try:
        help_result = subprocess.run(
            ['python', '-c', 'import sys; sys.path.insert(0, "src"); from deia.cli import main; main(["--help"])'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if help_result.returncode == 0:
            available_commands = help_result.stdout
            console.print("  [green]OK[/green] CLI accessible")
        else:
            issues.append({"severity": "medium", "message": "CLI not accessible for verification"})
    except Exception as e:
        issues.append({"severity": "medium", "message": f"Could not verify CLI: {e}"})

    # Check for common issues
    console.print("Checking for common documentation issues...")

    # Check if ROADMAP exists
    if not Path('ROADMAP.md').exists():
        issues.append({"severity": "high", "message": "ROADMAP.md missing - cannot verify feature claims"})

    # Check for backup files
    backup_files = list(Path('.').rglob('*.backup')) + list(Path('.').rglob('*.bak'))
    if backup_files:
        issues.append({"severity": "low", "message": f"Found {len(backup_files)} backup files to clean up: {', '.join(str(f) for f in backup_files[:3])}"})

    # Check for BOK_MOVED.md specifically (from our audit)
    if Path('BOK_MOVED.md').exists():
        issues.append({"severity": "critical", "message": "BOK_MOVED.md exists but BOK is in bok/ directory - file is incorrect"})

    # Phase 3: Redundancy
    console.print("\n[bold]Phase 3: Redundancy Analysis[/bold]")

    quickstart_variants = [f for f in md_files if 'quickstart' in f.lower() or 'quick' in f.lower()]
    if len(quickstart_variants) > 1:
        issues.append({"severity": "medium", "message": f"Multiple quickstart guides: {', '.join(quickstart_variants)}"})
        console.print(f"  [yellow]WARNING[/yellow] Found {len(quickstart_variants)} quickstart-related files")

    setup_variants = [f for f in md_files if 'setup' in f.lower() or 'integration' in f.lower()]
    if len(setup_variants) > 2:
        issues.append({"severity": "low", "message": f"Many setup guides ({len(setup_variants)}) - consider consolidation"})
        console.print(f"  [cyan]INFO[/cyan] Found {len(setup_variants)} setup-related files")

    # Phase 4: Report
    console.print("\n[bold]Phase 4: Summary[/bold]")

    critical = [i for i in issues if i['severity'] == 'critical']
    high = [i for i in issues if i['severity'] == 'high']
    medium = [i for i in issues if i['severity'] == 'medium']
    low = [i for i in issues if i['severity'] == 'low']

    if not issues:
        console.print("[green]PASS - No issues found! Documentation looks good.[/green]")
        grade = "A"
    else:
        console.print(f"\n[bold]Issues Found:[/bold]")

        if critical:
            console.print(f"\n[red]Critical ({len(critical)}):[/red]")
            for issue in critical:
                console.print(f"  • {issue['message']}")

        if high:
            console.print(f"\n[yellow]High Priority ({len(high)}):[/yellow]")
            for issue in high:
                console.print(f"  • {issue['message']}")

        if medium:
            console.print(f"\n[cyan]Medium Priority ({len(medium)}):[/cyan]")
            for issue in medium:
                console.print(f"  • {issue['message']}")

        if low:
            console.print(f"\n[dim]Low Priority ({len(low)}):[/dim]")
            for issue in low:
                console.print(f"  • {issue['message']}")

        # Assign grade
        if critical:
            grade = "D"
        elif high:
            grade = "C"
        elif len(medium) > 3:
            grade = "B-"
        elif medium:
            grade = "B"
        else:
            grade = "A-"

    console.print(f"\n[bold]Overall Grade:[/bold] {grade}")

    # Save report
    if save_report and issues:
        audit_dir = Path('docs/audits')
        audit_dir.mkdir(parents=True, exist_ok=True)

        report_file = audit_dir / f"{datetime.now().strftime('%Y-%m-%d')}-audit.md"

        report_content = f"""# Documentation Audit Report
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Files Audited:** {len(md_files)}
**Grade:** {grade}

## Summary

Issues found: {len(issues)} ({len(critical)} critical, {len(high)} high, {len(medium)} medium, {len(low)} low)

## Critical Issues

"""
        for issue in critical:
            report_content += f"- {issue['message']}\n"

        report_content += "\n## High Priority\n\n"
        for issue in high:
            report_content += f"- {issue['message']}\n"

        report_content += "\n## Medium Priority\n\n"
        for issue in medium:
            report_content += f"- {issue['message']}\n"

        report_content += "\n## Low Priority\n\n"
        for issue in low:
            report_content += f"- {issue['message']}\n"

        report_content += f"\n## Recommendations\n\nFor detailed audit process, see: `bok/patterns/documentation/documentation-audit.md`\n\nFor AI-assisted audit, run: `/doc-audit` in Claude Code\n"

        report_file.write_text(report_content, encoding='utf-8')
        console.print(f"\n[green]Report saved:[/green] {report_file}")

    # Apply fixes if requested
    if fix and issues:
        console.print("\n[bold]Applying fixes...[/bold]")

        for issue in critical + high:
            if 'BOK_MOVED.md' in issue['message']:
                if Confirm.ask("Delete BOK_MOVED.md (factually incorrect)?"):
                    Path('BOK_MOVED.md').unlink()
                    console.print("  [green]OK[/green] Deleted BOK_MOVED.md")

            if 'backup files' in issue['message']:
                if Confirm.ask(f"Delete {len(backup_files)} backup files?"):
                    for f in backup_files:
                        f.unlink()
                    console.print(f"  [green]OK[/green] Deleted {len(backup_files)} backup files")

    console.print("\n[bold]Next Steps:[/bold]")
    console.print("  1. Review the audit report")
    console.print("  2. For detailed guided audit: /doc-audit in Claude Code")
    console.print("  3. See pattern: bok/patterns/documentation/documentation-audit.md")


@main.group()
def admin():
    """Admin tools for BOK quality control (maintainers only)"""
    pass


@admin.command('scan')
@click.argument('file_path', type=click.Path(exists=True))
def admin_scan(file_path):
    """Security scan a file for secrets and malicious code"""
    from .admin import SecurityScanner

    scanner = SecurityScanner()
    result = scanner.scan_file(file_path)

    console.print(f"\n[bold]Security Scan: {file_path}[/bold]\n")

    if result.get('error'):
        console.print(f"[red]Error:[/red] {result['error']}")
        sys.exit(1)

    # Show secrets found
    secrets = result['secrets_found']
    if secrets:
        console.print(f"[red]🔒 Secrets found: {len(secrets)}[/red]")
        for secret in secrets:
            console.print(f"  Line {secret['line']}: {secret['type']} - {secret['match']}")
        console.print()

    # Show malicious patterns
    malicious = result['malicious_patterns']
    if malicious:
        safe_print(console, f"[red]⚠️  Malicious patterns: {len(malicious)}[/red]")
        for pattern in malicious:
            console.print(f"  Line {pattern['line']}: {pattern['type']} - {pattern['context']}")
        console.print()

    # Show risk score and recommendation
    risk_score = result['risk_score']
    recommendation = result['recommendation']

    if risk_score >= 80:
        color = 'red'
    elif risk_score >= 50:
        color = 'yellow'
    else:
        color = 'green'

    console.print(f"[{color}]Risk Score: {risk_score}/100[/{color}]")
    console.print(f"Recommendation: [{color}]{recommendation}[/{color}]")


@admin.command('quality')
@click.argument('file_path', type=click.Path(exists=True))
def admin_quality(file_path):
    """Quality check a file"""
    from .admin import QualityChecker

    checker = QualityChecker()
    result = checker.check_file(file_path)

    console.print(f"\n[bold]Quality Check: {file_path}[/bold]\n")

    if result.get('error'):
        console.print(f"[red]Error:[/red] {result['error']}")
        sys.exit(1)

    issues = result['issues']
    if issues:
        console.print("[yellow]Issues found:[/yellow]")
        for issue in issues:
            console.print(f"  • {issue}")
        console.print()

    quality_score = result['quality_score']
    recommendation = result['recommendation']

    color = 'green' if quality_score >= 70 else 'yellow'
    console.print(f"[{color}]Quality Score: {quality_score}/100[/{color}]")
    console.print(f"Recommendation: [{color}]{recommendation}[/{color}]")


@admin.command('review')
@click.argument('file_path', type=click.Path(exists=True))
def admin_review(file_path):
    """Full review (security + quality)"""
    from .admin import AIReviewer

    reviewer = AIReviewer()
    result = reviewer.review_file(file_path)

    console.print(f"\n[bold]Full Review: {file_path}[/bold]\n")

    console.print(result['summary'])
    console.print()

    risk_score = result['risk_score']
    recommendation = result['recommendation']

    if risk_score >= 80:
        color = 'red'
    elif risk_score >= 50:
        color = 'yellow'
    else:
        color = 'green'

    console.print(f"[{color}]Overall Risk: {risk_score}/100[/{color}]")
    console.print(f"[{color}]Recommendation: {recommendation}[/{color}]")


@admin.command('ban-user')
@click.argument('username')
@click.option('--reason', default='No reason provided', help='Ban reason')
@click.option('--duration', default='permanent', help='Ban duration')
def admin_ban_user(username, reason, duration):
    """Ban a user from BOK submissions"""
    from .admin import UserManager

    manager = UserManager()
    manager.ban_user(username, reason, duration)


@admin.command('unban-user')
@click.argument('username')
def admin_unban_user(username):
    """Unban a user"""
    from .admin import UserManager

    manager = UserManager()
    manager.unban_user(username)


@admin.command('flag-user')
@click.argument('username')
@click.option('--reason', default='No reason provided', help='Flag reason')
def admin_flag_user(username, reason):
    """Flag a user for review"""
    from .admin import UserManager

    manager = UserManager()
    manager.flag_user(username, reason)


@admin.command('list-banned')
def admin_list_banned():
    """List all banned users"""
    from .admin import UserManager

    manager = UserManager()
    banned = manager.list_banned()

    if not banned:
        console.print("No banned users")
        return

    console.print("\n[bold]Banned Users:[/bold]\n")
    for username, data in banned.items():
        console.print(f"[red]{username}[/red]")
        console.print(f"  Reason: {data['reason']}")
        console.print(f"  Duration: {data['duration']}")
        console.print(f"  Banned at: {data['banned_at']}")
        console.print()


@admin.command('list-flagged')
def admin_list_flagged():
    """List all flagged users"""
    from .admin import UserManager

    manager = UserManager()
    flagged = manager.list_flagged()

    if not flagged:
        console.print("No flagged users")
        return

    console.print("\n[bold]Flagged Users:[/bold]\n")
    for username, flags in flagged.items():
        console.print(f"[yellow]{username}[/yellow] ({len(flags)} flag(s))")
        for flag in flags:
            console.print(f"  • {flag['reason']} ({flag['flagged_at']})")
        console.print()


@main.command()
def status():
    """Show current DEIA status and configuration"""
    from datetime import datetime
    import json

    # Check if .deia exists
    deia_dir = Path('.deia')
    if not deia_dir.exists():
        console.print("[yellow]DEIA not initialized in this directory[/yellow]")
        console.print("Run [cyan]deia init[/cyan] to get started")
        return

    # Load config
    config_file = deia_dir / 'config.json'
    if not config_file.exists():
        console.print("[red]Error:[/red] .deia/config.json not found")
        return

    with open(config_file, 'r') as f:
        config = json.load(f)

    # Count sessions
    sessions_dir = deia_dir / 'sessions'
    session_count = len(list(sessions_dir.glob('*.md'))) if sessions_dir.exists() else 0

    # Get last session time
    last_session = "Never"
    if sessions_dir.exists() and session_count > 0:
        sessions = sorted(sessions_dir.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True)
        if sessions:
            last_modified = datetime.fromtimestamp(sessions[0].stat().st_mtime)
            last_session = last_modified.strftime('%Y-%m-%d %H:%M')

    # Display status
    console.print("\n[bold cyan]DEIA Status[/bold cyan]\n")
    console.print(f"[bold]Project:[/bold] {config.get('project', 'unknown')}")
    console.print(f"[bold]User:[/bold] {config.get('user', 'unknown')}")

    auto_log = config.get('auto_log', False)
    auto_log_status = "[green]enabled[/green]" if auto_log else "[yellow]disabled[/yellow]"
    console.print(f"[bold]Auto-log:[/bold] {auto_log_status}")

    console.print(f"[bold]Version:[/bold] {config.get('version', 'unknown')}")
    console.print(f"[bold]Last session:[/bold] {last_session}")
    console.print(f"[bold]Sessions logged:[/bold] {session_count}")
    console.print()


@main.command()
@click.option('--once', is_flag=True, help='Process existing files and exit (one-time scan)')
@click.option('--daemon', is_flag=True, help='Run as background daemon (future)')
@click.option('--config', 'config_path', type=click.Path(), help='Custom routing config file')
def sync(once, daemon, config_path):
    """
    Sync markdown documents from Downloads to projects.

    Watches Downloads folder for .md files with DEIA routing headers
    and routes them to appropriate project folders based on frontmatter.

    Features:
      - Version tracking with gap detection
      - Unsubmitted draft provenance
      - Safe temp staging (copies, not moves)
      - State persistence across runs

    Examples:
      deia sync              # Watch Downloads folder (interactive)
      deia sync --once       # Process existing files and exit
      deia sync --daemon     # Background mode (coming soon)
    """
    from .sync import DownloadsSyncer

    try:
        syncer = DownloadsSyncer(config_path=config_path)

        if once:
            console.print("Scanning Downloads folder...")
            syncer.process_existing_files()
            console.print("[green]Scan complete[/green]")
        elif daemon:
            console.print("[yellow]Daemon mode not yet implemented. Use --once or interactive mode.[/yellow]")
            return
        else:
            console.print("Starting Downloads folder watch...")
            console.print("Press Ctrl+C to stop")
            syncer.run_interactive()
    except KeyboardInterrupt:
        console.print("\n[green]Sync stopped[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]", err=True)
        sys.exit(1)


@main.group()
def config():
    """Manage DEIA configuration"""
    pass


@config.command('list')
def config_list():
    """Show all configuration settings"""
    import json

    config_file = Path('.deia/config.json')
    if not config_file.exists():
        console.print("[yellow]DEIA not initialized in this directory[/yellow]")
        console.print("Run [cyan]deia init[/cyan] to get started")
        return

    with open(config_file, 'r') as f:
        config_data = json.load(f)

    console.print("\n[bold cyan]DEIA Configuration[/bold cyan]\n")
    for key, value in config_data.items():
        console.print(f"[bold]{key}:[/bold] {value}")
    console.print()


@config.command('get')
@click.argument('key')
def config_get(key):
    """Get a specific configuration value"""
    import json

    config_file = Path('.deia/config.json')
    if not config_file.exists():
        console.print("[red]Error:[/red] .deia/config.json not found")
        sys.exit(1)

    with open(config_file, 'r') as f:
        config_data = json.load(f)

    if key in config_data:
        console.print(config_data[key])
    else:
        console.print(f"[red]Error:[/red] Key '{key}' not found in config")
        sys.exit(1)


@config.command('set')
@click.argument('key')
@click.argument('value')
def config_set(key, value):
    """Set a configuration value"""
    import json

    config_file = Path('.deia/config.json')
    if not config_file.exists():
        console.print("[red]Error:[/red] .deia/config.json not found")
        console.print("Run [cyan]deia init[/cyan] first")
        sys.exit(1)

    with open(config_file, 'r') as f:
        config_data = json.load(f)

    # Convert boolean strings
    if value.lower() in ['true', 'false']:
        value = value.lower() == 'true'

    # Convert numeric strings
    elif value.isdigit():
        value = int(value)

    config_data[key] = value

    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)

    safe_print(console, f"[green]✓[/green] Set [bold]{key}[/bold] = {value}")


def _parse_conversation(text: str) -> dict:
    """
    Parse a conversation and extract key information

    Args:
        text: Raw conversation text

    Returns:
        dict with: context, decisions, action_items, files_modified, next_steps, message_count
    """
    import re

    lines = text.split('\n')

    # Count messages (look for User:/Assistant: or Human:/Assistant: patterns)
    message_count = len(re.findall(r'^(User|Human|Assistant|Claude):', text, re.MULTILINE))

    # Extract context from first few lines (summary of what conversation is about)
    context_lines = []
    for line in lines[:20]:  # Look at first 20 lines
        if line.strip() and not line.startswith(('User:', 'Human:', 'Assistant:', 'Claude:', '#', '```')):
            context_lines.append(line.strip())
            if len(' '.join(context_lines)) > 100:
                break

    context = ' '.join(context_lines) if context_lines else "Conversation logged from clipboard"

    # Extract decisions (look for patterns like "decided to", "decision:", "chose to")
    decisions = []
    decision_patterns = [
        r'decided to (.+?)[\.\n]',
        r'decision[:\s]+(.+?)[\.\n]',
        r'chose to (.+?)[\.\n]',
        r'will (.+?)[\.\n]'
    ]
    for pattern in decision_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        decisions.extend(matches[:3])  # Limit to 3 per pattern

    # Extract file references (look for file paths and code file mentions)
    files_modified = []
    file_patterns = [
        r'`([a-zA-Z0-9_/\-\.]+\.(py|js|ts|md|json|yml|yaml|txt))`',
        r'([a-zA-Z0-9_/\-\.]+\.(py|js|ts|md|json|yml|yaml|txt))',
        r'Created:?\s+(.+?\.(py|js|ts|md|json|yml|yaml|txt))',
        r'Modified:?\s+(.+?\.(py|js|ts|md|json|yml|yaml|txt))',
        r'Updated:?\s+(.+?\.(py|js|ts|md|json|yml|yaml|txt))'
    ]
    for pattern in file_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            file_path = match[0] if isinstance(match, tuple) else match
            if file_path not in files_modified and len(file_path) < 100:
                files_modified.append(file_path)

    # Extract action items (look for "TODO", "- [ ]", "next:", "pending:")
    action_items = []
    action_patterns = [
        r'TODO:?\s+(.+?)[\.\n]',
        r'- \[ \] (.+?)[\n]',
        r'pending:?\s+(.+?)[\.\n]',
        r'next:?\s+(.+?)[\.\n]'
    ]
    for pattern in action_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        action_items.extend(matches[:5])  # Limit to 5 per pattern

    # Extract next steps (look at end of conversation)
    next_steps = "Continue from this conversation"
    last_lines = lines[-20:]  # Last 20 lines
    for line in reversed(last_lines):
        if line.strip() and not line.startswith(('```', '#')):
            if any(word in line.lower() for word in ['next', 'todo', 'should', 'will', 'need to']):
                next_steps = line.strip()
                break

    return {
        'context': context[:200],  # Limit context length
        'decisions': list(set(decisions))[:10],  # Unique, max 10
        'action_items': list(set(action_items))[:10],  # Unique, max 10
        'files_modified': list(set(files_modified))[:20],  # Unique, max 20
        'next_steps': next_steps[:200],  # Limit length
        'message_count': message_count
    }


@main.group()
def hive():
    """Manage DEIA agent coordination and multi-bot hive"""
    pass


@hive.command('assign')
@click.option('--from-agent', required=True, help='Source agent (e.g., CLAUDE_CODE)')
@click.option('--to-agent', required=True, help='Target agent (e.g., CLAUDE_AI)')
@click.option('--type', 'msg_type', default='TASK', help='Message type (TASK, QUERY, etc.)')
@click.option('--subject', required=True, help='Task subject (kebab-case)')
@click.option('--content', required=True, type=click.Path(exists=True), help='Task content file')
def hive_assign(from_agent, to_agent, msg_type, subject, content):
    """Assign a task to an agent"""
    from .services.messaging import create_task_file

    with open(content, 'r') as f:
        task_content = f.read()

    try:
        filepath = create_task_file(
            from_agent=from_agent,
            to_agent=to_agent,
            task_type=msg_type,
            subject=subject,
            content=task_content
        )

        console.print(f"[green]✓ Task created:[/green] {filepath}")
        console.print(f"[cyan]From:[/cyan] {from_agent}")
        console.print(f"[cyan]To:[/cyan] {to_agent}")
        console.print(f"[cyan]Type:[/cyan] {msg_type}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@hive.command('queue')
@click.argument('agent_id', required=False)
def hive_queue_cmd(agent_id):
    """Show agent message queue status"""
    from .services.messaging import get_agent_queue_status, VALID_AGENTS

    if agent_id:
        # Show specific agent
        try:
            status = get_agent_queue_status(agent_id)

            console.print(f"\n[bold]{agent_id} Queue Status[/bold]\n")
            console.print(f"[cyan]Queue Size:[/cyan] {status['queue_size']}")
            console.print(f"[cyan]Queue Dir:[/cyan] {status['queue_dir']}")

            if status['pending_files']:
                console.print(f"\n[bold]Pending Tasks:[/bold]")
                for fname in status['pending_files']:
                    console.print(f"  • {fname}")
            else:
                console.print(f"\n[green]No pending tasks[/green]")

        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)
    else:
        # Show all agents
        console.print("\n[bold]Agent Queue Status[/bold]\n")

        for agent in sorted(VALID_AGENTS):
            if agent in ["ALL", "ANY"]:
                continue

            try:
                status = get_agent_queue_status(agent)
                size = status['queue_size']

                if size > 0:
                    console.print(f"🟡 {agent:20} [{size} task(s)]")
                else:
                    console.print(f"🟢 {agent:20} [idle]")

            except Exception:
                console.print(f"⚪ {agent:20} [unknown]")

        console.print()


@hive.command('watch')
@click.option('--interval', default=2, help='Check interval in seconds')
def hive_watch(interval):
    """Watch inbox and route messages"""
    from .services.messaging import MessageRouter

    console.print(f"[bold]Starting message router[/bold]")
    console.print(f"Watching ~/Downloads/uploads every {interval}s")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")

    router = MessageRouter()

    try:
        router.watch_inbox(interval=interval)
    except KeyboardInterrupt:
        console.print("\n[green]Router stopped[/green]")
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {e}")
        sys.exit(1)


@hive.command('status')
@click.argument('agent_id', required=False)
@click.option('--format', 'output_format', type=click.Choice(['text', 'json']), default='text')
def hive_agent_status(agent_id, output_format):
    """Show agent heartbeat status"""
    try:
        from .services.agent_status import AgentStatusTracker
        import json

        tracker = AgentStatusTracker()

        if agent_id:
            agent_status = tracker.get_agent_status(agent_id)
            if output_format == 'json':
                console.print(json.dumps(agent_status, indent=2))
            else:
                console.print(f"Agent: {agent_id}")
                console.print(f"Status: [bold]{agent_status['status']}[/bold]")
                if 'current_task' in agent_status:
                    console.print(f"Current Task: {agent_status['current_task']}")
        else:
            if output_format == 'json':
                console.print(json.dumps(tracker.get_all_agents(), indent=2))
            else:
                console.print(tracker.render_dashboard())
    except ImportError:
        console.print("[yellow]AgentStatusTracker not available yet[/yellow]")
        console.print("This feature requires agent_status.py integration")


@hive.command('agents')
@click.option('--role', type=click.Choice(['coordinator', 'worker', 'queen', 'drone']))
def hive_agents(role):
    """List agents, optionally filtered by role"""
    try:
        from .services.agent_status import AgentStatusTracker

        tracker = AgentStatusTracker()
        agents = tracker.get_all_agents()

        if role:
            agents = {k: v for k, v in agents.items() if v.get('role') == role}

        for agent_id, data in agents.items():
            console.print(f"{agent_id}: [yellow]{data.get('role', 'unknown')}[/yellow] - [bold]{data.get('status', 'unknown')}[/bold]")
    except ImportError:
        console.print("[yellow]AgentStatusTracker not available yet[/yellow]")


@hive.command('heartbeat')
@click.argument('agent_id')
@click.option('--status', type=click.Choice(['idle', 'busy', 'waiting', 'paused', 'offline']))
@click.option('--task', default=None, help='Current task description')
def hive_heartbeat(agent_id, status, task):
    """Update agent heartbeat"""
    try:
        from .services.agent_status import AgentStatusTracker

        tracker = AgentStatusTracker()
        tracker.update_heartbeat(agent_id, status, task)
        console.print(f"[green]Heartbeat updated for[/green] [bold]{agent_id}[/bold]")
    except ImportError:
        console.print("[yellow]AgentStatusTracker not available yet[/yellow]")


@hive.command('monitor')
@click.option('--interval', default=60, help='Monitoring interval in seconds')
def hive_monitor(interval):
    """Start agent heartbeat monitoring loop"""
    try:
        from .services.agent_status import AgentStatusTracker

        tracker = AgentStatusTracker()
        console.print("[green]Agent monitor started[/green]")
        console.print(f"Checking heartbeats every {interval} seconds")
        console.print("Press Ctrl+C to stop")
        tracker.start_monitor_loop(interval)
    except ImportError:
        console.print("[yellow]AgentStatusTracker not available yet[/yellow]")
    except KeyboardInterrupt:
        console.print("\n[green]Monitor stopped[/green]")


@hive.command('dashboard')
def hive_dashboard():
    """Live agent status dashboard (full screen)"""
    try:
        from .services.agent_status import AgentStatusTracker
        from asciimatics.screen import Screen
        import time

        tracker = AgentStatusTracker()

        def update_dashboard(screen):
            while True:
                screen.clear()
                screen.print_at(tracker.render_dashboard(), 0, 0)
                screen.refresh()
                tracker.check_heartbeats()
                time.sleep(1)

        Screen.wrapper(update_dashboard)
    except ImportError as e:
        if 'asciimatics' in str(e):
            console.print("[yellow]asciimatics library not installed[/yellow]")
            console.print("Install with: pip install asciimatics")
        else:
            console.print("[yellow]AgentStatusTracker not available yet[/yellow]")


@hive.command('register')
@click.argument('agent_id')
@click.argument('role', type=click.Choice(['coordinator', 'worker', 'queen', 'drone']))
def hive_register(agent_id, role):
    """Register a new agent in the hive"""
    try:
        from .services.agent_status import AgentStatusTracker

        tracker = AgentStatusTracker()
        tracker.register_agent(agent_id, role)
        console.print(f"[bold]{agent_id}[/bold] registered as [yellow]{role}[/yellow]")
    except ImportError:
        console.print("[yellow]AgentStatusTracker not available yet[/yellow]")


@hive.command('join')
@click.argument('hive_file', type=click.Path(exists=True))
@click.option('--role', help='Specific bot ID to claim (e.g., BOT-00002)')
def hive_join(hive_file, role):
    """
    Join an existing hive as a drone.

    Reads a hive configuration file and claims an available bot identity.
    Auto-assigns a role if not specified.

    Examples:
      deia hive join .deia/hive-recipe.json          # Auto-assign role
      deia hive join hive.json --role BOT-00002      # Claim specific bot
    """
    from .hive import HiveManager, HiveJoinError

    console.print(Panel.fit(
        "[bold cyan]Joining Hive[/bold cyan]\n"
        f"Reading configuration from {hive_file}...",
        border_style="cyan"
    ))

    try:
        manager = HiveManager()
        result = manager.join_hive(hive_file, bot_id=role)

        if result['success']:
            console.print(Panel.fit(
                f"[bold green]Successfully Joined Hive![/bold green]\n\n"
                f"[cyan]Bot ID:[/cyan] {result['bot_id']}\n"
                f"[cyan]Role:[/cyan] {result['role']}\n"
                f"[cyan]Instance ID:[/cyan] {result['instance_id']}\n"
                f"[cyan]Instructions:[/cyan] {result['instruction_file']}\n\n"
                f"[dim]Read your instruction file to see assigned tasks.[/dim]",
                border_style="green",
                title="Hive Join Success"
            ))
        else:
            console.print(f"[red]Failed to join hive[/red]")
            sys.exit(1)

    except HiveJoinError as e:
        console.print(f"[red]Hive Join Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@hive.command('launch')
@click.argument('hive_file', type=click.Path(exists=True))
@click.option('--no-queen', is_flag=True, help='Initialize structure only (don\'t become Queen)')
def hive_launch(hive_file, no_queen):
    """
    Launch a new hive and become the Queen.

    Reads a hive configuration file, creates the directory structure,
    and initializes instruction files for all bots.

    Examples:
      deia hive launch .deia/hive-recipe.json        # Launch and become Queen
      deia hive launch hive.json --no-queen          # Just initialize structure
    """
    from .hive import HiveManager, HiveLaunchError

    console.print(Panel.fit(
        "[bold cyan]Launching Hive[/bold cyan]\n"
        f"Reading configuration from {hive_file}...",
        border_style="cyan"
    ))

    try:
        manager = HiveManager()
        result = manager.launch_hive(hive_file, become_queen=not no_queen)

        if result['success']:
            queen_status = f"[cyan]Queen ID:[/cyan] {result['queen_id']}" if result['queen_id'] else "[yellow]No Queen assigned[/yellow]"

            drones_list = "\n".join(f"  • {drone}" for drone in result['drones_initialized'])

            console.print(Panel.fit(
                f"[bold green]Hive Launched Successfully![/bold green]\n\n"
                f"[cyan]Hive Name:[/cyan] {result['hive_name']}\n"
                f"{queen_status}\n"
                f"[cyan]Drones Initialized:[/cyan]\n{drones_list}\n\n"
                f"[dim]Instruction files created in .deia/instructions/[/dim]",
                border_style="green",
                title="Hive Launch Success"
            ))

            if result['queen_id']:
                console.print("\n[bold]You are the Queen![/bold]")
                console.print("Check [cyan].deia/instructions/BOT-00001-instructions.md[/cyan] for your role")
        else:
            console.print(f"[red]Failed to launch hive[/red]")
            sys.exit(1)

    except HiveLaunchError as e:
        console.print(f"[red]Hive Launch Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option('--port', default=8000, type=int, help='Port for chat server (default: 8000)')
@click.option('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
@click.option('--no-browser', is_flag=True, help='Do not open browser automatically')
def chat(port, host, no_browser):
    """Start the chat interface with bot selector on specified port"""
    # Check if port is available
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()

    if result == 0:
        console.print(f"[red]Error: Port {port} already in use[/red]")
        sys.exit(1)

    console.print(f"[cyan]Starting chat interface on {host}:{port}...[/cyan]")

    # Open browser if requested
    if not no_browser:
        time.sleep(0.5)
        try:
            webbrowser.open(f'http://{host}:{port}')
            console.print(f"[cyan]Browser opened at http://{host}:{port}[/cyan]")
        except Exception as e:
            console.print(f"[yellow]Could not open browser: {e}[/yellow]")

    # Run chat server
    try:
        from deia.services.chat_interface_app import app
        import uvicorn
        uvicorn.run(app, host=host, port=port, log_level='info')
    except KeyboardInterrupt:
        console.print("\n[yellow]Chat server stopped[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@main.command(name='/')
@click.argument('command', nargs=-1, required=False)
@click.option('--bot', help='Target specific bot by ID (e.g., BOT-00002)')
@click.option('--broadcast', is_flag=True, help='Send to all active bots')
@click.option('--wait', is_flag=True, help='Wait for bot response')
@click.option('--timeout', default=30, help='Response timeout in seconds (default: 30)')
def slash_command(command, bot, broadcast, wait, timeout):
    """
    Execute slash commands or send messages to bots.

    Send commands to specific bots via their instruction files, or broadcast
    to all active bots in the hive.

    Examples:
      deia / --bot BOT-00002 "check status"     # Send to specific bot
      deia / --broadcast "heartbeat check"      # Broadcast to all bots
      deia / --bot BOT-00003 --wait "report"    # Send and wait for response
    """
    from .slash_command import SlashCommandHandler

    # Join command parts into string
    command_text = ' '.join(command) if command else ''

    if not command_text and not bot and not broadcast:
        console.print("[yellow]Error:[/yellow] No command provided")
        console.print("\nUsage:")
        console.print("  deia / --bot BOT-00002 \"your message\"")
        console.print("  deia / --broadcast \"your message\"")
        sys.exit(1)

    try:
        handler = SlashCommandHandler()

        if bot:
            # Send to specific bot
            result = handler.send_to_bot(bot, command_text, wait=wait, timeout=timeout)

            if result['success']:
                console.print(f"[green]Command sent to {bot}[/green]")
                if wait and 'response' in result:
                    if result['response']:
                        console.print(f"[cyan]Response:[/cyan] {result['response']}")
                    else:
                        console.print(f"[yellow]No response received within {timeout}s[/yellow]")
            else:
                console.print(f"[red]Error:[/red] {result.get('error', 'Unknown error')}")
                sys.exit(1)

        elif broadcast:
            # Broadcast to all bots
            result = handler.broadcast_to_all(command_text)

            if result['success']:
                console.print(f"[green]Broadcasted to {result['bot_count']} bot(s)[/green]")
                for bot_id in result['bots']:
                    console.print(f"  {bot_id}")
            else:
                console.print(f"[red]Error:[/red] {result.get('error', 'Unknown error')}")
                sys.exit(1)

        else:
            console.print("[yellow]Must specify --bot or --broadcast[/yellow]")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command("cleanup-temp-staging")
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Optional path to .deia/config.json (defaults to project config).",
)
def cleanup_temp_staging_cmd(config: Optional[Path]):
    """Manually clean the temp staging folder used by the sync service."""
    from .tools.temp_staging_cleanup import cleanup_temp_staging

    config_path = config if config else None
    result = cleanup_temp_staging(config_path=config_path, source="cli")

    if result["success"]:
        console.print(f"[green]{result['message']}[/green]")
        console.print(
            f"deleted={result['deleted_files']} archived={result['archived_files']}"
        )
    else:
        console.print(f"[red]{result['message']}[/red]")
        sys.exit(1)


@main.command("install-cleanup-hook")
@click.option("--force", is_flag=True, help="Overwrite an existing post-commit hook.")
def install_cleanup_hook(force: bool):
    """Install git post-commit hook to purge temp staging after commits."""
    project_root = find_project_root()
    git_dir = project_root / ".git"
    if not git_dir.exists():
        console.print("[red]No .git directory found. Run inside a git repository.[/red]")
        sys.exit(1)

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = hooks_dir / "post-commit"

    if hook_path.exists() and not force:
        console.print(
            "[yellow]A post-commit hook already exists. Use --force to replace it.[/yellow]"
        )
        sys.exit(1)

    if hook_path.exists() and force:
        backup_path = hook_path.with_suffix(".pre-deia")
        hook_path.replace(backup_path)
        console.print(f"[yellow]Existing hook backed up to {backup_path.name}[/yellow]")

    script_contents = _render_cleanup_hook_script(project_root)
    hook_path.write_text(script_contents, encoding="utf-8", newline="\n")
    _make_hook_executable(hook_path)

    console.print(
        "[green]Installed post-commit hook for temp staging cleanup.[/green]\n"
        "Hook runs `deia.tools.temp_staging_cleanup` after every successful commit."
    )


def _render_cleanup_hook_script(project_root: Path) -> str:
    python_path = Path(sys.executable).resolve().as_posix().replace('"', '\\"')
    root_path = project_root.resolve().as_posix().replace('"', '\\"')
    return textwrap.dedent(
        f"""\
        #!/bin/sh
        PYTHON_BIN="{python_path}"
        PROJECT_ROOT="{root_path}"

        if [ ! -d "$PROJECT_ROOT" ]; then
          exit 0
        fi

        cd "$PROJECT_ROOT" || exit 0
        "$PYTHON_BIN" -m deia.tools.temp_staging_cleanup --source post-commit >/dev/null 2>&1 || true
        """
    )


def _make_hook_executable(hook_path: Path) -> None:
    current_mode = hook_path.stat().st_mode
    hook_path.chmod(current_mode | stat.S_IEXEC)


@main.group()
def librarian():
    """Master Librarian - Query and manage the Global Commons index"""
    pass


@librarian.command('query')
@click.argument('query', nargs=-1, required=True)
@click.option('--urgency', type=click.Choice(['critical', 'high', 'medium', 'low']),
              help='Filter by urgency level')
@click.option('--platform', help='Filter by platform (e.g., netlify, windows)')
@click.option('--audience', type=click.Choice(['beginner', 'intermediate', 'advanced']),
              help='Filter by audience level')
@click.option('--no-fuzzy', is_flag=True,
              help='Disable fuzzy matching (enabled by default)')
@click.option('--limit', type=int, default=5,
              help='Number of results to show (default: 5)')
def librarian_query(query, urgency, platform, audience, no_fuzzy, limit):
    """
    Query the Global Commons index with advanced search

    Supports fuzzy matching, AND/OR logic, and multiple filters.

    Examples:
      deia librarian query "deployment failed"
      deia librarian query "DNS not working" --urgency critical
      deia librarian query "python encoding" --platform windows
      deia librarian query "coordination" AND "governance"
      deia librarian query "deployment" OR "release"
    """
    import subprocess

    # Build command for query.py
    cmd = [sys.executable, str(Path(__file__).parent / 'tools' / 'query.py')]
    cmd.extend(query)

    if urgency:
        cmd.extend(['--urgency', urgency])
    if platform:
        cmd.extend(['--platform', platform])
    if audience:
        cmd.extend(['--audience', audience])
    if no_fuzzy:
        cmd.append('--no-fuzzy')
    cmd.extend(['--limit', str(limit)])

    try:
        result = subprocess.run(cmd, check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Query failed:[/red] {e}")
        sys.exit(1)
    except FileNotFoundError:
        console.print("[red]Error:[/red] Query tool not found")
        console.print("Expected location: src/deia/tools/query.py")
        sys.exit(1)


def get_editor():
    """Get system default editor"""
    import os
    return os.environ.get('EDITOR', 'notepad' if sys.platform == 'win32' else 'nano')


if __name__ == '__main__':
    main()
