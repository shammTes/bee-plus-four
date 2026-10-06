#!/usr/bin/env python3
"""Round-2 authored content -> notes JSON.

usage: python3 tool/notes_audit/author.py [book ...]   (default: every tool/notes_audit/r2/*.txt)

Each r2/<book>.txt holds hand-written items in a small block format (blank line between blocks):

  @unit <unit id>           following Q blocks go to that unit's exercise
  @lesson <lesson id>       following C / WK / X blocks go to that lesson
  @tip <text>               default tip for Q/C blocks after it

  Q: <question>             exercise question: O -> mcq (the option starting with * is the key; options are shuffled
  O: *right | wrong | ...      deterministically), A -> short answer, TF: true|false -> true/false
  W: step | step | ...      explanation steps
  T: <tip>                  (optional, else @tip)
  S: <similar q> => <answer>  (1+)

  C: <check question>       quick check card (O, W, T as above)
  WK: <title>               worked example: P: problem, ST: step | step, A: answer
  X: <title>                text card: B: one line per paragraph (inserted before the lesson's first check/worked card)
  R: <title>                remember card: B: lines

'\\n' inside a field is a line break. Everything this script adds has src 'r2'; re-running first removes the old 'r2' items.
"""
import glob, hashlib, json, os, random, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
NOTES = os.path.join(ROOT, 'assets/high/notes/notes')
SRC = os.path.join(os.path.dirname(__file__), 'r2')
LET = 'ABCDE'


def short(t, n=100):
    t = ' '.join(t.split())
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'


def parse(path):
    blocks, ctx = [], {'unit': None, 'lesson': None, 'tip': None}
    for raw in re.split(r'\n\s*\n', open(path, encoding='utf-8').read()):
        lines = [l for l in raw.strip().split('\n') if l.strip() and not l.lstrip().startswith('#')]
        if not lines:
            continue
        rest = []
        for l in lines:
            if l.startswith('@'):
                k, _, v = l[1:].partition(' ')
                ctx[k] = v.strip()
                if k == 'unit':
                    ctx['lesson'] = None
            else:
                rest.append(l)
        if not rest:
            continue
        b = {'_ctx': dict(ctx), 'S': [], 'B': []}
        for l in rest:
            m = re.match(r'^(Q|O|W|T|S|C|WK|P|ST|A|TF|X|R|B):\s?(.*)$', l)
            if not m:
                if b.get('_last') in ('B',):
                    b['B'][-1] += ' ' + l.strip()
                    continue
                k = b.get('_last')
                if k and k not in ('S',):
                    b[k] += ' ' + l.strip()
                    continue
                raise SystemExit(f'{path}: bad line: {l!r}')
            k, v = m.group(1), m.group(2).strip().replace('\\n', '\n')
            if k in ('S', 'B'):
                b[k].append(v)
            else:
                b[k] = v
            b['_last'] = k
        b['_kind'] = next(k for k in ('Q', 'C', 'WK', 'X', 'R') if k in b)
        blocks.append(b)
    return blocks


def split(v):
    return [s.strip() for s in v.split(' | ') if s.strip()]


def options(b, qid):
    opts = split(b['O'])
    keys = [o for o in opts if o.startswith('*')]
    if len(keys) != 1:
        raise SystemExit(f'{qid}: need exactly one *key: {b["O"]}')
    key = keys[0][1:].strip()
    opts = [o[1:].strip() if o.startswith('*') else o for o in opts]
    if len(set(opts)) != len(opts):
        raise SystemExit(f'{qid}: duplicate options')
    if not re.search(r'\b(all|none|both) of the (above|these)\b|\b[A-D] and [A-D]\b', b['O'], re.I):
        random.Random(hashlib.md5(qid.encode()).hexdigest()).shuffle(opts)
    o = {LET[i]: t for i, t in enumerate(opts)}
    ans = next(k for k, t in o.items() if t == key)
    return o, ans


def page_of(x):
    p = x.get('pages') if isinstance(x, dict) else None
    if isinstance(p, list) and p:
        return p[0]
    return p if isinstance(p, int) else (x.get('page') if isinstance(x.get('page'), int) else 1)


