"""Helpers for the Grade 9 Biology Unit 2 (Taxonomy) rebuild. Content lives in l*.py, assembly in build.py."""
U = 'bio9-u2'


def T(i, title, page, *body):
    return {'id': f'{U}-{i}', 'type': 'text', 'title': title, 'page': page, 'src': 'notes', 'body': list(body)}


def RM(i, title, page, *body):
    return {'id': f'{U}-{i}', 'type': 'remember', 'title': title, 'page': page, 'src': 'notes', 'body': list(body)}


def MN(i, title, page, body, letters=None):
    c = {'id': f'{U}-{i}', 'type': 'mnemonic', 'title': title, 'page': page, 'src': 'notes', 'body': body if isinstance(body, list) else [body]}
    if letters:
        c['letters'] = [{'l': l, 'w': w, 'm': m} for l, w, m in letters]
    return c


def TB(i, title, page, head, rows, *body):
    c = {'id': f'{U}-{i}', 'type': 'table', 'title': title, 'page': page, 'src': 'notes', 'head': head, 'rows': rows}
    if body:
        c['body'] = list(body)
    return c


def DG(i, title, page, diagram, mode='plain', *body):
    c = {'id': f'{U}-{i}', 'type': 'diagram', 'title': title, 'page': page, 'src': 'notes', 'diagram': diagram, 'mode': mode}
    if body:
        c['body'] = list(body)
    return c


def ST(i, title, page, diagram, steps, *body):
    c = {'id': f'{U}-{i}', 'type': 'steps', 'title': title, 'page': page, 'src': 'notes', 'diagram': diagram,
         'steps': [{'text': t, 'show': s} if s else {'text': t} for t, s in steps]}
    if body:
        c['body'] = list(body)
    return c


def CK(i, page, q, opts, ans, why, title='Quick check'):
    return {'id': f'{U}-{i}', 'type': 'check', 'title': title, 'page': page, 'src': 'notes', 'q': q,
            'options': dict(zip('ABCDE', opts)), 'answer': ans, 'why': why}


def WK(i, title, page, problem, steps, answer, mode='try'):
    return {'id': f'{U}-{i}', 'type': 'worked', 'title': title, 'page': page, 'src': 'notes', 'mode': mode,
            'problem': problem, 'steps': [{'text': s} for s in steps], 'answer': answer}


def L(n, number, title, pages, cards):
    return {'id': f'{U}-l{n}', 'number': number, 'title': title, 'pages': pages, 'cards': cards}


def Q(i, typ, page, q, answer, why, tip, similar, label=None, options=None, choices=None, accept=None):
    x = {'id': f'{U}-{i}', 'type': typ, 'q': q}
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
