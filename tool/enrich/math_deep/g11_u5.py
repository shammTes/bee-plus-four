r"""Grade 11 Unit 5 — Similarity and the Geometry of Shape (pp. 167-200)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side

UID = 'math11-u5'
set_unit(UID)
LB, LG, LR = '#dbe7f3', '#d6ece6', '#f6dcd5'


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


# ------------------------------------------------------------------ figures
def f_bpt():
    f = Fig(330, 236)
    A, B, C = (165, 22), (40, 200), (295, 200)
    D, E = lerp(A, B, 0.4), lerp(A, C, 0.4)
    f.g('k2 k3').poly([A, D, E], None, 0, LB).end()
    f.poly([A, B, C], INK, 2.2)
    f.g('k1 k2 k3').line(D[0], D[1], E[0], E[1], BLUE, 2.4)
    f.par(D, E, 1, BLUE).par(B, C, 1, INK).end()
    for p, s, dx, dy in ((A, 'A', 0, -8), (B, 'B', -12, 8), (C, 'C', 12, 8), (D, 'D', -14, 0), (E, 'E', 14, 0)):
        f.label(p[0] + dx, p[1] + dy, s, size=13)
    f.g('k3').text(165, 226, 'AD / AB = AE / AC = DE / BC', 12.5, RED).end()
    return f


def f_altitude():
    f = Fig(340, 222)
    s = 12
    A, B = (20, 190), (320, 190)
    D = (20 + 9 * s, 190)
    C = (D[0], 190 - 12 * s)
    f.g('k2 k3').poly([A, D, C], None, 0, LB).end()
    f.g('k3').poly([D, B, C], None, 0, LG).end()
    f.poly([A, B, C], INK, 2.2)
    f.g('k1 k2 k3').line(C[0], C[1], D[0], D[1], RED, 2, dash='5 4')
    f.right(C, A, B, 10).right(D, C, B, 9, RED).end()
    for p, t, dx, dy in ((A, 'A', -10, 8), (B, 'B', 10, 8), (C, 'C', 0, -12), (D, 'D', 0, 14)):
        f.label(p[0] + dx, p[1] + dy, t, size=13)
    f.seglabel(A, D, '9', 12, INK, side=-1).seglabel(D, B, '16', 12, INK, side=-1)
    f.text(D[0] + 6, (C[1] + D[1]) / 2 + 4, '12', 12, RED, 'start')
    f.seglabel(A, C, '15', 13, BLUE, side=-1).seglabel(C, B, '20', 13, GREEN, side=-1)
    return f


def f_shadow():
    f = Fig(340, 250)
    g = 232
    f.line(10, g, 330, g, INK, 2)
    f.g('k1 k2 k3').line(40, g, 40, g - 30, BLUE, 4).line(40, g - 30, 60, g, ORANGE, 1.6, dash='5 4')
    f.line(40, g, 60, g, GREY, 5).text(36, g - 36, '6 m', 12, BLUE, 'end').text(50, g + 15, '4 m', 12, GREY).end()
    f.g('k2 k3').line(170, g, 170, g - 210, GREEN, 5).line(170, g - 210, 310, g, ORANGE, 1.6, dash='5 4')
    f.line(170, g, 310, g, GREY, 5).text(240, g + 15, '28 m', 12, GREY).text(164, g - 110, 'h', 14, GREEN, 'end')
    f.angle((310, g), (170, g - 210), (170, g), 22, ORANGE).angle((60, g), (40, g - 30), (40, g), 14, ORANGE).end()
    f.g('k3').text(250, 60, 'h / 28 = 6 / 4', 13, RED).text(250, 80, 'h = 42 m', 13, RED).end()
    return f


def f_elev():
    f = Fig(340, 176)
    g, s = 150, 3.5
    T = (40 + 30 * 1.7320508 * s, g - 30 * s)
    M1, M2 = (40, g), (T[0] + 10 * 1.7320508 * s, g)
    F = (T[0], g)
    f.line(15, g, 330, g, INK, 2)
    f.line(F[0], F[1], T[0], T[1], GREEN, 5)
    f.line(M1[0], M1[1], T[0], T[1], ORANGE, 1.8, dash='5 4').line(M2[0], M2[1], T[0], T[1], ORANGE, 1.8, dash='5 4')
    f.angle(M1, T, F, 34, RED, '30°', 50).angle(M2, T, F, 24, RED, '60°', 38)
    f.right(F, T, M1, 9)
    f.text(T[0] - 8, (T[1] + g) / 2, '30 m', 12, GREEN, 'end')
    f.text((M1[0] + F[0]) / 2, g + 17, 'x = 30√3', 12, INK).text((F[0] + M2[0]) / 2 + 6, g + 17, 'y = 10√3', 12, INK)
    f.dot(M1[0], M1[1], INK, 4).dot(M2[0], M2[1], INK, 4)
    return f


def tri_grid(k, side):
    w = side * k
    h = w * 0.82
    f = Fig(w + 16, h + 16)
    P0, P1, P2 = (8, h + 8), (w + 8, h + 8), (8 + w / 2, 8)
    f.poly([P0, P1, P2], INK, 2, FILL[BLUE])
    for i in range(1, k):
        t = i / k
        a, b = lerp(P0, P2, t), lerp(P1, P2, t)
        f.line(a[0], a[1], b[0], b[1], BLUE, 1.2)
        a, b = lerp(P0, P1, t), lerp(P1, P2, 1 - t)
        f.line(a[0], a[1], b[0], b[1], BLUE, 1.2)
        a, b = lerp(P0, P1, t), lerp(P0, P2, t)
        f.line(a[0], a[1], b[0], b[1], BLUE, 1.2)
    return f


def f_areagrid():
    return side_by_side([tri_grid(1, 48), tri_grid(2, 48), tri_grid(3, 48)], 14, ['k = 1', 'k = 2: 4 copies', 'k = 3: 9 copies'])


def f_bowtie():
    f = Fig(320, 182)
    A, C, E = (40, 30), (140, 30), (170, 100)
    B = (E[0] + 0.8 * (E[0] - A[0]), E[1] + 0.8 * (E[1] - A[1]))
    D = (E[0] + 0.8 * (E[0] - C[0]), E[1] + 0.8 * (E[1] - C[1]))
    f.poly([A, C, E], INK, 2, LB).poly([B, D, E], INK, 2, LG)
    f.par(A, C, 1, INK).par(D, B, 1, INK)
    f.angle(E, A, C, 16, RED).angle(E, B, D, 16, RED)
    f.angle(A, C, E, 20, PURPLE).angle(B, D, E, 20, PURPLE)
    for p, t, dx, dy in ((A, 'A', -10, -2), (C, 'C', 10, -4), (E, 'E', 14, -4), (B, 'B', 12, 6), (D, 'D', -12, 6)):
        f.label(p[0] + dx, p[1] + dy, t, size=13)
    return f


DIAGRAMS = {
    'bpt': (f_bpt(), 'Theorem 5.1: the Basic Proportionality Theorem', 177),
    'altitude': (f_altitude(), 'The altitude to the hypotenuse (Review Q4)', 189),
    'shadow': (f_shadow(), 'Review Q10: heights from shadows', 200),
    'elev': (f_elev(), 'Example 5.10: two angles of elevation', 194),
    'areagrid': (f_areagrid(), 'Scale factor k multiplies area by k²', 195),
    'bowtie': (f_bowtie(), 'Example 5.6: AC parallel to BD gives similar triangles', 183),
}

# ------------------------------------------------------------------ 5.1
L1 = [
    T('prop-t', 'Proportional sequences and the means', 169,
      'Sequences $a, b, c, \\dots$ and $p, q, r, \\dots$ are **proportional** if $\\frac{a}{p} = \\frac{b}{q} = \\frac{c}{r} = \\dots$ (one constant ratio $k$).',
      'Useful facts: if $\\frac{a}{b} = \\frac{p}{q}$ then $aq = bp$ (cross-multiply), $\\frac{a}{p} = \\frac{b}{q}$ (swap the means) and $\\frac{a + b}{b} = \\frac{p + q}{q}$ (add 1 to both sides).',
      '**Geometric mean** of $a, b > 0$: $\\sqrt{ab}$. **Arithmetic mean**: $\\frac{a + b}{2}$. For 4 and 9: GM $= 6$, AM $= 6.5$.',
      'Always $\\sqrt{ab} \\le \\frac{a + b}{2}$, because $\\frac{a + b}{2} - \\sqrt{ab} = \\frac{(\\sqrt{a} - \\sqrt{b})^2}{2} \\ge 0$ (equal only when $a = b$).'),
    TB('cong-sim', 'Congruent vs similar polygons', 170, ['', 'Congruent (≅)', 'Similar (~)'],
       [['angles', 'equal', 'equal'], ['sides', 'equal', 'proportional (ratio $k$)'], ['size', 'same', 'may differ'], ['example', 'two 3 cm squares', 'any two squares']]),
    WK('ex-51a', 'Worked example: why "same angles" is not enough for polygons (Example 5.1)', 170,
       'A square of side 2 cm and a rhombus of side 2 cm with a 60° angle: similar?',
       ['Sides: all ratios are 1, so the sides are proportional.', 'Angles: 90° vs 60° — not equal.', 'Both conditions are needed for polygons with more than 3 sides.'],
       'not similar'),
    RM('rm-51', 'Always similar / not always similar', 172,
       '**Always similar:** circles, squares, equilateral triangles, regular polygons with the **same number of sides**.',
       '**Not always:** rectangles (2 × 1 vs 3 × 1), rhombuses, isosceles triangles, right triangles. (The book\'s "all regular polygons are similar" is false unless they have the same number of sides: a square is not similar to a regular hexagon.)'),
    'math11-u5-c09', 'math11-u5-wrk-extra1', 'math11-u5-tblE1',
]

# ------------------------------------------------------------------ 5.2
L2 = [
    T('=math11-u5-c03', '5.2.1 Similar triangles: definition', 172,
      '$\\triangle ABC \\sim \\triangle DEF$ means $\\angle A = \\angle D$, $\\angle B = \\angle E$, $\\angle C = \\angle F$ **and** $\\frac{AB}{DE} = \\frac{BC}{EF} = \\frac{AC}{DF}$.',
      '**The order of the letters matters:** it tells you which vertices match. From the statement you can write the ratios without looking at the picture.',
      'Example 5.3: $\\triangle STQ \\sim \\triangle SPR$ with $TQ = 5$, $PR = 15$, $SQ = 4$: $\\frac{TQ}{PR} = \\frac{SQ}{SR} \\Rightarrow \\frac{5}{15} = \\frac{4}{SR} \\Rightarrow SR = 12$, so $QR = 12 - 4 = 8$.'),
    T('bpt-t', '5.2.2 The Basic Proportionality Theorem', 176,
      '**Theorem 5.1:** if a line parallel to one side of a triangle cuts the other two sides, it divides them proportionally: in $\\triangle ABC$ with $DE \\parallel BC$, $$\\frac{AB}{AD} = \\frac{AC}{AE}$$ and equally $\\frac{AD}{DB} = \\frac{AE}{EC}$.',
      '**Why (Activity 5.4):** $\\triangle BDE$ and $\\triangle CDE$ have the same base $DE$ and the same height (because $DE \\parallel BC$), so equal areas. Comparing each with $\\triangle ADE$ gives $\\frac{BD}{AD} = \\frac{CE}{AE}$; add 1 to both sides.',
      '**Theorem 5.2 (converse):** if $\\frac{AB}{AD} = \\frac{AC}{AE}$ then $DE \\parallel BC$. Example 5.5: $\\frac{RU}{RS} = \\frac{2}{9}$ and $\\frac{SV}{ST} = \\frac{4}{18} = \\frac{2}{9}$, so $UV \\parallel RT$.'),
    ST('bpt', 'Reading the theorem from the figure', 177, 'bpt',
       [('$DE \\parallel BC$ (the matching arrow marks).', 'k1'),
        ('The small triangle $ADE$ (shaded) has the same angles as $ABC$ (corresponding angles), so it is similar to it.', 'k2'),
        ('So the sides are proportional: $\\frac{AD}{AB} = \\frac{AE}{AC} = \\frac{DE}{BC}$. Note $DE$ only appears with whole sides $AB$, $AC$ — not with $DB$, $EC$.', 'k3')]),
    WK('ex-52a', 'Worked example: Example 5.4', 177,
       'In $\\triangle ABC$, $DE \\parallel AB$ with $D$ on $AC$, $E$ on $BC$. (a) $AC = 12$, $CD = 4$, $BC = 24$: find $CE$. (b) $AC = 15$, $AD = 3$, $BC = 25$: find $BE$.',
       ['(a) From vertex $C$: $\\frac{AC}{CD} = \\frac{BC}{CE} \\Rightarrow \\frac{12}{4} = \\frac{24}{CE} \\Rightarrow CE = 8$.', '(b) The pieces next to $AB$: $\\frac{AC}{AD} = \\frac{BC}{BE} \\Rightarrow \\frac{15}{3} = \\frac{25}{BE} \\Rightarrow BE = 5$.'],
       '$CE = 8$; $BE = 5$'),
    T('tests-t', '5.2.3 Three tests for similar triangles', 181,
      '**AA (AAA), Theorem 5.3:** two pairs of equal angles are enough (the third pair is then equal too, since angles add to 180°).',
      '**SAS, Theorem 5.4:** one equal angle and the two sides **forming** it in the same ratio. Example 5.7: $OP = OQ = 3$, $OR = OS = 6$, vertical angles at $O$ equal ⇒ $\\triangle OPQ \\sim \\triangle ORS$ (ratio $\\frac{1}{2}$).',
      '**SSS, Theorem 5.5:** all three pairs of sides in the same ratio. Activity 5.7: 3, 6, 8 and 6, 12, 16 (ratio 2).',
      'Compare with congruence (SAS, ASA, SSS): for similarity "equal sides" becomes "sides in the same ratio".'),
    TB('tests-tb', 'Choosing a test', 186, ['You know', 'Use', 'Typical source'],
       [['two angle pairs', 'AA', 'parallel lines, vertical angles, a shared angle'],
        ['an angle + its two sides', 'SAS', 'vertical angles with measured sides'],
        ['three sides', 'SSS', 'all lengths given']]),
    DG('bowtie', 'Example 5.6: the "bow-tie"', 183, 'bowtie',
       '$AC \\parallel BD$: vertical angles at $E$ are equal (red) and alternate angles $\\angle EAC = \\angle EBD$ (and the purple pair) are equal. AA ⇒ $\\triangle ACE \\sim \\triangle BDE$, so $\\frac{AE}{EB} = \\frac{CE}{ED}$, i.e. $AE \\times ED = CE \\times EB$.'),
    WK('ex-52b', 'Worked example: similar by SAS?', 186,
       'In $\\triangle PQR$ a 70° angle lies between sides 6 and 8. In $\\triangle LMN$ a 70° angle lies between sides 3 and 4. Are the triangles similar?',
       ['Ratios of the sides around the 70° angles: $\\frac{6}{3} = 2$ and $\\frac{8}{4} = 2$.', 'Equal included angles, sides in ratio 2 ⇒ SAS similarity.', 'Then the third sides are in ratio 2 as well.'],
       'yes, by SAS (ratio 2)'),
    'math11-u5-c02', 'math11-u5-c10', 'math11-u5-c04', 'math11-u5-c05', 'math11-u5-xtra2', 'math11-u5-wrk1',
]

# ------------------------------------------------------------------ 5.3
L3 = [
    T('alt-t', '5.3.1 The altitude to the hypotenuse', 189,
      '**Theorem (5.6 in the book):** in a right triangle $ABC$ (right angle at $C$), the altitude $CD$ to the hypotenuse makes two triangles that are similar to each other and to $ABC$: $\\triangle ACD \\sim \\triangle ABC \\sim \\triangle CBD$ (each pair shares an angle and has a right angle — AA).',
      'From the ratios we get three **geometric-mean** results:',
      '- $CD^2 = AD \\times DB$ (the altitude is the GM of the two pieces);',
      '- $AC^2 = AD \\times AB$ and $BC^2 = BD \\times AB$ (each leg is the GM of the hypotenuse and its adjacent piece).',
      'Adding the last two: $AC^2 + BC^2 = AB(AD + DB) = AB^2$ — a proof of **Pythagoras** (Example 5.9). (The book cites "Theorem 5.5" in steps 2 and 5; the reason is the altitude theorem / AA.)'),
    ST('altitude', 'Review Q4: AD = 9, BD = 16', 199, 'altitude',
       [('$CD^2 = 9 \\times 16 = 144$, so $CD = 12$.', 'k1'),
        ('$AC^2 = AD \\times AB = 9 \\times 25 = 225$: $AC = 15$ (blue triangle).', 'k2'),
        ('$BC^2 = 16 \\times 25 = 400$: $BC = 20$ (green). Check: $15^2 + 20^2 = 625 = 25^2$.', 'k3')]),
    ST('shadow', 'Shadows: same sun, same angle', 191, 'shadow',
       [('Pole 6 m casts 4 m: a right triangle.', 'k1'),
        ('Tower with 28 m shadow at the same time: the sun\'s rays make the same angle (orange), so the triangles are similar (AA).', 'k2'),
        ('$\\frac{h}{28} = \\frac{6}{4} \\Rightarrow h = 42$ m.', 'k3')]),
    T('trig-t', '5.3.2 Trigonometric ratios come from similarity', 192,
      'All right triangles with the same acute angle $A$ are similar, so the ratios of their sides depend **only on the angle**:',
      '$$\\sin A = \\frac{\\text{opposite}}{\\text{hypotenuse}}, \\quad \\cos A = \\frac{\\text{adjacent}}{\\text{hypotenuse}}, \\quad \\tan A = \\frac{\\text{opposite}}{\\text{adjacent}}$$',
      'Exact values: 45° (legs 1, 1, hypotenuse $\\sqrt{2}$): $\\sin = \\cos = \\frac{\\sqrt{2}}{2}$, $\\tan = 1$. 60° (sides 1, $\\sqrt{3}$, 2): $\\sin 60° = \\frac{\\sqrt{3}}{2}$, $\\cos 60° = \\frac{1}{2}$, $\\tan 60° = \\sqrt{3}$; and $\\tan 30° = \\frac{1}{\\sqrt{3}}$.',
      '**Angle of elevation:** from the horizontal **up** to the object. **Angle of depression:** from the horizontal **down**. They are equal for two observers looking at each other (alternate angles).'),
    DG('elev', 'Example 5.10', 194, 'elev',
       'Tower 30 m. The man who sees the top at 30° stands $30 \\div \\tan 30° = 30\\sqrt{3}$ m away; the one at 60° stands $30 \\div \\tan 60° = 10\\sqrt{3}$ m away. Distance apart $40\\sqrt{3} \\approx 69.3$ m. (The angle values are missing from the book\'s question text.)'),
    'math11-u5-c11', 'math11-u5-mn3', 'math11-u5-wrk3',
]

# ------------------------------------------------------------------ 5.4
L4 = [
    T('=math11-u5-c08', '5.4 Perimeter, area and volume of similar figures', 194,
      'If corresponding lengths are in ratio $k$ (scale factor):',
      '- **every length** (sides, perimeter, altitudes, medians, angle bisectors) is in ratio $k$;',
      '- **every area** (triangle area, surface area) is in ratio $k^2$;',
      '- **every volume** is in ratio $k^3$.',
      'Example 5.11: longest sides 3 and 4 ⇒ areas in ratio $\\frac{9}{16}$. Example 5.12: perimeters 24 and 32 ⇒ sides in ratio $\\frac{3}{4}$.',
      '**Going backwards:** area ratio $\\frac{4}{25}$ ⇒ $k = \\sqrt{\\frac{4}{25}} = \\frac{2}{5}$; volume ratio $\\frac{1}{8}$ ⇒ $k = \\sqrt[3]{\\frac{1}{8}} = \\frac{1}{2}$.'),
    DG('areagrid', 'Why area goes with k²', 195, 'areagrid',
       'Doubling every side of a triangle makes room for $2 \\times 2 = 4$ copies of the original; tripling gives $3 \\times 3 = 9$ copies.'),
    TB('kkk', 'Scale factor table', 198, ['Quantity', 'Ratio', 'k = 2', 'k = 3'],
       [['length, perimeter', '$k$', '2', '3'], ['area, surface area', '$k^2$', '4', '9'], ['volume', '$k^3$', '8', '27']]),
    WK('ex-54a', 'Worked example: Review Q9 (trapezium)', 200,
       'ABCD is a trapezium with $AB \\parallel DC$ and $AB = 2CD$. The diagonals meet at $O$. Find $\\frac{a(\\triangle AOB)}{a(\\triangle COD)}$.',
       ['$AB \\parallel DC$: alternate angles and vertical angles at $O$ ⇒ $\\triangle AOB \\sim \\triangle COD$ (AA).', 'Scale factor $\\frac{AB}{CD} = 2$.', 'Area ratio $2^2 = 4$.'],
       '4 : 1'),
    RM('summary-t', 'Unit summary', 200,
       'Similar polygons: equal angles **and** proportional sides. Triangles: AA, SAS or SSS is enough.',
       'Parallel line in a triangle ⇒ proportional pieces (and conversely).',
       'Right triangle + altitude: $CD^2 = AD \\cdot DB$, $AC^2 = AD \\cdot AB$.',
       'Scale factor $k$: lengths $k$, areas $k^2$, volumes $k^3$.'),
    'math11-u5-mn4', 'math11-u5-wrk5', 'math11-u5-wrk6',
]

LESSONS = {'math11-u5-l5-1': L1, 'math11-u5-l5-2': L2, 'math11-u5-l5-3': L3, 'math11-u5-l5-4': L4}

# ------------------------------------------------------------------ practice
a = QSet('5.1 Practice — similar polygons', 's51')
a.S(170, 'Exercise 5.1 Q8: find the geometric and arithmetic means of (a) 2 and 8 (b) 9 and 16 (c) 12 and 15.', '4, 5; 12, 12.5; $6\\sqrt{5} \\approx 13.4$, 13.5',
    ['Step 1: GM $= \\sqrt{ab}$: $\\sqrt{16}$, $\\sqrt{144}$, $\\sqrt{180}$.', 'Step 2: AM $= \\frac{a + b}{2}$.'], 'GM ≤ AM always.', [('4 and 9?', 'GM 6, AM 6.5.')])
a.S(170, 'Exercise 5.1 Q10: solve $\\frac{x}{50} = \\frac{30}{20}$ and $\\frac{y}{20} = \\frac{30}{50}$ (proportions).', '$x = 75$; $y = 12$',
    ['Step 1: $x = 50 \\times 1.5$.', 'Step 2: $y = 20 \\times 0.6$.'], 'Cross-multiply.', [('$\\frac{5}{x} = \\frac{15}{18}$?', '$x = 6$.')])
a.S(171, 'Exercise 5.2 Q2: a print shows an object 2 cm wide and 2.3 cm high; in an enlargement it is 7.5 cm wide. Find its height.', '8.625 cm',
    ['Step 1: scale factor $\\frac{7.5}{2} = 3.75$.', 'Step 2: $2.3 \\times 3.75 = 8.625$.'], 'Same factor for width and height.', [('Width 10 cm instead?', 'height 11.5 cm.')])
a.S(169, 'Show: if $\\frac{a}{p} = \\frac{b}{q}$ then $\\frac{a + p}{p} = \\frac{b + q}{q}$.', 'add 1 to both sides',
    ['Step 1: $\\frac{a}{p} + 1 = \\frac{b}{q} + 1$.', 'Step 2: $\\frac{a + p}{p} = \\frac{b + q}{q}$.'], 'Write 1 as $\\frac{p}{p}$.', [('Show $\\frac{a - p}{p} = \\frac{b - q}{q}$.', 'subtract 1.')])
a.M(172, 'Which pair is always similar?', ['two squares', 'two rectangles', 'two isosceles triangles', 'two right triangles'], 'A',
    ['Step 1: all angles 90°, sides in one ratio.'], 'Test with a counter-example.', [('Two regular hexagons?', 'always similar.')])
a.TF(172, 'Every two rhombuses are similar.', False, ['Step 1: a square and a rhombus with a 60° angle have equal sides but different angles.'], 'Angles must match too.', [('Every two equilateral triangles?', 'True.')])
a.TF(169, 'For positive $a \\ne b$, $\\sqrt{ab} < \\frac{a + b}{2}$.', True, ['Step 1: the difference is $\\frac{(\\sqrt{a} - \\sqrt{b})^2}{2} > 0$.'], 'Equality only when $a = b$.', [('$a = b = 5$?', 'both means equal 5.')])

b = QSet('5.2 Practice — similar triangles', 's52')
b.S(174, 'Exercise 5.3 Q1: $\\triangle ABC \\sim \\triangle ADE$, $AD = 5$, $AE = 6$, $BC = 12$, $AB = 15$. Find $AC$ and $DE$.', '$AC = 18$, $DE = 4$',
    ['Step 1: $k = \\frac{AB}{AD} = 3$.', 'Step 2: $AC = 3 \\times 6 = 18$; $DE = 12 \\div 3 = 4$.'], 'Find $k$ from a known pair.', [('$AB = 10$ instead?', '$k = 2$: $AC = 12$, $DE = 6$.')])
b.S(173, 'Example 5.2: $\\triangle ABC \\sim \\triangle DEF$ with $AB = 3$, $DE = 7$, $BC = x$, $EF = y$. Write $y$ in terms of $x$.', '$y = \\frac{7x}{3}$',
    ['Step 1: $\\frac{AB}{DE} = \\frac{BC}{EF}$: $\\frac{3}{7} = \\frac{x}{y}$.', 'Step 2: $3y = 7x$.'], 'Match letters in order.', [('If $x = 6$?', '$y = 14$.')])
b.S(177, 'In $\\triangle ABC$, $DE \\parallel BC$ with $AD = 4$, $DB = 6$, $AE = 5$. Find $EC$.', '7.5',
    ['Step 1: $\\frac{AD}{DB} = \\frac{AE}{EC}$.', 'Step 2: $\\frac{4}{6} = \\frac{5}{EC}$.'], 'Pieces to pieces.', [('$AD = 3$, $DB = 9$, $AE = 2$?', '$EC = 6$.')])
b.S(177, 'In $\\triangle ABC$, $DE \\parallel BC$, $AD = 4$, $AB = 10$, $BC = 15$. Find $DE$.', '6',
    ['Step 1: $\\frac{DE}{BC} = \\frac{AD}{AB}$ (whole sides!).', 'Step 2: $DE = 15 \\times 0.4$.'], 'For $DE$ use $AD : AB$, not $AD : DB$.', [('$AD = 2$, $AB = 8$, $BC = 12$?', '$DE = 3$.')])
b.S(178, 'Is $UV \\parallel RT$ if $RU = 3$, $RS = 12$, $SV = 5$, $ST = 20$?', 'yes',
    ['Step 1: $\\frac{RU}{RS} = \\frac{1}{4}$, $\\frac{SV}{ST} = \\frac{1}{4}$.', 'Step 2: converse of the BPT.'], 'Equal ratios ⇒ parallel.', [('$SV = 6$?', 'no ($\\frac{6}{20} \\ne \\frac{1}{4}$).')])
b.S(188, 'Exercise 5.7 Q1: $AB = 3$, $BC = 4$, $AC = 5$ and $DE = 12$. Find $EF$, $DF$ for $\\triangle ABC \\sim \\triangle DEF$.', '$EF = 16$, $DF = 20$',
    ['Step 1: $k = \\frac{12}{3} = 4$.', 'Step 2: multiply each side by 4.'], 'SSS: same ratio for all sides.', [('$DE = 6$?', '8 and 10.')])
b.S(199, 'Review Q2: $\\angle A = \\angle D = 60°$, $AB = 4$, $AC = 10$, $DE = 2$, $DF = 5$. Similar?', 'yes, SAS (ratio 2)',
    ['Step 1: $\\frac{AB}{DE} = 2$, $\\frac{AC}{DF} = 2$.', 'Step 2: the equal angle is between those sides.'], 'Check the angle is the included one.', [('$DF = 4$?', 'not similar by SAS.')])
b.S(184, 'Exercise 5.5 Q5: prove that two right triangles with one equal acute angle are similar.', 'AA',
    ['Step 1: the right angles are equal.', 'Step 2: the given acute angles are equal.', 'Step 3: two pairs of angles ⇒ AA.'], 'Right angle counts as one pair.', [('Two isosceles triangles with equal vertex angles?', 'similar (SAS or AA).')])
b.S(183, 'Example 5.6: chords $AB$, $CD$ of a circle cross at $P$ (Review Q6). Explain why $AP \\times PB = CP \\times PD$.', 'similar triangles APC and DPB',
    ['Step 1: vertical angles at $P$ are equal.', 'Step 2: $\\angle CAB = \\angle CDB$ (angles on the same arc $CB$).', 'Step 3: AA ⇒ $\\frac{AP}{DP} = \\frac{CP}{BP}$; cross-multiply.'], 'Look for vertical angles and equal inscribed angles.', [('Secants from an outside point $P$?', '$PA \\cdot PB = PC \\cdot PD$ (Review Q7).')])
b.M(186, 'Which is **not** a similarity test for triangles?', ['SSA', 'AA', 'SAS', 'SSS'], 'A',
    ['Step 1: two sides and a non-included angle do not fix the shape.'], 'The angle must be between the sides.', [('Is AAA a test?', 'Yes (same as AA).')])
b.TF(175, 'If $DE \\parallel BC$ in $\\triangle ABC$, then $\\frac{AD}{DB} = \\frac{DE}{BC}$.', False,
     ['Step 1: $\\frac{DE}{BC} = \\frac{AD}{AB}$, not $\\frac{AD}{DB}$.'], 'Part to whole for the parallel side.', [('Is $\\frac{AD}{DB} = \\frac{AE}{EC}$?', 'Yes.')])

c = QSet('5.3 Practice — applications', 's53')
c.S(199, 'Review Q4: right angle at $C$, altitude $CD$, $AD = 9$, $BD = 16$. Find $CD$, $AC$, $BC$.', '12, 15, 20',
    ['Step 1: $CD = \\sqrt{9 \\times 16}$.', 'Step 2: $AC = \\sqrt{9 \\times 25}$; $BC = \\sqrt{16 \\times 25}$.'], 'Geometric means.', [('$AD = 4$, $BD = 9$?', '$CD = 6$, $AC = 2\\sqrt{13}$, $BC = 3\\sqrt{13}$.')])
c.S(199, 'Review Q5 (corrected): altitude $CD = 12$ and $BD$ exceeds $AD$ by 18. Find $AD$ and $BD$.', '$AD = 6$, $BD = 24$',
    ['Step 1: $AD(AD + 18) = 144$.', 'Step 2: $AD^2 + 18AD - 144 = 0 \\Rightarrow (AD + 24)(AD - 6) = 0$.'],
    'The book says "BC exceeds AD by 18", which gives no neat answer; "BD exceeds AD" is the intended data.', [('$CD = 6$, $BD = AD + 9$?', '$AD = 3$, $BD = 12$.')])
c.S(191, 'Exercise 5.8 Q4: a 30 m tree casts a 10 m shadow. A building casts 15 m at the same time. Height?', '45 m',
    ['Step 1: ratio height : shadow $= 3$.', 'Step 2: $15 \\times 3$.'], 'Same time ⇒ same ratio.', [('Pole 2 m, shadow 3 m, tree shadow 18 m?', '12 m.')])
c.S(200, 'Review Q10: a 6 m pole casts 4 m; a tower casts 28 m. Height of the tower?', '42 m',
    ['Step 1: $\\frac{h}{28} = \\frac{6}{4}$.'], 'Write height over shadow on both sides.', [('Shadow 10 m?', '15 m.')])
c.S(192, 'Exercise 5.9 Q2: hypotenuse $AB = 25$ cm. (a) $\\sin A = \\frac{4}{5}$: find $BC$. (b) $\\cos A = 0.6$: find $\\tan A$.', '20 cm; about 1.33',
    ['Step 1: $BC = 25 \\times \\frac{4}{5}$.', 'Step 2: $\\sin A = 0.8$, $\\tan A = \\frac{0.8}{0.6}$.'], '$\\sin^2 A + \\cos^2 A = 1$.', [('$\\sin A = 0.6$?', '$BC = 15$, $\\tan A = 0.75$.')])
c.S(193, 'Exercise 5.9 Q3 and Q5: how are $\\tan 60°$ and $\\tan 30°$ related? Show $\\tan A \\cdot \\tan(90° - A) = 1$.', 'reciprocals',
    ['Step 1: $\\sqrt{3} \\times \\frac{1}{\\sqrt{3}} = 1$.', 'Step 2: the opposite side of $A$ is the adjacent side of $90° - A$.'], 'Complementary angles swap opposite and adjacent.', [('$\\tan 20° \\cdot \\tan 70°$?', '1.')])
c.S(194, 'Exercise 5.10 Q1: 24 m from a building the angle of elevation is 30°. Height?', '$8\\sqrt{3} \\approx 13.9$ m',
    ['Step 1: $h = 24 \\tan 30° = \\frac{24}{\\sqrt{3}}$.'], 'tan = opposite / adjacent.', [('Angle 45°?', '24 m.')])
c.S(194, 'Exercise 5.10 Q3: from the top of a tower a car 20 m from the foot is seen at a depression of 60°. Height?', '$20\\sqrt{3} \\approx 34.6$ m',
    ['Step 1: the elevation from the car is also 60° (alternate angles).', 'Step 2: $h = 20 \\tan 60°$.'], 'Depression = elevation from the other end.', [('Depression 30°?', '$\\frac{20}{\\sqrt{3}} \\approx 11.5$ m.')])
c.S(200, 'Review Q8: planes fly north at 1000 km/h and west at 1200 km/h. Distance apart after 5 h?', 'about 7810 km',
    ['Step 1: legs 5000 and 6000 km.', 'Step 2: $\\sqrt{5000^2 + 6000^2} = 1000\\sqrt{61}$.'], 'Pythagoras.', [('After 1 h?', 'about 1562 km.')])
c.M(194, 'A cat sees a bird at the top of a 4 m tree at elevation 45°. Distance to the tree?', ['4 m', '2 m', '$4\\sqrt{2}$ m', '8 m'], 'A',
    ['Step 1: $\\tan 45° = 1$, so distance = height.'], '45° ⇒ isosceles right triangle.', [('Elevation 60°?', '$\\frac{4}{\\sqrt{3}}$ m.')])
c.TF(191, 'The altitude to the hypotenuse is the geometric mean of the two pieces of the hypotenuse.', True, ['Step 1: $\\triangle ACD \\sim \\triangle CBD$ gives $\\frac{AD}{CD} = \\frac{CD}{DB}$.'], 'Middle term squared = product of outer terms.', [('Each leg is the GM of …?', 'the hypotenuse and the adjacent piece.')])

d = QSet('5.4 Practice — ratios of perimeter, area, volume', 's54')
d.S(196, 'Exercise 5.11 Q1: similar triangles with areas 64 cm² and 121 cm²; $EF = 15.4$ cm. Find $BC$.', '11.2 cm',
    ['Step 1: $k = \\sqrt{\\frac{64}{121}} = \\frac{8}{11}$.', 'Step 2: $BC = 15.4 \\times \\frac{8}{11}$.'], 'Square root of the area ratio.', [('Areas 9 and 25, side 10 in the larger?', '6.')])
d.S(196, 'Exercise 5.11 Q3: one triangle\'s sides are 5 times the other\'s; the smaller area is 6 cm². Larger area?', '150 cm²',
    ['Step 1: area ratio $5^2 = 25$.'], 'Square the scale factor.', [('Factor 3?', '54 cm².')])
d.S(198, 'Exercise 5.12 Q2: areas in ratio 4 : 25. Ratio of sides and perimeters?', '2 : 5 and 2 : 5',
    ['Step 1: $\\sqrt{4} : \\sqrt{25}$.', 'Step 2: perimeter is a length.'], 'All lengths share $k$.', [('Areas 9 : 49?', '3 : 7.')])
d.S(198, 'Exercise 5.13: volumes in ratio 1 : 8. Ratio of edges? If the larger edge is 30 cm, find the smaller.', '1 : 2; 15 cm',
    ['Step 1: $\\sqrt[3]{8} = 2$.', 'Step 2: $30 \\div 2$.'], 'Cube root for volumes.', [('Volumes 8 : 27?', 'edges 2 : 3.')])
d.S(198, 'Activity 5.13: cubes with edges 1 cm and 4 cm. Ratios of surface areas and volumes?', '1 : 16 and 1 : 64',
    ['Step 1: $4^2 = 16$.', 'Step 2: $4^3 = 64$.'], 'Area $k^2$, volume $k^3$.', [('Edges 2 : 3, larger volume 54?', 'smaller 16.')])
d.S(197, 'Example 5.12: perimeters 24 m and 32 m. Ratio of sides and of areas?', '3 : 4 and 9 : 16',
    ['Step 1: $\\frac{24}{32} = \\frac{3}{4}$.', 'Step 2: square it.'], 'Perimeter ratio = $k$.', [('Perimeters 10 and 15?', 'areas 4 : 9.')])
d.M(198, 'Two similar cones have heights 6 and 9. The small one holds 160 ml. The large one holds', ['540 ml', '240 ml', '360 ml', '480 ml'], 'A',
    ['Step 1: $k = 1.5$, $k^3 = 3.375$.', 'Step 2: $160 \\times 3.375 = 540$.'], 'Capacity is a volume.', [('Surface ratio?', '4 : 9.')])
d.TF(197, 'If two similar triangles have sides in ratio $k$, their altitudes are in ratio $k^2$.', False, ['Step 1: an altitude is a length, so the ratio is $k$.'], 'Only areas use $k^2$.', [('Medians?', 'ratio $k$.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Similar figures', 'Same shape: equal angles and proportional sides.', 170),
    ('Scale factor', 'The constant ratio $k$ of corresponding lengths.', 194),
    ('Geometric mean', '$\\sqrt{ab}$ for positive $a, b$.', 170),
    ('Basic Proportionality Theorem', 'A line parallel to one side cuts the other two sides proportionally.', 176),
    ('Angle of elevation', 'Angle from the horizontal up to an object.', 193),
    ('Angle of depression', 'Angle from the horizontal down to an object.', 193),
]
TIPS = [('Write the similarity statement in matching order before writing ratios.', 172),
        ('Parallel side: DE / BC = AD / AB (whole sides).', 177), ('Lengths k, areas k², volumes k³.', 198)]
IDEAS = [('bpt', 'Basic Proportionality Theorem', 'l5_2', 'math11-u5-md-bpt-t'), ('tests', 'AA, SAS, SSS', 'l5_2', 'math11-u5-md-tests-t'),
         ('alt', 'Altitude on the hypotenuse', 'l5_3', 'math11-u5-md-alt-t'), ('kkk', 'k, k², k³', 'l5_4', 'math11-u5-c08')]
