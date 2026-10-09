r"""Grade 11 Unit 4 — Exponential and Logarithmic Functions (pp. 142-166)."""
from math import log
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side, with_legend

UID = 'math11-u4'
set_unit(UID)


# ------------------------------------------------------------------ figures
def tw(t, size):
    """rough Nunito ExtraBold width of a string"""
    w = 0
    for ch in t:
        w += 0.27 if ch == ' ' else 0.32 if ch in '()/.,' else 0.6
    return w * size


def sup2(f, x, y, base, u, rest='', size=12, c=INK, anchor='start'):
    wt = tw(base, size) + tw(u, size * 0.72) + 1 + tw(rest, size)
    x0 = x - wt / 2 if anchor == 'middle' else (x - wt if anchor == 'end' else x)
    f.text(x0, y, base, size, c, 'start')
    x1 = x0 + tw(base, size) + 0.5
    f.text(x1, y - size * 0.42, u, size * 0.72, c, 'start')
    if rest:
        f.text(x1 + tw(u, size * 0.72) + 1.5, y, rest, size, c, 'start')
    return f


def leg(p, items, size=12, gap=16):
    """legend row with superscripts: items = [(base, sup, rest, colour)]"""
    f = Fig(p.w, p.h + 20)
    f.raw('<g>' + ''.join(p.p) + '</g>')
    widths = [tw(b, size) + tw(u, size * 0.72) + tw(r, size) + gap for b, u, r, _ in items]
    x = (p.w - sum(widths) + gap) / 2
    for (b, u, r, c), wd in zip(items, widths):
        sup2(f, x, p.h + 14, b, u, r, size, c, 'start')
        x += wd
    return f


def f_bases():
    p = Plot(-3, 3, -1, 10, unit=42, uy=19, every=1, yevery=2, gstep=1)
    p.fn(lambda x: 2 ** x, -3, 3, BLUE, 2.6, steps=40)
    p.fn(lambda x: 3 ** x, -3, 2.1, GREEN, 2.6, steps=40)
    p.fn(lambda x: 10 ** x, -3, 1, RED, 2.6, steps=40)
    p.pt(0, 1, None, c=INK, r=4.6).text(p.X(0) + 10, p.Y(1) + 14, '(0, 1)', 12, INK, 'start')
    return leg(p, [('y = 2', 'x', '', BLUE), ('y = 3', 'x', '', GREEN), ('y = 10', 'x', '', RED)])


def f_mirror():
    p = Plot(-3, 3, -1, 8, unit=42, uy=21, every=1, yevery=1, gstep=1)
    p.g('k1 k2').fn(lambda x: 2 ** x, -3, 3, BLUE, 2.8, steps=40).pt(1, 2, None, c=BLUE, r=4).pt(2, 4, None, c=BLUE, r=4).end()
    p.g('k2').fn(lambda x: 0.5 ** x, -3, 3, RED, 2.8, steps=40).pt(-1, 2, None, c=RED, r=4).pt(-2, 4, None, c=RED, r=4)
    p.seg((-2, 4), (2, 4), GREY, 1.3, dash='3 3').end()
    p.pt(0, 1, None, c=INK, r=4.4)
    sup2(p, p.X(2.2), p.Y(6.2), 'y = 2', 'x', '', 12, BLUE, 'start')
    sup2(p, p.X(-0.45), p.Y(5.6), 'y = (1/2)', 'x', '', 12, RED, 'end')
    return p


def f_shift():
    p = Plot(-4, 3, -2, 8, unit=40, uy=20, every=1, yevery=1, gstep=1)
    p.fn(lambda x: 2 ** x, -4, 3, BLUE, 2.6, steps=40)
    p.fn(lambda x: 2 ** x + 3, -4, 2.3, GREEN, 2.6, steps=40)
    p.fn(lambda x: 2 ** x - 1, -4, 3, RED, 2.6, steps=40)
    p.seg((-4, 3), (3, 3), GREEN, 1.4, dash='6 4').seg((-4, -1), (3, -1), RED, 1.4, dash='6 4')
    p.pt(0, 1, None, c=BLUE, r=4).pt(0, 4, None, c=GREEN, r=4).pt(0, 0, None, c=RED, r=4)
    return leg(p, [('2', 'x', '', BLUE), ('2', 'x', ' + 3 (asymptote y = 3)', GREEN), ('2', 'x', ' − 1', RED)], 11.5)


def f_inverse():
    p = Plot(-3, 8, -3, 8, unit=26, uy=26, every=1, yevery=1, gstep=1)
    p.g('k1 k2 k3').fn(lambda x: 2 ** x, -3, 3, BLUE, 2.8, steps=40).pt(0, 1, None, c=BLUE, r=4).pt(1, 2, None, c=BLUE, r=4).pt(3, 8, None, c=BLUE, r=4).end()
    p.g('k2 k3').seg((-3, -3), (8, 8), GREY, 1.5, dash='6 4').end()
    p.g('k3').fn(lambda x: log(x, 2), 0.125, 8, RED, 2.8, steps=44).pt(1, 0, None, c=RED, r=4).pt(2, 1, None, c=RED, r=4).pt(8, 3, None, c=RED, r=4)
    p.text(p.X(5.2), p.Y(1.6), 'y = log₂ x', 12, RED, 'start').end()
    sup2(p, p.X(1.6), p.Y(6.2), 'y = 2', 'x', '', 12, BLUE, 'end').text(p.X(6.6), p.Y(7.4), 'y = x', 12, GREY)
    return p


