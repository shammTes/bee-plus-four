"""Tiny SVG builder for the Mathematics tutor figures (flutter_svg-safe: no markers, no CSS, no filters, no <use>).

Two canvases:
    Fig(w, h)                       plain pixel canvas (geometry figures, solids, Venn / arrow diagrams)
    Plot(xmin, xmax, ymin, ymax)    coordinate plane with grid, axes, tick labels; .X(x) / .Y(y) map maths -> pixels
Every drawing helper returns self so calls can be chained. str(fig) is the SVG text (numbers rounded to 0.1 px).
Colours follow lib/high/notes/jr/notes/graph_svg.dart so the figures match the app's own graph cards.
"""
import math

INK, GRID, AXIS = '#3E3129', '#E6DACB', '#6A5B50'
BLUE, RED, GREEN, PURPLE, ORANGE, GREY = '#2F5F8F', '#C24E32', '#2A7A6B', '#6A4C9C', '#B86E12', '#8A7F76'
FILL = {BLUE: '#E3EDF7', RED: '#FBE6E0', GREEN: '#DFF1EC', PURPLE: '#ECE6F5', ORANGE: '#FCEFD9', GREY: '#F1EEEA', INK: '#F1EEEA'}
FONT = 'HighNunito'


def n(v):
    r = round(v, 1)
    return str(int(r)) if r == int(r) else str(r)


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def num(v):
    """axis / label number: 2, 0.5, −3 (true minus sign)"""
    r = round(v, 3)
    s = str(int(r)) if r == int(r) else ('%g' % r)
    return s.replace('-', '\u2212')


