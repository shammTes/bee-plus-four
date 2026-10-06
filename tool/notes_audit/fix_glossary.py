#!/usr/bin/env python3
"""Round 2: replace glossary meanings that were OCR sentences (not definitions) with concise definitions.
Input: tool/notes_audit/r2/glossary.txt, lines 'book|unit|term|definition'. History books are not touched."""
import json, os, collections
HERE = os.path.dirname(__file__)
BASE = os.path.join(HERE, '..', '..', 'assets/high/notes/notes')
todo = collections.defaultdict(dict)
for line in open(os.path.join(HERE, 'r2', 'glossary.txt'), encoding='utf-8'):
    if line.strip() and not line.startswith('#'):
        b, u, t, m = line.rstrip('\n').split('|', 3)
        assert not b.startswith('history'), line
        todo[b][(u, t)] = m
n = 0
for b, m in todo.items():
    p = os.path.join(BASE, b + '.json')
    raw = open(p, encoding='utf-8').read()
    d = json.loads(raw)
    for u in d.get('units') or [d]:
        for g in u.get('glossary') or []:
            k = (u['id'], g.get('term'))
            if k in m:
                g['meaning'] = m.pop(k)
                g.pop('enriched', None)
                g['src'] = 'hand'
                n += 1
    if m:
        raise SystemExit(f'{b}: not found {list(m)}')
    compact = not raw.startswith('{\n')
    txt = json.dumps(d, ensure_ascii=False, separators=(',', ':')) if compact else json.dumps(d, ensure_ascii=False, indent=2)
    open(p, 'w', encoding='utf-8').write(txt + '\n')
print('glossary meanings rewritten:', n)
