# REAL TASK: Add deia chat CLI Command
**From:** Q33N
**To:** BOT-003
**Date:** 2025-10-26 11:30 AM CDT
**Priority:** P0 - BLOCKING
**Status:** Waits for BOT-001 Anthropic service

---

## What to do

Add `deia chat` command to `src/deia/cli.py`

**Add this function (around line 1549, before the slash_command):**

```python
@main.command()
@click.option('--port', default=8000, help='Port to run on (default: 8000)')
@click.option('--host', default='127.0.0.1', help='Host to bind to')
@click.option('--no-browser', is_flag=True, help='Don\'t open browser')
def chat(port, host, no_browser):
    """Launch chat interface with bot selector"""
    import uvicorn
    import webbrowser
    import time

    # Check if port is in use
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    if result == 0:
        console.print(f"[red]Error:[/red] Port {port} already in use")
        sys.exit(1)

    console.print(f"[green]Starting chat server on {host}:{port}...[/green]")

    # Open browser if requested
    if not no_browser:
        time.sleep(1)  # Wait for server to start
        webbrowser.open(f'http://localhost:{port}')
        console.print("[cyan]Browser opened[/cyan]")

    # Run the FastAPI app
    try:
        from deia.services.chat_interface_app import app
        uvicorn.run(app, host=host, port=port, log_level='info')
    except KeyboardInterrupt:
        console.print("\n[yellow]Chat server stopped[/yellow]")
```

**Tests:**
- Verify command launches
- Verify server runs on port
- Verify --no-browser flag works
- 3-4 tests, all pass

**Time:** 20 minutes

**Deliverable:** `.deia/hive/responses/deiasolutions/bot-003-chat-cli-done.md`

Wait for BOT-001 to finish, then do this.
