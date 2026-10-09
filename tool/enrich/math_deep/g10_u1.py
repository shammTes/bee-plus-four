r"""Grade 10 Unit 1 — Foundations for Functions (textbook pp. 1-29)."""
import math
from common import set_unit, T, RM, MN, TB, DG, WK, GR, CK, QSet, plane
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import arrow_diagram, machine, side_by_side

UID = 'math10-u1'
set_unit(UID)

# ------------------------------------------------------------------ figures
def f_ways():
    a = arrow_diagram([(1, 2), (2, 3), (5, 6)], [1, 2, 3, 5, 6], [1, 2, 3, 5, 6])
    p = Plot(0, 7, 0, 7, unit=19)
    for x, y in [(1, 2), (2, 3), (5, 6)]:
        p.pt(x, y, f'({x}, {y})', 'nw' if x == 5 else 'ne', size=11)
    return side_by_side([a, p], labels=['Arrow diagram', 'Graph (discrete points)'])


def f_discrete():
    a = Plot(-3, 3, -6, 4, unit=17)
    for x in range(-2, 3):
        a.pt(x, 2 * x - 1, None)
    b = Plot(-3, 3, -2, 8, unit=17)
    b.fn(lambda x: x * x - 1, -3, 3, BLUE)
    return side_by_side([a, b], 16, ['Discrete: y = 2x − 1', 'Continuous: y = x² − 1'])


def f_fn_or_not():
    a = arrow_diagram([(-1, 0), (1, 2), (0, 3), (4, 2), (5, 0)], [-1, 0, 1, 4, 5], [0, 2, 3], 'x', 'y')
    b = arrow_diagram([(13, 14), (16, 7), (13, 5), (18, 13)], [13, 16, 18], [5, 7, 13, 14], 'x', 'y', hl={13})
    return side_by_side([a, b], 10, ['S: a function', 'Not a function: 13 has two arrows'])


def f_vlt():
    a = Plot(-3, 3, -4, 4, unit=20)
    a.fn(lambda x: -x * x + 3, -3, 3, BLUE)
    a.fullline(x=1.3, c=RED, w=2, dash=True)
    a.pt(1.3, -1.3 ** 2 + 3, None, c=RED)
    b = Plot(-3, 4, -4, 4, unit=20)
    b.param(lambda t: t * t - 1, lambda t: t, -3, 3)
    b.fullline(x=2, c=RED, w=2, dash=True)
    b.pt(2, math.sqrt(3), None, c=RED).pt(2, -math.sqrt(3), None, c=RED)
    return side_by_side([a, b], 14, ['y = 3 − x²: a function', 'x = y² − 1: not a function'])


def f_domain_range():
    p = Plot(-4, 4, -1, 4, unit=34)
    p.fn(lambda x: math.sqrt(max(0, 9 - x * x)), -3, 3, BLUE, 2.8)
    p.pt(-3, 0, '(−3, 0)', 'nw', BLUE).pt(3, 0, '(3, 0)', 'ne', BLUE).pt(0, 3, '(0, 3)', 'ne', BLUE)
    p.line(p.X(-3), p.Y(0) + 0, p.X(3), p.Y(0), GREEN, 7, op=0.45)
    p.line(p.X(0), p.Y(0), p.X(0), p.Y(3), ORANGE, 7, op=0.5)
    p.text(p.X(2.2), p.Y(-0.62), 'domain −3 ≤ x ≤ 3', 12, GREEN)
    p.text(p.X(0.15), p.Y(1.5), 'range 0 ≤ y ≤ 3', 12, ORANGE, 'start')
    return p


def f_machine():
    return machine('x', 'rule: subtract x from 4, then take the square root', 'f(x) = √(4 − x)')


def f_hlt():
    a = Plot(-3, 3, -2, 6, unit=20)
    a.fn(lambda x: x * x, -2.5, 2.5, BLUE)
    a.fullline(0, 2.5, c=RED, w=2, dash=True)
    a.pt(-math.sqrt(2.5), 2.5, None, c=RED).pt(math.sqrt(2.5), 2.5, None, c=RED)
    b = Plot(-3, 3, -4, 4, unit=20)
    b.fn(lambda x: x ** 3 / 2, -2.5, 2.5, BLUE)
    b.fullline(0, 1.5, c=GREEN, w=2, dash=True)
    b.pt((3) ** (1 / 3), 1.5, None, c=GREEN)
    return side_by_side([a, b], 14, ['y = x²: NOT one-to-one', 'y = ½x³: one-to-one'])


def f_inverse_arrows():
    a = arrow_diagram([(-1, 2), (-3, 1), (0, -2), (5, 6)], [-3, -1, 0, 5], [-2, 1, 2, 6], 'x', 'f(x)')
    b = arrow_diagram([(2, -1), (1, -3), (-2, 0), (6, 5)], [-2, 1, 2, 6], [-3, -1, 0, 5], 'x', 'f', c=PURPLE, rsup=('−1', '(x)'))
    return side_by_side([a, b], 10, ['the function f', 'its inverse: every arrow reversed'])


def f_reflect_pts():
    p = Plot(-4, 4, -4, 4, unit=30)
    p.fullline(1, 0, c=GREY, w=2, dash=True, lab='y = x', labx=3.2, labpos='nw')
    for (a, b), col in [((3, 1), BLUE), ((-2, 0), RED), ((-1, 2), GREEN)]:
        p.seg((a, b), (b, a), col, 1.4, dash='3 3')
        p.pt(a, b, f'({a}, {b})'.replace('-', '−'), 'se' if a > b else 'nw', col)
        p.pt(b, a, f'({b}, {a})'.replace('-', '−'), 'nw' if a > b else 'se', col)
    return p


def f_sqrt_inverse():
    p = Plot(-1, 5, -1, 5, unit=44)
    p.fullline(1, 0, c=GREY, w=2, dash=True, lab='y = x', labx=4.4, labpos='nw')
    p.fn(lambda x: x * x, 0, 2.3, BLUE)
    p.fn(lambda x: math.sqrt(x), 0, 5, RED)
    p.text(p.X(-0.85), p.Y(4.65), 'f(x) = x², x ≥ 0', 12.5, BLUE, 'start')
    p.sup(p.X(2.9), p.Y(1.25), 'f', '−1', '(x) = √x', 12.5, RED, 'start')
    p.pt(2, 4, '(2, 4)', 'e', BLUE).pt(4, 2, '(4, 2)', 'n', RED)
    return p


def f_line_test_summary():
    f = Fig(320, 150)
    f.rect(8, 8, 148, 134, BLUE, 1.6, FILL[BLUE], 12)
    f.rect(164, 8, 148, 134, PURPLE, 1.6, FILL[PURPLE], 12)
    f.text(82, 30, 'Vertical line test', 13, BLUE)
    f.text(238, 30, 'Horizontal line test', 13, PURPLE)
    f.line(82, 44, 82, 120, RED, 2.2, dash=True)
    f.path('M30 110 Q82 30 134 110', BLUE, 2.4)
    f.text(82, 136, 'is it a FUNCTION?', 11.5, INK)
    f.line(178, 80, 298, 80, RED, 2.2, dash=True)
    f.path('M186 120 C 220 40, 256 120, 292 40', PURPLE, 2.4)
    f.text(238, 136, 'is it ONE-TO-ONE?', 11.5, INK)
    return f


