#!/usr/bin/env python3
from __future__ import annotations
import sys, json, re
from pathlib import Path


def parse_front_matter(text: str):
    if not text.startswith('---'):
        return {}, text
    parts = text.split('\n', 1)
    if len(parts) < 2 or '\n---\n' not in parts[1]:
        return {}, text
    header_raw, body = parts[1].split('\n---\n', 1)
    header = {}
    for line in header_raw.splitlines():
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if ':' in s:
            k, v = s.split(':', 1)
            header[k.strip()] = v.strip()
    return header, body


REQUIRED_KEYS = ['id', 'role', 'llh', 'capacities', 'stances']


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: validate_persona.py <persona.md>')
        return 2
    p = Path(argv[1])
    text = p.read_text(encoding='utf-8', errors='replace')
    header, body = parse_front_matter(text)
    errors, warnings = [], []
    for k in REQUIRED_KEYS:
        if k not in header or not header[k].strip():
            errors.append(f'missing:{k}')
    # Basic id/role checks
    if 'id' in header and not re.fullmatch(r'[a-z0-9-]+', header['id']):
        warnings.append('id_not_kebab_case')
    if 'stances' in header and header['stances'] == '[]':
        warnings.append('empty_stances')
    # Very light citation presence check in body
    if 'http' not in body:
        warnings.append('no_citations_in_body (expected links)')
    result = {'ok': not errors, 'errors': errors, 'warnings': warnings, 'id': header.get('id'), 'role': header.get('role'), 'path': str(p)}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

