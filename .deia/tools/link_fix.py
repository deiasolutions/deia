#!/usr/bin/env python3
"""Suggest fixes for broken local Markdown links (safe mode).

Reads the latest link-check report (or scans the repo) and produces a
suggested-fixes report under .deia/reports/link-fix-<timestamp>.md.

Safe: does NOT modify files. It suggests likely target paths.
"""
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple, Dict
import re


MD_EXTS = {".md"}
SKIP_DIRS = {".git", "node_modules", ".deia/reports", "flappy-bird-ai/models"}


@dataclass
class BrokenLink:
    file: Path
    line_no: int
    target: str


def should_skip(path: Path) -> bool:
    parts = set(str(path).replace("\\", "/").split("/"))
    return any(d in parts for d in SKIP_DIRS)


def iter_markdown_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        dirnames[:] = [d for d in dirnames if not should_skip(rel / d)]
        for fn in filenames:
            p = rel / fn
            if should_skip(p):
                continue
            if Path(fn).suffix.lower() in MD_EXTS:
                yield root / p


def parse_broken_links_from_md(md_path: Path) -> List[BrokenLink]:
    broken: List[BrokenLink] = []
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception:
        return broken

    # Find markdown links: [text](target)
    link_pat = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for i, line in enumerate(text.splitlines(), start=1):
        for m in link_pat.finditer(line):
            target = m.group(1).strip()
            if target.startswith("http") or target.startswith("mailto:"):
                continue
            # resolve relative to file
            target_path = (md_path.parent / target).resolve()
            if not target_path.exists():
                broken.append(BrokenLink(file=md_path, line_no=i, target=target))
    return broken


def index_repo_files(root: Path) -> Dict[str, List[Path]]:
    """Index files by basename for fuzzy suggestions."""
    idx: Dict[str, List[Path]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        dirnames[:] = [d for d in dirnames if not should_skip(rel / d)]
        for fn in filenames:
            p = (root / rel / fn).resolve()
            idx.setdefault(fn.lower(), []).append(p)
    return idx


def suggest_paths(root: Path, target: str, index: Dict[str, List[Path]]) -> List[Path]:
    cand = []
    base = Path(target).name.lower()
    if base in index:
        cand.extend(index[base])
    # Also try without anchors and fragments
    base2 = base.split("#", 1)[0]
    if base2 != base and base2 in index:
        cand.extend([p for p in index[base2] if p not in cand])
    return cand[:5]


def write_report(root: Path, broken: List[BrokenLink], index: Dict[str, List[Path]]) -> Path:
    reports = root / ".deia" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    out = reports / f"link-fix-{ts}.md"

    lines: List[str] = [
        "# Link Fix Suggestions (Safe Mode)\n\n",
        f"**When:** {datetime.now().isoformat()}\n\n",
        "Notes: Suggestions only, no files modified. Apply manually or generate a patch script.\n\n",
    ]

    if not broken:
        lines.append("No broken local links detected.\n")
    else:
        for bl in broken:
            lines.append(f"## {bl.file.as_posix()}:{bl.line_no}\n")
            lines.append(f"Broken: `{bl.target}`\n\n")
            sugs = suggest_paths(root, bl.target, index)
            if sugs:
                lines.append("Likely targets:\n")
                for p in sugs:
                    rel = p.relative_to(root).as_posix()
                    lines.append(f"- `{rel}`\n")
            else:
                lines.append("No suggestions found\n")
            lines.append("\n")

    out.write_text("".join(lines), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true", help="Scan repo markdown (default)")
    args = ap.parse_args()

    root = Path.cwd()
    broken: List[BrokenLink] = []
    for md in iter_markdown_files(root):
        broken.extend(parse_broken_links_from_md(md))

    index = index_repo_files(root)
    report = write_report(root, broken, index)
    print(f"Suggestions written: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

