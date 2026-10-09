r"""Grade 10 Unit 2 — Geometric Structure (textbook pp. 30-55)."""
import math
from common import set_unit, T, RM, MN, TB, DG, ST, WK, GR, CK, QSet, plane
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL, polar, mid, lerp
from figs_common import side_by_side

UID = 'math10-u2'
set_unit(UID)


def upto(i, k):
    """step keys k<i> .. k<k> (an element drawn at step i stays for the later steps)"""
    return ' '.join(f'k{j}' for j in range(i, k + 1))


# ------------------------------------------------------------------ figures
def f_plp():
    f = Fig(320, 170)
    f.poly([(40, 130), (110, 40), (300, 40), (230, 130)], BLUE, 1.8, FILL[BLUE])
    f.text(285, 60, 'plane m', 13, BLUE, 'end', italic=True)
    f.arrow(70, 112, 215, 58, INK, 2, 8, both=True)
    f.arrow(95, 64, 230, 118, INK, 2, 8, both=True)
    cx, cy = 152.6, 81.6
    f.dot(cx, cy, RED).ptlabel(cx, cy, 'C', 's', RED)
    f.dot(120, 93.4, INK).ptlabel(120, 93.4, 'A', 'n')
    f.dot(190, 108, INK).ptlabel(190, 108, 'B', 'n')
    f.text(216, 52, 'k', 13, INK, italic=True)
    f.text(236, 126, 'h', 13, INK, italic=True)
    f.text(160, 160, 'lines h and k lie in plane m and meet at the point C', 11.5, GREY, bold=False)
    return f


def f_postulates():
    a = Fig(150, 120)
    a.arrow(10, 90, 140, 30, INK, 2, 8, both=True)
    a.dot(45, 74, RED).ptlabel(45, 74, 'P', 's', RED)
    a.dot(105, 46, RED).ptlabel(105, 46, 'Q', 's', RED)
    a.text(75, 112, 'exactly one line', 11.5, INK)
    b = Fig(170, 120)
    b.poly([(10, 90), (50, 25), (165, 25), (125, 90)], BLUE, 1.6, FILL[BLUE])
    for (x, y), l in [((55, 75), 'A'), ((85, 38), 'B'), ((125, 62), 'C')]:
        b.dot(x, y, RED).ptlabel(x, y, l, 'e', RED)
    b.text(85, 112, 'exactly one plane', 11.5, INK)
    return side_by_side([a, b], 6, ['two points', 'three non-collinear points'])


def f_collinear():
    f = Fig(320, 120)
    f.arrow(20, 80, 300, 30, INK, 2, 8, both=True)
    for x, l in [(70, 'A'), (150, 'B'), (240, 'C')]:
        y = 80 - (x - 20) * 50 / 280
        f.dot(x, y, BLUE).ptlabel(x, y, l, 'n', BLUE)
    f.dot(170, 95, RED).ptlabel(170, 95, 'D', 'e', RED)
    f.text(160, 115, 'A, B, C are collinear;  A, B, D are not', 12, INK)
    return f


def f_copyseg():
    f = Fig(320, 150)
    P, Q = (30, 40), (150, 40)
    f.line(*P, *Q, INK, 2.4)
    for p, l in [(P, 'P'), (Q, 'Q')]:
        f.dot(*p, INK).ptlabel(*p, l, 'n')
    R = (30, 110)
    f.g(upto(1, 4)).arrow(R[0], R[1], 300, 110, GREY, 1.6, 7).dot(*R, BLUE).ptlabel(*R, 'R', 's', BLUE).end()
    f.g(upto(2, 4)).arc(P, 120, -12, 12, ORANGE, 1.6).line(*P, 145, 30, ORANGE, 1.4, dash='4 3').end()
    f.g(upto(3, 4)).arc(R, 120, -14, 14, ORANGE, 2).end()
    f.g('k4').dot(150, 110, RED).ptlabel(150, 110, 'S', 's', RED).line(*R, 150, 110, RED, 3).end()
    return f


def f_bisectseg():
    f = Fig(320, 200)
    A, B = (80, 100), (240, 100)
    r = 110
    f.line(*A, *B, INK, 2.4)
    f.dot(*A).ptlabel(*A, 'A', 'w').dot(*B).ptlabel(*B, 'B', 'e')
    h = math.sqrt(r * r - 80 * 80)
    Pp, Qp = (160, 100 - h), (160, 100 + h)
    t = math.degrees(math.atan2(h, 80))
    f.g(upto(1, 4)).arc(A, r, t - 12, t + 12, ORANGE, 1.8).arc(A, r, -t - 12, -t + 12, ORANGE, 1.8).end()
    f.g(upto(2, 4)).arc(B, r, 180 - t - 12, 180 - t + 12, PURPLE, 1.8).arc(B, r, 180 + t - 12, 180 + t + 12, PURPLE, 1.8).end()
    f.g(upto(3, 4)).dot(*Pp, RED).ptlabel(*Pp, 'P', 'e', RED).dot(*Qp, RED).ptlabel(*Qp, 'Q', 'e', RED).line(*Pp, *Qp, RED, 2, dash=True).end()
    f.g('k4').dot(160, 100, GREEN, 4.5).ptlabel(160, 100, 'M', 'ne', GREEN).ticks(A, (160, 100), 1, GREEN).ticks((160, 100), B, 1, GREEN).right((160, 100), B, Pp, 9, GREEN).end()
    return f


def f_copyangle():
    f = Fig(330, 170)
    A = (25, 140)
    a1, a2 = (150, 140), polar(A, 125, 40)
    f.line(*A, *a1, INK, 2.2).line(*A, *a2, INK, 2.2)
    f.dot(*A).ptlabel(*A, 'A', 'sw')
    D = (185, 140)
    E2 = (320, 140)
    f.g(upto(1, 4)).line(*D, *E2, INK, 2.2).dot(*D).ptlabel(*D, 'D', 'sw').end()
    r = 70
    B, C = polar(A, r, 0), polar(A, r, 40)
    E, F = polar(D, r, 0), polar(D, r, 40)
    f.g(upto(2, 4)).arc(A, r, -8, 52, ORANGE, 1.8).arc(D, r, -8, 55, ORANGE, 1.8)
    f.dot(*B, ORANGE, 3).ptlabel(*B, 'B', 's', ORANGE).dot(*C, ORANGE, 3).ptlabel(*C, 'C', 'nw', ORANGE)
    f.dot(*E, ORANGE, 3).ptlabel(*E, 'E', 's', ORANGE).end()
    bc = math.dist(B, C)
    ang = math.degrees(math.atan2(-(F[1] - E[1]), F[0] - E[0]))
    f.g(upto(3, 4)).line(*B, *C, PURPLE, 1.4, dash='4 3').arc(E, bc, ang - 15, ang + 15, PURPLE, 1.8).dot(*F, RED, 3).ptlabel(*F, 'F', 'ne', RED).end()
    f.g('k4').line(*D, *polar(D, 125, 40), RED, 2.4).angle(D, E2, polar(D, 50, 40), 26, RED).angle(A, a1, a2, 26, RED).end()
    return f


