import json
import time
import click
from rich import print as rprint
from asciimatics.screen import Screen

from deia.services.agent_status import AgentStatusTracker

# Import the main CLI group
# If deia.cli doesn't exist yet, this will need to be created as:
# from deia.cli import cli
# Or create it here:
try:
    from deia.cli import cli
except ImportError:
    # If main CLI doesn't exist yet, create a standalone CLI
    cli = click.Group()

tracker = AgentStatusTracker()

@cli.group('hive')
def hive():
    """Manage DEIA agent coordination"""
    pass

@hive.command('status')
@click.argument('agent_id', required=False)
@click.option('--format', 'output_format', type=click.Choice(['text', 'json']), default='text')
def status(agent_id, output_format):
    """Show agent status"""
    if agent_id:
        agent_status = tracker.get_agent_status(agent_id)
        if output_format == 'json':
            rprint(json.dumps(agent_status, indent=2))
        else:
            rprint(f"Agent: {agent_id}")
            rprint(f"Status: [bold]{agent_status['status']}[/bold]")
            if 'current_task' in agent_status:
                rprint(f"Current Task: {agent_status['current_task']}")
    else:
        if output_format == 'json':
            rprint(json.dumps(tracker.get_all_agents(), indent=2))
        else:
            rprint(tracker.render_dashboard())

@hive.command('agents')
@click.option('--role', type=click.Choice(['coordinator', 'worker', 'queen', 'drone']))
def agents(role):
    """List agents, filter by role"""
    agents = tracker.get_all_agents()
    if role:
        agents = {k: v for k, v in agents.items() if v['role'] == role}

    for agent_id, data in agents.items():
        rprint(f"{agent_id}: [yellow]{data['role']}[/yellow] - [bold]{data['status']}[/bold]")

@hive.command('heartbeat')
@click.argument('agent_id')
@click.option('--status', type=click.Choice(['idle', 'busy', 'waiting', 'paused']))
@click.option('--task', default=None)
def heartbeat(agent_id, status, task):
    """Update heartbeat"""
    tracker.update_heartbeat(agent_id, status, task)
    rprint(f"Heartbeat updated for [bold]{agent_id}[/bold]")

@hive.command('monitor')
@click.option('--interval', default=60, help='Monitoring interval in seconds')
def monitor(interval):
    """Start monitor loop"""
    tracker.start_monitor_loop(interval)
    rprint("[green]Agent monitor started[/green]")
    rprint(f"Checking heartbeats every {interval} seconds")
    rprint("Press Ctrl+C to stop")

@hive.command('dashboard')
def dashboard():
    """Live dashboard (clears screen)"""
    def update_dashboard(screen):
        while True:
            screen.clear()
            screen.print_at(tracker.render_dashboard(), 0, 0)
            screen.refresh()
            tracker.check_heartbeats()
            time.sleep(1)

    Screen.wrapper(update_dashboard)

@hive.command('register')
@click.argument('agent_id')
@click.argument('role', type=click.Choice(['coordinator', 'worker', 'queen', 'drone']))
def register(agent_id, role):
    """Register new agent"""
    tracker.register_agent(agent_id, role)
    rprint(f"[bold]{agent_id}[/bold] registered as [yellow]{role}[/yellow]")
