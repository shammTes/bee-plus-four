r"""Grade 9 Unit 7 — Business Mathematics (pp. 154-168)."""
from common import set_unit, T, RM, MN, TB, DG, ST, GR, WK, CK, QSet, plane
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL

UID = 'math9-u7'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_grid():
    f = Fig(330, 150)
    s, x0, y0 = 12, 14, 14
    f.rect(x0, y0, 4 * s, 10 * s, BLUE, 0, BLUE)
    for k in range(11):
        f.line(x0 + k * s, y0, x0 + k * s, y0 + 10 * s, GREY, 1, cap=False).line(x0, y0 + k * s, x0 + 10 * s, y0 + k * s, GREY, 1, cap=False)
    f.text(250, 44, '40 of 100 squares', 13, BLUE)
    f.text(250, 72, '40% = 40/100', 15, INK).text(250, 98, '= 2/5', 15, GREEN).text(250, 124, '= 0.4', 15, RED)
    return f


def f_ratiobar():
    f = Fig(330, 130)
    x0, w = 14, 25
    cols = [BLUE] * 3 + [GREEN] * 4 + [ORANGE] * 5
    for k, c in enumerate(cols):
        f.rect(x0 + k * w, 40, w - 2, 30, c, 1.5, FILL[c], 3)
    f.text(165, 24, '3 + 4 + 5 = 12 equal parts;  1 part = 408 000 ÷ 12 = 34 000', 11.5, INK)
    for a, b, c, t in ((0, 3, BLUE, '3 × 34 000 = 102 000'), (3, 7, GREEN, '4 parts = 136 000'), (7, 12, ORANGE, '5 parts = 170 000')):
        xa, xb = x0 + a * w, x0 + b * w - 2
        f.line(xa, 78, xb, 78, c, 2).line(xa, 74, xa, 82, c, 2).line(xb, 74, xb, 82, c, 2)
    f.text(x0 + 1.5 * w, 98, '102 000', 12.5, BLUE).text(x0 + 5 * w, 98, '136 000', 12.5, GREEN).text(x0 + 9.5 * w, 98, '170 000', 12.5, ORANGE)
    f.text(165, 122, 'first : second : third = 3 : 4 : 5', 12.5, GREY)
    return f


def f_pctchange():
    f = Fig(330, 190)
    def bar(y, w, c, lab, val):
        f.rect(90, y, w, 24, c, 1.6, FILL[c], 3).text(84, y + 17, lab, 12.5, c, 'end').text(96 + w, y + 17, val, 12.5, c, 'start')
    f.g('k1', 'k1')
    f.rect(90, 22, 160, 24, BLUE, 1.6, FILL[BLUE], 3).text(84, 39, 'old', 12.5, BLUE, 'end').text(170, 39, '100%', 12.5, BLUE)
    f.rect(90, 54, 160, 24, BLUE, 1.6, FILL[BLUE], 3).rect(250, 54, 16, 24, GREEN, 1.6, FILL[GREEN], 3).text(84, 71, 'new', 12.5, GREEN, 'end')
    f.text(170, 71, '110%', 12.5, GREEN).text(272, 71, '× 1.10', 12.5, GREEN, 'start').end()
    f.g('k2', 'k2')
    f.rect(90, 92, 160, 24, BLUE, 1.6, FILL[BLUE], 3).text(84, 109, 'old', 12.5, BLUE, 'end').text(170, 109, '100%', 12.5, BLUE)
    f.rect(90, 124, 128, 24, RED, 1.6, FILL[RED], 3).rect(218, 124, 32, 24, RED, 1.4, 'none', 3, dash=True).text(84, 141, 'new', 12.5, RED, 'end')
    f.text(154, 141, '80%', 12.5, RED).text(256, 141, '× 0.80', 12.5, RED, 'start').end()
    f.g('k3', 'k3').text(165, 176, 'reverse: new ÷ 0.80 gives the old price', 12.5, PURPLE).end()
    return f


def f_broker():
    f = Fig(330, 170)
    f.rect(6, 58, 86, 50, BLUE, 2, FILL[BLUE], 8).text(49, 80, 'Senay', 13, BLUE).text(49, 98, '(buyer)', 11.5, BLUE)
    f.rect(238, 58, 86, 50, GREEN, 2, FILL[GREEN], 8).text(281, 80, 'Kaltum', 13, GREEN).text(281, 98, '(seller)', 11.5, GREEN)
    f.rect(122, 120, 86, 40, ORANGE, 2, FILL[ORANGE], 8).text(165, 145, 'broker', 13, ORANGE)
    f.arrow(94, 72, 236, 72, INK, 2, 8).text(165, 64, 'pays 652 000', 12, INK)
    f.arrow(60, 110, 120, 134, ORANGE, 2, 8).text(52, 140, '0.5% = 3 260', 12, ORANGE)
    f.arrow(270, 110, 210, 134, ORANGE, 2, 8).text(282, 140, '1% = 6 520', 12, ORANGE)
    f.text(49, 30, 'pays 655 260', 12.5, BLUE).text(281, 30, 'keeps 645 480', 12.5, GREEN)
    f.text(165, 30, 'broker: 9 780', 12.5, ORANGE)
    return f