DIAGRAMS = {
    'ways': (f_ways(), 'R = {(1, 2), (2, 3), (5, 6)} drawn two ways', 3),
    'discrete': (f_discrete(), 'Discrete graph (separate points) vs continuous graph (unbroken curve)', 4),
    'fnornot': (f_fn_or_not(), 'Arrow diagrams: a function and a relation that is not a function', 6),
    'vlt': (f_vlt(), 'Vertical line test', 10),
    'domrange': (f_domain_range(), 'Reading the domain and range from a graph (upper half of a circle)', 10),
    'machine': (f_machine(), 'A function machine', 15),
    'hlt': (f_hlt(), 'Horizontal line test', 19),
    'invarrows': (f_inverse_arrows(), 'A one-to-one function and its inverse', 22),
    'reflectpts': (f_reflect_pts(), 'Swapping the coordinates reflects a point in the line y = x', 25),
    'sqrtinv': (f_sqrt_inverse(), 'f(x) = x² (x ≥ 0) and its inverse √x are mirror images in y = x', 26),
    'tests': (f_line_test_summary(), 'Which line test answers which question', 19),
}

# ------------------------------------------------------------------ lesson 1.1
L11 = [
    T('=math10-u1-c01', '1.1.1 Relations — pairing things up', 2,
      'In daily life we pair things all the time: a person with their age, a town with its zoba, a number with a bigger number. Mathematics records each pairing as an **ordered pair** $(x, y)$: the order matters, because "Hagos is the father of Selam" is not the same as "Selam is the father of Hagos".',
      '**A relation** is any set of ordered pairs. We name relations with capital letters $R, S, T, \\dots$',
      '- The **domain** of a relation is the set of all **first** elements (the $x$-values, the inputs).',
      '- The **range** of a relation is the set of all **second** elements (the $y$-values, the outputs).',
      'Example: $R = \\{(1, 2), (2, 3), (5, 6)\\}$ has domain $\\{1, 2, 5\\}$ and range $\\{2, 3, 6\\}$. Read the first numbers for the domain, the second numbers for the range — never mix them.',
      'A relation can also be described by a rule, for example $R = \\{(x, y) : y = x + 1\\}$, read "the set of all pairs $(x, y)$ such that $y = x + 1$". A pair belongs to $R$ exactly when it makes the rule true: $(5, 6)$ belongs because $6 = 5 + 1$; $(3, 5)$ does not because $5 \\ne 3 + 1$.'),
    TB('ways-t', 'Five ways to describe the same relation', 3, ['Way', 'R: "a number is paired with the number one larger"'],
       [['Words', 'each number is assigned to the number larger than it by one'],
        ['Set of ordered pairs', '$R = \\{(1, 2), (2, 3), (5, 6)\\}$'],
        ['Table of values', '$x$: 1, 2, 5  →  $y$: 2, 3, 6'],
        ['Arrow diagram', 'an arrow from each $x$ in the domain oval to its $y$ in the range oval'],
        ['Graph', 'the points $(1, 2), (2, 3), (5, 6)$ plotted on the plane'],
        ['Algebraic rule', '$R = \\{(x, y) : y = x + 1\\}$']],
       'All six rows describe one and the same relation. In exams you are often given one form and asked for another — change form carefully, pair by pair.'),
    DG('ways', 'The same relation as an arrow diagram and as a graph', 3, 'ways',
       'Each arrow in the left picture is one ordered pair. Each dot in the right picture is the same ordered pair plotted: go right $x$ units, then up $y$ units.'),
    WK('ex-rule', 'Worked example: from a rule to every form', 4,
       'Let $R = \\{(x, y) : y = 2x - 1\\}$ with domain $\\{-2, -1, 0, 1, 2\\}$. List $R$ as ordered pairs, give its range and say whether the graph is discrete or continuous.',
       ['Put each domain value into the rule $y = 2x - 1$: $x = -2 \\Rightarrow y = 2(-2) - 1 = -5$.',
        '$x = -1 \\Rightarrow y = -3$; $x = 0 \\Rightarrow y = -1$; $x = 1 \\Rightarrow y = 1$; $x = 2 \\Rightarrow y = 3$.',
        'Write the pairs: $R = \\{(-2, -5), (-1, -3), (0, -1), (1, 1), (2, 3)\\}$.',
        'Range = the set of all second elements $= \\{-5, -3, -1, 1, 3\\}$.',
        'The domain has only 5 separate numbers, so the graph is 5 separate dots: a **discrete** graph. (If the domain were all real numbers, the dots would join into an unbroken line: a **continuous** graph.)'],
       '$R = \\{(-2,-5),(-1,-3),(0,-1),(1,1),(2,3)\\}$, range $\\{-5,-3,-1,1,3\\}$, discrete'),
    DG('discrete', 'Discrete or continuous?', 4, 'discrete',
       '**Discrete**: the domain is a list of separate values, so the graph is separate dots — do not join them. **Continuous**: the domain is an interval or all real numbers, so the graph is an unbroken line or curve.'),
    T('=math10-u1-c02', '1.1.2 Functions — exactly one output for each input', 6,
      '**A function** is a special relation: every element of the domain is paired with **exactly one** element of the range.',
      'How to test a relation given as ordered pairs:',
      '- Look only at the **first** elements.',
      '- If some first element appears twice with **different** second elements, the relation is **not** a function.',
      '- If every first element appears once (or repeats with the same partner), it **is** a function.',
      'In an arrow diagram: a relation is a function when **exactly one arrow leaves each element of the domain**. Two arrows leaving the same $x$ ⇒ not a function. Two arrows **arriving** at the same $y$ is allowed.',
      'Example: $S = \\{(-1, 0), (1, 2), (0, 3), (4, 2), (5, 0)\\}$ is a function — the outputs 0 and 2 repeat, but no input repeats. $\\{(13, 14), (16, 7), (13, 5), (18, 13)\\}$ is not a function: the input 13 goes to both 14 and 5.'),
    DG('fnornot', 'Counting arrows that LEAVE each input', 6, 'fnornot',
       'Left: every input sends out one arrow (outputs 0 and 2 receive two arrows — that is fine). Right: 13 sends out two arrows, so this relation is not a function.'),
    TB('relfun', 'Relation or function? How the two ideas differ', 6, ['', 'Relation', 'Function'],
       [['What it is', 'any set of ordered pairs', 'a relation with one output per input'],
        ['Same input, two outputs?', 'allowed', '**not** allowed'],
        ['Same output for two inputs?', 'allowed', 'allowed'],
        ['Arrow diagram', 'any arrows', 'exactly one arrow leaves each $x$'],
        ['Graph test', '—', 'passes the vertical line test'],
        ['Example', '$\\{(1, 2), (1, 3)\\}$', '$\\{(1, 2), (3, 2)\\}$']],
       'Every function is a relation, but not every relation is a function.'),
    WK('ex-fn', 'Worked example: which relations are functions?', 7,
       'Decide which are functions: $R = \\{(3, 90), (4, 54), (6, 71), (8, 90)\\}$, $T = \\{(3, 4), (4, 5), (6, 7), (3, 9)\\}$, $W = \\{(0, 0), (2, 2), (2, -2), (6, 8), (6, -8)\\}$.',
       ['$R$: first elements 3, 4, 6, 8 — all different. The repeated output 90 does not matter. $R$ **is a function**.',
        '$T$: first elements 3, 4, 6, 3 — the input 3 appears with 4 and with 9. $T$ is **not** a function.',
        '$W$: input 2 goes to 2 and $-2$; input 6 goes to 8 and $-8$. $W$ is **not** a function.'],
       'Only $R$ is a function.'),
    WK('ex-x', 'Worked example: which value can x NOT take?', 8,
       'For $R = \\{(8, 1), (3, 4), (6, 7), (x, 22)\\}$ to be a function, which numbers can $x$ not be?',
       ['A function cannot pair one input with two different outputs.',
        'If $x = 8$, the input 8 would go to 1 and to 22 — not allowed. Same for $x = 3$ (4 and 22) and $x = 6$ (7 and 22).',
        'Any other value of $x$ is a new input, which is fine.'],
       '$x \\ne 8, 3, 6$'),
    T('=math10-u1-c03', '1.1.3 Graphs of functions — the vertical line test', 10,
      'On a graph, two points with the same $x$-value lie on the same **vertical** line. So a graph shows a function exactly when no vertical line meets it twice.',
      '**Vertical line test:** if some vertical line crosses the graph at more than one point, the relation is **not** a function. If every vertical line crosses it at most once, it **is** a function.',
      'Reading domain and range from a graph:',
      '- **Domain**: squash the graph flat onto the $x$-axis — the $x$-values it covers.',
      '- **Range**: squash the graph flat onto the $y$-axis — the $y$-values it covers.',
      '- An arrow at the end of a graph means it continues for ever in that direction; a filled dot is an end point that belongs to the graph; an open dot is an end point that does not.'),
    DG('vlt', 'Sweep a vertical line across the graph', 10, 'vlt',
       'Left: wherever you place the dashed line it meets the parabola once, so $y = 3 - x^2$ is a function. Right: the line $x = 2$ meets the curve $x = y^2 - 1$ at $(2, \\sqrt3)$ and $(2, -\\sqrt3)$ — one input, two outputs — not a function.'),
    DG('domrange', 'Domain and range by "squashing" the graph', 10, 'domrange',
       'The graph of $y = \\sqrt{9 - x^2}$ is the top half of a circle of radius 3. Its shadow on the $x$-axis (green) is $-3 \\le x \\le 3$ — the domain. Its shadow on the $y$-axis (orange) is $0 \\le y \\le 3$ — the range.'),
    TB('graphs-t', 'Domain and range of graphs you meet often', 10, ['Graph', 'Domain', 'Range', 'Function?'],
       [['Non-vertical line $y = mx + b$, $m \\ne 0$', 'all real numbers', 'all real numbers', 'yes'],
        ['Horizontal line $y = 2$', 'all real numbers', '$\\{2\\}$', 'yes'],
        ['Vertical line $x = 2$', '$\\{2\\}$', 'all real numbers', 'no'],
        ['Parabola $y = x^2$', 'all real numbers', '$y \\ge 0$', 'yes'],
        ['Parabola $y = 3 - x^2$', 'all real numbers', '$y \\le 3$', 'yes'],
        ['Sideways parabola $x = y^2$', '$x \\ge 0$', 'all real numbers', 'no'],
        ['Circle $x^2 + y^2 = 9$', '$-3 \\le x \\le 3$', '$-3 \\le y \\le 3$', 'no'],
        ['Upper semicircle $y = \\sqrt{9 - x^2}$', '$-3 \\le x \\le 3$', '$0 \\le y \\le 3$', 'yes']]),
    T('=math10-u1-c04', '1.1.4 Function notation f(x)', 12,
      'When an equation gives exactly one $y$ for each $x$, we say **$y$ is a function of $x$**. $x$ is the **independent variable** (you choose it); $y$ is the **dependent variable** (it depends on $x$).',
      'To decide whether an equation gives $y$ as a function of $x$, **solve for $y$**: if you get one value of $y$ for each $x$ it is a function; if you get "$\\pm$" (two values) it is not. Example: $y + x^2 = 1$ gives $y = 1 - x^2$ (one value) — a function. $y^2 - x^2 = 1$ gives $y = \\pm\\sqrt{1 + x^2}$ — when $x = 0$, $y = 1$ or $-1$ — not a function.',
      'Functions are named with small letters $f, g, h$. Instead of $y = 4x + 3$ we write $f(x) = 4x + 3$, read "**f of x**". $f(1)$ means "the output when the input is 1": $f(1) = 4(1) + 3 = 7$, so the point $(1, 7)$ is on the graph. Note: $f(x)$ does **not** mean $f$ times $x$.',
      'To evaluate $f(a)$: replace **every** $x$ in the formula by $a$ in brackets, then simplify. Brackets matter with negatives: if $g(x) = x^2 - 4$ then $g(-2) = (-2)^2 - 4 = 0$, not $-2^2 - 4 = -8$.'),
    DG('machine', 'A function is like a machine', 15, 'machine',
       'Put an input $x$ in, the machine follows its rule, one output comes out. For $f(x) = \\sqrt{4 - x}$: input 0 gives 2, input 3 gives 1, input $-5$ gives 3. Input 5 jams the machine ($\\sqrt{-1}$ is not real), so 5 is not in the domain. The outputs are never negative, so the range is $y \\ge 0$.'),
    TB('domrules', 'Finding the domain of a formula', 14, ['If the formula has…', 'Condition', 'Example → domain'],
       [['only $+, -, \\times$ and powers (polynomial)', 'none', '$2x^3 - 5x + 1$ → all real numbers'],
        ['a fraction', 'denominator $\\ne 0$', '$\\frac{x}{x + 1}$ → $x \\ne -1$'],
        ['an even root $\\sqrt{\\;\\;}$', 'inside $\\ge 0$', '$\\sqrt{x - 4}$ → $x \\ge 4$'],
        ['an even root in a denominator', 'inside $> 0$', '$\\frac{1}{\\sqrt{4 - 2x}}$ → $x < 2$'],
        ['an odd root $\\sqrt[3]{\\;\\;}$', 'none', '$\\sqrt[3]{x - 1}$ → all real numbers']],
       'Rule of thumb: start from "all real numbers" and throw away only the $x$-values that break the formula (divide by zero, square root of a negative).'),
    WK('ex-eval', 'Worked example: evaluating a function', 14,
       'Let $g(x) = x^2 - 4$. Find $g(-2)$, $g(3)$ and $g(\\sqrt5)$, and write the matching ordered pairs.',
       ['$g(-2) = (-2)^2 - 4 = 4 - 4 = 0$.',
        '$g(3) = 3^2 - 4 = 9 - 4 = 5$.',
        '$g(\\sqrt5) = (\\sqrt5)^2 - 4 = 5 - 4 = 1$.',
        'Each input with its output is a point on the graph of $g$.'],
       '$(-2, 0)$, $(3, 5)$, $(\\sqrt5, 1)$'),
    WK('ex-notation', 'Worked example: writing an equation in function notation', 13,
       'Write $f = \\{(x, y) : 2x^2 + 2y - 4 = 0\\}$ in function notation.',
       ['Isolate $y$: $2y = -2x^2 + 4$ (subtract $2x^2$, add 4).',
        'Divide by 2: $y = -x^2 + 2$.',
        'There is one $y$ for each $x$, so replace $y$ by $f(x)$.'],
       '$f(x) = -x^2 + 2$'),
    WK('ex-domain', 'Worked example: domains of formulas', 15,
       'Find the domain of (a) $f(x) = \\sqrt{4 - 2x}$, (b) $h(x) = \\frac{1 - 5x}{x^2 - 1}$, (c) $k(x) = \\frac{3}{\\sqrt{x + 2}}$.',
       ['(a) Square root: need $4 - 2x \\ge 0 \\Rightarrow -2x \\ge -4 \\Rightarrow x \\le 2$ (dividing by a negative flips the sign). Domain $\\{x : x \\le 2\\}$.',
        '(b) Fraction: need $x^2 - 1 \\ne 0 \\Rightarrow x^2 \\ne 1 \\Rightarrow x \\ne 1$ and $x \\ne -1$. Domain $\\{x : x \\ne \\pm 1\\}$.',
        '(c) Root in a denominator: need $x + 2 > 0$ (not $= 0$, we cannot divide by 0). Domain $\\{x : x > -2\\}$.'],
       '(a) $x \\le 2$  (b) $x \\ne \\pm1$  (c) $x > -2$'),
    WK('ex-tea', 'Worked example: a function in real life', 16,
       'A tea shop makes a profit of 0.40 Nakfa on each cup and pays 70 Nakfa rent a month, so the monthly profit is $p = 0.4c - 70$ for $c$ cups. Write it as a function $f$, find the profit for 100 and 300 cups, and give the domain.',
       ['Each number of cups gives one profit, so $p$ is a function of $c$: $f(c) = 0.4c - 70$.',
        '$f(100) = 0.4(100) - 70 = 40 - 70 = -30$: a **loss** of 30 Nakfa.',
        '$f(300) = 0.4(300) - 70 = 120 - 70 = 50$: a profit of 50 Nakfa.',
        'Break-even: $0.4c - 70 = 0 \\Rightarrow c = 175$ cups.',
        'Cups are counted, so $c$ cannot be negative or a fraction: domain $\\{0, 1, 2, 3, \\dots\\}$.'],
       '$f(c) = 0.4c - 70$; $f(100) = -30$, $f(300) = 50$; domain = whole numbers'),
    MN('tip11', 'Tip: four quick questions', 16,
       '1. **Function?** — no input with two outputs (vertical line test). 2. **Domain?** — all inputs allowed (watch denominators and square roots). 3. **Range?** — all outputs produced. 4. **f(a)?** — replace every $x$ by $(a)$.'),
    'math10-u1-tbl1',
    CK('ck1', 14, 'If $f(x) = 3 - 2x$, what is $f(-4)$?', ['$-5$', '$11$', '$-11$', '$5$'], 'B',
       'Replace $x$ by $(-4)$: $f(-4) = 3 - 2(-4) = 3 + 8 = 11$.'),
    CK('ck2', 12, 'Which equation does NOT give $y$ as a function of $x$?', ['$y = x^2 + 1$', '$y - 2x + 3 = 0$', '$y^2 = x + 1$', '$y = \\sqrt[3]{x}$'], 'C',
       'Solving $y^2 = x + 1$ gives $y = \\pm\\sqrt{x + 1}$: for $x = 3$, $y = 2$ or $y = -2$. One input, two outputs — not a function.'),
]

