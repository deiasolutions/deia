#!/usr/bin/env python3
"""Fix UTF-8 BOM by rewriting files without BOM (with backups).

Usage:
  python ./.deia/tools/bom_fix.py --report ./.deia/reports/bom-scan-YYYYMMDD-HHMM.md

This reads a BOM scan report and, for each listed file, writes a `.bak` backup
and then rewrites the file without the UTF‑8 BOM. Non-destructive: original
content preserved in `.bak`.
"""
import argparse
from pathlib import Path
from datetime import datetime

UTF8_BOM = b"\xef\xbb\xbf"


def strip_bom(path: Path) -> bool:
    data = path.read_bytes()
    if data.startswith(UTF8_BOM):
        bak = path.with_suffix(path.suffix + ".bak")
        bak.write_bytes(data)
        path.write_bytes(data[len(UTF8_BOM) :])
        return True
    return False


def parse_report(report_path: Path) -> list[Path]:
    offenders = []
    root = Path.cwd()
    for line in report_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        rel = line[2:].strip()
        rel = rel.replace("/", Path.sep)
        p = (root / rel).resolve()
        if p.exists():
            offenders.append(p)
    return offenders


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True, help="Path to bom-scan report")
    args = ap.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        print(f"Report not found: {report_path}")
        return 1

    offenders = parse_report(report_path)
    fixed = []
    skipped = []
    for p in offenders:
        try:
            if strip_bom(p):
                fixed.append(p)
            else:
                skipped.append(p)
        except Exception as e:
            skipped.append(p)
            print(f"ERROR fixing {p}: {e}")

    ts = datetime.now().strftime("%Y%m%d-%H%M")
    out = Path(".deia") / "reports" / f"bom-fix-{ts}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# BOM Fix Report\n\n**When:** {datetime.now().isoformat()}\n\n"]
    lines.append(f"Fixed: {len(fixed)} file(s)\n\n")
    for p in fixed:
        lines.append(f"- {p}\n")
    if skipped:
        lines.append(f"\nSkipped/No BOM: {len(skipped)} file(s)\n\n")
        for p in skipped:
            lines.append(f"- {p}\n")
    out.write_text("".join(lines), encoding="utf-8")
    print(f"Fix report written: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

