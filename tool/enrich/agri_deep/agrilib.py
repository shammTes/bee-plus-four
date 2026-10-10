"""Figure helpers for the Agriculture tutor figures (on top of math_deep/svglib.py, flutter_svg-safe: no markers, CSS,
filters or <use>). Flow charts, cycles, labelled drawings and simple outlines of Eritrean crops, livestock and farm scenes.
People are drawn as simple figures with brown skin in Eritrean dress (white netsela / gabi, turban), in Eritrean settings."""
import math
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL, n, esc

BROWN, SOIL, SOIL2, SOIL3, LEAF, LEAF2, STRAW, SKY, WATER, ROCK = (
    '#7A4E2D', '#B98A5E', '#9C6B43', '#7D5233', '#4E8B3A', '#7DB25A', '#D9B65F', '#EAF3FA', '#5B9BD5', '#A39C93')
SKIN, CLOTH = '#7B4A2E', '#F7F4EE'


def wrap(s, w):
    """split text into lines of at most w characters (at spaces); '\n' forces a break"""
    out = []
    for part in str(s).split('\n'):
        line = ''
        for word in part.split(' '):
            if line and len(line) + 1 + len(word) > w:
                out.append(line)
                line = word
            else:
                line = (line + ' ' + word).strip()
        out.append(line)
    return out


def tlines(f, x, y, lines, size=12, c=INK, anchor='middle', bold=True, lh=None):
    """several lines of text centred vertically on y"""
    lh = lh or size * 1.22
    y0 = y - (len(lines) - 1) * lh / 2 + size * 0.35
    for i, s in enumerate(lines):
        f.text(x, y0 + i * lh, s, size, c, anchor, bold)
    return f


def box(f, x, y, w, h, text, c=BLUE, size=12, fill=None, rx=8, wchars=None, sw=1.8, tc=None, bold=True):
    """rounded box with wrapped, centred text"""
    f.rect(x, y, w, h, c, sw, fill or FILL.get(c, '#fff'), rx)
    wc = wchars or max(4, int((w - 8) / (size * 0.56)))
    return tlines(f, x + w / 2, y + h / 2, wrap(text, wc), size, tc or INK, 'middle', bold)


def leader(f, x, y, tx, ty, label, c=INK, size=11.5, anchor=None, dot=True, lc=GREY):
    """a label at (tx, ty) joined to the point (x, y) by a thin line"""
    f.line(x, y, tx, ty, lc, 1.2)
    if dot:
        f.circle(x, y, 2.2, None, 0, lc)
    an = anchor or ('start' if tx >= x else 'end')
    dx = 3 if an == 'start' else (-3 if an == 'end' else 0)
    lines = wrap(label, 40) if '\n' in label else [label]
    return tlines(f, tx + dx, ty, lines, size, c, an)


def flow(items, w=330, bw=None, bh=34, gap=16, x0=None, cols=(BLUE, GREEN, ORANGE, PURPLE, RED), size=12, title=None,
         steps=False, notes=None):
    """vertical flow chart; items = list of texts; steps=True puts each box in data-s 'k1..kn' groups (cumulative)"""
    bw = bw or w - 40
    top = 28 if title else 6
    f = Fig(w, top + len(items) * (bh + gap) - gap + 6)
    if title:
        f.title(title, 13)
    x = x0 if x0 is not None else (w - bw) / 2
    for i, t in enumerate(items):
        y = top + i * (bh + gap)
        if steps:
            f.g(' '.join(f'k{j}' for j in range(i + 1, len(items) + 1)))
        c = cols[i % len(cols)]
        box(f, x, y, bw, bh, t, c, size)
        if i:
            f.arrow(x + bw / 2, y - gap + 1, x + bw / 2, y - 2, INK, 1.8, 7)
        if notes and notes[i]:
            f.text(x + bw + 6, y + bh / 2 + 4, notes[i], 10.5, GREY, 'start', False)
        if steps:
            f.end()
    return f


