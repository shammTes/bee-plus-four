import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *

B = Book('mathematics_12')
T = 'Practice'
TIP = 'Write the formula first, then substitute; check the answer with a quick estimate.'

# ---- move misplaced check/worked pairs to the lesson they belong to
B.move(['math12-u1-chk76', 'math12-u1-wrk3'], 'math12-u1-l1-1')
B.move(['math12-u1-chk78', 'math12-u1-wrk5', 'math12-u1-chk79', 'math12-u1-wrk6', 'math12-u1-chk80', 'math12-u1-wrk7'], 'math12-u1-l1-2')
B.move(['math12-u1-chk81', 'math12-u1-wrk8', 'math12-u1-chk82', 'math12-u1-wrk9'], 'math12-u1-l1-3')
B.move(['math12-u1-chk83', 'math12-u1-wrk10'], 'math12-u1-l1-4')
B.move(['math12-u2-chk75', 'math12-u2-wrk2', 'math12-u2-chk76', 'math12-u2-wrk3', 'math12-u2-chk77', 'math12-u2-wrk4',
        'math12-u2-chk78', 'math12-u2-wrk5', 'math12-u2-chk79', 'math12-u2-wrk6'], 'math12-u2-l2-4', after='math12-u2-c08')
B.move(['math12-u3-chk74', 'math12-u3-wrk1', 'math12-u3-chk75', 'math12-u3-wrk2'], 'math12-u3-l3-2', after='math12-u3-c07')
B.move(['math12-u3-chk78', 'math12-u3-wrk5'], 'math12-u3-l3-2')
B.move(['math12-u4-chk76', 'math12-u4-wrk3', 'math12-u4-chk77', 'math12-u4-wrk4'], 'math12-u4-l4-1')

B.remove('math12-u2-c13')
B.set('math12-u3-c08', body=[
    'A **circle** is the set of all points in a plane that are the same distance (the **radius** r) from a fixed point (the **centre**).',
    'If the centre is C(h, k) and P(x, y) is any point on the circle, the distance formula CP = r gives the **standard form**: $$(x - h)^2 + (y - k)^2 = r^2$$. With the centre at the origin this is x² + y² = r².',
    '**Example:** centre (2, −1), radius 5: (x − 2)² + (y + 1)² = 25. Expanding gives the **general form** x² + y² − 4x + 2y − 20 = 0.',
    '**From general to standard form:** complete the square in x and in y. x² + y² + Dx + Ey + F = 0 has centre (−D/2, −E/2) and radius √(D²/4 + E²/4 − F) (a real circle only if this is positive).',
    'To plot points, give one variable a value and solve for the other: in (x − 2)² + (y + 1)² = 25, x = 5 gives (y + 1)² = 16, so y = 3 or y = −5.',
    '**Point and circle:** substitute the point into (x − h)² + (y − k)²: less than r² → inside, equal → on the circle, greater → outside.'])
B.set('math12-u3-c02', body=[
    '**Section formula.** The point P that divides the segment from A(x₁, y₁) to B(x₂, y₂) internally in the ratio m : n (AP : PB = m : n) is $$P\\left(\\frac{nx_1 + mx_2}{m + n}, \\frac{ny_1 + my_2}{m + n}\\right)$$.',
    'The midpoint is the special case m = n = 1. **Example:** A(1, 2), B(7, 8), ratio 1 : 2 → x = (2·1 + 1·7)/3 = 3, y = (2·2 + 1·8)/3 = 4, so P = (3, 4).'])
B.set('math12-u1-c02', body=[
    'An **arithmetic progression (AP)** is a sequence in which each term is obtained from the previous one by adding the same number, the **common difference** d = aₙ₊₁ − aₙ.',
    '**General term:** aₙ = a₁ + (n − 1)d. **Sum of the first n terms:** Sₙ = n/2 · (2a₁ + (n − 1)d) = n/2 · (a₁ + aₙ).',
    '**Arithmetic mean:** if a, b, c are in AP then b = (a + c)/2. Inserting k arithmetic means between a and b gives an AP with k + 2 terms, so d = (b − a)/(k + 1).',
    '**Example (business):** a business makes a profit of 10,000 Nakfa in its first year and the profit grows by 2,500 Nakfa each year. Profit in year 6: a₆ = 10,000 + 5 × 2,500 = 22,500 Nakfa. Total profit in 6 years: S₆ = 6/2 × (10,000 + 22,500) = 97,500 Nakfa.',
    '**Testing for an AP:** compute the differences between consecutive terms; the sequence is an AP only if they are all equal. 3, 7, 11, 15 (d = 4) is an AP; 1, 4, 9, 16 is not.'])
B.set('math12-u1-c03', body=[
    'A **geometric progression (GP)** is a sequence where each term is the previous term multiplied by the same non-zero number, the **common ratio** r = aₙ₊₁ / aₙ.',
    '**General term:** aₙ = a₁ rⁿ⁻¹. **Sum of n terms:** Sₙ = a₁(rⁿ − 1)/(r − 1) for r ≠ 1 (if r = 1, Sₙ = n a₁).',
    '**Geometric mean:** if a, b, c are in GP then b² = ac, so b = √(ac) for positive a, c.',
    '**Example (growth):** an E. coli cell divides into two every 20 minutes. Starting from 1 cell, after 3 hours there are 9 divisions, so 1 × 2⁹ = 512 cells.',
    '**Example:** in a GP a₂ = 6 and a₅ = 48. Then r³ = 48/6 = 8, so r = 2 and a₁ = 3.'])
