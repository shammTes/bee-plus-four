import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *

B = Book('mathematics_10')
T = 'Practice'
B.sub('(Textbook formula P = 2nr sin(180°/n) = 2·6·5·sin 30° = 30.)', '(Formula for a regular n-gon inscribed in a circle of radius r: P = 2nr sin(180°/n) = 2·6·5·sin 30° = 30.)')
B.set('math10-u4-c05', body=[
    'A **net** is a flat pattern that folds up into a solid. A cube has 6 square faces, so every net of a cube is made of 6 squares joined edge to edge — there are 11 different cube nets (for example a "cross" of 4 squares in a row with one square above and one below the second square). A regular tetrahedron has 4 equilateral-triangle faces; its common net is one large triangle divided into 4 smaller triangles.',
    'Solids are also drawn by their **views**: the **front view**, **side view** and **top view (plan)**. A cylinder standing upright has a rectangle as front view and a circle as top view; a square pyramid has a triangle as front view and a square with its diagonals as top view.'])
B.set('math10-u5-c10', body=[
    '**Prism:** two congruent parallel bases joined by rectangular faces. Volume V = (area of base) × (height of the prism). Total surface area = 2 × (area of base) + (perimeter of base) × (height).',
    '**Example — right triangular prism:** the bases are right-angled triangles with legs 3 cm and 4 cm (hypotenuse 5 cm), and the prism is 10 cm long. Base area = ½ × 3 × 4 = 6 cm². Volume = 6 × 10 = 60 cm³. Lateral area = (3 + 4 + 5) × 10 = 120 cm². Total surface area = 2 × 6 + 120 = 132 cm².'])

# 1.2 inverses
B.add('math10-u1-l1-2', [
    worked('math10-u1-wk2', 'Worked example: find and check an inverse', 'Find the inverse of f(x) = (3x − 2)/5 and check it.', [
        'Step 1: write y = (3x − 2)/5.', 'Step 2: swap x and y: x = (3y − 2)/5.', 'Step 3: solve for y: 5x = 3y − 2 → 3y = 5x + 2 → y = (5x + 2)/3.',
        'Step 4: rename: f⁻¹(x) = (5x + 2)/3.', 'Step 5: check with a number: f(4) = (12 − 2)/5 = 2 and f⁻¹(2) = (10 + 2)/3 = 4 ✔.'], 'f⁻¹(x) = (5x + 2)/3'),
    check('math10-u1-pc21', 'Which function has an inverse that is also a function on all real numbers?', ['f(x) = 2x − 7', 'f(x) = x²', 'f(x) = |x|', 'f(x) = 5'], 'A',
          'Only one-to-one functions have inverse functions. 2x − 7 is a non-horizontal straight line, so it passes the horizontal-line test. x² and |x| give the same output for x and −x, and the constant 5 gives the same output for every x.', title=T),
    check('math10-u1-pc22', 'If f(x) = 4x + 1, what is f⁻¹(9)?', ['2', '37', '1/37', '9/4'], 'A',
          'f⁻¹(9) is the input that f sends to 9: 4x + 1 = 9 → x = 2. (37 is f(9), the wrong direction.)', title=T),
    check('math10-u1-pc23', 'The point (3, −1) is on the graph of a one-to-one function f. Which point must be on the graph of f⁻¹?', ['(−1, 3)', '(3, 1)', '(−3, 1)', '(1, −3)'], 'A',
          'The inverse swaps the coordinates of every point: (a, b) on f becomes (b, a) on f⁻¹. So (3, −1) → (−1, 3). Geometrically this is the reflection in y = x.', title=T)])

