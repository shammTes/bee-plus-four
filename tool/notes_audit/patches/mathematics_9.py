import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *

B = Book('mathematics_9')
T = 'Practice'

B.set('math9-u4-c01', title='4.1 Representing a quadratic function', body=[
    'A **quadratic function** has the form $$f(x) = ax^2 + bx + c$$ with a ≠ 0. Examples: f(x) = x², f(x) = 2x² − 3x + 1, the area of a square A(s) = s². Not quadratic: f(x) = 3x + 1 (no x² term) or f(x) = x³.',
    'Like any function, a quadratic can be shown **in words, by a formula, by a table of values, or by a graph**. Example in words: "a ball is thrown up; its height after t seconds is 20t − 5t² metres" → h(t) = −5t² + 20t.',
    '**Table of values for f(x) = x² − 4 (step by step):** choose x = −3, −2, −1, 0, 1, 2, 3 → f(x) = 5, 0, −3, −4, −3, 0, 5. Notice the values repeat symmetrically around x = 0 — every quadratic table is symmetric about its axis.',
    '**Identifying a, b and c:** write the function in the order x², x, constant. f(x) = 5 − 2x + 3x² becomes 3x² − 2x + 5, so a = 3, b = −2, c = 5. The constant c is always the y-intercept: f(0) = c.',
    '**Test from a table:** in a quadratic table (equal steps in x) the second differences are constant. For x² − 4: 5, 0, −3, −4 → differences −5, −3, −1 → second differences 2, 2.'])
B.set('math9-u4-c03', title='4.3 Effects of changing a, h and k', body=[
    'Start from the basic parabola **y = x²** (vertex (0, 0), opens up). Changing one number at a time changes the graph in a predictable way.',
    '**Changing a in y = ax²:** a > 1 makes the parabola **narrower** (steeper), 0 < a < 1 makes it **wider**, and a negative a turns it **upside down** (opens downward). Example: y = 3x² is narrower than y = x²; y = ½x² is wider; y = −x² opens down.',
    '**Changing k in y = x² + k:** the whole graph moves **up k units** (k > 0) or **down** (k < 0). y = x² + 3 has vertex (0, 3); y = x² − 2 has vertex (0, −2).',
    '**Changing h in y = (x − h)²:** the graph moves **right h units** when h > 0 and left when h < 0. Careful: y = (x − 2)² moves RIGHT 2 (vertex (2, 0)); y = (x + 2)² moves LEFT 2 (vertex (−2, 0)).',
    '**All together — vertex form y = a(x − h)² + k:** vertex (h, k), axis of symmetry x = h, shape and direction from a. Example: y = −2(x − 1)² + 4 has vertex (1, 4), opens downward, is narrower than y = x², and its maximum value is 4.',
    '**Tip:** "inside the bracket moves sideways the opposite way; outside moves up and down the same way".'])
B.set('math9-u2-c09', body=[
    '**Inverse variation:** y varies inversely as x when **xy = k** (a constant), i.e. y = k/x with k ≠ 0. When x is doubled, y is halved; when x gets larger, y gets smaller.',
    'Example: Nejat rides her bicycle 6 km from home to Semhar Secondary School in Massawa. Her travel time x (hours) and her speed y (km/h) satisfy x·y = 6. If she rides at 12 km/h she needs 6 ÷ 12 = 0.5 h; at 18 km/h she needs 6 ÷ 18 = 1/3 h (20 minutes). Faster speed → shorter time.',
    'The graph of y = 6/x (for x > 0) is a curve that falls from left to right and gets closer and closer to both axes without touching them.',
    '**Finding k:** if y = 4 when x = 3, then k = xy = 12 and y = 12/x; so when x = 6, y = 2.'])
B.set('math9-u6-c05', body=[
    'The **angle of elevation** is the angle between the horizontal line and your line of sight when you look **up** at an object (for example, from the ground up to the top of a tree). The **angle of depression** is the angle between the horizontal and your line of sight when you look **down** (for example, from a cliff down to a boat).',
    'Because the horizontal lines at the observer and at the object are parallel, the angle of depression from A to B equals the angle of elevation from B to A (alternate angles).',
    '**Example:** a rope supporting a flagpole is fixed to the ground 8 m from the foot of the pole and makes an angle of elevation of 60° with the ground. Find the height of the point where the rope is tied and the length of the rope.',
    '**Solution:** the pole, the rope and the ground form a right-angled triangle. Height h is opposite the 60° angle and 8 m is adjacent: tan 60° = h/8, so h = 8 × √3 ≈ 13.9 m. The rope is the hypotenuse: cos 60° = 8/r, so r = 8 ÷ 0.5 = 16 m.'])