def f_bisectangle():
    f = Fig(300, 190)
    P = (30, 165)
    f.line(*P, 280, 165, INK, 2.2).line(*P, *polar(P, 250, 60), INK, 2.2)
    f.dot(*P).ptlabel(*P, 'P', 'sw')
    r = 90
    Q, R = polar(P, r, 60), polar(P, r, 0)
    f.g(upto(1, 4)).arc(P, r, -6, 66, ORANGE, 1.8).dot(*Q, ORANGE, 3).ptlabel(*Q, 'Q', 'w', ORANGE).dot(*R, ORANGE, 3).ptlabel(*R, 'R', 's', ORANGE).end()
    W = polar(P, 2 * r * math.cos(math.radians(30)), 30)
    f.g(upto(2, 4)).arc(Q, 90, -22, 22, PURPLE, 1.8).end()
    f.g(upto(3, 4)).arc(R, 90, 38, 82, PURPLE, 1.8).dot(*W, RED, 3.4).ptlabel(*W, 'W', 'ne', RED).end()
    f.g('k4').line(*P, *polar(P, 250, 30), RED, 2.4).angle(P, R, W, 50, RED, '30°', 64).angle(P, W, Q, 56, RED, '30°', 70).end()
    return f


def f_hexagon():
    f = Fig(300, 230)
    O = (150, 118)
    r = 95
    f.circle(*O, r, INK, 1.8)
    pts = [polar(O, r, k * 60) for k in range(6)]
    f.poly(pts, BLUE, 2.4, FILL[BLUE])
    for k, l in enumerate('ABCDEF'):
        p = pts[k]
        f.dot(*p, BLUE).ptlabel(*p, l, ['e', 'ne', 'nw', 'w', 'sw', 'se'][k], BLUE)
    for p in pts:
        f.line(*O, *p, GREY, 1.2, dash='4 3')
    f.dot(*O).ptlabel(*O, 'O', 's')
    f.angle(O, pts[0], pts[1], 24, RED, '60°', 38)
    f.text(150, 226, '360° ÷ 6 = 60° at the centre; each side = radius', 11.5, INK)
    return f


def f_rect_circle():
    f = Fig(300, 230)
    O = (150, 112)
    s = 18  # px per unit
    w, h = 8 * s, 6 * s
    A, B, C, D = (O[0] - w / 2, O[1] + h / 2), (O[0] + w / 2, O[1] + h / 2), (O[0] + w / 2, O[1] - h / 2), (O[0] - w / 2, O[1] - h / 2)
    f.circle(*O, 5 * s, INK, 1.8)
    f.poly([A, B, C, D], BLUE, 2.4, FILL[BLUE])
    f.line(*A, *C, RED, 2, dash=True).line(*B, *D, RED, 2, dash=True)
    f.dot(*O, RED).ptlabel(*O, 'O', 'e', RED)
    f.seglabel(A, B, '8', 12, BLUE, 13, -1)
    f.seglabel(B, C, '6', 12, BLUE, 13, -1)
    f.label(O[0] - 28, O[1] - 26, '5', size=13, c=RED)
    for p in (A, B, C, D):
        f.right(p, (O[0], p[1]), (p[0], O[1]), 8, INK)
    f.text(150, 222, 'diagonal = √(8² + 6²) = 10, so radius = 5', 12, INK)
    return f


def f_vert():
    f = Fig(300, 170)
    O = (150, 85)
    a, c = polar(O, 130, 155), polar(O, 130, -25)
    d, b = polar(O, 130, 30), polar(O, 130, 210)
    f.line(*a, *c, INK, 2.2).line(*d, *b, INK, 2.2)
    f.ptlabel(*a, 'A', 'w').ptlabel(*c, 'C', 'e').ptlabel(*d, 'D', 'e').ptlabel(*b, 'B', 'w')
    f.angle(O, a, d, 22, RED, 'x', 36, fill=FILL[RED])
    f.angle(O, c, b, 22, RED, 'x', 36, fill=FILL[RED])
    f.angle(O, d, c, 28, BLUE, 'y', 42, fill=FILL[BLUE])
    f.angle(O, b, a, 28, BLUE, 'y', 42, fill=FILL[BLUE])
    f.dot(*O).ptlabel(*O, 'O', 's', size=12)
    return f


def f_transversal():
    f = Fig(320, 200)
    y1, y2 = 60, 140
    f.arrow(15, y1, 305, y1, INK, 2.2, 8).arrow(15, y2, 305, y2, INK, 2.2, 8)
    f.par((15, y1), (305, y1), 1).par((15, y2), (305, y2), 1)
    f.text(300, y1 - 8, 'h', 13, INK, 'end', italic=True).text(300, y2 - 8, 'k', 13, INK, 'end', italic=True)
    P, Q = (190, y1), (130, y2)
    t0, t1 = lerp(P, Q, -0.55), lerp(P, Q, 1.55)
    f.line(*t0, *t1, BLUE, 2.2)
    f.text(t0[0] + 8, t0[1] + 4, 'm', 13, BLUE, 'start', italic=True)
    f.angle(P, (15, y1), Q, 22, RED, '1', 34, fill=FILL[RED])
    f.angle(Q, (305, y2), P, 22, RED, '2', 34, fill=FILL[RED])
    f.angle(P, (15, y1), t0, 20, GREEN, '3', 32, fill=FILL[GREEN])
    f.angle(Q, (15, y2), P, 20, GREEN, '4', 32, fill=FILL[GREEN])
    f.text(160, 190, 'alternate: 1 = 2     corresponding: 3 = 4', 12.5, INK)
    return f


def f_regions():
    figs = []
    for k in (1, 2, 3):
        g = Fig(100, 100)
        g.circle(50, 50, 40, BLUE, 2, FILL[BLUE])
        for j in range(k):
            a = 90 + j * 180 / k
            p, q = polar((50, 50), 40, a), polar((50, 50), 40, a + 180)
            g.line(*p, *q, INK, 1.8)
        figs.append(g)
    return side_by_side(figs, 10, ['1 line: 2', '2 lines: 4', '3 lines: 6'])


def f_exterior():
    f = Fig(320, 170)
    A, B, C = (40, 140), (180, 30), (230, 140)
    D = (310, 140)
    f.poly([A, B, C], INK, 2.2, FILL[GREY])
    f.line(*C, *D, INK, 2.2, dash='6 4')
    f.ptlabel(*A, 'A', 'sw').ptlabel(*B, 'B', 'n').ptlabel(*C, 'C', 's')
    f.angle(A, C, B, 26, BLUE, 'c', 40, fill=FILL[BLUE])
    f.angle(B, A, C, 22, GREEN, 'b', 36, fill=FILL[GREEN])
    f.angle(C, B, A, 20, ORANGE, 'a', 32, fill=FILL[ORANGE])
    f.angle(C, D, B, 24, RED, 'x', 38, fill=FILL[RED])
    f.text(160, 166, 'exterior angle x = b + c', 12.5, INK)
    return f