B.set('math12-u1-c04', body=[
    'A sequence is a **harmonic progression (HP)** if the reciprocals of its terms form an arithmetic progression. Example: 1, 1/2, 1/3, 1/4, … is an HP because 1, 2, 3, 4, … is an AP.',
    '**To find a term of an HP:** take reciprocals, find the term of the AP, then take the reciprocal again. For 1/2, 1/5, 1/8, …: the AP is 2, 5, 8, … with d = 3, so its 10th term is 2 + 9 × 3 = 29 and the 10th term of the HP is 1/29.',
    '**Harmonic mean** of a and b: H = 2ab/(a + b). For positive a, b the means satisfy AM ≥ GM ≥ HM and AM × HM = GM².',
    'There is no simple formula for the sum of an HP.'])
B.set('math12-u2-c03', body=[
    'A **pie chart** is a circle divided into sectors; each sector angle = (frequency ÷ total) × 360°, so the area is proportional to the frequency.',
    'A **bar graph** labels the categories on the horizontal axis and the frequency (or relative frequency) on the vertical axis; bars have equal width and gaps between them.',
    'A **histogram** is used for grouped (continuous) data: the bars stand on the class boundaries and touch each other. A **frequency polygon** joins the midpoints of the tops of the histogram bars.',
    'An **ogive** (cumulative frequency curve) plots cumulative frequency against upper class boundaries; it is used to estimate the median and quartiles.',
    '**Example:** 60 students: 15 walk, 30 take the bus, 15 cycle. Angles: walk 15/60 × 360° = 90°, bus 180°, cycle 90°.'])

# ---- extra checks
B.add('math12-u1-l1-3', [check('math12-u1-pc31', 'In a GP, a₁ = 5 and r = 3. What is a₄?', ['135', '45', '405', '14'], 'A',
      'aₙ = a₁rⁿ⁻¹, so a₄ = 5 × 3³ = 5 × 27 = 135. (14 would come from adding 3 each time — that is an AP.)', title=T)])
B.add('math12-u1-l1-4', [
    check('math12-u1-pc41', 'Which sequence is a harmonic progression?', ['1/3, 1/6, 1/9, 1/12', '3, 6, 9, 12', '1/2, 1/4, 1/8, 1/16', '1, 3, 9, 27'], 'A',
          'Take reciprocals: 3, 6, 9, 12 is an AP (d = 3), so 1/3, 1/6, 1/9, 1/12 is an HP. 1/2, 1/4, 1/8 has reciprocals 2, 4, 8 — a GP, not an AP.', title=T),
    check('math12-u1-pc42', 'What is the harmonic mean of 4 and 12?', ['6', '8', '√48', '16'], 'A',
          'H = 2ab/(a + b) = 2 × 4 × 12/16 = 96/16 = 6. (8 is the arithmetic mean and √48 the geometric mean; note 8 > √48 > 6.)', title=T)])
B.add('math12-u1-l1-5', [
    check('math12-u1-pc51', 'Find the sum to infinity of 8 + 4 + 2 + 1 + …', ['16', '15', '∞', '12'], 'A',
          '|r| = 1/2 < 1, so the series converges: S∞ = a₁/(1 − r) = 8/(1/2) = 16.', title=T),
    check('math12-u1-pc52', 'For which common ratio does a geometric series converge?', ['r = −0.5', 'r = 1', 'r = 2', 'r = −1.5'], 'A',
          'An infinite geometric series converges only when |r| < 1. Only −0.5 satisfies this.', title=T),
    check('math12-u1-pc53', 'Write 0.777… as a fraction.', ['7/9', '7/10', '77/100', '7/99'], 'A',
          '0.777… = 0.7 + 0.07 + 0.007 + …, a geometric series with a₁ = 0.7, r = 0.1: S = 0.7/0.9 = 7/9.', title=T)])
B.add('math12-u2-l2-2', [
    check('math12-u2-pc21', 'Classes are 10–19, 20–29, 30–39. What is the class width?', ['10', '9', '19', '20'], 'A',
          'Class width = difference between consecutive lower class limits: 20 − 10 = 10 (or between the class boundaries 9.5 and 19.5).', title=T),
    check('math12-u2-pc22', 'Frequencies are 3, 7, 5, 5. What is the cumulative frequency of the third class?', ['15', '5', '12', '20'], 'A',
          'Cumulative frequency adds all frequencies up to that class: 3 + 7 + 5 = 15.', title=T),
    check('math12-u2-pc23', 'What is the midpoint (class mark) of the class 20–29?', ['24.5', '25', '9', '20'], 'A',
          'Class mark = (lower limit + upper limit)/2 = (20 + 29)/2 = 24.5. Class marks are used as x when finding the mean of grouped data.', title=T)])