def f_logs():
    p = Plot(0, 9, -3, 3.4, unit=34, uy=30, every=1, yevery=1, gstep=1)
    p.fn(lambda x: log(x, 2), 0.13, 9, BLUE, 2.6, steps=44)
    p.fn(lambda x: log(x, 3), 0.04, 9, GREEN, 2.6, steps=44)
    p.fn(lambda x: log(x, 10), 0.01, 9, ORANGE, 2.6, steps=44)
    p.fn(lambda x: log(x, 0.5), 0.13, 9, RED, 2.6, steps=44)
    p.pt(1, 0, None, c=INK, r=4.4)
    return with_legend(p, [('log₂ x', BLUE), ('log₃ x', GREEN), ('log x', ORANGE), ('log of base 1/2', RED)], 11.5)


def f_hopper():
    p = Plot(0, 4.4, 0, 16000, unit=60, uy=0.0125, pad=34, grid=False, every=1, yevery=4000, xlab='n', ylab='')
    p.text(p.X(0.15), p.Y(14600), 'A (hectares)', 12, GREY, 'start').text(p.X(4.2), p.Y(0) + 30, 'weeks', 11.5, GREY)
    for k in range(4000, 16001, 4000):
        p.seg((0, k), (4.4, k), '#e8e0d8', 1)
    p.g('k1 k2').fn(lambda n: 1000 * 2 ** n, 0, 4, BLUE, 2.8, steps=40)
    for n in range(5):
        p.pt(n, 1000 * 2 ** n, None, c=BLUE, r=3.8)
    p.end().g('k2').seg((0, 8000), (3, 8000), RED, 1.6, dash='5 4').seg((3, 0), (3, 8000), RED, 1.6, dash='5 4').pt(3, 8000, None, c=RED, r=5)
    p.text(p.X(3) - 8, p.Y(8000) - 10, '8000 ha after 3 weeks', 12, RED, 'end').end()
    return p


DIAGRAMS = {
    'bases': (f_bases(), 'Fig 4.2: y = 2^x, 3^x and 10^x', 147),
    'mirror': (f_mirror(), 'Growth and decay: y = 2^x and y = (1/2)^x', 149),
    'shift': (f_shift(), 'Exercise 4.3 Q2: moving y = 2^x up and down', 151),
    'inverse': (f_inverse(), 'y = 2^x and y = log₂ x are mirror images in y = x', 157),
    'logs': (f_logs(), 'Figs 4.7–4.9: logarithm graphs with different bases', 158),
    'hopper': (f_hopper(), 'Example 4.6(4): the grasshopper area doubles each week', 162),
}