def f_triangulate():
    figs = []
    for nside, name in ((4, 'quadrilateral'), (5, 'pentagon'), (6, 'hexagon')):
        g = Fig(104, 100)
        pts = [polar((52, 52), 42, 90 + 360 * i / nside + (45 if nside == 4 else 0)) for i in range(nside)]
        g.poly(pts, BLUE, 2, FILL[BLUE])
        for p in pts[2:-1]:
            g.line(*pts[0], *p, RED, 1.6, dash='5 3')
        g.dot(*pts[0], RED)
        figs.append(g)
    return side_by_side(figs, 8, ['4 sides: 2', '5 sides: 3', '6 sides: 4'])


def f_venn():
    f = Fig(320, 160)
    f.rect(10, 10, 300, 140, INK, 1.4, 'none', 12)
    f.text(22, 30, 'all figures', 11, GREY, 'start', bold=False)
    f.ellipse(170, 85, 130, 58, BLUE, 2, FILL[BLUE])
    f.text(255, 60, 'polygons', 13, BLUE)
    f.ellipse(120, 92, 58, 36, RED, 2, FILL[RED])
    f.text(120, 96, 'triangles', 13, RED)
    f.dot(250, 100, BLUE).ptlabel(250, 100, 'a square', 'e', BLUE, 11)
    return f


DIAGRAMS = {
    'plp': (f_plp(), 'Points, lines and a plane', 32),
    'postulates': (f_postulates(), 'Two postulates: points determine lines and planes', 35),
    'collinear': (f_collinear(), 'Collinear and non-collinear points', 33),
    'copyseg': (f_copyseg(), 'Copying a segment with compass and straightedge', 36),
    'bisectseg': (f_bisectseg(), 'Bisecting a segment (perpendicular bisector)', 39),
    'copyangle': (f_copyangle(), 'Copying an angle', 40),
    'bisectangle': (f_bisectangle(), 'Bisecting an angle', 42),
    'hexagon': (f_hexagon(), 'A regular hexagon inscribed in a circle', 45),
    'rectcircle': (f_rect_circle(), 'A rectangle inscribed in a circle', 45),
    'vert': (f_vert(), 'Vertically opposite angles', 46),
    'transversal': (f_transversal(), 'Parallel lines cut by a transversal', 47),
    'regions': (f_regions(), 'Lines through the centre cut a circle into regions', 49),
    'exterior': (f_exterior(), 'Exterior angle of a triangle', 53),
    'triangulate': (f_triangulate(), 'Diagonals from one vertex split a polygon into triangles', 55),
    'venn': (f_venn(), 'Every triangle is a polygon, but not every polygon is a triangle', 52),
}

# ------------------------------------------------------------------ 2.1
L21 = [
    T('=math10-u2-c01', '2.1 Why geometry starts with undefined terms', 30,
      'Try to define a square: "a quadrilateral with four equal sides and four right angles". Then define *side* ("a line segment"), then *segment* ("two points and all points between them"), then *point*… Sooner or later you go round in circles. To stop this, geometry **chooses a few simple words that are not defined**: **point, line and plane**. Everything else is built from them.',
      '- **Point**: an exact position. It has no length, width or thickness. Drawn as a dot, named with a capital letter ($A$), or by coordinates $(x, y)$ on the plane.',
      '- **Line**: straight, no thickness, goes on for ever in both directions (drawn with two arrowheads). Named by a small letter ($l$, $h$) or two of its points ($\\overleftrightarrow{AB}$).',
      '- **Plane**: a flat surface with no thickness that goes on for ever in all directions. Drawn like a table top (a parallelogram) and named with a letter ($m$) — the drawing has edges, the plane does not.',
      'Real objects only *model* these ideas: the tip of a needle or a corner of a box ≈ point; the edge of a table ≈ line; the floor or a TV screen ≈ plane.'),
    DG('plp', 'Undefined terms in one picture', 32, 'plp'),
    T('defs', 'Definitions are built from undefined terms', 33,
      'A **definition** gives the exact meaning of a new word using undefined terms and words defined earlier. A good definition is short, precise and can be read both ways ("if… then…" and "only if").',
      '- **Collinear points** are points that lie on the same line.',
      '- **Coplanar points** are points that lie in the same plane.',
      '- A **line segment** $\\overline{AB}$ is the points $A$ and $B$ and all the points of the line between them.',
      '- A **ray** $\\overrightarrow{AB}$ starts at $A$ and goes on for ever through $B$.',
      '- An **angle** is two rays with a common end point (the **vertex**).',
      '"A line is a set of points" is a poor definition: a circle is also a set of points. It does not say which points.'),
    DG('collinear', 'Collinear means "on one line"', 33, 'collinear'),
    T('axioms', 'Axioms (postulates) and theorems', 34,
      'Just as we cannot define every word, we cannot **prove** every statement — a proof must start somewhere. So we accept a few basic statements **without proof**. These are **axioms** or **postulates**. Statements that we **prove** from axioms, definitions and earlier theorems are **theorems**.',
      'Postulates about points, lines and planes:',
      '- **P1.** A line contains at least two points; a plane contains at least three non-collinear points.',
      '- **P2.** Through any two points there is **exactly one** line.',
      '- **P3.** Through any three non-collinear points there is **exactly one** plane.',
      '- **P4.** If two planes intersect, their intersection is a line.',
      'Other familiar axioms (common notions): things equal to the same thing are equal to each other; the whole is greater than the part; the shortest path between two points is the straight segment joining them.'),
    DG('postulates', 'Postulates P2 and P3', 35, 'postulates',
       'Why a three-legged stool never wobbles: its three feet are three non-collinear points, and they fix exactly one plane — the floor.'),
    TB('axsys', 'The four building blocks of an axiomatic system', 35, ['Part', 'Proved / defined?', 'Examples'],
       [['Undefined terms', 'not defined (described only)', 'point, line, plane'],
        ['Defined terms', 'defined from undefined and earlier terms', 'segment, ray, angle, collinear, square'],
        ['Axioms / postulates', 'accepted without proof', 'through two points there is exactly one line'],
        ['Theorems', 'proved from axioms, definitions and earlier theorems', 'vertically opposite angles are equal']],
       'Terms : undefined → defined. Statements : axioms → theorems. Keep the two ladders apart.'),
    WK('ex-21', 'Worked example: theorem or axiom?', 34,
       'Sort into axioms and theorems: (a) the whole is greater than the part; (b) an exterior angle of a triangle equals the sum of the two opposite interior angles; (c) things equal to the same thing are equal to each other; (d) in an isosceles triangle the line from the vertex to the midpoint of the base is perpendicular to the base.',
       ['Ask: "is this so basic that we simply accept it, or can it be shown from simpler facts?"',
        '(a) and (c) are obvious common notions, accepted without proof → **axioms**.',
        '(b) follows from the angle sum of a triangle and a straight angle → **theorem** (proved in 2.4).',
        '(d) follows from congruent triangles (SSS) → **theorem**.'],
       'Axioms: (a), (c). Theorems: (b), (d).'),
    'math10-u2-tbl1',
]