B.add('math12-u2-l2-3', [
    check('math12-u2-pc31', 'In a pie chart of 72 students, 18 chose biology. What is the angle of the biology sector?', ['90°', '18°', '25°', '72°'], 'A',
          'Angle = (18/72) × 360° = 1/4 × 360° = 90°.', title=T),
    check('math12-u2-pc32', 'Which graph is drawn with touching bars on class boundaries?', ['Histogram', 'Bar graph', 'Pie chart', 'Line graph'], 'A',
          'A histogram is for grouped continuous data, so its bars touch. A bar graph is for categories and has gaps.', title=T),
    check('math12-u2-pc33', 'Which graph is used to estimate the median of grouped data?', ['Ogive (cumulative frequency curve)', 'Pie chart', 'Bar graph', 'Pictogram'], 'A',
          'On an ogive, read across from half the total frequency (n/2) to the curve and down to the x-axis to get the median.', title=T)])
B.add('math12-u2-l2-5', [check('math12-u2-pc51', 'A bag has 3 red and 5 blue balls. One is drawn at random. P(red) = ?', ['3/8', '3/5', '5/8', '1/3'], 'A',
      'P = favourable outcomes / total outcomes = 3/(3 + 5) = 3/8.', title=T)])
B.add('math12-u3-l3-1', [check('math12-u3-pc11', 'Find the point dividing A(2, 1) and B(8, 7) internally in the ratio 2 : 1.', ['(6, 5)', '(4, 3)', '(5, 4)', '(10, 8)'], 'A',
      'x = (1·2 + 2·8)/3 = 18/3 = 6, y = (1·1 + 2·7)/3 = 15/3 = 5. P is twice as far from A as from B, so it is nearer B.', title=T)])
B.add('math12-u3-l3-3', [
    check('math12-u3-pc31', 'Find the radius of the circle x² + y² − 6x + 8y = 0.', ['5', '25', '10', '√7'], 'A',
          'Complete the squares: (x − 3)² + (y + 4)² = 9 + 16 = 25, so r = √25 = 5 and the centre is (3, −4).', title=T),
    check('math12-u3-pc32', 'Which is the equation of the circle with centre (−1, 2) and radius 3?', ['(x + 1)² + (y − 2)² = 9', '(x − 1)² + (y + 2)² = 9', '(x + 1)² + (y − 2)² = 3', 'x² + y² = 9'], 'A',
          'Standard form (x − h)² + (y − k)² = r² with h = −1, k = 2, r² = 9.', title=T)])
B.add('math12-u4-l4-2', [
    worked('math12-u4-wk2', 'Worked example: Cramer’s rule', 'Solve 3x + 2y = 12 and x − y = −1 using determinants.', [
        'Step 1: D = |3 2; 1 −1| = 3(−1) − 2(1) = −5.', 'Step 2: Dx: replace the x-column by the constants: |12 2; −1 −1| = −12 + 2 = −10.',
        'Step 3: Dy: replace the y-column: |3 12; 1 −1| = −3 − 12 = −15.', 'Step 4: x = Dx/D = 2, y = Dy/D = 3. Check: 3(2) + 2(3) = 12 ✔, 2 − 3 = −1 ✔.'], 'x = 2, y = 3'),
    check('math12-u4-pc21', 'Evaluate |5 −2; 3 4|.', ['26', '14', '−26', '23'], 'A', 'ad − bc = 5 × 4 − (−2)(3) = 20 + 6 = 26.', title=T),
    check('math12-u4-pc22', 'A system has D = 0. What can you say?', ['Cramer’s rule cannot be used: no unique solution', 'The solution is x = y = 0', 'There are exactly two solutions', 'x = Dx'], 'A',
          'Cramer’s rule divides by D. If D = 0 the lines are parallel (no solution) or the same line (infinitely many solutions).', title=T),
    check('math12-u4-pc23', 'For 2x + y = 5 and x + 3y = 5, what is Dx?', ['10', '5', '−10', '15'], 'A',
          'D = 2·3 − 1·1 = 5. Dx replaces the x-column by the constants: |5 1; 5 3| = 15 − 5 = 10, so x = 10/5 = 2 (and y = 1).', title=T)])

# ---- exercise: fix weak whys, then extend every unit to 22 questions
u1 = B.unit('math12-u1')['exercise']['questions']
u1[0]['why'] = ['aₙ = a₁ + (n − 1)d, so a₅ = 4 + 4 × 5 = 24.', '20 comes from forgetting that a₅ needs only four steps of d (it would be 4 × 5).']
u1[1]['why'] = ['r = a₂/a₁ = 6/2 = 3; check a₃/a₂ = 18/6 = 3 ✔.', '4 is the difference 6 − 2 — that would describe an AP, not a GP.']
for q in u1: q.pop('why_src', None)
u2 = B.unit('math12-u2')['exercise']['questions']
u2[0] = mcq('math12-u2-q01', 'The mean of 4, 8, 6, 10 and 12 is', ['8', '6', '10', '40'], 'A',
            ['Mean = sum ÷ number of values = (4 + 8 + 6 + 10 + 12)/5 = 40/5 = 8.'], TIP, [('Mean of 3, 5, 7?', '5')], page=78)
u2[1]['why'] = ['The outcomes are HH, HT, TH, TT (4 equally likely). Only TT has no head.', 'P(at least one head) = 1 − P(no head) = 1 − 1/4 = 3/4.']
u2[6] = fill('math12-u2-q07', 'An event that contains exactly one outcome of the sample space is called a ____ event.', ['simple', 'compound', 'sure', 'impossible'], 'simple',
             ['A simple (elementary) event has one outcome, e.g. "getting a 3" on a die. "Getting an even number" = {2, 4, 6} is a compound event.'], 'Count the outcomes in the event.', page=95)
