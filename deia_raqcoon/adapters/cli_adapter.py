from __future__ import annotations

import os
import subprocess
import sys
from shutil import which
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .base import AdapterResult


@dataclass
class CLILaunchResult:
    success: bool
    pid: Optional[int]
    error: Optional[str] = None


class CLIAdapter:
    """Launches a CLI tool in a specific repo root."""

    def __init__(
        self,
        executable: str,
        args: Optional[List[str]] = None,
        new_console: bool = True,
    ):
        self.executable = executable
        self.args = args or []
        self.new_console = new_console

    def _resolve_executable(self) -> Optional[str]:
        if not self.executable:
            return None
        if os.path.isabs(self.executable) or os.sep in self.executable:
            return self.executable if Path(self.executable).exists() else None
        return which(self.executable)

    def launch(self, repo_root: Path, env: Optional[dict] = None) -> CLILaunchResult:
        repo_root = repo_root.resolve()
        if not repo_root.exists():
            return CLILaunchResult(False, None, "repo_root does not exist")

        resolved = self._resolve_executable()
        if not resolved:
            return CLILaunchResult(False, None, f"Executable not found: {self.executable}")

        cmd = [resolved] + self.args
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)

        try:
            popen_kwargs = {
                "cwd": str(repo_root),
                "env": merged_env,
            }
            if os.name == "nt" and self.new_console:
                popen_kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
            elif sys.platform != "win32":
                popen_kwargs["start_new_session"] = True
            process = subprocess.Popen(
                cmd,
                **popen_kwargs,
            )
            return CLILaunchResult(True, process.pid, None)
        except FileNotFoundError:
            return CLILaunchResult(False, None, f"Executable not found: {self.executable}")
        except Exception as exc:
            return CLILaunchResult(False, None, str(exc))

    def send(self, payload: dict) -> AdapterResult:
        return AdapterResult(success=False, output="CLI adapter does not send messages directly")