def f_cpsp():
    f = Fig(330, 170)
    f.text(90, 18, 'PROFIT (SP > CP)', 12.5, GREEN).text(245, 18, 'LOSS (SP < CP)', 12.5, RED)
    f.rect(40, 70, 40, 90, BLUE, 1.6, FILL[BLUE], 3).text(60, 120, 'CP', 13, BLUE)
    f.rect(100, 50, 40, 110, GREEN, 1.6, FILL[GREEN], 3).text(120, 120, 'SP', 13, GREEN)
    f.line(36, 70, 146, 70, INK, 1.2, dash=True).text(152, 64, 'profit', 12, GREEN, 'start')
    f.rect(195, 50, 40, 110, BLUE, 1.6, FILL[BLUE], 3).text(215, 120, 'CP', 13, BLUE)
    f.rect(255, 80, 40, 80, RED, 1.6, FILL[RED], 3).text(275, 120, 'SP', 13, RED)
    f.line(191, 50, 299, 50, INK, 1.2, dash=True).rect(255, 50, 40, 30, RED, 1.2, 'none', 2, dash=True).text(275, 70, 'loss', 11.5, RED)
    return f


def f_interest():
    p = Plot(0, 5.6, 0, 1200, unit=52, uy=0.13, pad=34, grid=False, every=1, yevery=200, xlab='years', ylab='')
    for t in range(1, 6):
        p.line(p.X(t), p.Y(0), p.X(t), p.Y(800), BLUE, 14, cap=False)
        p.line(p.X(t), p.Y(800), p.X(t), p.Y(800 + 40 * t), GREEN, 14, cap=False)
        p.text(p.X(t), p.Y(800 + 40 * t) - 6, str(800 + 40 * t), 11, GREEN)
    p.text(p.X(0.3), p.Y(1150), 'A = 800 + 40T', 13, GREEN, 'start').text(p.X(2.6), p.Y(1150), 'blue: principal, green: interest', 11.5, GREY, 'start')
    return p


DIAGRAMS = {
    'grid': (f_grid(), '40% of a hundred-square', 154),
    'ratiobar': (f_ratiobar(), 'Sharing 408 000 Nakfa in the ratio 3 : 4 : 5 (Example 7.2)', 157),
    'pctchange': (f_pctchange(), 'Percentage increase, decrease and reverse', 155),
    'broker': (f_broker(), 'Who pays whom? (Example 7.5)', 162),
    'cpsp': (f_cpsp(), 'Profit and loss compared with the cost price', 164),
    'interest': (f_interest(), 'Simple interest grows by the same amount every year', 165),
}