u4 = B.unit('math12-u4')['exercise']['questions']
w4 = ['That is the definition: numbers arranged in rows and columns in a rectangle; a matrix with m rows and n columns has order m × n.',
      'Each number in a matrix is an element (entry); aᵢⱼ is the entry in row i and column j.',
      'Square matrix: number of rows = number of columns (2 × 2, 3 × 3, …). Only square matrices have determinants and inverses.',
      'The identity matrix I has 1s on the main diagonal and 0s elsewhere; AI = IA = A, like multiplying a number by 1.',
      'A + B is defined only for matrices of the same order; then (A + B)ᵢⱼ = aᵢⱼ + bᵢⱼ.']
u4[7]['q'] = 'The sum of two matrices of the same order is found by adding the corresponding elements.'
for q, w in zip(u4[3:8], w4):
    q['why'] = [w]
for g in B.unit('math12-u4').get('games', []):
    for c in g.get('cards', []):
        if c.get('back', '').endswith('The textbook says this.'):
            front = c['front']
            for q, w in zip(u4[3:8], w4):
                if q['q'][:30] == front[:30] or (front.startswith('Observe') and q['id'] == 'math12-u4-q08'):
                    c['front'] = q['q']; c['back'] = 'True. ' + w

S = lambda q, a: (q, a)
B.ex('math12-u1', [
    mcq('math12-u1-q09', 'The 20th term of the AP 7, 11, 15, … is', ['83', '87', '80', '79'], 'A', ['d = 4, a₂₀ = a₁ + 19d = 7 + 76 = 83.'], TIP, [S('10th term of 3, 8, 13, …?', '48')], page=10),
    mcq('math12-u1-q10', 'The sum of the first 15 terms of 2, 5, 8, … is', ['345', '330', '360', '690'], 'A', ['S₁₅ = 15/2 × (2·2 + 14·3) = 15/2 × 46 = 345.'], TIP, [S('Sum of first 10 terms of 1, 3, 5, …?', '100')], page=14),
    mcq('math12-u1-q11', 'The 7th term of the GP 3, 6, 12, … is', ['192', '384', '96', '21'], 'A', ['r = 2, a₇ = 3 × 2⁶ = 3 × 64 = 192.'], TIP, [S('5th term of 2, 6, 18, …?', '162')], page=21),
    mcq('math12-u1-q12', 'The sum of the first 6 terms of the GP 1, 3, 9, … is', ['364', '243', '728', '121'], 'A', ['S₆ = 1 × (3⁶ − 1)/(3 − 1) = (729 − 1)/2 = 364.'], TIP, [S('Sum of 1 + 2 + 4 + … (8 terms)?', '255')], page=24),
    mcq('math12-u1-q13', 'The sum to infinity of 12 + 6 + 3 + … is', ['24', '21', '36', 'It does not exist'], 'A', ['r = 1/2, |r| < 1, so S∞ = 12/(1 − 1/2) = 24.'], 'Check |r| < 1 before using a/(1 − r).', [S('Sum to infinity of 9 + 3 + 1 + …?', '13.5')], page=33),
    short('math12-u1-q14', 'Find the arithmetic mean of 8 and 20.', '14', ['AM = (8 + 20)/2 = 14; then 8, 14, 20 is an AP with d = 6.'], TIP, [S('AM of −4 and 10?', '3')], page=15),
    short('math12-u1-q15', 'Find the (positive) geometric mean of 4 and 25.', '10', ['GM = √(4 × 25) = √100 = 10; then 4, 10, 25 is a GP with r = 2.5.'], TIP, [S('GM of 2 and 18?', '6')], page=25),
    mcq('math12-u1-q16', 'The harmonic mean of 3 and 6 is', ['4', '4.5', '√18', '9'], 'A', ['H = 2ab/(a + b) = 36/9 = 4. (4.5 is the AM and √18 ≈ 4.24 the GM; AM ≥ GM ≥ HM.)'], TIP, [S('HM of 2 and 6?', '3')], page=31),
    tf('math12-u1-q17', '1/2, 1/4, 1/6, 1/8, … is a harmonic progression.', True, ['The reciprocals 2, 4, 6, 8 form an AP with d = 2, so the sequence is an HP.'], 'Flip each term and look for a common difference.', [S('Is 1, 1/2, 1/4, 1/8 an HP?', 'No (2⁰, 2¹, 2², 2³ is a GP)')], page=31),
    tf('math12-u1-q18', 'The series 1 + 2 + 4 + 8 + … converges.', False, ['r = 2, so |r| > 1: the terms grow without bound and the sum goes to infinity (diverges).'], 'Converges only if |r| < 1.', [S('Does 1 − 1/3 + 1/9 − … converge?', 'Yes, r = −1/3, S = 3/4')], page=33),
    mcq('math12-u1-q19', 'How many terms of the AP 5, 9, 13, … must be added to get 189?', ['9', '7', '10', '12'], 'A', ['Sₙ = n/2 × (10 + 4(n − 1)) = n(2n + 3) = 189.', '2n² + 3n − 189 = 0 → (n − 9)(2n + 21) = 0 → n = 9.'], 'Set up Sₙ = total and solve the quadratic; reject negative n.', [S('How many terms of 1, 3, 5, … give 64?', '8')], page=14),
    mcq('math12-u1-q20', 'In a GP, a₃ = 12 and a₆ = 96. The first term is', ['3', '6', '2', '4'], 'A', ['a₆/a₃ = r³ = 8, so r = 2.', 'a₃ = a₁r² → 12 = 4a₁ → a₁ = 3.'], 'Divide two terms to get a power of r.', [S('GP with a₂ = 10, a₄ = 40, r > 0: a₁?', '5')], page=22),
    mcq('math12-u1-q21', 'The repeating decimal 0.333… written as a fraction is', ['1/3', '3/10', '33/100', '1/30'], 'A', ['0.3 + 0.03 + 0.003 + … has a₁ = 0.3, r = 0.1: S = 0.3/0.9 = 1/3.'], TIP, [S('0.555… = ?', '5/9')], page=35),
    fill('math12-u1-q22', 'The nth term of an AP is aₙ = a₁ + (n − ____)d.', ['1', 'n', '2', '0'], '1', ['From a₁ to aₙ you add d exactly n − 1 times (a₂ = a₁ + d, a₃ = a₁ + 2d, …).'], 'Test with n = 1: you must get a₁.', page=10),
])
B.ex('math12-u2', [
    mcq('math12-u2-q09', 'The median of 7, 3, 9, 5, 11, 1 is', ['6', '5', '7', '6.5'], 'A', ['Sort: 1, 3, 5, 7, 9, 11. Even number of values → mean of the two middle values: (5 + 7)/2 = 6.'], 'Always sort first.', [S('Median of 2, 9, 4, 7, 5?', '5')], page=82),
    mcq('math12-u2-q10', 'The mode of 4, 6, 4, 8, 6, 4, 9 is', ['4', '6', '8', '5.9'], 'A', ['4 appears three times, more than any other value.'], TIP, [S('Mode of 1, 2, 2, 3, 3, 3?', '3')], page=83),
    mcq('math12-u2-q11', 'The range of 12, 25, 7, 19, 30 is', ['23', '18', '30', '5'], 'A', ['Range = largest − smallest = 30 − 7 = 23.'], TIP, [S('Range of −3, 4, 10?', '13')], page=86),
    mcq('math12-u2-q12', 'In a pie chart of 90 students, 30 prefer football. The football sector angle is', ['120°', '30°', '90°', '33°'], 'A', ['Angle = 30/90 × 360° = 120°.'], TIP, [S('45 of 180 people — angle?', '90°')], page=64),
    mcq('math12-u2-q13', 'The population variance of 2, 4, 6 is', ['8/3', '8', '4', '2'], 'A', ['Mean = 4; squared deviations 4, 0, 4; variance = 8/3 ≈ 2.67.'], 'Variance = mean of the squared deviations.', [S('Variance of 1, 3?', '1')], page=88),
    mcq('math12-u2-q14', 'The standard deviation of 2, 4, 4, 4, 5, 5, 7, 9 is', ['2', '4', '5', '32'], 'A', ['Mean = 40/8 = 5. Squared deviations: 9, 1, 1, 1, 0, 0, 4, 16 (sum 32).', 'Variance = 32/8 = 4, standard deviation = √4 = 2.'], 'Standard deviation is the square root of the variance.', [S('SD of 5, 5, 5?', '0')], page=89),
    mcq('math12-u2-q15', 'A fair die is rolled. P(a number greater than 4) =', ['1/3', '1/2', '2/3', '1/6'], 'A', ['Favourable outcomes {5, 6}: 2 of 6, so P = 2/6 = 1/3.'], TIP, [S('P(prime) on a die?', '1/2')], page=100),
    mcq('math12-u2-q16', 'Two fair dice are rolled. P(sum = 7) =', ['1/6', '7/36', '1/12', '1/36'], 'A', ['36 equally likely pairs; sum 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 pairs. P = 6/36 = 1/6.'], 'List the pairs in a 6 × 6 table.', [S('P(sum = 12)?', '1/36')], page=104),
    mcq('math12-u2-q17', 'In how many ways can the letters of MATH be arranged?', ['24', '16', '12', '4'], 'A', ['4 different letters: 4! = 4 × 3 × 2 × 1 = 24.'], TIP, [S('Arrangements of ABCDE?', '120')], page=110),
    mcq('math12-u2-q18', 'In how many ways can 2 students be chosen from 5 (order does not matter)?', ['10', '20', '25', '5'], 'A', ['C(5, 2) = 5!/(2!·3!) = 10. (20 counts ordered pairs.)'], 'Order matters → permutation; not → combination.', [S('C(6, 3)?', '20')], page=114),
    tf('math12-u2-q19', 'An event can have probability 1.2.', False, ['Every probability satisfies 0 ≤ P(A) ≤ 1.'], TIP, [S('Can P(A) = 0?', 'Yes: an impossible event')], page=96),
    tf('math12-u2-q20', 'A sample is a part (subset) of the population.', True, ['The population is the whole group under study; a sample is the part actually observed.'], TIP, [S('Is the census a sample?', 'No, it studies the whole population')], page=41),
    short('math12-u2-q21', 'If P(A) = 0.35, find P(A′).', '0.65', ['P(A′) = 1 − P(A) = 1 − 0.35 = 0.65.'], TIP, [S('P(A) = 2/7, P(A′)?', '5/7')], page=97),
    mcq('math12-u2-q22', 'Which variable is qualitative (categorical)?', ['Blood type', 'Height', 'Number of siblings', 'Mass'], 'A', ['Blood type is a category (A, B, AB, O), not a number. Height and mass are quantitative continuous; number of siblings is quantitative discrete.'], TIP, [S('Is "colour of car" qualitative?', 'Yes')], page=47),
])
B.ex('math12-u3', [
    mcq('math12-u3-q09', 'The distance between (−2, 1) and (4, 9) is', ['10', '14', '8', '√52'], 'A', ['d = √(6² + 8²) = √100 = 10.'], TIP, [S('Distance (1, 1) to (4, 5)?', '5')], page=127),
    mcq('math12-u3-q10', 'The midpoint of (−3, 7) and (5, −1) is', ['(1, 3)', '(4, 4)', '(2, 6)', '(1, 4)'], 'A', ['((−3 + 5)/2, (7 − 1)/2) = (1, 3).'], TIP, [S('Midpoint of (0, 0) and (6, −4)?', '(3, −2)')], page=128),
    mcq('math12-u3-q11', 'The slope of the line through (1, −2) and (4, 7) is', ['3', '1/3', '−3', '5/3'], 'A', ['m = (7 − (−2))/(4 − 1) = 9/3 = 3.'], 'Rise over run: y-difference over x-difference, same order.', [S('Slope through (0, 1), (2, 5)?', '2')], page=131),
    mcq('math12-u3-q12', 'The line through (2, 3) parallel to y = 4x − 1 is', ['y = 4x − 5', 'y = 4x + 3', 'y = −x/4 + 3.5', 'y = 4x − 11'], 'A', ['Parallel → same slope 4. y − 3 = 4(x − 2) → y = 4x − 5.'], TIP, [S('Through (0, 2) parallel to y = −x?', 'y = −x + 2')], page=138),
    mcq('math12-u3-q13', 'The slope of a line perpendicular to 2x + 3y = 6 is', ['3/2', '−2/3', '2/3', '−3/2'], 'A', ['y = −(2/3)x + 2, slope −2/3. Perpendicular: m₁m₂ = −1, so m₂ = 3/2.'], 'Negative reciprocal.', [S('Perpendicular to y = 5x?', '−1/5')], page=140),
    mcq('math12-u3-q14', 'The centre and radius of x² + y² − 6x + 4y − 12 = 0 are', ['(3, −2), 5', '(−3, 2), 5', '(3, −2), 25', '(6, −4), 12'], 'A', ['(x − 3)² + (y + 2)² = 12 + 9 + 4 = 25.', 'Centre (3, −2), radius 5.'], 'Complete the square in x and in y.', [S('Centre of x² + y² + 2x = 3?', '(−1, 0), r = 2')], page=153),
    mcq('math12-u3-q15', 'The circle with centre (0, 0) passing through (6, 8) is', ['x² + y² = 100', 'x² + y² = 10', 'x² + y² = 14', 'x² + y² = 48'], 'A', ['r = √(36 + 64) = 10, so x² + y² = r² = 100.'], TIP, [S('Centre O through (3, 4)?', 'x² + y² = 25')], page=151),
    mcq('math12-u3-q16', 'A line has slope 1. Its angle of inclination is', ['45°', '30°', '60°', '90°'], 'A', ['m = tan θ → tan θ = 1 → θ = 45°.'], TIP, [S('Slope √3 — angle?', '60°')], page=130),
    mcq('math12-u3-q17', 'The point dividing (1, 2) to (7, 8) internally in the ratio 2 : 1 is', ['(5, 6)', '(3, 4)', '(4, 5)', '(13, 14)'], 'A', ['x = (1·1 + 2·7)/3 = 5, y = (1·2 + 2·8)/3 = 6.'], TIP, [S('Ratio 1 : 1?', '(4, 5)')], page=127),
    tf('math12-u3-q18', 'The lines y = 2x + 1 and y = 2x − 5 are parallel.', True, ['Both have slope 2 and different y-intercepts, so they never meet.'], TIP, [S('Are y = 3x and y = −x/3 perpendicular?', 'Yes, 3 × (−1/3) = −1')], page=138),
    tf('math12-u3-q19', 'The line x = 4 has slope 0.', False, ['x = 4 is vertical; its slope is undefined. The horizontal line y = 4 has slope 0.'], TIP, [S('Slope of y = −2?', '0')], page=132),
    short('math12-u3-q20', 'Find the y-intercept of 3x − 2y = 8.', '−4', ['Put x = 0: −2y = 8 → y = −4 (also y = 1.5x − 4).'], TIP, [S('y-intercept of x + y = 5?', '5')], page=135, accept=['-4']),
    mcq('math12-u3-q21', 'The point (3, 4) lies ____ the circle x² + y² = 16.', ['outside', 'inside', 'on', 'at the centre of'], 'A', ['3² + 4² = 25 > 16, so the point is farther than r = 4 from the centre: outside.'], TIP, [S('(2, 2) and x² + y² = 16?', 'Inside (8 < 16)')], page=152),
    mcq('math12-u3-q22', 'The distance from (1, 2) to the line 3x + 4y − 1 = 0 is', ['2', '10', '5', '1/2'], 'A', ['d = |3·1 + 4·2 − 1|/√(3² + 4²) = 10/5 = 2.'], 'd = |ax₀ + by₀ + c|/√(a² + b²).', [S('Distance from O to 3x + 4y = 10?', '2')], page=146),
])
B.ex('math12-u4', [
    mcq('math12-u4-q09', '|4 3; 2 5| =', ['14', '26', '−14', '7'], 'A', ['ad − bc = 20 − 6 = 14.'], TIP, [S('|1 2; 3 4|?', '−2')], page=168),
    mcq('math12-u4-q10', 'If A = [[1, 2], [3, 4]], then 2A − I =', ['[[1, 4], [6, 7]]', '[[2, 4], [6, 8]]', '[[1, 3], [5, 7]]', '[[0, 4], [6, 6]]'], 'A', ['2A = [[2, 4], [6, 8]]; subtract I = [[1, 0], [0, 1]] → [[1, 4], [6, 7]].'], 'I only changes the diagonal.', [S('A + I for A = [[0, 1], [1, 0]]?', '[[1, 1], [1, 1]]')], page=162),
    mcq('math12-u4-q11', 'A = [[1, 0], [2, 1]], B = [[3, 1], [0, 2]]. AB =', ['[[3, 1], [6, 4]]', '[[3, 0], [0, 2]]', '[[5, 1], [2, 2]]', '[[3, 1], [6, 2]]'], 'A', ['Row 1 · columns: [1·3 + 0·0, 1·1 + 0·2] = [3, 1].', 'Row 2 · columns: [2·3 + 1·0, 2·1 + 1·2] = [6, 4].'], 'Row of A times column of B.', [S('BA?', '[[5, 1], [4, 2]] — different from AB')], page=165),
    mcq('math12-u4-q12', 'The inverse of [[2, 1], [5, 3]] is', ['[[3, −1], [−5, 2]]', '[[3, 1], [5, 2]]', '[[−3, 1], [5, −2]]', '[[2, −5], [−1, 3]]'], 'A', ['det = 6 − 5 = 1. Swap a and d, change the signs of b and c, divide by det: [[3, −1], [−5, 2]].'], 'Check: A·A⁻¹ should give I.', [S('Inverse of [[1, 1], [0, 1]]?', '[[1, −1], [0, 1]]')], page=169),
    mcq('math12-u4-q13', 'For which k is [[k, 4], [2, 2]] singular?', ['4', '2', '8', '−4'], 'A', ['Singular ⇔ det = 0: 2k − 8 = 0 → k = 4.'], TIP, [S('k for [[k, 3], [3, k]] singular?', '±3')], page=169),
    mcq('math12-u4-q14', 'Using determinants, solve 2x + y = 7, x − y = 2.', ['x = 3, y = 1', 'x = 1, y = 3', 'x = 2, y = 3', 'x = 3, y = −1'], 'A', ['D = 2(−1) − 1(1) = −3; Dx = 7(−1) − 1(2) = −9; Dy = 2(2) − 7(1) = −3.', 'x = −9/−3 = 3, y = −3/−3 = 1.'], 'x = Dx/D, y = Dy/D.', [S('x + y = 4, x − y = 2?', 'x = 3, y = 1')], page=170),
    mcq('math12-u4-q15', 'A is 2 × 3 and B is 3 × 4. The order of AB is', ['2 × 4', '3 × 3', '4 × 2', 'AB is not defined'], 'A', ['Inner numbers match (3 = 3), so AB exists; its order is given by the outer numbers: 2 × 4.'], TIP, [S('Is BA defined?', 'No: 3 × 4 times 2 × 3, 4 ≠ 2')], page=164),
    tf('math12-u4-q16', 'For all 2 × 2 matrices, AB = BA.', False, ['Matrix multiplication is not commutative. Example in q11: AB = [[3, 1], [6, 4]] but BA = [[5, 1], [4, 2]].'], TIP, [S('Does AI = IA always?', 'Yes')], page=166),
    tf('math12-u4-q17', 'The transpose of [[1, 2], [3, 4]] is [[1, 3], [2, 4]].', True, ['The transpose turns rows into columns: row 1 (1, 2) becomes column 1.'], TIP, [S('Transpose of [[0, 5], [0, 0]]?', '[[0, 0], [5, 0]]')], page=160),
    short('math12-u4-q18', 'Evaluate |3 −2; 4 1|.', '11', ['ad − bc = 3·1 − (−2)(4) = 3 + 8 = 11.'], 'Watch the double negative.', [S('|2 −1; 1 2|?', '5')], page=168),
    mcq('math12-u4-q19', 'A square matrix whose determinant is 0 is called', ['singular', 'identity', 'symmetric', 'diagonal'], 'A', ['det = 0 means the matrix has no inverse: it is singular. If det ≠ 0 it is non-singular (invertible).'], TIP, [S('Is I singular?', 'No, det I = 1')], page=169),
    mcq('math12-u4-q20', 'If A has order 3 × 2, then its transpose has order', ['2 × 3', '3 × 2', '3 × 3', '2 × 2'], 'A', ['Transposing swaps rows and columns, so 3 × 2 becomes 2 × 3.'], TIP, [S('Transpose of a 1 × 4 row?', '4 × 1 column')], page=160),
    mcq('math12-u4-q21', 'A is 2 × 2 with det A = 5. Then det(3A) =', ['45', '15', '135', '8'], 'A', ['Multiplying a 2 × 2 matrix by 3 multiplies each row by 3, so det(3A) = 3² det A = 9 × 5 = 45.'], TIP, [S('det(2A) if det A = −1?', '−4')], page=168),
    mcq('math12-u4-q22', 'If |x 2; 3 x| = 10, then x =', ['±4', '4 only', '±2', '16'], 'A', ['x² − 6 = 10 → x² = 16 → x = 4 or x = −4.'], TIP, [S('|x 1; 4 x| = 0?', 'x = ±2')], page=168),
])
B.add('math12-u1-l1-4', [worked('math12-u1-xw4', 'Worked example: a term of an HP', 'Find the 8th term of the harmonic progression 1/3, 1/5, 1/7, …', [
    'Step 1: take reciprocals: 3, 5, 7, … is an AP with a₁ = 3 and d = 2.', 'Step 2: 8th term of the AP: 3 + 7 × 2 = 17.', 'Step 3: take the reciprocal again: the 8th term of the HP is 1/17.'], '1/17')])
