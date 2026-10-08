"""Card helpers (same schema and style as tool/enrich/bio9_u2/common.py). Every id made here is <unit>-cm-<x>, so the build
can remove and re-insert this tool's cards without touching anything else in the unit."""


class Unit:
    def __init__(self, uid):
        self.U = uid
        self.qs = []

    def id(self, i):
        return f'{self.U}-cm-{i}'

    def T(self, i, title, page, *body):
        return {'id': self.id(i), 'type': 'text', 'title': title, 'page': page, 'src': 'notes', 'body': list(body)}

    def RM(self, i, title, page, *body):
        return {'id': self.id(i), 'type': 'remember', 'title': title, 'page': page, 'src': 'notes', 'body': list(body)}

    def MN(self, i, title, page, body, letters=None):
        c = {'id': self.id(i), 'type': 'mnemonic', 'title': title, 'page': page, 'src': 'notes', 'body': body if isinstance(body, list) else [body]}
        if letters:
            c['letters'] = [{'l': a, 'w': b, 'm': m} for a, b, m in letters]
        return c

    def TB(self, i, title, page, head, rows, *body):
        c = {'id': self.id(i), 'type': 'table', 'title': title, 'page': page, 'src': 'notes', 'head': head, 'rows': rows}
        if body:
            c['body'] = list(body)
        return c

    def DG(self, i, title, page, diagram, *body):
        c = {'id': self.id(i), 'type': 'diagram', 'title': title, 'page': page, 'src': 'notes', 'diagram': diagram, 'mode': 'plain'}
        if body:
            c['body'] = list(body)
        return c

    def ST(self, i, title, page, diagram, steps, *body):
        """steps card: each step highlights (data-hl) or shows (data-s) part of the diagram"""
        c = {'id': self.id(i), 'type': 'steps', 'title': title, 'page': page, 'src': 'notes', 'diagram': diagram,
             'steps': [{'text': x, 'show': k} if k else {'text': x} for x, k in steps]}
        if body:
            c['body'] = list(body)
        return c

    def SS(self, i, title, page, diagram, states, *body):
        """states card: a slider through the diagram's data-s states (a cheap, offline 'animation')"""
        c = {'id': self.id(i), 'type': 'states', 'title': title, 'page': page, 'src': 'notes', 'diagram': diagram,
             'states': [{'key': k, 'label': lab, 'text': x} for k, lab, x in states]}
        if body:
            c['body'] = list(body)
        return c

    def CK(self, i, page, q, opts, ans, why, title='Quick check'):
        return {'id': self.id(i), 'type': 'check', 'title': title, 'page': page, 'src': 'notes', 'q': q,
                'options': dict(zip('ABCDE', opts)), 'answer': ans, 'why': why}

    def WK(self, i, title, page, problem, steps, answer, mode='try'):
        assert 2 <= len(steps) <= 10, (i, len(steps))
        return {'id': self.id(i), 'type': 'worked', 'title': title, 'page': page, 'src': 'notes', 'mode': mode,
                'problem': problem, 'steps': [{'text': s} for s in steps], 'answer': answer}

    # ---- unit exercise questions (label = practice section shown in the Exercise list)
    def _q(self, i, typ, label, page, q, answer, why, tip, similar, options=None, choices=None, accept=None):
        x = {'id': self.id(i), 'type': typ, 'q': q}
        if options:
            x['options'] = dict(zip('ABCDE', options))
        if choices:
            x['choices'] = choices
        x['answer'] = answer
        if accept:
            x['accept'] = accept
        x['why'] = why if isinstance(why, list) else [why]
        x['tip'] = tip
        x['similar'] = [{'q': a, 'a': b} for a, b in similar]
        x['page'] = page
        x['src'] = 'notes'
        x['label'] = label
        self.qs.append(x)
        return x

    def M(self, i, label, page, q, opts, ans, why, tip, sim):
        return self._q(i, 'mcq', label, page, q, ans, why, tip, sim, options=opts)

    def S(self, i, label, page, q, ans, why, tip, sim, accept=None):
        return self._q(i, 'short', label, page, q, ans, why, tip, sim, accept=accept)

    def F(self, i, label, page, q, ans, choices, why, tip, sim):
        return self._q(i, 'fill', label, page, q, ans, why, tip, sim, choices=choices)

    def TF(self, i, label, page, q, ans, why, tip, sim):
        return self._q(i, 'tf', label, page, q, ans, why, tip, sim)
