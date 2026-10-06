#!/usr/bin/env python3
"""Add per-unit question counts to the school-paper index (assets/high/exercises/school/index.json).

    python3 tool/school_units.py            # writes grades.<g>.<subject>.units = {unitId | "general": n}
    python3 tool/school_units.py --check    # exit 1 if the counts are missing or out of date

The Exercise tab shows per-unit counts before a grade + subject is loaded (the bank and school files are read lazily,
see ExamRepo.ensureExercises). The bank index already has "units"; with this the school papers have them too, so the
counts are exact before loading. A school question counts once, under its "unit" (null -> "general"), unless its id is
already in the bank file of the same grade + subject or earlier in the same file (the app skips those).
test/lazy_load_test.dart checks the counts against what the app loads. Only the "units" maps are written; the file
keeps its compact one-line format.
"""
import argparse
import json
import os
import sys
from collections import Counter

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
EX = os.path.join(ROOT, 'assets', 'high', 'exercises')
SCHOOL = os.path.join(EX, 'school')


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def build():
    idx = load(os.path.join(SCHOOL, 'index.json'))
    bank = load(os.path.join(EX, 'index.json'))
    for g, subs in (idx.get('grades') or {}).items():
        for s, e in (subs or {}).items():
            seen = set()
            be = ((bank.get('grades') or {}).get(g) or {}).get(s)
            if be and os.path.exists(os.path.join(EX, be['file'])):
                seen |= {str(q['id']) for q in load(os.path.join(EX, be['file'])).get('questions', [])}
            n = Counter()
            for q in load(os.path.join(SCHOOL, e['file'])).get('questions', []):
                i = str(q['id'])
                if i in seen:
                    continue
                seen.add(i)
                n[q.get('unit') or 'general'] += 1
            e['units'] = {k: n[k] for k in sorted(n)}
    return json.dumps(idx, ensure_ascii=True, separators=(',', ':'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    p = os.path.join(SCHOOL, 'index.json')
    text = build()
    with open(p, encoding='utf-8') as f:
        cur = f.read()
    if a.check:
        if cur != text:
            sys.exit('school index unit counts out of date: run python3 tool/school_units.py')
        print('school index unit counts up to date')
        return
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    print('wrote unit counts into', os.path.relpath(p, ROOT))


if __name__ == '__main__':
    main()
