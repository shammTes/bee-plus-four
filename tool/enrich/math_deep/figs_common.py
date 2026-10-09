"""Reusable figure builders shared by several units (arrow diagrams, function machine, line tests, Venn diagrams)."""
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL, AXIS


def arrow_diagram(pairs, left, right, ltitle='Domain', rtitle='Range', w=None, c=BLUE, x0=0, hl=None, fig=None, title=None, rsup=None):
    """two ovals with elements and arrows for each (a, b) in pairs; hl = set of left elements whose arrows are red"""
    rows = max(len(left), len(right))
    h = 64 + rows * 30
    w = w or x0 + 170
    f = fig or Fig(w, h + (18 if title else 0))
    top = 22 + (18 if title else 0)
    if title:
        f.text(x0 + 85, 15, title, 13)
    lx, rx = x0 + 32, x0 + 138
    oh = rows * 30 + 18
    f.ellipse(lx, top + 18 + oh / 2, 28, oh / 2 + 4, c, 1.8, FILL.get(c, '#fff'))
    f.ellipse(rx, top + 18 + oh / 2, 28, oh / 2 + 4, GREEN, 1.8, FILL[GREEN])
    f.text(lx, top + 4, ltitle, 12, c)
    if rsup:
        f.sup(rx, top + 4, rtitle, rsup[0], rsup[1], 12, GREEN)
    else:
        f.text(rx, top + 4, rtitle, 12, GREEN)

    def ly(i, k):
        return top + 18 + oh / 2 + (i - (k - 1) / 2) * 30

    pos_l = {v: ly(i, len(left)) for i, v in enumerate(left)}
    pos_r = {v: ly(i, len(right)) for i, v in enumerate(right)}
    for v, y in pos_l.items():
        f.label(lx, y, str(v), size=13)
    for v, y in pos_r.items():
        f.label(rx, y, str(v), size=13)
    for a, b in pairs:
        col = RED if hl and a in hl else INK
        f.arrow(lx + 15, pos_l[a], rx - 16, pos_r[b], col, 1.7, 8)
    return f


def machine(inp='x', rule='subtract from 4, take √', out='f(x)', w=320, h=130):
    f = Fig(w, h)
    f.rect(105, 22, 110, 62, BLUE, 2.2, FILL[BLUE], 10)
    f.text(160, 50, 'f', 20, BLUE, italic=True)
    f.text(160, 72, 'machine', 11, BLUE, bold=False)
    f.arrow(18, 53, 101, 53, INK, 2.2)
    f.arrow(219, 53, 302, 53, INK, 2.2)
    f.text(58, 44, 'input ' + inp, 12.5, INK)
    f.text(262, 44, 'output', 12.5, INK)
    f.text(58, 72, 'from the domain', 10, GREY, bold=False)
    f.text(262, 72, 'in the range', 10, GREY, bold=False)
    f.text(160, 108, rule, 12, INK)
    f.text(160, 125, out, 12, BLUE)
    return f


def side_by_side(figs, gap=10, labels=None):
    """put several Fig objects next to each other in one SVG (each keeps its own coordinates via a translate group)"""
    w = sum(f.w for f in figs) + gap * (len(figs) - 1)
    h = max(f.h for f in figs) + (20 if labels else 0)
    out = Fig(w, h)
    x = 0
    for i, f in enumerate(figs):
        out.raw(f'<g transform="translate({x:.1f},{20 if labels else 0})">' + ''.join(f.p) + '</g>')
        if labels:
            out.text(x + f.w / 2, 14, labels[i], 11.5, labels_color(labels[i]))
        x += f.w + gap
    return out


def labels_color(s):
    s = s.lower()
    if 'not' in s or '✗' in s or 'fails' in s:
        return RED
    if 'function' in s or 'yes' in s or 'passes' in s or 'one-to-one' in s:
        return GREEN
    return INK
