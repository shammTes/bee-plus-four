r"""Grade 11 Unit 2 — Square Root Functions: graphs, domain and range, radical equations, inverses (pp. 62-70)."""
from math import sqrt
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side, with_legend

UID = 'math11-u2'
set_unit(UID)

R = lambda v: sqrt(max(v, 0))


# ------------------------------------------------------------------ figures
def f_stretch():
    p = Plot(0, 9, 0, 6, unit=32, uy=30, every=1, yevery=1, gstep=1)
    p.fn(lambda x: R(x), 0, 9, BLUE, 2.6, steps=48)
    p.fn(lambda x: R(2 * x), 0, 9, GREEN, 2.6, steps=48)
    p.fn(lambda x: R(4 * x), 0, 9, RED, 2.6, steps=48)
    for x, y, c in ((4, 2, BLUE), (2, 2, GREEN), (1, 2, RED)):
        p.pt(x, y, None, c=c, r=4)
    return with_legend(p, [('y = √x', BLUE), ('y = √(2x)', GREEN), ('y = √(4x)', RED)], 12)


def f_reflect():
    p = Plot(-6, 6, -3, 3, unit=26, uy=30, every=2, yevery=1, gstep=1)
    p.fn(lambda x: R(x), 0, 6, BLUE, 2.6, steps=40)
    p.fn(lambda x: R(-x), -6, 0, GREEN, 2.6, steps=40)
    p.fn(lambda x: -R(x), 0, 6, RED, 2.6, steps=40)
    p.pt(4, 2, None, c=BLUE, r=4).pt(-4, 2, None, c=GREEN, r=4).pt(4, -2, None, c=RED, r=4)
    return with_legend(p, [('y = √x', BLUE), ('y = √(−x)', GREEN), ('y = −√x', RED)], 12)


def f_shift():
    p = Plot(-1, 8, -3, 5, unit=32, uy=26, every=1, yevery=1, gstep=1)
    p.g('k1 k2 k3').fn(lambda x: R(x), 0, 8, BLUE, 2.6, steps=44).pt(0, 0, None, c=BLUE, r=4.2).end()
    p.g('k2 k3').fn(lambda x: R(x) + 2, 0, 8, GREEN, 2.6, steps=44).pt(0, 2, None, c=GREEN, r=4.2)
    p.fn(lambda x: R(x) - 2, 0, 8, RED, 2.6, steps=44).pt(0, -2, None, c=RED, r=4.2).end()
    p.g('k3').fn(lambda x: R(x - 3), 3, 8, PURPLE, 2.6, steps=40).pt(3, 0, None, c=PURPLE, r=4.2)
    p.text(p.X(3) - 6, p.Y(0) - 8, '(3, 0)', 11.5, PURPLE, 'end').end()
    return with_legend(p, [('√x', BLUE), ('√x + 2', GREEN), ('√x − 2', RED), ('√(x − 3)', PURPLE)], 12)


def f_twobranch():
    p = Plot(-7, 7, -1, 6, unit=22, uy=28, every=1, yevery=1, gstep=1)
    p.text(p.X(-3), p.Y(5.2), 'x ≤ −3', 12, BLUE).text(p.X(3), p.Y(5.2), 'x ≥ 3', 12, BLUE)
    p.g('k1 k2 k3').pt(-3, 0, None, c=RED, r=4.4).pt(3, 0, None, c=RED, r=4.4).end()
    p.g('k2 k3').seg((-2.95, 0), (2.95, 0), RED, 5).text(p.X(0), p.Y(0) - 10, 'no graph here', 11.5, RED).end()
    p.g('k3').fn(lambda x: R(x * x - 9), -7, -3, BLUE, 2.8, steps=40)
    p.fn(lambda x: R(x * x - 9), 3, 7, BLUE, 2.8, steps=40)
    p.text(p.X(0.3), p.Y(4.1), 'y = √(x² − 9)', 12, BLUE, 'start').end()
    return p


def f_extra():
    p = Plot(-1, 10, -4, 7, unit=27, uy=19, every=1, yevery=1, gstep=1)
    p.g('k1 k2 k3').fn(lambda x: R(3 * x + 1), -1 / 3, 10, BLUE, 2.8, steps=44)
    p.fn(lambda x: x - 3, -1, 10, GREEN, 2.6, steps=4).end()
    p.g('k2 k3').pt(8, 5, None, c=RED, r=5).text(p.X(8) - 10, p.Y(5) - 8, '(8, 5) real', 12, RED, 'end').end()
    p.g('k3').fn(lambda x: -R(3 * x + 1), -1 / 3, 10, GREY, 2, steps=44, dash=True)
    p.pt(1, -2, None, c=ORANGE, r=5, open_=True).text(p.X(1) + 10, p.Y(-2) + 4, '(1, −2) false root', 12, ORANGE, 'start').end()
    return with_legend(p, [('y = √(3x + 1)', BLUE), ('y = x − 3', GREEN), ('y = −√(3x + 1)', GREY)], 11.5)


def f_inverse():
    p = Plot(-1, 6, -1, 6, unit=32, uy=32, every=1, yevery=1, gstep=1)
    p.g('k1 k2 k3').fn(lambda x: R(x - 1), 1, 6, BLUE, 2.8, steps=40).pt(1, 0, None, c=BLUE, r=4.2).pt(5, 2, None, c=BLUE, r=4.2).end()
    p.g('k2 k3').seg((-1, -1), (6, 6), GREY, 1.6, dash='6 4').text(p.X(5.75), p.Y(4.9), 'y = x', 12, GREY).end()
    p.g('k3').fn(lambda x: x * x + 1, 0, 2.24, RED, 2.8, steps=30).pt(0, 1, None, c=RED, r=4.2).pt(2, 5, None, c=RED, r=4.2)
    p.seg((5, 2), (2, 5), PURPLE, 1.4, dash='3 3').end()
    p.text(p.X(3.5), p.Y(1.0), 'f(x) = √(x − 1)', 12, BLUE, 'start')
    p.text(p.X(2.35), p.Y(5.75), 'x² + 1, x ≥ 0', 12, RED, 'start')
    return p