# ------------------------------------------------------------------ 2.2
L22 = [
    T('=math10-u2-c02', '2.2 Attributes of figures and constructions', 36,
      'Geometric figures are described by their **attributes**: the number of sides, the lengths of the sides, the sizes of the angles, which sides are parallel or perpendicular, what the diagonals do, and so on. A square, for example, has 4 equal sides, 4 right angles, 2 pairs of parallel sides and equal diagonals that bisect each other at right angles.',
      'A **construction** is an accurate drawing made with only two tools: a **straightedge** (a ruler without marks, for straight lines) and a **compass** (for circles and arcs). We do not measure with a ruler scale or a protractor — the compass copies lengths for us.',
      'Why this works: every point on an arc is the same distance (the radius) from the centre. So two arcs of the same radius transfer a length exactly.'),
    ST('copyseg', 'Construction 1: copy a segment PQ', 37, 'copyseg',
       [('Draw a ray and mark its end point $R$ — the new segment will start here.', 'k1'),
        ('Put the compass point on $P$ and open it until the pencil is on $Q$. The compass width is now $PQ$.', 'k2'),
        ('Without changing the width, put the point on $R$ and draw an arc across the ray.', 'k3'),
        ('Call the crossing point $S$. Then $RS = PQ$, because both are radii of the same compass setting.', 'k4')]),
    ST('bisectseg', 'Construction 2: bisect a segment AB (find its midpoint)', 39, 'bisectseg',
       [('Open the compass to more than half of $AB$ (using $AB$ itself is easy). With centre $A$ draw arcs above and below the segment.', 'k1'),
        ('With the **same** width and centre $B$ draw arcs that cross the first ones.', 'k2'),
        ('Name the crossing points $P$ and $Q$ and join them with the straightedge.', 'k3'),
        ('$PQ$ cuts $AB$ at its midpoint $M$, and at right angles: $PQ$ is the **perpendicular bisector** of $AB$. ($P$ and $Q$ are each the same distance from $A$ and $B$.)', 'k4')]),
    ST('copyangle', 'Construction 3: copy an angle A', 40, 'copyangle',
       [('Draw a ray with end point $D$.', 'k1'),
        ('With centre $A$ draw an arc cutting both arms at $B$ and $C$. With the same width and centre $D$ draw a long arc cutting the ray at $E$.', 'k2'),
        ('Set the compass to the distance $BC$. With centre $E$ draw an arc crossing the long arc at $F$.', 'k3'),
        ('Draw ray $DF$. Then $\\angle EDF = \\angle BAC$ (triangles $ABC$ and $DEF$ have three equal sides).', 'k4')]),
    ST('bisectangle', 'Construction 4: bisect an angle P', 42, 'bisectangle',
       [('With centre $P$ draw an arc cutting both arms at $Q$ and $R$.', 'k1'),
        ('With centre $Q$ draw an arc inside the angle.', 'k2'),
        ('With the same width and centre $R$ draw an arc crossing it at $W$.', 'k3'),
        ('Draw ray $PW$: it is the **angle bisector** — here a 60° angle is cut into two 30° angles.', 'k4')]),
    TB('constr-t', 'The four basic constructions at a glance', 39, ['Construction', 'Key idea', 'Arcs needed'],
       [['Copy a segment', 'compass width = the length', '1'],
        ['Bisect a segment', 'two equal arcs from each end meet on the perpendicular bisector', '4 (2 from each end)'],
        ['Copy an angle', 'copy two lengths: the radius and the chord $BC$', '3'],
        ['Bisect an angle', 'equal arcs from $Q$ and $R$ meet on the bisector', '3']],
       'Never change the compass width in the middle of one step — the equal widths are what make the construction exact.'),
    T('inscribed', 'Polygons inscribed in a circle', 44,
      'A polygon is **inscribed** in a circle when **every vertex lies on the circle**. Any points on the circle, joined in order, give an inscribed polygon.',
      'A **regular** inscribed polygon (all sides equal) with $n$ sides: divide the full turn $360°$ by $n$ to get the angle at the centre, $\\frac{360°}{n}$. Mark that angle again and again from a radius; the points on the circle are the vertices.',
      '- Hexagon: $360° \\div 6 = 60°$. Each central triangle is equilateral, so **each side equals the radius** — you can step the compass (set to the radius) six times round the circle.',
      '- Square: $360° \\div 4 = 90°$: draw two perpendicular diameters.',
      '- Octagon: $360° \\div 8 = 45°$: bisect the right angles of the square.',
      'For an inscribed **rectangle**, the diagonals are diameters, so the centre is where the diagonals cross.'),
    DG('hexagon', 'Regular hexagon: step the radius six times', 45, 'hexagon'),
    DG('rectcircle', 'Rectangle 8 × 6 inscribed in a circle', 45, 'rectcircle',
       'The diagonal is a diameter: $d = \\sqrt{8^2 + 6^2} = \\sqrt{100} = 10$, so the radius is $5$ and the centre is the crossing point of the diagonals.'),
    WK('ex-22a', 'Worked example: the side of a square inscribed in a circle', 44,
       'A square $ABCD$ is inscribed in a circle of radius 3 cm. Find the length of one side.',
       ['The diagonals of the square are diameters: $AC = 2 \\times 3 = 6$ cm.',
        'Triangle $ABC$ has a right angle at $B$ and $AB = BC = s$. By Pythagoras $s^2 + s^2 = 6^2$.',
        '$2s^2 = 36 \\Rightarrow s^2 = 18 \\Rightarrow s = \\sqrt{18} = 3\\sqrt2 \\approx 4.24$ cm.'],
       '$3\\sqrt2 \\approx 4.24$ cm'),
    'math10-u2-wk2',
    WK('ex-22b', 'Worked example: segments from given segments', 38,
       '$AB = 3$ cm and $CD = 2$ cm. Describe how to construct segments of length $AB + CD$ and $CD + 2AB$ with compass and straightedge only.',
       ['Draw a long ray from a point $X$.',
        'Set the compass to $AB$; from $X$ cut the ray at $Y$: $XY = 3$ cm.',
        'Set the compass to $CD$; from $Y$ cut the ray further at $Z$: $XZ = AB + CD = 5$ cm.',
        'For $CD + 2AB$: step $AB$ twice from $X$ (to $Y$, then to $Y\'$), then step $CD$ once: total $3 + 3 + 2 = 8$ cm.'],
       'Lay the copied lengths end to end along one ray.'),
]

