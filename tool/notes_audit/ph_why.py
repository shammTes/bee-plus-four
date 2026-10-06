#!/usr/bin/env python3
"""Round 3: replace 'Textbook p.N:' quote explanations with written step-by-step ones.
Input tool/notes_audit/r3/<book>.why, blocks:
  @<question id>
  Q: new stem (optional, adds missing context)   A: new answer (optional)
  W: step | step | step                          T: tip
Writes into the book file or into its unit_<id>.json override (kept compact)."""
import json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, '..', '..', 'assets/high/notes/notes')
TB = re.compile(r'^\s*Textbook p\.?\s*\d+', re.I)


def parse(path):
    out, cur = {}, None
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('#'):
            continue
        if line.startswith('@'):
            cur = out.setdefault(line[1:].strip(), {})
            continue
        k, v = line.split(':', 1)
        cur[k.strip()] = v.strip()
    return out


def apply(q, e):
    assert 'W' in e and 'T' in e, q['id']
    if 'Q' in e:
        q['q'] = e['Q']
        if isinstance(q.get('label'), str):
            m = re.match(r'^(\d+\.\s*)', q['label'])
            s = e['Q'] if len(e['Q']) <= 100 else e['Q'][:100].rsplit(' ', 1)[0] + '…'
            q['label'] = (m.group(1) if m else '') + s
    if 'A' in e:
        q['answer'] = e['A']
    if q['type'] == 'mcq':
        assert q['answer'] in q['options'], q['id']
    q['why'] = [s.strip() for s in e['W'].split(' | ') if s.strip()]
    q['tip'] = e['T']
    q['why_src'] = 'written'


def main(book):
    ed = parse(os.path.join(HERE, 'r3', book + '.why'))
    files = {os.path.join(B, book + '.json'): None}
    d = json.load(open(os.path.join(B, book + '.json')))
    targets = [(os.path.join(B, book + '.json'), d, d['units'])]
    ids = {u['id'] for u in d['units']}
    for f in glob.glob(os.path.join(B, 'unit_*.json')):
        u = json.load(open(f))
        if u.get('id') in ids:
            targets.append((f, u, [u]))
    done, left, seen = 0, [], set()
    for f, root, units in targets:
        ch = False
        for u in units:
            for q in (u.get('exercise') or {}).get('questions', []):
                if q['id'] in ed:
                    apply(q, ed[q['id']]); seen.add(q['id']); done += 1; ch = True
                elif any(TB.match(x) for x in (q['why'] if isinstance(q['why'], list) else [q['why']])):
                    left.append(q['id'])
        if ch:
            raw = open(f).read()
            compact = not raw.startswith('{\n')
            txt = json.dumps(root, ensure_ascii=False, separators=(',', ':')) if compact else json.dumps(root, indent=2, ensure_ascii=False)
            open(f, 'w').write(txt + '\n')
    # overrides replace their unit: also mirror into the book copy if both have the question (harmless)
    print(book, 'written:', done, 'unknown ids:', sorted(set(ed) - seen), 'still quoting:', len(left))
    return left


if __name__ == '__main__':
    for b in sys.argv[1:]:
        main(b)