# ------------------------------------------------------------------ lesson 1.2
L12 = [
    T('=math10-u1-c06', '1.2.1 One-to-one functions', 17,
      'A function never sends one input to two outputs. A **one-to-one function** goes further: **no two different inputs share the same output**. Every output comes from exactly one input.',
      'Test with ordered pairs: look at the **second** elements. If an output repeats (with different inputs), the function is **not** one-to-one. $f = \\{(2, 1), (4, 5), (-2, -1), (6, 7), (8, 9), (3, 5)\\}$ is not one-to-one, because 4 and 3 both go to 5.',
      '**Horizontal line test:** if some horizontal line meets the graph of a function at more than one point, the function is **not** one-to-one. Points on one horizontal line have the same $y$ (output) but different $x$ (inputs).',
      'Test with a formula: find two different inputs with equal outputs to show it is NOT one-to-one (e.g. $f(x) = x^2$: $f(2) = f(-2) = 4$). To show it IS one-to-one, start from $f(a) = f(b)$ and show this forces $a = b$.'),
    DG('hlt', 'Sweep a horizontal line across the graph', 19, 'hlt',
       'Left: the line $y = 2.5$ meets $y = x^2$ twice (at $x = \\pm\\sqrt{2.5}$) — two inputs, one output — not one-to-one. Right: every horizontal line meets $y = \\frac12 x^3$ once — one-to-one.'),
    DG('tests', 'Two line tests, two different questions', 19, 'tests',
       'Vertical line test → "is this graph a function?" (one output for each input). Horizontal line test → "is this function one-to-one?" (one input for each output). Do the vertical test first; the horizontal test only makes sense for a function.'),
    WK('ex-11a', 'Worked example: showing a function is NOT one-to-one', 20,
       'Is $f(x) = \\frac{3}{x^2 + 1}$ one-to-one?',
       ['Look for two different inputs with the same output. Because of $x^2$, try $x = 1$ and $x = -1$.',
        '$f(1) = \\frac{3}{1 + 1} = \\frac32$ and $f(-1) = \\frac{3}{(-1)^2 + 1} = \\frac32$.',
        'Two different inputs, same output ⇒ not one-to-one.'],
       'No, $f(1) = f(-1) = \\frac32$.'),
    WK('ex-11b', 'Worked example: proving a function IS one-to-one', 20,
       'Show that $f(x) = 5x - \\frac12$ is one-to-one.',
       ['Suppose two inputs $a$ and $b$ give the same output: $f(a) = f(b)$.',
        'Then $5a - \\frac12 = 5b - \\frac12$.',
        'Add $\\frac12$: $5a = 5b$. Divide by 5: $a = b$.',
        'Equal outputs force equal inputs, so no two different inputs share an output.'],
       'Yes — every linear function $f(x) = mx + b$ with $m \\ne 0$ is one-to-one.'),
    TB('oneone-t', 'One-to-one or not? Common functions', 20, ['Function', 'One-to-one?', 'Reason'],
       [['$f(x) = mx + b$, $m \\ne 0$', 'yes', 'a slanted line passes the horizontal line test'],
        ['$f(x) = c$ (constant)', 'no', 'every input gives the same output'],
        ['$f(x) = x^2$', 'no', '$f(-2) = f(2) = 4$'],
        ['$f(x) = x^2$, $x \\ge 0$ only', 'yes', 'the left half is removed'],
        ['$f(x) = x^3$', 'yes', 'always increasing'],
        ['$f(x) = |x - 4|$', 'no', '$f(3) = f(5) = 1$'],
        ['$f(x) = \\sqrt{x}$', 'yes', 'always increasing'],
        ['$f(x) = \\frac{1}{2x - 4}$', 'yes', '$f(a) = f(b) \\Rightarrow 2a - 4 = 2b - 4 \\Rightarrow a = b$']]),
    T('=math10-u1-c09', '1.2.2 Inverse of a relation and of a function', 22,
      'The **inverse** of a relation $R$, written $R^{-1}$, is obtained by **swapping the two entries of every ordered pair**. If $R = \\{(1, 3), (2, 5), (3, 7)\\}$ then $R^{-1} = \\{(3, 1), (5, 2), (7, 3)\\}$.',
      'Because the entries swap, the **domain of $R^{-1}$ is the range of $R$**, and the **range of $R^{-1}$ is the domain of $R$**.',
      'The inverse of a function is **not always** a function. $g = \\{(3, 6), (8, 6)\\}$ gives $g^{-1} = \\{(6, 3), (6, 8)\\}$ — input 6 has two outputs. This happens exactly when $g$ is not one-to-one.',
      '**Key fact:** the inverse of a function $f$ is a function **if and only if $f$ is one-to-one**. Then we write it $f^{-1}$ (read "f inverse"). Careful: $f^{-1}(x)$ does **not** mean $\\frac{1}{f(x)}$.'),
    DG('invarrows', 'The inverse reverses every arrow', 22, 'invarrows',
       '$f = \\{(-1, 2), (-3, 1), (0, -2), (5, 6)\\}$ is one-to-one, so reversing the arrows still leaves one arrow from each input: $f^{-1} = \\{(2, -1), (1, -3), (-2, 0), (6, 5)\\}$ is a function.'),
    RM('=math10-u1-c05', 'Four steps to the formula of an inverse', 23,
       '**Step 1.** Replace $f(x)$ by $y$.',
       '**Step 2.** Interchange $x$ and $y$.',
       '**Step 3.** Solve the new equation for $y$.',
       '**Step 4.** Replace $y$ by $f^{-1}(x)$ — and state its domain (= the range of $f$).',
       'Check: $f(f^{-1}(x)) = x$ and $f^{-1}(f(x)) = x$. Quick number check: if $f(2) = 7$ then $f^{-1}(7)$ must be 2.'),
    WK('ex-inv1', 'Worked example: inverse of a linear function', 23,
       'Find $f^{-1}(x)$ for $f(x) = 3x - 6$.',
       ['Replace $f(x)$ by $y$: $y = 3x - 6$.',
        'Swap $x$ and $y$: $x = 3y - 6$.',
        'Solve for $y$: $x + 6 = 3y \\Rightarrow y = \\frac{x + 6}{3} = \\frac13 x + 2$.',
        'So $f^{-1}(x) = \\frac13 x + 2$. Check: $f(4) = 6$ and $f^{-1}(6) = 2 + 2 = 4$ (correct).'],
       '$f^{-1}(x) = \\frac13 x + 2$'),
    WK('ex-inv2', 'Worked example: inverse of a rational function', 23,
       'Find $g^{-1}(x)$ for $g(x) = \\frac{x - 2}{x + 3}$.',
       ['$y = \\frac{x - 2}{x + 3}$; swap: $x = \\frac{y - 2}{y + 3}$.',
        'Multiply both sides by $(y + 3)$: $xy + 3x = y - 2$.',
        'Collect the $y$ terms on one side: $xy - y = -3x - 2$.',
        'Factor out $y$: $y(x - 1) = -3x - 2$, so $y = \\frac{-3x - 2}{x - 1} = \\frac{3x + 2}{1 - x}$.',
        'Domain of $g^{-1}$: $x \\ne 1$ (that is exactly the value $g$ never reaches).'],
       '$g^{-1}(x) = \\frac{3x + 2}{1 - x}$, $x \\ne 1$'),
    WK('ex-inv3', 'Worked example: inverse with a cube and with a square root', 24,
       'Find the inverses of (a) $h(x) = x^3 + 3$ and (b) $k(x) = \\sqrt{x - 1}$.',
       ['(a) $x = y^3 + 3 \\Rightarrow y^3 = x - 3 \\Rightarrow y = \\sqrt[3]{x - 3}$. So $h^{-1}(x) = \\sqrt[3]{x - 3}$ for all real $x$.',
        '(b) $k$ has domain $x \\ge 1$ and range $y \\ge 0$. Swap: $x = \\sqrt{y - 1}$.',
        'Square both sides: $x^2 = y - 1 \\Rightarrow y = x^2 + 1$.',
        'The domain of $k^{-1}$ is the range of $k$, so $k^{-1}(x) = x^2 + 1$ **for $x \\ge 0$ only**.'],
       '(a) $\\sqrt[3]{x - 3}$  (b) $x^2 + 1$, $x \\ge 0$'),
    WK('ex-temp', 'Worked example: Celsius and Fahrenheit', 24,
       'Water freezes at 0 °C = 32 °F and boils at 100 °C = 212 °F, and Celsius $y$ is a linear function of Fahrenheit $x$. Find the formula, its inverse, and convert 50 °F and 20 °C.',
       ['Slope $= \\frac{100 - 0}{212 - 32} = \\frac{100}{180} = \\frac59$.',
        'Through $(32, 0)$: $y = \\frac59(x - 32)$, i.e. $C(x) = \\frac59(x - 32)$.',
        'Inverse: swap, $x = \\frac59(y - 32) \\Rightarrow y - 32 = \\frac95 x \\Rightarrow C^{-1}(x) = \\frac95 x + 32$.',
        '$C(50) = \\frac59(18) = 10$ °C; $C^{-1}(20) = 36 + 32 = 68$ °F.'],
       '$C(x) = \\frac59(x - 32)$, $C^{-1}(x) = \\frac95x + 32$; 50 °F = 10 °C, 20 °C = 68 °F'),
    'math10-u1-wk2',
    'math10-u1-c07',
    T('=math10-u1-xt2', '1.2.3 Graph of the inverse — a mirror in y = x', 25,
      'Swapping the coordinates of a point $(a, b)$ gives $(b, a)$. On squared paper with equal scales, $(b, a)$ is the **mirror image of $(a, b)$ in the line $y = x$** — fold the paper along $y = x$ and the two points land on each other.',
      'So the **graph of $f^{-1}$ is the reflection of the graph of $f$ in the line $y = x$.** To draw it: plot a few points of $f$, swap their coordinates, plot those, and join them.',
      'Points that lie on $y = x$ itself stay where they are, so $f$ and $f^{-1}$ meet on the line $y = x$ (if they meet at all).',
      'Always use the **same scale on both axes**, otherwise the mirror picture is distorted.'),
    DG('reflectpts', 'Swap the coordinates = reflect in y = x', 25, 'reflectpts',
       '$(3, 1) \\leftrightarrow (1, 3)$, $(-2, 0) \\leftrightarrow (0, -2)$, $(-1, 2) \\leftrightarrow (2, -1)$. The dashed segment joining each pair is cut at right angles and in half by the line $y = x$.'),
    GR('gr-lin', 'f(x) = 2x + 1 and its inverse', 26,
       plane(-4, 4, -4, 4, points=[{'x': 1, 'y': 3, 'label': '(1, 3)'}, {'x': 3, 'y': 1, 'label': '(3, 1)', 'color': '#2A7A6B'},
                                   {'x': -1, 'y': -1, 'label': '(−1, −1)', 'color': '#6A4C9C'}],
             lines=[{'m': 2, 'c': 1, 'label': 'f', 'color': '#2F5F8F'}, {'m': 0.5, 'c': -0.5, 'label': 'f⁻¹', 'color': '#2A7A6B'},
                    {'m': 1, 'c': 0, 'dash': True, 'label': 'y = x', 'color': '#8A7F76'}]),
       'From $y = 2x + 1$: swap and solve, $x = 2y + 1 \\Rightarrow f^{-1}(x) = \\frac{x - 1}{2}$. The point $(1, 3)$ on $f$ becomes $(3, 1)$ on $f^{-1}$. Both lines cross $y = x$ at $(-1, -1)$. Slopes 2 and $\\frac12$ are reciprocals — true for every linear function and its inverse.'),
    DG('sqrtinv', 'A curve and its inverse', 26, 'sqrtinv',
       '$f(x) = x^2$ is not one-to-one on all real numbers, but if we keep only $x \\ge 0$ it is. Its inverse is $f^{-1}(x) = \\sqrt{x}$; $(2, 4)$ on $f$ matches $(4, 2)$ on $f^{-1}$.'),
    TB('fvsinv', 'A function and its inverse side by side', 22, ['', 'f', 'f⁻¹'],
       [['Ordered pair', '$(a, b)$', '$(b, a)$'],
        ['Domain', 'domain of $f$', '= range of $f$'],
        ['Range', 'range of $f$', '= domain of $f$'],
        ['Graph', 'graph of $f$', 'mirror image in $y = x$'],
        ['Undo', '$f^{-1}(f(x)) = x$', '$f(f^{-1}(x)) = x$'],
        ['Exists as a function when', '—', '$f$ is one-to-one']]),
    'math10-u1-c08',
    CK('ck3', 23, 'If $f(x) = \\frac{x + 5}{2}$, then $f^{-1}(x) =$', ['$2x + 5$', '$2x - 5$', '$\\frac{2}{x + 5}$', '$\\frac{x - 5}{2}$'], 'B',
       'Swap: $x = \\frac{y + 5}{2} \\Rightarrow 2x = y + 5 \\Rightarrow y = 2x - 5$.'),
    CK('ck4', 22, 'The range of a one-to-one function $f$ is $\\{1, 4, 9\\}$. The domain of $f^{-1}$ is', ['$\\{1, 2, 3\\}$', '$\\{1, 4, 9\\}$', '$\\{-1, -4, -9\\}$', 'cannot be found'], 'B',
       'Swapping the pairs turns the range of $f$ into the domain of $f^{-1}$.'),
]

