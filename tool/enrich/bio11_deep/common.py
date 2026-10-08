"""Card / question helpers for the Grade 11 Biology deep expansion (same schema as tool/enrich/bio9_u2/common.py).

Every helper takes the unit prefix through the module-level CTX so the content files read like the bio9 rebuild:
    set_unit('bio11-u1');  T('s111-c1', 'title', 3, 'para', 'para')
"""
CTX = {'u': None}


def set_unit(u):
    CTX['u'] = u


def _id(i):
    return f"{CTX['u']}-{i}"


def T(i, title, page, *body):
    return {'id': _id(i), 'type': 'text', 'title': title, 'page': page, 'src': 'notes', 'body': list(body)}


def RM(i, title, page, *body):
    return {'id': _id(i), 'type': 'remember', 'title': title, 'page': page, 'src': 'notes', 'body': list(body)}


def MN(i, title, page, body, letters=None):
    c = {'id': _id(i), 'type': 'mnemonic', 'title': title, 'page': page, 'src': 'notes', 'body': body if isinstance(body, list) else [body]}
    if letters:
        c['letters'] = [{'l': l, 'w': w, 'm': m} for l, w, m in letters]
    return c


def TB(i, title, page, head, rows):
    """Table card. The app does not render a table body, so put explanations in a T/RM card next to it."""
    return {'id': _id(i), 'type': 'table', 'title': title, 'page': page, 'src': 'notes', 'head': head, 'rows': rows}


def DG(i, title, page, diagram, *body, mode='plain'):
    c = {'id': _id(i), 'type': 'diagram', 'title': title, 'page': page, 'src': 'notes', 'diagram': diagram, 'mode': mode}
    if body:
        c['body'] = list(body)
    return c


def ST(i, title, page, diagram, steps, *body):
    c = {'id': _id(i), 'type': 'steps', 'title': title, 'page': page, 'src': 'notes', 'diagram': diagram,
         'steps': [{'text': t, 'show': s} if s else {'text': t} for t, s in steps]}
    # the app does not render a steps card's body, so extra notes become a last step showing the whole diagram
    c['steps'] += [{'text': b} for b in body]
    return c


def CK(i, page, q, opts, ans, why, title='Quick check'):
    return {'id': _id(i), 'type': 'check', 'title': title, 'page': page, 'src': 'notes', 'q': q,
            'options': dict(zip('ABCDE', opts)), 'answer': ans, 'why': why}


def WK(i, title, page, problem, steps, answer, mode='try'):
    return {'id': _id(i), 'type': 'worked', 'title': title, 'page': page, 'src': 'notes', 'mode': mode,
            'problem': problem, 'steps': [{'text': s} for s in steps], 'answer': answer}


def Q(i, typ, page, q, answer, why, tip, similar, label=None, options=None, choices=None, accept=None):
    x = {'id': _id(i), 'type': typ, 'q': q}
    if options:
        x['options'] = dict(zip('ABCDE', options))
    if choices:
        x['choices'] = choices
    x['answer'] = answer
    if accept:
        x['accept'] = accept
    x['why'] = why
    x['tip'] = tip
    x['similar'] = [{'q': a, 'a': b} for a, b in similar]
    x['page'] = page
    x['src'] = 'notes'
    if label:
        x['label'] = label
    return x


class QSet:
    """Collects unit-exercise questions for one sub-unit: qs = QSet('1.1.1 Practice', 's111')."""

    def __init__(self, label, pre):
        self.label, self.pre, self.items, self.n = label, pre, [], 0

    def _i(self):
        self.n += 1
        return f'{self.pre}-q{self.n:02d}'

    def M(self, page, q, opts, ans, why, tip, sim):
        self.items.append(Q(self._i(), 'mcq', page, q, ans, why, tip, sim, label=self.label, options=opts))

    def S(self, page, q, ans, why, tip, sim, accept=None):
        self.items.append(Q(self._i(), 'short', page, q, ans, why, tip, sim, label=self.label, accept=accept))

    def F(self, page, q, ans, choices, why, tip, sim):
        self.items.append(Q(self._i(), 'fill', page, q, ans, why, tip, sim, label=self.label, choices=choices))

    def TF(self, page, q, ans, why, tip, sim):
        self.items.append(Q(self._i(), 'tf', page, q, ans, why, tip, sim, label=self.label))
