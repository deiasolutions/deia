from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RepoPreflight:
    status: str
    message: str
    repo_root: Optional[Path] = None
    cwd: Optional[Path] = None


def is_repo_root(path: Path) -> bool:
    """Repo root is valid only if it has a .deia directory."""
    return (path / ".deia").exists()


def find_repo_root(start: Path) -> Optional[Path]:
    """Walk upward to find the nearest repo root with .deia."""
    current = start.resolve()
    for parent in [current] + list(current.parents):
        if is_repo_root(parent):
            return parent
    return None


def preflight_repo_root(cwd: Path) -> RepoPreflight:
    """Enforce repo-root discipline for CLI launches."""
    cwd = cwd.resolve()
    if is_repo_root(cwd):
        return RepoPreflight(
            status="ok",
            message="Repo root confirmed",
            repo_root=cwd,
            cwd=cwd,
        )

    repo_root = find_repo_root(cwd)
    if repo_root:
        return RepoPreflight(
            status="prompt",
            message="Not at repo root. Prompt before launch.",
            repo_root=repo_root,
            cwd=cwd,
        )

    return RepoPreflight(
        status="error",
        message="No .deia found. Cannot launch CLI bee.",
        repo_root=None,
        cwd=cwd,
    )