def hflow(items, w=340, h=None, bh=46, size=11.5, cols=(BLUE, GREEN, ORANGE, PURPLE, RED), rows=1, gap=12, title=None,
          steps=False):
    """left-to-right flow wrapped over `rows` rows (snake order)"""
    per = math.ceil(len(items) / rows)
    bw = (w - 12 - gap * (per - 1)) / per
    top = 26 if title else 6
    h = h or top + rows * (bh + 22) - 16
    f = Fig(w, h)
    if title:
        f.title(title, 13)
    pos = []
    for i, t in enumerate(items):
        r, k = divmod(i, per)
        if r % 2:
            k = per - 1 - k
        x = 6 + k * (bw + gap)
        y = top + r * (bh + 22)
        pos.append((x, y))
        if steps:
            f.g(' '.join(f'k{j}' for j in range(i + 1, len(items) + 1)))
        box(f, x, y, bw, bh, t, cols[i % len(cols)], size)
        if i:
            px, py = pos[i - 1]
            if py == y:
                if px < x:
                    f.arrow(px + bw + 1, y + bh / 2, x - 1, y + bh / 2, INK, 1.7, 6)
                else:
                    f.arrow(px - 1, y + bh / 2, x + bw + 1, y + bh / 2, INK, 1.7, 6)
            else:
                f.arrow(px + bw / 2, py + bh + 1, x + bw / 2, y - 1, INK, 1.7, 6)
        if steps:
            f.end()
    return f


def cycle(items, w=330, h=300, r=None, bw=104, bh=40, size=11.5, cols=(GREEN, BLUE, ORANGE, PURPLE, RED, BROWN),
          centre=None, steps=False, start=90):
    """boxes round a circle joined by clockwise arrows; centre = text in the middle"""
    f = Fig(w, h)
    cx, cy = w / 2, h / 2
    r = r or min(w - bw, h - bh) / 2 - 4
    k = len(items)
    pts = []
    for i in range(k):
        a = math.radians(start - 360 * i / k)
        pts.append((cx + r * math.cos(a) * (w - bw) / (h - bh) * 0.98 if w > h else cx + r * math.cos(a), cy - r * math.sin(a)))
    for i in range(k):
        a0 = math.radians(start - 360 * i / k - 360 / k * 0.30)
        a1 = math.radians(start - 360 * (i + 1) / k + 360 / k * 0.30)
        rr = r * 0.80
        p0 = (cx + rr * math.cos(a0), cy - rr * math.sin(a0))
        p1 = (cx + rr * math.cos(a1), cy - rr * math.sin(a1))
        if steps:
            f.g(' '.join(f'k{j}' for j in range(i + 1, k + 1)) if i < k - 1 else f'k{k}')
        f.curve_arrow(p0[0], p0[1], p1[0], p1[1], -rr * 0.18, GREY, 2, 8)
        if steps:
            f.end()
    for i, (t, (x, y)) in enumerate(zip(items, pts)):
        if steps:
            f.g(' '.join(f'k{j}' for j in range(i + 1, k + 1)))
        box(f, x - bw / 2, y - bh / 2, bw, bh, t, cols[i % len(cols)], size)
        if steps:
            f.end()
    if centre:
        tlines(f, cx, cy, wrap(centre, 16), 12.5, INK)
    return f


def table_fig(head, rows, w=340, colw=None, rh=24, size=11, hc=GREEN):
    """small drawn table (used inside figures only when a picture needs a key)"""
    colw = colw or [w / len(head)] * len(head)
    f = Fig(w, (len(rows) + 1) * rh + 2)
    x = 0
    for j, h in enumerate(head):
        f.rect(x + 1, 1, colw[j] - 2, rh - 2, hc, 1.2, FILL[hc], 3)
        f.text(x + colw[j] / 2, rh / 2 + 4, h, size, INK)
        x += colw[j]
    for i, r in enumerate(rows):
        x = 0
        for j, v in enumerate(r):
            f.rect(x + 1, (i + 1) * rh + 1, colw[j] - 2, rh - 2, GREY, 0.8, '#fff', 2)
            f.text(x + colw[j] / 2, (i + 1) * rh + rh / 2 + 4, v, size, INK, 'middle', False)
            x += colw[j]
    return f