B.set('math9-u1-c05', body=['**∪ (union)** looks like a cup or umbrella that collects everything from both sets — think "**or**". **∩ (intersection)** looks like a bridge/pinch that keeps only what is in both — think "**and**".'])
B.sub('write 0x as placeholder when aligning', 'write 0x for a missing power so the columns line up')

def step(id, title, body): return text(id, title, body)

B.add('math9-u1-l1-2', [step('math9-u1-st2', 'Step by step: equal or equivalent?', [
    '**Equal sets (A = B):** exactly the same elements; order and repetition do not matter. {1, 2, 3} = {3, 1, 2} = {1, 1, 2, 3}.',
    '**Equivalent sets (A ↔ B):** the same number of elements, n(A) = n(B), so they can be matched one-to-one. {a, b, c} ↔ {1, 2, 3}.',
    '**How to decide:** Step 1: list both sets without repeats. Step 2: count the elements — different counts → neither equal nor equivalent. Step 3: same count → equivalent; if also the very same elements → equal.',
    'Every pair of equal sets is equivalent, but equivalent sets need not be equal.']),
    check('math9-u1-pc2', 'A = {letters of the word "BOOK"} and B = {K, O, B}. Which statement is true?', ['A and B are equivalent but not equal', 'A and B are equal', 'A has 4 elements', 'A and B are neither equal nor equivalent'], 'B',
          'Listing the letters of "BOOK" without repetition gives A = {B, O, K}. B has exactly the same three elements (order does not matter), so A = B. Equal sets are of course also equivalent.', title=T)])
B.add('math9-u1-l1-3', [step('math9-u1-st3', 'Step by step: subsets', [
    'A ⊆ B (A is a **subset** of B) means every element of A is also in B. A ⊂ B (**proper subset**) means A ⊆ B and B has at least one element that A does not have.',
    'Facts: ∅ ⊆ A for every set A; A ⊆ A for every set A; but A is never a proper subset of itself.',
    '**Counting subsets:** a set with n elements has **2ⁿ subsets** and **2ⁿ − 1 proper subsets**. Example: {a, b} has 2² = 4 subsets: ∅, {a}, {b}, {a, b}; 3 of them are proper.',
    '**Tip:** to list all subsets of {1, 2, 3} systematically, list by size: ∅; {1}, {2}, {3}; {1, 2}, {1, 3}, {2, 3}; {1, 2, 3} — 8 subsets.']),
    check('math9-u1-pc3', 'How many proper subsets does {2, 4, 6, 8} have?', ['15', '16', '8', '4'], 'A',
          'A set with n = 4 elements has 2⁴ = 16 subsets. All except the set itself are proper, so there are 16 − 1 = 15 proper subsets.', title=T)])
B.add('math9-u1-l1-4', [step('math9-u1-st4', 'Step by step: union and intersection', [
    '**A ∪ B** = all elements that are in A **or** B (or both). **A ∩ B** = elements in **both** A and B.',
    'Example: A = {1, 2, 3, 4}, B = {3, 4, 5}. A ∪ B = {1, 2, 3, 4, 5} (write 3 and 4 only once); A ∩ B = {3, 4}.',
    '**Counting formula:** n(A ∪ B) = n(A) + n(B) − n(A ∩ B). The overlap is subtracted once because it was counted twice. Check: 4 + 3 − 2 = 5 ✔.',
    '**Word problem:** in a class of 40, 25 like football, 18 like volleyball and 8 like both. Students who like at least one = 25 + 18 − 8 = 35; students who like neither = 40 − 35 = 5.']),
    check('math9-u1-pc4', 'n(A) = 12, n(B) = 9 and n(A ∪ B) = 17. Find n(A ∩ B).', ['4', '3', '21', '5'], 'A',
          'Use n(A ∪ B) = n(A) + n(B) − n(A ∩ B): 17 = 12 + 9 − n(A ∩ B), so n(A ∩ B) = 21 − 17 = 4.', title=T)])
