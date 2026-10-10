r"""Grade 12 Unit 3 — Analytic Geometry (pp. 126-157)."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY

UID = 'math12-u3'
set_unit(UID)
LB, LG, LR = '#dbe7f3', '#d6ece6', '#f6dcd5'


# ------------------------------------------------------------------ figures
def f_divide():
    f = Fig(330, 210)
    P1, P2 = (40, 175), (290, 30)
    t = 2 / 5
    P = (P1[0] + t * (P2[0] - P1[0]), P1[1] + t * (P2[1] - P1[1]))
    f.g('k1 k2 k3').line(*P1, *P2, INK, 2.2)
    f.dot(*P1, BLUE, 4.4).dot(*P2, BLUE, 4.4).dot(*P, RED, 4.6)
    f.text(P1[0] + 2, P1[1] + 22, 'P1(x1, y1)', 12, BLUE).text(P2[0] - 14, P2[1] - 12, 'P2(x2, y2)', 12, BLUE)
    f.text(P[0] - 34, P[1] - 8, 'P(x, y)', 12, RED).end()
    f.g('k1 k2 k3').text((P1[0] + P[0]) / 2 + 12, (P1[1] + P[1]) / 2 + 16, 'r1', 13, PURPLE).text((P[0] + P2[0]) / 2 + 12, (P[1] + P2[1]) / 2 + 16, 'r2', 13, PURPLE).end()
    f.g('k2 k3').line(P1[0], P1[1], P[0], P1[1], GREEN, 1.8, dash='5 3').line(P[0], P1[1], *P, GREEN, 1.8, dash='5 3')
    f.line(P[0], P[1], P2[0], P[1], ORANGE, 1.8, dash='5 3').line(P2[0], P[1], *P2, ORANGE, 1.8, dash='5 3').end()
    f.g('k3').text((P1[0] + P[0]) / 2, P1[1] + 18, 'x - x1', 12, GREEN).text((P[0] + P2[0]) / 2, P[1] + 18, 'x2 - x', 12, ORANGE).end()
    return f


def f_slope():
    p = Plot(-2, 4, -2, 8, unit=40, uy=19, every=1, yevery=2, gstep=1, xlab='x', ylab='y')
    p.g('k1 k2 k3').fullline(2, 1, c=BLUE, lab='y = 2x + 1', labx=1.6, labpos='nw')
    p.pt(1, 3, 'P(1, 3)', 'nw', RED).pt(3, 7, 'Q(3, 7)', 'nw', RED).end()
    p.g('k2 k3').seg((1, 3), (3, 3), GREEN, 2, dash=True).seg((3, 3), (3, 7), ORANGE, 2, dash=True)
    p.text(p.X(2), p.Y(3) + 16, 'run 2', 12, GREEN).text(p.X(3) + 8, p.Y(5), 'rise 4', 12, ORANGE, 'start').end()
    p.g('k3').angle(p.P(-0.5, 0), p.P(1, 0), p.P(0, 1), 22, PURPLE, 'a').end()
    return p


def f_parperp():
    p = Plot(-3, 7, -6, 8, unit=28, uy=14, every=1, yevery=2, gstep=1, xlab='x', ylab='y')
    p.fullline(2, 0, c=BLUE, lab='y = 2x', labx=3.4)
    p.fullline(2, -5, c=BLUE, dash=True, lab='y = 2x - 5', labx=1.4, labpos='se')
    p.fullline(-0.5, 5, c=RED, lab='y = -x/2 + 5', labx=-2.7, labpos='ne')
    return p


def f_intercept():
    p = Plot(-2, 6, -6, 3, unit=36, uy=24, every=1, yevery=1, gstep=1, xlab='x', ylab='y')
    p.fullline(1.25, -5, c=BLUE, lab='x/4 + y/(-5) = 1', labx=5.4, labpos='nw')
    p.pt(4, 0, '(4, 0)', 'nw', RED).pt(0, -5, '(0, -5)', 'e', RED)
    return p


def f_median():
    p = Plot(-4, 6, -4, 9, unit=28, uy=17, every=2, yevery=2, gstep=1, xlab='x', ylab='y')
    p.ppoly([(-3, 4), (3, -3), (5, 8)], BLUE, '#dbe7f3')
    p.seg((-3, 4), (4, 2.5), RED, 2.4)
    p.pt(-3, 4, 'A(-3, 4)', 'n', BLUE).pt(3, -3, 'B(3, -3)', 'e', BLUE).pt(5, 8, 'C(5, 8)', 'w', BLUE).pt(4, 2.5, 'M(4, 2.5)', 'e', RED)
    return p


def f_circle():
    p = Plot(-1, 7, -1, 6, unit=36, uy=36, every=1, yevery=1, gstep=1, xlab='x', ylab='y')
    h, k, r = 3, 2, 3
    import math
    x, y = h + r * math.cos(math.radians(40)), k + r * math.sin(math.radians(40))
    p.g('k1 k2 k3').circle(p.X(h), p.Y(k), r * 36, BLUE, 2.4)
    p.pt(h, k, 'C(h, k)', 'sw', INK).pt(x, y, 'P(x, y)', 'ne', RED).end()
    p.g('k2 k3').seg((h, k), (x, y), RED, 2.2).text(p.X((h + x) / 2) - 8, p.Y((k + y) / 2) - 6, 'r', 14, RED).end()
    p.g('k3').seg((h, k), (x, k), GREEN, 2, dash=True).seg((x, k), (x, y), ORANGE, 2, dash=True)
    p.text(p.X((h + x) / 2), p.Y(k) + 16, 'x - h', 12, GREEN).text(p.X(x) + 8, p.Y((k + y) / 2) + 16, 'y - k', 12, ORANGE, 'start').end()
    return p


def f_tower():
    f = Fig(300, 272)
    c, s = (150, 135), 1.0
    f.circle(*c, 100 * s, BLUE, 2.2, '#dbe7f3')
    f.dot(*c, INK, 4).text(c[0], c[1] + 18, 'tower', 12, INK)
    home = (c[0] + 33 * s, c[1] - 97 * s)
    f.line(*c, *home, RED, 2, dash='5 3').dot(*home, RED, 4.6).text(home[0] + 8, home[1] + 2, 'home (33, 97)', 12, RED, 'start')
    f.text(c[0] - 64, c[1] + 50, 'radius 100 km', 12, BLUE)
    f.text(150, 264, 'distance 102.5 km: outside', 12, RED)
    return f


DIAGRAMS = {
    'divide': (f_divide(), 'Dividing P1P2 in the ratio r1 : r2', 127),
    'slope': (f_slope(), 'Slope = rise / run = tan of the inclination', 132),
    'parperp': (f_parperp(), 'Parallel lines (same slope) and a perpendicular line', 134),
    'intercept': (f_intercept(), 'Double-intercept form: x/4 - y/5 = 1', 143),
    'median': (f_median(), 'Example 3.13: the median from A', 148),
    'circle': (f_circle(), 'Standard equation of a circle', 151),
    'tower': (f_tower(), 'Exercise 3.7 Q7: is home inside the reception circle?', 156),
}

# ------------------------------------------------------------------ 3.1
L1 = [
    T('=math12-u3-c01', '3.1 Distance, midpoint and division of a segment', 126,
      'Recall for $A(x_1, y_1)$ and $B(x_2, y_2)$: $$AB = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$ and the **midpoint** $M = \\left(\\frac{x_1 + x_2}{2}, \\frac{y_1 + y_2}{2}\\right)$.',
      'A point $P$ on segment $P_1P_2$ **divides it internally in the ratio** $r_1 : r_2$ when $P_1P : PP_2 = r_1 : r_2$.',
      '**Activity 3.1:** $A(3, 2)$, $B(13, 10)$: $AB = \\sqrt{100 + 64} = 2\\sqrt{41}$, midpoint $(8, 6)$, quarter points $(5.5, 4)$, $(8, 6)$, $(10.5, 8)$; the 1 : 4 point is $(5, 3.6)$.'),
    ST('divide', 'Why the section formula works', 127, 'divide',
       [('$P$ is $r_1$ parts from $P_1$ and $r_2$ parts from $P_2$.', 'k1'),
        ('Drop horizontal and vertical lines: the two right triangles are similar (AA), so the horizontal pieces are in the same ratio.', 'k2'),
        ('$\\frac{x - x_1}{x_2 - x} = \\frac{r_1}{r_2}$. Solve for $x$ (the same for $y$): $$x = \\frac{r_1x_2 + r_2x_1}{r_1 + r_2}, \\quad y = \\frac{r_1y_2 + r_2y_1}{r_1 + r_2}$$', 'k3')]),
    RM('sect-rm', 'Section formula — cross-multiply', 128,
       '$$P = \\left(\\frac{r_1x_2 + r_2x_1}{r_1 + r_2}, \\frac{r_1y_2 + r_2y_1}{r_1 + r_2}\\right)$$',
       '$r_1$ (the part next to $P_1$) multiplies the coordinates of $P_2$. With $r_1 = r_2$ it becomes the midpoint formula (Exercise 3.1 Q7).'),
    WK('ex31', 'Worked example: Example 3.1', 128, 'Find the point dividing $P_1(-1, 7)$ to $P_2(4, -3)$ in the ratio 2 : 3.',
       ['$r_1 = 2$, $r_2 = 3$.', '$x = \\frac{2(4) + 3(-1)}{5} = \\frac{5}{5} = 1$ (the book writes $2(-1) + 3(4)$ but still gets 1).', '$y = \\frac{2(-3) + 3(7)}{5} = \\frac{15}{5} = 3$.'], '$P(1, 3)$'),
    WK('ratio-wk', 'Worked example: finding the ratio (Exercise 3.1 Q4)', 129,
       'In what ratio does the y-axis divide the segment from $(5, -6)$ to $(-1, -4)$? Where does it cross?',
       ['On the y-axis $x = 0$. Let the ratio be $k : 1$.', '$\\frac{k(-1) + 1(5)}{k + 1} = 0 \\Rightarrow k = 5$: ratio 5 : 1.', '$y = \\frac{5(-4) + 1(-6)}{6} = -\\frac{26}{6}$.'],
       '5 : 1 at $\\left(0, -\\frac{13}{3}\\right)$'),
    'math12-u3-c02', 'math12-u3-c04', 'math12-u3-c05', 'math12-u3-c06', 'math12-u3-c07', 'math12-u3-tblE1', 'math12-u3-chkE1', 'math12-u3-chkE2', 'math12-u3-pc11', 'math12-u3-xw1',
]

# ------------------------------------------------------------------ 3.2
L2 = [
    T('=math12-u3-c03', '3.2.1 Inclination and slope', 132,
      'The **inclination** $\\alpha$ of a line is the angle from the positive x-axis to the line, measured anticlockwise: $0° \\le \\alpha < 180°$. Horizontal lines: $0°$; vertical lines: $90°$.',
      '**Slope** $m = \\tan\\alpha$, or from two points $$m = \\frac{y_2 - y_1}{x_2 - x_1} = \\frac{\\text{rise}}{\\text{run}}$$ (subtract in the same order top and bottom).',
      'A vertical line has **no slope** ($x_2 - x_1 = 0$). "1 in 30" means slope $\\frac{1}{30}$ — steeper than 1 in 100.'),
    ST('slope', 'Rise over run (Activity 3.2)', 132, 'slope',
       [('The line $y = 2x + 1$ through $P(1, 3)$ and $Q(3, 7)$.', 'k1'),
        ('Run $= 3 - 1 = 2$, rise $= 7 - 3 = 4$, slope $= \\frac{4}{2} = 2$ — the coefficient of $x$.', 'k2'),
        ('$\\tan\\alpha = 2$, so $\\alpha \\approx 63.4°$.', 'k3')]),
    TB('slope-tb', 'What the slope tells you', 133, ['Slope', 'Line'],
       [['$m > 0$', 'rises left to right; bigger $m$ = steeper'], ['$m < 0$', 'falls left to right; more negative = steeper'], ['$m = 0$', 'horizontal, $y = q$'], ['undefined', 'vertical, $x = p$']]),
    TB('incl-tb', 'Exercise 3.2: slope ↔ inclination', 132, ['Slope', 'Inclination'],
       [['$\\sqrt{3}$', '$60°$'], ['$\\frac{1}{\\sqrt{3}}$', '$30°$'], ['1', '$45°$'], ['0', '$0°$'], ['−1', '$135°$']]),
    DG('parperp', '3.2.2 Parallel and perpendicular lines', 136, 'parperp',
       '**Parallel:** same slope, $m_1 = m_2$ ($y = 2x$ and $y = 2x - 5$).',
       '**Perpendicular:** $m_1m_2 = -1$, i.e. $m_2 = -\\frac{1}{m_1}$ ($2 \\times (-\\frac{1}{2}) = -1$). A horizontal and a vertical line are also perpendicular.'),
    WK('ex36', 'Worked example: prove a square (Example 3.6)', 137, 'Show $P(0, -2)$, $Q(4, 2)$, $R(0, 6)$, $S(-4, 2)$ is a square.',
       ['Each side: $PQ^2 = 4^2 + 4^2 = 32$; likewise $QR^2 = RS^2 = SP^2 = 32$. All sides equal.', 'Slopes: $PQ$: $\\frac{4}{4} = 1$; $QR$: $\\frac{4}{-4} = -1$.', '$1 \\times (-1) = -1$, so $PQ \\perp QR$: a rhombus with a right angle.'], 'a square'),
    T('lineq-t', '3.2.3 Equations of a line', 140,
      '**Point–slope:** $y - y_1 = m(x - x_1)$. **Slope–intercept:** $y = mx + b$. **Two-point:** find $m$ first, then use point–slope.',
      '**Double-intercept:** $\\frac{x}{a} + \\frac{y}{b} = 1$ (crosses at $(a, 0)$ and $(0, b)$). **General form:** $ax + by + c = 0$ — covers every line, including vertical ones.',
      '**From general to slope form:** $3y + 5x - 11 = 0 \\Rightarrow y = -\\frac{5}{3}x + \\frac{11}{3}$ (slope $-\\frac{5}{3}$, y-intercept $\\frac{11}{3}$).'),
    TB('forms-tb', 'Which form to use', 142, ['You know', 'Use'],
       [['slope and y-intercept', '$y = mx + b$'], ['slope and a point', '$y - y_1 = m(x - x_1)$'], ['two points', 'slope first, then point–slope'], ['both intercepts', '$\\frac{x}{a} + \\frac{y}{b} = 1$'],
        ['horizontal through $(p, q)$', '$y = q$'], ['vertical through $(p, q)$', '$x = p$']]),
    DG('intercept', 'Double-intercept form (Review Q5)', 143, 'intercept',
       'x-intercept 4, y-intercept −5: $\\frac{x}{4} + \\frac{y}{-5} = 1$. Multiply by 20: $5x - 4y = 20$, i.e. $5x - 4y - 20 = 0$.',
       '(Example 3.12 writes "$b = -3$" but uses $b = -5$; its answer $-5x + 9y + 45 = 0$ is right.)'),
    WK('perpwk', 'Worked example: a perpendicular line (Review Q3)', 156, 'Find the line through $(1, -2)$ perpendicular to $x - 2y + 3 = 0$.',
       ['Rewrite: $y = \\frac{1}{2}x + \\frac{3}{2}$, slope $\\frac{1}{2}$.', 'Perpendicular slope $-2$.', '$y + 2 = -2(x - 1)$.'], '$y = -2x$'),
    DG('median', '3.2.4 Analytic proofs: a median (Example 3.13)', 148, 'median',
       'The median from $A(-3, 4)$ goes to the midpoint of $BC$: $M\\left(4, \\frac{5}{2}\\right)$.',
       'Slope $AM = \\frac{2.5 - 4}{4 + 3} = -\\frac{3}{14}$, so $y - 4 = -\\frac{3}{14}(x + 3)$: $3x + 14y - 47 = 0$. (The book numbers this example and the first circle example both 3.13.)'),
    T('concur-t', 'Concurrent lines in a triangle', 147,
      'Lines are **concurrent** when they all pass through one point.',
      '**Medians** (vertex to midpoint of the opposite side) meet at the **centroid** $G = \\left(\\frac{x_1 + x_2 + x_3}{3}, \\frac{y_1 + y_2 + y_3}{3}\\right)$, $\\frac{2}{3}$ of the way down each median. **Altitudes** meet at the orthocentre, **perpendicular bisectors** at the circumcentre (equal distance from the vertices), **angle bisectors** at the incentre (equal distance from the sides).',
      '**Activity 3.6 (altitudes):** with $A(0, 0)$, $B(b, 0)$, $C(c, d)$ the altitude from $C$ is $x = c$; the altitude from $B$ has slope $-\\frac{c}{d}$; they meet at $\\left(c, \\frac{c(b - c)}{d}\\right)$, which also lies on the altitude from $A$.'),
    'math12-u3-chk74', 'math12-u3-wrk1', 'math12-u3-chk75', 'math12-u3-wrk2', 'math12-u3-chk76', 'math12-u3-wrk3', 'math12-u3-chk77', 'math12-u3-wrk4', 'math12-u3-chk78', 'math12-u3-wrk5',
]

# ------------------------------------------------------------------ 3.3
L3 = [
    'math12-u3-c08',
    ST('circle', 'From the distance formula to the circle equation', 151, 'circle',
       [('A circle: all points $P(x, y)$ at the same distance $r$ from the centre $C(h, k)$.', 'k1'),
        ('Distance $CP = r$: $\\sqrt{(x - h)^2 + (y - k)^2} = r$.', 'k2'),
        ('Square both sides: $$(x - h)^2 + (y - k)^2 = r^2$$ (standard form). Centre at the origin: $x^2 + y^2 = r^2$.', 'k3')]),
    T('genc-t', 'General form and completing the square', 153,
      '**General form:** $x^2 + y^2 + Dx + Ey + F = 0$. Expand the standard form to get it: centre $(-2, 4)$, $r = \\sqrt{5}$: $x^2 + 4x + 4 + y^2 - 8y + 16 = 5$, so $x^2 + y^2 + 4x - 8y + 15 = 0$.',
      '**Back to standard form:** group $x$-terms and $y$-terms, add $\\left(\\frac{D}{2}\\right)^2$ and $\\left(\\frac{E}{2}\\right)^2$ to both sides, factor.',
      'Shortcut: centre $\\left(-\\frac{D}{2}, -\\frac{E}{2}\\right)$, $r^2 = \\frac{D^2 + E^2}{4} - F$.',
      'If $r^2 > 0$: a circle. If $r^2 = 0$: a single point. If $r^2 < 0$: no points at all (Exercise 3.7 Q8, Q9).'),
    WK('ex316', 'Worked example: Example 3.16', 154, 'Find the centre and radius of $x^2 + y^2 - 2x + 8y - 8 = 0$.',
       ['Group: $(x^2 - 2x) + (y^2 + 8y) = 8$.', 'Complete the squares: add 1 and 16: $(x^2 - 2x + 1) + (y^2 + 8y + 16) = 25$.', '$(x - 1)^2 + (y + 4)^2 = 25$.'], 'centre $(1, -4)$, radius 5'),
    WK('diam', 'Worked example: circle on a diameter (Exercise 3.7 Q5)', 156, 'The ends of a diameter are $(1, 7)$ and $(-5, -1)$. Find the general equation.',
       ['Centre = midpoint $(-2, 3)$.', '$r^2 = (1 + 2)^2 + (7 - 3)^2 = 25$.', '$(x + 2)^2 + (y - 3)^2 = 25 \\Rightarrow x^2 + 4x + 4 + y^2 - 6y + 9 = 25$.'], '$x^2 + y^2 + 4x - 6y - 12 = 0$'),
    DG('tower', 'Inside or outside a circle?', 156, 'tower',
       'Compare the distance from the centre with $r$. Home 97 km north and 33 km east: $\\sqrt{97^2 + 33^2} = \\sqrt{10498} \\approx 102.5$ km $> 100$: **no** signal. Review Q9 (45 km south, 87 km west): $\\sqrt{9594} \\approx 97.9$ km $< 100$: **yes**.'),
    'math12-u3-chk79', 'math12-u3-wrk6', 'math12-u3-pc31', 'math12-u3-pc32',
    RM('summary-t', 'Unit summary', 157,
       'Section formula $\\left(\\frac{r_1x_2 + r_2x_1}{r_1 + r_2}, \\frac{r_1y_2 + r_2y_1}{r_1 + r_2}\\right)$; midpoint when $r_1 = r_2$.',
       'Slope $m = \\frac{y_2 - y_1}{x_2 - x_1} = \\tan\\alpha$; parallel $m_1 = m_2$; perpendicular $m_1m_2 = -1$.',
       'Lines: $y = mx + b$, $y - y_1 = m(x - x_1)$, $\\frac{x}{a} + \\frac{y}{b} = 1$, $ax + by + c = 0$.',
       'Circle: $(x - h)^2 + (y - k)^2 = r^2$; general form $x^2 + y^2 + Dx + Ey + F = 0$.'),
]

LESSONS = {'math12-u3-l3-1': L1, 'math12-u3-l3-2': L2, 'math12-u3-l3-3': L3}

# ------------------------------------------------------------------ practice
a = QSet('3.1 Practice — dividing segments', 's31')
a.S(129, 'Exercise 3.1 Q1 and Q3: find the points that trisect (a) $(5, -3)$ to $(14, 18)$ (b) $A(2, -2)$ to $B(-7, 4)$.', '(a) $(8, 4)$, $(11, 11)$ (b) $(-1, 0)$, $(-4, 2)$',
    ['Step 1: trisection points divide in 1 : 2 and 2 : 1.', 'Step 2: (a) step $= \\frac{1}{3}(9, 21) = (3, 7)$.', 'Step 3: (b) step $= \\frac{1}{3}(-9, 6) = (-3, 2)$.'], 'Add equal steps from the first endpoint.', [('Quarter points of $(0, 0)$ to $(8, 4)$?', '$(2, 1)$, $(4, 2)$, $(6, 3)$.')])
a.S(129, 'Exercise 3.1 Q2: in what ratio does $(-4, 6)$ divide $A(-6, 10)$ to $B(3, -8)$?', '2 : 7',
    ['Step 1: x-distances: from $A$ $2$, to $B$ $7$.', 'Step 2: check y: $10 + \\frac{2}{9}(-18) = 6$ ✓.'], 'Use one coordinate, check with the other.', [('Ratio for $(0, 4)$ on $(-3, 1)$ to $(6, 10)$?', '1 : 2.')])
a.S(129, 'Exercise 3.1 Q8 and Q10: divide internally (a) $(-9, -2)$ to $(6, 2)$ in 3 : 4 (b) $(0, 0)$ to $(12, 10)$ in 4 : 7.', '(a) $\\left(-\\frac{18}{7}, -\\frac{2}{7}\\right)$ (b) $\\left(\\frac{48}{11}, \\frac{40}{11}\\right)$',
    ['Step 1: (a) $x = \\frac{3(6) + 4(-9)}{7}$, $y = \\frac{3(2) + 4(-2)}{7}$.', 'Step 2: (b) $\\frac{4}{11}$ of the way: $\\frac{4}{11}(12, 10)$.'], 'From the origin, multiply by $\\frac{r_1}{r_1 + r_2}$.', [('$(0, 0)$ to $(10, 5)$ in 2 : 3?', '$(4, 2)$.')])
a.S(130, 'Exercise 3.1 Q5, Q6, Q9: (5) $A(6, 1)$, $B(8, 2)$, $C(9, 4)$, $D(p, 3)$ is a parallelogram: $p$? (6) rhombus $(3, 0)$, $(4, 5)$, $(-1, 4)$, $(-2, -1)$: area? (9) $P(6, -2)$ divides $AB$ ($A$ on the x-axis, $B$ on the y-axis) in 1 : 2: $A$, $B$?', '$p = 7$; 24; $A(9, 0)$, $B(0, -6)$',
    ['Step 1: diagonals bisect each other: $6 + 9 = 8 + p$.', 'Step 2: diagonals $\\sqrt{32}$ and $\\sqrt{72}$; area $\\frac{1}{2}\\sqrt{32 \\cdot 72} = 24$.', 'Step 3: $P = \\frac{2A + B}{3}$: $6 = \\frac{2a}{3}$, $-2 = \\frac{b}{3}$.'], 'Rhombus area = half the product of the diagonals.', [('Parallelogram $(0, 0)$, $(4, 0)$, $(5, 3)$, $(x, 3)$?', '$x = 1$.')])
a.M(128, 'The point dividing $(4, -3)$ to $(8, 5)$ in 3 : 1 is', ['$(7, 3)$', '$(5, -1)$', '$(6, 1)$', '$(7, 1)$'], 'A',
    ['Step 1: $x = \\frac{3(8) + 1(4)}{4} = 7$, $y = \\frac{3(5) + 1(-3)}{4} = 3$.'], '3 : 1 means three-quarters of the way.', [('In 1 : 3?', '$(5, -1)$.')])

b = QSet('3.2 Practice — slopes and lines', 's32')
b.S(133, 'Exercise 3.3 Q1: slopes through (a) $(2, 3)$, $(9, 12)$ (b) $(-7, 10)$, $(8, -2)$ (c) $(a, b)$, $(b, a)$ (d) $(3, -2)$, $(-1, 4)$ (e) $(a, b)$, $(-a, -b)$ (f) $(0, 4)$, $(-2, 0)$.', '$\\frac{9}{7}$, $-\\frac{4}{5}$, $-1$, $-\\frac{3}{2}$, $\\frac{b}{a}$, 2',
    ['Step 1: $m = \\frac{y_2 - y_1}{x_2 - x_1}$.', 'Step 2: (c) $\\frac{a - b}{b - a} = -1$ ($a \\ne b$).'], 'Same order top and bottom.', [('$(1, 1)$ and $(4, -5)$?', '$-2$.')])
b.S(133, 'Exercise 3.3 Q2: collinear? (a) $(8, 5)$, $(3, 2)$, $(-3, -1)$ (b) $(-3, 3)$, $(2, 1)$, $(12, -3)$ (c) $(-4, 6)$, $(-4, -1)$, $(-4, 20)$.', '(a) no (b) yes (c) yes',
    ['Step 1: (a) slopes $\\frac{3}{5}$ and $\\frac{1}{2}$ differ.', 'Step 2: (b) both $-\\frac{2}{5}$.', 'Step 3: (c) all on $x = -4$.'], 'Equal slopes through a common point ⇒ collinear.', [('Exercise 3.4 Q9: $(x, -1)$, $(2, 1)$, $(4, 5)$ collinear?', '$x = 1$.')])
b.S(138, 'Exercise 3.4 Q1, Q3, Q4: (1) line through $(a, 5)$ and $(-2, 3)$ and line through $(6, a)$ and $(2, 0)$: $a$ for parallel; for perpendicular. (3) $p$? (4) $q$?', '$a = 2$ or $-4$; $a = -\\frac{4}{3}$; $p = 4$; $q = 6$',
    ['Step 1: slopes $\\frac{2}{a + 2}$ and $\\frac{a}{4}$; parallel: $a^2 + 2a - 8 = 0$.', 'Step 2: perpendicular: $\\frac{2a}{4(a + 2)} = -1 \\Rightarrow 6a = -8$.', 'Step 3: (3) $\\frac{p + 2}{2} = 3$; (4) $\\frac{1 - 4}{q - 2} = -\\frac{3}{4}$.'], 'Write both slopes, then use $m_1 = m_2$ or $m_1m_2 = -1$.', [('Perpendicular to slope 5?', '$-\\frac{1}{5}$.')])
b.S(139, 'Exercise 3.4 Q5: type of triangle: (a) $(3, 0)$, $(-4, 0)$, $(0, 5)$ (b) $(-1, 0)$, $(1, 0)$, $(0, 1)$.', '(a) scalene, acute (b) right isosceles',
    ['Step 1: (a) sides $7$, $\\sqrt{34}$, $\\sqrt{41}$; $34 + 41 > 49$.', 'Step 2: (b) sides $\\sqrt{2}$, $\\sqrt{2}$, 2 and slopes $1 \\cdot (-1) = -1$.'], 'Compare side lengths and slopes.', [('$(0, 0)$, $(4, 0)$, $(0, 3)$?', 'right-angled, scalene.')])
b.S(144, 'Exercise 3.5 Q1: equation, slope and intercepts for (a) $(2, 4)$, $(-1, -5)$ (b) $(3, -3)$, $(-3, 1)$ (d) $(1, 5)$, $(-10, 5)$ (e) $(-1, -1)$, $(4, 4)$.', '(a) $y = 3x - 2$ (b) $y = -\\frac{2}{3}x - 1$ (d) $y = 5$ (e) $y = x$',
    ['Step 1: (a) $m = \\frac{9}{3} = 3$, $4 = 6 + b$.', 'Step 2: (b) $m = -\\frac{4}{6}$, $-3 = -2 + b$.', 'Step 3: (a) intercepts $(\\frac{2}{3}, 0)$, $(0, -2)$.'], 'Find $m$, then $b$ from one point.', [('$(0, 1)$ and $(2, 7)$?', '$y = 3x + 1$.')])
b.S(145, 'Exercise 3.5 Q2–Q3: (2) slope 3 through $(0, -1)$; slope $-5$ through $(0, \\frac{1}{2})$. (3) slope $-5$ through $(5, -5)$; $\\frac{1}{2}$ through $(4, -3)$; 3 through $(-7, 2)$; $-6$ through $(4, 2)$.', '$y = 3x - 1$; $y = -5x + \\frac{1}{2}$; $y = -5x + 20$; $y = \\frac{1}{2}x - 5$; $y = 3x + 23$; $y = -6x + 26$',
    ['Step 1: (2) $b$ is given.', 'Step 2: (3) $y - y_1 = m(x - x_1)$, e.g. $y + 5 = -5(x - 5)$.'], 'Expand and collect.', [('Slope 2 through $(1, 1)$?', '$y = 2x - 1$.')])
b.S(145, 'Exercise 3.5 Q4: slope and y-intercept of (a) $3y + 2x - 5 = 0$ (b) $-4x + 5y + 12 = 0$ (c) $4x - 6y = 12$ (d) $5y - 6x = 30$.', '(a) $-\\frac{2}{3}$, $\\frac{5}{3}$ (b) $\\frac{4}{5}$, $-\\frac{12}{5}$ (c) $\\frac{2}{3}$, $-2$ (d) $\\frac{6}{5}$, 6',
    ['Step 1: make $y$ the subject.', 'Step 2: (c) $-6y = -4x + 12 \\Rightarrow y = \\frac{2}{3}x - 2$.'], 'For $ax + by + c = 0$: $m = -\\frac{a}{b}$.', [('$2x + y = 7$?', 'slope $-2$, intercept 7.')])
b.S(145, 'Exercise 3.5 Q5: (b) through $(4, 3)$, slope $-4$ (c) crosses the x-axis 3 units left of $O$, slope $-2$ (d) median from $R(4, 5)$ in $P(2, 1)$, $Q(-2, 3)$, $R$ (e) through $(-3, 5)$ perpendicular to the line through $(2, 5)$ and $(-3, 6)$.', '$y = -4x + 19$; $y = -2x - 6$; $y = \\frac{3}{4}x + 2$; $y = 5x + 20$',
    ['Step 1: (c) point $(-3, 0)$.', 'Step 2: (d) midpoint of $PQ$ is $(0, 2)$, slope $\\frac{3}{4}$.', 'Step 3: (e) slope $-\\frac{1}{5}$ → perpendicular 5.'], 'Median = vertex to midpoint.', [('(f) Are $(-2, -2)$, $(8, 2)$, $(3, 0)$ collinear?', 'yes, both slopes $\\frac{2}{5}$.')])
b.S(149, 'Exercise 3.6 Q4–Q5: (4) centroid of $A(2, 2)$, $B(0, 6)$, $C(8, 10)$ (5) perpendicular bisector of $P(-2, 3)$, $Q(8, -1)$.', '$\\left(\\frac{10}{3}, 6\\right)$; $5x - 2y - 13 = 0$',
    ['Step 1: average the vertices.', 'Step 2: midpoint $(3, 1)$, slope $PQ = -\\frac{2}{5}$, perpendicular $\\frac{5}{2}$: $y - 1 = \\frac{5}{2}(x - 3)$.'], 'Perpendicular bisector = midpoint + negative reciprocal slope.', [('Centroid of $(0, 0)$, $(6, 0)$, $(0, 9)$?', '$(2, 3)$.')])
b.S(156, 'Review Q1, Q2, Q4: (1) through $(3, 4)$, slope 2 (2) through $(-2, 3)$, $(1, 5)$ (4) $k$ for $2x - ky + 5 = 0$ parallel / perpendicular to $8x - 14y + 3 = 0$.', '$y = 2x - 2$; $2x - 3y + 13 = 0$; $k = \\frac{7}{2}$; $k = -\\frac{8}{7}$',
    ['Step 1: (2) $m = \\frac{2}{3}$.', 'Step 2: (4) slopes $\\frac{2}{k}$ and $\\frac{4}{7}$.', 'Step 3: $\\frac{2}{k} \\cdot \\frac{4}{7} = -1 \\Rightarrow k = -\\frac{8}{7}$.'], 'Write each line as $y = mx + b$.', [('$y = kx$ perpendicular to $y = 3x$?', '$k = -\\frac{1}{3}$.')])
b.M(132, 'A line with inclination $135°$ has slope', ['$-1$', '1', '$\\sqrt{3}$', 'undefined'], 'A',
    ['Step 1: $\\tan 135° = -1$.'], 'Obtuse inclination ⇒ negative slope.', [('Inclination $90°$?', 'slope undefined.')])
b.TF(136, 'The lines $y = \\frac{2}{3}x + 1$ and $y = -\\frac{3}{2}x + 5$ are perpendicular.', True, ['Step 1: $\\frac{2}{3} \\cdot (-\\frac{3}{2}) = -1$.'], 'Negative reciprocals.', [('$y = 2x$ and $y = \\frac{1}{2}x$?', 'not perpendicular (product 1).')])

c = QSet('3.3 Practice — circles', 's33')
c.S(155, 'Exercise 3.7 Q1–Q3: standard equations: (a) $r = 4$, centre $(-3, -4)$ (c) $r = \\sqrt{5}$, centre $(1, -1)$ (Q2) the unit circle (Q3) centre $(7, -8)$ through $(10, -4)$.', '$(x + 3)^2 + (y + 4)^2 = 16$; $(x - 1)^2 + (y + 1)^2 = 5$; $x^2 + y^2 = 1$; $(x - 7)^2 + (y + 8)^2 = 25$',
    ['Step 1: substitute $h$, $k$, $r$.', 'Step 2: Q3: $r^2 = 3^2 + 4^2$.'], 'Signs flip inside the brackets.', [('$r = 2$, centre $(2, 1)$?', '$(x - 2)^2 + (y - 1)^2 = 4$.')])
c.S(155, 'Exercise 3.7 Q4: centre and radius of (a) $(x - 1)^2 + (y - 3)^2 = 25$ (b) $(x + 3)^2 + (y - 7)^2 = 81$ (c) $(x + 1)^2 + (y + 3)^2 = 11$ (d) $x^2 + y^2 = 12$ (e) $(x - \\frac{1}{2})^2 + (y + \\frac{1}{3})^2 = \\frac{9}{25}$.', '(1, 3), 5; (−3, 7), 9; (−1, −3), $\\sqrt{11}$; (0, 0), $2\\sqrt{3}$; $(\\frac{1}{2}, -\\frac{1}{3})$, $\\frac{3}{5}$',
    ['Step 1: read $h$, $k$ with opposite signs.', 'Step 2: $r = \\sqrt{\\text{right side}}$.'], 'The right side is $r^2$, not $r$.', [('$(x + 5)^2 + y^2 = 49$?', '$(-5, 0)$, 7.')])
c.S(155, 'Exercise 3.7 Q5: general form of (a) $(x + 2)^2 + (y - 3)^2 = 5$ (b) $(x - 3)^2 + (y + 3)^2 = 20$ (c) $r = 3$, centre $(4, -10)$ (d) $r = 9$, centre $(5, 7)$ (e) $r = \\sqrt{2}$, centre $O$.', '$x^2 + y^2 + 4x - 6y + 8 = 0$; $x^2 + y^2 - 6x + 6y - 2 = 0$; $x^2 + y^2 - 8x + 20y + 107 = 0$; $x^2 + y^2 - 10x - 14y - 7 = 0$; $x^2 + y^2 - 2 = 0$',
    ['Step 1: expand both squares.', 'Step 2: move $r^2$ to the left: (c) $16 + 100 - 9 = 107$.'], '$F = h^2 + k^2 - r^2$.', [('Centre $(1, 1)$, $r = 1$?', '$x^2 + y^2 - 2x - 2y + 1 = 0$.')])
c.S(156, 'Exercise 3.7 Q6: complete the squares: (a) $x^2 + y^2 + 6x + 8y - 75 = 0$ (b) $x^2 + y^2 + 16x - 14y + 88 = 0$ (c) $x^2 + y^2 - 4x - 16y + 32 = 0$ (d) $x^2 + y^2 - 10x + 6y + 22 = 0$ (e) $x^2 + y^2 - x + y + \\frac{1}{4} = 0$.', '(−3, −4), 10; (−8, 7), 5; (2, 8), 6; (5, −3), $2\\sqrt{3}$; $(\\frac{1}{2}, -\\frac{1}{2})$, $\\frac{1}{2}$',
    ['Step 1: (a) $(x + 3)^2 + (y + 4)^2 = 75 + 9 + 16 = 100$.', 'Step 2: (d) $(x - 5)^2 + (y + 3)^2 = -22 + 25 + 9 = 12$.'], 'Centre $(-\\frac{D}{2}, -\\frac{E}{2})$.', [('$x^2 + y^2 - 6x = 0$?', '(3, 0), 3.')])
c.S(156, 'Exercise 3.7 Q8–Q9: what do $x^2 + y^2 - 2x + 6y + 10 = 0$ and $x^2 + y^2 - 4x + 10y + 49 = 0$ represent?', 'the single point $(1, -3)$; no points (empty set)',
    ['Step 1: $(x - 1)^2 + (y + 3)^2 = 0$.', 'Step 2: $(x - 2)^2 + (y + 5)^2 = -20 < 0$.'], 'Check the sign of $r^2$.', [('$x^2 + y^2 + 1 = 0$?', 'no points.')])
c.S(157, 'Review Q7: standard and general forms: (a) $r = 8$, centre $(7, -3)$ (b) $r = \\sqrt{7}$, centre $(-1, 2)$ (c) centre $(4, 9)$ through $(2, 5)$ (d) diameter from $(-2, 6)$ to $(4, 2)$.', '$x^2 + y^2 - 14x + 6y - 6 = 0$; $x^2 + y^2 + 2x - 4y - 2 = 0$; $(x - 4)^2 + (y - 9)^2 = 20$, $x^2 + y^2 - 8x - 18y + 77 = 0$; $(x - 1)^2 + (y - 4)^2 = 13$, $x^2 + y^2 - 2x - 8y + 4 = 0$',
    ['Step 1: (c) $r^2 = 2^2 + 4^2 = 20$.', 'Step 2: (d) centre $(1, 4)$, $r^2 = 3^2 + 2^2 = 13$.'], 'Diameter ⇒ centre is the midpoint.', [('Centre $(0, 0)$ through $(3, 4)$?', '$x^2 + y^2 = 25$.')])
c.S(157, 'Review Q8: centre and radius: (a) $(x + 3)^2 + (y + 2)^2 = 36$ (b) $x^2 + y^2 - 4x + 2y - 45 = 0$ (c) $x^2 + y^2 - 10x + 4y = 0$ (d) $x^2 + y^2 - 10x + 21 = 0$.', '(−3, −2), 6; (2, −1), $5\\sqrt{2}$; (5, −2), $\\sqrt{29}$; (5, 0), 2',
    ['Step 1: (b) $r^2 = 4 + 1 + 45 = 50$.', 'Step 2: (c) $r^2 = 25 + 4 = 29$.', 'Step 3: (d) $r^2 = 25 - 21 = 4$.'], '$r^2 = (\\frac{D}{2})^2 + (\\frac{E}{2})^2 - F$.', [('$x^2 + y^2 + 2y - 3 = 0$?', '(0, −1), 2.')])
c.M(156, 'Is $(4, 5)$ inside, on or outside $(x - 1)^2 + (y - 1)^2 = 25$?', ['on', 'inside', 'outside', 'cannot tell'], 'A',
    ['Step 1: $3^2 + 4^2 = 25 = r^2$.'], 'Compare with $r^2$.', [('$(2, 2)$?', 'inside.')])
c.TF(151, 'The circle $(x + 2)^2 + (y - 5)^2 = 9$ has centre $(2, -5)$.', False, ['Step 1: $(x - h)$ with $h = -2$, $(y - k)$ with $k = 5$: centre $(-2, 5)$.'], 'Flip the signs you see.', [('Radius?', '3.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Section formula', 'Coordinates of the point dividing a segment in a ratio $r_1 : r_2$.', 128),
    ('Inclination', 'The anticlockwise angle from the positive x-axis to a line.', 132),
    ('Concurrent', 'Lines that all pass through one point.', 147),
    ('Centroid', 'The point where the medians of a triangle meet.', 148),
    ('General form of a circle', '$x^2 + y^2 + Dx + Ey + F = 0$.', 153),
]
TIPS = [('$r_1$ multiplies the far endpoint.', 128), ('Perpendicular: negative reciprocal slope.', 136), ('Complete the square to find centre and radius.', 154)]
IDEAS = [('sect', 'Section formula', 'l3_1', 'math12-u3-md-sect-rm'), ('slope', 'Slope and parallel/perpendicular', 'l3_2', 'math12-u3-md-parperp'),
         ('lines', 'Forms of a line', 'l3_2', 'math12-u3-md-forms-tb'), ('circ', 'Circle equations', 'l3_3', 'math12-u3-md-circle')]