LESSONS = {'math10-u1-l1-1': L11, 'math10-u1-l1-2': L12}

# ------------------------------------------------------------------ practice
a = QSet('1.1 Practice — relations and functions', 's11')
a.S(3, 'Find the domain and range of $R = \\{(-1, 2), (2, 51), (1, 3), (8, 22), (9, 51)\\}$.', 'Domain $\\{-1, 1, 2, 8, 9\\}$; range $\\{2, 3, 22, 51\\}$',
    ['Step 1: domain = all first elements: $-1, 2, 1, 8, 9$.', 'Step 2: range = all second elements: $2, 51, 3, 22, 51$; list 51 only once.', 'Step 3: write each set in increasing order.'],
    'Domain = the first numbers, range = the second numbers. Never list a repeated number twice in a set.',
    [('Find the domain and range of $\\{(0, 5), (3, 5), (-2, 1)\\}$.', 'Domain $\\{-2, 0, 3\\}$, range $\\{1, 5\\}$.')])
a.M(7, 'Which relation is a function?', ['$\\{(3, 4), (4, 5), (6, 7), (3, 9)\\}$', '$\\{(8, 11), (34, 5), (6, 17), (8, 19)\\}$', '$\\{(-3, 4), (4, -5), (0, 0), (8, 9)\\}$', '$\\{(2, 2), (2, -2)\\}$'], 'C',
    ['Step 1: in each option look for a repeated FIRST element.', 'Step 2: A repeats 3, B repeats 8, D repeats 2 — each with different outputs.', 'Step 3: C has inputs $-3, 4, 0, 8$, all different → function.'],
    'Cover the second numbers with your finger and read only the first ones.',
    [('Is $\\{(1, 1), (2, 1), (3, 1)\\}$ a function?', 'Yes — no input repeats; the same output for every input is allowed.')])