B.add('math9-u1-l1-5', [step('math9-u1-st5', 'Step by step: complement and difference', [
    'The **universal set U** contains everything under discussion. The **complement** A′ (also written Aᶜ) is everything in U that is **not** in A. The **difference** A − B (also A \\ B) is everything in A that is **not** in B.',
    'Example: U = {1, 2, …, 10}, A = {2, 4, 6, 8, 10}, B = {1, 2, 3, 4}. A′ = {1, 3, 5, 7, 9}; A − B = {6, 8, 10}; B − A = {1, 3}. Note A − B ≠ B − A.',
    'Useful facts: A − B = A ∩ B′; n(A′) = n(U) − n(A); (A′)′ = A.',
    '**De Morgan\'s laws:** (A ∪ B)′ = A′ ∩ B′ and (A ∩ B)′ = A′ ∪ B′.']),
    check('math9-u1-pc5', 'U = {1, 2, 3, 4, 5, 6}, A = {1, 2, 3} and B = {2, 4, 6}. What is (A ∪ B)′?', ['{5}', '{4, 5, 6}', '{1, 3}', '∅'], 'A',
          'A ∪ B = {1, 2, 3, 4, 6}. The only element of U not in it is 5, so (A ∪ B)′ = {5}. Check with De Morgan: A′ ∩ B′ = {4, 5, 6} ∩ {1, 3, 5} = {5} ✔.', title=T)])
B.add('math9-u1-l1-6', [step('math9-u1-st6', 'Step by step: Cartesian product', [
    'The **Cartesian product** A × B is the set of all ordered pairs (a, b) with a ∈ A and b ∈ B. Order matters: (1, x) is not the same as (x, 1).',
    'Example: A = {1, 2}, B = {x, y, z}. A × B = {(1, x), (1, y), (1, z), (2, x), (2, y), (2, z)}. Method: take each element of A in turn and pair it with every element of B.',
    '**Counting:** n(A × B) = n(A) × n(B) = 2 × 3 = 6. In general A × B ≠ B × A (but they have the same number of elements).',
    'A × B can be shown as a grid of points (lattice) — this is the idea behind the coordinate plane ℝ × ℝ.']),
    check('math9-u1-pc6', 'If n(A) = 3 and n(A × B) = 15, how many elements does B have?', ['5', '12', '18', '45'], 'A',
          'n(A × B) = n(A) × n(B), so 15 = 3 × n(B) and n(B) = 5.', title=T)])
B.add('math9-u2-l2-2', [check('math9-u2-pc2', 'Solve 3(x − 2) > 2x + 1.', ['x > 7', 'x > 5', 'x < 7', 'x > 3'], 'A',
    'Expand: 3x − 6 > 2x + 1. Subtract 2x: x − 6 > 1. Add 6: x > 7. No multiplication by a negative number was needed, so the sign stays. Check x = 8: 18 > 17 ✔.', title=T)])
B.add('math9-u2-l2-3', [check('math9-u2-pc3', 'y varies inversely as x, and y = 6 when x = 4. Find y when x = 8.', ['3', '12', '2', '48'], 'A',
    'Inverse variation: xy = k. k = 4 × 6 = 24. When x = 8: y = 24 ÷ 8 = 3. Doubling x halves y. (12 would be direct variation.)', title=T),
    mnemonic('math9-u2-mn3', 'Direct vs inverse: "divide or multiply"', ['**Direct:** y ÷ x stays the same (y = kx) — both go up together.', '**Inverse:** y × x stays the same (y = k/x) — one up, the other down.'])])
B.add('math9-u2-l2-4', [check('math9-u2-pc4', 'Solve |2x − 1| = 5.', ['x = 3 or x = −2', 'x = 3 only', 'x = −3 or x = 2', 'No solution'], 'A',
    'An absolute value equal to 5 means the inside is 5 or −5. Case 1: 2x − 1 = 5 → x = 3. Case 2: 2x − 1 = −5 → x = −2. Check: |5| = 5 ✔ and |−5| = 5 ✔.', title=T)])
B.add('math9-u3-l3-2', [step('math9-u3-st2', 'Step by step: graphing a line and a linear inequality', [
    '**Graph y = 2x − 1:** Step 1: make a small table: x = 0 → y = −1; x = 1 → y = 1; x = 2 → y = 3. Step 2: plot the points. Step 3: draw a straight line through them with a ruler and extend it. (Two points are enough; a third is a check.)',
    '**Quick method:** start at the y-intercept (0, −1), then use the slope 2 = "up 2, right 1" to find more points.',
    '**Graph y < 2x − 1:** Step 1: draw the boundary y = 2x − 1 as a **dashed** line (< or > means the line is not included; ≤ or ≥ uses a solid line). Step 2: test a point not on the line, e.g. (0, 0): 0 < −1 is false. Step 3: shade the side that does **not** contain (0, 0) — here the region below/right of the line.']),
    check('math9-u3-pc2', 'Which point lies in the region y ≥ x + 2?', ['(1, 4)', '(2, 3)', '(0, 1)', '(3, 4)'], 'A',
          'Test each point in y ≥ x + 2: (1, 4): 4 ≥ 3 ✔. (2, 3): 3 ≥ 4 ✘. (0, 1): 1 ≥ 2 ✘. (3, 4): 4 ≥ 5 ✘.', title=T)])