# 2.2 attributes of figures
B.set('math10-u2-c02', title='2.2 Attributes of geometric figures', body=[
    'Geometric figures are described by their **attributes** (properties): number of sides, lengths of sides, sizes of angles, parallel sides, diagonals and symmetry. Knowing the attributes lets you classify a figure and reason about it.',
    '**Basic figures:** a **segment** AB has two endpoints; a **ray** AB starts at A and goes on through B; a **line** goes on in both directions. **Collinear** points lie on one line; **coplanar** points lie in one plane. The **midpoint** of AB divides it into two equal parts.',
    '**Angles:** acute (< 90°), right (= 90°), obtuse (between 90° and 180°), straight (180°), reflex (> 180°). **Complementary** angles add to 90°; **supplementary** angles add to 180°; **vertically opposite** angles are equal.',
    '**Triangles** by sides: scalene (no equal sides), isosceles (two equal sides, base angles equal), equilateral (three equal sides, each angle 60°). By angles: acute, right, obtuse.',
    '**Quadrilaterals:** parallelogram (both pairs of opposite sides parallel and equal, opposite angles equal, diagonals bisect each other); rectangle (parallelogram with right angles, equal diagonals); rhombus (parallelogram with all sides equal, diagonals perpendicular); square (rectangle and rhombus together); trapezium (exactly one pair of parallel sides); kite (two pairs of equal adjacent sides).',
    '**Constructions with compass and straightedge:** to copy segment PQ, open the compass to the length PQ, put the point on a new point P′ and draw an arc; mark Q′ on a ray from P′ where the arc cuts it. P′Q′ = PQ. The same idea is used to bisect segments and angles.'])
B.add('math10-u2-l2-2', [
    worked('math10-u2-wk2', 'Worked example: using attributes', 'In parallelogram ABCD, ∠A = 3x + 10 and ∠B = 2x + 20. Find all four angles.', [
        'Step 1: consecutive angles of a parallelogram are co-interior angles between parallel sides, so ∠A + ∠B = 180°.', 'Step 2: 3x + 10 + 2x + 20 = 180 → 5x = 150 → x = 30.',
        'Step 3: ∠A = 100°, ∠B = 80°.', 'Step 4: opposite angles are equal: ∠C = ∠A = 100°, ∠D = ∠B = 80°. Check: 100 + 80 + 100 + 80 = 360° ✔.'], '∠A = ∠C = 100°, ∠B = ∠D = 80°'),
    check('math10-u2-pc21', 'Which quadrilateral always has diagonals that are equal AND perpendicular?', ['Square', 'Rectangle', 'Rhombus', 'Parallelogram'], 'A',
          'A rectangle has equal diagonals; a rhombus has perpendicular diagonals; only the square (which is both a rectangle and a rhombus) always has both properties.', title=T),
    check('math10-u2-pc22', 'Two angles are supplementary and one is 4 times the other. What is the smaller angle?', ['36°', '18°', '45°', '72°'], 'A',
          'x + 4x = 180°, so 5x = 180° and x = 36° (the other is 144°). 18° would be for complementary angles (sum 90°).', title=T),
    check('math10-u2-pc23', 'An isosceles triangle has a vertex angle of 40°. What is each base angle?', ['70°', '40°', '140°', '50°'], 'A',
          'The base angles are equal and the angles sum to 180°: 2b + 40° = 180°, so b = 70°.', title=T)])

# 2.3 conjectures
B.set('math10-u2-c03', title='2.3 Conjectures and counter-examples', body=[
    'A **conjecture** is a statement that you believe is true because of a pattern you observed, but that has not yet been proved. Making conjectures from examples is called **inductive reasoning**.',
    '**Example of forming a conjecture:** draw two intersecting lines and measure the four angles. Whatever lines you draw, the opposite angles are equal. Conjecture: "vertically opposite angles are equal." It is later proved (each one plus the same adjacent angle makes 180°), so it becomes a theorem.',
    '**Testing a conjecture:** try many different cases, including unusual ones (negative numbers, 0, 1, very large numbers, special shapes).',
    '**Counter-example:** one example that makes a conjecture false. Conjecture: "the sum of two prime numbers is even." Counter-example: 2 + 3 = 5, which is odd. One counter-example is enough to disprove a conjecture, but no number of examples can prove it — a proof is needed.',
    '**Number pattern example:** 1 = 1², 1 + 3 = 2², 1 + 3 + 5 = 3², 1 + 3 + 5 + 7 = 4². Conjecture: the sum of the first n odd numbers is n². (It is true and can be proved.)'])
