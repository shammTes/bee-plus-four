r"""Grade 10 Unit 5 — Congruency and the Geometry of Size: congruence tests, quadrilateral theorems, perimeter and area
of polygons, sectors and segments, surface area and volume of prisms, cylinders, pyramids, cones and spheres (pp. 143-225)."""
import math
from common import set_unit, T, RM, MN, TB, DG, WK, CK, QSet
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL, polar, mid, lerp
from figs_common import side_by_side
from g10_u4 import ell, cyl, cone, LIGHT, MIDF, TOPF

UID = 'math10-u5'
set_unit(UID)


def lab3(f, pts, names, poss, c=INK, size=12):
    for p, s, pos in zip(pts, names, poss):
        f.ptlabel(*p, s, pos, c, size)


# ------------------------------------------------------------------ 5.1 figures
def f_congmarks():
    f = Fig(330, 150)
    A, B, C = (60, 22), (16, 128), (140, 128)
    D, E, F = (220, 22), (176, 128), (304, 128)
    for P, Q, R, col in ((A, B, C, BLUE), (D, E, F, GREEN)):
        f.poly([P, Q, R], col, 2.2, FILL[col])
        f.ticks(P, Q, 1, RED).ticks(Q, R, 2, RED).ticks(R, P, 3, RED)
        f.angle(Q, P, R, 16, ORANGE).angle(R, Q, P, 18, PURPLE).angle(P, R, Q, 22, GREEN if col == BLUE else BLUE)
    lab3(f, (A, B, C), 'ABC', ('n', 'sw', 'se'))
    lab3(f, (D, E, F), 'DEF', ('n', 'sw', 'se'))
    return f


def _panel(title, col=INK):
    g = Fig(108, 100)
    g.text(54, 14, title, 12.5, col)
    return g