DIAGRAMS = {
    'stretch': (f_stretch(), 'Example 2.2(a): y = √x, √(2x) and √(4x)', 64),
    'reflect': (f_reflect(), 'Example 2.2(b): reflections of y = √x', 64),
    'shift': (f_shift(), 'Example 2.2(c): moving y = √x up, down and right', 64),
    'twobranch': (f_twobranch(), 'Example 2.4: y = √(x² − 9) has two pieces', 66),
    'extra': (f_extra(), 'Example 2.7: why x = 1 is a false root', 68),
    'inverse': (f_inverse(), 'Example 2.8: a function and its inverse mirror in y = x', 70),
}

# ------------------------------------------------------------------ 2.1
L1 = [
    T('=math11-u2-c01', '2.1 The square root function', 62,
      'Every positive number has **two** square roots: $x^2 = 16$ gives $x = 4$ or $x = -4$. The symbol $\\sqrt{a}$ always means the **positive** (principal) one: $\\sqrt{16} = 4$, and the negative root is written $-\\sqrt{16}$.',
      'The **square root function** is $f(x) = \\sqrt{x}$. In real numbers we cannot take the square root of a negative number, so the graph exists only for $x \\ge 0$, and every output is $\\ge 0$.',
      '**Table of values** (choose perfect squares so the outputs are whole numbers):',
      '$x = 0, 1, 4, 9, 16$ gives $\\sqrt{x} = 0, 1, 2, 3, 4$.',
      'Shape: it starts at $(0, 0)$, rises quickly at first, then more and more slowly. It is the **upper half of a parabola lying on its side** ($x = y^2$, $y \\ge 0$).'),
    T('family-t', 'How the numbers in y = a√(b(x − h)) + k move the graph', 63,
      'Start from $y = \\sqrt{x}$ and its **starting point** $(0, 0)$. Each number in the formula does one job:',
      '- $+k$ outside: move **up** $k$ (down if $k < 0$). Start $(0, k)$.',
      '- $(x - h)$ inside: move **right** $h$ (left if $h < 0$). Start $(h, 0)$. Inside the root the shift goes the "opposite" way to the sign.',
      '- $\\sqrt{bx}$ with $b > 1$: the graph is **steeper** (above $\\sqrt{x}$); with $0 < b < 1$ it is flatter (below).',
      '- $\\sqrt{-x}$: **reflect in the y-axis** (the graph goes to the left).',
      '- $-\\sqrt{x}$: **reflect in the x-axis** (the graph goes down).',
      'Combined: $y = \\sqrt{x - h} + k$ starts at $(h, k)$. For $y = \\sqrt{b x + c} + k$, first find where the inside is 0: $x = -\\frac{c}{b}$; the start is $\\left(-\\frac{c}{b}, k\\right)$.'),
    TB('family-tb', 'Summary of transformations', 63, ['Equation', 'Start point', 'Direction', 'Change from √x'],
       [['$y = \\sqrt{x}$', '$(0, 0)$', 'right, up', 'parent'],
        ['$y = \\sqrt{x} + 2$', '$(0, 2)$', 'right, up', 'up 2'],
        ['$y = \\sqrt{x - 3}$', '$(3, 0)$', 'right, up', 'right 3'],
        ['$y = \\sqrt{4x}$', '$(0, 0)$', 'right, up', 'steeper (= $2\\sqrt{x}$)'],
        ['$y = \\sqrt{-x}$', '$(0, 0)$', 'left, up', 'mirror in y-axis'],
        ['$y = -\\sqrt{x}$', '$(0, 0)$', 'right, down', 'mirror in x-axis'],
        ['$y = -\\sqrt{x + 1} + 4$', '$(-1, 4)$', 'right, down', 'left 1, flip, up 4']]),
    DG('stretch', 'Stretching: √(ax) with a > 1', 64, 'stretch',
       'All three start at $(0, 0)$. Each passes through height 2: $\\sqrt{x}$ at $x = 4$, $\\sqrt{2x}$ at $x = 2$, $\\sqrt{4x}$ at $x = 1$. Note $\\sqrt{4x} = 2\\sqrt{x}$: every height is doubled.'),
    DG('reflect', 'Reflections', 64, 'reflect',
       '$\\sqrt{-x}$ needs $-x \\ge 0$, so $x \\le 0$: the graph goes to the **left**. $-\\sqrt{x}$ keeps $x \\ge 0$ but every output becomes negative: the graph goes **down**.'),
    ST('shift', 'Moving the graph (Example 2.2c)', 64, 'shift',
       [('Parent $y = \\sqrt{x}$: start $(0, 0)$.', 'k1'),
        ('$\\sqrt{x} + 2$ and $\\sqrt{x} - 2$: the same shape moved up 2 and down 2. Starts $(0, 2)$ and $(0, -2)$.', 'k2'),
        ('$\\sqrt{x - 3}$: the same shape moved **right** 3, start $(3, 0)$. Domain becomes $x \\ge 3$.', 'k3')]),
    WK('ex-21a', 'Worked example: sketch y = √(x − 2) + 1', 64,
       'Sketch $y = \\sqrt{x - 2} + 1$ and state its starting point.',
       ['Inside $= 0$ when $x = 2$, and then $y = 1$: start $(2, 1)$.',
        'Pick $x$ values that make the inside a perfect square: $x = 3$ gives $y = 2$; $x = 6$ gives $y = 3$; $x = 11$ gives $y = 4$.',
        'Plot $(2, 1), (3, 2), (6, 3), (11, 4)$ and join with a smooth curve to the right.'],
       'start $(2, 1)$; through $(3, 2)$, $(6, 3)$'),
    WK('ex-21b', 'Worked example: Exercise 2.1 (d) y = √(−2x) + 4', 65,
       'Describe and sketch $y = \\sqrt{-2x} + 4$.',
       ['Inside $-2x \\ge 0 \\Rightarrow x \\le 0$: the graph goes **left**.', 'Start: $x = 0$, $y = 4$: $(0, 4)$.',
        'Points: $x = -2$: $\\sqrt{4} + 4 = 6$; $x = -8$: $\\sqrt{16} + 4 = 8$.', 'Shape: $\\sqrt{x}$ mirrored in the y-axis, made steeper, moved up 4.'],
       'start $(0, 4)$, goes left and up through $(-2, 6)$ and $(-8, 8)$'),
    RM('rm-21', 'Common mistakes', 63,
       '$\\sqrt{x + 3}$ moves **left** 3, not right. $\\sqrt{x} + 3$ moves **up** 3. Bracket inside vs number outside.',
       '$\\sqrt{x^2} = |x|$, not $x$: $\\sqrt{(-5)^2} = 5$.',
       'Textbook note (p. 63 box): "if $a < 0$, the graph of $\\sqrt{ax}$ is the image of $\\sqrt{x}$ under reflection across the y-axis" is exactly true only for $a = -1$. In general $\\sqrt{ax}$ with $a < 0$ is the mirror image of $\\sqrt{|a|x}$.'),
    'math11-u2-c07', 'math11-u2-tblE1',
]