B.add('math10-u2-l2-3', [
    worked('math10-u2-wk3', 'Worked example: disprove with a counter-example', 'Conjecture: "For every whole number n, n² + n + 41 is a prime number." Is it true?', [
        'Step 1: test small values: n = 0 → 41, n = 1 → 43, n = 2 → 47 — all prime. The pattern looks convincing.',
        'Step 2: try a clever value: n = 41 gives 41² + 41 + 41 = 41(41 + 1 + 1) = 41 × 43.',
        'Step 3: 41 × 43 = 1763 has factors 41 and 43, so it is not prime.', 'Step 4: one counter-example disproves the conjecture.'], 'False: n = 41 gives 1763 = 41 × 43.'),
    check('math10-u2-pc31', 'Which is a counter-example to "If a number is divisible by 2, it is divisible by 4"?', ['6', '8', '12', '7'], 'A',
          'A counter-example must make the "if" part true and the "then" part false. 6 is divisible by 2 but not by 4. 8 and 12 satisfy both parts; 7 does not satisfy the "if" part.', title=T),
    check('math10-u2-pc32', 'Reaching a general conclusion from observed examples is called…', ['inductive reasoning', 'deductive reasoning', 'an axiom', 'a definition'], 'A',
          'Inductive reasoning goes from examples to a general conjecture. Deductive reasoning goes from accepted statements to a certain conclusion (a proof).', title=T),
    check('math10-u2-pc33', 'How many examples are needed to show that a conjecture is false?', ['One counter-example', 'At least ten examples', 'A formal proof only', 'It can never be shown'], 'A',
          'A general statement claims something for every case, so a single case where it fails is enough to disprove it.', title=T)])

# 2.4 proofs
B.set('math10-u2-c06', title='2.4 Understanding mathematical proofs', body=[
    '**Deductive reasoning** draws a conclusion that must be true from statements already accepted (definitions, axioms/postulates, and previously proved theorems). A **proof** is a chain of such steps, each with a reason.',
    '**Conditional statements:** "If p, then q" (p → q); p is the hypothesis, q the conclusion. The **converse** is q → p, the **inverse** is "not p → not q", the **contrapositive** is "not q → not p". A statement and its contrapositive are always both true or both false; the converse may be false. Example: "If an angle measures 30°, it is acute" is true, but its converse "If an angle is acute, it measures 30°" is false.',
    '**Two-column proof:** list **statements** on the left and **reasons** on the right, starting with the given facts and ending with what was to be proved.',
    '**Example — vertically opposite angles are equal.** Given: lines AB and CD meet at O. Prove: ∠AOC = ∠BOD. 1. ∠AOC + ∠COB = 180° (angles on a straight line AB). 2. ∠COB + ∠BOD = 180° (angles on a straight line CD). 3. ∠AOC + ∠COB = ∠COB + ∠BOD (both equal 180°). 4. ∠AOC = ∠BOD (subtract ∠COB from both sides). ∎',
    '**Indirect proof (proof by contradiction):** assume the opposite of what you want to prove and show that this leads to something impossible.'])
B.add('math10-u2-l2-4', [
    worked('math10-u2-wk4', 'Worked example: a two-column proof', 'Prove that the angles of a triangle add up to 180°.', [
        'Given: triangle ABC. Construction: draw the line through A parallel to BC; mark angles x (left) and y (right) next to ∠A on this line.',
        '1. x = ∠B (alternate angles, parallel lines).', '2. y = ∠C (alternate angles, parallel lines).', '3. x + ∠A + y = 180° (angles on a straight line).',
        '4. Substitute 1 and 2 into 3: ∠B + ∠A + ∠C = 180°. ∎'], '∠A + ∠B + ∠C = 180°'),
    check('math10-u2-pc41', 'What is the contrapositive of "If it rains, the ground is wet"?', ['If the ground is not wet, it did not rain.', 'If the ground is wet, it rained.', 'If it does not rain, the ground is not wet.', 'It rains and the ground is not wet.'], 'A',
          'Contrapositive: swap AND negate both parts: "not q → not p". B is the converse and C the inverse; neither is guaranteed to be true.', title=T),
    check('math10-u2-pc42', 'In a proof, which of these can be used as a reason?', ['A previously proved theorem', 'The diagram looks right', 'It is true in one example', 'The teacher said so in class'], 'A',
          'Valid reasons are given facts, definitions, axioms (postulates) and theorems already proved. Appearance and single examples are not proofs.', title=T),
    check('math10-u2-pc43', 'A proof that starts by assuming the conclusion is false and reaches an impossibility is called…', ['indirect proof (contradiction)', 'a two-column proof', 'inductive reasoning', 'a counter-example'], 'A',
          'This is an indirect proof, or proof by contradiction: the impossible result shows the assumption was wrong, so the conclusion is true.', title=T)])