# ----------------------------------------------------------------- simple drawings
def ground(f, y, x0=0, x1=None, c=SOIL, h=None):
    x1 = f.w if x1 is None else x1
    f.rect(x0, y, x1 - x0, h or f.h - y, None, 0, c)
    return f.line(x0, y, x1, y, SOIL3, 1.6)


def grass_tufts(f, xs, y, c=LEAF, s=1):
    for x in xs:
        f.path(f'M{n(x - 5 * s)} {n(y)} Q{n(x - 4 * s)} {n(y - 8 * s)} {n(x - 7 * s)} {n(y - 12 * s)} M{n(x)} {n(y)} L{n(x)} {n(y - 13 * s)} M{n(x + 5 * s)} {n(y)} Q{n(x + 4 * s)} {n(y - 8 * s)} {n(x + 7 * s)} {n(y - 12 * s)}', c, 1.6)
    return f


def leaf(f, x, y, L, ang, c=LEAF, wd=0.32, vein=True):
    """leaf from (x, y), length L, angle ang (degrees, 0 = right, 90 = up)"""
    a = math.radians(ang)
    ux, uy = math.cos(a), -math.sin(a)
    px, py = -uy, ux
    tip = (x + ux * L, y + uy * L)
    c1 = (x + ux * L * 0.35 + px * L * wd, y + uy * L * 0.35 + py * L * wd)
    c2 = (x + ux * L * 0.35 - px * L * wd, y + uy * L * 0.35 - py * L * wd)
    f.path(f'M{n(x)} {n(y)} Q{n(c1[0])} {n(c1[1])} {n(tip[0])} {n(tip[1])} Q{n(c2[0])} {n(c2[1])} {n(x)} {n(y)}Z', '#3B6E2C', 1.1, c)
    if vein:
        f.line(x, y, tip[0] - ux * L * 0.12, tip[1] - uy * L * 0.12, '#2F5A24', 0.9)
    return f


def grass_leaf(f, x, y, L, ang, bend=0.25, c=LEAF, wd=3.2):
    """long narrow monocot leaf (curved strap)"""
    a = math.radians(ang)
    ux, uy = math.cos(a), -math.sin(a)
    px, py = -uy, ux
    tip = (x + ux * L + px * L * bend, y + uy * L + py * L * bend + L * 0.15)
    m = (x + ux * L * 0.55, y + uy * L * 0.55)
    f.path(f'M{n(x - px * wd)} {n(y - py * wd)} Q{n(m[0] - px * wd)} {n(m[1] - py * wd)} {n(tip[0])} {n(tip[1])} Q{n(m[0] + px * wd)} {n(m[1] + py * wd)} {n(x + px * wd)} {n(y + py * wd)}Z', '#3B6E2C', 1, c)
    return f


def sorghum(f, x, y, h=120, head=True, c=LEAF):
    """sorghum / maize-like cereal plant standing on (x, y)"""
    f.line(x, y, x, y - h, '#5E7F33', 3.2)
    for i, (k, s) in enumerate(((0.25, 1), (0.42, -1), (0.58, 1), (0.74, -1))):
        grass_leaf(f, x, y - h * k, h * 0.42, 90 - 62 * s, 0.18 * s, c)
    if head:
        f.ellipse(x, y - h - 10, 7, 13, '#7A3E1D', 1.2, '#B5652E')
        for j in range(5):
            f.circle(x - 4 + (j % 2) * 8, y - h - 18 + j * 4, 2, None, 0, '#8E4A22')
    return f


def roots_fibrous(f, x, y, L=34, c=BROWN):
    for a in (-70, -50, -30, -10, 10, 30, 50, 70):
        t = math.radians(a)
        ex, ey = x + math.sin(t) * L, y + math.cos(t) * L * (0.9 if abs(a) < 40 else 0.6)
        f.path(f'M{n(x)} {n(y)} Q{n(x + math.sin(t) * L * 0.4)} {n(y + L * 0.5)} {n(ex)} {n(ey)}', c, 1.3)
    return f