# ------------------------------------------------------------------ 4.1
L1 = [
    TB('laws-tb', 'Laws of exponents ($a, b > 0$; $m, n$ real)', 143, ['Law', 'Rule', 'Example'],
       [['Product', '$a^m \\cdot a^n = a^{m + n}$', '$2^3 \\cdot 2^4 = 2^7$'],
        ['Quotient', '$a^m \\div a^n = a^{m - n}$', '$5^6 \\div 5^2 = 5^4$'],
        ['Power of a power', '$(a^m)^n = a^{mn}$', '$(3^2)^3 = 3^6$'],
        ['Power of a product', '$(ab)^n = a^n b^n$', '$(2x)^3 = 8x^3$'],
        ['Power of a quotient', '$\\left(\\frac{a}{b}\\right)^n = \\frac{a^n}{b^n}$', '$\\left(\\frac{2}{3}\\right)^2 = \\frac{4}{9}$'],
        ['Zero / negative', '$a^0 = 1$, $a^{-n} = \\frac{1}{a^n}$', '$2^{-3} = \\frac{1}{8}$'],
        ['Fractional', '$a^{\\frac{m}{n}} = \\left(\\sqrt[n]{a}\\right)^m$', '$27^{\\frac{2}{3}} = 3^2 = 9$']]),
    WK('ex-41a', 'Worked example: Example 4.1 (same base)', 143,
       'Simplify (a) $(3^2)^3 \\times 9^2 \\div 3^3$ (b) $(3ab)^3 \\times (2a^2)^2 \\div (2a)^3$.',
       ['(a) Write 9 as $3^2$: $3^6 \\times 3^4 \\div 3^3 = 3^{6 + 4 - 3} = 3^7$.',
        '(b) $27a^3b^3 \\times 4a^4 \\div 8a^3 = \\frac{108}{8} a^{3 + 4 - 3} b^3 = \\frac{27}{2} a^4 b^3$.'],
       '$3^7$; $\\frac{27}{2}a^4b^3$'),
    T('expeq-t', 'Solving exponential equations', 145,
      '**Method 1 — same base:** write both sides as powers of one base, then use $a^m = a^n \\Rightarrow m = n$. Example 4.2: $32^{x + 1} = 128 \\Rightarrow 2^{5x + 5} = 2^7 \\Rightarrow x = \\frac{2}{5}$.',
      '**Method 2 — substitution:** in $2^{2x} + 5(2^x) - 14 = 0$ put $u = 2^x$ (so $2^{2x} = u^2$): $u^2 + 5u - 14 = 0 \\Rightarrow u = 2$ or $u = -7$. $2^x$ is always positive, so only $2^x = 2$, $x = 1$.',
      '**Method 3 — logarithms** (when the bases cannot match): $2^x = 5 \\Rightarrow x = \\frac{\\log 5}{\\log 2} \\approx 2.32$.'),
    TB('cmp-41', 'Which method?', 145, ['Equation looks like', 'Method', 'Example'],
       [['both sides powers of 2, 3, 5 …', 'same base', '$8^x = 16^{3x + 9}$'],
        ['$a^{2x}$ and $a^x$ together', 'substitute $u = a^x$', '$3^{2x} - 8(3^x) + 15 = 0$'],
        ['bases do not match', 'take logs', '$10^x = 20$']]),
    T('=math11-u4-c01', '4.1 Exponential functions and their graphs', 146,
      'An **exponential function** is $f(x) = a^x$ with base $a > 0$, $a \\ne 1$; $x$ can be any real number. ($a = 1$ gives a constant; $a < 0$ fails, e.g. $(-16)^{\\frac{1}{2}}$ is not real.)',
      '**Properties of $y = a^x$:**',
      '- domain: **all real numbers**; range: **$y > 0$**. (The book\'s note (f) on p. 148 says "the domain is the set of positive real numbers" — that is the range.)',
      '- passes through $(0, 1)$; no x-intercept; the x-axis $y = 0$ is the horizontal asymptote.',
      '- $a > 1$: **increasing** (growth), the graph hugs the x-axis on the **left**. $0 < a < 1$: **decreasing** (decay), it hugs the x-axis on the **right**.',
      '- $y = \\left(\\frac{1}{a}\\right)^x = a^{-x}$ is the mirror image of $y = a^x$ in the y-axis.',
      '- $y = a^x + k$ moves the graph up $k$: y-intercept $1 + k$, asymptote $y = k$.'),
    DG('bases', 'Bigger base, steeper curve', 147, 'bases',
       'All pass through $(0, 1)$. For $x > 0$: $10^x > 3^x > 2^x$; for $x < 0$ the order reverses, e.g. $10^{-1} = 0.1 < 2^{-1} = 0.5$.'),
    ST('mirror', 'Growth vs decay (Exercise 4.3 Q1)', 149, 'mirror',
       [('$y = 2^x$: $(1, 2)$, $(2, 4)$; rises to the right.', 'k1'),
        ('$y = \\left(\\frac{1}{2}\\right)^x = 2^{-x}$: $(-1, 2)$, $(-2, 4)$ — the same points mirrored in the y-axis. It falls to the right.', 'k2')]),
    DG('shift', 'Vertical shifts', 151, 'shift',
       '$y = 2^x + 3$: same shape moved up 3; y-intercept 4; asymptote $y = 3$; range $y > 3$. $y = 2^x - 1$ passes through the origin; range $y > -1$.'),
    WK('ex-41b', 'Worked example: reading a graph (Example 4.4)', 151,
       'Use $y = 3^x$ to estimate (a) $3^{1.5}$ (b) $x$ with $3^x = 9.5$.',
       ['(a) $3^{1.5} = 3\\sqrt{3} \\approx 5.2$ (the book rounds to 5).', '(b) between $x = 2$ ($y = 9$) and slightly more: $x = \\frac{\\log 9.5}{\\log 3} \\approx 2.05$.'],
       '$\\approx 5.2$; $x \\approx 2.05$'),
    'math11-u4-c03', 'math11-u4-tblE1', 'math11-u4-wrkE2',
]