# ------------------------------------------------------------------ 2.2
L2 = [
    T('dom-t', '2.2 Domain and range: the rule', 65,
      '**Domain rule:** the expression under the root (the **radicand**) must be $\\ge 0$. Write the inequality and solve it.',
      '**Range rule:** $\\sqrt{\\;\\;}$ is never negative, so $\\sqrt{\\dots} \\ge 0$. Then apply what is outside: $y = \\sqrt{\\dots} + k$ gives $y \\ge k$; $y = -\\sqrt{\\dots} + k$ gives $y \\le k$.',
      '**Example 2.3:** $y = \\sqrt{x + 5}$: $x + 5 \\ge 0 \\Rightarrow x \\ge -5$; range $y \\ge 0$. (The book writes "we get $y \\ge 0$" in the domain line: it means $x \\ge -5$.)',
      '**Example 2.5:** $y = \\sqrt{x^2 + 4}$: $x^2 + 4 \\ge 4 > 0$ always, so the domain is all real numbers; the smallest value is $\\sqrt{4} = 2$, so the range is $y \\ge 2$.'),
    TB('dom-tb', 'Types of radicand and how to find the domain', 66, ['Radicand', 'Method', 'Example', 'Domain'],
       [['linear $ax + b$', 'solve $ax + b \\ge 0$ (flip if $a < 0$)', '$\\sqrt{6 - 2x}$', '$x \\le 3$'],
        ['quadratic, two roots', 'sign chart / outside or between roots', '$\\sqrt{x^2 - 9}$', '$x \\le -3$ or $x \\ge 3$'],
        ['quadratic, $a < 0$', 'between the roots', '$\\sqrt{9 - x^2}$', '$-3 \\le x \\le 3$'],
        ['always positive', 'no restriction', '$\\sqrt{x^2 + 4}$', 'all reals'],
        ['perfect square', '$\\sqrt{(x - 3)^2} = |x - 3|$', '$\\sqrt{x^2 - 6x + 9}$', 'all reals']]),
    ST('twobranch', 'Example 2.4: domain of y = √(x² − 9)', 66, 'twobranch',
       [('Solve $x^2 - 9 \\ge 0$: factorise $(x - 3)(x + 3) \\ge 0$; roots $-3$ and 3.', 'k1'),
        ('Sign chart: positive for $x < -3$, negative between, positive for $x > 3$; zero at $\\pm 3$.', 'k2'),
        ('Domain: $x \\le -3$ or $x \\ge 3$ (the book prints "$x < -3$": $-3$ must be included because $\\sqrt{0} = 0$). Range $y \\ge 0$.', 'k3')]),
    WK('ex-22a', 'Worked example: √(9 − x²) (Review 1b)', 70,
       'Find the domain and range of $y = \\sqrt{9 - x^2}$.',
       ['$9 - x^2 \\ge 0 \\Rightarrow x^2 \\le 9 \\Rightarrow -3 \\le x \\le 3$.', 'Biggest radicand: $x = 0$ gives $\\sqrt{9} = 3$; smallest: $x = \\pm 3$ gives 0.',
        'So $0 \\le y \\le 3$. (The graph is the top half of the circle $x^2 + y^2 = 9$.)'],
       'domain $[-3, 3]$, range $[0, 3]$'),
    WK('ex-22b', 'Worked example: a negative outside', 66,
       'Find the domain and range of $y = 5 - \\sqrt{2x - 4}$.',
       ['$2x - 4 \\ge 0 \\Rightarrow x \\ge 2$.', '$\\sqrt{2x - 4} \\ge 0$, so $-\\sqrt{2x - 4} \\le 0$, so $y \\le 5$.'],
       'domain $x \\ge 2$, range $y \\le 5$'),
    MN('mn-22', 'Memory hook', 66, '**"Inside ≥ 0 for the domain; outside number for the range."** Then check the sign in front of the root: plus → $y \\ge k$, minus → $y \\le k$.'),
    'math11-u2-c02', 'math11-u2-c03', 'math11-u2-c08', 'math11-u2-l2-2-r3x1',
]