B.add('math12-u2-l2-1', [text('math12-u2-xt1', 'Sampling methods', [
    'A **census** studies the whole population; a **sample** studies part of it (cheaper and faster). A sample must be **representative**, otherwise the results are **biased**.',
    '**Simple random sampling:** every member has the same chance (lottery method or random numbers). **Systematic sampling:** choose every k-th member from a list after a random start. **Stratified sampling:** divide the population into groups (strata, e.g. grades) and sample from each group in proportion to its size. **Cluster sampling:** randomly choose whole groups (e.g. some schools) and study everyone in them.',
    '**Example:** a school has 300 Grade 9 and 200 Grade 10 students; a stratified sample of 50 takes 30 from Grade 9 and 20 from Grade 10.'])])
B.add('math12-u2-l2-2', [
    text('math12-u2-xt2', 'Frequency distributions', [
        'Raw data are organised in a **frequency distribution table**: each value or class with its **frequency** (how many times it occurs). **Relative frequency** = frequency ÷ total; **cumulative frequency** = running total.',
        'For **grouped data** choose 5–15 classes of equal width: width ≈ (largest − smallest) ÷ number of classes, rounded up. Each class has lower and upper **limits** (e.g. 20–29), **boundaries** (19.5–29.5) and a **class mark** (midpoint 24.5).',
        'Variables are **qualitative** (categories) or **quantitative**: **discrete** (counted, e.g. number of children) or **continuous** (measured, e.g. height).']),
    worked('math12-u2-xw2', 'Worked example: build a frequency table', 'Marks of 12 students: 12, 15, 21, 25, 28, 31, 33, 34, 38, 41, 45, 47. Make a table with classes 10–19, 20–29, 30–39, 40–49.', [
        'Step 1: tally: 10–19: 12, 15 → 2; 20–29: 21, 25, 28 → 3; 30–39: 31, 33, 34, 38 → 4; 40–49: 41, 45, 47 → 3.',
        'Step 2: check the total: 2 + 3 + 4 + 3 = 12 ✔.', 'Step 3: cumulative frequencies: 2, 5, 9, 12. Class marks: 14.5, 24.5, 34.5, 44.5.'], 'f = 2, 3, 4, 3; cf = 2, 5, 9, 12')])