B.add('math9-u3-l3-3', [step('math9-u3-st3', 'Step by step: slope', [
    'The **slope** (gradient) m of a line measures its steepness: $$m = \\frac{\\text{rise}}{\\text{run}} = \\frac{y_2 - y_1}{x_2 - x_1}$$.',
    'Example: through (2, 1) and (5, 7): m = (7 − 1)/(5 − 2) = 6/3 = 2. Keep the same order of points in the top and the bottom.',
    '**Meaning of the sign:** m > 0 rises to the right; m < 0 falls; m = 0 horizontal; vertical lines have undefined slope.',
    '**Parallel and perpendicular:** parallel lines have equal slopes (m₁ = m₂); perpendicular lines have slopes whose product is −1 (m₁ · m₂ = −1), e.g. 2 and −½.']),
    check('math9-u3-pc3', 'A line is perpendicular to y = 3x + 2. What is its slope?', ['−1/3', '3', '−3', '1/3'], 'A',
          'Perpendicular slopes multiply to −1: 3 × m = −1, so m = −1/3 (the negative reciprocal). 3 would give a parallel line.', title=T)])
B.add('math9-u3-l3-4', [step('math9-u3-st4', 'Step by step: intercepts', [
    'The **y-intercept** is where the line crosses the y-axis (x = 0); the **x-intercept** is where it crosses the x-axis (y = 0).',
    'Example: 2x + 3y = 12. y-intercept: put x = 0 → 3y = 12 → y = 4, point (0, 4). x-intercept: put y = 0 → 2x = 12 → x = 6, point (6, 0). Plot both points and join them — a fast way to draw a line.',
    'In y = mx + c the y-intercept is c directly. **Intercept form:** x/a + y/b = 1 has x-intercept a and y-intercept b (here x/6 + y/4 = 1).']),
    check('math9-u3-pc4', 'What is the x-intercept of 3x − 4y = 12?', ['(4, 0)', '(0, −3)', '(−4, 0)', '(3, 0)'], 'A',
          'At the x-intercept y = 0: 3x = 12, so x = 4 → (4, 0). (0, −3) is the y-intercept (x = 0 gives −4y = 12, y = −3).', title=T)])
B.add('math9-u3-l3-5', [check('math9-u3-pc5', 'Solve: 2x + y = 8 and x − y = 1.', ['x = 3, y = 2', 'x = 2, y = 4', 'x = 4, y = 0', 'x = 3, y = −2'], 'A',
    'Add the equations to eliminate y: 3x = 9, so x = 3. Substitute: 2(3) + y = 8 → y = 2. Check in the second: 3 − 2 = 1 ✔.', title=T)])
B.add('math9-u4-l4-2', [step('math9-u4-st2', 'Step by step: graphing y = ax² + bx + c', [
    'Step 1 — **direction:** a > 0 opens up, a < 0 opens down.',
    'Step 2 — **axis and vertex:** x = −b/(2a); put this x into the function to get the y-coordinate of the vertex.',
    'Step 3 — **y-intercept:** (0, c).',
    'Step 4 — **x-intercepts:** solve ax² + bx + c = 0 (if there are real roots).',
    'Step 5 — plot the points, use symmetry about the axis to get mirror points, and draw a smooth U-shape.',
    '**Example y = x² − 4x + 3:** opens up; x = 4/2 = 2, y = 4 − 8 + 3 = −1, vertex (2, −1); y-intercept (0, 3), mirror point (4, 3); roots x = 1 and x = 3.']),
    check('math9-u4-pc2', 'What is the vertex of y = x² + 6x + 5?', ['(−3, −4)', '(3, 32)', '(−3, 4)', '(6, 5)'], 'A',
          'x = −b/(2a) = −6/2 = −3. y = (−3)² + 6(−3) + 5 = 9 − 18 + 5 = −4. Vertex (−3, −4).', title=T)])
