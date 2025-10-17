"""RSE to Obsidian Notes - generate an Obsidian-friendly one-pager.

Reads .deia/telemetry/rse.jsonl and writes docs/obsidian/notes/one-pager.md
with grouped swimlane-like sections per lane.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def load_rse(path: Path) -> list[dict]:
    events = []
    if not path.exists():
        return events
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except Exception:
                pass
    return events


def main() -> None:
    root = Path.cwd()
    rse = root / ".deia" / "telemetry" / "rse.jsonl"
    events = load_rse(rse)
    lanes = defaultdict(list)
    for e in events:
        lane = e.get("lane", "Misc")
        ts = e.get("ts", "")
        tshort = ts.replace("T", " ")[:19]
        etype = e.get("type", "event")
        data = e.get("data", {})
        lanes[lane].append((tshort, etype, data))

    out_dir = root / "docs" / "obsidian" / "notes"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "one-pager.md"

    lines = [
        "# Efemera Swimlane One-Pager",
        "",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_",
        "",
        "Use Obsidian Graph to visualize links/tags. This one-pager groups recent events by lane.
",
    ]
    for lane in sorted(lanes.keys()):
        lines.append(f"## {lane}")
        for tshort, etype, data in lanes[lane][-50:]:
            summary = json.dumps(data, ensure_ascii=False)
            lines.append(f"- {tshort} — **{etype}** — {summary}")
        lines.append("")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

