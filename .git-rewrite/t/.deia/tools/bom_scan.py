#!/usr/bin/env python3
"""Scan repository for UTF-8 BOM and write a report.

Finds files that start with the UTF-8 BOM bytes (EF BB BF) and writes a
timestamped report under .deia/reports/ listing each offending file.

Non-destructive: does NOT modify files.
"""
import os
from pathlib import Path
from datetime import datetime

UTF8_BOM = b"\xef\xbb\xbf"
SKIP_DIRS = {".git", "node_modules", ".deia\\reports", "flappy-bird-ai\\models"}
EXTS = {".md", ".json", ".yml", ".yaml", ".txt", ".toml"}


def should_skip(path: Path) -> bool:
    parts = set(str(path).replace("/", "\\").split("\\"))
    return any(d in parts for d in SKIP_DIRS)


def has_bom(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            head = f.read(3)
        return head == UTF8_BOM
    except Exception:
        return False


def scan(root: Path):
    offenders = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        # prune skip dirs
        dirnames[:] = [d for d in dirnames if not should_skip(rel / d)]
        for fn in filenames:
            p = rel / fn
            if should_skip(p):
                continue
            if Path(fn).suffix.lower() in EXTS:
                full = root / p
                if has_bom(full):
                    offenders.append(p)
    return sorted(offenders)


def main() -> int:
    root = Path.cwd()
    offenders = scan(root)

    reports_dir = root / ".deia" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    report = reports_dir / f"bom-scan-{ts}.md"

    lines = ["# UTF-8 BOM Scan Report\n", f"**When:** {datetime.now().isoformat()}\n", "\n"]
    if offenders:
        lines.append(f"Found {len(offenders)} files with UTF-8 BOM.\n\n")
        for p in offenders:
            lines.append(f"- {p.as_posix()}\n")
    else:
        lines.append("No UTF-8 BOM found in scanned files.\n")

    report.write_text("".join(lines), encoding="utf-8")
    print(f"Report written: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

