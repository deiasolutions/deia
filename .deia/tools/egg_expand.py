#!/usr/bin/env python3
from __future__ import annotations
import re
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
import sys


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n", 1)
    if len(parts) < 2 or "\n---\n" not in parts[1]:
        return {}, text
    header_raw, body = parts[1].split("\n---\n", 1)
    header = {}
    for line in header_raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if ":" in s:
            k, v = s.split(":", 1)
            header[k.strip()] = v.strip()
    return header, body


def next_dir_name(base_dir: Path, base_name: str) -> Path:
    candidate = base_dir / base_name
    if not candidate.exists():
        return candidate
    m = re.match(r"^(.*?)(?:_([0-9]+))?$", base_name)
    if not m:
        # Fallback: append _001
        prefix, start = base_name, 1
    else:
        prefix = m.group(1)
        if m.group(2):
            start = int(m.group(2)) + 1
        else:
            start = 1
    # find highest existing
    max_n = 0
    for p in base_dir.iterdir():
        if p.is_dir():
            mm = re.match(rf"^{re.escape(prefix)}_(\d+)$", p.name)
            if mm:
                n = int(mm.group(1))
                if n > max_n:
                    max_n = n
    n = max(max_n + 1, start)
    # width: keep at least 3 digits if any existing had >=3, else 3 by default
    width = 3
    return base_dir / f"{prefix}_{n:0{width}d}"


def emit_rse(event: dict):
    sink = Path('.deia/telemetry/rse.jsonl')
    sink.parent.mkdir(parents=True, exist_ok=True)
    with sink.open('a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: egg_expand.py <egg.md>")
        return 2
    egg_path = Path(argv[1]).resolve()
    if not egg_path.exists():
        print(f"Not found: {egg_path}", file=sys.stderr)
        return 2
    base_dir = egg_path.parent
    base_name = egg_path.stem
    text = egg_path.read_text(encoding='utf-8', errors='replace')
    header, _ = parse_front_matter(text)
    target_dir = next_dir_name(base_dir, base_name)
    target_dir.mkdir(parents=True, exist_ok=False)
    # copy egg to target as egg.md; leave original in place (DND)
    shutil.copy2(str(egg_path), str(target_dir / 'egg.md'))
    # write a README seed
    (target_dir / 'README.md').write_text(
        f"# {header.get('title') or base_name}\n\nEgg expanded at {iso_now()} from {egg_path}\n\n",
        encoding='utf-8'
    )
    # emit RSE
    emit_rse({
        "ts": iso_now(),
        "type": "egg_expanded",
        "lane": "Process",
        "actor": "Whisperwing",
        "data": {"egg": str(egg_path), "dir": str(target_dir)}
    })
    print(str(target_dir))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