# ------------------------------------------------------------------ 7.1
L1 = [
    T('=math9-u7-c01', '7.1.1 Percentages', 154,
      '**Per cent** means "out of 100": $40\\% = \\frac{40}{100}$.',
      '**Percentage → fraction:** write over 100 and simplify: $68\\% = \\frac{68}{100} = \\frac{17}{25}$. **→ decimal:** divide by 100 (move the point 2 places left): $0.8\\% = 0.008$.',
      '**Fraction or decimal → percentage:** multiply by 100: $\\frac{9}{20} \\times 100 = 45\\%$; $0.025 \\times 100 = 2.5\\%$.',
      '**Percentage of a quantity:** change to a decimal and multiply: 24% of 34 600 books $= 0.24 \\times 34\\,600 = 8304$.',
      'A percentage can be more than 100%: $120\\% = 1.2$ (more than the whole).'),
    DG('grid', 'Three ways to write the same amount', 155, 'grid'),
    T('pctch-t', 'Percentage increase, decrease and discount', 155,
      '- **Increase by r%:** new = old × $(1 + \\frac{r}{100})$. Salary 2500 up 10%: $2500 \\times 1.10 = 2750$.',
      '- **Decrease (or discount) by r%:** new = old × $(1 - \\frac{r}{100})$. Malaria cases 1000 down 35%: $1000 \\times 0.65 = 650$.',
      '- **Reverse (find the original):** divide by the multiplier. A raincoat costs 125 after 20% off: $125 \\div 0.80 = 156.25$.',
      '- **Percentage change** $= \\frac{\\text{change}}{\\text{original}} \\times 100\\%$ — always divide by the **original** value.'),
    ST('pctchange', 'Multipliers make percentage change easy', 155, 'pctchange',
       [('Increase by 10%: the new amount is 110% of the old, so multiply by 1.10.', 'k1'),
        ('Decrease by 20%: 80% is left, so multiply by 0.80.', 'k2'),
        ('Going back to the original: divide by the same multiplier (never "add 20%" back).', 'k3')]),
    WK('ex-71a', 'Worked example: Exercise 7.1 Q9 (reverse percentage)', 156,
       "This month's sales are 40 420 Nakfa, 6% less than last month. Find last month's sales.",
       ["This month = last month × 0.94.", 'Last month $= 40\\,420 \\div 0.94 = 43\\,000$ Nakfa.', 'Check: 6% of 43 000 is 2580, and $43\\,000 - 2580 = 40\\,420$ (correct).'],
       '43 000 Nakfa'),
    WK('ex-71b', 'Worked example: Exercise 7.1 Q7 (percentage increase)', 156,
       'Sales rose from 10 452 000 to 11 565 000 Nakfa. Find the percentage increase.',
       ['Change $= 11\\,565\\,000 - 10\\,452\\,000 = 1\\,113\\,000$.', 'Divide by the original: $\\frac{1\\,113\\,000}{10\\,452\\,000} \\approx 0.1065$.', 'About 10.6%.'],
       'about 10.6%'),
    T('=math9-u7-c02', '7.1.2 Ratio', 156,
      'A **ratio** compares quantities **in the same units**: profits of 8000 and 24 000 Nakfa are in the ratio $8000 : 24\\,000 = 1 : 3$ (the second is 3 times the first).',
      '**Simplify** by dividing every part by the same number; **change units first**: 10 Nakfa to 50 cents $= 1000 : 50 = 20 : 1$; 20 hours to 5 days $= 20 : 120 = 1 : 6$.',
      '**Sharing in a ratio** $m : n$: add the parts ($m + n$), find one part (total ÷ sum), multiply.',
      '**Combining ratios:** if $x : y = 2 : 7$ and $y : z = 4 : 3$, make $y$ the same: $8 : 28$ and $28 : 21$, so $x : z = 8 : 21$.'),
    DG('ratiobar', 'Bar model for sharing', 157, 'ratiobar'),
    T('=math9-u7-c03', '7.1.3 Proportion', 159,
      'Two ratios form a **proportion** when they are equal: $a : b = c : d \\iff \\frac{a}{b} = \\frac{c}{d} \\iff ad = bc$ (cross-multiply).',
      'Example: $2 : 5 = 4 : 10 = 6 : 15$ (boys to girls in groups of 7, 14 and 21).',
      '**Direct proportion problems** ("more books, more cost"): set up equal ratios and cross-multiply. 8 books cost 560, so 17 books cost $x$: $\\frac{8}{560} = \\frac{17}{x} \\Rightarrow x = \\frac{560 \\times 17}{8} = 1190$ Nakfa.',
      '**Unitary method** (same thing): one book costs $560 \\div 8 = 70$, so 17 books cost $17 \\times 70 = 1190$.'),
    'math9-u7-tbl1',
    WK('ex-71c', 'Worked example: Exercise 7.2 Q4 (sharing in proportion)', 158,
       '550 quintals of fertiliser are shared among villages with 200, 500 and 600 farmers. Find each share.',
       ['Ratio $200 : 500 : 600 = 2 : 5 : 6$, sum 13.', 'One part $= 550 \\div 13 \\approx 42.31$ quintals.', 'Shares: $2 \\times 42.31 \\approx 84.6$, $5 \\times 42.31 \\approx 211.5$, $6 \\times 42.31 \\approx 253.8$ quintals (total 550, correct).'],
       'about 84.6, 211.5 and 253.8 quintals'),
]

