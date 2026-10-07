#!/usr/bin/env python3
"""Assemble tool/bookkeeping/tables.json from the automatic PDF extraction plus the hand transcriptions.

  python3 tool/bookkeeping/extract_tables.py   # needs the two textbook PDFs in /workspace/textbooks -> /tmp/raw_tables.json
  python3 tool/bookkeeping/clean_tables.py     # -> /tmp/clean_tables.json
  python3 tool/bookkeeping/assemble.py         # -> tool/bookkeeping/tables.json (committed; the notes are built from it)
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from overrides import OVERRIDES, ADDED, TITLE_FIX  # noqa: E402

SRC = sys.argv[1] if len(sys.argv) > 1 else '/tmp/clean_tables.json'
OUT = os.path.join(os.path.dirname(__file__), 'tables.json')
NOISE = re.compile(r'^(Business and Economics for Grade 1[01]|Unit [23] - Bookkeeping)')


def title_of(t):
    if t.get('titles'):
        return ' — '.join(x for x in t['titles'] if x)
    cap = [a for a in t.get('above', []) if a and not NOISE.match(a)][-2:]
    if any(a in TITLE_FIX for a in cap):
        return [a for a in cap if a in TITLE_FIX][-1]
    good = [a for a in cap if not a.startswith('Date') and a != 'Post.' and not a.endswith(('.', ':', ',')) and len(a) < 70
            and not re.search(r'\d,\d{3}|\b(CPJ|CRJ|SJ|PJ|GJ|J)\d', a) and not re.search(r'\b(the|of|is|are|and|to)\b.*\b(the|of|is|are|to)\b', a)]
    if good:
        return ' — '.join(good)
    return ''


def norm_rows(rows, w):
    out = []
    for r in rows:
        r = [re.sub(r'\s+', ' ', (c or '')).replace('Þ', 'fi').strip() for c in r] + [''] * (w - len(r))
        if any(r):
            out.append(r[:w])
    return out


def contained(a, b):
    """every row of a appears in b (ignoring empty cells of a)"""
    if len(a['rows']) >= len(b['rows']) or len(a['head']) != len(b['head']):
        return False
    def key(r): return [re.sub(r'[^0-9A-Za-z]', '', c).lower() for c in r]
    bk = [key(r) for r in b['rows']]
    for r in a['rows']:
        k = key(r)
        if not any(all(x == '' or x == y for x, y in zip(k, kb)) for kb in bk):
            return False
    return True


def main():
    d = json.load(open(SRC))
    out = {}
    for g in ('10', '11'):
        tabs = []
        for i, t in enumerate(d[g]):
            if (g, i) in OVERRIDES:
                rep = OVERRIDES[(g, i)]
                for x in rep or []:
                    tabs.append(dict(x, order=(x['page'], i)))
                continue
            title = title_of(t)
            tabs.append({'title': title, 'head': [h.replace('Þ', 'fi') for h in t['head']], 'rows': t['rows'], 'page': t['page'], 'order': (t['page'], i)})
        for j, x in enumerate(ADDED[g]):
            tabs.append(dict(x, order=(x['page'], 900 + j)))
        for t in tabs:
            t['title'] = TITLE_FIX.get(t['title'], t['title'])
            t['head'] = [re.sub(r'\s+', ' ', h).strip() for h in t['head']]
            t['rows'] = norm_rows(t['rows'], len(t['head']))
        for t in tabs:
            h = [x.lower() for x in t['head']]
            jp = next((j for j, x in enumerate(h) if x.startswith('p/') or x in ('pr', 'p/r', 'p/r.')), None)
            jd = next((j for j, x in enumerate(h) if x == 'debit'), None)
            if jp is not None and jd is not None:
                for r in t['rows']:
                    if re.fullmatch(r'[\d,]+\.\d\d', r[jp]) and not r[jd] and not any(r[:jp]):
                        r[jd], r[jp] = r[jp], ''
        tabs = [t for t in tabs if t['rows'] and any(re.search(r'\d{2}', c) for r in t['rows'] for c in r)]
        tabs.sort(key=lambda t: t['order'])
        # drop exact repeats and tables whose every row re-appears in a later, longer copy (the book grows a journal row by row)
        keep = []
        for k, t in enumerate(tabs):
            sig = json.dumps([t['head'], t['rows']])
            if any(json.dumps([u['head'], u['rows']]) == sig for u in keep):
                continue
            if any(contained(t, u) and 0 <= u['page'] - t['page'] <= 12 for u in tabs[k + 1:]):
                continue
            keep.append(t)
        for t in keep:
            t.pop('order', None)
        out[g] = keep
        print(g, len(tabs), '->', len(keep))
    json.dump(out, open(OUT, 'w'), ensure_ascii=False, indent=1)
    open(OUT, 'a').write('\n')


if __name__ == '__main__':
    main()
