#!/usr/bin/env python3
"""Geography 12 round 2: study-note checks that sat one lesson off are moved to the lesson they test; the jumbled
7.3 text card (it was made of exercise sentences) is rewritten."""
import json, os
P = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets/high/notes/notes/geography_12.json')
d = json.load(open(P, encoding='utf-8'))
L = {l['id']: l for u in d['units'] for l in u['lessons']}
MOVES = [
    ('geo12-u3-l3-8', 'geo12-u3-l3-6', ['geo12-u3-chk15', 'geo12-u3-wrk15']),   # relative humidity -> 3.6 Humidity
    ('geo12-u6-l6-2', 'geo12-u6-l6-1', ['geo12-u6-chk3', 'geo12-u6-chk4']),     # staple / cash crops -> 6.1 Farming
    ('geo12-u7-l7-2', 'geo12-u7-l7-3', ['geo12-u7-chk3', 'geo12-u7-l7-2-mx1']), # ethnic groups -> 7.3
    ('geo12-u7-l7-2', 'geo12-u7-l7-1', ['geo12-u7-chk4']),                     # Hamitic migration -> 7.1 Background
    ('geo12-u7-l7-3', 'geo12-u7-l7-2', ['geo12-u7-chk5', 'geo12-u7-wrk5', 'geo12-u7-chk6', 'geo12-u7-wrk6']),  # TFR, age -> 7.2
]
for src, dst, ids in MOVES:
    for cid in ids:
        cs = L[src]['cards']
        i = next((i for i, c in enumerate(cs) if c['id'] == cid), None)
        if i is not None:
            L[dst]['cards'].append(cs.pop(i))
for c in L['geo12-u7-l7-3']['cards']:
    if c['id'] == 'geo12-u7-c03':
        c['body'] = [
            'Eritrea has **nine ethnic groups**. Without a census the figures are estimates, but they show the main pattern.',
            '**Tigrigna** (about 50%) live mainly in the highlands of Maekel and Debub. **Tigre** (about 31%), the second largest group, live in the Northern Red Sea, Anseba and Gash-Barka.',
            '**Afar** (about 5%) live in the Southern and Northern Red Sea; **Saho** (about 5%) in Debub and the Northern Red Sea; **Bidhaawyeet** (Hedareb, about 2.5%) in Anseba and Gash-Barka; **Bilen** (about 2.1%) in Anseba around Keren.',
            '**Kunama** (about 2%) and **Nara** (about 1.5%) live only in Gash-Barka; the **Rashaida** (under 1%) live in the Northern Red Sea.',
        ]
open(P, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