# ------------------------------------------------------------------ 7.2
L2 = [
    T('=math9-u7-c04', '7.2.1 Commission', 160,
      'A **commission** is payment to an agent or salesperson, usually a percentage of the **sales**: $$\\text{commission} = \\text{rate} \\times \\text{sales}, \\qquad \\text{rate} = \\frac{\\text{commission}}{\\text{sales}} \\times 100\\%$$',
      'Example 7.4: Gabriel sells 20 tickets of 5 Nakfa a day and earns 0.50 per ticket. In 30 days: sales $= 30 \\times 100 = 3000$, commission $= 30 \\times 10 = 300$, rate $= \\frac{300}{3000} = 10\\%$.',
      'Many jobs pay **salary + commission**: income = basic salary + rate × sales.',
      '**Tiered rates:** each band of sales gets its own rate (like a ladder): 6% on the first 10 000, 8% on the next 10 000, 9% on the rest.'),
    WK('ex-72a', 'Worked example: Exercise 7.4 Q3 (salary + commission)', 161,
       'A saleswoman earns 3400 Nakfa a month plus 8% commission. Last month she received 4076 Nakfa. Find (a) her commission (b) her sales.',
       ['(a) Commission $= 4076 - 3400 = 676$ Nakfa.', '(b) $0.08 \\times \\text{sales} = 676$, so sales $= 676 \\div 0.08 = 8450$ Nakfa.'],
       '(a) 676 Nakfa (b) 8450 Nakfa'),
    WK('ex-72b', 'Worked example: Exercise 7.4 Q5 (tiered commission)', 161,
       'Trhas earns 6% on sales up to 10 000, 8% on 10 001 – 20 000 and 9% above 20 000. Find her income on sales of 32 768 Nakfa.',
       ['First band: $0.06 \\times 10\\,000 = 600$.', 'Second band: $0.08 \\times 10\\,000 = 800$.', 'Rest: $32\\,768 - 20\\,000 = 12\\,768$; $0.09 \\times 12\\,768 = 1149.12$.', 'Total $= 600 + 800 + 1149.12 = 2549.12$ Nakfa. (If instead the whole amount earns 9%, the answer would be 2949.12 — the textbook does not say which; the band method is the usual meaning.)'],
       '2549.12 Nakfa'),
    T('=math9-u7-c05', '7.2.2 Brokerage', 162,
      'A **broker** brings buyers and sellers together; the fee is the **brokerage**, usually a percentage of the price. A broker may charge **both** sides.',
      '- The **buyer pays** price + buyer\'s brokerage.',
      '- The **seller receives** price − seller\'s brokerage.',
      '- The **broker gets** both fees.',
      '**Reverse problems:** to keep 1500 Nakfa after 3% brokerage, the seller must ask $1500 \\div 0.97 \\approx 1546.39$ Nakfa (not $1500 + 3\\%$).'),
    DG('broker', 'Example 7.5: a 652 000 Nakfa house', 162, 'broker',
       'Seller pays 1%: $6520$. Buyer pays 0.5%: $3260$. Broker gets $6520 + 3260 = 9780$. Buyer pays $652\\,000 + 3260 = 655\\,260$; seller keeps $652\\,000 - 6520 = 645\\,480$.'),
    WK('ex-72c', 'Worked example: Exercise 7.5 Q3', 163,
       'Awet paid 4% brokerage and 2.5% registration on a car\'s value, 120 000 Nakfa in total. Find the value of the car.',
       ['Total = value × $(1 + 0.04 + 0.025) = 1.065 \\times$ value.', 'Value $= 120\\,000 \\div 1.065 \\approx 112\\,676$ Nakfa.'],
       'about 112 676 Nakfa'),
]

# ------------------------------------------------------------------ 7.3
L3 = [
    T('=math9-u7-c06', '7.3 Profit and loss', 163,
      '**Cost price (CP)**: what the trader paid. **Selling price (SP)**: what the customer paid.',
      '- SP > CP: **profit** $= SP - CP$; SP < CP: **loss** $= CP - SP$.',
      '- Profit % $= \\frac{\\text{profit}}{CP} \\times 100\\%$; loss % $= \\frac{\\text{loss}}{CP} \\times 100\\%$ — always compared with the **cost price**.',
      '- **Selling for a given profit:** SP $= CP \\times (1 + \\frac{r}{100})$. **Finding CP from SP:** CP $= SP \\div (1 + \\frac{r}{100})$.',
      'Activity 7.6: Harnet buys 20 hens at 55 and sells at 65: CP $= 1100$, SP $= 1300$, profit $= 200 = 18.2\\%$ of CP.'),
    DG('cpsp', 'Comparing SP with CP', 164, 'cpsp'),
    WK('ex-73a', 'Worked example: Exercise 7.6 Q1 (which is more profitable?)', 164,
       'A radio costing 500 sells for 550; a tape recorder costing 1000 sells for 1050. Which is more profitable?',
       ['Both make a profit of 50 Nakfa.', 'Radio: $\\frac{50}{500} = 10\\%$. Tape recorder: $\\frac{50}{1000} = 5\\%$.', 'Compare percentages, not amounts: the radio is more profitable.'],
       'the radio (10% vs 5%)'),
    WK('ex-73b', 'Worked example: Exercise 7.6 Q5 (chain of sales)', 164,
       'Ali bought an article for 740 and sold it to Tesfu at 12.5% profit; Tesfu sold it to Halima at a 15% loss. What did Halima pay?',
       ['Tesfu paid $740 \\times 1.125 = 832.50$.', 'Halima paid $832.50 \\times 0.85 = 707.625 \\approx 707.63$ Nakfa.', 'Note: +12.5% then −15% is not −2.5%; each percentage is of a different cost price.'],
       'about 707.63 Nakfa'),
]