# ------------------------------------------------------------------ 2.3
L23 = [
    T('=math10-u2-c03', '2.3 Conjectures — educated guesses from patterns', 46,
      'A **conjecture** is a statement that **seems** true because of what we observed in drawings, measurements or examples, but which has **not been proved yet**. Making conjectures is how new mathematics is discovered.',
      'How to make a conjecture: (1) draw or calculate several cases; (2) record the results in a table; (3) look for what stays the same; (4) state it as a general sentence.',
      'Examples from drawings:',
      '- Two intersecting lines: the opposite angles always measure the same → conjecture "**vertically opposite angles are equal**".',
      '- Parallel lines and a transversal: the alternate interior angles always match → "**alternate angles are equal**".',
      '- Measure the angles of many triangles: the total is always about $180°$ → "**the angles of a triangle add up to $180°$**".',
      'A conjecture can be **false**. Measurements are never exact, and a pattern can break later. One **counter-example** is enough to show a conjecture is false; but no number of examples proves it true — only a proof does.'),
    DG('vert', 'Conjecture: vertically opposite angles are equal', 46, 'vert',
       'Lines $AC$ and $BD$ cross at $O$. The angles marked $x$ face each other; so do the angles marked $y$. Measure them: they match. In 2.4 we prove it.'),
    DG('transversal', 'Conjecture: alternate angles are equal', 47, 'transversal',
       'Line $m$ cuts the parallel lines $h$ and $k$. The alternate interior angles 1 and 2 (a "Z" shape) are equal; the corresponding angles 3 and 4 (an "F" shape) are equal; co-interior angles such as 1 and 4 (a "C" shape) add up to $180°$.'),
    TB('parallel-t', 'Angles formed by parallel lines and a transversal', 47, ['Pair', 'Shape to spot', 'Relationship'],
       [['Alternate interior', 'Z', 'equal'],
        ['Corresponding', 'F', 'equal'],
        ['Co-interior (same side)', 'C or U', 'add up to $180°$'],
        ['Vertically opposite', 'X', 'equal (parallel lines not needed)']]),
    'math10-u2-c04',
    WK('ex-23a', 'Worked example: making a conjecture from a table', 49,
       'A circle is cut by lines through its centre. 1 line gives 2 regions, 2 lines give 4, 3 lines give 6. Make a conjecture for $n$ lines and use it for 5 and 8 lines.',
       ['Table: $n$ = 1, 2, 3 → regions 2, 4, 6.',
        'Each new line through the centre adds 2 regions (it cuts two old regions in half).',
        'Conjecture: $n$ lines through the centre give $2n$ regions.',
        'For 5 lines: $2 \\times 5 = 10$; for 8 lines: $16$ regions. (Check one by drawing — 4 lines give 8.)'],
       '$2n$ regions; 10 and 16'),
    DG('regions', 'Counting regions', 49, 'regions'),
    'math10-u2-wk3',
    WK('ex-23b', 'Worked example: a conjecture that breaks', 48,
       'Points are put on a circle and every pair is joined. 2 points → 2 regions, 3 → 4, 4 → 8, 5 → 16. Conjecture: $n$ points give $2^{n-1}$ regions. Is it true?',
       ['The pattern 2, 4, 8, 16 suggests doubling, so 6 points should give 32 regions.',
        'Draw it carefully (points not evenly spaced so that no three chords meet at one point): you get only **31** regions.',
        'One counter-example is enough: the conjecture is **false**, even though it worked four times.'],
       'False — 6 points give 31 regions, not 32.'),
    MN('tip23', 'Tip: verification is not proof', 50,
       'Checking examples (3 + 5 = 8, 7 + 9 = 16…) **verifies** a conjecture for those numbers only. A **proof** must work for every case — usually by using letters, e.g. odd numbers $2m + 1$ and $2n + 1$.'),
]

# ------------------------------------------------------------------ 2.4
L24 = [
    T('=math10-u2-c06', '2.4 Inductive and deductive reasoning', 48,
      '**Inductive reasoning** goes from several particular cases to a general conclusion (a conjecture). Example: the angles of the five triangles I drew add up to about $180°$, so every triangle probably has angle sum $180°$. It is useful for discovering, but the conclusion **may be false**.',
      '**Deductive reasoning** goes from accepted general statements (definitions, axioms, proved theorems) to a conclusion that **must** be true. Example: "All mammals are warm-blooded. A cow is a mammal. Therefore a cow is warm-blooded."',
      'The deductive pattern: **If $p$ then $q$. $p$ is true. Therefore $q$ is true.** ("All rectangles are parallelograms; $ABCD$ is a rectangle; so $ABCD$ is a parallelogram.")',
      'A **proof** is a chain of deductive steps, each justified by a reason (given, definition, axiom or earlier theorem), that leads from the hypothesis to the conclusion. Once a conjecture is proved it becomes a **theorem**.'),
    TB('reason-t', 'Inductive vs deductive reasoning', 50, ['', 'Inductive', 'Deductive'],
       [['Direction', 'particular cases → general rule', 'general rules → particular case'],
        ['Based on', 'observation, measurement, examples', 'definitions, axioms, theorems'],
        ['Result', 'a conjecture (may be false)', 'a certain conclusion (a theorem)'],
        ['Example', '3 + 5, 7 + 9, 11 + 1 are even ⇒ odd + odd is even?', '$(2m + 1) + (2n + 1) = 2(m + n + 1)$ is even']]),
    T('cond', 'Conditional statements and converses', 51,
      'Most theorems are **conditional statements**: "**If** $p$, **then** $q$." The part after *if* ($p$) is the **hypothesis** (what is given); the part after *then* ($q$) is the **conclusion** (what must be proved).',
      'The **converse** swaps them: "If $q$, then $p$." A true statement can have a **false** converse:',
      '- "If a figure is a triangle, then it is a polygon." — true.',
      '- Converse: "If a figure is a polygon, then it is a triangle." — false (a square is a polygon but not a triangle).',
      'When a statement and its converse are both true we can join them with "**if and only if**": "A triangle is equilateral if and only if all its angles are $60°$."'),
    DG('venn', 'Why the converse can fail', 52, 'venn',
       'The triangles sit inside the polygons. So "triangle ⇒ polygon" is true, but a square is a polygon outside the triangles, so "polygon ⇒ triangle" is false.'),
    WK('ex-vert', 'Proof: vertically opposite angles are equal', 51,
       'Lines $AB$ and $CD$ meet at $O$. Prove that $\\angle AOD = \\angle COB$.',
       ['$\\angle AOD + \\angle DOB = 180°$ — reason: $AOB$ is a straight angle.',
        '$\\angle COB + \\angle BOD = 180°$ — reason: $COD$ is a straight angle.',
        'So $\\angle AOD + \\angle DOB = \\angle COB + \\angle DOB$ — reason: things equal to the same thing ($180°$) are equal.',
        'Subtract $\\angle DOB$ from both sides: $\\angle AOD = \\angle COB$. ∎'],
       'Vertically opposite angles are equal (a direct proof).', diagram='vert'),
    'math10-u2-wk4',
    WK('ex-ext', 'Proof: the exterior angle theorem', 53,
       'Side $AC$ of triangle $ABC$ is extended past $C$. Prove that the exterior angle $x$ at $C$ equals $b + c$, the two opposite interior angles.',
       ['$a + b + c = 180°$ — angle sum of a triangle.',
        '$x + a = 180°$ — $x$ and $a$ form a straight angle.',
        'So $x + a = a + b + c$ (both equal $180°$).',
        'Subtract $a$: $x = b + c$. ∎'],
       '$x = b + c$', diagram='exterior'),
    WK('ex-odd', 'Proof: the sum of two odd numbers is even', 50,
       'Prove that the sum of any two odd integers is even.',
       ['An even number has the form $2k$; an odd number has the form $2k + 1$ ($k$ an integer).',
        'Let the odd numbers be $x = 2m + 1$ and $y = 2n + 1$.',
        '$x + y = 2m + 2n + 2 = 2(m + n + 1)$.',
        '$m + n + 1$ is an integer, so $x + y$ is 2 times an integer: even. ∎ (Checking $3 + 5 = 8$ only verifies one case.)'],
       'Proved for all odd $x, y$.'),
    WK('ex-fake', 'Worked example: find the error in a "proof" that 2 = 1', 53,
       'Let $a = b$. Then $a^2 = ab$, $a^2 - b^2 = ab - b^2$, $(a - b)(a + b) = b(a - b)$, so $a + b = b$, $2b = b$ and $2 = 1$. What is wrong?',
       ['Every step is fine up to $(a - b)(a + b) = b(a - b)$.',
        'The next step divides both sides by $a - b$.',
        'But $a = b$, so $a - b = 0$: the "proof" **divides by zero**, which is not allowed.',
        'Lesson: each step of a proof needs a valid reason — check especially divisions and square roots.'],
       'Division by $a - b = 0$.'),
    DG('triangulate', 'Inductive reasoning with polygons', 55, 'triangulate',
       'From one vertex, an $n$-sided polygon has $n - 3$ diagonals, which cut it into $n - 2$ triangles. So the angle sum is $(n - 2) \\times 180°$ — this conjecture is proved in Unit 3.'),
    TB('triangulate-t', 'Pattern table for polygons', 55, ['Polygon', 'Sides $n$', 'Diagonals from one vertex', 'Triangles'],
       [['Triangle', '3', '0', '1'], ['Quadrilateral', '4', '1', '2'], ['Pentagon', '5', '2', '3'], ['Hexagon', '6', '3', '4'],
        ['Heptagon', '7', '4', '5'], ['Octagon', '8', '5', '6'], ['$n$-gon', '$n$', '$n - 3$', '$n - 2$']],
       'Number of triangles = number of diagonals from one vertex + 1.'),
]

