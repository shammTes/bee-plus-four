r"""Grade 11 Unit 6 — Business Mathematics (pp. 201-229)."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY

UID = 'math11-u6'
set_unit(UID)
LB, LG = '#dbe7f3', '#d6ece6'


# ------------------------------------------------------------------ figures
def f_growth():
    p = Plot(0, 12, 0, 3.4, unit=24, uy=60, every=2, yevery=1, gstep=1, xlab='t', ylab='A')
    p.g('k1 k2 k3').fn(lambda t: 1 + 0.1 * t, c=BLUE, w=2.6)
    p.text(p.X(11.6), p.Y(2.16) + 18, 'simple', 12, BLUE, 'end').end()
    p.g('k2 k3').fn(lambda t: 1.1 ** t, c=RED, w=2.6)
    p.text(p.X(9.4), p.Y(2.6) - 8, 'compound', 12, RED, 'end').end()
    p.g('k3').line(p.X(12), p.Y(2.2), p.X(12), p.Y(3.138), ORANGE, 2.2, dash='4 3')
    p.text(p.X(11.8), p.Y(2.7) + 4, '+938', 12, ORANGE, 'end').end()
    p.text(p.X(0.3), p.Y(3.1), 'thousand Nakfa', 11, GREY, 'start', False)
    return p


def f_dep():
    p = Plot(0, 5, 0, 5.6, unit=56, uy=36, every=1, yevery=1, gstep=1, xlab='yr', ylab='BV')
    p.g('k1 k2 k3').fn(lambda t: 5.1 - 0.84 * t, c=BLUE, w=2.6)
    for t in range(6):
        p.dot(p.X(t), p.Y(5.1 - 0.84 * t), BLUE, 3.2)
    p.text(p.X(2.6), p.Y(3.0) - 12, 'straight line', 12, BLUE, 'start').end()
    vals = [5.1 * 0.7 ** t for t in range(6)]
    p.g('k2 k3').curve([(t, v) for t, v in enumerate(vals)], RED, 2.4)
    for t, v in enumerate(vals):
        p.dot(p.X(t), p.Y(v), RED, 3.2)
    p.text(p.X(1.5), p.Y(1.6), 'reducing 30%', 12, RED, 'end').end()
    p.g('k3').line(p.X(1) + 7, p.Y(5.1), p.X(1) + 7, p.Y(4.26), BLUE, 3)
    p.line(p.X(1) - 7, p.Y(5.1), p.X(1) - 7, p.Y(3.57), RED, 3).end()
    p.text(p.X(4.9), p.Y(5.3), 'thousand Nakfa', 11, GREY, 'end', False)
    return p


def f_loan():
    W, H = 330, 210
    f = Fig(W, H)
    x0, y0, sx, sy = 40, 180, 90, 2.0

    def P(t, v):
        return (x0 + t * sx, y0 - v * sy)
    f.line(x0, y0, x0 + 3 * sx + 15, y0, INK, 1.6).line(x0, y0, x0, 20, INK, 1.6)
    for t in range(4):
        f.text(x0 + t * sx, y0 + 15, f'yr {t}', 10.5, GREY)
    for v in (25, 50, 75):
        f.line(x0 - 3, y0 - v * sy, x0 + 3, y0 - v * sy, INK, 1.2).text(x0 - 6, y0 - v * sy + 4, f'{v}k', 10.5, GREY, 'end', False)
    data = [(66.2, 72.82, 46.2), (46.2, 50.82, 24.2), (24.2, 26.62, 0)]
    for i, (a, b, c) in enumerate(data):
        k = ['k1 k2 k3', 'k2 k3', 'k3'][i]
        p, q, r = P(i, a), P(i + 1, b), P(i + 1, c)
        f.g(k).line(p[0], p[1], q[0], q[1], RED, 2.4).line(q[0], q[1], r[0], r[1], GREEN, 2.4, dash='5 3')
        f.dot(q[0], q[1], RED, 3.4).dot(r[0], r[1], GREEN, 3.4)
        f.text(q[0] - 6, q[1] - 8, f'{b * 1000:,.0f}', 10.5, RED, 'end')
        if c:
            f.text(r[0] + 8, r[1] + 16, f'{c * 1000:,.0f}', 10.5, GREEN, 'start')
        f.end()
    f.dot(*P(0, 66.2), INK, 3.4).text(x0 + 6, P(0, 66.2)[1] - 8, '66,200', 10.5, INK, 'start')
    f.text(W - 8, 30, 'red: + 10% interest', 11, RED, 'end').text(W - 8, 46, 'green: pay 26,620', 11, GREEN, 'end')
    return f


def f_alligation():
    f = Fig(330, 190)
    f.g('k1 k2 k3').text(60, 40, 'Wheat 8', 14, INK).text(60, 160, 'Sorghum 3', 14, INK)
    f.circle(165, 100, 26, PURPLE, 2, '#ECE6F5').text(165, 105, '5', 15, PURPLE).text(165, 64, 'mixture', 11, PURPLE).end()
    f.g('k2 k3').line(100, 48, 144, 84, GREY, 1.6).arrow(186, 116, 232, 150, GREY, 1.6, 7)
    f.line(100, 152, 144, 116, GREY, 1.6).arrow(186, 84, 232, 50, GREY, 1.6, 7)
    f.text(270, 44, '5 - 3 = 2', 13, BLUE).text(270, 164, '8 - 5 = 3', 13, GREEN).end()
    f.g('k3').text(270, 64, 'parts wheat', 11, BLUE).text(270, 184, 'parts sorghum', 11, GREEN).end()
    return f


def f_profit():
    f = Fig(330, 92)
    x0, w, y, h = 15, 300, 30, 30
    f.rect(x0, y, 2 * w / 5, h, BLUE, 1.6, LB).rect(x0 + 2 * w / 5, y, 3 * w / 5, h, GREEN, 1.6, LG)
    for i in range(1, 5):
        f.line(x0 + i * w / 5, y, x0 + i * w / 5, y + h, GREY, 1, dash='3 3')
    f.text(x0 + w / 5, y - 8, 'Belay 2 parts', 12, BLUE).text(x0 + 2 * w / 5 + 3 * w / 10, y - 8, 'Gilai 3 parts', 12, GREEN)
    f.text(x0 + w / 5, y + 20, '28,000', 12, BLUE).text(x0 + 2 * w / 5 + 3 * w / 10, y + 20, '42,000', 12, GREEN)
    f.text(x0 + w / 2, y + h + 22, 'each part = 70,000 / 5 = 14,000 Nakfa', 12, INK)
    return f


DIAGRAMS = {
    'growth': (f_growth(), '1000 Nakfa at 10% per year: simple vs compound', 203),
    'dep': (f_dep(), 'A 5100 Nakfa machine: two ways to depreciate', 215),
    'loan': (f_loan(), 'Example 6.5(3): the loan balance year by year', 212),
    'alligation': (f_alligation(), 'Example 6.9(3): the alligation cross', 226),
    'profit': (f_profit(), 'Example 6.8(3): sharing 70,000 Nakfa in the ratio 2 : 3', 221),
}

# ------------------------------------------------------------------ 6.1
L1 = [
    T('=math11-u6-c01', '6.1.1 Simple interest', 201,
      '**Words:** the **principal** $P$ is the money borrowed or saved; the **rate** $r$ is the percent charged per year; the **time** $t$ is in years; the **interest** $I$ is the extra money; the **amount** $A$ is principal + interest.',
      '$$I = Prt, \\qquad A = P + I = P(1 + rt)$$',
      'Write $r$ as a decimal ($5\\% = 0.05$) and $t$ in years (9 months $= \\frac{9}{12} = 0.75$ year).',
      '**Example 6.1:** 3500 Nakfa at 5% for 3 years: $I = 3500 \\times 0.05 \\times 3 = 525$ Nakfa, so $A = 4025$ Nakfa.'),
    TB('si-tb', 'One formula, four questions', 202, ['Unknown', 'Formula', 'Example'],
       [['interest $I$', '$I = Prt$', '$2500 \\times 0.06 \\times 3 = 450$'],
        ['rate $r$', '$r = \\frac{I}{Pt}$', '$\\frac{720}{6000 \\times 4} = 0.03 = 3\\%$'],
        ['time $t$', '$t = \\frac{I}{Pr}$', '$\\frac{450}{2500 \\times 0.06} = 3$ years'],
        ['principal $P$', '$P = \\frac{I}{rt}$', '$\\frac{210}{0.04 \\times 14} = 375$']]),
    T('=math11-u6-c07', '6.1.2 Compound interest', 202,
      'With **compound interest** the interest of each year is added to the principal, and next year\'s interest is worked out on the bigger sum: "interest on interest".',
      '**Where the formula comes from:** each year the money is multiplied by $(1 + r)$:',
      '- end of year 1: $P(1 + r)$;',
      '- end of year 2: $P(1 + r)(1 + r) = P(1 + r)^2$;',
      '- end of year $t$: $$A = P(1 + r)^t, \\qquad \\text{compound interest} = A - P.$$',
      'Banks pay interest on savings and charge a higher rate on loans; the difference is how a bank earns its income.'),
    TB('ex62-tb', 'Example 6.2 (corrected): 1000 Nakfa at 6% for 3 years', 203, ['Year', 'Simple: interest', 'Simple: amount', 'Compound: interest', 'Compound: amount'],
       [['1', '$1000 \\times 0.06 = 60$', '1060', '$1000 \\times 0.06 = 60$', '1060'],
        ['2', '$1000 \\times 0.06 = 60$', '1120', '$1060 \\times 0.06 = 63.60$', '1123.60'],
        ['3', '$1000 \\times 0.06 = 60$', '1180', '$1123.60 \\times 0.06 = 67.42$', '1191.02']]),
    T('ex62-note', 'Reading Example 6.2', 203,
      'Berhe (simple) gets **1180** Nakfa; Saliha (compound) gets **1191.02** Nakfa. The book\'s first table multiplies 1060 and 1123.60 by 0.06 although simple interest always uses the original 1000, and it says "the amount to be paid to Saliha is 1180" where it means Berhe. In the second table "= 06" should be "= 60" and "1123.06" should be "1123.60".'),
    ST('growth', 'Simple grows in a straight line, compound bends upward', 203, 'growth',
       [('Simple: the same 100 Nakfa is added every year, so the graph is a **straight line**: $A = 1000(1 + 0.1t)$.', 'k1'),
        ('Compound: each year the amount is **multiplied** by 1.1, so the graph curves upward: $A = 1000(1.1)^t$.', 'k2'),
        ('After 12 years: simple 2200, compound $1000 \\times 1.1^{12} \\approx 3138$ Nakfa, about 938 more. The longer the time, the bigger the gap.', 'k3')]),
    WK('ex63b', 'Worked example: Example 6.3(2) with logarithms (corrected)', 206,
       'Find the amount of 3000 Nakfa for 8 years at 10% per annum compounded annually.',
       ['$A = 3000(1.1)^8$.', 'Take logs: $\\log A = \\log 3 + 3 + 8\\log 1.1 = 0.4771 + 3 + 8(0.0414) = 3.8083$.',
        'Antilog: $A = 10^{3.8083} \\approx 6.43 \\times 10^3$.', 'Check by calculator: $1.1^8 = 2.14359$, $3000 \\times 2.14359 = 6430.77$.'],
       '$A \\approx 6430.77$ Nakfa. (The book uses $\\log 3 = 0.4471$ instead of 0.4771 and gets 6002 — wrong.)'),
    WK('ex63c', 'Worked example: how long? (Example 6.3(3))', 206,
       '5000 Nakfa at 5.2% compounded annually. When does it reach 20,000 Nakfa?',
       ['$20000 = 5000(1.052)^t$, so $(1.052)^t = 4$.', 'Logs bring the power down: $t \\log 1.052 = \\log 4$.',
        '$t = \\frac{0.6021}{0.0220} \\approx 27.4$.'],
       'about 27.4 years (the book lists "t = 3 years" as given data, but $t$ is the unknown)'),
    T('freq-t', 'Compounding more than once a year', 208,
      'If interest is added $n$ times a year, each period uses the rate $\\frac{r}{n}$ and there are $nt$ periods: $$A = P\\left(1 + \\frac{r}{n}\\right)^{nt}$$',
      '**Example 6.4(1):** 2500 Nakfa at 8% quarterly for 5 years: rate per quarter $0.02$, periods $20$: $A = 2500(1.02)^{20} = 3714.87$ Nakfa.',
      '**Example 6.4(2):** 1000 Nakfa at 9.5% half-yearly reaches 2529.77: $(1.0475)^{2t} = 2.52977$, so $2t = \\frac{\\log 2.52977}{\\log 1.0475} = 20$ and $t = 10$ years.',
      'More frequent compounding gives slightly more: 12% yearly multiplies by 1.12, but 12% monthly multiplies by $1.01^{12} \\approx 1.1268$ (an **effective rate** of 12.68%).'),
    TB('freq-tb', 'Periods and rate per period', 208, ['Compounded', '$n$', 'rate per period', 'periods in $t$ years'],
       [['annually', '1', '$r$', '$t$'], ['semi-annually', '2', '$\\frac{r}{2}$', '$2t$'], ['quarterly', '4', '$\\frac{r}{4}$', '$4t$'],
        ['monthly', '12', '$\\frac{r}{12}$', '$12t$'], ['daily', '365', '$\\frac{r}{365}$', '$365t$']]),
    'math11-u6-tblE1', 'math11-u6-c08', 'math11-u6-c03', 'math11-u6-chkE1', 'math11-u6-wrkE2', 'math11-u6-chk73',
    T('inst-t', '6.1.3 Instalment plan', 211,
      'An **instalment plan** lets you take an item now and pay for it (price + interest) in a sequence of equal payments. Often there is a **down payment** (deposit) first.',
      '$$\\text{total instalment cost} = \\text{down payment} + (\\text{number of payments}) \\times (\\text{payment})$$ $$\\text{charge for credit (interest)} = \\text{total instalment cost} - \\text{cash price}$$',
      '**Example 6.5(1):** TV 12,000 Nakfa; 2400 down and 48 payments of 230: total $2400 + 48 \\times 230 = 13{,}440$; credit charge 1440 Nakfa.',
      '**Example 6.5(2) (simple interest):** dress 2500, 10% deposit (250), balance 2250 at 7.5% for 2 years: $A = 2250(1 + 0.075 \\times 2) = 2587.50$; monthly payment $2587.50 \\div 24 = 107.81$ Nakfa.'),
    ST('loan', 'Example 6.5(3): equal yearly instalments with compound interest', 212, 'loan',
       [('Helen owes 66,200 at 10%. Year 1: $66200 \\times 1.1 = 72{,}820$; she pays $x = 26{,}620$, leaving 46,200.', 'k1'),
        ('Year 2: $46200 \\times 1.1 = 50{,}820$; pay 26,620, leaving 24,200.', 'k2'),
        ('Year 3: $24200 \\times 1.1 = 26{,}620$; the last payment clears it exactly.', 'k3')]),
    T('inst-eq', 'Finding the equal instalment', 212,
      'Move every payment to the **end**: the first payment earns interest for 2 years, the second for 1, the last for 0. Together they must equal the loan grown for 3 years:',
      '$$x(1.1)^2 + x(1.1) + x = 66200(1.1)^3$$',
      '$$x(1.21 + 1.1 + 1) = 88112.2 \\;\\Rightarrow\\; x = \\frac{88112.2}{3.31} = 26{,}620 \\text{ Nakfa}$$',
      'General rule (loan $P$, rate $r$ per period, $n$ payments): $x\\left[(1 + r)^{n-1} + \\dots + (1 + r) + 1\\right] = P(1 + r)^n$.',
      '(The book\'s check lists "10% of 33100", "10% of 3310", "10% of 1210" — it means 10% of 66,200, 46,200 and 24,200; the interest values printed are right.)'),
    T('dep-t', '6.1.4 Depreciation', 214,
      'Machines, cars and buildings (**fixed assets**) lose value with age and use. The loss is the **depreciation**; the value left is the **book value** (BV).',
      '$$\\text{depreciation} = \\text{original cost (OC)} - \\text{book value (BV)}$$',
      '**Straight-line method:** the same amount every year: $$\\text{annual depreciation} = \\frac{OC - BV}{t}, \\quad \\text{rate} = \\frac{\\text{annual depreciation}}{OC} \\times 100\\%, \\quad BV = OC(1 - rt).$$',
      '**Diminishing (reducing) value method:** the same **percent** of last year\'s value each year: $$BV = OC\\left(1 - r\\right)^t.$$ It is compound interest run backwards.'),
    TB('sl-tb', 'Activity 6.6 completed: straight line (5100 → 900 in 5 years)', 215, ['Year', 'Book value', 'Annual dep.', 'Accumulated dep.'],
       [['0', '5100', '—', '—'], ['1', '4260', '840', '840'], ['2', '3420', '840', '1680'], ['3', '2580', '840', '2520'], ['4', '1740', '840', '3360'], ['5', '900', '840', '4200']]),
    TB('db-tb', 'Activity 6.7 completed: 40% diminishing value (cost 4800)', 217, ['Year', 'Book value', 'Annual dep.', 'Accumulated dep.'],
       [['0', '4800', '—', '—'], ['1', '2880', '1920.00', '1920.00'], ['2', '1728', '1152.00', '3072.00'], ['3', '1036.80', '691.20', '3763.20'],
        ['4', '622.08', '414.72', '4177.92'], ['5', '373.25', '248.83', '4426.75']]),
    T('db-note', 'How to fill a diminishing schedule', 217,
      'Each row: depreciation $= 40\\% \\times$ last book value; new book value $=$ last book value $-$ depreciation (or simply $\\times 0.6$); accumulated $=$ last accumulated $+$ this year\'s depreciation. Check: accumulated $=$ 4800 $-$ book value. (The book prints the year-4 accumulated depreciation as 3177.92; it is 4177.92.)'),
    ST('dep', 'Comparing the two methods', 215, 'dep',
       [('Straight line: 5100 → 900 by 840 every year — a straight line.', 'k1'),
        ('Reducing 30% a year: $5100 \\times 0.7^t$ — big drops first, small later; after 5 years about 857.', 'k2'),
        ('Year 1 loss: 840 (straight line) vs 1530 (reducing). Cars really lose most value early, so the reducing method is more realistic for them.', 'k3')]),
    WK('ex66', 'Worked example: Example 6.6(1)', 215,
       'A tape recorder cost 5600 Nakfa; after 2 years its value is estimated at 4200 Nakfa. It is sold for 5000. Find (a) annual depreciation (b) annual rate (c) percent gain on the estimated value.',
       ['Depreciation $= 5600 - 4200 = 1400$; per year $1400 \\div 2 = 700$.', 'Rate $= \\frac{700}{5600} \\times 100\\% = 12.5\\%$.', 'Gain $= 5000 - 4200 = 800$; $\\frac{800}{4200} \\times 100\\% \\approx 19.05\\%$.'],
       '700 Nakfa; 12.5%; about 19.05%'),
    WK('ex67', 'Worked example: Example 6.7 (corrected)', 217,
       'A plant costs 240,000 Nakfa and depreciates 15% a year on the reducing value. Value after 3 years?',
       ['Year 1: $15\\% \\times 240000 = 36000$; value 204,000.', 'Year 2: $15\\% \\times 204000 = 30600$; value 173,400.',
        'Year 3: $15\\% \\times 173400 = 26010$ (the book prints 2610); value 147,390.', 'Formula check: $240000(0.85)^3 = 240000 \\times 0.614125 = 147390$.'],
       '147,390 Nakfa'),
    'math11-u6-chkE2',
]

# ------------------------------------------------------------------ 6.2
L2 = [
    T('=math11-u6-c02', '6.2 Partnership: four ways to share profit', 220,
      'A **partnership** is a business owned by two or more people who share management and profit. The money each puts in is the **capital** (investment).',
      '1. **Equal shares:** profit $\\div$ number of partners (Example 6.8(1): $99000 \\div 3 = 33000$).',
      '2. **Agreed ratio** $a : b$: one part $= \\frac{\\text{profit}}{a + b}$ (Example 6.8(2): 2 : 3 of 20,000 gives 8000 and 12,000).',
      '3. **Ratio of capital** (Example 6.8(3)): each gets $\\frac{\\text{own capital}}{\\text{total capital}} \\times$ profit.',
      '4. **Salary or interest first, then ratio** (Example 6.8(4)): take the salaries/interest out first and share only what is left.',
      'If money stays in for different times, use **capital × time** as the share ratio.'),
    DG('profit', 'Example 6.8(3) as a bar', 221, 'profit',
       'Belay 60,000 and Gilai 90,000: ratio $60 : 90 = 2 : 3$, so 5 equal parts of $70000 \\div 5 = 14000$. Belay $2 \\times 14000 = 28000$, Gilai $3 \\times 14000 = 42000$.'),
    WK('ex68d', 'Worked example: salary first (Example 6.8(4))', 222,
       'Goitom (150,000) and Abdella (300,000) own a restaurant; the manager is paid 30,000 a year. Profit 90,000. Share it by investment.',
       ['Pay the salary first: $90000 - 30000 = 60000$ left.', 'Ratio $150000 : 300000 = 1 : 2$ (3 parts of 20,000).', 'Goitom $1 \\times 20000$, Abdella $2 \\times 20000$.'],
       'Goitom 20,000 Nakfa; Abdella 40,000 Nakfa'),
    'math11-u6-c09', 'math11-u6-c10', 'math11-u6-chk75', 'math11-u6-wrk2', 'math11-u6-pc2',
    T('mix-t', '6.2 Mixtures', 223,
      'A mixture problem asks how much of each ingredient to use. Two standard tools:',
      '**1. A table with two equations.** One equation for the **total amount**, one for the **amount of the pure part** (percent × quantity). Example 6.9(1): $x + y = 100$ and $0.30x + 0.55y = 0.40 \\times 100$ give $x = 60$ kg, $y = 40$ kg.',
      '**2. Alligation (price mixtures):** to mix a cheap item (price $c$) and a dear item (price $d$) to get a mean price $m$: $$\\text{cheap} : \\text{dear} = (d - m) : (m - c).$$',
      '**3. Keep the unchanged part fixed:** when you add only one ingredient, the other stays the same amount — work with that one (Example 6.9(4)).'),
    ST('alligation', 'The alligation cross', 225, 'alligation',
       [('Write the two prices on the left and the mixture price 5 in the middle.', 'k1'),
        ('Subtract along the diagonals (always bigger minus smaller): $8 - 5 = 3$ and $5 - 3 = 2$.', 'k2'),
        ('Each difference lands opposite its own price: wheat gets 2 parts, sorghum 3 parts. **wheat : sorghum = 2 : 3.** Check: $\\frac{2 \\times 8 + 3 \\times 3}{5} = 5$.', 'k3')]),
    WK('ex69b', 'Worked example: Example 6.9(2)', 224,
       'How many litres of a 20% solution must be added to 40 litres of an 80% solution to get a 50% mixture?',
       ['Let $x$ litres of 20% be added. Pure part: $0.2x + 0.8 \\times 40 = 0.2x + 32$.', 'The mixture has $x + 40$ litres at 50%: $0.5(x + 40)$.',
        '$0.5x + 20 = 0.2x + 32 \\Rightarrow 0.3x = 12 \\Rightarrow x = 40$.', 'Alligation check: $(80 - 50) : (50 - 20) = 30 : 30 = 1 : 1$.'],
       '40 litres of the 20% solution (mixed with the 40 litres of the 80% solution — the book wrongly says "55%")'),
    WK('ex69d', 'Worked example: the part that does not change (Example 6.9(4))', 226,
       '120 cm³ of soil-and-fertiliser is 10% fertiliser. How much fertiliser must be added to make it 28% fertiliser?',
       ['Soil (does not change) $= 90\\% \\times 120 = 108$ cm³.', 'In the new mixture soil is $100\\% - 28\\% = 72\\%$: $0.72 \\times \\text{new total} = 108$.', 'New total $= 150$ cm³, so add $150 - 120 = 30$ cm³.'],
       '30 cm³ of fertiliser'),
    TB('meth-tb', 'Which method?', 224, ['Problem type', 'Best method', 'Why'],
       [['percent/strength of two solutions', 'two equations or alligation', 'pure part is conserved'],
        ['price per kg of two goods', 'alligation', 'quick ratio'],
        ['add only water / only one ingredient', 'keep the other part fixed', 'one equation']]),
    'math11-u6-c04', 'math11-u6-c11', 'math11-u6-xtra2', 'math11-u6-chk74', 'math11-u6-wrk1',
    RM('summary-t', 'Unit summary', 229,
       'Simple: $I = Prt$, $A = P(1 + rt)$. Compound: $A = P(1 + \\frac{r}{n})^{nt}$.',
       'Instalments: total cost $-$ cash price $=$ credit charge; equal yearly payments: grow each payment to the end.',
       'Depreciation: straight line $BV = OC(1 - rt)$; diminishing $BV = OC(1 - r)^t$.',
       'Partnership: share in the agreed ratio (capital, capital × time), after salaries/interest.',
       'Mixtures: conserve the pure part; alligation cheap : dear $= (d - m) : (m - c)$.'),
]

LESSONS = {'math11-u6-l6-1': L1, 'math11-u6-l6-2': L2}

# ------------------------------------------------------------------ practice
a = QSet('6.1 Practice — simple and compound interest', 's61')
a.S(202, 'Exercise 6.1 Q1: find the missing value: (a) $P = 6000$, $T = 4$, $I = 720$; (b) $P = 2500$, $R = 6\\%$, $I = 450$; (c) $P = 1750$, $R = 3\\%$, $T = 5$; (d) $R = 4\\%$, $T = 14$, $I = 210$.', '(a) 3% (b) 3 years (c) 262.50 (d) 375',
    ['Step 1: (a) $r = \\frac{720}{6000 \\times 4} = 0.03$.', 'Step 2: (b) $t = \\frac{450}{2500 \\times 0.06} = 3$.', 'Step 3: (c) $I = 1750 \\times 0.03 \\times 5 = 262.5$.', 'Step 4: (d) $P = \\frac{210}{0.04 \\times 14} = 375$.'],
    'Rearrange $I = Prt$ for the missing letter.', [('$P = 4000$, $R = 5\\%$, $I = 600$: $T$?', '3 years.')])
a.S(202, 'Exercise 6.1 Q2: 10,000 Nakfa at 6% simple interest for 5 years. Amount?', '13,000 Nakfa',
    ['Step 1: $I = 10000 \\times 0.06 \\times 5 = 3000$.', 'Step 2: $A = 10000 + 3000$.'], '$A = P(1 + rt)$.', [('For 8 years?', '14,800 Nakfa.')])
a.S(202, 'Find the simple interest on 4500 Nakfa at 8% for 9 months.', '270 Nakfa',
    ['Step 1: $t = \\frac{9}{12} = 0.75$.', 'Step 2: $I = 4500 \\times 0.08 \\times 0.75$.'], 'Months ÷ 12.', [('For 4 months?', '120 Nakfa.')])
a.S(213, 'Exercise 6.4 Q1: 15,000 Nakfa grew to 18,000 Nakfa in 5 years at simple interest. Rate?', '4%',
    ['Step 1: $I = 3000$.', 'Step 2: $r = \\frac{3000}{15000 \\times 5} = 0.04$.'], 'Interest first, then $r = \\frac{I}{Pt}$.', [('Grew to 21,000?', '8%.')])
a.S(207, 'Exercise 6.2 Q1–Q3: compound interest on (1) 400 Nakfa, 2 years, 5%; (2) 1000 Nakfa, 3 years, 6%. (3) Amount of 500 Nakfa for 4 years at 6%.', '41; 191.02; 631.24',
    ['Step 1: $400(1.05)^2 = 441$, interest 41.', 'Step 2: $1000(1.06)^3 = 1191.02$, interest 191.02.', 'Step 3: $500(1.06)^4 = 631.24$.'], 'Interest $= A - P$.', [('400 Nakfa, 3 years, 5%?', 'interest 63.05.')])
a.S(207, 'Exercise 6.2 Q4–Q5: 5000 Nakfa for 3 years at 4%. As the lender, which would you prefer? As the borrower?', 'lender: compound; borrower: simple',
    ['Step 1: simple $A = 5600$.', 'Step 2: compound $A = 5000(1.04)^3 = 5624.32$.', 'Step 3: the lender gains 24.32 more with compound; the borrower pays less with simple.'], 'Compound ≥ simple for $t \\ge 1$.', [('For exactly 1 year?', 'same: 5200.')])
a.S(210, 'Exercise 6.3 Q1–Q2: number of periods and rate per period: (a) 4 years, 6%, half-yearly (b) 2 years, 8%, quarterly (c) 1.5 years, 12%, monthly. Also 8% per year as half-yearly, quarterly, monthly rates.', '(a) 8 at 3% (b) 8 at 2% (c) 18 at 1%; 4%, 2%, 0.67%',
    ['Step 1: periods $= nt$.', 'Step 2: rate per period $= \\frac{r}{n}$.'], 'Divide the rate, multiply the time.', [('3 years at 12% quarterly?', '12 periods at 3%.')])
a.S(210, 'Exercise 6.3 Q3–Q4: compound interest on (a) 4000 Nakfa, 1.5 years, 8% half-yearly; (b) 800 Nakfa, 1 year, 6% quarterly.', '(a) 499.46 (b) 49.09',
    ['Step 1: (a) $4000(1.04)^3 = 4499.46$.', 'Step 2: (b) $800(1.015)^4 = 849.09$.'], 'Rate per period and number of periods first.', [('(a) yearly at 8% for 1 year?', '320.')])
a.S(210, 'Exercise 6.3 Q5–Q7: (5) interest on 2500 Nakfa, 5 years, 4% half-yearly; (6) amount of 20,000 Nakfa, 8 years, 4% quarterly; (7) interest on 25,000 Nakfa, 12 years, 6% half-yearly.', '547.49; 27,498.82; 25,819.85',
    ['Step 1: $2500(1.02)^{10} = 3047.49$.', 'Step 2: $20000(1.01)^{32} = 27498.82$.', 'Step 3: $25000(1.03)^{24} = 50819.85$; subtract 25,000.'], 'Use the $x^y$ key.', [('2500 at 4% yearly for 5 years?', 'interest 541.63.')])
a.S(228, 'Review Q1–Q2: (1) amount of 10,000 Nakfa for 6 years at 5% compounded annually; (2) compound minus simple interest on 14,000 Nakfa for 5 years at 6%.', '13,400.96; 535.16',
    ['Step 1: $10000(1.05)^6 = 13400.96$.', 'Step 2: CI $= 14000(1.06^5 - 1) = 4735.16$; SI $= 4200$.'], 'Difference grows with time.', [('Difference for 2 years?', '50.40.')])
a.S(228, 'Review Q3: how much must be deposited now at 6% compound interest to have 8000 Nakfa in 5 years?', '5978.07 Nakfa',
    ['Step 1: $P(1.06)^5 = 8000$.', 'Step 2: $P = \\frac{8000}{1.338226}$.'], 'Present value: divide by the growth factor.', [('10,000 Nakfa in 3 years at 5%?', '8638.38 Nakfa.')])
a.S(228, 'Review Q4–Q5: (4) 3500 Nakfa compounded quarterly becomes 5735.16 in 5 years: interest? rate? (5) Population 4 million grows 2.5% a year: after 2 years?', '2235.16 (10% per year); 4,202,500',
    ['Step 1: $5735.16 - 3500 = 2235.16$; $(1.6386)^{1/20} = 1.025$ per quarter, so 10% per year.', 'Step 2: $4000000(1.025)^2$.'], 'Population growth = compound interest.', [('After 3 years?', 'about 4,307,563.')])
a.S(206, 'How long does money take to double at 8% compounded yearly?', 'about 9 years',
    ['Step 1: $(1.08)^t = 2$.', 'Step 2: $t = \\frac{\\log 2}{\\log 1.08} = \\frac{0.3010}{0.0334} \\approx 9$.'], 'Rule of 72: $72 \\div 8 = 9$.', [('At 6%?', 'about 12 years.')])
a.M(209, 'Which gives the most after 1 year on 1000 Nakfa at 12% per year?', ['monthly compounding', 'yearly compounding', 'simple interest', 'half-yearly compounding'], 'A',
    ['Step 1: monthly $1000(1.01)^{12} = 1126.83$; half-yearly 1123.60; yearly and simple 1120.'], 'More periods ⇒ more interest.', [('Effective rate of 12% monthly?', 'about 12.68%.')])
a.TF(203, 'With simple interest the interest in year 3 is bigger than in year 1.', False,
     ['Step 1: simple interest is $Pr$ every year, always on the original principal.'], 'Only compound interest grows each year.', [('With compound interest?', 'True.')])

b = QSet('6.1 Practice — instalments and depreciation', 's62')
b.S(213, 'Exercise 6.4 Q2: a cupboard costs 8500 Nakfa; on instalments over 3 years the price rises by 17.5%. (a) total (b) interest (c) yearly instalment.', '9987.50; 1487.50; 3329.17',
    ['Step 1: $8500 \\times 1.175 = 9987.50$.', 'Step 2: $9987.50 - 8500$.', 'Step 3: $9987.50 \\div 3$.'], 'Total first, then divide.', [('Rise 12% over 2 years?', 'total 9520, 4760 a year.')])
b.S(213, 'Exercise 6.4 Q3: a radio costs 8500 Nakfa; 1500 down and 48 payments of 184.34. Total and interest?', '10,348.32; 1848.32',
    ['Step 1: $1500 + 48 \\times 184.34 = 10348.32$.', 'Step 2: $10348.32 - 8500$.'], 'Total instalment cost − cash price.', [('36 payments of 220 instead?', 'total 9420, interest 920.')])
b.S(213, 'Exercise 6.4 Q4: wheat worth 3750 Nakfa, nothing down, 12 payments of 330.16. Annual (simple) interest rate?', 'about 5.65%',
    ['Step 1: total $12 \\times 330.16 = 3961.92$.', 'Step 2: interest 211.92 for 1 year: $\\frac{211.92}{3750} \\approx 0.0565$.'], 'Rate = interest ÷ (principal × years).', [('Payments of 325?', 'interest 150, rate 4%.')])
b.S(214, 'Exercise 6.4 Q5: a 500,000 Nakfa house; 50% paid now, the rest in 3 equal yearly instalments at 5% compound. Instalment?', 'about 91,802.14 Nakfa',
    ['Step 1: loan 250,000.', 'Step 2: $x(1.05^2 + 1.05 + 1) = 250000(1.05)^3$.', 'Step 3: $x = \\frac{289406.25}{3.1525}$.'], 'Grow every payment to the end.', [('Loan 100,000 at 10%, 2 payments?', '57,619.05.')])
b.S(214, 'Exercise 6.4 Q6: what loan is repaid by 3 yearly instalments of 4000 Nakfa at 5% compound?', 'about 10,892.99 Nakfa',
    ['Step 1: bring each payment back: $\\frac{4000}{1.05} + \\frac{4000}{1.05^2} + \\frac{4000}{1.05^3}$.', 'Step 2: $3809.52 + 3628.12 + 3455.35$.'], 'Present value of each payment.', [('2 instalments of 4000?', '7437.64.')])
b.S(228, 'Review Q9: 23,400 Nakfa borrowed at 9% compound, repaid in 6 equal yearly instalments. Instalment?', 'about 5216.32 Nakfa',
    ['Step 1: $x \\cdot \\frac{1.09^6 - 1}{0.09} = 23400(1.09)^6$.', 'Step 2: $x = \\frac{23400 \\times 0.09}{1 - 1.09^{-6}}$.'], 'Same idea as Helen\'s loan, longer list.', [('Over 3 years?', 'about 9244.25.')])
b.S(228, 'Review Q8: a 16,000 Nakfa fridge, no deposit, 333.34 Nakfa a month for 5 years. Simple interest rate?', '5% per year',
    ['Step 1: total $333.34 \\times 60 = 20000.40$.', 'Step 2: interest about 4000: $\\frac{4000}{16000 \\times 5} = 0.05$.'], 'Straight-line here means simple interest.', [('Over 4 years at the same total?', '6.25%.')])
b.S(219, 'Exercise 6.5 Q1–Q2: (1) a car 150,000 → 70,000 in 5 years: annual depreciation and rate? (2) a machine 8000, scrap 1280 after 12 years: rate?', '16,000 and 10.67%; 7%',
    ['Step 1: $\\frac{80000}{5} = 16000$; $\\frac{16000}{150000} \\approx 10.67\\%$.', 'Step 2: $\\frac{6720}{12} = 560$; $\\frac{560}{8000} = 7\\%$.'], 'Rate is on the original cost.', [('60,000 → 6000 in 9 years?', '6000 a year, 10%.')])
b.S(220, 'Exercise 6.5 Q3: 20 computers at 40,000 each; BV 4000 each after 12 years (straight line). Annual depreciation and rate?', '3000 per computer (60,000 for all 20); 7.5%',
    ['Step 1: $\\frac{36000}{12} = 3000$.', 'Step 2: $\\frac{3000}{40000} = 7.5\\%$.'], 'Work per item, then multiply.', [('BV 8000 after 8 years?', '4000, 10%.')])
b.S(220, 'Exercise 6.5 Q4–Q5: (4) equipment 100,000, value falls 12% a year: value after 10 years? (5) TV 15,000, 10% a year, sold after 5 years for 10,500: gain or loss on the book value?', '27,850.10; gain 1642.65',
    ['Step 1: $100000(0.88)^{10}$.', 'Step 2: $15000(0.9)^5 = 8857.35$; $10500 - 8857.35$.'], 'Diminishing: multiply by $(1 - r)$ each year.', [('TV after 3 years?', '10,935.')])
b.S(229, 'Review Q10: a 120,000 Nakfa car loses 15% a year. After 4 years it is sold at 30% above its value then. Gain or loss against the cost?', 'loss of about 38,567 Nakfa',
    ['Step 1: $120000(0.85)^4 = 62640.75$.', 'Step 2: price $1.3 \\times 62640.75 = 81432.98$.', 'Step 3: $120000 - 81432.98$.'], 'Compare with the original cost, not the book value.', [('Sold at 50% above?', 'loss about 26,039.')])
b.S(216, 'Example 6.6(2): cost 12,500, value 2300 after 7 years. Simple rate of depreciation?', 'about 11.7%',
    ['Step 1: $2300 = 12500(1 - 7r)$.', 'Step 2: $7r = 1 - 0.184 = 0.816$, $r \\approx 0.1166$.'], '$BV = OC(1 - rt)$.', [('Value 5000 after 5 years?', '12%.')])
b.M(214, 'A car of 80,000 Nakfa depreciates 20% a year (reducing value). After 3 years it is worth', ['40,960', '32,000', '48,000', '51,200'], 'A',
    ['Step 1: $80000 \\times 0.8^3 = 80000 \\times 0.512$.'], 'Not $80000 - 3 \\times 16000$.', [('After 2 years?', '51,200.')])
b.TF(215, 'With straight-line depreciation the book value falls by the same percent every year.', False,
     ['Step 1: it falls by the same **amount**; as the value shrinks that amount is a bigger percent.'], 'Same amount = straight line; same percent = diminishing.', [('Diminishing value falls by the same amount?', 'False.')])

c = QSet('6.2 Practice — partnership and mixtures', 's63')
c.S(222, 'Exercise 6.6 Q1–Q2: (1) 5 doctors share 140,000 equally. (2) Capitals 25,000 and 15,000 share a profit of 30,000.', '28,000 each; 18,750 and 11,250',
    ['Step 1: $140000 \\div 5$.', 'Step 2: ratio 5 : 3, part $= 30000 \\div 8 = 3750$.'], 'Simplify the ratio first.', [('Capitals 20,000 and 30,000?', '12,000 and 18,000.')])
c.S(223, 'Exercise 6.6 Q3: profits/losses in the ratio 2 : 3 : 7. (a) Share a profit of 9000. (b) How is a loss shared?', '1500, 2250, 5250; same ratio 2 : 3 : 7',
    ['Step 1: 12 parts; one part $= 750$.', 'Step 2: losses follow the same agreed ratio.'], 'Total parts $= 2 + 3 + 7$.', [('A loss of 2400?', '400, 600, 1400.')])
c.S(223, 'Exercise 6.6 Q4: Salem 60,000, Dawd 30,000; each takes 10% interest on capital, the rest is split equally. Profit 15,000.', 'Salem 9000; Dawd 6000',
    ['Step 1: interest 6000 and 3000.', 'Step 2: left $15000 - 9000 = 6000$, 3000 each.', 'Step 3: add.'], 'Take out interest first.', [('Profit 12,000?', 'Salem 7500, Dawd 4500.')])
c.S(223, 'Exercise 6.6 Q5: capitals 14,000, 17,000, 33,000. 10% of a 6000 profit goes to a national programme; the rest by capital.', '1181.25; 1434.38; 2784.38',
    ['Step 1: $6000 - 600 = 5400$.', 'Step 2: ratio 14 : 17 : 33 (64 parts), part $= 84.375$.'], 'Total parts first.', [('Profit 12,800?', '2520, 3060, 5940.')])
c.S(228, 'Review Q6–Q7: (6) capitals 10,000, 20,000, 20,000; profit 15,600. (7) Winta invests 360,000 and gets 10% return first; the rest of a 90,000 profit is split 2 : 3 (Winta : Nejat).', '3120, 6240, 6240; Winta 57,600, Nejat 32,400',
    ['Step 1: ratio 1 : 2 : 2, part 3120.', 'Step 2: return 36,000; left 54,000: Winta 21,600, Nejat 32,400.', 'Step 3: Winta $36000 + 21600$.'], 'Return first, then ratio.', [('Profit 60,000 in Q7?', 'Winta 45,600, Nejat 14,400.')])
c.S(229, 'Review Q11: Amir and Ghirmay invest 180,000 in total. Amir\'s salary is 10% of the profit; the rest is shared by investment. Profit 80,000; Ghirmay gets 40,000. Find the investments.', 'Amir 80,000; Ghirmay 100,000',
    ['Step 1: salary 8000; 72,000 shared.', 'Step 2: Ghirmay\'s fraction $\\frac{40000}{72000} = \\frac{5}{9}$.', 'Step 3: $\\frac{5}{9} \\times 180000 = 100000$.'], 'Shares are proportional to investments.', [('Ghirmay gets 48,000?', 'Ghirmay 120,000, Amir 60,000.')])
c.S(220, 'A invests 50,000 for 12 months, B 40,000 for 9 months. Share a profit of 32,000.', 'A 20,000; B 12,000',
    ['Step 1: $50000 \\times 12 = 600000$; $40000 \\times 9 = 360000$.', 'Step 2: ratio 5 : 3.'], 'Capital × time.', [('B for 12 months too?', 'ratio 5 : 4.')])
c.S(227, 'Exercise 6.7 Q1–Q2: (1) tea at 6.80 and 8.20 per kg to give 7.60; (2) gold 15.20 and silver 0.20 per g to give 3.20 per g.', '3 : 4; 1 : 4 (gold : silver)',
    ['Step 1: cheap : dear $= (8.20 - 7.60) : (7.60 - 6.80) = 0.6 : 0.8$.', 'Step 2: gold : silver $= (3.20 - 0.20) : (15.20 - 3.20) = 3 : 12$.'], 'Each difference goes to the opposite item.', [('Rice 12 and 18 to give 16?', 'cheap : dear $= 1 : 2$.')])
c.S(227, 'Exercise 6.7 Q3 (data completed): coffees at 120 and 75 Nakfa per kg; the mixture sells at 99 Nakfa per kg with 10% profit. Ratio?', '1 : 2 (dear : cheap)',
    ['Step 1: cost price $= \\frac{99}{1.1} = 90$.', 'Step 2: dear : cheap $= (90 - 75) : (120 - 90) = 15 : 30$.'],
    'The book gives no selling price, so the question cannot be done as printed; 99 Nakfa is an example value.', [('Sold at 110 with 10% profit?', 'cost 100: dear : cheap $= 25 : 20 = 5 : 4$.')])
c.S(227, 'Exercise 6.7 Q4 (corrected): wheat at 810 and 730 Nakfa per quintal; the mixture sells at 864 per **quintal** with 8% profit. Ratio?', '7 : 1 (dear : cheap)',
    ['Step 1: cost $= \\frac{864}{1.08} = 800$.', 'Step 2: dear : cheap $= (800 - 730) : (810 - 800) = 70 : 10$.'], 'Remove the profit first. (The book says "per kg", which cannot be right.)', [('Selling at 810 with 8% profit?', 'cost 750: 1 : 3.')])
c.S(227, 'Exercise 6.7 Q5: 90 litres of acid and water is 60% water. How much water to make it 75% water?', '54 litres',
    ['Step 1: acid stays $= 40\\% \\times 90 = 36$ L.', 'Step 2: acid is 25% of the new mix: $36 \\div 0.25 = 144$.', 'Step 3: $144 - 90$.'], 'Fix the ingredient that does not change.', [('To make it 70% water?', '30 litres.')])
c.S(224, 'How many litres of 60% acid must be added to 10 litres of 30% acid to get 50% acid?', '20 litres',
    ['Step 1: $0.3(10) + 0.6x = 0.5(10 + x)$.', 'Step 2: $3 + 0.6x = 5 + 0.5x$, $x = 20$.'], 'Alligation: $(60 - 50) : (50 - 30) = 1 : 2$.', [('To get 40%?', '5 litres.')])
c.M(225, 'Sugar at 20 and 30 Nakfa per kg is mixed to sell at 24 per kg (no profit). Ratio cheap : dear?', ['3 : 2', '2 : 3', '1 : 1', '4 : 6'], 'A',
    ['Step 1: $(30 - 24) : (24 - 20) = 6 : 4 = 3 : 2$.'], 'The mean is closer to the item used more.', [('To sell at 26?', '2 : 3.')])
c.TF(221, 'If partners invest different amounts for different times, the profit is shared in the ratio of capital × time.', True,
     ['Step 1: 1000 Nakfa for 2 months does the same work as 2000 for 1 month.'], 'Multiply before comparing.', [('Same time, different capital?', 'ratio of capitals.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Principal', 'The money borrowed, lent or saved.', 201),
    ('Compound interest', 'Interest worked out on the principal plus earlier interest.', 202),
    ('Instalment plan', 'Paying for an item with a deposit and a sequence of equal payments.', 211),
    ('Depreciation', 'The loss in value of a fixed asset: original cost − book value.', 214),
    ('Book value', 'The estimated value of an asset after some years.', 214),
    ('Partnership', 'A business owned by two or more people who share profits.', 220),
    ('Alligation', 'A quick rule for the ratio of two items mixed to a given mean price.', 225),
]
TIPS = [('Rate as a decimal, time in years.', 201), ('Compound: multiply by (1 + r) each period.', 205),
        ('Diminishing depreciation is compound interest with (1 − r).', 218), ('Alligation: cheap : dear = (d − m) : (m − c).', 225)]
IDEAS = [('si', 'Simple interest', 'l6_1', 'math11-u6-c01'), ('ci', 'Compound interest', 'l6_1', 'math11-u6-c07'),
         ('dep', 'Depreciation', 'l6_1', 'math11-u6-md-dep-t'), ('mix', 'Mixtures and alligation', 'l6_2', 'math11-u6-md-mix-t')]