# ------------------------------------------------------------------ 7.4
L4 = [
    T('=math9-u7-c07', '7.4 Simple interest', 165,
      'With **simple interest** the interest each year is the same: a fixed percentage of the original **principal**. Activity 7.7: 800 Nakfa at 5% earns 40 each year, so 40, 80, 120, 160, 200 after 1–5 years.',
      '$$I = P \\times R \\times T, \\qquad A = P + I$$ $P$ = principal, $R$ = rate per year as a decimal ($6\\% = 0.06$), $T$ = time in **years**, $A$ = amount.',
      '**Months and days:** 9 months $= \\frac{9}{12}$ year; 20 days $= \\frac{20}{365}$ year.',
      '**Rearranged:** $P = \\frac{I}{RT}$, $R = \\frac{I}{PT}$, $T = \\frac{I}{PR}$. When you know the amount $A$, first find $I = A - P$, or use $P = \\frac{A}{1 + RT}$.'),
    DG('interest', 'Linear growth', 165, 'interest',
       'The green part grows by the same 40 Nakfa every year — simple interest gives a **straight-line** (linear) graph: $A = 800 + 40T$.'),
    TB('si-t', 'Which form of I = PRT?', 166, ['Want', 'Formula', 'Example'],
       [['interest $I$', '$PRT$', '$2000 \\times 0.04 \\times 4 = 320$'], ['principal $P$', '$\\frac{I}{RT}$', '$\\frac{300}{0.06 \\times 3} \\approx 1666.67$'],
        ['rate $R$', '$\\frac{I}{PT}$', '$\\frac{180}{1500 \\times 4} = 0.03 = 3\\%$'], ['time $T$', '$\\frac{I}{PR}$', '$\\frac{810}{4500 \\times 0.06} = 3$ years'],
        ['principal from amount', '$\\frac{A}{1 + RT}$', '$\\frac{3500}{1 + 0.09 \\times \\frac{8}{12}} \\approx 3301.89$']]),
    WK('ex-74a', 'Worked example: Exercise 7.7 Q4 (find the time)', 167,
       'Rigbe deposits 4500 Nakfa at 6%. After how many years will she have 5310 Nakfa?',
       ['Interest needed: $I = 5310 - 4500 = 810$.', 'One year earns $4500 \\times 0.06 = 270$.', '$T = 810 \\div 270 = 3$ years.'],
       '3 years'),
    WK('ex-74b', 'Worked example: Exercise 7.7 Q5 (principal from the amount)', 167,
       'Money at 5.5% simple interest amounts to 770 Nakfa after 9 months. Find the principal.',
       ['$T = \\frac{9}{12} = 0.75$; $RT = 0.055 \\times 0.75 = 0.04125$.', '$A = P(1 + RT)$, so $P = 770 \\div 1.04125 \\approx 739.50$ Nakfa.', 'Check: interest $= 739.50 \\times 0.04125 \\approx 30.50$; $739.50 + 30.50 = 770$ (correct).'],
       'about 739.50 Nakfa'),
    WK('ex-74c', 'Worked example: Review Q8 (comparing offers)', 168,
       'Offer (i): 4600 Nakfa a month. Offer (ii): 3200 Nakfa plus 1% of monthly sales. Sales are about 150 000 Nakfa. Which is better?',
       ['(ii): $3200 + 0.01 \\times 150\\,000 = 3200 + 1500 = 4700$.', '4700 > 4600, so (ii) is better at these sales.', 'Break-even: $3200 + 0.01s = 4600 \\Rightarrow s = 140\\,000$. Above 140 000 in sales, (ii) wins.'],
       'offer (ii), 4700 Nakfa'),
    RM('=math9-u7-c08', 'Business mathematics — summary', 168,
       'Percent change $= \\frac{\\text{change}}{\\text{original}} \\times 100\\%$; increase → × $(1 + r)$, decrease → × $(1 - r)$, reverse → ÷.',
       'Commission = rate × sales; brokerage may be paid by both sides.',
       'Profit % and loss % are of the **cost price**.',
       '$I = PRT$ ($T$ in years), $A = P + I$.'),
]

LESSONS = {'math9-u7-l7-1': L1, 'math9-u7-l7-2': L2, 'math9-u7-l7-3': L3, 'math9-u7-l7-4': L4}

# ------------------------------------------------------------------ practice
a = QSet('7.1 Practice — percentages, ratio and proportion', 's71')
a.S(155, 'Write as a fraction in lowest terms and as a decimal: (a) 85% (b) 120% (c) 0.8%', '(a) $\\frac{17}{20}$, 0.85 (b) $\\frac{6}{5}$, 1.2 (c) $\\frac{1}{125}$, 0.008',
    ['Step 1: put over 100: $\\frac{85}{100}$, $\\frac{120}{100}$, $\\frac{0.8}{100} = \\frac{8}{1000}$.', 'Step 2: simplify.', 'Step 3: decimals: divide by 100.'],
    'Clear decimals in the numerator first.', [('5% as a fraction?', '$\\frac{1}{20}$.')])
a.S(155, 'Write as percentages: (a) $\\frac{1}{5}$ (b) 0.12 (c) $\\frac{22}{25}$ (d) 0.025', '20%, 12%, 88%, 2.5%',
    ['Step 1: multiply each by 100%.', 'Step 2: $\\frac{22}{25} = \\frac{88}{100}$.'],
    'Fractions with denominator 25, 20, 50: scale to 100.', [('$\\frac{9}{20}$ as a percentage?', '45%.')])
a.S(155, 'A person invests 48 000 Nakfa and expects a 9% gain in a year. How much will they have?', '52 320 Nakfa',
    ['Step 1: multiplier 1.09.', 'Step 2: $48\\,000 \\times 1.09 = 52\\,320$.'],
    'Increase → multiply by $1 + r$.', [('2000 Nakfa salary up 10%?', '2200 Nakfa.')])
