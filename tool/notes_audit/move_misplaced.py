#!/usr/bin/env python3
"""Round 2: move checks (and their paired step-by-step worked card) that sit in the wrong lesson of a unit.

Input: a TSV of moves `book<TAB>card_id<TAB>from_lesson<TAB>to_lesson` (tool/notes_audit/r2/moves.tsv). Candidates
were found by comparing each check's words with every lesson of its unit; only candidates whose words match the
destination lesson's title (and not the current one's) were kept, then spot-checked by hand.
usage: python3 tool/notes_audit/move_misplaced.py [--dry]
"""
import json, os, sys, collections
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
TSV = os.path.join(os.path.dirname(__file__), 'r2', 'moves.tsv')
dry = '--dry' in sys.argv
by_book = collections.defaultdict(list)
for line in open(TSV, encoding='utf-8'):
    if line.strip() and not line.startswith('#'):
        b, cid, src, dst = line.rstrip('\n').split('\t')[:4]
        by_book[b].append((cid, src, dst))
n = 0
for b, moves in sorted(by_book.items()):
    p = os.path.join(ROOT, 'assets/high/notes/notes', b + '.json')
    d = json.load(open(p, encoding='utf-8'))
    L = {l['id']: l for u in d['units'] for l in u['lessons']}
    for cid, src, dst in moves:
        cs = L[src]['cards']
        chk = next((c for c in cs if c['id'] == cid), None)
        if chk is None:
            continue  # already moved
        key = (chk.get('q') or '').strip()
        moving = [c for c in cs if c is chk or (c['type'] == 'worked' and key and (c.get('problem') or '').strip() == key)]
        L[src]['cards'] = [c for c in cs if not any(c is m for m in moving)]
        L[dst]['cards'].extend(moving)
        n += len(moving)
    if not dry:
        open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print(('would move' if dry else 'moved'), n, 'cards')
