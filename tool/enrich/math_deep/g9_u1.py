r"""Grade 9 Unit 1 — Set Theory (pp. 1-19)."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, CK, QSet
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from figs_common import side_by_side, arrow_diagram, venn2, SHADE

UID = 'math9-u1'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_numsets():
    f = Fig(330, 210)
    f.rect(6, 6, 318, 198, PURPLE, 2, FILL[PURPLE], 14)
    f.text(20, 26, 'R  real numbers', 12.5, PURPLE, 'start')
    f.text(300, 120, '√2', 13, PURPLE, 'end').text(300, 150, 'π', 13, PURPLE, 'end')
    f.rect(18, 36, 248, 160, GREEN, 2, FILL[GREEN], 12)
    f.text(30, 54, 'Q  rational', 12.5, GREEN, 'start')
    f.text(242, 90, '½', 13, GREEN, 'end').text(246, 180, '−0.75', 12, GREEN, 'end')
    f.rect(30, 64, 176, 124, ORANGE, 2, FILL[ORANGE], 10)
    f.text(42, 82, 'Z  integers', 12.5, ORANGE, 'start')
    f.text(186, 112, '−3', 13, ORANGE, 'end').text(186, 176, '−1', 13, ORANGE, 'end')
    f.rect(42, 92, 118, 88, BLUE, 2, FILL[BLUE], 8)
    f.text(54, 110, 'N  natural', 12.5, BLUE, 'start')
    f.text(101, 145, '1, 2, 3, …', 13, BLUE)
    return f


def f_oneone():
    a = arrow_diagram([(1, 'a'), (2, 'b'), (3, 'c')], [1, 2, 3], ['a', 'b', 'c'], 'A', 'B', title='equivalent')
    c = arrow_diagram([(1, 'p'), (2, 'q'), (3, 'r')], [1, 2, 3], ['p', 'q', 'r', 't'], 'A', 'C', title='NOT equivalent')
    f = side_by_side([a, c], 0)
    f.circle(170 + 138, 40 + 18 + (4 * 30 + 18) / 2 + 1.5 * 30, 13, RED, 2)
    return f


def f_subset():
    a = Fig(165, 150)
    a.rect(5, 5, 155, 120, INK, 1.4, 'none', 8)
    a.ellipse(82, 66, 70, 52, RED, 2, FILL[RED]).text(124, 34, 'B', 13, RED)
    a.ellipse(66, 72, 36, 28, BLUE, 2, FILL[BLUE]).text(66, 77, 'A', 13, BLUE)
    a.text(130, 90, '7', 12, INK)
    a.text(82, 143, 'A is a proper subset of B', 11.5, INK)
    b = Fig(165, 150)
    b.rect(5, 5, 155, 120, INK, 1.4, 'none', 8)
    b.ellipse(82, 66, 66, 48, PURPLE, 2.4, FILL[PURPLE]).text(82, 71, 'A = B', 13, PURPLE)
    b.text(82, 143, 'A = B: each is a subset', 11.5, INK)
    return side_by_side([a, b], 4)


def f_unionint():
    figs = []
    for sh, cap in (('union', 'union: A or B'), ('inter', 'intersection: A and B')):
        g = Fig(165, 135)
        venn2(g, 4, 6, 157, 104, sh, nums=('0', '2\n3', '7', None), cap=cap, size=13.5)
        figs.append(g)
    return side_by_side(figs, 4)


def f_disjoint():
    f = Fig(300, 140)
    f.rect(6, 6, 288, 108, INK, 1.4, 'none', 8).text(14, 22, 'U', 12, GREY, 'start')
    f.circle(95, 62, 44, BLUE, 2, FILL[BLUE]).circle(210, 62, 40, RED, 2, FILL[RED])
    f.text(60, 26, 'A', 13, BLUE).text(246, 28, 'C', 13, RED)
    f.text(82, 58, '0', 13).text(108, 58, '2', 13).text(95, 80, '3', 13).text(197, 67, '7', 13).text(223, 67, '8', 13)
    f.text(150, 132, 'no common element: A and C are disjoint', 12, INK)
    return f


def f_survey():
    f = Fig(320, 175)
    venn2(f, 6, 18, 308, 140, None, 'bicycle 63', 'calculator 84', 'U = 150',
          nums=('36', '27', '57', '30'), steps=('k2 k3 k4 k5', 'k1 k2 k3 k4 k5', 'k3 k4 k5', 'k4 k5'), r=56, d=34)
    f.raw('<g data-hl="k5">')
    f.rect(9, 21, 302, 134, ORANGE, 3, 'none', 8)
    f.raw('</g>')
    return f


def f_fig15():
    f = Fig(300, 165)
    venn2(f, 6, 6, 288, 140, None, nums=('3\n7', '1\n5', '2\n4', None), r=58, d=34, size=14)
    f.text(52, 132, '6', 14).text(270, 135, '0', 14)
    f.text(150, 160, 'U = {0, 1, 2, 3, 4, 5, 6, 7}', 12, GREY)
    return f


def f_ops4():
    figs = []
    for sh, cap in (('notA', "A′ (outside A)"), ('AmB', 'A − B (A only)'), ('BmA', 'B − A (B only)'), ('notU', "(A or B)′ (outside both)")):
        g = Fig(165, 128)
        venn2(g, 4, 4, 157, 98, sh, cap=cap, r=34, d=20)
        figs.append(g)
    top = side_by_side(figs[:2], 4)
    bot = side_by_side(figs[2:], 4)
    f = Fig(334, 262)
    f.raw('<g>' + ''.join(top.p) + '</g>')
    f.raw('<g transform="translate(0,134)">' + ''.join(bot.p) + '</g>')
    return f


def f_demorgan():
    figs = []
    for sh, cap, s in (('notA', 'step 1: shade A′', 'k1'), ('notB', 'step 2: shade B′', 'k2'), ('notU', "overlap = (A or B)′", 'k3')):
        g = Fig(110, 108)
        g.g(s)
        venn2(g, 3, 4, 104, 80, sh, cap=cap, r=24, d=14)
        g.end()
        figs.append(g)
    return side_by_side(figs, 2)


def f_seating():
    f = Fig(320, 206)
    x0, y0, s = 40, 12, 26
    for col in range(10):
        for row in range(6):
            x, y = x0 + col * s, y0 + (5 - row) * s
            fill = SHADE if (col, row) == (3, 2) else ('#E3EDF7' if (col, row) == (2, 0) else '#ffffff')
            f.rect(x, y, s - 3, s - 3, GREY, 1, fill, 3)
    f.text(x0 + 2 * s + 11, y0 + 5 * s + 17, 'S', 13, BLUE)
    for col in range(10):
        f.text(x0 + col * s + 11, y0 + 6 * s + 12, str(col + 1), 11.5, INK)
    for row in range(6):
        f.text(x0 - 10, y0 + (5 - row) * s + 17, str(row + 1), 11.5, INK)
    f.text(x0 + 5 * s, y0 + 6 * s + 30, 'column (first number)', 12, INK)
    f.text(14, y0 + 2 * s, 'row', 12, INK, 'middle')
    f.text(x0 + 3 * s + 11, y0 + 3 * s - 6, '(4, 3)', 11, RED)
    return f


def f_axb():
    f = Fig(300, 230)
    O = (50, 190)
    u = 34
    X = lambda v: O[0] + v * u
    Y = lambda v: O[1] - v * 27
    f.arrow(O[0], O[1], 290, O[1], INK, 1.6, 7).arrow(O[0], O[1], O[0], 12, INK, 1.6, 7)
    for a in (2, 4, 5):
        f.line(X(a), O[1], X(a), Y(6.4), BLUE, 1, dash='3 3').text(X(a), O[1] + 16, str(a), 12.5, BLUE)
    for b in (1, 3, 6):
        f.line(O[0], Y(b), X(5.6), Y(b), GREEN, 1, dash='3 3').text(O[0] - 10, Y(b) + 4, str(b), 12.5, GREEN)
    for a in (2, 4, 5):
        for b in (1, 3, 6):
            f.dot(X(a), Y(b), RED, 4)
    f.text(X(4) + 2, Y(3) - 8, '(4, 3)', 11, RED, 'start')
    f.text(268, O[1] + 16, 'A', 13, BLUE).text(O[0] - 14, 22, 'B', 13, GREEN)
    f.text(175, 226, '3 × 3 = 9 ordered pairs', 12, INK)
    return f


DIAGRAMS = {
    'numsets': (f_numsets(), 'Number sets inside one another: N, Z, Q, R', 8),
    'oneone': (f_oneone(), 'One-to-one correspondence (Fig. 1.1 and 1.2)', 5),
    'subset': (f_subset(), 'Subset pictures (Fig. 1.3)', 7),
    'unionint': (f_unionint(), 'Union and intersection of A = {0, 2, 3} and B = {2, 3, 7}', 10),
    'disjoint': (f_disjoint(), 'Disjoint sets', 10),
    'survey': (f_survey(), 'Survey Venn diagram (Activity 1.11)', 11),
    'fig15': (f_fig15(), 'Venn diagram with elements (Fig. 1.5)', 12),
    'ops4': (f_ops4(), 'Complement and difference regions (Fig. 1.6 and 1.7)', 13),
    'demorgan': (f_demorgan(), "De Morgan's law with shading", 14),
    'seating': (f_seating(), 'A seating plan: positions are ordered pairs', 16),
    'axb': (f_axb(), 'A × B drawn as a grid of points', 17),
}

# ------------------------------------------------------------------ lesson 1.1
L1 = [
    T('=math9-u1-c01', '1.1 What is a set?', 1,
      'A **set** is a **well-defined** collection of objects. "Well-defined" means that for any object we can say clearly **yes, it belongs** or **no, it does not**. The objects are called **elements** (or members).',
      '- "The vowels of the English alphabet" is a set: a, e, i, o, u — everybody agrees.',
      '- "The tall students in our class" is **not** a set: "tall" is an opinion, so two people could list different students.',
      'We name sets with capital letters and write the elements inside braces: $A = \\{a, b, c\\}$. We write $a \\in A$ ("$a$ is an element of $A$") and $d \\notin A$ ("$d$ is not an element of $A$").',
      'Two rules about listing: **order does not matter** ($\\{1, 2, 3\\} = \\{3, 1, 2\\}$) and **repeats are written once** (the letters of "BOOK" form $\\{B, O, K\\}$).'),
    'math9-u1-tbl1',
    TB('methods-t', 'Three ways to describe a set', 2, ['Method', 'How it works', 'Example', 'Best for'],
       [['Complete listing (roster)', 'write every element inside braces', '$\\{0, 1, 2, \\dots, 10\\}$ written out in full: $\\{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10\\}$', 'small finite sets'],
        ['Partial listing (roster)', 'write the first few elements so the pattern is clear, then three dots', '$\\{2, 4, 6, 8, \\dots\\}$, the integers $\\{\\dots, -2, -1, 0, 1, 2, \\dots\\}$', 'sets with a clear pattern (often infinite)'],
        ['Set-builder notation', 'give the rule the elements must obey: $\\{x : \\text{condition on } x\\}$, read "the set of $x$ such that ..."', '$\\{x : x \\text{ is an odd integer and } 1 \\le x \\le 7\\}$', 'sets with no pattern, e.g. all real numbers'],
        ['Verbal description', 'say it in words', '"the set of the four seasons of the year"', 'everyday sets']],
       'Partial listing and complete listing are both called the **roster method**. The colon ":" in set-builder notation can also be written as a bar "|".'),
    WK('ex-11a', 'Worked example: the same set three ways', 3,
       'Describe $S$ = the set of odd integers from 1 to 7 by complete listing, and in set-builder notation.',
       ['List the odd integers starting at 1 and stopping at 7: 1, 3, 5, 7.', 'Complete listing: $S = \\{1, 3, 5, 7\\}$.',
        'Set-builder: say what every element has in common: $S = \\{x : x \\text{ is an odd integer and } 1 \\le x \\le 7\\}$.'],
       '$S = \\{1, 3, 5, 7\\} = \\{x : x \\text{ is odd}, 1 \\le x \\le 7\\}$'),
    WK('ex-11b', 'Worked example: from a pattern to set-builder notation', 3,
       'Write $\\{5, 7, 9, 11, \\dots\\}$ and $\\{9, 11, 13, \\dots, 51\\}$ in set-builder notation.',
       ['$\\{5, 7, 9, 11, \\dots\\}$: odd numbers that never stop, starting at 5 → $\\{x : x \\text{ is an odd integer and } x \\ge 5\\}$.',
        '$\\{9, 11, 13, \\dots, 51\\}$: odd numbers from 9 up to 51 → $\\{x : x \\text{ is an odd integer and } 9 \\le x \\le 51\\}$.',
        'Check the ends: the first set has no last element (infinite); the second stops at 51 (finite, 22 elements).'],
       'Two conditions: the **type** of number and the **range**'),
    T('finite-t', 'Finite, infinite and empty sets', 3,
      '- A set is **finite** if counting its elements comes to an end: the letters of the English alphabet (26 elements), $\\{1, 2, 3, \\dots, 1000\\}$.',
      '- A set is **infinite** if counting never ends: the even numbers, $\\{3, 5, 7, 9, \\dots\\}$, the integers.',
      '- The **empty set** has no elements at all. It is written $\\varnothing$ or $\\{\\}$. Examples: real numbers whose square is negative; natural numbers between 3 and 4.',
      '**Careful:** $\\{0\\}$ is **not** empty — it has one element, 0. And $\\{\\varnothing\\}$ is not empty either — it has one element (the empty set).'),
    T('numsets-t', 'Number sets you will meet', 8,
      '$\\mathbb{N}$ = natural numbers $\\{1, 2, 3, \\dots\\}$; $\\mathbb{Z}$ = integers $\\{\\dots, -2, -1, 0, 1, 2, \\dots\\}$; $\\mathbb{Q}$ = rational numbers (fractions $\\frac{p}{q}$ with $q \\ne 0$); $\\mathbb{R}$ = all real numbers (rationals plus irrationals like $\\sqrt{2}$ and $\\pi$).',
      'Each set sits inside the next one: every natural number is an integer, every integer is rational, every rational number is real.'),
    DG('numsets', 'N inside Z inside Q inside R', 8, 'numsets', 'Read the picture from the inside out. $-3$ is in $\\mathbb{Z}$ but not in $\\mathbb{N}$; $\\frac{1}{2}$ is in $\\mathbb{Q}$ but not in $\\mathbb{Z}$; $\\sqrt{2}$ is in $\\mathbb{R}$ only.'),
    MN('mn11', 'Roster lists, builder rules', 2,
       '**Roster = role call**: you call out every name (or the first few and "...").',
       '**Builder = building rule**: you give the rule, and anything that obeys it is in.'),
]

# ------------------------------------------------------------------ lesson 1.2
L2 = [
    T('=math9-u1-c02', '1.2 One-to-one correspondence', 4,
      'Imagine a class with 40 chairs and 40 students, one student in each chair, nobody standing. Without counting, we know the numbers are the same, because each student is **paired** with exactly one chair and each chair with exactly one student.',
      'This pairing is called a **one-to-one correspondence**. Two sets can be paired this way exactly when they have the **same number of elements**.'),
    DG('oneone', 'Pairing the elements', 5, 'oneone',
       'Left: $A = \\{1, 2, 3\\}$ and $B = \\{a, b, c\\}$ pair off perfectly. Right: $C = \\{p, q, r, t\\}$ has one element too many, so $t$ has no partner — no one-to-one correspondence.'),
    TB('eqv-t', 'Equal sets vs equivalent sets', 5, ['', 'Equal sets $A = B$', 'Equivalent sets $A \\sim B$'],
       [['Meaning', 'exactly the **same elements**', 'the **same number** of elements'],
        ['How to test', 'every element of A is in B **and** every element of B is in A', 'count both, or pair them one-to-one: $n(A) = n(B)$'],
        ['Example', '$\\{1, 3, 5, 7\\}$ and $\\{x : x \\text{ odd natural}, x < 8\\}$', '$\\{1, 3, 5, 7\\}$ and $\\{2, 4, 6, 8\\}$'],
        ['Order / repeats', 'do not matter', 'do not matter (count distinct elements)']],
       'Equal sets are **always** equivalent (same elements → same number). Equivalent sets are **not always** equal.'),
    WK('ex-12a', 'Worked example: Exercise 1.2 style', 5,
       'Are the sets equal, equivalent, or neither? (a) $A$ = whole numbers less than 8, $B$ = the distinct digits of the phone number 07251634. (b) $A = \\{1, 2, 3, 4, 5\\}$, $B = \\{0, 1, 2, 3, 4\\}$.',
       ['(a) $A = \\{0, 1, 2, 3, 4, 5, 6, 7\\}$. The digits of 07251634 are 0, 7, 2, 5, 1, 6, 3, 4, so $B = \\{0, 1, 2, 3, 4, 5, 6, 7\\}$.',
        'Same elements → $A = B$ (and so also equivalent).',
        '(b) $5 \\in A$ but $5 \\notin B$, so they are not equal. Both have 5 elements, so they are **equivalent** only.'],
       '(a) equal (b) equivalent but not equal'),
]

# ------------------------------------------------------------------ lesson 1.3
L3 = [
    T('=math9-u1-c03', '1.3 Subsets and proper subsets', 6,
      '$A$ is a **subset** of $B$, written $A \\subseteq B$, if **every** element of $A$ is also an element of $B$.',
      '$A$ is a **proper subset** of $B$, written $A \\subset B$, if $A \\subseteq B$ **and** $B$ has at least one element that is not in $A$ (so $A \\ne B$).',
      'To show $A \\not\\subseteq B$ you need just **one** element of $A$ that is missing from $B$.',
      'Two facts that are always true: **every set is a subset of itself** ($A \\subseteq A$), and **the empty set is a subset of every set** ($\\varnothing \\subseteq A$) — it has no element that could fail the test.'),
    DG('subset', 'Subset and equal sets', 7, 'subset',
       'Left: circle $A$ lies inside $B$ and $B$ has extra elements (like 7), so $A \\subset B$. Right: the two circles are the same circle: $A \\subseteq B$ and $B \\subseteq A$, which means $A = B$.'),
    TB('sub-t', 'Subset symbols compared', 7, ['Symbol', 'Read as', 'True example', 'False example'],
       [['$\\in$', 'is an element of', '$3 \\in \\{1, 3, 5\\}$', '$\\{3\\} \\in \\{1, 3, 5\\}$'],
        ['$\\subseteq$', 'is a subset of', '$\\{3\\} \\subseteq \\{1, 3, 5\\}$, $\\{1, 3, 5\\} \\subseteq \\{1, 3, 5\\}$', '$\\{3, 4\\} \\subseteq \\{1, 3, 5\\}$'],
        ['$\\subset$', 'is a proper subset of', '$\\{1, 5\\} \\subset \\{1, 3, 5\\}$', '$\\{1, 3, 5\\} \\subset \\{1, 3, 5\\}$']],
       '$\\in$ joins an **element** to a set; $\\subseteq$ and $\\subset$ join a **set** to a set. Braces on the left → use a subset symbol.'),
    TB('count-t', 'How many subsets?', 8, ['Set', 'All its subsets', 'Number of subsets', 'Proper subsets'],
       [['$\\varnothing$', '$\\varnothing$', '$1 = 2^0$', '0'],
        ['$\\{1\\}$', '$\\varnothing, \\{1\\}$', '$2 = 2^1$', '1'],
        ['$\\{1, 2\\}$', '$\\varnothing, \\{1\\}, \\{2\\}, \\{1, 2\\}$', '$4 = 2^2$', '3'],
        ['$\\{1, 2, 3\\}$', '$\\varnothing$, three with 1 element, three with 2 elements, $\\{1, 2, 3\\}$', '$8 = 2^3$', '7'],
        ['$n$ elements', 'each element is either in or out: $2 \\times 2 \\times \\dots \\times 2$', '$2^n$', '$2^n - 1$']],
       'Why $2^n$? Building a subset, you decide "in or out" for each element — 2 choices, $n$ times. Proper subsets leave out only the set itself, so subtract 1.'),
    WK('ex-13a', 'Worked example: list the subsets', 8,
       'List all subsets of $\\{a, b, c\\}$ and say how many are proper.',
       ['Size 0: $\\varnothing$.', 'Size 1: $\\{a\\}, \\{b\\}, \\{c\\}$.', 'Size 2: $\\{a, b\\}, \\{a, c\\}, \\{b, c\\}$.', 'Size 3: $\\{a, b, c\\}$.',
        'Total $1 + 3 + 3 + 1 = 8 = 2^3$. All except $\\{a, b, c\\}$ itself are proper: 7.'],
       '8 subsets, 7 proper'),
    WK('ex-13b', 'Worked example: Example 1.8', 7,
       '$A = \\{1, 2, 3, 4\\}$, $B = \\{2, 3, 4\\}$, $C = \\{1, 2\\}$, $D = \\{2, 1, 4, 3\\}$. True or false: (a) $C \\subseteq A$ (b) $A \\subseteq B$ (c) $C \\subseteq B$ (d) $D \\subseteq A$ (e) $A \\subseteq D$.',
       ['(a) 1 and 2 are both in $A$ → **true**.', '(b) $1 \\in A$ but $1 \\notin B$ → **false**.', '(c) $1 \\in C$ but $1 \\notin B$ → **false**.',
        '(d) and (e): $D$ has the same elements as $A$ (order does not matter), so $D = A$; both are **true** (but neither is a proper subset).'],
       'T, F, F, T, T'),
]

# ------------------------------------------------------------------ lesson 1.4
L4 = [
    T('=math9-u1-c06', '1.4.1 Union: everything in A or B', 9,
      'The **union** $A \\cup B$ is the set of all elements that are in $A$, **or** in $B$, or in both.',
      '$$A \\cup B = \\{x : x \\in A \\text{ or } x \\in B\\}$$',
      'How to find it: write all of $A$, then add the elements of $B$ that are not already there. **Never write a common element twice.**',
      'Example 1.9: $A = \\{0, 2, 3\\}$, $B = \\{2, 3, 7\\}$, $C = \\{0, 7, 8\\}$. $A \\cup B = \\{0, 2, 3, 7\\}$ and $A \\cup C = \\{0, 2, 3, 7, 8\\}$.'),
    T('=math9-u1-c07', '1.4.2 Intersection: only what is in both', 10,
      'The **intersection** $A \\cap B$ is the set of elements that are in $A$ **and** in $B$ at the same time.',
      '$$A \\cap B = \\{x : x \\in A \\text{ and } x \\in B\\}$$',
      'Two sets are **disjoint** if they have no element in common, that is $A \\cap B = \\varnothing$.',
      'Example 1.10: $A = \\{0, 2, 3\\}$, $B = \\{2, 3, 7\\}$, $C = \\{7, 8\\}$. $A \\cap B = \\{2, 3\\}$, $B \\cap C = \\{7\\}$, $A \\cap C = \\varnothing$ ($A$ and $C$ are disjoint).'),
    'math9-u1-c05',
    T('=math9-u1-c08', '1.4.3 Venn diagrams', 10,
      'A **Venn diagram** draws each set as a closed curve (usually a circle) inside a rectangle that stands for the **universal set** $U$. Elements are written in the region where they belong.',
      'Two overlapping circles make **four regions**: in $A$ only, in both (the overlap), in $B$ only, and outside both.',
      'Fill a Venn diagram **from the middle outwards**: the overlap first, then "only A", then "only B", then the outside.'),
    DG('unionint', 'Union vs intersection on a Venn diagram', 10, 'unionint',
       'The same two sets. Union shades **both whole circles** → $\\{0, 2, 3, 7\\}$. Intersection shades **only the overlap** → $\\{2, 3\\}$.'),
    DG('disjoint', 'Disjoint sets', 10, 'disjoint', 'Disjoint sets are drawn as circles that do not touch: $A \\cap C = \\varnothing$, and then $n(A \\cup C) = n(A) + n(C) = 3 + 2 = 5$.'),
    TB('uni-t', 'Union and intersection compared', 11, ['', 'Union $A \\cup B$', 'Intersection $A \\cap B$'],
       [['Key word', 'OR (at least one)', 'AND (both)'],
        ['Venn region', 'both circles completely', 'overlap only'],
        ['Size', 'at least as big as each set', 'at most as small as each set'],
        ['If $B \\subseteq A$', '$A \\cup B = A$', '$A \\cap B = B$'],
        ['If disjoint', 'all elements of both', '$\\varnothing$']],
       'Both operations are **commutative**: $A \\cup B = B \\cup A$ and $A \\cap B = B \\cap A$.'),
    RM('=math9-u1-c04', 'Counting rule for a union', 11,
       '$n(A)$ is the **cardinality** (number of elements) of a finite set $A$: $n(\\{1, 2, 3\\}) = 3$, $n(\\text{vowels}) = 5$.',
       '$$n(A \\cup B) = n(A) + n(B) - n(A \\cap B)$$',
       'Why subtract? The elements in the overlap are counted once in $n(A)$ and again in $n(B)$ — subtract them once so they are counted only once.'),
    ST('survey', 'Activity 1.11: filling a survey Venn diagram', 11, 'survey',
       [('150 learners: 63 own a bicycle, 84 a calculator, 27 both. Start in the middle: write **27** in the overlap.', 'k1'),
        ('Bicycle only $= 63 - 27 = 36$.', 'k2'),
        ('Calculator only $= 84 - 27 = 57$.', 'k3'),
        ('Inside the circles: $36 + 27 + 57 = 120$. Neither $= 150 - 120 = 30$, written outside the circles.', 'k4'),
        ('Answers: none 30; calculator only 57; bicycle only 36; bicycle or calculator $= 120$ — check with the formula: $63 + 84 - 27 = 120$ (correct).', 'k5')]),
    WK('ex-14a', 'Worked example: Review question 6', 18,
       'In a group of 200 learners each speaks Tigre or Tigrigna. 50 speak both and 110 speak Tigre. How many speak Tigrigna only?',
       ['"Each speaks Tigre or Tigrigna" means nobody is outside: $n(T \\cup G) = 200$.', 'Tigre only $= 110 - 50 = 60$.', 'Tigrigna only $= 200 - 60 - 50 = 90$.',
        'Check: Tigrigna altogether $= 90 + 50 = 140$, and $110 + 140 - 50 = 200$ (correct).'],
       '90 learners'),
    WK('ex-14b', 'Worked example: mixing union and intersection', 12,
       '$A = \\{2, 3, 5, 7\\}$, $B = \\{2, 5, 7\\}$, $C = \\{3, 5, 7, 11\\}$. Find $A \\cap (B \\cup C)$.',
       ['Brackets first: $B \\cup C = \\{2, 3, 5, 7, 11\\}$.', 'Now keep the elements of $A$ that are also in that set: 2, 3, 5, 7 are all there.'],
       '$A \\cap (B \\cup C) = \\{2, 3, 5, 7\\}$'),
]

# ------------------------------------------------------------------ lesson 1.5
L5 = [
    T('=math9-u1-c09', '1.5.1 Universal set and complement', 12,
      'The **universal set** $U$ contains all the elements being talked about in a problem. It changes from problem to problem.',
      'The **complement** of $A$, written $A\'$, is everything in $U$ that is **not** in $A$:',
      '$$A\' = \\{x : x \\in U \\text{ and } x \\notin A\\}$$',
      'Facts: $A \\cup A\' = U$, $A \\cap A\' = \\varnothing$, $(A\')\' = A$, $U\' = \\varnothing$ and $\\varnothing\' = U$. Also $n(A\') = n(U) - n(A)$.'),
    DG('fig15', 'Reading elements from a Venn diagram (Fig. 1.5)', 12, 'fig15',
       '$A = \\{1, 3, 5, 7\\}$, $B = \\{1, 2, 4, 5\\}$, $U = \\{0, 1, \\dots, 7\\}$. Not in $A$: $A\' = \\{0, 2, 4, 6\\}$. Not in $B$: $B\' = \\{0, 3, 6, 7\\}$. The numbers 6 and 0 belong to $U$ but to neither set.'),
    T('=math9-u1-c10', '1.5.2 Difference of sets', 13,
      '$A - B$ ("A minus B") is the set of elements that are in $A$ **but not** in $B$:',
      '$$A - B = \\{x : x \\in A \\text{ and } x \\notin B\\}$$',
      'In the same way $B - A$ is the elements of $B$ that are not in $A$. The textbook calls $B - A$ "the difference of $A$ with respect to $B$".',
      'Example (Activity 1.13): $A = \\{2, -2, 5\\}$, $B = \\{2, -2, 0, -3\\}$. $A - B = \\{5\\}$ and $B - A = \\{0, -3\\}$. Usually $A - B \\ne B - A$.',
      'Link with the complement: $A - B = A \\cap B\'$ and $A\' = U - A$.'),
    DG('ops4', 'Four regions to know', 13, 'ops4',
       'Shaded: the complement $A\'$; the difference $A - B$ (the moon-shaped part of $A$ outside $B$); $B - A$; and $(A \\cup B)\'$, the part outside both circles.'),
    TB('ops-t', 'All the set operations in one table', 14, ['Operation', 'Symbol', 'Contains', 'Venn region'],
       [['Union', '$A \\cup B$', 'in A or B (or both)', 'both circles'],
        ['Intersection', '$A \\cap B$', 'in A and B', 'overlap'],
        ['Complement', "$A'$", 'in U, not in A', 'outside circle A'],
        ['Difference', '$A - B$', 'in A, not in B', 'A without the overlap'],
        ['Difference', '$B - A$', 'in B, not in A', 'B without the overlap']],
       'Complement needs $U$; difference does not. $A - B$ and $B - A$ are different regions.'),
    ST('demorgan', "De Morgan's laws", 14, 'demorgan',
       [('Shade $A\'$: everything outside circle $A$ (this includes the "B only" region).', 'k1'),
        ('Shade $B\'$ on a second copy: everything outside circle $B$.', 'k2'),
        ('$A\' \\cap B\'$ is where **both** shadings meet: only the part outside both circles — exactly $(A \\cup B)\'$. So $(A \\cup B)\' = A\' \\cap B\'$. In the same way $(A \\cap B)\' = A\' \\cup B\'$.', 'k3')]),
    RM('dm-rm', "De Morgan's laws", 14,
       '$$(A \\cup B)\' = A\' \\cap B\' \\qquad (A \\cap B)\' = A\' \\cup B\'$$',
       'Rule of thumb: when the dash moves inside the bracket, **flip the sign** ($\\cup \\leftrightarrow \\cap$).'),
    WK('ex-15a', 'Worked example: Exercise 1.5 question 2', 14,
       '$U = \\{4, 5, 6, 7, 8, a, e, i, o, u\\}$, $A = \\{5, 6, 7, a\\}$, $B = \\{4, 7, e, a\\}$. Find $(A \\cup B)\'$ and $A\' \\cap B\'$.',
       ['$A \\cup B = \\{4, 5, 6, 7, a, e\\}$, so $(A \\cup B)\' = \\{8, i, o, u\\}$.',
        '$A\' = \\{4, 8, e, i, o, u\\}$ and $B\' = \\{5, 6, 8, i, o, u\\}$.',
        'Common to both: $A\' \\cap B\' = \\{8, i, o, u\\}$ — the same set, as De Morgan says.'],
       '$(A \\cup B)\' = A\' \\cap B\' = \\{8, i, o, u\\}$'),
    WK('ex-15b', 'Worked example: differences', 14,
       '$A = \\{1, 2, \\dots, 8\\}$, $B = \\{2, 3, \\dots, 12\\}$. Find $B - A$ and $A - B$. Are they equal?',
       ['$B - A$: cross out of $B$ everything that is in $A$ (2 to 8): $\\{9, 10, 11, 12\\}$.', '$A - B$: cross out of $A$ everything in $B$: only 1 is left, $\\{1\\}$.', 'They are different.'],
       '$B - A = \\{9, 10, 11, 12\\}$, $A - B = \\{1\\}$; not equal'),
]

# ------------------------------------------------------------------ lesson 1.6
L6 = [
    T('=math9-u1-c11', '1.6 Ordered pairs', 15,
      'In a classroom seating plan we can give each desk two numbers: its **column** and its **row**. The desk in column 4, row 3 is written $(4, 3)$ — column first, then row.',
      'A pair written in a fixed order, $(x, y)$, is an **ordered pair**. $x$ is the first component and $y$ the second.',
      '**Order matters:** $(4, 3)$ and $(3, 4)$ are different desks. Two ordered pairs are equal only when $(a, b) = (c, d)$ means $a = c$ **and** $b = d$.',
      'Compare: the sets $\\{3, 4\\}$ and $\\{4, 3\\}$ are equal, but the ordered pairs $(3, 4)$ and $(4, 3)$ are not.'),
    DG('seating', 'Seating plan', 16, 'seating', 'Saba sits in column 3, row 1: S$(3, 1)$. The shaded desk is $(4, 3)$, which is not the same desk as $(3, 4)$.'),
    T('cart-t', 'The Cartesian product A × B', 16,
      'The **Cartesian product** of $A$ and $B$ is the set of **all** ordered pairs whose first component comes from $A$ and second from $B$:',
      '$$A \\times B = \\{(a, b) : a \\in A \\text{ and } b \\in B\\}$$',
      'Method: take each element of $A$ in turn and pair it with **every** element of $B$.',
      'Number of pairs: $n(A \\times B) = n(A) \\times n(B)$. If either set is empty, $A \\times B = \\varnothing$.'),
    WK('ex-16a', 'Worked example: Example 1.12', 17,
       'If $A = \\{2, 4, 5\\}$ and $B = \\{1, 3, 6\\}$, find $A \\times B$.',
       ['Pair 2 with every element of B: $(2, 1), (2, 3), (2, 6)$.', 'Pair 4: $(4, 1), (4, 3), (4, 6)$.', 'Pair 5: $(5, 1), (5, 3), (5, 6)$.', 'Count: $3 \\times 3 = 9$ pairs (correct).'],
       '$A \\times B = \\{(2,1), (2,3), (2,6), (4,1), (4,3), (4,6), (5,1), (5,3), (5,6)\\}$', diagram='axb'),
    TB('cart-tb', 'A × B is not B × A', 17, ['', '$A \\times B$', '$B \\times A$'],
       [['With $C = \\{1, 2\\}$, $D = \\{0, 1\\}$', '$C \\times D = \\{(1,0), (1,1), (2,0), (2,1)\\}$', '$D \\times C = \\{(0,1), (0,2), (1,1), (1,2)\\}$'],
        ['First components from', 'A', 'B'],
        ['Number of pairs', '$n(A) \\cdot n(B)$', '$n(B) \\cdot n(A)$ — the same number'],
        ['Equal sets?', 'only if $A = B$ (or one set is empty)', '']],
       'Same **number** of pairs, but usually **different** pairs: $(2, 0) \\in C \\times D$ but $(2, 0) \\notin D \\times C$.'),
]

LESSONS = {'math9-u1-l1-1': L1, 'math9-u1-l1-2': L2, 'math9-u1-l1-3': L3, 'math9-u1-l1-4': L4, 'math9-u1-l1-5': L5, 'math9-u1-l1-6': L6}

# ------------------------------------------------------------------ practice
a = QSet('1.1 Practice — describing sets', 's11')
a.S(4, 'Describe $C$, the set of positive multiples of 4, by the roster method and in set-builder notation.', '$\\{4, 8, 12, \\dots\\}$; $\\{x : x = 4k, k \\in \\mathbb{N}\\}$',
    ['Step 1: the first positive multiples are 4, 8, 12, 16, ...', 'Step 2: infinite with a clear pattern → partial listing $\\{4, 8, 12, 16, \\dots\\}$.', 'Step 3: rule: $\\{x : x \\text{ is a positive multiple of } 4\\}$, or $\\{x : x = 4k, k \\in \\mathbb{N}\\}$.'],
    'Infinite set → three dots at the end; never try to list it all.', [('Describe the set of even integers by partial listing.', '$\\{\\dots, -4, -2, 0, 2, 4, \\dots\\}$.')])
a.S(4, 'List the set $G$ of letters in the word "mathematics". How many elements does it have?', '$\\{m, a, t, h, e, i, c, s\\}$; 8',
    ['Step 1: go through the word: m, a, t, h, e, m, a, t, i, c, s.', 'Step 2: write repeated letters once: m, a, t, h, e, i, c, s.', 'Step 3: count: 8.'],
    'A set never contains the same element twice.', [('How many elements has the set of letters of "Eritrea"?', '5: $\\{e, r, i, t, a\\}$.')])
a.M(4, 'Which set is infinite?', ['$\\{1, 2, 3, \\dots, 1000\\}$', 'letters of the English alphabet', '$\\{3, 5, 7, 9, \\dots\\}$', 'positive multiples of 3 less than 30'], 'C',
    ['Step 1: A stops at 1000 and B at 26 letters — finite.', 'Step 2: D is $\\{3, 6, \\dots, 27\\}$, 9 elements — finite.', 'Step 3: C has three dots at the end with no last number — infinite.'],
    'Dots in the middle (… 1000) still mean finite; dots at the end mean infinite.', [('Is $\\{x : x \\text{ is a student in Eritrea}\\}$ finite?', 'Yes — very large, but the counting ends.')])
a.TF(4, '$0 \\in \\{x : x \\text{ is a multiple of } 5\\}$', True,
     ['Step 1: a multiple of 5 is $5k$ for an integer $k$.', 'Step 2: $0 = 5 \\times 0$, so 0 is a multiple of 5 → true.'],
     'Zero is a multiple of every integer.', [('True or false: $10 \\notin \\{1, 2, 3, \\dots, 16\\}$.', 'False — 10 is in the list.')])
a.S(18, 'List the elements of $\\{x : x \\text{ is an odd natural number between } 12 \\text{ and } 20\\}$.', '$\\{13, 15, 17, 19\\}$',
    ['Step 1: "between 12 and 20" does not include 12 and 20.', 'Step 2: odd numbers there: 13, 15, 17, 19.'],
    '"Between" usually excludes the end numbers; "from ... to" includes them.', [('List $\\{x : x \\text{ is an integer}, -3 \\le x < 2\\}$.', '$\\{-3, -2, -1, 0, 1\\}$.')])
a.S(18, 'Use set-builder notation: $x$ is a real number greater than $-1$ and less than or equal to 10.', '$\\{x : x \\in \\mathbb{R}, -1 < x \\le 10\\}$',
    ['Step 1: "greater than $-1$" → $-1 < x$ (strict).', 'Step 2: "less than or equal to 10" → $x \\le 10$.', 'Step 3: join them: $\\{x : x \\in \\mathbb{R}, -1 < x \\le 10\\}$.'],
    '"or equal to" → use $\\le$ or $\\ge$; otherwise use $<$ or $>$.', [('Write: $x$ is real and $x < 0$ or $x > 5$.', '$\\{x : x \\in \\mathbb{R}, x < 0 \\text{ or } x > 5\\}$.')])
a.M(1, 'Which of these is a well-defined set?', ['the beautiful cities of Eritrea', 'the good footballers in Asmara', 'the Zobas (regions) of Eritrea', 'the difficult subjects in Grade 9'], 'C',
    ['Step 1: "beautiful", "good" and "difficult" are opinions — people disagree.', 'Step 2: the Zobas form a fixed official list → well-defined.'],
    'Look for opinion words; they make a collection not well-defined.', [('Is "the prime numbers less than 20" a set?', 'Yes — exactly 2, 3, 5, 7, 11, 13, 17, 19.')])
a.TF(3, '$\\{0\\}$ is the empty set.', False,
     ['Step 1: the empty set has no elements.', 'Step 2: $\\{0\\}$ has one element, the number 0 → not empty.'],
     'Look inside the braces: anything there means not empty.', [('Is the set of natural numbers between 5 and 6 empty?', 'Yes — no natural number lies strictly between 5 and 6.')])

b = QSet('1.2 Practice — equal and equivalent sets', 's12')
b.M(5, '$A = \\{1, 2, 3, 4\\}$ and $B = \\{1, 2, 3, 4, 5\\}$. The sets are', ['equal', 'equivalent but not equal', 'both equal and equivalent', 'neither equal nor equivalent'], 'D',
    ['Step 1: $5 \\in B$, $5 \\notin A$ → not equal.', 'Step 2: $n(A) = 4$, $n(B) = 5$ → not equivalent.'],
    'Count first: different counts rule out both.', [('$A = \\{1, 2, 3, 4\\}$, $B = \\{4, 3, 2, 1\\}$?', 'Equal (and so also equivalent).')])
b.S(5, 'A = the set of Zobas in Eritrea, B = the set of Zoba administrators. Equal or equivalent?', 'Equivalent, not equal',
    ['Step 1: Eritrea has 6 Zobas and each has one administrator, so the sets pair one-to-one.', 'Step 2: but a Zoba is a region and an administrator is a person — the elements are different.'],
    'Pairing works → equivalent; same objects → equal.', [('Students of a class and their desks (one each)?', 'Equivalent, not equal.')])
b.TF(5, 'Every pair of equivalent sets is also equal.', False,
     ['Step 1: $\\{1, 2\\}$ and $\\{a, b\\}$ both have 2 elements → equivalent.', 'Step 2: they share no element → not equal.'],
     'One counter-example is enough to show "always" is false.', [('True or false: equal sets are always equivalent.', 'True.')])
b.S(4, 'Are $C = \\{w, x, y, z\\}$ and $D = \\{u, x, y, z\\}$ equal, equivalent, or both?', 'Equivalent only',
    ['Step 1: $w \\in C$, $w \\notin D$ → not equal.', 'Step 2: both have 4 elements → equivalent.'],
    'One different element is enough to break equality.', [('$\\{a, b, c\\}$ and $\\{b, a, c\\}$?', 'Equal (same elements, order does not matter).')])
b.F(5, 'Two sets are equivalent exactly when they can be put in a ____ correspondence.', 'one-to-one', ['one-to-one', 'many-to-one', 'two-to-one', 'reverse'],
    ['Step 1: equivalent means the same number of elements.', 'Step 2: that is exactly when each element pairs with exactly one partner: one-to-one.'],
    'Think: students and chairs, one each.', [('If $n(A) = 7$ and $A \\sim B$, what is $n(B)$?', '7.')])
b.S(5, '$A = \\{x : x \\text{ is a letter of "LEVEL"}\\}$, $B = \\{E, V, L\\}$. Compare A and B.', 'Equal (so also equivalent)',
    ['Step 1: letters of LEVEL without repeats: L, E, V.', 'Step 2: $A = \\{L, E, V\\} = B$.'],
    'Remove repeats before comparing.', [('Letters of "NOON" and $\\{O, N\\}$?', 'Equal.')])

c = QSet('1.3 Practice — subsets', 's13')
c.S(8, 'How many subsets and how many proper subsets does a set with 10 elements have?', '1024 subsets; 1023 proper',
    ['Step 1: subsets $= 2^{10} = 1024$.', 'Step 2: proper subsets $= 1024 - 1 = 1023$ (leave out the set itself).'],
    'Proper subsets = all subsets minus one.', [('A set has 6 elements. How many subsets?', '$2^6 = 64$.')])
c.M(8, 'A set has 32 subsets. How many elements does it have?', ['4', '5', '6', '16'], 'B',
    ['Step 1: $2^n = 32$.', 'Step 2: $2^5 = 32$, so $n = 5$.'],
    'Count the doublings: 2, 4, 8, 16, 32 → 5.', [('A set has 15 proper subsets. How many elements?', '4 (16 subsets).')])
c.TF(8, '$\\{x : x \\text{ is a prime number}\\} \\subseteq \\{x : x \\text{ is an odd integer}\\}$', False,
     ['Step 1: look for a prime that is not odd.', 'Step 2: 2 is prime and even → it is in the first set but not in the second.'],
     'One counter-example disproves a subset statement.', [('Primes $\\subseteq$ rational numbers?', 'True — every integer is rational.')])
c.S(8, 'True or false: (a) $\\mathbb{N} \\subseteq \\mathbb{Z}$ (b) $\\mathbb{Q} \\subseteq \\mathbb{Z}$ (c) $\\mathbb{Z} \\subseteq \\mathbb{Q}$ (d) $\\mathbb{Q} \\subseteq \\mathbb{R}$', 'T, F, T, T',
    ['Step 1 (a): every natural number is an integer → true.', 'Step 2 (b): $\\frac{1}{2}$ is rational but not an integer → false.', 'Step 3 (c): $n = \\frac{n}{1}$ → true.', 'Step 4 (d): every rational is real → true.'],
    'Use the nested picture N inside Z inside Q inside R.', [('Is $\\mathbb{R} \\subseteq \\mathbb{Q}$?', 'No — $\\sqrt{2}$ is real but not rational.')])
c.M(17, 'Which statement is true?', ['$3 \\subseteq \\{1, 2, 3\\}$', '$\\{3\\} \\in \\{1, 2, 3\\}$', '$\\{3\\} \\subseteq \\{1, 2, 3\\}$', '$\\varnothing \\in \\{1, 2, 3\\}$'], 'C',
    ['Step 1: 3 is an element, so it goes with $\\in$, not $\\subseteq$ → A false.', 'Step 2: $\\{3\\}$ is a set, so it goes with $\\subseteq$ → B false, C true.', 'Step 3: $\\varnothing$ is a subset of every set, but it is not listed as an element → D false.'],
    'Element → $\\in$. Set (braces) → $\\subseteq$.', [('True or false: $\\varnothing \\subseteq \\varnothing$.', 'True — every set is a subset of itself.')])
c.S(8, 'List all subsets of $\\{1, 2, 3, 4\\}$ that have exactly 2 elements.', '6 subsets',
    ['Step 1: pair 1 with each later number: $\\{1,2\\}, \\{1,3\\}, \\{1,4\\}$.', 'Step 2: pair 2 with later numbers: $\\{2,3\\}, \\{2,4\\}$.', 'Step 3: then $\\{3,4\\}$. Total 6.'],
    'Work in order so you never repeat or miss one.', [('How many 3-element subsets has $\\{1, 2, 3, 4\\}$?', '4.')])
c.TF(8, 'If $A \\subseteq B$ and $B \\subseteq A$, then $A = B$.', True,
     ['Step 1: every element of A is in B.', 'Step 2: every element of B is in A.', 'Step 3: so they have exactly the same elements → equal.'],
     'This is how we prove two sets are equal.', [('If $A \\subset B$, can $B \\subseteq A$?', 'No — B has an element not in A.')])

d = QSet('1.4 Practice — union, intersection, Venn diagrams', 's14')
d.S(12, '$A = \\{0, 1, 2\\}$, $B = \\{3, 4, 5, 6\\}$, $D = \\{2, 4, 6\\}$, $E = \\{1, 3\\}$. Find $A \\cup B$, $A \\cap D$, $B \\cap E$ and $D \\cap E$.', '$\\{0,\\dots,6\\}$; $\\{2\\}$; $\\{3\\}$; $\\varnothing$',
    ['Step 1: $A \\cup B = \\{0, 1, 2, 3, 4, 5, 6\\}$.', 'Step 2: common to A and D: 2 → $\\{2\\}$.', 'Step 3: common to B and E: 3 → $\\{3\\}$.', 'Step 4: D is even, E is odd → nothing common, $\\varnothing$ (disjoint).'],
    'For ∩ go through the smaller set and tick what is in the other.', [('Find $A \\cap B$.', '$\\varnothing$ — A and B are disjoint.')])
d.S(11, '$n(A) = 12$, $n(B) = 9$ and $n(A \\cap B) = 4$. Find $n(A \\cup B)$.', '17',
    ['Step 1: $n(A \\cup B) = n(A) + n(B) - n(A \\cap B)$.', 'Step 2: $12 + 9 - 4 = 17$.'],
    'Add, then subtract the overlap once.', [('$n(A \\cup B) = 30$, $n(A) = 18$, $n(B) = 20$. Find $n(A \\cap B)$.', '8.')])
d.S(11, 'In a class of 40, 25 play football, 18 play volleyball and 7 play neither. How many play both?', '10',
    ['Step 1: players of at least one game $= 40 - 7 = 33$.', 'Step 2: $33 = 25 + 18 - x$.', 'Step 3: $x = 43 - 33 = 10$.', 'Step 4: check the Venn: football only 15, both 10, volleyball only 8, neither 7; $15 + 10 + 8 + 7 = 40$ (correct).'],
    'Remove "neither" first to get $n(A \\cup B)$.', [('50 learners: 30 like maths, 26 like physics, 4 like neither. Both?', '10.')])
d.M(12, 'If $B \\subseteq A$, then $A \\cup B$ equals', ['$A$', '$B$', '$\\varnothing$', '$A \\cap B$'], 'A',
    ['Step 1: B is inside A, so adding B to A adds nothing new.', 'Step 2: $A \\cup B = A$ (and $A \\cap B = B$).'],
    'Draw B as a small circle inside A.', [('If $B \\subseteq A$, what is $A \\cap B$?', '$B$.')])
d.S(18, '$A = \\{2, 0, 5\\}$, $B = \\{4, 5, 6\\}$, $C = \\{2, 4, 6\\}$. Find $A \\cup B$, $A \\cap C$ and $B \\cap C$.', '$\\{0, 2, 4, 5, 6\\}$; $\\{2\\}$; $\\{4, 6\\}$',
    ['Step 1: join A and B, 5 only once: $\\{0, 2, 4, 5, 6\\}$.', 'Step 2: A and C share 2.', 'Step 3: B and C share 4 and 6.'],
    'Write answers in increasing order to check nothing is missing.', [('Find $C \\cup A$.', '$\\{0, 2, 4, 5, 6\\}$.')])
d.TF(10, 'If $A \\cap B = \\varnothing$ then $n(A \\cup B) = n(A) + n(B)$.', True,
     ['Step 1: $n(A \\cup B) = n(A) + n(B) - n(A \\cap B)$.', 'Step 2: $n(\\varnothing) = 0$, so nothing is subtracted.'],
     'Disjoint sets: just add.', [('Disjoint, $n(A) = 4$, $n(A \\cup B) = 9$. Find $n(B)$.', '5.')])
d.S(11, '$A$ = counting numbers less than 9, $B$ = primes less than 15. List $A \\cap B$.', '$\\{2, 3, 5, 7\\}$',
    ['Step 1: $A = \\{1, \\dots, 8\\}$; $B = \\{2, 3, 5, 7, 11, 13\\}$.', 'Step 2: common: 2, 3, 5, 7.'],
    'Remember 1 is not prime.', [('Find $A \\cup B$.', '$\\{1, 2, \\dots, 8, 11, 13\\}$.')])

e = QSet('1.5 Practice — complement and difference', 's15')
e.S(14, '$U = \\{1, \\dots, 7\\}$, $A = \\{1, 3, 5, 7\\}$, $B = \\{2, 4, 6\\}$, $C = \\{3, 6\\}$. Find $A\'$, $B\'$ and $C\'$.', "$A' = \\{2,4,6\\}$, $B' = \\{1,3,5,7\\}$, $C' = \\{1,2,4,5,7\\}$",
    ['Step 1: cross the elements of A out of U: 2, 4, 6 remain.', 'Step 2: for B: 1, 3, 5, 7 remain.', 'Step 3: for C: 1, 2, 4, 5, 7 remain.'],
    'Complement = U with the set crossed out.', [("Here, notice $A' = B$. What is $B'$?", '$A$.')])
e.S(14, 'Same sets. Find $A - B$, $A - C$, $B - C$, $B - A$ and $C - A$.', '$A$; $\\{1,5,7\\}$; $\\{2,4\\}$; $B$; $\\{6\\}$',
    ['Step 1: A and B are disjoint, so $A - B = A$ and $B - A = B$.', 'Step 2: $A - C$: remove 3 → $\\{1, 5, 7\\}$.', 'Step 3: $B - C$: remove 6 → $\\{2, 4\\}$.', 'Step 4: $C - A$: remove 3 → $\\{6\\}$.'],
    '$X - Y$: start with X, cross out anything in Y.', [('Can $A - B = B - A$?', 'Only when $A = B$ (both are then $\\varnothing$).')])
e.M(13, 'In a Venn diagram, $A - B$ is', ['the overlap', 'the part of A outside B', 'everything outside A', 'the part of B outside A'], 'B',
    ['Step 1: $A - B$ keeps elements of A.', 'Step 2: it removes those also in B, i.e. the overlap.'],
    'Minus B = cut the B circle away.', [('Which region is $(A \\cap B)\'$?', 'Everything except the overlap.')])
e.TF(14, '$(A \\cup B)\' = A\' \\cup B\'$ for all sets $A, B$.', False,
     ["Step 1: De Morgan: $(A \\cup B)' = A' \\cap B'$, not $A' \\cup B'$.", 'Step 2: example $U = \\{1, 2\\}$, $A = \\{1\\}$, $B = \\{2\\}$: $(A \\cup B)\' = \\varnothing$ but $A\' \\cup B\' = \\{1, 2\\}$.'],
     'When the dash goes inside, flip ∪ and ∩.', [("Complete: $(A \\cap B)' = $", "$A' \\cup B'$.")])
e.S(18, '$U = \\{0, 1, \\dots, 9\\}$, $A = \\{1, 3, 5, 7\\}$, $C = \\{0, 2, 4, 6, 8\\}$. Find $A\'$ and $A - C$.', "$A' = \\{0, 2, 4, 6, 8, 9\\}$; $A - C = A$",
    ['Step 1: remove 1, 3, 5, 7 from U: 0, 2, 4, 6, 8, 9.', 'Step 2: A (odd) and C (even) share nothing, so $A - C = A = \\{1, 3, 5, 7\\}$.'],
    'Do not forget 9 — it is in U but in neither listed set.', [('Find $C\'$.', '$\\{1, 3, 5, 7, 9\\}$.')])
e.S(12, '$n(U) = 50$ and $n(A) = 18$. Find $n(A\')$.', '32',
    ['Step 1: $n(A\') = n(U) - n(A)$.', 'Step 2: $50 - 18 = 32$.'],
    'A and its complement fill U exactly once.', [('$n(U) = 40$, $n(A\') = 15$. Find $n(A)$.', '25.')])
e.F(13, '$A - B = A \\cap$ ____', "$B'$", ["$B'$", '$B$', "$A'$", '$U$'],
    ['Step 1: $A - B$ = in A and not in B.', "Step 2: \"not in B\" is $B'$, so $A - B = A \\cap B'$."],
    'Translate "not in B" into $B\'$.', [('$B - A = B \\cap$ ?', "$A'$.")])

g = QSet('1.6 Practice — Cartesian product', 's16')
g.S(17, '$C = \\{1, 2\\}$, $D = \\{0, 1\\}$. Find $C \\times D$ and $D \\times C$. Are they equal?', 'Not equal',
    ['Step 1: $C \\times D = \\{(1,0), (1,1), (2,0), (2,1)\\}$.', 'Step 2: $D \\times C = \\{(0,1), (0,2), (1,1), (1,2)\\}$.', 'Step 3: $(1, 0)$ is in the first but not the second → not equal.'],
    'First component always comes from the first set written.', [('Find $C \\times C$.', '$\\{(1,1), (1,2), (2,1), (2,2)\\}$.')])
g.M(17, 'If $n(A) = 3$ and $n(B) = 2$, then $n(A \\times B)$ is', ['5', '6', '8', '9'], 'B',
    ['Step 1: $n(A \\times B) = n(A) \\times n(B)$.', 'Step 2: $3 \\times 2 = 6$.'],
    'Multiply, do not add.', [('$n(A) = n$, $n(B) = m$. Find $n(A \\times B)$.', '$nm$.')])
g.S(17, '$n(A \\times B) = 15$ and $n(A) = 3$. Find $n(B)$.', '5',
    ['Step 1: $3 \\times n(B) = 15$.', 'Step 2: $n(B) = 5$.'],
    'Divide the product by the known count.', [('$n(A \\times A) = 49$. Find $n(A)$.', '7.')])
g.S(15, 'Find $x$ and $y$ if $(x + 2, 5) = (7, y - 1)$.', '$x = 5$, $y = 6$',
    ['Step 1: equal ordered pairs → first components equal: $x + 2 = 7$, so $x = 5$.', 'Step 2: second components equal: $5 = y - 1$, so $y = 6$.'],
    'Match first with first and second with second.', [('$(2x, 3) = (8, y)$?', '$x = 4$, $y = 3$.')])
g.TF(16, '$(3, 4) = (4, 3)$', False,
     ['Step 1: ordered pairs are equal only if the first components match and the second components match.', 'Step 2: $3 \\ne 4$ → not equal.'],
     'Sets ignore order; ordered pairs do not.', [('Is $\\{3, 4\\} = \\{4, 3\\}$?', 'Yes — these are sets.')])
g.S(17, '$A = \\{a\\}$, $B = \\{1, 2, 3\\}$. Write $A \\times B$ and $B \\times A$.', '$\\{(a,1),(a,2),(a,3)\\}$; $\\{(1,a),(2,a),(3,a)\\}$',
    ['Step 1: pair $a$ with each of 1, 2, 3.', 'Step 2: for $B \\times A$, put the number first.'],
    'Count check: $1 \\times 3 = 3$ pairs each.', [('$A = \\{1\\}$, $B = \\varnothing$. Find $A \\times B$.', '$\\varnothing$.')])

QS = a.items + b.items + c.items + d.items + e.items + g.items

GLOSSARY = [
    ('Set', 'A well-defined collection of objects.', 1),
    ('Element', 'An object that belongs to a set; written $a \\in A$.', 1),
    ('Roster method', 'Describing a set by listing its elements (completely or partially).', 2),
    ('Set-builder notation', 'Describing a set by a rule: $\\{x : \\text{condition}\\}$.', 3),
    ('Empty set', 'The set with no elements, $\\varnothing$.', 3),
    ('Equivalent sets', 'Sets with the same number of elements (a one-to-one correspondence exists).', 5),
    ('Equal sets', 'Sets with exactly the same elements.', 5),
    ('Proper subset', '$A \\subset B$: every element of A is in B and B has an extra element.', 7),
    ('Disjoint sets', 'Sets with no common element.', 10),
    ('Cardinality', 'The number of elements of a finite set, $n(A)$.', 11),
    ('Universal set', 'The set of all elements under discussion, $U$.', 12),
    ('Complement', "$A'$: the elements of U that are not in A.", 12),
    ('Ordered pair', '$(x, y)$: two components in a fixed order.', 16),
    ('Cartesian product', '$A \\times B$: all ordered pairs $(a, b)$ with $a \\in A$, $b \\in B$.', 16),
]
TIPS = [
    ('Union = OR (both circles); intersection = AND (overlap); difference A − B = A with the overlap cut away.', 13),
    ('Venn problems: fill the overlap first, then the "only" parts, then the outside.', 11),
    ('A set with n elements has 2ⁿ subsets and 2ⁿ − 1 proper subsets.', 8),
    ("De Morgan: (A ∪ B)′ = A′ ∩ B′ and (A ∩ B)′ = A′ ∪ B′.", 14),
]
IDEAS = [('methods', 'Three ways to describe a set', 'l1_1', 'math9-u1-md-methods-t'),
         ('equiv', 'Equal vs equivalent', 'l1_2', 'math9-u1-md-eqv-t'),
         ('count', 'Counting subsets 2ⁿ', 'l1_3', 'math9-u1-md-count-t'),
         ('venn', 'Survey Venn diagram', 'l1_4', 'math9-u1-md-survey'),
         ('ops', 'Set operations table', 'l1_5', 'math9-u1-md-ops-t'),
         ('cart', 'Cartesian product', 'l1_6', 'math9-u1-md-cart-t')]