a.S(7, 'Which of these rules are functions? (a) people → their birthday; (b) fathers → their children; (c) children → their blood mother.', '(a) and (c) are functions; (b) is not.',
    ['Step 1: ask "can one input have two outputs?"', 'Step 2: (a) a person has one birthday → function. (b) a father can have several children → not a function.', 'Step 3: (c) a child has exactly one blood mother → function.'],
    'Think of one input with many outputs. If that can happen, it is not a function.',
    [('Is "pencils assigned to their lengths" a function?', 'Yes — each pencil has one length (two pencils may share a length).')])
a.S(8, 'For $T = \\{(12, 14), (13, 5), (-2, 7), (x, 13)\\}$ to be a function, which values can $x$ not take?', '$x \\ne 12, 13, -2$',
    ['Step 1: the new pair $(x, 13)$ must not reuse an existing input with a different output.', 'Step 2: the existing inputs 12, 13 and $-2$ have outputs 14, 5, 7, none of them 13.', 'Step 3: so $x$ cannot be 12, 13 or $-2$.'],
    'If $x$ equals an old input whose output is ALREADY the same, it is allowed — check each one.',
    [('For $\\{(1, 4), (2, 9), (x, 9)\\}$ to be a function, which value(s) can $x$ not take?', '$x \\ne 1$ ($x = 2$ is allowed: $(2, 9)$ just repeats).')])