# ------------------------------------------------------------------ 2.3
L3 = [
    T('=math11-u2-c05', '2.3 Solving square root (radical) equations', 67,
      'A **radical equation** has the unknown under a root, e.g. $\\sqrt{3x + 8} = 4$. Method:',
      '1. **Isolate** one root on one side.',
      '2. **Square** both sides (this removes the root).',
      '3. Solve the new (linear or quadratic) equation.',
      '4. **Check every answer** in the **original** equation and reject false (extraneous) roots.',
      '**Why check?** "$a = b \\Rightarrow a^2 = b^2$" is always true, but "$a^2 = b^2 \\Rightarrow a = b$" is not ($(-3)^2 = 3^2$). Squaring can create answers that solve $\\sqrt{\\dots} = -(\\text{right side})$ instead.',
      '**Two roots:** isolate one root, square, simplify, isolate the remaining root, square again.'),
    WK('ex-26', 'Example 2.6: √(x + 1) = 4', 68, 'Solve $\\sqrt{x + 1} = 4$.',
       ['Square: $x + 1 = 16$.', '$x = 15$.', 'Check: $\\sqrt{16} = 4$ (correct).'], '$x = 15$'),
    ST('extra', 'Example 2.7: √(3x + 1) = x − 3, and the false root', 68, 'extra',
       [('Square: $3x + 1 = x^2 - 6x + 9 \\Rightarrow x^2 - 9x + 8 = 0 \\Rightarrow (x - 8)(x - 1) = 0$.', 'k1'),
        ('Check $x = 8$: $\\sqrt{25} = 5$ and $8 - 3 = 5$ (correct). Check $x = 1$: $\\sqrt{4} = 2$ but $1 - 3 = -2$ (false).', 'k2'),
        ('The graph shows why: $x = 1$ is where the line meets $-\\sqrt{3x + 1}$, the curve that squaring brought in. Solution set $\\{8\\}$.', 'k3')]),
    WK('ex-23a', 'Worked example: two roots (Exercise 2.3, Q3)', 68,
       'Solve $\\sqrt{2x - 5} - \\sqrt{x - 3} = 1$.',
       ['Isolate: $\\sqrt{2x - 5} = 1 + \\sqrt{x - 3}$.', 'Square: $2x - 5 = 1 + 2\\sqrt{x - 3} + x - 3$, so $x - 3 = 2\\sqrt{x - 3}$.',
        'Square again: $(x - 3)^2 = 4(x - 3) \\Rightarrow (x - 3)(x - 7) = 0$, so $x = 3$ or $x = 7$.',
        'Check $x = 3$: $\\sqrt{1} - 0 = 1$ (correct). Check $x = 7$: $\\sqrt{9} - \\sqrt{4} = 1$ (correct).'],
       '$\\{3, 7\\}$'),
    WK('ex-23b', 'Worked example: no solution (Exercise 2.3, Q2)', 68,
       'Solve $2\\sqrt{x + 1} = \\sqrt{x - 7}$.',
       ['Square: $4(x + 1) = x - 7 \\Rightarrow 3x = -11 \\Rightarrow x = -\\frac{11}{3}$.',
        'Check: $x + 1 = -\\frac{8}{3} < 0$, so $\\sqrt{x + 1}$ is not defined.', 'The only candidate fails.'],
       'no solution ($\\varnothing$)'),
    TB('eq-tb', 'Which first step?', 67, ['Equation type', 'First step', 'Watch out'],
       [['$\\sqrt{A} = c$, $c \\ge 0$', 'square: $A = c^2$', 'none'],
        ['$\\sqrt{A} = c$, $c < 0$', 'stop', 'no solution'],
        ['$\\sqrt{A} = $ expression in $x$', 'square, solve quadratic', 'check: right side must be $\\ge 0$'],
        ['$\\sqrt{A} + \\sqrt{B} = c$', 'move one root across, square twice', '$(p + q)^2 = p^2 + 2pq + q^2$'],
        ['$c + \\sqrt{A} = x$', 'isolate $\\sqrt{A}$ first', 'never square before isolating']]),
    RM('rm-23', 'Avoid these slips', 67,
       '$(1 + \\sqrt{x})^2 = 1 + 2\\sqrt{x} + x$, **not** $1 + x$.',
       'A quick filter: in $\\sqrt{A} = B$ any answer must make $B \\ge 0$ and $A \\ge 0$.'),
    'math11-u2-c09', 'math11-u2-rm3',
]

# ------------------------------------------------------------------ 2.4
L4 = [
    T('=math11-u2-c06', '2.4 Inverses of square root functions', 69,
      'A function has an inverse only if it is **one-to-one** (each output comes from one input). The inverse swaps every pair $(a, b)$ to $(b, a)$; e.g. the inverse of $\\{(1, 2), (-3, -4), (0, -1)\\}$ is $\\{(2, 1), (-4, -3), (-1, 0)\\}$.',
      '$y = x^2$ on all reals is **not** one-to-one ($2^2 = (-2)^2$), so it has no inverse. Restrict it to $x \\ge 0$ and it becomes one-to-one; then its inverse is $\\sqrt{x}$.',
      '**Steps to find $f^{-1}$:** (1) write $y = f(x)$; (2) swap $x$ and $y$; (3) solve for $y$ (here: isolate the root and square); (4) **restrict the domain** of $f^{-1}$ to the range of $f$.',
      'The domain of $f^{-1}$ = range of $f$, and the range of $f^{-1}$ = domain of $f$. The graphs are mirror images in the line $y = x$.'),
    ST('inverse', 'Example 2.8: inverse of f(x) = √(x − 1)', 70, 'inverse',
       [('$f$: domain $x \\ge 1$, range $y \\ge 0$; points $(1, 0)$ and $(5, 2)$.', 'k1'),
        ('Swap: $x = \\sqrt{y - 1}$. Square: $x^2 = y - 1$, so $y = x^2 + 1$.', 'k2'),
        ('Restrict to $x \\ge 0$ (range of $f$): $f^{-1}(x) = x^2 + 1$, $x \\ge 0$. Points $(0, 1)$, $(2, 5)$: mirror images in $y = x$.', 'k3')]),
    WK('ex-24a', 'Worked example: Exercise 2.4, Q4', 70,
       'Find the inverse of $h(x) = \\frac{1}{4}\\sqrt{\\frac{3x - 7}{2}} + 4$.',
       ['Range of $h$: root $\\ge 0$, so $y \\ge 4$.', 'Swap: $x = \\frac{1}{4}\\sqrt{\\frac{3y - 7}{2}} + 4 \\Rightarrow 4(x - 4) = \\sqrt{\\frac{3y - 7}{2}}$.',
        'Square: $16(x - 4)^2 = \\frac{3y - 7}{2} \\Rightarrow 3y - 7 = 32(x - 4)^2$.', '$y = \\frac{32(x - 4)^2 + 7}{3}$, with $x \\ge 4$.'],
       '$h^{-1}(x) = \\frac{32(x - 4)^2 + 7}{3}$, $x \\ge 4$'),
    WK('ex-24b', 'Worked example: g(x) = 2 + √x', 70, 'Find $g^{-1}$ for $g(x) = 2 + \\sqrt{x}$.',
       ['Range of $g$: $y \\ge 2$.', 'Swap: $x = 2 + \\sqrt{y} \\Rightarrow \\sqrt{y} = x - 2 \\Rightarrow y = (x - 2)^2$.', 'Restrict: $x \\ge 2$.'],
       '$g^{-1}(x) = (x - 2)^2$, $x \\ge 2$'),
    TB('inv-tb', 'Function and inverse pairs', 70, ['$f(x)$', 'domain / range of $f$', '$f^{-1}(x)$'],
       [['$\\sqrt{x}$', '$x \\ge 0$ / $y \\ge 0$', '$x^2$, $x \\ge 0$'],
        ['$\\sqrt{x - 1}$', '$x \\ge 1$ / $y \\ge 0$', '$x^2 + 1$, $x \\ge 0$'],
        ['$\\sqrt{x + 2}$', '$x \\ge -2$ / $y \\ge 0$', '$x^2 - 2$, $x \\ge 0$'],
        ['$\\sqrt{5x - 2}$', '$x \\ge \\frac{2}{5}$ / $y \\ge 0$', '$\\frac{x^2 + 2}{5}$, $x \\ge 0$'],
        ['$\\sqrt{x/2}$', '$x \\ge 0$ / $y \\ge 0$', '$2x^2$, $x \\ge 0$'],
        ['$2 + \\sqrt{x}$', '$x \\ge 0$ / $y \\ge 2$', '$(x - 2)^2$, $x \\ge 2$']]),
    RM('rm-24', 'Do not forget the restriction', 70,
       '$x^2 + 1$ on its own is not one-to-one. Without "$x \\ge 0$" the answer is wrong.',
       'Check an inverse with one point: $f(5) = 2$, so $f^{-1}(2)$ must be 5: $2^2 + 1 = 5$ (correct).'),
    RM('summary-t', 'Unit summary', 70,
       '$y = a\\sqrt{x - h} + k$ starts at $(h, k)$; $a < 0$ flips it down, $\\sqrt{-x}$ flips it left.',
       'Domain: radicand $\\ge 0$. Range: from $k$ upward (or downward if there is a minus in front).',
       'Radical equations: isolate, square, solve, **check**.',
       'Inverse: swap, solve, restrict $f^{-1}$ to the range of $f$.'),
]

