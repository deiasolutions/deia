"""Tags Audit - scan markdown for inline tags and summarize usage.

Usage:
  PYTHONPATH=src python -m tools.tags_audit

Outputs:
  docs/tags/TAGS-INDEX.md with counts and file references.
"""
from __future__ import annotations

import re
from pathlib import Path
from collections import Counter, defaultdict

RE_TAG = re.compile(r"(?<![A-Za-z0-9_])#([A-Za-z0-9_\-]+)")


def find_md_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.md") if ".git" not in p.parts and ".obsidian" not in p.parts]


def scan_tags(path: Path) -> set[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return set()
    return set(RE_TAG.findall(text))


def main() -> None:
    root = Path.cwd()
    files = find_md_files(root)
    per_file: dict[Path, set[str]] = {}
    counts = Counter()
    for f in files:
        tags = scan_tags(f)
        if tags:
            per_file[f] = tags
            counts.update(tags)

    out_dir = root / "docs" / "tags"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "TAGS-INDEX.md"

    lines: list[str] = [
        "# EFEMERA Tags Index",
        "",
        "This report summarizes inline tag usage (e.g., #note, #ask, #todo).",
        "",
        "## Tag Counts",
    ]
    for tag, cnt in counts.most_common():
        lines.append(f"- #{tag}: {cnt}")
    lines.append("")
    lines.append("## Files")
    for f, tags in sorted(per_file.items()):
        tag_list = ", ".join(sorted(f"#{t}" for t in tags))
        lines.append(f"- `{f}` — {tag_list}")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

