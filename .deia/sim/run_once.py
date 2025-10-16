#!/usr/bin/env python3
"""
Dry-run simulation driver: loads scenario + personas, emits a few RSE lines
to .deia/telemetry/rse.jsonl to verify integration. Non-destructive.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import subprocess


def emit_rse(event: dict, sink: Path):
    sink.parent.mkdir(parents=True, exist_ok=True)
    with sink.open('a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print('Usage: run_once.py <scenario.yaml> <personas_dir>')
        return 2
    repo = Path(__file__).resolve().parents[2]
    scen = repo / argv[1]
    personas = repo / argv[2]
    tele = repo / '.deia' / 'telemetry' / 'rse.jsonl'

    # Validate scenario & resolve actors
    val = subprocess.run([sys.executable, str(repo/'.deia/tools/validate_scenario.py'), str(scen)], capture_output=True, text=True)
    emit_rse({"ts":"", "type":"scenario_validated", "lane":"Process", "actor":"Whisperwing", "data":{"ok": val.returncode==0}}, tele)
    load = subprocess.run([sys.executable, str(repo/'.deia/tools/load_scenario.py'), str(scen), str(personas)], capture_output=True, text=True)
    emit_rse({"ts":"", "type":"scenario_loaded", "lane":"Process", "actor":"Whisperwing", "data": json.loads(load.stdout or '{}')}, tele)

    # Example bill pathway skeleton
    events = [
        {"type":"bill_introduced","lane":"Governance","actor":"Sim","data":{"bill_id":"HR-0001","chamber":"House"}},
        {"type":"committee_referral","lane":"Governance","actor":"Sim","data":{"bill_id":"HR-0001","committee":"H-Appropriations"}},
        {"type":"committee_hearing","lane":"Governance","actor":"Sim","data":{"bill_id":"HR-0001","committee":"H-Appropriations"}},
    ]
    for e in events:
        emit_rse({"ts":"", **e}, tele)
    print(json.dumps({"ok": True, "emitted": len(events)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