LESSONS = {'math11-u2-l2-1': L1, 'math11-u2-l2-2': L2, 'math11-u2-l2-3': L3, 'math11-u2-l2-4': L4}

# ------------------------------------------------------------------ practice
a = QSet('2.1 Practice — graphs', 's21')
a.S(65, 'Give the starting point and direction of (a) $y = \\sqrt{5x}$ (b) $y = \\sqrt{-3x}$ (c) $y = \\sqrt{3x} + 5$ (d) $y = \\sqrt{-2x} + 4$.', '(0,0) right; (0,0) left; (0,5) right; (0,4) left',
    ['Step 1: inside $= 0$ at $x = 0$ in every case.', 'Step 2: $+5$ and $+4$ move the start up.', 'Step 3: a negative number times $x$ inside makes the graph go left.'],
    'Find where the inside is zero; that is the start.', [('$y = \\sqrt{-x} - 1$?', 'start $(0, -1)$, goes left.')])
a.S(65, 'Sketch $y = \\sqrt{x - 3}$ and $y = \\sqrt{x + 3}$. How are they related?', 'start (3, 0) and (−3, 0); one is the other moved 6 units',
    ['Step 1: $\\sqrt{x - 3}$: start $(3, 0)$, through $(4, 1)$, $(7, 2)$.', 'Step 2: $\\sqrt{x + 3}$: start $(-3, 0)$, through $(-2, 1)$, $(1, 2)$.', 'Step 3: same shape, 6 units apart horizontally.'],
    'Minus inside → right; plus inside → left.', [('$y = \\sqrt{x} - 3$?', 'start $(0, -3)$, moved down.')])
a.S(64, 'Which points with whole-number coordinates lie on $y = \\sqrt{4x}$ for $0 \\le x \\le 9$?', '(0,0), (1,2), (4,4), (9,6)',
    ['Step 1: need $4x$ a perfect square: $x = 0, 1, 4, 9$.', 'Step 2: $y = 2\\sqrt{x}$: 0, 2, 4, 6.'], '$\\sqrt{4x} = 2\\sqrt{x}$.', [('On $y = \\sqrt{9x}$?', '(0,0), (1,3), (4,6), (9,9).')])
a.S(70, 'Review 5: sketch $y = \\sqrt{2x - 1} + 2$.', 'start $(\\frac{1}{2}, 2)$, through (1, 3), (5, 5)',
    ['Step 1: $2x - 1 = 0 \\Rightarrow x = \\frac{1}{2}$; $y = 2$.', 'Step 2: $x = 1$: $\\sqrt{1} + 2 = 3$; $x = 5$: $\\sqrt{9} + 2 = 5$.', 'Step 3: smooth curve to the right.'],
    'Choose $x$ that make the inside a perfect square.', [('$y = \\sqrt{2x + 4} - 1$?', 'start $(-2, -1)$.')])
a.M(63, 'Compared with $y = \\sqrt{x}$, the graph of $y = -\\sqrt{x} + 3$ is', ['reflected in the x-axis and moved up 3', 'reflected in the y-axis and moved up 3', 'moved right 3', 'reflected in the x-axis and moved down 3'], 'A',
    ['Step 1: minus in front → upside down.', 'Step 2: $+3$ → up 3.'], 'Minus outside flips vertically.', [('$y = \\sqrt{-x} + 3$?', 'reflected in the y-axis, up 3.')])
a.M(64, 'Which graph lies **below** $y = \\sqrt{x}$ for $x > 0$?', ['$y = \\sqrt{\\frac{x}{4}}$', '$y = \\sqrt{4x}$', '$y = \\sqrt{x} + 1$', '$y = \\sqrt{2x}$'], 'A',
    ['Step 1: $\\sqrt{x/4} = \\frac{1}{2}\\sqrt{x}$: half the height.'], '$0 < a < 1$ → below.', [('Is $\\sqrt{3x}$ above or below?', 'above.')])
a.S(63, 'Write the equation of $y = \\sqrt{x}$ moved 2 left and 5 down.', '$y = \\sqrt{x + 2} - 5$',
    ['Step 1: left 2 → $x + 2$ inside.', 'Step 2: down 5 → $-5$ outside.'], 'Left = plus inside.', [('Right 4, up 1?', '$y = \\sqrt{x - 4} + 1$.')])
