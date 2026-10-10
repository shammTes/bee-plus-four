r"""Chemical equations as TeX for the app's maths renderer (flutter_math_fork has no \ce, so we build it).

    ce('2H2(g) + O2(g) -> 2H2O(l)')          ->  2\mathrm{H_2(g)} + \mathrm{O_2(g)} \rightarrow 2\mathrm{H_2O(l)}
    ce('Cu^2+(aq) + 2e^- -> Cu(s)')
    ce('2SO2(g) + O2(g) <=> 2SO3(g)')
    ce('CaCO3(s) ->{heat} CaO(s) + CO2(g)')  ->  \xrightarrow{\text{heat}}
    ce('CuSO4.5H2O(s) -> ...')               ->  hydrate dot
Display form: eq(...) wraps it in $$ $$.
"""
import re

ARROWS = {'->': r'\rightarrow', '<=>': r'\rightleftharpoons', '=>': r'\rightarrow'}


def species(sp):
    sp = sp.strip()
    m = re.match(r'^(\d+(?:/\d+)?|½)?\s*(.*)$', sp)
    coef, body = m.group(1) or '', m.group(2)
    if coef == '½' or coef == '1/2':
        coef = r'\tfrac{1}{2}'
    elif '/' in coef:
        a, b = coef.split('/')
        coef = rf'\tfrac{{{a}}}{{{b}}}'
    if re.fullmatch(r'[a-z][a-z ]*', body):  # a word such as energy / heat
        return coef + rf'\text{{{body}}}'
    state = ''
    sm = re.search(r'\((s|l|g|aq)\)$', body)
    if sm:
        state, body = sm.group(0), body[:sm.start()]
    charge = ''
    cm = re.search(r'\^(\d*[+-])$', body)
    if cm:
        charge, body = cm.group(1), body[:cm.start()]
    parts = body.split('.')
    out = []
    for i, p in enumerate(parts):
        lead = ''
        if i > 0:
            lm = re.match(r'^(\d+)', p)
            if lm:
                lead, p = lm.group(1), p[lm.end():]
        p = re.sub(r'(?<=[A-Za-z\)\]])(\d+)', r'_{\1}', p)
        out.append(lead + p)
    tex = r'\cdot '.join(out)
    if charge:
        tex += '^{' + charge + '}'
    return coef + r'\mathrm{' + tex + state + '}'


def cond(c):
    '''arrow condition: "V2O5, 450 °C" -> formula parts as chemistry, words as text, °C as a degree sign'''
    parts = []
    for p in [x.strip() for x in c.split(',')]:
        if re.fullmatch(r'(?:[A-Z][a-z]?\d*)+', p) and any(ch.isdigit() for ch in p):
            parts.append(species(p))
        else:
            m = re.fullmatch(r'(.*?)\s*°C', p)
            if m:
                parts.append((r'\text{' + m.group(1) + '}' if m.group(1) else '') + r'{}^{\circ}\text{C}')
            else:
                parts.append(r'\text{' + p + '}')
    return r',\ '.join(parts)


def ce(s):
    toks = re.split(r'\s+(->\{[^}]*\}|<=>\{[^}]*\}|<=>|->|=>|\+)\s+', s.strip())
    out = []
    for tk in toks:
        if tk == '+':
            out.append('+')
        elif tk in ARROWS:
            out.append(ARROWS[tk])
        elif tk.startswith('->{'):
            out.append(r'\xrightarrow{' + cond(tk[3:-1]) + '}')
        elif tk.startswith('<=>{'):
            out.append(r'\overset{' + cond(tk[4:-1]) + r'}{\rightleftharpoons}')
        else:
            out.append(species(tk))
    return ' '.join(out)


def eq(s, extra=''):
    return '$$' + ce(s) + (r' \qquad ' + extra if extra else '') + '$$'


def ie(s):
    """inline"""
    return r'\(' + ce(s) + r'\)'