# ------------------------------------------------------------------ 4.2
L2 = [
    T('=math11-u4-c04', '4.2 Logarithms', 153,
      '**Definition:** for $a > 0$, $a \\ne 1$, $x > 0$: $$y = \\log_a x \\iff a^y = x$$ A logarithm **is an exponent**: "to what power must I raise $a$ to get $x$?"',
      '$\\log_2 16 = 4$ because $2^4 = 16$; $10^{-4} = 0.0001$ means $\\log_{10} 0.0001 = -4$.',
      '**Special values:** $\\log_a 1 = 0$, $\\log_a a = 1$, $\\log_a a^n = n$, $a^{\\log_a x} = x$.',
      '$\\log x$ with no base means base 10 (common logarithm).'),
    TB('loglaws-tb', 'Laws of logarithms ($m, n > 0$)', 153, ['Law', 'Rule', 'Example'],
       [['Product', '$\\log_a(mn) = \\log_a m + \\log_a n$', '$\\log_2 8 + \\log_2 4 = \\log_2 32 = 5$'],
        ['Quotient', '$\\log_a \\frac{m}{n} = \\log_a m - \\log_a n$', '$\\log 500 - \\log 5 = \\log 100 = 2$'],
        ['Power', '$\\log_a m^p = p \\log_a m$', '$\\log_3 81 = 4\\log_3 3 = 4$'],
        ['Change of base', '$\\log_a m = \\frac{\\log_b m}{\\log_b a}$', '$\\log_2 5 = \\frac{\\log 5}{\\log 2} \\approx 2.32$'],
        ['One-to-one', '$\\log_a m = \\log_a n \\Rightarrow m = n$', '$\\log_3 x = \\log_3 56 \\Rightarrow x = 56$']]),
    T('logeq-t', 'Solving logarithmic equations', 154,
      '1. Write the **domain** condition: every log argument $> 0$.',
      '2. Combine logs with the laws until you have $\\log_a(\\text{something}) = c$ or $\\log_a A = \\log_a B$.',
      '3. Convert: $A = a^c$, or $A = B$.',
      '4. Solve and **reject** answers outside the domain.',
      'Example 4.5(3): $\\log_2(x + 2) = 3$: $x > -2$; $x + 2 = 8$, $x = 6$.'),
    WK('ex-42a', 'Worked example: log₅(x + 1) + log₅(x − 3) = log₅ 5', 155,
       'Solve $\\log_5(x + 1) + \\log_5(x - 3) = \\log_5 5$.',
       ['Domain: $x > -1$ and $x > 3$, so $x > 3$.', 'Product law: $\\log_5[(x + 1)(x - 3)] = 1 \\Rightarrow (x + 1)(x - 3) = 5$.',
        '$x^2 - 2x - 8 = 0 \\Rightarrow (x - 4)(x + 2) = 0$.', '$x = -2$ is outside the domain.'],
       '$x = 4$'),
    WK('ex-42b', 'Worked example: Exercise 4.4 Q3 — what is wrong?', 156,
       '"$3 > 2$, so $3\\log_2\\frac{1}{2} > 2\\log_2\\frac{1}{2}$, so $\\frac{1}{8} > \\frac{1}{4}$." Find the error.',
       ['$\\log_2 \\frac{1}{2} = -1$ is **negative**.', 'Multiplying both sides of $3 > 2$ by a negative number reverses the sign: $3(-1) < 2(-1)$.', 'So the correct statement is $\\left(\\frac{1}{2}\\right)^3 < \\left(\\frac{1}{2}\\right)^2$, i.e. $\\frac{1}{8} < \\frac{1}{4}$.'],
       'the inequality must flip because $\\log_2 \\frac{1}{2} < 0$'),
    ST('inverse', 'The graph of y = log₂ x (Activity 4.7)', 157, 'inverse',
       [('Start from $y = 2^x$: points $(0, 1)$, $(1, 2)$, $(3, 8)$.', 'k1'),
        ('$\\log_2$ is the **inverse** of $2^x$, so its graph is the mirror image in $y = x$.', 'k2'),
        ('Swap coordinates: $(1, 0)$, $(2, 1)$, $(8, 3)$. Domain $x > 0$, range all reals, vertical asymptote $x = 0$.', 'k3')]),
    DG('logs', 'Logarithm graphs compared', 158, 'logs',
       'Every $y = \\log_a x$ passes through $(1, 0)$ and has the y-axis as asymptote. Base $> 1$: increasing (larger base → flatter). Base between 0 and 1: decreasing (red, base $\\frac{1}{2}$).'),
    TB('cmp-42', 'Exponential vs logarithmic function ($a > 1$)', 159, ['', '$y = a^x$', '$y = \\log_a x$'],
       [['domain', 'all reals', '$x > 0$'], ['range', '$y > 0$', 'all reals'], ['fixed point', '$(0, 1)$', '$(1, 0)$'],
        ['asymptote', '$y = 0$ (horizontal)', '$x = 0$ (vertical)'], ['grows', 'very fast', 'very slowly']]),
    'math11-u4-c09', 'math11-u4-mn2', 'math11-u4-c02', 'math11-u4-xtra2',
]

