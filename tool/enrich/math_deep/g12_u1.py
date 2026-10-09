r"""Grade 12 Unit 1 — Sequence and Series (pp. 1-39)."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY

UID = 'math12-u1'
set_unit(UID)
LB, LG = '#dbe7f3', '#d6ece6'


# ------------------------------------------------------------------ figures
def f_dots():
    p = Plot(0, 7, 0, 10, unit=40, uy=22, every=1, yevery=2, gstep=1, xlab='n', ylab='a')
    p.g('k1 k2 k3')
    for n in range(1, 7):
        p.dot(p.X(n), p.Y(8 / (2 * n - 1)), RED, 4.2)
    p.text(p.X(1.2), p.Y(8) + 4, '8', 11, RED, 'start').text(p.X(2.2), p.Y(8 / 3) + 4, '8/3', 11, RED, 'start')
    p.end()
    p.g('k2 k3').seg((1, 3), (6, 8), BLUE, 1.4, dash=True)
    for n in range(1, 7):
        p.dot(p.X(n), p.Y(n + 2), BLUE, 3.6)
    p.text(p.X(6.15), p.Y(8) + 4, 'AP', 12, BLUE, 'start').end()
    p.g('k3')
    for n in range(1, 6):
        p.dot(p.X(n), p.Y(0.5 * 2 ** (n - 1)), GREEN, 3.6)
    p.text(p.X(5) - 10, p.Y(8) + 4, 'GP', 12, GREEN, 'end').end()
    return p


def f_pairs():
    n, s = 5, 26
    f = Fig(330, 210)
    x0, y0 = 30, 185
    f.g('k1 k2 k3')
    for i in range(n):
        for j in range(i + 1):
            f.rect(x0 + i * s, y0 - (j + 1) * s, s, s, BLUE, 1.2, LB)
    f.end()
    f.g('k2 k3')
    for i in range(n):
        for j in range(n - i):
            f.rect(x0 + i * s, y0 - (n + 1 - j) * s, s, s, GREEN, 1.2, LG)
    f.end()
    f.g('k3').text(x0 + n * s / 2, y0 + 18, 'n = 5 columns', 12, INK)
    f.text(x0 + n * s + 14, y0 - (n + 1) * s / 2, 'n + 1 = 6 rows', 12, INK, 'start')
    f.text(x0 + n * s + 14, y0 - (n + 1) * s / 2 + 24, '2S = 5 x 6', 13, RED, 'start')
    f.text(x0 + n * s + 14, y0 - (n + 1) * s / 2 + 46, 'S = 15', 13, RED, 'start').end()
    return f


def f_ball():
    f = Fig(340, 190)
    g, sc = 170, 24
    f.line(10, g, 330, g, INK, 2)
    hs = [6, 4, 8 / 3, 16 / 9, 32 / 27, 64 / 81]
    x = 30
    f.line(x, g - hs[0] * sc, x, g, RED, 2.2).dot(x, g - hs[0] * sc, RED, 4)
    f.text(x + 8, g - hs[0] * sc + 4, '6 m', 12, RED, 'start')
    for i, h in enumerate(hs[1:]):
        w = 26 + 28 * h / 4 * 2
        a, b = x, x + w
        d = f'M{a} {g} Q{(a + b) / 2} {g - 2 * h * sc} {b} {g}'
        f.path(d, BLUE if i % 2 == 0 else GREEN, 2)
        if i < 3:
            f.text((a + b) / 2, g - h * sc - 8, ['4', '8/3', '16/9'][i], 11.5, INK)
        x = b
    f.text(250, 40, 'falls: 6 + 4 + 8/3 + ... = 18', 12, RED)
    f.text(250, 60, 'rises: 4 + 8/3 + ... = 12', 12, BLUE)
    return f


def f_halves():
    f = Fig(330, 210)
    x, y, W, H = 20, 10, 190, 190
    f.rect(x, y, W, H, INK, 2)
    cols = ['#dbe7f3', '#d6ece6', '#f6dcd5', '#ECE6F5', '#FCEFD9', '#dbe7f3', '#d6ece6']
    labs = ['1/2', '1/4', '1/8', '1/16', '', '', '']
    cx, cy, w, h = x, y, W, H
    keys = ['k1 k2 k3', 'k2 k3', 'k2 k3', 'k3', 'k3', 'k3', 'k3']
    for i in range(7):
        f.g(keys[i])
        if i % 2 == 0:
            f.rect(cx, cy, w / 2, h, INK, 1.2, cols[i])
            if labs[i]:
                f.text(cx + w / 4, cy + h / 2 + 5, labs[i], 14 - i, INK)
            cx += w / 2
            w /= 2
        else:
            f.rect(cx, cy, w, h / 2, INK, 1.2, cols[i])
            if labs[i]:
                f.text(cx + w / 2, cy + h / 4 + 5, labs[i], 14 - i, INK)
            cy += h / 2
            h /= 2
        f.end()
    f.g('k3').text(270, 90, 'total area', 12, INK).text(270, 110, '= 1 whole square', 12, RED).end()
    return f


def f_nested():
    f = Fig(340, 220)
    c, s = (110, 110), 100
    pts = [(c[0] - s, c[1] - s), (c[0] + s, c[1] - s), (c[0] + s, c[1] + s), (c[0] - s, c[1] + s)]
    cols = [BLUE, GREEN, RED, PURPLE, ORANGE]
    labs = ['4 m²', '2 m²', '1 m²', '1/2 m²', '1/4 m²']
    for k in range(5):
        f.poly(pts, cols[k], 1.8, '#dbe7f3' if k == 0 else 'none')
        f.text(232, 40 + 26 * k, labs[k], 12.5, cols[k], 'start')
        pts = [((pts[i][0] + pts[(i + 1) % 4][0]) / 2, (pts[i][1] + pts[(i + 1) % 4][1]) / 2) for i in range(4)]
    f.text(232, 190, 'sum = 8 m²', 13, INK, 'start')
    return f


DIAGRAMS = {
    'dots': (f_dots(), 'Sequences are graphed as separate dots', 5),
    'pairs': (f_pairs(), 'Why S = n(a1 + an)/2: two copies make a rectangle', 15),
    'ball': (f_ball(), 'Example 1.26: a ball rebounding 2/3 of its height', 35),
    'halves': (f_halves(), '1/2 + 1/4 + 1/8 + ... fills one whole square', 35),
    'nested': (f_nested(), 'Review Q15: each square has half the area of the one before', 39),
}

# ------------------------------------------------------------------ 1.1
L1 = [
    T('=math12-u1-c01', '1.1 Sequences: terms and formulas', 3,
      'A **sequence** is a function whose domain is the positive integers $1, 2, 3, \\dots$. Its values $a_1, a_2, a_3, \\dots$ are the **terms**; $a_n$ is the **$n$th term** (general term). If the domain is only $1, 2, \\dots, n$ the sequence is **finite**.',
      '**Two ways to give a sequence:**',
      '- **explicit formula:** $a_n$ is computed straight from $n$, e.g. $a_n = 4n + 2$ gives $6, 10, 14, \\dots$;',
      '- **recursive formula:** the first term(s) plus a rule using earlier terms, e.g. $a_1 = 2$, $a_n = a_{n-1} + 3$.',
      '**Finding a formula from terms (Example 1.2):** $6, 10, 14, 18, \\dots$ goes up by 4 each time, so $a_n = 6 + (n - 1)4 = 4n + 2$. Check: $a_3 = 14$. (The book\'s line for $a_5$ repeats "18 − 14"; $a_5 = 22$.)'),
    ST('dots', 'Graphing a sequence (Example 1.3)', 5, 'dots',
       [('Because $n$ takes only whole values, the graph is a set of **separate dots**, not a curve. Red: $a_n = \\frac{8}{2n - 1}$: $8, \\frac{8}{3}, \\frac{8}{5}, \\frac{8}{7}, \\dots$ falling toward 0.', 'k1'),
        ('Blue: the AP $3, 4, 5, \\dots$ ($a_n = n + 2$) — its dots lie on a straight line.', 'k2'),
        ('Green: the GP $\\frac{1}{2}, 1, 2, 4, 8$ — its dots bend upward faster and faster.', 'k3')]),
    WK('ex11', 'Worked example: Example 1.1 (T cells)', 1,
       'A person has 1025 T cells and loses 75 per year. When does the count first fall to 200 or below?',
       ['After $n$ years: $a_n = 1025 - 75n$.', 'Solve $1025 - 75n \\le 200$: $-75n \\le -825$.', 'Divide by $-75$ and **reverse the sign**: $n \\ge 11$.'],
       'after 11 years (check: $1025 - 825 = 200$)'),
    T('rec-t', 'Recursive sequences and factorials', 6,
      '**Example 1.4(a):** $a_1 = 3$, $a_n = n + a_{n-1}$: $a_2 = 2 + 3 = 5$, $a_3 = 3 + 5 = 8$, $a_4 = 12$, $a_5 = 17$.',
      '**Example 1.4(b) (Fibonacci):** $a_1 = a_2 = 1$, $a_n = a_{n-2} + a_{n-1}$: $1, 1, 2, 3, 5, 8, \\dots$',
      '**Factorial:** $n! = 1 \\times 2 \\times 3 \\times \\dots \\times n$, and $0! = 1$. So $5! = 120$, $7! = 5040$.',
      '**Key trick for simplifying:** $n! = n \\times (n - 1)!$, so $\\frac{(n + 1)!}{n!} = n + 1$ and $\\frac{8!}{4!} = 8 \\times 7 \\times 6 \\times 5 = 1680$.'),
    TB('fact-tb', 'Factorials to know', 6, ['$n$', '$n!$', 'built as'],
       [['0', '1', 'by definition'], ['1', '1', '1'], ['2', '2', '2 × 1!'], ['3', '6', '3 × 2!'], ['4', '24', '4 × 3!'], ['5', '120', '5 × 4!'], ['6', '720', '6 × 5!'], ['7', '5040', '7 × 6!']]),
    'math12-u1-tblE1', 'math12-u1-chkE1', 'math12-u1-chkE2', 'math12-u1-chk74', 'math12-u1-wrk1', 'math12-u1-chk75', 'math12-u1-wrk2', 'math12-u1-chk76', 'math12-u1-wrk3',
]

# ------------------------------------------------------------------ 1.2
L2 = [
    'math12-u1-c02',
    T('ap-why', 'Where the AP formulas come from', 9,
      '$A_1$, $A_1 + d$, $A_1 + 2d$, …: to reach term $n$ you add $d$ exactly $n - 1$ times, so $$A_n = A_1 + (n - 1)d.$$',
      '**Two unknowns, two facts:** if you know two terms, write each as $A_1 + (k - 1)d$ and solve the pair of equations (Example 1.10: $A_1 + 4d = 44$ and $A_1 + 16d = 152$ give $d = 9$, $A_1 = 8$).',
      '**Arithmetic mean** of $a$ and $b$: $x - a = b - x$, so $x = \\frac{a + b}{2}$.'),
    WK('ex16', 'Worked example: Example 1.6 (corrected)', 10,
       'An AP has $A_1 = 4$ and $A_4 = 19$. Find $d$, $A_n$ and $A_8$, $A_{10}$, $A_{14}$.',
       ['$A_4 = A_1 + 3d$: $4 + 3d = 19$, so $d = 5$.', '$A_n = 4 + (n - 1)5 = 5n - 1$.', '$A_8 = 39$, $A_{10} = 50 - 1 = 49$, $A_{14} = 69$.'],
       '$d = 5$, $A_n = 5n - 1$; 39, 49, 69 (the book writes "$5(10) - 1 = 10 - 1$"; it is $50 - 1$)'),
    ST('pairs', 'Gauss\'s pairing trick for $S_n$', 15, 'pairs',
       [('$1 + 2 + 3 + 4 + 5$ drawn as columns of blocks: a staircase.', 'k1'),
        ('Put a second copy upside down on top ($5 + 4 + 3 + 2 + 1$): every column now has $1 + 5 = 6$ blocks.', 'k2'),
        ('Two copies make a $5 \\times 6$ rectangle, so $2S = 30$ and $S = 15$. In general $2S_n = n(A_1 + A_n)$: $$S_n = \\frac{n}{2}(A_1 + A_n) = \\frac{n}{2}\\left(2A_1 + (n - 1)d\\right).$$', 'k3')]),
    TB('ap-tb', 'Which sum formula?', 16, ['You know', 'Use'],
       [['first and last term', '$S_n = \\frac{n}{2}(A_1 + A_n)$'], ['first term and $d$', '$S_n = \\frac{n}{2}(2A_1 + (n - 1)d)$'], ['first, last and $d$ (find $n$)', '$n = \\frac{A_n - A_1}{d} + 1$, then the first formula']]),
    WK('ex110', 'Worked example: Example 1.10', 16,
       'In an AP, $A_5 = 44$ and $A_{17} = 152$. Find $S_{20}$.',
       ['Subtract: $(A_1 + 16d) - (A_1 + 4d) = 108$, so $12d = 108$ and $d = 9$.', '$A_1 = 44 - 36 = 8$.', '$S_{20} = 10(2 \\times 8 + 19 \\times 9) = 10(16 + 171)$.'],
       '$S_{20} = 1870$'),
    WK('ex111', 'Worked example: sum of odd numbers (Example 1.11)', 17,
       'Show that $1 + 3 + 5 + \\dots + (2n - 1) = n^2$.',
       ['AP with $A_1 = 1$, $d = 2$, so $A_n = 2n - 1$.', '$S_n = \\frac{n}{2}(1 + 2n - 1) = \\frac{n}{2} \\times 2n = n^2$.'],
       '$n^2$ (the book\'s line says "even integers"; it means odd)'),
    WK('ex112', 'Worked example: a falling object (Example 1.12)', 17,
       'An object falls 4.9 m in the 1st second, 14.7 m in the 2nd, 24.5 m in the 3rd, … How far in 10 seconds?',
       ['Differences are all 9.8: AP with $A_1 = 4.9$, $d = 9.8$.', '$S_{10} = 5(9.8 + 9 \\times 9.8) = 5 \\times 98$.'],
       '490 m (the same as $\\frac{1}{2}gt^2 = 4.9 \\times 100$)'),
    'math12-u1-c06', 'math12-u1-c07', 'math12-u1-c08', 'math12-u1-chk77', 'math12-u1-wrk4', 'math12-u1-chk78', 'math12-u1-wrk5', 'math12-u1-chk79', 'math12-u1-wrk6', 'math12-u1-chk80', 'math12-u1-wrk7',
]

# ------------------------------------------------------------------ 1.3
L3 = [
    'math12-u1-c03',
    T('gp-why', 'Where the GP formulas come from', 20,
      '$G_1$, $G_1 r$, $G_1 r^2$, …: term $n$ has been multiplied by $r$ exactly $n - 1$ times, so $G_n = G_1 r^{n-1}$.',
      '**Sum — the "multiply and subtract" trick:** $S_n = G_1 + G_1 r + \\dots + G_1 r^{n-1}$ and $rS_n = G_1 r + \\dots + G_1 r^n$. Subtracting, almost everything cancels: $S_n - rS_n = G_1 - G_1 r^n$, so $$S_n = \\frac{G_1(1 - r^n)}{1 - r} \\quad (r \\ne 1), \\qquad S_n = nG_1 \\;(r = 1).$$',
      '**Geometric mean** of positive $a$ and $b$: $\\frac{x}{a} = \\frac{b}{x}$, so $x^2 = ab$ and $x = \\sqrt{ab}$.'),
    TB('apgp-tb', 'AP and GP side by side', 20, ['', 'Arithmetic (AP)', 'Geometric (GP)'],
       [['next term', 'add $d$', 'multiply by $r$'], ['test', 'equal differences', 'equal ratios'], ['$n$th term', '$A_1 + (n - 1)d$', '$G_1 r^{n-1}$'],
        ['sum of $n$ terms', '$\\frac{n}{2}(A_1 + A_n)$', '$\\frac{G_1(1 - r^n)}{1 - r}$'], ['mean of $a$, $b$', '$\\frac{a + b}{2}$', '$\\sqrt{ab}$'], ['graph of terms', 'dots on a line', 'dots on an exponential curve']]),
    WK('ex114', 'Worked example: students per computer (Example 1.14)', 21,
       'Students per computer: 128 in 2008, 64 in 2009, … (a GP). Formula? Value in 2011? When is it 1?',
       ['$r = \\frac{64}{128} = \\frac{1}{2}$, so $G_n = 128\\left(\\frac{1}{2}\\right)^{n-1} = 2^7 \\cdot 2^{1-n} = 2^{8-n}$.', '2011 is $n = 4$: $2^4 = 16$.', '$2^{8-n} = 1 = 2^0$ gives $n = 8$, the year 2015.'],
       '$G_n = 2^{8-n}$; 16; in 2015'),
    WK('ex115', 'Worked example: Example 1.15 (corrected)', 22,
       '(a) Geometric mean of 8 and 12. (b) The GM of two numbers is 10 and one is $10\\sqrt{2}$. Find the other.',
       ['(a) $\\sqrt{8 \\times 12} = \\sqrt{96} = 4\\sqrt{6}$. (The book starts "GM of 6 and 72" by mistake.)', '(b) $x \\times 10\\sqrt{2} = 10^2 = 100$ (the book prints "= 10").', '$x = \\frac{100}{10\\sqrt{2}} = \\frac{10}{\\sqrt{2}} = 5\\sqrt{2}$.'],
       '$4\\sqrt{6}$; $5\\sqrt{2}$'),
    WK('ex116', 'Worked example: two terms given (Example 1.16)', 27,
       'In a GP, $G_3 = 6$ and $G_5 = \\frac{3}{2}$. Find $G_1$, $r$ and $S_{10}$.',
       ['Divide: $\\frac{G_5}{G_3} = r^2 = \\frac{1}{4}$, so $r = \\frac{1}{2}$ or $r = -\\frac{1}{2}$.', '$G_1 = \\frac{6}{r^2} = 24$ in both cases.',
        '$r = \\frac{1}{2}$: $S_{10} = \\frac{24(1 - 2^{-10})}{0.5} = \\frac{3069}{64}$.', '$r = -\\frac{1}{2}$ (signs alternate): $S_{10} = \\frac{24(1 - 2^{-10})}{1.5} = \\frac{1023}{64}$.'],
       '$G_1 = 24$; $S_{10} = \\frac{3069}{64} \\approx 47.95$ or $\\frac{1023}{64} \\approx 15.98$'),
    WK('ex117', 'Worked example: bouncing ball, 7 hits (Example 1.17, corrected)', 28,
       'Dropped from 90 cm, each bounce rises $\\frac{2}{3}$ of the previous height. Distance travelled when it hits the ground the 7th time?',
       ['Falls: $90 + 60 + 40 + \\dots$, **7** falls: $S_7 = \\frac{90(1 - (2/3)^7)}{1/3} = 270 \\times \\frac{2059}{2187} \\approx 254.2$.',
        'Rises: $60 + 40 + \\dots$, only **6** rises (it has not risen after the 7th hit): $\\frac{60(1 - (2/3)^6)}{1/3} = 180 \\times \\frac{665}{729} \\approx 164.2$.', 'Total $254.2 + 164.2$.'],
       '418.4 cm (the book writes $(2/3)^7$ in the rises formula; the value 164.2 comes from $(2/3)^6$)'),
    'math12-u1-c09', 'math12-u1-c10', 'math12-u1-c11', 'math12-u1-c12', 'math12-u1-pc31', 'math12-u1-chk81', 'math12-u1-wrk8', 'math12-u1-chk82', 'math12-u1-wrk9',
]

# ------------------------------------------------------------------ 1.4
L4 = [
    'math12-u1-c04',
    T('hp-t', 'Working with harmonic progressions', 31,
      '**Rule of thumb: flip, work in the AP, flip back.**',
      '**Example 1.18 (corrected):** $\\frac{1}{2}, \\frac{1}{4}, \\frac{1}{6}, \\dots$ is an HP because $2, 4, 6, \\dots$ is an AP. (The book writes $\\frac{1}{8}$ and "2, 4, 8 is an AP" — but 2, 4, 8 is a GP, so $\\frac{1}{2}, \\frac{1}{4}, \\frac{1}{8}$ is **not** an HP.)',
      '**Example 1.20:** HP with first term $\\frac{1}{2}$ and fifth term $\\frac{1}{22}$: AP $2, \\dots, 22$ with $4d = 20$, $d = 5$: $2, 7, 12, 17, 22$, so the HP is $\\frac{1}{2}, \\frac{1}{7}, \\frac{1}{12}, \\frac{1}{17}, \\frac{1}{22}$.',
      '**Harmonic mean (Example 1.21):** $\\frac{1}{m} = \\frac{1}{2}\\left(\\frac{1}{a} + \\frac{1}{b}\\right)$ gives $m = \\frac{2ab}{a + b}$.'),
    TB('means-tb', 'Three means of 4 and 16', 30, ['Mean', 'Formula', 'Value'],
       [['arithmetic', '$\\frac{a + b}{2}$', '10'], ['geometric', '$\\sqrt{ab}$', '8'], ['harmonic', '$\\frac{2ab}{a + b}$', '6.4']]),
    RM('means-rm', 'AM ≥ GM ≥ HM', 30, 'For positive numbers the arithmetic mean is the biggest and the harmonic mean the smallest; they are equal only when $a = b$. Also $AM \\times HM = GM^2$: $10 \\times 6.4 = 64 = 8^2$.'),
    'math12-u1-pc41', 'math12-u1-pc42', 'math12-u1-xw4', 'math12-u1-chk83', 'math12-u1-wrk10',
]

# ------------------------------------------------------------------ 1.5
L5 = [
    T('=math12-u1-c05', '1.5 Series and sigma notation', 32,
      'A **series** is the sum of the terms of a sequence: $a_1 + a_2 + a_3 + \\dots$. It is finite or infinite like the sequence.',
      '**Sigma notation:** $\\sum_{k=1}^{n} a_k = a_1 + a_2 + \\dots + a_n$. The letter $k$ is the counter; it starts at the bottom number and goes up by 1 to the top number. For example $\\sum_{n=1}^{10} 2n = 2 + 4 + \\dots + 20 = 110$.',
      'An infinite series **converges** if its partial sums $S_1, S_2, S_3, \\dots$ settle down to a finite number (its sum); otherwise it **diverges**. $2 + 4 + 8 + \\dots$ diverges; $\\frac{2}{3} + \\frac{4}{9} + \\frac{8}{27} + \\dots$ converges to 2.'),
    T('inf-t', 'Infinite geometric series', 34,
      'In $S_n = \\frac{G_1(1 - r^n)}{1 - r}$, if $|r| < 1$ the power $r^n$ shrinks to 0 as $n$ grows, so $$S_\\infty = \\frac{G_1}{1 - r} \\qquad (|r| < 1).$$',
      'If $|r| \\ge 1$ the terms do not shrink and the series diverges (e.g. $1 + 1 + 1 + \\dots$, and $1 - 1 + 1 - \\dots$ which keeps jumping between 1 and 0).',
      '**Example 1.25:** $\\sum_{n=1}^{\\infty} 2\\left(\\frac{3}{4}\\right)^{n-1} = \\frac{2}{1 - 3/4} = 8$.',
      '**Repeating decimals:** $0.\\overline{7} = \\frac{7}{10} + \\frac{7}{100} + \\dots = \\frac{0.7}{0.9} = \\frac{7}{9}$; $1.\\overline{81} = 1 + \\frac{0.81}{0.99} = 1 + \\frac{9}{11} = \\frac{20}{11}$.'),
    ST('halves', 'Seeing $\\frac{1}{2} + \\frac{1}{4} + \\frac{1}{8} + \\dots = 1$ (Example 1.24)', 35, 'halves',
       [('Shade half of a unit square.', 'k1'),
        ('Then half of what is left ($\\frac{1}{4}$), then half of that ($\\frac{1}{8}$)…', 'k2'),
        ('The pieces fill the whole square: $S_\\infty = \\frac{1/2}{1 - 1/2} = 1$.', 'k3')]),
    DG('ball', 'Example 1.26: total distance of a bouncing ball', 35, 'ball',
       'Dropped from 6 m, rebounds $\\frac{2}{3}$ each time. Falls $F = 6 + 4 + \\frac{8}{3} + \\dots = \\frac{6}{1 - 2/3} = 18$; rises $R = 4 + \\frac{8}{3} + \\dots = \\frac{4}{1/3} = 12$. Total **30 m**. Shortcut: total $= $ first drop $+ 2 \\times$ (all rises).'),
    TB('conv-tb', 'Converge or diverge?', 36, ['Series', '$r$', 'Result'],
       [['$16 + 8 + 4 + \\dots$', '$\\frac{1}{2}$', 'converges to 32'], ['$0.7 + 0.07 + \\dots$', '$0.1$', 'converges to $\\frac{7}{9}$'],
        ['$2 + 6 + 18 + \\dots$', '3', 'diverges'], ['$1 + 1 + 1 + \\dots$', '1', 'diverges'], ['$1 - 1 + 1 - \\dots$', '$-1$', 'diverges']]),
    DG('nested', 'Review Q15: squares inside squares', 39, 'nested',
       'Joining midpoints of a 2 m square gives a square of half the area. Areas: $4 + 2 + 1 + \\dots = \\frac{4}{1 - 1/2} = 8$ m².'),
    'math12-u1-pc51', 'math12-u1-pc52', 'math12-u1-pc53',
    RM('summary-t', 'Unit summary', 39,
       'AP: $A_n = A_1 + (n - 1)d$, $S_n = \\frac{n}{2}(A_1 + A_n)$; AM $= \\frac{a + b}{2}$.',
       'GP: $G_n = G_1 r^{n-1}$, $S_n = \\frac{G_1(1 - r^n)}{1 - r}$; GM $= \\sqrt{ab}$.',
       'HP: reciprocals form an AP; HM $= \\frac{2ab}{a + b}$.',
       'Infinite GP: $S_\\infty = \\frac{G_1}{1 - r}$ only when $|r| < 1$.'),
]

LESSONS = {'math12-u1-l1-1': L1, 'math12-u1-l1-2': L2, 'math12-u1-l1-3': L3, 'math12-u1-l1-4': L4, 'math12-u1-l1-5': L5}

# ------------------------------------------------------------------ practice
a = QSet('1.1 Practice — sequences', 's11')
a.S(7, 'Exercise 1.1 Q1: first five terms of (a) $a_n = 4n - 1$ (b) $a_n = n^2 - 3n + 1$ (c) $a_n = 3^n + 1$ (d) $a_n = \\sqrt{n}$ (e) $a_n = \\frac{2n + 1}{n}$.',
    '(a) 3, 7, 11, 15, 19 (b) −1, −1, 1, 5, 11 (c) 4, 10, 28, 82, 244 (d) 1, √2, √3, 2, √5 (e) 3, 5/2, 7/3, 9/4, 11/5',
    ['Step 1: put $n = 1, 2, 3, 4, 5$ into each formula.', 'Step 2: e.g. (b) $n = 4$: $16 - 12 + 1 = 5$.'], 'Make a small table of $n$ and $a_n$.', [('$a_n = 2^n - n$?', '1, 2, 5, 12, 27.')])
a.S(7, 'Exercise 1.1 Q2: find (a) $a_7$ for $a_n = (-1)^n(2n + 3)$ (b) $a_{11}$ for $a_n = \\frac{4n}{2n^2 - 3}$ (c) $a_6$ for $a_n = \\frac{n}{n!}$ (d) $a_{25}$ for $a_n = 1 + \\log 10^n$.', '−17; 44/239; 1/120; 26',
    ['Step 1: $(-1)^7 = -1$, $2(7) + 3 = 17$.', 'Step 2: $\\frac{44}{242 - 3}$.', 'Step 3: $\\frac{6}{720}$.', 'Step 4: $\\log 10^{25} = 25$.'], 'Odd power of $-1$ is $-1$.', [('$a_8$ in (a)?', '19.')])
a.S(7, 'Exercise 1.1 Q3: next three terms: (a) 8, 5, 2, −1, −4 (b) 3, −6, 12, −24, 48 (c) −1, 2, 7, 14, 23 (d) $\\frac{1}{3}, -\\frac{2}{9}, \\frac{1}{9}, -\\frac{4}{81}$.',
    '(a) −7, −10, −13 (b) −96, 192, −384 (c) 34, 47, 62 (d) 5/243, −2/243, 7/2187',
    ['Step 1: (a) subtract 3; (b) multiply by −2.', 'Step 2: (c) differences 3, 5, 7, 9, so next 11, 13, 15.', 'Step 3: (d) $a_n = (-1)^{n+1}\\frac{n}{3^n}$ ($\\frac{1}{9} = \\frac{3}{27}$).'],
    'Look at differences, then ratios.', [('1, 4, 9, 16?', '25, 36, 49.')])
a.S(8, 'Exercise 1.1 Q4: general formulas for the sequences in Q3.', '(a) $11 - 3n$ (b) $3(-2)^{n-1}$ (c) $n^2 - 2$ (d) $(-1)^{n+1}\\frac{n}{3^n}$',
    ['Step 1: (a) AP: $8 + (n - 1)(-3)$.', 'Step 2: (b) GP with $r = -2$.', 'Step 3: (c) each term is 2 less than $n^2$.'], 'Check your formula with $n = 1$ and $n = 2$.', [('2, 5, 10, 17?', '$n^2 + 1$.')])
a.S(8, 'Exercise 1.1 Q5: first five terms: (a) $a_1 = 2$, $a_n = 5 + a_{n-1}$ (b) $a_1 = 60$, $a_n = 0.5a_{n-1} - 2$ (c) $a_1 = 1$, $a_2 = 2$, $a_n = a_{n-2} + 2a_{n-1} - 3$.',
    '(a) 2, 7, 12, 17, 22 (b) 60, 28, 12, 4, 0 (c) 1, 2, 2, 3, 5',
    ['Step 1: (a) keep adding 5 (the book prints $a_{n-n}$; it means $a_{n-1}$).', 'Step 2: (b) $0.5(60) - 2 = 28$, $0.5(28) - 2 = 12$, …', 'Step 3: (c) $a_3 = 1 + 4 - 3 = 2$, $a_4 = 2 + 4 - 3 = 3$, $a_5 = 2 + 6 - 3 = 5$.'],
    'Each new term uses the ones just found.', [('$a_1 = 1$, $a_n = 2a_{n-1} + 1$?', '1, 3, 7, 15, 31.')])
a.S(8, 'Exercise 1.1 Q6: simplify (a) $\\frac{8!}{4!}$ (b) $\\frac{9!}{7!\\,2!}$ (c) $\\frac{(n + 1)!}{n!}$ (d) $\\frac{(n + 1)!}{(n + 3)!}$.', '1680; 36; $n + 1$; $\\frac{1}{(n + 2)(n + 3)}$',
    ['Step 1: $8 \\times 7 \\times 6 \\times 5$.', 'Step 2: $\\frac{9 \\times 8}{2}$.', 'Step 3: $(n + 1)! = (n + 1) \\cdot n!$.', 'Step 4: $(n + 3)! = (n + 3)(n + 2)(n + 1)!$.'], 'Write the bigger factorial until the smaller one appears.', [('$\\frac{10!}{8!}$?', '90.')])
a.S(8, 'Exercise 1.1 Q7: population (thousands) $a_n = n^2 + 2n + 204$, $n = 1$ for 1981. (a) 1981, 1982, 1983 (b) last three terms ($n = 28, 29, 30$).', '207, 212, 219; 1044, 1103, 1164',
    ['Step 1: $1 + 2 + 204$, $4 + 4 + 204$, $9 + 6 + 204$.', 'Step 2: $784 + 56 + 204$, $841 + 58 + 204$, $900 + 60 + 204$.'], '2010 is $n = 30$.', [('Year 2000 ($n = 20$)?', '644 thousand.')])
a.S(8, 'Exercise 1.1 Q8: first five terms of $a_n = \\frac{4^n}{n!}$.', '4, 8, 32/3, 32/3, 128/15',
    ['Step 1: $\\frac{4}{1}$, $\\frac{16}{2}$, $\\frac{64}{6}$, $\\frac{256}{24}$, $\\frac{1024}{120}$.'], 'Simplify each fraction.', [('$a_6$?', '$\\frac{4096}{720} = \\frac{256}{45}$.')])

b = QSet('1.2 Practice — arithmetic progressions', 's12')
b.S(13, 'Exercise 1.2 Q1: AP or not? (a) 3, 7, 11, 15 (b) 1, 4, 8, 13 (c) 0.5, 3, 5.5, 8 (d) $\\frac{5}{6}, \\frac{2}{3}, \\frac{1}{2}, \\frac{1}{3}$ (e) 1, 5, 9, 14.', 'AP: (a) d = 4, (c) d = 2.5, (d) d = −1/6; not: (b), (e)',
    ['Step 1: find all differences.', 'Step 2: (b) 3, 4, 5 and (e) 4, 4, 5 are not constant.'], 'Check **every** difference.', [('2, 2.5, 3, 3.5?', 'AP, $d = 0.5$.')])
b.S(13, 'Exercise 1.2 Q2: AP or not? (a) $a_n = -2n + 5$ (b) $a_n = n^2$ (c) $a_n = 5n - 3$ (d) $a_n = 3(2^n)$.', '(a) AP, d = −2 (c) AP, d = 5; (b), (d) not',
    ['Step 1: $a_{n+1} - a_n$ must be a constant.', 'Step 2: for $n^2$ it is $2n + 1$, which changes.'], 'A linear formula $pn + q$ is always an AP with $d = p$.', [('$a_n = 7 - 3n$?', 'AP, $d = -3$.')])
b.S(13, 'Exercise 1.2 Q3: general term: (a) $A_1 = 7$, $d = 8$ (b) $A_1 = 4$, $A_2 = -1$ (c) $A_3 = 11$, $A_7 = 3$ (d) $A_5 = 2$, $d = 3$.', '(a) $8n - 1$ (b) $9 - 5n$ (c) $17 - 2n$ (d) $3n - 13$',
    ['Step 1: (b) $d = -5$.', 'Step 2: (c) $4d = -8$, $d = -2$, $A_1 = 15$.', 'Step 3: (d) $A_1 = 2 - 12 = -10$.'], 'Find $d$ first, then $A_1$.', [('$A_2 = 5$, $A_6 = 17$?', '$3n - 1$.')])
b.S(13, 'Exercise 1.2 Q4–Q5: (4) 36 °F at 5 PM, falling 3 °F every half-hour: when 0 °F? (5) 250 students, +32 a year: after 4 years?', '11 PM; 378',
    ['Step 1: $36 - 3k = 0$, $k = 12$ half-hours = 6 h.', 'Step 2: $250 + 4 \\times 32$.'], 'Count the steps, not the terms.', [('Falling 4 °F per half-hour?', '9:30 PM.')])
b.S(13, 'Exercise 1.2 Q6–Q7: AM of (a) 3.5 and 7 (b) $2 + \\sqrt{2}$ and $2 - \\sqrt{2}$ (c) $9x$ and $5x$ (d) $(a - b)^2$ and $(a + b)^2$. (7) For which $x$ is 2 the AM of $x^2 - 1$ and $2x + 2$?', '5.25; 2; 7x; $a^2 + b^2$; $x = 1$ or $x = -3$',
    ['Step 1: add and halve.', 'Step 2: (d) $\\frac{2a^2 + 2b^2}{2}$.', 'Step 3: $x^2 + 2x + 1 = 4$, $(x + 1)^2 = 4$.'], 'AM = half the sum.', [('AM of 4 and 11?', '7.5.')])
b.S(18, 'Exercise 1.3 Q1: (a) $A_1 = 7$, $d = 2$: $S_{10}$ (b) $A_3 = 10$, $A_7 = -2$: $S_8$ (c) $A_n = 3n + 8$: $S_{11}$ (e) $A_n = -5n + 2$: $S_{12}$.', '160; 44; 286; −366',
    ['Step 1: (a) $5(14 + 18)$.', 'Step 2: (b) $d = -3$, $A_1 = 16$, $S_8 = 4(32 - 21) = 44$.', 'Step 3: (c) $A_1 = 11$, $A_{11} = 41$: $\\frac{11}{2}(52)$.', 'Step 4: (e) $A_1 = -3$, $A_{12} = -58$: $6(-61)$.'], 'With a formula for $A_n$, use first + last.', [('(d) $A_{11} = -3$, $A_{31} = -2$: $S_5$?', '$d = \\frac{1}{20}$, $A_1 = -3.5$, $S_5 = -17$.')])
b.S(18, 'Exercise 1.3 Q2–Q4: (2) sum of integers from −20 to 80 (3) sum of positive multiples of 7 up to 700 (4) $S_{20} = 650$, $d = 3$: first term?', '3030; 35,350; 4',
    ['Step 1: 101 terms: $\\frac{101}{2}(-20 + 80)$.', 'Step 2: 100 terms: $50(7 + 700)$.', 'Step 3: $10(2A_1 + 57) = 650$.'], 'Count terms: last − first, divided by $d$, plus 1.', [('Sum of 1 to 100?', '5050.')])
b.S(18, 'Exercise 1.3 Q5–Q6: (5) 16 teams share 8000 Nakfa in an AP; the last gets 275. First prize? (6) 20 rows: 10, 12, 14, … seats. Total?', '725 Nakfa; 580 seats',
    ['Step 1: $8(A_1 + 275) = 8000$.', 'Step 2: $10(20 + 19 \\times 2)$.'], 'Use whichever sum formula fits the data.', [('30 rows?', '1170 seats.')])
b.S(37, 'Review Q2–Q3: (2) first 8 terms of an AP with $A_1 + A_7 = 40$ and $A_1 A_4 = 160$. (3) Brick rows 60, 58, …, 10: total bricks?', '8, 12, 16, 20, 24, 28, 32, 36; 910',
    ['Step 1: $2A_1 + 6d = 40$ so $A_4 = 20$; $A_1 = 8$, $d = 4$.', 'Step 2: 26 rows: $13(60 + 10)$.'], '$A_1 + A_7 = 2A_4$.', [('Rows 40 down to 10 by 3?', '275.')])
b.M(14, 'In a trapezium the segment joining the midpoints of the legs (Exercise 1.2 Q8) is', ['the AM of the parallel sides', 'the GM of the parallel sides', 'the HM of the parallel sides', 'the longer parallel side'], 'A',
    ['Step 1: the midline $CD = \\frac{AB + EF}{2}$.'], 'Midline = average of the bases.', [('Bases 6 and 10?', 'midline 8.')])
b.TF(16, '$S_n = \\frac{n}{2}(A_1 + A_n)$ works for any AP.', True, ['Step 1: pairing first+last, second+second-last, … always gives equal pair sums.'], 'Gauss\'s trick.', [('For a GP?', 'False.')])

c = QSet('1.3 Practice — geometric progressions', 's13')
c.S(23, 'Exercise 1.4 Q1: GP or not? (a) −11, −16, −21 (b) $\\frac{1}{2}, \\frac{1}{3}, \\frac{2}{9}, \\frac{4}{27}$ (c) $\\frac{1}{25}, \\frac{1}{10}, \\frac{1}{4}, \\frac{5}{8}$ (d) 3, 12, 21, 30 (e) 800, 1360, 2312, 3930.4.', 'GP: (b) r = 2/3 (c) r = 5/2 (e) r = 1.7; not: (a), (d) (they are APs)',
    ['Step 1: divide each term by the one before.', 'Step 2: (a) $\\frac{-16}{-11} \\ne \\frac{-21}{-16}$.'], 'Equal ratios ⇒ GP.', [('5, −10, 20?', 'GP, $r = -2$.')])
c.S(23, 'Exercise 1.4 Q3: general term: (a) $G_1 = 1$, $r = 4$ (b) $G_1 = -81$, $r = \\frac{1}{3}$ (c) $G_1 = 5$, $G_2 = -1$ (d) $G_5 = 6$, $G_7 = \\frac{27}{8}$.', '$4^{n-1}$; $-81(\\frac{1}{3})^{n-1}$; $5(-\\frac{1}{5})^{n-1}$; $r = \\pm\\frac{3}{4}$, $G_n = 6(\\pm\\frac{3}{4})^{n-5}$',
    ['Step 1: (c) $r = -\\frac{1}{5}$.', 'Step 2: (d) $r^2 = \\frac{27}{48} = \\frac{9}{16}$.'], 'Divide two given terms to get a power of $r$.', [('$G_2 = 6$, $G_4 = 54$?', '$r = \\pm 3$, $G_1 = \\pm 2$.')])
c.S(24, 'Exercise 1.4 Q4: 1500 Nakfa at 4% compounded half-yearly. Amount after (a) 1 year (b) 3 years (c) $n$ years (d) 10 years.', '1560.60; 1689.24; $1500(1.02)^{2n}$; 2228.92',
    ['Step 1: 2% per half-year, ratio 1.02.', 'Step 2: $1500(1.02)^2$, $1500(1.02)^6$, $1500(1.02)^{20}$.'], 'Compound interest is a GP.', [('After 5 years?', '1828.49.')])
c.S(24, 'Exercise 1.4 Q5–Q6: (5) population 3.6 M, 4.32 M, 5.184 M, … from 2007: in 2012? (6) E. coli doubles every 20 min: cells after 12 h and 24 h from one cell?', 'about 8,957,952; $2^{36} \\approx 6.87 \\times 10^{10}$ and $2^{72} \\approx 4.7 \\times 10^{21}$',
    ['Step 1: $r = 1.2$; 2012 is the 6th term: $3.6\\text{M} \\times 1.2^5$.', 'Step 2: 3 doublings per hour: 36 and 72 doublings.'], 'Count the number of multiplications.', [('After 3 hours?', '$2^9 = 512$.')])
c.S(24, 'Exercise 1.4 Q7: GM of (a) 3 and 12 (b) 0.6 and 0.8 (c) $3 - \\sqrt{5}$ and $3 + \\sqrt{5}$ (d) $ab^2$ and $ab^4$ (positive).', '6; $\\sqrt{0.48} \\approx 0.69$; 2; $ab^3$',
    ['Step 1: $\\sqrt{36}$.', 'Step 2: (c) $(3 - \\sqrt{5})(3 + \\sqrt{5}) = 4$.', 'Step 3: (d) $\\sqrt{a^2 b^6}$.'], 'Multiply, then square root.', [('GM of 2 and 18?', '6.')])
c.S(29, 'Exercise 1.5 Q1: (a) $G_1 = 3$, $r = 2$: $S_{10}$ (b) $G_2 = 6$, $r = \\frac{1}{4}$: $S_9$ (d) $G_n = 5(2^{n-1})$: $S_{11}$ (e) $G_n = -6(0.9^{n-1})$: $S_{14}$.', '3069; ≈ 32.0; 10,235; ≈ −46.27',
    ['Step 1: $3(2^{10} - 1)$.', 'Step 2: $G_1 = 24$: $\\frac{24(1 - 4^{-9})}{3/4} \\approx 32$.', 'Step 3: $5(2^{11} - 1)$.', 'Step 4: $\\frac{-6(1 - 0.9^{14})}{0.1} = -60(1 - 0.2288)$.'], 'For $r > 1$ use $\\frac{G_1(r^n - 1)}{r - 1}$.', [('$G_1 = 1$, $r = 3$, $S_5$?', '121.')])
c.S(30, 'Exercise 1.5 Q4: 1 cent on day 1, doubling daily, for a 30-day month. Total?', '$2^{30} - 1$ cents ≈ 10.7 million (in whole currency units)',
    ['Step 1: $S_{30} = \\frac{2^{30} - 1}{2 - 1}$.', 'Step 2: $1{,}073{,}741{,}823$ cents.'], 'The book mixes "November" and "October"; with 31 days the total is $2^{31} - 1$ cents.', [('For 10 days?', '1023 cents.')])
c.S(30, 'Exercise 1.5 Q5: profit 30,000 in year 1, rising 5% a year for 40 years. Total?', 'about 3,623,993 Nakfa',
    ['Step 1: $S_{40} = \\frac{30000(1.05^{40} - 1)}{0.05}$.', 'Step 2: $1.05^{40} \\approx 7.04$.'], 'Growth by a percent = GP.', [('For 10 years?', 'about 377,337.')])
c.S(38, 'Review Q7–Q8: (7) a ball dropped from 5 m rises to 45% each bounce: distance when it hits the ground the 6th time? (8) a 80,000 car loses 25% a year: value after 8 years?', 'about 13.03 m; about 8009 Nakfa',
    ['Step 1: falls $\\frac{5(1 - 0.45^6)}{0.55} \\approx 9.02$; rises $\\frac{2.25(1 - 0.45^5)}{0.55} \\approx 4.02$.', 'Step 2: $80000(0.75)^8$.'], 'n hits = n falls but n − 1 rises.', [('Car after 3 years?', '33,750.')])
c.S(38, 'Review Q9: two numbers have AM 25 and GM 15. Find them.', '45 and 5',
    ['Step 1: $x + y = 50$, $xy = 225$.', 'Step 2: $t^2 - 50t + 225 = 0$: $(t - 45)(t - 5) = 0$.'], 'Sum and product ⇒ quadratic.', [('AM 5, GM 4?', '8 and 2.')])
c.M(29, 'Each term of 1, 2, 4, 8, 16, … equals', ['one plus the sum of all earlier terms', 'the sum of all earlier terms', 'twice the previous AP term', 'the previous term squared'], 'A',
    ['Step 1: $1 + 2 + \\dots + 2^{k-1} = 2^k - 1$, so $2^k = 1 + (2^k - 1)$.'], 'Use $S_n$ of a GP.', [('For 2, 6, 18, …?', 'each term = 2 × (1 + sum of earlier terms).')])

d = QSet('1.4–1.5 Practice — harmonic and infinite series', 's14')
d.S(32, 'Exercise 1.6 Q1: which are HPs? (a) $\\frac{1}{3}, \\frac{1}{6}, \\frac{1}{9}, \\frac{1}{12}$ (b) 0.1, 0.01, 0.001 (c) 20, 18, 16 (d) 2, 4, 6, 8 (e) 0.1, 0.2, 0.3.', 'only (a)',
    ['Step 1: reciprocals: (a) 3, 6, 9, 12 — an AP.', 'Step 2: (b) 10, 100, 1000 — a GP; (c), (d), (e) are APs themselves, so their reciprocals are not.'], 'Flip, then test for AP.', [('$1, \\frac{1}{3}, \\frac{1}{5}$?', 'HP.')])
d.S(32, 'Exercise 1.6 Q2: harmonic mean of (a) $\\frac{1}{3}$ and $\\frac{1}{7}$ (b) $\\frac{1}{4}$ and $\\frac{1}{16}$.', '$\\frac{1}{5}$; $\\frac{1}{10}$',
    ['Step 1: AM of the reciprocals: $\\frac{3 + 7}{2} = 5$.', 'Step 2: flip back.'], 'HM of $\\frac{1}{a}$, $\\frac{1}{b}$ is $\\frac{2}{a + b}$.', [('HM of 4 and 12?', '6.')])
d.S(32, 'Exercise 1.6 Q3: insert three harmonic means between (a) $\\frac{1}{4}$ and $\\frac{1}{24}$ (b) $\\frac{1}{14}$ and $\\frac{1}{2}$.', '(a) $\\frac{1}{9}, \\frac{1}{14}, \\frac{1}{19}$ (b) $\\frac{1}{11}, \\frac{1}{8}, \\frac{1}{5}$',
    ['Step 1: AP from 4 to 24 in 4 steps: $d = 5$.', 'Step 2: AP from 14 to 2: $d = -3$.'], 'The book says "arithmetic means" in the HP exercise; the harmonic means are intended. (Arithmetic means for (a) would be $\\frac{19}{96}, \\frac{7}{48}, \\frac{3}{32}$.)', [('One HM between $\\frac{1}{2}$ and $\\frac{1}{6}$?', '$\\frac{1}{4}$.')])
d.S(33, 'Exercise 1.7: write in sigma notation and sum if possible: (a) 1 + 3 + 9 + … + 243 (b) 1 + 3 + 9 + … (c) $3 + 2 + \\frac{4}{3} + \\dots$ (d) 5 + 10 + 15 + …', '(a) $\\sum_{k=1}^{6} 3^{k-1} = 364$ (b) $\\sum 3^{k-1}$ diverges (c) $\\sum 3(\\frac{2}{3})^{k-1} = 9$ (d) $\\sum 5k$ diverges',
    ['Step 1: (a) $243 = 3^5$, so 6 terms: $\\frac{3^6 - 1}{2}$.', 'Step 2: (c) $r = \\frac{2}{3}$: $\\frac{3}{1/3}$.'], 'Infinite sum exists only for $|r| < 1$.', [('$\\sum_{k=1}^{4} 2k$?', '20.')])
d.S(36, 'Exercise 1.8 Q2: converge or diverge? (a) $\\frac{1}{3} + \\frac{1}{9} + \\frac{1}{27} + \\dots$ (b) 16 + 8 + 4 + … (c) 0.7 + 0.07 + … (d) 1 + 1 + 1 + … (e) 1 − 1 + 1 − …', '(a) ½ (b) 32 (c) 7/9; (d), (e) diverge',
    ['Step 1: (a) $\\frac{1/3}{2/3}$.', 'Step 2: (b) $\\frac{16}{1/2}$.', 'Step 3: (c) $\\frac{0.7}{0.9}$.'], '$|r| = 1$ also diverges.', [('$9 - 3 + 1 - \\dots$?', '$\\frac{9}{4/3} = 6.75$.')])
d.S(37, 'Exercise 1.8 Q3: sum (a) $1 + \\frac{1}{9} + \\frac{1}{81} + \\dots$ (b) $\\frac{1}{4} + \\frac{1}{4^2} + \\frac{1}{4^3} + \\dots$ (c) $\\frac{4}{9} + \\frac{8}{27} + \\frac{16}{81} + \\dots$', '9/8; 1/3; 4/3',
    ['Step 1: $\\frac{1}{8/9}$.', 'Step 2: $\\frac{1/4}{3/4}$.', 'Step 3: $r = \\frac{2}{3}$: $\\frac{4/9}{1/3}$.'], 'First term over (1 − ratio).', [('$\\frac{1}{2} - \\frac{1}{4} + \\frac{1}{8} - \\dots$?', '$\\frac{1}{3}$.')])
d.S(37, 'Exercise 1.8 Q4 and Review Q11–12: write as fractions: 1.8181…, 0.444…, 0.2424…', '20/11; 4/9; 8/33',
    ['Step 1: $0.\\overline{81} = \\frac{81}{99} = \\frac{9}{11}$.', 'Step 2: $\\frac{0.4}{0.9}$.', 'Step 3: $\\frac{0.24}{0.99} = \\frac{24}{99}$.'], 'Repeating block over as many 9s.', [('0.3636…?', '4/11.')])
d.S(39, 'Review Q14: sum (a) $\\frac{1}{8} + \\frac{1}{16} + \\frac{1}{32} + \\dots$ (b) $\\frac{1}{9} + \\frac{1}{27} + \\dots$ (c) $4 + 2 + 1 + \\dots$ (d) $\\sum_{i=1}^{\\infty} 0.3^i$ (e) $\\sum_{i=1}^{\\infty} 12(0.01)^i$.', '1/4; 1/6; 8; 3/7; 4/33',
    ['Step 1: (a) $\\frac{1/8}{1/2}$.', 'Step 2: (d) $\\frac{0.3}{0.7}$.', 'Step 3: (e) $\\frac{0.12}{0.99}$.'], 'Write the first term carefully when $i$ starts at 1.', [('$\\sum_{i=1}^{\\infty} 0.5^i$?', '1.')])
d.TF(39, 'Review Q13: $2 + 4 + 8 + 16 + \\dots = \\frac{2}{1 - 2} = -2$.', False,
     ['Step 1: $r = 2$, so $|r| > 1$ and the series diverges.', 'Step 2: the formula $\\frac{G_1}{1 - r}$ may only be used when $|r| < 1$.'], 'A sum of positive numbers cannot be negative.', [('Is $1 + \\frac{1}{2} + \\frac{1}{4} + \\dots = 2$?', 'True.')])
d.S(38, 'Review Q5–Q6: show that $\\log G_1, \\log G_2, \\dots$ is an AP, and that $C^{a_1}, C^{a_2}, \\dots$ is a GP (AP $a_n$, $C > 0$).', 'AP with $d = \\log r$; GP with ratio $C^d$',
    ['Step 1: $\\log G_{n+1} - \\log G_n = \\log \\frac{G_{n+1}}{G_n} = \\log r$.', 'Step 2: $\\frac{C^{a_{n+1}}}{C^{a_n}} = C^{a_{n+1} - a_n} = C^d$.'], 'Logs turn ratios into differences; powers turn differences into ratios.', [('$2^1, 2^3, 2^5, \\dots$ ratio?', '4.')])
d.M(38, 'For two positive numbers $x \\ne y$ (Review Q10):', ['AM > GM', 'AM < GM', 'AM = GM', 'it depends'], 'A',
    ['Step 1: $\\frac{x + y}{2} - \\sqrt{xy} = \\frac{(\\sqrt{x} - \\sqrt{y})^2}{2} > 0$.'], 'A square is never negative.', [('When are they equal?', 'when $x = y$.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Sequence', 'A function whose domain is the positive integers; its values are the terms.', 3),
    ('Recursive formula', 'Gives the first term(s) and a rule using earlier terms.', 6),
    ('Common difference', 'The constant $d$ added each time in an AP.', 9),
    ('Common ratio', 'The constant $r$ multiplied each time in a GP.', 20),
    ('Harmonic progression', 'A sequence whose reciprocals form an AP.', 31),
    ('Convergent series', 'An infinite series whose partial sums approach a finite number.', 34),
]
TIPS = [('n! = n × (n − 1)! simplifies factorial fractions.', 6), ('AP: add d; GP: multiply by r.', 20), ('Infinite GP sum G1/(1 − r) needs |r| < 1.', 35)]
IDEAS = [('ap', 'Arithmetic progression', 'l1_2', 'math12-u1-md-ap-why'), ('gp', 'Geometric progression', 'l1_3', 'math12-u1-md-gp-why'),
         ('hp', 'Harmonic progression', 'l1_4', 'math12-u1-md-hp-t'), ('inf', 'Infinite geometric series', 'l1_5', 'math12-u1-md-inf-t')]
