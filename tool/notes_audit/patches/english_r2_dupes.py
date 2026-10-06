#!/usr/bin/env python3
"""Round 2: generic cards copied into unrelated lessons. eng9 unit-3 pronoun items also sat in 1.1 Past tenses;
the same 'She go to school' worked card sat in eight eng11 units (kept only in u11 Verbs). Lesson-specific r2 cards
replace them."""
import json, os
B = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets/high/notes/notes/')
DROP = {
    'english_9.json': {'eng9-u1-wrkE1', 'eng9-u1-wrkE2', 'eng9-u1-chkE1', 'eng9-u1-chkE2'},
    'english_11.json': {f'eng11-u{n}-l1-wk1' for n in (9, 10, 12, 13, 14, 15, 16)},
}
for fn, ids in DROP.items():
    p = B + fn
    d = json.load(open(p, encoding='utf-8'))
    for u in d['units']:
        for l in u['lessons']:
            l['cards'] = [c for c in l['cards'] if c['id'] not in ids]
    open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