# ------------------------------------------------------------------ 4.3
L3 = [
    T('=math11-u4-c05', '4.3 Growth and decay models', 160,
      '**Repeated multiplication** gives exponential models. If a quantity is multiplied by $b$ every period: $N = A \\cdot b^n$ ($n$ periods).',
      '- **Growth by $r$%** per period: $b = 1 + \\frac{r}{100}$. Mice +20% a month: $P_n = 100(1.2)^n$.',
      '- **Decay by $r$%** per period: $b = 1 - \\frac{r}{100}$. Sugar −5% a day: $W_n = 20(0.95)^n$.',
      '- **Doubling / tripling** every $d$ days: $N = A \\cdot 2^{\\frac{t}{d}}$ or $A \\cdot 3^{\\frac{t}{d}}$. Example 4.6(1): $5 \\cdot 3^{\\frac{8}{2}} = 405$ Nakfa.',
      '- **Half-life** $h$: $N = A\\left(\\frac{1}{2}\\right)^{\\frac{t}{h}}$.',
      '**Finding the time:** take logs: $1000 \\cdot 2^n = 8000 \\Rightarrow 2^n = 8 \\Rightarrow n = \\frac{\\log 8}{\\log 2} = 3$.'),
    ST('hopper', 'Example 4.6(4): when does the area reach 8000 ha?', 162, 'hopper',
       [('$A_n = 1000 \\times 2^n$: 1000, 2000, 4000, 8000, … The graph shows $A = 8000$ at $n = 3$.', 'k1'),
        ('Algebra: $2^n = 8 \\Rightarrow n \\log 2 = \\log 8 \\Rightarrow n = 3$. (The book prints "$n = 4$" but then correctly says three weeks.)', 'k2')]),
    WK('ex-43a', 'Worked example: Example 4.6(5) — decay', 163,
       '$W = 200 \\times 2^{-\\frac{t}{1000}}$ grams. Find the original weight and the time to reach 2 g.',
       ['$t = 0$: $W = 200$ g.', '$2 = 200 \\times 2^{-0.001t} \\Rightarrow 2^{-0.001t} = 0.01$.', 'Logs: $-0.001t \\log 2 = \\log 0.01 = -2$, so $t = \\frac{2}{0.001 \\times 0.3010} \\approx 6645$ years.'],
       '200 g; about 6645 years'),
    WK('ex-43b', 'Worked example: Review 3 — doubling cells', 164,
       '700 cells double every 40 minutes. How many after 9 hours?',
       ['9 h = 540 min = $\\frac{540}{40} = 13.5$ doubling periods.', '$N = 700 \\times 2^{13.5} \\approx 700 \\times 11\\,585 \\approx 8.1$ million.'],
       'about 8.1 million cells'),
    RM('rm-43', 'Model checklist', 161,
       'Write: start value $A$, factor $b$ per period, number of periods $n$. Growth: $b > 1$. Decay: $0 < b < 1$.',
       'Percent → factor: +2.5% → 1.025; −5% → 0.95. Never use 0.05 as the factor.'),
    RM('=math11-u4-c14', 'Unit summary', 166,
       '$a^x$ ($a > 0$, $a \\ne 1$): domain all reals, range $y > 0$, through $(0, 1)$, asymptote $y = 0$; $a > 1$ grows, $0 < a < 1$ decays.',
       '$\\log_a x = y \\iff a^y = x$; domain $x > 0$; through $(1, 0)$; inverse of $a^x$.',
       'Product → add logs, quotient → subtract, power → multiply; change of base $\\frac{\\log m}{\\log a}$.',
       'Equations: same base, substitution or logs; for log equations check the domain.'),
    'math11-u4-c10', 'math11-u4-c11', 'math11-u4-c12',
]

LESSONS = {'math11-u4-l4-1': L1, 'math11-u4-l4-2': L2, 'math11-u4-l4-3': L3}

# ------------------------------------------------------------------ practice
a = QSet('4.1 Practice — exponents and exponential functions', 's41')
a.S(164, 'Review 1: simplify (a) $625^{\\frac{1}{4}}$ (b) $27^{-\\frac{2}{3}}$ (c) $\\left(\\frac{16}{49}\\right)^{-\\frac{1}{2}}$.', '5; $\\frac{1}{9}$; $\\frac{7}{4}$',
    ['Step 1: $625 = 5^4$.', 'Step 2: $27^{\\frac{1}{3}} = 3$, squared 9, negative → $\\frac{1}{9}$.', 'Step 3: negative power flips: $\\left(\\frac{49}{16}\\right)^{\\frac{1}{2}} = \\frac{7}{4}$.'],
    'Root first, then power.', [('$8^{\\frac{2}{3}}$?', '4.')])
a.S(144, 'Exercise 4.1 Q4: simplify $x^{a + b} \\times x^{2a + b} \\div x^{2a - 7}$.', '$x^{a + 2b + 7}$',
    ['Step 1: add then subtract exponents: $(a + b) + (2a + b) - (2a - 7)$.', 'Step 2: $= a + 2b + 7$.'], 'Bracket the exponent you subtract.', [('$x^{3n} \\div x^{n - 2}$?', '$x^{2n + 2}$.')])
a.S(145, 'Exercise 4.1 Q5(a): show $\\frac{3^{n + 1} + 3^{2n}}{3 + 3^n} = 3^n$.', 'shown',
    ['Step 1: numerator $3 \\cdot 3^n + 3^n \\cdot 3^n = 3^n(3 + 3^n)$.', 'Step 2: cancel $(3 + 3^n)$.'], 'Factor out the common power.', [('Simplify $\\frac{2^{n + 2} - 2^n}{2^n}$.', '3.')])
a.S(145, 'Exercise 4.2: solve (a) $2^{x^2 + 5x} = 4^{-3}$ (c) $3^{-x + 5} = \\frac{1}{81}$.', '$x = -2$ or $-3$; $x = 9$',
    ['Step 1: $4^{-3} = 2^{-6}$: $x^2 + 5x + 6 = 0$.', 'Step 2: $\\frac{1}{81} = 3^{-4}$: $-x + 5 = -4$.'], 'Same base, equate exponents.', [('$5^{x + 1} = 125$?', '$x = 2$.')])
a.S(145, 'Exercise 4.2(d): solve $625^{2x + 1} = 5(25^{x - 1})$.', '$x = -\\frac{5}{6}$',
    ['Step 1: $5^{4(2x + 1)} = 5^{1 + 2(x - 1)}$.', 'Step 2: $8x + 4 = 2x - 1 \\Rightarrow 6x = -5$.'], 'Write 625 and 25 as powers of 5.', [('$9^x = 3^{x + 4}$?', '$x = 4$.')])
