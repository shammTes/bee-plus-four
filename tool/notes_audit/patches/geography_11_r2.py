#!/usr/bin/env python3
"""Geography 11 round 2: move river checks out of the desert lesson, drop/move cards that sat in the wrong lesson,
and make the contour-map exam checks self-contained (the exam map is not in the app)."""
import json, os, re
P = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets/high/notes/notes/geography_11.json')
d = json.load(open(P, encoding='utf-8'))
L = {l['id']: l for u in d['units'] for l in u['lessons']}


def take(lid, cid):
    cs = L[lid]['cards']
    i = next(i for i, c in enumerate(cs) if c['id'] == cid)
    return cs.pop(i)


def move(src, dst, *ids):
    for cid in ids:
        if any(c['id'] == cid for c in L[src]['cards']):
            L[dst]['cards'].append(take(src, cid))


# ox-bow lake / levee items belong to 2.3 Stages of a River, not 2.5 desert landscapes
move('geo11-u2-l2-5', 'geo11-u2-l2-3', 'geo11-u2-chk80', 'geo11-u2-wrk9', 'geo11-u2-chk81', 'geo11-u2-wrk10')
# a copy of the unit 5 "pre-industrial / industrial" table sat in the contour-map lesson
for lid, cid in [('geo11-u8-l8-1', 'geo11-u8-tbl1'), ('geo11-u7-l7-3', 'geo11-u7-c13')]:
    if any(c['id'] == cid for c in L[lid]['cards']):
        take(lid, cid)
# valley-vs-spur text belongs to 8.2
move('geo11-u8-l8-4', 'geo11-u8-l8-2', 'geo11-u8-c07')
# the contour-map exam checks: no map in the app, so describe the map in the stem
FIX = {
    'geo11-u8-l8-2-mx1': dict(q='On a contour map, point **K** lies where the contours form a V shape pointing towards **lower** ground. Point K is on a:',
                              why='Contours that form a V pointing towards lower ground show a tongue of high land sticking out into lower land. That is a **spur**. (A valley\'s V points the other way, towards higher ground.)'),
    'geo11-u8-l8-2-mx2': dict(q='On a contour map, point **T** lies at a low point on the crest between two hilltops, only slightly lower than both. Point T is on a:',
                              why='A low area between two higher hilltops, only slightly lower than them, is a **saddle** (col). A pass is a lower gap that provides a route through mountains.'),
    'geo11-u8-l8-4-mx1': dict(q='Which pair of points on a contour map is most likely to be **intervisible**?',
                              options={'A': 'P (900 m) and M (700 m) on one smooth concave slope with no higher ground between them',
                                       'B': 'X (600 m) and Y (650 m) with a 700 m ridge between them',
                                       'C': 'K and L on opposite sides of a hill summit',
                                       'D': 'two points in neighbouring valleys separated by a spur'},
                              answer='A',
                              why='Two points are intervisible only if no ground between them rises above the line joining them.\n- **P and M** lie on one concave slope with nothing higher in between, so they can see each other.\n- In the other pairs a ridge, summit or spur blocks the line of sight.'),
}
for u in d['units']:
    for l in u['lessons']:
        for c in l['cards']:
            if c['id'] in FIX:
                c.update(FIX[c['id']])
        # the duplicate gradient exam check is replaced by a self-contained r2 check
        l['cards'] = [c for c in l['cards'] if c['id'] != 'geo11-u8-l8-3-mx1']
        # unit-2 weathering cards copied into 6.1 Location and 7.1 Relief (they test unit 2 and already exist there)
        if l['id'] in ('geo11-u6-l6-1', 'geo11-u7-l7-1'):
            u_ = l['id'][:8]
            dup = {u_ + s_ for s_ in ('-wrk1', '-wrk2', '-chk1', '-chk2', '-chk73')}
            l['cards'] = [c for c in l['cards'] if c['id'] not in dup]
        for c in l['cards']:
            if isinstance(c.get('why'), str):
                c['why'] = re.sub(r'\n*!\[[^\]]*\]\([^)]*\)', '', c['why']).rstrip()
open(P, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
