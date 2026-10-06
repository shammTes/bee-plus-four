#!/usr/bin/env python3
"""Round 3: replacement checks / worked examples for lessons that give away a misplaced check.
Reads tool/notes_audit/r3/rep_<book>.txt and inserts the new cards after the lesson's last check card
(or at the end of the lesson). Re-runnable: strips earlier '-r3r' cards first.

  @lesson <lesson id>
  C: question              (check)
  O: *correct | wrong | wrong | wrong     (shuffled deterministically; * marks the key)
  W: step | step | Tip: tip

  WK: title                (worked example)
  P: problem
  ST: step | step | step
  A: answer
"""
import json, os, re, sys, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAG = 'study notes (r3)'


def blocks(path):
    out, cur_lesson = [], None
    for chunk in re.split(r'\n\s*\n', open(path, encoding='utf-8').read()):
        b = {}
        for line in chunk.strip().splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('@lesson '):
                cur_lesson = line.split(None, 1)[1].strip(); continue
            k, _, v = line.partition(':')
            b[k.strip()] = v.strip()
        if b:
            b['lesson'] = cur_lesson
            out.append(b)
    return out


def main(book):
    # book may also be a unit override such as unit_phys11-u3 (a single unit object that replaces that unit in the app)
    path = os.path.join(ROOT, 'assets/high/notes/notes', book + '.json')
    raw = open(path, encoding='utf-8').read()
    d = json.loads(raw)
    compact = not raw.startswith('{\n')
    L = {l['id']: l for u in d.get('units', [d]) for l in u.get('lessons', [])}
    for l in L.values():
        l['cards'] = [c for c in l['cards'] if '-r3r' not in str(c.get('id', ''))]
    cnt = {'check': 0, 'worked': 0}
    seq = {}
    for b in blocks(os.path.join(ROOT, 'tool/notes_audit/r3', 'rep_' + book + '.txt')):
        l = L[b['lesson']]
        pg = next((c.get('page') for c in l['cards'] if c.get('page')), None)
        n = seq[l['id']] = seq.get(l['id'], 0) + 1
        if 'C' in b:
            opts = [o.strip() for o in b['O'].split('|')]
            key = next(o[1:].strip() for o in opts if o.startswith('*'))
            opts = [o.lstrip('*').strip() for o in opts]
            h = int(hashlib.md5(b['C'].encode()).hexdigest(), 16)
            rot = h % len(opts)
            opts = opts[rot:] + opts[:rot]
            letters = 'ABCDE'
            parts = [p.strip() for p in b['W'].split('|') if p.strip()]
            tip = next((p[4:].strip() for p in parts if p.lower().startswith('tip:')), None)
            steps = [p for p in parts if not p.lower().startswith('tip:')]
            why = '\n\n'.join(f'**Step {i}:** {s}' for i, s in enumerate(steps, 1)) + (f'\n\n**Tip:** {tip}' if tip else '')
            card = {'id': f"{l['id']}-r3r{n}", 'type': 'check', 'title': 'Quick check', 'page': pg, 'src': TAG, 'q': b['C'],
                    'options': {letters[i]: o for i, o in enumerate(opts)}, 'answer': letters[opts.index(key)], 'why': why}
        else:
            card = {'id': f"{l['id']}-r3rw{n}", 'type': 'worked', 'title': b['WK'], 'page': pg, 'src': TAG, 'problem': b['P'],
                    'steps': [{'text': s.strip()} for s in b['ST'].split('|') if s.strip()], 'answer': b['A']}
        if pg is None:
            card.pop('page')
        cs = l['cards']
        last = max((i for i, c in enumerate(cs) if c.get('type') == card['type']), default=len(cs) - 1)
        cs.insert(last + 1, card)
        cnt[card['type']] += 1
    out = json.dumps(d, ensure_ascii=False, separators=(',', ':')) if compact else json.dumps(d, ensure_ascii=False, indent=2)
    open(path, 'w', encoding='utf-8').write(out + ('\n' if raw.endswith('\n') else ''))
    print(book, cnt)


if __name__ == '__main__':
    for bk in sys.argv[1:]:
        main(bk)