a.S(145, 'Exercise 4.2(e): solve $2^{2x} - 3(2^x) - 10 = 0$.', '$x = \\log_2 5 \\approx 2.32$',
    ['Step 1: $u = 2^x$: $u^2 - 3u - 10 = 0 \\Rightarrow u = 5$ or $-2$.', 'Step 2: $2^x = -2$ is impossible; $2^x = 5$.'], 'Reject negative values of $a^x$.', [('$2^{2x} + 5(2^x) - 14 = 0$?', '$x = 1$.')])
a.S(152, 'Exercise 4.3 Q5: solve (c) $8^x = 16^{3x + 9}$ (d) $81^{2x - 3} = 27^x$.', '$x = -4$; $x = \\frac{12}{5}$',
    ['Step 1: $2^{3x} = 2^{12x + 36} \\Rightarrow -9x = 36$.', 'Step 2: $3^{8x - 12} = 3^{3x} \\Rightarrow 5x = 12$.'], 'Find a common base first.', [('$4^x = 8^{x - 1}$?', '$x = 3$.')])
a.S(152, 'Exercise 4.3 Q5: solve (f) $3^{2x} - 8(3^x) + 15 = 0$ (g) $\\left(\\frac{1}{3}\\right)^{x - 1} = 3^{2x + 4}$.', '$x = 1$ or $\\log_3 5$; $x = -1$',
    ['Step 1: $u = 3^x$: $(u - 3)(u - 5) = 0$.', 'Step 2: $3^{-(x - 1)} = 3^{2x + 4} \\Rightarrow -x + 1 = 2x + 4$.'], '$\\frac{1}{3} = 3^{-1}$.', [('$\\left(\\frac{1}{2}\\right)^x = 8$?', '$x = -3$.')])
a.S(151, 'Exercise 4.3 Q2: compare $y = 2^x + 3$ with $y = 2^x$.', 'same shape moved up 3; y-int 4; asymptote $y = 3$; range $y > 3$',
    ['Step 1: every $y$ value increases by 3.', 'Step 2: $2^0 + 3 = 4$.'], '$+k$ outside moves the asymptote too.', [('$y = 2^x - 1$?', 'down 1; through $(0, 0)$; asymptote $y = -1$.')])
a.M(148, 'The range of $y = a^x$ ($a > 0$, $a \\ne 1$) is', ['$y > 0$', 'all reals', '$y \\ge 1$', '$x > 0$'], 'A',
    ['Step 1: a positive base to any power is positive and never 0.'], 'Domain all reals, range positive.', [('Domain?', 'all real numbers.')])
a.M(149, 'Which function is decreasing?', ['$y = 0.8^x$', '$y = 1.2^x$', '$y = 3^x$', '$y = 10^x$'], 'A',
    ['Step 1: base between 0 and 1 → decay.'], 'Compare the base with 1.', [('Is $y = 2^{-x}$ decreasing?', 'Yes, it is $(0.5)^x$.')])
a.TF(148, 'The graph of $y = 5^x$ crosses the x-axis.', False, ['Step 1: $5^x > 0$ for every $x$; the x-axis is an asymptote.'], 'Exponentials never reach 0.', [('Does it cross the y-axis?', 'Yes, at $(0, 1)$.')])

b = QSet('4.2 Practice — logarithms', 's42')
b.S(152, 'Activity 4.6: (a) write $16 = 2^4$ in log form (b) write $4 = \\log_3 81$ in exponential form.', '$\\log_2 16 = 4$; $3^4 = 81$',
    ['Step 1: base 2, exponent 4.', 'Step 2: base 3 to the power 4 gives 81.'], 'The log is the exponent.', [('$10^{-2} = 0.01$?', '$\\log 0.01 = -2$.')])
b.S(155, 'Exercise 4.4 Q1: find (a) $\\log_5 625 + \\log_5 125$ (b) $\\log_2 \\sqrt[4]{2} + \\log_2 \\sqrt[5]{16}$.', '7; $\\frac{21}{20}$',
    ['Step 1: $4 + 3 = 7$.', 'Step 2: $\\frac{1}{4} + \\frac{4}{5} = \\frac{21}{20}$.'], 'Write roots as fractional powers. (Q1 b and c are printed identically in the book.)', [('$\\log_3 27 + \\log_3 9$?', '5.')])
b.S(156, 'Exercise 4.4 Q2: find (a) $3^{\\log_3 9}$ (b) $2^{\\log_2 \\frac{1}{8}}$ (c) $9^{\\log_9 9^3}$.', '9; $\\frac{1}{8}$; 729',
    ['Step 1: $a^{\\log_a x} = x$ each time.'], 'Exponential and log cancel.', [('$10^{\\log 7}$?', '7.')])
b.S(155, 'Solve $\\log_2(x + 2) = 3$.', '$x = 6$',
    ['Step 1: domain $x > -2$.', 'Step 2: $x + 2 = 2^3 = 8$.'], 'Convert to exponential form.', [('$\\log_3(2x + 1) = 2$?', '$x = 4$.')])