# 3.2 circle angles
B.add('math10-u3-l3-2', [
    worked('math10-u3-wk2', 'Worked example: angles in a circle', 'O is the centre of a circle. A, B, C, D lie on the circle with ABCD a cyclic quadrilateral. The central angle on the minor arc AC is ∠AOC = 140°, B lies on the major arc and D on the minor arc. Find ∠ABC and ∠ADC.', [
        'Step 1: the angle at the circumference on the same arc is half the central angle. If B is on the major arc, ∠ABC = ½ × 140° = 70°.',
        'Step 2: ABCD is cyclic, so opposite angles are supplementary: ∠ADC = 180° − 70° = 110°.',
        'Step 3: check: D is on the minor arc, and its angle uses the reflex central angle 360° − 140° = 220°, half of which is 110° ✔.'], '∠ABC = 70°, ∠ADC = 110°'),
    check('math10-u3-pc21', 'The angle at the centre of a circle on arc PQ is 96°. What is the angle at the circumference on the same arc?', ['48°', '96°', '192°', '84°'], 'A',
          'The angle at the centre is twice the angle at the circumference on the same arc, so the circumference angle is 96° ÷ 2 = 48°.', title=T),
    check('math10-u3-pc22', 'In cyclic quadrilateral PQRS, ∠P = 75°. What is ∠R?', ['105°', '75°', '150°', '15°'], 'A',
          'Opposite angles of a cyclic quadrilateral add up to 180°: ∠R = 180° − 75° = 105°.', title=T),
    check('math10-u3-pc23', 'AB is a diameter and C is any other point on the circle. What is ∠ACB?', ['90°', '180°', '60°', 'It depends on C'], 'A',
          'The angle in a semicircle is a right angle: the central angle on the diameter is 180°, and half of it is 90°, wherever C is.', title=T)])

# 3.3 secants tangents chords
B.set('math10-u3-c11', body=[
    'A **chord** joins two points of a circle; a **secant** is a line that cuts the circle at two points; a **tangent** touches it at exactly one point and is perpendicular to the radius there.',
    '**Two chords intersecting inside** at E (chords AB and CD): AE × EB = CE × ED. Angle between them: ∠AEC = ½(arc AC + arc BD).',
    '**Two secants from an outside point P** (PAB and PCD, with A and C nearer): PA × PB = PC × PD (outer part × whole secant).',
    '**Tangent and secant from P** (tangent PT, secant PAB): PT² = PA × PB.',
    '**Two tangents from P** are equal: PT₁ = PT₂.',
    '**Example:** from P, a secant meets the circle at A and B with PA = 4 cm and AB = 5 cm, so PB = 9 cm. The tangent PT satisfies PT² = 4 × 9 = 36, so PT = 6 cm.'])
