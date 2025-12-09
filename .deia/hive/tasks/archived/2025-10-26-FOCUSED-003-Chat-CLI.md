# FOCUSED TASK - BOT-003: Add deia chat Command
**Priority:** P0 BLOCKING
**Time:** 20 minutes
**Start:** When BOT-001 is done
**Blocker:** Waits for BOT-001 AnthropicService

---

## EXACTLY what to do:

### 1. Add this import to `src/deia/cli.py` (top with other imports):
```python
import webbrowser
import time
import socket
```

### 2. Add this function in `src/deia/cli.py` (BEFORE @main.command(name='/') around line 1548):
```python
@main.command()
@click.option('--port', default=8000, type=int, help='Port for chat server')
@click.option('--host', default='127.0.0.1', help='Host to bind to')
@click.option('--no-browser', is_flag=True, help='Do not open browser')
def chat(port, host, no_browser):
    """Start chat interface"""
    # Check port available
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    if result == 0:
        console.print(f"[red]Error: Port {port} already in use[/red]")
        sys.exit(1)

    console.print(f"[cyan]Starting chat on {host}:{port}[/cyan]")

    # Open browser
    if not no_browser:
        time.sleep(0.5)
        try:
            webbrowser.open(f'http://{host}:{port}')
        except Exception as e:
            console.print(f"[yellow]Could not open browser: {e}[/yellow]")

    # Run chat server
    try:
        from deia.services.chat_interface_app import app
        import uvicorn
        uvicorn.run(app, host=host, port=port, log_level='info')
    except KeyboardInterrupt:
        console.print("\n[yellow]Chat stopped[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
```

### 3. Create `tests/unit/test_chat_command.py`:
```python
import pytest
from click.testing import CliRunner
from deia.cli import chat

def test_chat_command_exists():
    """Test chat command exists"""
    assert callable(chat)

def test_chat_help():
    """Test chat command help"""
    runner = CliRunner()
    result = runner.invoke(chat, ['--help'])
    assert result.exit_code == 0
    assert 'chat' in result.output.lower()

def test_chat_port_option():
    """Test chat command accepts port option"""
    runner = CliRunner()
    # Don't actually run, just test the option exists
    result = runner.invoke(chat, ['--help'])
    assert '--port' in result.output

def test_chat_no_browser_option():
    """Test chat command accepts no-browser option"""
    runner = CliRunner()
    result = runner.invoke(chat, ['--help'])
    assert '--no-browser' in result.output
```

### 4. Run tests:
```bash
pytest tests/unit/test_chat_command.py -v
```

All 4 tests must PASS.

---

## DONE - Report completion:
Create: `.deia/hive/responses/deiasolutions/bot-003-chat-command-done.md`

Write:
- Command added to CLI successfully
- All 4 tests passing
- Ready for BOT-004

---

## NO OTHER WORK. Just this.
