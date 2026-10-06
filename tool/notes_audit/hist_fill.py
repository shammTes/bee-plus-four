#!/usr/bin/env python3
"""Round 4 (History, ADDITIVE ONLY): fill textbook pointers, complete cut-off points and expand short lessons.
Reads tool/notes_audit/r4/<book>*.txt (all files for that book, in name order) and INSERTS new text cards.
Pre-existing cards are never edited; re-running first strips earlier '-r4' cards, so the build is reproducible.

Blocks (blank line between blocks):
  @after <card id>            new card goes directly after that card; it 'fills' (completes) that card
  @unit <lesson id> <field prefix> [<field prefix> ...]
                              new card at the end of the lesson's teaching cards; fills unit-level items
                              (e.g. exercise.questions[2] or games[0]) whose explanation pointed at the course book
  @lesson <lesson id>         new explanation card for a short lesson (after its last original teaching card)
  T: title
  B: paragraph | paragraph | ...
  F: <extra field prefixes or card ids this card also fills>   (optional)
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEACH = ('text', 'remember', 'table', 'mnemonic', 'grammar', 'reading', 'diagram', 'steps', 'states', 'graph')


def blocks(path):
    out = []
    for chunk in re.split(r'\n\s*\n', open(path, encoding='utf-8').read()):
        b = {}
        for line in chunk.strip().splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('@'):
                kind, *args = line[1:].split()
                b['kind'], b['args'] = kind, args
                continue
            k, _, v = line.partition(':')
            b[k.strip()] = v.strip()
        if b:
            out.append(b)
    return out


def main(book):
    grade = book.split('_')[1]
    path = os.path.join(ROOT, 'assets/high/notes/notes', book + '.json')
    raw = open(path, encoding='utf-8').read()
    indent = 1 if raw.startswith('{\n "') else 2
    d = json.loads(raw)
    lessons = {l['id']: l for u in d['units'] for l in u.get('lessons', [])}
    where = {c['id']: l for l in lessons.values() for c in l['cards'] if 'id' in c}
    for l in lessons.values():
        l['cards'] = [c for c in l['cards'] if '-r4' not in str(c.get('id', ''))]
    n = {'after': 0, 'unit': 0, 'lesson': 0}
    seq = {}
    files = sorted(glob.glob(os.path.join(ROOT, 'tool/notes_audit/r4', book + '*.txt')))
    for f in files:
        for b in blocks(f):
            kind, args = b['kind'], b['args']
            if kind == 'after':
                l = where[args[0]]
                anchor = args[0]
            else:
                l = lessons[args[0]]
                anchor = None
            k = seq[l['id']] = seq.get(l['id'], 0) + 1
            cards = l['cards']
            pg = next((c.get('page') for c in cards if c.get('page')), None)
            card = {'id': f"{l['id']}-r4{kind[0]}{k}", 'type': 'text', 'title': b['T'], 'page': pg,
                    'src': f'Grade {grade} History course (r4)', 'body': [p.strip() for p in b['B'].split('|') if p.strip()]}
            if pg is None:
                card.pop('page')
            if kind == 'after':
                card['fills'] = [anchor]
                i = next(i for i, c in enumerate(cards) if c.get('id') == anchor)
                # keep consecutive completions for the same anchor in file order
                while i + 1 < len(cards) and anchor in (cards[i + 1].get('fills') or []):
                    i += 1
            else:
                if kind == 'unit':
                    card['fills'] = args[1:]
                orig = [i for i, c in enumerate(cards) if c.get('type') in TEACH and not re.search(r'-r[34]', str(c.get('id', '')))]
                i = orig[-1] if orig else -1
                while i + 1 < len(cards) and '-r4' in str(cards[i + 1].get('id', '')):
                    i += 1
            if b.get('F'):
                card['fills'] = card.get('fills', []) + b['F'].split()
            cards.insert(i + 1, card)
            n[kind] += 1
    open(path, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=indent) + '\n')
    print(book, n)


if __name__ == '__main__':
    for bk in sys.argv[1:]:
        main(bk)