B.add('math9-u4-l4-3', [check('math9-u4-pc3', 'Compared with y = x², the graph of y = (x + 3)² − 1 is moved…', ['3 left and 1 down', '3 right and 1 down', '3 left and 1 up', '3 right and 1 up'], 'A',
    'Write it as y = (x − (−3))² + (−1): h = −3 (3 units **left**) and k = −1 (1 unit **down**). The vertex is (−3, −1).', title=T),
    mnemonic('math9-u4-mn3', '"Inside: opposite. Outside: same."', ['Inside the bracket, (x − h) moves the graph sideways the **opposite** way to the sign you see: (x − 2)² → right 2.', 'Outside, + k moves it up/down the **same** way: + 3 → up 3. A minus in front of the whole thing flips it.'])])
B.add('math9-u4-l4-4', [check('math9-u4-pc4', 'How many real roots does 2x² − 4x + 5 = 0 have?', ['None', 'One', 'Two', 'Infinitely many'], 'A',
    'Discriminant D = b² − 4ac = (−4)² − 4(2)(5) = 16 − 40 = −24 < 0, so there are no real roots (the parabola stays above the x-axis).', title=T)])
B.add('math9-u5-l5-2', [check('math9-u5-pc2', 'Simplify log₂ 32 − log₂ 4.', ['3', '28', '8', '5'], 'A',
    'Quotient rule: log₂ 32 − log₂ 4 = log₂(32/4) = log₂ 8 = 3, because 2³ = 8. (Or: 5 − 2 = 3.)', title=T),
    mnemonic('math9-u5-mn2', 'Log laws: "times → plus, divide → minus, power → front"', ['log(MN) = log M + log N; log(M/N) = log M − log N; log Mᵏ = k log M.', 'There is **no** law for log(M + N).'])])
B.add('math9-u6-l6-2', [check('math9-u6-pc2', 'A ladder 13 m long reaches a window 12 m above the ground. How far is the foot of the ladder from the wall?', ['5 m', '1 m', '25 m', '√313 m'], 'A',
    'The ladder is the hypotenuse: d² + 12² = 13², d² = 169 − 144 = 25, d = 5 m. (5, 12, 13) is a Pythagorean triple.', title=T),
    step('math9-u6-st2', 'Step by step: word problems with Pythagoras', [
        'Step 1: draw a sketch and mark the right angle. Step 2: label the hypotenuse c (opposite the right angle). Step 3: write a² + b² = c². Step 4: substitute and solve — to find a leg, subtract: a² = c² − b². Step 5: check the answer is reasonable (the hypotenuse must be the longest side).',
        'Common situations: ladders against walls, diagonals of rectangles and TV screens, distances on a grid (walk east then north), heights of isosceles triangles.'])])
B.add('math9-u6-l6-3', [check('math9-u6-pc3', 'From the top of a 30 m cliff, the angle of depression of a boat is 30°. How far is the boat from the foot of the cliff?', ['30√3 m ≈ 52 m', '15 m', '60 m', '10√3 m ≈ 17 m'], 'A',
    'The angle of elevation from the boat to the top equals the angle of depression (30°). tan 30° = 30/d, so d = 30/tan 30° = 30 × √3 ≈ 52 m.', title=T)])
B.add('math9-u7-l7-2', [check('math9-u7-pc2', 'A salesperson earns a basic salary of 2000 Nakfa plus 5% commission on sales. Sales this month were 30 000 Nakfa. What is the total pay?', ['3500 Nakfa', '1500 Nakfa', '2150 Nakfa', '32 000 Nakfa'], 'A',
    'Commission = 5% × 30 000 = 1500 Nakfa. Total pay = 2000 + 1500 = 3500 Nakfa.', title=T)])
B.add('math9-u7-l7-3', [step('math9-u7-st3', 'Step by step: profit and loss', [
    '**Cost price (CP)** is what the seller paid; **selling price (SP)** is what the buyer pays. SP > CP → profit = SP − CP. SP < CP → loss = CP − SP.',
    '**Percentages are on the cost price:** profit % = profit/CP × 100%; loss % = loss/CP × 100%.',
    'Example: a trader buys a goat for 1600 Nakfa and sells it for 2000 Nakfa. Profit = 400; profit % = 400/1600 × 100% = 25%.',
    '**Finding SP from a percentage:** SP = CP × (1 + p%) for a profit, CP × (1 − p%) for a loss. **Finding CP:** CP = SP ÷ (1 + p%). Example: sold for 1150 Nakfa at 15% profit → CP = 1150 ÷ 1.15 = 1000 Nakfa.']),
    check('math9-u7-pc3', 'A bicycle bought for 2500 Nakfa is sold at a loss of 12%. What is the selling price?', ['2200 Nakfa', '2800 Nakfa', '2488 Nakfa', '300 Nakfa'], 'A',
          'Loss = 12% of 2500 = 300 Nakfa. SP = 2500 − 300 = 2200 Nakfa (or 2500 × 0.88).', title=T)])
