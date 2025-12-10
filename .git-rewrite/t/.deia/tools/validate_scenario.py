#!/usr/bin/env python3
from __future__ import annotations
import sys, json, yaml
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: validate_scenario.py <scenario.yaml>')
        return 2
    p = Path(argv[1])
    data = yaml.safe_load(p.read_text(encoding='utf-8'))
    errors, warnings = [], []
    # Required top-level keys
    for k in ['id', 'title', 'actors', 'tag_teams', 'deadlines', 'budgets']:
        if k not in data:
            errors.append(f'missing:{k}')
    # Actors must be list of IDs
    if isinstance(data.get('actors'), list):
        if not all(isinstance(x, str) for x in data['actors']):
            errors.append('actors_not_string_ids')
    else:
        warnings.append('actors_not_list')
    # tag_teams basic shape
    tts = data.get('tag_teams', []) or []
    for i, tt in enumerate(tts):
        if 'id' not in tt or 'members' not in tt:
            errors.append(f'tag_team_{i}_missing_id_or_members')
    result = {'ok': not errors, 'errors': errors, 'warnings': warnings, 'id': data.get('id'), 'path': str(p)}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