a.TF(62, '$\\sqrt{25} = \\pm 5$.', False,
     ['Step 1: the symbol means the positive root only: $\\sqrt{25} = 5$. The two square roots of 25 are $\\pm\\sqrt{25}$.'], '√ is always ≥ 0.', [('Is $\\sqrt{(-4)^2} = -4$?', 'No, it is 4.')])

b = QSet('2.2 Practice — domain and range', 's22')
b.S(67, 'Find the domain and range: (a) $y = \\sqrt{x - 1}$ (b) $y = \\sqrt{2x - 11}$.', '(a) $x \\ge 1$, $y \\ge 0$ (b) $x \\ge \\frac{11}{2}$, $y \\ge 0$',
    ['Step 1 (a): $x - 1 \\ge 0$.', 'Step 2 (b): $2x \\ge 11$.', 'Step 3: nothing outside, so $y \\ge 0$.'], 'Radicand ≥ 0.', [('$y = \\sqrt{3x + 6}$?', '$x \\ge -2$, $y \\ge 0$.')])
b.S(67, 'Exercise 2.2 Q3: domain and range of $y = \\sqrt{x^2 - 1}$.', '$x \\le -1$ or $x \\ge 1$; $y \\ge 0$',
    ['Step 1: $(x - 1)(x + 1) \\ge 0$.', 'Step 2: outside the roots, ends included.'], 'Upward parabola: "≥ 0" outside.', [('$y = \\sqrt{x^2 - 16}$?', '$x \\le -4$ or $x \\ge 4$, $y \\ge 0$.')])
b.S(67, 'Exercise 2.2 Q4: domain and range of $y = \\sqrt{3 - x^2}$.', '$-\\sqrt{3} \\le x \\le \\sqrt{3}$; $0 \\le y \\le \\sqrt{3}$',
    ['Step 1: $x^2 \\le 3$.', 'Step 2: largest radicand 3 at $x = 0$.'], 'Look for the largest value under the root.', [('$y = \\sqrt{4 - x^2}$?', '$[-2, 2]$, $[0, 2]$.')])
b.S(67, 'Exercise 2.2 Q5 and Q6: domain and range of $y = \\sqrt{x^2 + 1}$ and $y = \\sqrt{x^2 - 6x + 9}$.', 'all reals, $y \\ge 1$; all reals, $y \\ge 0$',
    ['Step 1: $x^2 + 1 \\ge 1$ always; minimum $\\sqrt{1} = 1$.', 'Step 2: $x^2 - 6x + 9 = (x - 3)^2 \\ge 0$ always; $\\sqrt{(x - 3)^2} = |x - 3| \\ge 0$.'],
    'Spot perfect squares.', [('$y = \\sqrt{x^2 + 2x + 1}$?', 'all reals; $y \\ge 0$ (it is $|x + 1|$).')])
b.S(66, 'Domain and range of $y = \\sqrt{6 - 2x} + 1$.', '$x \\le 3$; $y \\ge 1$',
    ['Step 1: $6 - 2x \\ge 0 \\Rightarrow -2x \\ge -6 \\Rightarrow x \\le 3$ (flip!).', 'Step 2: root ≥ 0, plus 1.'], 'Dividing by a negative flips the sign.', [('$y = \\sqrt{4 - x}$?', '$x \\le 4$, $y \\ge 0$.')])
b.S(70, 'Review 1c: domain and range of $y = \\sqrt{x^2 - 16}$.', '$x \\le -4$ or $x \\ge 4$; $y \\ge 0$',
    ['Step 1: $(x - 4)(x + 4) \\ge 0$.', 'Step 2: outside the roots.'], 'Factorise the difference of squares.', [('$y = \\sqrt{x^2 - 25}$?', '$|x| \\ge 5$.')])
b.S(66, 'Domain and range of $y = -2\\sqrt{x + 3} + 4$.', '$x \\ge -3$; $y \\le 4$',
    ['Step 1: $x + 3 \\ge 0$.', 'Step 2: $-2\\sqrt{\\dots} \\le 0$, add 4.'], 'Minus in front → range goes down.', [('$y = 1 - \\sqrt{x}$?', '$x \\ge 0$, $y \\le 1$.')])
b.S(66, 'Domain of $y = \\sqrt{x^2 - 5x + 6}$.', '$x \\le 2$ or $x \\ge 3$',
    ['Step 1: $(x - 2)(x - 3) \\ge 0$.', 'Step 2: outside.'], 'Factorise first.', [('$y = \\sqrt{x^2 - x - 2}$?', '$x \\le -1$ or $x \\ge 2$.')])
b.S(66, 'Domain of $y = \\sqrt{x} + \\sqrt{4 - x}$.', '$0 \\le x \\le 4$',
    ['Step 1: $x \\ge 0$ and $4 - x \\ge 0$.', 'Step 2: both together.'], 'Two roots → both radicands ≥ 0.', [('$y = \\sqrt{x - 1} + \\sqrt{5 - x}$?', '$1 \\le x \\le 5$.')])
b.M(66, 'The range of $y = \\sqrt{x^2 + 9}$ is', ['$y \\ge 3$', '$y \\ge 0$', '$y \\ge 9$', 'all reals'], 'A',
    ['Step 1: smallest radicand 9 at $x = 0$; $\\sqrt{9} = 3$.'], 'Minimum of the radicand → minimum of $y$.', [('Range of $\\sqrt{x^2 + 4}$?', '$y \\ge 2$.')])
b.TF(66, 'The domain of $y = \\sqrt{x^2 - 9}$ is $x \\ge 3$.', False,
     ['Step 1: $x = -5$ gives $\\sqrt{16} = 4$, so negative values also work: $x \\le -3$ or $x \\ge 3$.'], 'Test a value on the other side.', [('Is $x = -3$ in the domain?', 'Yes, $\\sqrt{0} = 0$.')])

c = QSet('2.3 Practice — radical equations', 's23')
c.S(68, 'Exercise 2.3 Q1: solve $\\sqrt{3x + 8} = 10$.', '$x = \\frac{92}{3}$',
    ['Step 1: square: $3x + 8 = 100$.', 'Step 2: $3x = 92$.', 'Step 3: check: $\\sqrt{100} = 10$ (correct).'], 'Right side positive → one square is enough.', [('$\\sqrt{3x + 8} = 4$?', '$x = \\frac{8}{3}$.')])