a.S(156, 'A car priced at 178 740 Nakfa is discounted by 8%. Find the new price.', '164 440.80 Nakfa',
    ['Step 1: multiplier 0.92.', 'Step 2: $178\\,740 \\times 0.92 = 164\\,440.80$.'],
    'Discount → multiply by $1 - r$.', [('1000 cases down 35%?', '650.')])
a.S(156, 'A raincoat costs 125 Nakfa after a 20% discount. Find the original price.', '156.25 Nakfa',
    ['Step 1: 125 is 80% of the original.', 'Step 2: $125 \\div 0.8 = 156.25$.'],
    'Never add 20% of 125 — that gives 150, which is wrong.', [('After 25% off a bag costs 90. Original?', '120.')])
a.S(156, 'A bicycle is reduced from 1725 to 1425 Nakfa. Find the discount rate.', 'about 17.4%',
    ['Step 1: reduction $= 300$.', 'Step 2: $\\frac{300}{1725} \\times 100 \\approx 17.4\\%$.'],
    'Divide by the ORIGINAL price.', [('Review Q2a: 300 to 250?', 'about 16.7% decrease.')])
a.S(158, 'In a class of 80, 30% are girls. Find the number of boys and the ratio boys : girls.', '56 boys; 7 : 3',
    ['Step 1: girls $= 0.3 \\times 80 = 24$; boys $= 56$.', 'Step 2: $56 : 24 = 7 : 3$ (÷ 8).'],
    'Simplify by the HCF.', [('Ratio of girls to the whole class?', '3 : 10.')])
a.S(158, 'Divide 670 in the ratio 3 : 7.', '201 and 469',
    ['Step 1: $3 + 7 = 10$ parts; 1 part $= 67$.', 'Step 2: $3 \\times 67 = 201$, $7 \\times 67 = 469$.'],
    'Check the shares add to the total.', [('Divide 5500 so one part is 4 times the other.', '1100 and 4400.')])
a.S(158, 'A plan has scale 1 : 2000. A road measures 9 cm on the plan. Find its real length in metres.', '180 m',
    ['Step 1: real $= 9 \\times 2000 = 18\\,000$ cm.', 'Step 2: $18\\,000 \\div 100 = 180$ m.'],
    'Scale ratios have the same units on both sides.', [('5 cm on a 1 : 50 000 map, in km?', '2.5 km.')])
a.S(167, 'If $x : y = 2 : 7$ and $y : z = 4 : 3$, find $x : z$.', '8 : 21',
    ['Step 1: make $y$ equal: LCM of 7 and 4 is 28.', 'Step 2: $x : y = 8 : 28$, $y : z = 28 : 21$.', 'Step 3: $x : z = 8 : 21$.'],
    'Match the shared term first.', [('$a : b = 1 : 2$, $b : c = 3 : 4$; $a : c$?', '3 : 8.')])
a.S(160, 'If $25 : N$ and $5 : 3$ are proportional, find $N$.', '15',
    ['Step 1: $\\frac{25}{N} = \\frac{5}{3}$.', 'Step 2: $5N = 75$, $N = 15$.'],
    'Cross-multiply.', [('$3 : 5 = 12 : y$?', '$y = 20$.')])
a.S(160, 'A car travels 540 km on 45 litres. How far on (a) 60 litres (b) 20 litres?', '720 km; 240 km',
    ['Step 1: per litre $540 \\div 45 = 12$ km.', 'Step 2: $60 \\times 12 = 720$, $20 \\times 12 = 240$.'],
    'Unitary method: find one first.', [('12 pens cost 20 Nakfa. 20 pens?', 'about 33.33 Nakfa.')])
a.S(160, '7 quintals of fertiliser cover 3325 m². How many for 7125 m²?', '15 quintals',
    ['Step 1: $\\frac{7}{3325} = \\frac{x}{7125}$.', 'Step 2: $x = \\frac{7 \\times 7125}{3325} = 15$.'],
    'More land, more fertiliser: direct proportion.', [('Tax 6000 on income 42 000. Tax on 63 000?', '9000.')])
a.TF(168, '2, 1, 6 and 18 are in proportion.', False,
     ['Step 1: $\\frac{2}{1} = 2$, $\\frac{6}{18} = \\frac{1}{3}$.', 'Step 2: not equal.'],
     'Check $ad = bc$: $2 \\times 18 = 36 \\ne 6$.', [('Are 5, 9, 15, 27 in proportion?', 'Yes ($5 \\times 27 = 9 \\times 15 = 135$).')])

b = QSet('7.2 Practice — commission and brokerage', 's72')
b.S(161, 'Nasser earns 4% commission on sales of 120 000 Nakfa. Find his commission.', '4800 Nakfa',
    ['Step 1: $0.04 \\times 120\\,000 = 4800$.'], 'Rate as a decimal × sales.', [('5% of 30 000?', '1500.')])
b.S(161, 'A salesperson got 540 Nakfa commission on 10 800 Nakfa sales. Find the rate.', '5%',
    ['Step 1: $\\frac{540}{10\\,800} = 0.05$.', 'Step 2: 5%.'], 'Rate = commission ÷ sales.', [('300 on 3000?', '10%.')])
