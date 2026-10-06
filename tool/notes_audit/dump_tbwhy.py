#!/usr/bin/env python3
"""print the exercise questions whose explanation is only a 'Textbook p.N:' quote (one line each) for rewriting"""
import json, re, sys, os
BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'assets/high/notes/notes')
TB = re.compile(r'^Textbook p\.\s*\d+[:\.]?\s*', re.I)
b = sys.argv[1]
d = json.load(open(os.path.join(BASE, b + '.json')))
for u in d['units']:
    for q in u['exercise']['questions']:
        w = q['why'] if isinstance(q['why'], list) else [q['why']]
        if not any(TB.match(x) for x in w):
            continue
        if q['type'] == 'mcq':
            a = f"{q['answer']}) {q['options'].get(q['answer'])}"
            opts = ' / '.join(f'{k}) {v}' for k, v in q['options'].items())
        elif q['type'] == 'tf':
            a, opts = str(q['answer']), ''
        else:
            a, opts = q['answer'], ' / '.join(q.get('choices', []))
        other = [x for x in w if not TB.match(x) and not x.startswith('Answer')]
        print(f"{q['id']}|{q['type']}|{q['q'][:220]}|{opts[:200]}|=> {a[:120]}" + (f"|other: {' '.join(other)[:150]}" if other else ''))
