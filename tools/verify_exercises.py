#!/usr/bin/env python3
"""Sanity checks for the Exercise tab banks (assets/high/exercises).

Checks every main + school file listed in index.json:
  * parses; every question has a non-empty prompt and explanation, a list of
    non-empty, distinct options and an int answer index inside the list
  * even number of $$ in every string; no string cut off mid-word
  * index.json totals/per-unit counts match the files (main file only)
  * every notes unit (assets/high/notes/notes/index.json) has >= MIN items
    (main + school), and every Grade 12 / English unit is non-empty
Exit code 1 on any failure.
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, 'assets/high/exercises')
NOTES = os.path.join(ROOT, 'assets/high/notes/notes/index.json')
MIN = int(os.environ.get('MIN_PER_UNIT', 25))

errors = []


def err(msg):
    errors.append(msg)


# A string "ends mid-word" if it stops on a lowercase letter right after another letter and
# the last word is not a real word ending. We only flag long strings (explanations) that end
# with a letter and no punctuation, which in this data always meant truncated OCR text.
def cut_off(s, long_only):
    t = s.rstrip()
    if not t:
        return False
    if t.endswith('$$') or t[-1] in '.!?)"\'’”]:;%°*`>…' or t[-1].isdigit():
        return False
    if long_only and len(t) < 120:
        return False
    return bool(re.search(r'[a-z]{1,2}$', t)) and not re.search(r'\b(is|an|a|of|to|in|on|at|by|or|as|it|be|we|he|me|no|so|up|us|do|go|if|my)$', t) and len(t.split()[-1]) <= 2


def check_q(fn, q):
    qid = q.get('id', '?')
    where = f'{fn}:{qid}'
    p, ex, opts, ans = q.get('prompt'), q.get('explanation'), q.get('options'), q.get('answer')
    if not isinstance(p, str) or not p.strip():
        err(f'{where}: empty prompt')
    if not isinstance(ex, str) or not ex.strip():
        err(f'{where}: empty explanation')
    if not isinstance(opts, list) or len(opts) < 2:
        err(f'{where}: options must be a list of >= 2')
        return
    if any(not isinstance(o, str) or not o.strip() for o in opts):
        err(f'{where}: empty option')
    if len({re.sub(r"\s+", " ", o).strip() for o in opts if isinstance(o, str)}) != len(opts):
        err(f'{where}: duplicate options')
    if not isinstance(ans, int) or not (0 <= ans < len(opts)):
        err(f'{where}: answer index {ans!r} out of range')
    for s in [p, ex] + list(opts):
        if isinstance(s, str) and s.count('$$') % 2:
            err(f'{where}: odd $$ count')
    if isinstance(ex, str) and cut_off(ex, True):
        err(f'{where}: explanation looks cut off: ...{ex[-40:]!r}')


def main():
    idx = json.load(open(os.path.join(EX, 'index.json'), encoding='utf-8'))
    notes = json.load(open(NOTES, encoding='utf-8'))['grades']
    total = 0
    per_unit = {}
    for g, subs in idx['grades'].items():
        for subj, ent in subs.items():
            fn = ent['file']
            qs = json.load(open(os.path.join(EX, fn), encoding='utf-8'))['questions']
            ids = [q.get('id') for q in qs]
            if len(ids) != len(set(ids)):
                err(f'{fn}: duplicate ids')
            for q in qs:
                check_q(fn, q)
            c = collections.Counter(q.get('unit') or 'general' for q in qs)
            if ent.get('count') != len(qs):
                err(f'{fn}: index count {ent.get("count")} != {len(qs)}')
            if ent.get('units') and dict(c) != ent['units']:
                err(f'{fn}: index unit counts differ')
            total += len(qs)
            sp = os.path.join(EX, 'school', fn)
            sc = []
            if os.path.exists(sp):
                sc = json.load(open(sp, encoding='utf-8'))['questions']
                for q in sc:
                    check_q('school/' + fn, q)
            per_unit[(g, subj)] = c + collections.Counter(q.get('unit') or 'general' for q in sc)
    if idx.get('total') != total:
        err(f'index total {idx.get("total")} != {total}')
    rows = []
    for g, subs in notes.items():
        for subj, book in subs.items():
            c = per_unit.get((g, subj))
            if c is None:
                err(f'no exercise file for grade {g} {subj}')
                continue
            for u in book['units']:
                n = c[u['id']]
                rows.append((g, subj, u['id'], n))
                if n < MIN:
                    err(f'{u["id"]}: only {n} items (< {MIN})')
                if (g == '12' or subj == 'english') and n == 0:
                    err(f'{u["id"]}: EMPTY')
    print(f'{total} main-file questions; {len(rows)} units checked; min per unit {min(r[3] for r in rows)}')
    if errors:
        print(f'{len(errors)} problem(s):')
        for e in errors[:200]:
            print('  ' + e)
        sys.exit(1)
    print('OK')


if __name__ == '__main__':
    main()