LESSONS = {'math10-u2-l2-1': L21, 'math10-u2-l2-2': L22, 'math10-u2-l2-3': L23, 'math10-u2-l2-4': L24}

# ------------------------------------------------------------------ practice
a = QSet('2.1 Practice — axiomatic systems', 's21')
a.M(31, 'Which are the undefined terms of geometry?', ['angle, ray, segment', 'point, line, plane', 'triangle, square, circle', 'axiom, theorem, definition'], 'B',
    ['Step 1: undefined terms are the starting words that are only described.', 'Step 2: angle, ray and segment are defined using points and lines.', 'Step 3: so the undefined terms are point, line and plane.'],
    'If you can define it with other geometry words, it is not undefined.',
    [('Which of these is a defined term: point, ray, plane?', 'Ray (part of a line starting at a point).')])
a.M(32, 'Which object best models a plane?', ['the tip of a needle', 'the edge of a table', 'the floor of a classroom', 'the corner of a box'], 'C',
    ['Step 1: a plane is a flat surface.', 'Step 2: tip and corner are points; an edge is a line.', 'Step 3: the floor is a flat surface → plane.'],
    'Count dimensions: 0 = point, 1 = line, 2 = plane.',
    [('What does the edge of a table model?', 'A line (or segment).')])
a.TF(34, 'An axiom is a statement that is proved from theorems.', False,
     ['Step 1: axioms are accepted WITHOUT proof.', 'Step 2: theorems are the statements that are proved.'],
     'Axiom = accepted; theorem = proved.',
     [('Is "through any two points there is exactly one line" an axiom or a theorem?', 'An axiom (postulate).')])
a.S(35, 'How many lines can be drawn through two different points? Through three collinear points? Through three non-collinear points (taking two at a time)?', 'Exactly one; exactly one; three.',
    ['Step 1: postulate P2 — two points determine exactly one line.', 'Step 2: three collinear points all lie on that one line.', 'Step 3: three non-collinear points give 3 pairs → 3 different lines (the sides of a triangle).'],
    'Count pairs: $n$ points, no three collinear, give $\\frac{n(n-1)}{2}$ lines.',
    [('How many lines are determined by 4 points, no three collinear?', '6.')])
a.S(35, 'Two rays lie on the same line, have a common end point and no other common points. What angle do they form?', 'A straight angle, $180°$.',
    ['Step 1: the rays point in opposite directions from the common end point.', 'Step 2: together they make a straight line.', 'Step 3: a straight angle measures $180°$.'],
    'Opposite rays always form a straight angle.',
    [('Two rays from one point form a right angle. What is its measure?', '$90°$.')])
a.S(35, 'Why is "a line is a set of points" not a good definition?', 'It does not say which points; a circle or a triangle is also a set of points.',
    ['Step 1: a definition must pick out exactly one kind of object.', 'Step 2: many figures are sets of points.', 'Step 3: so the sentence is true about lines but does not define them.'],
    'Test a definition by looking for something else that fits it.',
    [('Is "a square is a quadrilateral with four equal sides" a complete definition?', 'No — a rhombus also fits; add "and four right angles".')])
a.M(35, 'Which statement is a postulate about planes?', ['A plane has edges', 'If two planes intersect, their intersection is a line', 'A plane contains only two points', 'Two planes always meet'], 'B',
    ['Step 1: planes have no edges (A false).', 'Step 2: a plane contains at least three non-collinear points (C false).', 'Step 3: parallel planes never meet (D false). B is postulate P4.'],
    'Picture two walls of a room: they meet along a line.',
    [('Where do the floor and a wall of a room meet?', 'Along a line (the bottom edge of the wall).')])

b = QSet('2.2 Practice — constructions and inscribed polygons', 's22')
b.M(37, 'In the construction that copies a segment $PQ$ to $RS$, why is $RS = PQ$?', ['Because we measured both with a ruler', 'Because both are radii of the same compass setting', 'Because $R$ and $P$ are the same point', 'Because the arc is a straight line'], 'B',
    ['Step 1: the compass was opened to $PQ$.', 'Step 2: the same width drew the arc from $R$.', 'Step 3: every point of that arc is $PQ$ away from $R$ — so $RS = PQ$.'],
    'In constructions, equal compass widths = equal lengths.',
    [('When bisecting a segment, why must both pairs of arcs use the same width?', 'So that the crossing points are equally far from both ends (they lie on the perpendicular bisector).')])
