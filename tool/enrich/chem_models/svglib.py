"""Tiny SVG helpers for the chemistry model diagrams (hand-written vector, a few KB each, rendered by flutter_svg).

Only plain shapes and text are used (no CSS, no <marker>, no filters) so the files render the same on every phone.
data-s="k1 k2" shows an element only on those steps/states; data-hl="k" dims it (opacity .28) on other steps.
"""
import math

F = 'font-family="sans-serif"'
INK = '#1b2b25'
GLASS = '#55665f'
WATER = '#cfe8f5'
WATER2 = '#9fd0ec'
MUD = '#a9824f'
OIL = '#f3d36b'
RED = '#c0392b'
BLUE = '#2f6fa5'
GREEN = '#2f6f4e'
ORANGE = '#e67e22'


def r(v):
    v = round(v, 1)
    return str(int(v)) if v == int(v) else str(v)


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" {F}>\n{body}\n</svg>\n'


def attrs(**kw):
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        out.append(f' {k.rstrip("_").replace("_", "-")}="{v}"')
    return ''.join(out)


def g(body, s=None, hl=None, **kw):
    a = (f' data-s="{s}"' if s else '') + (f' data-hl="{hl}"' if hl else '') + attrs(**kw)
    if isinstance(body, (list, tuple)):
        body = '\n'.join(body)
    return f'<g{a}>{body}</g>'


def t(x, y, s, size=11, anchor='middle', weight='normal', fill=INK, extra=''):
    w = f' font-weight="{weight}"' if weight != 'normal' else ''
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{r(x)}" y="{r(y)}"{a} font-size="{size}"{w} fill="{fill}"{extra}>{s}</text>'


def rect(x, y, w, h, fill='none', stroke=None, sw=1.5, rx=0, extra=''):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    rr = f' rx="{rx}"' if rx else ''
    return f'<rect x="{r(x)}" y="{r(y)}" width="{r(w)}" height="{r(h)}"{rr} fill="{fill}"{st}{extra}/>'


def line(x1, y1, x2, y2, c=GLASS, w=1.5, dash=None, extra=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{r(x1)}" y1="{r(y1)}" x2="{r(x2)}" y2="{r(y2)}" stroke="{c}" stroke-width="{w}"{d}{extra}/>'


def path(d, stroke=GLASS, fill='none', w=1.6, dash=None, extra=''):
    st = f' stroke="{stroke}" stroke-width="{w}"' if stroke else ''
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="{fill}"{st}{da}{extra}/>'


def circ(x, y, rad, fill, stroke=None, sw=1, extra=''):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<circle cx="{r(x)}" cy="{r(y)}" r="{r(rad)}" fill="{fill}"{st}{extra}/>'


def poly(pts, fill, stroke=None, sw=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<polygon points="{" ".join(f"{r(x)},{r(y)}" for x, y in pts)}" fill="{fill}"{st}/>'


def arrow(x1, y1, x2, y2, c=INK, w=1.6, head=7, dash=None, both=False):
    """a straight arrow with a filled triangular head (no <marker>)"""
    a = math.atan2(y2 - y1, x2 - x1)
    out = []

    def tip(xe, ye, ang):
        p1 = (xe - head * math.cos(ang - 0.42), ye - head * math.sin(ang - 0.42))
        p2 = (xe - head * math.cos(ang + 0.42), ye - head * math.sin(ang + 0.42))
        return poly([(xe, ye), p1, p2], c)
    sx, sy = x1, y1
    ex, ey = x2 - (head * 0.7) * math.cos(a), y2 - (head * 0.7) * math.sin(a)
    if both:
        sx, sy = x1 + (head * 0.7) * math.cos(a), y1 + (head * 0.7) * math.sin(a)
    out.append(line(sx, sy, ex, ey, c, w, dash))
    out.append(tip(x2, y2, a))
    if both:
        out.append(tip(x1, y1, a + math.pi))
    return ''.join(out)


def beaker(x, y, w, h, c=GLASS):
    """open beaker outline with a small lip"""
    return path(f'M{r(x - 4)} {r(y)} L{r(x)} {r(y + 4)} L{r(x)} {r(y + h)} L{r(x + w)} {r(y + h)} L{r(x + w)} {r(y + 4)} L{r(x + w + 4)} {r(y)}', c, w=2)


def dots(pts, rad, fill):
    return ''.join(circ(x, y, rad, fill) for x, y in pts)


def flame(cx, by, h=26):
    return (path(f'M{r(cx - 9)} {r(by)} Q{r(cx - 12)} {r(by - h * .55)} {r(cx)} {r(by - h)} Q{r(cx + 12)} {r(by - h * .55)} {r(cx + 9)} {r(by)} Z', None, ORANGE)
            + path(f'M{r(cx - 4)} {r(by)} Q{r(cx - 6)} {r(by - h * .35)} {r(cx)} {r(by - h * .6)} Q{r(cx + 6)} {r(by - h * .35)} {r(cx + 4)} {r(by)} Z', None, '#f9e076'))


def burner(cx, by):
    """small burner body under a flame whose base is at by"""
    return rect(cx - 6, by, 12, 18, '#8a9a94') + rect(cx - 14, by + 18, 28, 5, '#6f7d78', rx=2)


def tripod(cx, top, w=60, h=40):
    return (line(cx - w / 2, top, cx + w / 2, top, '#6f7d78', 3) + line(cx - w / 2 + 6, top, cx - w / 2 - 4, top + h, '#6f7d78', 2.5)
            + line(cx + w / 2 - 6, top, cx + w / 2 + 4, top + h, '#6f7d78', 2.5))


def label(x, y, s, tx, ty, size=10, anchor='start', fill=INK, c='#7a8a84'):
    """text at (tx, ty) with a thin leader line to the point (x, y)"""
    return line(x, y, tx + (-3 if anchor == 'start' else 3 if anchor == 'end' else 0), ty - 4, c, 1) + t(tx, ty, s, size, anchor, fill=fill)
