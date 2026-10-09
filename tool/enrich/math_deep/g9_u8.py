r"""Grade 9 Unit 8 — Polynomials (pp. 169-198)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet, plane
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side

UID = 'math9-u8'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_anatomy():
    f = Fig(330, 150)
    f.text(165, 80, '−5x³ + 4x² − 9', 26, INK)
    f.arrow(50, 34, 82, 58, RED, 1.8, 7).text(8, 26, 'leading coefficient −5', 12.5, RED, 'start')
    f.arrow(176, 30, 136, 54, BLUE, 1.8, 7).text(180, 34, 'power 3 = degree', 12.5, BLUE, 'start')
    f.arrow(178, 112, 178, 94, GREEN, 1.8, 7).text(150, 128, 'term 4x², coefficient 4', 12.5, GREEN)
    f.arrow(252, 112, 252, 94, PURPLE, 1.8, 7).text(272, 128, 'constant term', 12.5, PURPLE)
    f.text(165, 146, 'three terms: a trinomial of degree 3', 12, GREY)
    return f


def f_square():
    f = Fig(330, 200)
    x0, y0, a, b = 20, 20, 110, 50
    f.g('k2 k3').rect(x0, y0, a, a, BLUE, 2, FILL[BLUE]).text(x0 + a / 2, y0 + a / 2 + 6, 'a²', 18, BLUE)
    f.rect(x0 + a, y0, b, a, GREEN, 2, FILL[GREEN]).text(x0 + a + b / 2, y0 + a / 2 + 6, 'ab', 15, GREEN)
    f.rect(x0, y0 + a, a, b, GREEN, 2, FILL[GREEN]).text(x0 + a / 2, y0 + a + b / 2 + 6, 'ab', 15, GREEN)
    f.rect(x0 + a, y0 + a, b, b, ORANGE, 2, FILL[ORANGE]).text(x0 + a + b / 2, y0 + a + b / 2 + 6, 'b²', 15, ORANGE).end()
    f.g('k1').rect(x0, y0, a + b, a + b, INK, 2.6, FILL[GREY]).text(x0 + (a + b) / 2, y0 + (a + b) / 2 + 6, '(a + b)²', 17, INK).end()
    f.text(x0 + a / 2, 14, 'a', 13, INK).text(x0 + a + b / 2, 14, 'b', 13, INK)
    f.text(x0 + a + b + 10, y0 + a / 2, 'a', 13, INK, 'start').text(x0 + a + b + 10, y0 + a + b / 2, 'b', 13, INK, 'start')
    f.g('k3').text(262, 90, '(a + b)²', 15, INK).text(262, 114, '= a² + 2ab + b²', 14, RED).text(262, 140, 'NOT a² + b²', 12.5, GREY).end()
    return f


def f_longdiv():
    f = Fig(330, 210)
    L, d = 70, 24
    f.text(L, 30 + d, '3x² − 7x + 4', 17, INK, 'start').line(L - 6, 12 + d, L - 6, 40 + d, INK, 2).line(L - 6, 12 + d, 200, 12 + d, INK, 2)
    f.text(L - 12, 30 + d, 'x − 1', 17, BLUE, 'end')
    f.g('k1 k2 k3', 'k1').text(L + 50, 26, '3x', 16, RED, 'start').end()
    f.g('k3', 'k3').text(L + 92, 26, '− 4', 16, RED, 'start').end()
    f.g('k2 k3', 'k2').text(L, 62 + d, '3x² − 3x', 17, PURPLE, 'start').line(L, 70 + d, L + 118, 70 + d, INK, 1.4).text(L + 34, 92 + d, '− 4x + 4', 17, INK, 'start')
    f.text(10, 62 + d, 'subtract', 11.5, GREY, 'start').end()
    f.g('k3', 'k3').text(L + 34, 124 + d, '− 4x + 4', 17, PURPLE, 'start').line(L + 34, 132 + d, L + 118, 132 + d, INK, 1.4)
    f.text(L + 100, 156 + d, '0', 17, GREEN).text(L + 120, 156 + d, 'remainder', 11.5, GREY, 'start').end()
    f.text(230, 26, 'quotient', 12, GREY, 'start').text(230, 54, 'dividend', 12, GREY, 'start')
    f.text(165, 204, 'dividend = divisor × quotient + remainder', 12, GREY)
    return f


def f_cubic():
    p = Plot(-2.6, 2.6, -9, 9, unit=40, uy=10, pad=20, every=1, yevery=2, gstep=1)
    p.fn(lambda x: x ** 3, -2.1, 2.1, BLUE, 2.8, steps=48)
    for x, y in ((-2, -8), (-1, -1), (0, 0), (1, 1), (2, 8)):
        p.pt(x, y, None, c=RED, r=4.2)
    p.text(p.X(2), p.Y(8) - 10, '(2, 8)', 12, RED, 'end').text(p.X(-2) + 6, p.Y(-8) + 4, '(−2, −8)', 12, RED, 'start')
    p.text(p.X(-1.4), p.Y(4), 'y = x³', 14, BLUE, 'start')
    return p


def f_endbeh():
    specs = [(lambda x: x * x - 1, 'a > 0, even', GREEN), (lambda x: x ** 3, 'a > 0, odd', BLUE),
             (lambda x: 1 - x * x, 'a < 0, even', RED), (lambda x: -x ** 3, 'a < 0, odd', PURPLE)]
    ps = []
    for fn, lab, c in specs:
        p = Plot(-1.7, 1.7, -2.4, 2.4, unit=22, uy=18, pad=6, grid=False, labels=False, xlab='', ylab='')
        p.fn(fn, -1.6, 1.6, c, 3, steps=30)
        ps.append(p)
    return side_by_side(ps, 8, ['both up', 'down, up', 'both down', 'up, down'])


def f_cubic3():
    p = Plot(-3, 4, -6, 10, unit=40, uy=11, pad=20, every=1, yevery=2, gstep=1)
    p.fn(lambda x: x ** 3 - 2 * x * x - 5 * x + 6, -2.4, 3.6, BLUE, 2.8, steps=50)
    for x in (-2, 1, 3):
        p.pt(x, 0, None, c=RED, r=4.4)
    p.pt(0, 6, None, c=GREEN, r=4.2).text(p.X(0) + 8, p.Y(6) - 6, '(0, 6)', 12, GREEN, 'start')
    p.pt(-0.79, 8.2, None, c=ORANGE, r=4).pt(2.12, -4.06, None, c=ORANGE, r=4)
    p.text(p.X(-0.79), p.Y(8.2) - 9, 'turning point', 11.5, ORANGE).text(p.X(2.12) + 10, p.Y(-4.06) + 14, 'turning point', 11.5, ORANGE, 'start')
    return p


DIAGRAMS = {
    'anatomy': (f_anatomy(), 'The parts of a polynomial', 170),
    'square': (f_square(), '(a + b)² as an area', 179),
    'longdiv': (f_longdiv(), 'Long division: (3x² − 7x + 4) ÷ (x − 1)', 184),
    'cubic': (f_cubic(), 'Fig. 8.2: y = x³', 188),
    'endbeh': (f_endbeh(), 'End behaviour from the leading term', 191),
    'cubic3': (f_cubic3(), 'Fig. 8.3: y = x³ − 2x² − 5x + 6', 190),
}

# ------------------------------------------------------------------ 8.1
L1 = [
    T('=math9-u8-c01', '8.1 What is a polynomial?', 169,
      'A **polynomial** in $x$ is a sum of terms $a x^n$ where each $a$ is a real number and each exponent $n$ is a **whole number** (0, 1, 2, …): $$a_n x^n + a_{n-1}x^{n-1} + \\dots + a_1 x + a_0, \\quad a_n \\ne 0$$',
      'Examples from a cube of side $x$: perimeter of the base $4x$ (linear), base area $x^2$ (quadratic), volume $x^3$ (cubic).',
      '- **Degree** = the highest power ($n$). **Leading coefficient** = $a_n$. **Constant term** = $a_0$.',
      '- **Standard form**: powers in decreasing order: $-11x^7 - 2x^6 + 0.5x^3 - 12x + 9$.',
      '- **Like terms** have the same variables with the same powers ($3x^2$ and $-5x^2$); $3x^2$ and $3x^4$ are unlike.',
      '- By number of terms: **monomial** (1), **binomial** (2), **trinomial** (3).',
      'The zero polynomial 0 has **no degree**.'),
    DG('anatomy', 'Naming the parts', 170, 'anatomy'),
    TB('notpoly-t', 'Polynomial or not?', 172, ['Expression', 'Polynomial?', 'Why'],
       [['$3x^2 + 11$', 'yes', 'whole-number powers'], ['$3x^{-2} + 4$', 'no', 'negative exponent'],
        ['$\\frac{1}{x} + \\frac{1}{x^2}$', 'no', 'same as $x^{-1} + x^{-2}$'], ['$5\\sqrt{x}$', 'no', '$x^{\\frac{1}{2}}$ is not a whole power'],
        ['$\\sqrt{3}x^5 - 2x^2$', 'yes', 'a coefficient may be any real number'], ['$\\log_2(x + 4)$', 'no', 'not built from powers of $x$'],
        ['$\\frac{3x^2 + 6x - 12}{6}$', 'yes', '$= \\frac{1}{2}x^2 + x - 2$'], ['$-8$', 'yes', 'a constant (degree 0)']],
       'Test: only the **variable\'s exponents** must be whole numbers; coefficients may be fractions, decimals or roots.'),
    'math9-u8-tbl1',
    WK('ex-81a', 'Worked example: Exercise 8.1 Q3', 171,
       'For $-2x^6 + 0.5x^3 - 11x^7 + 9 - 12x$: write it in standard form and give the degree, leading coefficient, constant term and the coefficients of $x^6$, $x^5$, $x^4$, $x^2$.',
       ['Standard form: $-11x^7 - 2x^6 + 0.5x^3 - 12x + 9$.', 'Degree 7; leading coefficient $-11$; constant term 9.', 'Coefficient of $x^6$ is $-2$; $x^5$, $x^4$ and $x^2$ are missing, so their coefficients are 0.'],
       'degree 7, leading coefficient −11, constant 9'),
    WK('ex-81b', 'Worked example: evaluating a polynomial', 173,
       'Evaluate (a) $3x^2 - 5x + 7$ at $x = -1$ (b) $2x^4 - 5$ at $x = -2$ (c) $a^{17} + a^{20}$ at $a = -1$.',
       ['(a) $3(1) - 5(-1) + 7 = 3 + 5 + 7 = 15$.', '(b) $2(16) - 5 = 27$.', '(c) $(-1)^{17} = -1$, $(-1)^{20} = 1$, sum $= 0$.'],
       '15, 27, 0'),
]

# ------------------------------------------------------------------ 8.2
L2 = [
    T('=math9-u8-c02', '8.2.1 Adding polynomials', 173,
      'You can only add **like terms** (8 goats + 4 goats = 12 goats, but 8 goats + 4 dogs stays as it is): add their **coefficients**, keep the power.',
      '**Horizontal:** group like terms: $(x^2 - 5x - 7) + (7x^2 - 4x + 10) = 8x^2 - 9x + 3$.',
      '**Vertical:** write in standard form, line up equal powers (use $0x^k$ for gaps) and add the columns.',
      'Common mistake (Activity 8.3): $3x^3 + 4x^2$ is **not** $7x^5$ — unlike terms cannot be combined, and powers are never added when you add.'),
    T('=math9-u8-c03', '8.2.2 Subtracting polynomials', 175,
      'Subtracting = adding the **opposite**: change the sign of **every** term of the polynomial being subtracted, then add.',
      '$(2x^3 + x^2 - 7x - 2) - (5x^2 + 6x - 4) = 2x^3 + x^2 - 7x - 2 - 5x^2 - 6x + 4 = 2x^3 - 4x^2 - 13x + 2$.',
      '"Subtract $A$ from $B$" means $B - A$ (the order is reversed in words!).',
      'The usual error is changing only the first sign: $(x^2 - 4x + 4) - (x^2 + 5x - 1) \\ne x^2 - 4x + 4 - x^2 + 5x - 1$.'),
    WK('ex-82a', 'Worked example: subtract −3m² + 5m + 9 from 7m³ − 4m + 11', 176,
       'Subtract $-3m^2 + 5m + 9$ from $7m^3 - 4m + 11$.',
       ['Order: $(7m^3 - 4m + 11) - (-3m^2 + 5m + 9)$.', 'Change every sign of the second: $7m^3 - 4m + 11 + 3m^2 - 5m - 9$.', 'Collect: $7m^3 + 3m^2 - 9m + 2$.'],
       '$7m^3 + 3m^2 - 9m + 2$'),
    T('=math9-u8-c04', '8.2.3 Multiplying polynomials', 176,
      '**Monomial × monomial:** multiply coefficients, **add** exponents of the same variable: $(-2x^3)(4x^2) = -8x^5$; $(2ab^2)(3a^2b) = 6a^3b^3$.',
      '**Monomial × polynomial:** distribute: $-7x(-3 + 2x) = 21x - 14x^2$.',
      '**Polynomial × polynomial:** multiply **every** term of the first by **every** term of the second, then collect like terms: $(x - 3)(5x - 1) = 5x^2 - x - 15x + 3 = 5x^2 - 16x + 3$.',
      'Check the count: a binomial × trinomial gives $2 \\times 3 = 6$ products before collecting. The degree of a product = sum of the degrees.'),
    TB('box-t', 'Grid (box) method for (3y + 7)(2y² − 5y − 2)', 180, ['×', '$2y^2$', '$-5y$', '$-2$'],
       [['$3y$', '$6y^3$', '$-15y^2$', '$-6y$'], ['$7$', '$14y^2$', '$-35y$', '$-14$']],
       'Add the cells, collecting like terms: $6y^3 + (-15 + 14)y^2 + (-6 - 35)y - 14 = 6y^3 - y^2 - 41y - 14$.'),
    T('special-t', 'Special products', 178,
      '- **Sum × difference:** $(a + b)(a - b) = a^2 - b^2$. The middle terms cancel: $(5x + 3)(5x - 3) = 25x^2 - 9$.',
      '- **Square of a sum:** $(a + b)^2 = a^2 + 2ab + b^2$: $(x + 3)^2 = x^2 + 6x + 9$.',
      '- **Square of a difference:** $(a - b)^2 = a^2 - 2ab + b^2$: $(2x - 3y)^2 = 4x^2 - 12xy + 9y^2$.',
      'Mental arithmetic: $59 \\times 61 = (60 - 1)(60 + 1) = 3600 - 1 = 3599$; $103^2 = 10\\,000 + 600 + 9 = 10\\,609$.',
      '**Biggest mistake:** $(a + b)^2 \\ne a^2 + b^2$ — you forget $2ab$. Check: $(2 + 3)^2 = 25$ but $4 + 9 = 13$.'),
    ST('square', 'Why (a + b)² has a middle term', 179, 'square',
       [('Draw a square of side $a + b$. Its area is $(a + b)^2$.', 'k1'), ('Cut it: one $a \\times a$ square, one $b \\times b$ square and **two** $a \\times b$ rectangles.', 'k2'),
        ('Total: $a^2 + 2ab + b^2$. The two rectangles are the $2ab$ that people forget.', 'k3')]),
    TB('spec-t', 'Special products at a glance', 180, ['Pattern', 'Result', 'Example'],
       [['$(a + b)(a - b)$', '$a^2 - b^2$', '$(7 - 4y)(7 + 4y) = 49 - 16y^2$'], ['$(a + b)^2$', '$a^2 + 2ab + b^2$', '$(2m + 5)^2 = 4m^2 + 20m + 25$'],
        ['$(a - b)^2$', '$a^2 - 2ab + b^2$', '$(6 - 5v)^2 = 36 - 60v + 25v^2$'], ['$(a - b)(a^2 + ab + b^2)$', '$a^3 - b^3$', '$(x - 2)(x^2 + 2x + 4) = x^3 - 8$']],
       'The last row (Exercise 8.7 Q2, Q3) is a bonus pattern.'),
    T('=math9-u8-c05', '8.2.4 Dividing polynomials', 181,
      '**By a monomial:** split the fraction and divide each term (subtract exponents): $\\frac{6x^3 - 15x^2 + 12x}{3x} = 2x^2 - 5x + 4$ ($x \\ne 0$).',
      '**By factorising:** if the dividend factorises with the divisor as a factor, cancel it: $(x^2 + 7x + 10) \\div (x + 5) = \\frac{(x + 5)(x + 2)}{x + 5} = x + 2$.',
      '**Long division** (always works): 1. Write both in standard form and insert $0x^k$ for missing powers. 2. Divide the first term by the first term. 3. Multiply back and **subtract**. 4. Bring down and repeat. 5. Stop when the remainder\'s degree is **less** than the divisor\'s.',
      'Check: **dividend = divisor × quotient + remainder**. (The textbook says division "makes sense only when the degree of the dividend is equal to or less than" the divisor\'s — it is the other way round: the dividend\'s degree must be **at least** the divisor\'s.)'),
    ST('longdiv', 'Long division step by step (Activity 8.13)', 184, 'longdiv',
       [('$3x^2 \\div x = 3x$: the first term of the quotient.', 'k1'),
        ('Multiply $3x(x - 1) = 3x^2 - 3x$ and subtract: $-4x + 4$ is left.', 'k2'),
        ('$-4x \\div x = -4$; $-4(x - 1) = -4x + 4$; subtract: remainder 0. Quotient $3x - 4$.', 'k3')]),
    WK('ex-82b', 'Worked example: Example 8.3 (missing term)', 185,
       'Find the quotient and remainder for $(-x^2 - 1 + 2x^3) \\div (x^2 - 3)$.',
       ['Standard form with a zero term: $2x^3 - x^2 + 0x - 1$.', '$2x^3 \\div x^2 = 2x$; $2x(x^2 - 3) = 2x^3 - 6x$; subtract: $-x^2 + 6x - 1$.', '$-x^2 \\div x^2 = -1$; $-1(x^2 - 3) = -x^2 + 3$; subtract: $6x - 4$.', 'Degree 1 < 2, stop. Check: $(x^2 - 3)(2x - 1) + 6x - 4 = 2x^3 - x^2 - 6x + 3 + 6x - 4$ (correct).'],
       'quotient $2x - 1$, remainder $6x - 4$'),
    WK('ex-82c', 'Worked example: Exercise 8.9 Q5 (rebuild the dividend)', 185,
       'A polynomial divided by $3x^2 - 2x + 1$ gives quotient $5x - 4$ and remainder $-7x + 9$. Find it.',
       ['Dividend $= (3x^2 - 2x + 1)(5x - 4) + (-7x + 9)$.', 'Product: $15x^3 - 12x^2 - 10x^2 + 8x + 5x - 4 = 15x^3 - 22x^2 + 13x - 4$.', 'Add the remainder: $15x^3 - 22x^2 + 6x + 5$.'],
       '$15x^3 - 22x^2 + 6x + 5$'),
]

# ------------------------------------------------------------------ 8.3
L3 = [
    T('=math9-u8-c06', '8.3 Graphs of polynomial functions', 186,
      'A **polynomial function** is $y = a_n x^n + \\dots + a_1 x + a_0$. Degree 1 → straight line; degree 2 → parabola; degree 3 → an S-shaped **cubic**.',
      '**Drawing $y = x^3$:** make a table ($x = -2, -1.5, \\dots, 2$ gives $y = -8, -3.4, -1, -0.13, 0, 0.13, 1, 3.4, 8$), plot and join with a smooth curve.',
      'Facts about $y = x^3$: domain and range are all real numbers; it always rises; it passes through $(0, 0)$ only, but looks flat near 0 because small numbers cubed are tiny ($0.5^3 = 0.125$).',
      '**$y = ax^3 + b$:** $b$ moves the graph up or down (y-intercept $b$); $a > 0$ rises left to right, $a < 0$ falls.'),
    DG('cubic', 'The basic cubic', 188, 'cubic'),
    T('endb-t', 'End behaviour and the leading term', 191,
      'For large $|x|$ the leading term $a_n x^n$ dominates, so it decides where the two ends of the graph go:',
      '- $a_n > 0$, $n$ even: both ends **up** (has a lowest point), e.g. $y = x^2 - 4$.',
      '- $a_n > 0$, $n$ odd: left **down**, right **up**, e.g. $y = \\frac{1}{2}x^3 + 2$.',
      '- $a_n < 0$, $n$ even: both ends **down** (has a highest point), e.g. $y = -x^2 + 4$.',
      '- $a_n < 0$, $n$ odd: left **up**, right **down**, e.g. $y = -\\frac{1}{2}x^3$.',
      'Reading a graph backwards: ends the same way → even degree; ends opposite → odd degree. Right end up → $a_n > 0$.'),
    DG('endbeh', 'Four possible end shapes', 191, 'endbeh'),
    DG('cubic3', 'Reading a cubic graph (Activity 8.16 Q3)', 190, 'cubic3',
       'x-intercepts $-2$, 1, 3 (check: $f(1) = 1 - 2 - 5 + 6 = 0$). y-intercept 6 (the constant term). Two turning points near $x \\approx -0.8$ and $x \\approx 2.1$. The right end rises, the left end falls → odd degree, positive leading coefficient. Domain and range: all real numbers.'),
    TB('count-t', 'How many x-intercepts and turning points?', 194, ['Degree', 'x-intercepts', 'Turning points'],
       [['1', 'exactly 1', '0'], ['2', '0, 1 or 2', 'exactly 1'], ['3', '1, 2 or 3 (never 0)', '0 or 2']],
       'A cubic must cross the x-axis at least once because its ends go in opposite directions. $y = x^3 - 8$ has only one x-intercept ($x = 2$).'),
    WK('ex-83a', 'Worked example: Exercise 8.10 Q6', 196,
       '$y = ax^3 + b$ passes through $(-1, 5)$ and $(1, 1)$. Find $a$ and $b$.',
       ['$(-1, 5)$: $-a + b = 5$. $(1, 1)$: $a + b = 1$.', 'Add: $2b = 6$, $b = 3$; then $a = -2$.', '$y = -2x^3 + 3$: falls left to right, y-intercept 3.'],
       '$a = -2$, $b = 3$'),
    WK('ex-83b', 'Worked example: Review Q10', 198,
       'A quadratic has y-intercept $-5$ and passes through $(-1, 0)$ and $(5, 0)$. Find it.',
       ['Roots $-1$ and 5: $y = a(x + 1)(x - 5)$.', 'y-intercept: $a(1)(-5) = -5$, so $a = 1$.', '$y = x^2 - 4x - 5$ (opens upward, vertex at $x = 2$, $y = -9$).'],
       '$y = x^2 - 4x - 5$'),
    RM('=math9-u8-c07', 'Unit summary', 198,
       'Degree = highest power; add/subtract like terms only; to subtract change **every** sign.',
       '$(a + b)(a - b) = a^2 - b^2$, $(a \\pm b)^2 = a^2 \\pm 2ab + b^2$.',
       'Dividend = divisor × quotient + remainder.',
       'Ends of the graph: even degree → same direction; odd → opposite; sign of $a_n$ decides which.'),
]

LESSONS = {'math9-u8-l8-1': L1, 'math9-u8-l8-2': L2, 'math9-u8-l8-3': L3}

# ------------------------------------------------------------------ practice
a = QSet('8.1 Practice — polynomials', 's81')
a.S(171, 'For $4x^3 - 7x - 5$ give the degree and the coefficients of $x^3$, $x^2$, $x$, and the constant term.', '3; 4, 0, $-7$; $-5$',
    ['Step 1: highest power 3.', 'Step 2: no $x^2$ term → 0.', 'Step 3: keep the signs.'], 'Signs belong to the coefficient.', [('Same for $x^2 - 5x - 7$?', 'degree 2; 1, $-5$; $-7$.')])
a.S(171, 'Like or unlike? (a) $3x$, $3y$ (b) $5x^2$, $-2x^2$ (c) $5x^7$, $5x^2$', 'unlike, like, unlike',
    ['Step 1: same letter AND same power needed.'], 'Coefficients do not matter.', [('$k^3$ and $7k^3$?', 'like.')])
a.S(172, 'For $3m^7 - \\frac{2}{3}m^2 + 5m^{10} - 2m + 1$ give the degree, leading coefficient, coefficient of $m^9$ and constant term.', '10; 5; 0; 1',
    ['Step 1: standard form $5m^{10} + 3m^7 - \\frac{2}{3}m^2 - 2m + 1$.', 'Step 2: read off.'],
    'Missing power → coefficient 0.', [('Degree of $-3x^2 + 7x^5 - 2x - x^3$?', '5 (leading coefficient 7).')])
a.S(172, 'Which are polynomials? (a) $3x^{-2} + 4$ (b) $-8x^2 + 11x + x^{40} - 3$ (c) $2\\sqrt{x}$ (d) $\\sqrt{3}x^5 - 2x^2$', '(b) and (d)',
    ['Step 1: (a) negative power — no.', 'Step 2: (b) whole powers — yes.', 'Step 3: (c) power ½ — no.', 'Step 4: (d) root only in a coefficient — yes.'],
    'Check the exponents of the variable only.', [('Is $\\frac{1}{x}$ a polynomial?', 'No.')])
a.S(172, 'Classify: (a) $x^4 - 8x^3$ (b) $-8$ (c) $7x^5 - 0.4x^3 + 5x - 3$', 'binomial, monomial, neither (4 terms)',
    ['Step 1: count the terms.'], 'More than 3 terms has no special name here.', [('$x^2 - 9$?', 'binomial.')])
a.S(173, 'Evaluate (a) $x^2 - 3$ at $x = 5$ (b) $-t^3 + 3t - 5$ at $t = 2$ (c) $2x^4 - 5$ at $x = -2$.', '22, $-7$, 27',
    ['Step 1: $25 - 3 = 22$.', 'Step 2: $-8 + 6 - 5 = -7$.', 'Step 3: $32 - 5 = 27$.'], 'Brackets around negatives.', [('$3x^2 - 5x + 7$ at $x = -1$?', '15.')])
a.TF(197, 'The degree of $x^2 + 3x - 5x^3 + 4$ is 2.', False, ['Step 1: highest power is 3 (from $-5x^3$).'], 'Look at every term, not just the first.', [('Is $4r^2$ and $5t^2$ like?', 'No (different letters).')])
a.S(198, 'Give (a) a monomial of degree 7 with negative leading coefficient (b) a binomial of degree 4 with constant term 0.', 'e.g. $-2x^7$; $x^4 + 3x$',
    ['Step 1: one term, power 7, negative coefficient.', 'Step 2: two terms, top power 4, no constant.'], 'Many answers are possible.', [('A degree 2 polynomial never equal to 0?', 'e.g. $x^2 + 1$.')])

b = QSet('8.2 Practice — operations', 's82')
b.S(174, 'Add $(-5x^3 - 11x^2 + 8x - 6) + (8x^3 + 9x^2 - 12x - 5)$.', '$3x^3 - 2x^2 - 4x - 11$',
    ['Step 1: $x^3$: $-5 + 8 = 3$.', 'Step 2: $x^2$: $-11 + 9 = -2$; $x$: $8 - 12 = -4$; constants $-11$.'], 'Line up like terms.', [('$(x^2 - 5x - 7) + (7x^2 - 4x + 10)$?', '$8x^2 - 9x + 3$.')])
b.S(174, 'Add $(3n^2 - 4n + 13) + (n^3 - 2n^2 + 5n) + (-3n^3 + 4n^2 + 6n - 14)$.', '$-2n^3 + 5n^2 + 7n - 1$',
    ['Step 1: $n^3$: $1 - 3 = -2$.', 'Step 2: $n^2$: $3 - 2 + 4 = 5$; $n$: $-4 + 5 + 6 = 7$; constants $13 - 14 = -1$.'], 'Tick off terms as you use them.', [('$(x + 2) + (x - 7)$?', '$2x - 5$.')])
b.S(176, 'Subtract: $(2y^2 - 3y - 8) - (y^2 + 4y - 1)$.', '$y^2 - 7y - 7$',
    ['Step 1: change signs: $2y^2 - 3y - 8 - y^2 - 4y + 1$.', 'Step 2: collect.'], 'Every sign in the second bracket flips.', [('$(2x^3 - 4x - 3) - (x^2 - 2x + 5)$?', '$2x^3 - x^2 - 2x - 8$.')])
b.S(176, 'Simplify $4(y^2 + 5y) - 2(y - 3)$.', '$4y^2 + 18y + 6$',
    ['Step 1: $4y^2 + 20y - 2y + 6$.', 'Step 2: $4y^2 + 18y + 6$.'], '$-2 \\times -3 = +6$.', [('$3(x - 1) - (x + 2)$?', '$2x - 5$.')])
b.M(176, '$(-2x^3)(4x^2) = $', ['$-8x^6$', '$-8x^5$', '$2x^5$', '$8x^5$'], 'B',
    ['Step 1: $-2 \\times 4 = -8$.', 'Step 2: $x^{3 + 2} = x^5$.'], 'Multiply → add exponents.', [('$(5x^4)(4x^3)$?', '$20x^7$.')])
b.S(177, 'Expand $(3x - 5)(2x + 8)$.', '$6x^2 + 14x - 40$',
    ['Step 1: $6x^2 + 24x - 10x - 40$.', 'Step 2: collect: $6x^2 + 14x - 40$.'], 'Four products for two binomials.', [('$(x + 2)(-x + 7)$?', '$-x^2 + 5x + 14$.')])
b.S(181, 'Expand $(x^2 - 5x + 6)(2x - 3)$.', '$2x^3 - 13x^2 + 27x - 18$',
    ['Step 1: $2x^3 - 10x^2 + 12x$.', 'Step 2: $-3x^2 + 15x - 18$.', 'Step 3: add: $2x^3 - 13x^2 + 27x - 18$.'], 'Use the grid method to avoid missing products.', [('$(a - 3)(a^2 + 3a + 9)$?', '$a^3 - 27$.')])
b.S(178, 'Expand (a) $(7 - 4y)(7 + 4y)$ (b) $(3x^2 - 2)(3x^2 + 2)$.', '$49 - 16y^2$; $9x^4 - 4$',
    ['Step 1: sum × difference = square − square.', 'Step 2: $(3x^2)^2 = 9x^4$.'], 'Square the WHOLE term, coefficient included.', [('$(10m - 9n)(10m + 9n)$?', '$100m^2 - 81n^2$.')])
b.S(179, 'Expand (a) $(7w + 4)^2$ (b) $(2x - 3y)^2$.', '$49w^2 + 56w + 16$; $4x^2 - 12xy + 9y^2$',
    ['Step 1: $a^2 = 49w^2$, $2ab = 56w$, $b^2 = 16$.', 'Step 2: $4x^2 - 2(2x)(3y) + 9y^2$.'], 'Middle term = 2 × first × second.', [('$(a + 2)^2$?', '$a^2 + 4a + 4$.')])
b.TF(197, '$(x - 7)^2 = x^2 - 49$', False, ['Step 1: $(x - 7)^2 = x^2 - 14x + 49$.', 'Step 2: check $x = 0$: $49 \\ne -49$.'],
     'Squares of differences have three terms.', [('Is $(60 - 1)(60 + 1) = 3600 - 1$?', 'True.')])
b.S(182, 'Divide $10x^7 - 5x^5 + 15x^2$ by $5x^2$.', '$2x^5 - x^3 + 3$',
    ['Step 1: divide each term: $\\frac{10x^7}{5x^2} = 2x^5$, $\\frac{-5x^5}{5x^2} = -x^3$, $\\frac{15x^2}{5x^2} = 3$.'], 'Split the fraction.', [('$12x^3 + 9x^2 - 21x$ by $3x$?', '$4x^2 + 3x - 7$.')])
b.S(183, 'Divide by factorising: (a) $(x^2 - 25) \\div (x + 5)$ (b) $(6u^2 + u - 1) \\div (3u - 1)$.', '$x - 5$; $2u + 1$',
    ['Step 1: $x^2 - 25 = (x + 5)(x - 5)$.', 'Step 2: $6u^2 + u - 1 = (3u - 1)(2u + 1)$.'], 'Factorise, then cancel the divisor.', [('$(4y^2 - 9) \\div (2y - 3)$?', '$2y + 3$.')])
b.S(185, 'Find the quotient and remainder: $(x^2 + 7x + 13) \\div (x + 5)$.', '$x + 2$, remainder 3',
    ['Step 1: $x$; $x(x + 5) = x^2 + 5x$; left $2x + 13$.', 'Step 2: $2$; $2(x + 5) = 2x + 10$; left 3.'], 'Stop when the remainder has lower degree.', [('$(x^3 + 8) \\div (x + 2)$?', '$x^2 - 2x + 4$, remainder 0.')])
b.S(185, 'Quotient and remainder: $(5x^4 - 3x^2 - 9) \\div (-x^2 + 2)$.', '$-5x^2 - 7$, remainder 5',
    ['Step 1: $5x^4 \\div (-x^2) = -5x^2$; $-5x^2(-x^2 + 2) = 5x^4 - 10x^2$; left $7x^2 - 9$.', 'Step 2: $7x^2 \\div (-x^2) = -7$; $-7(-x^2 + 2) = 7x^2 - 14$; left 5.'],
    'Watch the negative leading term of the divisor.', [('$(x^4 - 5) \\div (x + 1)$?', '$x^3 - x^2 + x - 1$, remainder $-4$.')])
b.S(198, 'Review Q8(a): $(5x^3 + 3x - 9) \\div (x^2 + x - 2)$.', '$5x - 5$, remainder $18x - 19$',
    ['Step 1: insert $0x^2$: $5x^3 + 0x^2 + 3x - 9$.', 'Step 2: $5x$: subtract $5x^3 + 5x^2 - 10x$ → $-5x^2 + 13x - 9$.', 'Step 3: $-5$: subtract $-5x^2 - 5x + 10$ → $18x - 19$.'],
    'Insert zero terms first.', [('$(3x^3 + 7x^2 - 7x - 3) \\div (x^2 + 2x - 3)$?', '$3x + 1$, remainder 0.')])
b.S(198, 'Divided by $5x^2 + 3x - 2$, a polynomial gives quotient $-3x + 1$ and remainder 10. Find it.', '$-15x^3 - 4x^2 + 9x + 8$',
    ['Step 1: $(5x^2 + 3x - 2)(-3x + 1) = -15x^3 + 5x^2 - 9x^2 + 3x + 6x - 2$.', 'Step 2: $= -15x^3 - 4x^2 + 9x - 2$; add 10.'], 'Dividend = divisor × quotient + remainder.', [('Room area $x^2 + 4x + 3$, length $x + 3$: width?', '$x + 1$.')])

c = QSet('8.3 Practice — graphs', 's83')
c.S(189, 'For $y = x^3$: give the domain, range and intercepts. Does the graph go up or down for $x > 0$?', 'all reals; all reals; (0, 0); up',
    ['Step 1: any $x$ can be cubed.', 'Step 2: every real number is a cube.', 'Step 3: $x^3 = 0$ only at 0.'], 'A cubic covers all $y$ values.', [('Range of $y = x^2$?', '$y \\ge 0$.')])
c.S(190, 'How is $y = x^3 + 1$ related to $y = x^3$? Give its intercepts.', 'shifted up 1; y-int 1, x-int $-1$',
    ['Step 1: add 1 to every y.', 'Step 2: $x^3 + 1 = 0 \\Rightarrow x = -1$.'], '$+b$ moves up by $b$.', [('$y = x^3 - 1$?', 'down 1; x-intercept 1.')])
c.M(191, 'The ends of $y = -2x^4 + x$ are', ['both up', 'both down', 'left down, right up', 'left up, right down'], 'B',
    ['Step 1: leading term $-2x^4$: even, negative.', 'Step 2: both ends down.'], 'Only the leading term matters.', [('$y = 3x^5 - x$?', 'left down, right up.')])
c.S(194, 'Can a third-degree polynomial have no x-intercept? Give an example of one with three.', 'No; e.g. $y = x(x - 1)(x + 1)$',
    ['Step 1: its ends go opposite ways, so it must cross the x-axis.', 'Step 2: $x(x - 1)(x + 1) = x^3 - x$ crosses at $-1, 0, 1$.'],
    'Build from factors.', [('Fourth-degree with no x-intercept?', 'e.g. $y = x^4 + 1$.')])
c.TF(195, 'The graph of $y = (x - 2)^2(x + 3)$ has x-intercepts at $-2$ and 3.', False,
     ['Step 1: set each factor to zero: $x = 2$, $x = -3$.'], 'Factor $(x - k)$ ↔ intercept $+k$.', [('Intercepts of $y = (x + 1)(x - 4)$?', '$-1$ and 4.')])
c.TF(195, 'The y-intercept of $y = 3x^3 - 7x^2 + 8x - 9$ is 9.', False, ['Step 1: put $x = 0$: $y = -9$.'], 'y-intercept = constant term, with its sign.', [('y-intercept of $y = x^3 - 2x^2$?', '0.')])
c.S(196, 'A cubic and a quadratic: what is the degree of their sum, and of their product?', '3; 5',
    ['Step 1: the $x^3$ term cannot cancel, so the sum has degree 3.', 'Step 2: product: $3 + 2 = 5$.'], 'Sum → highest; product → add degrees.', [('Two cubics $x^3 + x$ and $-x^3 + 2$: degree of the sum?', '1 (the $x^3$ cancel).')])
c.S(190, 'From the graph of $y = x^3 - 2x^2 - 5x + 6$, list the x-intercepts and the y-intercept, and verify one intercept.', '$-2$, 1, 3; y-int 6',
    ['Step 1: read the crossings.', 'Step 2: $f(3) = 27 - 18 - 15 + 6 = 0$ (correct).'], 'Always check an intercept by substitution.', [('Is $x = 2$ an intercept?', 'No, $f(2) = -4$.')])
c.S(196, 'Which could be the equation of a graph whose left end goes up, right end goes down and y-intercept is 3: $y = -2x^3 + 3$, $y = -2x^2 + 3$, $y = x^3 + 3$?', '$y = -2x^3 + 3$',
    ['Step 1: ends opposite → odd degree.', 'Step 2: right end down → negative leading coefficient.'], 'Ends first, then intercepts.', [('Both ends down, y-intercept 3?', '$y = -2x^2 + 3$.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Polynomial', 'A sum of terms $ax^n$ with whole-number exponents.', 170), ('Degree', 'The highest power of the variable.', 170),
    ('Leading coefficient', 'The coefficient of the highest power term.', 170), ('Constant term', 'The term with no variable.', 170),
    ('Like terms', 'Terms with the same variables raised to the same powers.', 171), ('Standard form', 'Terms written in decreasing powers.', 171),
    ('Monomial / binomial / trinomial', 'A polynomial with 1 / 2 / 3 terms.', 171),
    ('Quotient and remainder', 'Dividend = divisor × quotient + remainder.', 184),
    ('End behaviour', 'Where the graph goes for very large positive or negative $x$.', 191),
]
TIPS = [('To subtract, change the sign of EVERY term in the second bracket.', 175), ('(a + b)² = a² + 2ab + b² — never forget 2ab.', 179),
        ('Insert 0xᵏ for missing powers before long division.', 184)]
IDEAS = [('spec', 'Special products', 'l8_2', 'math9-u8-md-spec-t'), ('count', 'Intercepts and turning points', 'l8_3', 'math9-u8-md-count-t')]
