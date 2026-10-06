#!/usr/bin/env python3
"""Round-3 thin-lesson expansion. Reads tool/notes_audit/r3/thin_<book>.txt and adds, per lesson,
a step-by-step explanation card (with a worked example), a mnemonic card and an exam-tip card.
Re-runnable: strips earlier '-r3x' cards first.

Block syntax (blank line between blocks):
  @lesson <lesson id>
  TITLE: <topic>
  S: step 1 | step 2 | ...
  E: example
  M: <mnemonic heading> — <how to use it>
  T: tip
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAG = 'study notes (r3)'
TEACH = ('text', 'remember', 'table', 'mnemonic', 'grammar', 'reading', 'diagram', 'steps', 'states', 'graph', 'worked')


def blocks(path):
    out = []
    for chunk in re.split(r'\n\s*\n', open(path, encoding='utf-8').read()):
        b = {}
        for line in chunk.strip().splitlines():
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if line.startswith('@lesson '):
                b['lesson'] = line.split(None, 1)[1].strip()
                continue
            k, _, v = line.partition(':')
            b[k.strip()] = v.strip()
        if b:
            out.append(b)
    return out


def main(book):
    path = os.path.join(ROOT, 'assets/high/notes/notes', book + '.json')
    raw = open(path, encoding='utf-8').read()
    indent = 1 if '\n "' in raw[:50] else 2
    d = json.loads(raw)
    lessons = {l['id']: l for u in d['units'] for l in u.get('lessons', [])}
    for l in lessons.values():
        l['cards'] = [c for c in l['cards'] if '-r3x' not in str(c.get('id', ''))]
    n = 0
    for b in blocks(os.path.join(ROOT, 'tool/notes_audit/r3', 'thin_' + book + '.txt')):
        l = lessons[b['lesson']]
        pg = next((c.get('page') for c in l['cards'] if c.get('page')), None)
        steps = [s.strip() for s in b['S'].split('|') if s.strip()]
        body = [f'**Step {i}:** {s}' for i, s in enumerate(steps, 1)] + ['**Example:** ' + b['E']]
        head, _, use = b['M'].partition(' — ')
        new = [
            {'id': l['id'] + '-r3x1', 'type': 'text', 'title': 'Step by step: ' + b['TITLE'], 'page': pg, 'src': TAG, 'body': body},
            {'id': l['id'] + '-r3x2', 'type': 'mnemonic', 'title': 'Mnemonic — ' + head.strip(), 'page': pg, 'src': TAG, 'body': [use.strip() or head.strip()]},
            {'id': l['id'] + '-r3x3', 'type': 'remember', 'title': 'Exam tip', 'page': pg, 'src': TAG, 'body': [b['T']]},
        ]
        for c in new:
            if pg is None:
                c.pop('page')
        cards = l['cards']
        last = max((i for i, c in enumerate(cards) if c.get('type') in TEACH and c.get('type') != 'worked'), default=-1)
        l['cards'] = cards[:last + 1] + new + cards[last + 1:]
        n += 1
    open(path, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=indent) + '\n')
    print(book, 'expanded lessons:', n)


if __name__ == '__main__':
    for bk in sys.argv[1:]:
        main(bk)
