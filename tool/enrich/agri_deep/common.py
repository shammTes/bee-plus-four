"""Card / question helpers for the Agriculture deep expansion (schema: assets/high/notes/notes_schema.json). Copied from
math_deep/common.py with the marker "-ad-" (diagram keys "ad_") instead of "-md-".
Ids: every card, question and diagram this tool adds carries "-ad-" (diagram keys "ad_"), so build.py can remove what an
earlier run added and re-insert it. A card dict that reuses an existing id replaces that card in place.
    set_unit('math10-u1');  T('rel-1', 'title', 3, 'para', 'para')   -> id math10-u1-ad-rel-1
    T('=math10-u1-c01', ...)                                           -> replaces the existing card math10-u1-c01
"""
CTX = {'u': None}


def set_unit(u):
    CTX['u'] = u


def _id(i):
    return i[1:] if i.startswith('=') else f"{CTX['u']}-ad-{i}"


def _c(i, typ, title, page, **kw):
    c = {'id': _id(i), 'type': typ, 'title': title, 'page': page, 'src': 'notes'}
    c.update({k: v for k, v in kw.items() if v is not None})
    return c


def T(i, title, page, *body):
    """explanation (text) card: one paragraph per argument; '**bold**', $maths$, '- ' bullets are rendered"""
    return _c(i, 'text', title, page, body=list(body))


def RM(i, title, page, *body):
    """'remember' card (key rule box)"""
    return _c(i, 'remember', title, page, body=list(body))


def MN(i, title, page, *body):
    """tip / trick card"""
    return _c(i, 'mnemonic', title, page, body=list(body))


def TB(i, title, page, head, rows, *body, layout=None):
    """table card; layout (optional): 'cards' | 'compare' | 'stack' | 'terms' | 'grid' (see ntable.dart) for narrow phones"""
    return _c(i, 'table', title, page, head=head, rows=rows, body=list(body) or None, layout=layout)


def DG(i, title, page, diagram, *body):
    """figure card: diagram = unit diagram key (see DIAGRAMS in the unit module)"""
    return _c(i, 'diagram', title, page, diagram='ad_' + diagram, mode='plain', body=list(body) or None)


def ST(i, title, page, diagram, steps, *body):
    """step-through figure: steps = [(text, show-key or None)], the SVG marks parts with data-hl / data-s"""
    return _c(i, 'steps', title, page, diagram='ad_' + diagram,
              steps=[{'text': t, 'show': s} if s else {'text': t} for t, s in steps], body=list(body) or None)


def GR(i, title, page, graph, *body, steps=None):
    """native graph card (kind plane / numberline, see GraphSpec in notes_models.dart)"""
    return _c(i, 'graph', title, page, graph=graph, body=list(body) or None,
              steps=[{'text': t, 'show': s} if s else {'text': t} for t, s in steps] if steps else None)


def WK(i, title, page, problem, steps, answer, diagram=None, graph=None, mode='show', body=None):
    """worked example: steps = list of strings (one numbered step each)"""
    return _c(i, 'worked', title, page, mode=mode, problem=problem, diagram=('ad_' + diagram) if diagram else None,
              graph=graph, steps=[{'text': s} for s in steps], answer=answer, body=body)


def CK(i, page, q, opts, ans, why, title='Quick check'):
    return _c(i, 'check', title, page, q=q, options=dict(zip('ABCDE', opts)), answer=ans, why=why)


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
    """Unit-exercise questions for one section: qs = QSet('1.1 Practice — relations and functions', 's11').
    Each question: step-by-step answer (why = list of steps), a tip, and at least one similar question with its answer."""

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
        ans = ans if isinstance(ans, bool) else str(ans).strip().lower() == 'true'  # schema: tf answer is a bool
        self.items.append(Q(self._i(), 'tf', page, q, ans, why, tip, sim, label=self.label))


def plane(xmin, xmax, ymin, ymax, points=(), lines=(), polygons=(), grid=True):
    """GraphSpec dict for a native 'plane' graph card"""
    g = {'kind': 'plane', 'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax, 'grid': grid}
    if points:
        g['points'] = list(points)
    if lines:
        g['lines'] = list(lines)
    if polygons:
        g['polygons'] = list(polygons)
    return g


def numberline(mn, mx, step=1, points=(), ranges=(), jumps=(), every=1):
    g = {'kind': 'numberline', 'min': mn, 'max': mx, 'step': step, 'label_every': every}
    if points:
        g['points'] = list(points)
    if ranges:
        g['ranges'] = list(ranges)
    if jumps:
        g['jumps'] = list(jumps)
    return g
