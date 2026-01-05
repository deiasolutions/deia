from __future__ import annotations

import os
import shlex

from .cli_adapter import CLIAdapter


def get_cli_adapter(tool: str) -> CLIAdapter:
    tool = tool.lower().strip()
    if tool == "claude-code":
        executable = os.getenv("DEIA_CLAUDE_CMD", "claude")
        args = shlex.split(os.getenv("DEIA_CLAUDE_ARGS", ""))
        return CLIAdapter(executable, args=args, new_console=True)
    if tool == "codex":
        executable = os.getenv("DEIA_CODEX_CMD", "codex")
        args = shlex.split(os.getenv("DEIA_CODEX_ARGS", ""))
        return CLIAdapter(executable, args=args, new_console=True)
    return CLIAdapter(tool, new_console=True)


def get_cli_command(tool: str) -> list[str]:
    tool = tool.lower().strip()
    if tool == "claude-code":
        executable = os.getenv("DEIA_CLAUDE_CMD", "claude")
        args = shlex.split(os.getenv("DEIA_CLAUDE_ARGS", ""))
        return [executable, *args]
    if tool == "codex":
        executable = os.getenv("DEIA_CODEX_CMD", "codex")
        args = shlex.split(os.getenv("DEIA_CODEX_ARGS", ""))
        return [executable, *args]
    return shlex.split(tool)