c.S(68, 'Exercise 2.3 Q4: solve $\\sqrt{x + 2} + \\sqrt{3x + 4} = 2$.', '$x = -1$',
    ['Step 1: $\\sqrt{3x + 4} = 2 - \\sqrt{x + 2}$; square: $3x + 4 = 4 - 4\\sqrt{x + 2} + x + 2$.', 'Step 2: $2x - 2 = -4\\sqrt{x + 2} \\Rightarrow 1 - x = 2\\sqrt{x + 2}$.',
     'Step 3: square: $x^2 - 2x + 1 = 4x + 8 \\Rightarrow x^2 - 6x - 7 = 0 \\Rightarrow x = 7$ or $-1$.', 'Step 4: check: $x = -1$: $1 + 1 = 2$ (correct); $x = 7$: $3 + 5 = 8$ (false).'],
    'Two roots → square twice, check at the end.', [('$\\sqrt{x} + \\sqrt{x + 5} = 5$?', '$x = 4$.')])
c.S(70, 'Review 2a: solve $3 + \\sqrt{x - 1} = x$.', '$x = 5$',
    ['Step 1: isolate: $\\sqrt{x - 1} = x - 3$.', 'Step 2: $x - 1 = x^2 - 6x + 9 \\Rightarrow x^2 - 7x + 10 = 0$: $x = 2$ or 5.', 'Step 3: check: $x = 5$: $3 + 2 = 5$ (correct); $x = 2$: $3 + 1 = 4 \\ne 2$ (false).'],
    'Isolate the root before squaring.', [('$x - \\sqrt{x} = 6$?', '$x = 9$.')])
c.S(70, 'Review 2b: solve $\\sqrt{2x + 9} - \\sqrt{x + 1} = 2$.', '$x = 0$ or $x = 8$',
    ['Step 1: $\\sqrt{2x + 9} = 2 + \\sqrt{x + 1}$; square: $2x + 9 = 4 + 4\\sqrt{x + 1} + x + 1$.', 'Step 2: $x + 4 = 4\\sqrt{x + 1}$; square: $x^2 + 8x + 16 = 16x + 16 \\Rightarrow x(x - 8) = 0$.', 'Step 3: check 0: $3 - 1 = 2$ (correct); 8: $5 - 3 = 2$ (correct).'],
    'Both can be real: always check.', [('$\\sqrt{x + 7} - \\sqrt{x} = 1$?', '$x = 9$.')])
c.S(70, 'Review 2c: solve $5 + \\sqrt{x + 6} = 8$.', '$x = 3$',
    ['Step 1: $\\sqrt{x + 6} = 3$.', 'Step 2: $x + 6 = 9$.'], 'Isolate first.', [('$2 + \\sqrt{x} = 7$?', '$x = 25$.')])
c.S(67, 'Activity 2.4: solve $\\sqrt{x + 7} = x - 5$.', '$x = 9$',
    ['Step 1: need $x \\ge 5$ (right side ≥ 0).', 'Step 2: $x + 7 = x^2 - 10x + 25 \\Rightarrow x^2 - 11x + 18 = 0$: $x = 9$ or 2.', 'Step 3: $x = 2 < 5$ is false; $\\sqrt{16} = 4 = 9 - 5$ (correct).'], 'Use $B \\ge 0$ as a quick filter.', [('$\\sqrt{x + 1} = x - 1$?', '$x = 3$.')])
c.S(68, 'Solve $\\sqrt{x - 3} = -2$.', 'no solution',
    ['Step 1: a square root is never negative.', 'Step 2: (squaring gives $x = 7$, but $\\sqrt{4} = 2 \\ne -2$.)'], 'Look before you square.', [('$\\sqrt{2x} + 5 = 1$?', 'no solution.')])
c.S(68, 'Solve $\\sqrt{5x - 1} = \\sqrt{x + 7}$.', '$x = 2$',
    ['Step 1: square: $5x - 1 = x + 7$.', 'Step 2: $x = 2$; check: $\\sqrt{9} = \\sqrt{9}$ (correct).'], 'Root = root: just square once.', [('$\\sqrt{2x + 3} = \\sqrt{x + 5}$?', '$x = 2$.')])
c.S(68, 'Solve $\\sqrt{2x + 3} = x$.', '$x = 3$',
    ['Step 1: $2x + 3 = x^2 \\Rightarrow (x - 3)(x + 1) = 0$.', 'Step 2: $x = -1$ is false (right side negative).'], 'Right side must be ≥ 0.', [('$\\sqrt{x + 6} = x$?', '$x = 3$.')])
c.S(70, 'Review 3 (completed): solve $b = \\sqrt{c^2 - a^2}$ for $a$ ($a > 0$).', '$a = \\sqrt{c^2 - b^2}$',
    ['Step 1: square: $b^2 = c^2 - a^2$.', 'Step 2: $a^2 = c^2 - b^2$, take the positive root.'], 'The book prints only "$\\sqrt{c^2 - a^2}$": an equation is needed, as here (Pythagoras).', [('Solve $r = \\sqrt{A/\\pi}$ for $A$.', '$A = \\pi r^2$.')])
c.S(70, 'Review 4 (completed): the pendulum period is $T = 2\\pi\\sqrt{\\frac{l}{g}}$. Solve for $l$.', '$l = \\frac{gT^2}{4\\pi^2}$',
    ['Step 1: $\\frac{T}{2\\pi} = \\sqrt{\\frac{l}{g}}$.', 'Step 2: square: $\\frac{T^2}{4\\pi^2} = \\frac{l}{g}$.', 'Step 3: multiply by $g$.'], 'Isolate the root, square, then solve.', [('Solve $v = \\sqrt{2gh}$ for $h$.', '$h = \\frac{v^2}{2g}$.')])