a.TF(10, 'A circle drawn on the coordinate plane is the graph of a function.', False,
     ['Step 1: apply the vertical line test.', 'Step 2: a vertical line through the inside of the circle meets it twice (top and bottom).', 'Step 3: so a circle is not a function.'],
     'Draw the dashed vertical line through the middle of the shape — two hits means "no".',
     [('Is the upper half of a circle (with its end points) a function?', 'Yes — every vertical line meets it at most once.')])
a.S(14, 'Let $g(x) = 4 - x^2$. Find $g(-3)$, $g(-\\frac12)$ and $g(0)$.', '$g(-3) = -5$, $g(-\\frac12) = \\frac{15}{4}$, $g(0) = 4$',
    ['Step 1: $g(-3) = 4 - (-3)^2 = 4 - 9 = -5$.', 'Step 2: $g(-\\frac12) = 4 - \\frac14 = \\frac{15}{4}$.', 'Step 3: $g(0) = 4 - 0 = 4$.'],
    'Always put the input in brackets before squaring: $(-3)^2 = 9$, but $-3^2 = -9$.',
    [('If $h(x) = x^3 + 1$, find $h(-1)$ and $h(2)$.', '$h(-1) = 0$, $h(2) = 9$.')])
a.M(15, 'The domain of $f(x) = \\sqrt{4 - 2x}$ is', ['$x \\ge 2$', '$x \\le 2$', '$x > 2$', 'all real numbers'], 'B',
    ['Step 1: inside the root must be $\\ge 0$: $4 - 2x \\ge 0$.', 'Step 2: $-2x \\ge -4$.', 'Step 3: divide by $-2$ and FLIP the sign: $x \\le 2$.'],
    'Dividing or multiplying an inequality by a negative number reverses it.',
    [('Find the domain of $f(x) = \\sqrt{x + 1}$.', '$x \\ge -1$.')])
