"""Turn flattened tables in text-card bodies ('H1 — H2 | a — b | ...') into real table cards placed right after the card."""
import json, os, sys
D = os.path.join(os.path.dirname(__file__), '../../assets/high/notes/notes')

def parse(s):
    if ' | ' not in s or ' — ' not in s:
        return None
    rows = [r.strip() for r in s.split(' | ')]
    cells = [[c.strip() for c in r.split(' — ')] for r in rows]
    n = len(cells[0])
    if n < 2 or len(cells) < 3 or any(len(r) != n for r in cells):
        return None
    return cells[0], cells[1:]

def run(book):
    p = os.path.join(D, book + '.json')
    b = json.load(open(p)); made = 0
    ids = {c['id'] for u in b['units'] for l in u['lessons'] for c in l['cards']}
    for u in b['units']:
        for l in u['lessons']:
            out = []
            for c in l['cards']:
                out.append(c)
                if c.get('type') not in ('text', 'remember') or not isinstance(c.get('body'), list):
                    continue
                keep, tabs = [], []
                for s in c['body']:
                    t = parse(s) if isinstance(s, str) else None
                    if t:
                        tabs.append(t)
                    else:
                        keep.append(s)
                if not tabs:
                    continue
                c['body'] = keep
                for i, (h, rows) in enumerate(tabs):
                    nid = f"{c['id']}-t{i+1}"
                    while nid in ids:
                        nid += 'x'
                    ids.add(nid)
                    t = {'id': nid, 'type': 'table', 'title': h[0] if len(h[0]) < 40 else 'Summary table', 'head': h, 'rows': rows, 'src': c.get('src', 'notes')}
                    t['title'] = c.get('title', 'Table').split(' (')[0] + ' — table'
                    if 'page' in c:
                        t['page'] = c['page']
                    out.append(t); made += 1
                if not keep:
                    out.remove(c)
            l['cards'] = out
    json.dump(b, open(p, 'w'), ensure_ascii=False, indent=2); open(p, 'a').write('\n')
    return made

if __name__ == '__main__':
    for bk in sys.argv[1:]:
        print(bk, run(bk))
