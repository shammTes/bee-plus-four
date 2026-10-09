r"""Grade 10 Unit 4 — Dimensionality and Geometry of Location: solids, nets and views, coordinate geometry,
reflection / translation / dilation (pp. 106-142)."""
from common import set_unit, T, RM, MN, TB, DG, GR, WK, CK, QSet, plane
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL, polar, mid, lerp
from figs_common import side_by_side

UID = 'math10-u4'
set_unit(UID)

LIGHT = '#EAF1F8'
MIDF = '#C9DBEC'
TOPF = '#F4F8FC'


# ------------------------------------------------------------------ drawing helpers
def ell(f, cx, cy, rx, ry, c=INK, w=2, back='dash', fill=None):
    """horizontal ellipse seen from slightly above: front half solid, back half dashed (back='dash'), solid, or none"""
    if fill:
        f.ellipse(cx, cy, rx, ry, 'none', 0, fill)
    f.path(f'M{cx - rx} {cy} A{rx} {ry} 0 0 0 {cx + rx} {cy}', c, w)
    if back == 'dash':
        f.path(f'M{cx - rx} {cy} A{rx} {ry} 0 0 1 {cx + rx} {cy}', c, 1.4, dash=True)
    elif back == 'solid':
        f.path(f'M{cx - rx} {cy} A{rx} {ry} 0 0 1 {cx + rx} {cy}', c, w)


def cube(f, x, y, s, d=(16, -12), c=INK):
    """opaque oblique cube, front face top-left corner (x, y)"""
    dx, dy = d
    f.poly([(x, y), (x + dx, y + dy), (x + s + dx, y + dy), (x + s, y)], c, 1.6, TOPF)
    f.poly([(x + s, y), (x + s + dx, y + dy), (x + s + dx, y + s + dy), (x + s, y + s)], c, 1.6, MIDF)
    f.rect(x, y, s, s, c, 1.6, LIGHT)


def cyl(f, cx, top, bot, rx, ry, c=INK):
    f.rect(cx - rx, top, 2 * rx, bot - top, 'none', 0, LIGHT)
    f.ellipse(cx, bot, rx, ry, 'none', 0, LIGHT)
    f.line(cx - rx, top, cx - rx, bot, c, 2).line(cx + rx, top, cx + rx, bot, c, 2)
    ell(f, cx, bot, rx, ry, c)
    f.ellipse(cx, top, rx, ry, c, 2, TOPF)


def cone(f, cx, apex, base, rx, ry, c=INK):
    f.poly([(cx, apex), (cx - rx, base), (cx + rx, base)], 'none', 0, LIGHT)
    f.ellipse(cx, base, rx, ry, 'none', 0, LIGHT)
    f.line(cx, apex, cx - rx, base, c, 2).line(cx, apex, cx + rx, base, c, 2)
    ell(f, cx, base, rx, ry, c)


# ------------------------------------------------------------------ figures 4.1
def f_solids():
    f = Fig(330, 262)
    f.text(165, 16, 'Polyhedrons: only flat faces', 12.5, BLUE)
    f.text(165, 142, 'Not polyhedrons: a curved surface', 12.5, RED)
    # cube
    cube(f, 22, 46, 50)
    # triangular prism
    x0 = 130
    A, B, C = (x0, 98), (x0 + 52, 98), (x0 + 24, 50)
    d = (34, -16)
    A2, B2, C2 = [(p[0] + d[0], p[1] + d[1]) for p in (A, B, C)]
    f.poly([C, C2, B2, B], 'none', 0, MIDF)
    f.poly([A, B, C], INK, 1.8, LIGHT)
    f.line(*C, *C2, INK, 1.8).line(*B, *B2, INK, 1.8).line(*C2, *B2, INK, 1.8)
    f.line(*A, *A2, INK, 1.3, dash=True).line(*A2, *B2, INK, 1.3, dash=True).line(*A2, *C2, INK, 1.3, dash=True)
    # square pyramid
    x0 = 230
    P = [(x0, 104), (x0 + 58, 104), (x0 + 82, 84), (x0 + 24, 84)]
    apex = (x0 + 41, 36)
    f.poly([P[0], P[1], apex], 'none', 0, LIGHT).poly([P[1], P[2], apex], 'none', 0, MIDF)
    f.poly([P[0], P[1], P[2]], INK, 1.8, closed=False)
    f.line(*P[2], *P[3], INK, 1.3, dash=True).line(*P[3], *P[0], INK, 1.3, dash=True).line(*P[3], *apex, INK, 1.3, dash=True)
    for p in P[:3]:
        f.line(*p, *apex, INK, 1.8)
    for x, s in ((60, 'cube'), (165, 'triangular prism'), (272, 'square pyramid')):
        f.text(x, 124, s, 11.5, INK)
    # cylinder, cone, sphere
    cyl(f, 58, 172, 222, 30, 9)
    cone(f, 165, 158, 222, 32, 9)
    f.circle(272, 192, 34, INK, 2, LIGHT)
    ell(f, 272, 192, 34, 10, INK)
    for x, s in ((58, 'cylinder'), (165, 'cone'), (272, 'sphere')):
        f.text(x, 252, s, 11.5, INK)
    return f


def f_prism():
    f = Fig(330, 214)
    A, C, B = (30, 196), (150, 196), (200, 166)
    up = 140
    A1, B1, C1 = [(p[0], p[1] - up) for p in (A, B, C)]
    D, E, F = [(p[0], p[1] - 66) for p in (A, B, C)]
    f.poly([A, C, C1, A1], 'none', 0, LIGHT).poly([C, B, B1, C1], 'none', 0, MIDF)
    f.poly([D, F, E], PURPLE, 2, FILL[PURPLE], dash=True)
    f.poly([A1, B1, C1], INK, 2, TOPF)
    f.line(*A, *C, INK, 2).line(*C, *B, INK, 2)
    f.line(*A, *B, INK, 1.3, dash=True)
    for a, b in ((A, A1), (B, B1), (C, C1)):
        f.line(*a, *b, ORANGE, 2.2)
    for p, l, pos in ((A, 'A', 'sw'), (B, 'B', 'e'), (C, 'C', 's'), (A1, "A'", 'nw'), (B1, "B'", 'ne'), (C1, "C'", 'n'),
                      (D, 'D', 'w'), (E, 'E', 'e'), (F, 'F', 'sw')):
        f.ptlabel(*p, l, pos, PURPLE if l in 'DEF' else INK, 12)
    f.text(230, 40, 'upper base', 12, BLUE, 'start')
    f.text(230, 104, 'cross-section', 12, PURPLE, 'start').text(230, 119, 'DEF', 12, PURPLE, 'start')
    f.text(230, 170, 'lower base', 12, BLUE, 'start')
    f.text(230, 146, 'lateral edges', 12, ORANGE, 'start')
    f.text(90, 168, 'lateral face', 11.5, GREEN)
    return f


def f_pyramid():
    f = Fig(330, 214)
    P = [(30, 180), (180, 180), (240, 130), (90, 130)]
    apex = (135, 24)
    foot = (135, 155)
    m = mid(P[0], P[1])
    f.poly([P[0], P[1], apex], 'none', 0, LIGHT).poly([P[1], P[2], apex], 'none', 0, MIDF)
    f.line(*P[2], *P[3], INK, 1.3, dash=True).line(*P[3], *P[0], INK, 1.3, dash=True).line(*P[3], *apex, INK, 1.3, dash=True)
    f.poly([P[0], P[1], P[2]], INK, 2, closed=False)
    for p in P[:3]:
        f.line(*p, *apex, INK, 2)
    f.line(*apex, *foot, RED, 2, dash=True)
    f.line(*apex, *m, ORANGE, 2.2)
    f.right(m, apex, P[1], 8, ORANGE)
    f.dot(*apex, INK, 3).dot(*foot, RED, 3)
    f.text(135, 15, 'apex', 12, INK)
    f.text(141, 140, 'h', 13, RED, 'start', italic=True)
    f.text(250, 50, 'altitude h', 12, RED, 'start')
    f.text(250, 68, 'slant height', 12, ORANGE, 'start')
    f.text(52, 96, 'lateral', 11.5, GREEN, 'end').text(52, 110, 'edge', 11.5, GREEN, 'end')
    f.text(105, 198, 'base edge', 12, BLUE)
    f.text(250, 160, 'base', 12, BLUE, 'start')
    return f


def f_frustum():
    a = Fig(150, 160)
    B = [(10, 140), (100, 140), (135, 112), (45, 112)]
    k = 0.45
    c = (72.5, 126)
    apex = (72.5, 10)
    T_ = [lerp(p, apex, 0.55) for p in B]
    a.poly([B[0], B[1], T_[1], T_[0]], 'none', 0, LIGHT).poly([B[1], B[2], T_[2], T_[1]], 'none', 0, MIDF)
    a.poly([B[0], B[1], B[2]], INK, 2, closed=False)
    a.line(*B[2], *B[3], INK, 1.3, dash=True).line(*B[3], *B[0], INK, 1.3, dash=True).line(*B[3], *T_[3], INK, 1.3, dash=True)
    a.poly(T_, INK, 2, TOPF)
    for i in range(3):
        a.line(*B[i], *T_[i], INK, 2)
    a.line(*mid(T_[0], T_[2]), *c, RED, 1.6, dash=True)
    a.text(c[0] + 6, 100, 'h', 13, RED, 'start', italic=True)
    b = Fig(150, 160)
    b.poly([(28, 54), (122, 54), (138, 128), (12, 128)], 'none', 0, LIGHT)
    b.ellipse(75, 128, 63, 14, 'none', 0, LIGHT)
    b.line(28, 54, 12, 128, INK, 2).line(122, 54, 138, 128, INK, 2)
    ell(b, 75, 128, 63, 14)
    b.ellipse(75, 54, 47, 11, INK, 2, TOPF)
    b.line(75, 54, 75, 128, RED, 1.6, dash=True)
    b.text(81, 98, 'h', 13, RED, 'start', italic=True)
    return side_by_side([a, b], 16, ['frustum of a pyramid', 'frustum of a cone'])


