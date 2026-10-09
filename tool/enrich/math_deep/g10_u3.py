r"""Grade 10 Unit 3 — Geometric Patterns: polygons, angles and arcs of circles, chords/secants/tangents (pp. 56-105)."""
import math
from common import set_unit, T, RM, MN, TB, DG, ST, WK, CK, QSet
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL, polar, mid, lerp
from figs_common import side_by_side

UID = 'math10-u3'
set_unit(UID)


def circ(f, O, r, lab_o=True):
    f.circle(*O, r, INK, 2)
    if lab_o:
        f.dot(*O, INK, 3).ptlabel(*O, 'O', 's', INK, 12)
    return f


def on(f, O, r, deg, lab, pos=None, c=INK):
    p = polar(O, r, deg)
    if pos is None:
        d = deg % 360
        pos = 'e' if d < 30 or d >= 330 else 'ne' if d < 70 else 'n' if d < 110 else 'nw' if d < 150 else 'w' if d < 210 else 'sw' if d < 250 else 's' if d < 290 else 'se'
    f.dot(*p, c, 3.2).ptlabel(*p, lab, pos, c)
    return p


# ------------------------------------------------------------------ figures
def f_polys():
    a = Fig(76, 70)
    a.poly([(6, 56), (24, 10), (52, 22), (70, 60), (38, 44)], BLUE, 2, FILL[BLUE])
    b = Fig(76, 70)
    b.poly([(6, 14), (70, 56), (70, 14), (6, 56)], RED, 2, FILL[RED])
    c = Fig(76, 70)
    c.poly([(10, 58), (14, 14), (66, 18), (62, 58)], RED, 2, FILL[RED], closed=False)
    d = Fig(76, 70)
    d.path('M10 58 L18 14 Q48 -2 68 30 L56 60 Z', RED, 2, FILL[RED])
    return side_by_side([a, b, c, d], 6, ['polygon', 'crossing', 'open', 'curved'])


def f_regular():
    figs = []
    for k in (3, 4, 5, 6, 8):
        g = Fig(60, 60)
        g.poly([polar((30, 32), 26, 90 + 360 * i / k + (45 if k == 4 else 0) + (22.5 if k == 8 else 0)) for i in range(k)], BLUE, 2, FILL[BLUE])
        figs.append(g)
    return side_by_side(figs, 4, ['3 sides', '4', '5', '6', '8'])


def f_triproof():
    f = Fig(320, 180)
    A, B, C = (130, 40), (40, 150), (270, 150)
    f.poly([A, B, C], INK, 2.2, FILL[GREY])
    f.line(15, 40, 305, 40, BLUE, 2, dash=True)
    f.par((15, 40), (305, 40), 1, BLUE).par(B, C, 1, BLUE)
    f.ptlabel(*A, 'A', 'n').ptlabel(*B, 'B', 'sw').ptlabel(*C, 'C', 'se')
    f.angle(A, B, C, 22, ORANGE, 'a', 36, fill=FILL[ORANGE])
    f.angle(B, C, A, 26, RED, 'b', 40, fill=FILL[RED])
    f.angle(C, A, B, 30, GREEN, 'c', 44, fill=FILL[GREEN])
    f.angle(A, (15, 40), B, 24, RED, 'e', 38, fill=FILL[RED])
    f.angle(A, C, (305, 40), 28, GREEN, 'd', 42, fill=FILL[GREEN])
    f.text(160, 176, 'e = b, d = c (alternate) and e + a + d = 180°', 12, INK)
    return f


def f_interior():
    f = Fig(320, 206)
    pts = [polar((160, 98), 80, 90 + 360 * i / 6) for i in range(6)]
    pts = [(x + (8 if i in (1, 2) else 0), y) for i, (x, y) in enumerate(pts)]
    f.poly(pts, BLUE, 2.2, FILL[BLUE])
    cols = [RED, GREEN, ORANGE, PURPLE]
    for i, p in enumerate(pts[2:-1]):
        f.line(*pts[0], *p, RED, 1.6, dash='5 3')
    for i in range(4):
        cen = ((pts[0][0] + pts[i + 1][0] + pts[i + 2][0]) / 3, (pts[0][1] + pts[i + 1][1] + pts[i + 2][1]) / 3)
        f.label(*cen, str(i + 1), size=14, c=cols[i])
    for i, l in enumerate('ABCDEF'):
        f.ptlabel(*pts[i], l, ['n', 'nw', 'sw', 's', 'se', 'ne'][i])
    f.text(160, 202, 'hexagon: 4 triangles, so 4 × 180° = 720°', 12.5, INK)
    return f


def f_exterior_poly():
    f = Fig(320, 200)
    pts = [(80, 150), (220, 160), (260, 80), (160, 30), (60, 70)]
    f.poly(pts, BLUE, 2.2, FILL[BLUE])
    for i in range(5):
        p, q = pts[i], pts[(i + 1) % 5]
        e = lerp(p, q, 1.38)
        f.line(*q, *e, INK, 1.6, dash='5 3')
        f.angle(q, e, pts[(i + 2) % 5], 18, RED, None, fill=FILL[RED])
    f.text(160, 196, 'the five turns add up to one full turn: 360°', 12, INK)
    return f


def f_circle_parts():
    f = Fig(320, 220)
    O, r = (150, 110), 85
    f.circle(*O, r, INK, 2.2)
    A, B = polar(O, r, 200), polar(O, r, 20)
    C, D = polar(O, r, 120), polar(O, r, 55)
    E = polar(O, r, -60)
    f.line(*A, *B, BLUE, 2.4)
    f.line(*C, *D, GREEN, 2.4)
    f.line(*O, *E, ORANGE, 2.4)
    f.arc(O, r, -60, 20, RED, 4.5)
    f.dot(*O).ptlabel(*O, 'O', 'n')
    for p, l, pos in [(A, 'A', 'w'), (B, 'B', 'e'), (C, 'C', 'nw'), (D, 'D', 'ne'), (E, 'E', 's')]:
        f.dot(*p, INK, 3).ptlabel(*p, l, pos)
    f.text(290, 60, 'chord CD', 12, GREEN, 'end')
    f.text(30, 200, 'diameter AB', 12, BLUE, 'start')
    f.text(166, 166, 'radius OE', 12, ORANGE, 'end')
    f.text(246, 140, 'arc BE', 12, RED, 'start')
    return f


def f_inscribed():
    f = Fig(320, 220)
    O, r = (160, 112), 92
    circ(f, O, r)
    A, C = polar(O, r, 200), polar(O, r, -20)
    B = polar(O, r, 100)
    f.arc(O, r, 200, 340, RED, 4)
    f.poly([A, B, C], BLUE, 2.2, closed=False)
    f.poly([A, O, C], ORANGE, 2.2, closed=False)
    for p, l, pos in [(A, 'A', 'w'), (C, 'C', 'e'), (B, 'B', 'n')]:
        f.dot(*p, INK, 3).ptlabel(*p, l, pos)
    f.angle(B, A, C, 26, BLUE, '70°', 42)
    f.angle(O, A, C, 22, ORANGE, '140°', 36)
    f.text(160, 217, 'central angle = 2 × inscribed angle on the same arc', 12, INK)
    return f