b.S(165, 'Review 12(b): solve $\\log_2(x - 9) + \\log_2(3x + 2) = 5$.', '$x = 10$',
    ['Step 1: domain $x > 9$.', 'Step 2: $(x - 9)(3x + 2) = 32 \\Rightarrow 3x^2 - 25x - 50 = 0 \\Rightarrow (3x + 5)(x - 10) = 0$.', 'Step 3: $-\\frac{5}{3}$ is outside the domain.'], 'Product law, then exponential form.', [('$\\log_5(x - 1) + \\log_5(2x + 1) = 1$?', '$x = 2$.')])
b.S(165, 'Review 12(c): solve $\\log_7 9 = 2\\log_7 x - \\log_7 25$.', '$x = 15$',
    ['Step 1: right side $= \\log_7 \\frac{x^2}{25}$.', 'Step 2: $\\frac{x^2}{25} = 9 \\Rightarrow x^2 = 225$; $x > 0$.'], 'Power law, then quotient law.', [('$\\log_3 x = \\log_3 8 + \\log_3 7$?', '$x = 56$.')])
b.S(165, 'Review 12(h): solve $\\log_4(x + 4) - \\log_4 5 = \\log_4(x - 1) - \\log_4 3$.', '$x = 8.5$',
    ['Step 1: $\\frac{x + 4}{5} = \\frac{x - 1}{3}$.', 'Step 2: $3x + 12 = 5x - 5 \\Rightarrow x = 8.5$ (domain $x > 1$ is fine).'], 'Same log on both sides → equal arguments.', [('$\\log x - \\log 2 = \\log 5$?', '$x = 10$.')])
b.S(165, 'Review 12(i) and (j): solve $\\log_3(x^2 + 6x) = 3$ and $\\log x + \\log(x - 3) = 1$.', '$x = 3$ or $-9$; $x = 5$',
    ['Step 1: $x^2 + 6x = 27 \\Rightarrow (x + 9)(x - 3) = 0$; both give $x^2 + 6x = 27 > 0$, so both are valid.', 'Step 2: $x(x - 3) = 10 \\Rightarrow (x - 5)(x + 2) = 0$; $x = -2$ fails $x > 3$.'],
    'Check the argument, not the sign of $x$.', [('$\\log_2(x^2 - 1) = 3$?', '$x = \\pm 3$.')])
b.S(165, 'Review 11: if $\\log_3 x = 4$, find $\\log_3 9x$ and $\\log_3 \\frac{81}{\\sqrt{x}}$.', '6; 2',
    ['Step 1: $\\log_3 9 + \\log_3 x = 2 + 4$.', 'Step 2: $\\log_3 81 - \\frac{1}{2}\\log_3 x = 4 - 2$.'], 'Split with the laws, then substitute. (The book prints "$\\log_3 9x = 4$" as the question — it should ask for the value.)', [('$\\log_3 x^2$?', '8.')])
b.S(157, 'State the domain, range, intercept and asymptote of $y = \\log_2 x$.', 'domain $x > 0$; range all reals; x-int 1; asymptote $x = 0$',
    ['Step 1: inverse of $2^x$: swap domain and range.', 'Step 2: $\\log_2 1 = 0$.'], 'Swap the facts of $2^x$.', [('Of $y = \\log_2 x + 2$?', 'same domain; x-int $\\frac{1}{4}$; asymptote $x = 0$.')])
b.M(153, '$\\log_a(m + n)$ equals', ['none of these in general', '$\\log_a m + \\log_a n$', '$\\log_a m \\cdot \\log_a n$', '$\\log_a(mn)$'], 'A',
    ['Step 1: the product law is about $\\log(mn)$, not $\\log(m + n)$. Test: $\\log 1 + \\log 1 = 0 \\ne \\log 2$.'], 'There is no sum law.', [('$\\log(mn)$?', '$\\log m + \\log n$.')])
b.M(158, 'All graphs $y = \\log_a x$ pass through', ['$(1, 0)$', '$(0, 1)$', '$(0, 0)$', '$(a, 0)$'], 'A',
    ['Step 1: $\\log_a 1 = 0$.'], 'Mirror of $(0, 1)$.', [('Through which point does $y = \\log_a x$ pass at height 1?', '$(a, 1)$.')])
b.TF(154, '$\\log_5 x$ is defined for $x = 0$.', False, ['Step 1: $5^y = 0$ has no solution.'], 'Arguments must be positive.', [('Is $\\log_5 1$ defined?', 'Yes, it is 0.')])

c = QSet('4.3 Practice — applications', 's43')
c.S(163, 'Exercise 4.6 Q1: Eritrea\'s population of 4.5 million grows 2.5% per year. How many more people after 2 years?', 'about 228 000',
    ['Step 1: $4.5 \\times 1.025^2 = 4.5 \\times 1.050625 \\approx 4.728$ million.', 'Step 2: increase $\\approx 0.228$ million.'], 'Growth factor 1.025.', [('After 1 year?', 'about 112 500 more.')])
