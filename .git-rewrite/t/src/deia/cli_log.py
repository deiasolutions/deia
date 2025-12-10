"""
CLI command for conversation logging
"""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from datetime import datetime

from .logger import ConversationLogger

console = Console()


@click.command()
@click.option('--context', help='Brief description of what you worked on')
@click.option('--transcript', help='Path to file containing conversation transcript')
@click.option('--auto', is_flag=True, help='Auto-generate from current session (if available)')
def log(context, transcript, auto):
    """
    Log a Claude Code conversation to .deia/sessions/

    This is your insurance against crashes - never lose context again.
    """

    logger = ConversationLogger()

    if auto:
        console.print("[yellow]Auto-logging feature coming soon - for now use manual logging[/yellow]")
        return

    # Prompt for context if not provided
    if not context:
        context = Prompt.ask("What were you working on?")

    # Get transcript
    transcript_text = ""
    if transcript:
        transcript_path = Path(transcript)
        if transcript_path.exists():
            transcript_text = transcript_path.read_text(encoding='utf-8')
        else:
            console.print(f"[red]Error: Transcript file not found: {transcript}[/red]")
            return
    else:
        console.print("[yellow]Note: No transcript provided. You can add it manually to the log file later.[/yellow]")
        transcript_text = "(Transcript to be added manually)"

    # Prompt for key info
    console.print("\n[cyan]Optional details (press Enter to skip):[/cyan]")

    decisions_input = Prompt.ask("Key decisions made (comma-separated)", default="")
    decisions = [d.strip() for d in decisions_input.split(",")] if decisions_input else []

    action_items_input = Prompt.ask("Action items (comma-separated)", default="")
    action_items = [a.strip() for a in action_items_input.split(",")] if action_items_input else []

    files_input = Prompt.ask("Files modified (comma-separated)", default="")
    files_modified = [f.strip() for f in files_input.split(",")] if files_input else []

    next_steps = Prompt.ask("Next steps", default="Continue from this conversation")

    # Create log
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
        f"[dim]Your conversation is now safe. View the index:[/dim]\n"
        f"[dim]{logger.index_file}[/dim]",
        border_style="green",
        title="Success"
    ))


if __name__ == '__main__':
    log()