def f_semicircle_samearc():
    a = Fig(160, 150)
    O, r = (80, 80), 60
    a.circle(*O, r, INK, 2)
    A, B, C = polar(O, r, 180), polar(O, r, 0), polar(O, r, 115)
    a.line(*A, *B, INK, 2).poly([A, C, B], BLUE, 2.2, closed=False)
    a.right(C, A, B, 9, RED)
    a.dot(*O, INK, 3)
    for p, l, pos in [(A, 'A', 'w'), (B, 'B', 'e'), (C, 'C', 'n')]:
        a.ptlabel(*p, l, pos)
    b = Fig(160, 150)
    O2 = (80, 80)
    b.circle(*O2, r, INK, 2)
    P, Q = polar(O2, r, 220), polar(O2, r, -40)
    X, Y = polar(O2, r, 70), polar(O2, r, 130)
    b.poly([P, X, Q], BLUE, 2, closed=False).poly([P, Y, Q], GREEN, 2, closed=False).line(*P, *Q, INK, 1.4, dash='4 3')
    b.angle(X, P, Q, 18, BLUE, 'a', 30).angle(Y, P, Q, 18, GREEN, 'b', 30)
    return side_by_side([a, b], 10, ['angle in a semicircle = 90°', 'same arc: a = b'])


def f_cyclic():
    f = Fig(320, 210)
    O, r = (160, 105), 88
    circ(f, O, r, False)
    J, K, L, M = polar(O, r, 155), polar(O, r, 70), polar(O, r, -15), polar(O, r, 245)
    f.poly([J, K, L, M], BLUE, 2.2, FILL[BLUE])
    for p, l, pos in [(J, 'J', 'w'), (K, 'K', 'n'), (L, 'L', 'e'), (M, 'M', 's')]:
        f.dot(*p, INK, 3).ptlabel(*p, l, pos)
    f.angle(J, K, M, 22, RED, 'J', 36, fill=FILL[RED])
    f.angle(L, M, K, 22, RED, 'L', 36, fill=FILL[RED])
    f.angle(K, L, J, 22, GREEN, 'K', 36, fill=FILL[GREEN])
    f.angle(M, J, L, 22, GREEN, 'M', 36, fill=FILL[GREEN])
    f.text(300, 30, 'J + L = 180°', 12.5, RED, 'end').text(300, 48, 'K + M = 180°', 12.5, GREEN, 'end')
    return f


def f_chords_inside():
    f = Fig(320, 210)
    O, r = (150, 105), 88
    circ(f, O, r, False)
    A, C = polar(O, r, 150), polar(O, r, -40)
    B, D = polar(O, r, 50), polar(O, r, 230)
    f.line(*A, *C, BLUE, 2.2).line(*B, *D, BLUE, 2.2)
    # intersection
    def inter(p1, p2, p3, p4):
        x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
        dd = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / dd
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    E = inter(A, C, B, D)
    f.arc(O, r, 50, 150, RED, 4.5).arc(O, r, 230, 320, ORANGE, 4.5)
    for p, l, pos in [(A, 'A', 'w'), (C, 'C', 'se'), (B, 'B', 'ne'), (D, 'D', 'sw')]:
        f.dot(*p, INK, 3).ptlabel(*p, l, pos)
    f.angle(E, B, A, 18, PURPLE, 'x', 30, fill=FILL[PURPLE])
    f.ptlabel(*E, 'E', 'e', INK, 12)
    f.text(150, 12, 'arc AB', 12, RED)
    f.text(160, 207, 'arc DC', 12, ORANGE)
    f.text(310, 120, 'x = ½(arc AB + arc DC)', 12, PURPLE, 'end')
    return f


def f_tangent():
    f = Fig(320, 200)
    O, r = (150, 90), 70
    circ(f, O, r)
    T = polar(O, r, -90)
    f.line(30, T[1], 290, T[1], BLUE, 2.4)
    f.line(*O, *T, ORANGE, 2.2)
    f.right(T, (290, T[1]), O, 10, RED)
    f.dot(*T, RED).ptlabel(*T, 'T', 's', RED)
    f.text(290, T[1] - 8, 'tangent', 12, BLUE, 'end')
    f.text(O[0] + 8, (O[1] + T[1]) / 2 + 10, 'radius', 12, ORANGE, 'start')
    f.text(160, 196, 'tangent meets the radius at 90°', 12, INK)
    return f


def f_tangent_chord():
    f = Fig(320, 210)
    O, r = (160, 95), 78
    circ(f, O, r)
    P = polar(O, r, -90)
    S = polar(O, r, 20)
    Tt = polar(O, r, 145)
    f.line(30, P[1], 300, P[1], BLUE, 2.2)
    f.line(*P, *S, INK, 2.2)
    f.poly([P, Tt, S], GREEN, 2, closed=False)
    f.dot(*P, RED).ptlabel(*P, 'P', 's', RED)
    f.dot(*S, INK, 3).ptlabel(*S, 'S', 'e').dot(*Tt, INK, 3).ptlabel(*Tt, 'T', 'nw')
    f.ptlabel(300, P[1], 'B', 'n', BLUE).ptlabel(30, P[1], 'R', 'n', BLUE)
    f.angle(P, (300, P[1]), S, 30, RED, 'x', 44, fill=FILL[RED])
    f.angle(Tt, P, S, 24, RED, 'x', 38, fill=FILL[RED])
    f.text(160, 207, 'tangent–chord angle = angle in the other segment', 12, INK)
    return f