B.add('math10-u3-l3-3', [
    worked('math10-u3-wk3', 'Worked example: intersecting chords', 'Chords AB and CD meet at E inside a circle. AE = 6 cm, EB = 4 cm and CE = 3 cm. Find ED and the length of CD.', [
        'Step 1: intersecting chords theorem: AE × EB = CE × ED.', 'Step 2: 6 × 4 = 3 × ED → 24 = 3·ED → ED = 8 cm.', 'Step 3: CD = CE + ED = 3 + 8 = 11 cm.'], 'ED = 8 cm, CD = 11 cm'),
    check('math10-u3-pc31', 'From an external point P, a tangent PT = 8 cm and a secant PAB with PA = 4 cm. Find PB.', ['16 cm', '12 cm', '2 cm', '32 cm'], 'A',
          'Tangent–secant theorem: PT² = PA × PB → 64 = 4 × PB → PB = 16 cm.', title=T),
    check('math10-u3-pc32', 'Two secants from P: PA = 3, PB = 12 and PC = 4. Find PD.', ['9', '16', '1', '36'], 'A',
          'PA × PB = PC × PD → 3 × 12 = 4 × PD → PD = 9.', title=T),
    check('math10-u3-pc33', 'A tangent meets a radius at the point of contact. The angle between them is…', ['90°', '45°', '180°', '60°'], 'A',
          'A tangent is always perpendicular to the radius drawn to the point of contact.', title=T)])

# 4.2 coordinate geometry
B.set('math10-u4-c06', body=[
    'The **x-axis** and **y-axis** meet at the origin O(0, 0) and divide the plane into four **quadrants**: I (+, +), II (−, +), III (−, −), IV (+, −). In the pair (a, b), a is the x-coordinate (abscissa) and b the y-coordinate (ordinate).',
    '**Distance formula:** $$PQ = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$ — Pythagoras on the grid. **Midpoint formula:** $$M = \\left(\\frac{x_1 + x_2}{2}, \\frac{y_1 + y_2}{2}\\right)$$.',
    '**Example:** show that P(−2, 3), Q(3, 8), R(4, 1) form an isosceles triangle. PQ = √(5² + 5²) = √50; QR = √(1² + (−7)²) = √50; PR = √(6² + (−2)²) = √40. Two sides are equal (PQ = QR), so the triangle is isosceles.',
    '**Collinear test:** three points are collinear if the two shorter distances add up to the longest one (or if the slopes between them are equal).'])
B.add('math10-u4-l4-2', [
    worked('math10-u4-wk2', 'Worked example: find an endpoint from the midpoint', 'M(2, −1) is the midpoint of AB and A = (−3, 4). Find B.', [
        'Step 1: x-coordinate: (−3 + x)/2 = 2 → −3 + x = 4 → x = 7.', 'Step 2: y-coordinate: (4 + y)/2 = −1 → 4 + y = −2 → y = −6.', 'Step 3: check: midpoint of (−3, 4) and (7, −6) is (2, −1) ✔.'], 'B = (7, −6)'),
    check('math10-u4-pc21', 'What is the distance between (−1, 2) and (5, 10)?', ['10', '14', '8', '√28'], 'A',
          'd = √((5 − (−1))² + (10 − 2)²) = √(36 + 64) = √100 = 10.', title=T),
    check('math10-u4-pc22', 'In which quadrant is the point (−4, −7)?', ['III', 'II', 'IV', 'I'], 'A',
          'Both coordinates negative → quadrant III (left of the y-axis and below the x-axis).', title=T),
    check('math10-u4-pc23', 'Find the midpoint of (−2, 5) and (6, −1).', ['(2, 2)', '(4, 4)', '(8, −6)', '(2, 3)'], 'A',
          'M = ((−2 + 6)/2, (5 + (−1))/2) = (4/2, 4/2) = (2, 2).', title=T)])

