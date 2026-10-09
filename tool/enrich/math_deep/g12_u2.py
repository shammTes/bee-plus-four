r"""Grade 12 Unit 2 — Descriptive Statistics and Probability (pp. 40-125)."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, polar

UID = 'math12-u2'
set_unit(UID)
LB, LG, LR, LP, LO = '#dbe7f3', '#d6ece6', '#f6dcd5', '#ECE6F5', '#FCEFD9'


# ------------------------------------------------------------------ figures
def f_classes():
    f = Fig(340, 150)
    y = 70
    f.line(20, y, 320, y, INK, 2)
    X = lambda v: 40 + (v - 18) * 22
    for v in range(19, 32):
        f.line(X(v), y - 5, X(v), y + 5, GREY, 1.2)
    f.g('k1 k2 k3').rect(X(20), y - 30, X(29) - X(20), 22, BLUE, 1.6, LB)
    f.text(X(20), y + 22, '20', 12, BLUE).text(X(29), y + 22, '29', 12, BLUE)
    f.text((X(20) + X(29)) / 2, y - 14, 'limits 20 - 29', 11.5, BLUE).end()
    f.g('k2 k3').line(X(19.5), y - 40, X(19.5), y + 30, RED, 2, dash='4 3').line(X(29.5), y - 40, X(29.5), y + 30, RED, 2, dash='4 3')
    f.text(X(19.5), y + 44, '19.5', 12, RED).text(X(29.5), y + 44, '29.5', 12, RED)
    f.text((X(19.5) + X(29.5)) / 2, y - 46, 'boundaries: width 10', 11.5, RED).end()
    f.g('k3').dot(X(24.5), y, GREEN, 5).text(X(24.5), y + 22, '24.5', 12, GREEN).text(X(24.5), y + 62, 'class mark = (20 + 29) / 2', 11.5, GREEN).end()
    return f


def f_pie():
    f = Fig(340, 220)
    c, r = (110, 110), 92
    data = [('Food 35%', 35, BLUE, LB), ('Rent 25%', 25, GREEN, LG), ('Savings 20%', 20, ORANGE, LO), ('Misc. 15%', 15, PURPLE, LP), ('Education 5%', 5, RED, LR)]
    a = 90
    for i, (lab, pct, col, fl) in enumerate(data):
        b = a - pct * 3.6
        p0, p1 = polar(c, r, a), polar(c, r, b)
        large = 1 if pct > 50 else 0
        f.path(f'M{c[0]} {c[1]} L{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f} Z', col, 1.6, fl)
        m = polar(c, r * 0.62, (a + b) / 2)
        f.text(m[0], m[1] + 4, f'{pct * 3.6:.0f}°', 11.5, col)
        f.rect(222, 30 + 30 * i, 14, 14, col, 1.4, fl).text(242, 42 + 30 * i, lab, 12, INK, 'start')
        a = b
    return f


def f_hist():
    fr = [2, 10, 21, 19, 7, 1]
    p = Plot(-10, 70, 0, 25, unit=3.9, uy=7.4, every=10, yevery=5, gstep=100, xlab='mark', ylab='f')
    p.g('k1 k2 k3')
    for i, v in enumerate(fr):
        x0, y0 = p.P(10 * i, v)
        x1, y1 = p.P(10 * i + 10, 0)
        p.rect(x0, y0, x1 - x0, y1 - y0, BLUE, 1.4, LB)
        p.text((x0 + x1) / 2, y0 - 5, str(v), 11, BLUE)
    p.end()
    pts = [(-5, 0)] + [(10 * i + 5, v) for i, v in enumerate(fr)] + [(65, 0)]
    p.g('k2 k3').curve(pts, RED, 2.2)
    for x, y in pts[1:-1]:
        p.dot(p.X(x), p.Y(y), RED, 3.4)
    p.end()
    p.g('k3').text(p.X(25), p.Y(23.5), 'modal class 20 - 30', 11.5, GREEN).end()
    return p


def f_spread():
    f = Fig(340, 150)
    A = [6.5, 6.6, 6.7, 6.8, 7.1, 7.3, 7.4, 7.7, 7.7, 7.7]
    B = [4.2, 5.4, 5.8, 6.2, 6.7, 7.7, 7.7, 8.5, 9.3, 10.0]
    X = lambda v: 50 + (v - 4) * 46
    for y, data, col, lab in ((50, A, BLUE, 'Bank A'), (115, B, RED, 'Bank B')):
        f.line(X(4), y, X(10.2), y, GREY, 1.4)
        seen = {}
        for v in data:
            k = seen.get(v, 0)
            seen[v] = k + 1
            f.dot(X(v), y - 7 - 7 * k, col, 2.6)
        f.text(8, y + 4, lab, 12, col, 'start')
        f.line(X(min(data)), y + 9, X(max(data)), y + 9, col, 2)
    f.line(X(7.15), 14, X(7.15), 135, GREEN, 1.6, dash='4 3').text(X(7.15), 148, 'both means 7.15', 11.5, GREEN)
    for v in (4, 6, 8, 10):
        f.text(X(v), 132, str(v), 10.5, GREY)
    return f


def f_venn():
    f = Fig(330, 190)
    f.rect(10, 10, 310, 170, INK, 1.6).text(26, 30, 'S', 13, INK)
    f.g('k1 k2 k3').circle(130, 98, 62, BLUE, 2, LB).text(92, 98, 'A', 15, BLUE).end()
    f.g('k2 k3').circle(205, 98, 62, RED, 2, LR).text(243, 98, 'B', 15, RED).circle(130, 98, 62, BLUE, 2).end()
    f.g('k3').text(167, 92, 'A and B', 11, PURPLE).text(167, 108, 'counted', 11, PURPLE).text(167, 122, 'twice', 11, PURPLE).end()
    return f


def f_tree():
    f = Fig(340, 236)
    x0, x1, x2, x3 = 20, 105, 190, 270
    ys = [18 + 28 * i for i in range(8)]
    for i in range(8):
        f.line(x2 + 10, (ys[i - i % 2] + ys[i - i % 2 + 1]) / 2, x3 - 12, ys[i], GREY, 1.3)
        lab = ''.join('PF'[(i >> k) & 1] for k in (2, 1, 0))
        f.text(x3 - 4, ys[i] + 4, lab[2], 12, GREEN if lab[2] == 'P' else RED).text(x3 + 18, ys[i] + 4, lab, 12, INK, 'start')
    for j in range(4):
        y = (ys[2 * j] + ys[2 * j + 1]) / 2
        yp = (ys[4 * (j // 2)] + ys[4 * (j // 2) + 3]) / 2
        f.line(x1 + 10, yp, x2 - 8, y, GREY, 1.3)
        f.text(x2, y + 4, 'PF'[j & 1], 12, GREEN if j % 2 == 0 else RED)
    for j in range(2):
        y = (ys[4 * j] + ys[4 * j + 3]) / 2
        f.line(x0 + 4, 116, x1 - 8, y, GREY, 1.3)
        f.text(x1, y + 4, 'PF'[j], 12, GREEN if j == 0 else RED)
    f.dot(x0, 116, INK, 4)
    f.text(x1, 232, '1st', 11, GREY).text(x2, 232, '2nd', 11, GREY).text(x3, 232, '3rd', 11, GREY)
    return f


def f_dice():
    f = Fig(300, 296)
    s, x0, y0 = 36, 50, 40
    for i in range(6):
        f.text(x0 + s * i + s / 2, y0 - 10, str(i + 1), 12, BLUE)
        f.text(x0 - 12, y0 + s * i + s / 2 + 4, str(i + 1), 12, RED)
        for j in range(6):
            t = i + j + 2
            fill = LG if t == 7 else (LO if t == 11 else 'none')
            f.rect(x0 + s * j, y0 + s * i, s, s, GREY, 1, fill)
            f.text(x0 + s * j + s / 2, y0 + s * i + s / 2 + 4, str(t), 12, GREEN if t == 7 else (ORANGE if t == 11 else INK))
    f.text(x0 + 3 * s, 18, 'die 1', 11, BLUE).text(16, y0 + 3 * s, 'die 2', 11, RED)
    f.text(x0 + 3 * s, y0 + 6 * s + 22, 'sum 7: 6 cells; sum 11: 2 cells', 11.5, INK)
    return f


DIAGRAMS = {
    'classes': (f_classes(), 'Class limits, boundaries and class mark', 58),
    'pie': (f_pie(), 'Example 2.10: a family budget as a pie chart', 64),
    'hist': (f_hist(), 'Example 2.13: histogram and frequency polygon', 69),
    'spread': (f_spread(), 'Example 2.24: same mean, different spread', 87),
    'venn': (f_venn(), 'The addition law', 105),
    'tree': (f_tree(), 'Example 2.36: a tree diagram for three students', 110),
    'dice': (f_dice(), 'The 36 outcomes of rolling two dice', 103),
}

# ------------------------------------------------------------------ 2.1
L1 = [
    T('=math12-u2-c01', '2.1 Statistics, population and sample', 41,
      '**Statistics** is collecting, presenting, analysing and interpreting numerical data. In the opening story, one son *collects* the weekly profits, the second *organises* them in a table, the third *interprets* them ("profit above 250 Nakfa in 5 of 20 weeks, a 25% chance").',
      '**Population:** every member of the group being studied. **Sample:** the part we actually collect data from, chosen to represent the population.',
      '**Census:** data from every member (accurate but slow and costly). **Sampling:** data from some members (fast and cheap, but it must be representative).',
      '**Simple random sampling (lottery method):** number every member, draw numbers from a hat (or random numbers) so that every group of the chosen size has the same chance.'),
    TB('popsam-tb', 'Population or sample? (Examples 2.1, Exercise 2.1)', 43, ['Study', 'Population', 'Sample'],
       [['newspaper readers (2009 study)', 'all Eritreans', 'the 963 people interviewed'],
        ['Coca-Cola quality check', 'all bottles produced that day', 'the 150 bottles tested'],
        ['Baito election poll', 'the 1800 registered voters', 'the 300 polled'],
        ['pass rate of a course', 'all students who took it (3 years)', 'the 37 students checked']]),
    RM('bias-rm', 'A biased sample (Activity 2.3)', 44, 'Selam\'s idea — ask only students in the first row who are excellent — is quick but **biased**: those students are not typical. Ahmed\'s lottery gives every student the same chance, so the sample is representative.'),
    'math12-u2-tblE1', 'math12-u2-l2-1-r3r1', 'math12-u2-xt1',
]

# ------------------------------------------------------------------ 2.2
L2 = [
    T('=math12-u2-c02', '2.2.1 Types of data', 47,
      'A **variable** is a characteristic that changes from member to member (height, blood type, number of children). One value is a **datum**; the collection is the **data**.',
      '**Qualitative (categorical):** a label or category — sex, blood type, Zoba, disease status.',
      '**Quantitative (numerical):** a count or measurement. It is **discrete** if the values can be counted (number of children, pages, calls: 0, 1, 2, …) and **continuous** if it can take any value in a range (height, time, rainfall, income measured exactly).',
      '**Quick test:** "how many?" → discrete; "how much / how long / how heavy?" → continuous.'),
    TB('types-tb', 'Classifying variables (Exercise 2.2)', 50, ['Variable', 'Type'],
       [['smoking status, HIV status, sex, ethnic group', 'qualitative'], ['rank in class', 'qualitative (ordered)'],
        ['number of children, cups of tea, visits to a doctor', 'quantitative, discrete'], ['annual income, body temperature, time', 'quantitative, continuous']]),
    T('freq-t', '2.2.2–2.2.3 Frequency tables', 52,
      '**Frequency** = how many times a value occurs. **Relative frequency** = frequency ÷ total; **percentage** = relative frequency × 100%. **Cumulative frequency** = running total up to that value.',
      '**Activity 2.8 (blood types of 40 students):** O 16, B 10, A 9, AB 5 — percentages 40%, 25%, 22.5%, 12.5%. Most common O, least common AB.',
      '**Example 2.6 (corrected):** dog 11, cow 10, goat 4, sheep 3, cat 2 (30 children). The **least** liked animal is the **cat** (the book says "cow"), the number who like dogs **or** cats is $11 + 2 = 13$ (the book adds cows and dogs: 21), and the proportion who like sheep is $\\frac{3}{30} = 0.1$.',
      '**Example 2.7:** women with fewer than 3 children: $7 + 8 + 11 = 26$ women (52%); more than 1 child: $11 + 14 + 8 + 2 = 35$ (70%).'),
    ST('classes', 'Grouped data: limits, boundaries, class mark', 58, 'classes',
       [('Class **limits** are the end numbers written in the table: 20 – 29.', 'k1'),
        ('Class **boundaries** close the gaps between classes: halfway between 29 and 30 is 29.5, so the class runs from 19.5 to 29.5. **Class width** = upper boundary − lower boundary = 10.', 'k2'),
        ('**Class mark** (midpoint) $= \\frac{20 + 29}{2} = 24.5$ — the value that stands for the whole class in calculations and graphs.', 'k3')]),
    TB('ex29-tb', 'Example 2.9: wages of 30 workers', 60, ['Wages (Nakfa)', 'Frequency', 'Cumulative'],
       [['800 – 810', '3', '3'], ['810 – 820', '2', '5'], ['820 – 830', '1', '6'], ['830 – 840', '9', '15'], ['840 – 850', '5', '20'],
        ['850 – 860', '1', '21'], ['860 – 870', '3', '24'], ['870 – 880', '1', '25'], ['880 – 890', '1', '26'], ['890 – 900', '4', '30']]),
    RM('ex28-rm', 'Reading a grouped table (Example 2.8)', 59, 'With classes 0–10, 10–20, … the width is 10. Marks of at most 40: add the frequencies up to the class 30–40: $2 + 10 + 21 + 19 = 52$ (the book\'s line says "less than or 60" but means 40). Wages of 850 or more in Example 2.9: $1 + 3 + 1 + 1 + 4 = 10$ workers.'),
    'math12-u2-chkE2', 'math12-u2-pc21', 'math12-u2-pc22', 'math12-u2-pc23', 'math12-u2-xt2', 'math12-u2-xw2', 'math12-u2-chkE1',
]

# ------------------------------------------------------------------ 2.3
L3 = [
    'math12-u2-c03',
    DG('pie', 'Pie chart: angle = percent × 3.6°', 64, 'pie',
       'Each sector angle $= \\frac{\\text{frequency}}{\\text{total}} \\times 360°$: Food $35\\% \\to 126°$, Rent $90°$, Savings $72°$, Misc. $54°$, Education $18°$. With an income of 1500 Nakfa: food $0.35 \\times 1500 = 525$, education 75, rent and savings $375 + 300 = 675$ Nakfa (the book\'s line prints "75" for the rent part).'),
    ST('hist', 'Histogram and frequency polygon (Example 2.13)', 69, 'hist',
       [('**Histogram:** bars stand on the class boundaries and **touch** (no gaps), heights = frequencies.', 'k1'),
        ('**Frequency polygon:** join the midpoints of the bar tops (class marks 5, 15, 25, …) with straight lines, and close it down to the axis at both ends.', 'k2'),
        ('The tallest bar is the **modal class** (20 – 30, frequency 21).', 'k3')]),
    TB('graphs-tb', 'Which graph?', 63, ['Data', 'Graph', 'Key rule'],
       [['parts of a whole', 'pie chart', 'angle = share × 360°'], ['categories, or comparing groups', 'bar / double bar graph', 'equal widths, gaps between bars'],
        ['grouped numbers', 'histogram, frequency polygon', 'bars touch; polygon through class marks'], ['change over time', 'line graph', 'time on the horizontal axis']]),
    'math12-u2-chk74', 'math12-u2-wrk1', 'math12-u2-pc31', 'math12-u2-pc32', 'math12-u2-pc33', 'math12-u2-xw3', 'math12-u2-xt3',
]

# ------------------------------------------------------------------ 2.4
L4 = [
    T('=math12-u2-c04', '2.4.1 Mean, median and mode', 79,
      'A **measure of central tendency** is one value that represents the whole data set.',
      '**Mean:** $\\bar{x} = \\frac{x_1 + x_2 + \\dots + x_N}{N} = \\frac{\\sum x_i}{N}$. Example 2.15: $\\frac{30}{10} = 3$ children.',
      '**Median:** sort the data. If $N$ is **odd**, it is the middle value, in position $\\frac{N + 1}{2}$. If $N$ is **even**, it is the mean of the values in positions $\\frac{N}{2}$ and $\\frac{N}{2} + 1$. (The book\'s first definition swaps "odd" and "even"; its step-by-step rule is right.)',
      '**Mode:** the most frequent value. There may be two modes (Example 2.21: 1 and 3) or none (Example 2.22).'),
    WK('ex219', 'Worked example: the median of 40 values (Example 2.19)', 81,
       'Battery lives of 40 phones, sorted: 1.6, 1.8, 2.2, …, 4.7. Find the median.',
       ['$N = 40$ is even: the middle positions are 20 and 21.', 'Counting in the sorted list: $x_{(20)} = 3.4$ and $x_{(21)} = 3.4$.', 'Median $= \\frac{3.4 + 3.4}{2}$.'],
       '3.4 years (the mean is $\\frac{136.4}{40} = 3.41$)'),
    TB('cmp-tb', 'Mean, median or mode?', 84, ['', 'Mean', 'Median', 'Mode'],
       [['uses every value', 'yes', 'no', 'no'], ['affected by an extreme value', 'a lot', 'hardly', 'no'], ['works for categories', 'no', 'no', 'yes'], ['best for', 'balanced data', 'skewed data (incomes)', 'most popular item']]),
    RM('outlier-rm', 'One extreme value (Activity 2.22, Exercise 2.5 Q3)', 84, 'Class A ages 16, 18, 17, 18, 19, **38**: mean 21, median 18. Class B with 20 instead of 38: mean 18, median 18. One extreme value pulls the mean but not the median. Likewise 1–10 has mean 5.5, but changing 10 to 100 makes the mean 14.5 while the median stays 5.5.'),
    T('disp-t', '2.4.2 Range, variance and standard deviation', 86,
      'Two data sets can have the same centre and very different **spread** (dispersion).',
      '**Range** $R$ = largest − smallest.',
      '**Variance** = average squared distance from the mean: $$\\sigma^2 = \\frac{\\sum (x_i - \\bar{x})^2}{N}$$',
      '**Standard deviation** $\\sigma = \\sqrt{\\sigma^2}$, in the same units as the data (variance is in squared units, e.g. hour²).',
      '**Shift and scale:** adding a constant to every value changes the mean but **not** the variance; multiplying every value by $k$ multiplies the standard deviation by $|k|$ (Exercise 2.6 Q3, Q4).',
      '(The book divides by $N$ and calls this the population variance; Example 2.27 calls it "sample" standard deviation and refers to Example 2.25 — it means Example 2.26. A sample variance divides by $n - 1$ instead.)'),
    DG('spread', 'Two banks, same average wait', 87, 'spread',
       'Both banks have mean 7.15 min, median 7.2 and mode 7.7, but the range at Bank A is $7.7 - 6.5 = 1.2$ min and at Bank B $10.0 - 4.2 = 5.8$ min (the book labels both lines "Bank A"). Bank B\'s waiting times vary much more.'),
    TB('var-tb', 'Example 2.26: study hours (mean 31)', 90, ['$x$', '$x - \\bar{x}$', '$(x - \\bar{x})^2$'],
       [['28', '−3', '9'], ['44', '13', '169'], ['36', '5', '25'], ['25', '−6', '36'], ['34', '3', '9'], ['30', '−1', '1'], ['32', '1', '1'], ['19', '−12', '144'], ['total 248', '0', '394']]),
    RM('var-rm', 'Reading the table', 91, 'Deviations always add to 0 (a check on the mean). $\\sigma^2 = \\frac{394}{8} = 49.25$ hour², $\\sigma = \\sqrt{49.25} \\approx 7.02$ hours.'),
    'math12-u2-c05', 'math12-u2-c06', 'math12-u2-c07', 'math12-u2-c08', 'math12-u2-chk75', 'math12-u2-wrk2', 'math12-u2-chk76', 'math12-u2-wrk3', 'math12-u2-chk77', 'math12-u2-wrk4',
    'math12-u2-chk78', 'math12-u2-wrk5', 'math12-u2-chk79', 'math12-u2-wrk6', 'math12-u2-chk80', 'math12-u2-wrk7', 'math12-u2-chk81', 'math12-u2-wrk8',
]

# ------------------------------------------------------------------ 2.5
L5 = [
    T('=math12-u2-c09', '2.5.1 Experiments, sample spaces and events', 94,
      'An **experiment** is a process with well-defined outcomes (toss a coin, roll a die). The **sample space** $S$ is the set of all outcomes; an **event** is a subset of $S$.',
      'Coin: $S = \\{H, T\\}$. Die: $\\{1, 2, 3, 4, 5, 6\\}$. Two coins: $\\{HH, HT, TH, TT\\}$. A **simple event** has one outcome; the **null event** $\\varnothing$ has none (Example 2.30: an even factor of 9).',
      '**Operations:** $A \\cap B$ (both), $A \\cup B$ (either or both), $A\'$ (not $A$). $A$ and $B$ are **mutually exclusive** if $A \\cap B = \\varnothing$.'),
    DG('tree', 'Listing outcomes with a tree', 110, 'tree',
       'Each student passes (P) or fails (F): 2 branches, then 2, then 2, so $2 \\times 2 \\times 2 = 8$ outcomes: PPP, PPF, PFP, PFF, FPP, FPF, FFP, FFF. The same tree lists D/N items (Example 2.29) or the sexes of three children.'),
    T('prob-t', '2.5.3–2.5.4 Experimental and theoretical probability', 99,
      '**Experimental probability** = relative frequency $= \\frac{\\text{times the outcome happened}}{\\text{number of trials}}$. Example 2.31: 35 of 100 students chose blue: $0.35$.',
      '**Theoretical probability** (equally likely outcomes): $$P(E) = \\frac{n(E)}{n(S)} = \\frac{\\text{favourable outcomes}}{\\text{all outcomes}}$$',
      'Always $0 \\le P(E) \\le 1$: 0 = impossible (a black card from green, yellow and blue cards), 1 = certain.',
      '**Comparing (Activity 2.34):** 13 sevens in 50 rolls of two dice gives $0.26$; theory gives $\\frac{6}{36} \\approx 0.17$. With more trials the experimental value gets closer to the theoretical one.'),
    DG('dice', 'Two dice: count the cells', 103, 'dice',
       '36 equally likely outcomes. Sum 7 appears 6 times ($P = \\frac{1}{6}$), sum 11 twice, so $P(7 \\text{ or } 11) = \\frac{8}{36} = \\frac{2}{9}$. A total of 8 appears 5 times ($\\frac{5}{36}$).'),
    ST('venn', '2.5.5 The addition law', 105, 'venn',
       [('$P(A)$ counts every outcome in $A$.', 'k1'),
        ('$P(B)$ counts every outcome in $B$ — the overlap is now counted twice.', 'k2'),
        ('Subtract it once: $$P(A \\cup B) = P(A) + P(B) - P(A \\cap B).$$ If $A$, $B$ are mutually exclusive the overlap is empty and $P(A \\cup B) = P(A) + P(B)$.', 'k3')]),
    TB('laws-tb', 'Laws of probability', 105, ['Law', 'Formula', 'Example'],
       [['complement', "$P(A') = 1 - P(A)$", 'Rahma wins: $1 - 0.7 = 0.3$'],
        ['addition', '$P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$', '$0.7 = P(A) + 0.4 - 0.3$: $P(A) = 0.6$'],
        ['multiplication (independent)', '$P(A \\cap B) = P(A)P(B)$', 'green then yellow: $\\frac{5}{16} \\cdot \\frac{6}{16} = \\frac{15}{128}$']], layout='cards'),
    RM('indep-rm', 'Only for independent events', 107, 'The rule $P(A \\cap B) = P(A) \\cdot P(B)$ holds when one event does not change the chances of the other: two different dice, a coin and a die, or drawing **with replacement**. The book states it for "events A and B" in general; it is not true for, e.g., "even" and "greater than 3" on one die ($\\frac{2}{6} \\ne \\frac{1}{2} \\cdot \\frac{1}{2}$).'),
    T('count-t', '2.5.6 Counting: the multiplication principle', 110,
      'If one choice can be made in $m$ ways and then another in $n$ ways, together there are $m \\times n$ ways; for more steps keep multiplying. Breakfast: $4 \\times 3 \\times 5 = 60$ choices; outfits: $2 \\times 3 \\times 2 = 12$.',
      'Arranging $n$ different objects in a line: $n!$ ways (FAST: $4! = 24$ words).'),
    TB('count-tb', 'Permutations or combinations?', 114, ['Situation', 'Formula', 'Example'],
       [['order matters, $r$ from $n$', '$_nP_r = \\frac{n!}{(n - r)!}$', '6 teachers to 4 classes: $_6P_4 = 360$'],
        ['order does not matter', '$_nC_r = \\frac{n!}{r!(n - r)!}$', 'committee of 3 from 4: $_4C_3 = 4$'],
        ['in a circle', '$(n - 1)!$', '6 people: $5! = 120$'],
        ['repeated letters', '$\\frac{n!}{n_1!\\,n_2! \\cdots}$', 'STATISTICS: $\\frac{10!}{3!3!2!} = 50400$']], layout='cards'),
    WK('ex244', 'Worked example: Example 2.44(b) (corrected)', 117,
       'The letters of STATISTICS are arranged at random. Probability that the arrangement begins with SSS?',
       ['All arrangements: $\\frac{10!}{3!\\,3!\\,2!} = 50400$.', 'After SSS the other 7 letters are T, T, T, I, I, A, C: $\\frac{7!}{3!\\,2!} = \\frac{5040}{12} = 420$ arrangements (the book gets 84).',
        '$P = \\frac{420}{50400} = \\frac{1}{120}$.', 'Check another way: the first three letters are S with probability $\\frac{3}{10} \\cdot \\frac{2}{9} \\cdot \\frac{1}{8} = \\frac{1}{120}$.'],
       '$\\frac{1}{120} \\approx 0.0083$ (not 0.0017)'),
    WK('ex243', 'Worked example: friends at a round table (Example 2.43)', 115,
       'Six students sit at a round table. Probability that two best friends sit together?',
       ['All arrangements: $(6 - 1)! = 120$.', 'Glue the friends into one unit: 5 units round a table: $4! = 24$, times $2!$ for the friends\' order: 48.', '$P = \\frac{48}{120}$.'],
       '$\\frac{2}{5}$'),
    WK('ex246', 'Worked example: choosing letters (Example 2.46)', 119,
       'Two letters are chosen at random from MONDAY. Probability that both are consonants?',
       ['All choices: $_6C_2 = 15$.', 'Consonants M, N, D, Y: $_4C_2 = 6$.', '$P = \\frac{6}{15}$.'],
       '$\\frac{2}{5}$'),
    'math12-u2-c10', 'math12-u2-c11', 'math12-u2-c12', 'math12-u2-chk82', 'math12-u2-wrk9', 'math12-u2-chk83', 'math12-u2-wrk10', 'math12-u2-pc51',
    RM('summary-t', 'Unit summary', 125,
       'Population vs sample; qualitative vs quantitative (discrete / continuous).',
       'Frequency tables, class boundaries and marks; pie, bar, histogram, polygon, line graphs.',
       'Mean, median, mode; range, variance $\\frac{\\sum (x - \\bar{x})^2}{N}$, standard deviation.',
       '$P(E) = \\frac{n(E)}{n(S)}$; complement, addition and (independent) multiplication laws; $_nP_r$, $_nC_r$.'),
]

LESSONS = {'math12-u2-l2-1': L1, 'math12-u2-l2-2': L2, 'math12-u2-l2-3': L3, 'math12-u2-l2-4': L4, 'math12-u2-l2-5': L5}

# ------------------------------------------------------------------ practice
a = QSet('2.1–2.2 Practice — data and tables', 's21')
a.S(45, 'Exercise 2.1 Q3: identify population and sample: (a) 100 Barka cows weighed after a special diet (b) 400 welfare households checked for disabled children.', '(a) all Barka cows on that diet / 100 cows (b) all supported households in the city / 400 households',
    ['Step 1: the population is the whole group the question is about.', 'Step 2: the sample is what was measured.'], 'Ask: "about whom is the conclusion?"', [('Exercise 2.1 Q4: average maths mark of Grade 10?', 'population: all Grade 10 students; sample: e.g. 30 chosen by lottery.')])
a.S(50, 'Exercise 2.2 Q4: discrete or continuous? (a) candidate supported (b) time for a wound to heal (c) calls in 10 minutes (d) distance a ball is kicked (e) pages in a book (f) family income (g) suitcases lost per day (h) kilometres driven.', '(a) qualitative (not numerical) (b), (d), (f), (h) continuous; (c), (e), (g) discrete',
    ['Step 1: counts → discrete.', 'Step 2: measurements → continuous.'], 'Is it "how many" or "how much"?', [('Number of eggs laid?', 'discrete.')])
a.S(61, 'Exercise 2.3 Q1: ratings A A A A B A B B A A E C A C D A B C D B. Frequencies? How many gave B?', 'A 9, B 5, C 3, D 2, E 1; 5 gave B',
    ['Step 1: tally each letter.', 'Step 2: relative frequency, e.g. A: $\\frac{9}{20} = 45\\%$.'], 'Frequencies must add to 20.', [('Percentage for C?', '15%.')])
a.S(61, 'Exercise 2.3 Q2: 66 injuries (Sp, Co, Fr, St). Most and least common? Proportion of fractures?', 'sprain 20 (most), contusion 18, fracture 17, strain 11 (least); $\\frac{17}{66} \\approx 0.26$',
    ['Step 1: tally the four codes.', 'Step 2: $17 \\div 66$.'], 'Check the total is 66.', [('Proportion of strains?', '$\\frac{11}{66} = \\frac{1}{6}$.')])
a.S(62, 'Exercise 2.3 Q4: a die rolled 200 times gives 1: 30, 2: 32, 3: 35, 4: 34, 5: 37, 6: 32. Least and most frequent? $P(3)$? Proportion of even numbers?', '1 least, 5 most; 0.175; 0.49',
    ['Step 1: $\\frac{35}{200}$.', 'Step 2: $\\frac{32 + 34 + 32}{200} = \\frac{98}{200}$.'], 'Close to $\\frac{1}{6}$ and $\\frac{1}{2}$: the die looks fair.', [('Proportion of numbers above 4?', '$\\frac{69}{200} = 0.345$.')])
a.S(62, 'Exercise 2.3 Q5: ages 20–29, 30–39, 40–49, 50–59, 60–69. Upper limit of 30–39? Lower boundary of 50–59? Class mark of 40–49?', '39; 49.5; 44.5',
    ['Step 1: limits are the printed numbers.', 'Step 2: boundary halfway between 49 and 50.', 'Step 3: $\\frac{40 + 49}{2}$.'], 'Boundaries end in .5 for whole-number data.', [('Width of each class?', '10.')])
a.M(51, 'Which is a continuous variable?', ['yearly rainfall in Asmara', 'number of bicycles parked', 'blood type', 'number of children'], 'A',
    ['Step 1: rainfall is measured and can take any value.'], 'Measured ⇒ continuous.', [('Number of absent students?', 'discrete.')])
a.TF(58, 'For classes 20–29, 30–39, … the class width is 9.', False, ['Step 1: width = 29.5 − 19.5 = 10 (use boundaries, or lower limits: 30 − 20).'], 'Never subtract the two limits of one class.', [('Classes 0–4, 5–9?', 'width 5.')])

b = QSet('2.3–2.4 Practice — graphs and measures', 's22')
b.S(74, 'Exercise 2.4 Q2: shirts Blue 18, Green 9, Red 6, Yellow 3 (36 people). Pie chart angles?', 'Blue 180°, Green 90°, Red 60°, Yellow 30°',
    ['Step 1: angle $= \\frac{f}{36} \\times 360° = 10f$.'], 'Angles must add to 360°.', [('If 40 people, Blue 20?', '180°.')])
b.S(78, 'Exercise 2.4 Q14: heart beats 65–68: 2, 68–71: 4, 71–74: 3, 74–77: 8, 77–80: 7, 80–83: 4, 83–86: 2. (a) Women at risk (more than 80)? (b) Proportion between 74 and 83?', '6 women; $\\frac{19}{30}$',
    ['Step 1: $4 + 2$.', 'Step 2: $\\frac{8 + 7 + 4}{30}$.'], 'Read whole classes.', [('Proportion below 74?', '$\\frac{9}{30} = 0.3$.')])
b.S(84, 'Exercise 2.5 Q1: times 15, 28, 25, 48, 22, 43, 49, 32, 22, 39, 31, 43, 49, 32, 22, 33, 27, 25, 22, 20, 24. Mean, median, mode?', 'mean 31, median 28, mode 22',
    ['Step 1: sum 651, $\\frac{651}{21} = 31$.', 'Step 2: sorted, the 11th value is 28.', 'Step 3: 22 occurs 4 times.'], 'Sort before the median.', [('Range?', '34 min.')])
b.S(84, 'Exercise 2.5 Q2: mean, median, mode of (a) 18, 23, 7, 33, 25, 26, 23, 42, 18, 23, 11 (b) 25, 26, 27, 28, 25, 28, 29, 30, 31, 30, 26, 27, 28.', '(a) ≈ 22.6, 23, 23 (b) ≈ 27.7, 28, 28',
    ['Step 1: (a) sum 249 ÷ 11.', 'Step 2: (b) sum 360 ÷ 13; middle (7th) value 28.'], 'Count the values first.', [('(c) 103, 99, 114, 22, 99, 119, 117, 105, 100, 119, 108, 96?', 'mean ≈ 100.1, median 104, modes 99 and 119.')])
b.S(85, 'Exercise 2.5 Q4 and Q6: (4) mean expenditure of 800, 700, 1000, 750, 1500, 1800, 1200, 250, 2100, 370. (6) Male mean 1520, female 1420, all 500 employees 1500: percent male?', '1047 Nakfa; 80% male (400), 20% female (100)',
    ['Step 1: $\\frac{10470}{10}$.', 'Step 2: $1520p + 1420(1 - p) = 1500 \\Rightarrow 100p = 80$.'], 'Weighted mean.', [('All-employee mean 1470?', '50% male.')])
b.S(92, 'Exercise 2.6 Q1: 8, 18, 10, 20, 24, 12, 14, 16, 6, 22. Range, variance, standard deviation?', '18; 33; ≈ 5.74',
    ['Step 1: range $24 - 6$.', 'Step 2: mean 15; squared deviations add to 330.', 'Step 3: $\\frac{330}{10} = 33$, $\\sqrt{33}$.'], 'Table: $x$, $x - \\bar{x}$, $(x - \\bar{x})^2$.', [('Variance of 2, 4, 6?', '$\\frac{8}{3}$.')])
b.S(92, 'Exercise 2.6 Q2: mean and variance of (a) 1, 3, 6, 7, 8, 9 (b) 11, 14, 18, 23, 29 (d) 200, 203, 206, 207, 209.', '(a) 5.67, 7.89 (b) 19, 41.2 (d) 205, 10',
    ['Step 1: (b) deviations −8, −5, −1, 4, 10; squares add to 206; $\\frac{206}{5}$.', 'Step 2: (d) subtract 200 first: 0, 3, 6, 7, 9 has mean 5, variance 10.'], 'Subtracting a constant does not change the variance.', [('(c) 4.6, 2.7, 3.1, 0.5, 6.2?', 'mean 3.42, variance ≈ 3.65.')])
b.S(92, 'Exercise 2.6 Q3–Q4: (3) 4, 6, 9, 3, 5, 6, 9 has mean 6 and variance $\\frac{32}{7}$. Deduce for 514, 516, … (add 510) and 52, 78, … (×13). (4) SD of 1–7 is 2; find the SD of 101–107, of 100, 200, …, 700, and of 2.01, 3.02, …, 8.07.', 'mean 516, var 32/7; mean 78, var 5408/7 ≈ 772.6; SDs 2, 200, 2.02',
    ['Step 1: adding 510 moves the mean only.', 'Step 2: ×13 multiplies the variance by 169.', 'Step 3: 2.01, 3.02, … $= 1.01k + 1$, so SD $= 1.01 \\times 2$.'], 'Shift: SD same; scale by $k$: SD × $|k|$.', [('SD of 3, 6, …, 21?', '6.')])
b.S(93, 'Exercise 2.6 Q5: Bakery 1: 96, 98, 98, 99, 100, 100, 101, 101, 102, 105. Bakery 2: 92, 94, 95, 98, 100, 101, 103, 104, 106, 107. Means, SDs, which bakery follows the 100 g rule?', 'both mean 100 g; SD ≈ 2.37 g and ≈ 4.90 g; Bakery 1',
    ['Step 1: both sums are 1000.', 'Step 2: variances 5.6 and 24.', 'Step 3: smaller SD ⇒ weights stay close to 100 g.'], 'Same mean? Compare the spread.', [('Ranges?', '9 g and 15 g.')])
b.S(123, 'Review Q8: orders 34, 39, 40, 46, 33, 31, 34, 14, 15, 45. Mean, median, mode, range, variance, SD.', '33.1; 34; 34; 32; 108.89; ≈ 10.4',
    ['Step 1: sum 331.', 'Step 2: sorted middle values 34 and 34.', 'Step 3: $\\sum (x - 33.1)^2 = 1088.9$, divide by 10.'], 'Dividing by $n - 1 = 9$ instead gives the sample variance ≈ 121.0.', [('Without the 14 and 15?', 'mean 37.75.')])
b.S(123, 'Review Q9–Q10: (9) mean 40; adding 50 and 64 makes the mean 42. How many items at first? (10) bill-paying days (30 values, sum 1220): mean, median, modes, range.', '15 items; 40.67, 39.5, modes 13, 34, 41, 47, range 79',
    ['Step 1: $40n + 114 = 42(n + 2)$, so $2n = 30$.', 'Step 2: median $\\frac{38 + 41}{2}$; four values occur 3 times each.'], 'Total = mean × count.', [('Mean 50 rising to 52 after adding 60 and 70?', '13 items.')])
b.M(84, 'Which measure is least affected by one very large value?', ['median', 'mean', 'range', 'variance'], 'A',
    ['Step 1: the median depends only on the middle position.'], 'Outliers drag the mean.', [('Which uses every value?', 'the mean.')])
b.TF(90, 'Adding 5 to every value increases the standard deviation by 5.', False, ['Step 1: every deviation $x - \\bar{x}$ stays the same.'], 'Shifts don\'t change spread.', [('Doubling every value?', 'doubles the SD.')])

c = QSet('2.5 Practice — probability and counting', 's23')
c.S(103, 'Exercise 2.8 Q1–Q2: (1) a coin tossed twice: $P$(at least one head)? (2) a die where each even number is twice as likely as each odd number: $P$(more than 3)?', '$\\frac{3}{4}$; $\\frac{5}{9}$',
    ['Step 1: $1 - P(TT) = 1 - \\frac{1}{4}$.', 'Step 2: odd $p$, even $2p$: $9p = 1$; $P(4, 5, 6) = 2p + p + 2p = \\frac{5}{9}$.'], 'Probabilities must add to 1.', [('In Q2, $P$(even)?', '$\\frac{2}{3}$.')])
c.S(103, 'Exercise 2.8 Q3–Q5: (3) a random letter of the alphabet is a consonant / comes after j / comes before g. (5) 40 students: names start A 23, B 12, D 5: $P(B)$, $P(\\text{not } D)$, $P(T)$.', '21/26, 8/13, 3/13; 3/10, 7/8, 0',
    ['Step 1: 21 consonants; k–z is 16 letters; a–f is 6.', 'Step 2: $\\frac{12}{40}$, $1 - \\frac{5}{40}$.'], 'Count favourable outcomes carefully.', [('Exercise 2.8 Q4: 8 brown of 12 eggs, $P$(white)?', '$\\frac{1}{3}$.')])
c.S(108, 'Exercise 2.9 Q1–Q3: (1) $P(C) = \\frac{2}{3}$, $P(Ph) = \\frac{4}{9}$, both $\\frac{2}{9}$: at least one? (2) total 7 or 11 with two dice? (3) at least one tail in 6 tosses?', '8/9; 2/9; 63/64',
    ['Step 1: $\\frac{6}{9} + \\frac{4}{9} - \\frac{2}{9}$.', 'Step 2: $\\frac{6 + 2}{36}$.', 'Step 3: $1 - (\\frac{1}{2})^6$.'], '"At least one" ⇒ complement.', [('At least one head in 3 tosses?', '$\\frac{7}{8}$.')])
c.S(108, 'Exercise 2.9 Q4–Q6: (4) 10% defective: $P$(not defective)? (5) $A$, $B$ mutually exclusive, $P(A) = 0.3$, $P(B) = 0.5$: $P(A \\cup B)$, $P(A\')$, $P(A \\cap B)$. (6) 3 green, 5 white, 7 yellow; two draws with replacement: both green?', '0.9; 0.8, 0.7, 0; 1/25',
    ['Step 1: complement.', 'Step 2: no overlap.', 'Step 3: $(\\frac{3}{15})^2$.'], 'With replacement ⇒ independent.', [('(6) both yellow?', '$\\frac{49}{225}$.')])
c.S(120, 'Exercise 2.11 Q1–Q4: (1) 3 roads Asmara–Barentu, 2 Barentu–Tessenei (2) 6 shirts, 4 trousers (3) plates with 2 letters then 4 digits (4) 3 boys and 2 girls in a line.', '6; 24; 6,760,000; 120',
    ['Step 1: $3 \\times 2$, $6 \\times 4$.', 'Step 2: $26^2 \\times 10^4$.', 'Step 3: $5!$.'], 'Multiplication principle.', [('Plates with 3 letters then 3 digits?', '17,576,000.')])
c.S(120, 'Exercise 2.11 Q5–Q7: (5) the two girls together (6) boys together and girls together (7) 4 English, 3 maths, 2 biology, 1 chemistry book with each subject together.', '48; 24; 6912',
    ['Step 1: glue the girls: $4! \\times 2!$.', 'Step 2: 2 blocks: $2! \\times 3! \\times 2!$.', 'Step 3: 4 blocks: $4! \\times 4! \\times 3! \\times 2!$.'], 'Arrange the blocks, then inside each block.', [('Girls never together?', '$120 - 48 = 72$.')])
c.S(121, 'Exercise 2.11 Q8–Q9: (8) 4 courses from 10, order important (9) 3 books from 7, order not important.', '5040; 35',
    ['Step 1: $_{10}P_4 = 10 \\cdot 9 \\cdot 8 \\cdot 7$.', 'Step 2: $_7C_3 = \\frac{7 \\cdot 6 \\cdot 5}{3!}$.'], 'Order matters ⇒ P; does not ⇒ C.', [('$_{10}C_4$?', '210.')])
c.S(124, 'Review Q12–Q14: (12) 3 of 5 coloured balls: $P$(black chosen), $P$(black and red)? (13) two dice: total 8; total at most 5? (14) 3 of 9 books (5 maths, 3 history, 1 dictionary): $P$(dictionary), $P$(2 maths, 1 history)?', '3/5, 3/10; 5/36, 5/18; 1/3, 5/14',
    ['Step 1: $\\frac{_4C_2}{_5C_3} = \\frac{6}{10}$; $\\frac{_3C_1}{10}$.', 'Step 2: 5 cells; $1 + 2 + 3 + 4 = 10$ cells.', 'Step 3: $\\frac{_8C_2}{_9C_3} = \\frac{28}{84}$; $\\frac{10 \\times 3}{84}$.'], 'Choose the "must" items first.', [('(14) no maths book?', '$\\frac{4}{84} = \\frac{1}{21}$.')])
c.S(124, 'Review Q16 and Q19: (16) $P$(A fails) = 0.2, $P$(B fails) = 0.3, independent: both, only one, at least one, none. (19) succeed 0.8 and 0.6: both, at least one.', '0.06, 0.38, 0.44, 0.56; 0.48, 0.92',
    ['Step 1: $0.2 \\times 0.3$; $0.2(0.7) + 0.8(0.3)$.', 'Step 2: none $0.8 \\times 0.7$; at least one $1 - 0.56$.', 'Step 3: $0.8 \\times 0.6$; $1 - 0.2 \\times 0.4$.'], 'List the four cases.', [('(19) exactly one?', '0.44.')])
c.S(125, 'Review Q17–Q18: (17) one number from 1–10: even; divisible by 3; odd or divisible by 3; larger than 6 or less than 3. (18) rain 0.6, lightning 0.3, both 0.2: no rain, rain or lightning, rain but no lightning, neither.', '1/2, 3/10, 3/5, 3/5; 0.4, 0.7, 0.4, 0.3',
    ['Step 1: odd {1, 3, 5, 7, 9} plus 6: 6 numbers.', 'Step 2: $0.6 + 0.3 - 0.2 = 0.7$; $0.6 - 0.2$; $1 - 0.7$.'], 'Venn diagram regions.', [('(18) lightning but no rain?', '0.1.')])
c.M(113, 'Plates with letters M, S, T then digits 1, 2, 3, each used once (Example 2.41):', ['36', '720', '6', '12'], 'A',
    ['Step 1: $3! \\times 3!$.'], 'Two separate arrangements multiply.', [('With 4 letters and 3 digits?', '144.')])
c.TF(107, '$P(A \\cap B) = P(A) \\cdot P(B)$ for any two events.', False,
     ['Step 1: only for independent events. One die: $P(\\text{even and} > 3) = \\frac{2}{6}$, but $\\frac{1}{2} \\cdot \\frac{1}{2} = \\frac{1}{4}$.'], 'Check independence first.', [('Coin and die?', 'True: independent.')])

QS = a.items + b.items + c.items

GLOSSARY = [
    ('Population', 'Every member of the group being studied.', 42),
    ('Sample', 'The part of the population that data are collected from.', 42),
    ('Class boundary', 'The value halfway between neighbouring class limits.', 58),
    ('Standard deviation', 'The square root of the variance; spread in the data\'s units.', 91),
    ('Sample space', 'The set of all possible outcomes of an experiment.', 94),
    ('Mutually exclusive', 'Events that cannot happen together.', 97),
    ('Combination', 'A selection where order does not matter.', 118),
]
TIPS = [('Sort the data before finding the median.', 81), ('Pie angle = share × 360°.', 64), ('"At least one" → 1 − P(none).', 108), ('Order matters → P; not → C.', 118)]
IDEAS = [('mmm', 'Mean, median, mode', 'l2_4', 'math12-u2-c04'), ('disp', 'Variance and SD', 'l2_4', 'math12-u2-md-disp-t'),
         ('prob', 'Probability laws', 'l2_5', 'math12-u2-md-laws-tb'), ('count', 'Permutations and combinations', 'l2_5', 'math12-u2-md-count-tb')]
