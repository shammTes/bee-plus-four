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


SHADE = '#F7C98B'


def venn2(f, x, y, w, h, shade=None, la='A', lb='B', lu='U', d=None, r=None, nums=None, cap=None, c1=BLUE, c2=RED, steps=None, size=13):
    """two-set Venn diagram in the box (x, y, w, h). shade: 'union' | 'inter' | 'A' | 'B' | 'AmB' | 'BmA' | 'notA' | 'notB' |
    'notU' (outside A and B) | None. nums = (only A, both, only B, outside) numbers written in the regions."""
    cx, cy = x + w / 2, y + h / 2 + (0 if not cap else -8)
    r = r or min(h * 0.36, w * 0.25)
    d = d if d is not None else r * 0.55
    hh = (r * r - d * d) ** 0.5
    T, Bt = (cx, cy - hh), (cx, cy + hh)
    ax, bx = cx - d, cx + d
    q = lambda p: f'{p[0]:.1f} {p[1]:.1f}'
    R = f'{r:.1f} {r:.1f}'
    circA = f'M{ax - r:.1f} {cy:.1f}a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0Z'
    circB = f'M{bx - r:.1f} {cy:.1f}a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0Z'
    union = f'M{q(T)}A{R} 0 1 0 {q(Bt)}A{R} 0 1 0 {q(T)}Z'
    rect = f'M{x} {y}h{w}v{h}h{-w}Z'
    paths = {'union': union, 'inter': f'M{q(T)}A{R} 0 0 1 {q(Bt)}A{R} 0 0 1 {q(T)}Z',
             'A': circA, 'B': circB, 'AmB': f'M{q(T)}A{R} 0 1 0 {q(Bt)}A{R} 0 0 1 {q(T)}Z',
             'BmA': f'M{q(T)}A{R} 0 1 1 {q(Bt)}A{R} 0 0 0 {q(T)}Z',
             'notA': rect + circA, 'notB': rect + circB, 'notU': rect + union}
    f.rect(x, y, w, h, INK, 1.6, 'none', 8)
    if shade:
        f.raw(f'<path d="{paths[shade]}" fill="{SHADE}" fill-rule="evenodd"/>')
    f.circle(ax, cy, r, c1, 2).circle(bx, cy, r, c2, 2)
    f.text(ax - r * 0.62, cy - r * 0.78, la, 13, c1).text(bx + r * 0.62, cy - r * 0.78, lb, 13, c2)
    f.text(x + 7, y + h - 7, lu, 12, GREY, 'start')
    if nums:
        pos = [(ax - r * 0.5, cy + 5, 'middle'), (cx, cy + 5, 'middle'), (bx + r * 0.5, cy + 5, 'middle'), (x + w - 10, y + h - 9, 'end')]
        for k, (v, (px, py, an)) in enumerate(zip(nums, pos)):
            if v is None:
                continue
            if steps:
                f.g(steps[k])
            for j, line in enumerate(str(v).split('\n')):
                f.text(px, py + (j - (str(v).count('\n')) / 2) * (size + 2), line, size, INK, an)
            if steps:
                f.end()
    if cap:
        f.text(cx, y + h + 16, cap, 12.5, INK)
    return f


def halfplane(p, a, b, c, fill=SHADE, op=0.6):
    """shade the part of Plot p's window where a*x + b*y + c >= 0 (Sutherland-Hodgman clip of the window rectangle)"""
    win = [(p.xmin, p.ymin), (p.xmax, p.ymin), (p.xmax, p.ymax), (p.xmin, p.ymax)]
    v = lambda q: a * q[0] + b * q[1] + c
    out = []
    for i, q in enumerate(win):
        r = win[(i + 1) % 4]
        if v(q) >= 0:
            out.append(q)
        if (v(q) >= 0) != (v(r) >= 0):
            t = v(q) / (v(q) - v(r))
            out.append((q[0] + t * (r[0] - q[0]), q[1] + t * (r[1] - q[1])))
    if len(out) >= 3:
        p.poly([p.P(*q) for q in out], None, 0, fill, op=op)
    return p


def with_legend(p, items, size=12.5, gap=14):
    """wrap a Fig/Plot and add a row of coloured legend texts underneath: items = [(text, colour), ...]"""
    f = Fig(p.w, p.h + 20)
    f.raw('<g>' + ''.join(p.p) + '</g>')
    widths = [len(t) * size * 0.55 + gap for t, _ in items]
    x = (p.w - sum(widths) + gap) / 2
    for (t, c), wd in zip(items, widths):
        f.text(x, p.h + 14, t, size, c, 'start')
        x += wd
    return f
