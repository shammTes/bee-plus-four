"""Small helpers for the Oct 2026 teacher-feedback patch of the English notes (idempotent edits by id)."""
import json
import os
import re
import zlib

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
NOTES = os.path.join(ROOT, 'assets', 'high', 'notes', 'notes')
EXER = os.path.join(ROOT, 'assets', 'high', 'exercises')

_FORMATS = [dict(ensure_ascii=False, indent=2), dict(ensure_ascii=False, indent=1), dict(ensure_ascii=False, separators=(',', ':')),
            dict(ensure_ascii=True, separators=(',', ':')), dict(ensure_ascii=False)]


def load_json(path):
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    d = json.loads(raw)
    fmt, nl = _FORMATS[0], True
    for kw in _FORMATS:
        s = json.dumps(d, **kw)
        if raw in (s, s + '\n'):
            fmt, nl = kw, raw.endswith('\n')
            break
    return d, (fmt, nl)


def save_json(path, d, style):
    fmt, nl = style
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(d, **fmt) + ('\n' if nl else ''))


# ------------------------------------------------------------------ card / question builders
def grammar(id, title, rule, examples, pattern=None, page=1):
    c = dict(id=id, type='grammar', title=title, page=page, src='notes', rule=list(rule),
             examples=[dict(text=e[0], ok=e[1], **({'fix': e[2]} if len(e) > 2 and e[2] else {})) for e in examples])
    if pattern:
        c['pattern'] = pattern
    return c


def table(id, title, head, rows, page=1):
    return dict(id=id, type='table', title=title, page=page, src='notes', head=list(head), rows=[list(r) for r in rows])


def text(id, title, body, page=1, kind='text'):
    return dict(id=id, type=kind, title=title, page=page, src='notes', body=list(body))


def worked(id, title, problem, steps, answer, page=1):
    return dict(id=id, type='worked', title=title, problem=problem, steps=[dict(text=s) for s in steps], answer=answer, src='notes', page=page)


def check(id, q, options, answer, why, page=1):
    """why: list of paragraphs (joined with blank lines, like the existing cards)"""
    assert answer in options, id
    w = why if isinstance(why, str) else '\n\n'.join(why)
    return dict(id=id, type='check', title='Quick check', page=page, src='notes', q=q, options=dict(options), answer=answer, why=w)


def _q(id, typ, q, answer, why, tip, similar, page, **kw):
    assert similar, id
    d = dict(id=id, q=q, src='notes', page=page, similar=[dict(q=a, a=b) for a, b in similar], type=typ)
    d.update(kw)
    d['answer'] = answer
    d['why'] = list(why)
    d['tip'] = tip
    return d


def mcq(id, q, options, answer, why, tip, similar, page=1):
    assert answer in options, id
    why = list(why)
    if not why[0].startswith('Answer '):
        why.insert(0, f'Answer {answer}: {options[answer]}')
    return _q(id, 'mcq', q, answer, why, tip, similar, page, options=dict(options))


def fill(id, q, answer, choices, why, tip, similar, page=1):
    assert answer in choices, id
    # the app shows choices in file order (A, B, C, D): rotate them by a stable amount so the answer is not always A
    ch = list(choices)
    k = zlib.crc32(id.encode()) % len(ch)
    ch = ch[k:] + ch[:k]
    return _q(id, 'fill', q, answer, why, tip, similar, page, choices=ch)


def tf(id, q, answer, why, tip, similar, page=1):
    return _q(id, 'tf', q, bool(answer), why, tip, similar, page)


def short(id, q, answer, why, tip, similar, page=1, accept=None):
    kw = {'accept': list(accept)} if accept else {}
    return _q(id, 'short', q, answer, why, tip, similar, page, **kw)