def f_cylcone():
    f = Fig(330, 200)
    cyl(f, 80, 40, 160, 50, 14)
    f.line(80, 40, 80, 160, RED, 1.6, dash=True)
    f.line(80, 160, 130, 160, BLUE, 2).dot(80, 160, INK, 3).dot(80, 40, INK, 3)
    f.text(105, 154, 'r', 13, BLUE, italic=True)
    f.text(86, 104, 'h', 13, RED, 'start', italic=True)
    f.text(80, 192, 'cylinder', 12, INK)
    cone(f, 245, 22, 160, 55, 15)
    f.line(245, 22, 245, 160, RED, 1.6, dash=True)
    f.line(245, 160, 300, 160, BLUE, 2).dot(245, 160, INK, 3)
    f.right((245, 160), (245, 22), (300, 160), 8, INK)
    f.line(245, 22, 300, 160, ORANGE, 3)
    f.text(272, 154, 'r', 13, BLUE, italic=True)
    f.text(239, 104, 'h', 13, RED, 'end', italic=True)
    f.text(282, 86, 'l', 13, ORANGE, 'start', italic=True)
    f.text(245, 14, 'vertex', 11.5, INK)
    f.text(245, 192, 'cone (l = slant height)', 12, INK)
    return f


def f_sphere():
    f = Fig(330, 200)
    O = (90, 100)
    r = 72
    f.circle(*O, r, INK, 2, LIGHT)
    ell(f, O[0], O[1], r, 16, RED)
    yE = O[1] - 44
    hw = (r * r - 44 * 44) ** 0.5
    ell(f, O[0], yE, hw, 10, GREEN)
    f.line(O[0], O[1] - r - 8, O[0], O[1] + r + 8, INK, 1.3, dash=True)
    f.dot(*O, INK, 3).ptlabel(*O, 'O', 'se', INK, 12)
    f.ptlabel(O[0], O[1] - r, 'A', 'ne', INK, 12).ptlabel(O[0], O[1] + r, 'B', 'se', INK, 12)
    f.dot(O[0] + r, O[1], RED, 3).ptlabel(O[0] + r, O[1], 'C', 'e', RED, 12)
    f.text(50, 196, 'great circle', 11.5, RED).text(140, 196, 'small circle', 11.5, GREEN)
    # cross-section
    O2 = (250, 120)
    R = 62
    s, t = 36, (62 ** 2 - 36 ** 2) ** 0.5
    f.circle(*O2, R, INK, 2)
    f.line(O2[0] - t, O2[1] - s, O2[0] + t, O2[1] - s, GREEN, 2.4)
    f.line(*O2, O2[0], O2[1] - s, BLUE, 2).line(*O2, O2[0] + t, O2[1] - s, RED, 2)
    f.right((O2[0], O2[1] - s), O2, (O2[0] + t, O2[1] - s), 7)
    f.dot(*O2, INK, 3)
    f.text(O2[0] - 6, O2[1] - 14, 's', 13, BLUE, 'end', italic=True)
    f.text(O2[0] + t / 2, O2[1] - s - 6, 't', 13, GREEN, italic=True)
    f.text(O2[0] + t / 2 + 8, O2[1] - 8, 'r', 13, RED, italic=True)
    f.text(250, 40, 't² = r² − s²', 13, INK)
    return f


def f_nets():
    s = 26
    a = Fig(4 * s + 8, 3 * s + 8)
    for i in range(4):
        a.rect(4 + i * s, 4 + s, s, s, BLUE, 1.6, LIGHT)
    a.rect(4 + s, 4, s, s, BLUE, 1.6, TOPF).rect(4 + s, 4 + 2 * s, s, s, BLUE, 1.6, TOPF)
    b = Fig(4 * s + 8, 3 * s + 8)
    for i, j in ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2)):
        b.rect(4 + i * s, 4 + j * s, s, s, GREEN, 1.6, FILL[GREEN])
    c = Fig(96, 3 * s + 8)
    h = 76
    P, Q, R = (6, 4 + h), (90, 4 + h), (48, 4)
    c.poly([P, Q, R], ORANGE, 1.8, FILL[ORANGE])
    c.poly([mid(P, Q), mid(Q, R), mid(R, P)], ORANGE, 1.6)
    return side_by_side([a, b, c], 12, ['cube net', 'another cube net', 'tetrahedron net'])


def f_views():
    f = Fig(330, 170)
    s = 40
    x, y = 20, 110
    cube(f, x, y - s, s, (18, -13))
    cube(f, x + s, y - s, s, (18, -13))
    cube(f, x, y - 2 * s, s, (18, -13))
    f.text(70, 150, 'solid of 3 cubes', 11.5, INK)
    q = 20
    # front view
    fx, fy = 150, 70
    for i, j in ((0, 0), (1, 0), (0, 1)):
        f.rect(fx + i * q, fy + 40 - j * q, q, q, RED, 1.6, FILL[RED])
    f.text(fx + q, 150, 'front', 11.5, RED)
    # side view (from the right)
    sx = 215
    for j in (0, 1):
        f.rect(sx, fy + 40 - j * q, q, q, GREEN, 1.6, FILL[GREEN])
    f.text(sx + q / 2, 150, 'side', 11.5, GREEN)
    # top view
    tx = 265
    for i in (0, 1):
        f.rect(tx + i * q, fy + 40, q, q, BLUE, 1.6, FILL[BLUE])
    f.line(tx, fy + 40, tx + q, fy + 40, BLUE, 1.6)
    f.text(tx + q, 150, 'top', 11.5, BLUE)
    return f


# ------------------------------------------------------------------ figures 4.2
def f_quadrants():
    p = Plot(-5, 5, -4, 4, unit=29)
    p.text(p.X(-2.5), p.Y(3.1), 'Quadrant II', 12, PURPLE).text(p.X(-2.5), p.Y(2.5), '(−, +)', 12, PURPLE)
    p.text(p.X(1.6), p.Y(3.1), 'Quadrant I', 12, BLUE).text(p.X(1.6), p.Y(2.5), '(+, +)', 12, BLUE)
    p.text(p.X(-2.5), p.Y(-2.6), 'Quadrant III', 12, GREEN).text(p.X(-2.5), p.Y(-3.2), '(−, −)', 12, GREEN)
    p.text(p.X(2.6), p.Y(-2.6), 'Quadrant IV', 12, ORANGE).text(p.X(2.6), p.Y(-3.2), '(+, −)', 12, ORANGE)
    p.seg((4, 1), (4, 0), RED, 1.6, dash=True).seg((4, 1), (0, 1), RED, 1.6, dash=True)
    p.pt(4, 1, 'P(4, 1)', 'ne', RED)
    p.pt(4, 0, 'M', 's', INK, r=3).pt(0, 1, 'N', 'nw', INK, r=3)
    return p


def f_distance():
    p = Plot(-1, 7, -1, 6, unit=36)
    P, R, Q = (1, 5), (6, 5), (6, 1)
    p.ppoly([P, R, Q], INK, FILL[GREY], 1.4)
    p.seg(P, R, BLUE, 3).seg(R, Q, GREEN, 3).seg(P, Q, RED, 3)
    p.right(p.P(*R), p.P(*P), p.P(*Q), 9)
    p.pt(*P, 'P', 'nw', INK).pt(*R, 'R', 'ne', INK).pt(*Q, 'Q', 'se', INK)
    p.text(p.X(3.5), p.Y(5) - 8, '|x₂ − x₁|', 12, BLUE)
    p.text(p.X(6) + 6, p.Y(3) + 4, '|y₂ − y₁|', 12, GREEN, 'start')
    p.text(p.X(2.6), p.Y(2.6), 'd', 15, RED, italic=True)
    return p


def f_midpoint():
    p = Plot(-1, 8, -1, 6, unit=34, labels=False)
    P1, P2, M = (1, 1), (7, 5), (4, 3)
    for (x, y) in (P1, P2, M):
        p.seg((x, y), (x, 0), GREY, 1.3, dash=True).seg((x, y), (0, y), GREY, 1.3, dash=True)
    p.seg(P1, P2, BLUE, 3)
    p.pt(*P1, 'P₁', 'se', BLUE).pt(*P2, 'P₂', 'nw', BLUE).pt(*M, 'P', 'nw', RED)
    p.pt(1, 0, 'R₁', 's', INK, r=3).pt(4, 0, 'R', 's', RED, r=3).pt(7, 0, 'R₂', 's', INK, r=3)
    p.pt(0, 1, 'S₁', 'w', INK, r=3).pt(0, 3, 'S', 'w', RED, r=3).pt(0, 5, 'S₂', 'w', INK, r=3)
    return p