def roots_tap(f, x, y, L=50, c=BROWN):
    f.path(f'M{n(x)} {n(y)} Q{n(x + 3)} {n(y + L * 0.5)} {n(x)} {n(y + L)}', c, 2.6)
    for k, s in ((0.25, 1), (0.35, -1), (0.5, 1), (0.62, -1), (0.75, 1)):
        yy = y + L * k
        f.path(f'M{n(x)} {n(yy)} Q{n(x + s * 10)} {n(yy + 2)} {n(x + s * 18)} {n(yy + 10)}', c, 1.2)
    return f


def cow(f, x, y, s=1.0, c='#8B5A3C', hump=True, horns=True, udder=False, face=1):
    """side view of a zebu-type (humped) cow, feet on y, body centre x; face = 1 head right, -1 head left"""
    def P(px, py):
        return f'{n(x + face * px * s)} {n(y + py * s)}'
    body = (f'M{P(-40, -30)} C{P(-42, -50)} {P(-25, -56)} {P(-5, -55)} ' +
            (f'L{P(12, -56)} C{P(16, -68)} {P(26, -68)} {P(28, -56)} ' if hump else f'L{P(28, -56)} ') +
            f'C{P(34, -55)} {P(38, -52)} {P(42, -48)} L{P(52, -50)} C{P(60, -50)} {P(64, -44)} {P(62, -36)} '
            f'L{P(56, -30)} C{P(50, -30)} {P(46, -34)} {P(40, -34)} C{P(36, -26)} {P(34, -22)} {P(32, -22)} '
            f'L{P(32, 0)} L{P(26, 0)} L{P(24, -20)} L{P(-28, -20)} L{P(-30, 0)} L{P(-36, 0)} L{P(-38, -22)} C{P(-42, -24)} {P(-42, -27)} {P(-40, -30)}Z')
    f.path(body, '#3E2A1E', 1.4, c)
    f.path(f'M{P(26, -20)} L{P(24, 0)} L{P(19, 0)} L{P(19, -20)} M{P(-24, -20)} L{P(-22, 0)} L{P(-17, 0)} L{P(-17, -20)}', '#3E2A1E', 1.3, c)
    f.path(f'M{P(34, -22)} C{P(36, -14)} {P(40, -12)} {P(42, -16)}', '#3E2A1E', 1.2)  # dewlap hint
    f.path(f'M{P(-40, -42)} C{P(-48, -36)} {P(-48, -22)} {P(-46, -12)}', '#3E2A1E', 1.4)  # tail
    f.circle(x + face * 55 * s, y - 44 * s, 1.6 * s, None, 0, '#1E140E')
    if horns:
        f.path(f'M{P(48, -50)} C{P(48, -60)} {P(54, -66)} {P(58, -64)}', '#E8DCC2', 2.4 * s)
    if udder:
        f.path(f'M{P(-6, -20)} C{P(-6, -10)} {P(10, -10)} {P(10, -20)}Z', '#5E3A26', 1, '#E8B9A0')
    return f


def goat(f, x, y, s=1.0, c='#5A4636', face=1):
    def P(px, py):
        return f'{n(x + face * px * s)} {n(y + py * s)}'
    f.path(f'M{P(-26, -26)} C{P(-26, -38)} {P(-12, -40)} {P(4, -40)} L{P(18, -40)} L{P(26, -52)} C{P(30, -56)} {P(36, -54)} {P(38, -48)} '
           f'L{P(36, -42)} L{P(30, -38)} L{P(24, -28)} L{P(22, 0)} L{P(18, 0)} L{P(16, -22)} L{P(-16, -22)} L{P(-18, 0)} L{P(-22, 0)} L{P(-24, -22)}Z', '#2E241C', 1.3, c)
    f.path(f'M{P(28, -54)} C{P(24, -64)} {P(18, -66)} {P(14, -64)}', '#2E241C', 1.8)  # horn back-swept
    f.path(f'M{P(36, -42)} L{P(37, -34)}', '#2E241C', 1.4)  # beard
    f.path(f'M{P(-26, -32)} L{P(-31, -38)}', '#2E241C', 1.6)  # tail up
    f.circle(x + face * 32 * s, y - 49 * s, 1.3 * s, None, 0, '#111')
    return f