c.S(163, 'Exercise 4.6 Q2: 50 m² of algae shrinks 5% a day. Area after 30 days?', 'about 10.7 m²',
    ['Step 1: $50 \\times 0.95^{30}$.', 'Step 2: $0.95^{30} \\approx 0.2146$; $50 \\times 0.2146 \\approx 10.7$.'], 'Decay factor 0.95.', [('After 10 days?', 'about 29.9 m².')])
c.S(164, 'Review 8: $I = (1.16)^t$ is the value of 1 Nakfa after $t$ years. Find $I$ for 3 and 8 years, and the value of 350 Nakfa after 4 years.', '1.56; 3.28; about 633.7 Nakfa',
    ['Step 1: $1.16^3 \\approx 1.561$; $1.16^8 \\approx 3.278$.', 'Step 2: $350 \\times 1.16^4 \\approx 350 \\times 1.8106 \\approx 633.7$.'], 'Multiply the start value by the factor.', [('1000 Nakfa for 2 years?', 'about 1345.6 Nakfa.')])
c.S(164, 'Review 9: $N = 100 \\times 10^{0.6}$. Find $N$.', 'about 398',
    ['Step 1: $10^{0.6} \\approx 3.981$.', 'Step 2: $\\times 100$.'], 'Use the $10^x$ key.', [('$100 \\times 10^{0.3}$?', 'about 200.')])
c.S(165, 'Review 14: $A = 128 \\times 10^{-0.016t}$ grams. When is $A = 25$ g?', 'about 44.3 hours',
    ['Step 1: $10^{-0.016t} = \\frac{25}{128} \\approx 0.1953$.', 'Step 2: $-0.016t = \\log 0.1953 \\approx -0.709$.', 'Step 3: $t \\approx 44.3$.'],
    'The book says "123 gm" but the formula starts at 128 g; we use the formula.', [('When is $A = 64$ g?', '$t = \\frac{\\log 2}{0.016} \\approx 18.8$ h.')])
c.S(165, 'Review 13: an equilateral triangle has area $A = \\frac{\\sqrt{3}}{4}s^2 = 12.6$ m². Find $s$.', 'about 5.39 m',
    ['Step 1: $s^2 = \\frac{4 \\times 12.6}{\\sqrt{3}} \\approx 29.1$.', 'Step 2: $s \\approx 5.39$.'], 'Isolate $s^2$ first.', [('Area $\\sqrt{3}$?', '$s = 2$.')])
c.S(161, 'Example 4.6(3): 20 kg of sugar, 5% used each day. How much is left after 3 days?', 'about 17.15 kg',
    ['Step 1: $W_3 = 20 \\times 0.95^3$.', 'Step 2: $0.95^3 = 0.857375$.'], 'Each day keeps 95%.', [('After $n$ days?', '$20(0.95)^n$.')])
c.S(162, 'A radioactive sample of 80 g has a half-life of 5 years. How much remains after 15 years, and when is 10 g left?', '10 g; after 15 years',
    ['Step 1: $15 \\div 5 = 3$ half-lives: $80 \\times \\left(\\frac{1}{2}\\right)^3 = 10$.'], 'Count half-lives.', [('64 g, half-life 3 days, after 12 days?', '4 g.')])
c.S(161, 'Kibrom starts with 5 Nakfa and triples it every 2 days. After how many days does he have 1215 Nakfa?', '10 days',
    ['Step 1: $5 \\times 3^n = 1215 \\Rightarrow 3^n = 243 = 3^5$.', 'Step 2: 5 periods × 2 days.'], 'Write the model, then same base.', [('Amount after 8 days?', '405 Nakfa.')])
c.M(162, '$1000 \\times 2^n = 8000$ gives', ['$n = 3$', '$n = 4$', '$n = 8$', '$n = 2$'], 'A',
    ['Step 1: $2^n = 8 = 2^3$. (The book prints $n = 4$ by mistake.)'], 'Divide by the start value first.', [('$500 \\times 2^n = 4000$?', '$n = 3$.')])
c.TF(161, 'A population growing by 20% a month is multiplied by 0.2 each month.', False, ['Step 1: it is multiplied by $1 + 0.2 = 1.2$.'], 'Factor = 1 + rate.', [('Decrease of 20%?', 'factor 0.8.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Exponential function', '$f(x) = a^x$, $a > 0$, $a \\ne 1$.', 146),
    ('Logarithm', '$\\log_a x$ is the power of $a$ that gives $x$.', 153),
    ('Common logarithm', '$\\log x = \\log_{10} x$.', 153),
    ('Growth factor', '$1 + r$ for growth at rate $r$ per period.', 161),
    ('Decay factor', '$1 - r$ for decrease at rate $r$ per period.', 161),
    ('Half-life', 'The time for a quantity to halve.', 162),
]
TIPS = [('Exponential: domain all reals, range y > 0.', 148), ('A log is an exponent: log₂ 8 = 3 because 2³ = 8.', 153),
        ('Log equations: write the domain first, reject answers outside it.', 155)]
IDEAS = [('expgraph', 'Graphs of a^x', 'l4_1', 'math11-u4-c01'), ('loglaws', 'Laws of logs', 'l4_2', 'math11-u4-md-loglaws-tb'),
         ('model', 'Growth and decay', 'l4_3', 'math11-u4-c05')]
