#!/usr/bin/env python3
from __future__ import annotations
import json, re
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
            header[k.strip()] = v.strip().strip('"')
    return header, body


def extract_actor_id_from_body(body: str):
    m = re.search(r"Actor ID:\s*`([^`]+)`", body)
    return m.group(1) if m else None


def audit_personas(root: Path):
    records = []
    for p in root.rglob('*.md'):
        text = p.read_text(encoding='utf-8', errors='replace')
        header, body = parse_front_matter(text)
        body_actor = extract_actor_id_from_body(body)
        rec = {
            'path': str(p),
            'id': header.get('id'),
            'role': header.get('role'),
            'llh': header.get('llh'),
            'has_front_matter': bool(header),
            'body_actor_id': body_actor,
            'conformance_missing': [k for k in ['id','role','llh','capacities','stances'] if k not in header or not str(header.get(k,'')).strip()],
        }
        records.append(rec)
    # Detect duplicates by normalized name tokens in ID/body
    def key_for(rec):
        rid = rec['id'] or rec['body_actor_id'] or Path(rec['path']).stem
        return re.sub(r'[^a-z0-9]+', '-', rid.lower()).strip('-')
    clusters = {}
    for r in records:
        k = key_for(r)
        clusters.setdefault(k, []).append(r)
    dup_clusters = {k:v for k,v in clusters.items() if len(v) > 1}
    return records, dup_clusters


def main():
    repo = Path(__file__).resolve().parents[2]
    personas_dir = repo / '.deia' / 'personas'
    records, dups = audit_personas(personas_dir)
    out_dir = personas_dir
    # Write validation log
    (out_dir / 'VALIDATION-LOG.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    # Prepare aliases candidates for duplicate clusters (prefer YAML-front-matter id if present)
    aliases = {}
    for k, items in dups.items():
        # pick canonical: first with front matter id, else shortest path
        canon = None
        for it in items:
            if it['id']:
                canon = it['id']
                break
        if not canon:
            canon = min(items, key=lambda x: len(x['path']))['body_actor_id'] or k
        for it in items:
            src = it['id'] or it['body_actor_id'] or k
            if src and src != canon:
                aliases[src] = canon
    if aliases:
        (out_dir / 'ALIASES.candidates.json').write_text(json.dumps(aliases, ensure_ascii=False, indent=2), encoding='utf-8')
    # Write human report
    lines = []
    lines.append('# Persona Audit — Duplicates & Conformance')
    lines.append('')
    lines.append('## Non-conforming (missing keys)')
    for r in records:
        if r['conformance_missing']:
            lines.append(f"- {r['path']}: missing {', '.join(r['conformance_missing'])} (body_actor_id={r['body_actor_id']})")
    lines.append('')
    lines.append('## Duplicate clusters (candidate aliases)')
    if not dups:
        lines.append('- None')
    else:
        for k, items in dups.items():
            lines.append(f"- {k}:")
            for it in items:
                lines.append(f"  - {it['path']} (id={it['id']} body_actor_id={it['body_actor_id']})")
    (out_dir / 'REPORT-duplicates-and-conformance.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'ok': True, 'records': len(records), 'dup_clusters': len(dups)}))


if __name__ == '__main__':
    main()

