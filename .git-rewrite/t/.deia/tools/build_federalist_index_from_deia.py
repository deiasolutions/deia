import os, re, json

DEIA_DIR = os.path.join('.deia','federalist')
REPORTS = os.path.join('.deia','reports')

def main():
    files = [f for f in os.listdir(DEIA_DIR) if f.lower().endswith('.md')]
    num_to_file = {}
    interludes = []
    for fn in sorted(files):
        m = re.match(r'^NO-(\d{2})-.*\.md$', fn)
        if m:
            num = int(m.group(1))
            num_to_file[num] = fn
        elif fn.upper().startswith('INTERLUDE') or fn.upper().startswith('PREFACE'):
            interludes.append(fn)

    index = []
    for n in range(1,31):
        if n in num_to_file:
            path = f".deia/federalist/{num_to_file[n]}"
            entry = {"number": n, "status": "Present", "path": path, "title": None}
        else:
            entry = {"number": n, "status": "Missing", "path": None, "title": None}
        index.append(entry)

    for fn in interludes:
        index.append({"number": None, "status": "Interlude", "path": f".deia/federalist/{fn}", "title": os.path.splitext(fn)[0], "notes": "Related"})

    os.makedirs(REPORTS, exist_ok=True)
    with open(os.path.join(REPORTS,'federalist_index.json'),'w', encoding='utf-8') as jf:
        json.dump(index, jf, indent=2, ensure_ascii=False)

    # MD table
    lines = [
        '# Federalist Papers Inventory (.deia canonical)',
        '',
        'Inventory 1..30',
        '',
        '| No. | Status   | Path |',
        '|-----|----------|------|',
    ]
    for e in index:
        if e['number'] is None:
            continue
        path = f"`{e['path']}`" if e['path'] else '-'
        lines.append(f"| {e['number']} | {e['status']:8} | {path} |")
    lines += ['', 'Interludes / Related']
    for e in index:
        if e['number'] is None:
            lines.append(f"- `{e['path']}`")
    with open(os.path.join(REPORTS,'FEDERALIST-INDEX.md'),'w', encoding='utf-8') as mf:
        mf.write('\n'.join(lines) + '\n')

if __name__ == '__main__':
    main()