b.S(39, 'After bisecting a 6 cm segment $AB$ with arcs, you join the arc crossings $P$ and $Q$. Give two facts about line $PQ$.', '$PQ$ passes through the midpoint $M$ of $AB$ ($AM = MB = 3$ cm), and $PQ \\perp AB$.',
    ['Step 1: $P$ and $Q$ are each the same distance from $A$ and $B$.', 'Step 2: all such points lie on the perpendicular bisector.', 'Step 3: so $PQ$ cuts $AB$ in half at right angles.'],
    'Perpendicular bisector = "cuts in half" + "at 90°".',
    [('A 7 cm segment is bisected. How long is each half?', '3.5 cm.')])
b.S(42, 'An angle of $70°$ is bisected, and then one of the halves is bisected again. What is the size of the smallest angle?', '$17.5°$',
    ['Step 1: bisecting halves the angle: $70° \\div 2 = 35°$.', 'Step 2: bisecting again: $35° \\div 2 = 17.5°$.'],
    'Each bisection divides by 2: after $k$ bisections the angle is $\\frac{\\theta}{2^k}$.',
    [('How can you construct a $45°$ angle with compass and straightedge?', 'Construct a $90°$ angle (perpendicular bisector) and bisect it.')])
b.S(45, 'A rectangle with sides 8 and 6 units is inscribed in a circle. Find the radius and say where the centre is.', 'Radius 5 units; the centre is where the diagonals cross.',
    ['Step 1: a diagonal of an inscribed rectangle is a diameter.', 'Step 2: diagonal $= \\sqrt{8^2 + 6^2} = 10$.', 'Step 3: radius $= 10 \\div 2 = 5$; the diagonals meet at the centre.'],
    'Inscribed rectangle → diagonal = diameter (the right angle stands on a diameter).',
    [('A rectangle 12 × 5 is inscribed in a circle. Find the radius.', '6.5 units (diagonal 13).')])
b.M(45, 'To construct a regular octagon inscribed in a circle, the angle at the centre between neighbouring vertices is', ['$30°$', '$40°$', '$45°$', '$60°$'], 'C',
    ['Step 1: the full turn is $360°$.', 'Step 2: 8 equal parts: $360° \\div 8 = 45°$.'],
    'Central angle of a regular $n$-gon $= \\frac{360°}{n}$.',
    [('What is the central angle for a regular pentagon?', '$72°$.')])
b.S(44, 'A regular hexagon is inscribed in a circle of radius 4 cm. Find its perimeter.', '24 cm',
    ['Step 1: central angle $= 60°$ and the two radii are equal, so each central triangle is equilateral.', 'Step 2: so each side $= $ radius $= 4$ cm.', 'Step 3: perimeter $= 6 \\times 4 = 24$ cm.'],
    'Hexagon side = radius — the compass never needs re-setting.',
    [('A regular hexagon has perimeter 30 cm. What is the radius of its circumscribed circle?', '5 cm.')])
b.S(38, '$AB = 4$ cm and $CD = 1.5$ cm. Which length do you get by laying $AB$, $AB$ and $CD$ end to end? And $AB - CD$?', '$CD + 2AB = 9.5$ cm; $AB - CD = 2.5$ cm.',
    ['Step 1: end to end means add: $4 + 4 + 1.5 = 9.5$.', 'Step 2: for a difference, copy $AB$ then cut $CD$ back from its end: $4 - 1.5 = 2.5$.'],
    'Adding segments: lay them in the same direction; subtracting: lay the second one backwards from the end.',
    [('Construct $3CD$ if $CD = 2$ cm. How long is it?', '6 cm (step $CD$ three times).')])

c = QSet('2.3 Practice — conjectures and counter-examples', 's23')
c.M(48, 'Which is a counter-example to "every prime number is odd"?', ['3', '9', '2', '15'], 'C',
    ['Step 1: a counter-example must be prime AND not odd.', 'Step 2: 2 is prime and even.', 'Step 3: 9 and 15 are not prime; 3 is odd.'],
    'A counter-example must satisfy the hypothesis but break the conclusion.',
    [('Give a counter-example to "every quadrilateral with 4 equal sides is a square".', 'A rhombus that is not a square.')])
c.S(47, 'Two parallel lines are cut by a transversal. One alternate interior angle is $65°$. Find the other alternate interior angle and the co-interior angle next to it.', 'Alternate angle $65°$; co-interior angle $115°$.',
    ['Step 1: alternate interior angles are equal: $65°$.', 'Step 2: co-interior angles add up to $180°$: $180° - 65° = 115°$.'],
    'Z → equal, F → equal, C → add to $180°$.',
    [('A corresponding angle is $112°$. Find its co-interior partner.', '$68°$.')])
c.S(46, 'Two lines intersect. One angle is $3x + 10°$ and the vertically opposite angle is $5x - 30°$. Find $x$ and all four angles.', '$x = 20$; angles $70°, 110°, 70°, 110°$.',
    ['Step 1: vertically opposite angles are equal: $3x + 10 = 5x - 30$.', 'Step 2: $40 = 2x \\Rightarrow x = 20$.', 'Step 3: angle $= 3(20) + 10 = 70°$; neighbours $= 180° - 70° = 110°$.'],
    'Vertically opposite → set equal. Neighbours on a line → add to $180°$.',
    [('Vertically opposite angles are $2x$ and $x + 40$. Find $x$.', '$x = 40$ (each angle $80°$).')])
c.S(49, 'Conjecture: the number of regions when $n$ lines pass through the centre of a circle. How many regions do 6 lines give?', '$2n$ regions; 12.',
    ['Step 1: data 1 → 2, 2 → 4, 3 → 6.', 'Step 2: each line adds 2.', 'Step 3: $2 \\times 6 = 12$.'],
    'Look at the differences in a table — a constant difference $d$ means the rule is $dn + c$.',
    [('Sequence of regions 3, 5, 7, 9 for $n = 1, 2, 3, 4$. Conjecture?', '$2n + 1$.')])
c.TF(48, 'If a conjecture is true for 100 examples, it is proved.', False,
     ['Step 1: examples only verify particular cases.', 'Step 2: the 101st case could fail (like the circle-regions pattern that breaks at 6 points).', 'Step 3: only a general deductive argument proves it.'],
     'Examples can disprove (one counter-example) but cannot prove.',
     [('How many counter-examples are needed to disprove a conjecture?', 'One.')])
c.S(48, 'Make a conjecture about (a) the diagonals of a rectangle, (b) the base angles of an isosceles triangle.', '(a) They are equal and bisect each other. (b) They are equal.',
    ['Step 1: draw several rectangles; measure the diagonals — always equal, crossing at their midpoints.', 'Step 2: draw isosceles triangles; measure the angles opposite the equal sides — always equal.'],
    'Draw at least three different-looking cases before you state a conjecture.',
    [('Conjecture about the diagonals of a rhombus?', 'They bisect each other at right angles.')])

