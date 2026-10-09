r"""Grade 9 Unit 4 — Quadratic Functions (pp. 82-102)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet, plane
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side, with_legend

UID = 'math9-u4'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_parab():
    p = Plot(-4, 4, -1, 10, unit=34, uy=22, every=1, yevery=2, gstep=1)
    p.g('k2 k3').fn(lambda x: x * x, -3.15, 3.15, BLUE, 2.8).end()
    for x in range(-3, 4):
        p.pt(x, x * x, None, c=RED, r=4.4)
    p.g('k1').text(p.X(-3), p.Y(9) - 12, '(−3, 9)', 12, RED).text(p.X(3), p.Y(9) - 12, '(3, 9)', 12, RED).end()
    p.g('k3').seg((0, -0.8), (0, 9.8), PURPLE, 2, dash='6 4').text(p.X(0) + 6, p.Y(8.6), 'axis x = 0', 12, PURPLE, 'start')
    p.text(p.X(0) + 10, p.Y(0) + 16, 'vertex (0, 0)', 12, GREEN, 'start').end()
    return p


def f_x2p4x():
    p = Plot(-7, 3, -5, 13, unit=28, uy=13, every=1, yevery=2)
    p.fn(lambda x: x * x + 4 * x, -6, 2, BLUE, 2.8)
    for x in range(-6, 3):
        p.pt(x, x * x + 4 * x, None, c=RED, r=3.6)
    p.pt(-2, -4, 'vertex (−2, −4)', 's', c=GREEN, r=4.5)
    p.seg((2.6, -4), (2.6, 12), ORANGE, 3)
    p.text(p.X(2.6) - 6, p.Y(4), 'range', 12, ORANGE, 'end')
    p.text(p.X(-6), p.Y(12) - 8, '(−6, 12)', 11.5, RED).text(p.X(2) - 6, p.Y(12) - 8, '(2, 12)', 11.5, RED, 'end')
    return p


def f_afamily():
    a = Plot(-3, 3, -1, 9, unit=22, uy=16, every=1, yevery=2, labels=True)
    a.fn(lambda x: 2 * x * x, -2.12, 2.12, RED, 2.6).fn(lambda x: x * x, -3, 3, BLUE, 2.6).fn(lambda x: x * x / 2, -3, 3, GREEN, 2.6)
    b = Plot(-3, 3, -9, 1, unit=22, uy=16, every=1, yevery=2, labels=True)
    b.fn(lambda x: -2 * x * x, -2.12, 2.12, RED, 2.6).fn(lambda x: -x * x, -3, 3, BLUE, 2.6).fn(lambda x: -x * x / 2, -3, 3, GREEN, 2.6)
    a = with_legend(a, [('2x²', RED), ('x²', BLUE), ('½x²', GREEN)])
    b = with_legend(b, [('−2x²', RED), ('−x²', BLUE), ('−½x²', GREEN)])
    return side_by_side([a, b], 8, ['a > 0: opens up', 'a < 0: opens down'])


def f_shiftc():
    p = Plot(-4, 4, -3, 10, unit=34, uy=18, every=1, yevery=2)
    p.fn(lambda x: x * x + 1, -3, 3, GREEN, 2.6).fn(lambda x: x * x, -3.16, 3.16, BLUE, 2.6).fn(lambda x: x * x - 2, -3.4, 3.4, RED, 2.6)
    p.pt(0, 1, '(0, 1)', 'nw', GREEN).pt(0, 0, None, BLUE).pt(0, -2, '(0, −2)', 'e', RED)
    return with_legend(p, [('y = x² + 1', GREEN), ('y = x²', BLUE), ('y = x² − 2', RED)])


def f_roots():
    p = Plot(-5, 1, -1, 7, unit=34, uy=24, every=1, yevery=1)
    p.fn(lambda x: x * x + 5 * x + 6, -4.75, 0.2, BLUE, 2.8)
    p.pt(-3, 0, None, RED, r=5).pt(-2, 0, None, RED, r=5).pt(0, 6, '(0, 6)', 'e', GREEN)
    p.text(p.X(-3) - 4, p.Y(0) - 10, 'x = −3', 12, RED, 'end').text(p.X(-2) + 4, p.Y(0) - 10, 'x = −2', 12, RED, 'start')
    p.text(p.X(-2.5), p.Y(5.4), 'y = x² + 5x + 6', 12.5, BLUE)
    return p


def f_complsq():
    f = Fig(330, 205)
    s, b = 110, 42
    x0, y0 = 40, 30
    f.g('k1 k2 k3').rect(x0, y0, s, s, BLUE, 2, FILL[BLUE]).text(x0 + s / 2, y0 + s / 2 + 5, 'x²', 15, BLUE).end()
    f.g('k1 k2 k3').rect(x0 + s, y0, b, s, GREEN, 2, FILL[GREEN]).text(x0 + s + b / 2, y0 + s / 2 + 5, '3x', 13, GREEN)
    f.rect(x0, y0 + s, s, b, GREEN, 2, FILL[GREEN]).text(x0 + s / 2, y0 + s + b / 2 + 5, '3x', 13, GREEN).end()
    f.g('k2 k3', 'k2').rect(x0 + s, y0 + s, b, b, ORANGE, 2.4, FILL[ORANGE]).text(x0 + s + b / 2, y0 + s + b / 2 + 5, '9', 14, ORANGE).end()
    f.g('k1', 'k1').rect(x0 + s, y0 + s, b, b, ORANGE, 2, 'none', dash=True).text(x0 + s + b / 2, y0 + s + b / 2 + 5, '?', 14, ORANGE).end()
    f.text(x0 + s / 2, y0 - 8, 'x', 13, INK).text(x0 + s + b / 2, y0 - 8, '3', 13, INK)
    f.text(x0 - 10, y0 + s / 2 + 4, 'x', 13, INK, 'end').text(x0 - 10, y0 + s + b / 2 + 4, '3', 13, INK, 'end')
    f.g('k1').text(264, 70, 'x² + 6x', 14, INK).text(264, 92, 'is not a square', 12, GREY).end()
    f.g('k2').text(264, 70, 'add (6 ÷ 2)² = 9', 14, ORANGE).end()
    f.g('k3').text(264, 70, 'x² + 6x + 9', 14, INK).text(264, 92, '= (x + 3)²', 14, GREEN).end()
    return f


def f_rocket():
    p = Plot(0, 10.5, 0, 270, unit=25, uy=0.62, pad=30, every=1, yevery=50, grid=False, xlab='t', ylab='h')
    p.fn(lambda t: -10 * t * t + 100 * t, 0, 10, BLUE, 2.8)
    for t, pos in ((2, 'nw'), (5, 'n'), (6, 'ne')):
        p.pt(t, -10 * t * t + 100 * t, f'({t}, {-10 * t * t + 100 * t})', pos, RED)
    return p


DIAGRAMS = {
    'parab': (f_parab(), 'Drawing y = x² from a table (Fig. 4.3 and 4.4)', 86),
    'x2p4x': (f_x2p4x(), 'y = x² + 4x for −6 ≤ x ≤ 2 (Fig. 4.5)', 87),
    'afamily': (f_afamily(), 'The effect of a in y = ax² (Fig. 4.6 and 4.7)', 89),
    'shiftc': (f_shiftc(), 'The effect of c in y = x² + c (Fig. 4.8)', 91),
    'roots': (f_roots(), 'Roots are the x-intercepts', 96),
    'complsq': (f_complsq(), 'Completing the square with areas', 100),
    'rocket': (f_rocket(), 'Height of a rocket, h = −10t² + 100t', 84),
}

# ------------------------------------------------------------------ lesson 4.1
L1 = [
    T('qexpr-t', 'Quadratic expressions in real situations', 83,
      'A **quadratic expression** is one that can be written $ax^2 + bx + c$ with $a \\ne 0$. If $a = 0$ the $x^2$ term disappears and we are left with $bx + c$, which is linear — that is why $a \\ne 0$.',
      'They appear whenever two lengths that both depend on $x$ are **multiplied**:',
      '- Isosceles right triangle with legs $x$: area $= \\frac{1}{2}x \\cdot x = \\frac{1}{2}x^2$.',
      '- Rectangle of width $x$ and length $x + 5$: area $= x(x + 5) = x^2 + 5x$.',
      '- Two consecutive integers $n$ and $n + 1$: product $n^2 + n$.',
      '- Falling objects: distance $S = 5t^2$ metres after $t$ seconds.'),
    WK('ex-41a', 'Worked example: Example 4.1 and the falling orange', 84,
       '(a) Write "the square of a number plus 4 times the number minus 7". (b) An orange falls for half a second ($S = 5t^2$). How high was it? (c) How long does an object take to fall 80 m?',
       ['(a) Number $n$: $n^2 + 4n - 7$.', '(b) $S = 5(0.5)^2 = 5 \\times 0.25 = 1.25$ m.', '(c) $80 = 5t^2 \\Rightarrow t^2 = 16 \\Rightarrow t = 4$ s (time cannot be negative).'],
       '(a) $n^2 + 4n - 7$ (b) 1.25 m (c) 4 s'),
    DG('rocket', 'A rocket\'s height is a quadratic function of time', 84, 'rocket',
       '$h = -10t^2 + 100t$: $h(2) = -40 + 200 = 160$ m, $h(5) = 250$ m (the highest point), $h(6) = 240$ m. The rocket rises, turns at the top, and falls back — the typical shape when $a < 0$. (The textbook\'s "initial velocity 96 m/s" does not match this formula, which corresponds to 100 m/s; use the formula.)'),
]

# ------------------------------------------------------------------ lesson 4.2
L2 = [
    T('=math9-u4-c02', '4.2 Graphing y = ax² + bx + c from a table', 85,
      'A quadratic is not linear, so two points are **not** enough. Make a table of values (usually 7 or more $x$-values), plot the points, and join them with a **smooth curve** — never with straight segments. The curve is called a **parabola**.',
      'Every parabola has a **vertex** (turning point) and is symmetric about a vertical line through the vertex, the **axis of symmetry**. Use the symmetry: equal $y$-values appear at equal distances on both sides of the axis.',
      'The **range** is read from the lowest (or highest) point of the graph.'),
    ST('parab', 'Example 4.2: y = x²', 86, 'parab',
       [('Table: $x = -3, -2, -1, 0, 1, 2, 3$ gives $y = 9, 4, 1, 0, 1, 4, 9$. Plot the seven points.', 'k1'),
        ('Join them with a smooth U-shaped curve and continue it beyond the last points.', 'k2'),
        ('Vertex $(0, 0)$ is the lowest point; the axis of symmetry is $x = 0$ (the $y$-axis). Range: $y \\ge 0$.', 'k3')]),
    DG('x2p4x', 'Example 4.3', 87, 'x2p4x',
       'Table: $x = -6, -5, \\dots, 2$ gives $y = 12, 5, 0, -3, -4, -3, 0, 5, 12$. The lowest point is $(-2, -4)$ and the largest value on this domain is 12, so the range is $-4 \\le y \\le 12$.'),
    'math9-u4-st2',
    TB('lq-t', 'Linear vs quadratic graphs', 85, ['', 'Linear $y = mx + b$', 'Quadratic $y = ax^2 + bx + c$'],
       [['Shape', 'straight line', 'parabola (U or upside-down U)'], ['Points needed', '2 (plus 1 to check)', 'a table of 5–7 or more'],
        ['Turning point', 'none', 'one vertex'], ['Symmetry', 'none needed', 'symmetric about $x = -\\frac{b}{2a}$'],
        ['Range (all real $x$)', 'all real numbers (if $m \\ne 0$)', '$y \\ge$ vertex value ($a > 0$) or $y \\le$ vertex value ($a < 0$)']],
       'Spot a quadratic in a table: equal steps in $x$ give **constant second differences** in $y$.'),
]

# ------------------------------------------------------------------ lesson 4.3
L3 = [
    'math9-u4-c03',
    DG('afamily', 'Changing a', 89, 'afamily',
       'Example 4.4 and 4.5: the bigger $|a|$, the narrower the parabola. A negative $a$ flips it upside down: $y = -x^2$ is $y = x^2$ reflected in the $x$-axis. All six graphs have vertex $(0, 0)$.'),
    DG('shiftc', 'Changing c', 91, 'shiftc',
       'Example 4.6: adding $c$ moves every point up $c$ units (down if $c < 0$). The vertex becomes $(0, c)$ and the range becomes $y \\ge c$.'),
    TB('param-t', 'Effects of a and c in y = ax² + c', 91, ['Change', 'Effect on the graph', 'Vertex', 'Range'],
       [['$a > 0$', 'opens upward (minimum)', '$(0, c)$', '$y \\ge c$'],
        ['$a < 0$', 'opens downward (maximum)', '$(0, c)$', '$y \\le c$'],
        ['$|a| > 1$', 'narrower than $y = x^2$', 'unchanged', 'unchanged'],
        ['$0 < |a| < 1$', 'wider than $y = x^2$', 'unchanged', 'unchanged'],
        ['$c > 0$', 'moves up $c$ units', '$(0, c)$', 'starts at $c$'],
        ['$c < 0$', 'moves down $|c|$ units', '$(0, c)$', 'starts at $c$']],
       '$a$ changes the **shape**; $c$ changes the **position**.'),
    WK('ex-43a', 'Worked example: describe without drawing', 92,
       'Compare $y = 2x^2 + 2$ and $y = -2(x^2 + 2)$.',
       ['$y = 2x^2 + 2$: opens up, narrower than $x^2$, vertex $(0, 2)$, range $y \\ge 2$.', '$y = -2(x^2 + 2) = -2x^2 - 4$: opens down, same width, vertex $(0, -4)$, range $y \\le -4$.', 'The second is NOT just the first flipped: flipping $y = 2x^2 + 2$ in the $x$-axis gives $-2x^2 - 2$, vertex $(0, -2)$.'],
       'vertices $(0, 2)$ and $(0, -4)$; ranges $y \\ge 2$ and $y \\le -4$'),
]

# ------------------------------------------------------------------ lesson 4.4
L4 = [
    T('=math9-u4-c05', '4.4.1 Solving by factorisation', 92,
      'A **quadratic equation** can be written $ax^2 + bx + c = 0$, $a \\ne 0$. Its solutions (roots) are the $x$-intercepts of $y = ax^2 + bx + c$.',
      '**Product property of zero:** if $pq = 0$ then $p = 0$ or $q = 0$. So once the left side is factorised, set each factor equal to 0.',
      '**Never divide by $x$!** Beshir solved $x^2 + 4x = 0$ by dividing by $x$ and found only $x = -4$; he lost $x = 0$, because dividing by $x$ is not allowed when $x$ could be 0. Yohana factorised: $x(x + 4) = 0$, so $x = 0$ or $x = -4$.',
      'Take out the **greatest** common factor: $4x^2 - 6x = 2x(2x - 3)$ (not $2(2x^2 - 3x)$ or $x(4x - 6)$).'),
    DG('roots', 'Solutions on the graph', 96, 'roots', '$x^2 + 5x + 6 = (x + 2)(x + 3) = 0$ gives $x = -2$ or $x = -3$ — exactly where the parabola crosses the $x$-axis.'),
    TB('fact-t', 'Which factorisation?', 95, ['Form', 'Method', 'Example'],
       [['$ax^2 + bx = 0$', 'common factor $x$', '$3x^2 - 12x = 3x(x - 4) = 0 \\Rightarrow x = 0, 4$'],
        ['$x^2 - k^2 = 0$', 'difference of two squares', '$x^2 - 16 = (x + 4)(x - 4) = 0 \\Rightarrow x = \\pm 4$'],
        ['$x^2 \\pm 2kx + k^2 = 0$', 'perfect square', '$x^2 - 6x + 9 = (x - 3)^2 = 0 \\Rightarrow x = 3$ (one root)'],
        ['$ax^2 + bx + c = 0$', 'split $b$ into $p + q$ with $pq = ac$', '$x^2 + 5x + 6$: $2 + 3 = 5$, $2 \\times 3 = 6$']],
       'Always move every term to one side first so that the right side is **0**.'),
    T('split-t', 'Splitting the middle term', 96,
      'For $ax^2 + bx + c = 0$: find $p, q$ with $p + q = b$ and $pq = ac$, write $bx = px + qx$, group in pairs and take out the common bracket.',
      'Example: $3x^2 + 8x + 5 = 0$. $ac = 15$; $3 + 5 = 8$ and $3 \\times 5 = 15$. $3x^2 + 3x + 5x + 5 = 3x(x + 1) + 5(x + 1) = (x + 1)(3x + 5) = 0$, so $x = -1$ or $x = -\\frac{5}{3}$.'),
    WK('ex-44a', 'Worked example: Example 4.10', 97,
       'The sum of the squares of two positive consecutive integers is 25. Find them.',
       ['Let them be $x$ and $x + 1$: $x^2 + (x + 1)^2 = 25$.', 'Expand: $2x^2 + 2x + 1 = 25 \\Rightarrow x^2 + x - 12 = 0$.', 'Split: $4 \\times (-3) = -12$, $4 + (-3) = 1$: $(x + 4)(x - 3) = 0$.', '$x = 3$ ($x = -4$ is rejected: not positive). Numbers 3 and 4; check $9 + 16 = 25$ (correct).'],
       '3 and 4'),
    T('=math9-u4-c06', '4.4.2 Completing the square', 99,
      'If an equation has the form $(x + p)^2 = k$ with $k \\ge 0$, take square roots: $x + p = \\pm\\sqrt{k}$. ($x^2 = 16$ has **two** answers, $4$ and $-4$, because $\\sqrt{x^2} = |x|$.)',
      'Completing the square turns any $x^2 + bx + c = 0$ into that form:',
      '1. Move $c$ to the right: $x^2 + bx = -c$.',
      '2. Add $\\left(\\frac{b}{2}\\right)^2$ to **both** sides.',
      '3. Write the left side as $\\left(x + \\frac{b}{2}\\right)^2$ and take square roots.',
      'If the right side turns out negative, there is **no real solution** (a square cannot be negative).'),
    ST('complsq', 'Why "completing the square"?', 100, 'complsq',
       [('$x^2 + 6x$ is an $x$-by-$x$ square plus two $3$-by-$x$ strips: one corner is missing.', 'k1'),
        ('The missing corner is $3 \\times 3 = 9 = \\left(\\frac{6}{2}\\right)^2$.', 'k2'),
        ('Adding 9 completes the square: $x^2 + 6x + 9 = (x + 3)^2$.', 'k3')]),
    WK('ex-44b', 'Worked example: Example 4.11', 100,
       'Solve $x^2 + 6x + 8 = 0$ by completing the square.',
       ['Move 8: $x^2 + 6x = -8$.', 'Add $\\left(\\frac{6}{2}\\right)^2 = 9$ to both sides: $x^2 + 6x + 9 = 1$.', '$(x + 3)^2 = 1 \\Rightarrow x + 3 = \\pm 1$.', '$x = -2$ or $x = -4$.'],
       '$\\{-4, -2\\}$'),
    WK('ex-44c', 'Worked example: an answer with roots', 100,
       'Solve $x^2 + 4x - 10 = 0$.',
       ['$x^2 + 4x = 10$.', 'Add 4: $(x + 2)^2 = 14$.', '$x + 2 = \\pm\\sqrt{14}$, so $x = -2 \\pm \\sqrt{14}$.', 'Approximately $x \\approx 1.74$ or $x \\approx -5.74$.'],
       '$x = -2 \\pm \\sqrt{14}$'),
    RM('=math9-u4-c04', 'Choosing a method', 100,
       '- Right side 0 and an easy factorisation → **factorise**.',
       '- No nice factors (answers with roots) → **complete the square**.',
       '- Only $x^2$ and a number ($x^2 = k$ or $(x - p)^2 = k$) → **square root both sides**, remembering $\\pm$.',
       'Check every answer in the original equation, and reject answers that make no sense in a word problem (negative lengths, ages).'),
    WK('ex-44d', 'Worked example: the basketball court (Review 2)', 101,
       'A court\'s length is 2 m less than twice its width and its area is 420 m². Find its dimensions.',
       ['Width $w$, length $2w - 2$: $w(2w - 2) = 420$.', '$2w^2 - 2w - 420 = 0 \\Rightarrow w^2 - w - 210 = 0$.', 'Numbers with product $-210$ and sum $-1$: $-15$ and $14$: $(w - 15)(w + 14) = 0$.', '$w = 15$ (reject $-14$), length $2(15) - 2 = 28$. Check $15 \\times 28 = 420$ (correct).'],
       '15 m by 28 m'),
]

LESSONS = {'math9-u4-l4-1': L1, 'math9-u4-l4-2': L2, 'math9-u4-l4-3': L3, 'math9-u4-l4-4': L4}

# ------------------------------------------------------------------ practice
a = QSet('4.1 Practice — quadratic expressions', 's41')
a.S(84, 'Write a quadratic expression for the area of a rectangle of width $x$ m and length $2x + 2$ m.', '$2x^2 + 2x$',
    ['Step 1: area = length × width = $x(2x + 2)$.', 'Step 2: expand: $2x^2 + 2x$.'],
    'Multiply, then expand.', [('Width $x$, length 5 m more than the width?', '$x^2 + 5x$.')])
a.S(84, 'Write the product of two consecutive odd integers as a quadratic expression.', '$4n^2 - 1$ (or $x^2 + 2x$)',
    ['Step 1: consecutive odd integers differ by 2: call them $x$ and $x + 2$.', 'Step 2: product $x(x + 2) = x^2 + 2x$.', 'Step 3: or with $2n - 1$ and $2n + 1$: $4n^2 - 1$.'],
    'Consecutive odd (or even) numbers are 2 apart.', [('Product of two consecutive even integers?', '$x(x + 2) = x^2 + 2x$ with $x$ even.')])
a.S(84, 'A piece of wood falls from a roof for 3 s ($S = 5t^2$). How high is the roof?', '45 m',
    ['Step 1: $S = 5 \\times 3^2$.', 'Step 2: $5 \\times 9 = 45$ m.'],
    'Square first, then multiply.', [('Falls for 2 s?', '20 m.')])
a.S(85, 'Write the total surface area of a cube with edge $x$.', '$6x^2$',
    ['Step 1: one face is $x \\times x = x^2$.', 'Step 2: a cube has 6 faces: $6x^2$.'],
    'Count faces.', [('Surface area of a box $x$ by $x + 1$ by $x + 3$?', '$2[x(x+1) + x(x+3) + (x+1)(x+3)] = 6x^2 + 16x + 6$.')])
a.M(83, 'Which is a quadratic expression?', ['$3x + 2$', '$x^3 - x$', '$5 - 2x^2$', '$\\frac{1}{x^2}$'], 'C',
    ['Step 1: highest power must be exactly 2 with only whole-number powers.', 'Step 2: $5 - 2x^2 = -2x^2 + 0x + 5$, $a = -2 \\ne 0$.'],
    'Rewrite in the order $x^2$, $x$, number.', [('Is $(x + 1)^2 - x^2$ quadratic?', 'No — it simplifies to $2x + 1$.')])
a.S(101, 'How many games are played if each of $n$ teams plays every other team twice?', '$n^2 - n$',
    ['Step 1: each team plays $n - 1$ others twice, but count each game once from its home side: every ordered pair (home, away) is one game.', 'Step 2: ordered pairs of different teams: $n(n - 1) = n^2 - n$.'],
    'Twice = home and away, so order matters.', [('How many for 16 teams?', '240.')])

b = QSet('4.2 Practice — graphing quadratics', 's42')
b.S(85, 'Complete the table for $y = 2x^2 - 1$ at $x = -3, -1, 1, 2$.', '17, 1, 1, 7',
    ['Step 1: $2(9) - 1 = 17$.', 'Step 2: $2(1) - 1 = 1$ for both $\\pm 1$.', 'Step 3: $2(4) - 1 = 7$.'],
    'Square before multiplying, and $(-3)^2 = +9$.', [('$y = x^2 + x - 6$ at $x = -3$?', '0.')])
b.S(88, 'Find the range of $y = x^2 + 2x$ for $-4 \\le x \\le 2$.', '$-1 \\le y \\le 8$',
    ['Step 1: table: $x = -4 \\to 8$, $-3 \\to 3$, $-2 \\to 0$, $-1 \\to -1$, $0 \\to 0$, $1 \\to 3$, $2 \\to 8$.', 'Step 2: lowest value $-1$ (vertex), highest 8.'],
    'Check both ends of the domain AND the vertex.', [('Range of $y = -x^2 - 2x + 3$ for $-5 \\le x \\le 3$?', '$-12 \\le y \\le 4$.')])
b.M(87, 'The axis of symmetry of $y = x^2 + 4x$ is', ['$x = 4$', '$x = -2$', '$x = 2$', '$y = -4$'], 'B',
    ['Step 1: $x = -\\frac{b}{2a} = -\\frac{4}{2} = -2$.', 'Step 2: the axis is a vertical line: $x = -2$.'],
    'An axis of symmetry is always "$x = $ number".', [('Axis of $y = x^2 - 6x + 1$?', '$x = 3$.')])
b.S(88, 'For $S = 5t^2$ (falling body), what is a sensible domain and what is $S$ at $t = 2.5$ s?', '$t \\ge 0$; 31.25 m',
    ['Step 1: time cannot be negative: $t \\ge 0$ (until the body lands).', 'Step 2: $5 \\times 6.25 = 31.25$ m.'],
    'Real situations restrict the domain.', [('$t = 3.5$ s?', '61.25 m.')])
b.TF(86, 'Two points are enough to draw the graph of $y = x^2$.', False,
     ['Step 1: two points only fix a straight line.', 'Step 2: a parabola bends, so we need a table of several points.'],
     'Lines: 2 points; parabolas: a table.', [('What is the lowest point of $y = x^2 - 9$?', '$(0, -9)$.')])
b.S(88, 'Give the vertex and the $y$-intercept of $y = -x^2 + 4x + 12$.', 'vertex $(2, 16)$; $y$-intercept 12',
    ['Step 1: $x = -\\frac{4}{2(-1)} = 2$; $y = -4 + 8 + 12 = 16$.', 'Step 2: $x = 0$ gives $12$.'],
    'Vertex $x$ from $-\\frac{b}{2a}$, then substitute.', [('Roots of $-x^2 + 4x + 12 = 0$?', '$x = -2$ or $6$.')])

c = QSet('4.3 Practice — effects of a and c', 's43')
c.M(90, 'Which graph is the narrowest?', ['$y = \\frac{1}{3}x^2$', '$y = x^2$', '$y = -3x^2$', '$y = 2x^2$'], 'C',
    ['Step 1: compare $|a|$: $\\frac{1}{3}, 1, 3, 2$.', 'Step 2: biggest $|a| = 3$ → narrowest (the sign only flips it).'],
    'Width depends on $|a|$, direction on the sign.', [('Which is the widest?', '$y = \\frac{1}{3}x^2$.')])
c.S(91, 'Give the vertex and range of $y = x^2 - 9$.', 'vertex $(0, -9)$; $y \\ge -9$',
    ['Step 1: $y = x^2$ moved down 9.', 'Step 2: opens up → minimum $-9$.'],
    '$c$ is the vertex height when $b = 0$.', [('$y = -2x^2 + 8$?', 'Vertex $(0, 8)$, range $y \\le 8$.')])
c.TF(91, '$y = -x^2$ is the reflection of $y = x^2$ in the $x$-axis.', True,
     ['Step 1: every $y$-value changes sign.', 'Step 2: $(2, 4) \\to (2, -4)$: a reflection in the $x$-axis.'],
     'Negative $a$ = mirror in the $x$-axis.', [('Reflection of $y = x^2 + 1$ in the $x$-axis?', '$y = -x^2 - 1$.')])
c.S(91, 'How is $y = 2x^2 + 2$ obtained from $y = 2x^2$?', 'shift up 2 units',
    ['Step 1: every $y$-value is 2 more.', 'Step 2: so the whole graph moves up 2; vertex $(0, 0) \\to (0, 2)$.'],
    'Adding outside → up.', [('From $y = -2x^2$ to $y = -2x^2 + 2$?', 'Up 2; vertex $(0, 2)$.')])
c.M(91, 'Which parabola has a maximum value of 5?', ['$y = x^2 + 5$', '$y = -x^2 + 5$', '$y = 5x^2$', '$y = -5x^2$'], 'B',
    ['Step 1: a maximum needs $a < 0$ (B or D).', 'Step 2: the vertex value is $c$: B has 5, D has 0.'],
    'Opens down → maximum at the vertex.', [('Minimum value of $y = 3x^2 - 4$?', '$-4$.')])

d = QSet('4.4 Practice — solving quadratic equations', 's44')
d.S(95, 'Solve $3x^2 + 12x = 0$.', '$x = 0$ or $x = -4$',
    ['Step 1: common factor $3x$: $3x(x + 4) = 0$.', 'Step 2: $3x = 0 \\Rightarrow x = 0$; $x + 4 = 0 \\Rightarrow x = -4$.'],
    'Never divide by $x$ — you would lose $x = 0$.', [('Solve $10x - 5x^2 = 0$.', '$x = 0$ or $2$.')])
d.S(95, 'Factorise $7x^2 - 28$ completely.', '$7(x + 2)(x - 2)$',
    ['Step 1: common factor 7: $7(x^2 - 4)$.', 'Step 2: difference of squares: $7(x + 2)(x - 2)$.'],
    'Common factor first, then look again.', [('Factorise $12 - 8x^2$.', '$4(3 - 2x^2)$.')])
d.S(98, 'Solve $x^2 - 4x - 12 = 0$.', '$x = 6$ or $x = -2$',
    ['Step 1: product $-12$, sum $-4$: $-6$ and $2$.', 'Step 2: $(x - 6)(x + 2) = 0$.', 'Step 3: $x = 6$ or $x = -2$.'],
    'Negative product → numbers of opposite sign.', [('Solve $x^2 - 6x + 9 = 0$.', '$x = 3$ (one repeated root).')])
d.S(98, 'Solve $4x^2 + 8x - 5 = 0$.', '$x = \\frac{1}{2}$ or $x = -\\frac{5}{2}$',
    ['Step 1: $ac = -20$; numbers with product $-20$, sum 8: $10$ and $-2$.', 'Step 2: $4x^2 + 10x - 2x - 5 = 2x(2x + 5) - (2x + 5) = (2x + 5)(2x - 1)$.', 'Step 3: $x = -\\frac{5}{2}$ or $\\frac{1}{2}$.'],
    'When $a \\ne 1$, use $ac$, not $c$.', [('Solve $2x^2 + 5x + 3 = 0$.', '$x = -1$ or $-\\frac{3}{2}$.')])
d.S(98, 'A rectangle has perimeter 28 cm and area 33 cm². Find its dimensions.', '11 cm by 3 cm',
    ['Step 1: $l + w = 14$, so $l = 14 - w$.', 'Step 2: $w(14 - w) = 33 \\Rightarrow w^2 - 14w + 33 = 0$.', 'Step 3: $(w - 3)(w - 11) = 0$: sides 3 and 11.'],
    'Half the perimeter is length + width.', [('Two positive numbers differ by 4 and have product 21?', '3 and 7.')])
d.S(99, 'Solve $(x - 2)^2 = 9$.', '$x = 5$ or $x = -1$',
    ['Step 1: square root both sides: $x - 2 = \\pm 3$.', 'Step 2: $x = 2 + 3 = 5$ or $x = 2 - 3 = -1$.'],
    'Square root → write $\\pm$.', [('Solve $-2(x - 4)^2 = -8$.', '$(x - 4)^2 = 4$: $x = 6$ or $2$.')])
d.F(99, 'To make $x^2 + 5x + \\_\\_$ a perfect square, add ____.', '$\\frac{25}{4}$', ['$\\frac{25}{4}$', '25', '$\\frac{5}{2}$', '10'],
    ['Step 1: half of 5 is $\\frac{5}{2}$.', 'Step 2: square it: $\\frac{25}{4}$; then $x^2 + 5x + \\frac{25}{4} = \\left(x + \\frac{5}{2}\\right)^2$.'],
    'Halve the coefficient of $x$, then square.', [('$x^2 - 2x + \\_$?', '1.')])
d.S(100, 'Solve $x^2 - 6x - 5 = 0$ by completing the square.', '$x = 3 \\pm \\sqrt{14}$',
    ['Step 1: $x^2 - 6x = 5$.', 'Step 2: add 9: $(x - 3)^2 = 14$.', 'Step 3: $x = 3 \\pm \\sqrt{14} \\approx 6.74$ or $-0.74$.'],
    'Add the same number to both sides.', [('Solve $x^2 + 8x - 9 = 0$.', '$x = 1$ or $-9$.')])
d.S(102, 'Solve $x^2 - 2x + 2 = 0$.', 'no real solution',
    ['Step 1: $x^2 - 2x = -2$.', 'Step 2: add 1: $(x - 1)^2 = -1$.', 'Step 3: no real number squared is negative → no real solution.'],
    'A negative right side after completing the square means no real roots.', [('Solve $-y^2 - 4y - 18 = 0$.', '$(y + 2)^2 = -14$: no real solution.')])
d.S(100, 'Can a rectangle have perimeter 36 cm and area 36 cm²? Find its sides.', 'yes: about 15.71 cm by 2.29 cm',
    ['Step 1: $l + w = 18$, $lw = 36$: $w^2 - 18w + 36 = 0$.', 'Step 2: $(w - 9)^2 = 45$, $w = 9 \\pm 3\\sqrt{5}$.', 'Step 3: $w \\approx 15.71$ or $2.29$ — the two sides.'],
    'Not every answer is a whole number — completing the square handles this.', [('Perimeter 20, area 24?', '6 by 4.')])
d.S(101, 'Profit from selling $n$ hens: $P = -n^2 + 8n$. How many hens give a profit of 12 Nakfa, and what is the maximum profit?', '2 or 6 hens; 16 Nakfa at 4 hens',
    ['Step 1: $-n^2 + 8n = 12 \\Rightarrow n^2 - 8n + 12 = 0 \\Rightarrow (n - 2)(n - 6) = 0$.', 'Step 2: vertex $n = -\\frac{8}{2(-1)} = 4$, $P = -16 + 32 = 16$.'],
    'Maximum of a downward parabola is at its vertex.', [('Profit or loss for 10 hens?', 'Loss of 20 Nakfa ($P = -20$).')])
d.S(102, 'Find a quadratic equation with roots 4 and $-1$.', '$x^2 - 3x - 4 = 0$',
    ['Step 1: roots 4 and $-1$ come from $(x - 4)(x + 1) = 0$.', 'Step 2: expand: $x^2 - 3x - 4 = 0$.'],
    'Root $r$ → factor $(x - r)$.', [('Roots $-5$ and $-3$?', '$x^2 + 8x + 15 = 0$.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Quadratic expression', '$ax^2 + bx + c$ with $a \\ne 0$.', 83),
    ('Quadratic function', '$y = ax^2 + bx + c$, $a \\ne 0$; its graph is a parabola.', 85),
    ('Parabola', 'The U-shaped graph of a quadratic function.', 86),
    ('Vertex', 'The turning point (lowest or highest point) of a parabola.', 90),
    ('Axis of symmetry', 'The vertical line through the vertex that divides the parabola into mirror halves.', 86),
    ('Quadratic equation', '$ax^2 + bx + c = 0$, $a \\ne 0$.', 94),
    ('Product property of zero', 'If $pq = 0$ then $p = 0$ or $q = 0$.', 93),
    ('Completing the square', 'Adding $(\\frac{b}{2})^2$ to make $x^2 + bx$ a perfect square $(x + \\frac{b}{2})^2$.', 100),
]
TIPS = [
    ('a > 0: opens up (minimum); a < 0: opens down (maximum); bigger |a| = narrower.', 91),
    ('Never divide an equation by x — factorise and use the product property of zero.', 93),
    ('Completing the square: halve the x-coefficient, square it, add to both sides.', 100),
]
IDEAS = [('lq', 'Linear vs quadratic', 'l4_2', 'math9-u4-md-lq-t'), ('param', 'Effects of a and c', 'l4_3', 'math9-u4-md-param-t'),
         ('fact', 'Which factorisation?', 'l4_4', 'math9-u4-md-fact-t')]
