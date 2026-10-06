#!/usr/bin/env python3
"""one line per lesson: id, title, pages, checks, worked, teaching chars, card titles"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scan import card_text
BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'assets/high/notes/notes')
d = json.load(open(os.path.join(BASE, sys.argv[1] + '.json')))
full = '-v' in sys.argv
for u in d['units']:
    print(f"== {u['id']} {u['title']} pages={u.get('pages')} ex={len(u['exercise']['questions'])} games={len(u.get('games') or [])} gloss={len(u.get('glossary') or [])}")
    for l in u['lessons']:
        cs = l['cards']
        ch = sum(c['type'] == 'check' for c in cs); wk = sum(c['type'] == 'worked' for c in cs)
        teach = sum(len(card_text(c)) for c in cs if c['type'] not in ('check',))
        print(f"  {l['id']} {l['number']} {l['title']} p{l.get('pages')} chk={ch} wk={wk} teach={teach}")
        if full:
            for c in cs:
                t = c.get('title', '')
                extra = (c.get('q') or c.get('problem') or ' '.join(c.get('body', [])) or '')[:110].replace('\n', ' ')
                print(f"     - {c['id']} {c['type']}: {t[:40]} | {extra}")