B.add('math9-u7-l7-4', [check('math9-u7-pc4', 'How much simple interest does 4000 Nakfa earn in 3 years at 6% per year?', ['720 Nakfa', '240 Nakfa', '7200 Nakfa', '4720 Nakfa'], 'A',
    'I = P × r × t = 4000 × 0.06 × 3 = 720 Nakfa. (4720 Nakfa is the amount A = P + I, not the interest.)', title=T),
    mnemonic('math9-u7-mn4', 'I = PRT: "I Pay Real Taxes"', ['**I**nterest = **P**rincipal × **R**ate (as a decimal) × **T**ime (in years).', 'Amount A = P + I.'],
             letters=[('I', 'Interest', 'what you earn or pay'), ('P', 'Principal', 'the money borrowed or saved'), ('R', 'Rate', 'per year, as a decimal'), ('T', 'Time', 'in years')])])
B.add('math9-u8-l8-2', [check('math9-u8-pc2', 'Simplify (2x + 3)(x − 4).', ['2x² − 5x − 12', '2x² − 12', '2x² + 5x − 12', '2x² − 8x − 12'], 'A',
    'Multiply each term: 2x·x = 2x², 2x·(−4) = −8x, 3·x = 3x, 3·(−4) = −12. Collect: 2x² − 5x − 12.', title=T)])
B.add('math9-u8-l8-3', [step('math9-u8-st3', 'Step by step: sketching a polynomial graph', [
    'Step 1 — **end behaviour** from the leading term: even degree with positive leading coefficient → both ends up; odd degree with positive leading coefficient → left end down, right end up (reverse both if the leading coefficient is negative).',
    'Step 2 — **y-intercept:** the constant term.',
    'Step 3 — **zeros:** factor and solve f(x) = 0; mark them on the x-axis.',
    'Step 4 — a few **test values** between the zeros to see whether the graph is above or below the axis.',
    '**Example f(x) = x(x − 2)(x + 1) = x³ − x² − 2x:** odd degree, positive leading coefficient; y-intercept 0; zeros −1, 0, 2; f(−0.5) = 0.625 > 0 and f(1) = −2 < 0. The graph comes up from the bottom left, crosses at −1, turns, crosses at 0, dips, and crosses at 2 going up.']),
    check('math9-u8-pc3', 'Which describes the ends of the graph of f(x) = −2x⁴ + x?', ['Both ends go down', 'Both ends go up', 'Left up, right down', 'Left down, right up'], 'A',
          'The leading term −2x⁴ has even degree (both ends the same way) and a negative coefficient (down). So both ends go down.', title=T)])
# ---- thin lessons: lesson-specific notes + worked examples
B.add('math9-u1-l1-2', [
    text('math9-u1-xt2', 'Equal vs equivalent — with examples', [
        '**Equal sets** have exactly the same elements: {2, 4, 6} = {6, 2, 4} = {x : x is an even number, 0 < x < 8}. **Equivalent sets** (A ~ B) only need the same number of elements, n(A) = n(B), so their elements can be matched one-to-one.',
        '{a, b, c} and {1, 2, 3} are equivalent but not equal. Every pair of equal sets is equivalent, but not every pair of equivalent sets is equal.',
        '**Finite and infinite sets:** {1, 2, …, 100} is finite (n = 100); the set of natural numbers {1, 2, 3, …} is infinite. The empty set ∅ = { } has n(∅) = 0, and {0} is NOT empty (it has one element).']),
    worked('math9-u1-xw2', 'Worked example: equal or equivalent?', 'A = {x : x is a letter of the word "LEVEL"}, B = {E, V, L}, C = {1, 2, 3}. Compare the sets.', [
        'Step 1: list A without repeats: A = {L, E, V}.', 'Step 2: A and B contain exactly the same letters, so A = B.',
        'Step 3: n(A) = 3 = n(C), so A ~ C (equivalent), but A ≠ C because the elements are different.'], 'A = B; A and C are equivalent, not equal.')])