B.add('math12-u2-l2-3', [worked('math12-u2-xw3', 'Worked example: pie chart angles', 'In a survey of 40 families, 10 use firewood, 18 use charcoal, 8 use gas and 4 use electricity for cooking. Find the sector angles.', [
    'Step 1: each family is worth 360° ÷ 40 = 9°.', 'Step 2: firewood 10 × 9° = 90°, charcoal 18 × 9° = 162°, gas 8 × 9° = 72°, electricity 4 × 9° = 36°.',
    'Step 3: check: 90 + 162 + 72 + 36 = 360° ✔.'], '90°, 162°, 72°, 36°')])
B.add('math12-u3-l3-1', [worked('math12-u3-xw1', 'Worked example: external division and the ratio', 'P(4, 5) lies on the segment from A(1, −1) to B(6, 9). In what ratio does P divide AB?', [
    'Step 1: let the ratio be k : 1. Then x = (1·1 + k·6)/(k + 1) = 4.', 'Step 2: 1 + 6k = 4k + 4 → 2k = 3 → k = 3/2, so the ratio is 3 : 2.',
    'Step 3: check y: (2·(−1) + 3·9)/5 = 25/5 = 5 ✔.'], 'AP : PB = 3 : 2')])
B.add('math12-u2-l2-3', [text('math12-u2-xt3', 'Choosing and reading a graph', [
    '**Which graph?** Categories (favourite subject, type of fuel) → bar graph or pie chart (pie chart when you want to show parts of a whole). Grouped numerical data (heights, marks) → histogram or frequency polygon. Change over time (monthly rainfall) → line graph. Running totals, median and quartiles → ogive.',
    '**Drawing a histogram:** mark the class boundaries on the horizontal axis (e.g. 9.5, 19.5, 29.5, …) and frequency on the vertical axis; draw touching bars whose heights are the frequencies. The tallest bar shows the **modal class**.',
    '**Reading an ogive:** for n = 40 values, the median is read at cumulative frequency 20, the lower quartile at 10 and the upper quartile at 30; interquartile range = Q₃ − Q₁.',
    '**Misleading graphs:** a vertical axis that does not start at 0, or bars of unequal width, can make small differences look large — always read the scale.'])])
B.save()