def f_tests():
    A, B, C = (40, 30), (10, 90), (98, 90)
    out = []
    # SSS
    g = _panel('SSS', BLUE)
    g.poly([A, B, C], INK, 1.4, FILL[GREY])
    g.line(*A, *B, BLUE, 3.4).line(*B, *C, BLUE, 3.4).line(*C, *A, BLUE, 3.4)
    out.append(g)
    # SAS
    g = _panel('SAS', BLUE)
    g.poly([A, B, C], INK, 1.4, FILL[GREY])
    g.line(*A, *B, BLUE, 3.4).line(*B, *C, BLUE, 3.4).angle(B, A, C, 15, RED, fill=FILL[RED])
    out.append(g)
    # ASA
    g = _panel('ASA', BLUE)
    g.poly([A, B, C], INK, 1.4, FILL[GREY])
    g.line(*B, *C, BLUE, 3.4).angle(B, A, C, 15, RED, fill=FILL[RED]).angle(C, A, B, 18, RED, fill=FILL[RED])
    out.append(g)
    # AAS
    g = _panel('AAS', BLUE)
    g.poly([A, B, C], INK, 1.4, FILL[GREY])
    g.line(*A, *C, BLUE, 3.4).angle(B, A, C, 15, RED, fill=FILL[RED]).angle(C, A, B, 18, RED, fill=FILL[RED])
    out.append(g)
    # RHS
    g = _panel('RHS', BLUE)
    P, Q, R = (14, 30), (14, 90), (98, 90)
    g.poly([P, Q, R], INK, 1.4, FILL[GREY])
    g.right(Q, P, R, 9, RED).line(*P, *R, BLUE, 3.4).line(*P, *Q, BLUE, 3.4)
    out.append(g)
    # AAA - not a test
    g = _panel('AAA: no!', RED)
    g.poly([(30, 50), (14, 80), (52, 80)], INK, 1.6, FILL[GREY])
    g.poly([(70, 30), (40, 92), (104, 92)], INK, 1.6, FILL[GREY])
    out.append(g)
    f = Fig(342, 214)
    for i, g in enumerate(out):
        x, y = (i % 3) * 114, (i // 3) * 108
        f.raw(f'<g transform="translate({x} {y})">' + ''.join(g.p) + '</g>')
    return f


def f_ex51():
    f = Fig(320, 160)
    O = (160, 80)
    A, B = (40, 140), (280, 20)
    D, C = (90, 18), (230, 142)
    f.poly([A, O, D], BLUE, 2, FILL[BLUE]).poly([B, O, C], GREEN, 2, FILL[GREEN])
    f.line(*A, *B, INK, 2).line(*D, *C, INK, 2)
    f.ticks(A, O, 1, RED).ticks(O, B, 1, RED).ticks(D, O, 2, RED).ticks(O, C, 2, RED)
    f.angle(O, A, D, 18, ORANGE, fill=FILL[ORANGE]).angle(O, B, C, 18, ORANGE, fill=FILL[ORANGE])
    lab3(f, (A, B, C, D, O), 'ABCDO', ('sw', 'ne', 'se', 'nw', 'n'))
    return f


def f_perpbis():
    f = Fig(320, 170)
    A, B, C = (40, 150), (280, 150), (160, 150)
    P = (160, 30)
    f.poly([A, C, P], BLUE, 2, FILL[BLUE]).poly([C, B, P], GREEN, 2, FILL[GREEN])
    f.line(160, 10, 160, 166, PURPLE, 2.2)
    f.text(150, 20, 'l', 14, PURPLE, 'end', italic=True)
    f.right(C, P, B, 10, INK)
    f.ticks(A, C, 1, RED).ticks(C, B, 1, RED)
    f.ticks(P, A, 2, ORANGE).ticks(P, B, 2, ORANGE)
    lab3(f, (A, B, C, P), 'ABCP', ('w', 'e', 's', 'ne'))
    return f


def f_isos():
    f = Fig(320, 170)
    A, B, C = (160, 16), (60, 150), (260, 150)
    D = (160, 150)
    f.poly([A, B, D], BLUE, 2, FILL[BLUE]).poly([A, D, C], GREEN, 2, FILL[GREEN])
    f.line(*A, *D, RED, 2, dash=True)
    f.ticks(A, B, 1, RED).ticks(A, C, 1, RED)
    f.angle(A, B, D, 20, ORANGE).angle(A, D, C, 24, ORANGE)
    f.angle(B, A, C, 30, PURPLE, fill=FILL[PURPLE]).angle(C, A, B, 30, PURPLE, fill=FILL[PURPLE])
    f.angle(B, D, A, 0.1, INK)
    lab3(f, (A, B, C, D), 'ABCD', ('n', 'sw', 'se', 's'))
    f.text(316, 40, 'AB = AC', 12, RED, 'end')
    f.text(316, 58, 'so angle B = angle C', 12, ORANGE, 'end')
    return f


def f_para():
    f = Fig(320, 160)
    A, B, C, D = (30, 140), (220, 140), (290, 30), (100, 30)
    M = mid(A, C)
    f.poly([A, B, C, D], INK, 2.2, FILL[BLUE])
    f.line(*A, *C, BLUE, 1.6).line(*B, *D, GREEN, 1.6)
    f.par(A, B, 1, INK).par(D, C, 1, INK).par(A, D, 2, INK).par(B, C, 2, INK)
    f.ticks(A, M, 1, BLUE).ticks(M, C, 1, BLUE).ticks(B, M, 2, GREEN).ticks(M, D, 2, GREEN)
    f.angle(A, B, D, 18, ORANGE, fill=FILL[ORANGE]).angle(C, D, B, 18, ORANGE, fill=FILL[ORANGE])
    f.dot(*M, INK, 3)
    lab3(f, (A, B, C, D, M), 'ABCDM', ('sw', 'se', 'ne', 'nw', 's'))
    return f


def f_rhombus():
    f = Fig(320, 170)
    O = (160, 85)
    A, B, C, D = (40, 85), (160, 155), (280, 85), (160, 15)
    f.poly([A, B, C, D], INK, 2.2, FILL[GREEN])
    f.line(*A, *C, BLUE, 1.8).line(*B, *D, BLUE, 1.8)
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        f.ticks(p, q, 1, RED)
    f.right(O, C, D, 10, RED)
    f.ticks(A, O, 2, BLUE).ticks(O, C, 2, BLUE).ticks(O, B, 3, BLUE, gap=3).ticks(O, D, 3, BLUE, gap=3)
    lab3(f, (A, B, C, D, O), 'ABCDO', ('w', 's', 'e', 'n', 'sw'))
    return f


def f_quadfamily():
    f = Fig(330, 214)

    def box(x, y, w, s, c):
        f.rect(x - w / 2, y - 13, w, 26, c, 1.8, FILL[c], rx=7)
        f.text(x, y + 4.5, s, 12, c)

    def arr(a, b):
        f.arrow(a[0], a[1], b[0], b[1], GREY, 1.5, 7)
    box(165, 20, 120, 'quadrilateral', INK)
    box(70, 76, 96, 'trapezium', ORANGE)
    box(240, 76, 120, 'parallelogram', BLUE)
    box(175, 140, 96, 'rectangle', GREEN)
    box(290, 140, 80, 'rhombus', PURPLE)
    box(230, 196, 80, 'square', RED)
    arr((140, 34), (90, 62))
    arr((190, 34), (225, 62))
    arr((225, 90), (190, 126))
    arr((255, 90), (280, 126))
    arr((185, 154), (215, 182))
    arr((280, 154), (248, 182))
    f.text(14, 120, 'each box has all', 11, GREY, 'start')
    f.text(14, 134, 'the properties of', 11, GREY, 'start')
    f.text(14, 148, 'the boxes above it', 11, GREY, 'start')
    return f


def f_midseg():
    f = Fig(320, 170)
    A, B, C = (110, 16), (20, 156), (250, 156)
    E, F = mid(A, B), mid(A, C)
    D = (F[0] + (F[0] - E[0]), F[1])
    f.poly([A, B, C], INK, 2, FILL[GREY])
    f.line(*E, *F, BLUE, 3)
    f.line(*F, *D, BLUE, 1.6, dash=True).line(*C, *D, GREY, 1.4, dash=True)
    f.ticks(A, E, 1, RED).ticks(E, B, 1, RED).ticks(A, F, 2, RED).ticks(F, C, 2, RED)
    f.par(E, F, 1, BLUE).par(B, C, 1, BLUE)
    lab3(f, (A, B, C, E, F, D), 'ABCEFD', ('n', 'sw', 'se', 'w', 'ne', 'e'))
    f.text(316, 30, 'EF || BC', 12.5, BLUE, 'end')
    f.text(316, 48, 'EF = ½ BC', 12.5, BLUE, 'end')
    return f


# ------------------------------------------------------------------ 5.2 figures
def f_areas():
    out = []
    g = Fig(150, 100)
    P = [(10, 86), (140, 86), (95, 16)]
    g.poly(P, BLUE, 2, FILL[BLUE]).line(95, 16, 95, 86, RED, 1.6, dash=True).right((95, 86), (95, 16), (140, 86), 7, RED)
    g.text(75, 99, 'b', 12, BLUE, italic=True).text(100, 56, 'h', 12, RED, 'start', italic=True)
    out.append((g, 'triangle  ½bh'))
    g = Fig(150, 100)
    g.poly([(10, 86), (110, 86), (140, 16), (40, 16)], GREEN, 2, FILL[GREEN]).line(40, 16, 40, 86, RED, 1.6, dash=True)
    g.right((40, 86), (40, 16), (110, 86), 7, RED)
    g.text(60, 99, 'b', 12, GREEN, italic=True).text(45, 56, 'h', 12, RED, 'start', italic=True)
    out.append((g, 'parallelogram  bh'))
    g = Fig(150, 100)
    g.poly([(10, 86), (140, 86), (105, 16), (40, 16)], ORANGE, 2, FILL[ORANGE]).line(40, 16, 40, 86, RED, 1.6, dash=True)
    g.text(72, 11, 'a', 12, ORANGE, italic=True).text(75, 99, 'b', 12, ORANGE, italic=True).text(45, 56, 'h', 12, RED, 'start', italic=True)
    out.append((g, 'trapezium  ½(a + b)h'))
    g = Fig(150, 100)
    g.poly([(10, 50), (75, 10), (140, 50), (75, 90)], PURPLE, 2, FILL[PURPLE])
    g.line(10, 50, 140, 50, RED, 1.6, dash=True).line(75, 10, 75, 90, BLUE, 1.6, dash=True)
    g.text(40, 46, 'd₁', 12, RED).text(82, 76, 'd₂', 12, BLUE, 'start')
    out.append((g, 'rhombus, kite  ½d₁d₂'))
    f = Fig(330, 250)
    for i, (g, s) in enumerate(out):
        x, y = (i % 2) * 168 + 6, (i // 2) * 124 + 4
        f.raw(f'<g transform="translate({x} {y})">' + ''.join(g.p) + '</g>')
        f.text(x + 75, y + 118, s, 12, INK)
    return f


def f_regpoly():
    a = Fig(150, 150)
    O, r = (75, 75), 64
    pts = [polar(O, r, 90 + 60 * i) for i in range(6)]
    a.circle(*O, r, GREY, 1.4)
    a.poly(pts, BLUE, 2, FILL[BLUE])
    A, B = pts[5], pts[0]
    A, B = polar(O, r, 30), polar(O, r, 90)
    E = mid(A, B)
    a.poly([O, A, B], RED, 1.8, FILL[RED])
    a.line(*O, *E, ORANGE, 1.6, dash=True).right(E, O, A, 6, ORANGE)
    a.dot(*O, INK, 3).ptlabel(*O, 'O', 's', INK, 11)
    a.ptlabel(*A, 'A', 'e', INK, 11).ptlabel(*B, 'B', 'n', INK, 11).ptlabel(*E, 'E', 'ne', ORANGE, 11)
    a.seglabel(O, A, 'r', 9, RED, 12, 1)
    b = Fig(150, 150)
    r2 = 52
    R2 = r2 / math.cos(math.radians(30))
    pts = [polar(O, R2, 60 * i) for i in range(6)]
    b.poly(pts, GREEN, 2, FILL[GREEN])
    b.circle(*O, r2, GREY, 1.4)
    A, B = polar(O, R2, 240), polar(O, R2, 300)
    E = mid(A, B)
    b.poly([O, A, B], RED, 1.8, FILL[RED])
    b.line(*O, *E, ORANGE, 2).right(E, O, B, 6, ORANGE)
    b.dot(*O, INK, 3).ptlabel(*O, 'O', 'n', INK, 11)
    b.ptlabel(*A, 'A', 'sw', INK, 11).ptlabel(*B, 'B', 'se', INK, 11).ptlabel(*E, 'E', 's', ORANGE, 11)
    b.text(O[0] + 6, O[1] + 30, 'r', 12, ORANGE, 'start', italic=True)
    return side_by_side([a, b], 16, ['inscribed in the circle', 'circumscribed about it'])


def f_quadex():
    f = Fig(320, 190)
    # D left, B right on a horizontal diagonal DB = 12; A above with AD = 9 (right angle at D); C below with BC = 5 (right angle at B)
    u = 18
    D = (40, 100)
    B = (D[0] + 12 * u * 0.9, 100)
    A = (D[0], 100 - 9 * u * 0.45)
    C = (B[0], 100 + 5 * u * 0.9)
    A = (D[0], 100 - 9 * 9)
    C = (B[0], 100 + 5 * 9)
    B = (D[0] + 12 * 18 * 0.9 * 1.0, 100)
    f.poly([A, B, C, D], INK, 2, FILL[GREY])
    f.line(*D, *B, BLUE, 2, dash=True)
    f.right(D, A, B, 9, RED).right(B, D, C, 9, RED)
    lab3(f, (A, B, C, D), 'ABCD', ('n', 'e', 's', 'w'))
    f.seglabel(A, B, '15', 12, INK, 13, -1)
    f.seglabel(D, C, '13', 12, INK, 13, 1)
    f.seglabel(B, C, '5', 10, INK, 13, 1)
    f.seglabel(D, B, '12', 10, BLUE, 13, -1)
    f.seglabel(A, D, '9', 10, RED, 13, -1)
    return f


def f_ex512():
    f = Fig(320, 190)
    k = 15
    A = (40, 30)
    D = (A[0] + 8 * k, 30)
    B = (A[0], 30 + 6 * k)
    # C with BC = 7, CD = 5 (BD = 10)
    bx, by = B
    dx, dy = D
    L = math.hypot(dx - bx, dy - by)
    a_ = (7 ** 2 - 5 ** 2 + 10 ** 2) / (2 * 10)
    h = math.sqrt(7 ** 2 - a_ ** 2)
    ux, uy = (dx - bx) / L, (dy - by) / L
    C = (bx + ux * a_ * k - uy * h * k, by + uy * a_ * k + ux * h * k)
    f.poly([A, D, C, B], INK, 2, FILL[GREY])
    f.line(*B, *D, BLUE, 2, dash=True)
    f.right(A, D, B, 9, RED)
    lab3(f, (A, B, C, D), 'ABCD', ('nw', 'sw', 'se', 'ne'))
    f.seglabel(A, D, '8', 10, INK, 13, -1)
    f.seglabel(A, B, '6', 10, INK, 13, 1)
    f.seglabel(B, C, '7', 11, INK, 13, 1)
    f.seglabel(D, C, '5', 10, INK, 13, -1)
    f.seglabel(B, D, '10', 10, BLUE, 13, -1)
    return f


def f_sector():
    a = Fig(150, 140)
    O, r = (40, 110), 100
    th = 60
    P, Q = polar(O, r, 0), polar(O, r, th)
    a.path(f'M{O[0]} {O[1]} L{P[0]:.1f} {P[1]:.1f} A{r} {r} 0 0 0 {Q[0]:.1f} {Q[1]:.1f} Z', BLUE, 2, FILL[BLUE])
    a.arc(O, r, 0, th, RED, 4)
    a.angle(O, P, Q, 22, ORANGE, fill=FILL[ORANGE])
    a.seglabel(O, P, 'r', 10, INK, 12, -1)
    a.text(118, 34, 'L', 13, RED, 'start', italic=True)
    b = Fig(150, 140)
    P, Q = polar(O, r, 0), polar(O, r, 70)
    b.path(f'M{O[0]} {O[1]} L{P[0]:.1f} {P[1]:.1f} A{r} {r} 0 0 0 {Q[0]:.1f} {Q[1]:.1f} Z', GREY, 1.4, 'none')
    b.path(f'M{P[0]:.1f} {P[1]:.1f} A{r} {r} 0 0 0 {Q[0]:.1f} {Q[1]:.1f} Z', GREEN, 2, FILL[GREEN])
    b.poly([O, P, Q], INK, 1.6, FILL[GREY])
    b.angle(O, P, Q, 22, ORANGE, fill=FILL[ORANGE])
    b.seglabel(O, P, 'r', 10, INK, 12, -1)
    return side_by_side([a, b], 20, ['sector', 'segment = sector − triangle'])


# ------------------------------------------------------------------ 5.3 figures
def f_cuboid():
    f = Fig(330, 180)
    x, y, l, h = 16, 70, 110, 70
    dx, dy = 44, -30
    f.poly([(x, y), (x + dx, y + dy), (x + l + dx, y + dy), (x + l, y)], INK, 1.8, TOPF)
    f.poly([(x + l, y), (x + l + dx, y + dy), (x + l + dx, y + h + dy), (x + l, y + h)], INK, 1.8, MIDF)
    f.rect(x, y, l, h, INK, 1.8, LIGHT)
    f.line(x + dx, y + dy + h, x, y + h, INK, 1.2, dash=True).line(x + dx, y + dy + h, x + dx + l, y + dy + h, INK, 1.2, dash=True)
    f.line(x + dx, y + dy + h, x + dx, y + dy, INK, 1.2, dash=True)
    f.text(x + l / 2, y + h + 16, 'l', 13, BLUE, italic=True)
    f.text(x + l + dx / 2 + 8, y + h + dy / 2 + 12, 'w', 13, GREEN, 'start', italic=True)
    f.text(x + l + dx + 8, y + dy + h / 2, 'h', 13, RED, 'start', italic=True)
    # net (cross shape) l x w base, sides
    s = 0.36
    L, W, H = l * s, 46 * s * 1.2, h * s
    X0, Y0 = 210, 14
    cells = [(X0 + H, Y0, L, W, TOPF), (X0 + H, Y0 + W, L, H, LIGHT), (X0, Y0 + W, H, L * 0 + H, MIDF)]
    L, W, H = 40, 22, 26
    X0, Y0 = 200, 8
    rects = [(X0 + H, Y0, L, H, LIGHT), (X0 + H, Y0 + H, L, W, TOPF), (X0, Y0 + H, H, W, MIDF), (X0 + H + L, Y0 + H, H, W, MIDF),
             (X0 + H, Y0 + H + W, L, H, LIGHT), (X0 + H, Y0 + 2 * H + W, L, W, TOPF)]
    for (rx, ry, rw, rh, c) in rects:
        f.rect(rx, ry, rw, rh, BLUE, 1.5, c)
    f.text(X0 + H + L / 2, Y0 + 2 * H + 2 * W + 16, 'net: 3 pairs of rectangles', 11.5, INK)
    return f


def f_triprism():
    f = Fig(320, 170)
    k = 26
    A, B, C = (60, 150), (60 + 4 * k, 150), (60, 150 - 3 * k)
    d = (110, -50)
    A2, B2, C2 = [(p[0] + d[0], p[1] + d[1]) for p in (A, B, C)]
    f.poly([C, C2, B2, B], 'none', 0, MIDF)
    f.poly([A, B, C], INK, 2, LIGHT)
    f.line(*C, *C2, INK, 2).line(*B, *B2, INK, 2).line(*C2, *B2, INK, 2)
    f.line(*A, *A2, INK, 1.3, dash=True).line(*A2, *B2, INK, 1.3, dash=True).line(*A2, *C2, INK, 1.3, dash=True)
    f.right(A, B, C, 8, RED)
    f.seglabel(A, B, '4 cm', 12, BLUE, 12, -1)
    f.seglabel(A, C, '3 cm', 22, BLUE, 12, -1)
    f.text(B[0] + 62, B[1] - 14, 'height 3 cm', 12, GREEN, 'start')
    f.seglabel(B, C, '5', 10, RED, 12, -1)
    return f


def f_cylnet():
    f = Fig(330, 190)
    cyl(f, 60, 40, 150, 40, 12)
    f.line(60, 40, 100, 40, BLUE, 2).dot(60, 40, INK, 3)
    f.text(80, 34, 'r', 13, BLUE, italic=True)
    f.text(108, 100, 'h', 13, RED, 'start', italic=True)
    f.arrow(126, 95, 150, 95, GREY, 1.6, 7)
    f.circle(240, 26, 20, BLUE, 1.8, TOPF)
    f.rect(165, 48, 150, 90, BLUE, 1.8, LIGHT)
    f.circle(240, 160, 20, BLUE, 1.8, TOPF)
    f.text(240, 98, '2πr × h', 13, RED)
    f.text(240, 62, '2πr', 12, INK)
    f.text(172, 98, 'h', 13, RED, 'start', italic=True)
    return f


def f_pyrnet():
    a = Fig(160, 160)
    s = 52
    c = (80, 80)
    sq = [(c[0] - s / 2, c[1] - s / 2), (c[0] + s / 2, c[1] - s / 2), (c[0] + s / 2, c[1] + s / 2), (c[0] - s / 2, c[1] + s / 2)]
    a.poly(sq, BLUE, 1.8, FILL[BLUE])
    tips = [(c[0], c[1] - s / 2 - 50), (c[0] + s / 2 + 50, c[1]), (c[0], c[1] + s / 2 + 50), (c[0] - s / 2 - 50, c[1])]
    for i in range(4):
        a.poly([sq[i], sq[(i + 1) % 4], tips[i]], ORANGE, 1.8, FILL[ORANGE])
    a.line(c[0], c[1] - s / 2, *tips[0], RED, 1.6, dash=True)
    a.text(c[0] + 5, c[1] - s / 2 - 22, 's', 12, RED, 'start', italic=True)
    a.text(c[0], c[1] + 4, 'b', 12, BLUE, italic=True)
    b = Fig(150, 160)
    apex, foot, m = (40, 20), (40, 130), (120, 130)
    b.poly([apex, foot, m], INK, 2, FILL[GREY])
    b.right(foot, apex, m, 9, RED)
    b.text(32, 80, 'h', 13, RED, 'end', italic=True)
    b.text(80, 146, 'b/2', 12, BLUE)
    b.text(88, 70, 's', 13, ORANGE, 'start', italic=True)
    b.line(*apex, *m, ORANGE, 3)
    return side_by_side([a, b], 16, ['net of a square pyramid', 'h, b/2 and s'])


def f_conenet():
    f = Fig(330, 190)
    cone(f, 70, 30, 150, 50, 13)
    f.line(70, 30, 120, 150, ORANGE, 3)
    f.line(70, 150, 120, 150, BLUE, 2).dot(70, 150, INK, 3)
    f.text(95, 166, 'r', 13, BLUE, italic=True)
    f.text(102, 84, 's', 13, ORANGE, 'start', italic=True)
    f.arrow(140, 95, 164, 95, GREY, 1.6, 7)
    O, R = (250, 30), 120
    a0, a1 = 230, 310
    P, Q = polar(O, R, 300), polar(O, R, 240)
    f.path(f'M{O[0]} {O[1]} L{P[0]:.1f} {P[1]:.1f} A{R} {R} 0 0 1 {Q[0]:.1f} {Q[1]:.1f} Z', ORANGE, 2, FILL[ORANGE])
    f.text(250, 100, 'πrs', 14, RED)
    f.text(250, 172, 'arc = 2πr', 12, INK)
    f.text(214, 70, 's', 13, ORANGE, 'end', italic=True)
    return f


def f_archimedes():
    a = Fig(150, 160)
    cyl(a, 75, 24, 134, 50, 13)
    a.path('M75 24 L25 134 M75 24 L125 134', RED, 2)
    a.path('M25 134 A50 13 0 0 0 125 134', RED, 2)
    a.text(75, 100, '1/3', 14, RED)
    b = Fig(150, 160)
    cyl(b, 75, 24, 134, 52, 13)
    b.circle(75, 79, 52, BLUE, 2, FILL[BLUE])
    b.text(75, 84, '2/3', 14, BLUE)
    return side_by_side([a, b], 20, ['cone = 1/3 of cylinder', 'sphere = 2/3 of cylinder'])


DIAGRAMS = {
    'congmarks': (f_congmarks(), 'Congruent triangles: matching marks', 144),
    'tests': (f_tests(), 'The congruence tests (marked parts are equal)', 148),
    'ex51': (f_ex51(), 'Example 5.1', 148),
    'perpbis': (f_perpbis(), 'Example 5.2: a point on the perpendicular bisector', 148),
    'isos': (f_isos(), 'Theorem 5.2: base angles of an isosceles triangle', 155),
    'para': (f_para(), 'Properties of a parallelogram', 162),
    'rhombus': (f_rhombus(), 'Diagonals of a rhombus', 166),
    'quadfamily': (f_quadfamily(), 'The quadrilateral family', 162),
    'midseg': (f_midseg(), 'Theorem 5.11: the mid-segment of a triangle', 166),
    'areas': (f_areas(), 'Area formulas', 178),
    'regpoly': (f_regpoly(), 'Regular hexagon inscribed in and circumscribed about a circle', 173),
    'quadex': (f_quadex(), 'Example 5.11', 179),
    'ex512': (f_ex512(), 'Example 5.12', 181),
    'sector': (f_sector(), 'Sector and segment', 190),
    'cuboid': (f_cuboid(), 'Cuboid and its net', 198),
    'triprism': (f_triprism(), 'Example 5.19: right triangular prism', 199),
    'cylnet': (f_cylnet(), 'Net of a cylinder', 208),
    'pyrnet': (f_pyrnet(), 'Net of a square pyramid and the slant-height triangle', 211),
    'conenet': (f_conenet(), 'Net of a cone', 216),
    'archimedes': (f_archimedes(), 'Cone, sphere and cylinder of the same radius and height', 218),
}

# ------------------------------------------------------------------ 5.1
L51 = [
    T('=math10-u5-c03', '5.1.1 Congruent figures', 143,
      '**Congruent figures** have exactly the same shape **and** the same size: if you cut one out, it fits exactly on top of the other (you may turn it over). Congruent segments have equal length; congruent angles have equal measure; two circles are congruent when their radii are equal.',
      'Two triangles are congruent when the three sides **and** the three angles of one are equal to the **corresponding** sides and angles of the other. We write $\\triangle ABC \\cong \\triangle DEF$.',
      'The order of the letters is a promise: $A \\leftrightarrow D$, $B \\leftrightarrow E$, $C \\leftrightarrow F$. From $\\triangle ABC \\cong \\triangle DEF$ you can read off six facts:',
      '- sides: $AB = DE$, $BC = EF$, $AC = DF$',
      '- angles: $\\angle A = \\angle D$, $\\angle B = \\angle E$, $\\angle C = \\angle F$',
      'Writing $\\triangle BAC \\cong \\triangle DEF$ for the same triangles would be **wrong**, because it would match $B$ with $D$.',
      'On a figure, equal sides carry the same number of **tick marks** and equal angles the same number of **arcs**.'),
    DG('congmarks', 'Matching marks show the correspondence', 144, 'congmarks',
       'One tick: $AB = DE$; two ticks: $BC = EF$; three ticks: $CA = FD$. Same-coloured arcs mark equal angles.'),
    'math10-u5-c02',
    T('=math10-u5-c04', '5.1.2 Tests for congruent triangles', 147,
      'You do not need to check all six parts. Any one of these sets of **three** matching parts is enough:',
      '- **SAS (Postulate 1):** two sides and the **included** angle (the angle between those two sides).',
      '- **ASA (Postulate 2):** two angles and the **included** side (the side between the two angles).',
      '- **AAS (Theorem 5.1):** two angles and a side that is **not** between them. Reason: the third angles are then also equal ($180°$ minus the other two), so it becomes ASA.',
      '- **SSS (Postulate 3):** all three sides.',
      '- **RHS (Theorem 5.3):** in **right** triangles: the **h**ypotenuse and one other **s**ide.',
      '**Not tests:** **AAA** — equal angles give the same shape but possibly a different size (similar, not congruent). **SSA** — two sides and a non-included angle can give two different triangles (except the right-angle case, which is RHS).',
      '**How to write a proof:** make a two-column table (Statement | Reason). List three matching parts with a reason each (given, common side, vertical angles, alternate angles, …), name the test, and then use "corresponding parts of congruent triangles are equal" to get any further fact.'),
    DG('tests', 'Blue sides and red angles must match', 148, 'tests'),
    TB('tests-t', 'Congruence tests at a glance', 148, ['Test', 'What must match', 'Watch out'],
       [['SSS', 'all 3 sides', 'no angles needed'], ['SAS', '2 sides + angle **between** them', 'angle must be included'],
        ['ASA', '2 angles + side **between** them', 'side must be included'], ['AAS', '2 angles + a non-included side', 'side must correspond'],
        ['RHS', 'right angle + hypotenuse + one side', 'only for right triangles'], ['AAA, SSA', '—', '**not** valid tests']]),
    WK('ex-51a', 'Example 5.1: a two-column proof with SAS', 148,
       'In the figure, $AO = BO$ and $CO = DO$. Prove that $\\triangle AOD \\cong \\triangle BOC$.',
       ['$AO = BO$ — given.', '$DO = CO$ — given.', '$\\angle AOD = \\angle BOC$ — vertically opposite angles.',
        'The angle is between the two sides in each triangle, so $\\triangle AOD \\cong \\triangle BOC$ by **SAS**.',
        'Bonus (corresponding parts): $AD = BC$ and $\\angle A = \\angle B$, so $AD \\parallel BC$ (alternate angles).'],
       '$\\triangle AOD \\cong \\triangle BOC$ (SAS)', diagram='ex51'),
    DG('perpbis', 'Example 5.2', 148, 'perpbis'),
    WK('ex-51b', 'Example 5.2: points on the perpendicular bisector', 148,
       '$l$ is the perpendicular bisector of $AB$ and meets $AB$ at $C$. $P$ is any point of $l$. Show that $PA = PB$.',
       ['$AC = BC$ — $C$ is the midpoint.', '$\\angle ACP = \\angle BCP = 90°$ — $l \\perp AB$.', '$PC = PC$ — common side.',
        '$\\triangle ACP \\cong \\triangle BCP$ by SAS.', 'Hence $PA = PB$ (corresponding sides).'],
       'every point of the perpendicular bisector is equidistant from $A$ and $B$'),
    WK('ex-51c', 'Example 5.3: ASA with a shared angle', 150,
       '$P$ is the midpoint of $AB$; $D$ and $E$ are on the same side of $AB$ with $\\angle BAD = \\angle ABE$ and $\\angle APE = \\angle BPD$. Show $\\triangle ADP \\cong \\triangle BEP$.',
       ['$AP = BP$ — given ($P$ is the midpoint).', '$\\angle PAD = \\angle PBE$ — given.',
        '$\\angle APD = \\angle APE + \\angle EPD$ and $\\angle BPE = \\angle BPD + \\angle EPD$. Since $\\angle APE = \\angle BPD$, adding the same $\\angle EPD$ gives $\\angle APD = \\angle BPE$.',
        'Two angles and the included side match: $\\triangle ADP \\cong \\triangle BEP$ by **ASA**.'],
       '$\\triangle ADP \\cong \\triangle BEP$ (ASA)'),
    T('isos-t', 'Isosceles triangles (Theorem 5.2)', 155,
      '**Theorem 5.2:** if two sides of a triangle are equal, the angles opposite them are equal (the **base angles**). **Converse:** if two angles are equal, the sides opposite them are equal.',
      '**Proof:** draw the bisector $AD$ of $\\angle A$. Then $AB = AC$ (given), $\\angle BAD = \\angle CAD$ (bisector) and $AD = AD$ (common), so $\\triangle ABD \\cong \\triangle ACD$ (SAS) and $\\angle B = \\angle C$.',
      'From the same congruent triangles: $BD = DC$ and $\\angle ADB = \\angle ADC = 90°$. So in an isosceles triangle the bisector of the top angle is also the **median** and the **altitude** to the base.',
      'An equilateral triangle is isosceles in every direction, so all its angles are equal: $180° \\div 3 = 60°$ each.'),
    DG('isos', 'Base angles are equal', 155, 'isos'),
    WK('ex-51d', 'Example 5.5: using base angles', 156,
       'In isosceles $\\triangle ABC$ with $AB = AC$, points $D$ and $E$ lie on $BC$ with $BE = CD$. Show $AD = AE$.',
       ['$AB = AC$ — given.', '$\\angle B = \\angle C$ — base angles of an isosceles triangle.',
        '$BD = BE - DE$ and $CE = CD - DE$; since $BE = CD$, $BD = CE$.', '$\\triangle ABD \\cong \\triangle ACE$ by SAS.', 'So $AD = AE$.'],
       '$AD = AE$'),
    T('rhs-t', 'SSS and RHS', 159,
      '**SSS:** if three sides match, the triangles are congruent — a triangle is rigid: once its sides are fixed, its angles are fixed too (that is why roofs and bridges use triangles).',
      '**RHS:** two right triangles with equal hypotenuses and one other pair of equal sides are congruent. (By Pythagoras the third sides are equal too, so it is really SSS.)',
      '**Example:** $P$ and $Q$ are each equidistant from $A$ and $B$ ($AP = PB$, $AQ = QB$). Then $\\triangle APQ \\cong \\triangle BPQ$ (SSS), so $PQ$ bisects $\\angle APB$ and $PQ$ is the perpendicular bisector of $AB$.'),
    T('=math10-u5-c05', '5.1.3 Quadrilaterals and congruency', 162,
      'A **parallelogram** has both pairs of opposite sides parallel. Drawing a diagonal splits it into two congruent triangles (ASA with alternate angles and the common side) — **Theorem 5.4**. From this we get:',
      '- **Theorem 5.5:** opposite sides are equal. **Theorem 5.7:** opposite angles are equal.',
      '- **Theorem 5.9:** the diagonals **bisect each other**.',
      '- Consecutive angles add up to $180°$ (co-interior angles).',
      'Ways to **prove** that a quadrilateral is a parallelogram:',
      '- both pairs of opposite sides equal (**Theorem 5.6**);',
      '- one pair of opposite sides equal **and** parallel (**Theorem 5.8**);',
      '- diagonals bisect each other; or both pairs of opposite sides parallel (definition).',
      'Special parallelograms: a **rectangle** (all angles $90°$; a parallelogram with one right angle is already a rectangle; its diagonals are equal), a **rhombus** (all sides equal; **Theorem 5.10:** its diagonals are perpendicular bisectors of each other), and a **square** (both).'),
    DG('para', 'Parallelogram ABCD', 162, 'para',
       'Arrows: parallel sides. Ticks on the diagonals: $AM = MC$ and $BM = MD$. Opposite angles $A$ and $C$ are equal.'),
    DG('quadfamily', 'How the quadrilaterals are related', 162, 'quadfamily',
       'A square is a rectangle and a rhombus at the same time; every rectangle and every rhombus is a parallelogram. A trapezium has only one pair of parallel sides, so it is not a parallelogram.'),
    DG('rhombus', 'Rhombus: diagonals cross at right angles', 166, 'rhombus'),
    TB('quad-t', 'Properties of the special quadrilaterals', 165, ['Property', 'Parallelogram', 'Rectangle', 'Rhombus', 'Square'],
       [['Opposite sides parallel and equal', 'yes', 'yes', 'yes', 'yes'], ['All sides equal', 'no', 'no', 'yes', 'yes'], ['All angles $90°$', 'no', 'yes', 'no', 'yes'],
        ['Diagonals bisect each other', 'yes', 'yes', 'yes', 'yes'], ['Diagonals equal', 'no', 'yes', 'no', 'yes'], ['Diagonals perpendicular', 'no', 'no', 'yes', 'yes'],
        ['Diagonals bisect the angles', 'no', 'no', 'yes', 'yes']]),
    T('midseg-t', 'The mid-segment theorem (Theorem 5.11)', 166,
      'The segment joining the midpoints of two sides of a triangle is **parallel** to the third side and **half** as long: if $E$, $F$ are the midpoints of $AB$, $AC$ then $EF \\parallel BC$ and $EF = \\frac12 BC$.',
      '**Proof idea:** extend $EF$ to $D$ with $FD = EF$. Then $\\triangle AEF \\cong \\triangle CDF$ (SAS), so $CD = AE = EB$ and $CD \\parallel AB$. So $BCDE$ is a parallelogram, giving $ED \\parallel BC$ and $ED = BC$, hence $EF = \\frac12 BC$.',
      '**Example 5.7:** joining the three midpoints $D$, $E$, $F$ of the sides of a triangle cuts it into **four congruent triangles**, each similar to the big one with half its sides.'),
    DG('midseg', 'Mid-segment EF', 166, 'midseg'),
    T('ineq-t', 'Triangle inequality (Theorem 5.12)', 170,
      'In every triangle, the sum of any two sides is **greater** than the third side. So three lengths make a triangle only if the two shorter ones add up to more than the longest one.',
      '- $\\{4, 7, 9\\}$: $4 + 7 = 11 > 9$ — a triangle. $\\{3, 8, 12\\}$: $3 + 8 = 11 < 12$ — no triangle.',
      '- If two sides are $3$ and $7$, the third side $x$ satisfies $7 - 3 < x < 7 + 3$, i.e. $4 < x < 10$.'),
    MN('=math10-u5-c01', 'Tip: SSA is a trap', 161,
       'Two sides and an angle that is **not** between them (SSA, "the donkey rule") does **not** prove congruence. The only exception is the right-angle case, which has its own name: RHS. Spell the order out loud: S-A-S has the A in the middle — the angle sits between the sides.'),
    'math10-u5-tbl1', 'math10-u5-wrk1', 'math10-u5-wrk2', 'math10-u5-chkM3', 'math10-u5-l5-1-r3r1', 'math10-u5-l5-1-r3r2', 'math10-u5-chk3',
]

# ------------------------------------------------------------------ 5.2
L52 = [
    T('=math10-u5-c06', '5.2.1 Perimeter of polygons', 171,
      'The **perimeter** of a polygon is the sum of the lengths of its sides (the distance round the edge). For a regular polygon with $n$ sides of length $s$: $P = ns$.',
      '**Example 5.8 idea:** for a shaded region, walk round its boundary and add every piece, including the "inside" edges that are part of the boundary; do not add edges that are not on the boundary.',
      '**Regular polygon inscribed in a circle of radius $r$:** join the centre $O$ to two neighbouring vertices $A$, $B$. Then $\\angle AOB = \\frac{360°}{n}$, and the perpendicular $OE$ bisects $AB$ and the angle, so $AE = r \\sin\\frac{180°}{n}$ and $AB = 2r \\sin\\frac{180°}{n}$:',
      '$$P_{\\text{in}} = 2nr \\sin\\frac{180°}{n}$$',
      '**Regular polygon circumscribed about a circle of radius $r$:** now $OE = r$ is the distance to the side (the **apothem**), so $AE = r\\tan\\frac{180°}{n}$:',
      '$$P_{\\text{out}} = 2nr \\tan\\frac{180°}{n}$$',
      'Check with the hexagon: inscribed $P = 12r \\sin 30° = 6r$ (each side equals $r$); circumscribed $P = 12r\\tan 30° = 4\\sqrt3\\, r$.'),
    DG('regpoly', 'Inscribed and circumscribed hexagons', 173, 'regpoly',
       'Left: $OA = OB = r$ (radius to a vertex). Right: $OE = r$ (radius to the midpoint of a side). That one difference changes $\\sin$ into $\\tan$.'),
    WK('ex-52a', 'Examples 5.9 and 5.10: perimeters of regular polygons', 174,
       'Find the perimeter of (a) a regular decagon inscribed in a circle of radius 5 cm; (b) a regular nonagon circumscribed about a circle of radius 6 cm.',
       ['(a) $n = 10$, $r = 5$: $P = 2(10)(5)\\sin 18° = 100 \\times 0.309 = 30.9$ cm.',
        '(b) $n = 9$, $r = 6$: $P = 2(9)(6)\\tan 20° = 108 \\times 0.364 = 39.3$ cm.',
        'Check: the circumscribed polygon lies outside the circle, so its perimeter is more than the circumference $2\\pi r$: $39.3 > 37.7$. The inscribed one is less: $30.9 < 31.4$.'],
       '(a) $\\approx 30.9$ cm (b) $\\approx 39.3$ cm'),
    T('=math10-u5-c07', '5.2.2 Area of polygons', 177,
      '**Area** is the number of unit squares that cover a region. The basic formulas all come from the rectangle $A = ab$:',
      '- A diagonal cuts a rectangle into two congruent right triangles, so a **right triangle** with legs $a$, $b$ has $A = \\frac12 ab$.',
      '- **Any triangle:** $A = \\frac12 bh$, where $h$ is the altitude to the base $b$ (split it into two right triangles).',
      '- **Two sides and the included angle:** $A = \\frac12 ab \\sin C$ (because the altitude is $h = b \\sin C$).',
      '- **Three sides — Heron’s formula:** with $s = \\frac12(a + b + c)$, $A = \\sqrt{s(s - a)(s - b)(s - c)}$.',
      '- **Parallelogram** $A = bh$; **trapezium** $A = \\frac12(a + b)h$; **rhombus / kite** $A = \\frac12 d_1 d_2$.',
      '- **Equilateral triangle** of side $a$: $h = \\frac{\\sqrt3}{2}a$, $A = \\frac{\\sqrt3}{4}a^2$. **Regular hexagon** of side $s$: six equilateral triangles, $A = \\frac{3\\sqrt3}{2}s^2$.',
      '**Composite figures:** split into triangles and rectangles (often along a diagonal), find any missing lengths with Pythagoras, then add (or subtract cut-out parts).'),
    DG('areas', 'Always use the perpendicular height', 178, 'areas',
       'The height $h$ is always measured at right angles to the base — never along a slanting side.'),
    DG('quadex', 'Example 5.11', 179, 'quadex'),
    WK('ex-52b', 'Example 5.11: area of a quadrilateral with two right triangles', 179,
       'In quadrilateral $ABCD$, $\\angle ADB = 90°$, $\\angle DBC = 90°$, $AB = 15$, $DC = 13$ and $BC = 5$. Find its area.',
       ['In right $\\triangle DBC$: $DB^2 = 13^2 - 5^2 = 169 - 25 = 144$, so $DB = 12$.',
        'In right $\\triangle ADB$: $AD^2 = 15^2 - 12^2 = 225 - 144 = 81$, so $AD = 9$. (The textbook prints 121 and 11 here by mistake.)',
        'Area $= \\frac12(9)(12) + \\frac12(5)(12) = 54 + 30 = 84$.'],
       '$84$ square units'),
    DG('ex512', 'Example 5.12', 181, 'ex512'),
    WK('ex-52c', 'Example 5.12: right triangle plus Heron', 181,
       'In $ABCD$, $\\angle BAD = 90°$, $AB = 6$, $AD = 8$, $BC = 7$, $CD = 5$. Find the area.',
       ['Right $\\triangle ABD$: area $= \\frac12(6)(8) = 24$ and $BD = \\sqrt{36 + 64} = 10$.',
        '$\\triangle BCD$ has sides $10, 7, 5$: $s = \\frac{10 + 7 + 5}{2} = 11$.',
        'Heron: $\\sqrt{11(11 - 10)(11 - 7)(11 - 5)} = \\sqrt{11 \\cdot 1 \\cdot 4 \\cdot 6} = \\sqrt{264} = 2\\sqrt{66} \\approx 16.2$.',
        'Total $= 24 + 2\\sqrt{66} \\approx 40.2$.'],
       '$24 + 2\\sqrt{66} \\approx 40.2$ square units'),
    T('regarea-t', 'Area of regular polygons', 186,
      'Cut a regular $n$-gon into $n$ congruent isosceles triangles with apex at the centre $O$.',
      '- **Inscribed** in a circle of radius $r$: each triangle has two sides $r$ and angle $\\frac{360°}{n}$, so $A = \\frac12 n r^2 \\sin\\frac{360°}{n}$.',
      '- **Circumscribed** about a circle of radius $r$: each triangle has height $r$ and base $2r\\tan\\frac{180°}{n}$, so $A = n r^2 \\tan\\frac{180°}{n}$.',
      '- With the **apothem** $a$ (distance from the centre to a side) and perimeter $P$: $A = \\frac12 aP$.',
      'Examples: hexagon inscribed in $r = 4$: $A = \\frac12(6)(16)\\sin 60° = 24\\sqrt3$ cm². Square circumscribed about $r = 3$: $A = 4(9)\\tan 45° = 36$ cm² (a $6 \\times 6$ square — correct).'),
    TB('reg-t', 'Regular polygon formulas', 188, ['', 'Inscribed in circle radius $r$', 'Circumscribed about circle radius $r$'],
       [['Side', '$2r\\sin\\frac{180°}{n}$', '$2r\\tan\\frac{180°}{n}$'], ['Perimeter', '$2nr\\sin\\frac{180°}{n}$', '$2nr\\tan\\frac{180°}{n}$'],
        ['Area', '$\\frac12 nr^2\\sin\\frac{360°}{n}$', '$nr^2\\tan\\frac{180°}{n}$']]),
    T('=math10-u5-c08', '5.2.3 Arc length, perimeter and area of a sector', 190,
      'A **sector** is the "pizza slice" between two radii and an arc. Its share of the whole circle is $\\frac{\\theta}{360°}$, where $\\theta$ is the central angle. So take that fraction of the circumference or of the area:',
      '$$L = \\frac{\\theta}{360°} \\cdot 2\\pi r = \\frac{\\pi r\\theta}{180°} \\qquad A = \\frac{\\theta}{360°} \\cdot \\pi r^2$$',
      '- **Perimeter of a sector** $= 2r + L$ (two radii plus the arc).',
      '- Shortcut linking them: $A = \\frac12 L r$.',
      '- Semicircle: $\\theta = 180°$; quadrant: $\\theta = 90°$.',
      '**Example 5.16:** $r = 5$, $\\theta = 120°$: $L = \\frac{\\pi \\cdot 5 \\cdot 120}{180} = \\frac{10\\pi}{3} \\approx 10.5$ cm; $P = 10 + \\frac{10\\pi}{3} \\approx 20.5$ cm.',
      '**Example 5.17:** $r = 6$, $\\theta = 45°$: $A = \\frac{45}{360}\\pi(36) = 4.5\\pi \\approx 14.1$ square units.'),
    DG('sector', 'Sector and segment', 190, 'sector',
       'The orange angle is the central angle $\\theta$; $L$ is the arc length. The green region on the right is a segment.'),
    T('=math10-u5-c09', '5.2.4 Area of a segment', 194,
      'A **segment** is the region between a chord and its arc. It is the sector **minus** the triangle formed by the two radii and the chord:',
      '$$A_{\\text{segment}} = \\frac{\\theta}{360°}\\pi r^2 - \\frac12 r^2 \\sin\\theta$$',
      '**Example 5.18:** $r = 5$, $\\theta = 45°$: sector $= \\frac{25\\pi}{8}$, triangle $= \\frac12(25)\\sin 45° = \\frac{25\\sqrt2}{4}$, so segment $= \\frac{25\\pi}{8} - \\frac{25\\sqrt2}{4} \\approx 9.82 - 8.84 = 0.98$ square units.',
      '**Shaded-region problems:** area of the big shape minus the area of what is cut out (e.g. circle minus inscribed rectangle).'),
    WK('ex-52d', 'Worked example: circle minus inscribed rectangle', 196,
       'A $16 \\text{ cm} \\times 12$ cm rectangle is inscribed in a circle. Find the area inside the circle but outside the rectangle.',
       ['The diagonal of an inscribed rectangle is a diameter (angle in a semicircle is $90°$): $d = \\sqrt{16^2 + 12^2} = 20$, so $r = 10$.',
        'Circle area $= 100\\pi \\approx 314.2$ cm².', 'Rectangle area $= 16 \\times 12 = 192$ cm².', 'Difference $= 100\\pi - 192 \\approx 122.2$ cm².'],
       '$100\\pi - 192 \\approx 122.2$ cm²'),
    'math10-u5-xt2', 'math10-u5-pc21', 'math10-u5-chk4', 'math10-u5-wrk4', 'math10-u5-chk1', 'math10-u5-chk2',
]

# ------------------------------------------------------------------ 5.3
L53 = [
    T('=math10-u5-c10', '5.3.1 Surface area and volume of prisms', 197,
      '**Surface area** = the total area of all the faces (how much paper covers the solid; think of its net). **Volume** = the space inside, measured in cubic units ($\\text{cm}^3$, $\\text{m}^3$). $1$ litre $= 1000\\ \\text{cm}^3$ and $1\\ \\text{m}^3 = 1000$ litres.',
      '**Cuboid** $l \\times w \\times h$: lateral area $LA = 2lh + 2wh$; base $B = lw$; total $SA = 2lh + 2wh + 2lw$; volume $V = lwh$.',
      '**Any right prism** with base area $B$, base perimeter $p$ and height $h$:',
      '$$LA = p \\cdot h \\qquad SA = 2B + ph \\qquad V = Bh$$',
      'Why $V = Bh$: one layer of unit cubes on the base holds $B$ cubes, and there are $h$ layers.'),
    DG('cuboid', 'Cuboid and its net', 198, 'cuboid'),
    DG('triprism', 'Example 5.19', 199, 'triprism'),
    WK('ex-53a', 'Example 5.19: surface area of a triangular prism', 199,
       'A right prism has right-triangle bases with legs 3 cm and 4 cm, and the prism is 3 cm long. Find its total surface area and volume.',
       ['Hypotenuse $= \\sqrt{3^2 + 4^2} = 5$ cm.', 'Base area $B = \\frac12(3)(4) = 6$ cm²; two bases $= 12$ cm².',
        'Lateral faces: $3 \\times 3 + 4 \\times 3 + 5 \\times 3 = 36$ cm² (or perimeter $12 \\times 3$).', '$SA = 12 + 36 = 48$ cm².', 'Volume $= Bh = 6 \\times 3 = 18$ cm³.'],
       '$SA = 48$ cm², $V = 18$ cm³'),
    WK('ex-53b', 'Examples 5.21 and 5.22: volumes of prisms', 203,
       '(a) A right prism of height 10 cm has an equilateral-triangle base of side 12 cm. Find its volume. (b) A tank is $120 \\times 80 \\times 50$ cm. How many litres does it hold?',
       ['(a) $B = \\frac12 s^2 \\sin 60° = \\frac12(144)\\frac{\\sqrt3}{2} = 36\\sqrt3$ cm².', '$V = Bh = 360\\sqrt3 \\approx 623.5$ cm³.',
        '(b) $V = 120 \\times 80 \\times 50 = 480\\,000$ cm³.', 'Divide by 1000: $480$ litres.'],
       '(a) $360\\sqrt3 \\approx 623.5$ cm³ (b) $480$ litres'),
    T('=math10-u5-c11', '5.3.2 Cylinders', 207,
      'Cut the curved surface of a cylinder straight down and unroll it: you get a **rectangle** whose length is the circumference $2\\pi r$ and whose width is the height $h$.',
      '$$LA = 2\\pi r h \\qquad SA = 2\\pi r h + 2\\pi r^2 = 2\\pi r(h + r) \\qquad V = \\pi r^2 h$$',
      'The volume rule is the prism rule "base area × height" with base area $\\pi r^2$.',
      '**Open containers** (a cup, a tank without lid) have only one base: $SA = 2\\pi rh + \\pi r^2$.'),
    DG('cylnet', 'Unrolling the curved surface', 208, 'cylnet'),
    WK('ex-53c', 'Examples 5.23 and 5.24: cylinders', 208,
       '(a) Find the total surface area of a cylinder with $r = 14$ cm, $h = 8$ cm. (b) Find the volume of a cylinder with $r = 7$ cm, $h = 20$ cm. Take $\\pi = \\frac{22}{7}$.',
       ['(a) $LA = 2 \\cdot \\frac{22}{7} \\cdot 14 \\cdot 8 = 704$ cm²; $B = \\frac{22}{7} \\cdot 196 = 616$ cm².', '$SA = 704 + 2(616) = 1936$ cm².',
        '(b) $V = \\frac{22}{7} \\cdot 49 \\cdot 20 = 3080$ cm³.'],
       '(a) $1936$ cm² (b) $3080$ cm³'),
    T('=math10-u5-c12', '5.3.3 Pyramids', 210,
      'A **regular pyramid** with an $n$-gon base of side $b$ and slant height $s$ has $n$ congruent triangular faces, each of area $\\frac12 bs$:',
      '$$LA = \\frac12 n b s \\qquad SA = LA + B \\qquad V = \\frac13 Bh$$',
      '- Find a missing slant height with Pythagoras: $s^2 = h^2 + \\left(\\frac{b}{2}\\right)^2$ (square base).',
      '- Why $\\frac13$: a cube can be cut into **three** congruent square pyramids with the same base and height as the cube, so each is one third of the cube.',
      '- Do not mix $h$ (height, used for volume) with $s$ (slant height, used for surface area).'),
    DG('pyrnet', 'Net and slant-height triangle', 211, 'pyrnet'),
    WK('ex-53d', 'Examples 5.25 and 5.26: pyramids', 212,
       '(a) A regular square pyramid has base 10 cm and height 9 cm. Find its total surface area. (b) A regular triangular pyramid has height 12 cm and base edges 8 cm. Find its volume.',
       ['(a) $s = \\sqrt{9^2 + 5^2} = \\sqrt{106} \\approx 10.3$ cm.', '$LA = \\frac12 \\cdot 4 \\cdot 10 \\cdot \\sqrt{106} = 20\\sqrt{106} \\approx 205.9$ cm²; $B = 100$.',
        '$SA = 20\\sqrt{106} + 100 \\approx 305.9$ cm².', '(b) $B = \\frac12(8^2)\\sin 60° = 16\\sqrt3$ cm².', '$V = \\frac13(16\\sqrt3)(12) = 64\\sqrt3 \\approx 110.9$ cm³.'],
       '(a) $\\approx 305.9$ cm² (b) $64\\sqrt3 \\approx 110.9$ cm³'),
    T('=math10-u5-c13', '5.3.4 Cones', 216,
      'Unroll the curved surface of a cone: you get a **sector** of a circle with radius $s$ (the slant height) and arc length $2\\pi r$. Its area is $\\frac12 \\times \\text{arc} \\times \\text{radius} = \\frac12(2\\pi r)s = \\pi rs$.',
      '$$s = \\sqrt{r^2 + h^2} \\qquad LA = \\pi r s \\qquad SA = \\pi r s + \\pi r^2 \\qquad V = \\frac13 \\pi r^2 h$$',
      'A cone holds one third of the cylinder with the same base and height — just as a pyramid holds one third of its prism.'),
    DG('conenet', 'Unrolling a cone gives a sector', 216, 'conenet'),
    WK('ex-53e', 'Examples 5.27 and 5.28: cones', 217,
       '(a) A cone has $r = 6$ cm and $h = 8$ cm. Find its total surface area. (b) A cone has height 12 cm and base diameter 10 cm. Find its volume. Use $\\pi = 3.14$.',
       ['(a) $s = \\sqrt{36 + 64} = 10$ cm.', '$LA = 3.14 \\cdot 6 \\cdot 10 = 188.4$ cm²; $B = 3.14 \\cdot 36 = 113.04$ cm²; $SA = 301.44$ cm².',
        '(b) $r = 5$ cm, $B = 3.14 \\cdot 25 = 78.5$ cm².', '$V = \\frac13(78.5)(12) = 314$ cm³.'],
       '(a) $301.44$ cm² (b) $314$ cm³'),
    T('=math10-u5-c14', '5.3.5 Spheres', 219,
      'Archimedes showed that a sphere of radius $r$ fits exactly in a cylinder of radius $r$ and height $2r$, and:',
      '- the surface of the sphere equals the curved surface of that cylinder: $2\\pi r \\cdot 2r$;',
      '- the sphere fills $\\frac23$ of the cylinder: $\\frac23 \\cdot \\pi r^2 \\cdot 2r$.',
      '$$SA = 4\\pi r^2 \\qquad V = \\frac43 \\pi r^3$$',
      '**Hemisphere** (half a sphere): $V = \\frac23 \\pi r^3$; curved surface $2\\pi r^2$; a solid hemisphere also has a flat circle, so total $3\\pi r^2$.',
      'Watch the diameter: always halve it first.'),
    DG('archimedes', 'Same radius r and height 2r', 218, 'archimedes',
       'Cone : sphere : cylinder $= 1 : 2 : 3$ in volume ($\\frac23\\pi r^3 : \\frac43\\pi r^3 : 2\\pi r^3$).'),
    WK('ex-53f', 'Examples 5.29 and 5.30: spheres', 220,
       '(a) A ball has diameter 14 cm. Find its surface area. (b) A basin is a hemisphere of diameter 42 cm. How many litres does it hold? Take $\\pi = \\frac{22}{7}$.',
       ['(a) $r = 7$: $SA = 4 \\cdot \\frac{22}{7} \\cdot 49 = 616$ cm².', '(b) $r = 21$: $V = \\frac23 \\pi r^3 = \\frac23 \\cdot \\frac{22}{7} \\cdot 9261 = 19\\,404$ cm³.',
        'Divide by 1000: $19.404$ litres. (The textbook’s $6468$ cm³ is one third of this — a slip.)'],
       '(a) $616$ cm² (b) $\\approx 19.4$ litres'),
    TB('solids-t', 'All the solid formulas in one table', 221, ['Solid', 'Lateral / curved area', 'Total surface area', 'Volume'],
       [['Cuboid', '$2h(l + w)$', '$2(lw + lh + wh)$', '$lwh$'], ['Prism', '$ph$', '$ph + 2B$', '$Bh$'], ['Cylinder', '$2\\pi rh$', '$2\\pi rh + 2\\pi r^2$', '$\\pi r^2 h$'],
        ['Pyramid (regular)', '$\\frac12 nbs$', '$\\frac12 nbs + B$', '$\\frac13 Bh$'], ['Cone', '$\\pi rs$', '$\\pi rs + \\pi r^2$', '$\\frac13\\pi r^2 h$'],
        ['Sphere', '—', '$4\\pi r^2$', '$\\frac43\\pi r^3$']],
       'Pattern: pointed solids (pyramid, cone) have $\\frac13$ of the volume of the matching "straight" solid (prism, cylinder).'),
    'math10-u5-chk5', 'math10-u5-wrk5', 'math10-u5-chk6', 'math10-u5-wrk6', 'math10-u5-pc31',
]

LESSONS = {'math10-u5-l5-1': L51, 'math10-u5-l5-2': L52, 'math10-u5-l5-3': L53}

# ------------------------------------------------------------------ practice
a = QSet('5.1 Practice — congruent triangles and quadrilaterals', 's51')
a.S(145, 'Given $\\triangle MQP \\cong \\triangle NOR$, list the six pairs of corresponding equal parts.', '$MQ = NO$, $QP = OR$, $MP = NR$; $\\angle M = \\angle N$, $\\angle Q = \\angle O$, $\\angle P = \\angle R$',
    ['Step 1: match letters in order: $M \\leftrightarrow N$, $Q \\leftrightarrow O$, $P \\leftrightarrow R$.', 'Step 2: sides use pairs of letters in the same positions: $MQ = NO$, $QP = OR$, $MP = NR$.', 'Step 3: angles: $\\angle M = \\angle N$, $\\angle Q = \\angle O$, $\\angle P = \\angle R$.'],
    'Write the two names one above the other and read down the columns.', [('If $\\triangle ABC \\cong \\triangle XYZ$, which side equals $BC$?', '$YZ$.')])
a.M(148, 'In $\\triangle ABC$ and $\\triangle PQR$: $AB = PQ$, $\\angle B = \\angle Q$, $BC = QR$. They are congruent by', ['SSS', 'SAS', 'ASA', 'RHS'], 'B',
    ['Step 1: two pairs of sides match.', 'Step 2: $\\angle B$ lies between $AB$ and $BC$ — the included angle.'],
    'Check where the angle is: between the sides → SAS.', [('$\\angle A = \\angle P$, $AB = PQ$, $\\angle B = \\angle Q$. Test?', 'ASA.')])
a.TF(151, 'If the three angles of one triangle equal the three angles of another, the triangles are congruent.', False,
     ['Step 1: AAA fixes the shape but not the size.', 'Step 2: a $30°$-$60°$-$90°$ triangle with hypotenuse 2 and one with hypotenuse 10 have equal angles but are not congruent.'],
     'At least one side must match for congruence.', [('Is SSA a congruence test?', 'No (except the right-triangle case RHS).')])
a.S(157, 'In right $\\triangle ABC$, $\\angle A = 90°$ and $AB = AC$. Find $\\angle B$ and $\\angle C$.', '$45°$ each',
    ['Step 1: $AB = AC$ → base angles $\\angle B = \\angle C$.', 'Step 2: $\\angle B + \\angle C = 180° - 90° = 90°$, so each is $45°$.'],
    'Isosceles → equal base angles; then use the angle sum.', [('An isosceles triangle has top angle $40°$. Base angles?', '$70°$ each.')])
a.S(152, 'In quadrilateral $ACBD$, $AC = AD$ and $AB$ bisects $\\angle A$. Show $\\triangle ABC \\cong \\triangle ABD$. What about $BC$ and $BD$?', 'Congruent by SAS; $BC = BD$',
    ['Step 1: $AC = AD$ — given.', 'Step 2: $\\angle CAB = \\angle DAB$ — $AB$ bisects $\\angle A$.', 'Step 3: $AB = AB$ — common side.', 'Step 4: SAS, so $BC = BD$ (corresponding sides).'],
    'A shared side is a free "S" in many proofs.', [('$P$ is on the bisector of $\\angle A$; $AX = AY$ on the two arms. Show $PX = PY$.', '$\\triangle AXP \\cong \\triangle AYP$ by SAS.')])
a.S(158, 'Prove that each angle of an equilateral triangle is $60°$.', '$60°$',
    ['Step 1: $AB = AC$ → $\\angle B = \\angle C$; $AB = BC$ → $\\angle A = \\angle C$.', 'Step 2: so all three angles are equal.', 'Step 3: $3x = 180°$, $x = 60°$.'],
    'Use the isosceles theorem twice.', [('Each exterior angle of an equilateral triangle?', '$120°$.')])
a.S(164, 'In parallelogram $ABCD$, $\\angle A = 3x + 10$ and $\\angle B = 2x + 20$ (degrees). Find all four angles.', '$100°, 80°, 100°, 80°$',
    ['Step 1: consecutive angles add up to $180°$: $3x + 10 + 2x + 20 = 180$.', 'Step 2: $5x = 150$, $x = 30$.', 'Step 3: $\\angle A = 100°$, $\\angle B = 80°$; opposite angles equal: $\\angle C = 100°$, $\\angle D = 80°$.'],
    'Neighbours add to $180°$, opposites are equal.', [('In parallelogram $PQRS$, $\\angle P = 65°$. Find $\\angle R$ and $\\angle Q$.', '$65°$ and $115°$.')])
a.M(166, 'Which quadrilateral always has diagonals that are equal AND perpendicular?', ['rectangle', 'rhombus', 'square', 'parallelogram'], 'C',
    ['Step 1: rectangle — equal diagonals, not always perpendicular.', 'Step 2: rhombus — perpendicular, not always equal.', 'Step 3: square — both.'],
    'Use the properties table: the square has every property.', [('Diagonals bisect each other at right angles. Which quadrilateral (at least)?', 'A rhombus.')])
a.S(167, 'In $\\triangle ABC$, $E$ and $F$ are the midpoints of $AB$ and $AC$, and $BC = 14$ cm. Find $EF$.', '$7$ cm',
    ['Step 1: mid-segment theorem: $EF \\parallel BC$ and $EF = \\frac12 BC$.', 'Step 2: $EF = 7$ cm.'],
    'Midpoints of two sides → half the third side.', [('The midpoints of the sides of a triangle with sides 6, 8, 10 are joined. Perimeter of the small triangle?', '12.')])
a.S(171, 'Which of these can be the sides of a triangle: (a) $\\{3, 8, 12\\}$ (b) $\\{4, 7, 9\\}$ (c) $\\{6, 15, 7\\}$?', 'only (b)',
    ['Step 1: compare the two shorter sides with the longest.', 'Step 2: (a) $3 + 8 = 11 < 12$ no; (b) $4 + 7 = 11 > 9$ yes; (c) $6 + 7 = 13 < 15$ no.'],
    'Only one check is needed: the two short sides together must beat the long one.', [('Two sides are 3 cm and 7 cm. Range of the third side?', 'Between 4 cm and 10 cm.')])

b = QSet('5.2 Practice — perimeter and area', 's52')
b.S(177, 'A 36 cm wire is bent into a rectangle with sides $x$ and $2x$. Find $x$ and the area.', '$x = 6$ cm, area $72$ cm²',
    ['Step 1: perimeter $2(x + 2x) = 6x = 36$, so $x = 6$.', 'Step 2: sides 6 and 12, area $= 72$ cm².'],
    'Perimeter first, then area.', [('A 36 cm wire makes an equilateral triangle. Side?', '12 cm.')])
b.S(176, 'Find the perimeter of a regular octagon inscribed in a circle of radius 2 cm.', '$\\approx 12.25$ cm',
    ['Step 1: $P = 2nr\\sin\\frac{180°}{n}$ with $n = 8$, $r = 2$.', 'Step 2: $P = 32 \\sin 22.5° = 32 \\times 0.3827 \\approx 12.25$ cm.'],
    'Inscribed → $\\sin$; circumscribed → $\\tan$.', [('Perimeter of a square circumscribed about a circle of radius 3 cm?', '24 cm ($2 \\cdot 4 \\cdot 3 \\tan 45°$).')])
b.S(183, 'Find the area of an equilateral triangle with side 6 cm.', '$9\\sqrt3 \\approx 15.6$ cm²',
    ['Step 1: $A = \\frac{\\sqrt3}{4}a^2$.', 'Step 2: $\\frac{\\sqrt3}{4} \\cdot 36 = 9\\sqrt3 \\approx 15.6$ cm².'],
    'Or: $\\frac12 ab\\sin C = \\frac12 \\cdot 6 \\cdot 6 \\cdot \\sin 60°$.', [('Area of a regular hexagon with side 4 cm?', '$24\\sqrt3$ cm².')])
b.S(181, 'Use Heron’s formula for the triangle with sides 13, 14, 15.', '$84$',
    ['Step 1: $s = \\frac{13 + 14 + 15}{2} = 21$.', 'Step 2: $A = \\sqrt{21 \\cdot 8 \\cdot 7 \\cdot 6} = \\sqrt{7056} = 84$.'],
    'Compute $s$ first, then the three differences $s - a$, $s - b$, $s - c$.', [('Area of the triangle with sides 3, 4, 5 by Heron?', '$s = 6$, $\\sqrt{6 \\cdot 3 \\cdot 2 \\cdot 1} = 6$.')])
b.S(184, 'A rhombus has diagonals 10 cm and 24 cm. Find its area and its side.', 'area $120$ cm², side $13$ cm',
    ['Step 1: $A = \\frac12 d_1d_2 = \\frac12 \\cdot 10 \\cdot 24 = 120$ cm².', 'Step 2: diagonals bisect at right angles: half-diagonals 5 and 12, side $= \\sqrt{25 + 144} = 13$ cm.'],
    'Rhombus: half the product of the diagonals.', [('A trapezium has parallel sides 8 and 12 and height 5. Area?', '$50$.')])
b.S(188, 'Find the area of a regular hexagon inscribed in a circle of radius 6 cm.', '$54\\sqrt3 \\approx 93.5$ cm²',
    ['Step 1: $A = \\frac12 nr^2\\sin\\frac{360°}{n} = \\frac12 \\cdot 6 \\cdot 36 \\cdot \\sin 60°$.', 'Step 2: $= 108 \\cdot \\frac{\\sqrt3}{2} = 54\\sqrt3 \\approx 93.5$ cm².'],
    'Six equilateral triangles of side $r$.', [('Area of a square inscribed in a circle of radius 5 cm?', '$50$ cm².')])
b.S(193, 'Find the area and perimeter of a sector with radius 6 cm and central angle $120°$.', 'area $12\\pi \\approx 37.7$ cm², perimeter $12 + 4\\pi \\approx 24.6$ cm',
    ['Step 1: area $= \\frac{120}{360}\\pi(36) = 12\\pi$ cm².', 'Step 2: arc $= \\frac{120}{360} \\cdot 2\\pi \\cdot 6 = 4\\pi$ cm.', 'Step 3: perimeter $= 6 + 6 + 4\\pi = 12 + 4\\pi$ cm.'],
    'Fraction of the circle $= \\theta / 360°$.', [('Arc length of a $90°$ sector of radius 10 cm?', '$5\\pi \\approx 15.7$ cm.')])
b.S(193, 'A sector has area $84\\pi$ cm² and central angle $70°$. Find the radius.', '$r = 12\\sqrt3 \\approx 20.8$ cm',
    ['Step 1: $\\frac{70}{360}\\pi r^2 = 84\\pi$; cancel $\\pi$.', 'Step 2: $r^2 = 84 \\cdot \\frac{360}{70} = 12 \\cdot 36 = 432$.', 'Step 3: $r = \\sqrt{432} = 12\\sqrt3 \\approx 20.8$ cm.'],
    'Cancel $\\pi$ first, then solve for $r^2$.', [('A $90°$ sector has area $25\\pi$. Radius?', '$10$.')])
b.S(196, 'In a circle of radius 10 cm, find the area of the segment with central angle $30°$.', '$\\frac{25\\pi}{3} - 25 \\approx 1.18$ cm²',
    ['Step 1: sector $= \\frac{30}{360}\\pi(100) = \\frac{25\\pi}{3} \\approx 26.18$.', 'Step 2: triangle $= \\frac12(100)\\sin 30° = 25$.', 'Step 3: segment $= 26.18 - 25 = 1.18$ cm².'],
    'Segment = sector − triangle.', [('Segment with $r = 6$ and $\\theta = 90°$?', '$9\\pi - 18 \\approx 10.3$.')])
b.S(196, 'An equilateral triangle is inscribed in a circle of radius 4 cm. Find the area inside the circle but outside the triangle.', '$16\\pi - 12\\sqrt3 \\approx 29.5$ cm²',
    ['Step 1: circle $= 16\\pi \\approx 50.27$ cm².', 'Step 2: inscribed triangle $= \\frac12 \\cdot 3 \\cdot 16 \\sin 120° = 12\\sqrt3 \\approx 20.78$ cm².', 'Step 3: difference $\\approx 29.5$ cm².'],
    'Inscribed regular polygon area: $\\frac12 nr^2\\sin\\frac{360°}{n}$.', [('Circle radius 5, inscribed square. Area outside the square?', '$25\\pi - 50 \\approx 28.5$.')])

c = QSet('5.3 Practice — surface area and volume', 's53')
c.S(203, 'A cuboid is 9 cm by 7 cm by 5 cm. Find its volume and total surface area.', '$V = 315$ cm³, $SA = 286$ cm²',
    ['Step 1: $V = 9 \\cdot 7 \\cdot 5 = 315$ cm³.', 'Step 2: $SA = 2(63 + 45 + 35) = 2(143) = 286$ cm².'],
    'Three different face sizes, each counted twice.', [('A cube has edge 4 cm. Volume and surface area?', '$64$ cm³, $96$ cm².')])
c.S(206, 'Biscuits $5 \\times 3 \\times 0.5$ cm are packed into a box $20 \\times 9 \\times 8$ cm. How many fit?', '$192$',
    ['Step 1: along the length $20 \\div 5 = 4$; along the width $9 \\div 3 = 3$; up the height $8 \\div 0.5 = 16$.', 'Step 2: one layer holds $4 \\times 3 = 12$ biscuits; 16 layers hold $12 \\times 16 = 192$.'],
    'Divide each dimension, then multiply — check that the pieces fit exactly.', [('Cubes of 2 cm in a $10 \\times 6 \\times 4$ box?', '$5 \\times 3 \\times 2 = 30$.')])
c.S(209, 'A straw is 24 cm long and 4 mm in diameter. How much liquid can it hold? ($\\pi = 3.14$)', '$\\approx 3.01$ cm³',
    ['Step 1: convert: $r = 2$ mm $= 0.2$ cm.', 'Step 2: $V = \\pi r^2 h = 3.14 \\cdot 0.04 \\cdot 24 \\approx 3.01$ cm³.'],
    'Same units everywhere before you multiply.', [('Volume of a can with diameter 10 cm and height 15 cm?', '$375\\pi \\approx 1177.5$ cm³.')])
c.S(209, 'Cylinder A is 8 times as tall as cylinder B, but B’s diameter is 4 times A’s. Which holds more, and how many times?', 'B, twice as much',
    ['Step 1: let A have $r$, $8h$; B has $4r$, $h$.', 'Step 2: $V_A = \\pi r^2(8h) = 8\\pi r^2h$; $V_B = \\pi(16r^2)h = 16\\pi r^2 h$.', 'Step 3: $V_B = 2V_A$.'],
    'The radius is squared, so it matters more than the height.', [('Doubling the radius of a cylinder multiplies its volume by?', '4.')])
c.S(212, 'A regular square pyramid has base edge 6 cm and slant height 4 cm. Find its total surface area.', '$84$ cm²',
    ['Step 1: four triangles: $4 \\cdot \\frac12 \\cdot 6 \\cdot 4 = 48$ cm².', 'Step 2: base $= 36$ cm².', 'Step 3: $SA = 84$ cm².'],
    'Slant height for faces; height for volume.', [('A pyramid has a $18 \\times 30$ cm base and height 36 cm. Volume?', '$6480$ cm³.')])
c.S(218, 'A cylinder of radius 6 cm and height 18 cm is melted and recast as a cone of radius 9 cm. Find the height of the cone.', '$24$ cm',
    ['Step 1: volume is unchanged: $\\pi(36)(18) = \\frac13\\pi(81)h$.', 'Step 2: $648 = 27h$, $h = 24$ cm.'],
    'Melting and recasting keeps the volume.', [('A cone (radius 3) and cylinder (radius 4) have equal volumes. Ratio of heights cone : cylinder?', '$16 : 3$.')])
c.S(218, 'A cone has radius 5 cm and slant height 13 cm. Find its height, volume and total surface area (leave $\\pi$).', '$h = 12$, $V = 100\\pi$ cm³, $SA = 90\\pi$ cm²',
    ['Step 1: $h = \\sqrt{169 - 25} = 12$ cm.', 'Step 2: $V = \\frac13\\pi(25)(12) = 100\\pi$ cm³.', 'Step 3: $SA = \\pi(5)(13) + \\pi(25) = 65\\pi + 25\\pi = 90\\pi$ cm².'],
    'Find the missing length of the $r$–$h$–$s$ triangle first.', [('Cone $r = 7$, $h = 24$: slant height?', '$25$.')])
c.S(221, 'A balloon is a sphere of diameter 12 cm. Find its volume and surface area (leave $\\pi$).', '$V = 288\\pi$ cm³, $SA = 144\\pi$ cm²',
    ['Step 1: $r = 6$.', 'Step 2: $V = \\frac43\\pi(216) = 288\\pi$ cm³.', 'Step 3: $SA = 4\\pi(36) = 144\\pi$ cm².'],
    'Halve the diameter first.', [('Volume of a ball with diameter 18 cm?', '$972\\pi \\approx 3052$ cm³.')])
c.S(221, 'A ball fits exactly in the smallest cube-shaped box. What percentage of the box does it fill?', '$\\approx 52.4\\%$',
    ['Step 1: box edge $= 2r$, box volume $= 8r^3$.', 'Step 2: ball $= \\frac43\\pi r^3$.', 'Step 3: ratio $= \\frac{\\pi}{6} \\approx 0.524$.'],
    'Use a letter $r$; it cancels.', [('What fraction of the smallest cylinder does a sphere fill?', '$\\frac23$.')])
c.M(221, 'A cylinder, a cone and a sphere each have radius 20 m; the cylinder and cone are 40 m tall. Which holds the most?', ['cone', 'sphere', 'cylinder', 'all equal'], 'C',
    ['Step 1: cylinder $= \\pi(400)(40) = 16000\\pi$.', 'Step 2: cone $= \\frac13$ of that $\\approx 5333\\pi$; sphere $= \\frac43\\pi(8000) \\approx 10667\\pi$.', 'Step 3: ratio $1 : 2 : 3$ — the cylinder is largest.'],
    'Cone : sphere : cylinder = 1 : 2 : 3 when height = diameter.', [('Hemisphere of radius 3 cm: volume?', '$18\\pi$ cm³.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Congruent', 'Same shape and same size.', 144),
    ('Included angle', 'The angle between two given sides of a triangle.', 147),
    ('Included side', 'The side between two given angles of a triangle.', 149),
    ('Hypotenuse', 'The side opposite the right angle.', 160),
    ('Parallelogram', 'A quadrilateral with both pairs of opposite sides parallel.', 162),
    ('Rhombus', 'A parallelogram with all four sides equal.', 166),
    ('Mid-segment', 'The segment joining the midpoints of two sides of a triangle.', 166),
    ('Perimeter', 'The total length of the boundary of a figure.', 171),
    ('Apothem', 'The distance from the centre of a regular polygon to a side.', 189),
    ('Heron’s formula', 'Area = √(s(s − a)(s − b)(s − c)) with s half the perimeter.', 181),
    ('Sector', 'The part of a disc between two radii and an arc.', 190),
    ('Segment (of a circle)', 'The part of a disc between a chord and its arc.', 194),
    ('Lateral surface area', 'The area of the side faces (or curved surface), without the bases.', 198),
    ('Total surface area', 'Lateral area plus the area of the base(s).', 198),
    ('Volume', 'The amount of space a solid takes up, in cubic units.', 200),
    ('Hemisphere', 'Half of a sphere.', 221),
]
TIPS = [
    ('Congruence tests: SSS, SAS, ASA, AAS, RHS. Never AAA or SSA.', 151),
    ('Sector = (θ/360°) of the circle; segment = sector − triangle.', 194),
    ('Pointed solids are one third: pyramid = ⅓Bh, cone = ⅓πr²h. Sphere: 4πr², (4/3)πr³.', 218),
]
IDEAS = [('tests', 'Congruence tests', 'l5_1', 'math10-u5-md-tests-t'), ('quad', 'Quadrilateral properties', 'l5_1', 'math10-u5-md-quad-t'),
         ('reg', 'Regular polygon formulas', 'l5_2', 'math10-u5-md-reg-t'), ('solids', 'Solid formulas', 'l5_3', 'math10-u5-md-solids-t')]