B.add('math9-u2-l2-2', [
    text('math9-u2-xt2', 'Solving equations and inequalities — the rules', [
        '**Linear equation:** do the same operation to both sides until x is alone. Example: 5x − 7 = 2x + 8 → 3x = 15 → x = 5. Check: 5(5) − 7 = 18 = 2(5) + 8 ✔.',
        '**Equations with fractions:** multiply every term by the LCD first. (x/3) + (x/4) = 7 → 4x + 3x = 84 → x = 12.',
        '**Absolute value:** |x − 2| = 5 means x − 2 = 5 or x − 2 = −5, so x = 7 or x = −3. (|x| = −1 has no solution.)',
        '**Linear inequality:** same steps as an equation, BUT when you multiply or divide by a negative number, reverse the sign. −3x < 12 → x > −4. Show the answer on a number line (open circle for < or >, filled circle for ≤ or ≥) or in interval notation, e.g. (−4, ∞).']),
    worked('math9-u2-xw2', 'Worked example: an inequality with a sign flip', 'Solve 4 − 2(x + 3) ≥ 6 and write the solution in interval notation.', [
        'Step 1: expand: 4 − 2x − 6 ≥ 6 → −2x − 2 ≥ 6.', 'Step 2: add 2: −2x ≥ 8.', 'Step 3: divide by −2 and REVERSE the sign: x ≤ −4.',
        'Step 4: check x = −5: 4 − 2(−2) = 8 ≥ 6 ✔; x = 0: 4 − 6 = −2 ≥ 6 ✘.'], 'x ≤ −4, i.e. (−∞, −4]')])
B.add('math9-u3-l3-2', [
    worked('math9-u3-xw2', 'Worked example: graph a linear inequality', 'Graph y < −x + 3.', [
        'Step 1: draw the boundary line y = −x + 3 (intercepts (0, 3) and (3, 0)) as a DASHED line, because the sign is < (points on the line are not included).',
        'Step 2: test the origin: 0 < −0 + 3 is true.', 'Step 3: shade the side that contains (0, 0) — the region below the line.',
        'Step 4: for ≤ or ≥ you would draw a solid line instead.'], 'Dashed line y = −x + 3, shade below (the side containing the origin).')])
B.add('math9-u4-l4-2', [
    worked('math9-u4-xw2', 'Worked example: sketch y = x² − 4x + 3', 'Find the direction, vertex, intercepts and axis of y = x² − 4x + 3, then sketch.', [
        'Step 1: a = 1 > 0, so it opens upward.', 'Step 2: axis x = −b/(2a) = 4/2 = 2; vertex y = 4 − 8 + 3 = −1, so the vertex is (2, −1) (minimum).',
        'Step 3: y-intercept (x = 0): 3. x-intercepts: x² − 4x + 3 = (x − 1)(x − 3) = 0 → x = 1 and x = 3.',
        'Step 4: plot (1, 0), (3, 0), (0, 3), its mirror image (4, 3) and the vertex (2, −1); join with a smooth U-shaped curve.'], 'Vertex (2, −1), axis x = 2, x-intercepts 1 and 3, y-intercept 3; range y ≥ −1')])
B.add('math9-u4-l4-4', [
    worked('math9-u4-xw4', 'Worked example: the quadratic formula', 'Solve 2x² − 3x − 4 = 0 (give answers to 2 decimal places).', [
        'Step 1: a = 2, b = −3, c = −4. Discriminant Δ = b² − 4ac = 9 + 32 = 41 > 0, so there are two real roots.',
        'Step 2: x = (3 ± √41)/4.', 'Step 3: √41 ≈ 6.403, so x ≈ (3 + 6.403)/4 ≈ 2.35 or x ≈ (3 − 6.403)/4 ≈ −0.85.'], 'x ≈ 2.35 or x ≈ −0.85')])
B.add('math9-u5-l5-2', [
    text('math9-u5-xt2', 'Logarithms in practice', [
        '**Definition:** log_b a = c means b^c = a (b > 0, b ≠ 1, a > 0). log₂ 8 = 3 because 2³ = 8; log₁₀ 0.01 = −2 because 10⁻² = 0.01; log_b 1 = 0 and log_b b = 1.',
        '**Common logarithms** use base 10 (written log x). Write the number in scientific notation: 3 450 = 3.45 × 10³, so log 3450 = 3 + log 3.45 ≈ 3 + 0.5378 = 3.5378. The whole-number part (3) is the **characteristic**, the decimal part (0.5378, from the table) is the **mantissa**.',
        '**Antilogarithm:** if log x = 2.5378 then x = 10^2.5378 = 3.45 × 10² = 345.']),
    worked('math9-u5-xw2', 'Worked example: using the laws of logarithms', 'Given log 2 ≈ 0.3010 and log 3 ≈ 0.4771, find log 12 and log 1.5.', [
        'Step 1: 12 = 2² × 3, so log 12 = 2 log 2 + log 3 = 0.6020 + 0.4771 = 1.0791.',
        'Step 2: 1.5 = 3/2, so log 1.5 = log 3 − log 2 = 0.4771 − 0.3010 = 0.1761.'], 'log 12 ≈ 1.0791, log 1.5 ≈ 0.1761')])