def sheep(f, x, y, s=1.0, c='#EFE6D6', head='#3A2C22', face=1, fat_tail=True):
    def P(px, py):
        return f'{n(x + face * px * s)} {n(y + py * s)}'
    f.path(f'M{P(-28, -24)} C{P(-34, -40)} {P(-14, -46)} {P(0, -44)} C{P(14, -48)} {P(28, -42)} {P(26, -26)} C{P(24, -18)} {P(-20, -16)} {P(-28, -24)}Z', '#7A6A58', 1.3, c)
    f.path(f'M{P(22, -40)} L{P(32, -46)} C{P(38, -48)} {P(42, -42)} {P(40, -36)} L{P(30, -30)}Z', '#1E1712', 1.2, head)
    f.path(f'M{P(16, -20)} L{P(17, 0)} M{P(10, -19)} L{P(10, 0)} M{P(-14, -19)} L{P(-14, 0)} M{P(-20, -20)} L{P(-21, 0)}', '#3A2C22', 2.4)
    if fat_tail:
        f.ellipse(x - face * 30 * s, y - 20 * s, 6 * s, 9 * s, '#7A6A58', 1.2, c)
    return f


def camel(f, x, y, s=1.0, c='#C9A16A', face=1):
    def P(px, py):
        return f'{n(x + face * px * s)} {n(y + py * s)}'
    f.path(f'M{P(-34, -46)} C{P(-30, -60)} {P(-14, -78)} {P(-2, -66)} C{P(6, -58)} {P(16, -52)} {P(24, -54)} L{P(34, -76)} C{P(36, -84)} {P(46, -86)} {P(50, -80)} '
           f'L{P(52, -74)} L{P(42, -72)} L{P(34, -48)} C{P(30, -40)} {P(26, -38)} {P(22, -38)} L{P(22, 0)} L{P(17, 0)} L{P(16, -36)} L{P(-20, -36)} L{P(-22, 0)} L{P(-27, 0)} L{P(-29, -38)} C{P(-34, -40)} {P(-36, -42)} {P(-34, -46)}Z', '#5A4128', 1.3, c)
    f.circle(x + face * 44 * s, y - 80 * s, 1.3 * s, None, 0, '#222')
    return f


def hen(f, x, y, s=1.0, c='#FFFFFF', face=1):
    def P(px, py):
        return f'{n(x + face * px * s)} {n(y + py * s)}'
    f.path(f'M{P(-16, -14)} C{P(-20, -30)} {P(-10, -34)} {P(-4, -26)} C{P(2, -22)} {P(8, -24)} {P(10, -32)} C{P(12, -40)} {P(22, -40)} {P(22, -32)} L{P(27, -30)} L{P(22, -28)} '
           f'C{P(22, -16)} {P(14, -8)} {P(2, -8)} C{P(-8, -8)} {P(-14, -10)} {P(-16, -14)}Z', '#6A5B50', 1.3, c)
    f.path(f'M{P(14, -40)} C{P(14, -46)} {P(20, -46)} {P(20, -40)}', RED, 2.4)
    f.path(f'M{P(0, -8)} L{P(-1, 0)} M{P(6, -8)} L{P(7, 0)}', ORANGE, 1.6)
    f.circle(x + face * 18 * s, y - 34 * s, 1.2 * s, None, 0, '#222')
    return f


