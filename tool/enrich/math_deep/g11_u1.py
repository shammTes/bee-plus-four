r"""Grade 11 Unit 1 — Polynomial Function: quadratics (forms, equations, inequalities, graphs) and polynomial functions (pp. 1-61)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet, plane, numberline
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side, with_legend

UID = 'math11-u1'
set_unit(UID)
GBLUE, GRED, GGREEN = '#2F5F8F', '#C0503A', '#2A7A6B'


# ------------------------------------------------------------------ figures
def f_ex12():
    p = Plot(-3, 5, -5, 7, unit=30, uy=16, every=1, yevery=2, gstep=1)
    p.g('k1 k2 k3').fn(lambda x: x * x - 2 * x - 3, -2.4, 4.4, BLUE, 2.8, steps=40).end()
    for x in range(-2, 5):
        p.pt(x, x * x - 2 * x - 3, None, c=RED, r=3.8)
    p.g('k2 k3').seg((1, -5), (1, 7), PURPLE, 2, dash='6 4').text(p.X(1) + 6, p.Y(6.4), 'x = 1', 12, PURPLE, 'start').end()
    p.g('k3').pt(1, -4, None, c=GREEN, r=5).text(p.X(1) + 10, p.Y(-4) + 4, 'vertex (1, −4)', 12, GREEN, 'start').end()
    p.g('k1').text(p.X(-1) - 6, p.Y(0) - 8, '(−1, 0)', 11.5, RED, 'end').text(p.X(3) + 6, p.Y(0) - 8, '(3, 0)', 11.5, RED, 'start').end()
    return p


def f_shifts():
    p = Plot(-4, 4, -4, 6, unit=34, uy=17, every=1, yevery=2, gstep=1)
    p.fn(lambda x: x * x, -2.5, 2.5, BLUE, 2.6, steps=30)
    p.fn(lambda x: (x - 1) ** 2 + 2, -1.1, 3.1, GREEN, 2.6, steps=30)
    p.fn(lambda x: (x + 2) ** 2 - 3, -4, 0.4, RED, 2.6, steps=30)
    for (x, y, c) in ((0, 0, BLUE), (1, 2, GREEN), (-2, -3, RED)):
        p.pt(x, y, None, c=c, r=4.4)
    return with_legend(p, [('y = x²', BLUE), ('y = (x − 1)² + 2', GREEN), ('y = (x + 2)² − 3', RED)], 12)


def f_disc():
    ps = []
    for fn, c in ((lambda x: x * x - 1, BLUE), (lambda x: x * x, GREEN), (lambda x: x * x + 1, RED)):
        p = Plot(-2, 2, -1.5, 3, unit=24, uy=20, pad=8, grid=False, labels=False, xlab='', ylab='')
        p.fn(fn, -1.9, 1.9, c, 2.8, steps=30)
        ps.append(p)
    ps[0].pt(-1, 0, None, c=RED, r=4).pt(1, 0, None, c=RED, r=4)
    ps[1].pt(0, 0, None, c=RED, r=4)
    return side_by_side(ps, 8, ['D > 0: two roots', 'D = 0: one root', 'D < 0: no real root'])


def f_signchart():
    f = Fig(330, 150)
    X = lambda v: 190 + v * 18
    f.text(70, 30, 'x + 2', 13, BLUE, 'end').text(70, 60, 'x − 5', 13, GREEN, 'end').text(70, 90, 'product', 13, INK, 'end')
    for v, c in ((-2, BLUE), (5, GREEN)):
        f.line(X(v), 14, X(v), 116, c, 1.4, dash=True)
    rows = [('−', '+', '+'), ('−', '−', '+'), ('+', '−', '+')]
    cols = [X(-5), X(1.5), X(7)]
    for i, r in enumerate(rows):
        for x, s in zip(cols, r):
            f.text(x, 34 + 30 * i, s, 18, RED if s == '−' else GREEN)
    f.arrow(80, 124, 326, 124, INK, 1.8, 7)
    f.dot(X(-2), 124, INK, 4).dot(X(5), 124, INK, 4)
    f.text(X(-2), 142, '−2', 12.5, INK).text(X(5), 142, '5', 12.5, INK)
    return f


def f_maxarea():
    p = Plot(0, 1600, 0, 650, unit=0.19, uy=0.28, pad=30, grid=False, every=500, yevery=200, xlab='x (m)', ylab='')
    p.text(p.X(0) + 10, p.Y(650) + 4, 'A (1000 m²)', 12, GREY, 'start')
    p.fn(lambda x: x * (1500 - x) / 1000, 0, 1500, BLUE, 2.8, steps=40)
    p.seg((750, 0), (750, 562.5), PURPLE, 1.6, dash='5 4').pt(750, 562.5, None, c=RED, r=5)
    p.text(p.X(750), p.Y(562.5) - 10, 'max 562 500 m² at x = 750', 12, RED)
    p.text(p.X(1150), p.Y(400), 'A = x(1500 − x)', 12.5, BLUE, 'start')
    return p


def f_location():
    p = Plot(-2.5, 2.5, -2, 4, unit=50, uy=22, every=1, yevery=1, gstep=1)
    p.fn(lambda x: x ** 3 - 3 * x + 1, -2.15, 2.15, BLUE, 2.8, steps=40)
    for x in (-2, -1, 0, 1, 2):
        y = x ** 3 - 3 * x + 1
        p.pt(x, y, None, c=GREEN if y > 0 else RED, r=4.2)
    p.text(p.X(1.55), p.Y(-1.6), 'f(1) < 0 < f(2)', 12, INK)
    return p


DIAGRAMS = {
    'ex12': (f_ex12(), 'Example 1.2: y = x² − 2x − 3', 4),
    'shifts': (f_shifts(), 'Shifting y = x² (Examples 1.13–1.15)', 32),
    'disc': (f_disc(), 'The discriminant and the x-intercepts', 18),
    'signchart': (f_signchart(), 'Sign chart for (x + 2)(x − 5)', 26),
    'maxarea': (f_maxarea(), 'Example 1.17: the largest field', 38),
    'location': (f_location(), 'A sign change means a zero in between', 50),
}

# ------------------------------------------------------------------ 1.1
L1 = [
    T('=math11-u1-c01', '1.1 Representing quadratic functions', 1,
      'A **quadratic function** is $f(x) = ax^2 + bx + c$ with real $a, b, c$ and $a \\ne 0$. Its graph is a **parabola**.',
      'You can represent it by a **formula**, a **table of values**, a **graph**, or in **words** (a real situation). Moving between them is the skill of this section.',
      '**Example 1.1 (braking distance):** $B(s) = 0.01s^2 + 0.7s$ metres at $s$ km/h. At 30 km/h: $B = 9 + 21 = 30$ m; at 100 km/h: $100 + 70 = 170$ m. A car that needed 60 m: $0.01s^2 + 0.7s = 60 \\Rightarrow s^2 + 70s - 6000 = 0 \\Rightarrow (s - 50)(s + 120) = 0$, so $s = 50$ km/h (speed cannot be negative).',
      '**Finding a model from data:** if the table is symmetric (same $y$ on both sides of a lowest point), that point is the vertex $(h, k)$ and $f(x) = a(x - h)^2 + k$; use one more point to find $a$.'),
    ST('ex12', 'Reading the graph of y = x² − 2x − 3', 4, 'ex12',
       [('Table: $x = -2, \\dots, 4$ gives $y = 5, 0, -3, -4, -3, 0, 5$. The x-intercepts are $-1$ and 3.', 'k1'),
        ('Equal $y$-values pair up around $x = 1$: that is the **axis of symmetry**.', 'k2'),
        ('The lowest point is the **vertex** $(1, -4)$, so the range is $\\{y : y \\ge -4\\}$.', 'k3')]),
    WK('ex-11a', 'Worked example: a model from a table (Activity 1.1)', 2,
       'Women working: (0, 5), (1, 4), (2, 5), (3, 8), (4, 13), (5, 20), with $x = 0$ for 1990. Find $f(x) = ax^2 + bx + c$, estimate 2000, and find when there will be 53 women.',
       ['Symmetry: $f(0) = f(2) = 5$, so the vertex is at $x = 1$: $f(x) = a(x - 1)^2 + 4$.', '$f(0) = a + 4 = 5 \\Rightarrow a = 1$: $f(x) = x^2 - 2x + 5$. Check $f(5) = 25 - 10 + 5 = 20$ (correct).', '2000 is $x = 10$: $100 - 20 + 5 = 85$ women.', '$x^2 - 2x + 5 = 53 \\Rightarrow x^2 - 2x - 48 = 0 \\Rightarrow (x - 8)(x + 6) = 0$, $x = 8$: in 1998.'],
       '$f(x) = x^2 - 2x + 5$; 85 women; 1998'),
    WK('ex-11b', 'Worked example: a ball thrown upward (Activity 1.2)', 3,
       '$h(t) = 50t - 5t^2$. Find the maximum height, when it is reached, when the ball lands, and the domain and range.',
       ['Factor: $h = 5t(10 - t)$: zeros $t = 0$ and $t = 10$.', 'The vertex is halfway: $t = 5$, $h(5) = 250 - 125 = 125$ m.', 'Lands at $t = 10$ s. Domain $0 \\le t \\le 10$, range $0 \\le h \\le 125$.'],
       'max 125 m at 5 s; lands at 10 s'),
]

# ------------------------------------------------------------------ 1.2
L2 = [
    T('=math11-u1-c02', '1.2.1 Solving quadratic equations', 6,
      'Standard form: $ax^2 + bx + c = 0$, $a \\ne 0$. Four methods:',
      '**1. Factorising (split the middle term):** find $m, n$ with $m + n = b$ and $mn = ac$. For $3x^2 - 10x + 8$: $m + n = -10$, $mn = 24$ → $-4, -6$: $3x^2 - 4x - 6x + 8 = x(3x - 4) - 2(3x - 4) = (3x - 4)(x - 2)$. Then use "product = 0 ⇒ a factor = 0".',
      '**2. Completing the square:** make the coefficient of $x^2$ equal to 1, move $c$, add $\\left(\\frac{b}{2}\\right)^2$: $x^2 - 6x = -2 \\Rightarrow (x - 3)^2 = 7 \\Rightarrow x = 3 \\pm \\sqrt{7}$.',
      '**3. Quadratic formula** (completing the square done once for all): $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$',
      '**4. Graph:** the solutions are the x-intercepts of $y = ax^2 + bx + c$.',
      'Textbook slip: in Example 1.5 the factorisation of $3x^2 - 4x - 4$ is $(3x + 2)(x - 2)$, not "$(x + 2)(x - 2)$"; the answers $x = -\\frac{2}{3}$ and $x = 2$ are right.'),
    'math11-u1-c10',
    T('disc-t', 'The discriminant', 17,
      '$D = b^2 - 4ac$ is the part under the root. It tells you **how many** real solutions there are **before** solving:',
      '- $D > 0$: two different real solutions (the parabola crosses the x-axis twice). A **perfect square** $D$ means they are rational (it factorises).',
      '- $D = 0$: one (repeated) solution $x = -\\frac{b}{2a}$ (it touches the axis at the vertex).',
      '- $D < 0$: no real solution (the parabola misses the axis).',
      'Example 1.9: $-4x^2 + 12x - 9 = 0$: $D = 144 - 144 = 0$, one solution $x = \\frac{3}{2}$.'),
    DG('disc', 'Three cases', 18, 'disc'),
    WK('ex-12a', 'Worked example: Example 1.8 (quadratic formula)', 15,
       'Solve (a) $2x^2 + 6x + 3 = 0$ (b) $-5x^2 + 13x - 7 = 0$.',
       ['(a) $a = 2, b = 6, c = 3$: $D = 36 - 24 = 12$; $x = \\frac{-6 \\pm 2\\sqrt{3}}{4} = \\frac{-3 \\pm \\sqrt{3}}{2}$.', '(b) $a = -5, b = 13, c = -7$: $D = 169 - 140 = 29$; $x = \\frac{-13 \\pm \\sqrt{29}}{-10} = \\frac{13 \\mp \\sqrt{29}}{10}$.'],
       '(a) $\\frac{-3 \\pm \\sqrt{3}}{2}$ (b) $\\frac{13 \\pm \\sqrt{29}}{10}$'),
    WK('ex-12b', 'Worked example: Example 1.6 (two trains)', 11,
       'Two trains leave a station at right angles; one is 20 km/h faster. After 1 hour they are 100 km apart. Find their speeds.',
       ['Distances after 1 h: $x$ and $x + 20$ (legs); 100 is the hypotenuse.', '$x^2 + (x + 20)^2 = 100^2 \\Rightarrow 2x^2 + 40x - 9600 = 0 \\Rightarrow x^2 + 20x - 4800 = 0$.', '$(x + 80)(x - 60) = 0$; speed is positive: $x = 60$.'],
       '60 km/h and 80 km/h'),
    T('ineq-t', '1.2.2 Quadratic inequalities', 21,
      'To solve $ax^2 + bx + c > 0$ (or $<$, $\\ge$, $\\le$):',
      '1. Move everything to one side and **factorise** (or find the roots).',
      '2. **Case method:** a product is positive when both factors have the same sign, negative when they have opposite signs. $x^2 - x - 12 = (x - 4)(x + 3) > 0$: both positive ($x > 4$) **or** both negative ($x < -3$).',
      '3. **Sign chart:** mark the roots on a number line; test one value in each interval.',
      '4. **Graph:** for $a > 0$ the parabola is **below** the axis **between** the roots and **above** it **outside** them.',
      'Shortcut ($a > 0$, roots $r_1 < r_2$): "$< 0$" → $r_1 < x < r_2$ (between); "$> 0$" → $x < r_1$ or $x > r_2$ (outside). If $a < 0$, multiply by $-1$ and **reverse** the sign first.'),
    DG('signchart', 'Sign chart', 26, 'signchart',
       'For $(x + 2)(x - 5)$: positive for $x < -2$, negative between $-2$ and 5, positive for $x > 5$. So $(x + 2)(x - 5) < 0$ ⇔ $-2 < x < 5$.'),
    GR('nl-ineq', 'Solution of x² − x − 12 > 0 on the number line', 23,
       numberline(-6, 7, 1, points=[{'x': -3, 'open': True, 'color': GRED}, {'x': 4, 'open': True, 'color': GRED}],
                  ranges=[{'from': -6, 'to': -3, 'to_open': True, 'color': GBLUE}, {'from': 4, 'to': 7, 'from_open': True, 'color': GBLUE}]),
       'Open circles: $-3$ and 4 are not included because the inequality is strict.'),
    WK('ex-12c', 'Worked example: Example 1.12 (sign chart)', 27,
       'Solve $-2x^2 + 15x - 7 > 0$.',
       ['Multiply by $-1$ and reverse: $2x^2 - 15x + 7 < 0$.', 'Factor: $(2x - 1)(x - 7) < 0$; roots $\\frac{1}{2}$ and 7.', 'Opening up and "< 0" → between the roots.'],
       '$\\frac{1}{2} < x < 7$'),
    'math11-u1-c11',
]

# ------------------------------------------------------------------ 1.3
L3 = [
    T('=math11-u1-c04', '1.3 Graphs of quadratic functions: transformations', 30,
      'Every parabola is $y = x^2$ moved and stretched:',
      '- $y = x^2 + k$: up $k$ (down if $k < 0$).',
      '- $y = (x - h)^2$: **right** $h$ (note the minus: $(x + 2)^2$ moves **left** 2).',
      '- $y = a x^2$: $|a| > 1$ narrower, $|a| < 1$ wider, $a < 0$ flipped upside down.',
      '**Vertex form:** $y = a(x - h)^2 + k$ has vertex $(h, k)$, axis $x = h$; minimum $k$ if $a > 0$, maximum $k$ if $a < 0$.'),
    DG('shifts', 'Same shape, different vertex', 32, 'shifts',
       'Vertices: $(0, 0)$, $(1, 2)$, $(-2, -3)$. All three have $a = 1$, so they are congruent.'),
    'math11-u1-c09',
    T('vform-t', 'From ax² + bx + c to vertex form', 35,
      'Completing the square gives $$f(x) = a\\left(x + \\frac{b}{2a}\\right)^2 + \\frac{4ac - b^2}{4a}$$ so the vertex is $\\left(-\\frac{b}{2a}, \\frac{4ac - b^2}{4a}\\right)$.',
      'In practice: $x_v = -\\frac{b}{2a}$, then $y_v = f(x_v)$. Example: $f(x) = 2x^2 - 8x + 20$: $x_v = 2$, $f(2) = 12$, so $f(x) = 2(x - 2)^2 + 12$ (minimum 12).',
      'Range: $a > 0$ → $y \\ge y_v$; $a < 0$ → $y \\le y_v$.'),
    'math11-u1-c13',
    DG('maxarea', 'Maximum area', 38, 'maxarea'),
    WK('ex-13a', 'Worked example: Example 1.17 (largest field)', 38,
       'Find the largest rectangular field that can be fenced with 3000 m of wire.',
       ['Sides $x$ and $y$: $2x + 2y = 3000 \\Rightarrow y = 1500 - x$.', 'Area $A = x(1500 - x) = -x^2 + 1500x$ (a downward parabola).', 'Vertex: $x = -\\frac{1500}{2(-1)} = 750$, $y = 750$; $A = 562\\,500$ m².'],
       'a 750 m × 750 m square, 562 500 m²'),
    WK('ex-13b', 'Worked example: Exercise 1.1 Q3 (budget)', 6,
       'The budget is $f(x) = 2x^2 - 8x + 20$ million Nakfa ($x = 0$ in 2000). Find the lowest budget and when it reaches 44 million.',
       ['Vertex $x = 2$: $f(2) = 8 - 16 + 20 = 12$ million (in 2002).', '$2x^2 - 8x + 20 = 44 \\Rightarrow x^2 - 4x - 12 = 0 \\Rightarrow (x - 6)(x + 2) = 0$.', '$x = 6$: in 2006.'],
       'lowest 12 million (2002); 44 million in 2006'),
]

# ------------------------------------------------------------------ 1.4
L4 = [
    T('=math11-u1-c08', '1.4 Polynomial functions', 41,
      '$f(x) = a_n x^n + \\dots + a_1 x + a_0$ ($a_n \\ne 0$, whole-number powers): degree $n$, leading coefficient $a_n$, constant term $a_0$.',
      '**Degree of a product** = sum of degrees: $(3x^2 + 7x^5 - 1)(2x - x^2 + 6)$ has degree $5 + 2 = 7$, leading coefficient $7 \\times (-1) = -7$, constant term $-1 \\times 6 = -6$.',
      '**Graphs:** a degree-$n$ polynomial has at most $n$ x-intercepts and at most $n - 1$ turning points. The ends follow $a_n x^n$: even degree → both ends the same way; odd → opposite ways; $a_n > 0$ → right end up.',
      '**Location theorem:** if $f(a)$ and $f(b)$ have opposite signs, $f$ has a zero between $a$ and $b$ (the smooth graph must cross the axis).'),
    'math11-u1-c05',
    DG('location', 'Locating zeros of f(x) = x³ − 3x + 1', 50, 'location',
       'Values at $x = -2, -1, 0, 1, 2$: $-1, 3, 1, -1, 3$ (green dots above the axis, red below). Sign changes between $-2$ and $-1$, between 0 and 1, and between 1 and 2 — three zeros, the most a cubic can have.'),
    T('divalg-t', 'Division, remainder and factor theorems', 52,
      '**Division algorithm:** $f(x) = g(x)\\,q(x) + r(x)$ with $\\deg r < \\deg g$. Example 1.23: $x^3 + 3x^2 - 6x + 8 = (x^2 + 2x)(x + 1) + (-8x + 8)$.',
      '**Remainder theorem:** the remainder when $f(x)$ is divided by $x - a$ is $f(a)$. $f(x) = 2x^3 - 5x + 1$ ÷ $(x - 2)$: remainder $f(2) = 7$; ÷ $(x + 4)$: $f(-4) = -107$.',
      '**Factor theorem:** $x - a$ is a factor ⇔ $f(a) = 0$.',
      '**Possible integer roots:** for integer coefficients, an integer zero $a$ must divide the constant term $a_0$ (try $\\pm 1, \\pm 2, \\dots$).',
      '**Cubes:** $a^3 + b^3 = (a + b)(a^2 - ab + b^2)$, $a^3 - b^3 = (a - b)(a^2 + ab + b^2)$. (In Example 1.26(b) the textbook writes $x^3 - y^3 = (x - y)(x^2 + 2xy + y^2)$; the middle term must be $xy$.)'),
    'math11-u1-mn4',
    WK('ex-14a', 'Worked example: Example 1.25 (factorise completely)', 57,
       'Factorise $f(x) = 2x^4 + 3x^3 - 12x^2 - 7x + 6$ and find its zeros.',
       ['Try divisors of 6: $f(1) = -8$, $f(-1) = 2 - 3 - 12 + 7 + 6 = 0$ → $(x + 1)$ is a factor.', 'Divide: $f(x) = (x + 1)(2x^3 + x^2 - 13x + 6)$.', 'In the cubic, $x = 2$ gives $16 + 4 - 26 + 6 = 0$ → $(x - 2)(2x^2 + 5x - 3)$.', '$2x^2 + 5x - 3 = (2x - 1)(x + 3)$. Zeros: $-1, 2, \\frac{1}{2}, -3$.'],
       '$(x + 1)(x - 2)(2x - 1)(x + 3)$'),
    WK('ex-14b', 'Worked example: find k', 58,
       'Find $k$ if $(x + 5)$ is a factor of $f(x) = x^3 + 2x^2 - kx + 10$.',
       ['Factor theorem: $f(-5) = 0$.', '$-125 + 50 + 5k + 10 = 0 \\Rightarrow 5k = 65$.', '$k = 13$.'],
       '$k = 13$'),
    RM('summary-t', 'Unit summary', 61,
       'Quadratic: factorise ($m + n = b$, $mn = ac$), complete the square or use $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$; $D = b^2 - 4ac$ counts the roots.',
       'Inequalities: $a > 0$ → "< 0" between the roots, "> 0" outside.',
       'Vertex $\\left(-\\frac{b}{2a}, f\\left(-\\frac{b}{2a}\\right)\\right)$; $y = a(x - h)^2 + k$.',
       '$f(a)$ = remainder on division by $x - a$; $f(a) = 0$ ⇔ $(x - a)$ is a factor.'),
]

LESSONS = {'math11-u1-l1-1': L1, 'math11-u1-l1-2': L2, 'math11-u1-l1-3': L3, 'math11-u1-l1-4': L4}

# ------------------------------------------------------------------ practice
a = QSet('1.1 Practice — representing quadratics', 's11')
a.S(6, 'Tourist spending: (0, 10), (1, 7), (2, 6), (3, 7), (4, 10), (5, 15) with $x = 0$ in 1998. Find $f(x)$ and estimate 2004.', '$f(x) = x^2 - 4x + 10$; 22 million',
    ['Step 1: symmetric about $x = 2$; vertex $(2, 6)$.', 'Step 2: $f(0) = 4a + 6 = 10 \\Rightarrow a = 1$.', 'Step 3: 2004 is $x = 6$: $16 + 6 = 22$.'],
    'Look for the symmetry in the table first.', [('Minimum spending year?', '2000 (6 million).')])
a.S(3, 'Braking distance $B(s) = 0.01s^2 + 0.7s$. Find $B(50)$.', '60 m',
    ['Step 1: $0.01 \\times 2500 = 25$.', 'Step 2: $0.7 \\times 50 = 35$; total 60 m.'], 'Square first, then multiply.', [('$B(20)$?', '$4 + 14 = 18$ m.')])
a.S(5, 'For $f(x) = 8x - x^2$, find the vertex, axis and range.', 'vertex $(4, 16)$, $x = 4$, $y \\le 16$',
    ['Step 1: zeros 0 and 8 → axis $x = 4$.', 'Step 2: $f(4) = 32 - 16 = 16$.', 'Step 3: $a = -1 < 0$: maximum, range $y \\le 16$.'], 'Axis = midpoint of the zeros.', [('$f(x) = x^2 - 1$?', 'vertex $(0, -1)$, range $y \\ge -1$.')])
a.M(4, 'The range of $f(x) = x^2 - 2x - 3$ is', ['all reals', '$y \\ge -4$', '$y \\le -4$', '$y \\ge -3$'], 'B',
    ['Step 1: vertex $(1, -4)$, opens up.'], 'Range starts at the vertex.', [('Range of $-x^2 + 4$?', '$y \\le 4$.')])

b = QSet('1.2 Practice — equations and inequalities', 's12')
b.S(9, 'Factorise (a) $3x^2 - 13x - 10$ (b) $-3x^2 + 20x + 7$.', '$(3x + 2)(x - 5)$; $-(3x + 1)(x - 7)$',
    ['Step 1 (a): $m + n = -13$, $mn = -30$: $2, -15$ → $3x^2 + 2x - 15x - 10 = x(3x + 2) - 5(3x + 2)$.', 'Step 2 (b): take out $-1$: $3x^2 - 20x - 7 = (3x + 1)(x - 7)$.'],
    'Check by expanding.', [('$x^2 + 9x + 20$?', '$(x + 4)(x + 5)$.')])
b.S(9, 'Is $2x^2 - 5x - 3 = (x - 1)(2x + 3)$? If not, correct it.', 'No: $(2x + 1)(x - 3)$',
    ['Step 1: expand: $2x^2 + x - 3$ — middle term wrong.', 'Step 2: $m + n = -5$, $mn = -6$: $1, -6$ → $(2x + 1)(x - 3)$.'], 'Always check the middle term.', [('Is $x^2 - 2x - 8 = (x - 2)(x + 4)$?', 'No, $(x - 4)(x + 2)$.')])
b.S(12, 'Solve by factorising: (a) $5x^2 + 18x = 8$ (b) $2n^2 = 12n + 54$.', '$\\frac{2}{5}, -4$; $9, -3$',
    ['Step 1 (a): $5x^2 + 18x - 8 = (5x - 2)(x + 4) = 0$.', 'Step 2 (b): $n^2 - 6n - 27 = (n - 9)(n + 3) = 0$.'], 'Standard form first (right side 0).', [('$x^2 - 5x = 14$?', '7, $-2$.')])
b.S(12, 'The length of a rectangle is 5 cm more than its width and its area is 84 cm². Find its sides.', '7 cm and 12 cm',
    ['Step 1: $w(w + 5) = 84 \\Rightarrow w^2 + 5w - 84 = 0$.', 'Step 2: $(w + 12)(w - 7) = 0$, $w = 7$.'], 'Reject negative lengths.', [('Two consecutive even integers with product 224?', '14 and 16 (or −16 and −14).')])
b.S(13, 'A circle of radius 8 cm: by how much must the radius decrease to reduce the area by $48\\pi$ cm²?', '4 cm',
    ['Step 1: new area $64\\pi - 48\\pi = 16\\pi$.', 'Step 2: $r^2 = 16$, $r = 4$: decrease by 4 cm.'], 'Work with $r^2$.', [('Radius 5, increase area by $11\\pi$?', 'new $r = 6$, +1 cm.')])
b.S(14, 'Solve by completing the square: $x^2 + 8x - 6 = 0$.', '$x = -4 \\pm \\sqrt{22}$',
    ['Step 1: $x^2 + 8x = 6$.', 'Step 2: add 16: $(x + 4)^2 = 22$.', 'Step 3: $x = -4 \\pm \\sqrt{22}$.'], 'Add (half of b)².', [('$x^2 - 6x = -2$?', '$3 \\pm \\sqrt{7}$.')])
b.S(14, 'One leg of a right triangle is 4 cm longer than the other; the hypotenuse is 12 cm. Find the legs.', '$-2 + 2\\sqrt{17} \\approx 6.25$ and $\\approx 10.25$ cm',
    ['Step 1: $x^2 + (x + 4)^2 = 144 \\Rightarrow x^2 + 4x - 64 = 0$.', 'Step 2: $(x + 2)^2 = 68$, $x = -2 + 2\\sqrt{17} \\approx 6.25$.'], 'Pythagoras gives the quadratic.', [('Legs differ by 7, hypotenuse 13?', '5 and 12.')])
b.S(14, 'A square card of side $x$ cm has 5 cm squares cut from each corner and is folded into an open box of volume 400 cm³. Find $x$.', '$10 + 4\\sqrt{5} \\approx 18.9$ cm',
    ['Step 1: base $(x - 10)^2$, height 5: $5(x - 10)^2 = 400$.', 'Step 2: $(x - 10)^2 = 80$, $x = 10 + \\sqrt{80} \\approx 18.9$.'], 'The base loses 5 cm at each end.', [('Volume 500 instead?', '$x = 20$.')])
b.S(16, 'Use the formula: (a) $4x^2 - 14x = 9$ (b) $10x - x^2 = -3$.', '$\\frac{7 \\pm \\sqrt{85}}{4}$; $5 \\pm 2\\sqrt{7}$',
    ['Step 1 (a): $4x^2 - 14x - 9 = 0$: $D = 196 + 144 = 340$; $x = \\frac{14 \\pm 2\\sqrt{85}}{8}$.', 'Step 2 (b): $x^2 - 10x - 3 = 0$: $D = 112$; $x = \\frac{10 \\pm 4\\sqrt{7}}{2}$.'], 'Simplify the root at the end.', [('$x^2 + 8x + 12 = 0$?', '$-2, -6$.')])
b.S(18, 'How many real solutions? (a) $x^2 + 4x + 13 = 0$ (b) $9x^2 + 12x = -4$ (c) $3x^2 - x - 2 = 0$', 'none; one; two',
    ['Step 1: $D = 16 - 52 < 0$.', 'Step 2: $9x^2 + 12x + 4$: $D = 144 - 144 = 0$.', 'Step 3: $D = 1 + 24 = 25 > 0$.'], 'Only the sign of $D$ matters.', [('$x^2 + x + 1 = 0$?', 'none ($D = -3$).')])
b.S(24, 'Solve $x^2 - 5x - 14 < 0$.', '$-2 < x < 7$',
    ['Step 1: $(x - 7)(x + 2) < 0$.', 'Step 2: opens up, "< 0" → between.'], 'Between the roots.', [('$x^2 - 2x - 3 < 0$?', '$-1 < x < 3$.')])
b.S(28, 'Solve (a) $x^2 - 25 > 0$ (b) $2x^2 + 7x > 0$.', '$x < -5$ or $x > 5$; $x < -\\frac{7}{2}$ or $x > 0$',
    ['Step 1: roots $\\pm 5$, outside.', 'Step 2: $x(2x + 7) > 0$: roots $-\\frac{7}{2}$, 0, outside.'], 'Outside the roots for "> 0".', [('$x^2 - 6x > 16$?', '$x < -2$ or $x > 8$.')])
b.S(28, 'Solve $9x - 2x^2 \\le -5$.', '$x \\le -\\frac{1}{2}$ or $x \\ge 5$',
    ['Step 1: $2x^2 - 9x - 5 \\ge 0$.', 'Step 2: $(2x + 1)(x - 5) \\ge 0$: outside, endpoints included.'], 'Make $a$ positive, flip the sign.', [('$-x^2 + 4 \\ge 0$?', '$-2 \\le x \\le 2$.')])
b.TF(18, 'If $D = 0$, the parabola touches the x-axis at its vertex.', True,
     ['Step 1: one repeated root $x = -\\frac{b}{2a}$, which is the vertex x-coordinate.'], 'Touch, not cross.', [('If $D < 0$ and $a > 0$, where is the parabola?', 'entirely above the x-axis.')])

c = QSet('1.3 Practice — graphs', 's13')
c.S(33, 'Describe how to get $y = (x + 2)^2 - 3$ from $y = x^2$, and give the vertex.', 'left 2, down 3; $(-2, -3)$',
    ['Step 1: $(x + 2)$ → left 2.', 'Step 2: $-3$ → down 3.'], 'Inside the bracket: opposite direction.', [('$y = (x - 1)^2 + 2$?', 'right 1, up 2; $(1, 2)$.')])
c.S(36, 'Write $f(x) = x^2 - 4x + 1$ in vertex form.', '$(x - 2)^2 - 3$',
    ['Step 1: $x_v = 2$, $f(2) = -3$.', 'Step 2: $a = 1$.'], '$x_v = -\\frac{b}{2a}$.', [('$f(x) = -3x^2 + 12x - 5$: vertex?', '$(2, 7)$.')])
c.S(36, 'Find the maximum or minimum of $f(x) = -2(x - 1)^2 + 5$.', 'maximum 5 at $x = 1$',
    ['Step 1: $a = -2 < 0$ → maximum.', 'Step 2: vertex $(1, 5)$.'], 'Read $(h, k)$ directly.', [('$f(x) = 3(x + 4)^2 - 1$?', 'minimum $-1$ at $x = -4$.')])
c.S(39, 'Two numbers add to 20. Find the largest possible product.', '100',
    ['Step 1: $P = x(20 - x)$.', 'Step 2: vertex $x = 10$, $P = 100$.'], 'Max of a downward parabola at the vertex.', [('Perimeter 40 m: largest rectangle area?', '100 m² (a square).')])
c.M(37, 'The axis of symmetry of $y = 2x^2 + 5x + 6$ is', ['$x = -\\frac{5}{4}$', '$x = \\frac{5}{4}$', '$x = -\\frac{5}{2}$', '$x = 6$'], 'A',
    ['Step 1: $-\\frac{b}{2a} = -\\frac{5}{4}$.'], 'Divide by $2a$, not $a$.', [('Axis of $y = x^2 - 6x$?', '$x = 3$.')])

d = QSet('1.4 Practice — polynomial functions', 's14')
d.S(45, 'For $f(x) = (3x^2 + 7x - 1)(2x - x^2 + 6)$ find the degree, leading coefficient and constant term.', '4; $-3$; $-6$',
    ['Step 1: degrees $2 + 2 = 4$.', 'Step 2: leading $3 \\times (-1) = -3$.', 'Step 3: constant $-1 \\times 6 = -6$.'], 'Multiply only leading terms / constant terms.', [('Degree of $(x^3 + 1)(x^2 - 2)$?', '5.')])
d.S(55, 'Find the remainder when $f(x) = 3x - 5$ is divided by $x - 8$, and when $x^3 - 2x + 4$ is divided by $x + 2$.', '19; 0',
    ['Step 1: $f(8) = 19$.', 'Step 2: $(-2)^3 + 4 + 4 = 0$.'], 'Remainder = $f(a)$ for divisor $x - a$.', [('$x^2 + 1$ ÷ $(x - 3)$?', '10.')])
d.S(58, 'Is (a) $(x - 2)$ a factor of $2x^3 - 11x + 6$? (b) $(x + 3)$ a factor of $3x^3 + 7x^2 - 10x - 2$? (c) $(x + 4)$ a factor of $x^5 + 1024$?', 'yes; no; yes',
    ['Step 1: $f(2) = 16 - 22 + 6 = 0$.', 'Step 2: $f(-3) = -81 + 63 + 30 - 2 = 10$.', 'Step 3: $(-4)^5 = -1024$, sum 0.'], 'Zero remainder ⇔ factor.', [('$(x - 1)$ of $x^4 + 2x^3 - 3x^2 + 8x - 8$?', 'yes ($f(1) = 0$).')])
d.S(58, 'Find $k$ if $(x - 1)$ is a factor of $x^3 + kx^2 + 9x - 5$.', '$k = -5$',
    ['Step 1: $f(1) = 1 + k + 9 - 5 = 0$.', 'Step 2: $k = -5$.'], 'Set $f(a) = 0$.', [('$(x - 2)$ a factor of $x^2 + kx + 6$?', '$k = -5$.')])
d.S(54, 'Divide $x^2 + 8x - 6$ by $x - 7$: find $q(x)$ and $r$.', '$q = x + 15$, $r = 99$',
    ['Step 1: $x$: subtract $x^2 - 7x$ → $15x - 6$.', 'Step 2: $15$: subtract $15x - 105$ → 99.', 'Check: $f(7) = 49 + 56 - 6 = 99$ (correct).'], 'Check with the remainder theorem.', [('$x^2 - 1$ ÷ $(x - 1)$?', '$x + 1$, 0.')])
d.S(59, 'Factorise $x^3 - 27$ and $8x^3 + 1$.', '$(x - 3)(x^2 + 3x + 9)$; $(2x + 1)(4x^2 - 2x + 1)$',
    ['Step 1: $a = x$, $b = 3$.', 'Step 2: $a = 2x$, $b = 1$.'], 'SOAP: Same, Opposite, Always Positive signs.', [('$a^3 + 64$?', '$(a + 4)(a^2 - 4a + 16)$.')])
d.S(50, 'Between which consecutive integers does $f(x) = x^3 - 3x + 1$ have zeros?', '$-2$ and $-1$; 0 and 1; 1 and 2',
    ['Step 1: $f(-2) = -1$, $f(-1) = 3$, $f(0) = 1$, $f(1) = -1$, $f(2) = 3$.', 'Step 2: look for sign changes.'], 'Location theorem.', [('$f(x) = x^2 - 2$?', '$-2$ and $-1$; 1 and 2.')])
d.S(47, 'Describe the end behaviour of $f(x) = -2x^5 + 10x^2 - 8x + 2$.', 'left up, right down',
    ['Step 1: leading term $-2x^5$: odd, negative.'], 'Only the leading term matters.', [('$g(x) = -x^4 + 5x^2$?', 'both ends down.')])
d.TF(52, 'A polynomial of degree 4 can have 5 x-intercepts.', False, ['Step 1: at most $n = 4$ zeros.'], 'Degree caps the number of zeros.', [('Max turning points of a cubic?', '2.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Quadratic function', '$f(x) = ax^2 + bx + c$, $a \\ne 0$.', 1), ('Discriminant', '$D = b^2 - 4ac$.', 17),
    ('Vertex', 'The turning point of a parabola, $\\left(-\\frac{b}{2a}, f\\left(-\\frac{b}{2a}\\right)\\right)$.', 35),
    ('Axis of symmetry', 'The vertical line $x = -\\frac{b}{2a}$ through the vertex.', 4),
    ('Sign chart', 'A number line showing the sign of each factor in each interval.', 26),
    ('Remainder theorem', 'Dividing $f(x)$ by $x - a$ leaves remainder $f(a)$.', 55),
    ('Factor theorem', '$x - a$ is a factor of $f(x)$ ⇔ $f(a) = 0$.', 56),
    ('Location theorem', 'Opposite signs of $f(a)$ and $f(b)$ ⇒ a zero between $a$ and $b$.', 50),
]
TIPS = [('Split the middle term: m + n = b, mn = ac.', 8), ('a > 0: "< 0" between the roots, "> 0" outside.', 25),
        ('Vertex x = −b/(2a); then substitute for y.', 35)]
IDEAS = [('disc', 'Discriminant', 'l1_2', 'math11-u1-md-disc-t'), ('vform', 'Vertex form', 'l1_3', 'math11-u1-md-vform-t'),
         ('divalg', 'Remainder and factor theorems', 'l1_4', 'math11-u1-md-divalg-t')]