B.add('math9-u6-l6-1', [
    text('math9-u6-xt1', 'Pythagoras’ theorem and its converse', [
        'In a right-angled triangle with legs a, b and hypotenuse c (the side opposite the right angle, always the longest): **a² + b² = c²**.',
        '**Finding a leg:** a = √(c² − b²). Example: hypotenuse 13, leg 5 → other leg √(169 − 25) = √144 = 12.',
        '**Converse:** if a² + b² = c² for the sides of a triangle, the triangle is right-angled (the right angle is opposite c). If a² + b² > c² the largest angle is acute; if a² + b² < c² it is obtuse.',
        '**Pythagorean triples:** 3-4-5, 5-12-13, 8-15-17, 7-24-25 and their multiples (6-8-10, 9-12-15).'])])
B.add('math9-u6-l6-2', [
    worked('math9-u6-xw2', 'Worked example: a ladder problem', 'A 5 m ladder leans against a wall. Its foot is 1.4 m from the wall. How high up the wall does it reach?', [
        'Step 1: sketch — the wall and ground form the right angle; the ladder (5 m) is the hypotenuse.', 'Step 2: h² + 1.4² = 5² → h² = 25 − 1.96 = 23.04.',
        'Step 3: h = √23.04 = 4.8 m.'], '4.8 m')])
B.add('math9-u7-l7-2', [
    text('math9-u7-xt2', 'Commission and brokerage — formulas', [
        '**Commission** is money paid to a salesperson as a percentage of the value of sales: commission = rate × sales. 5% commission on 40 000 Nakfa of sales = 0.05 × 40 000 = 2 000 Nakfa.',
        'Some workers get a **basic salary plus commission**: total = salary + rate × sales.',
        '**Brokerage** is the fee paid to a broker (agent) who arranges a sale or purchase between a buyer and a seller, usually a percentage of the price: brokerage = rate × price. For a 600 000 Nakfa house at 1.5%, brokerage = 9 000 Nakfa.',
        '**Finding the rate:** rate = commission ÷ sales × 100%. **Finding the sales:** sales = commission ÷ rate.']),
    worked('math9-u7-xw2', 'Worked example: salary plus commission', 'Senait earns a basic salary of 3 000 Nakfa per month plus 4% commission on sales above 20 000 Nakfa. In March she sold goods worth 65 000 Nakfa. Find her total pay.', [
        'Step 1: sales above 20 000 = 65 000 − 20 000 = 45 000 Nakfa.', 'Step 2: commission = 4% of 45 000 = 0.04 × 45 000 = 1 800 Nakfa.',
        'Step 3: total pay = 3 000 + 1 800 = 4 800 Nakfa.'], '4 800 Nakfa')])
B.add('math9-u8-l8-2', [
    text('math9-u8-xt2', 'The four operations on polynomials', [
        '**Add/subtract:** combine like terms (same variable, same power). (3x² − 2x + 5) − (x² + 4x − 1) = 3x² − 2x + 5 − x² − 4x + 1 = 2x² − 6x + 6. Change every sign in the bracket after a minus.',
        '**Multiply:** multiply every term of the first polynomial by every term of the second, then collect like terms: (x + 3)(2x − 1) = 2x² − x + 6x − 3 = 2x² + 5x − 3. Special products: (a + b)² = a² + 2ab + b², (a − b)² = a² − 2ab + b², (a + b)(a − b) = a² − b².',
        '**Divide:** long division as with numbers — divide the leading terms, multiply back, subtract, bring down. Dividend = divisor × quotient + remainder.']),
    worked('math9-u8-xw2', 'Worked example: long division', 'Divide x² + 5x + 7 by x + 2.', [
        'Step 1: x² ÷ x = x. Multiply x(x + 2) = x² + 2x and subtract: (x² + 5x) − (x² + 2x) = 3x. Bring down +7: 3x + 7.',
        'Step 2: 3x ÷ x = 3. Multiply 3(x + 2) = 3x + 6 and subtract: 7 − 6 = 1.',
        'Step 3: quotient x + 3, remainder 1. Check: (x + 2)(x + 3) + 1 = x² + 5x + 6 + 1 ✔.'], 'x² + 5x + 7 = (x + 2)(x + 3) + 1')])
B.save()