def person(f, x, y, s=1.0, woman=False, pose='stand', cloth=CLOTH, face=1):
    """simple Eritrean farmer: brown skin, white netsela (woman: shawl over the head) / white shirt and trousers (man)"""
    def P(px, py):
        return f'{n(x + face * px * s)} {n(y + py * s)}'
    f.circle(x, y - 62 * s, 7 * s, '#4A2C1B', 1, SKIN)
    if woman:
        f.path(f'M{P(-8, -60)} C{P(-10, -74)} {P(10, -74)} {P(9, -60)} L{P(12, -42)} L{P(14, 0)} L{P(-14, 0)} L{P(-11, -42)}Z', '#8A7F76', 1.2, cloth)
        f.path(f'M{P(-11, -10)} L{P(14, -10)}', BLUE, 2)  # coloured border (tilet)
    else:
        f.path(f'M{P(-9, -54)} L{P(9, -54)} L{P(10, -30)} L{P(-10, -30)}Z', '#8A7F76', 1.2, cloth)
        f.path(f'M{P(-8, -30)} L{P(-7, 0)} M{P(7, -30)} L{P(6, 0)}', '#8A7F76', 4.2 * s)
        f.path(f'M{P(-7, -69)} C{P(-4, -73)} {P(5, -73)} {P(7, -68)}', '#F2F0EA', 2.4 * s)  # light head cloth
    if pose == 'plough':
        f.path(f'M{P(8, -48)} L{P(22, -40)}', SKIN, 2.6 * s)
    elif pose == 'hoe':
        f.path(f'M{P(8, -48)} L{P(18, -36)}', SKIN, 2.6 * s)
    return f


def maresha(f, x, y, s=1.0, face=1):
    """traditional Eritrean ox-drawn plough (maresha): beam, handle and iron point; (x, y) = point in the soil"""
    def P(px, py):
        return f'{n(x + face * px * s)} {n(y + py * s)}'
    f.path(f'M{P(-30, -40)} L{P(-10, -2)} L{P(10, 2)}', '#6B4A2B', 3)
    f.path(f'M{P(-8, -4)} L{P(70, -26)}', '#6B4A2B', 3)
    f.path(f'M{P(6, 0)} L{P(16, 2)}', '#55606A', 3)
    return f


def sun(f, x, y, r=12):
    f.circle(x, y, r, '#D79A1E', 1.4, '#F6C445')
    for i in range(8):
        a = math.radians(i * 45)
        f.line(x + math.cos(a) * (r + 3), y + math.sin(a) * (r + 3), x + math.cos(a) * (r + 8), y + math.sin(a) * (r + 8), '#D79A1E', 1.8)
    return f


def cloud(f, x, y, s=1.0, rain=False):
    f.path(f'M{n(x - 22 * s)} {n(y + 8 * s)} C{n(x - 32 * s)} {n(y + 8 * s)} {n(x - 30 * s)} {n(y - 6 * s)} {n(x - 20 * s)} {n(y - 4 * s)} C{n(x - 18 * s)} {n(y - 16 * s)} {n(x)} {n(y - 18 * s)} {n(x + 4 * s)} {n(y - 8 * s)} '
           f'C{n(x + 14 * s)} {n(y - 14 * s)} {n(x + 28 * s)} {n(y - 6 * s)} {n(x + 22 * s)} {n(y + 8 * s)}Z', '#8FA3B5', 1.3, '#FFFFFF')
    if rain:
        for i in range(5):
            xx = x - 18 * s + i * 9 * s
            f.line(xx, y + 13 * s, xx - 3 * s, y + 22 * s, WATER, 1.6)
    return f


def tree(f, x, y, h=60, c=LEAF, trunk='#6B4A2B', kind='round'):
    f.path(f'M{n(x - 3)} {n(y)} L{n(x - 2)} {n(y - h * 0.55)} L{n(x + 2)} {n(y - h * 0.55)} L{n(x + 3)} {n(y)}Z', None, 0, trunk)
    if kind == 'acacia':
        f.path(f'M{n(x)} {n(y - h * 0.5)} L{n(x - h * 0.3)} {n(y - h * 0.8)} M{n(x)} {n(y - h * 0.5)} L{n(x + h * 0.3)} {n(y - h * 0.82)}', trunk, 2)
        f.ellipse(x, y - h * 0.86, h * 0.55, h * 0.14, '#3B6E2C', 1, c)
    else:
        f.circle(x, y - h * 0.72, h * 0.3, '#3B6E2C', 1, c)
    return f