a.M(15, 'The domain of $f(x) = \\frac{1}{x^2 - 9}$ is', ['$x \\ne 9$', '$x \\ne 3$', '$x \\ne \\pm 3$', 'all real numbers'], 'C',
    ['Step 1: the denominator cannot be 0: $x^2 - 9 \\ne 0$.', 'Step 2: $x^2 \\ne 9$ means $x \\ne 3$ and $x \\ne -3$.'],
    'A squared term equal to a positive number has TWO solutions — do not forget the negative one.',
    [('Find the domain of $\\frac{x}{x^2 + 1}$.', 'All real numbers ($x^2 + 1$ is never 0).')])
a.S(12, 'Does $y^2 = x + 1$ give $y$ as a function of $x$? Explain.', 'No.',
    ['Step 1: solve for $y$: $y = \\pm\\sqrt{x + 1}$.', 'Step 2: take $x = 3$: $y = 2$ or $y = -2$.', 'Step 3: one input with two outputs → not a function.'],
    'An even power of $y$ in the equation usually means "not a function" — find a concrete $x$ with two $y$-values to prove it.',
    [('Does $x^2 + y = 4$ give $y$ as a function of $x$?', 'Yes: $y = 4 - x^2$, one value for each $x$; $f(x) = 4 - x^2$.')])
a.S(17, 'The area of a circle is $A = \\pi r^2$. Write it as a function $g$ of $r$, find $g(2)$ and $g(5)$, and give the domain.', '$g(r) = \\pi r^2$; $g(2) = 4\\pi$ cm², $g(5) = 25\\pi$ cm²; domain $r > 0$.',
    ['Step 1: each radius gives one area → function $g(r) = \\pi r^2$.', 'Step 2: $g(2) = \\pi(2)^2 = 4\\pi \\approx 12.57$; $g(5) = 25\\pi \\approx 78.54$.', 'Step 3: a radius is a length, so it must be positive: domain $\\{r : r > 0\\}$.'],
    'In word problems the domain is limited by the situation (lengths positive, counts whole numbers), not only by the formula.',
    [('The perimeter of a square of side $s$ is $P(s) = 4s$. Find $P(2.5)$ and the domain.', '$P(2.5) = 10$; domain $s > 0$.')])
a.S(11, 'A graph is a straight line through $(-2, 0)$ and $(0, 4)$ that stops at the filled points $(-2, 0)$ and $(3, 10)$. Give its domain and range.', 'Domain $-2 \\le x \\le 3$; range $0 \\le y \\le 10$.',
    ['Step 1: the $x$-values run from the left end $x = -2$ to the right end $x = 3$.', 'Step 2: the $y$-values run from 0 (lowest point) to 10 (highest point).', 'Step 3: filled dots are included, so use $\\le$.'],
    'Open dot → strict inequality ($<$); filled dot → $\\le$.',
    [('A segment joins the filled point $(1, 1)$ to the open point $(4, -5)$. Domain and range?', 'Domain $1 \\le x < 4$; range $-5 < y \\le 1$.')])
a.F(12, 'In $f(x) = 2x + 7$, the variable $x$ is called the ____ variable.', 'independent', ['independent', 'dependent', 'constant', 'range'],
    ['Step 1: we choose $x$ freely (from the domain).', 'Step 2: $f(x)$ depends on that choice.', 'Step 3: so $x$ is independent and $y = f(x)$ is dependent.'],
    'Independent = input = $x$ = domain. Dependent = output = $y$ = range.',
    [('In $p = 0.4c - 70$, which is the dependent variable?', '$p$ (the profit depends on the number of cups $c$).')])

b = QSet('1.2 Practice — one-to-one and inverse functions', 's12')
b.M(20, 'Which function is one-to-one?', ['$\\{(3, -4), (8, 5), (6, 7), (22, 4)\\}$', '$\\{(9, 19), (34, 5), (6, 17), (8, 19)\\}$', '$\\{(11, 14), (12, 14), (16, 7)\\}$', '$\\{(1, 0), (2, 0)\\}$'], 'A',
    ['Step 1: for one-to-one look for a repeated SECOND element.', 'Step 2: B repeats 19, C repeats 14, D repeats 0.', 'Step 3: in A the outputs $-4, 5, 7, 4$ are all different → one-to-one.'],
    'Function test → look at first elements. One-to-one test → look at second elements.',
    [('Is $\\{(2, 27), (3, 28), (4, 29), (5, 30)\\}$ one-to-one?', 'Yes — all outputs are different.')])
b.TF(20, '$g(x) = x^2 + 2$ is a one-to-one function.', False,
     ['Step 1: try opposite inputs: $g(1) = 3$ and $g(-1) = 3$.', 'Step 2: two inputs share an output → not one-to-one.'],
     'Any function with only $x^2$ (no odd power of $x$) gives the same output for $x$ and $-x$.',
     [('Is $f(x) = x^3 - 1$ one-to-one?', 'Yes — $a^3 - 1 = b^3 - 1 \\Rightarrow a^3 = b^3 \\Rightarrow a = b$.')])
b.S(20, 'Show that $h(x) = \\frac{1}{2x - 4}$ is one-to-one.', 'If $h(a) = h(b)$ then $2a - 4 = 2b - 4$, so $a = b$.',
    ['Step 1: assume $\\frac{1}{2a - 4} = \\frac{1}{2b - 4}$.', 'Step 2: take reciprocals: $2a - 4 = 2b - 4$.', 'Step 3: add 4 and divide by 2: $a = b$. Equal outputs force equal inputs.'],
    'To PROVE one-to-one use $f(a) = f(b) \\Rightarrow a = b$. To DISPROVE, one counter-example is enough.',
    [('Show that $f(x) = 7 - 3x$ is one-to-one.', '$7 - 3a = 7 - 3b \\Rightarrow -3a = -3b \\Rightarrow a = b$.')])
b.S(24, 'Find the inverse of $R = \\{(2, -3), (4, 6), (3, -1), (6, 6), (2, 3)\\}$. Is $R^{-1}$ a function?', '$R^{-1} = \\{(-3, 2), (6, 4), (-1, 3), (6, 6), (3, 2)\\}$; not a function.',
    ['Step 1: swap every pair.', 'Step 2: in $R^{-1}$ the input 6 goes to 4 and to 6.', 'Step 3: so $R^{-1}$ is not a function (in $R$, the output 6 came from two inputs).'],
    'The inverse is a function exactly when the original has no repeated outputs.',
    [('Find the inverse of $\\{(-3, 0), (-1, 1), (0, 5), (2, 6)\\}$. Is it a function?', '$\\{(0, -3), (1, -1), (5, 0), (6, 2)\\}$ — yes, a function.')])
