"""Tiny helpers for hand-written notes patches (tool/notes_audit/patches/<book>.py). Upserts by id, so a patch
can be re-run safely. Keeps the book's JSON style (indent 2, UTF-8, trailing newline)."""
import json, os, re

BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'assets/high/notes/notes')
META = {'id', 'src', 'pdf', 'source', 'book', 'file', 'src_qid', 'why_src', 'answer_src', 'type', 'page'}


class Book:
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(BASE, name + '.json')
        self.d = json.load(open(self.path))
        self.stats = {'cards_added': 0, 'cards_rewritten': 0, 'cards_removed': 0, 'ex_added': 0, 'subs': 0}

    # ---------------------------------------------------------------- lookup
    def unit(self, uid):
        return next(u for u in self.d['units'] if u['id'] == uid)

    def lesson(self, lid):
        return next(l for u in self.d['units'] for l in u['lessons'] if l['id'] == lid)

    def unit_of_lesson(self, lid):
        return next(u for u in self.d['units'] for l in u['lessons'] if l['id'] == lid)

    def card(self, cid):
        return next(c for u in self.d['units'] for l in u['lessons'] for c in l['cards'] if c.get('id') == cid)

    def where(self, cid):
        for u in self.d['units']:
            for l in u['lessons']:
                for i, c in enumerate(l['cards']):
                    if c.get('id') == cid:
                        return l, i
        return None, None

    # ---------------------------------------------------------------- edits
    def set(self, cid, **kw):
        c = self.card(cid)
        c.update(kw)
        c.pop('enriched', None)
        if c.get('src', '').startswith('textbook'):
            c['src'] = 'notes'
        self.stats['cards_rewritten'] += 1
        return c

    def remove(self, cid):
        l, i = self.where(cid)
        if l is not None:
            l['cards'].pop(i)
            self.stats['cards_removed'] += 1

    def add(self, lid, cards, after=None):
        """upsert cards into lesson lid (after card id `after`, else at the end)"""
        l = self.lesson(lid)
        pg = l['pages'][0] if l.get('pages') else 1
        for c in cards:
            c.setdefault('page', pg)
            c.setdefault('src', 'notes')
            ol, oi = self.where(c['id'])
            if ol is not None:
                ol['cards'][oi] = c
                continue
            if after:
                _, ai = self.where(after)
                l['cards'].insert(ai + 1, c)
                after = c['id']
            else:
                l['cards'].append(c)
            self.stats['cards_added'] += 1

    def move(self, cids, lid, after=None):
        """move existing cards (in order) to lesson lid (after card `after`, else at the end)"""
        l = self.lesson(lid)
        for cid in cids:
            ol, oi = self.where(cid)
            if ol is None:
                continue
            c = ol['cards'].pop(oi)
            if after:
                _, ai = self.where(after)
                l['cards'].insert(ai + 1, c)
                after = cid
            else:
                l['cards'].append(c)

    def ex(self, uid, qs):
        u = self.unit(uid)
        lst = u.setdefault('exercise', {}).setdefault('questions', [])
        pg = u['pages'][0] if u.get('pages') else 1
        for q in qs:
            q.setdefault('page', pg)
            q.setdefault('src', 'notes')
            i = next((k for k, x in enumerate(lst) if x['id'] == q['id']), None)
            if i is None:
                lst.append(q)
                self.stats['ex_added'] += 1
            else:
                lst[i] = q

    def sub(self, old, new, regex=False):
        n = 0

        def fx(s):
            nonlocal n
            t = re.sub(old, new, s) if regex else s.replace(old, new)
            if t != s:
                n += 1
            return t

        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in META:
                        continue
                    if isinstance(v, str):
                        o[k] = fx(v)
                    else:
                        walk(v)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    if isinstance(v, str):
                        o[i] = fx(v)
                    else:
                        walk(v)
        walk(self.d['units'])
        self.stats['subs'] += n
        if n == 0:
            print(f'  ! sub matched nothing: {old[:60]}')
        return n

    def save(self):
        open(self.path, 'w').write(json.dumps(self.d, indent=2, ensure_ascii=False) + '\n')
        print(self.name, self.stats)
        log = os.path.join(os.path.dirname(__file__), 'patch_stats.json')
        allst = json.load(open(log)) if os.path.exists(log) else {}
        allst[self.name] = self.stats
        json.dump(allst, open(log, 'w'), indent=1, sort_keys=True)


# ---------------------------------------------------------------- card / question builders
def text(id, title, body, **kw):
    return {'id': id, 'type': 'text', 'title': title, 'body': body if isinstance(body, list) else [body], **kw}


def remember(id, title, body, **kw):
    return {'id': id, 'type': 'remember', 'title': title, 'body': body if isinstance(body, list) else [body], **kw}


def table(id, title, head, rows, **kw):
    return {'id': id, 'type': 'table', 'title': title, 'head': head, 'rows': rows, **kw}


def mnemonic(id, title, body, letters=None, **kw):
    c = {'id': id, 'type': 'mnemonic', 'title': title, 'body': body if isinstance(body, list) else [body], **kw}
    if letters:
        c['letters'] = [{'l': l, 'w': w, 'm': m} for l, w, m in letters]
    return c


def check(id, q, opts, ans, why, title='Quick check', **kw):
    if isinstance(opts, list):
        opts = {k: v for k, v in zip('ABCD', opts)}
    assert ans in opts, (id, ans)
    return {'id': id, 'type': 'check', 'title': title, 'q': q, 'options': opts, 'answer': ans, 'why': why, **kw}


def worked(id, title, problem, steps, answer, **kw):
    return {'id': id, 'type': 'worked', 'title': title, 'problem': problem, 'steps': [{'text': s} for s in steps], 'answer': answer, **kw}


def mcq(id, q, opts, ans, why, tip, similar=(), **kw):
    if isinstance(opts, list):
        opts = {k: v for k, v in zip('ABCDE', opts)}
    assert ans in opts, (id, ans)
    return {'id': id, 'type': 'mcq', 'q': q, 'options': opts, 'answer': ans, 'why': why if isinstance(why, list) else [why],
            'tip': tip, 'similar': [{'q': a, 'a': b} for a, b in similar], **kw}


def tf(id, q, ans, why, tip, similar=(), **kw):
    return {'id': id, 'type': 'tf', 'q': q, 'answer': bool(ans), 'why': why if isinstance(why, list) else [why], 'tip': tip,
            'similar': [{'q': a, 'a': b} for a, b in similar], **kw}


def short(id, q, ans, why, tip, similar=(), accept=(), **kw):
    q_ = {'id': id, 'type': 'short', 'q': q, 'answer': ans, 'why': why if isinstance(why, list) else [why], 'tip': tip,
          'similar': [{'q': a, 'a': b} for a, b in similar], **kw}
    if accept:
        q_['accept'] = list(accept)
    return q_


def fill(id, q, choices, ans, why, tip, similar=(), **kw):
    assert ans in choices, (id, ans)
    return {'id': id, 'type': 'fill', 'q': q, 'choices': choices, 'answer': ans, 'why': why if isinstance(why, list) else [why],
            'tip': tip, 'similar': [{'q': a, 'a': b} for a, b in similar], **kw}