b.S(161, 'Semere earns 225 Nakfa a week plus 3% commission. Find his income when his sales are 7250 Nakfa.', '442.50 Nakfa',
    ['Step 1: commission $= 0.03 \\times 7250 = 217.50$.', 'Step 2: $225 + 217.50 = 442.50$.'],
    'Salary + commission.', [('3000 plus 4% of 20 000?', '3800.')])
b.S(163, 'Salih rents his shop to Naib for 20 000 Nakfa a year; the broker charges each 10%. Find (a) the brokerage (b) what Naib pays (c) what Salih receives.', '4000; 22 000; 18 000',
    ['Step 1: each fee $= 2000$; total 4000.', 'Step 2: Naib $= 20\\,000 + 2000$.', 'Step 3: Salih $= 20\\,000 - 2000$.'],
    'Buyer adds, seller subtracts.', [('House 100 000, 2% each side: broker gets?', '4000.')])
b.S(163, 'Yemane wants 1500 Nakfa net after 3% brokerage. At what price should he sell?', 'about 1546.39 Nakfa',
    ['Step 1: he keeps 97% of the price.', 'Step 2: $1500 \\div 0.97 \\approx 1546.39$.'],
    'Reverse percentage → divide.', [('Net 4750 after 5%?', '5000.')])
b.S(163, 'A company buys 2500 kg of tomatoes at 4 Nakfa/kg, pays 5% brokerage and 250 Nakfa transport. Find the total cost.', '10 750 Nakfa',
    ['Step 1: price $= 10\\,000$.', 'Step 2: brokerage $= 500$.', 'Step 3: $10\\,000 + 500 + 250 = 10\\,750$.'],
    'Brokerage is on the price only, not on transport.', [('1000 kg at 6, 2% brokerage, 100 transport?', '6220.')])
b.M(161, 'Gabriel earns 0.50 Nakfa on each 5 Nakfa ticket. His commission rate is', ['5%', '10%', '50%', '0.5%'], 'B',
    ['Step 1: $\\frac{0.5}{5} = 0.1 = 10\\%$.'], 'Per-item commission ÷ price.', [('2 Nakfa on a 40 Nakfa item?', '5%.')])
b.S(168, 'Salary 3200 + 1% of sales vs 4600 fixed. For what sales are they equal?', '140 000 Nakfa',
    ['Step 1: $3200 + 0.01s = 4600$.', 'Step 2: $s = 140\\,000$.'],
    'Set the two incomes equal.', [('2000 + 5% of sales vs 3000 fixed?', '20 000.')])

c = QSet('7.3 Practice — profit and loss', 's73')
c.S(164, 'A motorcycle bought for 24 000 is sold for 20 000. Find the loss and the loss %.', '4000; about 16.7%',
    ['Step 1: loss $= 4000$.', 'Step 2: $\\frac{4000}{24\\,000} \\approx 16.7\\%$.'], 'Divide by CP.', [('CP 500, SP 450?', 'loss 50, 10%.')])
c.S(164, 'An item sold for 82 Nakfa made a 6% profit. Find the cost price.', 'about 77.36 Nakfa',
    ['Step 1: SP $= CP \\times 1.06$.', 'Step 2: CP $= 82 \\div 1.06 \\approx 77.36$.'], 'Reverse → divide.', [('SP 120 at 20% profit?', 'CP 100.')])
c.S(164, 'Bananas cost 5 Nakfa/kg. What selling price gives a 20% profit?', '6 Nakfa/kg',
    ['Step 1: $5 \\times 1.2 = 6$.'], 'SP = CP × (1 + r).', [('CP 40, 25% profit?', '50.')])
c.S(163, 'Harnet buys 20 hens at 55 each and sells them at 65 each. Find the profit %.', 'about 18.2%',
    ['Step 1: CP $= 1100$, SP $= 1300$, profit $= 200$.', 'Step 2: $\\frac{200}{1100} \\approx 18.2\\%$.'],
    'Per hen gives the same answer: $\\frac{10}{55}$.', [('Buy at 40, sell at 50?', '25%.')])
c.S(164, 'A bicycle bought for 2500 is sold at a 12% loss. Find the selling price.', '2200 Nakfa',
    ['Step 1: $2500 \\times 0.88 = 2200$.'], 'Loss → multiply by $1 - r$.', [('CP 800 at 5% loss?', '760.')])
c.M(164, 'Profit percentage is calculated as a percentage of', ['SP', 'CP', 'profit', 'SP + CP'], 'B',
    ['Step 1: profit % $= \\frac{\\text{profit}}{CP} \\times 100$.'], 'CP is the base.', [('Loss % is of?', 'CP.')])
c.TF(164, 'A 10% profit followed by a 10% loss brings you back to the original price.', False,
     ['Step 1: $100 \\times 1.1 = 110$.', 'Step 2: $110 \\times 0.9 = 99$, not 100.'],
     'The second percentage is of a different amount.', [('100 up 20% then down 20%?', '96.')])

