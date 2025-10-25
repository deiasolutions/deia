import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone


FEDERALIST_DIR = os.path.join('bok', 'federalist')
REPORTS_DIR = os.path.join('.deia', 'reports')


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def slugify(text: str) -> str:
    text = text.strip().lower()
    # replace non-alphanumeric with underscores
    text = re.sub(r"[^a-z0-9]+", "_", text)
    # collapse repeats
    text = re.sub(r"_+", "_", text)
    return text.strip('_')


def find_h1_title(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip().strip('*').strip()
    return None


def parse_number_from_filename(name: str) -> int | None:
    m = re.search(r"federalist\s*_?no\s*[_\-\s]?(\d{1,2})", name, re.I)
    if m:
        return int(m.group(1))
    m2 = re.search(r"federalist\s*no\s*(\d{1,2})", name, re.I)
    if m2:
        return int(m2.group(1))
    return None


def parse_number_from_h1(title: str) -> int | None:
    m = re.search(r"Federalist\s+No\.\s*(\d{1,2})", title, re.I)
    if m:
        return int(m.group(1))
    return None


def ensure_front_matter(content: str, number: int | None, title_text: str) -> str:
    iso = datetime.now(timezone.utc).isoformat()
    # Build title
    if number is not None:
        full_title = f"Federalist No. {number} — {title_text}"
    else:
        full_title = title_text

    if content.startswith('---'):
        # Update minimal fields if missing: integrated_by, integrated_at, title (only if absent)
        parts = content.split('\n')
        # find end of yaml
        end_idx = None
        for i in range(1, min(len(parts), 200)):
            if parts[i].strip() == '---':
                end_idx = i
                break
        if end_idx is None:
            # malformed, prepend a clean block
            meta = [
                '---',
                f'title: "{full_title}"',
                'tags: [#DEIA, #Federalist, #Commons, #PUBLIUS]',
                'source: downloads',
                'integrated_by: BOT-00002',
                f'integrated_at: {iso}',
                '---',
            ]
            return '\n'.join(meta) + '\n' + content
        # ensure keys
        have_title = any(l.lower().startswith('title:') for l in parts[1:end_idx])
        have_integrated_by = any(l.lower().startswith('integrated_by:') for l in parts[1:end_idx])
        have_integrated_at = any(l.lower().startswith('integrated_at:') for l in parts[1:end_idx])
        insert_lines = []
        if not have_title:
            insert_lines.append(f'title: "{full_title}"')
        if not have_integrated_by:
            insert_lines.append('integrated_by: BOT-00002')
        if not have_integrated_at:
            insert_lines.append(f'integrated_at: {iso}')
        if insert_lines:
            new_header = ['---'] + parts[1:end_idx] + insert_lines + ['---']
            rest = parts[end_idx+1:]
            return '\n'.join(new_header + rest)
        return content
    else:
        meta = [
            '---',
            f'title: "{full_title}"',
            'tags: [#DEIA, #Federalist, #Commons, #PUBLIUS]',
            'source: downloads',
            'integrated_by: BOT-00002',
            f'integrated_at: {iso}',
            '---',
        ]
        return '\n'.join(meta) + '\n' + content


def normalize_newlines(text: str) -> str:
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text


def scan_downloads(root: str):
    candidates = []
    for dirpath, dirnames, filenames in os.walk(root):
        # skip obvious noise
        if any(part.lower() in {'node_modules', '.git'} for part in dirpath.split(os.sep)):
            continue
        for fn in filenames:
            if fn.lower().endswith('.md') and ('federalist' in fn.lower() or 'interlude' in fn.lower()):
                full = os.path.join(dirpath, fn)
                try:
                    size = os.path.getsize(full)
                    mtime = os.path.getmtime(full)
                except OSError:
                    continue
                candidates.append({'path': full, 'name': fn, 'size': size, 'mtime': mtime})
    return candidates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--downloads', default=os.path.join(os.path.expanduser('~'), 'Downloads'))
    ap.add_argument('--dest', default=FEDERALIST_DIR)
    ap.add_argument('--reports', default=REPORTS_DIR)
    args = ap.parse_args()

    os.makedirs(args.dest, exist_ok=True)
    os.makedirs(args.reports, exist_ok=True)

    candidates = scan_downloads(args.downloads)

    # read and classify
    entries = []
    for c in candidates:
        path = c['path']
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore', newline='') as f:
                raw = f.read()
        except Exception:
            continue
        text = normalize_newlines(raw)
        title = find_h1_title(text) or ''
        num = parse_number_from_filename(c['name'])
        if num is None and title:
            num = parse_number_from_h1(title)
        h = sha256_file(path)
        entries.append({
            'path': path,
            'name': c['name'],
            'size': c['size'],
            'mtime': c['mtime'],
            'sha256': h,
            'number': num,
            'h1': title,
            'text': text,
        })

    # dedupe by hash
    by_hash = {}
    for e in entries:
        if e['sha256'] not in by_hash:
            by_hash[e['sha256']] = []
        by_hash[e['sha256']].append(e)

    # choose canonical per number (latest mtime), ignore dup hashes
    by_number = {}
    for e in entries:
        num = e['number']
        # treat interludes as number None; we'll handle separately
        if num is None and 'interlude' not in e['name'].lower():
            continue
        cur = by_number.get(num)
        if cur is None or e['mtime'] >= cur['mtime']:
            by_number[num] = e

    move_log = []
    present_nums = set()
    # integrate files
    for num, e in by_number.items():
        src_path = e['path']
        title_text = e['h1'] or os.path.splitext(e['name'])[0]
        if num is None:
            # interlude
            dest_name = 'interlude_introductory_preface_to_the_federalist_cycle.md' if 'preface' in e['name'].lower() else f'interlude_{slugify(title_text)}.md'
        else:
            # ensure title after dash if present in H1 like "Federalist No. N — Title"
            tt = title_text
            # strip potential leading marker like "**Federalist No. N — "
            m = re.search(r"—\s*(.+)$", tt)
            if m:
                tt = m.group(1).strip()
            slug = slugify(tt) or f'no_{num:02d}'
            dest_name = f'federalist_no_{num:02d}_{slug}.md'
            present_nums.add(num)

        dest_path = os.path.join(args.dest, dest_name)

        # prepare content: ensure front matter; LF newlines
        content = ensure_front_matter(e['text'], num, (re.search(r"—\s*(.+)$", e['h1']).group(1).strip() if e['h1'] and '—' in e['h1'] else e['h1'] or os.path.splitext(e['name'])[0]))
        content = normalize_newlines(content)

        with open(dest_path, 'w', encoding='utf-8', newline='\n') as out:
            out.write(content)

        move_log.append({
            'number': num,
            'source_path': src_path,
            'dest_path': dest_path.replace('\\', '/'),
            'sha256': e['sha256'],
            'size': e['size'],
        })

    # Build index JSON
    index = []
    titles_lookup = {}
    # attempt to read H1 from integrated files for titles
    for num in range(1, 31):
        entry = {'number': num}
        fname_prefix = f'federalist_no_{num:02d}_'
        matched = None
        for fn in os.listdir(args.dest):
            if fn.startswith(fname_prefix) and fn.endswith('.md'):
                matched = fn
                break
        if matched:
            path_rel = os.path.join(FEDERALIST_DIR, matched).replace('\\', '/')
            # read H1
            try:
                with open(os.path.join(args.dest, matched), 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('# '):
                            titles_lookup[num] = line[2:].strip().strip('*').strip()
                            break
            except Exception:
                pass
            entry.update({'status': 'Present', 'path': path_rel, 'title': titles_lookup.get(num, None)})
        else:
            entry.update({'status': 'Missing', 'path': None, 'title': None})
        index.append(entry)

    # add interludes if any
    for fn in os.listdir(args.dest):
        if fn.startswith('interlude_') and fn.endswith('.md'):
            index.append({'number': None, 'status': 'Interlude', 'path': os.path.join(FEDERALIST_DIR, fn).replace('\\','/'), 'title': os.path.splitext(fn)[0].replace('_',' ').title(), 'notes': 'Related'})

    # write JSON
    json_path = os.path.join(args.reports, 'federalist_index.json')
    with open(json_path, 'w', encoding='utf-8') as jf:
        json.dump(index, jf, indent=2, ensure_ascii=False)

    # write MD
    md_path = os.path.join(args.reports, 'FEDERALIST-INDEX.md')
    lines = [
        '# Federalist Papers Inventory (Repo-wide)',
        '',
        'Inventory 1..30',
        '',
        '| No. | Status   | Path |',
        '|-----|----------|------|',
    ]
    for e in index:
        if e['number'] is None:
            continue
        no = e['number']
        status = e['status']
        path = f"`{e['path']}`" if e['path'] else '-'
        lines.append(f"| {no} | {status:8} | {path} |")
    lines += ['', 'Interludes / Related']
    for e in index:
        if e['number'] is None:
            lines.append(f"- `{e['path']}`")
    with open(md_path, 'w', encoding='utf-8', newline='\n') as mf:
        mf.write('\n'.join(lines) + '\n')

    # integration report
    rpt_path = os.path.join(args.reports, 'FEDERALIST-INTEGRATION-REPORT.md')
    rpt = [
        '# Federalist Integration Report',
        '',
        f'Date: {datetime.now(timezone.utc).isoformat()}',
        '',
        'Actions',
        '- Dedupe by content hash; choose latest modified per number',
        '- Normalize filenames; ensure front matter; write with LF',
        '',
        'Move Log (source → destination)',
    ]
    for m in move_log:
        rpt.append(f"- No. {m['number'] if m['number'] is not None else 'Interlude'}: {m['source_path']} → {m['dest_path']} ({m['sha256'][:12]}..., {m['size']} bytes)")
    with open(rpt_path, 'w', encoding='utf-8', newline='\n') as rf:
        rf.write('\n'.join(rpt) + '\n')

    print('OK')
    print(json_path)
    print(md_path)
    print(rpt_path)


if __name__ == '__main__':
    main()