c.M(68, 'Squaring both sides of $\\sqrt{x + 3} = x - 3$ gives', ['$x^2 - 7x + 6 = 0$', '$x^2 - 5x + 6 = 0$', '$x + 3 = x^2 + 9$', '$x^2 - 6x = 0$'], 'A',
    ['Step 1: $x + 3 = x^2 - 6x + 9$.', 'Step 2: $x^2 - 7x + 6 = 0$, roots 6 and 1; only 6 checks.'], '$(x - 3)^2$ has a middle term.', [('Which root is real?', '$x = 6$.')])
c.TF(67, 'If $a^2 = b^2$ then $a = b$.', False,
     ['Step 1: $(-3)^2 = 3^2$ but $-3 \\ne 3$. This is why squaring can add false roots.'], 'Only "$a = b \\Rightarrow a^2 = b^2$" is always true.', [('If $a = b$, is $a^3 = b^3$?', 'Yes.')])

d = QSet('2.4 Practice — inverses', 's24')
d.S(70, 'Exercise 2.4 Q1: find the inverse of $f(x) = \\sqrt{5x - 2}$.', '$f^{-1}(x) = \\frac{x^2 + 2}{5}$, $x \\ge 0$',
    ['Step 1: swap: $x = \\sqrt{5y - 2}$.', 'Step 2: $x^2 = 5y - 2 \\Rightarrow y = \\frac{x^2 + 2}{5}$.', 'Step 3: range of $f$ is $y \\ge 0$, so $x \\ge 0$.'], 'Swap, square, solve, restrict.', [('$f(x) = \\sqrt{3x + 1}$?', '$\\frac{x^2 - 1}{3}$, $x \\ge 0$.')])
d.S(70, 'Exercise 2.4 Q2 and Q3: inverses of $f(x) = \\sqrt{x + 2}$ and $g(x) = \\sqrt{\\frac{x}{2}}$.', '$x^2 - 2$; $2x^2$ (both $x \\ge 0$)',
    ['Step 1: $x = \\sqrt{y + 2} \\Rightarrow y = x^2 - 2$.', 'Step 2: $x = \\sqrt{y/2} \\Rightarrow y = 2x^2$.', 'Step 3: both ranges are $y \\ge 0$.'], 'Restriction = range of $f$.', [('$\\sqrt{x/3}$?', '$3x^2$, $x \\ge 0$.')])
d.S(70, 'Review 6: find the inverse of $f(x) = \\sqrt{x - 4}$ and check with one point.', '$x^2 + 4$, $x \\ge 0$',
    ['Step 1: swap and square: $x^2 = y - 4$.', 'Step 2: $f(8) = 2$ and $f^{-1}(2) = 8$ (correct).'], 'Check with a pair of points.', [('$f(x) = \\sqrt{x + 9}$?', '$x^2 - 9$, $x \\ge 0$.')])
d.S(69, 'Find the inverse of $f(x) = 3 - \\sqrt{x}$ and its domain.', '$f^{-1}(x) = (3 - x)^2$, $x \\le 3$',
    ['Step 1: range of $f$: $y \\le 3$.', 'Step 2: $x = 3 - \\sqrt{y} \\Rightarrow \\sqrt{y} = 3 - x \\Rightarrow y = (3 - x)^2$.', 'Step 3: domain of $f^{-1}$: $x \\le 3$.'], 'Minus in front → range goes down.', [('$f(x) = 1 - \\sqrt{x}$?', '$(1 - x)^2$, $x \\le 1$.')])
d.S(69, 'Find the inverse of $f(x) = x^2 - 4$, $x \\ge 0$.', '$f^{-1}(x) = \\sqrt{x + 4}$, $x \\ge -4$',
    ['Step 1: swap: $x = y^2 - 4$.', 'Step 2: $y^2 = x + 4$, $y \\ge 0$: $y = \\sqrt{x + 4}$.'], 'Square ↔ square root.', [('$f(x) = x^2 + 1$, $x \\ge 0$?', '$\\sqrt{x - 1}$, $x \\ge 1$.')])
d.S(69, 'Activity 2.5: write the inverse of $\\{(1, 2), (-3, -4), (0, -1)\\}$. Is $f(x) = x + 1$ invertible?', '$\\{(2, 1), (-4, -3), (-1, 0)\\}$; yes, $f^{-1}(x) = x - 1$',
    ['Step 1: swap each pair.', 'Step 2: $x + 1$ is one-to-one; $y = x + 1 \\Rightarrow$ swap: $x = y + 1$.'], 'One-to-one ⇔ invertible.', [('Inverse of $\\{(2, 5), (3, 7)\\}$?', '$\\{(5, 2), (7, 3)\\}$.')])
d.M(69, 'Why is $f(x) = x^2$ (all real $x$) not invertible?', ['two inputs give the same output', 'it is not continuous', 'its range is all reals', 'it has no zeros'], 'A',
    ['Step 1: $f(2) = f(-2) = 4$: not one-to-one.'], 'Horizontal line test.', [('Fix?', 'restrict to $x \\ge 0$.')])
d.TF(70, 'The domain of $f^{-1}$ is the range of $f$.', True, ['Step 1: swapping $x$ and $y$ swaps the domain and range.'], 'Inverse swaps everything.', [('Range of $f^{-1}$ if $f$ has domain $x \\ge 1$?', '$y \\ge 1$.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Principal square root', '$\\sqrt{a}$, the non-negative square root of $a \\ge 0$.', 62),
    ('Radicand', 'The expression under the root sign.', 66),
    ('Radical equation', 'An equation with the unknown under a root.', 67),
    ('Extraneous root', 'A false answer created by squaring; it fails the original equation.', 68),
    ('One-to-one function', 'Different inputs always give different outputs.', 69),
    ('Inverse function', '$f^{-1}$ undoes $f$: swap $x$ and $y$; graphs mirror in $y = x$.', 69),
]
TIPS = [('y = √(x − h) + k starts at (h, k).', 63), ('Radical equation: isolate, square, solve, CHECK.', 67),
        ('Inverse: domain of f⁻¹ = range of f.', 70)]
IDEAS = [('family', 'Moving √x', 'l2_1', 'math11-u2-md-family-t'), ('dom', 'Radicand ≥ 0', 'l2_2', 'math11-u2-md-dom-t'),
         ('check', 'Check for false roots', 'l2_3', 'math11-u2-c05'), ('inv', 'Swap, solve, restrict', 'l2_4', 'math11-u2-c06')]
