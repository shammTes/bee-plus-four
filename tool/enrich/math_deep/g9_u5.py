r"""Grade 9 Unit 5 — Exponential and Logarithmic Expressions (pp. 103-129)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet, plane
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side

UID = 'math9-u5'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_growth():
    a = Plot(0, 5.5, 0, 34, unit=26, uy=4, pad=26, grid=False, every=1, yevery=8, xlab='n', ylab='N')
    for n in range(0, 6):
        a.line(a.X(n), a.Y(0), a.X(n), a.Y(2 ** n), BLUE, 9)
    a.text(a.X(5) - 16, a.Y(32) + 4, '32', 11.5, BLUE).text(a.X(2.2), a.Y(26), '× 2 each step', 12, BLUE)
    b = Plot(0, 5.5, 0, 34, unit=26, uy=4, pad=26, grid=False, every=1, yevery=8, xlab='n', ylab='N')
    for n in range(0, 6):
        b.line(b.X(n), b.Y(0), b.X(n), b.Y(32 / 2 ** n), RED, 9)
    b.text(b.X(0) + 18, b.Y(32) + 4, '32', 11.5, RED).text(b.X(3.2), b.Y(26), '× ½ each step', 12, RED)
    return side_by_side([a, b], 6, ['doubling (× 2)', 'halving (× ½)'])


def f_logcycle():
    f = Fig(330, 170)
    f.rect(10, 20, 140, 60, BLUE, 2, FILL[BLUE], 10).rect(180, 20, 140, 60, GREEN, 2, FILL[GREEN], 10)
    f.text(80, 14, 'exponential form', 12, BLUE).text(250, 14, 'logarithmic form', 12, GREEN)
    f.text(62, 60, '2', 24, RED).text(76, 46, '3', 16, ORANGE).text(88, 60, '= 8', 22, PURPLE, 'start')
    f.text(196, 60, 'log', 20, INK, 'start').text(228, 68, '2', 14, RED, 'start').text(240, 60, '8 = 3', 22, PURPLE, 'start')
    f.curve_arrow(150, 40, 180, 40, -14, INK, 1.8, 7).curve_arrow(180, 62, 150, 62, -14, INK, 1.8, 7)
    f.text(30, 112, 'base', 13, RED, 'start').text(30, 132, 'exponent = the log', 13, ORANGE, 'start').text(30, 152, 'answer (power)', 13, PURPLE, 'start')
    f.circle(20, 108, 5, RED, 2, RED).circle(20, 128, 5, ORANGE, 2, ORANGE).circle(20, 148, 5, PURPLE, 2, PURPLE)
    f.text(320, 132, 'a log is an exponent', 13, GREEN, 'end')
    return f


def f_logtable():
    rows = [(26, ['4150', '4166', '4183', '4200', '4216', '4232', '4249']), (27, ['4314', '4330', '4346', '4362', '4378', '4393', '4409']),
            (28, ['4472', '4487', '4502', '4518', '4533', '4548', '4564'])]
    f = Fig(330, 150)
    x0, y0, cw, rh = 40, 30, 41, 28
    f.text(x0 - 18, y0 - 10, 'N', 13, INK)
    for j in range(7):
        f.text(x0 + 6 + j * cw + cw / 2, y0 - 10, str(j), 13, ORANGE if j == 6 else INK)
    for i, (n, vals) in enumerate(rows):
        y = y0 + i * rh
        f.text(x0 - 18, y + 19, str(n), 13, BLUE if n == 27 else INK)
        for j, v in enumerate(vals):
            hit = n == 27 and j == 6
            f.rect(x0 + 6 + j * cw, y, cw - 2, rh - 3, ORANGE if hit else GREY, 2 if hit else 0.8, FILL[ORANGE] if hit else '#ffffff', 3)
            f.text(x0 + 6 + j * cw + cw / 2 - 1, y + 18, v, 12, RED if hit else INK)
    f.text(165, 140, 'row 27, column 6:  log 2.76 = 0.4409', 13, RED)
    return f


def f_charman():
    f = Fig(330, 150)
    f.text(165, 30, '359 = 3.59 × 10²', 18, INK)
    f.text(165, 80, 'log 359 = 2 + 0.5551 = 2.5551', 17, INK)
    f.line(140, 88, 112, 106, BLUE, 2).line(208, 88, 240, 106, GREEN, 2)
    f.text(100, 122, 'characteristic', 13, BLUE).text(100, 140, '= the power of 10', 11.5, BLUE)
    f.text(250, 122, 'mantissa', 13, GREEN).text(250, 140, '= log 3.59 (table)', 11.5, GREEN)
    f.curve_arrow(212, 36, 132, 68, 24, BLUE, 1.6, 7)
    f.curve_arrow(120, 36, 208, 66, -18, GREEN, 1.6, 7)
    return f


DIAGRAMS = {
    'growth': (f_growth(), 'Repeated doubling and halving', 104),
    'logcycle': (f_logcycle(), 'Exponential form ⇄ logarithmic form', 116),
    'charman': (f_charman(), 'Characteristic and mantissa', 122),
    'logtable': (f_logtable(), 'Reading the table of logarithms (Activity 5.17)', 123),
}

# ------------------------------------------------------------------ lesson 5.1
L1 = [
    T('=math9-u5-c01', '5.1.1 Power notation', 103,
      'Repeated multiplication is written as a **power**: $$a^n = \\underbrace{a \\times a \\times \\dots \\times a}_{n \\text{ factors}}$$ $a$ is the **base**, $n$ the **exponent** (index) and $a^n$ the **power**.',
      'Brackets matter: $(-2)^4 = 16$ (the base is $-2$) but $-2^4 = -(2^4) = -16$ (the base is 2). $(-2)^5 = -32$: a negative base gives a negative answer for an odd exponent.',
      'Growth and decay: insects that double every month starting from 500 number $500 \\times 2^n$ after $n$ months — after 12 months $500 \\times 4096 = 2\\,048\\,000$. A colony that halves each month from 20 000 has $20\\,000 \\times \\left(\\frac{1}{2}\\right)^n$.'),
    DG('growth', 'Doubling vs halving', 104, 'growth',
       'Doubling multiplies by 2 each step: 1, 2, 4, 8, 16, 32. Halving multiplies by $\\frac{1}{2}$: 32, 16, 8, 4, 2, 1. The change gets bigger and bigger (or smaller and smaller) — not a constant amount as in a linear pattern.'),
    T('=math9-u5-c02', '5.1.2 – 5.1.3 Product and quotient laws', 106,
      '**Same base, multiply → add the exponents:** $a^m \\times a^n = a^{m + n}$. Because $2^3 \\times 2^2 = (2 \\cdot 2 \\cdot 2)(2 \\cdot 2) = 2^5$.',
      '**Same base, divide → subtract the exponents:** $\\frac{a^m}{a^n} = a^{m - n}$ ($a \\ne 0$). Because $\\frac{2^6}{2^2}$ cancels two 2s, leaving $2^4$.',
      'Numbers in front are multiplied or divided normally: $5y^3 \\times 2y^6 = 10y^9$; $36a^{12}b^6 \\div 9a^3b^2 = 4a^9b^4$.',
      '**Different bases cannot be combined** this way: $2^3 \\times 3^2$ is just $8 \\times 9 = 72$.'),
    T('=math9-u5-c03', '5.1.4 – 5.1.6 Power of a product, quotient and power', 108,
      '$(ab)^n = a^n b^n$: $(2 \\times 3)^3 = 2^3 \\times 3^3$ — every factor inside gets the exponent.',
      '$\\left(\\frac{a}{b}\\right)^n = \\frac{a^n}{b^n}$ ($b \\ne 0$): $\\left(\\frac{2}{3}\\right)^2 = \\frac{4}{9}$.',
      '$(a^m)^n = a^{mn}$: $(2^3)^4 = 2^{12}$ — a power of a power **multiplies** the exponents.',
      '**Warning:** there is no law for sums: $(a + b)^2 \\ne a^2 + b^2$. Check: $(5 + 7)^2 = 144$ but $5^2 + 7^2 = 74$.'),
    T('=math9-u5-c04', '5.1.7 Zero and negative exponents', 110,
      '$\\frac{7^3}{7^3} = 1$, and the quotient law gives $7^{3 - 3} = 7^0$. So **$a^0 = 1$** for every $a \\ne 0$: $6^0 = (-4)^0 = (1.5446)^0 = 1$.',
      '$\\frac{5^4}{5^7} = \\frac{1}{5^3}$, and the quotient law gives $5^{-3}$. So **$a^{-n} = \\frac{1}{a^n}$**: a negative exponent means "one over", **not** a negative number. $2^{-4} = \\frac{1}{16}$, $(0.1)^{-2} = 100$, $\\left(\\frac{2}{3}\\right)^{-2} = \\frac{9}{4}$.',
      'In growth problems a negative $n$ means "in the past": insects doubling monthly with 80 now had $80 \\times 2^{-3} = 10$ three months ago.'),
    'math9-u5-tbl1',
    T('=math9-u5-c05', '5.1.8 Fractional exponents and radicals', 113,
      '$2^{\\frac{1}{2}} \\times 2^{\\frac{1}{2}} = 2^1 = 2$, so $2^{\\frac{1}{2}}$ is the number whose square is 2: $2^{\\frac{1}{2}} = \\sqrt{2}$. In general $$a^{\\frac{1}{n}} = \\sqrt[n]{a}, \\qquad a^{\\frac{m}{n}} = \\sqrt[n]{a^m} = \\left(\\sqrt[n]{a}\\right)^m$$ ($a \\ge 0$ when $n$ is even).',
      'Work out the root first — the numbers stay small: $16^{\\frac{3}{2}} = (\\sqrt{16})^3 = 4^3 = 64$; $27^{-\\frac{2}{3}} = \\frac{1}{(\\sqrt[3]{27})^2} = \\frac{1}{9}$.',
      'The edge of a cube of volume $v$ is $\\sqrt[3]{v} = v^{\\frac{1}{3}}$.'),
    TB('frac-t', 'Reading an exponent', 113, ['Exponent', 'Meaning', 'Example'],
       [['positive whole $n$', 'multiply $n$ copies', '$3^4 = 81$'], ['0', 'equals 1', '$9^0 = 1$'],
        ['negative $-n$', 'reciprocal of $a^n$', '$3^{-2} = \\frac{1}{9}$'], ['$\\frac{1}{n}$', '$n$th root', '$8^{\\frac{1}{3}} = 2$'],
        ['$\\frac{m}{n}$', '$n$th root, then power $m$', '$8^{\\frac{2}{3}} = 4$'], ['$-\\frac{m}{n}$', 'all three: root, power, reciprocal', '$8^{-\\frac{2}{3}} = \\frac{1}{4}$']],
       'Order for $a^{-\\frac{m}{n}}$: denominator → root, numerator → power, minus sign → flip.'),
    WK('ex-51a', 'Worked example: simplify with the laws', 110,
       'Simplify (a) $\\frac{a^3 \\times a^6}{a^2}$ (b) $\\left(2^3\\right)^2 \\times 2^{-5}$ (c) $\\left(\\frac{8}{27}\\right)^{-\\frac{2}{3}}$.',
       ['(a) Top: $a^{3 + 6} = a^9$; divide: $a^{9 - 2} = a^7$.', '(b) $(2^3)^2 = 2^6$; $2^6 \\times 2^{-5} = 2^1 = 2$.',
        '(c) Flip for the minus: $\\left(\\frac{27}{8}\\right)^{\\frac{2}{3}}$. Cube root: $\\frac{3}{2}$. Square: $\\frac{9}{4}$.'],
       '(a) $a^7$ (b) 2 (c) $\\frac{9}{4}$'),
    T('=math9-u5-c06', '5.1.9 Exponential equations', 114,
      'An **exponential equation** has the unknown in the exponent, e.g. $2^n = 32$.',
      '**Method:** write both sides as powers of the **same base**, then use: if $a^x = a^y$ (with $a > 0$, $a \\ne 1$) then $x = y$.',
      'Table tennis knockout with 32 players: each round halves the players, so $2^n = 32 = 2^5$ and there are $n = 5$ rounds.',
      'Useful powers to know: $2^5 = 32$, $2^6 = 64$, $3^4 = 81$, $3^5 = 243$, $4^3 = 64$, $5^3 = 125$, $5^4 = 625$, $10^{-2} = 0.01$.'),
    WK('ex-51b', 'Worked example: Example 5.3', 115,
       'Insects triple every month. Starting with 100, how long until there are 8100?',
       ['$100 \\times 3^n = 8100$.', 'Divide by 100: $3^n = 81 = 3^4$.', 'Same base, so $n = 4$ months.'],
       '4 months'),
    WK('ex-51c', 'Worked example: different bases that match', 115,
       'Solve (a) $4^{x - 1} = 8$ (b) $9^{1 - 2x} = 81$.',
       ['(a) Use base 2: $(2^2)^{x - 1} = 2^3 \\Rightarrow 2x - 2 = 3 \\Rightarrow x = \\frac{5}{2}$.', '(b) $81 = 9^2$, so $1 - 2x = 2 \\Rightarrow x = -\\frac{1}{2}$.', 'Check (a): $4^{1.5} = (\\sqrt{4})^3 = 8$ (correct).'],
       '(a) $x = \\frac{5}{2}$ (b) $x = -\\frac{1}{2}$'),
]

# ------------------------------------------------------------------ lesson 5.2
L2 = [
    T('logdef-t', '5.2.1 What is a logarithm?', 116,
      '$\\log_a x$ answers the question: **"$a$ to what power gives $x$?"**',
      '$$y = \\log_a x \\iff a^y = x \\qquad (a > 0,\\ a \\ne 1,\\ x > 0)$$',
      'Examples: $\\log_3 27 = 3$ because $3^3 = 27$; $\\log_{64} 8 = \\frac{1}{2}$ because $64^{\\frac{1}{2}} = 8$; $\\log_{10} 0.001 = -3$ because $10^{-3} = 0.001$.',
      'Two values to remember: $\\log_a 1 = 0$ (since $a^0 = 1$) and $\\log_a a = 1$. You cannot take the log of 0 or of a negative number.'),
    DG('logcycle', 'The same fact written two ways', 116, 'logcycle',
       'The base stays the base; the exponent becomes the value of the log; the answer of the power goes inside the log.'),
    WK('ex-52a', 'Worked example: evaluate logs', 117,
       'Find (a) $\\log_5 625$ (b) $\\log_2 0.25$ (c) $\\log_7 7\\sqrt{7}$.',
       ['(a) $5^4 = 625$, so 4.', '(b) $0.25 = \\frac{1}{4} = 2^{-2}$, so $-2$.', '(c) $7\\sqrt{7} = 7^1 \\times 7^{\\frac{1}{2}} = 7^{\\frac{3}{2}}$, so $\\frac{3}{2}$.'],
       '(a) 4 (b) $-2$ (c) $\\frac{3}{2}$'),
    T('loglaws-t', '5.2.2 Laws of logarithms', 117,
      'Because logs are exponents, the exponent laws become log laws (for positive $m, n$):',
      '- **Product:** $\\log_a (mn) = \\log_a m + \\log_a n$ (multiply inside → add logs).',
      '- **Quotient:** $\\log_a \\frac{m}{n} = \\log_a m - \\log_a n$ (divide inside → subtract logs).',
      '- **Power:** $\\log_a m^n = n \\log_a m$ (exponent comes to the front).',
      'Check: $\\log_{10} 100 + \\log_{10} 1000 = 2 + 3 = 5 = \\log_{10} 100\\,000$.',
      '**No law for sums:** $\\log (m + n) \\ne \\log m + \\log n$.'),
    TB('law-t', 'Exponent law ↔ log law', 119, ['Exponent law', 'Log law', 'Example'],
       [['$a^m a^n = a^{m+n}$', '$\\log (mn) = \\log m + \\log n$', '$\\log_3 54 + \\log_3 \\frac{3}{2} = \\log_3 81 = 4$'],
        ['$\\frac{a^m}{a^n} = a^{m-n}$', '$\\log \\frac{m}{n} = \\log m - \\log n$', '$\\log_2 144 - \\log_2 9 = \\log_2 16 = 4$'],
        ['$(a^m)^n = a^{mn}$', '$\\log m^n = n \\log m$', '$\\log_2 8^3 = 3 \\times 3 = 9$'],
        ['$a^0 = 1$', '$\\log_a 1 = 0$', '$\\log_7 1 = 0$'], ['$a^1 = a$', '$\\log_a a = 1$', '$\\log_{10} 10 = 1$']],
       'Strategy: combine the logs into **one** log first, then evaluate.'),
    'math9-u5-mn2',
    MN('=math9-u5-c08', 'Logs undo exponents', 118,
       '"A log is an exponent." Every log law is an exponent law in disguise: **times → plus, divide → minus, power → front**. And there is NO rule for $\\log (x + y)$.'),
    T('logeq-t', '5.2.3 Simple logarithmic equations', 120,
      '- If the unknown is **inside** the log ($\\log_2 k = 5$), change to exponential form: $k = 2^5 = 32$.',
      '- If the unknown is the **value** ($\\log_9 3 = m$), write $9^m = 3$, i.e. $3^{2m} = 3^1$, so $m = \\frac{1}{2}$.',
      '- If several logs with the same base appear, combine them into one log on each side, then compare: $\\log_3 x = \\log_3 12 + \\log_3 4 = \\log_3 48$ gives $x = 48$.',
      'Always check that every number inside a log is positive.'),
    WK('ex-52b', 'Worked example: Exercise 5.14', 120,
       'Solve (a) $\\log_6 (x - 3) = 2$ (b) $\\log_2 72 - \\log_2 x = \\log_2 12$.',
       ['(a) $x - 3 = 6^2 = 36$, so $x = 39$.', '(b) Left side: $\\log_2 \\frac{72}{x}$. So $\\frac{72}{x} = 12$ and $x = 6$.', 'Check (b): $\\log_2 72 - \\log_2 6 = \\log_2 12$ (correct).'],
       '(a) 39 (b) 6'),
    T('=math9-u5-c09', '5.2.4 Common logarithms', 121,
      '**Scientific notation:** write a number as $n \\times 10^m$ with $1 \\le n < 10$ and $m$ an integer: $276\\,000 = 2.76 \\times 10^5$ (the textbook writes $2.76 \\times 10\\,000$, but $10\\,000 = 10^4$; it should be $100\\,000$). $0.000521 = 5.21 \\times 10^{-4}$.',
      '**Common logarithms** have base 10 and are written $\\log x$. Then $$\\log (n \\times 10^m) = m + \\log n$$ where $0 \\le \\log n < 1$ comes from the table.',
      'The whole-number part $m$ is the **characteristic**; the decimal part $\\log n$ is the **mantissa**. For numbers less than 1 the characteristic is negative: $\\log 0.0643 = -2 + 0.8082$.'),
    DG('charman', 'Splitting a common logarithm', 122, 'charman'),
    DG('logtable', 'How to read the table', 123, 'logtable',
       'For log 2.76: go to row **27** (the first two digits) and column **6** (the third digit): 4409, so $\\log 2.76 = 0.4409$. For an antilogarithm do the reverse: find the mantissa inside the table and read off the row and column.'),
    T('=math9-u5-c10', '5.2.5 Antilogarithms and calculating with logs', 123,
      'If $\\log x = c$ then $x = 10^c$ = **antilog** $c$. Split $c$ = characteristic + mantissa: $\\log x = 2.4969 = 2 + 0.4969$, so $x = 10^2 \\times \\text{antilog}(0.4969) = 100 \\times 3.14 = 314$.',
      'Calculating with logs turns hard operations into easier ones: **multiply → add logs, divide → subtract logs, power → multiply the log, root → divide the log.** Then take the antilog.'),
    WK('ex-52c', 'Worked example: Activity 5.17 (multiplying with logs)', 124,
       'Use logarithms to estimate $2680 \\times 81.6$.',
       ['$\\log 2680 = 3 + \\log 2.68 = 3.4281$ and $\\log 81.6 = 1 + \\log 8.16 = 1.9117$. (The textbook\'s "log 2860" is a misprint for log 2680.)', 'Add: $\\log x = 5.3398 = 5 + 0.3398$.', 'Antilog of 0.3398: the table has 3385 (for 2.18) and 3404 (for 2.19); 3404 is closer, so 2.19.', '$x \\approx 2.19 \\times 10^5 = 219\\,000$ (exact value 218 688).'],
       '≈ 219 000'),
    WK('ex-52d', 'Worked example: Example 5.6 (dividing with logs)', 125,
       'Evaluate $864 \\div 0.745$ using logarithms.',
       ['$\\log 864 = 2 + 0.9365$; $\\log 0.745 = -1 + 0.8722$.', 'Subtract: $(2 + 0.9365) - (-1 + 0.8722) = 3 + 0.0643$.', 'Antilog 0.0643 ≈ 1.16, so $x \\approx 1.16 \\times 10^3 = 1160$.', 'Check with a calculator: $864 \\div 0.745 \\approx 1159.7$ (correct). (The textbook writes "$864 \\times 0.745$" in the question; the working is a division.)'],
       '≈ 1160'),
    RM('=math9-u5-c07', 'Unit summary', 125,
       'Exponents: $a^m a^n = a^{m+n}$, $\\frac{a^m}{a^n} = a^{m-n}$, $(a^m)^n = a^{mn}$, $a^0 = 1$, $a^{-n} = \\frac{1}{a^n}$, $a^{\\frac{m}{n}} = \\sqrt[n]{a^m}$.',
       'Logs: $\\log_a x = y \\iff a^y = x$; $\\log (mn) = \\log m + \\log n$; $\\log \\frac{m}{n} = \\log m - \\log n$; $\\log m^n = n \\log m$.'),
]

LESSONS = {'math9-u5-l5-1': L1, 'math9-u5-l5-2': L2}

# ------------------------------------------------------------------ practice
a = QSet('5.1 Practice — exponents', 's51')
a.S(105, 'Evaluate (a) $(-2)^4$ (b) $-2^4$ (c) $(-2)^5$ (d) $-(-2)^5$.', '16, $-16$, $-32$, 32',
    ['Step 1 (a): base $-2$, even exponent → $+16$.', 'Step 2 (b): only 2 is raised: $-(16) = -16$.', 'Step 3 (c): odd exponent → $-32$.', 'Step 4 (d): $-(-32) = 32$.'],
    'The exponent applies only to what is directly in front of it.', [('Evaluate $-7^2$ and $(-7)^2$.', '$-49$ and 49.')])
a.S(105, 'Simplify $3(-2)^3 + 5(3)^2$.', '21',
    ['Step 1: powers first: $(-2)^3 = -8$, $3^2 = 9$.', 'Step 2: $3(-8) + 5(9) = -24 + 45 = 21$.'],
    'Powers before multiplication.', [('Simplify $(-1)^4 + (-3)^3$.', '$1 - 27 = -26$.')])
a.S(105, 'A hive has 1000 bees and doubles every month. How many after 5 months?', '32 000',
    ['Step 1: $1000 \\times 2^5$.', 'Step 2: $2^5 = 32$, so 32 000.'],
    'Start value × (growth factor)$^{\\text{steps}}$.', [('20 000 insects halve every month. After 5 months?', '$20\\,000 \\times \\frac{1}{32} = 625$.')])
a.M(106, '$5y^3 \\times 2y^6 = $', ['$7y^9$', '$10y^{18}$', '$10y^9$', '$7y^{18}$'], 'C',
    ['Step 1: numbers multiply: $5 \\times 2 = 10$.', 'Step 2: same base: add exponents $3 + 6 = 9$.'],
    'Multiply the numbers, add the exponents.', [('$a^6b^3 \\times a^8b^6$?', '$a^{14}b^9$.')])
a.S(107, 'Simplify $36a^{12}b^6 \\div 9a^3b^2$.', '$4a^9b^4$',
    ['Step 1: $36 \\div 9 = 4$.', 'Step 2: $a^{12 - 3} = a^9$, $b^{6 - 2} = b^4$.'],
    'Divide numbers, subtract exponents base by base.', [('$125k^{18} \\div 25k^6$?', '$5k^{12}$.')])
a.S(110, 'Write $(3^2)^3$ and $\\left(\\frac{2}{3}\\right)^{3 \\times 2}$ as single powers and evaluate the first.', '$3^6 = 729$; $\\left(\\frac{2}{3}\\right)^6$',
    ['Step 1: power of a power → multiply: $3^{2 \\times 3} = 3^6 = 729$.', 'Step 2: the second is already $\\left(\\frac{2}{3}\\right)^6 = \\frac{64}{729}$.'],
    'Brackets with an outside exponent → multiply.', [('$(a^5)^3$?', '$a^{15}$.')])
a.S(111, 'Evaluate (a) $2^{-4}$ (b) $(0.1)^{-2}$ (c) $7^0 + 3^{-3}$.', '$\\frac{1}{16}$; 100; $\\frac{28}{27}$',
    ['Step 1: $\\frac{1}{2^4} = \\frac{1}{16}$.', 'Step 2: $\\frac{1}{0.01} = 100$.', 'Step 3: $1 + \\frac{1}{27} = \\frac{28}{27}$.'],
    'Negative exponent → reciprocal, the sign of the number stays.', [('$-5^{-3}$?', '$-\\frac{1}{125}$.')])
a.S(112, 'Insects triple every month; there are 135 now. How many were there 2 months ago?', '15',
    ['Step 1: $135 \\times 3^{-2}$.', 'Step 2: $135 \\div 9 = 15$.'],
    'Going back in time → negative exponent → divide.', [('600 g halves every month. How much 4 months ago?', '$600 \\times 2^4 = 9600$ g.')])
a.S(113, 'Evaluate (a) $25^{\\frac{1}{2}}$ (b) $81^{\\frac{1}{4}}$ (c) $(-27)^{\\frac{1}{3}}$ (d) $64^{0.5}$.', '5, 3, $-3$, 8',
    ['Step 1: square root of 25 = 5.', 'Step 2: fourth root of 81 = 3 ($3^4 = 81$).', 'Step 3: cube root of $-27$ = $-3$ (odd roots of negatives are fine).', 'Step 4: $0.5 = \\frac{1}{2}$: $\\sqrt{64} = 8$.'],
    'Decimal exponents: change to fractions first.', [('$16^{0.25}$?', '2.')])
a.S(114, 'Evaluate (a) $27^{\\frac{2}{3}}$ (b) $16^{0.75}$ (c) $125^{-\\frac{2}{3}}$.', '9, 8, $\\frac{1}{25}$',
    ['Step 1: $(\\sqrt[3]{27})^2 = 3^2 = 9$.', 'Step 2: $0.75 = \\frac{3}{4}$: $(\\sqrt[4]{16})^3 = 2^3 = 8$.', 'Step 3: $\\frac{1}{(\\sqrt[3]{125})^2} = \\frac{1}{25}$.'],
    'Root first, then power, then flip.', [('$4^{-\\frac{3}{2}}$?', '$\\frac{1}{8}$.')])
a.S(115, 'Solve (a) $5^x = 125$ (b) $10^x = 0.01$ (c) $16^{x - 1} = 64$.', '3; $-2$; $\\frac{5}{2}$',
    ['Step 1: $125 = 5^3 \\Rightarrow x = 3$.', 'Step 2: $0.01 = 10^{-2} \\Rightarrow x = -2$.', 'Step 3: base 4: $4^{2(x - 1)} = 4^3 \\Rightarrow 2x - 2 = 3 \\Rightarrow x = \\frac{5}{2}$.'],
    'Find a common base, then equate exponents.', [('Solve $9^x = 729$.', '$x = 3$.')])
a.S(115, 'Solve $3 \\times 6^x = 108$.', '$x = 2$',
    ['Step 1: divide by 3: $6^x = 36$.', 'Step 2: $36 = 6^2 \\Rightarrow x = 2$.'],
    'Get the power alone before comparing.', [('Solve $5 \\times 2^x = 80$.', '$2^x = 16$, $x = 4$.')])
a.S(115, 'Bugs triple every month. There are 20 now. When will there be 540?', '3 months',
    ['Step 1: $20 \\times 3^n = 540$.', 'Step 2: $3^n = 27 = 3^3$, $n = 3$.'],
    'Divide by the starting amount first.', [('300 ants double monthly. When 4800?', '4 months.')])
a.TF(108, '$(a + b)^2 = a^2 + b^2$ for all $a, b$.', False,
     ['Step 1: try $a = 5$, $b = 7$: $(12)^2 = 144$.', 'Step 2: $25 + 49 = 74 \\ne 144$.'],
     'Exponent laws work for products, not sums.', [('Is $(ab)^2 = a^2b^2$ always true?', 'Yes.')])
a.S(126, 'A ball dropped from 4 m bounces to $h = 4 \\times 0.9^n$ m after $n$ bounces. Find the height after 2 and after 3 bounces.', '3.24 m; 2.916 m',
    ['Step 1: $0.9^2 = 0.81$, $4 \\times 0.81 = 3.24$ m.', 'Step 2: $0.9^3 = 0.729$, $4 \\times 0.729 = 2.916$ m.'],
    'Each bounce keeps 90% of the height.', [('After how many bounces is it first below 3 m?', '3 bounces.')])

b = QSet('5.2 Practice — logarithms', 's52')
b.S(116, 'Write in logarithmic form: (a) $5^3 = 125$ (b) $64^{\\frac{1}{2}} = 8$ (c) $0.04 = 5^{-2}$.', '$\\log_5 125 = 3$; $\\log_{64} 8 = \\frac{1}{2}$; $\\log_5 0.04 = -2$',
    ['Step 1: base stays, exponent becomes the log value, the answer goes inside.', 'Step 2: apply to each.'],
    'The log IS the exponent.', [('Write $a^6 = k$ as a log.', '$\\log_a k = 6$.')])
b.S(116, 'Write $\\log_{10} 0.001 = -3$ in exponential form.', '$10^{-3} = 0.001$',
    ['Step 1: base 10, exponent $-3$, answer 0.001.', 'Step 2: $10^{-3} = 0.001$.'],
    'Read it as "10 to the $-3$ is 0.001".', [('$\\log_3 27 = 3$ in exponential form?', '$3^3 = 27$.')])
b.M(117, '$\\log_7 343 = $', ['3', '49', '7', '$\\frac{1}{3}$'], 'A',
    ['Step 1: $7^2 = 49$, $7^3 = 343$.', 'Step 2: so the exponent is 3.'],
    'Ask: 7 to what power is 343?', [('$\\log_{25} 625$?', '2.')])
b.S(117, 'Evaluate $\\log_5 0.04$ and $\\log_2 0.25$.', '$-2$ and $-2$',
    ['Step 1: $0.04 = \\frac{1}{25} = 5^{-2}$.', 'Step 2: $0.25 = \\frac{1}{4} = 2^{-2}$.'],
    'Numbers between 0 and 1 have negative logs (base > 1).', [('$\\log_{10} 0.1$?', '$-1$.')])
b.S(118, 'Find $\\log_{10} 40 + \\log_{10} \\frac{10}{4}$.', '2',
    ['Step 1: product law: $\\log_{10} \\left(40 \\times \\frac{10}{4}\\right) = \\log_{10} 100$.', 'Step 2: $= 2$.'],
    'Combine first — the product is a nice number.', [('$\\log_5 20 + \\log_5 \\frac{25}{4}$?', '$\\log_5 125 = 3$.')])
b.S(118, 'Find $\\log_3 135 - \\log_3 5$.', '3',
    ['Step 1: quotient law: $\\log_3 \\frac{135}{5} = \\log_3 27$.', 'Step 2: $= 3$.'],
    'Subtracting logs = dividing inside.', [('$\\log_2 40 - \\log_2 5$?', '3.')])
b.S(119, 'Find $\\log_2 \\sqrt[5]{16}$.', '$\\frac{4}{5}$',
    ['Step 1: $\\sqrt[5]{16} = 16^{\\frac{1}{5}} = 2^{\\frac{4}{5}}$.', 'Step 2: $\\log_2 2^{\\frac{4}{5}} = \\frac{4}{5}$.'],
    'Write roots as fractional powers.', [('$\\log_{10} \\sqrt[3]{100}$?', '$\\frac{2}{3}$.')])
b.S(126, 'If $\\log_5 m = 3$, find $\\log_5 (25m^2)$.', '8',
    ['Step 1: $\\log_5 25 + 2\\log_5 m$.', 'Step 2: $2 + 2(3) = 8$.'],
    'Break the product apart, bring powers to the front.', [('If $\\log_2 m = 4$, find $\\log_2 (8m)$.', '7.')])
b.S(120, 'Solve (a) $\\log_5 x = 6$ (b) $\\log_9 3 = m$.', '$x = 15\\,625$; $m = \\frac{1}{2}$',
    ['Step 1: $x = 5^6 = 15\\,625$.', 'Step 2: $9^m = 3 \\Rightarrow 3^{2m} = 3^1 \\Rightarrow m = \\frac{1}{2}$.'],
    'Unknown inside → exponential form; unknown is the log → common base.', [('Solve $\\log_2 k = 5$.', '$k = 32$.')])
b.S(127, 'Solve $\\log_8 5 + \\log_8 x = \\log_8 55$.', '$x = 11$',
    ['Step 1: $\\log_8 5x = \\log_8 55$.', 'Step 2: $5x = 55$, $x = 11$.'],
    'One log on each side → compare the insides.', [('Solve $4\\log_8 x = \\log_8 16$.', '$x^4 = 16$, $x = 2$.')])
b.S(121, 'Write in scientific notation: (a) 149 600 000 000 m (b) 0.0008793.', '$1.496 \\times 10^{11}$; $8.793 \\times 10^{-4}$',
    ['Step 1: move the point 11 places left: $1.496 \\times 10^{11}$.', 'Step 2: move the point 4 places right: $8.793 \\times 10^{-4}$.'],
    'Count the jumps; big numbers → positive power, small → negative.', [('Write 300 000 000.', '$3 \\times 10^8$.')])
b.S(122, 'Using $\\log 2.38 = 0.3766$, find $\\log 238$ and $\\log 0.00238$.', '2.3766; $-3 + 0.3766$',
    ['Step 1: $238 = 2.38 \\times 10^2$: characteristic 2.', 'Step 2: $0.00238 = 2.38 \\times 10^{-3}$: characteristic $-3$, mantissa unchanged.'],
    'The mantissa depends only on the digits; the characteristic on the position of the point.', [('$\\log 2500$ if $\\log 2.5 = 0.3979$?', '3.3979.')])
b.S(124, 'If $\\log x = 2.4969$, find $x$ (use $\\log 3.14 = 0.4969$).', '314',
    ['Step 1: $x = 10^2 \\times 10^{0.4969}$.', 'Step 2: $= 100 \\times 3.14 = 314$.'],
    'Characteristic → power of 10; mantissa → digits from the table.', [('Antilog of $-3$?', '0.001.')])
b.TF(118, '$\\log (m + n) = \\log m + \\log n$', False,
     ['Step 1: try $m = n = 10$: $\\log 20 \\approx 1.30$.', 'Step 2: $\\log 10 + \\log 10 = 2$, not equal.'],
     'The product law is for $\\log (mn)$.', [('What does $\\log m + \\log n$ equal?', '$\\log (mn)$.')])

QS = a.items + b.items

GLOSSARY = [
    ('Base', 'The number that is multiplied repeatedly in a power.', 103),
    ('Exponent', 'The small raised number that tells how many factors (also called index).', 103),
    ('Exponential equation', 'An equation with the unknown in the exponent, e.g. $2^n = 32$.', 115),
    ('Logarithm', '$\\log_a x$ is the exponent to which $a$ must be raised to give $x$.', 116),
    ('Common logarithm', 'A logarithm to base 10, written $\\log x$.', 122),
    ('Scientific notation', '$n \\times 10^m$ with $1 \\le n < 10$ and $m$ an integer.', 121),
    ('Characteristic', 'The integer part of a common logarithm (the power of 10).', 122),
    ('Mantissa', 'The decimal part of a common logarithm, read from the table.', 122),
    ('Antilogarithm', 'The number whose logarithm is given: antilog $c = 10^c$.', 123),
]
TIPS = [
    ('Same base: multiply → add exponents, divide → subtract, power of a power → multiply.', 110),
    ('a⁻ⁿ = 1/aⁿ (reciprocal, not negative); a^(m/n): root, then power.', 113),
    ('A log is an exponent: log_a x = y means a^y = x.', 116),
]
IDEAS = [('read', 'Reading an exponent', 'l5_1', 'math9-u5-md-frac-t'), ('law', 'Exponent law ↔ log law', 'l5_2', 'math9-u5-md-law-t')]
