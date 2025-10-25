"""
DEIA Notebook Bootstrap Helpers

Usage (in a Jupyter notebook cell):

  %run .deia/analytics/notebook_bootstrap.py
  configure_deia()            # adds <project_root>/src to sys.path
  show_env()                  # prints interpreter info
  # ensure_packages(['pandas','plotly'])  # optional install into current kernel

This avoids import issues by not requiring `deia` to be importable first.
"""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path
from typing import Iterable, Optional


def find_project_root(start: Path = Path.cwd()) -> Path:
    p = start.resolve()
    for _ in range(10):
        if (p / '.deia').is_dir():
            return p
        if p.parent == p:
            break
        p = p.parent
    return start.resolve()


def configure_deia(src_subdir: str = 'src', verbose: bool = True) -> Path:
    """Add <project_root>/<src_subdir> to sys.path so `import deia` works.

    Returns the path added (or existing).
    """
    root = find_project_root()
    src = (root / src_subdir).resolve()
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
        if verbose:
            print(f"[deia] Added to sys.path: {src}")
    else:
        if verbose:
            print(f"[deia] Already on sys.path: {src}")
    return src


def show_env() -> None:
    """Print interpreter and site information for the current kernel."""
    import site
    print('Python version:', sys.version)
    print('Executable   :', sys.executable)
    try:
        print('User site    :', site.getusersitepackages())
    except Exception as e:
        print('User site    : <unavailable>', e)


def ensure_packages(packages: Iterable[str], upgrade: bool = True) -> None:
    """Install packages into THIS kernel's interpreter using pip.

    Example:
      ensure_packages(['pandas','plotly'])
    """
    args = [sys.executable, '-m', 'pip', 'install']
    if upgrade:
        args.append('-U')
    args.extend(list(packages))
    print('[deia] pip', ' '.join(args[2:]))
    subprocess.check_call(args)


if __name__ == '__main__':
    # Friendly message when run via %run
    added = configure_deia(verbose=True)
    print('[deia] Notebook bootstrap loaded. You can now import deia.* modules.')
