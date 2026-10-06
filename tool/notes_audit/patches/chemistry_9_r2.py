#!/usr/bin/env python3
"""Chemistry 9 round 2: drop the flattened, cut-off markdown apparatus table from the 4.1 text card (the same table
is already shown as a proper table card in the lesson)."""
import json, os, re
P = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets/high/notes/notes/chemistry_9.json')
d = json.load(open(P, encoding='utf-8'))
for u in d['units']:
    for l in u['lessons']:
        for c in l['cards']:
            if c['id'] == 'chem9-u4-c01':
                c['body'] = [b for b in c['body'] if not re.search(r'\|\s*:?-{3}', b)]
open(P, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