def strip_r2(o):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if isinstance(v, list):
                o[k] = [strip_r2(x) for x in v if not (isinstance(x, dict) and x.get('src') == 'r2')]
            elif isinstance(v, dict):
                strip_r2(v)
    return o


def build(book):
    path = os.path.join(NOTES, book + '.json')
    d = strip_r2(json.load(open(path, encoding='utf-8')))
    units = {u['id']: u for u in d['units']}
    lessons = {l['id']: (u, l) for u in d['units'] for l in u['lessons']}
    n = {'exercise': 0, 'check': 0, 'worked': 0, 'text': 0}
    counters = {}
    for b in parse(os.path.join(SRC, book + '.txt')):
        c, kind = b['_ctx'], b['_kind']
        tip = b.get('T') or c.get('tip') or 'Read every option against the rule before choosing.'
        if kind == 'Q':
            u = units[c['unit']]
            qs = u.setdefault('exercise', {}).setdefault('questions', [])
            counters[u['id']] = counters.get(u['id'], 0) + 1
            qid = f"{u['id']}-r2q{counters[u['id']]:02d}"
            q = {'id': qid, 'q': b['Q'], 'src': 'r2', 'page': page_of(u), 'label': f"{len(qs) + 1}. {short(b['Q'])}"}
            if not b['S']:
                raise SystemExit(f'{qid}: no similar question')
            q['similar'] = [dict(zip(('q', 'a'), (x.strip() for x in s.split(' => ', 1)))) for s in b['S']]
            if any(len(s) != 2 for s in q['similar']):
                raise SystemExit(f'{qid}: similar needs "q => a"')
            steps = split(b.get('W', ''))
            if not steps:
                raise SystemExit(f'{qid}: no explanation')
            if 'O' in b:
                q['type'], (q['options'], q['answer']) = 'mcq', options(b, qid)
                q['why'] = [f"Answer {q['answer']}: {q['options'][q['answer']]}"] + steps
            elif 'TF' in b:
                q['type'], q['answer'] = 'tf', b['TF'].lower() == 'true'
                q['why'] = [('True. ' if q['answer'] else 'False. ') + steps[0]] + steps[1:]
            else:
                q['type'], q['answer'] = 'short', b['A']
                q['why'] = steps
            q['tip'] = tip
            qs.append(q)
            n['exercise'] += 1
        else:
            u, l = lessons[c['lesson']]
            cards = l['cards']
            counters[l['id']] = counters.get(l['id'], 0) + 1
            cid = f"{l['id']}-r2{kind.lower()}{counters[l['id']]}"
            pg = page_of(l) or page_of(u)
            if kind == 'C':
                o, ans = options(b, cid)
                steps = split(b.get('W', ''))
                if not steps:
                    raise SystemExit(f'{cid}: no explanation')
                why = '\n\n'.join(f'**Step {i + 1}:** {s}' for i, s in enumerate(steps)) + f'\n\n**Tip:** {tip}'
                cards.append({'id': cid, 'type': 'check', 'title': 'Quick check', 'page': pg, 'src': 'r2', 'q': b['C'],
                              'options': o, 'answer': ans, 'why': why})
                n['check'] += 1
            else:
                if kind == 'WK':
                    card = {'id': cid, 'type': 'worked', 'title': b['WK'], 'page': pg, 'src': 'r2', 'problem': b['P'],
                            'steps': [{'text': s} for s in split(b['ST'])], 'answer': b['A']}
                    n['worked'] += 1
                else:
                    card = {'id': cid, 'type': 'text' if kind == 'X' else 'remember', 'title': b[kind], 'page': pg,
                            'src': 'r2', 'body': b['B']}
                    if not b['B']:
                        raise SystemExit(f'{cid}: empty body')
                    n['text'] += 1
                at = next((i for i, x in enumerate(cards) if x.get('type') in (('check', 'worked') if kind != 'WK' else ('check',))), len(cards))
                cards.insert(at, card)
    s = json.dumps(d, ensure_ascii=False, indent=2) + '\n'
    open(path, 'w', encoding='utf-8').write(s)
    print(book, n)


if __name__ == '__main__':
    books = sys.argv[1:] or sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(SRC, '*.txt')))
    for bk in books:
        build(bk)