# ------------------------------------------------------------------ figures 4.3
def f_reflect_line():
    f = Fig(320, 190)
    l0, l1 = (60, 180), (260, 10)
    f.line(*l0, *l1, BLUE, 2.4)
    f.text(266, 20, 'l', 15, BLUE, 'start', italic=True)
    # P and its image Q: line direction
    import math
    dx, dy = l1[0] - l0[0], l1[1] - l0[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    O = lerp(l0, l1, 0.48)
    P = (O[0] - 70 * nx, O[1] - 70 * ny)
    Q = (O[0] + 70 * nx, O[1] + 70 * ny)
    f.line(*P, *Q, INK, 1.6, dash=True)
    f.right(O, P, l1, 9, INK)
    f.ticks(P, O, 1, RED).ticks(O, Q, 1, RED)
    f.dot(*P, RED).ptlabel(*P, 'P', 'w', RED)
    f.dot(*Q, GREEN).ptlabel(*Q, "P'", 'e', GREEN)
    f.dot(*O, INK, 3).ptlabel(*O, 'O', 'se', INK, 12)
    C = lerp(l0, l1, 0.15)
    f.dot(*C, PURPLE).ptlabel(*C, "C = C'", 'w', PURPLE, 12)
    return f


def f_reflect_xy():
    p = Plot(-4, 4, -4, 4, unit=34)
    p.fullline(1, 0, c=GREY, w=1.6, dash=True).fullline(-1, 0, c=GREY, w=1.6, dash=True)
    p.text(p.X(3.6), p.Y(3.95) + 4, 'y = x', 11, GREY, 'end')
    p.text(p.X(-3.6), p.Y(3.95) + 4, 'y = −x', 11, GREY, 'start')
    p.pt(3, 2, 'P(3, 2)', 'e', RED)
    p.pt(3, -2, 'A', 'e', BLUE).pt(-3, 2, 'B', 'w', GREEN).pt(2, 3, 'C', 'n', PURPLE).pt(-3, -2, 'D', 'w', ORANGE).pt(-2, -3, 'E', 's', INK)
    return p


def f_translate():
    p = Plot(-5, 5, -3, 5, unit=30)
    A, B, C = (-4, -2), (-1, -2), (-4, 1)
    v = (5, 3)
    A1, B1, C1 = [(x + v[0], y + v[1]) for x, y in (A, B, C)]
    p.ppoly([A, B, C], BLUE, FILL[BLUE])
    p.ppoly([A1, B1, C1], GREEN, FILL[GREEN])
    for a, b in ((A, A1), (B, B1), (C, C1)):
        p.arrow(*p.P(*a), *p.P(*b), ORANGE, 1.6, 7)
    p.pt(*A, 'A', 'sw', BLUE).pt(*B, 'B', 'se', BLUE).pt(*C, 'C', 'nw', BLUE)
    p.pt(*A1, "A'", 'se', GREEN).pt(*B1, "B'", 'se', GREEN).pt(*C1, "C'", 'nw', GREEN)
    return p


def f_dilation():
    f = Fig(320, 200)
    O = (24, 182)
    A, B, C = (84, 150), (130, 162), (96, 112)
    k = 2
    A1, B1, C1 = [(O[0] + k * (p[0] - O[0]), O[1] + k * (p[1] - O[1])) for p in (A, B, C)]
    for p in (A1, B1, C1):
        f.line(*O, *p, GREY, 1.3, dash=True)
    f.poly([A1, B1, C1], GREEN, 2.2, FILL[GREEN])
    f.poly([A, B, C], BLUE, 2.2, FILL[BLUE])
    f.dot(*O, RED).ptlabel(*O, 'O', 'n', RED)
    for p, l, pos in ((A, 'A', 'nw'), (B, 'B', 's'), (C, 'C', 'w'), (A1, "A'", 'nw'), (B1, "B'", 'e'), (C1, "C'", 'nw')):
        f.ptlabel(*p, l, pos, GREEN if "'" in l else BLUE, 12)
    f.text(316, 30, "OA' = 2 × OA", 12, INK, 'end')
    f.text(316, 48, "A'B' = 2 × AB", 12, INK, 'end')
    f.text(316, 66, 'scale factor r = 2', 12, RED, 'end')
    return f


def f_symmetry():
    a = Fig(80, 80)
    a.poly([(40, 6), (10, 74), (70, 74)], BLUE, 2, FILL[BLUE])
    a.line(40, 0, 40, 80, RED, 1.4, dash=True)
    b = Fig(96, 80)
    b.rect(10, 18, 76, 46, BLUE, 2, FILL[BLUE])
    b.line(48, 8, 48, 74, RED, 1.4, dash=True).line(2, 41, 94, 41, RED, 1.4, dash=True)
    c = Fig(80, 80)
    pts = [polar((40, 40), 34, 30 + 60 * i) for i in range(6)]
    c.poly(pts, BLUE, 2, FILL[BLUE])
    for i in range(3):
        c.line(*polar((40, 40), 40, 30 + 60 * i), *polar((40, 40), 40, 210 + 60 * i), RED, 1.2, dash=True)
        c.line(*polar((40, 40), 38, 60 * i), *polar((40, 40), 38, 180 + 60 * i), RED, 1.2, dash=True)
    d = Fig(80, 80)
    d.circle(40, 40, 32, BLUE, 2, FILL[BLUE])
    for ang in (0, 30, 60, 90, 120, 150):
        d.line(*polar((40, 40), 38, ang), *polar((40, 40), 38, ang + 180), RED, 1.1, dash=True)
    return side_by_side([a, b, c, d], 8, ['1 axis', '2 axes', '6 axes', 'infinitely many'])


DIAGRAMS = {
    'solids': (f_solids(), 'Polyhedrons and solids with curved surfaces', 107),
    'prism': (f_prism(), 'Parts of a triangular prism and a cross-section', 109),
    'pyramid': (f_pyramid(), 'Parts of a rectangular pyramid', 111),
    'frustum': (f_frustum(), 'Frustums: the top is cut off parallel to the base', 112),
    'cylcone': (f_cylcone(), 'Right cylinder and right cone', 114),
    'sphere': (f_sphere(), 'Sphere: great and small circles; a cross-section', 116),
    'nets': (f_nets(), 'Nets fold into solids', 117),
    'views': (f_views(), 'Front, side and top views of a solid made of cubes', 120),
    'quadrants': (f_quadrants(), 'The four quadrants and the coordinates of a point', 123),
    'distance': (f_distance(), 'The distance formula is Pythagoras on the grid', 126),
    'midpoint': (f_midpoint(), 'Midpoint: average the x’s and average the y’s', 130),
    'reflectline': (f_reflect_line(), 'Reflection in a line l', 135),
    'reflectxy': (f_reflect_xy(), 'Images of P(3, 2) under five reflections', 137),
    'translate': (f_translate(), 'Translation by (5, 3)', 139),
    'dilation': (f_dilation(), 'Dilation with centre O and scale factor 2', 140),
    'symmetry': (f_symmetry(), 'Lines (axes) of symmetry', 134),
}

# ------------------------------------------------------------------ 4.1
L41 = [
    T('=math10-u4-c03', '4.1.1 Plane figures, solids and polyhedrons', 107,
      '**Plane figures** (triangles, squares, circles …) have only length and width, so they are **two-dimensional (2-D)**. A **solid** has length, width **and** height, so it is **three-dimensional (3-D)** and occupies space. A solid is an enclosed part of space bounded by plane (flat) or curved surfaces.',
      'A **polyhedron** (plural polyhedrons or polyhedra) is a solid bounded by **flat polygon faces only**. The faces meet in line segments called **edges**, and the edges meet at points called **vertices**.',
      '- Cubes, prisms and pyramids are polyhedrons.',
      '- Cylinders, cones and spheres are **not** polyhedrons: each has a curved surface.',
      'A polyhedron is **regular** when all its faces are congruent regular polygons **and** the same number of faces meet at every vertex. Examples: the cube (6 squares) and the regular tetrahedron (4 equilateral triangles).',
      '**Smallest polyhedron:** you need at least 4 faces to close up space, so 3 triangles can never make a polyhedron, but 4 triangles can (a tetrahedron), and one square with 4 triangles makes a square pyramid.'),
    DG('solids', 'Which solids are polyhedrons?', 107, 'solids',
       'Dashed lines are edges hidden at the back. A solid is a polyhedron only when **every** face is flat.'),
    T('prism-t', 'Prisms', 109,
      'A **prism** has two congruent, parallel faces called the **bases**; the other faces (**lateral faces**) are parallelograms joining corresponding sides of the bases. The edges joining the two bases are the **lateral edges**; they are all parallel and equal.',
      '- A prism is named after its base: triangular prism, rectangular prism, pentagonal prism, hexagonal prism …',
      '- **Right prism:** the lateral edges are perpendicular to the bases, so the lateral faces are rectangles. Otherwise the prism is **oblique**.',
      '- A **rectangular solid** (cuboid) is a prism bounded by six rectangles; a **cube** is a rectangular solid bounded by six squares. A square prism is a cube only if its height equals the side of the square.',
      'A **cross-section** of a prism is where a plane **parallel to the base** cuts the prism.',
      '**Theorem 4.1:** every cross-section of a triangular prism is congruent to the base. **Theorem 4.2:** the upper and lower bases are congruent. **Theorem 4.3:** all cross-sections of any prism have the same area.',
      'The union of the lateral faces is the **lateral surface**; lateral faces plus both bases make the **total surface**.'),
    DG('prism', 'A right triangular prism', 109, 'prism',
       'The purple cross-section $DEF$ is parallel to the base, so $\\triangle DEF \\cong \\triangle ABC \\cong \\triangle A\'B\'C\'$.'),
    T('pyr-t', 'Pyramids and frustums', 111,
      'A **pyramid** has one polygon **base** and triangular **lateral faces** that meet at a common vertex, the **apex**. It is named after its base (triangular, square, pentagonal … pyramid).',
      '- **Lateral edges:** where two lateral faces meet (from the apex to a base corner).',
      '- **Altitude:** the perpendicular segment from the apex to the base; its length is the **height** $h$.',
      '- **Slant height:** the altitude of a lateral face drawn from the apex (from the apex to the midpoint of a base edge).',
      '- **Regular pyramid:** the base is a regular polygon and the foot of the altitude is the centre of the base. Then all lateral faces are congruent isosceles triangles.',
      'A **tetrahedron** is a pyramid with a triangular base: 4 triangular faces, 3 meeting at each vertex.',
      'If a plane parallel to the base cuts off the top of a pyramid, the part left is a **frustum**. Its two bases are similar polygons and its lateral faces are **trapezoids**.'),
    DG('pyramid', 'Parts of a rectangular pyramid', 111, 'pyramid',
       'Height and slant height are different: the height goes straight down to the base (inside the pyramid), the slant height runs down the middle of a face. The slant height is always the longer one.'),
    WK('ex-41a', 'Worked example: height, slant height and lateral edge', 111,
       'A regular square pyramid has base edge $12$ cm and height $8$ cm. Find the slant height and the length of a lateral edge.',
       ['Draw the right triangle: apex, centre of the base, midpoint of a base edge. Its legs are the height $8$ and half the base edge $6$.',
        'Slant height $s = \\sqrt{8^2 + 6^2} = \\sqrt{100} = 10$ cm.',
        'Now the right triangle: apex, midpoint of a base edge, a corner. Its legs are the slant height $10$ and half the edge $6$.',
        'Lateral edge $= \\sqrt{10^2 + 6^2} = \\sqrt{136} \\approx 11.66$ cm.'],
       'slant height $10$ cm, lateral edge $\\sqrt{136} \\approx 11.7$ cm'),
    DG('frustum', 'Frustums', 112, 'frustum'),
    T('=math10-u4-c04', '4.1.2 Cylinders, cones and spheres', 113,
      'A **cylinder** has two parallel, congruent circular bases and a curved **lateral surface** joining them. If the segment joining the centres of the bases (the **axis**) is perpendicular to the bases, it is a **right cylinder**. Every horizontal cross-section is a circle congruent to the base — just like a prism, which is why cylinder and prism share the volume rule "base area × height".',
      'A **cone** has a circular base and a lateral surface that comes to a point, the **vertex**. The **altitude** (height $h$) goes from the vertex perpendicular to the base; the **slant height** $l$ goes from the vertex to the edge of the base. In a right cone $l^2 = r^2 + h^2$. A cone is to a cylinder what a pyramid is to a prism. Cutting a cone parallel to its base leaves a **frustum of a cone**.',
      'A **sphere** is the set of all points in space at the same distance $r$ (the radius) from a fixed point $O$ (the centre). It is formed by rotating a semicircle about its diameter. A **great circle** is a cross-section through the centre (radius $r$); any other cross-section is a **small circle**.',
      'A circle is flat (2-D); a sphere is solid (3-D). Do not mix them up.'),
    DG('cylcone', 'Height, radius and slant height', 114, 'cylcone',
       'For the cone the height $h$, the radius $r$ and the slant height $l$ make a right triangle: $l = \\sqrt{r^2 + h^2}$.'),
    DG('sphere', 'Cross-sections of a sphere', 116, 'sphere',
       'A cross-section at distance $s$ from the centre is a circle of radius $t$ with $t^2 = r^2 - s^2$ (Pythagoras). Its area is $\\pi t^2 = \\pi(r^2 - s^2)$ — the same as the area of a ring (**annulus**) between circles of radius $r$ and $s$.'),
    WK('ex-41b', 'Worked example: cross-section of a sphere', 116,
       'A sphere has radius $13$ cm. A plane cuts it $5$ cm from the centre. Find the radius and the area of the cross-section.',
       ['The radius of the sphere, the distance from the centre and the radius of the section form a right triangle: $t^2 = r^2 - s^2$.',
        '$t^2 = 13^2 - 5^2 = 169 - 25 = 144$, so $t = 12$ cm.',
        'Area $= \\pi t^2 = 144\\pi \\approx 452.4$ cm².'],
       '$t = 12$ cm, area $= 144\\pi \\approx 452$ cm²'),
    T('=math10-u4-c05', '4.1.3 Nets and views of solids', 117,
      'A **net** is a flat (2-D) figure that can be folded into a solid. Every face of the solid appears exactly once in the net, and no two faces overlap after folding.',
      '- A cube has 6 square faces, so a cube net has 6 squares. There are exactly **11** different cube nets. A row of 4 squares with one square above and one below (anywhere) always works.',
      '- A tetrahedron net is 4 triangles, for example one large triangle split into 4 by joining the midpoints of its sides.',
      '- A cylinder net: two circles and a rectangle whose length is the circumference $2\\pi r$. A cone net: a circle and a sector.',
      '**Test a net:** pick one square as the bottom and fold the others up in your head. If two squares land on the same face, it is not a net (for example 6 squares in a row, or a $2 \\times 3$ block).',
      'A 3-D solid can also be described by its **views**: the **front view**, the **side view** (from the right) and the **top view** (plan), each drawn as a flat figure.',
      '- Upright cylinder: front and side views rectangles, top view a circle.',
      '- Square pyramid: front and side views triangles, top view a square with its diagonals.',
      '- Cone: front view a triangle, top view a circle with its centre marked.'),
    DG('nets', 'Nets', 117, 'nets'),
    DG('views', 'Views of a solid made of cubes', 120, 'views',
       'Count squares: from the front you see an L of 3 squares; from the right only 2 stacked squares (the right-hand cube hides the left column); from the top 2 squares in a row.'),
    RM('=math10-u4-c02', 'Euler’s formula', 119,
       'For every polyhedron (without holes) the numbers of faces $F$, vertices $V$ and edges $E$ satisfy',
       '$$F + V - E = 2$$',
       'Prism with an $n$-sided base: $F = n + 2$, $V = 2n$, $E = 3n$. Pyramid with an $n$-sided base: $F = n + 1$, $V = n + 1$, $E = 2n$. In both cases $F + V - E = 2$.'),
    TB('euler-t', 'Counting faces, vertices and edges', 119, ['Solid', '$F$', '$V$', '$E$', '$F + V - E$'],
       [['Rectangular solid', '6', '8', '12', '2'], ['Square pyramid', '5', '5', '8', '2'], ['Triangular prism', '5', '6', '9', '2'],
        ['Hexagonal prism', '8', '12', '18', '2'], ['Triangular pyramid', '4', '4', '6', '2'], ['Pentagonal pyramid', '6', '6', '10', '2']]),
    WK('ex-41c', 'Worked example: using Euler’s formula', 119,
       'A polyhedron has $12$ vertices and $30$ edges. How many faces does it have?',
       ['Write Euler’s formula: $F + V - E = 2$.', 'Substitute: $F + 12 - 30 = 2$.', 'Solve: $F = 2 + 30 - 12 = 20$.'],
       '$20$ faces (this is the regular icosahedron)'),
    'math10-u4-tbl1', 'math10-u4-chk7c1', 'math10-u4-chk7c2', 'math10-u4-l4-1-r3r1', 'math10-u4-wrk7c1', 'math10-u4-wrk7c2',
]

# ------------------------------------------------------------------ 4.2
L42 = [
    T('=math10-u4-c06', '4.2.1 Coordinates in a plane', 122,
      'On a number line the distance between two numbers $a$ and $b$ is $|b - a|$, e.g. between $-3$ and $9$: $|9 - (-3)| = 12$ units.',
      'Two perpendicular number lines, the **x-axis** (horizontal) and the **y-axis** (vertical), meet at the **origin** $O(0, 0)$ and make the **coordinate plane** (xy-plane). The axes divide the plane into four **quadrants**, numbered anticlockwise starting top-right.',
      'To find the coordinates of a point $P$: drop a perpendicular to the x-axis (foot $M$, number $a$) and to the y-axis (foot $N$, number $b$). Then $P = (a, b)$. The first number is the **x-coordinate (abscissa)**, the second the **y-coordinate (ordinate)**. Order matters: $(4, 1) \\ne (1, 4)$ — that is why it is called an **ordered pair**.',
      '- Points on the x-axis have $y = 0$: $(4, 0)$. Points on the y-axis have $x = 0$: $(0, 9)$.',
      '- Signs: I $(+, +)$, II $(-, +)$, III $(-, -)$, IV $(+, -)$.'),
    DG('quadrants', 'Quadrants and coordinates', 123, 'quadrants'),
    GR('ex44', 'Example 4.4: triangle P(0, 0), Q(5, 0), R(0, 12)', 124,
       plane(-1, 7, -1, 13, points=[{'x': 0, 'y': 0, 'label': 'P'}, {'x': 5, 'y': 0, 'label': 'Q(5, 0)'}, {'x': 0, 'y': 12, 'label': 'R(0, 12)'}],
             polygons=[{'pts': [[0, 0], [5, 0], [0, 12]], 'color': '#2F5F8F'}]),
       'The legs lie on the axes: $PQ = 5$, $PR = 12$, and the angle at $P$ is a right angle.',
       '**Area** $= \\frac12 \\times 5 \\times 12 = 30$ square units. **Hypotenuse** $QR = \\sqrt{5^2 + 12^2} = \\sqrt{169} = 13$, so the **perimeter** $= 5 + 12 + 13 = 30$ units.'),
    T('=math10-u4-c07', '4.2.2 Distance between two points', 125,
      '**Same horizontal line** ($y$ equal): distance $= |x_2 - x_1|$. **Same vertical line** ($x$ equal): distance $= |y_2 - y_1|$. Example: $P(2, 4)$, $Q(2, 10)$ → $PQ = 6$.',
      '**General case:** for $P(x_1, y_1)$ and $Q(x_2, y_2)$ draw the right triangle $PRQ$ with $R(x_2, y_1)$. Then $PR = |x_2 - x_1|$ and $RQ = |y_2 - y_1|$, and Pythagoras gives',
      '$$PQ = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$',
      '- The order of the points does not matter, because $(x_1 - x_2)^2 = (x_2 - x_1)^2$.',
      '- Distance is never negative; take the positive square root.',
      '- Write brackets around negative numbers: $2 - (-1) = 3$.',
      '**Uses:** prove a triangle is isosceles (two equal sides), equilateral (three equal sides) or right-angled (converse of Pythagoras: $a^2 + b^2 = c^2$ for the longest side $c$); test collinearity (the two short distances add up to the long one).'),
    DG('distance', 'Why the distance formula works', 126, 'distance',
       'The horizontal leg is the change in $x$, the vertical leg is the change in $y$; the distance is the hypotenuse.'),
    WK('ex-42a', 'Worked example: distance and type of triangle', 127,
       'Do $P(3, 2)$, $Q(-2, -3)$ and $R(2, 3)$ form a triangle? If so, what type?',
       ['$PQ = \\sqrt{(-2 - 3)^2 + (-3 - 2)^2} = \\sqrt{25 + 25} = \\sqrt{50}$.',
        '$QR = \\sqrt{(2 - (-2))^2 + (3 - (-3))^2} = \\sqrt{16 + 36} = \\sqrt{52}$.',
        '$PR = \\sqrt{(2 - 3)^2 + (3 - 2)^2} = \\sqrt{2}$.',
        'Sum of the two shorter sides $\\sqrt{50} + \\sqrt2 \\approx 8.49 > \\sqrt{52} \\approx 7.21$, so it is a triangle.',
        'Check Pythagoras on the squares: $PQ^2 + PR^2 = 50 + 2 = 52 = QR^2$, so the angle at $P$ is $90°$.'],
       'Yes — a right-angled triangle (right angle at $P$)',
       graph=plane(-3, 4, -4, 4, points=[{'x': 3, 'y': 2, 'label': 'P'}, {'x': -2, 'y': -3, 'label': 'Q'}, {'x': 2, 'y': 3, 'label': 'R'}],
                   polygons=[{'pts': [[3, 2], [-2, -3], [2, 3]], 'color': '#2F5F8F'}])),
    WK('ex-42b', 'Worked example: isosceles triangle', 127,
       'Show that $P(-2, 3)$, $Q(3, 8)$, $R(4, 1)$ form an isosceles triangle.',
       ['$PQ = \\sqrt{(3 + 2)^2 + (8 - 3)^2} = \\sqrt{25 + 25} = \\sqrt{50}$.',
        '$QR = \\sqrt{(4 - 3)^2 + (1 - 8)^2} = \\sqrt{1 + 49} = \\sqrt{50}$.',
        '$PR = \\sqrt{(4 + 2)^2 + (1 - 3)^2} = \\sqrt{36 + 4} = \\sqrt{40}$.',
        '$PQ = QR$, so two sides are equal.'],
       'isosceles, with $PQ = QR = \\sqrt{50}$'),
    WK('ex-42c', 'Worked example: a point on the x-axis equidistant from two points', 128,
       'Find the point on the x-axis that is the same distance from $A(2, -5)$ and $B(-2, 9)$.',
       ['A point on the x-axis is $P(x, 0)$.',
        'Set the squared distances equal (no square roots needed): $(x - 2)^2 + (0 + 5)^2 = (x + 2)^2 + (0 - 9)^2$.',
        'Expand: $x^2 - 4x + 4 + 25 = x^2 + 4x + 4 + 81$.',
        'The $x^2$ cancel: $-4x + 29 = 4x + 85$, so $-8x = 56$, $x = -7$.',
        'Check: $PA^2 = 81 + 25 = 106$, $PB^2 = 25 + 81 = 106$. Equal.'],
       '$(-7, 0)$'),
    T('=math10-u4-c08', '4.2.3 Midpoint of a line segment', 129,
      'The **midpoint** $M$ of $P_1P_2$ is the point of the segment halfway between the ends. Its coordinates are the **averages** of the end coordinates:',
      '$$M = \\left(\\frac{x_1 + x_2}{2}, \\frac{y_1 + y_2}{2}\\right)$$',
      '**Why:** drop perpendiculars from $P_1$, $P$, $P_2$ to the x-axis ($R_1$, $R$, $R_2$). Parallel lines cut equal pieces, so $R$ is the midpoint of $R_1R_2$ and its number is $\\frac{x_1 + x_2}{2}$. In the same way $S$ on the y-axis gives $\\frac{y_1 + y_2}{2}$.',
      '- Horizontal segment $(x_1, y)$ to $(x_2, y)$: midpoint $\\left(\\frac{x_1 + x_2}{2}, y\\right)$. Vertical: $\\left(x, \\frac{y_1 + y_2}{2}\\right)$.',
      '- Examples: $(0, 3)$ and $(0, 8)$ → $\\left(0, \\frac{11}{2}\\right)$; $(-4, 4)$ and $(3, -2)$ → $\\left(-\\frac12, 1\\right)$.',
      '**Missing endpoint:** if $M$ and $A$ are known, $B = (2x_M - x_A, 2y_M - y_A)$ — "double the midpoint, subtract the known end".',
      '**Do not confuse:** distance **subtracts** and squares (gives a number); midpoint **adds** and halves (gives a point).'),
    DG('midpoint', 'Deriving the midpoint formula', 130, 'midpoint'),
    RM('=math10-u4-c01', 'Distance and midpoint formulas', 129,
       'For $A(x_1, y_1)$ and $B(x_2, y_2)$:',
       '$$AB = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2} \\qquad M = \\left(\\frac{x_1 + x_2}{2}, \\frac{y_1 + y_2}{2}\\right)$$',
       'Distance: subtract, square, add, square-root — the answer is a **number**. Midpoint: add and halve — the answer is a **point**.'),
    'math10-u4-wk2',
    WK('ex-42d', 'Worked example: parallelogram from midpoints', 141,
       '$A(1, 2)$, $B(4, y)$, $C(x, 6)$ and $D(3, 5)$ are the vertices of a parallelogram taken in order. Find $x$ and $y$.',
       ['The diagonals of a parallelogram bisect each other, so $AC$ and $BD$ have the same midpoint.',
        'Midpoint of $AC = \\left(\\frac{1 + x}{2}, \\frac{2 + 6}{2}\\right) = \\left(\\frac{1 + x}{2}, 4\\right)$.',
        'Midpoint of $BD = \\left(\\frac{4 + 3}{2}, \\frac{y + 5}{2}\\right) = \\left(\\frac72, \\frac{y + 5}{2}\\right)$.',
        'Compare: $\\frac{1 + x}{2} = \\frac72 \\Rightarrow x = 6$; $\\frac{y + 5}{2} = 4 \\Rightarrow y = 3$.'],
       '$x = 6$, $y = 3$'),
    WK('ex-42e', 'Worked example: collinear points', 141,
       'Are $A(1, 5)$, $B(2, 3)$ and $C(-2, 11)$ collinear?',
       ['Slope $AB = \\frac{3 - 5}{2 - 1} = -2$.', 'Slope $AC = \\frac{11 - 5}{-2 - 1} = \\frac{6}{-3} = -2$.',
        'Same slope through the common point $A$, so the three points lie on one line.',
        'Distance check: $AB = \\sqrt5$, $AC = \\sqrt{45} = 3\\sqrt5$, $BC = \\sqrt{80} = 4\\sqrt5$, and $\\sqrt5 + 3\\sqrt5 = 4\\sqrt5$.'],
       'Yes, they are collinear'),
    'math10-u4-l4-2-r2r1', 'math10-u4-pc21', 'math10-u4-pc22', 'math10-u4-pc23', 'math10-u4-chk7c3',
]

# ------------------------------------------------------------------ 4.3
L43 = [
    T('=math10-u4-c09', 'Transformations of the plane', 131,
      'A **transformation** of the plane is a one-to-one mapping of the whole plane onto itself: every point $P$ has exactly one **image** $P\'$, and every point is the image of exactly one point (its **pre-image**).',
      'In this unit: **reflection** (flip in a mirror line or a point), **translation** (slide) and **dilation** (enlarge or shrink from a centre).',
      '- Reflections and translations keep every length and angle: the image is **congruent** to the figure. They are **rigid motions** (isometries).',
      '- A dilation keeps angles and shape but multiplies all lengths by the scale factor $r$: the image is **similar** to the figure.'),
    T('=math10-u4-c11', '4.3.1 Reflection', 135,
      'A **reflection in a line $l$** maps a point $P$ to the point $P\'$ such that $l$ is the **perpendicular bisector** of $PP\'$: $PP\' \\perp l$ and $P$ and $P\'$ are the same distance from $l$, on opposite sides. A point on $l$ is its own image.',
      'Like a mirror: your image is as far behind the mirror as you are in front of it.',
      '- A reflection keeps distances: $A\'B\' = AB$. It reverses orientation (clockwise becomes anticlockwise).',
      '- A figure is **symmetric about $l$** if reflecting it in $l$ gives the same figure; $l$ is an **axis (line) of symmetry**.'),
    DG('reflectline', 'Reflection in a line', 135, 'reflectline',
       '$l$ is the perpendicular bisector of $PP\'$: right angle at $O$ and $PO = OP\'$. $C$ is on the mirror, so $C\' = C$.'),
    DG('symmetry', 'Axes of symmetry', 134, 'symmetry',
       'Isosceles triangle 1, rectangle 2, regular hexagon 6 (a regular $n$-gon has $n$), circle infinitely many (every diameter). A scalene triangle has none.'),
    T('refl-coord', 'Reflections on the coordinate plane', 137,
      'Use the rule — no drawing needed:',
      '- in the **x-axis**: $(x, y) \\to (x, -y)$ (change the sign of $y$)',
      '- in the **y-axis**: $(x, y) \\to (-x, y)$ (change the sign of $x$)',
      '- in the line **$y = x$**: $(x, y) \\to (y, x)$ (swap)',
      '- in the line **$y = -x$**: $(x, y) \\to (-y, -x)$ (swap and change both signs)',
      '- in the **origin** (point reflection): $(x, y) \\to (-x, -y)$. $O$ is the midpoint of $PP\'$.',
      '**Why $y = x$ swaps:** the midpoint $\\left(\\frac{x + x\'}{2}, \\frac{y + y\'}{2}\\right)$ lies on $y = x$, and $PP\'$ has slope $-1$ (perpendicular to slope $1$). Solving the two equations gives $x\' = y$, $y\' = x$.'),
    DG('reflectxy', 'Five reflections of P(3, 2)', 137, 'reflectxy',
       '$A(3, -2)$ in the x-axis, $B(-3, 2)$ in the y-axis, $C(2, 3)$ in $y = x$, $D(-3, -2)$ in the origin, $E(-2, -3)$ in $y = -x$.'),
    TB('refl-t', 'Reflection rules', 137, ['Reflect in', 'Rule', '$P(3, 2) \\to$'],
       [['x-axis', '$(x, y) \\to (x, -y)$', '$(3, -2)$'], ['y-axis', '$(x, y) \\to (-x, y)$', '$(-3, 2)$'], ['$y = x$', '$(x, y) \\to (y, x)$', '$(2, 3)$'],
        ['$y = -x$', '$(x, y) \\to (-y, -x)$', '$(-2, -3)$'], ['origin', '$(x, y) \\to (-x, -y)$', '$(-3, -2)$']]),
    WK('ex-43a', 'Worked example: two reflections, two orders', 138,
       'Reflect $(2, -3)$ in the line $y = -x$ and then in the x-axis. Then do it in the opposite order. Is the result the same?',
       ['In $y = -x$: $(x, y) \\to (-y, -x)$, so $(2, -3) \\to (3, -2)$.', 'Then in the x-axis: $(3, -2) \\to (3, 2)$.',
        'Opposite order: x-axis first, $(2, -3) \\to (2, 3)$; then $y = -x$: $(2, 3) \\to (-3, -2)$.',
        '$(3, 2) \\ne (-3, -2)$: the order matters.'],
       '$(3, 2)$ one way, $(-3, -2)$ the other way'),
    T('=math10-u4-c12', '4.3.2 Translation', 139,
      'A **translation** slides every point the **same distance in the same direction**. It is described by where it takes the origin: if $T(0, 0) = (m, n)$ then',
      '$$T: (x, y) \\to (x + m, y + n)$$',
      '- "Translation by $(3, 7)$" means add 3 to $x$ and 7 to $y$.',
      '- If $T$ takes $(a, b)$ to $(c, d)$, then $T$ moves every point by $(c - a, d - b)$; in particular $T(0, 0) = (c - a, d - b)$.',
      '- **Pre-image:** go backwards — subtract: the pre-image of $(4, 9)$ under translation by $(3, 7)$ is $(1, 2)$.',
      '- "1 to the left and 2 down" means translation by $(-1, -2)$.',
      'The image of a figure is congruent to it and points the same way (no flip, no turn).'),
    DG('translate', 'A translation', 139, 'translate',
       'All the arrows $AA\'$, $BB\'$, $CC\'$ are equal and parallel: each point moves 5 right and 3 up.'),
    WK('ex-43b', 'Worked example: find the translation, then use it', 139,
       'A translation takes $(2, 3)$ to $(3, -4)$. Where does it take $(0, 0)$, $(2, -1)$ and $(1, 0)$?',
       ['Movement $= (3 - 2, -4 - 3) = (1, -7)$: one right, seven down.', '$(0, 0) \\to (1, -7)$.', '$(2, -1) \\to (3, -8)$.', '$(1, 0) \\to (2, -7)$.'],
       '$(1, -7)$, $(3, -8)$, $(2, -7)$'),
    'math10-u4-wk3',
    GR('wk3-gr', 'Translate then reflect (the worked example above)', 131,
       plane(-3, 5, -7, 7, polygons=[{'pts': [[1, 2], [4, 2], [1, 5]], 'color': '#2F5F8F'}, {'pts': [[-2, 3], [1, 3], [-2, 6]], 'color': '#2A7A6B'},
                                     {'pts': [[-2, -3], [1, -3], [-2, -6]], 'color': '#C0392B'}]),
       'Blue: $ABC$. Green: after the translation by $(-3, 1)$. Red: after the reflection in the x-axis. All three triangles are congruent.'),
    T('=math10-u4-c13', '4.3.3 Dilation', 140,
      'A **dilation** with centre $O$ and **scale factor** $r > 0$ maps each point $P$ to the point $P\'$ on ray $OP$ with $OP\' = r \\cdot OP$. Then every length is multiplied by $r$: $P_1\'P_2\' = r \\cdot P_1P_2$.',
      '- $r > 1$: **expansion** (enlargement), the figure grows.',
      '- $0 < r < 1$: **contraction** (reduction), a scale model.',
      '- $r = 1$: every point stays where it is (a rigid motion).',
      'Angles do not change, so the image is **similar** to the original. Areas are multiplied by $r^2$.',
      '**With centre at the origin:** $(x, y) \\to (rx, ry)$.',
      '**To draw a dilation:** draw rays from $O$ through each vertex, measure $OA$, mark $A\'$ at $r \\times OA$ along the ray, then join the images.'),
    DG('dilation', 'Expansion with r = 2', 140, 'dilation'),
    WK('ex-43c', 'Worked example: a contraction (Example 4.8)', 141,
       'Triangle $RST$ has $R(-6, -3)$, $S(6, -3)$, $T(0, 6)$. Find its image under the dilation with centre $O(0, 0)$ and scale factor $\\frac23$.',
       ['Centre at the origin, so multiply both coordinates by $\\frac23$.', '$R\' = \\left(\\frac23 \\cdot (-6), \\frac23 \\cdot (-3)\\right) = (-4, -2)$.',
        '$S\' = (4, -2)$ and $T\' = (0, 4)$.', 'Check lengths: $RS = 12$, $R\'S\' = 8 = \\frac23 \\times 12$.'],
       '$R\'(-4, -2)$, $S\'(4, -2)$, $T\'(0, 4)$',
       graph=plane(-7, 7, -4, 7, polygons=[{'pts': [[-6, -3], [6, -3], [0, 6]], 'color': '#2F5F8F'}, {'pts': [[-4, -2], [4, -2], [0, 4]], 'color': '#2A7A6B'}],
                   points=[{'x': 0, 'y': 0, 'label': 'O', 'color': '#C0392B'}])),
    TB('trans-cmp', 'Comparing the transformations', 141, ['', 'Reflection', 'Translation', 'Dilation (factor r)'],
       [['Lengths', 'kept', 'kept', 'multiplied by $r$'], ['Angles', 'kept', 'kept', 'kept'], ['Image is', 'congruent (flipped)', 'congruent (same direction)', 'similar'],
        ['Fixed points', 'the mirror line', 'none (unless no move)', 'the centre $O$'], ['Coordinate rule', 'see the table above', '$(x + m, y + n)$', '$(rx, ry)$ for centre $O$']]),
    'math10-u4-tb3',
    MN('=math10-u4-c10', 'Tip: remember the rules by one example', 139,
       'Learn every rule on the single point $(3, 2)$: x-axis $(3, -2)$, y-axis $(-3, 2)$, $y = x$ $(2, 3)$, origin $(-3, -2)$. If you forget a rule in the exam, sketch $(3, 2)$ and its mirror image — the picture gives the rule back.'),
    'math10-u4-pc31', 'math10-u4-pc32', 'math10-u4-pc33',
]

LESSONS = {'math10-u4-l4-1': L41, 'math10-u4-l4-2': L42, 'math10-u4-l4-3': L43}

# ------------------------------------------------------------------ practice
a = QSet('4.1 Practice — solids, nets and views', 's41')
a.M(112, 'Which set of faces can form a polyhedron?', ['3 triangles', '2 squares', '4 triangles', '1 circle and 1 triangle'], 'C',
    ['Step 1: a polyhedron needs at least 4 flat faces to close up space.', 'Step 2: 4 triangles make a tetrahedron (triangular pyramid). A circle is not a polygon.'],
    'Count faces first: fewer than 4 can never enclose space.', [('Can a square and four triangles be the faces of a polyhedron?', 'Yes — a square pyramid.')])
a.TF(108, 'A cylinder is a polyhedron.', False,
     ['Step 1: a polyhedron is bounded by flat polygon faces only.', 'Step 2: a cylinder has a curved lateral surface and circular bases, so it is not a polyhedron.'],
     'Any curved surface → not a polyhedron.', [('Is a hexagonal prism a polyhedron?', 'Yes — all 8 faces are flat polygons.')])
a.S(119, 'A pentagonal prism: find $F$, $V$, $E$ and verify Euler’s formula.', '$F = 7$, $V = 10$, $E = 15$; $7 + 10 - 15 = 2$',
    ['Step 1: prism with $n = 5$: faces $= n + 2 = 7$ (2 bases + 5 lateral faces).', 'Step 2: vertices $= 2n = 10$ (5 on each base).',
     'Step 3: edges $= 3n = 15$ (5 + 5 on the bases, 5 lateral).', 'Step 4: $7 + 10 - 15 = 2$.'],
    'Prism with $n$-gon base: $F = n + 2$, $V = 2n$, $E = 3n$.', [('Find $F$, $V$, $E$ for an octagonal pyramid.', '$F = 9$, $V = 9$, $E = 16$; $9 + 9 - 16 = 2$.')])
a.S(119, 'A polyhedron has 8 faces and 6 vertices. How many edges?', '12',
    ['Step 1: $F + V - E = 2$.', 'Step 2: $8 + 6 - E = 2$, so $E = 12$.'],
    'Put the two numbers you know into $F + V - E = 2$ and solve.', [('A polyhedron has 6 faces and 12 edges. How many vertices?', '8.')])
a.S(111, 'A regular square pyramid has base edge 10 cm and slant height 13 cm. Find its height.', '12 cm',
    ['Step 1: right triangle with hypotenuse = slant height 13 and one leg = half the base edge 5.', 'Step 2: $h = \\sqrt{13^2 - 5^2} = \\sqrt{144} = 12$ cm.'],
    'Height, half-edge and slant height form a right triangle; the slant height is the hypotenuse.', [('Base edge 16 cm, height 6 cm. Slant height?', '$\\sqrt{36 + 64} = 10$ cm.')])
a.S(114, 'A right cone has radius 5 cm and height 12 cm. Find its slant height.', '13 cm',
    ['Step 1: $l^2 = r^2 + h^2 = 25 + 144 = 169$.', 'Step 2: $l = 13$ cm.'],
    'Slant height is always the hypotenuse.', [('Slant height 10 cm, radius 6 cm. Height?', '8 cm.')])
a.S(116, 'A sphere of radius 10 cm is cut by a plane 6 cm from the centre. Find the radius of the cross-section.', '8 cm',
    ['Step 1: $t^2 = r^2 - s^2 = 100 - 36 = 64$.', 'Step 2: $t = 8$ cm.'],
    'Draw the right triangle: sphere radius is the hypotenuse.', [('Where is the cross-section of largest area?', 'Through the centre ($s = 0$): a great circle.')])
a.M(117, 'Which arrangement of 6 squares is NOT a net of a cube?', ['A row of 4 with one square above and one below', 'Six squares in a row', 'A "staircase" 2-2-2', 'A row of 3, then a row of 3 shifted by 2'], 'B',
    ['Step 1: fold a row of 4: the 4 squares go round the cube.', 'Step 2: squares 5 and 6 of a straight row would land on the same faces as squares 1 and 2 — the top and bottom stay open.'],
    'A cube net never has 5 or more squares in one row.', [('How many different cube nets are there?', '11.')])
a.S(120, 'Name the solid: front view a triangle, side view a triangle, top view a square with its diagonals.', 'A square pyramid',
    ['Step 1: top view a square → square base.', 'Step 2: triangles from the front and side → faces slope up to a point, and the diagonals in the plan are the edges to the apex.'],
    'Start with the top view: it shows the shape of the base.', [('Front view rectangle, top view circle?', 'A cylinder.')])
a.F(114, 'A cone is to a cylinder as a ____ is to a prism.', 'pyramid', ['pyramid', 'sphere', 'cube', 'frustum'],
    ['Step 1: a cylinder and a prism have two equal bases.', 'Step 2: cutting the top to a point turns a cylinder into a cone and a prism into a pyramid.'],
    'Think "two bases" vs "one base and an apex".', [('The part of a cone left after cutting off the top parallel to the base is a …', 'frustum of a cone.')])

b = QSet('4.2 Practice — coordinates, distance and midpoint', 's42')
b.S(124, 'In which quadrant or on which axis is each point: $(2, 4)$, $(-2, -3)$, $(1, -9)$, $(0, 1)$, $(4, 0)$?', 'I, III, IV, y-axis, x-axis',
    ['Step 1: look at the signs: $(+, +)$ I, $(-, -)$ III, $(+, -)$ IV.', 'Step 2: a zero coordinate puts the point on an axis: $x = 0$ → y-axis, $y = 0$ → x-axis.'],
    'Signs give the quadrant; a zero gives an axis.', [('If $a < 0$ and $b > 0$, where is $(-a, -b)$?', '$-a > 0$, $-b < 0$: quadrant IV.')])
b.S(128, 'Find the distance between $(1, -2)$ and $(-3, 4)$.', '$2\\sqrt{13} \\approx 7.21$',
    ['Step 1: $\\Delta x = -3 - 1 = -4$, $\\Delta y = 4 - (-2) = 6$.', 'Step 2: $d = \\sqrt{16 + 36} = \\sqrt{52} = 2\\sqrt{13}$.'],
    'Square the differences — the minus signs disappear.', [('Distance between $(5, 4)$ and $(-1, 2)$?', '$\\sqrt{40} = 2\\sqrt{10}$.')])
b.M(128, 'The distance between $(-3, 2)$ and $(6, 2)$ is', ['3', '9', '81', '$\\sqrt{13}$'], 'B',
    ['Step 1: same $y$ → horizontal segment.', 'Step 2: distance $= |6 - (-3)| = 9$.'],
    'Same $y$: subtract the x’s; same $x$: subtract the y’s.', [('Distance between $(5, 4)$ and $(5, -9)$?', '13.')])
b.S(128, 'Show that $A(1, 1)$, $B(4, 3)$, $C(4, 1)$ form a right-angled triangle.', '$AC^2 + BC^2 = 9 + 4 = 13 = AB^2$',
    ['Step 1: $AC = 3$ (horizontal), $BC = 2$ (vertical), $AB = \\sqrt{9 + 4} = \\sqrt{13}$.', 'Step 2: $3^2 + 2^2 = 13 = AB^2$, so the angle at $C$ is $90°$.'],
    'Compare the sum of the two smaller squares with the largest square.', [('Is the triangle $(0, 0)$, $(3, 0)$, $(0, 4)$ right-angled?', 'Yes: $9 + 16 = 25 = 5^2$.')])
b.S(128, 'Show that $(5, -2)$, $(6, 4)$ and $(7, -2)$ are the vertices of an isosceles triangle.', 'Two sides equal $\\sqrt{37}$',
    ['Step 1: $(5, -2)$ to $(6, 4)$: $\\sqrt{1 + 36} = \\sqrt{37}$.', 'Step 2: $(6, 4)$ to $(7, -2)$: $\\sqrt{1 + 36} = \\sqrt{37}$.', 'Step 3: $(5, -2)$ to $(7, -2)$: $2$. Two sides are equal.'],
    'Compute all three sides, then compare.', [('Is $(0, 0)$, $(4, 0)$, $(2, 2\\sqrt3)$ equilateral?', 'Yes: all sides are 4.')])
b.S(131, 'Find the midpoint of $(-6, 5)$ and $(7, 2)$.', '$\\left(\\frac12, \\frac72\\right)$',
    ['Step 1: $x = \\frac{-6 + 7}{2} = \\frac12$.', 'Step 2: $y = \\frac{5 + 2}{2} = \\frac72$.'],
    'Midpoint = average of the x’s, average of the y’s.', [('Midpoint of $(7, 11)$ and $(7, -13)$?', '$(7, -1)$.')])
b.S(131, 'The midpoint of a segment is $(3, 2)$ and one endpoint is $(-5, 12)$. Find the other endpoint.', '$(11, -8)$',
    ['Step 1: other end $= (2 \\cdot 3 - (-5), 2 \\cdot 2 - 12)$.', 'Step 2: $= (6 + 5, 4 - 12) = (11, -8)$.', 'Step 3: check: average of $-5$ and $11$ is 3; of 12 and $-8$ is 2.'],
    'Double the midpoint, subtract the known end.', [('Midpoint $(0, 0)$, one end $(4, -7)$. Other end?', '$(-4, 7)$.')])
b.S(141, 'Are $(1, 5)$, $(2, 3)$ and $(-2, 11)$ collinear?', 'Yes',
    ['Step 1: slope of the first two: $\\frac{3 - 5}{2 - 1} = -2$.', 'Step 2: slope of the first and third: $\\frac{11 - 5}{-2 - 1} = -2$.', 'Step 3: equal slopes through a common point → collinear.'],
    'Collinear = same slope (or the short distances add up to the long one).', [('Are $(0, 0)$, $(1, 2)$, $(3, 5)$ collinear?', 'No: slopes 2 and $\\frac53$.')])
b.S(141, 'Show, using coordinates, that the midpoint of the hypotenuse of a right triangle is the same distance from all three vertices.', 'Each distance $= \\frac12\\sqrt{a^2 + b^2}$',
    ['Step 1: put the right angle at $O(0, 0)$, $A(2a, 0)$, $B(0, 2b)$.', 'Step 2: midpoint of $AB$: $M(a, b)$.', 'Step 3: $MO = \\sqrt{a^2 + b^2}$, $MA = \\sqrt{a^2 + b^2}$, $MB = \\sqrt{a^2 + b^2}$.'],
    'Choose easy coordinates: right angle at the origin and the legs on the axes; use $2a$, $2b$ to avoid fractions.', [('What does this tell us about the circle through the three vertices?', 'Its centre is the midpoint of the hypotenuse (the hypotenuse is a diameter).')])
b.S(126, 'Town M is 36 km east and 15 km north of town N. How far apart are they?', '39 km',
    ['Step 1: put N at $(0, 0)$, M at $(36, 15)$.', 'Step 2: $d = \\sqrt{36^2 + 15^2} = \\sqrt{1296 + 225} = \\sqrt{1521} = 39$ km.'],
    'East/north distances are the legs of a right triangle.', [('A point is 8 km east and 6 km south of a town. Distance?', '10 km.')])

c = QSet('4.3 Practice — reflection, translation and dilation', 's43')
c.S(138, 'Reflect $(4, 5)$ in (i) the x-axis (ii) the y-axis (iii) $y = x$ (iv) $y = -x$ (v) the origin.', '$(4, -5)$, $(-4, 5)$, $(5, 4)$, $(-5, -4)$, $(-4, -5)$',
    ['Step 1: x-axis: change sign of $y$ → $(4, -5)$.', 'Step 2: y-axis: change sign of $x$ → $(-4, 5)$.', 'Step 3: $y = x$: swap → $(5, 4)$.',
     'Step 4: $y = -x$: swap and change both signs → $(-5, -4)$.', 'Step 5: origin: change both signs → $(-4, -5)$.'],
    'Learn the five rules on one point and check with a sketch.', [('Reflect $(-11, 2)$ in $y = x$.', '$(2, -11)$.')])
c.S(138, 'Reflect $(6, -3)$ in the x-axis and then reflect the image in the x-axis again.', '$(6, -3)$',
    ['Step 1: $(6, -3) \\to (6, 3)$.', 'Step 2: $(6, 3) \\to (6, -3)$ — back to the start.'],
    'Reflecting twice in the same line undoes it.', [('Reflect $(2, 7)$ in the origin twice.', '$(2, 7)$.')])
c.M(137, 'The image of $(x, y)$ under reflection in the line $y = x$ is', ['$(-x, y)$', '$(y, x)$', '$(-y, -x)$', '$(x, -y)$'], 'B',
    ['Step 1: the line $y = x$ is the perpendicular bisector of $PP\'$.', 'Step 2: this happens exactly when the coordinates are swapped.'],
    'Test with $(3, 2)$: its mirror in $y = x$ is $(2, 3)$.', [('Image of $(x, y)$ in $y = -x$?', '$(-y, -x)$.')])
c.S(139, 'A translation takes the origin to $(-2, 1)$. Where does it take $(2, 1)$, $(-2, 1)$ and $(0, 1)$?', '$(0, 2)$, $(-4, 2)$, $(-2, 2)$',
    ['Step 1: the rule is $(x, y) \\to (x - 2, y + 1)$.', 'Step 2: $(2, 1) \\to (0, 2)$; $(-2, 1) \\to (-4, 2)$; $(0, 1) \\to (-2, 2)$.'],
    'Where the origin goes = what you add to every point.', [('A translation moves every point 1 left and 2 down. Image of $(1, 1)$?', '$(0, -1)$.')])
c.S(139, 'Find the pre-image of $(-3, 4)$ under the translation by $(3, 7)$.', '$(-6, -3)$',
    ['Step 1: the translation adds $(3, 7)$, so the pre-image subtracts it.', 'Step 2: $(-3 - 3, 4 - 7) = (-6, -3)$.'],
    'Pre-image: undo the move.', [('Pre-image of $(4, 9)$ under translation by $(3, 7)$?', '$(1, 2)$.')])
c.S(141, 'Find the images of $(4, 7)$, $(-2, 1)$ and $(-5, -4)$ under the translation by $(2, -3)$.', '$(6, 4)$, $(0, -2)$, $(-3, -7)$',
    ['Step 1: add 2 to each $x$ and $-3$ to each $y$.', 'Step 2: $(4, 7) \\to (6, 4)$; $(-2, 1) \\to (0, -2)$; $(-5, -4) \\to (-3, -7)$.'],
    'Write the rule $(x + 2, y - 3)$ first.', [('Image of $(0, 0)$ under the same translation?', '$(2, -3)$.')])
c.S(140, 'A dilation with centre $O(0, 0)$ and scale factor 3 maps $A(2, -1)$ to $A\'$. Find $A\'$ and the ratio $OA\' : OA$.', '$A\'(6, -3)$; $3 : 1$',
    ['Step 1: centre at the origin: multiply coordinates by 3 → $(6, -3)$.', 'Step 2: $OA\' = 3 \\cdot OA$, so the ratio is $3 : 1$.'],
    'Centre $O$: multiply both coordinates by the scale factor.', [('Image of $(9, -6)$ under the dilation with centre $O$, factor $\\frac13$?', '$(3, -2)$.')])
c.M(140, 'A triangle with area 6 cm² is enlarged with scale factor 2. The area of the image is', ['12 cm²', '24 cm²', '8 cm²', '36 cm²'], 'B',
    ['Step 1: lengths are multiplied by $r = 2$.', 'Step 2: areas are multiplied by $r^2 = 4$: $6 \\times 4 = 24$ cm².'],
    'Length × $r$, area × $r^2$.', [('Scale factor $\\frac12$, original area 20 cm². Image area?', '5 cm².')])
c.TF(140, 'A dilation with scale factor $r \\ne 1$ is a rigid motion.', False,
     ['Step 1: rigid motions keep all lengths.', 'Step 2: a dilation multiplies lengths by $r$, so lengths change unless $r = 1$.'],
     'Rigid = congruent image; dilation = similar image.', [('Is a translation a rigid motion?', 'Yes — lengths and angles are kept.')])
c.S(142, 'How many lines of symmetry: (a) equilateral triangle (b) scalene triangle (c) regular $n$-gon (d) circle?', '(a) 3 (b) 0 (c) $n$ (d) infinitely many',
    ['Step 1: equilateral triangle: one through each vertex and the midpoint of the opposite side → 3.', 'Step 2: scalene: no two sides equal → none.',
     'Step 3: regular $n$-gon: $n$ axes.', 'Step 4: circle: every diameter is an axis.'],
    'Fold the shape in your mind: each fold that matches is one axis.', [('Lines of symmetry of a square?', '4.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Polyhedron', 'A solid bounded only by flat polygon faces.', 108),
    ('Prism', 'A polyhedron with two congruent parallel bases joined by parallelogram faces.', 109),
    ('Cross-section', 'The figure cut from a solid by a plane parallel to its base.', 109),
    ('Pyramid', 'A polyhedron with one polygon base and triangular faces meeting at the apex.', 111),
    ('Apex', 'The common vertex of the lateral faces of a pyramid.', 111),
    ('Slant height', 'Height of a lateral face of a pyramid, or distance from the vertex of a cone to the edge of its base.', 111),
    ('Frustum', 'What remains of a pyramid or cone when the top is cut off parallel to the base.', 112),
    ('Tetrahedron', 'A pyramid with a triangular base (4 triangular faces).', 112),
    ('Great circle', 'A cross-section of a sphere through its centre.', 115),
    ('Annulus', 'The ring between two circles with the same centre.', 116),
    ('Net', 'A flat figure that folds into a solid.', 117),
    ('Euler’s formula', 'F + V − E = 2 for every polyhedron.', 119),
    ('Abscissa', 'The x-coordinate of a point.', 123),
    ('Ordinate', 'The y-coordinate of a point.', 123),
    ('Quadrant', 'One of the four regions into which the axes divide the plane.', 123),
    ('Transformation', 'A one-to-one mapping of the whole plane onto itself.', 133),
    ('Reflection', 'The transformation in which the mirror line is the perpendicular bisector of every segment PP′.', 135),
    ('Axis of symmetry', 'A line in which a figure is its own mirror image.', 136),
    ('Translation', 'A slide of every point by the same distance in the same direction.', 139),
    ('Dilation', 'Enlargement or reduction from a centre by a scale factor r.', 140),
    ('Rigid motion', 'A transformation that keeps all lengths (reflection, translation).', 140),
]
TIPS = [
    ('Euler: F + V − E = 2. Prism (n-gon): F = n + 2, V = 2n, E = 3n. Pyramid: F = V = n + 1, E = 2n.', 119),
    ('Distance subtracts and squares (a number); midpoint adds and halves (a point).', 130),
    ('Reflection rules on (3, 2): x-axis (3, −2), y-axis (−3, 2), y = x (2, 3), origin (−3, −2).', 137),
]
IDEAS = [('euler', 'Euler’s formula', 'l4_1', 'math10-u4-md-euler-t'), ('dist', 'Distance & midpoint', 'l4_2', 'math10-u4-c01'),
         ('trans', 'Comparing transformations', 'l4_3', 'math10-u4-md-trans-cmp')]
