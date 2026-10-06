"""Remove repeated worked examples (same problem text shown 2-3 times in a unit) and repeated checks
(same question twice in one lesson). The first copy is kept."""
import json, glob, os, re
BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'assets/high/notes/notes')
SKIP = ('physics', 'unit_phys', 'history', 'index')
norm = lambda s: re.sub(r'\s+', ' ', ' '.join(s) if isinstance(s, list) else (s or '')).strip().lower()
tot = 0
for f in sorted(glob.glob(os.path.join(BASE, '*.json'))):
    n = os.path.basename(f)
    if n.startswith(SKIP): continue
    b = json.load(open(f)); removed = []
    for u in b.get('units', []):
        seen_w = set()
        for l in u.get('lessons', []):
            seen_c = set(); keep = []
            for c in l.get('cards', []):
                if c.get('type') == 'worked':
                    k = norm(c.get('problem'))
                    if len(k) > 30 and k in seen_w: removed.append(c['id']); continue
                    seen_w.add(k)
                if c.get('type') == 'check':
                    k = norm(c.get('q'))
                    if len(k) > 30 and k in seen_c: removed.append(c['id']); continue
                    seen_c.add(k)
                keep.append(c)
            l['cards'] = keep
    if removed:
        tot += len(removed); print(n, len(removed), removed[:6])
        with open(f, 'w') as fh: json.dump(b, fh, ensure_ascii=False, indent=2); fh.write('\n')
print('total removed', tot)
