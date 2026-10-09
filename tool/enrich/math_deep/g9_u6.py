r"""Grade 9 Unit 6 — Right Angled Triangle and Trigonometric Ratios (pp. 130-153)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet, plane
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL

UID = 'math9-u6'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_pyth():
    f = Fig(340, 220)
    C, B, A = (100, 140), (100, 86), (172, 140)
    f.g('k2 k3').rect(46, 86, 54, 54, BLUE, 2, FILL[BLUE]).text(73, 118, '3² = 9', 13, BLUE)
    f.rect(100, 140, 72, 72, GREEN, 2, FILL[GREEN]).text(136, 182, '4² = 16', 14, GREEN).end()
    f.g('k3').poly([B, A, (226, 68), (154, 14)], RED, 2, FILL[RED]).text(163, 64, '5² = 25', 15, RED).end()
    f.poly([C, B, A], INK, 2.6).right(C, B, A, 9)
    f.g('k1').text(274, 110, 'legs 3 and 4,', 13, INK).text(274, 128, 'hypotenuse 5', 13, RED).end()
    f.g('k2').text(274, 110, 'squares on legs:', 12.5, INK).text(274, 128, '9 + 16 = 25', 14, GREEN).end()
    f.g('k3').text(274, 110, 'square on the', 12.5, INK).text(274, 128, 'hypotenuse = 25', 13, RED)
    f.text(274, 156, '3² + 4² = 5²', 15, RED).end()
    return f


def f_sides():
    f = Fig(330, 205)
    A, C, B = (40, 165), (240, 165), (240, 40)
    f.poly([A, C, B], INK, 2.6).right(C, A, B, 11)
    f.text(32, 182, 'A', 14).text(248, 182, 'C', 14).text(250, 36, 'B', 14, INK, 'start')
    f.text(124, 92, 'hypotenuse', 13, PURPLE).raw('')
    f.g('k1', 'k1').angle(A, C, B, 26, RED, None, w=2.4)
    f.line(240, 40, 240, 165, RED, 4).text(248, 100, 'opposite', 13, RED, 'start').text(248, 116, 'to A', 13, RED, 'start')
    f.line(40, 165, 240, 165, BLUE, 4).text(140, 186, 'adjacent to A', 13, BLUE).end()
    f.g('k2', 'k2').angle(B, A, C, 26, RED, None, w=2.4)
    f.line(40, 165, 240, 165, RED, 4).text(140, 186, 'opposite to B', 13, RED)
    f.line(240, 40, 240, 165, BLUE, 4).text(248, 100, 'adjacent', 13, BLUE, 'start').text(248, 116, 'to B', 13, BLUE, 'start').end()
    return f


def f_similar():
    import math
    f = Fig(330, 170)
    A = (24, 150)
    t = math.tan(math.radians(22))
    f.line(A[0], A[1], 316, A[1], INK, 2).line(A[0], A[1], 310, A[1] - 286 * t, INK, 2)
    for x, c, nm in ((110, BLUE, 'D E'), (190, GREEN, 'F G'), (280, RED, 'P Q')):
        top = (x, A[1] - (x - A[0]) * t)
        f.line(x, A[1], top[0], top[1], c, 3).right((x, A[1]), A, top, 7, c)
        f.text(x - 6, top[1] - 6, nm.split()[0], 12.5, c, 'end').text(x, A[1] + 15, nm.split()[1], 12.5, c)
    f.angle(A, (300, A[1]), (300, A[1] - 276 * t), 30, ORANGE, 'A', w=2)
    f.text(24, 20, 'DE/AD = FG/AF = PQ/AP', 13.5, INK, 'start').text(24, 38, '= sin A (same for every size)', 13, GREEN, 'start')
    return f


def f_trigtable():
    rows = [(10, '.1736', '.9848', '.1763'), (11, '.1908', '.9816', '.1944'), (12, '.2079', '.9781', '.2126'),
            (13, '.2250', '.9744', '.2309'), (14, '.2419', '.9703', '.2493')]
    f = Fig(330, 190)
    xs = [50, 130, 210, 290]
    for x, h in zip(xs, ['Angle', 'sin', 'cos', 'tan']):
        f.text(x, 22, h, 14, ORANGE if h == 'sin' else INK)
    for i, r in enumerate(rows):
        y = 34 + i * 28
        hit = r[0] == 12
        if hit:
            f.rect(14, y, 156, 24, ORANGE, 2, FILL[ORANGE], 5)
        f.text(xs[0], y + 17, f'{r[0]}°', 13, BLUE if hit else INK)
        for x, v in zip(xs[1:], r[1:]):
            f.text(x, y + 17, v, 13, RED if hit and x == 130 else INK)
    f.arrow(76, 92, 104, 92, RED, 2, 7)
    f.text(165, 184, 'sin 12° = 0.2079', 14, RED)
    return f


def f_elevdep():
    f = Fig(330, 170)
    # elevation
    E, T = (20, 140), (140, 40)
    f.line(140, 40, 140, 150, GREEN, 4).line(10, 150, 160, 150, GREY, 1.5)
    f.line(E[0], E[1], 150, E[1], INK, 1.6, dash=True).line(E[0], E[1], T[0], T[1], RED, 2.2)
    f.angle(E, (150, E[1]), T, 34, ORANGE, 'e', w=2.2)
    f.text(80, 30, 'elevation: look up', 12.5, ORANGE)
    f.dot(E[0], E[1], INK, 4)
    # depression
    D, Bt = (190, 50), (310, 150)
    f.line(190, 50, 190, 150, INK, 3).line(180, 150, 322, 150, GREY, 1.5)
    f.line(D[0], D[1], 318, D[1], INK, 1.6, dash=True).line(D[0], D[1], Bt[0], Bt[1], RED, 2.2)
    f.angle(D, (318, D[1]), Bt, 40, ORANGE, 'd', w=2.2)
    f.text(252, 30, 'depression: look down', 12.5, ORANGE)
    f.dot(D[0], D[1], INK, 4).dot(Bt[0], Bt[1], BLUE, 5)
    f.text(165, 166, 'both measured from the horizontal (dashed)', 12, GREY)
    return f


def f_labels():
    f = Fig(330, 190)
    A, B, C = (40, 160), (290, 160), (196, 34)
    f.poly([A, B, C], INK, 2.4)
    f.line(B[0], B[1], C[0], C[1], RED, 4).line(A[0], A[1], C[0], C[1], BLUE, 4).line(A[0], A[1], B[0], B[1], GREEN, 4)
    f.angle(A, B, C, 26, RED, None, w=2.2).angle(B, A, C, 26, BLUE, None, w=2.2).angle(C, A, B, 22, GREEN, None, w=2.2)
    f.text(28, 176, 'A', 15, RED).text(302, 176, 'B', 15, BLUE).text(196, 24, 'C', 15, GREEN)
    f.text(256, 92, 'a', 16, RED, 'start').text(104, 90, 'b', 16, BLUE, 'end').text(165, 182, 'c', 16, GREEN)
    f.text(10, 20, 'side a is opposite angle A', 12, GREY, 'start')
    return f


def f_ships():
    import math
    f = Fig(240, 190)
    H = (40, 92)
    a = (H[0] + 122 * math.cos(math.radians(40)), H[1] - 122 * math.sin(math.radians(40)))
    b = (H[0] + 94 * math.cos(math.radians(40)), H[1] + 94 * math.sin(math.radians(40)))
    f.line(H[0], H[1], a[0], a[1], BLUE, 2.6).line(H[0], H[1], b[0], b[1], GREEN, 2.6)
    f.line(a[0], a[1], b[0], b[1], RED, 2.6, dash=True)
    f.angle(H, a, b, 26, ORANGE, '80°', lr=44, w=2)
    f.seglabel(H, a, '102 km', 22, BLUE, 12.5, -1).seglabel(H, b, '78 km', 22, GREEN, 12.5, 1)
    f.text((a[0] + b[0]) / 2 + 14, (a[1] + b[1]) / 2 + 4, 'd = ?', 14, RED, 'start')
    f.text(28, 100, 'H', 14).text(a[0] + 8, a[1] - 2, 'A', 14, BLUE, 'start').text(b[0] + 8, b[1] + 6, 'B', 14, GREEN, 'start')
    return f


def f_planecars():
    f = Fig(330, 190)
    P, L, R = (180, 30), (12, 160), (277, 160)
    f.line(0, 160, 330, 160, GREY, 2).line(4, 30, 326, 30, INK, 1.4, dash=True)
    f.line(P[0], P[1], P[0], 160, PURPLE, 2, dash=True).text(P[0] - 6, 120, '5150 m', 12.5, PURPLE, 'end')
    f.line(P[0], P[1], L[0], L[1], RED, 2.2).line(P[0], P[1], R[0], R[1], BLUE, 2.2)
    f.angle(P, (4, 30), L, 40, RED, '37°', lr=52, w=2).angle(P, (326, 30), R, 34, BLUE, '53°', lr=46, w=2)
    f.angle(L, (100, 160), P, 34, RED, '37°', lr=48, w=2).angle(R, (200, 160), P, 26, BLUE, '53°', lr=38, w=2)
    f.rect(P[0] - 12, P[1] - 5, 24, 10, INK, 0, INK, 4)
    f.rect(L[0] - 8, L[1] - 9, 18, 9, RED, 0, RED, 2).rect(R[0] - 9, R[1] - 9, 18, 9, BLUE, 0, BLUE, 2)
    f.text(96, 180, 'x', 13, RED).text(228, 180, 'y', 13, BLUE)
    return f


DIAGRAMS = {
    'pyth': (f_pyth(), "Pythagoras' theorem with squares", 131),
    'sides': (f_sides(), 'Opposite, adjacent and hypotenuse', 136),
    'similar': (f_similar(), 'Trig ratios depend only on the angle (Fig. 6.6)', 137),
    'trigtable': (f_trigtable(), 'Reading the table of trigonometric ratios (Fig. 6.7)', 138),
    'elevdep': (f_elevdep(), 'Angle of elevation and angle of depression', 142),
    'labels': (f_labels(), 'Standard labelling of a triangle', 146),
    'ships': (f_ships(), 'Two ships (Exercise 6.6 Q4)', 151),
    'planecars': (f_planecars(), 'Aeroplane and two cars (Review Q5)', 152),
}

# ------------------------------------------------------------------ lesson 6.1
L1 = [
    T('=math9-u6-c01', "6.1 Pythagoras' theorem", 130,
      'In a right-angled triangle the side opposite the right angle is the **hypotenuse** — always the longest side. The other two sides are the **legs**.',
      "**Pythagoras' theorem:** the square on the hypotenuse equals the sum of the squares on the legs: $$c^2 = a^2 + b^2$$",
      'Use it in two directions:',
      '- **Find the hypotenuse** (add): $c = \\sqrt{a^2 + b^2}$. Legs 6 and 8: $c = \\sqrt{36 + 64} = 10$.',
      '- **Find a leg** (subtract): $a = \\sqrt{c^2 - b^2}$. Hypotenuse 15, leg 12: $a = \\sqrt{225 - 144} = 9$.',
      'The theorem works **only** for right-angled triangles.'),
    ST('pyth', 'Seeing the theorem: the 3-4-5 triangle', 131, 'pyth',
       [('A right triangle with legs 3 and 4 and hypotenuse 5.', 'k1'),
        ('Squares on the legs have areas $3^2 = 9$ and $4^2 = 16$.', 'k2'),
        ('The square on the hypotenuse has area $5^2 = 25 = 9 + 16$.', 'k3')]),
    'math9-u6-tbl1',
    T('conv-t', 'The converse: is it a right triangle?', 131,
      "**Converse of Pythagoras:** if the sides satisfy $c^2 = a^2 + b^2$ (where $c$ is the **longest** side), the triangle is right-angled, and the right angle is opposite $c$.",
      '**Method:** 1. Pick the longest side as $c$. 2. Compute $c^2$ and $a^2 + b^2$ separately. 3. Equal → right-angled; not equal → not right-angled.',
      'Going further: if $c^2 < a^2 + b^2$ the largest angle is acute; if $c^2 > a^2 + b^2$ it is obtuse.'),
    WK('ex-61a', 'Worked example: Examples 6.1 and 6.2', 131,
       'Are triangles with sides (a) 5, 12, 13 (b) 7, 8, 12 right-angled?',
       ['(a) Longest side 13: $13^2 = 169$; $5^2 + 12^2 = 25 + 144 = 169$. Equal → right-angled.', '(b) Longest 12: $12^2 = 144$; $7^2 + 8^2 = 49 + 64 = 113$. Not equal → not right-angled (in fact $144 > 113$, so it is obtuse).'],
       '(a) yes (b) no'),
    TB('triples-t', 'Pythagorean triples to recognise', 132, ['Triple', 'Check', 'Multiples'],
       [['3, 4, 5', '9 + 16 = 25', '6, 8, 10; 9, 12, 15; 30, 40, 50'], ['5, 12, 13', '25 + 144 = 169', '10, 24, 26'],
        ['8, 15, 17', '64 + 225 = 289', '16, 30, 34'], ['7, 24, 25', '49 + 576 = 625', '14, 48, 50']],
       'Any multiple of a triple is another triple: 36, 48, 60 is $12 \\times (3, 4, 5)$.'),
    WK('ex-61b', 'Worked example: Exercise 6.1 Q4 (parallelogram)', 133,
       'A parallelogram has adjacent sides 21 cm and 28 cm and a diagonal of 35 cm. Is it a rectangle?',
       ['The two sides and the diagonal form a triangle with sides 21, 28, 35.', '$35^2 = 1225$ and $21^2 + 28^2 = 441 + 784 = 1225$.', 'So the angle between the 21 cm and 28 cm sides is $90°$.', 'A parallelogram with one right angle is a rectangle.'],
       'Yes, it is a rectangle (21, 28, 35 is $7 \\times$ (3, 4, 5)).'),
]

# ------------------------------------------------------------------ lesson 6.2
L2 = [
    T('=math9-u6-c02', "6.2 Solving problems with Pythagoras' theorem", 133,
      'Ladders against walls, diagonals of rectangles, screens, journeys "south then east" and aeroplanes climbing all hide a right triangle.',
      '**Method:**',
      '1. Draw a sketch and mark the right angle (wall and ground, sides of a rectangle, south and east).',
      '2. Label the hypotenuse (opposite the right angle) and the legs.',
      '3. Decide: unknown is the hypotenuse → **add** squares; unknown is a leg → **subtract** squares.',
      '4. Square-root, then answer with units and check that the hypotenuse is the longest.'),
    WK('ex-62a', 'Worked example: Example 6.3 (aeroplane)', 134,
       'A plane rises uniformly. After 400 m horizontally its altitude is 300 m. How far has it flown?',
       ['Right triangle: ground 400 m and height 300 m are the legs; the flight path $g$ is the hypotenuse.', '$g^2 = 400^2 + 300^2 = 160\\,000 + 90\\,000 = 250\\,000$.', '$g = 500$ m. (A 3-4-5 triangle × 100.)'],
       '500 m'),
    WK('ex-62b', 'Worked example: Example 6.4 (television)', 134,
       'A 30-inch television (measured on the diagonal) is 18 inches high. How wide is it?',
       ['Diagonal 30 is the hypotenuse; the height 18 is a leg; width $w$ is the other leg.', '$w^2 = 30^2 - 18^2 = 900 - 324 = 576$.', '$w = 24$ inches.'],
       '24 inches'),
    WK('ex-62c', 'Worked example: Review Q3 (Pythagoras + a quadratic)', 151,
       'A rectangle is 7 cm longer than it is wide, and its diagonal is 17 cm. Find its sides.',
       ['Let the width be $x$; length $x + 7$.', '$x^2 + (x + 7)^2 = 17^2 \\Rightarrow 2x^2 + 14x + 49 = 289$.', '$x^2 + 7x - 120 = 0 \\Rightarrow (x + 15)(x - 8) = 0$.', 'Width cannot be negative: $x = 8$, length 15. Check: $64 + 225 = 289$ (correct).'],
       '8 cm by 15 cm'),
    WK('ex-62d', 'Worked example: Review Q4 (window cleaner)', 152,
       'A window is 8 m above the ground and the ladder is 10 m long. (a) How far from the wall must the foot be? (b) Can he reach the window if the foot is 7 m from the wall? (c) If not, how long a ladder is needed?',
       ['(a) $\\sqrt{10^2 - 8^2} = \\sqrt{36} = 6$ m.', '(b) Height reached $= \\sqrt{100 - 49} = \\sqrt{51} \\approx 7.14$ m < 8 m, so no.', '(c) Needed: $\\sqrt{8^2 + 7^2} = \\sqrt{113} \\approx 10.6$ m.'],
       '(a) 6 m (b) no (c) about 10.6 m'),
]

# ------------------------------------------------------------------ lesson 6.3
L3 = [
    T('trigdef-t', '6.3.1 The three trigonometric ratios', 136,
      'In a right triangle, name the sides **relative to the angle you are using**: the **opposite** side faces the angle, the **adjacent** side touches it (and is not the hypotenuse), and the **hypotenuse** faces the right angle.',
      '$$\\sin A = \\frac{\\text{opposite}}{\\text{hypotenuse}}, \\quad \\cos A = \\frac{\\text{adjacent}}{\\text{hypotenuse}}, \\quad \\tan A = \\frac{\\text{opposite}}{\\text{adjacent}}$$',
      'Memory aid: **SOH CAH TOA**.',
      'Example: sides 3, 4, 5 with 3 opposite $A$: $\\sin A = \\frac{3}{5}$, $\\cos A = \\frac{4}{5}$, $\\tan A = \\frac{3}{4}$. For the other acute angle $B$, opposite and adjacent swap: $\\sin B = \\frac{4}{5} = \\cos A$.'),
    ST('sides', 'Opposite and adjacent change with the angle', 136, 'sides',
       [('Using angle $A$: $BC$ is opposite, $AC$ is adjacent.', 'k1'), ('Using angle $B$: $AC$ is opposite, $BC$ is adjacent. The hypotenuse $AB$ never changes.', 'k2')]),
    DG('similar', 'Why a ratio belongs to an angle', 137, 'similar',
       'All the right triangles with the same angle $A$ are similar, so their side ratios are equal. That is why $\\sin A$, $\\cos A$, $\\tan A$ depend only on the size of $A$, not on the size of the triangle.'),
    'math9-u6-c03',
    TB('special-t', 'Exact values (from Grade 8)', 137, ['Angle', 'sin', 'cos', 'tan'],
       [['30°', '$\\frac{1}{2}$', '$\\frac{\\sqrt{3}}{2} \\approx 0.8660$', '$\\frac{\\sqrt{3}}{3} \\approx 0.5774$'],
        ['45°', '$\\frac{\\sqrt{2}}{2} \\approx 0.7071$', '$\\frac{\\sqrt{2}}{2} \\approx 0.7071$', '1'],
        ['60°', '$\\frac{\\sqrt{3}}{2} \\approx 0.8660$', '$\\frac{1}{2}$', '$\\sqrt{3} \\approx 1.7321$']],
       'Notice $\\sin 30° = \\cos 60°$ and $\\sin 60° = \\cos 30°$: in general $\\sin x = \\cos(90° - x)$.'),
    T('=math9-u6-c04', 'Using the table of trigonometric ratios', 138,
      'The table at the end of the chapter gives sin, cos and tan of every whole-degree angle from 0° to 90°, to 4 decimal places.',
      '- **Angle → ratio:** find the angle in the Angle column, move right to the sin / cos / tan column: $\\sin 12° = 0.2079$, $\\cos 45° = 0.7071$, $\\tan 70° = 2.7475$.',
      '- **Ratio → angle:** look for the value inside the correct column, move left to the Angle column: $\\tan x = 28.6363 \\Rightarrow x = 88°$; $\\cos y = 0.8090 \\Rightarrow y = 36°$; $\\sin z = 0.7660 \\Rightarrow z = 50°$. (The textbook writes "sin y = 0.7660"; it must be $\\sin z$.)',
      'Patterns: as the angle grows from 0° to 90°, **sin grows** (0 → 1), **cos shrinks** (1 → 0), **tan grows without limit**. If the value is not in the table, take the nearest entry.'),
    DG('trigtable', 'Reading sin 12°', 138, 'trigtable'),
    TB('which-t', 'Which ratio do I use?', 139, ['You know / want', 'Use', 'Rearranged'],
       [['hypotenuse and opposite', 'sin', 'opp = hyp × sin A'], ['hypotenuse and adjacent', 'cos', 'adj = hyp × cos A'],
        ['opposite and adjacent', 'tan', 'opp = adj × tan A'], ['unknown in the denominator', 'any', 'hyp = opp ÷ sin A, adj = opp ÷ tan A']],
       'Step 1: mark the angle. Step 2: label the two sides you know or want. Step 3: pick the ratio that contains exactly those two.'),
    WK('ex-63a', 'Worked example: Example 6.7 (ladder)', 139,
       'An 8 m ladder leans against a wall, making 60° with the ground. How high up the wall does it reach?',
       ['Hypotenuse = 8 m (the ladder); want the side opposite 60° (the height $f$).', 'Opposite & hypotenuse → sin: $\\sin 60° = \\frac{f}{8}$.', '$f = 8 \\times 0.8660 = 6.928 \\approx 6.9$ m.'],
       'about 6.9 m'),
    WK('ex-63b', 'Worked example: Exercise 6.3 Q4 (rectangle)', 141,
       'The diagonal of a rectangle makes 39° with the longer side, which is 30 cm. Find the width.',
       ['The width is opposite 39°; the 30 cm side is adjacent.', 'tan: $\\tan 39° = \\frac{w}{30}$.', '$w = 30 \\times 0.8098 \\approx 24.3$ cm.'],
       'about 24.3 cm'),
    T('=math9-u6-c05', '6.3.2 Angles of elevation and depression', 141,
      'The **angle of elevation** is the angle **up** from the horizontal to an object above the eye. The **angle of depression** is the angle **down** from the horizontal to an object below the eye.',
      'Both are measured from the **horizontal**, never from the vertical.',
      'Because the two horizontals are parallel, the angle of depression from A to B equals the angle of elevation from B to A (alternate angles).',
      'If the observer\'s eyes are above the ground, **add the eye height** at the end.'),
    DG('elevdep', 'Elevation vs depression', 142, 'elevdep'),
    WK('ex-63c', 'Worked example: Example 6.8 (flagpole rope)', 142,
       'A rope is fixed to the ground 8 m from a flagpole and makes an angle of elevation of 60° with the ground. Find the rope length.',
       ['8 m is adjacent to 60°; the rope $b$ is the hypotenuse.', 'cos: $\\cos 60° = \\frac{8}{b}$.', 'Unknown in the denominator: $b = \\frac{8}{\\cos 60°} = \\frac{8}{0.5} = 16$ m.'],
       '16 m'),
    WK('ex-63d', 'Worked example: Exercise 6.4 Q5 (eye height)', 145,
       'Jemila stands 14 m from a flagpole; the angle of elevation of the top is 27°. Her eyes are 1.4 m above the ground. Find the height of the flagpole.',
       ['The right triangle starts at eye level: adjacent 14 m, opposite = height above her eyes $h$.', '$h = 14 \\tan 27° = 14 \\times 0.5095 \\approx 7.13$ m.', 'Add the eye height: $7.13 + 1.4 \\approx 8.5$ m.'],
       'about 8.5 m'),
    T('=math9-u6-c06', '6.3.3 The law of sines', 146,
      'For a triangle that is **not** right-angled, use the standard labels: side $a$ is opposite angle $A$, $b$ opposite $B$, $c$ opposite $C$.',
      '**Law of sines:** $$\\frac{\\sin A}{a} = \\frac{\\sin B}{b} = \\frac{\\sin C}{c}$$',
      '**Use it when you know a side and its opposite angle** plus one more side or angle (e.g. two angles and one side).',
      'Tip: if you know two angles, the third is $180°$ minus their sum — find it first.'),
    DG('labels', 'Matching sides and angles', 146, 'labels'),
    WK('ex-63e', 'Worked example: Example 6.9', 147,
       'In triangle $ABC$, $a = 7$, $B = 45°$, $C = 75°$. Find $b$ and $c$.',
       ['$A = 180° - 45° - 75° = 60°$.', '$\\frac{\\sin 60°}{7} = \\frac{\\sin 45°}{b} \\Rightarrow b = \\frac{7 \\times 0.7071}{0.8660} \\approx 5.7$.', '$c = \\frac{7 \\sin 75°}{\\sin 60°} = \\frac{7 \\times 0.9659}{0.8660} \\approx 7.8$. (The textbook\'s last line writes "b ≈ 7.8"; it is $c$.)'],
       '$b \\approx 5.7$, $c \\approx 7.8$'),
    T('=math9-u6-c07', '6.3.4 The law of cosines', 149,
      '**Law of cosines:** $$a^2 = b^2 + c^2 - 2bc \\cos A$$ and similarly $b^2 = a^2 + c^2 - 2ac\\cos B$, $c^2 = a^2 + b^2 - 2ab\\cos C$.',
      '**Use it when you know two sides and the angle between them** (to find the third side), or **all three sides** (to find an angle): $$\\cos A = \\frac{b^2 + c^2 - a^2}{2bc}$$',
      'It is Pythagoras with a correction: if $A = 90°$ then $\\cos A = 0$ and it becomes $a^2 = b^2 + c^2$.'),
    TB('laws-t', 'Choosing the right tool', 150, ['What you know', 'Tool'],
       [['right-angled triangle, 2 sides', "Pythagoras"], ['right-angled triangle, side + angle', 'sin / cos / tan'],
        ['two angles + one side', 'law of sines'], ['side + its opposite angle + one more', 'law of sines'],
        ['two sides + the angle between them', 'law of cosines'], ['three sides, want an angle', 'law of cosines']]),
    WK('ex-63f', 'Worked example: Example 6.10', 150,
       'In triangle $ABC$, $a = 7$, $c = 10$, $B = 45°$. Find $b$.',
       ['Two sides and the included angle → law of cosines.', '$b^2 = 7^2 + 10^2 - 2(7)(10)\\cos 45° = 149 - 140 \\times 0.7071 = 149 - 98.99$.', '$b^2 \\approx 50$, so $b \\approx 7.1$.'],
       '$b \\approx 7.1$'),
    WK('ex-63g', 'Worked example: Exercise 6.6 Q4 (two ships)', 151,
       'Two ships leave a harbour at the same time on routes 80° apart, at 34 km/h and 26 km/h. How far apart are they after 3 hours?',
       ['Distances: $34 \\times 3 = 102$ km and $26 \\times 3 = 78$ km, with 80° between them.', '$d^2 = 102^2 + 78^2 - 2(102)(78)\\cos 80° = 10\\,404 + 6\\,084 - 15\\,912 \\times 0.1736$.', '$d^2 \\approx 16\\,488 - 2\\,762 = 13\\,726$, so $d \\approx 117$ km.'],
       'about 117 km', diagram='ships'),
    WK('ex-63h', 'Worked example: Review Q2(d) (angle from three sides)', 151,
       'A triangle has sides $a = 5$, $b = 8$, $c = 7$. Find angle $C$.',
       ['$\\cos C = \\frac{a^2 + b^2 - c^2}{2ab} = \\frac{25 + 64 - 49}{80} = \\frac{40}{80} = 0.5$.', 'From the table, $\\cos 60° = 0.5$, so $C = 60°$.'],
       '$C = 60°$'),
    WK('ex-63i', 'Worked example: Review Q5 (aeroplane and two cars)', 152,
       'A plane flies at 5150 m directly above a straight highway. The angles of depression to two cars on opposite sides are 37° and 53°. How far apart are the cars?',
       ['Angle of depression = angle of elevation at each car (alternate angles).', 'Left car: $x = \\frac{5150}{\\tan 37°} = \\frac{5150}{0.7536} \\approx 6834$ m.', 'Right car: $y = \\frac{5150}{\\tan 53°} = \\frac{5150}{1.3270} \\approx 3881$ m.', 'Distance $= x + y \\approx 10\\,715$ m ≈ 10.7 km.'],
       'about 10.7 km', diagram='planecars'),
    RM('summary-t', 'Unit summary', 152,
       "Right triangle: $c^2 = a^2 + b^2$; SOH CAH TOA.",
       'Any triangle: $\\frac{\\sin A}{a} = \\frac{\\sin B}{b} = \\frac{\\sin C}{c}$; $a^2 = b^2 + c^2 - 2bc\\cos A$.',
       'Elevation = look up, depression = look down, both from the horizontal.'),
]

LESSONS = {'math9-u6-l6-1': L1, 'math9-u6-l6-2': L2, 'math9-u6-l6-3': L3}

# ------------------------------------------------------------------ practice
a = QSet("6.1 Practice — Pythagoras' theorem", 's61')
a.S(132, 'Right-angled or not? (a) 7, 24, 25 (b) 5, 7, 8 (c) 10, 15, 20', '(a) yes (b) no (c) no',
    ['Step 1 (a): $625 = 49 + 576$ (correct).', 'Step 2 (b): $64$ vs $25 + 49 = 74$, not equal.', 'Step 3 (c): $400$ vs $100 + 225 = 325$, not equal.'],
    'Always square the LONGEST side alone.', [('Is 9, 40, 41 right-angled?', 'Yes: $81 + 1600 = 1681 = 41^2$.')])
a.S(132, 'Right-angled or not? (a) 36, 48, 60 (b) 4, 8, $4\\sqrt{3}$', 'both yes',
    ['Step 1 (a): $12 \\times (3, 4, 5)$, or $2304 + 1296 = 3600$.', 'Step 2 (b): longest is 8 ($4\\sqrt{3} \\approx 6.9$): $16 + 48 = 64 = 8^2$.'],
    'Compare surds by squaring: $(4\\sqrt{3})^2 = 48$.', [('Is 6, 8, 10 right-angled?', 'Yes.')])
a.S(132, 'The legs of a right triangle are 9 cm and 12 cm. Find the hypotenuse.', '15 cm',
    ['Step 1: $c^2 = 81 + 144 = 225$.', 'Step 2: $c = 15$ cm.'],
    'Hypotenuse → add the squares.', [('Legs 8 and 15?', '17.')])
a.S(132, 'The hypotenuse is 26 cm and one leg 10 cm. Find the other leg.', '24 cm',
    ['Step 1: $b^2 = 676 - 100 = 576$.', 'Step 2: $b = 24$ cm.'],
    'Leg → subtract the squares.', [('Hypotenuse 17, leg 8?', '15.')])
a.S(132, 'Legs 2 and 3. Find the hypotenuse exactly and to 2 d.p.', '$\\sqrt{13} \\approx 3.61$',
    ['Step 1: $c^2 = 4 + 9 = 13$.', 'Step 2: $c = \\sqrt{13} \\approx 3.61$.'],
    'Leave a surd if the question says "exact".', [('Legs 1 and 2?', '$\\sqrt{5} \\approx 2.24$.')])
a.M(131, 'In triangle $PQR$ the right angle is at $Q$. The hypotenuse is', ['$PQ$', '$QR$', '$PR$', 'cannot tell'], 'C',
    ['Step 1: the hypotenuse is opposite the right angle.', 'Step 2: the side not touching $Q$ is $PR$.'],
    'Hypotenuse = the side that does not touch the right-angle vertex.', [('Right angle at $Y$ in $XYZ$?', '$XZ$.')])
a.TF(132, 'A triangle with sides $\\frac{5}{3}, \\frac{8}{3}, \\frac{10}{3}$ is right-angled.', False,
     ['Step 1: multiply by 3: 5, 8, 10 (same shape).', 'Step 2: $25 + 64 = 89 \\ne 100$.'],
     'Scaling all sides does not change the answer — clear the fractions.', [('Is 1.5, 2, 2.5 right-angled?', 'Yes (× 2 gives 3, 4, 5).')])
a.S(133, 'A parallelogram has sides 9 cm and 12 cm and a diagonal of 16 cm. Is it a rectangle?', 'No',
    ['Step 1: $81 + 144 = 225$.', 'Step 2: $16^2 = 256 \\ne 225$, so the angle is not $90°$.'],
    'Rectangle ⇔ the diagonal is the hypotenuse of a side-side right triangle.', [('Sides 5, 12, diagonal 13?', 'Yes, a rectangle.')])
a.S(132, 'An isosceles right triangle has legs of 5 cm. Find the hypotenuse.', '$5\\sqrt{2} \\approx 7.07$ cm',
    ['Step 1: $c^2 = 25 + 25 = 50$.', 'Step 2: $c = \\sqrt{50} = 5\\sqrt{2}$.'],
    'Hypotenuse = leg × $\\sqrt{2}$ for a 45-45-90 triangle.', [('Legs 3?', '$3\\sqrt{2} \\approx 4.24$.')])
a.S(151, 'Review Q1: right-angled or not? (a) 10, 24, 27 (b) 0.75, 1, 1.25 (c) 20, 24, 31', '(a) no (b) yes (c) no',
    ['Step 1 (a): $676 \\ne 729$.', 'Step 2 (b): $0.5625 + 1 = 1.5625 = 1.25^2$.', 'Step 3 (c): $400 + 576 = 976 \\ne 961$.'],
    '0.75, 1, 1.25 is $\\frac{1}{4} \\times (3, 4, 5)$.', [('Is 12, 35, 37 right-angled?', 'Yes.')])

b = QSet('6.2 Practice — problems with Pythagoras', 's62')
b.S(135, 'A rectangle has a diagonal of 25 cm and width 15 cm. Find its length.', '20 cm',
    ['Step 1: $l^2 = 625 - 225 = 400$.', 'Step 2: $l = 20$ cm.'],
    'The diagonal is the hypotenuse.', [('Diagonal 13, width 5?', '12.')])
b.S(135, 'A football field is 90 m by 120 m. How far is it corner to opposite corner?', '150 m',
    ['Step 1: $d^2 = 8100 + 14\\,400 = 22\\,500$.', 'Step 2: $d = 150$ m.'],
    'Spot the triple: $30 \\times (3, 4, 5)$.', [('Field 60 m by 80 m?', '100 m.')])
b.S(135, 'A window is 12 m high; the ladder foot is 5 m from the wall. How long is the ladder?', '13 m',
    ['Step 1: $L^2 = 144 + 25 = 169$.', 'Step 2: $L = 13$ m.'],
    'The ladder is the hypotenuse.', [('Window 8 m, foot 6 m?', '10 m.')])
b.S(135, 'An 11 m ladder has its foot 4 m from a wall. How high does it reach?', '$\\sqrt{105} \\approx 10.25$ m',
    ['Step 1: $h^2 = 121 - 16 = 105$.', 'Step 2: $h \\approx 10.25$ m.'],
    'Height is a leg → subtract.', [('13 m ladder, foot 5 m?', '12 m.')])
b.S(135, 'Ghenet rides 9 km south then 12 km east. How far is she from the start?', '15 km',
    ['Step 1: south and east are at right angles, so the legs are 9 and 12.', 'Step 2: $\\sqrt{81 + 144} = 15$ km.'],
    'Compass directions at right angles make a right triangle.', [('6 km north then 8 km west?', '10 km.')])
b.S(151, 'A rectangle\'s length is 2 cm more than its width and its diagonal is 10 cm. Find its sides.', '6 cm and 8 cm',
    ['Step 1: $x^2 + (x + 2)^2 = 100 \\Rightarrow 2x^2 + 4x - 96 = 0$.', 'Step 2: $x^2 + 2x - 48 = 0 \\Rightarrow (x + 8)(x - 6) = 0$.', 'Step 3: $x = 6$, length 8.'],
    'Reject negative lengths.', [('Length 7 more than width, diagonal 13?', '5 and 12.')])
b.S(134, 'A 50-inch television is 30 inches high. How wide is it?', '40 inches',
    ['Step 1: $w^2 = 2500 - 900 = 1600$.', 'Step 2: $w = 40$.'],
    'TV sizes are diagonals.', [('25-inch, 15 high?', '20 inches.')])
b.S(135, 'A square has a diagonal of 10 cm. Find its side and area.', 'side $5\\sqrt{2} \\approx 7.07$ cm, area 50 cm²',
    ['Step 1: $s^2 + s^2 = 100 \\Rightarrow s^2 = 50$.', 'Step 2: area $= s^2 = 50$ cm²; $s \\approx 7.07$ cm.'],
    'You may not need $s$ itself — area is $s^2$.', [('Square side 6: diagonal?', '$6\\sqrt{2} \\approx 8.49$.')])
b.S(135, 'Find the distance between $(1, 2)$ and $(7, 10)$.', '10',
    ['Step 1: horizontal leg $7 - 1 = 6$, vertical leg $10 - 2 = 8$.', 'Step 2: $\\sqrt{36 + 64} = 10$.'],
    'Distance between points is Pythagoras on the grid.', [('$(0, 0)$ to $(5, 12)$?', '13.')])
b.S(152, 'A 5 m ladder must reach a window 4 m high. How far from the wall is the foot?', '3 m',
    ['Step 1: $\\sqrt{25 - 16} = 3$.'], 'Spot 3-4-5.', [('10 m ladder, 6 m high?', '8 m.')])

c = QSet('6.3 Practice — trigonometric ratios and the laws', 's63')
c.S(140, 'A right triangle has sides 3, 4, 5, with 3 opposite $A$. Find $\\sin A$, $\\cos A$, $\\tan A$ and $\\sin B$.', '$\\frac{3}{5}, \\frac{4}{5}, \\frac{3}{4}$; $\\sin B = \\frac{4}{5}$',
    ['Step 1: opp 3, adj 4, hyp 5 for $A$.', 'Step 2: for $B$, opposite is 4.'],
    'Relabel opposite/adjacent for each angle.', [('Sides 5, 12, 13 with 5 opposite $A$?', '$\\sin A = \\frac{5}{13}$, $\\cos A = \\frac{12}{13}$, $\\tan A = \\frac{5}{12}$.')])
c.S(141, 'From the table: $\\sin 18°$, $\\cos 21°$, $\\cos 75°$, $\\tan 58°$, $\\tan 45°$.', '0.3090, 0.9336, 0.2588, 1.6003, 1',
    ['Step 1: find each angle in the Angle column.', 'Step 2: read across to the right column.'],
    'Do not mix up the columns.', [('$\\sin 30°$ and $\\cos 60°$?', 'both 0.5000.')])
c.S(141, 'Find $x$, $y$, $z$: $\\sin x = 0.9703$, $\\cos y = 0.5150$, $\\tan z = 0.2679$.', '76°, 59°, 15°',
    ['Step 1: search the sin column for 0.9703 → 76°.', 'Step 2: cos column 0.5150 → 59°.', 'Step 3: tan column 0.2679 → 15°.'],
    'Ratio → angle: read the table backwards.', [('$\\tan x = 1$?', '45°.')])
c.S(141, 'Find $w$ if $\\sin w = \\cos w$ (acute).', '45°',
    ['Step 1: divide by $\\cos w$: $\\tan w = 1$.', 'Step 2: $w = 45°$.'],
    '$\\sin x = \\cos(90° - x)$, so equal when $x = 90° - x$.', [('$\\sin 30° = \\cos\\,?$', '60°.')])
c.M(136, '$\\tan A = $', ['$\\frac{\\text{opp}}{\\text{hyp}}$', '$\\frac{\\text{adj}}{\\text{hyp}}$', '$\\frac{\\text{opp}}{\\text{adj}}$', '$\\frac{\\text{adj}}{\\text{opp}}$'], 'C',
    ['Step 1: TOA: Tan = Opposite / Adjacent.'], 'SOH CAH TOA.', [('$\\sin A$?', 'opposite / hypotenuse.')])
c.S(141, 'A hill slopes at 12°. How much does a person rise walking 90 m up the hill?', 'about 18.7 m',
    ['Step 1: 90 m is the hypotenuse; rise is opposite 12°.', 'Step 2: $90 \\sin 12° = 90 \\times 0.2079 \\approx 18.7$ m.'],
    'Distance along a slope = hypotenuse.', [('200 m up an 8° road ($\\sin 8° = 0.1392$)?', 'about 27.8 m.')])
c.S(143, 'Tekle stands 10 m from a tree; the angle of elevation of the top is 33°. How tall is the tree?', 'about 6.5 m',
    ['Step 1: adjacent 10, want opposite → tan.', 'Step 2: $10 \\times 0.6494 \\approx 6.5$ m.'],
    'Ground distance = adjacent.', [('20 m away, 40° ($\\tan 40° = 0.8391$)?', 'about 16.8 m.')])
c.S(144, 'A building is 50 m high; the angle of elevation from a point on the ground is 41°. How far is the point from the building?', 'about 57.5 m',
    ['Step 1: $\\tan 41° = \\frac{50}{d}$.', 'Step 2: $d = \\frac{50}{0.8693} \\approx 57.5$ m.'],
    'Unknown in the denominator → divide.', [('Tower 30 m, elevation 60°?', '$30 \\div 1.7321 \\approx 17.3$ m.')])
c.S(144, 'A plane is 2 km high and 5 km (along the ground) from the airport. Find the angle of depression to the airport.', 'about 22°',
    ['Step 1: $\\tan D = \\frac{2}{5} = 0.4$.', 'Step 2: nearest table value $\\tan 22° = 0.4040$, so $D \\approx 22°$.'],
    'Depression angle = elevation angle from the airport.', [('Height 3 km, ground 3 km?', '45°.')])
c.S(144, 'A bird on a lamppost sees an observer\'s feet at a depression of 35°; the bird–observer distance is 25 m. How high is the lamppost?', 'about 14.3 m',
    ['Step 1: elevation from the feet is 35°; 25 m is the hypotenuse.', 'Step 2: $h = 25 \\sin 35° = 25 \\times 0.5736 \\approx 14.3$ m.'],
    'Line of sight = hypotenuse.', [('Kite string 50 m at 30°: height?', '25 m.')])
c.S(145, 'Jemila (eyes 1.4 m high) is 14 m from a flagpole; elevation 27°. Find the flagpole height.', 'about 8.5 m',
    ['Step 1: $14 \\tan 27° = 14 \\times 0.5095 \\approx 7.13$ m.', 'Step 2: add 1.4: about 8.5 m.'],
    'Remember the eye height.', [('20 m away, 30°, eyes 1.5 m?', 'about 13.05 m.')])
c.S(148, 'Triangle $ABC$: $A = 71°$, $B = 39°$, $a = 14$. Find $b$.', 'about 9.3',
    ['Step 1: $\\frac{\\sin 71°}{14} = \\frac{\\sin 39°}{b}$.', 'Step 2: $b = \\frac{14 \\times 0.6293}{0.9455} \\approx 9.32$.'],
    'A side and its opposite angle → law of sines.', [('$A = 30°$, $B = 45°$, $a = 10$: $b$?', '$\\approx 14.1$.')])
c.S(148, 'Triangle $ABC$: $A = 73°$, $B = 28°$, $c = 14$. Find $b$.', 'about 6.7',
    ['Step 1: $C = 180° - 73° - 28° = 79°$.', 'Step 2: $b = \\frac{14 \\sin 28°}{\\sin 79°} = \\frac{14 \\times 0.4695}{0.9816} \\approx 6.70$.'],
    'Find the third angle so you have a full pair.', [('$A = 50°$, $B = 60°$, $c = 10$: $b$?', '$C = 70°$, $b \\approx 9.22$.')])
c.S(151, 'Triangle $ABC$: $A = 60°$, $b = 8$ cm, $c = 10$ cm. Find $a$.', 'about 9.17 cm',
    ['Step 1: $a^2 = 64 + 100 - 160 \\cos 60° = 164 - 80 = 84$.', 'Step 2: $a = \\sqrt{84} \\approx 9.17$ cm.'],
    'Two sides + included angle → law of cosines.', [('$C = 60°$, $a = b = 5$: $c$?', '5 (equilateral).')])
c.S(151, 'Triangle $PQR$: $R = 14°$, $p = 5$ cm, $q = 10$ cm. Find $r$.', 'about 5.29 cm',
    ['Step 1: $r^2 = 25 + 100 - 100 \\cos 14° = 125 - 97.03 = 27.97$.', 'Step 2: $r \\approx 5.29$ cm.'],
    'Same pattern for any letters.', [('Ships 30 km and 40 km apart at 60°: distance?', '$\\sqrt{1300} \\approx 36.1$ km.')])
c.S(151, 'Review Q2(b): $A = 24°$, $C = 90°$, $a = 8$. Find $B$, $b$, $c$.', '$B = 66°$, $b \\approx 18.0$, $c \\approx 19.7$',
    ['Step 1: $B = 90° - 24° = 66°$.', 'Step 2: $c = \\frac{8}{\\sin 24°} = \\frac{8}{0.4067} \\approx 19.7$.', 'Step 3: $b = \\frac{8}{\\tan 24°} = \\frac{8}{0.4452} \\approx 18.0$. Check: $64 + 324 \\approx 388 \\approx 19.7^2$.'],
    'Right triangle → SOH CAH TOA is quicker than the laws.', [('$C = 90°$, $a = 12$, $b = 5$: $c$?', '13.')])
c.S(151, 'Review Q2(a): $B = 12°$, $C = 80°$, $b = 13$. Find $A$, $a$, $c$.', '$A = 88°$, $a \\approx 62.5$, $c \\approx 61.6$',
    ['Step 1: $A = 88°$.', 'Step 2: $a = \\frac{13 \\sin 88°}{\\sin 12°} = \\frac{13 \\times 0.9994}{0.2079} \\approx 62.5$.', 'Step 3: $c = \\frac{13 \\times 0.9848}{0.2079} \\approx 61.6$.'],
    'The largest side faces the largest angle — use this to check.', [('$A = 30°$, $B = 60°$, $c = 10$: $a$?', '5.')])
c.S(151, 'Sides 7, 5, 8: find the angle opposite the side 7.', '60°',
    ['Step 1: $\\cos = \\frac{5^2 + 8^2 - 7^2}{2 \\times 5 \\times 8} = \\frac{40}{80} = 0.5$.', 'Step 2: angle $= 60°$.'],
    'Three sides → law of cosines rearranged.', [('Review Q2(e): sides 8, 6, 10, angle opposite 10?', '90° ($\\cos = 0$).')])
c.S(152, 'A plane at 1000 m sees two cars on opposite sides at depressions of 45° each. How far apart are the cars?', '2000 m',
    ['Step 1: $\\tan 45° = 1$, so each car is 1000 m horizontally from the point below the plane.', 'Step 2: total 2000 m.'],
    'Split into two right triangles and add.', [('Same plane, depressions 45° and 60°?', '$1000 + 577 \\approx 1577$ m.')])
c.TF(146, 'The law of sines can only be used in right-angled triangles.', False,
     ['Step 1: it is stated "for any triangle ABC".', 'Step 2: it is mostly used when there is **no** right angle.'],
     'Right triangle → SOH CAH TOA; other triangles → laws.', [('If $C = 90°$, the law of cosines becomes…?', "Pythagoras' theorem.")])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Hypotenuse', 'The side opposite the right angle; the longest side.', 130),
    ('Legs', 'The two sides that form the right angle.', 130),
    ('Opposite side', 'The side facing the angle being used.', 136),
    ('Adjacent side', 'The side next to the angle that is not the hypotenuse.', 136),
    ('Angle of elevation', 'Angle up from the horizontal to an object above the eye.', 142),
    ('Angle of depression', 'Angle down from the horizontal to an object below the eye.', 142),
    ('Law of sines', '$\\frac{\\sin A}{a} = \\frac{\\sin B}{b} = \\frac{\\sin C}{c}$ for any triangle.', 146),
    ('Law of cosines', '$a^2 = b^2 + c^2 - 2bc\\cos A$ for any triangle.', 149),
]
TIPS = [
    ('Hypotenuse → add the squares; leg → subtract the squares.', 131),
    ('SOH CAH TOA — label opposite/adjacent from the angle you are using.', 136),
    ('Two sides + included angle, or three sides → law of cosines; otherwise law of sines.', 150),
]
IDEAS = [('triples', 'Pythagorean triples', 'l6_1', 'math9-u6-md-triples-t'), ('which', 'Which ratio?', 'l6_3', 'math9-u6-md-which-t'),
         ('laws', 'Choosing the right tool', 'l6_3', 'math9-u6-md-laws-t')]

# narrow phones: the textbook key table reads better as one card per row
PATCH = {'math9-u6-tbl1': {'layout': 'cards', '_inline': True}}