def f_outside():
    f = Fig(320, 210)
    O, r = (190, 105), 80
    circ(f, O, r, False)
    P = (25, 105)
    B, C = polar(O, r, 130), polar(O, r, 230)
    # secants from P through near points A, D to far points B, C
    def second(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        fx, fy = p[0] - O[0], p[1] - O[1]
        a = dx * dx + dy * dy; b = 2 * (fx * dx + fy * dy); c = fx * fx + fy * fy - r * r
        disc = math.sqrt(b * b - 4 * a * c)
        t1, t2 = (-b - disc) / (2 * a), (-b + disc) / (2 * a)
        return (p[0] + t1 * dx, p[1] + t1 * dy), (p[0] + t2 * dx, p[1] + t2 * dy)
    Bd = polar(O, r, 60)
    Cd = polar(O, r, -60)
    A, B2 = second(P, Bd)
    D, C2 = second(P, Cd)
    f.line(*P, *B2, BLUE, 2.2).line(*P, *C2, BLUE, 2.2)
    a1 = math.degrees(math.atan2(-(A[1] - O[1]), A[0] - O[0]))
    a2 = math.degrees(math.atan2(-(D[1] - O[1]), D[0] - O[0]))
    b1 = math.degrees(math.atan2(-(B2[1] - O[1]), B2[0] - O[0]))
    b2 = math.degrees(math.atan2(-(C2[1] - O[1]), C2[0] - O[0]))
    f.arc(O, r, a1, a2 if a2 > a1 else a2 + 360, ORANGE, 4.5)
    f.arc(O, r, b2, b1, RED, 4.5)
    for p, l, pos in [(A, 'A', 'nw'), (D, 'D', 'sw'), (B2, 'B', 'ne'), (C2, 'C', 'se')]:
        f.dot(*p, INK, 3).ptlabel(*p, l, pos)
    f.dot(*P, PURPLE).ptlabel(*P, 'P', 'w', PURPLE)
    f.angle(P, B2, C2, 30, PURPLE, 'x', 44, fill=FILL[PURPLE])
    f.text(160, 207, 'x = ½(far arc BC − near arc AD)', 12.5, PURPLE)
    return f


def f_two_tangents():
    f = Fig(320, 190)
    O, r = (210, 92), 62
    circ(f, O, r)
    P = (35, 92)
    d = O[0] - P[0]
    t = math.degrees(math.acos(r / d))
    A, B = polar(O, r, 180 - t), polar(O, r, 180 + t)
    f.line(*P, *A, BLUE, 2.2).line(*P, *B, BLUE, 2.2)
    f.line(*O, *A, ORANGE, 1.8).line(*O, *B, ORANGE, 1.8)
    f.right(A, P, O, 8, RED).right(B, P, O, 8, RED)
    f.ticks(P, A, 1, BLUE).ticks(P, B, 1, BLUE)
    f.dot(*P, PURPLE).ptlabel(*P, 'P', 'w', PURPLE)
    f.dot(*A, INK, 3).ptlabel(*A, 'A', 'n').dot(*B, INK, 3).ptlabel(*B, 'B', 's')
    f.text(160, 186, 'PA = PB;  P + angle AOB = 180°', 12.5, INK)
    return f


def f_parallel_chords():
    f = Fig(220, 190)
    O, r = (110, 95), 80
    circ(f, O, r, False)
    A, B = polar(O, r, 140), polar(O, r, 40)
    C, D = polar(O, r, 200), polar(O, r, -20)
    f.line(*A, *B, BLUE, 2.2).line(*C, *D, BLUE, 2.2)
    f.par(A, B, 1, BLUE).par(C, D, 1, BLUE)
    f.arc(O, r, 140, 200, RED, 4.5).arc(O, r, -20, 40, RED, 4.5)
    for p, l, pos in [(A, 'A', 'nw'), (B, 'B', 'ne'), (C, 'C', 'sw'), (D, 'D', 'se')]:
        f.ptlabel(*p, l, pos)
    f.text(110, 186, 'arc AC = arc BD', 12.5, RED)
    return f


def f_chord_products():
    f = Fig(320, 200)
    O, r = (160, 100), 84
    circ(f, O, r, False)
    R, S = polar(O, r, 160), polar(O, r, -30)
    Tq, Q = polar(O, r, 75), polar(O, r, 245)
    f.line(*R, *S, BLUE, 2.4).line(*Tq, *Q, GREEN, 2.4)
    x1, y1 = R; x2, y2 = S; x3, y3 = Tq; x4, y4 = Q
    dd = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / dd
    E = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    for p, l, pos in [(R, 'R', 'w'), (S, 'S', 'se'), (Tq, 'T', 'n'), (Q, 'Q', 's')]:
        f.dot(*p, INK, 3).ptlabel(*p, l, pos)
    f.dot(*E, RED).ptlabel(*E, 'E', 'ne', RED)
    f.text(316, 30, 'RE × ES', 12.5, BLUE, 'end').text(316, 48, '= TE × EQ', 12.5, GREEN, 'end')
    return f


def f_tan_secant():
    f = Fig(320, 200)
    O, r = (205, 95), 70
    circ(f, O, r, False)
    P = (25, 165)
    d = math.dist(P, O)
    ang_po = math.degrees(math.atan2(-(P[1] - O[1]), P[0] - O[0]))
    t = math.degrees(math.acos(r / d))
    A = polar(O, r, ang_po - t)
    f.line(*P, *A, RED, 2.4)
    # secant through the centre direction slightly rotated
    q = polar(O, r, 30)
    dx, dy = q[0] - P[0], q[1] - P[1]
    fx, fy = P[0] - O[0], P[1] - O[1]
    a = dx * dx + dy * dy; b = 2 * (fx * dx + fy * dy); c = fx * fx + fy * fy - r * r
    disc = math.sqrt(b * b - 4 * a * c)
    B = (P[0] + (-b - disc) / (2 * a) * dx, P[1] + (-b - disc) / (2 * a) * dy)
    C = (P[0] + (-b + disc) / (2 * a) * dx, P[1] + (-b + disc) / (2 * a) * dy)
    f.line(*P, *C, BLUE, 2.4)
    for p, l, pos in [(A, 'A', 's'), (B, 'B', 'nw'), (C, 'C', 'ne')]:
        f.dot(*p, INK, 3).ptlabel(*p, l, pos)
    f.dot(*P, PURPLE).ptlabel(*P, 'P', 'w', PURPLE)
    f.text(20, 24, 'tangent PA, secant PBC:', 12, INK, 'start')
    f.text(20, 44, 'PA² = PB × PC', 13, RED, 'start')
    return f


def f_two_secants():
    f = Fig(320, 200)
    O, r = (205, 100), 72
    circ(f, O, r, False)
    P = (22, 100)

    def cut(q):
        dx, dy = q[0] - P[0], q[1] - P[1]
        fx, fy = P[0] - O[0], P[1] - O[1]
        a = dx * dx + dy * dy; b = 2 * (fx * dx + fy * dy); c = fx * fx + fy * fy - r * r
        disc = math.sqrt(b * b - 4 * a * c)
        return (P[0] + (-b - disc) / (2 * a) * dx, P[1] + (-b - disc) / (2 * a) * dy), (P[0] + (-b + disc) / (2 * a) * dx, P[1] + (-b + disc) / (2 * a) * dy)
    A, B = cut(polar(O, r, 70))
    C, D = cut(polar(O, r, -60))
    f.line(*P, *B, BLUE, 2.4).line(*P, *D, GREEN, 2.4)
    for p, l, pos in [(A, 'A', 'n'), (B, 'B', 'ne'), (C, 'C', 's'), (D, 'D', 'se')]:
        f.dot(*p, INK, 3).ptlabel(*p, l, pos)
    f.dot(*P, PURPLE).ptlabel(*P, 'P', 'w', PURPLE)
    f.text(160, 195, 'PA × PB = PC × PD', 13, INK)
    return f


DIAGRAMS = {
    'polys': (f_polys(), 'Polygon or not?', 57),
    'regular': (f_regular(), 'Regular polygons with 3, 4, 5, 6 and 8 sides', 58),
    'triproof': (f_triproof(), 'Why the angles of a triangle add up to 180°', 60),
    'interior': (f_interior(), 'Splitting a polygon into triangles from one vertex', 63),
    'extpoly': (f_exterior_poly(), 'One exterior angle at each vertex', 72),
    'cparts': (f_circle_parts(), 'Parts of a circle', 75),
    'inscribed': (f_inscribed(), 'Inscribed angle and central angle on the same arc', 79),
    'semi': (f_semicircle_samearc(), 'Two consequences of the inscribed-angle theorem', 80),
    'cyclic': (f_cyclic(), 'Cyclic quadrilateral', 82),
    'inside': (f_chords_inside(), 'Angle between two chords that cross inside the circle', 86),
    'tangent': (f_tangent(), 'Tangent and radius', 88),
    'tanchord': (f_tangent_chord(), 'Tangent–chord angle', 89),
    'outside': (f_outside(), 'Angle between two secants that meet outside the circle', 92),
    'twotan': (f_two_tangents(), 'Two tangents from one external point', 95),
    'parchords': (f_parallel_chords(), 'Parallel chords cut off equal arcs', 91),
    'chordprod': (f_chord_products(), 'Intersecting chords', 97),
    'tansec': (f_tan_secant(), 'Tangent and secant from an external point', 98),
    'twosec': (f_two_secants(), 'Two secants from an external point', 99),
}

# ------------------------------------------------------------------ 3.1
L31 = [
    T('=math10-u3-c03', '3.1.1 Polygons and their names', 56,
      'A **polygon** is a closed plane figure made of straight line segments (its **sides**) such that each side meets exactly two others, at its end points (the **vertices**), and the sides do not cross each other. A figure with a curved side, a gap, or two sides crossing in the middle is **not** a polygon.',
      'Polygons are named by the number of sides $n$: 3 triangle, 4 quadrilateral, 5 pentagon, 6 hexagon, 7 heptagon, 8 octagon, 9 nonagon, 10 decagon, 12 dodecagon; in general an **$n$-gon**.',
      'A **regular polygon** is both **equilateral** (all sides equal) and **equiangular** (all angles equal). Both conditions are needed: a rhombus is equilateral but not equiangular; a rectangle is equiangular but not equilateral; only the square is regular. (For triangles alone, equilateral already forces equiangular.)'),
    DG('polys', 'Only the first figure is a polygon', 57, 'polys'),
    TB('names', 'Names of polygons', 57, ['Sides', 'Name', 'Sides', 'Name'],
       [['3', 'triangle', '8', 'octagon'], ['4', 'quadrilateral', '9', 'nonagon'], ['5', 'pentagon', '10', 'decagon'],
        ['6', 'hexagon', '12', 'dodecagon'], ['7', 'heptagon', '$n$', '$n$-gon']]),
    DG('regular', 'Regular polygons: equal sides AND equal angles', 58, 'regular'),
    T('=math10-u3-c04', '3.1.2 Sum of the interior angles', 59,
      '**Theorem 3.1 — triangle:** the three angles of any triangle add up to $180°$. Proof idea: draw the line through $A$ parallel to $BC$. The two alternate angles at $A$ equal $b$ and $c$, and together with $a$ they make a straight angle, so $a + b + c = 180°$.',
      '**Any polygon:** from one vertex of an $n$-gon draw all the diagonals. They cut it into $(n - 2)$ triangles, and the angles of these triangles make up exactly the interior angles of the polygon. So:',
      '$$S = (n - 2) \\times 180°$$',
      'For a **regular** $n$-gon all $n$ angles are equal, so each interior angle is $\\dfrac{(n - 2) \\times 180°}{n}$.',
      'Working backwards: if you know the angle sum $S$, then $n - 2 = \\frac{S}{180°}$, so $n = \\frac{S}{180°} + 2$. If this is not a whole number, no such polygon exists.'),
    DG('triproof', 'Proof that a + b + c = 180°', 60, 'triproof'),
    WK('ex-31a', 'Worked example: missing angles in triangles', 60,
       '(a) A triangle has angles $x$, $30°$ and $130°$. (b) An isosceles triangle has two equal angles $x$ and a third angle $70°$. Find $x$.',
       ['(a) $x + 30° + 130° = 180° \\Rightarrow x = 180° - 160° = 20°$.',
        '(b) $x + x + 70° = 180° \\Rightarrow 2x = 110° \\Rightarrow x = 55°$.'],
       '(a) $20°$ (b) $55°$'),
    DG('interior', 'Interior angle sum of a hexagon', 63, 'interior'),
    TB('angles-t', 'Interior and exterior angles of polygons', 64, ['Polygon', '$n$', 'Interior sum', 'Each interior (regular)', 'Each exterior (regular)'],
       [['Triangle', '3', '$180°$', '$60°$', '$120°$'], ['Quadrilateral', '4', '$360°$', '$90°$', '$90°$'],
        ['Pentagon', '5', '$540°$', '$108°$', '$72°$'], ['Hexagon', '6', '$720°$', '$120°$', '$60°$'],
        ['Octagon', '8', '$1080°$', '$135°$', '$45°$'], ['Decagon', '10', '$1440°$', '$144°$', '$36°$'],
        ['Dodecagon', '12', '$1800°$', '$150°$', '$30°$'], ['$n$-gon', '$n$', '$(n-2) \\cdot 180°$', '$\\frac{(n-2) \\cdot 180°}{n}$', '$\\frac{360°}{n}$']],
       'Interior + exterior at each vertex $= 180°$. Check a row: hexagon $120° + 60° = 180°$ (correct).'),
    WK('ex-31b', 'Worked example: using the angle-sum formula both ways', 64,
       '(a) Find each interior angle of a regular 12-gon. (b) A polygon has interior angle sum $2160°$. How many sides? (c) Six angles of a heptagon add up to $820°$; find the seventh.',
       ['(a) $S = (12 - 2) \\times 180° = 1800°$; each angle $= 1800° \\div 12 = 150°$.',
        '(b) $(n - 2) \\times 180° = 2160° \\Rightarrow n - 2 = 12 \\Rightarrow n = 14$ sides.',
        '(c) Heptagon: $S = 5 \\times 180° = 900°$; seventh angle $= 900° - 820° = 80°$.'],
       '(a) $150°$ (b) 14 (c) $80°$'),
    'math10-u3-wrk7c1',
    T('ext-tri', '3.1.3 Exterior angle of a triangle', 69,
      'Extend one side of a triangle. The angle between the extension and the next side is an **exterior angle**. The two angles of the triangle that are **not** next to it are its **opposite (remote) interior angles**.',
      '**Theorem 3.2 (exterior angle theorem):** an exterior angle of a triangle equals the **sum of the two opposite interior angles**.',
      'Proof: $a + b + c = 180°$ (angle sum) and $c + d = 180°$ (straight line), so $a + b + c = c + d$, hence $d = a + b$.',
      'Consequence: an exterior angle is always **bigger than each** opposite interior angle.'),
    WK('ex-31c', 'Worked example: exterior angle theorem', 70,
       'In triangle $ABC$, the exterior angle at $C$ is $110°$ and $\\angle A = 60°$. Find the interior angle $a$ at $C$ and the angle $b$ at $B$. Then find the exterior angle at $B$.',
       ['Interior and exterior at $C$ lie on a straight line: $a = 180° - 110° = 70°$.',
        'Exterior angle theorem at $C$: $110° = \\angle A + \\angle B = 60° + b$, so $b = 50°$.',
        'Exterior angle at $B$ $= \\angle A + \\angle C = 60° + 70° = 130°$ (check: $180° - 50° = 130°$, correct).'],
       '$a = 70°$, $b = 50°$, exterior at $B$ $= 130°$'),
    T('=math10-u3-c05', '3.1.4 Sum of the exterior angles of a polygon', 72,
      'At each vertex take **one** exterior angle (extend the sides in turn, all in the same direction round the polygon).',
      '**Theorem 3.4:** the exterior angles of **any** polygon add up to $360°$ — whatever the number of sides.',
      'Proof: at each of the $n$ vertices, interior + exterior $= 180°$, so all of them together give $n \\times 180°$. The interior angles use $(n - 2) \\times 180°$, so the exterior angles get $n \\times 180° - (n - 2) \\times 180° = 2 \\times 180° = 360°$.',
      'Picture: walk round the polygon; at each corner you turn through the exterior angle; after one lap you face the starting direction again — one full turn, $360°$.',
      'For a **regular** $n$-gon: each exterior angle $= \\dfrac{360°}{n}$, so $n = \\dfrac{360°}{\\text{exterior angle}}$. This is the **fastest** way to find $n$ from an interior angle: exterior $= 180° -$ interior.'),
    DG('extpoly', 'Exterior angles add up to 360°', 72, 'extpoly'),
    WK('ex-31d', 'Worked example: regular polygons from their angles', 73,
       '(a) Each exterior angle of a regular polygon is $60°$. How many sides? (b) Each interior angle is $156°$. How many sides? (c) Is there a regular polygon with interior angle $100°$?',
       ['(a) $n = 360° \\div 60° = 6$ (hexagon).',
        '(b) Exterior $= 180° - 156° = 24°$, so $n = 360° \\div 24° = 15$.',
        '(c) Exterior $= 80°$, $360° \\div 80° = 4.5$ — not a whole number, so **no** such regular polygon.'],
       '(a) 6 (b) 15 (c) no'),
    MN('tip31', 'Tip: go through the exterior angle', 73,
       'Interior angle given → subtract from $180°$ → divide $360°$ by it. Example: $140°$ → $40°$ → $n = 9$. Much quicker than solving $\\frac{(n-2)180}{n} = 140$.'),
    'math10-u3-c01',
    'math10-u3-tbl1',
]

# ------------------------------------------------------------------ 3.2
L32 = [
    T('=math10-u3-c08', '3.2.1 Parts of a circle, central and inscribed angles', 75,
      'A **chord** joins two points of the circle. A chord through the centre is a **diameter** (the longest chord, $d = 2r$). A **radius** joins the centre to the circle. An **arc** is a part of the circle: a **minor arc** is less than half the circle, a **major arc** more than half, a **semicircle** exactly half.',
      'The **measure of an arc** is the measure of the central angle that stands on it (a full circle is $360°$).',
      '- A **central angle** has its vertex at the centre $O$.',
      '- An **inscribed angle** has its vertex **on the circle** and its arms are chords.',
      '**Theorem 3.5 (inscribed angle theorem):** an inscribed angle is **half** the central angle standing on the same arc: $\\angle ABC = \\frac12 \\angle AOC = \\frac12 m(\\text{arc } AC)$.',
      'Two very useful consequences:',
      '- **Angle in a semicircle** is a right angle ($90°$): the central angle on a diameter is $180°$.',
      '- **Angles on the same arc are equal**: they are all half of the same central angle.'),
    DG('cparts', 'Chord, diameter, radius, arc', 75, 'cparts'),
    DG('inscribed', 'Inscribed angle = half of the central angle', 79, 'inscribed',
       'Both angles stand on the red arc $AC$. If $\\angle ABC = 70°$ then $\\angle AOC = 140°$ and arc $AC$ measures $140°$.'),
    WK('ex-insc-proof', 'Proof of the inscribed angle theorem (centre on one arm)', 79,
       'Let $O$ lie on $BC$. Prove $\\angle ABC = \\frac12\\angle AOC$.',
       ['Draw $OA$. $OA = OB$ (radii), so triangle $AOB$ is isosceles and $\\angle OAB = \\angle ABC$.',
        '$\\angle AOC$ is an exterior angle of triangle $AOB$, so $\\angle AOC = \\angle OAB + \\angle ABC = 2\\angle ABC$.',
        'Divide by 2: $\\angle ABC = \\frac12\\angle AOC$. ∎ (Other positions of $O$ follow by adding or subtracting two such cases.)'],
       '$\\angle ABC = \\frac12 \\angle AOC$'),
    DG('semi', 'Angle in a semicircle; angles on the same arc', 80, 'semi'),
    WK('ex-32a', 'Worked example: central and inscribed angles', 80,
       '(a) An inscribed angle $\\angle B = 70°$ stands on arc $ADC$. Find the arc. (b) Arc $DBF$ measures $130°$; find the inscribed angle $\\angle DKF$ on it. (c) $AB$ is a diameter and $\\angle CAB = 35°$; find $\\angle ABC$.',
       ['(a) Arc $= 2 \\times 70° = 140°$.',
        '(b) $\\angle DKF = \\frac12 \\times 130° = 65°$.',
        '(c) $\\angle ACB = 90°$ (semicircle), so $\\angle ABC = 180° - 90° - 35° = 55°$.'],
       '(a) $140°$ (b) $65°$ (c) $55°$'),
    T('=math10-u3-c09', '3.2.2 Cyclic quadrilaterals', 82,
      'A quadrilateral whose four vertices lie on a circle is a **cyclic quadrilateral**.',
      '**Theorem 3.6:** the **opposite angles** of a cyclic quadrilateral are **supplementary** (add up to $180°$).',
      'Proof: $\\angle A$ stands on arc $BCD$ and $\\angle C$ on arc $BAD$; the two arcs make the whole circle. So $\\angle A + \\angle C = \\frac12(\\text{arc } BCD + \\text{arc } BAD) = \\frac12 \\times 360° = 180°$.',
      'Consequence: an exterior angle of a cyclic quadrilateral equals the interior **opposite** angle.',
      'Converse (useful test): if a pair of opposite angles of a quadrilateral add up to $180°$, its vertices lie on a circle.'),
    DG('cyclic', 'Opposite angles add up to 180°', 82, 'cyclic'),
    WK('ex-32b', 'Worked example: cyclic quadrilateral', 83,
       'In cyclic quadrilateral $JKLM$, $\\angle L = 96°$ and $\\angle K = 80°$. Find $\\angle J$ and $\\angle M$.',
       ['$J$ and $L$ are opposite: $\\angle J = 180° - 96° = 84°$.',
        '$K$ and $M$ are opposite: $\\angle M = 180° - 80° = 100°$.',
        'Check: $84° + 80° + 96° + 100° = 360°$ (correct) (angle sum of a quadrilateral).'],
       '$\\angle J = 84°$, $\\angle M = 100°$'),
    'math10-u3-wk2',
    T('inside-t', 'Angle between two chords crossing inside', 86,
      '**Theorem 3.7:** when two chords cross inside a circle, each angle at the crossing point is **half the sum** of the arc it faces and the arc its vertically opposite angle faces:',
      '$$x = \\tfrac12(\\text{arc } AB + \\text{arc } CD)$$',
      'Proof: join $B$ to $C$. $x$ is an exterior angle of the small triangle, so it equals the sum of two inscribed angles, which are half of the two arcs.'),
    DG('inside', 'Two chords crossing at E', 86, 'inside'),
    WK('ex-32c', 'Worked example: chords crossing inside', 87,
       'Two chords cross inside a circle. The arcs facing the angle $a$ and its opposite angle measure $35°$ and $65°$. Find $a$.',
       ['Use $a = \\frac12(\\text{sum of the two arcs})$.', '$a = \\frac12(35° + 65°) = \\frac12(100°) = 50°$.'],
       '$a = 50°$'),
    T('=math10-u3-c10', '3.2.3 Tangents', 88,
      'A **tangent** is a line that touches the circle at exactly **one** point, the **point of contact (tangency)**. A **secant** is a line that cuts the circle at two points.',
      '- **Tangent is perpendicular to the radius:** the tangent is perpendicular to the radius at the point of contact.',
      '- **Two tangents from one external point are equal**: $PA = PB$, and $OP$ bisects the angle $APB$. In quadrilateral $PAOB$ the two right angles give $\\angle APB + \\angle AOB = 180°$.',
      '- **Tangent–chord angle (Theorem 3.8):** the angle between a tangent and a chord at the point of contact equals the inscribed angle on the **opposite** side of the chord (in the "alternate segment"). It is half the arc cut off by the chord.',
      '- **Parallel chords** cut off equal arcs between them.'),
    DG('tangent', 'Tangent is perpendicular to the radius', 88, 'tangent'),
    DG('twotan', 'Equal tangents', 95, 'twotan'),
    DG('tanchord', 'Angle in the alternate segment', 89, 'tanchord',
       'The angle $x$ between tangent $PB$ and chord $PS$ equals the angle $PTS$ at any point $T$ on the arc on the other side of $PS$.'),
    DG('parchords', 'Parallel chords', 91, 'parchords'),
    T('outside-t', 'Angle formed outside the circle', 92,
      '**Theorem 3.9:** if two secants (or a secant and a tangent, or two tangents) meet at a point $P$ **outside** the circle, the angle at $P$ is **half the difference** of the two arcs they cut off:',
      '$$\\angle P = \\tfrac12(\\text{far arc} - \\text{near arc})$$',
      'Compare: inside → half the **sum**; on the circle → **half** the arc; outside → half the **difference**.'),
    DG('outside', 'Two secants from P', 92, 'outside'),
    TB('circle-angles', 'All the circle angle rules in one table', 93, ['Where is the vertex?', 'Angle formed by', 'Rule'],
       [['at the centre', 'two radii', 'angle $=$ arc'],
        ['on the circle', 'two chords (inscribed)', 'angle $= \\frac12$ arc'],
        ['on the circle', 'tangent and chord', 'angle $= \\frac12$ arc $=$ angle in alternate segment'],
        ['inside the circle', 'two crossing chords', 'angle $= \\frac12$(sum of the two arcs)'],
        ['outside the circle', 'two secants / secant + tangent / two tangents', 'angle $= \\frac12$(far arc − near arc)']],
       'Special cases: angle in a semicircle $= 90°$; opposite angles of a cyclic quadrilateral add to $180°$; tangent is perpendicular to the radius.'),
    WK('ex-32d', 'Worked example: angle outside the circle', 94,
       'Two secants from $Q$ cut off arcs $PTR = 120°$ (far) and $SLM$ (near). If $\\angle PQR = 36°$, find arc $SLM$.',
       ['$\\angle Q = \\frac12(\\text{far} - \\text{near})$: $36° = \\frac12(120° - x)$.',
        '$72° = 120° - x \\Rightarrow x = 48°$.'],
       'arc $SLM = 48°$'),
    WK('ex-32e', 'Worked example: two tangents', 95,
       'Two tangents from an external point make an angle of $80°$. Find the two arcs between the points of contact.',
       ['Let the minor arc be $x$; the major arc is $360° - x$.',
        'Outside angle: $80° = \\frac12((360° - x) - x) = 180° - x$.',
        'So $x = 100°$ and the major arc is $260°$. (Also: $\\angle AOB = 180° - 80° = 100°$.)'],
       'minor arc $100°$, major arc $260°$'),
    'math10-u3-c06',
    'math10-u3-c07',
]

# ------------------------------------------------------------------ 3.3
L33 = [
    T('=math10-u3-c11', '3.3 Lengths of chords, secants and tangents', 97,
      'Three "product" theorems connect the lengths of segments cut off by a circle. Each says: **(part × part) on one line = (part × part) on the other line**, where all the parts are measured **from the crossing point**.'),
    T('=math10-u3-c12', '3.3.1 Two chords crossing inside', 97,
      'If chords $RS$ and $TQ$ cross at $E$ inside the circle, then',
      '$$RE \\times ES = TE \\times EQ$$',
      'Reason: triangles $RET$ and $QES$ are similar (equal angles on the same arcs and vertically opposite angles), so $\\frac{RE}{TE} = \\frac{EQ}{ES}$.'),
    DG('chordprod', 'Intersecting chords', 97, 'chordprod'),
    WK('ex-33a', 'Worked example: intersecting chords', 97,
       'Chords $RS$ and $TQ$ cross at $E$. $RE = 7$, $ES = 8$ and $EQ = 4$. Find $TE$.',
       ['$RE \\times ES = TE \\times EQ$.', '$7 \\times 8 = TE \\times 4$.', '$TE = 56 \\div 4 = 14$.'],
       '$TE = 14$'),
    'math10-u3-wk3',
    T('tansec-t', '3.3.2 A tangent and a secant from one point', 98,
      'From an external point $P$ draw a tangent touching at $A$ and a secant cutting the circle at $B$ (near) and $C$ (far). Then',
      '$$PA^2 = PB \\times PC$$',
      'The tangent is "its own two parts" (both from $P$ to $A$), so it appears squared. **$PC$ is the whole secant**, not just the part inside the circle.'),
    DG('tansec', 'Tangent–secant theorem', 98, 'tansec'),
    WK('ex-33b', 'Worked example: tangent and secant', 99,
       'Tangent $PA = 12$. A secant from $P$ has outside part $PB = 6$ and inside part $BC = x$. Find $x$.',
       ['$PA^2 = PB \\times PC$ with $PC = 6 + x$.', '$144 = 6(6 + x) = 36 + 6x$.', '$6x = 108 \\Rightarrow x = 18$.'],
       '$x = 18$'),
    T('=math10-u3-c13', '3.3.3 Two secants from one point', 99,
      'If two secants from an external point $P$ cut the circle at $A, B$ and at $C, D$ ($A$, $C$ nearer to $P$), then',
      '$$PA \\times PB = PC \\times PD$$',
      '"**Outside part × whole secant** is the same for both secants." Proof: both products equal $PE^2$ for a tangent $PE$ from $P$.'),
    DG('twosec', 'Secant–secant theorem', 99, 'twosec'),
    WK('ex-33c', 'Worked example: two secants', 100,
       '$PA = 6$, $AB = 6$ and $PC = 4$. Find $CD = x$.',
       ['Whole secants: $PB = 6 + 6 = 12$ and $PD = 4 + x$.', '$PA \\times PB = PC \\times PD$: $6 \\times 12 = 4(4 + x)$.', '$72 = 16 + 4x \\Rightarrow 4x = 56 \\Rightarrow x = 14$.'],
       '$CD = 14$'),
    TB('seg-t', 'Segment theorems compared', 100, ['Situation', 'Formula', 'Common mistake'],
       [['Two chords cross inside at $E$', '$RE \\cdot ES = TE \\cdot EQ$', 'multiplying a part by a whole chord'],
        ['Tangent $PA$ + secant $PBC$', '$PA^2 = PB \\cdot PC$', 'using $BC$ instead of the whole $PC$'],
        ['Two secants $PAB$, $PCD$', '$PA \\cdot PB = PC \\cdot PD$', 'using the inside parts $AB$, $CD$']],
       'Inside: part × part. Outside: outside part × whole.'),
    WK('ex-33d', 'Worked example: an equation from crossing chords', 104,
       'Chords $PQ$ and $RS$ cross at $A$. $PA = 12$, $QA = x$, $RA = x + 1$ and $SA = x + 6$. Find $PQ$ and $RS$.',
       ['$PA \\cdot QA = RA \\cdot SA$: $12x = (x + 1)(x + 6) = x^2 + 7x + 6$.',
        '$x^2 - 5x + 6 = 0 \\Rightarrow (x - 2)(x - 3) = 0$, so $x = 2$ or $x = 3$.',
        '$x = 2$: $PQ = 14$, $RS = 3 + 8 = 11$. $x = 3$: $PQ = 15$, $RS = 4 + 9 = 13$. Both are possible.'],
       '$PQ = 14, RS = 11$ or $PQ = 15, RS = 13$'),
]

LESSONS = {'math10-u3-l3-1': L31, 'math10-u3-l3-2': L32, 'math10-u3-l3-3': L33}

# ------------------------------------------------------------------ practice
a = QSet('3.1 Practice — angles of polygons', 's31')
a.S(64, 'Find the sum of the interior angles of a 15-sided polygon.', '$2340°$',
    ['Step 1: $S = (n - 2) \\times 180°$.', 'Step 2: $(15 - 2) \\times 180° = 13 \\times 180° = 2340°$.'],
    'Subtract 2 first, then multiply by 180.', [('Sum of the interior angles of an octagon?', '$1080°$.')])
a.M(65, 'Each interior angle of a regular polygon is $140°$. How many sides?', ['7', '8', '9', '10'], 'C',
    ['Step 1: exterior angle $= 180° - 140° = 40°$.', 'Step 2: $n = 360° \\div 40° = 9$.'],
    'Go through the exterior angle — it is one division.', [('Each interior angle is $108°$. How many sides?', '5 (exterior $72°$).')])
a.S(65, 'The four angles of a pentagon are $110°, 70°, 100°$ and $110°$. Find the fifth.', '$150°$',
    ['Step 1: pentagon sum $= 3 \\times 180° = 540°$.', 'Step 2: given angles add to $390°$.', 'Step 3: fifth $= 540° - 390° = 150°$.'],
    'Missing angle = total − known angles.', [('Three angles of a quadrilateral are $80°, 95°, 110°$. Find the fourth.', '$75°$.')])
a.S(65, 'Is there a regular polygon with (a) each interior angle $100°$? (b) interior angle sum $820°$?', '(a) No (b) No',
    ['Step 1 (a): exterior $= 80°$; $360 \\div 80 = 4.5$, not whole → no.', 'Step 2 (b): $820 \\div 180 = 4.56$, not whole → no polygon has this angle sum.'],
    'The number of sides must come out as a whole number of at least 3.', [('Is there a regular polygon with exterior angle $72°$?', 'Yes — a pentagon ($360 \\div 72 = 5$).')])
a.S(65, 'The angles of a quadrilateral are $x$, $2x$, $3x$ and $4x$. Find them.', '$36°, 72°, 108°, 144°$',
    ['Step 1: $x + 2x + 3x + 4x = 360°$.', 'Step 2: $10x = 360° \\Rightarrow x = 36°$.', 'Step 3: multiply: $36°, 72°, 108°, 144°$.'],
    'Ratios of angles: add the parts, divide the angle sum, then multiply back.', [('The angles of a triangle are in the ratio 2 : 3 : 4. Find them.', '$40°, 60°, 80°$.')])
a.S(70, 'An exterior angle of a triangle is $120°$ and one opposite interior angle is $50°$. Find all three interior angles.', '$50°, 70°, 60°$',
    ['Step 1: other opposite angle $= 120° - 50° = 70°$ (exterior angle theorem).', 'Step 2: the adjacent interior angle $= 180° - 120° = 60°$.', 'Step 3: check $50 + 70 + 60 = 180$ (correct).'],
    'The exterior angle "belongs" to the two far angles.', [('An exterior angle is $135°$ and the two remote angles are equal. Find them.', '$67.5°$ each.')])
a.S(73, 'In a right-angled triangle one acute angle is twice the other. Find the exterior angles.', '$90°$, $150°$, $120°$',
    ['Step 1: acute angles $x$ and $2x$ with $x + 2x = 90°$, so $x = 30°$, $2x = 60°$.', 'Step 2: exterior $= 180° -$ interior: $180 - 90 = 90°$, $180 - 30 = 150°$, $180 - 60 = 120°$.', 'Step 3: check the sum $= 360°$ (correct).'],
    'Exterior angles always add to $360°$ — use it to check.', [('Find the exterior angles of an equilateral triangle.', '$120°$ each.')])
a.M(73, 'Each exterior angle of a regular polygon is twice each interior angle. How many sides?', ['3', '4', '5', '6'], 'A',
    ['Step 1: interior $x$, exterior $2x$, and $x + 2x = 180° \\Rightarrow x = 60°$.', 'Step 2: exterior $= 120°$, $n = 360 \\div 120 = 3$.'],
    'Interior + exterior = $180°$ at every vertex.', [('Each interior angle is 3 times each exterior angle. How many sides?', '8 (exterior $45°$).')])
a.TF(72, 'The sum of the exterior angles of a decagon is greater than that of a pentagon.', False,
     ['Step 1: the exterior angles of ANY polygon add up to $360°$.', 'Step 2: so both sums are $360°$.'],
     'Interior sum grows with $n$; exterior sum never changes.', [('Sum of exterior angles of a 100-gon?', '$360°$.')])
a.S(65, 'If the interior angle sum of a polygon is twice its exterior angle sum, how many sides does it have?', '6',
    ['Step 1: exterior sum $= 360°$, so interior sum $= 720°$.', 'Step 2: $(n - 2) 180 = 720 \\Rightarrow n - 2 = 4 \\Rightarrow n = 6$.'],
    'Turn words into the two sums first.', [('Interior sum equals exterior sum. How many sides?', '4.')])

b = QSet('3.2 Practice — angles and arcs of circles', 's32')
b.S(80, 'In a circle with centre $O$, minor arc $AB$ measures $80°$. Find (a) $\\angle AOB$ (b) an inscribed angle $\\angle ACB$ on the major arc.', '(a) $80°$ (b) $40°$',
    ['Step 1: central angle = its arc: $80°$.', 'Step 2: inscribed angle = half the arc it stands on: $40°$.'],
    'Centre → equal to the arc; circumference → half.', [('$\\angle ACB = 65°$. What is the central angle on the same arc?', '$130°$.')])
b.S(81, '$AB$ is a diameter and $C$ is on the circle with $\\angle CAB = 28°$. Find $\\angle ABC$.', '$62°$',
    ['Step 1: angle in a semicircle: $\\angle ACB = 90°$.', 'Step 2: $\\angle ABC = 180° - 90° - 28° = 62°$.'],
    'See a diameter? Look for the right angle on the circle.', [('$AB$ is a diameter and $\\angle ABC = 55°$. Find $\\angle CAB$.', '$35°$.')])
b.M(83, 'In cyclic quadrilateral $ABCD$, $\\angle DAB = 75°$. Then $\\angle BCD$ is', ['$75°$', '$105°$', '$150°$', '$15°$'], 'B',
    ['Step 1: $A$ and $C$ are opposite angles.', 'Step 2: $\\angle C = 180° - 75° = 105°$.'],
    'Opposite angles of a cyclic quadrilateral add to $180°$.', [('In cyclic $PQRS$, $\\angle Q = 112°$. Find $\\angle S$.', '$68°$.')])
b.S(84, 'Quadrilateral $ABCD$ is inscribed in a circle. $\\angle ADC = 70°$ and $\\angle ACD = 50°$. Find $\\angle ABC$ and $\\angle CAD$.', '$\\angle ABC = 110°$, $\\angle CAD = 60°$',
    ['Step 1: $\\angle ABC = 180° - \\angle ADC = 110°$ (opposite angles).', 'Step 2: in triangle $ACD$: $\\angle CAD = 180° - 70° - 50° = 60°$.'],
    'Use the triangle angle sum inside the circle as well as the circle rules.', [('Cyclic $ABCD$ with $\\angle B = 95°$, $\\angle C = 80°$. Find $\\angle A$ and $\\angle D$.', '$\\angle D = 85°$, $\\angle A = 100°$.')])
b.S(87, 'Two chords meet inside a circle. The intercepted arcs are $150°$ and $120°$. Find the angle $x$ between the chords.', '$135°$',
    ['Step 1: inside → half the sum.', 'Step 2: $x = \\frac12(150° + 120°) = 135°$.'],
    'Inside the circle → ADD the arcs, then halve.', [('Arcs $82°$ and $40°$. Find the angle.', '$61°$.')])
b.S(93, 'Two secants meet outside a circle at $40°$. The larger intercepted arc is $110°$. Find the smaller arc.', '$30°$',
    ['Step 1: outside → half the difference: $40 = \\frac12(110 - x)$.', 'Step 2: $80 = 110 - x \\Rightarrow x = 30°$.'],
    'Outside → SUBTRACT the arcs (big − small), then halve.', [('A tangent and a secant meet outside at $26°$; the far arc is $80°$. Find the near arc.', '$28°$.')])
b.S(95, 'Two tangents from $P$ touch a circle at $A$ and $B$. $\\angle APB = 50°$. Find $\\angle AOB$ and $\\angle OAB$.', '$\\angle AOB = 130°$, $\\angle OAB = 25°$',
    ['Step 1: $\\angle OAP = \\angle OBP = 90°$ (tangent is perpendicular to the radius).', 'Step 2: quadrilateral $PAOB$: $\\angle AOB = 360° - 90° - 90° - 50° = 130°$.', 'Step 3: triangle $OAB$ is isosceles: $\\angle OAB = (180° - 130°) \\div 2 = 25°$.'],
    'Tangent + radius = right angle; two tangents give a kite with two right angles.', [('Tangents from $P$ make $\\angle APB = 80°$. Find the minor arc $AB$.', '$100°$.')])
b.S(89, 'A tangent at $P$ makes an angle of $58°$ with chord $PS$. Find the inscribed angle $\\angle PTS$ on the other side of the chord and the arc $PS$.', '$\\angle PTS = 58°$; arc $PS = 116°$',
    ['Step 1: tangent–chord angle = angle in the alternate segment: $58°$.', 'Step 2: the arc is twice the inscribed angle: $116°$.'],
    'Tangent–chord angle behaves exactly like an inscribed angle on that chord.', [('A tangent–chord angle is $35°$. What arc does the chord cut off?', '$70°$.')])
b.TF(81, 'All inscribed angles standing on the same arc are equal.', True,
     ['Step 1: each is half the central angle of that arc.', 'Step 2: halves of the same angle are equal → true.'],
     'Same arc, same side → same angle.', [('Is an inscribed angle on a major arc bigger than one on the minor arc of the same chord?', 'They are supplementary (add to $180°$).')])
b.S(78, 'In a circle of radius 5 cm, can a chord be 12 cm long? What is the longest chord?', 'No; the longest chord is the diameter, 10 cm.',
    ['Step 1: the longest chord passes through the centre — the diameter.', 'Step 2: $d = 2r = 10$ cm < 12 cm.'],
    'No chord is longer than the diameter.', [('Radius 4 cm: is a point 5 cm from the centre inside, on or outside the circle?', 'Outside.')])

c = QSet('3.3 Practice — chords, secants and tangents', 's33')
c.S(101, 'Chords $RS$ and $TQ$ cross at $E$. $RE = 4$, $ES = 6$, $EQ = 3$. Find $TE$.', '$TE = 8$',
    ['Step 1: $RE \\cdot ES = TE \\cdot EQ$.', 'Step 2: $4 \\times 6 = 3 \\cdot TE$.', 'Step 3: $TE = 24 \\div 3 = 8$.'],
    'Inside: part × part = part × part.', [('$RE = 9$, $ES = 2$, $TE = 3$. Find $EQ$.', '$6$.')])
c.S(101, 'Secants $PAB$ and $PCD$: $PA = 5$, $PC = 6$, $CD = 4$. Find $PB$.', '$PB = 12$',
    ['Step 1: $PD = 6 + 4 = 10$.', 'Step 2: $PA \\cdot PB = PC \\cdot PD$: $5 \\cdot PB = 60$.', 'Step 3: $PB = 12$.'],
    'Outside part × WHOLE secant on both lines.', [('$PB = 10$, $PC = 5$, $CD = 3$. Find $PA$.', '$PA = 4$ ($PA \\cdot 10 = 5 \\cdot 8$).')])
c.S(102, 'From $P$ a tangent touches at $A$; a secant cuts at $B$ and $C$ with $PB = 4$ and $BC = 5$. Find $PA$.', '$PA = 6$',
    ['Step 1: $PC = 4 + 5 = 9$.', 'Step 2: $PA^2 = PB \\cdot PC = 36$.', 'Step 3: $PA = 6$.'],
    'Tangent squared = outside part × whole secant.', [('$PA = 6$, $BC = 5$. Find $PB$.', '$PB = 4$ ($PB(PB + 5) = 36$).')])
c.M(101, 'Secants $PAB$ and $PCD$ with $PB = 20$, $PC = 10$, $DC = 6$. Then $AB =$', ['8', '12', '6', '16'], 'B',
    ['Step 1: $PD = 16$; $PA \\cdot 20 = 10 \\cdot 16 = 160 \\Rightarrow PA = 8$.', 'Step 2: $AB = PB - PA = 20 - 8 = 12$.'],
    'Find the outside part first, then subtract from the whole.', [('$PB = 15$, $PC = 6$, $PD = 10$. Find $AB$.', '$PA = 4$, so $AB = 11$.')])
c.S(102, 'A tangent from $P$ has length 8 cm. A secant from $P$ through the centre has outside part 4 cm. Find the radius.', '6 cm',
    ['Step 1: whole secant $= 4 + 2r$.', 'Step 2: $8^2 = 4(4 + 2r) \\Rightarrow 64 = 16 + 8r$.', 'Step 3: $8r = 48 \\Rightarrow r = 6$ cm.'],
    'A secant through the centre has inside part = diameter.', [('Tangent 12, outside part 8 of a secant through the centre. Radius?', '5.')])
c.S(97, 'Two chords cross inside a circle; one is cut into 3 cm and 8 cm. The other is cut into two equal parts. How long is the other chord?', '$4\\sqrt6 \\approx 9.8$ cm',
    ['Step 1: let each part be $x$: $x \\cdot x = 3 \\cdot 8 = 24$.', 'Step 2: $x = \\sqrt{24} = 2\\sqrt6$.', 'Step 3: chord $= 2x = 4\\sqrt6 \\approx 9.80$ cm.'],
    'Equal parts → square one of them.', [('One chord is cut into 2 and 18; the other chord is bisected. Find its length.', '12.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Polygon', 'A closed plane figure made of line segments that meet only at their end points.', 57),
    ('Regular polygon', 'A polygon that is both equilateral and equiangular.', 58),
    ('Exterior angle', 'The angle between one side of a polygon and the extension of the next side.', 69),
    ('Chord', 'A segment joining two points of a circle.', 75),
    ('Arc', 'A part of a circle; its measure is that of the central angle on it.', 76),
    ('Central angle', 'An angle whose vertex is the centre of the circle.', 77),
    ('Inscribed angle', 'An angle whose vertex is on the circle and whose arms are chords.', 77),
    ('Cyclic quadrilateral', 'A quadrilateral whose four vertices lie on a circle.', 82),
    ('Tangent', 'A line that meets a circle at exactly one point.', 88),
    ('Secant', 'A line that cuts a circle at two points.', 97),
    ('Point of contact', 'The single point where a tangent touches the circle.', 88),
]
TIPS = [
    ('Polygon angles: interior sum (n − 2)·180°; exterior sum always 360°; regular: each exterior = 360°/n.', 73),
    ('Circle angles: centre = arc, on the circle = ½ arc, inside = ½ (sum of arcs), outside = ½ (difference of arcs).', 93),
    ('Segment lengths: inside part × part; outside: outside part × whole secant; tangent squared.', 100),
]
IDEAS = [('poly', 'Polygon angle table', 'l3_1', 'math10-u3-md-angles-t'), ('circ', 'Circle angle rules', 'l3_2', 'math10-u3-md-circle-angles'),
         ('seg', 'Segment theorems', 'l3_3', 'math10-u3-md-seg-t')]
