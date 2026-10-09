r"""Grade 11 Unit 3 — Rational Functions: domain/range, symmetry, asymptotes, sketching, operations, equations, inequalities (pp. 71-141)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side, with_legend

UID = 'math11-u3'
set_unit(UID)


def safe(f):
    def g(x):
        try:
            return f(x)
        except ZeroDivisionError:
            return None
    return g


# ------------------------------------------------------------------ figures
def f_recip():
    p = Plot(-5, 5, -5, 5, unit=26, uy=22, every=1, yevery=1, gstep=1)
    p.g('k1 k2 k3').fn(safe(lambda x: 1 / x), -5, -0.2, BLUE, 2.8, steps=40).fn(safe(lambda x: 1 / x), 0.2, 5, BLUE, 2.8, steps=40).end()
    p.g('k2 k3').seg((0, -5), (0, 5), RED, 2, dash='6 4').text(p.X(0) + 6, p.Y(-4.4), 'x = 0', 12, RED, 'start').end()
    p.g('k3').seg((-5, 0), (5, 0), PURPLE, 2, dash='6 4').text(p.X(-4.2), p.Y(0) - 8, 'y = 0', 12, PURPLE).end()
    p.text(p.X(2.6), p.Y(2.2), 'y = 1/x', 12.5, BLUE, 'start')
    return p


def f_sym():
    a = Plot(-2, 2, -1, 3, unit=34, uy=30, pad=12, every=1, yevery=1, gstep=1, xlab='', ylab='')
    a.fn(lambda x: x ** 4 - 2 * x * x + 1, -1.85, 1.85, BLUE, 2.6, steps=40)
    a.pt(1.5, 1.5625, None, c=RED, r=4).pt(-1.5, 1.5625, None, c=RED, r=4)
    a.seg((-1.5, 1.5625), (1.5, 1.5625), RED, 1.4, dash='3 3')
    b = Plot(-3, 3, -4, 4, unit=24, uy=15, pad=12, every=1, yevery=2, gstep=1, xlab='', ylab='')
    b.fn(lambda x: x ** 3 - 4 * x, -2.6, 2.6, GREEN, 2.6, steps=40)
    b.pt(1, -3, None, c=RED, r=4).pt(-1, 3, None, c=RED, r=4)
    b.seg((-1, 3), (1, -3), RED, 1.4, dash='3 3')
    return side_by_side([a, b], 14, ['even: mirror in y-axis', 'odd: half-turn about O'])


def f_ex18():
    p = Plot(-5, 5, -4, 4, unit=28, uy=22, every=1, yevery=1, gstep=1)
    f = safe(lambda x: x / (x * x - 4))
    p.g('k1 k2 k3').seg((-2, -4), (-2, 4), RED, 1.8, dash='6 4').seg((2, -4), (2, 4), RED, 1.8, dash='6 4')
    p.seg((-5, 0), (5, 0), PURPLE, 1.8, dash='6 4').pt(0, 0, None, c=INK, r=4.2).end()
    p.g('k2 k3').fn(f, -5, -2.06, BLUE, 2.8, steps=36).end()
    p.g('k3').fn(f, -1.94, 1.94, BLUE, 2.8, steps=36).fn(f, 2.06, 5, BLUE, 2.8, steps=36).end()
    p.text(p.X(-2) - 4, p.Y(3.5), 'x = −2', 11.5, RED, 'end').text(p.X(2) + 4, p.Y(3.5), 'x = 2', 11.5, RED, 'start')
    return p


def f_ex19():
    p = Plot(-6, 6, -4, 7, unit=24, uy=19, every=1, yevery=1, gstep=1)
    f = safe(lambda x: 2 * (x - 1) / x)
    p.seg((0, -4), (0, 7), RED, 1.8, dash='6 4').seg((-6, 2), (6, 2), PURPLE, 1.8, dash='6 4')
    p.fn(f, -6, -0.4, BLUE, 2.8, steps=40).fn(f, 0.3, 6, BLUE, 2.8, steps=40)
    p.pt(-2, 3, None, c=ORANGE, r=4.6, open_=True).text(p.X(-3.6), p.Y(4.6), 'hole (−2, 3)', 11.5, ORANGE)
    p.pt(1, 0, None, c=INK, r=4.2).text(p.X(4.6), p.Y(2) - 8, 'y = 2', 11.5, PURPLE).text(p.X(0) - 6, p.Y(-3.5), 'x = 0', 11.5, RED, 'end')
    return p


def f_ex20():
    p = Plot(-3, 5, -4, 8, unit=30, uy=18, every=1, yevery=2, gstep=1)
    f = safe(lambda x: x * x / (x - 1))
    p.g('k1 k2 k3').seg((1, -4), (1, 8), RED, 1.8, dash='6 4').end()
    p.g('k2 k3').seg((-3, -2), (5, 6), PURPLE, 1.8, dash='6 4').text(p.X(4.1), p.Y(2.8), 'y = x + 1', 11.5, PURPLE).end()
    p.g('k3').fn(f, -3, 0.85, BLUE, 2.8, steps=40).fn(f, 1.12, 5, BLUE, 2.8, steps=40).pt(0, 0, None, c=INK, r=4).pt(2, 4, None, c=GREEN, r=4.2).end()
    return p


def chart(labels, bounds, rows, result, w=340):
    """sign chart: labels per row, boundary values, rows of signs per interval, result row"""
    n = len(bounds) + 1
    h = 40 + 26 * (len(rows) + 1) + 36
    f = Fig(w, h)
    x0, x1 = 92, w - 10
    cw = (x1 - x0) / n
    xs = [x0 + cw * (i + 0.5) for i in range(n)]
    bx = [x0 + cw * (i + 1) for i in range(n - 1)]
    for b in bx:
        f.line(b, 10, b, h - 34, GREY, 1.3, dash='4 3')
    allrows = rows + [result]
    for r, (lab, signs) in enumerate(zip(labels, allrows)):
        y = 30 + 26 * r
        last = r == len(allrows) - 1
        f.g('k3' if last else 'k2 k3')
        f.text(x0 - 8, y, lab, 12, INK if last else BLUE, 'end')
        for x, s in zip(xs, signs):
            f.text(x, y + 1, s, 16 if s in '+−' else 12, (GREEN if s == '+' else RED if s == '−' else INK))
        f.end()
    yl = h - 22
    f.g('k1 k2 k3').arrow(x0 - 4, yl, x1, yl, INK, 1.6, 7)
    for b, t in zip(bx, bounds):
        f.dot(b, yl, INK, 3.6).text(b, yl + 17, t, 12, INK)
    return f.end()


def f_chart42():
    return chart(['x + 7', 'x + 2', 'x − 4', 'quotient'], ['−7', '−2', '4'],
                 [['−', '+', '+', '+'], ['−', '−', '+', '+'], ['−', '−', '−', '+']], ['−', '+', '−', '+'])


DIAGRAMS = {
    'recip': (f_recip(), 'Activity 3.6: y = 1/x and its two asymptotes', 87),
    'sym': (f_sym(), 'Even and odd graphs (Figs 3.4 and 3.6)', 78),
    'ex18': (f_ex18(), 'Example 3.18: y = x / (x² − 4)', 101),
    'ex19': (f_ex19(), 'Example 3.19: a hole and two asymptotes', 102),
    'ex20': (f_ex20(), 'Example 3.20: y = x² / (x − 1) with an oblique asymptote', 104),
    'chart42': (f_chart42(), 'Sign chart for (x + 2) / ((x − 4)(x + 7))', 137),
}

# ------------------------------------------------------------------ 3.1
L1 = [
    T('=math11-u3-c07', '3.1 What is a rational function?', 72,
      'A **rational function** is a quotient of two polynomials: $f(x) = \\frac{P(x)}{Q(x)}$ with $Q(x) \\ne 0$.',
      '**Test:** are the top and bottom both polynomials (whole-number powers of $x$, no roots of $x$, no $x$ in a denominator inside)? Then it is rational.',
      '- $\\frac{3x - 3}{x + 5}$: rational. $\\frac{5}{x^2 + 5x + 3}$: rational (a constant is a polynomial).',
      '- $\\frac{x + 5}{\\sqrt{x + 4}}$: **not** rational (root in the denominator).',
      '- Every polynomial is rational: $x^3 - 2x^2 + 5 = \\frac{x^3 - 2x^2 + 5}{1}$.',
      '**Domain:** all real numbers except the zeros of the denominator. Solve $Q(x) = 0$ and remove those values.'),
    WK('ex-31a', 'Worked example: domains (Example 3.2)', 73,
       'Find the domain of (a) $\\frac{x - 3}{x + 4}$ (b) $\\frac{5x + 2}{6x^2 - 13x + 6}$ (c) $\\frac{4x - 7}{x(x - 2)(x - 3)}$.',
       ['(a) $x + 4 = 0 \\Rightarrow x = -4$: all reals except $-4$.',
        '(b) $6x^2 - 13x + 6 = (3x - 2)(2x - 3) = 0 \\Rightarrow x = \\frac{2}{3}$ or $\\frac{3}{2}$: all reals except $\\frac{2}{3}$ and $\\frac{3}{2}$. (The book\'s last line says "except $\\frac{1}{4}$ and $\\frac{3}{2}$" — a misprint; its own working gives $\\frac{2}{3}$.)',
        '(c) zeros of the denominator: 0, 2, 3.'],
       '(a) $x \\ne -4$ (b) $x \\ne \\frac{2}{3}, \\frac{3}{2}$ (c) $x \\ne 0, 2, 3$'),
    T('range-t', 'Finding the range: two methods (Example 3.3)', 73,
      '$f(x) = \\frac{x - 3}{x - 4}$.',
      '**Method 1 — divide:** $x - 3 = (x - 4) + 1$, so $f(x) = 1 + \\frac{1}{x - 4}$. The fraction $\\frac{1}{x - 4}$ is never 0, so $f(x)$ is never 1. Range: $\\{y : y \\ne 1\\}$.',
      '**Method 2 — inverse:** swap and solve: $x(y - 4) = y - 3 \\Rightarrow y(x - 1) = 4x - 3 \\Rightarrow f^{-1}(x) = \\frac{4x - 3}{x - 1}$. Range of $f$ = domain of $f^{-1}$ = all reals except 1.',
      '**Shortcut for $\\frac{ax + b}{cx + d}$:** the range is all reals except $\\frac{a}{c}$ (the horizontal asymptote).'),
    TB('cmp-31', 'Comparing the two range methods', 74, ['Method', 'Best for', 'Watch out'],
       [['Divide (quotient + remainder)', '$\\frac{ax + b}{cx + d}$, quick', 'remainder fraction can never be 0'],
        ['Inverse function', 'one-to-one functions', 'must be able to solve for $y$'],
        ['Graph / asymptote', 'checking answers', 'a hole also removes a $y$-value']]),
    'math11-u3-c01', 'math11-u3-c02', 'math11-u3-tblE1', 'math11-u3-wrkE2',
]

# ------------------------------------------------------------------ 3.2
L2 = [
    T('=math11-u3-c03', '3.2.1 Even and odd functions', 80,
      '**Even:** $f(-x) = f(x)$ for every $x$ in the domain. The graph is **symmetric about the y-axis** (point $(a, b)$ ⇒ $(-a, b)$).',
      '**Odd:** $f(-x) = -f(x)$. The graph is **symmetric about the origin** (point $(a, b)$ ⇒ $(-a, -b)$; a half-turn).',
      '**Test:** replace $x$ by $-x$ and simplify. Example 3.6: $f(x) = x^3 - 3x$: $f(-x) = -x^3 + 3x = -f(x)$, odd. Example 3.7: $f(x) = \\frac{x^2 - 6}{x^2 + 6}$: $f(-x) = f(x)$, even.',
      '**Quick rule for $\\frac{P(x)}{Q(x)}$** (a constant counts as power 0, even):',
      '- all powers in $P$ and $Q$ even, or all odd → **even**;',
      '- all powers in one even and in the other all odd → **odd**;',
      '- mixed powers anywhere → usually **neither** (test to be sure).'),
    DG('sym', 'The two kinds of symmetry', 78, 'sym',
       'Left: $y = x^4 - 2x^2 + 1$ is even: the points at $x = \\pm 1.5$ have the same height. Right: $y = x^3 - 4x$ is odd: $(1, -3)$ and $(-1, 3)$ are opposite through the origin.'),
    WK('ex-32a', 'Worked example: even, odd or neither?', 81,
       'Classify (a) $\\frac{5x^4 - 7x^2 + 1}{x^2 + 3}$ (b) $\\frac{3x^2 - 5}{x^3 + 6x}$ (c) $\\frac{2x}{x^3 + 3x}$ (d) $\\frac{x^3 + 2x + 1}{x^2 + 1}$.',
       ['(a) powers 4, 2, 0 over 2, 0: all even → even.', '(b) top even (2, 0), bottom odd (3, 1) → odd: symmetric about the origin.',
        '(c) top odd, bottom odd → even (indeed it simplifies to $\\frac{2}{x^2 + 3}$).', '(d) top has 3, 1 and 0: mixed → neither ($f(-1) = -\\frac{1}{2}$, $f(1) = 2$).'],
       'even; odd; even; neither'),
    T('asym-t', '3.2.2 Asymptotes', 87,
      'An **asymptote** is a line that the graph gets closer and closer to as we move far along it. Drawn as a dashed line; it is not part of the graph.',
      '**Vertical asymptote** $x = c$: write $f$ in **lowest terms**; every zero $c$ of the remaining denominator gives $x = c$. Near it, $f(x) \\to \\infty$ or $-\\infty$.',
      '**Hole (point of discontinuity):** a factor that **cancels** from top and bottom gives a hole, not an asymptote. Example 3.12: $\\frac{x + 1}{x^2 - 2x - 3} = \\frac{1}{x - 3}$ ($x \\ne -1$): asymptote $x = 3$, hole at $x = -1$.',
      '**Horizontal asymptote** (compare degrees $m$ of top, $n$ of bottom):',
      '- $m < n$: $y = 0$.  - $m = n$: $y = \\frac{\\text{leading coefficient of top}}{\\text{leading coefficient of bottom}}$.  - $m > n$: none.',
      '**Oblique (slant) asymptote:** when $m = n + 1$, divide: $f(x) = (ax + b) + \\frac{r(x)}{Q(x)}$; the line is $y = ax + b$.'),
    ST('recip', 'Reading the asymptotes of y = 1/x (Activity 3.6)', 87, 'recip',
       [('The graph has two branches and never touches either axis.', 'k1'),
        ('Near $x = 0$ the values blow up: $x = 0.01$ gives 100, $x = -0.01$ gives $-100$. So $x = 0$ is a vertical asymptote.', 'k2'),
        ('Far left and far right the values shrink to 0: $y = 0$ is the horizontal asymptote.', 'k3')]),
    TB('asym-tb', 'Asymptote rules at a glance', 93, ['Situation', 'Asymptote', 'Example'],
       [['remaining denominator $= 0$ at $c$', 'vertical $x = c$', '$\\frac{2}{x + 1}$: $x = -1$'],
        ['factor cancels', 'hole, not asymptote', '$\\frac{x^2 - 25}{x - 5}$: hole at $(5, 10)$'],
        ['deg top < deg bottom', '$y = 0$', '$\\frac{2x}{x^2 + 1}$'],
        ['equal degrees', '$y = $ ratio of leading coefficients', '$\\frac{2x^2}{x^2 + 1}$: $y = 2$'],
        ['deg top = deg bottom + 1', 'oblique $y = $ quotient', '$\\frac{x^2 + 1}{x - 2}$: $y = x + 2$'],
        ['deg top ≥ deg bottom + 2', 'no horizontal or oblique', '$\\frac{x^3 - 8}{x - 1}$']]),
    WK('ex-32b', 'Worked example: oblique asymptotes (Example 3.16)', 96,
       'Find the oblique asymptotes of (a) $\\frac{x^2 + 1}{x - 2}$ (b) $\\frac{2x^3 - x^2 - 5}{x^2 - 3x + 2}$.',
       ['(a) $x^2 + 1 = (x - 2)(x + 2) + 5$, so $f(x) = (x + 2) + \\frac{5}{x - 2}$: asymptote $y = x + 2$. (The book prints "$(x + )$": the 2 is missing.)',
        '(b) long division: $2x^3 - x^2 - 5 = (x^2 - 3x + 2)(2x + 5) + (11x - 15)$, so the asymptote is $y = 2x + 5$ (the book leaves the line out of its last sentence).'],
       '$y = x + 2$; $y = 2x + 5$'),
    T('sketch-t', '3.2.3 Sketching a rational function: the 7 steps', 99,
      '1. **Domain** (zeros of the denominator). 2. **Symmetry** (even / odd).',
      '3. **Intercepts:** x-intercepts from numerator $= 0$ (in lowest terms); y-intercept $f(0)$ if 0 is in the domain.',
      '4. **Holes and asymptotes.** 5. **Behaviour** near each asymptote: test a value just left and right.',
      '6. Plot intercepts, a few extra points, dashed asymptotes and open circles for holes.',
      '7. Join with smooth curves that follow the asymptotic behaviour.'),
    ST('ex18', 'Example 3.18: sketch f(x) = x / (x² − 4)', 99, 'ex18',
       [('Domain $x \\ne \\pm 2$; odd (top odd, bottom even); only intercept $(0, 0)$; asymptotes $x = \\pm 2$ and $y = 0$.', 'k1'),
        ('Left of $-2$: $f(-3) = -\\frac{3}{5}$, negative, and $f \\to -\\infty$ as $x \\to -2$ from the left.', 'k2'),
        ('Middle piece passes through $(0, 0)$, from $+\\infty$ at $-2$ down to $-\\infty$ at 2; the right piece is the half-turn image of the left one.', 'k3')]),
    DG('ex19', 'Example 3.19: f(x) = (2x² + 2x − 4)/(x² + 2x)', 102, 'ex19',
       'Factorise: $\\frac{2(x - 1)(x + 2)}{x(x + 2)} = \\frac{2(x - 1)}{x}$, $x \\ne -2$. Hole at $x = -2$ with $y = \\frac{2(-3)}{-2} = 3$; vertical asymptote $x = 0$; horizontal $y = 2$; x-intercept 1; no y-intercept.'),
    ST('ex20', 'Example 3.20: f(x) = x² / (x − 1)', 103, 'ex20',
       [('Vertical asymptote $x = 1$; intercept $(0, 0)$.', 'k1'),
        ('Divide: $x^2 = (x - 1)(x + 1) + 1$, so $f(x) = x + 1 + \\frac{1}{x - 1}$: oblique asymptote $y = x + 1$.', 'k2'),
        ('For $x > 1$ the extra $\\frac{1}{x - 1} > 0$: the curve is above the line (lowest point $(2, 4)$); for $x < 1$ it is below.', 'k3')]),
    'math11-u3-c08', 'math11-u3-mn2', 'math11-u3-xtra2', 'math11-u3-wrk1',
]

# ------------------------------------------------------------------ 3.3
L3 = [
    T('=math11-u3-c04', '3.3 Operations on rational expressions', 106,
      'A **rational expression** is $\\frac{P}{Q}$ with polynomials $P, Q$ and $Q \\ne 0$. Everything works like ordinary fractions — but **factorise first**.',
      '**Equivalent:** $\\frac{P}{Q} = \\frac{M}{N}$ when $PN = QM$. **Fundamental property:** $\\frac{P}{Q} = \\frac{PK}{QK}$ for $K \\ne 0$.',
      '**Simplify:** factorise top and bottom, cancel common **factors** (never terms), state excluded values. $\\frac{3x^2 - 12}{x^2 - 5x + 6} = \\frac{3(x - 2)(x + 2)}{(x - 2)(x - 3)} = \\frac{3(x + 2)}{x - 3}$, $x \\ne 2, 3$.',
      '**Multiply:** $\\frac{P}{Q} \\cdot \\frac{M}{N} = \\frac{PM}{QN}$ (cancel before multiplying). **Divide:** multiply by the reciprocal: $\\frac{P}{Q} \\div \\frac{M}{N} = \\frac{P}{Q} \\cdot \\frac{N}{M}$.',
      '**Add / subtract:** same denominator → add numerators. Different denominators → use the **LCD**: factorise every denominator and take each factor to its highest power.'),
    TB('ops-tb', 'The four operations', 117, ['Operation', 'Rule', 'Key step'],
       [['Simplify', '$\\frac{PK}{QK} = \\frac{P}{Q}$', 'cancel factors, not terms'],
        ['Multiply', '$\\frac{P}{Q} \\cdot \\frac{M}{N} = \\frac{PM}{QN}$', 'factorise all, cancel across'],
        ['Divide', '$\\frac{P}{Q} \\div \\frac{M}{N} = \\frac{PN}{QM}$', 'flip the second fraction'],
        ['Add / subtract', '$\\frac{P}{Q} \\pm \\frac{K}{Q} = \\frac{P \\pm K}{Q}$', 'LCD first; bracket the numerator you subtract']]),
    WK('ex-33a', 'Worked example: multiply (Example 3.27)', 116,
       'Find $\\frac{x + 2}{x + 4} \\cdot \\frac{x^2 + 2x - 8}{x^2 + 5x + 6}$.',
       ['Factorise: $x^2 + 2x - 8 = (x + 4)(x - 2)$; $x^2 + 5x + 6 = (x + 2)(x + 3)$.', 'Cancel $(x + 2)$ and $(x + 4)$.', 'Result $\\frac{x - 2}{x + 3}$, with $x \\ne -4, -2, -3$.'],
       '$\\frac{x - 2}{x + 3}$'),
    WK('ex-33b', 'Worked example: divide (Example 3.29c)', 119,
       'Find $\\frac{y^2 + y - 12}{y^2 - 8y + 15} \\div \\frac{3y^2 + 7y - 20}{2y^2 - 7y - 15}$.',
       ['Flip: $\\frac{(y + 4)(y - 3)}{(y - 3)(y - 5)} \\cdot \\frac{(2y + 3)(y - 5)}{(3y - 5)(y + 4)}$.', 'Cancel $(y + 4)$, $(y - 3)$, $(y - 5)$.', '$\\frac{2y + 3}{3y - 5}$.'],
       '$\\frac{2y + 3}{3y - 5}$'),
    WK('ex-33c', 'Worked example: subtract with an LCD (Example 3.32b)', 125,
       'Find $\\frac{8}{x^2 - 16} - \\frac{5}{x^2 - 3x - 4}$.',
       ['Denominators $(x - 4)(x + 4)$ and $(x - 4)(x + 1)$; LCD $(x - 4)(x + 4)(x + 1)$. (The book\'s sentence names only $(x - 4)(x + 4)$, but its working uses all three factors.)',
        'Numerator: $8(x + 1) - 5(x + 4) = 3x - 12 = 3(x - 4)$.', 'Cancel $(x - 4)$: $\\frac{3}{(x + 4)(x + 1)}$, $x \\ne 4$.'],
       '$\\frac{3}{(x + 4)(x + 1)}$'),
    RM('rm-33', 'Classic mistakes', 113,
       '$\\frac{x + 3}{x}$ is **not** 3: you may only cancel a whole factor.',
       '$\\frac{a}{b} - \\frac{c - d}{b} = \\frac{a - c + d}{b}$: put brackets around the second numerator.',
       '$\\frac{4w}{2w - 5} + \\frac{10}{5 - 2w}$: write $5 - 2w = -(2w - 5)$, giving $\\frac{4w - 10}{2w - 5} = 2$.'),
    MN('mn-33', 'Memory hook', 117, '**"Factor, Flip, Cancel, Combine."** Factor everything; flip only when dividing; cancel factors; combine numerators over the LCD.'),
    'math11-u3-c09', 'math11-u3-wrk2',
]

# ------------------------------------------------------------------ 3.4
L4 = [
    T('=math11-u3-c05', '3.4.1 Solving rational equations', 128,
      '1. List the values that make any denominator 0 (**excluded values**).',
      '2. Multiply every term by the **LCD**; this clears the fractions.',
      '3. Solve the resulting polynomial equation.',
      '4. Throw away any answer that is an excluded value.',
      'Example 3.33: $\\frac{8}{x - 2} = \\frac{4}{x + 1}$: $8(x + 1) = 4(x - 2) \\Rightarrow x = -4$.',
      'Example 3.35: $\\frac{3x}{x - 3} = 2 + \\frac{9}{x - 3}$: $3x = 2(x - 3) + 9 \\Rightarrow x = 3$, excluded, so **no solution**.'),
    WK('ex-34a', 'Worked example: Example 3.34', 128,
       'Solve $\\frac{x + 1}{x - 3} = \\frac{-4}{x + 3}$.',
       ['Excluded: $\\pm 3$. LCD $(x - 3)(x + 3)$.', '$(x + 1)(x + 3) = -4(x - 3) \\Rightarrow x^2 + 4x + 3 = -4x + 12$.', '$x^2 + 8x - 9 = 0 \\Rightarrow (x + 9)(x - 1) = 0$. Neither is excluded.'],
       '$\\{-9, 1\\}$'),
    T('work-t', 'Word problems: rates and work', 130,
      '**Work:** if a job takes $t$ hours, the rate is $\\frac{1}{t}$ job per hour. Rates add when people work together: $\\frac{T}{t_1} + \\frac{T}{t_2} = 1$ for $T$ hours together.',
      'Example 3.37: Semhar 5 h, together 3 h: $\\frac{3}{5} + \\frac{3}{t} = 1 \\Rightarrow \\frac{3}{t} = \\frac{2}{5} \\Rightarrow t = 7.5$ h for Abdu.',
      '**Motion:** time $= \\frac{\\text{distance}}{\\text{speed}}$. Downstream speed $= v + c$, upstream $v - c$.',
      '**Fractions:** Example 3.36: $\\frac{x - 2}{x + 10} = \\frac{3}{5} \\Rightarrow 5x - 10 = 3x + 30 \\Rightarrow x = 20$: the fraction is $\\frac{20}{26} = \\frac{10}{13}$.'),
    T('=math11-u3-xt4', '3.4.2 Rational inequalities: case method and sign chart', 133,
      '**Case method** for $\\frac{P}{Q} < 0$: top and bottom have **opposite** signs; for $> 0$: the **same** sign. Solve each case and take the union. Example 3.38: $\\frac{x + 2}{x - 1} < 0$: only "$x + 2 > 0$ and $x - 1 < 0$" works: $-2 < x < 1$.',
      '**Sign chart method:** (1) get **0 on one side** and a single fraction on the other (never multiply by a denominator whose sign you do not know); (2) find the **boundary values** (zeros of top and bottom); (3) make a sign table; (4) choose the intervals with the right sign.',
      '**Endpoints:** zeros of the numerator are included for $\\ge$ / $\\le$; zeros of the denominator are **never** included.'),
    ST('chart42', 'Example 3.42: (11x − 38)/(x − 4) + 5/(x + 7) ≥ 11', 137, 'chart42',
       [('Subtract 11 and combine: the numerator is $(11x - 38)(x + 7) + 5(x - 4) - 11(x - 4)(x + 7) = 11x + 22$.', 'k1'),
        ('So the inequality is $\\frac{x + 2}{(x - 4)(x + 7)} \\ge 0$; boundary values $-7, -2, 4$.', 'k2'),
        ('Positive on $-7 < x < -2$ and $x > 4$; zero at $x = -2$. Answer: $-7 < x \\le -2$ or $x > 4$. (The book\'s interval list "$-7 < x < 1$, $1 < x < 4$" should read $-2$ instead of 1.)', 'k3')]),
    WK('ex-34b', 'Worked example: Exercise 3.10, 1(c)', 138,
       'Solve $\\frac{x^2 + 3x - 10}{x^2 - x - 56} \\le 0$.',
       ['Factorise: $\\frac{(x + 5)(x - 2)}{(x - 8)(x + 7)}$. Boundaries $-7, -5, 2, 8$.', 'Signs left to right: $+, -, +, -, +$.', 'Take the "−" intervals; include $-5$ and 2 (numerator zeros), exclude $-7$ and 8.'],
       '$-7 < x \\le -5$ or $2 \\le x < 8$'),
    RM('rm-34', 'Never multiply an inequality by an unknown sign', 134,
       '$\\frac{3}{x - 3} > 1$ does **not** become $3 > x - 3$ for every $x$: if $x < 3$ the sign flips. Move 1 across instead: $\\frac{6 - x}{x - 3} > 0 \\Rightarrow 3 < x < 6$.'),
    RM('summary-t', 'Unit summary', 141,
       'Domain: denominator $\\ne 0$. Lowest terms: cancelled factor → hole; remaining zero → vertical asymptote.',
       'Degrees: top < bottom → $y = 0$; equal → ratio of leading coefficients; one more → oblique (divide).',
       'Operations: factor first; divide = multiply by the reciprocal; add over the LCD.',
       'Equations: multiply by the LCD, then reject excluded values. Inequalities: 0 on one side, sign chart.'),
    'math11-u3-xw4', 'math11-u3-wrk3', 'math11-u3-wrk4',
]

LESSONS = {'math11-u3-l3-1': L1, 'math11-u3-l3-2': L2, 'math11-u3-l3-3': L3, 'math11-u3-l3-4': L4}

# ------------------------------------------------------------------ practice
a = QSet('3.1 Practice — rational functions', 's31')
a.S(74, 'Which are rational? (a) $\\frac{x}{x - 2}$ (b) $3x - 1$ (c) $\\frac{x + 2}{\\sqrt{x}}$ (d) $5x^2 - \\sqrt{x}$', '(a) and (b) only',
    ['Step 1: (a) polynomial over polynomial.', 'Step 2: (b) a polynomial over 1.', 'Step 3: (c), (d) contain $\\sqrt{x}$: not polynomials.'],
    'Look for roots of $x$ or $x$ under a root.', [('Is $\\frac{7}{5}$ rational as a function?', 'Yes, a constant function.')])
a.S(74, 'Find the domain of $f(x) = \\frac{x^2 - 4x - 5}{x^2 + 3x - 10}$.', 'all reals except $-5$ and 2',
    ['Step 1: $x^2 + 3x - 10 = (x + 5)(x - 2)$.', 'Step 2: remove $-5$ and 2.'], 'Only the denominator matters.', [('Domain of $\\frac{1}{x^2 - 25}$?', '$x \\ne \\pm 5$.')])
a.S(74, 'Find the domain of $\\frac{3}{(x - 1)(x + 2)(2x - 6)}$.', '$x \\ne 1, -2, 3$',
    ['Step 1: each factor $= 0$: $x = 1$, $x = -2$, $2x = 6 \\Rightarrow x = 3$.'], 'Set each factor to zero.', [('$\\frac{x}{x(x + 4)}$?', '$x \\ne 0, -4$.')])
a.S(74, 'Find the domain of $\\frac{x + 1}{x^2 + 9}$.', 'all real numbers',
    ['Step 1: $x^2 + 9 \\ge 9 > 0$, never 0.'], 'A sum of a square and a positive number is never 0.', [('$\\frac{2}{x^2 + 1}$?', 'all reals.')])
a.S(74, 'Find the range of $f(x) = \\frac{2x + 1}{x - 3}$.', 'all reals except 2',
    ['Step 1: $2x + 1 = 2(x - 3) + 7$.', 'Step 2: $f(x) = 2 + \\frac{7}{x - 3}$; the fraction is never 0.'], 'Range of $\\frac{ax + b}{cx + d}$ misses $\\frac{a}{c}$.', [('Range of $\\frac{x}{x + 1}$?', '$y \\ne 1$.')])
a.M(73, 'The range of $f(x) = \\frac{x - 3}{x - 4}$ is', ['$y \\ne 1$', '$y \\ne 4$', '$y \\ne 3$', 'all reals'], 'A',
    ['Step 1: $f(x) = 1 + \\frac{1}{x - 4}$.'], 'Divide first.', [('Range of $\\frac{4x - 3}{x - 1}$?', '$y \\ne 4$.')])
a.TF(72, 'Every polynomial function is a rational function.', True, ['Step 1: $P(x) = \\frac{P(x)}{1}$.'], 'Denominator 1 is a polynomial.', [('Is every rational function a polynomial?', 'No, e.g. $\\frac{1}{x}$.')])

b = QSet('3.2 Practice — symmetry, asymptotes, graphs', 's32')
b.S(86, 'Even, odd or neither? (a) $x^2 - 3$ (b) $x^5 - 3x^3 + 5x$ (c) $x^4 + x^3 - 5$', 'even; odd; neither',
    ['Step 1: (a) $(-x)^2 - 3 = x^2 - 3$.', 'Step 2: (b) every power odd: $f(-x) = -f(x)$.', 'Step 3: (c) $f(-1) = -5$, $f(1) = -3$: neither.'], 'Substitute $-x$.', [('$x^3 + 1$?', 'neither.')])
b.S(86, 'Symmetry of (a) $\\frac{x^2 + 1}{x^4 - 3}$ (b) $\\frac{x^3}{x^2 + 4}$ (c) $\\frac{x + 1}{x^2}$', 'y-axis; origin; neither',
    ['Step 1: (a) all even → even → y-axis.', 'Step 2: (b) odd over even → odd → origin.', 'Step 3: (c) top mixed → neither.'], 'Even ↔ y-axis; odd ↔ origin.', [('$\\frac{4x}{x^2 - 1}$?', 'odd, origin.')])
b.S(97, 'Exercise 3.3 Q2: asymptotes and discontinuities of $f(x) = \\frac{2x + 4}{x^2 - x - 6}$.', 'VA $x = 3$; HA $y = 0$; hole at $(-2, -\\frac{2}{5})$',
    ['Step 1: $\\frac{2(x + 2)}{(x - 3)(x + 2)} = \\frac{2}{x - 3}$, $x \\ne -2$.', 'Step 2: VA $x = 3$; degree 0 < 1 → $y = 0$.', 'Step 3: hole: $\\frac{2}{-2 - 3} = -\\frac{2}{5}$.'],
    'Cancel first, then read the asymptotes.', [('$\\frac{x - 1}{x^2 - 1}$?', 'VA $x = -1$, hole $(1, \\frac{1}{2})$, HA $y = 0$.')])
b.S(97, 'Exercise 3.3 Q3 and Q5: asymptotes of $\\frac{7x^2 + 3}{x^2 + 11x + 28}$ and $\\frac{17 - 2x^2}{3x^2 - 75}$.', '$x = -4, -7$, $y = 7$; $x = \\pm 5$, $y = -\\frac{2}{3}$',
    ['Step 1: $x^2 + 11x + 28 = (x + 4)(x + 7)$; equal degrees → $y = \\frac{7}{1}$.', 'Step 2: $3x^2 - 75 = 3(x - 5)(x + 5)$; $y = \\frac{-2}{3}$.'], 'Equal degrees → ratio of leading coefficients.', [('$\\frac{6x^2 + 7}{2x^2 + 9}$?', 'no VA; $y = 3$.')])
b.S(97, 'Exercise 3.3 Q7: asymptotes of $f(x) = \\frac{x^2 + 4}{2x - 4}$.', 'VA $x = 2$; oblique $y = \\frac{x}{2} + 1$',
    ['Step 1: $2x - 4 = 0 \\Rightarrow x = 2$ (top $= 8 \\ne 0$).', 'Step 2: $x^2 + 4 = (x - 2)(x + 2) + 8$, so $f = \\frac{x + 2}{2} + \\frac{4}{x - 2}$.'], 'Degree one more → divide.', [('$\\frac{x^2}{x + 1}$?', 'VA $x = -1$; $y = x - 1$.')])
b.S(97, 'Exercise 3.3 Q8: asymptotes of $\\frac{-x^3 + x}{x^3 - 6x^2 + 12x - 8}$.', 'VA $x = 2$; HA $y = -1$',
    ['Step 1: bottom $= (x - 2)^3$; top at 2: $-8 + 2 \\ne 0$.', 'Step 2: equal degrees: $y = \\frac{-1}{1}$.'], 'Recognise $(x - 2)^3$.', [('$\\frac{x^3}{(x + 1)^3}$?', 'VA $x = -1$, HA $y = 1$.')])
b.S(97, 'Exercise 3.3 Q10: asymptotes of $\\frac{3x^3 + 2x^2 - 7x - 5}{x^2 + 1}$.', 'no VA; oblique $y = 3x + 2$',
    ['Step 1: $x^2 + 1 \\ne 0$: no vertical asymptote.', 'Step 2: divide: quotient $3x + 2$, remainder $-10x - 7$.'], 'Only the quotient gives the line.', [('Q9 $\\frac{x^3 - 8}{x - 1}$?', 'VA $x = 1$; no horizontal or oblique (degrees differ by 2).')])
b.S(105, 'Exercise 3.4 Q1: intercepts of (d) $\\frac{x^3 - x^2 - 6x}{-3x^2 - 3x + 18}$ (e) $\\frac{x^2 + x - 6}{-4x^2 - 16x - 12}$.', '(d) x: $0, 3, -2$; y: 0 (e) x: 2; y: $\\frac{1}{2}$',
    ['Step 1 (d): top $x(x - 3)(x + 2)$; bottom $-3(x + 3)(x - 2)$ — no common factor; $f(0) = 0$.',
     'Step 2 (e): $\\frac{(x + 3)(x - 2)}{-4(x + 1)(x + 3)}$: $x = -3$ is a **hole**, so only $x = 2$; $f(0) = \\frac{-6}{-12}$.'],
    'Cancel before reading x-intercepts.', [('(f) $\\frac{x^3 - 9x}{3x^2 - 6x - 9}$?', 'x: $0, -3$ (3 is a hole); y: 0.')])
b.S(105, 'Sketch facts for $f(x) = \\frac{2x + 5}{x + 1}$ (Exercise 3.4, 2c).', 'VA $x = -1$, HA $y = 2$, x-int $-\\frac{5}{2}$, y-int 5',
    ['Step 1: bottom 0 at $-1$.', 'Step 2: equal degrees: $y = 2$.', 'Step 3: top 0 at $-\\frac{5}{2}$; $f(0) = 5$.'], 'Collect all facts before drawing.', [('$\\frac{-1}{x - 3}$?', 'VA $x = 3$, HA $y = 0$, y-int $\\frac{1}{3}$.')])
b.S(105, 'Sketch facts for $f(x) = \\frac{2x^2 - 5x + 5}{x - 1}$ (Exercise 3.4, 2g).', 'VA $x = 1$; oblique $y = 2x - 3$; y-int $-5$; no x-int',
    ['Step 1: $2x^2 - 5x + 5 = (x - 1)(2x - 3) + 2$.', 'Step 2: top: $D = 25 - 40 < 0$, no zeros.', 'Step 3: $f(0) = -5$.'], 'Discriminant tells you about x-intercepts.', [('$\\frac{x^3 - 4x}{x^2 - 1}$?', 'odd; x-int $0, \\pm 2$; VA $\\pm 1$; oblique $y = x$.')])
b.M(93, 'The horizontal asymptote of $\\frac{2x^2}{x^2 + 1}$ is', ['$y = 2$', '$y = 0$', '$y = 1$', 'none'], 'A',
    ['Step 1: equal degrees: $\\frac{2}{1}$.'], 'Leading coefficients.', [('$\\frac{2x}{x^2 + 1}$?', '$y = 0$.')])
b.M(91, 'For $f(x) = \\frac{x^2 - 25}{x - 5}$, at $x = 5$ there is', ['a hole at $(5, 10)$', 'a vertical asymptote', 'an x-intercept', 'nothing special'], 'A',
    ['Step 1: $\\frac{(x - 5)(x + 5)}{x - 5} = x + 5$, $x \\ne 5$; $5 + 5 = 10$.'], 'Cancelled factor → hole.', [('$\\frac{x^2 - 9}{x + 3}$?', 'hole at $(-3, -6)$.')])
b.TF(88, 'A graph can never cross its horizontal asymptote.', False,
     ['Step 1: $\\frac{x}{x^2 + 1}$ crosses $y = 0$ at the origin; the asymptote only describes the far-left and far-right behaviour.'], 'Vertical asymptotes are never crossed; horizontal ones may be.', [('Can a graph cross a vertical asymptote?', 'No: $f$ is undefined there.')])

c = QSet('3.3 Practice — operations', 's33')
c.S(139, 'Review 2: simplify (a) $\\frac{x^2 - 25}{x^2 - 2x - 15}$ (b) $\\frac{w^2 - 8w - 9}{w^2 + 5w + 4}$.', '$\\frac{x + 5}{x + 3}$; $\\frac{w - 9}{w + 4}$',
    ['Step 1: $\\frac{(x - 5)(x + 5)}{(x - 5)(x + 3)}$.', 'Step 2: $\\frac{(w - 9)(w + 1)}{(w + 4)(w + 1)}$.'], 'Factor, cancel.', [('$\\frac{y^2 - 3y}{y^2 - 4y + 3}$?', '$\\frac{y}{y - 1}$.')])
c.S(139, 'Review 2: simplify (c) $\\frac{25x - x^3}{x^2 - 3x - 10}$ (f) $\\frac{3x^2 + 17x - 6}{9x^2 - 6x + 1}$.', '$-\\frac{x(x + 5)}{x + 2}$; $\\frac{x + 6}{3x - 1}$',
    ['Step 1: $25x - x^3 = x(5 - x)(5 + x) = -x(x - 5)(x + 5)$; bottom $(x - 5)(x + 2)$.', 'Step 2: $\\frac{(3x - 1)(x + 6)}{(3x - 1)^2}$.'], '$5 - x = -(x - 5)$.', [('$\\frac{x^3 + 3x^2}{x^2 + 6x + 9}$?', '$\\frac{x^2}{x + 3}$.')])
c.S(139, 'Review 2: simplify (g) $\\frac{12z^2 + 11z - 15}{20z^2 - 23z + 6}$ (j) $\\frac{a^2 - 5ab + 6b^2}{a^2 + 2ab - 8b^2}$.', '$\\frac{3z + 5}{5z - 2}$; $\\frac{a - 3b}{a + 4b}$',
    ['Step 1: $(4z - 3)(3z + 5)$ over $(4z - 3)(5z - 2)$.', 'Step 2: $(a - 2b)(a - 3b)$ over $(a + 4b)(a - 2b)$.'], 'Split the middle term ($ac$ method).', [('$\\frac{m^2 - n^2}{m^2 + 11mn + 10n^2}$?', '$\\frac{m - n}{m + 10n}$.')])
c.S(139, 'Review 3(a): $\\frac{3y - 6}{6y + 12} \\cdot \\frac{3y^2 - 12}{y^2 - 5y + 6}$.', '$\\frac{3(y - 2)}{2(y - 3)}$',
    ['Step 1: $\\frac{3(y - 2)}{6(y + 2)} \\cdot \\frac{3(y - 2)(y + 2)}{(y - 2)(y - 3)}$.', 'Step 2: cancel $(y + 2)$, one $(y - 2)$: $\\frac{9(y - 2)}{6(y - 3)}$.'], 'Factor out common numbers too.', [('$\\frac{4 - 2x}{6x + 30} \\cdot \\frac{x^2 - 25}{x^2 - 7x + 10}$?', '$-\\frac{1}{3}$.')])
c.S(139, 'Review 3(c): $\\frac{5x + 15}{x^2 - 9} \\div \\frac{10x^2 + 10x}{4x - 12}$.', '$\\frac{2}{x(x + 1)}$',
    ['Step 1: flip: $\\frac{5(x + 3)}{(x - 3)(x + 3)} \\cdot \\frac{4(x - 3)}{10x(x + 1)}$.', 'Step 2: cancel: $\\frac{20}{10x(x + 1)}$.'], 'Flip the second fraction only.', [('$\\frac{x}{x - 1} \\div \\frac{1}{x^2 - 1}$?', '$x(x + 1)$.')])
c.S(139, 'Review 3(d) and (e): (d) $\\frac{4w}{2w - 5} + \\frac{10}{5 - 2w}$ (e) $\\frac{5}{y + 2} + \\frac{5}{2 - y} - \\frac{6}{y^2 - 4}$.', '2; $-\\frac{26}{y^2 - 4}$',
    ['Step 1 (d): $\\frac{4w - 10}{2w - 5} = \\frac{2(2w - 5)}{2w - 5}$.', 'Step 2 (e): $\\frac{5}{2 - y} = -\\frac{5}{y - 2}$; LCD $y^2 - 4$: $5(y - 2) - 5(y + 2) - 6 = -26$.'],
    'Turn $a - b$ into $-(b - a)$ to match denominators.', [('$\\frac{3}{x - 1} - \\frac{3}{1 - x}$?', '$\\frac{6}{x - 1}$.')])
c.S(139, 'Review 3(f): $\\frac{2y^2}{y^4 - 1} + \\frac{y}{y^2 - 1} - \\frac{1}{y - 1}$.', '$\\frac{1}{y^2 + 1}$',
    ['Step 1: LCD $(y - 1)(y + 1)(y^2 + 1)$.', 'Step 2: numerator $2y^2 + y(y^2 + 1) - (y + 1)(y^2 + 1) = y^2 - 1$.', 'Step 3: cancel $y^2 - 1$.'], 'Factor $y^4 - 1$ fully.', [('$\\frac{5}{xy + y^2} + \\frac{3}{x^2 + xy}$?', '$\\frac{5x + 3y}{xy(x + y)}$.')])
c.S(124, 'Find the LCD of $\\frac{x - 3}{x^2 - 4x + 4}$ and $\\frac{x}{x^2 + 2x - 8}$.', '$(x - 2)^2(x + 4)$',
    ['Step 1: $(x - 2)^2$ and $(x - 2)(x + 4)$.', 'Step 2: highest power of each factor.'], 'Highest power of every factor.', [('LCD of $\\frac{1}{x^2 - x - 6}$, $\\frac{1}{x^2 - 9}$?', '$(x + 2)(x - 3)(x + 3)$.')])
c.S(125, 'Simplify $\\frac{x}{x - 1} + \\frac{2}{x + 1}$.', '$\\frac{x^2 + 3x - 2}{(x - 1)(x + 1)}$',
    ['Step 1: LCD $(x - 1)(x + 1)$.', 'Step 2: $x(x + 1) + 2(x - 1) = x^2 + 3x - 2$.'], 'Multiply each numerator by the missing factor.', [('$\\frac{1}{x} + \\frac{1}{x + 1}$?', '$\\frac{2x + 1}{x(x + 1)}$.')])
c.M(109, 'Which pair is equivalent?', ['$\\frac{x + 1}{x - 3}$ and $\\frac{x^2 + 4x + 3}{x^2 - 9}$', '$\\frac{3}{x + 4}$ and $\\frac{6}{2x + 6}$', '$\\frac{x + 3}{x}$ and 3', '$\\frac{5x - x^2}{25 - x^2}$ and $\\frac{x}{5 - x}$'], 'A',
    ['Step 1: $\\frac{(x + 1)(x + 3)}{(x - 3)(x + 3)}$ cancels to $\\frac{x + 1}{x - 3}$.', 'Step 2: D: $\\frac{x(5 - x)}{(5 - x)(5 + x)} = \\frac{x}{5 + x}$, not $\\frac{x}{5 - x}$.'],
    'Cross-multiply or simplify.', [('Are $\\frac{2}{2x + 2}$ and $\\frac{1}{x + 1}$ equivalent?', 'Yes.')])
c.TF(113, '$\\frac{x + 6}{x + 3} = 2$.', False, ['Step 1: $x$ is a term, not a factor; test $x = 1$: $\\frac{7}{4} \\ne 2$.'], 'Cancel factors only.', [('Is $\\frac{2x + 6}{x + 3} = 2$?', 'Yes, for $x \\ne -3$.')])

d = QSet('3.4 Practice — equations and inequalities', 's34')
d.S(140, 'Review 4(a): solve $\\frac{5}{x - 2} = \\frac{3}{x + 1}$.', '$x = -\\frac{11}{2}$',
    ['Step 1: $5(x + 1) = 3(x - 2)$.', 'Step 2: $2x = -11$.'], 'Cross-multiply.', [('$\\frac{4}{x - 4} = \\frac{2}{x - 2}$?', '$x = 0$.')])
d.S(140, 'Review 4(b): solve $\\frac{x + 1}{x + 4} = \\frac{-3}{x + 3}$.', 'no real solution',
    ['Step 1: $(x + 1)(x + 3) = -3(x + 4) \\Rightarrow x^2 + 7x + 15 = 0$.', 'Step 2: $D = 49 - 60 < 0$.'], 'Check the discriminant.', [('$\\frac{x}{x + 1} = \\frac{2}{x}$?', '$x = 2$ or $-1$; $-1$ is excluded, so $x = 2$.')])
d.S(140, 'Review 4(d): solve $\\frac{2}{3x - 9} - \\frac{1}{3x + 6} = \\frac{4}{x^2 - x - 6}$.', '$x = 5$',
    ['Step 1: LCD $3(x - 3)(x + 2)$; excluded 3, $-2$.', 'Step 2: $2(x + 2) - (x - 3) = 12 \\Rightarrow x + 7 = 12$.'], 'Factor every denominator first.', [('$\\frac{2}{x + 5} + \\frac{1}{x - 5} = \\frac{16}{x^2 - 25}$?', '$x = 7$.')])
d.S(140, 'Review 4(c): solve $\\frac{7}{3x + 9} - \\frac{x}{x^2 + 6x + 9} = \\frac{1}{3}$.', '$x = -1 \\pm \\sqrt{13}$',
    ['Step 1: LCD $3(x + 3)^2$.', 'Step 2: $7(x + 3) - 3x = (x + 3)^2 \\Rightarrow x^2 + 2x - 12 = 0$.', 'Step 3: formula: $x = -1 \\pm \\sqrt{13}$; neither is $-3$.'], 'Quadratic formula when it will not factor.', [('$\\frac{x}{x - 3} = 2 + \\frac{3}{x - 3}$?', 'no solution ($x = 3$ excluded).')])
d.S(132, 'An aeroplane is 3 times as fast as a car. Over 450 km it arrives 6 hours earlier. Find the aeroplane\'s speed.', '150 km/h',
    ['Step 1: car $v$: $\\frac{450}{v} - \\frac{450}{3v} = 6$.', 'Step 2: $\\frac{300}{v} = 6 \\Rightarrow v = 50$.'], 'Time = distance ÷ speed.', [('Same with 600 km, 4 hours?', 'car 100, plane 300 km/h.')])
d.S(132, 'A boat does 15 km/h in calm water. 140 km downstream takes as long as 35 km upstream. Find the current.', '9 km/h',
    ['Step 1: $\\frac{140}{15 + c} = \\frac{35}{15 - c}$.', 'Step 2: $2100 - 140c = 525 + 35c \\Rightarrow c = 9$.'], 'Downstream adds, upstream subtracts.', [('Boat 20 km/h, 60 down = 40 up?', '4 km/h.')])
d.S(132, 'Abraham takes 10 hours longer than Elsa; together they take 12 hours. Find each time.', 'Elsa 20 h, Abraham 30 h',
    ['Step 1: $\\frac{12}{t} + \\frac{12}{t + 10} = 1$.', 'Step 2: $t^2 - 14t - 120 = 0 \\Rightarrow (t - 20)(t + 6) = 0$.'], 'Rates add.', [('A 6 h, B 3 h together?', '2 h.')])
d.S(141, 'Review 7: Kedija drove 240 km. 15 km/h faster, she would go 30 km further in $\\frac{3}{4}$ of the time. Find her speed.', '30 km/h',
    ['Step 1: $\\frac{270}{v + 15} = \\frac{3}{4} \\cdot \\frac{240}{v} = \\frac{180}{v}$.', 'Step 2: $270v = 180v + 2700 \\Rightarrow v = 30$.'], 'Write the two times and compare.', [('Check:', '8 h at 30; 270 km at 45 km/h = 6 h = $\\frac{3}{4}$ of 8.')])
d.S(141, 'Review 8: the larger number exceeds twice the smaller by 17; larger ÷ smaller gives quotient 3, remainder 7. Find them.', '10 and 37',
    ['Step 1: $L = 2S + 17$ and $L = 3S + 7$.', 'Step 2: $2S + 17 = 3S + 7 \\Rightarrow S = 10$, $L = 37$.'], 'Dividend = quotient × divisor + remainder.', [('Check:', '$37 = 3 \\times 10 + 7$.')])
d.S(138, 'Exercise 3.10, 1(b): solve $\\frac{3x + 2}{x - 3} \\le 0$.', '$-\\frac{2}{3} \\le x < 3$',
    ['Step 1: boundaries $-\\frac{2}{3}$ and 3.', 'Step 2: negative between them.', 'Step 3: include $-\\frac{2}{3}$, exclude 3.'], 'Denominator zeros are never included.', [('$\\frac{3}{x - 3} > 0$?', '$x > 3$.')])
d.S(138, 'Exercise 3.10, 2(d): solve $\\frac{x}{x + 5} > 3$.', '$-\\frac{15}{2} < x < -5$',
    ['Step 1: $\\frac{x - 3(x + 5)}{x + 5} > 0 \\Rightarrow \\frac{-2x - 15}{x + 5} > 0$.', 'Step 2: same as $\\frac{2x + 15}{x + 5} < 0$.', 'Step 3: between $-7.5$ and $-5$.'], 'Get 0 on one side first.', [('$\\frac{x + 3}{x + 2} < 0$?', '$-3 < x < -2$.')])
d.S(138, 'Exercise 3.10, 2(c): solve $\\frac{3 - x}{x^2 - 3x + 2} \\ge 0$.', '$x < 1$ or $2 < x \\le 3$',
    ['Step 1: $\\frac{3 - x}{(x - 1)(x - 2)}$; boundaries 1, 2, 3.', 'Step 2: signs: $+, -, +, -$.', 'Step 3: include 3 only.'], 'A factor like $3 - x$ is negative to the right of 3.', [('$\\frac{x - 2}{x^2 - 9} \\ge 0$?', '$-3 < x \\le 2$ or $x > 3$.')])
d.S(140, 'Review 5(c): solve $\\frac{x}{x - 3} \\le \\frac{1}{x + 2}$.', '$-2 < x < 3$',
    ['Step 1: $\\frac{x(x + 2) - (x - 3)}{(x - 3)(x + 2)} = \\frac{x^2 + x + 3}{(x - 3)(x + 2)} \\le 0$.', 'Step 2: $x^2 + x + 3 > 0$ always ($D < 0$).', 'Step 3: need $(x - 3)(x + 2) < 0$.'], 'A numerator that is always positive can be ignored.', [('$\\frac{x}{x - 3} < 0$?', '$0 < x < 3$.')])
d.S(138, 'Exercise 3.10 Q3: cost $c = \\frac{4p}{100 - p}$ (thousand Nakfa) to remove $p$% of bacteria. Which $p$ is possible with less than 10 thousand Nakfa?', '$0 \\le p < 71.4$ (about)',
    ['Step 1: $\\frac{4p}{100 - p} < 10$ with $0 \\le p < 100$, so $100 - p > 0$.', 'Step 2: $4p < 1000 - 10p \\Rightarrow p < \\frac{1000}{14} \\approx 71.4$.'], 'Here the denominator is known to be positive, so multiplying is safe.', [('Budget under 4 thousand?', '$p < 50$.')])
d.S(141, 'Review 6: $f(x) = \\frac{50x}{x - 50}$ gives the lens-to-film distance. (c) Find $f(2000)$. (d) For which $x$ is $f(x) \\ge 60$?', '$\\approx 51.3$; $50 < x \\le 300$',
    ['Step 1: $\\frac{100000}{1950} \\approx 51.3$.', 'Step 2: for $x > 50$: $50x \\ge 60x - 3000 \\Rightarrow x \\le 300$.'],
    'The book mixes units ("ml" and m); take all distances in millimetres.', [('Domain for a real object?', '$x > 50$.')])
d.M(129, 'Solving $\\frac{3x}{x - 3} = 2 + \\frac{9}{x - 3}$ gives', ['no solution', '$x = 3$', '$x = -3$', 'all reals'], 'A',
    ['Step 1: $3x = 2x - 6 + 9 \\Rightarrow x = 3$, which is excluded.'], 'Always check excluded values.', [('$\\frac{x}{x - 1} = \\frac{1}{x - 1}$?', 'no solution.')])
d.TF(136, 'For $\\frac{P}{Q} \\ge 0$, the zeros of $Q$ are included in the answer.', False,
     ['Step 1: $Q = 0$ makes the expression undefined.'], 'Only numerator zeros join "≥" answers.', [('Are numerator zeros included for "> 0"?', 'No.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Rational function', '$f(x) = \\frac{P(x)}{Q(x)}$ with polynomials $P, Q$ and $Q(x) \\ne 0$.', 72),
    ('Even function', '$f(-x) = f(x)$; symmetric about the y-axis.', 80),
    ('Odd function', '$f(-x) = -f(x)$; symmetric about the origin.', 80),
    ('Vertical asymptote', 'A line $x = c$ near which $f(x) \\to \\pm\\infty$.', 89),
    ('Horizontal asymptote', 'A line $y = d$ that $f$ approaches as $x \\to \\pm\\infty$.', 92),
    ('Oblique asymptote', 'A slanted line $y = ax + b$ that $f$ approaches far out.', 95),
    ('Point of discontinuity (hole)', 'An excluded $x$ whose factor cancels.', 91),
    ('LCD', 'Least common denominator: product of every factor to its highest power.', 124),
    ('Boundary value', 'A zero of the numerator or denominator.', 135),
]
TIPS = [('Cancel first: cancelled factor → hole; leftover zero → vertical asymptote.', 91),
        ('Degrees: smaller top → y = 0; equal → ratio; one more → divide.', 93),
        ('Inequalities: 0 on one side, then a sign chart.', 136)]
IDEAS = [('asym', 'Asymptotes', 'l3_2', 'math11-u3-md-asym-t'), ('sketch', '7-step sketch', 'l3_2', 'math11-u3-md-sketch-t'),
         ('ops', 'Factor, flip, cancel, combine', 'l3_3', 'math11-u3-c04'), ('chart', 'Sign charts', 'l3_4', 'math11-u3-xt4')]