# 4.3 transformations
B.add('math10-u4-l4-3', [
    table('math10-u4-tb3', 'Coordinate rules for transformations', ['Transformation', 'Rule', 'Example: (3, −2) →'], [
        ['Reflection in the x-axis', '(x, y) → (x, −y)', '(3, 2)'], ['Reflection in the y-axis', '(x, y) → (−x, y)', '(−3, −2)'], ['Reflection in y = x', '(x, y) → (y, x)', '(−2, 3)'],
        ['Translation by (a, b)', '(x, y) → (x + a, y + b)', 'by (1, 4): (4, 2)'], ['Dilation, centre O, factor k', '(x, y) → (kx, ky)', 'k = 2: (6, −4)'], ['Rotation 180° about O', '(x, y) → (−x, −y)', '(−3, 2)']]),
    worked('math10-u4-wk3', 'Worked example: translate then reflect', 'Triangle ABC has A(1, 2), B(4, 2), C(1, 5). Translate it by (−3, 1), then reflect the image in the x-axis.', [
        'Step 1: translate (add −3 to x and 1 to y): A′(−2, 3), B′(1, 3), C′(−2, 6).', 'Step 2: reflect in the x-axis (change the sign of y): A″(−2, −3), B″(1, −3), C″(−2, −6).',
        'Step 3: both are isometries, so A″B″C″ is congruent to ABC (AB = 3 and A″B″ = 3 ✔).'], 'A″(−2, −3), B″(1, −3), C″(−2, −6)'),
    check('math10-u4-pc31', 'The point (−5, 2) is reflected in the line y = x. What is the image?', ['(2, −5)', '(5, −2)', '(−2, 5)', '(−5, −2)'], 'A',
          'Reflection in y = x swaps the coordinates: (x, y) → (y, x), so (−5, 2) → (2, −5).', title=T),
    check('math10-u4-pc32', 'A dilation with centre O and factor 3 maps a triangle of area 5 cm² to an image of area…', ['45 cm²', '15 cm²', '8 cm²', '125 cm²'], 'A',
          'Lengths are multiplied by k = 3 and areas by k² = 9: 5 × 9 = 45 cm².', title=T),
    check('math10-u4-pc33', 'Which transformation does NOT always give a congruent image?', ['Dilation', 'Reflection', 'Translation', 'Rotation'], 'A',
          'Reflections, translations and rotations keep all lengths (isometries). A dilation with k ≠ ±1 changes the size, giving a similar but not congruent image.', title=T)])

B.add('math10-u5-l5-2', [check('math10-u5-pc21', 'Find the area of a sector of radius 10 cm with central angle 72° (use π ≈ 3.14).', ['62.8 cm²', '314 cm²', '12.56 cm²', '125.6 cm²'], 'A',
    'Sector area = (θ/360°) × πr² = (72/360) × 3.14 × 100 = 0.2 × 314 = 62.8 cm².', title=T)])
B.add('math10-u5-l5-3', [check('math10-u5-pc31', 'A cone has base radius 3 cm and height 4 cm. What is its volume (in terms of π)?', ['12π cm³', '36π cm³', '15π cm³', '4π cm³'], 'A',
    'V = ⅓πr²h = ⅓ × π × 9 × 4 = 12π cm³. (36π is the cylinder with the same base and height — the cone is one third of it.)', title=T)])
B.add('math10-u1-l1-2', [text('math10-u1-xt2', 'Graphs of a function and its inverse', [
    'The graph of f⁻¹ is the **reflection of the graph of f in the line y = x**: every point (a, b) on f becomes (b, a) on f⁻¹. The domain of f becomes the range of f⁻¹ and vice versa.',
    '**Restricting the domain:** f(x) = x² is not one-to-one on all real numbers, but on x ≥ 0 it is, and its inverse is f⁻¹(x) = √x (domain x ≥ 0).',
    '**Composition check:** f(f⁻¹(x)) = x and f⁻¹(f(x)) = x. Example: f(x) = 2x + 3, f⁻¹(x) = (x − 3)/2: f(f⁻¹(x)) = 2·(x − 3)/2 + 3 = x ✔.'])])
B.add('math10-u5-l5-2', [text('math10-u5-xt2', 'Area formulas to know', [
    'Rectangle A = lw; parallelogram A = bh; triangle A = ½bh; trapezium A = ½(a + b)h; rhombus/kite A = ½d₁d₂; circle A = πr², circumference C = 2πr.',
    '**Sector** with central angle θ: arc length = (θ/360°) × 2πr, area = (θ/360°) × πr². **Segment** area = sector area − triangle area.',
    '**Example:** a rectangle 16 cm × 12 cm is inscribed in a circle. Its diagonal √(16² + 12²) = 20 cm is a diameter, so r = 10 cm. Area of the circle outside the rectangle = π(10)² − 16 × 12 ≈ 314.2 − 192 = 122.2 cm².'])])
B.save()