class Fig:
    def __init__(self, w=320, h=220):
        self.w, self.h, self.p = w, h, []

    # ---- primitives
    def raw(self, s):
        self.p.append(s)
        return self

    def line(self, x1, y1, x2, y2, c=INK, w=2, dash=False, op=None, cap=True):
        d = ' stroke-dasharray="6 4"' if dash is True else (f' stroke-dasharray="{dash}"' if dash else '')
        o = f' opacity="{op}"' if op else ''
        lc = ' stroke-linecap="round"' if cap else ''
        return self.raw(f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" stroke="{c}" stroke-width="{w}"{d}{o}{lc}/>')

    def path(self, d, c=INK, w=2, fill='none', dash=False, op=None):
        ds = ' stroke-dasharray="6 4"' if dash is True else (f' stroke-dasharray="{dash}"' if dash else '')
        o = f' opacity="{op}"' if op else ''
        st = f' stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"' if c else ''
        return self.raw(f'<path d="{d}" fill="{fill}"{st}{ds}{o}/>')

    def poly(self, pts, c=INK, w=2, fill='none', closed=True, dash=False, op=None):
        d = 'M' + ' L'.join(f'{n(x)} {n(y)}' for x, y in pts) + (' Z' if closed else '')
        return self.path(d, c, w, fill, dash, op)

    def rect(self, x, y, w, h, c=INK, sw=2, fill='none', rx=0, dash=False):
        ds = ' stroke-dasharray="6 4"' if dash else ''
        r = f' rx="{rx}"' if rx else ''
        st = f' stroke="{c}" stroke-width="{sw}"' if c else ''
        return self.raw(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"{r} fill="{fill}"{st}{ds}/>')

    def circle(self, cx, cy, r, c=INK, w=2, fill='none', dash=False, op=None):
        ds = ' stroke-dasharray="6 4"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        st = f' stroke="{c}" stroke-width="{w}"' if c else ''
        return self.raw(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"{st}{ds}{o}/>')

    def ellipse(self, cx, cy, rx, ry, c=INK, w=2, fill='none', dash=False):
        ds = ' stroke-dasharray="6 4"' if dash else ''
        return self.raw(f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" fill="{fill}" stroke="{c}" stroke-width="{w}"{ds}/>')

    def dot(self, x, y, c=RED, r=3.6, open_=False):
        return self.circle(x, y, r, c, 2, '#ffffff' if open_ else c)

    def text(self, x, y, s, size=13, c=INK, anchor='middle', bold=True, italic=False):
        wt = ' font-weight="800"' if bold else ' font-weight="600"'
        it = ' font-style="italic"' if italic else ''
        an = '' if anchor == 'start' else f' text-anchor="{anchor}"'
        return self.raw(f'<text x="{n(x)}" y="{n(y)}" font-size="{size}"{an} fill="{c}"{wt}{it}>{esc(s)}</text>')

    def sup(self, x, y, base, sup, rest='', size=13, c=INK, anchor='middle', italic=False):
        """text with a superscript, e.g. sup(x, y, 'f', '−1', '(x)') -> f⁻¹(x) without needing the ⁻ glyph"""
        cw = size * 0.56
        wt = cw * len(base) + cw * 0.72 * len(sup) + cw * len(rest)
        x0 = x - wt / 2 if anchor == 'middle' else (x - wt if anchor == 'end' else x)
        self.text(x0, y, base, size, c, 'start', True, italic)
        x1 = x0 + cw * len(base)
        self.text(x1, y - size * 0.42, sup, size * 0.72, c, 'start', True)
        if rest:
            self.text(x1 + cw * 0.72 * len(sup) + 1, y, rest, size, c, 'start', True, italic)
        return self

    def label(self, x, y, s, dx=0, dy=0, size=13, c=INK, bold=True, italic=False):
        """text centred at (x+dx, y+dy) with the baseline nudged so the centre is at that point"""
        return self.text(x + dx, y + dy + size * 0.35, s, size, c, 'middle', bold, italic)

    def ptlabel(self, x, y, s, pos='ne', c=INK, size=13, gap=9, italic=False):
        """label a point; pos = n s e w ne nw se sw"""
        dx = (gap if 'e' in pos else -gap if 'w' in pos else 0)
        dy = (-gap if 'n' in pos else gap if 's' in pos else 0)
        anchor = 'start' if 'e' in pos else 'end' if 'w' in pos else 'middle'
        return self.text(x + dx, y + dy + size * 0.35, s, size, c, anchor, True, italic)

    def arrow(self, x1, y1, x2, y2, c=INK, w=2, head=9, dash=False, both=False):
        self.line(x1, y1, x2, y2, c, w, dash)
        self._head(x1, y1, x2, y2, c, head)
        if both:
            self._head(x2, y2, x1, y1, c, head)
        return self

    def _head(self, x1, y1, x2, y2, c, head):
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - head * math.cos(a - 0.4), y2 - head * math.sin(a - 0.4))
        p2 = (x2 - head * math.cos(a + 0.4), y2 - head * math.sin(a + 0.4))
        return self.poly([(x2, y2), p1, p2], c, 1, c)

    def curve_arrow(self, x1, y1, x2, y2, bend=30, c=INK, w=2, head=8):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        L = math.hypot(x2 - x1, y2 - y1) or 1
        cx, cy = mx - (y2 - y1) / L * bend, my + (x2 - x1) / L * bend
        self.path(f'M{n(x1)} {n(y1)} Q{n(cx)} {n(cy)} {n(x2)} {n(y2)}', c, w)
        return self._head(cx, cy, x2, y2, c, head)

    def arc(self, c, r, a0, a1, col=INK, w=1.6, dash=False, fill='none'):
        """circular arc centre c, radius r, from a0 to a1 degrees (anticlockwise, maths convention)"""
        p0, p1 = polar(c, r, a0), polar(c, r, a1)
        large = 1 if (a1 - a0) % 360 > 180 else 0
        return self.path(f'M{n(p0[0])} {n(p0[1])} A{n(r)} {n(r)} 0 {large} 0 {n(p1[0])} {n(p1[1])}', col, w, fill, dash)

    def g(self, s=None, hl=None):
        """open a group shown only in steps s (space separated keys) or highlighted for step hl; close with .end()"""
        a = (f' data-s="{s}"' if s else '') + (f' data-hl="{hl}"' if hl else '')
        return self.raw(f'<g{a}>')

    def end(self):
        return self.raw('</g>')

    # ---- geometry marks
    def angle(self, v, a, b, r=18, c=RED, lab=None, lr=None, w=1.8, fill=None, size=12):
        """arc for the angle at vertex v between rays v->a and v->b (the smaller one); optional label"""
        a1 = math.atan2(a[1] - v[1], a[0] - v[0])
        a2 = math.atan2(b[1] - v[1], b[0] - v[0])
        d = (a2 - a1) % (2 * math.pi)
        if d > math.pi:
            a1, a2 = a2, a1
            d = 2 * math.pi - d
        p1 = (v[0] + r * math.cos(a1), v[1] + r * math.sin(a1))
        p2 = (v[0] + r * math.cos(a1 + d), v[1] + r * math.sin(a1 + d))
        if fill:
            self.path(f'M{n(v[0])} {n(v[1])} L{n(p1[0])} {n(p1[1])} A{n(r)} {n(r)} 0 0 1 {n(p2[0])} {n(p2[1])} Z', None, 0, fill)
        self.path(f'M{n(p1[0])} {n(p1[1])} A{n(r)} {n(r)} 0 0 1 {n(p2[0])} {n(p2[1])}', c, w)
        if lab:
            m = a1 + d / 2
            rr = lr or r + 11
            self.label(v[0] + rr * math.cos(m), v[1] + rr * math.sin(m), lab, size=size, c=c)
        return self

    def right(self, v, a, b, s=10, c=INK):
        ua = _unit(v, a)
        ub = _unit(v, b)
        p1 = (v[0] + ua[0] * s, v[1] + ua[1] * s)
        p3 = (v[0] + ub[0] * s, v[1] + ub[1] * s)
        p2 = (p1[0] + ub[0] * s, p1[1] + ub[1] * s)
        return self.poly([p1, p2, p3], c, 1.5, 'none', closed=False)

    def ticks(self, a, b, k=1, c=INK, L=7, gap=4):
        """k equal-length tick marks across the middle of segment ab"""
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        u = _unit(a, b)
        nx, ny = -u[1], u[0]
        for i in range(k):
            o = (i - (k - 1) / 2) * gap
            cx, cy = mx + u[0] * o, my + u[1] * o
            self.line(cx - nx * L / 2, cy - ny * L / 2, cx + nx * L / 2, cy + ny * L / 2, c, 1.8)
        return self

    def par(self, a, b, k=1, c=INK, s=6):
        """k parallel-arrow marks (chevrons) in the middle of ab"""
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        u = _unit(a, b)
        nx, ny = -u[1], u[0]
        for i in range(k):
            o = (i - (k - 1) / 2) * 6
            tx, ty = mx + u[0] * (o + 3), my + u[1] * (o + 3)
            self.poly([(tx - u[0] * s + nx * s * 0.7, ty - u[1] * s + ny * s * 0.7), (tx, ty), (tx - u[0] * s - nx * s * 0.7, ty - u[1] * s - ny * s * 0.7)], c, 1.8, closed=False)
        return self

    def seglabel(self, a, b, s, off=12, c=INK, size=12, side=1):
        """label in the middle of ab, pushed off the segment (side=+1 / -1 picks the side)"""
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        u = _unit(a, b)
        return self.label(mx - u[1] * off * side, my + u[0] * off * side, s, size=size, c=c)

    def title(self, s, size=13):
        return self.text(self.w / 2, 16, s, size, INK)

    def __str__(self):
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(self.w)} {n(self.h)}" font-family="{FONT}">' + ''.join(self.p) + '</svg>\n'


def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    return dx / L, dy / L


def _clip(p, q, x0, x1, y0, y1):
    """Liang-Barsky: the part of segment pq inside the box, or None"""
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return None
            continue
        r = qq / pp
        if pp < 0:
            if r > t1:
                return None
            t0 = max(t0, r)
        else:
            if r < t0:
                return None
            t1 = min(t1, r)
    a = p if t0 == 0 else (p[0] + t0 * dx, p[1] + t0 * dy)
    b = q if t1 == 1 else (p[0] + t1 * dx, p[1] + t1 * dy)
    return a, b


def polar(c, r, deg):
    """point on a circle, degrees measured anticlockwise from east (screen y goes down)"""
    t = math.radians(deg)
    return (c[0] + r * math.cos(t), c[1] - r * math.sin(t))


def mid(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


class Plot(Fig):
    """coordinate plane: unit = pixels per unit (same on both axes unless uy given)"""

    def __init__(self, xmin, xmax, ymin, ymax, unit=None, uy=None, pad=18, grid=True, labels=True, every=1, gstep=1,
                 xlab='x', ylab='y', axes=True, yevery=None):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.ux = unit or min(300 / (xmax - xmin), 26)
        self.uy = uy or self.ux
        self.pad = pad
        super().__init__(pad * 2 + (xmax - xmin) * self.ux, pad * 2 + (ymax - ymin) * self.uy)
        if grid:
            g, d = gstep, []
            k = math.ceil(xmin / g) * g
            while k <= xmax + 1e-9:
                d.append(f'M{n(self.X(k))} {n(self.Y(ymin))}V{n(self.Y(ymax))}')
                k += g
            k = math.ceil(ymin / g) * g
            while k <= ymax + 1e-9:
                d.append(f'M{n(self.X(xmin))} {n(self.Y(k))}H{n(self.X(xmax))}')
                k += g
            self.raw(f'<path d="{"".join(d)}" stroke="{GRID}" stroke-width="1" fill="none"/>')
        if axes:
            if ymin <= 0 <= ymax:
                self.arrow(self.X(xmin) - 6, self.Y(0), self.X(xmax) + 10, self.Y(0), AXIS, 1.6, 7)
                self.text(self.X(xmax) + 6, self.Y(0) - 7, xlab, 13, AXIS, 'middle', True, True)
            if xmin <= 0 <= xmax:
                self.arrow(self.X(0), self.Y(ymin) + 6, self.X(0), self.Y(ymax) - 10, AXIS, 1.6, 7)
                self.text(self.X(0) + 11, self.Y(ymax) - 2, ylab, 13, AXIS, 'middle', True, True)
            if labels:
                ye = yevery or every
                tk = []
                k = math.ceil(xmin / every) * every
                while k <= xmax + 1e-9:
                    if abs(k) > 1e-9 and ymin <= 0 <= ymax:
                        tk.append(f'M{n(self.X(k))} {n(self.Y(0) - 3)}v6')
                        self.text(self.X(k), self.Y(0) + 14, num(k), 10.5, AXIS, 'middle', False)
                    k += every
                k = math.ceil(ymin / ye) * ye
                while k <= ymax + 1e-9:
                    if abs(k) > 1e-9 and xmin <= 0 <= xmax:
                        tk.append(f'M{n(self.X(0) - 3)} {n(self.Y(k))}h6')
                        self.text(self.X(0) - 5, self.Y(k) + 4, num(k), 10.5, AXIS, 'end', False)
                    k += ye
                if tk:
                    self.raw(f'<path d="{"".join(tk)}" stroke="{AXIS}" stroke-width="1.4" fill="none"/>')
                if xmin <= 0 <= xmax and ymin <= 0 <= ymax:
                    self.text(self.X(0) - 5, self.Y(0) + 13, '0', 10.5, AXIS, 'end', False)

    def X(self, x):
        return self.pad + (x - self.xmin) * self.ux

    def Y(self, y):
        return self.pad + (self.ymax - y) * self.uy

    def P(self, x, y):
        return (self.X(x), self.Y(y))

    def fn(self, f, a=None, b=None, c=BLUE, w=2.6, steps=110, dash=False, lab=None, labat=None, labpos='ne'):
        """graph y = f(x) on [a, b], clipped to the window; breaks where f is undefined or jumps (asymptotes)"""
        a = self.xmin if a is None else a
        b = self.xmax if b is None else b
        pts = []
        for i in range(steps + 1):
            x = a + (b - a) * i / steps
            try:
                y = f(x)
                if isinstance(y, complex) or y != y or abs(y) > 1e6:
                    y = None
            except (ValueError, ZeroDivisionError, OverflowError):
                y = None
            pts.append(None if y is None else (x, y))
        self.curve(pts, c, w, dash)
        if lab and labat is not None:
            self.ptlabel(self.X(labat), self.Y(f(labat)), lab, labpos, c)
        return self

    def param(self, fx, fy, t0, t1, c=BLUE, w=2.6, steps=110, dash=False):
        """parametric curve (x(t), y(t)), clipped to the window"""
        pts = []
        for i in range(steps + 1):
            t = t0 + (t1 - t0) * i / steps
            try:
                pts.append((fx(t), fy(t)))
            except (ValueError, ZeroDivisionError):
                pts.append(None)
        return self.curve(pts, c, w, dash)

    def curve(self, pts, c=BLUE, w=2.6, dash=False):
        """polyline in maths coordinates (None = gap), clipped to the window (Liang-Barsky per piece)"""
        runs, cur = [], []
        span = (self.ymax - self.ymin) * 3
        for p, q in zip(pts, pts[1:]):
            if p is None or q is None or abs(q[1] - p[1]) > span:
                if len(cur) > 1:
                    runs.append(cur)
                cur = []
                continue
            seg = _clip(p, q, self.xmin, self.xmax, self.ymin, self.ymax)
            if seg is None:
                if len(cur) > 1:
                    runs.append(cur)
                cur = []
                continue
            s0, s1 = seg
            if cur and (abs(cur[-1][0] - s0[0]) > 1e-9 or abs(cur[-1][1] - s0[1]) > 1e-9):
                if len(cur) > 1:
                    runs.append(cur)
                cur = []
            if not cur:
                cur = [s0]
            cur.append(s1)
            if s1 != q:
                runs.append(cur)
                cur = []
        if len(cur) > 1:
            runs.append(cur)
        for r in runs:
            self.path('M' + ' L'.join(f'{n(self.X(x))} {n(self.Y(y))}' for x, y in r), c, w, dash=dash)
        return self

    def clip(self):
        """wrap everything drawn so far after the axes in a clip to the plot window (call last)"""
        return self

    def seg(self, p, q, c=BLUE, w=2.4, dash=False):
        return self.line(self.X(p[0]), self.Y(p[1]), self.X(q[0]), self.Y(q[1]), c, w, dash)

    def fullline(self, m=None, b=0, x=None, c=BLUE, w=2.4, dash=False, lab=None, labx=None, labpos='ne'):
        """infinite line y = m x + b (or vertical x = const) clipped to the window"""
        if x is not None:
            self.line(self.X(x), self.Y(self.ymin), self.X(x), self.Y(self.ymax), c, w, dash)
            if lab:
                self.ptlabel(self.X(x), self.Y(self.ymax) + 8, lab, 'e', c)
            return self
        pts = []
        for xx in (self.xmin, self.xmax):
            pts.append((xx, m * xx + b))
        if m != 0:
            for yy in (self.ymin, self.ymax):
                pts.append(((yy - b) / m, yy))
        pts = [p for p in pts if self.xmin - 1e-9 <= p[0] <= self.xmax + 1e-9 and self.ymin - 1e-9 <= p[1] <= self.ymax + 1e-9]
        pts.sort()
        if len(pts) >= 2:
            self.seg(pts[0], pts[-1], c, w, dash)
        if lab:
            lx = labx if labx is not None else pts[-1][0] - 0.5
            self.ptlabel(self.X(lx), self.Y(m * lx + b), lab, labpos, c)
        return self

    def pt(self, x, y, lab=None, pos='ne', c=RED, open_=False, r=3.8, size=12):
        self.dot(self.X(x), self.Y(y), c, r, open_)
        if lab:
            self.ptlabel(self.X(x), self.Y(y), lab, pos, c, size)
        return self

    def ppoly(self, pts, c=BLUE, fill=None, w=2.4, closed=True, dash=False):
        return self.poly([self.P(*p) for p in pts], c, w, fill or 'none', closed, dash)