b.M(23, 'If $g(x) = 3x + 2$, then $g^{-1}(x)$ is', ['$3x - 2$', '$\\frac{x - 2}{3}$', '$\\frac{x + 2}{3}$', '$\\frac{1}{3x + 2}$'], 'B',
    ['Step 1: $y = 3x + 2$; swap: $x = 3y + 2$.', 'Step 2: $x - 2 = 3y$.', 'Step 3: $y = \\frac{x - 2}{3}$.'],
    'An inverse undoes the operations in reverse order: $g$ multiplies by 3 then adds 2, so $g^{-1}$ subtracts 2 then divides by 3.',
    [('Find $f^{-1}(x)$ for $f(x) = x - 1$.', '$f^{-1}(x) = x + 1$.')])
b.S(24, 'Find $h^{-1}(x)$ for $h(x) = \\frac{x + 1}{x - 1}$.', '$h^{-1}(x) = \\frac{x + 1}{x - 1}$ (the function is its own inverse), $x \\ne 1$.',
    ['Step 1: swap: $x = \\frac{y + 1}{y - 1}$.', 'Step 2: $xy - x = y + 1$.', 'Step 3: $xy - y = x + 1 \\Rightarrow y(x - 1) = x + 1$.', 'Step 4: $y = \\frac{x + 1}{x - 1}$ — the same formula as $h$.'],
    'With a fraction: multiply out, gather all $y$ terms on one side, then factor $y$ out.',
    [('Find $k^{-1}(x)$ for $k(x) = \\frac1x$.', '$k^{-1}(x) = \\frac1x$, $x \\ne 0$ — also its own inverse.')])
b.S(24, 'Does $f(x) = x^2 - 4$ (all real $x$) have an inverse function? What if we restrict to $x \\ge 0$?', 'Not on all real numbers; for $x \\ge 0$, $f^{-1}(x) = \\sqrt{x + 4}$, $x \\ge -4$.',
    ['Step 1: $f(2) = f(-2) = 0$, so $f$ is not one-to-one → no inverse function.', 'Step 2: for $x \\ge 0$ it is one-to-one with range $y \\ge -4$.', 'Step 3: swap: $x = y^2 - 4 \\Rightarrow y^2 = x + 4 \\Rightarrow y = \\sqrt{x + 4}$ (positive root, because the original $x \\ge 0$).'],
    'Restricting the domain to one side of the vertex makes a parabola one-to-one.',
    [('Find the inverse of $f(x) = x^2$, $x \\le 0$.', '$f^{-1}(x) = -\\sqrt{x}$, $x \\ge 0$.')])
b.M(25, 'The point $(5, -2)$ is on the graph of a one-to-one function $f$. Which point is on the graph of $f^{-1}$?', ['$(-5, 2)$', '$(5, 2)$', '$(-2, 5)$', '$(2, -5)$'], 'C',
    ['Step 1: the graph of $f^{-1}$ is the reflection in $y = x$.', 'Step 2: reflecting in $y = x$ swaps the coordinates.', 'Step 3: $(5, -2) \\to (-2, 5)$.'],
    'Swap — do not change any signs.',
    [('$(0, 3)$ is on $f$. Which point is on $f^{-1}$?', '$(3, 0)$.')])
b.S(24, 'Using $C(x) = \\frac59(x - 32)$, convert $-40$ °F to Celsius, and use the inverse to convert $-5$ °C to Fahrenheit.', '$-40$ °F $= -40$ °C; $-5$ °C $= 23$ °F.',
    ['Step 1: $C(-40) = \\frac59(-72) = -40$.', 'Step 2: $C^{-1}(x) = \\frac95x + 32$.', 'Step 3: $C^{-1}(-5) = -9 + 32 = 23$.'],
    '$-40$ is the one temperature that is the same on both scales — a nice check.',
    [('Convert 14 °F to Celsius.', '$C(14) = \\frac59(-18) = -10$ °C.')])
b.M(26, 'Where do the graphs of $f(x) = 2x + 1$ and $f^{-1}$ meet?', ['$(0, 1)$', '$(1, 0)$', '$(-1, -1)$', 'they never meet'], 'C',
    ['Step 1: $f$ and $f^{-1}$ meet on the mirror line $y = x$.', 'Step 2: solve $2x + 1 = x \\Rightarrow x = -1$.', 'Step 3: the point is $(-1, -1)$.'],
    'For an increasing function, intersections with its inverse lie on $y = x$ — solve $f(x) = x$.',
    [('Where does $f(x) = 3x - 4$ meet its inverse?', 'At $(2, 2)$.')])
b.F(22, 'The domain of $f^{-1}$ is equal to the ____ of $f$.', 'range', ['range', 'domain', 'inverse', 'graph'],
    ['Step 1: $f^{-1}$ swaps every pair $(a, b)$ to $(b, a)$.', 'Step 2: the second elements of $f$ become the first elements of $f^{-1}$.'],
    'Swap pairs ⇒ swap domain and range.',
    [('The range of $f^{-1}$ equals the ____ of $f$.', 'Domain.')])
b.S(25, 'Find the point that pairs with $(-2, 1)$ and with $(3, 0)$ when reflected in the line $y = x$.', '$(1, -2)$ and $(0, 3)$',
    ['Step 1: reflection in $y = x$ swaps the coordinates.', 'Step 2: $(-2, 1) \\to (1, -2)$; $(3, 0) \\to (0, 3)$.'],
    'Fold-the-paper check: both points must be the same distance from $y = x$.',
    [('Reflect $(4, 4)$ in $y = x$.', '$(4, 4)$ — points on the mirror stay put.')])

QS = a.items + b.items

GLOSSARY = [
    ('Relation', 'A set of ordered pairs.', 2),
    ('Domain', 'The set of all first elements (inputs, x-values) of a relation.', 2),
    ('Range', 'The set of all second elements (outputs, y-values) of a relation.', 2),
    ('Function', 'A relation in which every element of the domain is paired with exactly one element of the range.', 6),
    ('Vertical line test', 'A graph is a function if no vertical line crosses it more than once.', 10),
    ('Independent variable', 'The input variable (usually x) that we choose freely from the domain.', 12),
    ('Dependent variable', 'The output variable (usually y = f(x)) whose value depends on the input.', 12),
    ('One-to-one function', 'A function in which no two different inputs have the same output.', 18),
    ('Horizontal line test', 'A function is one-to-one if no horizontal line crosses its graph more than once.', 19),
    ('Inverse of a relation', 'The relation obtained by interchanging the entries of every ordered pair; written R⁻¹.', 22),
    ('Discrete graph', 'A graph made of separate points (the domain is a list of separate values).', 4),
    ('Continuous graph', 'An unbroken graph (the domain is an interval or all real numbers).', 4),
]
TIPS = [
    ('Domain: start with all real numbers, then remove what breaks the formula — zero denominators and negative numbers under an even root.', 14),
    ('Vertical line test → function? Horizontal line test → one-to-one? Only a one-to-one function has an inverse function.', 19),
    ('Inverse in 4 steps: y = …, swap x and y, solve for y, write f⁻¹(x). The graph is the mirror image in y = x.', 23),
]
IDEAS = [('vlt', 'Vertical line test', 'l1_1', 'math10-u1-md-vlt'), ('domrules', 'Domain rules', 'l1_1', 'math10-u1-md-domrules'),
         ('hlt', 'Horizontal line test', 'l1_2', 'math10-u1-md-hlt'), ('inv', 'Inverse in 4 steps', 'l1_2', 'math10-u1-c05')]
