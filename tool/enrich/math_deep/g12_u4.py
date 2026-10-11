r"""Grade 12 Unit 4 — Matrices and Determinant (pp. 158-170)."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, QSet
from svglib import Fig, Plot, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY

UID = 'math12-u4'
set_unit(UID)
LB, LG, LR, LO = '#dbe7f3', '#d6ece6', '#f6dcd5', '#FCEFD9'


def mat(f, x, y, rows, cw=34, rh=26, col=INK, size=14, bars=False):
    """draw a matrix with its top-left inner corner at (x, y); returns (width, height)"""
    m, n = len(rows), len(rows[0])
    w, h = n * cw, m * rh
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            f.text(x + cw * j + cw / 2, y + rh * i + rh / 2 + 5, str(v), size, col)
    if bars:
        f.line(x - 2, y, x - 2, y + h, INK, 1.8).line(x + w + 2, y, x + w + 2, y + h, INK, 1.8)
    else:
        f.path(f'M{x + 4} {y - 2} Q{x - 6} {y + h / 2} {x + 4} {y + h + 2}', INK, 1.8)
        f.path(f'M{x + w - 4} {y - 2} Q{x + w + 6} {y + h / 2} {x + w - 4} {y + h + 2}', INK, 1.8)
    return w, h


# ------------------------------------------------------------------ figures
def f_order():
    f = Fig(330, 180)
    x0, y0, cw, rh = 110, 40, 50, 34
    rows = [['a11', 'a12'], ['a21', 'a22'], ['a31', 'a32']]
    f.rect(x0 + 2, y0 + rh + 3, 2 * cw - 4, rh - 6, BLUE, 1.4, LB)
    f.rect(x0 + cw + 5, y0 + 2, cw - 10, 3 * rh - 4, RED, 1.4, LR)
    mat(f, x0, y0, rows, cw, rh, INK, 13)
    f.text(x0 - 16, y0 + rh * 1.5 + 5, 'row 2', 12, BLUE, 'end')
    f.text(x0 + cw * 1.5, y0 - 12, 'column 2', 12, RED)
    f.text(x0 + cw, y0 + 3 * rh + 26, '3 rows, 2 columns: order 3 x 2', 12.5, INK)
    f.text(10, 18, 'a21: row 2, column 1', 11.5, PURPLE, 'start')
    return f


def f_mult():
    f = Fig(340, 170)
    A = [['1', '-3', '6'], ['2', '5', '4']]
    B = [['-1', '3'], ['2', '5'], ['6', '-9']]
    C = [['29', '-66'], ['32', '-5']]
    f.g('k1 k2 k3').rect(14, 38, 108, 24, BLUE, 1.4, LB).end()
    f.g('k2 k3').rect(140, 26, 36, 80, RED, 1.4, LR).end()
    mat(f, 16, 38, A, 36, 26, INK, 13)
    mat(f, 140, 26, B, 36, 26, INK, 13)
    f.text(228, 70, '=', 16, INK)
    f.g('k3').rect(246, 38, 40, 24, GREEN, 1.4, LG).end()
    mat(f, 246, 38, C, 40, 26, INK, 13)
    f.text(18, 126, 'row 1 of A', 12, BLUE, 'start').text(140, 126, 'column 1 of B', 12, RED, 'start')
    f.g('k3').text(170, 156, '(1)(-1) + (-3)(2) + (6)(6) = 29', 12.5, GREEN).end()
    return f


def f_det():
    f = Fig(300, 140)
    f.line(50, 36, 118, 96, BLUE, 2.4, op=0.45).line(118, 36, 50, 96, RED, 2.4, op=0.45)
    mat(f, 40, 30, [['a', 'b'], ['c', 'd']], 44, 36, INK, 16, bars=True)
    f.text(150, 128, 'blue diagonal minus red diagonal', 11.5, GREY)
    f.text(170, 62, 'ad', 18, BLUE, 'start').text(204, 62, '-', 18, INK, 'start').text(222, 62, 'bc', 18, RED, 'start')
    f.text(170, 96, 'e.g. 3(12) - 6(5) = 6', 11.5, INK, 'start')
    return f


def f_cramer():
    p = Plot(-1, 5, -3, 5, unit=40, uy=26, every=1, yevery=1, gstep=1, xlab='x', ylab='y')
    p.fullline(-1.5, 4, c=BLUE, lab='3x + 2y = 8', labx=0.1, labpos='ne')
    p.fullline(4 / 3, -5 / 3, c=RED, lab='4x - 3y = 5', labx=3.8, labpos='nw')
    p.pt(2, 1, '(2, 1)', 'e', GREEN)
    return p


def f_cases():
    f = Fig(340, 150)
    for k, (title, sub, lines) in enumerate((('D not 0', 'one solution', [(-0.8, 0.3), (0.9, -0.2)]),
                                             ('D = 0', 'no solution', [(0.6, 0.35), (0.6, -0.35)]),
                                             ('D = 0', 'infinitely many', [(0.6, 0.0)]))):
        x0 = 12 + k * 110
        f.rect(x0, 10, 98, 98, GREY, 1, 'none')
        cx, cy = x0 + 49, 59
        for j, (m, c) in enumerate(lines):
            col = [BLUE, RED][j]
            f.line(cx - 44, cy + 44 * m - c * 44, cx + 44, cy - 44 * m - c * 44, col, 2.4)
        if k == 2:
            f.line(cx - 44, cy + 44 * 0.6, cx + 44, cy - 44 * 0.6, RED, 2.2, dash='6 5')
        if k == 0:
            s0 = (lines[1][1] - lines[0][1]) / (lines[0][0] - lines[1][0])
            f.dot(cx + 44 * s0, cy - 44 * (lines[0][0] * s0 + lines[0][1]), GREEN, 5)
        f.text(cx, 126, title, 12.5, INK).text(cx, 143, sub, 11.5, GREY)
    return f


DIAGRAMS = {
    'order': (f_order(), 'Rows, columns and the position of an entry', 159),
    'mult': (f_mult(), 'Example 4.13 (corrected): row times column', 163),
    'det': (f_det(), 'The 2 x 2 determinant', 166),
    'cramer': (f_cramer(), 'Example 4.20: the solution is where the lines meet', 169),
    'cases': (f_cases(), 'What the determinant D says about a 2 x 2 system', 168),
}

# ------------------------------------------------------------------ 4.1
L1 = [
    T('=math12-u4-c01', '4.1.1 What is a matrix?', 158,
      'A **matrix** is a rectangular array of numbers in brackets; the numbers are its **entries** (elements). Activity 4.1: Ali has 3 notebooks and 2 pencils, Abraham 10 and 13: $\\begin{pmatrix} 3 & 2 \\\\ 10 & 13 \\end{pmatrix}$ — rows are people, columns are items.',
      'A matrix with $m$ rows and $n$ columns has **order** $m \\times n$ (rows first). $a_{ij}$ is the entry in row $i$, column $j$ (for $1 \\le i \\le m$, $1 \\le j \\le n$; the book prints "$1 \\le i \\le m$" twice).'),
    DG('order', 'Reading a matrix', 159, 'order',
       'Example 4.1: $B$ has 3 rows and 2 columns, order $3 \\times 2$. $a_{21}$ means row 2, column 1. Always say rows first.'),
    TB('types-tb', '4.1.2 Types of matrices', 159, ['Type', 'Meaning', 'Example'],
       [['row matrix', 'one row', '$(12 \\ \\ 3 \\ \\ 6)$'], ['column matrix', 'one column', '$\\begin{pmatrix} 1 \\\\ 4 \\\\ 9 \\end{pmatrix}$'],
        ['square', 'rows = columns', '$\\begin{pmatrix} 2 & 3 \\\\ 5 & 13 \\end{pmatrix}$'], ['diagonal', 'square, zero off the diagonal', '$\\begin{pmatrix} 2 & 0 \\\\ 0 & 6 \\end{pmatrix}$'],
        ['identity $I$', 'diagonal with 1s', '$\\begin{pmatrix} 1 & 0 \\\\ 0 & 1 \\end{pmatrix}$'], ['zero matrix $O$', 'every entry 0', '$\\begin{pmatrix} 0 & 0 \\\\ 0 & 0 \\end{pmatrix}$']], layout='cards'),
    RM('equal-rm', 'Equal matrices', 160, 'Two matrices are equal when they have the **same order** and **every** corresponding entry is equal ($a_{ij} = b_{ij}$). So $\\begin{pmatrix} x + 2 & 5 \\\\ 1 & y - 3 \\end{pmatrix} = \\begin{pmatrix} 7 & 5 \\\\ 1 & 2 \\end{pmatrix}$ gives $x = 5$, $y = 5$.'),
    T('ops-t', '4.1.3 Adding, subtracting and scalar multiples', 161,
      '**Sum / difference:** only for matrices of the same order — add or subtract matching entries. Example 4.9: $\\begin{pmatrix} 1 & 4 \\\\ -2 & 1 \\end{pmatrix} + \\begin{pmatrix} 11 & 23 \\\\ 0 & -6 \\end{pmatrix} = \\begin{pmatrix} 12 & 27 \\\\ -2 & -5 \\end{pmatrix}',
      '**Scalar multiple** $\\lambda A$: multiply every entry by $\\lambda$. $5\\begin{pmatrix} 6 & -7 \\\\ 1 & 2 \\end{pmatrix} = \\begin{pmatrix} 30 & -35 \\\\ 5 & 10 \\end{pmatrix}$. The **negative** $-A = (-1)A$.',
      'A $2 \\times 2$ and a $3 \\times 2$ matrix cannot be added (Activity 4.2 Q2).'),
    ST('mult', '4.1.4 Multiplying matrices: row × column', 163, 'mult',
       [('$AB$ exists only if (columns of $A$) = (rows of $B$). Here $2 \\times 3$ times $3 \\times 2$ gives a $2 \\times 2$ matrix.', 'k1'),
        ('Entry $(i, k)$ of $AB$: take row $i$ of $A$ and column $k$ of $B$.', 'k2'),
        ('Multiply pair by pair and add: $(1)(-1) + (-3)(2) + (6)(6) = 29$. The other entries are $-66$, $32$, $-5$ (the book prints $-63$ and $-15$; check: $3 - 15 - 54 = -66$, $6 + 25 - 36 = -5$).', 'k3')]),
    RM('mult22-rm', '2 × 2 product', 164,
       '$$\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}\\begin{pmatrix} e & f \\\\ g & h \\end{pmatrix} = \\begin{pmatrix} ae + bg & af + bh \\\\ ce + dg & cf + dh \\end{pmatrix}$$',
       'Usually $AB \\ne BA$. With $$A = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}, \\quad B = \\begin{pmatrix} 6 & 8 \\\\ 5 & 7 \\end{pmatrix}$$ we get $$AB = \\begin{pmatrix} 16 & 22 \\\\ 38 & 52 \\end{pmatrix}, \\quad BA = \\begin{pmatrix} 30 & 44 \\\\ 26 & 38 \\end{pmatrix}$$',
       'Also $AB = AC$ does not force $B = C$ (Review Q2). (The book\'s $3 \\times 3$ product box has small index slips, e.g. $a_{13}b_{32}$ for $a_{13}b_{31}$.)'),
    WK('m2', 'Worked example: Exercise 4.2 Q2', 165, 'If $M = \\begin{pmatrix} 1 & 3 \\\\ -2 & 2 \\end{pmatrix}$, show that $M^2 - 3M + 8I = O$.',
       ['$M^2 = \\begin{pmatrix} 1 - 6 & 3 + 6 \\\\ -2 - 4 & -6 + 4 \\end{pmatrix} = \\begin{pmatrix} -5 & 9 \\\\ -6 & -2 \\end{pmatrix}$.', '$-3M = \\begin{pmatrix} -3 & -9 \\\\ 6 & -6 \\end{pmatrix}$, $8I = \\begin{pmatrix} 8 & 0 \\\\ 0 & 8 \\end{pmatrix}$.', 'Add: $\\begin{pmatrix} -5 - 3 + 8 & 9 - 9 + 0 \\\\ -6 + 6 + 0 & -2 - 6 + 8 \\end{pmatrix}$.'],
       '$\\begin{pmatrix} 0 & 0 \\\\ 0 & 0 \\end{pmatrix}$ ✓'),
    T('inv-t', '4.1.5 The inverse of a 2 × 2 matrix', 165,
      '$B$ is the **inverse** of $A$ ($B = A^{-1}$) if $AB = BA = I$. Activity 4.3: $\\begin{pmatrix} 2 & 3 \\\\ 1 & 2 \\end{pmatrix}\\begin{pmatrix} 2 & -3 \\\\ -1 & 2 \\end{pmatrix} = I$.',
      '**Shortcut:** for $A = \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$ with $ad - bc \\ne 0$: $$A^{-1} = \\frac{1}{ad - bc}\\begin{pmatrix} d & -b \\\\ -c & a \\end{pmatrix}$$ (swap $a$ and $d$, change the signs of $b$ and $c$, divide by the determinant).',
      'If $ad - bc = 0$ the matrix has **no inverse** (it is singular).'),
    WK('ex416', 'Worked example: Example 4.16 two ways', 166, 'Find the inverse of $A = \\begin{pmatrix} 2 & 1 \\\\ 1 & 1 \\end{pmatrix}$.',
       ['Book method: $\\begin{pmatrix} 2 & 1 \\\\ 1 & 1 \\end{pmatrix}\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} = I$ gives $2a + c = 1$, $a + c = 0$, $2b + d = 0$, $b + d = 1$, so $a = 1$, $c = -1$, $b = -1$, $d = 2$.',
        'Shortcut: $ad - bc = 2 - 1 = 1$; swap and change signs: $\\begin{pmatrix} 1 & -1 \\\\ -1 & 2 \\end{pmatrix}$.', 'Check: $\\begin{pmatrix} 2 & 1 \\\\ 1 & 1 \\end{pmatrix}\\begin{pmatrix} 1 & -1 \\\\ -1 & 2 \\end{pmatrix} = \\begin{pmatrix} 1 & 0 \\\\ 0 & 1 \\end{pmatrix}$.'],
       '$A^{-1} = \\begin{pmatrix} 1 & -1 \\\\ -1 & 2 \\end{pmatrix}$'),
    DG('det', '4.1.6 The determinant', 166, 'det',
       '$$\\det A = |A| = \\begin{vmatrix} a & b \\\\ c & d \\end{vmatrix} = ad - bc$$ A determinant is a **number**; a matrix is a table. Example 4.17: $\\begin{vmatrix} -3 & 5 \\\\ 9 & -2 \\end{vmatrix} = 6 - 45 = -39$.'),
    T('det3-t', '3 × 3 determinants (expansion along row 1)', 167,
      '$|A| = a_{11}\\begin{vmatrix} a_{22} & a_{23} \\\\ a_{32} & a_{33} \\end{vmatrix} - a_{12}\\begin{vmatrix} a_{21} & a_{23} \\\\ a_{31} & a_{33} \\end{vmatrix} + a_{13}\\begin{vmatrix} a_{21} & a_{22} \\\\ a_{31} & a_{32} \\end{vmatrix}$ — signs $+ \\, - \\, +$; each small determinant deletes that entry\'s row and column.',
      '**Example 4.18 (corrected):** $\\begin{vmatrix} 2 & 1 & 0 \\\\ 3 & -1 & 1 \\\\ 4 & 6 & -2 \\end{vmatrix} = 2(2 - 6) - 1(-6 - 4) + 0 = -8 + 10 = 2$. The book uses $-8$ for the first minor (it is $-4$) and gets $-6$.'),
    'math12-u4-tblE1', 'math12-u4-chkE1', 'math12-u4-chkE2', 'math12-u4-chk74', 'math12-u4-wrk1', 'math12-u4-chk75', 'math12-u4-wrk2', 'math12-u4-chk76', 'math12-u4-wrk3', 'math12-u4-chk77', 'math12-u4-wrk4',
]

# ------------------------------------------------------------------ 4.2
L2 = [
    T('=math12-u4-c02', '4.2 Cramer\'s rule', 168,
      'For $\\begin{cases} ax + by = e \\\\ cx + dy = f \\end{cases}$ form three determinants:',
      '$D = \\begin{vmatrix} a & b \\\\ c & d \\end{vmatrix}$ (coefficients), $D_x = \\begin{vmatrix} e & b \\\\ f & d \\end{vmatrix}$ (constants replace the $x$-column), $D_y = \\begin{vmatrix} a & e \\\\ c & f \\end{vmatrix}$ (constants replace the $y$-column).',
      'If $D \\ne 0$: $x = \\frac{D_x}{D}$, $y = \\frac{D_y}{D}$ — one solution.'),
    DG('cramer', 'Worked example: Example 4.20', 169, 'cramer',
       '$3x + 2y = 8$, $4x - 3y = 5$. $D = -9 - 8 = -17$, $D_x = -24 - 10 = -34$, $D_y = 15 - 32 = -17$.',
       '$x = \\frac{-34}{-17} = 2$, $y = \\frac{-17}{-17} = 1$: the lines cross at $(2, 1)$.'),
    DG('cases', 'When Cramer\'s rule fails', 168, 'cases',
       'If $D = 0$ the lines have the same slope: they are parallel (no solution, inconsistent) or the same line (infinitely many solutions, dependent). Cramer\'s rule needs $D \\ne 0$.'),
    WK('act46', 'Worked example: Activity 4.6', 168, 'Solve $x - 2y = 3$, $2x + y = 4$ by Cramer\'s rule.',
       ['$D = \\begin{vmatrix} 1 & -2 \\\\ 2 & 1 \\end{vmatrix} = 1 + 4 = 5$.', '$D_x = \\begin{vmatrix} 3 & -2 \\\\ 4 & 1 \\end{vmatrix} = 3 + 8 = 11$, $D_y = \\begin{vmatrix} 1 & 3 \\\\ 2 & 4 \\end{vmatrix} = 4 - 6 = -2$.', '$x = \\frac{11}{5}$, $y = -\\frac{2}{5}$.'],
       '$\\left\\{\\left(\\frac{11}{5}, -\\frac{2}{5}\\right)\\right\\}$'),
    TB('methods-tb', 'Elimination or Cramer?', 168, ['', 'Elimination', 'Cramer\'s rule'],
       [['idea', 'add multiples of the equations to remove a variable', 'three determinants and two divisions'], ['best when', 'coefficients are easy to match', 'you want a formula / a quick check'],
        ['if $D = 0$', 'shows no or many solutions', 'cannot be used']]),
    WK('digits', 'Worked example: Review Q4 (digits)', 170, 'The digits of a two-digit number add to 10. Reversed, the number is one less than twice the original. Find it.',
       ['Let tens digit $x$, units $y$: $x + y = 10$ and $10y + x = 2(10x + y) - 1$, i.e. $-19x + 8y = -1$.', '$D = \\begin{vmatrix} 1 & 1 \\\\ -19 & 8 \\end{vmatrix} = 27$, $D_x = \\begin{vmatrix} 10 & 1 \\\\ -1 & 8 \\end{vmatrix} = 81$, $D_y = \\begin{vmatrix} 1 & 10 \\\\ -19 & -1 \\end{vmatrix} = 189$.', '$x = 3$, $y = 7$; check $73 = 2(37) - 1$.'],
       '37'),
    'math12-u4-c03', 'math12-u4-c04', 'math12-u4-c05', 'math12-u4-c06', 'math12-u4-wk2', 'math12-u4-pc21', 'math12-u4-pc22', 'math12-u4-pc23',
    RM('summary-t', 'Unit summary', 170,
       'Order $m \\times n$; add only equal orders; $AB$ needs columns of $A$ = rows of $B$; usually $AB \\ne BA$.',
       '$\\det\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} = ad - bc$; $A^{-1} = \\frac{1}{ad - bc}\\begin{pmatrix} d & -b \\\\ -c & a \\end{pmatrix}$.',
       'Cramer: $x = \\frac{D_x}{D}$, $y = \\frac{D_y}{D}$ when $D \\ne 0$.'),
]

LESSONS = {'math12-u4-l4-1': L1, 'math12-u4-l4-2': L2}

# ------------------------------------------------------------------ practice
a = QSet('4.1 Practice — matrix operations', 's41')
a.S(161, 'Exercise 4.1: order of (a) $\\begin{pmatrix} 2 & 2 \\\\ 5 & 9 \\end{pmatrix}$ (b) a matrix with rows $(1, 17)$, $(17, 7)$, $(3, 2)$ (c) $\\begin{pmatrix} 1 & 5 & 4 \\\\ 3 & 6 & 8 \\\\ 7 & 2 & 9 \\end{pmatrix}$.', '$2 \\times 2$, $3 \\times 2$, $3 \\times 3$',
    ['Step 1: count rows, then columns.'], 'Rows first ("RC" like Roman Catholic).', [('$(12 \\ \\ 3 \\ \\ 6)$?', '$1 \\times 3$.')])
a.S(161, 'Activity 4.2: $A = \\begin{pmatrix} 2 & 5 \\\\ 2 & 9 \\end{pmatrix}$, $B = \\begin{pmatrix} 2 & 9 \\\\ 1 & 4 \\end{pmatrix}$: find $A + B$, $A - B$, $3A$.', '$\\begin{pmatrix} 4 & 14 \\\\ 3 & 13 \\end{pmatrix}$, $\\begin{pmatrix} 0 & -4 \\\\ 1 & 5 \\end{pmatrix}$, $\\begin{pmatrix} 6 & 15 \\\\ 6 & 27 \\end{pmatrix}$',
    ['Step 1: entry by entry.', 'Step 2: $3A$ multiplies every entry by 3.'], 'Same position ↔ same position.', [('$AB$?', '$\\begin{pmatrix} 9 & 38 \\\\ 13 & 54 \\end{pmatrix}$.')])
a.S(165, 'Exercise 4.2 Q1: $A = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$, $B = \\begin{pmatrix} 6 & 8 \\\\ 5 & 7 \\end{pmatrix}$: $A + B$, $AB$, $BA$.', '$\\begin{pmatrix} 7 & 10 \\\\ 8 & 11 \\end{pmatrix}$, $\\begin{pmatrix} 16 & 22 \\\\ 38 & 52 \\end{pmatrix}$, $\\begin{pmatrix} 30 & 44 \\\\ 26 & 38 \\end{pmatrix}$',
    ['Step 1: $AB$ row 1: $(6 + 10, 8 + 14)$.', 'Step 2: $BA$ row 1: $(6 + 24, 12 + 32)$.'], '$AB \\ne BA$ in general.', [('$A^2$?', '$\\begin{pmatrix} 7 & 10 \\\\ 15 & 22 \\end{pmatrix}$.')])
a.S(165, 'Exercise 4.2 Q3: (a) $\\begin{pmatrix} a & b \\\\ -b & a \\end{pmatrix} + \\begin{pmatrix} a & b \\\\ b & a \\end{pmatrix}$ (b) $\\begin{pmatrix} 1 \\\\ 2 \\\\ 3 \\end{pmatrix}(2 \\ \\ 3 \\ \\ 4)$', '(a) $\\begin{pmatrix} 2a & 2b \\\\ 0 & 2a \\end{pmatrix}$ (b) $\\begin{pmatrix} 2 & 3 & 4 \\\\ 4 & 6 & 8 \\\\ 6 & 9 & 12 \\end{pmatrix}$',
    ['Step 1: (a) add entries.', 'Step 2: (b) $3 \\times 1$ times $1 \\times 3$ gives $3 \\times 3$; entry $(i, k) = $ (row entry)(column entry).'], 'Check the order first.', [('$(2 \\ \\ 3 \\ \\ 4)\\begin{pmatrix} 1 \\\\ 2 \\\\ 3 \\end{pmatrix}$?', '$(20)$, a $1 \\times 1$ matrix.')])
a.S(165, 'Exercise 4.2 Q3(c): $\\begin{pmatrix} 2 & 3 & 4 \\\\ 3 & 4 & 5 \\\\ 4 & 5 & 6 \\end{pmatrix}\\begin{pmatrix} 1 & -3 & 5 \\\\ 0 & 2 & 4 \\\\ 3 & 0 & 5 \\end{pmatrix}$', '$\\begin{pmatrix} 14 & 0 & 42 \\\\ 18 & -1 & 56 \\\\ 22 & -2 & 70 \\end{pmatrix}$',
    ['Step 1: entry (1, 1): $2 + 0 + 12 = 14$.', 'Step 2: entry (1, 2): $-6 + 6 + 0 = 0$.', 'Step 3: continue row by row.'], 'Nine row × column sums.', [('Entry (3, 3)?', '$20 + 20 + 30 = 70$.')])
a.S(166, 'Exercise 4.3: inverses of (a) $\\begin{pmatrix} 2 & 5 \\\\ 1 & 3 \\end{pmatrix}$ (b) $\\begin{pmatrix} 1 & 2 \\\\ 2 & -1 \\end{pmatrix}$ (c) $\\begin{pmatrix} 2 & 1 \\\\ 7 & 4 \\end{pmatrix}$ (d) $\\begin{pmatrix} 7 & -10 \\\\ -2 & 3 \\end{pmatrix}$.', '(a) $\\begin{pmatrix} 3 & -5 \\\\ -1 & 2 \\end{pmatrix}$ (b) $\\frac{1}{5}\\begin{pmatrix} 1 & 2 \\\\ 2 & -1 \\end{pmatrix}$ (c) $\\begin{pmatrix} 4 & -1 \\\\ -7 & 2 \\end{pmatrix}$ (d) $\\begin{pmatrix} 3 & 10 \\\\ 2 & 7 \\end{pmatrix}$',
    ['Step 1: determinants 1, −5, 1, 1.', 'Step 2: swap the diagonal, negate the others, divide by $D$.', 'Step 3: (b) $\\frac{1}{-5}\\begin{pmatrix} -1 & -2 \\\\ -2 & 1 \\end{pmatrix}$.'], 'Check with $AA^{-1} = I$.', [('$\\begin{pmatrix} 4 & 3 \\\\ 1 & 1 \\end{pmatrix}^{-1}$?', '$\\begin{pmatrix} 1 & -3 \\\\ -1 & 4 \\end{pmatrix}$.')])
a.S(167, 'Exercise 4.4 Q1: evaluate $\\begin{vmatrix} 1 & 2 \\\\ 3 & 4 \\end{vmatrix}$, $\\begin{vmatrix} -5 & 5 \\\\ 9 & 7 \\end{vmatrix}$, $\\begin{vmatrix} 0 & 1 \\\\ -1 & 9 \\end{vmatrix}$, $\\begin{vmatrix} \\cos 30° & -\\sin 30° \\\\ \\sin 30° & \\cos 30° \\end{vmatrix}$.', '−2, −80, 1, 1',
    ['Step 1: $ad - bc$.', 'Step 2: $-35 - 45 = -80$.', 'Step 3: $\\cos^2 30° + \\sin^2 30° = 1$.'], 'Watch double negatives.', [('$\\begin{vmatrix} 2 & -3 \\\\ 4 & 1 \\end{vmatrix}$?', '14.')])
a.S(167, 'Exercise 4.4 Q2–Q3: (a) $\\begin{vmatrix} 2 & 4 \\\\ 5 & 1 \\end{vmatrix} = \\begin{vmatrix} 2x & 4 \\\\ 6 & x \\end{vmatrix}$ (b) $\\begin{vmatrix} 2 & 3 \\\\ 4 & 5 \\end{vmatrix} = \\begin{vmatrix} x & 3 \\\\ 2x & -5 \\end{vmatrix}$ (Q3) $\\begin{vmatrix} 1 & 2 & 4 \\\\ -1 & 3 & 0 \\\\ 4 & 1 & 0 \\end{vmatrix}$', '(a) $x = \\pm\\sqrt{3}$ (b) $x = \\frac{2}{11}$ (Q3) $-52$',
    ['Step 1: (a) $-18 = 2x^2 - 24$.', 'Step 2: (b) $-2 = -5x - 6x$.', 'Step 3: (Q3) expand along column 3: $4\\begin{vmatrix} -1 & 3 \\\\ 4 & 1 \\end{vmatrix} = 4(-13)$.'], 'Expand along a row or column with zeros.', [('$\\begin{vmatrix} x & 2 \\\\ 3 & x \\end{vmatrix} = 10$?', '$x = \\pm 4$.')])
a.S(170, 'Review Q1–Q2: (1) $A = \\begin{pmatrix} 7 & -3 \\\\ 2 & 5 \\end{pmatrix}$, $B = \\begin{pmatrix} -11 & 9 \\\\ 4 & -6 \\end{pmatrix}$: $A + B$, $A - B$, $AB$. (2) $A = \\begin{pmatrix} 1 & 1 \\\\ 1 & 1 \\end{pmatrix}$: show $AB = AC$ for $B = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$, $C = \\begin{pmatrix} 0 & 3 \\\\ 4 & 3 \\end{pmatrix}$.', '$\\begin{pmatrix} -4 & 6 \\\\ 6 & -1 \\end{pmatrix}$, $\\begin{pmatrix} 18 & -12 \\\\ -2 & 11 \\end{pmatrix}$, $\\begin{pmatrix} -89 & 81 \\\\ -2 & -12 \\end{pmatrix}$; both products are $\\begin{pmatrix} 4 & 6 \\\\ 4 & 6 \\end{pmatrix}$',
    ['Step 1: $AB$ entry (1, 1): $-77 - 12$.', 'Step 2: each row of $A$ adds the two rows of $B$ (or $C$): $(4, 6)$ both times.'], 'You cannot "cancel" $A$: it has no inverse ($\\det A = 0$).', [('$BA$ in Q1?', '$\\begin{pmatrix} -59 & 78 \\\\ 16 & -42 \\end{pmatrix}$.')])
a.M(163, 'If $A$ is $2 \\times 3$ and $B$ is $3 \\times 4$, $AB$ is', ['$2 \\times 4$', '$3 \\times 3$', '$4 \\times 2$', 'not defined'], 'A',
    ['Step 1: inner numbers match (3), outer numbers give the order.'], '$(m \\times n)(n \\times p) = m \\times p$.', [('$BA$?', 'not defined (4 ≠ 2).')])
a.TF(164, 'For $2 \\times 2$ matrices, $AB = BA$ always.', False, ['Step 1: Exercise 4.2 Q1 gives different products.'], 'Order matters.', [('$AI = IA$?', 'yes, always.')])

b = QSet('4.2 Practice — Cramer\'s rule', 's42')
b.S(168, 'Activity 4.5 Q5 by elimination and by Cramer: $3x + 4y = 12$, $x - y = -1$.', '$x = \\frac{8}{7}$, $y = \\frac{15}{7}$',
    ['Step 1: $D = -3 - 4 = -7$.', 'Step 2: $D_x = -12 + 4 = -8$, $D_y = -3 - 12 = -15$.', 'Step 3: divide by $-7$.'], 'Both methods must agree.', [('$x + y = 5$, $x - y = 1$?', '(3, 2).')])
b.S(170, 'Exercise 4.5 Q1–Q3: (1) $9x - 2y = 3$, $3x - y = 6$ (2) $x + y = 3$, $y - x = 1$ (3) $0.8x - 0.6y = 1$, $0.6x + 0.8y = 2$.', '(1) $(-3, -15)$ (2) $(1, 2)$ (3) $(2, 1)$',
    ['Step 1: (1) $D = -9 + 6 = -3$, $D_x = -3 + 12 = 9$, $D_y = 54 - 9 = 45$.', 'Step 2: (2) rewrite as $-x + y = 1$: $D = 2$.', 'Step 3: (3) $D = 0.64 + 0.36 = 1$.'], 'Line up $x$, $y$ and constants first.', [('$2x + y = 7$, $x - y = 2$?', '(3, 1).')])
b.S(170, 'Exercise 4.5 Q4 (3 × 3 Cramer): $3x - 2y + 3z = 8$, $2x + y - z = 1$, $4x - 3y + 2z = 4$.', '$x = 1$, $y = 2$, $z = 3$',
    ['Step 1: $D = 3(2 - 3) + 2(4 + 4) + 3(-6 - 4) = -3 + 16 - 30 = -17$.', 'Step 2: $D_x = -17$, $D_y = -34$, $D_z = -51$.', 'Step 3: divide by $D$.'], 'Same rule: replace one column by the constants.', [('Check in equation 3?', '$4 - 6 + 6 = 4$ ✓.')])
b.S(170, 'Review Q3: (a) $3x - 2y = 4$, $2x + y = -3$ (b) $2x - 3(y + 1) = -3$, $2y = 3x - 5$ (c) $2x - y = 5$, $3x + 2y = -3$.', '(a) $\\left(-\\frac{2}{7}, -\\frac{17}{7}\\right)$ (b) $(3, 2)$ (c) $(1, -3)$',
    ['Step 1: (a) $D = 7$, $D_x = -2$, $D_y = -17$.', 'Step 2: (b) simplify: $2x - 3y = 0$, $3x - 2y = 5$; $D = 5$.', 'Step 3: (c) $D = 7$, $D_x = 7$, $D_y = -21$.'], 'Simplify brackets before forming $D$.', [('$x - y = 0$, $x + y = 4$?', '(2, 2).')])
b.S(168, 'For which $k$ does $kx + 2y = 1$, $3x + 6y = 5$ have no unique solution?', '$k = 1$',
    ['Step 1: $D = 6k - 6 = 0$.', 'Step 2: then the lines are parallel ($x + 2y = 1$ vs $x + 2y = \\frac{5}{3}$): no solution.'], '$D = 0$ ⇒ parallel or the same line.', [('$2x + ky = 4$, $x + 3y = 2$?', '$k = 6$: same line, infinitely many.')])
b.M(169, 'For $3x + 2y = 8$, $4x - 3y = 5$, $D_y$ is', ['$-17$', '$-34$', '17', '31'], 'A',
    ['Step 1: $\\begin{vmatrix} 3 & 8 \\\\ 4 & 5 \\end{vmatrix} = 15 - 32$.'], 'Constants replace the $y$-column.', [('$D_x$?', '$-34$.')])
b.TF(168, 'If $D = 0$, Cramer\'s rule gives the solution $x = 0$, $y = 0$.', False, ['Step 1: dividing by $D = 0$ is impossible; the system has no or infinitely many solutions.'], 'Check $D$ first.', [('$D = 4$?', 'a unique solution.')])

QS = a.items + b.items

GLOSSARY = [
    ('Order of a matrix', 'Rows × columns, e.g. $3 \\times 2$.', 159),
    ('Identity matrix', 'Square matrix with 1s on the diagonal and 0s elsewhere.', 160),
    ('Inverse matrix', '$A^{-1}$ with $AA^{-1} = A^{-1}A = I$.', 165),
    ('Determinant', 'For $\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$: $ad - bc$.', 166),
    ("Cramer's rule", '$x = \\frac{D_x}{D}$, $y = \\frac{D_y}{D}$ for $D \\ne 0$.', 169),
]
TIPS = [('Order: rows first, then columns.', 159), ('Inverse: swap a and d, negate b and c, divide by ad − bc.', 166), ('D = 0: no unique solution.', 168)]
IDEAS = [('mult', 'Matrix multiplication', 'l4_1', 'math12-u4-md-mult'), ('inv', 'Inverse', 'l4_1', 'math12-u4-md-inv-t'),
         ('det', 'Determinant', 'l4_1', 'math12-u4-md-det'), ('cram', "Cramer's rule", 'l4_2', 'math12-u4-c02')]


# tall matrices render cleanly only as display maths on phones: promote inline $..matrix..$ to $$..$$
import re as _re
_MX = _re.compile(r'(?<!\$)\$(?!\$)([^$]*?\\begin\{[pv]matrix\}[^$]*?)\$(?!\$)')


def _disp(o):
    if isinstance(o, str):
        return _MX.sub(r'$$\1$$', o)
    if isinstance(o, list):
        return [_disp(v) for v in o]
    if isinstance(o, tuple):
        return tuple(_disp(v) for v in o)
    if isinstance(o, dict):
        return {k: _disp(v) for k, v in o.items()}
    return o


LESSONS = {k: _disp(v) for k, v in LESSONS.items()}
QS = _disp(QS)