# ------------------------------------------------------------------ book helpers
class Book:
    def __init__(self, grade):
        self.grade = grade
        self.path = os.path.join(NOTES, f'english_{grade}.json')
        self.d, self.style = load_json(self.path)

    def save(self):
        save_json(self.path, self.d, self.style)

    def unit(self, uid):
        for u in self.d['units']:
            if u['id'] == uid:
                return u
        raise KeyError(uid)

    def lesson(self, lid):
        for u in self.d['units']:
            for l in u['lessons']:
                if l['id'] == lid:
                    return u, l
        raise KeyError(lid)

    def find_card(self, cid):
        for u in self.d['units']:
            for l in u['lessons']:
                for i, c in enumerate(l['cards']):
                    if c['id'] == cid:
                        return u, l, i, c
        return None

    def card(self, cid):
        r = self.find_card(cid)
        if not r:
            raise KeyError(cid)
        return r[3]

    def has_card(self, cid):
        return self.find_card(cid) is not None

    def replace_card(self, new):
        """replace the card with the same id (content changes, id and place stay)"""
        u, l, i, _ = self.find_card(new['id'])
        if 'page' not in new or new.get('page') == 1:
            new['page'] = l['cards'][i].get('page', 1)
        l['cards'][i] = new

    def put_cards(self, lid, cards, after=None, before=None, page=None):
        """upsert cards into a lesson: existing ids are replaced in place (wherever they are), new ones are inserted
        after the card `after` (or before `before`, or at the end)"""
        u, l = self.lesson(lid)
        pg = page or l['pages'][0]
        for c in cards:
            if c.get('page', 1) == 1:
                c['page'] = pg
        new = []
        for c in cards:
            if self.has_card(c['id']):
                self.replace_card(c)
            else:
                new.append(c)
        if not new:
            return
        ids = [c['id'] for c in l['cards']]
        if after and after in ids:
            pos = ids.index(after) + 1
        elif before and before in ids:
            pos = ids.index(before)
        else:
            pos = len(ids)
        l['cards'][pos:pos] = new

    def move_card(self, cid, lid, after=None):
        u, l, i, c = self.find_card(cid)
        if l['id'] == lid:
            return
        del l['cards'][i]
        _, tl = self.lesson(lid)
        ids = [x['id'] for x in tl['cards']]
        pos = ids.index(after) + 1 if after and after in ids else len(ids)
        tl['cards'].insert(pos, c)

    def remove_card(self, cid):
        r = self.find_card(cid)
        if r:
            del r[1]['cards'][r[2]]

    def put_lesson(self, uid, lesson, after=None):
        u = self.unit(uid)
        for i, l in enumerate(u['lessons']):
            if l['id'] == lesson['id']:
                # keep cards already there (upserted separately); refresh the header
                for k in ('number', 'title', 'pages'):
                    l[k] = lesson[k]
                return l
        ids = [l['id'] for l in u['lessons']]
        pos = ids.index(after) + 1 if after in ids else len(ids)
        u['lessons'].insert(pos, lesson)
        return lesson

    def put_questions(self, uid, qs, after=None):
        u = self.unit(uid)
        lst = u['exercise']['questions']
        for q in qs:
            for i, x in enumerate(lst):
                if x['id'] == q['id']:
                    lst[i] = q
                    break
            else:
                lst.append(q)

    def question(self, qid):
        for u in self.d['units']:
            for q in u['exercise']['questions']:
                if q['id'] == qid:
                    return q
        raise KeyError(qid)

    def put_glossary(self, uid, items):
        u = self.unit(uid)
        terms = {g['term'].lower(): g for g in u['glossary']}
        for term, meaning in items:
            g = terms.get(term.lower())
            if g:
                g['meaning'] = meaning
            else:
                u['glossary'].append(dict(term=term, meaning=meaning, page=u['pages'][0], src='notes'))

    def strings(self):
        """yield (container, key) for every string in the book (for global replacements)"""
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if isinstance(v, str):
                        yield o, k
                    else:
                        yield from walk(v)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    if isinstance(v, str):
                        yield o, i
                    else:
                        yield from walk(v)
        yield from walk(self.d['units'])

    def sub_all(self, rules, where=None):
        """apply [(regex, repl)] to every string (or only inside the units/cards whose id is in `where`)"""
        n = 0
        roots = self.d['units'] if where is None else [x for x in self._objs() if x.get('id') in where]
        for root in roots:
            for o, k in _walk_strings(root):
                s = o[k]
                for rx, rp in rules:
                    s = re.sub(rx, rp, s)
                if s != o[k]:
                    o[k] = s
                    n += 1
        return n

    def _objs(self):
        for u in self.d['units']:
            yield u
            for l in u['lessons']:
                yield l
                for c in l['cards']:
                    yield c
            for q in u['exercise']['questions']:
                yield q


def _walk_strings(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str):
                if k not in ('id', 'type', 'src', 'lesson', 'from', 'to', 'root', 'kind'):
                    yield o, k
            else:
                yield from _walk_strings(v)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, str):
                yield o, i
            else:
                yield from _walk_strings(v)


def unitmap(uid, unit_label, topics):
    """topics: [(node_id, label, lesson_id, [card ids])] -> hand-made concept map (unit -> topics)"""
    first = [t[3][0] for t in topics]
    nodes = [dict(id='unit', label=unit_label[:40], kind='unit', cards=first)]
    edges = []
    for nid, label, lid, cards in topics:
        nodes.append(dict(id=nid, label=label[:40], kind='topic', lesson=lid, cards=list(cards)))
        edges.append({'from': 'unit', 'to': nid, 'label': 'includes'})
    return dict(root='unit', src='hand', nodes=nodes, edges=edges)
