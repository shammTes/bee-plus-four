#!/usr/bin/env python3
"""Drive-bank packs (bank_*.json) number Part I questions by their slot in the converted batch, so Part II items
that sit between them leave holes (Q4, Q6, ... "Q5 is missing" in the app). When every Part I number equals the
question's position in the pack, renumber each part 1..n in pack order and list Part I before Part II.
Packs that also lost repeats to dedupe_within.py (so positions moved) are listed in FORCE and renumbered the same way.
Usage: renumber.py [--dry]"""
import json, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'high', 'exams')


FORCE = {'bank_math-matric-2026-part2.json', 'bank_mathematics-model-2017.json', 'bank_mathematics-model-2024.json'}


def main():
    dry = '--dry' in sys.argv
    idx = json.load(open(os.path.join(ROOT, 'index.json')))
    for f in idx['exams']:
        if not f.startswith('bank_'):
            continue
        p = os.path.join(ROOT, f)
        raw = open(p, encoding='utf-8').read()
        d = json.loads(raw)
        qs = d.get('questions', [])
        p1 = [(i, q) for i, q in enumerate(qs) if q.get('part', 1) == 1]
        if not qs or (f not in FORCE and (len(p1) == len(qs) or not all(q.get('number') == i + 1 for i, q in p1))):
            continue
        nums = sorted(q['number'] for _, q in p1)
        if nums == list(range(1, len(nums) + 1)):
            continue
        parts = sorted({q.get('part', 1) for q in qs})
        out = []
        for pt in parts:
            for k, q in enumerate([q for q in qs if q.get('part', 1) == pt], 1):
                q['number'] = k
                out.append(q)
        d['questions'] = out
        print(f, 'renumbered', {pt: sum(1 for q in out if q.get('part', 1) == pt) for pt in parts})
        if not dry:
            with open(p, 'w', encoding='utf-8') as fh:
                json.dump(d, fh, ensure_ascii=False, separators=(',', ':') if raw.startswith('{"') else None, indent=None if raw.startswith('{"') else 2)
                if raw.endswith('\n'):
                    fh.write('\n')


if __name__ == '__main__':
    main()
