#!/usr/bin/env python3
"""Split every notes book into one small JSON file per unit (build step, run before `flutter build`).

    python3 tool/split_notes.py            # writes assets/high/notes/split/<unitId>.json
    python3 tool/split_notes.py --check    # exit 1 if the split files are missing or out of date

Why: opening a unit used to load and parse the whole textbook (150-500 KB of JSON, every unit of the book) on a
1-2 GB phone. With the split files the app reads only the unit that is opened (~40-110 KB), parses it in a
background isolate and keeps the last few units in memory (lib/high/notes/jr/data/repository.dart, NotesRepo.unitBook).

The sources are NOT touched: assets/high/notes/notes/<book>.json stay the single source of truth (other branches edit
them). This script only reads them. The generated files ARE committed (so every build, including CI, ships them) and
marked linguist-generated in .gitattributes. Re-run this script after editing any notes book or unit override, or after
a rebase/merge that touched notes; `flutter test` (test/notes_split_test.dart) fails while they are stale. If a file is
missing the app falls back to the full book file.

Each output file is {"book": <the book's "book" block>, "units": [<one unit>]}, i.e. a one-unit book, so the app parses
it with the same code. A unit_<id>.json override next to the books replaces that unit, exactly like the app does at
runtime. Output is deterministic: UTF-8 JSON, one-space indent, keys in source order (key order is meaningful, e.g.
diagram order), trailing newline; values are copied unchanged (json load -> dump keeps numbers and strings). Same
sources -> byte-identical files, so after a conflicting rebase just re-run the script.
"""
import argparse
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
NOTES = os.path.join(ROOT, 'assets', 'high', 'notes', 'notes')
OUT = os.path.join(ROOT, 'assets', 'high', 'notes', 'split')


def book_files():
    files = []
    for name in ('index.json', 'english_index.json'):
        p = os.path.join(NOTES, name)
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8') as f:
            idx = json.load(f)
        for subjects in (idx.get('grades') or {}).values():
            for b in (subjects or {}).values():
                fn = b.get('file') if isinstance(b, dict) else None
                if fn and fn not in files:
                    files.append(fn)
    return files


def build():
    """{unitId: json text}"""
    out, owner = {}, {}
    for fn in book_files():
        p = os.path.join(NOTES, fn)
        if not os.path.exists(p):
            print(f'  skip {fn}: missing', file=sys.stderr)
            continue
        with open(p, encoding='utf-8') as f:
            raw = json.load(f)
        if not isinstance(raw, dict) or not isinstance(raw.get('units'), list):
            print(f'  skip {fn}: no units', file=sys.stderr)
            continue
        for u in raw['units']:
            if not isinstance(u, dict) or u.get('id') is None:
                continue
            uid = str(u['id'])
            if uid in owner:
                sys.exit(f'unit id {uid} is in both {owner[uid]} and {fn}: split files are named by unit id')
            if not uid.replace('-', '').replace('_', '').isalnum():
                sys.exit(f'unit id {uid!r} in {fn} is not a safe file name')
            owner[uid] = fn
            ov = os.path.join(NOTES, f'unit_{uid}.json')
            if os.path.exists(ov):
                try:
                    with open(ov, encoding='utf-8') as f:
                        u = json.load(f)
                except ValueError:
                    pass  # the app ignores a broken override too
            out[uid] = json.dumps({'book': raw.get('book'), 'units': [u]}, ensure_ascii=False, indent=1) + '\n'
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='only check that the split files are present and current')
    a = ap.parse_args()
    files = build()
    if not files:
        sys.exit('no notes units found')
    have = {f[:-5] for f in os.listdir(OUT) if f.endswith('.json')} if os.path.isdir(OUT) else set()
    if a.check:
        bad = [u for u, t in files.items() if not os.path.exists(os.path.join(OUT, f'{u}.json')) or open(os.path.join(OUT, f'{u}.json'), encoding='utf-8', newline='').read() != t]
        extra = sorted(have - set(files))
        if bad or extra:
            sys.exit(f'split notes out of date ({len(bad)} changed/missing, {len(extra)} stale): run python3 tool/split_notes.py')
        print(f'split notes up to date ({len(files)} units)')
        return
    os.makedirs(OUT, exist_ok=True)
    for u in have - set(files):
        os.remove(os.path.join(OUT, f'{u}.json'))
    for u, t in files.items():
        json.loads(t)  # sanity
        with open(os.path.join(OUT, f'{u}.json'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(t)
    sizes = sorted(len(t.encode('utf-8')) for t in files.values())
    print(f'split {len(files)} units into {os.path.relpath(OUT, ROOT)}: median {sizes[len(sizes) // 2] // 1024} KB, max {sizes[-1] // 1024} KB')


if __name__ == '__main__':
    main()
