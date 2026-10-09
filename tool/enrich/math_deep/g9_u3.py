r"""Grade 9 Unit 3 — Linear Functions (pp. 50-81)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet, plane
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side, halfplane

UID = 'math9-u3'
set_unit(UID)
GBLUE, GRED, GGREEN, GPURPLE = '#2F5F8F', '#C0503A', '#2A7A6B', '#6B4F9E'


# ------------------------------------------------------------------ figures
def f_ineq2():
    a = Plot(-4, 4, -4, 4, unit=16)
    halfplane(a, 1, 1, 0)
    a.fullline(-1, 0, c=BLUE, w=2.6, dash=True)
    a.pt(0, 1, None, c=GREEN).pt(2, -1, None, c=GREEN)
    a.text(a.X(1.6), a.Y(2.6), 'y > −x', 13, BLUE)
    b = Plot(-4, 4, -4, 4, unit=16)
    halfplane(b, 2, -3, -5)
    b.fullline(2 / 3, -5 / 3, c=RED, w=2.6, dash=True)
    b.pt(0, 0, None, c=PURPLE).text(b.X(-3.8), b.Y(3.3), '(0, 0): 0 > 5 false', 11.5, PURPLE, 'start')
    b.pt(1, -1, None, c=RED).pt(-2, -3, None, c=RED)
    b.text(b.X(0.4), b.Y(-3.4), '2x − 3y > 5', 12.5, RED, 'start')
    return side_by_side([a, b], 10, ['shade above the dashed line', 'shade away from (0, 0)'])


def f_ladder():
    f = Fig(300, 190)
    B, A, C = (60, 160), (240, 160), (60, 40)
    f.rect(36, 20, 24, 150, GREY, 1.4, '#EDE8E0')
    f.line(20, 160, 290, 160, INK, 2)
    f.line(*A, *C, ORANGE, 6)
    for t in (0.2, 0.4, 0.6, 0.8):
        x, y = A[0] + (C[0] - A[0]) * t, A[1] + (C[1] - A[1]) * t
        f.line(x - 6, y - 4, x + 6, y + 4, '#B07A2A', 2)
    f.right(B, A, C, 12, INK)
    f.seglabel(B, A, 'run 3 m', 14, BLUE, 13, -1)
    f.text(68, 104, 'rise 2 m', 13, RED, 'start')
    f.text(B[0] - 10, B[1] + 16, 'B', 13).text(A[0] + 8, A[1] + 16, 'A', 13).text(C[0] - 10, C[1] - 6, 'C', 13)
    f.text(200, 70, 'slope = rise ÷ run', 13, INK).text(200, 90, '= 2 ÷ 3', 13, INK)
    return f


def f_slopetri():
    p = Plot(-3, 4, -4, 3, unit=30)
    p.fullline(2, -3, c=BLUE, w=2.6)
    p.g('k1 k3').seg((0, -3), (1, -3), GREEN, 3).seg((1, -3), (1, -1), RED, 3).end()
    p.g('k1 k3').text(p.X(0.5), p.Y(-3) + 16, 'run 1', 12, GREEN).text(p.X(1) + 6, p.Y(-2) + 4, 'rise 2', 12, RED, 'start').end()
    p.g('k2 k3').seg((0, -3), (2, -3), GREEN, 2, dash='5 3').seg((2, -3), (2, 1), RED, 2, dash='5 3').end()
    p.g('k2 k3').text(p.X(2) + 6, p.Y(-1) + 4, 'rise 4, run 2', 12, PURPLE, 'start').end()
    p.pt(0, -3).text(p.X(-0.9), p.Y(-3) + 5, 'P(0, −3)', 13, RED, 'end').pt(1, -1, 'Q(1, −1)', 'nw').pt(2, 1, 'R(2, 1)', 'nw')
    return p


def f_slopesigns():
    figs = []
    for lab, kind in (('positive: rises', 'pos'), ('negative: falls', 'neg'), ('zero: flat', 'zero'), ('undefined: vertical', 'vert')):
        p = Plot(-3, 3, -3, 3, unit=12, labels=False, grid=False)
        c = {'pos': GREEN, 'neg': RED, 'zero': BLUE, 'vert': PURPLE}[kind]
        if kind == 'pos':
            p.fullline(1, 0.3, c=c, w=3)
        elif kind == 'neg':
            p.fullline(-1.2, 0.5, c=c, w=3)
        elif kind == 'zero':
            p.fullline(0, 1.5, c=c, w=3)
        else:
            p.fullline(x=1.5, c=c, w=3)
        g = Fig(p.w + 4, p.h + 18)
        g.raw('<g>' + ''.join(p.p) + '</g>')
        g.text(p.w / 2, p.h + 14, lab, 11.5, c)
        figs.append(g)
    return side_by_side(figs, 2)


def f_cases():
    figs = []
    for kind in ('one', 'none', 'many'):
        p = Plot(-1, 5, -1, 5, unit=16, labels=False)
        if kind == 'one':
            p.fullline(-1, 5, c=BLUE, w=2.6).fullline(1, -1, c=RED, w=2.6).pt(3, 2, None, c=INK, r=4.5)
        elif kind == 'none':
            p.fullline(1, 1, c=BLUE, w=2.6).fullline(1, -1.5, c=RED, w=2.6)
        else:
            p.fullline(-1, 4, c=RED, w=6).fullline(-1, 4, c=BLUE, w=2.4, dash='6 4')
        figs.append(p)
    return side_by_side(figs, 8, ['cross: one solution', 'parallel: none', 'same line: infinitely many'])


DIAGRAMS = {
    'ineq2': (f_ineq2(), 'Graphs of linear inequalities (Fig. 3.4 and 3.5)', 58),
    'ladder': (f_ladder(), 'Slope of a ladder: rise over run (Fig. 3.7)', 61),
    'slopetri': (f_slopetri(), 'Any two points give the same slope (Fig. 3.9)', 64),
    'slopesigns': (f_slopesigns(), 'Four kinds of slope', 66),
    'cases': (f_cases(), 'Three possibilities for two lines', 80),
}

# ------------------------------------------------------------------ lesson 3.1
L1 = [
    T('=math9-u3-c01', '3.1 What makes a function linear?', 52,
      'A **linear function** can be written as $$y = mx + b$$ where $m$ and $b$ are fixed real numbers. Its graph is a straight line. Points that lie on one straight line are called **collinear**.',
      'Equivalent form: $Ax + By = C$ with $B \\ne 0$ — solve for $y$ to get $y = mx + b$.',
      'Signs that a rule is **not** linear: $x$ is squared ($x^2$), under a root ($\\sqrt{x}$), in a denominator ($\\frac{1}{x}$), or multiplied by $y$ ($xy$).',
      'Tirhas saves 5 Nakfa a week: $S = 5N$ is linear, but since $N$ is a whole number of weeks its graph is **dots on a line**, not a full line. A rectangle of length 5 and width $w$: $A = 5w$ — here $w$ can be any positive number, so the graph is a ray.'),
    GR('gr-save', 'Fig. 3.1: Tirhas\'s savings, S = 5N', 51,
       plane(-1, 9, -5, 45, points=[{'x': n, 'y': 5 * n, 'color': GRED} for n in range(1, 8)]),
       'The dots are collinear (they lie on the line $S = 5N$), but we do not join them: there is no "week 2.5".'),
    TB('lin-t', 'Linear or not?', 53, ['Equation', 'Rewrite', 'Linear?'],
       [['$y = -3x + 2$', 'already $y = mx + b$, $m = -3$, $b = 2$', 'yes'],
        ['$2y - 3x = 6$', '$y = \\frac{3}{2}x + 3$', 'yes'],
        ['$5x = 2y + 10$', '$y = \\frac{5}{2}x - 5$', 'yes'],
        ['$y = 3x^2 - 12$', '$x$ is squared', 'no'],
        ['$t = (u + 1)(u - 1)$', '$t = u^2 - 1$', 'no'],
        ['$s$ = side of a square of area $A$', '$s = \\sqrt{A}$', 'no'],
        ['$C = \\pi d$', '$m = \\pi$, $b = 0$', 'yes ($\\pi$ is just a number)']],
       'Expand and simplify **before** you decide — $(u + 1)(u - 1)$ hides a square.'),
    WK('ex-31a', 'Worked example: from a table to an equation', 53,
       'Dahlak\'s ages 1, 2, 3, 4, 5 and her brother Aron\'s ages 7, 8, 9, 10, 11. Write an equation and find Aron\'s age when Dahlak is 10.',
       ['Each pair differs by 6: Aron is 6 years older.', '$y = x + 6$ (linear, $m = 1$, $b = 6$).', '$x = 10$: $y = 16$.'],
       '$y = x + 6$; Aron is 16'),
]

# ------------------------------------------------------------------ lesson 3.2
L2 = [
    T('=math9-u3-c02', '3.2.1 Graphing a line', 54,
      'Two points fix a line, but plot **three** so that a mistake shows up (the three must be collinear).',
      'Method: choose easy $x$-values (like $-1, 0, 1$ or $0, 1, 2$), compute $y$, plot, rule a line through them and extend it with arrows.',
      '**Shifting:** the graph of $y = mx + b$ is the graph of $y = mx$ moved **up** $b$ units (down if $b$ is negative). All lines $y = mx + b$ with the same $m$ are **parallel**. To shift a point down 2, subtract 2 from its **$y$-coordinate**: $(1, 1) \\to (1, -1)$.'),
    GR('gr-shift', 'Fig. 3.2: y = x shifted up and down', 55,
       plane(-5, 5, -5, 5, lines=[{'m': 1, 'c': 0, 'label': 'y = x', 'color': GBLUE}, {'m': 1, 'c': 2, 'label': 'y = x + 2', 'color': GGREEN},
                                  {'m': 1, 'c': -2, 'label': 'y = x − 2', 'color': GRED}],
             points=[{'x': 0, 'y': 0, 'color': GBLUE}, {'x': 0, 'y': -2, 'label': '(0, −2)', 'color': GRED}, {'x': 0, 'y': 2, 'label': '(0, 2)', 'color': GGREEN}]),
       'Every point of $y = x$ moves straight up 2 or down 2. Same slope → parallel lines.'),
    GR('gr-family', 'y = mx always passes through the origin', 54,
       plane(-4, 4, -4, 4, lines=[{'m': -1, 'c': 0, 'label': 'y = −x', 'color': GRED}, {'m': 1, 'c': 0, 'label': 'y = x', 'color': GBLUE},
                                  {'m': 3, 'c': 0, 'label': 'y = 3x', 'color': GGREEN}]),
       'With $b = 0$ every line passes through $(0, 0)$. A bigger $|m|$ gives a steeper line; a negative $m$ makes it fall.'),
    T('=math9-u3-c03', '3.2.2 Graphing a linear inequality in two variables', 58,
      'The graph of $y > mx + b$ (or $Ax + By > C$) is a **half-plane**: all points on one side of the boundary line.',
      '**Step 1 — boundary:** draw the line you get by replacing the inequality sign with "=". Use a **dashed** line for $<$ or $>$ (points on it are not solutions) and a **solid** line for $\\le$ or $\\ge$.',
      '**Step 2 — test point:** pick a point not on the line — $(0, 0)$ is easiest — and substitute it.',
      '**Step 3 — shade:** if the test point makes the inequality true, shade its side; if false, shade the other side.',
      'Shortcut for $y > \\dots$ / $y < \\dots$ (with $y$ alone): "greater" → shade **above**, "less" → shade **below**.'),
    DG('ineq2', 'Two inequalities, shaded', 59, 'ineq2',
       'Left: $y > -x$ — the line $y = -x$ is dashed, the region above is shaded (e.g. $(0, 1)$: $1 > 0$ true). Right: Example 3.3, $2x - 3y > 5$ — testing $(0, 0)$ gives $0 > 5$, false, so the side **without** the origin (below the line) is shaded.'),
    TB('bound-t', 'Boundary line and shading', 59, ['Sign', 'Boundary line', 'Points on the line'],
       [['$<$', 'dashed', 'not included'], ['$>$', 'dashed', 'not included'], ['$\\le$', 'solid', 'included'], ['$\\ge$', 'solid', 'included']],
       'Vertical and horizontal boundaries: $x > 0$ → right of the $y$-axis; $y \\le -3$ → on and below the line $y = -3$.'),
    WK('ex-32a', 'Worked example: graph y ≤ −2x + 1', 81,
       'Describe the graph of $y \\le -2x + 1$ and decide whether $(1, -3)$ and $(2, 0)$ are in it.',
       ['Boundary $y = -2x + 1$ through $(0, 1)$ and $(1, -1)$; **solid** because of $\\le$.', 'Test $(0, 0)$: $0 \\le 1$ true → shade the side containing the origin (below the line).',
        '$(1, -3)$: $-3 \\le -1$ true → in the region. $(2, 0)$: $0 \\le -3$ false → not in it.'],
       'solid line, shade below; $(1, -3)$ yes, $(2, 0)$ no',
       graph=plane(-3, 3, -4, 4, lines=[{'m': -2, 'c': 1, 'label': 'y = −2x + 1', 'color': GBLUE}],
                   points=[{'x': 1, 'y': -3, 'label': '(1, −3)', 'color': GGREEN}, {'x': 2, 'y': 0, 'label': '(2, 0)', 'color': GRED}])),
]

# ------------------------------------------------------------------ lesson 3.3
L3 = [
    T('=math9-u3-c04', '3.3 Slope: how steep is a line?', 61,
      'A ladder leans on a wall: its foot is 3 m from the wall (horizontal distance, the **run**) and it reaches 2 m up (vertical distance, the **rise**). Its **slope** is $\\frac{\\text{rise}}{\\text{run}} = \\frac{2}{3}$.',
      'For a line through $P_1(x_1, y_1)$ and $P_2(x_2, y_2)$:',
      '$$m = \\frac{y_2 - y_1}{x_2 - x_1} = \\frac{\\text{change in } y}{\\text{change in } x}, \\quad x_2 \\ne x_1$$',
      'It does not matter which point you call $P_1$ — but keep the **same order** on top and bottom. Any two points of a line give the same slope.'),
    DG('ladder', 'Rise over run', 61, 'ladder'),
    ST('slopetri', 'Slope of y = 2x − 3 from different points', 64, 'slopetri',
       [('$P$ to $Q$: run $= 1 - 0 = 1$, rise $= -1 - (-3) = 2$, slope $= \\frac{2}{1} = 2$.', 'k1'),
        ('$P$ to $R$: run $= 2$, rise $= 1 - (-3) = 4$, slope $= \\frac{4}{2} = 2$.', 'k2'),
        ('Same slope from any two points — and it equals the coefficient of $x$ in $y = 2x - 3$.', 'k3')]),
    T('mform-t', 'Reading the slope from the equation', 65,
      'When the equation is in the form $y = mx + b$, the slope is $m$ — the coefficient of $x$.',
      'Example 3.4: $-12x + 3y = 5 \\Rightarrow 3y = 12x + 5 \\Rightarrow y = 4x + \\frac{5}{3}$, so $m = 4$.',
      'For $Ax + By = C$ in general: $m = -\\frac{A}{B}$.'),
    DG('slopesigns', 'Positive, negative, zero, undefined', 66, 'slopesigns',
       'Read from **left to right**: rising → positive; falling → negative; horizontal ($y = 2$) → zero; vertical ($x = 3$) → undefined, because the run is 0 and we cannot divide by 0.'),
    TB('slope-t', 'Slope summary', 66, ['Line', 'Example', 'Slope'],
       [['Rises left to right', '$y = 3x - 2$', 'positive (3)'], ['Falls left to right', '$y = -3x - 2$', 'negative ($-3$)'],
        ['Horizontal', '$y = 2$, $2y = -3$', '0'], ['Vertical', '$x = 3$, $x + 5 = 0$', 'undefined'],
        ['Parallel lines', '$y = 2x + 1$, $y = 2x - 1$', 'equal slopes'],
        ['Real life', 'temperature rising 5 °C every 15 s', 'rate of change: $\\frac{5}{15} = \\frac{1}{3}$ °C per second']],
       'Slope is a **rate**: "how much $y$ changes for each 1 unit of $x$". For $S = 50T$ it is the speed, 50 km/h.'),
    WK('ex-33a', 'Worked example: slopes from points', 63,
       'Find the slope through (a) $(1, 6)$ and $(3, 5)$ (b) $(5, 1)$ and $(-2, 1)$ (c) $(3, -4)$ and $(3, 7)$.',
       ['(a) $m = \\frac{5 - 6}{3 - 1} = \\frac{-1}{2}$ — the line falls.', '(b) $m = \\frac{1 - 1}{-2 - 5} = \\frac{0}{-7} = 0$ — horizontal.', '(c) $x_2 - x_1 = 3 - 3 = 0$ — division by zero, slope undefined — vertical line $x = 3$.'],
       '(a) $-\\frac{1}{2}$ (b) 0 (c) undefined'),
    WK('ex-33b', 'Worked example: the ladder (Exercise 3.4)', 67,
       'A ladder\'s foot is 1.5 m from a wall and its slope is $\\frac{5}{3}$. How high up the wall does it reach?',
       ['Slope $= \\frac{\\text{rise}}{\\text{run}}$, so rise $= $ slope $\\times$ run.', 'Rise $= \\frac{5}{3} \\times 1.5 = 2.5$ m.'],
       '2.5 m'),
]

# ------------------------------------------------------------------ lesson 3.4
L4 = [
    T('=math9-u3-c05', '3.4 Intercepts', 68,
      'The **$x$-intercept** is the $x$-coordinate where the line crosses the $x$-axis: put $y = 0$ and solve.',
      'The **$y$-intercept** is the $y$-coordinate where it crosses the $y$-axis: put $x = 0$. In $y = mx + b$ it is simply $b$.',
      'Example 3.5 (the textbook\'s problem says $y = -2x + 4$ but its working uses $y = -2x + 3$). For $y = -2x + 3$: $0 = -2x + 3$ gives $x$-intercept $1.5$; $y$-intercept 3. For $y = -2x + 4$ the intercepts would be 2 and 4.'),
    GR('gr-int', 'Fig. 3.10: 3x + 2y = 6 from its intercepts', 70,
       plane(-2, 5, -3, 5, lines=[{'m': -1.5, 'c': 3, 'label': '3x + 2y = 6', 'color': GBLUE}],
             points=[{'x': 2, 'y': 0, 'label': '(2, 0)', 'color': GRED}, {'x': 0, 'y': 3, 'label': '(0, 3)', 'color': GGREEN}]),
       '$y = 0$: $3x = 6$, $x = 2$. $x = 0$: $2y = 6$, $y = 3$. Join $(2, 0)$ and $(0, 3)$ — the quickest way to draw a line in the form $Ax + By = C$.'),
    TB('eqn-t', 'Finding the equation of a line', 71, ['You know', 'Method', 'Example'],
       [['slope $m$ and $y$-intercept $b$', 'write $y = mx + b$', '$m = 1$, $b = 2$: $y = x + 2$'],
        ['slope $m$ and one point', 'substitute the point in $y = mx + b$ to find $b$', '$m = -2$ through $(5, 2)$: $2 = -10 + b$, $b = 12$'],
        ['two points', 'find $m$ first, then $b$ from either point', 'Example 3.7 below'],
        ['both intercepts $a$ and $b$', 'points $(a, 0)$, $(0, b)$; $m = -\\frac{b}{a}$', '$x$-int $-1$, $y$-int $-3$: $y = -3x - 3$']],
       'Check by substituting the **other** given point into your final equation.'),
    WK('ex-34a', 'Worked example: Example 3.7', 70,
       'Write the equation of the line through $(-1, 3)$ and $(2, 9)$.',
       ['Slope: $m = \\frac{9 - 3}{2 - (-1)} = \\frac{6}{3} = 2$.', 'Substitute $(-1, 3)$ in $y = 2x + b$: $3 = -2 + b$, so $b = 5$.', 'Check with $(2, 9)$: $2(2) + 5 = 9$ (correct).'],
       '$y = 2x + 5$'),
    WK('ex-34b', 'Worked example: x-intercept and slope', 71,
       'Find the line with $x$-intercept 4 and slope $-3$.',
       ['The $x$-intercept 4 means the point $(4, 0)$.', '$0 = -3(4) + b$, so $b = 12$.'],
       '$y = -3x + 12$'),
]

# ------------------------------------------------------------------ lesson 3.5
L5 = [
    T('=math9-u3-c07', '3.5.1 Systems of two linear equations', 72,
      'A **system** (simultaneous equations) is two equations that must be true **at the same time**. A solution is an ordered pair $(x, y)$ that satisfies **both**.',
      'Example: the sum of two numbers is 7 and their difference is 3: $x + y = 7$, $x - y = 3$. Try $(5, 2)$: $5 + 2 = 7$ and $5 - 2 = 3$ — both true, so $(5, 2)$ is the solution.',
      'Three methods: **elimination**, **substitution**, and **graphing**.'),
    T('elim-t', '3.5.2 Elimination method', 73,
      '1. Write both equations as $ax + by = c$ (variables on the left, numbers on the right).',
      '2. Multiply one or both equations so that one variable has **opposite** (or equal) coefficients.',
      '3. **Add** the equations (opposite coefficients) or **subtract** them (equal coefficients) — that variable disappears.',
      '4. Solve for the remaining variable, substitute back to find the other, and check in **both** original equations.'),
    WK('ex-35a', 'Worked example: Example 3.8 (elimination)', 74,
       'Solve $5x - 3y = 1$ and $3x + 4y = 18$.',
       ['To eliminate $y$: multiply the first by 4 and the second by 3: $20x - 12y = 4$ and $9x + 12y = 54$.', 'Add: $29x = 58$, so $x = 2$.', 'Substitute in $3x + 4y = 18$: $6 + 4y = 18$, $y = 3$.', 'Check in $5x - 3y = 1$: $10 - 9 = 1$ (correct).'],
       '$(2, 3)$'),
    T('=math9-u3-c08', '3.5.3 Substitution method', 75,
      '1. Make one variable the subject of one equation (choose one with coefficient 1 if possible).',
      '2. **Substitute** that expression into the other equation — you get one equation in one variable.',
      '3. Solve it, then put the value back into the expression from step 1.',
      'Word problem (Exercise 3.6): perimeter 16, length three times the breadth: $l = 3b$ and $2l + 2b = 16$ → $6b + 2b = 16$, $b = 2$, $l = 6$.'),
    WK('ex-35b', 'Worked example: Example 3.10 (substitution)', 75,
       'Solve $3a - 2b = 5$ and $a + 5b = -4$.',
       ['From the second: $a = -5b - 4$.', 'Substitute: $3(-5b - 4) - 2b = 5$ → $-15b - 12 - 2b = 5$ → $-17b = 17$ → $b = -1$.', '$a = -5(-1) - 4 = 1$.', 'Check: $3(1) - 2(-1) = 5$ (correct).'],
       '$a = 1$, $b = -1$'),
    T('=math9-u3-c09', '3.5.4 Graphical method', 77,
      'Draw both lines on the same axes. The **intersection point** is the solution, because it lies on both lines. Always check the point in both equations — reading a graph is not exact.'),
    GR('gr-sys', 'Fig. 3.11: x + y = 5 and x − y = 1', 78,
       plane(-2, 7, -3, 7, lines=[{'m': -1, 'c': 5, 'label': 'y = −x + 5', 'color': GBLUE}, {'m': 1, 'c': -1, 'label': 'y = x − 1', 'color': GRED}],
             points=[{'x': 3, 'y': 2, 'label': '(3, 2)', 'color': GGREEN}]),
       'The lines cross at $(3, 2)$: $3 + 2 = 5$ and $3 - 2 = 1$ (both correct).'),
    DG('cases', 'How many solutions?', 80, 'cases',
       'Different slopes → the lines cross once: **one solution**. Same slope, different intercepts → parallel: **no solution** (algebra ends in something false like $0 = 5$). Same line → **infinitely many** (algebra ends in something always true like $0 = 0$).'),
    TB('sys-t', 'Choosing a method', 80, ['Method', 'Best when', 'Watch out for'],
       [['Elimination', 'both equations in the form $ax + by = c$', 'multiply **every** term, including the right side'],
        ['Substitution', 'a variable already alone, e.g. $x = 2y - 3$', 'brackets when you substitute: $5(2y - 3)$'],
        ['Graphing', 'you want a picture or the number of solutions', 'answers that are not whole numbers are hard to read'],
        ['Quick test', 'compare slopes $m$ and intercepts $b$', 'equal $m$, different $b$ → none; equal $m$ and $b$ → infinitely many']],
       'Whatever the method, check the answer in **both** original equations.'),
    WK('ex-35c', 'Worked example: stamps (Review question 7)', 81,
       'Semira bought 32 stamps, some 20-cent and some 50-cent, worth 10.90 Nakfa altogether. How many of each?',
       ['Let $t$ = number of 20-cent and $f$ = number of 50-cent stamps. Work in cents: 10.90 Nakfa = 1090 cents.', '$t + f = 32$ and $20t + 50f = 1090$ (divide by 10: $2t + 5f = 109$).', 'From the first $t = 32 - f$: $2(32 - f) + 5f = 109$ → $64 + 3f = 109$ → $f = 15$.', '$t = 17$. Check: $17 \\times 20 + 15 \\times 50 = 340 + 750 = 1090$ (correct).'],
       '17 twenty-cent and 15 fifty-cent stamps'),
]

LESSONS = {'math9-u3-l3-1': L1, 'math9-u3-l3-2': L2, 'math9-u3-l3-3': L3, 'math9-u3-l3-4': L4, 'math9-u3-l3-5': L5}

# ------------------------------------------------------------------ practice
a = QSet('3.1 Practice — linear functions', 's31')
a.M(53, 'Which equation is NOT linear?', ['$-3x + 7y = 9$', '$y = 2x$', '$y = 3x^2 - 12$', '$5x = 2y + 10$'], 'C',
    ['Step 1: A, B, D can all be written as $y = mx + b$.', 'Step 2: C contains $x^2$ → not linear.'],
    'Look for powers of $x$ other than 1.', [('Is $d = -10t^2 + 40$ linear?', 'No — $t$ is squared.')])
a.S(53, 'Write an equation: the second number $y$ is the product of $-3$ and the first number $x$. Is it linear?', '$y = -3x$; yes',
    ['Step 1: "product of $-3$ and $x$" is $-3x$.', 'Step 2: $y = -3x$ has the form $y = mx + b$ with $m = -3$, $b = 0$.'],
    'Translate word by word.', [('The sum of two numbers is 10. Equation?', '$x + y = 10$, i.e. $y = -x + 10$ — linear.')])
a.S(54, 'Fill the gaps for $y = 2x - 5$: $x = 1 \\to y = ?$; $y = 3 \\to x = ?$; $y = 11 \\to x = ?$', '$-3$; 4; 8',
    ['Step 1: $2(1) - 5 = -3$.', 'Step 2: $2x - 5 = 3 \\Rightarrow x = 4$.', 'Step 3: $2x - 5 = 11 \\Rightarrow x = 8$.'],
    'Given $y$, solve an equation for $x$.', [('$y = 27$?', '$x = 16$.')])
a.S(54, 'The mass of pure gold is $m = 19v$ (grams, cm³). Find $m$ when $v = 0.1$ and $v$ when $m = 38$.', '1.9 g; 2 cm³',
    ['Step 1: $m = 19 \\times 0.1 = 1.9$ g.', 'Step 2: $38 = 19v \\Rightarrow v = 2$ cm³.'],
    'Direct variation is a linear function with $b = 0$.', [('$v = 5$ cm³?', '95 g.')])
a.TF(54, 'A father\'s age $y$ being 20 more than twice his son\'s age $x$ is a linear function.', True,
     ['Step 1: $y = 2x + 20$.', 'Step 2: this is $y = mx + b$ with $m = 2$, $b = 20$ → linear.'],
     '"Twice … plus …" is always linear.', [('Is "the side of a square is the square root of its area" linear?', 'No.')])

b = QSet('3.2 Practice — graphing lines and inequalities', 's32')
b.M(56, 'If $(a, b)$ is on $y = mx$, which point is on $y = mx - 7$?', ['$(a + 7, b)$', '$(a - 7, b)$', '$(a, b - 7)$', '$(a, b + 7)$'], 'C',
    ['Step 1: $y = mx - 7$ is $y = mx$ moved down 7.', 'Step 2: keep $x$, subtract 7 from $y$: $(a, b - 7)$.'],
    'Vertical shift changes only the $y$-coordinate.', [('Which point is on $y = mx + 3$?', '$(a, b + 3)$.')])
b.S(56, 'Make a table for $y = 0.5x + 1$ with $x = -2, 0, 2$ and give the points.', '$(-2, 0), (0, 1), (2, 2)$',
    ['Step 1: $x = -2$: $-1 + 1 = 0$.', 'Step 2: $x = 0$: $y = 1$.', 'Step 3: $x = 2$: $1 + 1 = 2$.'],
    'With $m = 0.5$ choose even $x$-values to avoid fractions.', [('Points of $y = 2x - 3$ for $x = 0, 1, 2$?', '$(0, -3), (1, -1), (2, 1)$.')])
b.M(60, 'For the graph of $y > 2x + 3$ the boundary line is', ['solid, shade above', 'dashed, shade above', 'solid, shade below', 'dashed, shade below'], 'B',
    ['Step 1: ">" → dashed (points on the line are not included).', 'Step 2: $y$ greater → above.'],
    'Strict sign → dashed.', [('$y \\le -3x + 1$?', 'Solid, shade below.')])
b.S(60, 'Do $(0, -1)$ and $(0, -2)$ satisfy $y < -3x + 1$? Can this inequality be a function?', 'both yes; no',
    ['Step 1: $-1 < 1$ true; $-2 < 1$ true.', 'Step 2: the input $x = 0$ has many outputs, so the inequality is not a function.'],
    'A region contains many points above one $x$.', [('Does $(1, -1)$ satisfy it?', 'No: $-1 < -2$ is false.')])
b.TF(59, 'In the graph of $3x + 2y > 0$, the point $(0, 0)$ can be used as the test point.', False,
     ['Step 1: $(0, 0)$ is ON the boundary $3x + 2y = 0$.', 'Step 2: a test point must be off the line; use e.g. $(1, 0)$: $3 > 0$ true → shade that side.'],
     'Lines through the origin need another test point.', [('Which side for $y - 2x \\ge 1$?', 'Test $(0, 0)$: $0 \\ge 1$ false → shade the side without the origin (above).')])
b.S(57, 'Describe the graph of $x \\le -2$.', 'solid vertical line $x = -2$, shade to the left',
    ['Step 1: boundary $x = -2$ is vertical; $\\le$ → solid.', 'Step 2: smaller $x$-values are to the left.'],
    'Only $x$ → vertical boundary; only $y$ → horizontal.', [('$y > -3$?', 'Dashed horizontal line $y = -3$, shade above.')])

c = QSet('3.3 Practice — slope', 's33')
c.S(67, 'Find the slope through $(6, -4)$ and $(4, -2)$ and say if the line rises or falls.', '$-1$, falls',
    ['Step 1: $m = \\frac{-2 - (-4)}{4 - 6} = \\frac{2}{-2} = -1$.', 'Step 2: negative → falls left to right.'],
    'Subtracting a negative: $-2 - (-4) = +2$.', [('$(0, 1)$ and $(1, -2)$?', '$-3$, falls.')])
c.M(67, 'The slope of $5x + 3y = 15$ is', ['5', '$\\frac{5}{3}$', '$-\\frac{5}{3}$', '$-5$'], 'C',
    ['Step 1: $3y = -5x + 15$.', 'Step 2: $y = -\\frac{5}{3}x + 5$ → $m = -\\frac{5}{3}$.'],
    'Get $y$ alone first, or use $m = -\\frac{A}{B}$.', [('Slope of $5x = 7y - 6$?', '$\\frac{5}{7}$.')])
c.S(67, 'Find the slopes of (a) $2y = -3$ (b) $x + 5 = 0$.', '(a) 0 (b) undefined',
    ['Step 1 (a): $y = -1.5$ — horizontal → 0.', 'Step 2 (b): $x = -5$ — vertical → undefined.'],
    'No $x$ → horizontal; no $y$ → vertical.', [('Slope of $y + 2 = 0$?', '0.')])
c.S(66, 'Water temperature rises from 30 °C to 60 °C in 90 seconds at a steady rate. What is the slope of the graph and what does it mean?', '$\\frac{1}{3}$ °C per second',
    ['Step 1: rise $= 60 - 30 = 30$ °C, run $= 90$ s.', 'Step 2: slope $= \\frac{30}{90} = \\frac{1}{3}$.', 'Step 3: meaning: the temperature goes up $\\frac{1}{3}$ °C every second (5 °C per 15 s).'],
    'Slope = rate of change; give its units.', [('A car: $S = 50T$. What does 50 mean?', 'Speed 50 km/h.')])
c.TF(63, 'The slope through $A(0, -3)$ and $B(1, -1)$ changes if you start from $B$ instead of $A$.', False,
     ['Step 1: from A: $\\frac{-1 + 3}{1 - 0} = 2$.', 'Step 2: from B: $\\frac{-3 + 1}{0 - 1} = \\frac{-2}{-1} = 2$. Same.'],
     'Swap both top and bottom together — the signs cancel.', [('Slope through $(-2, 1)$ and $(2, 2)$?', '$\\frac{1}{4}$.')])
c.S(64, 'Are the points $(0, 1)$, $(2, 5)$ and $(4, 9)$ collinear?', 'yes',
    ['Step 1: slope of the first two: $\\frac{5 - 1}{2} = 2$.', 'Step 2: slope of the last two: $\\frac{9 - 5}{2} = 2$.', 'Step 3: equal slopes through a shared point → one line.'],
    'Collinear ⇔ equal slopes between pairs.', [('Is $(3, 8)$ on the same line?', 'No — $y = 2x + 1$ gives 7.')])

d = QSet('3.4 Practice — intercepts and equations of lines', 's34')
d.S(71, 'Find the slope and $y$-intercept of $7y - 3x - 10 = 0$.', '$m = \\frac{3}{7}$, $b = \\frac{10}{7}$',
    ['Step 1: $7y = 3x + 10$.', 'Step 2: $y = \\frac{3}{7}x + \\frac{10}{7}$.'],
    'Divide **every** term by 7.', [('$5y + x = 15$?', '$m = -\\frac{1}{5}$, $b = 3$.')])
d.S(71, 'Find the equation of the line through $(-4, 7)$ and $(6, -3)$.', '$y = -x + 3$',
    ['Step 1: $m = \\frac{-3 - 7}{6 + 4} = \\frac{-10}{10} = -1$.', 'Step 2: $7 = -1(-4) + b = 4 + b \\Rightarrow b = 3$.', 'Step 3: check $(6, -3)$: $-6 + 3 = -3$ (correct).'],
    'Slope first, then $b$, then check.', [('Line through $(5, 2)$ with slope $-2$?', '$y = -2x + 12$.')])
d.S(71, 'Find the line with $y$-intercept $-5$ through $(1, 3)$.', '$y = 8x - 5$',
    ['Step 1: $b = -5$, so $y = mx - 5$.', 'Step 2: $3 = m - 5 \\Rightarrow m = 8$.'],
    'A known $y$-intercept leaves only $m$ to find.', [('$x$-intercept 1 through $(2, -1)$?', '$y = -x + 1$.')])
d.S(72, 'Fill the blanks so that $\\_x + \\_y = 10$ has $x$-intercept 5 and $y$-intercept 2.', '$2x + 5y = 10$',
    ['Step 1: $(5, 0)$ on the line: $5A = 10$, $A = 2$.', 'Step 2: $(0, 2)$: $2B = 10$, $B = 5$.'],
    'Each intercept gives one coefficient directly.', [('$\\_x + \\_y = 12$ with intercepts $-2$ and 3?', '$-6x + 4y = 12$.')])
d.M(71, 'The line through $(3, 5)$ and $(2, 5)$ has', ['$x$-intercept 5', 'no $x$-intercept and $y$-intercept 5', '$y$-intercept 3', 'slope 1'], 'B',
    ['Step 1: same $y$-values → horizontal line $y = 5$.', 'Step 2: it never meets the $x$-axis; it meets the $y$-axis at 5.'],
    'Horizontal lines (except $y = 0$) have no $x$-intercept.', [('Line through $(-4, 3)$ and $(-4, 7)$?', '$x = -4$: $x$-intercept $-4$, no $y$-intercept.')])
d.S(71, 'Find both intercepts of the line through $(1, -2)$ and $(-2, 1)$.', 'both $-1$',
    ['Step 1: $m = \\frac{1 + 2}{-2 - 1} = -1$.', 'Step 2: $-2 = -1 + b \\Rightarrow b = -1$, so $y = -x - 1$.', 'Step 3: $y = 0 \\Rightarrow x = -1$.'],
    'Get the equation first, then put $x = 0$ and $y = 0$.', [('Intercepts of the line through $(-2, -6)$ and $(5, 8)$?', '$y = 2x - 2$: $x$-int 1, $y$-int $-2$.')])

e = QSet('3.5 Practice — systems of equations', 's35')
e.S(76, 'Solve by substitution: $4x + y = 8$ and $5x - 2y = 23$.', '$(3, -4)$',
    ['Step 1: $y = 8 - 4x$.', 'Step 2: $5x - 2(8 - 4x) = 23 \\Rightarrow 13x - 16 = 23 \\Rightarrow x = 3$.', 'Step 3: $y = 8 - 12 = -4$.'],
    'Pick the variable with coefficient 1.', [('Solve $3x + 4y = 2$, $x - y = 17$.', '$(10, -7)$.')])
e.S(76, 'Solve by elimination: $2x + 3y = 6$ and $8x = 3y + 9$.', '$(1.5, 1)$',
    ['Step 1: rewrite the second: $8x - 3y = 9$.', 'Step 2: add: $10x = 15$, $x = 1.5$.', 'Step 3: $3 + 3y = 6$, $y = 1$.'],
    'Line up $x$, $y$ and numbers before adding.', [('Solve $x + y = 5$ and $x - y = 1$.', '$(3, 2)$.')])
e.S(77, 'The sum of two numbers is 17 and their difference is 5. Find them.', '11 and 6',
    ['Step 1: $x + y = 17$, $x - y = 5$.', 'Step 2: add: $2x = 22$, $x = 11$; $y = 6$.'],
    'Sum and difference → add the equations.', [('Sum 7, difference 3?', '5 and 2.')])
e.S(77, 'Ahmed has 27 coins, all 25-cent and 50-cent, worth 9.25 Nakfa. How many of each?', '17 of 25-cent, 10 of 50-cent',
    ['Step 1: $q + h = 27$ and $25q + 50h = 925$ (cents) → $q + 2h = 37$.', 'Step 2: subtract: $h = 10$.', 'Step 3: $q = 17$. Check $17 \\times 25 + 10 \\times 50 = 425 + 500 = 925$ (correct).'],
    'Change money to cents to avoid decimals.', [('Tickets: adults 10 Nakfa, children 5; 400 people paid 3000 Nakfa. How many adults?', '200 adults, 200 children.')])
e.S(77, 'A father\'s age is 5 more than twice his daughter\'s. In 5 years he will be twice her age. How old is the daughter now?', 'cannot be found — the two facts give the same equation',
    ['Step 1: $f = 2d + 5$.', 'Step 2: in 5 years: $f + 5 = 2(d + 5)$.', 'Step 3: substitute: $2d + 10 = 2d + 10$ — always true!', 'Step 4: the two conditions say the same thing, so the system has infinitely many solutions; the textbook question cannot fix one age.'],
    'When the variables cancel and leave a true statement, the equations are the same line.', [('What happens if the algebra ends with $0 = 5$?', 'No solution — parallel lines.')])
e.M(80, 'How many solutions has $y = 3x - 1$, $y = 3x + 3$?', ['one', 'none', 'two', 'infinitely many'], 'B',
    ['Step 1: both slopes are 3 → parallel or the same line.', 'Step 2: intercepts $-1$ and 3 differ → parallel → no solution.'],
    'Compare $m$ first, then $b$.', [('$m + 2n = 1$ and $4n + 2m = 2$?', 'Infinitely many (same line).')])
e.S(81, 'Awet is 3 years older than Danait and the sum of their ages is 27. How old are they?', 'Awet 15, Danait 12',
    ['Step 1: $a = d + 3$ and $a + d = 27$.', 'Step 2: $2d + 3 = 27 \\Rightarrow d = 12$, $a = 15$.'],
    'One variable is already in terms of the other → substitution.', [('A pool\'s length is twice its width; perimeter 42 m. Dimensions?', '7 m by 14 m.')])

QS = a.items + b.items + c.items + d.items + e.items

GLOSSARY = [
    ('Linear function', 'A function $y = mx + b$; its graph is a straight line.', 52),
    ('Collinear points', 'Points that lie on one straight line.', 52),
    ('Half-plane', 'All points on one side of a line: the graph of a linear inequality.', 59),
    ('Boundary line', 'The line $Ax + By = C$ that separates the two half-planes; dashed for < or >.', 59),
    ('Slope', 'Rise ÷ run = $\\frac{y_2 - y_1}{x_2 - x_1}$; the steepness of a line.', 63),
    ('x-intercept', 'The $x$-coordinate where a line crosses the $x$-axis ($y = 0$).', 68),
    ('y-intercept', 'The $y$-coordinate where a line crosses the $y$-axis ($x = 0$); $b$ in $y = mx + b$.', 68),
    ('System of linear equations', 'Two (or more) linear equations to be solved together.', 72),
]
TIPS = [
    ('Slope = (y₂ − y₁) ÷ (x₂ − x₁); keep the same order on top and bottom.', 63),
    ('Inequality graphs: < or > dashed, ≤ or ≥ solid; test (0, 0) to choose the side.', 59),
    ('Systems: different slopes → one solution; parallel → none; same line → infinitely many.', 80),
]
IDEAS = [('lin', 'Linear or not?', 'l3_1', 'math9-u3-md-lin-t'), ('bound', 'Boundary and shading', 'l3_2', 'math9-u3-md-bound-t'),
         ('slope', 'Slope summary', 'l3_3', 'math9-u3-md-slope-t'), ('eqn', 'Equation of a line', 'l3_4', 'math9-u3-md-eqn-t'),
         ('sys', 'Choosing a method', 'l3_5', 'math9-u3-md-sys-t')]
