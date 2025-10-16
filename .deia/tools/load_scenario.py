#!/usr/bin/env python3
from __future__ import annotations
import sys, json, yaml
from pathlib import Path


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print('Usage: load_scenario.py <scenario.yaml> <personas_dir>')
        return 2
    scen_path = Path(argv[1])
    personas_dir = Path(argv[2])
    scen = load_yaml(scen_path)
    # Map persona ids to paths
    id_to_path = {}
    for md in personas_dir.rglob('*.md'):
        txt = md.read_text(encoding='utf-8', errors='replace')
        if txt.startswith('---') and '\n---\n' in txt:
            hdr = txt.split('\n', 1)[1].split('\n---\n', 1)[0]
            for line in hdr.splitlines():
                if line.strip().startswith('id:'):
                    pid = line.split(':', 1)[1].strip()
                    id_to_path[pid] = str(md)
                    break
    # Load optional aliases
    aliases_path = personas_dir.parent / 'ALIASES.json'
    aliases = {}
    if aliases_path.exists():
        try:
            aliases = json.loads(aliases_path.read_text(encoding='utf-8'))
        except Exception:
            aliases = {}
    # Resolve actors with aliases
    unresolved = []
    resolved = {}
    for a in scen.get('actors', []) or []:
        canon = aliases.get(a, a)
        if canon in id_to_path:
            resolved[a] = {"canonical": canon, "path": id_to_path[canon]}
        else:
            unresolved.append(a)
    result = {
        'scenario_id': scen.get('id'),
        'actors_total': len(scen.get('actors', []) or []),
        'actors_resolved': len(resolved),
        'unresolved': unresolved,
        'resolved': resolved,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not unresolved else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