d = QSet('7.4 Practice — simple interest', 's74')
d.S(166, 'Ismael borrows 2000 Nakfa at 4% simple interest. Find the interest after 4 years.', '320 Nakfa',
    ['Step 1: $I = 2000 \\times 0.04 \\times 4 = 320$.'], 'I = PRT.', [('500 at 6% for 1 year?', '30.')])
d.S(166, 'The interest at 6% for 3 years is 300 Nakfa. How much was borrowed?', 'about 1666.67 Nakfa',
    ['Step 1: $P = \\frac{300}{0.06 \\times 3} = \\frac{300}{0.18}$.', 'Step 2: $\\approx 1666.67$.'],
    'P = I ÷ (RT).', [('I = 150 at 3% for 4 years?', 'P = 1250.')])
d.S(167, 'What rate makes 1500 Nakfa earn 180 Nakfa in 4 years?', '3%',
    ['Step 1: $R = \\frac{180}{1500 \\times 4} = 0.03$.'], 'R = I ÷ (PT).', [('3000 earns 360 in 4 years?', '3%.')])
d.S(167, '2400 Nakfa at 5%: find the amount after (a) 4 months (b) 9 months.', '2440; 2490',
    ['Step 1: $I = 2400 \\times 0.05 \\times \\frac{4}{12} = 40$ → 2440.', 'Step 2: $I = 2400 \\times 0.05 \\times \\frac{9}{12} = 90$ → 2490.'],
    'Months → divide by 12.', [('1200 at 10% for 6 months?', '1260.')])
d.S(167, '150 Nakfa at 7% for 20 days. Find the interest.', 'about 0.58 Nakfa',
    ['Step 1: $T = \\frac{20}{365}$.', 'Step 2: $150 \\times 0.07 \\times \\frac{20}{365} \\approx 0.575$.'],
    'Days → divide by 365.', [('3650 at 10% for 10 days?', '10.')])
d.S(168, 'Review Q9: fill in: (a) P 3000, T 4, I 360, R = ? (b) P 1250, R 3%, I 150, T = ? (c) P 850, R 6%, T 5, I = ? (d) R 2%, T 7, I 70, P = ?', '3%; 4 years; 255; 500',
    ['Step 1: $\\frac{360}{12\\,000} = 3\\%$.', 'Step 2: $\\frac{150}{37.5} = 4$.', 'Step 3: $850 \\times 0.06 \\times 5 = 255$.', 'Step 4: $\\frac{70}{0.14} = 500$.'],
    'Same formula, solved for the missing letter.', [('P 600, R 5%, T 2: I?', '60.')])
d.S(168, 'How long for 500 Nakfa to grow to 510 at 9%?', 'about 0.22 years (about 81 days)',
    ['Step 1: $I = 10$; one year earns 45.', 'Step 2: $T = \\frac{10}{45} \\approx 0.222$ year $\\approx 81$ days.'],
    'T = I ÷ (PR).', [('800 to 1040 at 10%?', '3 years.')])
d.S(168, 'What amount invested now grows to 3500 in 8 months at 9%?', 'about 3301.89 Nakfa',
    ['Step 1: $1 + RT = 1 + 0.09 \\times \\frac{8}{12} = 1.06$.', 'Step 2: $3500 \\div 1.06 \\approx 3301.89$.'],
    'From the amount use $P = \\frac{A}{1 + RT}$.', [('Grows to 1100 in 1 year at 10%?', '1000.')])
d.S(165, 'Adhanom deposits 800 at 5%. How much interest after 5 years, and after T years?', '200; $40T$',
    ['Step 1: 40 per year.', 'Step 2: $5 \\times 40 = 200$; $T$ years: $40T$.'],
    'Simple interest is the same every year.', [('1000 at 8% after T years?', '$80T$.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Percentage', 'A number out of 100.', 154), ('Ratio', 'A comparison of quantities in the same units, e.g. 1 : 3.', 157),
    ('Proportion', 'An equality of two ratios: $a : b = c : d$.', 159), ('Commission', 'A payment to an agent, a percentage of sales.', 161),
    ('Brokerage', 'The fee paid to a broker, usually a percentage of the price.', 162), ('Cost price', 'The price the trader paid.', 164),
    ('Selling price', 'The price the customer pays.', 164), ('Principal', 'The money invested or borrowed.', 166),
    ('Simple interest', '$I = PRT$; the same interest every year.', 165),
]
TIPS = [('Increase → × (1 + r); decrease → × (1 − r); find the original → divide.', 155),
        ('Profit % and loss % are always of the cost price.', 164), ('In I = PRT, time must be in years.', 166)]
IDEAS = [('pctch', 'Percentage change', 'l7_1', 'math9-u7-md-pctch-t'), ('si', 'Forms of I = PRT', 'l7_4', 'math9-u7-md-si-t')]

# narrow phones: the textbook key table reads better as one card per row
PATCH = {'math9-u7-tbl1': {'layout': 'cards', '_inline': True}}