d = QSet('2.4 Practice — reasoning and proof', 's24')
d.S(52, 'Make a correct deduction: "All rectangles are parallelograms. $ABCD$ is a rectangle."', '$ABCD$ is a parallelogram.',
    ['Step 1: general statement: rectangle ⇒ parallelogram.', 'Step 2: particular case: $ABCD$ is a rectangle.', 'Step 3: so $ABCD$ is a parallelogram (deductive reasoning).'],
    'Pattern: If $p$ then $q$; $p$; therefore $q$.',
    [('"All human beings are mortal. Socrates is a human being." Conclusion?', 'Socrates is mortal.')])
d.S(52, 'Angles $A$ and $B$ are complementary and $\\angle A = x°$. What can you deduce about $\\angle B$?', '$\\angle B = 90° - x°$.',
    ['Step 1: complementary means $\\angle A + \\angle B = 90°$.', 'Step 2: $\\angle B = 90° - x°$.'],
    'Complementary → 90° (Corner), supplementary → 180° (Straight).',
    [('$\\angle P$ and $\\angle Q$ are supplementary, $\\angle P = 3x$. Find $\\angle Q$.', '$180° - 3x$.')])
d.M(52, 'The converse of "If a triangle is isosceles, then two of its sides are equal" is', ['If two sides of a triangle are equal, then it is isosceles', 'If a triangle is not isosceles, then no two sides are equal', 'A triangle is isosceles', 'If a figure is a triangle then it is isosceles'], 'A',
    ['Step 1: hypothesis $p$ = "a triangle is isosceles"; conclusion $q$ = "two sides are equal".', 'Step 2: converse = "if $q$ then $p$".'],
    'Converse = swap the "if" part and the "then" part.',
    [('Converse of "If the radius is 5, the area is $25\\pi$"?', 'If the area is $25\\pi$, then the radius is 5.')])
d.S(52, 'Write the hypothesis, conclusion and converse of "If opposite sides of a quadrilateral are parallel, then it is a parallelogram." Is the converse true?', 'Hypothesis: opposite sides parallel. Conclusion: it is a parallelogram. Converse: if a quadrilateral is a parallelogram, then its opposite sides are parallel — true.',
    ['Step 1: the "if" part is the hypothesis.', 'Step 2: the "then" part is the conclusion.', 'Step 3: swap them for the converse; it is true by the definition of a parallelogram.'],
    'Definitions are always "if and only if", so their converses are true.',
    [('Is the converse of "If a figure is a square, then it is a rectangle" true?', 'No — a 4 × 2 rectangle is not a square.')])
d.S(53, 'In triangle $ABC$, $\\angle A = 48°$ and $\\angle B = 67°$. Side $AC$ is extended beyond $C$. Find the exterior angle at $C$ in two ways.', '$115°$',
    ['Way 1 (exterior angle theorem): $48° + 67° = 115°$.', 'Way 2: $\\angle C = 180° - 48° - 67° = 65°$, then exterior $= 180° - 65° = 115°$.'],
    'The exterior angle theorem saves a step: just add the two far angles.',
    [('An exterior angle of a triangle is $130°$ and one remote interior angle is $55°$. Find the other.', '$75°$.')])
d.S(51, 'Prove: the sum of two even integers is even.', '$2m + 2n = 2(m + n)$, which is even.',
    ['Step 1: let the even integers be $2m$ and $2n$ ($m, n$ integers).', 'Step 2: add: $2m + 2n = 2(m + n)$.', 'Step 3: $m + n$ is an integer, so the sum is even. ∎'],
    'Write general even/odd numbers with letters: even $2k$, odd $2k + 1$.',
    [('Prove that the product of two odd integers is odd.', '$(2m + 1)(2n + 1) = 2(2mn + m + n) + 1$, which is odd.')])
d.F(50, 'Reasoning from several particular cases to a general rule is called ____ reasoning.', 'inductive', ['inductive', 'deductive', 'circular', 'indirect'],
    ['Step 1: particular → general = inductive.', 'Step 2: general → particular = deductive.'],
    'IN-ductive: cases come IN, a rule comes out.',
    [('Reasoning that uses axioms and theorems to reach a certain conclusion is called ____.', 'Deductive reasoning.')])
d.S(55, 'Use the polygon table to find (a) the number of triangles and (b) the angle sum of a decagon (10 sides).', '(a) 8 triangles (b) $1440°$',
    ['Step 1: triangles from one vertex $= n - 2 = 8$.', 'Step 2: each triangle has $180°$.', 'Step 3: $8 \\times 180° = 1440°$.'],
    'Angle sum $= (n - 2) \\times 180°$.',
    [('How many diagonals can be drawn from one vertex of a 12-gon?', '9.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Undefined terms', 'Basic words (point, line, plane) that are described but not defined.', 31),
    ('Collinear points', 'Points that lie on the same line.', 33),
    ('Axiom (postulate)', 'A statement accepted as true without proof.', 34),
    ('Theorem', 'A statement proved from axioms, definitions and earlier theorems.', 35),
    ('Axiomatic system', 'Undefined terms, defined terms, axioms and theorems organised so each part is built from the earlier ones.', 35),
    ('Construction', 'An accurate drawing made with only a compass and a straightedge.', 38),
    ('Perpendicular bisector', 'The line through the midpoint of a segment at right angles to it.', 39),
    ('Angle bisector', 'The ray that divides an angle into two equal angles.', 42),
    ('Inscribed polygon', 'A polygon whose vertices all lie on a circle.', 44),
    ('Conjecture', 'A statement believed true from observations but not yet proved.', 47),
    ('Counter-example', 'One example that shows a general statement is false.', 48),
    ('Inductive reasoning', 'Forming a general conclusion (conjecture) from particular cases.', 50),
    ('Deductive reasoning', 'Reaching a certain conclusion from accepted statements (definitions, axioms, theorems).', 49),
    ('Converse', 'The statement formed by interchanging the hypothesis and the conclusion of a conditional statement.', 52),
]
TIPS = [
    ('Undefined → defined (terms); axioms → theorems (statements). A proof may only use things from earlier on these ladders.', 35),
    ('Constructions: keep the compass width fixed within a step — equal radii are the whole reason the construction is exact.', 39),
    ('One counter-example kills a conjecture; no number of examples proves it.', 48),
]
IDEAS = [('axsys', 'Axiomatic system', 'l2_1', 'math10-u2-md-axsys'), ('constr', 'Four constructions', 'l2_2', 'math10-u2-md-constr-t'),
         ('parallel', 'Parallel-line angles', 'l2_3', 'math10-u2-md-parallel-t'), ('reason', 'Inductive vs deductive', 'l2_4', 'math10-u2-md-reason-t')]
