r"""Grade 9 Unit 2 — Foundation of Functions (pp. 20-49)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet, plane, numberline
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side, arrow_diagram

UID = 'math9-u2'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_kelifa():
    a = arrow_diagram([(0, 0), (1, 2), (2, 4), (3, 6)], [0, 1, 2, 3], [0, 2, 4, 6], 'correct', 'score', title='function')
    b = arrow_diagram([(4, 2), (4, '−2'), (9, 3)], [4, 9], [2, '−2', 3], 'x', 'y', title='NOT a function', hl={4})
    return side_by_side([a, b], 0)


def f_disccont():
    figs = []
    for cont in (False, True):
        p = Plot(0, 5.4, 0, 27, unit=27, uy=5, grid=False, every=1, yevery=5, xlab='t', ylab='d')
        if cont:
            p.seg((0, 25), (5, 0), BLUE, 2.8)
        else:
            for t in range(6):
                p.dot(*p.P(t, 25 - 5 * t), RED, 4.2)
        figs.append(p)
    return side_by_side(figs, 14, ['discrete: whole hours only', 'continuous: every moment'])


def f_balance():
    f = Fig(320, 175)
    f.poly([(160, 150), (145, 170), (175, 170)], INK, 2, '#E8E2D8')
    f.line(160, 150, 160, 98, INK, 3)
    f.line(40, 98, 280, 98, INK, 3)
    f.line(30, 98, 120, 98, INK, 4).line(200, 98, 290, 98, INK, 4)

    def box(x, y, s=None):
        if s:
            f.g(s)
        f.rect(x, y, 26, 26, BLUE, 2, FILL[BLUE], 3).text(x + 13, y + 18, 'x', 14, BLUE, italic=True)
        if s:
            f.end()

    def ball(x, y, s=None, hl=None):
        f.g(s, hl)
        f.circle(x, y, 9, ORANGE, 2, FILL[ORANGE])
        f.end()

    box(36, 70)
    box(66, 70, 'k1 k2 k3')
    for i, x in enumerate((104, 104, 104)):
        pass
    ball(105, 86, 'k1 k2', 'k2')
    ball(105, 66, 'k1 k2', 'k2')
    ball(105, 46, 'k1 k2', 'k2')
    xs = [212, 232, 252, 272, 212, 232, 252, 272, 222]
    ys = [86, 86, 86, 86, 66, 66, 66, 66, 46]
    for k, (x, y) in enumerate(zip(xs, ys)):
        if k >= 6:
            ball(x, y, 'k1 k2', 'k2')
        elif k >= 3:
            ball(x, y, 'k1 k2 k3')
        else:
            ball(x, y)
    f.g('k1').text(160, 24, '2 boxes + 3 balls = 9 balls', 13, INK).end()
    f.g('k2').text(160, 24, 'take 3 balls off EACH side', 13, RED).end()
    f.g('k3').text(160, 24, '2 boxes = 6 balls; halve both sides', 13, INK).end()
    f.g('k4').text(160, 24, '1 box = 3 balls, so x = 3', 13, GREEN).end()
    return f


def f_variation():
    a = Plot(0, 5.4, 0, 11, unit=26, uy=14, grid=False, every=1, yevery=2)
    a.fn(lambda x: 2 * x, 0, 5.2, BLUE)
    for x in (1, 2, 4):
        a.dot(*a.P(x, 2 * x), RED, 3.6)
    a.text(a.X(1.2), a.Y(9.5), 'y = 2x', 13, BLUE, 'start')
    b = Plot(0, 6.4, 0, 13, unit=22, uy=12, grid=False, every=1, yevery=2)
    b.fn(lambda x: 12 / x, 0.95, 6.3, GREEN)
    for x in (1, 2, 3, 4, 6):
        b.dot(*b.P(x, 12 / x), RED, 3.6)
    b.text(b.X(2.4), b.Y(10.5), 'y = 12 ÷ x', 13, GREEN, 'start')
    return side_by_side([a, b], 10, ['direct: y ÷ x = 2', 'inverse: x × y = 12'])


def f_absdist():
    f = Fig(330, 110)
    y = 70
    X = lambda v: 165 + v * 36
    f.arrow(X(-4.4), y, X(4.4), y, INK, 1.8, 8, both=True)
    for v in range(-4, 5):
        f.line(X(v), y - 5, X(v), y + 5, INK, 1.6).text(X(v), y + 21, str(v).replace('-', '−'), 12, INK)
    f.dot(X(0), y, INK, 3.5)
    f.dot(X(3), y, BLUE, 5).dot(X(-3), y, RED, 5)
    f.curve_arrow(X(0), y - 8, X(3), y - 8, -26, BLUE, 2, 7)
    f.curve_arrow(X(0), y - 8, X(-3), y - 8, 26, RED, 2, 7)
    f.text(X(1.5), y - 36, '3 units', 12.5, BLUE).text(X(-1.5), y - 36, '3 units', 12.5, RED)
    f.text(X(3), 18, '|3| = 3', 13, BLUE).text(X(-3), 18, '|−3| = 3', 13, RED)
    return f


def f_absrule():
    f = Fig(330, 150)
    X = lambda v: 165 + v * 30
    for row, (y, inside) in enumerate(((48, True), (122, False))):
        f.line(X(-5), y, X(5), y, INK, 1.6)
        for v in range(-5, 6):
            f.line(X(v), y - 4, X(v), y + 4, INK, 1.2)
        for v in (-3, 0, 3):
            f.text(X(v), y + 19, str(v).replace('-', '−'), 12, INK)
        if inside:
            f.line(X(-3), y, X(3), y, BLUE, 5)
            f.dot(X(-3), y, BLUE, 5, True).dot(X(3), y, BLUE, 5, True)
            f.text(165, y - 14, '|x| < 3:  −3 < x < 3   (AND, one piece)', 12.5, BLUE)
        else:
            f.line(X(-5.2), y, X(-3), y, RED, 5).line(X(3), y, X(5.2), y, RED, 5)
            f.arrow(X(-4.6), y, X(-5.4), y, RED, 3, 8).arrow(X(4.6), y, X(5.4), y, RED, 3, 8)
            f.dot(X(-3), y, RED, 5).dot(X(3), y, RED, 5)
            f.text(165, y - 14, '|x| ≥ 3:  x ≤ −3 or x ≥ 3   (OR, two pieces)', 12.5, RED)
    return f


DIAGRAMS = {
    'kelifa': (f_kelifa(), 'Function or not? Each input must have one output', 22),
    'disccont': (f_disccont(), 'Discrete and continuous graphs (Fig. 2.3 and 2.4)', 24),
    'balance': (f_balance(), 'An equation is a balance (Fig. 2.5)', 31),
    'variation': (f_variation(), 'Direct and inverse variation graphs (Fig. 2.6 and 2.7)', 41),
    'absdist': (f_absdist(), 'Absolute value is distance from 0 (Fig. 2.8)', 43),
    'absrule': (f_absrule(), 'Less than → between; greater than → outside', 47),
}

GBLUE, GRED, GGREEN = '#2F5F8F', '#C0503A', '#2A7A6B'

# ------------------------------------------------------------------ lesson 2.1
L1 = [
    T('=math9-u2-c01', '2.1.1 Dependent and independent quantities', 20,
      'Abrehet sells eggs in Keren at 3 Nakfa each. Her **income depends on** the number of eggs she sells: 10 eggs → 30 Nakfa, 18 eggs → 54 Nakfa.',
      '- The quantity we choose or control (number of eggs) is the **independent quantity**.',
      '- The quantity that changes **because of** it (income) is the **dependent quantity**.',
      'Test: say "**___ depends on ___**". The first blank is dependent, the second is independent. "Income depends on eggs sold" — not "eggs depend on income".',
      'In a **function**, each value of the independent quantity gives **exactly one** value of the dependent quantity.'),
    T('dom-t', 'Domain and range', 21,
      'The **domain** is the set of all possible values of the independent quantity; the **range** is the set of all values the dependent quantity can take.',
      'Kelifa\'s exam has 30 questions, 2 marks each. He can get 0, 1, 2, …, 30 questions right, so',
      '$$\\text{Domain} = \\{0, 1, 2, \\dots, 30\\}, \\quad \\text{Range} = \\{0, 2, 4, \\dots, 60\\}$$',
      'Always think about what is **possible** in the real situation: you cannot answer $2.5$ questions or $-1$ questions.'),
    DG('kelifa', 'A function pairs each input with one output', 22, 'kelifa',
       'Left: each number of correct answers goes to exactly one score, score $= 2 \\times$ (correct answers) — a function. Right: the input 4 has two outputs, 2 and $-2$ — not a function.'),
    T('=math9-u2-c02', '2.1.2 Tables and graphs', 22,
      'A function can be shown as a **table of values**, which is a list of **ordered pairs** (input, output). Plot them with the **independent quantity on the horizontal ($x$) axis** and the dependent quantity on the vertical ($y$) axis.',
      'The first number of a pair is always the input: $(1, 2)$ means "1 correct answer gives 2 marks"; $(2, 1)$ would mean something different.'),
    GR('gr-disc', 'Fig. 2.2: score against correct answers (discrete)', 23,
       plane(-1, 11, -2, 22, points=[{'x': x, 'y': 2 * x, 'color': GRED} for x in range(0, 11)]),
       'The points are **separate dots** — you cannot get 2.5 answers right, so nothing lies between them. This is a **discrete graph**.'),
    TB('graph-t', 'Discrete or continuous?', 25, ['', 'Discrete graph', 'Continuous graph'],
       [['Inputs', 'only separate values (counts: people, eggs, pages)', 'every real number in an interval (time, length, mass)'],
        ['Picture', 'isolated dots — do **not** join them', 'an unbroken line or curve'],
        ['Example', 'score vs correct answers; entrance money vs people', 'distance vs time; area vs side length'],
        ['Question to ask', '"Can the input be a fraction?" → No', '"Can the input be a fraction?" → Yes']],
       'Rule of thumb: if you **count** the input it is discrete; if you **measure** it, it is continuous.'),
    DG('disccont', 'Same table, two graphs (Example 2.2)', 24, 'disccont',
       'Walking 25 km at 5 km/h: remaining distance $d = 25 - 5t$. Plotting only whole hours gives dots; allowing every moment $t$ (0.1 h, 3.5 h, …) fills the gaps with a straight segment.'),
    T('=math9-u2-c03', '2.1.3 Describing a function with an equation', 28,
      'An equation states the rule in one line. Let $x$ = independent variable and $y$ = dependent variable.',
      '- Kelifa: $y = 2x$. Abrehet: $y = 3x$.',
      '- Water tank with 10 litres leaking 0.2 litre per hour: $y = 10 - 0.2x$ (empty when $x = 50$ hours).',
      '- From a table, look at how $y$ changes when $x$ goes up by 1. If it always changes by the same amount $m$, the rule is $y = mx + c$, where $c$ is the value of $y$ when $x = 0$.'),
    WK('ex-21a', 'Worked example: find the rule from a table (Activity 2.5)', 28,
       'Find an equation for $x$: 1, 2, 3, 4, 5, 6 and $y$: 0.6, 0.9, 1.2, 1.5, 1.8, 2.1. Then find $y$ when $x = 10$.',
       ['Each time $x$ goes up by 1, $y$ goes up by 0.3, so $y = 0.3x + c$.', 'Use $(1, 0.6)$: $0.6 = 0.3 + c$, so $c = 0.3$.', 'Rule: $y = 0.3x + 0.3$. Check $(4, 1.5)$: $1.2 + 0.3 = 1.5$ (correct).', '$x = 10$: $y = 3 + 0.3 = 3.3$.'],
       '$y = 0.3x + 0.3$; $y = 3.3$'),
    WK('ex-21b', 'Worked example: the water tank', 28,
       'A tank holds 10 L and leaks 0.2 L per hour. Write the rule, find the water after 15 hours and after 2 days, and give the domain and range.',
       ['Water left $y = 10 - 0.2x$ ($x$ in hours).', 'After 15 h: $10 - 3 = 7$ L.', 'After 2 days $= 48$ h: $10 - 9.6 = 0.4$ L.', 'Empty when $10 - 0.2x = 0$, so $x = 50$. Domain $0 \\le x \\le 50$, range $0 \\le y \\le 10$.'],
       '7 L, 0.4 L; domain $[0, 50]$, range $[0, 10]$',
       graph=plane(-5, 55, -1, 11, lines=[{'p1': [0, 10], 'p2': [50, 0], 'seg': True, 'color': GBLUE}],
                   points=[{'x': 15, 'y': 7, 'label': '(15, 7)', 'color': GRED}, {'x': 48, 'y': 0.4, 'label': '(48, 0.4)', 'color': GRED}])),
]

# ------------------------------------------------------------------ lesson 2.2
L2 = [
    T('=math9-u2-c05', '2.2.1 Solving equations: keep the balance', 30,
      'Two equations with the same solution set are **equivalent**: $2x + 3 = 13$ and $2x = 10$ both have solution set $\\{5\\}$. Solving means changing the equation, step by step, into simpler equivalent equations until it reads $x = $ number.',
      'Think of a balance scale: whatever you do to one pan you must do to the other.'),
    ST('balance', 'Solving 2x + 3 = 9 on a balance', 31, 'balance',
       [('Each box weighs $x$ balls. The scale shows $2x + 3 = 9$.', 'k1'),
        ('Remove 3 balls from **both** pans (subtract 3): the scale stays level.', 'k2'),
        ('Now $2x = 6$. Split both pans into two equal halves (divide by 2).', 'k3'),
        ('$x = 3$. Check: $2(3) + 3 = 9$ (correct).', 'k4')]),
    RM('=math9-u2-c04', 'Moves that keep an equation equivalent', 32,
       '1. Add the same number to both sides. 2. Subtract the same number from both sides.',
       '3. Multiply both sides by the same **non-zero** number. 4. Divide both sides by the same **non-zero** number.',
       '5. Replace an expression by an equal one (e.g. expand brackets). 6. Swap the two sides.'),
    WK('ex-22a', 'Worked example: Example 2.4 and Activity 2.8', 32,
       'Solve (a) $x + 5 = -6$ (b) $15 = 3y - 9$.',
       ['(a) Subtract 5 from both sides: $x = -6 - 5 = -11$.', '(b) Add 9 to both sides: $24 = 3y$.', 'Divide both sides by 3: $8 = y$, so $y = 8$.', 'Check (b): $3(8) - 9 = 15$ (correct).'],
       '(a) $\\{-11\\}$ (b) $\\{8\\}$'),
    T('both-t', '2.2.2 Variables on both sides', 33,
      'Recipe: (1) expand brackets; (2) move all $x$-terms to one side and numbers to the other by adding/subtracting; (3) divide by the coefficient of $x$; (4) check in the **original** equation.',
      'Tip: move the $x$-terms to the side with the **bigger** coefficient to avoid negative coefficients.'),
    WK('ex-22b', 'Worked example: Example 2.5 and Activity 2.9', 33,
       'Solve (a) $x + 23 = 2x + 45$ (b) $2x + 6 = 4x - 2$.',
       ['(a) Subtract $x$: $23 = x + 45$. Subtract 45: $x = -22$.', '(b) Subtract $2x$: $6 = 2x - 2$. Add 2: $8 = 2x$, so $x = 4$.', 'Check (b): $2(4) + 6 = 14$ and $4(4) - 2 = 14$ (correct).'],
       '(a) $x = -22$ (b) $x = 4$'),
    WK('ex-22c', 'Worked example: brackets on both sides', 34,
       'Solve $4(x + 3) = 5 - 3(x - 1)$.',
       ['Expand: $4x + 12 = 5 - 3x + 3$ (careful: $-3 \\times -1 = +3$).', 'Simplify: $4x + 12 = 8 - 3x$.', 'Add $3x$: $7x + 12 = 8$. Subtract 12: $7x = -4$.', '$x = -\\frac{4}{7}$.'],
       '$x = -\\frac{4}{7}$'),
    T('=math9-u2-c06', '2.2.3 Fractions and decimals: clear them first', 34,
      '- **Fractions:** multiply **every term** on both sides by the LCM of the denominators.',
      '- **Decimals:** multiply every term by 10, 100, … to make all coefficients whole numbers.',
      'Example 2.6: $0.2x + 2 = 2.6$. Multiply by 10: $2x + 20 = 26$, so $2x = 6$ and $x = 3$.'),
    WK('ex-22d', 'Worked example: Activity 2.10', 34,
       'Solve $\\frac{x - 2}{4} - \\frac{x + 5}{6} = -2$.',
       ['LCM of 4 and 6 is 12. Multiply every term by 12: $3(x - 2) - 2(x + 5) = -24$.', 'Expand: $3x - 6 - 2x - 10 = -24$.', 'Simplify: $x - 16 = -24$, so $x = -8$.',
        'Check: $\\frac{-10}{4} - \\frac{-3}{6} = -2.5 + 0.5 = -2$ (correct).'],
       '$x = -8$'),
    WK('ex-22e', 'Worked example: the field trip (Exercise 2.6)', 35,
       'Two-thirds of a class arrived on time. Three more came late, making 25. How many learners are in the class?',
       ['Let $n$ = number in the class. On time: $\\frac{2}{3}n$.', '$\\frac{2}{3}n + 3 = 25$, so $\\frac{2}{3}n = 22$.', '$n = 22 \\times \\frac{3}{2} = 33$.'],
       '33 learners'),
    T('=math9-u2-c07', '2.2.4 Linear inequalities: one extra rule', 36,
      'Solve an inequality exactly like an equation, with **one** extra rule:',
      '**When you multiply or divide both sides by a negative number, reverse the inequality sign** ($<$ becomes $>$, $\\le$ becomes $\\ge$). Swapping the two sides also reverses it ($5 > x$ means $x < 5$).',
      'Why? $2 < 3$ is true, but multiplying by $-1$ gives $-2$ and $-3$, and $-2 > -3$.',
      'An inequality usually has **infinitely many** solutions, so we write a set $\\{x : x \\ge 1\\}$ and draw it on a number line: closed dot for $\\le, \\ge$; open dot for $<, >$.'),
    TB('eqineq-t', 'Equations and inequalities compared', 36, ['Step', 'Equation', 'Inequality'],
       [['Add / subtract a number', 'allowed', 'allowed, sign unchanged'],
        ['Multiply / divide by a positive', 'allowed', 'allowed, sign unchanged'],
        ['Multiply / divide by a negative', 'allowed', 'allowed, **reverse the sign**'],
        ['Swap sides', 'allowed', 'allowed, **reverse the sign**'],
        ['Answer', 'usually one number', 'a whole interval of numbers']],
       'Most lost marks come from forgetting to reverse the sign after dividing by a negative.'),
    WK('ex-22f', 'Worked example: Example 2.8', 37,
       'Solve $3x - 2 \\le 5x - 4$ and show the solution on a number line.',
       ['Subtract $5x$: $-2x - 2 \\le -4$.', 'Add 2: $-2x \\le -2$.', 'Divide by $-2$ and **reverse**: $x \\ge 1$.', 'Check $x = 2$: $4 \\le 6$ (true). Check $x = 0$: $-2 \\le -4$ (false, as expected).'],
       '$\\{x : x \\ge 1\\}$', graph=numberline(-3, 5, points=[{'x': 1}], ranges=[{'from': 1}])),
    WK('ex-22g', 'Worked example: the national examination (Activity 2.12)', 35,
       '50 questions, 2 marks each, pass mark at least 50. How many questions must be answered correctly to pass?',
       ['Let $q$ = questions correct. Marks $= 2q$.', '"At least 50": $2q \\ge 50$, so $q \\ge 25$.', 'Also $q \\le 50$ and $q$ is a whole number.'],
       '25 or more correct answers'),
]

# ------------------------------------------------------------------ lesson 2.3
L3 = [
    T('=math9-u2-c08', '2.3.1 Direct variation', 38,
      '$y$ **varies directly** with $x$ if $y = kx$ for a constant $k \\ne 0$, i.e. the **ratio** $\\frac{y}{x} = k$ never changes. $k$ is the **constant of proportionality**.',
      'Signs: when $x$ doubles, $y$ doubles; when $x$ is halved, $y$ is halved. The graph is a straight line **through the origin**.',
      'Examples: distance and time at a fixed speed ($d = 5t$); income and eggs sold ($I = 3n$); profit and inventory.'),
    T('=math9-u2-c09', '2.3.2 Inverse variation', 40,
      '$y$ **varies inversely** as $x$ if $xy = k$, i.e. $y = \\frac{k}{x}$ with $k \\ne 0$. The **product** never changes.',
      'Signs: when $x$ doubles, $y$ is halved. The graph is a curve that falls and never touches the axes.',
      'Example: Nejat rides 10 km to school. Speed $\\times$ time $= 10$: at 10 km/h she needs 1 h, at 20 km/h only 0.5 h.'),
    DG('variation', 'Direct vs inverse variation', 41, 'variation',
       'Left: $(1, 2), (2, 4), (4, 8)$ — divide $y$ by $x$, always 2. Right: $(1, 12), (2, 6), (3, 4), (4, 3), (6, 2)$ — multiply, always 12.'),
    TB('var-t', 'Direct and inverse variation compared', 42, ['', 'Direct', 'Inverse'],
       [['Equation', '$y = kx$', '$y = \\frac{k}{x}$ ($xy = k$)'],
        ['Constant', 'ratio $\\frac{y}{x} = k$', 'product $xy = k$'],
        ['$x$ doubles →', '$y$ doubles', '$y$ halves'],
        ['Graph', 'straight line through $(0, 0)$', 'curve, never meets the axes'],
        ['Find $k$', '$k = \\frac{y}{x}$', '$k = xy$']],
       'Method for every variation problem: (1) write the type of equation, (2) use the given pair to find $k$, (3) use $k$ with the new value.'),
    'math9-u2-mn3',
    WK('ex-23a', 'Worked example: Example 2.9 (direct)', 39,
       '$y$ varies directly with $x$, and $y = 2$ when $x = 5$. Find $y$ when $x = 15$.',
       ['$y = kx$: $2 = 5k$, so $k = \\frac{2}{5}$.', '$y = \\frac{2}{5} \\times 15 = 6$.', 'Shortcut check: $x$ was multiplied by 3, so $y$ is too: $2 \\times 3 = 6$ (correct).'],
       '$y = 6$'),
    WK('ex-23b', 'Worked example: Example 2.10 (inverse)', 42,
       '$z$ varies inversely as $p$, and $z = 200$ when $p = 4$. Find $z$ when $p = 10$.',
       ['$zp = k$: $k = 200 \\times 4 = 800$.', '$z = \\frac{800}{10} = 80$.'],
       '$z = 80$'),
    WK('ex-23c', 'Worked example: calories (Activity 2.15)', 39,
       'Calories burned vary directly with time. A person burns 75 calories sitting in class for 50 minutes. How long to burn 545 calories?',
       ['$C = kt$: $75 = 50k$, so $k = 1.5$ calories per minute.', '$545 = 1.5t$, so $t = 545 \\div 1.5 \\approx 363.3$ minutes.', 'That is about 6 hours 3 minutes.'],
       'about 363 minutes (≈ 6 h)'),
]

# ------------------------------------------------------------------ lesson 2.4
L4 = [
    T('=math9-u2-c10', '2.4.1 Absolute value = distance from 0', 43,
      'The **absolute value** $|x|$ is the distance of $x$ from 0 on the number line. A distance is never negative, so $|x| \\ge 0$ always.',
      '$$|x| = \\begin{cases} x & \\text{if } x \\ge 0 \\\\ -x & \\text{if } x < 0 \\end{cases}$$',
      'So $|6| = 6$ and $|-5| = -(-5) = 5$. The "$-x$" does **not** mean the answer is negative: when $x$ is negative, $-x$ is positive.',
      'Useful facts: $|x - y| = |y - x|$ (the distance between $x$ and $y$), $|xy| = |x||y|$, but $|x + y| \\le |x| + |y|$ (equal only when $x, y$ have the same sign or one is 0).'),
    DG('absdist', 'Two numbers with the same absolute value', 43, 'absdist', '3 and $-3$ are both 3 units from 0, on opposite sides. So $|x| = 3$ has two solutions.'),
    T('=math9-u2-c11', '2.4.2 Absolute value equations', 46,
      'For $k > 0$: $$|u| = k \\iff u = -k \\text{ or } u = k$$',
      'Solve both equations and put the answers together. Special cases: $|u| = 0$ gives only $u = 0$; $|u| = $ a negative number has **no solution** (distance cannot be negative).',
      'Before splitting, get the absolute value **alone** on one side: $|x + 1| + 2 = 7$ → $|x + 1| = 5$ first.'),
    WK('ex-24a', 'Worked example: Example 2.13', 46,
       'Solve $|2x - 5| = 9$.',
       ['Split: $2x - 5 = -9$ or $2x - 5 = 9$.', 'First: $2x = -4$, $x = -2$. Second: $2x = 14$, $x = 7$.', 'Check: $|2(-2) - 5| = |-9| = 9$ and $|2(7) - 5| = |9| = 9$ (correct).'],
       '$\\{-2, 7\\}$'),
    T('=math9-u2-c12', '2.4.3 Absolute value inequalities', 47,
      'For $k > 0$:',
      '- $|u| < k \\iff -k < u < k$ (distance **less** than $k$ → **between**, one piece, "and").',
      '- $|u| > k \\iff u < -k \\text{ or } u > k$ (distance **more** than $k$ → **outside**, two pieces, "or").',
      'The same holds with $\\le$ and $\\ge$ (then the end points are included). "And" gives the **intersection** of the two solution sets; "or" gives the **union**.'),
    DG('absrule', 'Less than: between. Greater than: outside.', 47, 'absrule'),
    WK('ex-24b', 'Worked example: Example 2.14', 48,
       'Solve $|2x - 3| < 5$.',
       ['Less than → between: $-5 < 2x - 3 < 5$.', 'Add 3 to all three parts: $-2 < 2x < 8$.', 'Divide all parts by 2: $-1 < x < 4$.'],
       '$\\{x : -1 < x < 4\\}$', graph=numberline(-3, 6, points=[{'x': -1, 'open': True}, {'x': 4, 'open': True}], ranges=[{'from': -1, 'to': 4, 'from_open': True, 'to_open': True}])),
    WK('ex-24c', 'Worked example: Example 2.15', 48,
       'Solve $|x + 2| \\ge 4$.',
       ['Greater than → outside: $x + 2 \\le -4$ or $x + 2 \\ge 4$.', 'Subtract 2: $x \\le -6$ or $x \\ge 2$.', 'Check $x = 0$ (between): $|2| = 2 \\ge 4$ is false, so the middle is correctly left out.'],
       '$\\{x : x \\le -6 \\text{ or } x \\ge 2\\}$', graph=numberline(-9, 5, points=[{'x': -6}, {'x': 2}], ranges=[{'to': -6}, {'from': 2}])),
    TB('abs-t', 'Absolute value: all cases ($k > 0$)', 48, ['Problem', 'Rewrite as', 'Picture'],
       [['$|u| = k$', '$u = -k$ or $u = k$', 'two points'],
        ['$|u| < k$', '$-k < u < k$', 'segment between, open ends'],
        ['$|u| \\le k$', '$-k \\le u \\le k$', 'segment between, closed ends'],
        ['$|u| > k$', '$u < -k$ or $u > k$', 'two rays outward, open ends'],
        ['$|u| \\ge k$', '$u \\le -k$ or $u \\ge k$', 'two rays outward, closed ends'],
        ['$|u| = $ negative, or $|u| < $ negative', 'no solution', 'nothing'],
        ['$|u| > $ negative', 'every real number', 'whole line']],
       'Memory hook: "less th**AND**" — less than gives AND (between); "great**OR**" — greater than gives OR (outside).'),
]

LESSONS = {'math9-u2-l2-1': L1, 'math9-u2-l2-2': L2, 'math9-u2-l2-3': L3, 'math9-u2-l2-4': L4}

# ------------------------------------------------------------------ practice
a = QSet('2.1 Practice — describing functions', 's21')
a.S(21, 'For "the wage a person earns and the number of hours worked", name the dependent and independent quantities.', 'dependent: wage; independent: hours',
    ['Step 1: say "wage depends on hours worked" — this makes sense.', 'Step 2: the first is dependent (wage), the second independent (hours).'],
    'Use the sentence "___ depends on ___".', [('Area of a square and its side length?', 'Area depends on the side: area dependent, side independent.')])
a.S(22, 'A company buys 5 tyres for each car (including a spare). Write the rule and give the domain and range if it owns up to 4 cars.', '$t = 5c$; domain $\\{0, 1, 2, 3, 4\\}$, range $\\{0, 5, 10, 15, 20\\}$',
    ['Step 1: tyres $t = 5 \\times$ cars $c$.', 'Step 2: cars can be 0, 1, 2, 3, 4.', 'Step 3: multiply each by 5 for the range.'],
    'The range comes from putting every domain value through the rule.', [('Ali is 3 years older than Keria. Rule for Ali\'s age $A$ given Keria\'s age $k$?', '$A = k + 3$.')])
a.M(25, 'Which relationship has a continuous graph?', ['entrance money and number of people', 'tyres needed and number of cars', 'area of a square and its side length', 'score and number of correct answers'], 'C',
    ['Step 1: people, cars and answers are counted → discrete.', 'Step 2: a side length can be any positive real number (2.37 cm) → continuous.'],
    'Counted → dots; measured → line.', [('Distance walked and time walked?', 'Continuous.')])
a.S(25, 'The drama club charges 0.50 Nakfa entrance. Find the income for 23, 60 and 121 people. Is the graph discrete or continuous?', '11.50, 30, 60.50 Nakfa; discrete',
    ['Step 1: income $= 0.5 \\times$ people.', 'Step 2: $0.5 \\times 23 = 11.5$; $0.5 \\times 60 = 30$; $0.5 \\times 121 = 60.5$.', 'Step 3: people are counted (no half people) → discrete.'],
    'Multiply by 0.5 = halve.', [('Maximum income if the hall has 125 seats?', '62.50 Nakfa.')])
a.S(29, 'The ordered pairs $(-2, 5), (0, 1), (4, -7), (7, -13)$ belong to a function. Find its equation.', '$y = -2x + 1$',
    ['Step 1: $(0, 1)$ gives $c = 1$.', 'Step 2: from $x = 0$ to $x = 4$, $y$ falls by 8, so it falls 2 per step: $m = -2$.', 'Step 3: $y = -2x + 1$. Check $(7, -13)$: $-14 + 1 = -13$ (correct).'],
    'The pair with $x = 0$ gives the constant straight away.', [('Find the rule for $(0, 2), (1, 3), (2, 4), (3, 5)$.', '$y = x + 2$.')])
a.S(29, 'A photocopy costs 1.50 Nakfa per page. Write the rule and find the cost of 13, 21 and 32 pages.', '$y = 1.5x$; 19.50, 31.50, 48 Nakfa',
    ['Step 1: $y = 1.5x$.', 'Step 2: $1.5 \\times 13 = 19.5$, $1.5 \\times 21 = 31.5$, $1.5 \\times 32 = 48$.'],
    '$1.5x = x + \\frac{x}{2}$ — easy mental maths.', [('How many pages for 60 Nakfa?', '40 pages.')])
a.TF(21, 'For a function, one input may give two different outputs.', False,
     ['Step 1: a function gives each input **exactly one** output.', 'Step 2: two outputs for one input is not a function.'],
     'Two different inputs may share an output; one input may not have two outputs.', [('Can two inputs share the same output in a function?', 'Yes, e.g. $y = x^2$: $(-2, 4)$ and $(2, 4)$.')])

b = QSet('2.2 Practice — equations and inequalities', 's22')
b.S(33, 'Solve $11 = 1 - 4z$.', '$z = -2.5$',
    ['Step 1: subtract 1: $10 = -4z$.', 'Step 2: divide by $-4$: $z = -2.5$.', 'Step 3: check: $1 - 4(-2.5) = 1 + 10 = 11$ (correct).'],
    'Dividing by a negative in an **equation** needs no sign flip.', [('Solve $14 = 12y + 8$.', '$y = \\frac{1}{2}$.')])
b.S(33, 'Each equal side of an isosceles triangle is 3 times the third side. The perimeter is 56 cm. Find the sides.', '8 cm, 24 cm, 24 cm',
    ['Step 1: third side $x$, equal sides $3x$ each.', 'Step 2: $x + 3x + 3x = 56$, so $7x = 56$, $x = 8$.', 'Step 3: sides 8, 24, 24.'],
    'Name the smallest quantity $x$ and write the others from it.', [('A rectangle is 3 times as long as wide; perimeter 48. Dimensions?', '6 by 18.')])
b.S(34, 'Solve $2(x - 10) = 3(2x + 7)$.', '$x = -\\frac{41}{4}$',
    ['Step 1: expand: $2x - 20 = 6x + 21$.', 'Step 2: subtract $2x$ and 21: $-41 = 4x$.', 'Step 3: $x = -\\frac{41}{4} = -10.25$.'],
    'Collect $x$ on the side with the bigger coefficient.', [('Solve $12x - 13 = 3x + 14$.', '$x = 3$.')])
b.S(34, 'If 4 is subtracted from twice a number, the result is 10 less than the number. Find the number.', '$-6$',
    ['Step 1: $2n - 4 = n - 10$.', 'Step 2: subtract $n$: $n - 4 = -10$, so $n = -6$.', 'Step 3: check: $2(-6) - 4 = -16$ and $-6 - 10 = -16$ (correct).'],
    '"10 less than the number" is $n - 10$, not $10 - n$.', [('Three times a number plus 5 is 20. The number?', '5.')])
b.S(35, 'Solve $0.4x + 0.3(2000 - x) = 750$.', '$x = 1500$',
    ['Step 1: multiply every term by 10: $4x + 3(2000 - x) = 7500$.', 'Step 2: expand: $4x + 6000 - 3x = 7500$.', 'Step 3: $x = 1500$.'],
    'Clear decimals first — the arithmetic becomes whole numbers.', [('Solve $0.06(x - 5) = 0.04(x + 8)$.', '$x = 31$.')])
b.M(37, 'Solve $3 - 2x > 15$.', ['$x > -6$', '$x < -6$', '$x > 6$', '$x < 6$'], 'B',
    ['Step 1: subtract 3: $-2x > 12$.', 'Step 2: divide by $-2$ and **reverse**: $x < -6$.'],
    'Negative divisor → flip the sign.', [('Solve $-1 < -2x + 1$.', '$x < 1$.')])
b.S(37, 'Solve $5x + 4 \\ge 11 - 2x$.', '$x \\ge 1$',
    ['Step 1: add $2x$: $7x + 4 \\ge 11$.', 'Step 2: subtract 4: $7x \\ge 7$.', 'Step 3: divide by 7 (positive): $x \\ge 1$.'],
    'Keep $x$ positive by moving to the side where it grows.', [('Solve $-0.1x + 5 < 0.3x + 1$.', '$x > 10$.')])
b.S(38, 'Three times a number is less than 8 plus twice the number. What numbers are possible?', 'all numbers less than 8',
    ['Step 1: $3n < 8 + 2n$.', 'Step 2: subtract $2n$: $n < 8$.'],
    'Inequality word problems have a set of answers, not one.', [('Twice a number minus 3 is at least 9. Possible numbers?', '$n \\ge 6$.')])

c = QSet('2.3 Practice — variation', 's23')
c.S(40, '$v$ varies directly with $g$, and $v = 30$ when $g = 70$. Find $v$ when $g = 14$.', '6',
    ['Step 1: $k = \\frac{30}{70} = \\frac{3}{7}$.', 'Step 2: $v = \\frac{3}{7} \\times 14 = 6$.'],
    'Shortcut: $g$ was divided by 5, so $v$ is too: $30 \\div 5 = 6$.', [('$P$ varies directly with $I$; $P = 100$ when $I = 20$. Find $P$ when $I = 50$.', '250.')])
c.S(40, 'A car travels 205 km on 20 L of petrol. How much petrol for 369 km?', '36 L',
    ['Step 1: petrol varies directly with distance: $p = kd$, $k = \\frac{20}{205}$.', 'Step 2: $p = \\frac{20}{205} \\times 369 = 36$.'],
    'Find "per km" or "per litre" first: $205 \\div 20 = 10.25$ km per litre, then $369 \\div 10.25 = 36$.', [('A falling object\'s speed is 19.6 m/s after 2 s. After 3 s?', '29.4 m/s.')])
c.S(43, '$R$ varies inversely with $T$, and $R = 168$ when $T = 24$. Find $R$ when $T = 30$.', '134.4',
    ['Step 1: $k = RT = 168 \\times 24 = 4032$.', 'Step 2: $R = \\frac{4032}{30} = 134.4$.'],
    'Inverse: multiply to get $k$, then divide.', [('$T$ varies inversely as $S$; $T = 50$ when $S = 5$. Find $T$ when $S = 20$.', '12.5.')])
c.M(42, 'The time to do a job and the number of people doing it vary', ['directly', 'inversely', 'neither', 'both'], 'B',
    ['Step 1: more people → less time.', 'Step 2: one goes up while the other goes down in the same ratio → inversely.'],
    'Ask: if one doubles, does the other double or halve?', [('Weight of a basket and the number of identical boxes in it?', 'Directly.')])
c.S(39, 'Write an equation for direct variation if $x = 12$, $y = 3$.', '$y = \\frac{1}{4}x$',
    ['Step 1: $k = \\frac{y}{x} = \\frac{3}{12} = \\frac{1}{4}$.', 'Step 2: $y = \\frac{1}{4}x$.'],
    'Direct: $k = y \\div x$.', [('Inverse variation with $x = 0.2$, $y = 0.25$?', '$xy = 0.05$, $y = \\frac{0.05}{x}$.')])
c.TF(42, 'If $y$ varies inversely as $x$ and $x$ is tripled, $y$ becomes one third.', True,
     ['Step 1: $xy = k$ stays fixed.', 'Step 2: if $x$ becomes $3x$, $y$ must become $\\frac{y}{3}$ so the product is still $k$.'],
     'Inverse: the change in $y$ is the reciprocal of the change in $x$.', [('$y$ varies directly as $x$ and $x$ is halved. What happens to $y$?', 'It is halved.')])
c.S(49, 'Machine A makes 18 units in 10 hours. Machine B works at the same rate for 15 hours. How many units?', '27',
    ['Step 1: units vary directly with time: rate $= 18 \\div 10 = 1.8$ per hour.', 'Step 2: $1.8 \\times 15 = 27$.'],
    'Same rate → direct variation.', [('How long for 45 units?', '25 hours.')])

d = QSet('2.4 Practice — absolute value', 's24')
d.S(44, 'Evaluate (a) $|5 - 14|$ (b) $|4| - |-7|$ (c) $|-3| \\times |5|$.', '(a) 9 (b) $-3$ (c) 15',
    ['Step 1 (a): inside first: $5 - 14 = -9$, $|-9| = 9$.', 'Step 2 (b): $4 - 7 = -3$ — the bars are separate, so the result can be negative.', 'Step 3 (c): $3 \\times 5 = 15$.'],
    'Work out the inside of each bar first.', [('Evaluate $|-2 - 5|$.', '7.')])
d.S(45, 'For $x = 5$ and $y = -3$, compare $|x + y|$ and $|x| + |y|$.', '$2 < 8$',
    ['Step 1: $|5 + (-3)| = |2| = 2$.', 'Step 2: $|5| + |-3| = 8$.', 'Step 3: different signs → the left is smaller.'],
    '$|x + y| = |x| + |y|$ only when $x$, $y$ have the same sign (or one is 0).', [('Compare $|x - y|$ and $|y - x|$ for $x = -1$, $y = 3$.', 'Both are 4.')])
d.S(46, 'Solve $|x + 4| = 13$.', '$\\{-17, 9\\}$',
    ['Step 1: $x + 4 = -13$ or $x + 4 = 13$.', 'Step 2: $x = -17$ or $x = 9$.'],
    'Always two cases when the right side is positive.', [('Solve $|2x| = 6$.', '$\\{-3, 3\\}$.')])
d.S(46, 'Solve $5 = |3 - 2x|$.', '$\\{-1, 4\\}$',
    ['Step 1: $3 - 2x = -5$ or $3 - 2x = 5$.', 'Step 2: $-2x = -8 \\Rightarrow x = 4$; $-2x = 2 \\Rightarrow x = -1$.', 'Step 3: check: $|3 - 8| = 5$ and $|3 + 2| = 5$ (correct).'],
    'The absolute value can be on either side.', [('Solve $|2 - x| = 3$.', '$\\{-1, 5\\}$.')])
d.M(46, 'How many solutions has $|2z - 14| = 0$?', ['none', 'one', 'two', 'infinitely many'], 'B',
    ['Step 1: only 0 has absolute value 0.', 'Step 2: $2z - 14 = 0$, $z = 7$ — one solution.'],
    '$|u| = 0$ → one case; $|u| = $ negative → none.', [('Solve $|x - 1| = -2$.', 'No solution.')])
d.S(48, 'Solve $|x - 3| < 2$.', '$1 < x < 5$',
    ['Step 1: less than → between: $-2 < x - 3 < 2$.', 'Step 2: add 3 to all parts: $1 < x < 5$.'],
    '$|x - a| < r$ means "within $r$ of $a$": here within 2 of 3.', [('Solve $|2x| < 8$.', '$-4 < x < 4$.')])
d.S(48, 'Solve $|2y - 1| \\ge 5$.', '$y \\le -2$ or $y \\ge 3$',
    ['Step 1: greater → outside: $2y - 1 \\le -5$ or $2y - 1 \\ge 5$.', 'Step 2: $2y \\le -4$ or $2y \\ge 6$.', 'Step 3: $y \\le -2$ or $y \\ge 3$.'],
    'Two rays → write the word "or".', [('Solve $|x - 5| > 9$.', '$x < -4$ or $x > 14$.')])
d.S(49, 'Solve $5 < |3 - x|$.', '$x < -2$ or $x > 8$',
    ['Step 1: rewrite: $|3 - x| > 5$.', 'Step 2: $3 - x < -5$ or $3 - x > 5$.', 'Step 3: $-x < -8 \\Rightarrow x > 8$; $-x > 2 \\Rightarrow x < -2$ (sign flips when dividing by $-1$).'],
    'Two traps in one: swapped sides and a negative $x$.', [('Solve $|2x + 6| \\le 2$.', '$-4 \\le x \\le -2$.')])
d.TF(48, 'The solution set of $|x| > -1$ is all real numbers.', True,
     ['Step 1: $|x| \\ge 0$ for every $x$.', 'Step 2: every number $\\ge 0$ is $> -1$, so every $x$ works.'],
     'Compare with a negative number before splitting.', [('Solve $|x| < -1$.', 'No solution.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Independent quantity', 'The quantity that is chosen or controlled; its values form the domain.', 20),
    ('Dependent quantity', 'The quantity that depends on the independent one; its values form the range.', 21),
    ('Domain', 'The set of all possible input (independent) values.', 21),
    ('Range', 'The set of all output (dependent) values.', 21),
    ('Discrete graph', 'A graph of separate points; the inputs take only separate values.', 23),
    ('Continuous graph', 'An unbroken graph; the inputs take every real value in an interval.', 25),
    ('Equivalent equations', 'Equations with exactly the same solution set.', 31),
    ('Constant of proportionality', 'The fixed number $k$ in $y = kx$ or $xy = k$.', 39),
    ('Absolute value', '$|x|$, the distance of $x$ from 0 on the number line.', 44),
]
TIPS = [
    ('Count the input → discrete dots; measure it → continuous line.', 25),
    ('Inequalities: multiply or divide by a negative → reverse the sign.', 36),
    ('Direct: y ÷ x constant. Inverse: x × y constant.', 42),
    ('|u| < k → between (and); |u| > k → outside (or).', 47),
]
IDEAS = [('graph', 'Discrete or continuous?', 'l2_1', 'math9-u2-md-graph-t'),
         ('ineq', 'Equation vs inequality moves', 'l2_2', 'math9-u2-md-eqineq-t'),
         ('var', 'Direct vs inverse variation', 'l2_3', 'math9-u2-md-var-t'),
         ('abs', 'Absolute value cases', 'l2_4', 'math9-u2-md-abs-t')]
