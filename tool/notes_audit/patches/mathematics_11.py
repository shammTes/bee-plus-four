import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *

B = Book('mathematics_11')

# ---------------------------------------------------------------- placeholder cards -> real lessons
B.set('math11-u1-c01', title='1.1 Representing a quadratic function', body=[
    'A **quadratic function** is a function of the form $$f(x) = ax^2 + bx + c$$ where a, b, c are real numbers and **a ≠ 0**. The highest power of x is 2, so its degree is 2.',
    'A quadratic function can be represented in four ways: **(1) in words** ("the area of a square of side x plus 3x"), **(2) by an equation** f(x) = x² + 3x, **(3) by a table of values** and **(4) by a graph**, which is always a U-shaped curve called a **parabola**.',
    '**Step by step — making a table and a graph for f(x) = x² − 2x − 3:** Step 1: choose x-values on both sides of the middle, e.g. −2, −1, 0, 1, 2, 3, 4. Step 2: work out f(x): f(−2) = 4 + 4 − 3 = 5, f(−1) = 0, f(0) = −3, f(1) = −4, f(2) = −3, f(3) = 0, f(4) = 5. Step 3: plot the points and join them with a smooth curve (not straight segments).',
    'Reading the table: the y-values are **symmetric** about x = 1 (f(0) = f(2) = −3, f(−1) = f(3) = 0). The middle point (1, −4) is the **vertex** — the lowest point because a = 1 > 0. The line x = 1 is the **axis of symmetry**. The x-intercepts (−1, 0) and (3, 0) are where f(x) = 0, and the y-intercept is (0, c) = (0, −3).',
    'The sign of a decides the shape: **a > 0** → opens upward, has a minimum value; **a < 0** → opens downward, has a maximum value. The bigger |a| is, the narrower the parabola. The **range** depends on the vertex: for f(x) = x² − 2x − 3 the minimum is −4, so the range is y ≥ −4.',
    '**Tip:** In a table of a quadratic, the first differences are not constant but the **second differences are constant** (equal to 2a). For x² − 2x − 3: values 5, 0, −3, −4, −3 → first differences −5, −3, −1, 1 → second differences 2, 2, 2. This is a quick test that a table comes from a quadratic.'])

B.set('math11-u1-c02', title='1.2 Solving quadratic equations and inequalities', body=[
    'A **quadratic equation** is ax² + bx + c = 0 (a ≠ 0). Its solutions are called **roots** or **zeros**; they are the x-intercepts of y = ax² + bx + c. There are three standard methods.',
    '**Method 1 — Factorising.** Write the left side as a product and use "if pq = 0 then p = 0 or q = 0". Example: x² − 5x + 6 = 0. Find two numbers with product 6 and sum −5: −2 and −3. So (x − 2)(x − 3) = 0 and x = 2 or x = 3. For a ≠ 1 use the "ac method": 3x² − 10x + 8: ac = 24, numbers −4 and −6: 3x² − 4x − 6x + 8 = x(3x − 4) − 2(3x − 4) = (x − 2)(3x − 4), so x = 2 or x = 4/3.',
    '**Method 2 — Completing the square.** Example: x² + 6x − 7 = 0. Step 1: move the constant: x² + 6x = 7. Step 2: add (half of 6)² = 9 to both sides: x² + 6x + 9 = 16. Step 3: write as a square: (x + 3)² = 16. Step 4: take square roots: x + 3 = ±4, so x = 1 or x = −7.',
    '**Method 3 — The quadratic formula** (works for every quadratic): $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$. The number **D = b² − 4ac** is the **discriminant**: D > 0 → two different real roots; D = 0 → one repeated real root; D < 0 → no real roots (the parabola does not meet the x-axis).',
    '**Simplifying first:** always write the equation in the form ax² + bx + c = 0 and divide by any common factor. Example: 2x² = 8x − 6 → 2x² − 8x + 6 = 0 → x² − 4x + 3 = 0 → (x − 1)(x − 3) = 0.',
    '**Quadratic inequalities** (e.g. x² − x − 12 > 0). Step 1: solve the equation x² − x − 12 = 0: (x − 4)(x + 3) = 0, so x = −3 or x = 4. Step 2: these critical values cut the number line into three intervals: x < −3, −3 < x < 4, x > 4. Step 3: test one number in each: x = −4 gives 8 > 0 ✔; x = 0 gives −12 ✘; x = 5 gives 8 ✔. Step 4: answer x < −3 or x > 4. Picture: the parabola opens upward, so it is above the x-axis outside the roots and below it between them.',
    '**Sum and product of roots:** if r₁ and r₂ are the roots of ax² + bx + c = 0, then r₁ + r₂ = −b/a and r₁r₂ = c/a. Use this to check answers quickly: for x² − 5x + 6 = 0, 2 + 3 = 5 ✔ and 2 × 3 = 6 ✔.'])

B.set('math11-u1-c08', title='1.4 Polynomial functions', body=[
    'A **polynomial function** of degree n is $$f(x) = a_nx^n + a_{n-1}x^{n-1} + \\dots + a_1x + a_0$$ with a_n ≠ 0 and n a whole number. a_n is the **leading coefficient**, a₀ the **constant term** (the y-intercept). Examples: f(x) = 4x³ − x + 2 (degree 3, cubic). Not polynomials: 1/x, √x, 2ˣ.',
    '**Operations.** Add/subtract by collecting like terms; multiply by multiplying every term of one by every term of the other. The degree of a product is the sum of the degrees: (x² + 1)(x³ − 2) has degree 5 and constant term (1)(−2) = −2.',
    '**Division algorithm:** dividing f(x) by d(x) gives a quotient q(x) and remainder r(x): f(x) = d(x)·q(x) + r(x), where r has smaller degree than d. Dividing by (x − c) is fastest with **synthetic division**: write c and the coefficients, bring down the first one, multiply by c, add to the next coefficient, and repeat.',
    '**Remainder Theorem:** when f(x) is divided by (x − c), the remainder is f(c). Example: f(x) = 2x³ − 5x + 1 divided by (x − 2): remainder f(2) = 16 − 10 + 1 = 7.',
    '**Factor Theorem:** (x − c) is a factor of f(x) exactly when f(c) = 0. Example: f(x) = x³ − 4x² + x + 6. f(2) = 8 − 16 + 2 + 6 = 0, so (x − 2) is a factor. Dividing gives x² − 2x − 3 = (x − 3)(x + 1), so f(x) = (x − 2)(x − 3)(x + 1) and the zeros are 2, 3 and −1.',
    '**Rational Root Theorem:** if a polynomial with integer coefficients has a rational zero p/q (in lowest terms), then p divides the constant term and q divides the leading coefficient. So for x³ − 4x² + x + 6 the only possible rational zeros are ±1, ±2, ±3, ±6 — test them with the Factor Theorem.',
    '**Graphs.** A polynomial of degree n has at most n real zeros and at most n − 1 turning points. At a zero of odd multiplicity the graph **crosses** the x-axis; at a zero of even multiplicity (e.g. (x − 1)²) it **touches and turns back**. **End behaviour** depends only on the leading term: even degree → both ends go the same way (up if a_n > 0); odd degree → the ends go opposite ways (left down, right up if a_n > 0).'])

B.set('math11-u2-c01', title='2.1 Graphs of square root functions', body=[
    'The **square root function** is $$f(x) = \\sqrt{x}$$. Because we cannot take the real square root of a negative number, its domain is x ≥ 0, and because √x is never negative, its range is y ≥ 0.',
    '**Table of values (choose perfect squares):** x = 0, 1, 4, 9, 16 gives y = 0, 1, 2, 3, 4. Plot the points and join them with a smooth curve. The graph starts at the origin and rises to the right, getting flatter and flatter — it is the upper half of a parabola lying on its side (x = y², y ≥ 0).',
    '**Transformations of y = a√(x − h) + k:** h moves the graph right (h > 0) or left; k moves it up or down; the starting point (endpoint) moves from (0, 0) to **(h, k)**. If a < 0 the graph is reflected in the horizontal line through the start (it goes down instead of up); |a| > 1 stretches it vertically. y = √(−x) is the reflection in the y-axis: it starts at (0, 0) and goes to the left.',
    '**Step by step — sketch g(x) = √(x − 2) + 1:** Step 1: starting point (h, k) = (2, 1). Step 2: a = 1 > 0, so the curve goes up and to the right. Step 3: a second point: x = 3 gives √1 + 1 = 2, so (3, 2); x = 6 gives √4 + 1 = 3, so (6, 3). Step 4: domain x ≥ 2, range y ≥ 1.',
    '**Tip:** to find the starting point of y = √(bx + c) + k, set the inside equal to zero: bx + c = 0. For y = √(2x − 8) + 3: 2x − 8 = 0 gives x = 4, so the curve starts at (4, 3).'])

B.set('math11-u2-c05', title='2.3 Solving square root (radical) equations', body=[
    'A **radical equation** has the unknown inside a square root, e.g. √(3x + 1) = 4. The method is to isolate the root and square both sides — but squaring can create false answers, so every answer must be checked in the original equation.',
    '**Steps:** (1) Isolate the square root on one side. (2) Square both sides. (3) Solve the resulting linear or quadratic equation. (4) **Check** each answer in the original equation and reject any that do not work (these are called **extraneous** roots).',
    '**Example 1:** √(3x + 1) = 4. Square: 3x + 1 = 16, 3x = 15, x = 5. Check: √16 = 4 ✔.',
    '**Example 2:** √(x + 3) = x − 3. Square: x + 3 = x² − 6x + 9, so x² − 7x + 6 = 0, (x − 1)(x − 6) = 0, x = 1 or x = 6. Check x = 1: √4 = 2 but 1 − 3 = −2 ✘ (extraneous). Check x = 6: √9 = 3 and 6 − 3 = 3 ✔. Solution: x = 6 only.',
    '**Quick rejection:** a square root is never negative, so √(x − 3) = −2 has **no solution** — you can see this before doing any algebra.',
    '**Why false roots appear:** squaring turns both a = b and a = −b into a² = b². In Example 2, x = 1 solves √(x + 3) = −(x − 3), not the equation we were given.'])

B.set('math11-u2-c06', title='2.4 Inverses of square root functions', body=[
    'Two functions are **inverses** when each undoes the other: f(f⁻¹(x)) = x and f⁻¹(f(x)) = x. The graph of f⁻¹ is the reflection of the graph of f in the line y = x, so the domain of f becomes the range of f⁻¹ and the range of f becomes the domain of f⁻¹.',
    '**y = √x and y = x² are inverse partners only when x² is restricted to x ≥ 0.** On all real numbers x² is not one-to-one (2² = (−2)² = 4), so it has no inverse function; on x ≥ 0 it is one-to-one and its inverse is √x.',
    '**Steps to find the inverse of f(x) = √(x − 1), x ≥ 1:** Step 1: write y = √(x − 1) and note the range y ≥ 0. Step 2: swap x and y: x = √(y − 1). Step 3: solve for y: square both sides, x² = y − 1, so y = x² + 1. Step 4: state the domain of the inverse = range of f: f⁻¹(x) = x² + 1, **x ≥ 0**.',
    '**Check:** f(f⁻¹(3)) = f(10) = √9 = 3 ✔.',
    '**Going the other way:** the inverse of g(x) = x² − 4 with x ≥ 0 is g⁻¹(x) = √(x + 4), x ≥ −4. Always restrict the quadratic to one side of its vertex first.'])

B.set('math11-u3-c03', title='3.2 Graphing rational functions', body=[
    'A **rational function** is f(x) = P(x)/Q(x) with P, Q polynomials and Q(x) ≠ 0. Its graph can have breaks: **vertical asymptotes**, **holes**, and it may approach a **horizontal** or **slant (oblique) asymptote** far to the left and right.',
    '**Step-by-step graphing routine:** Step 1 — **Factor** numerator and denominator. Step 2 — **Domain:** exclude the zeros of the denominator. Step 3 — **Holes:** a factor that cancels from top and bottom gives a hole (a missing point), not an asymptote. Step 4 — **Vertical asymptotes:** zeros of the denominator that remain after cancelling. Step 5 — **Horizontal/slant asymptote** from the degrees n (top) and m (bottom): n < m → y = 0; n = m → y = (leading coeff. of P)/(leading coeff. of Q); n = m + 1 → slant asymptote found by long division. Step 6 — **Intercepts:** y-intercept f(0); x-intercepts where the (cancelled) numerator is 0. Step 7 — **Test points** in each interval between asymptotes and zeros, then sketch.',
    '**Example:** f(x) = (2x + 1)/(x − 3). Domain x ≠ 3; vertical asymptote x = 3; degrees equal → horizontal asymptote y = 2/1 = 2; y-intercept f(0) = −1/3; x-intercept 2x + 1 = 0 → x = −1/2. Test x = 4: f = 9 (above y = 2, right of x = 3); x = 0: −1/3 (below). Sketch two branches, one in the upper right and one in the lower left of the crossing asymptotes.',
    '**Hole example:** f(x) = (x² − 4)/(x − 2) = (x − 2)(x + 2)/(x − 2) = x + 2 for x ≠ 2. The graph is the line y = x + 2 with an open circle at (2, 4).',
    '**Basic shape to remember:** y = 1/x has asymptotes x = 0 and y = 0 and two branches in the 1st and 3rd quadrants. y = a/(x − h) + k is the same curve moved so that the asymptotes are x = h and y = k.'])

B.set('math11-u3-c04', title='3.3 Operations on rational expressions', body=[
    'Rational expressions follow the same rules as fractions of numbers. Always **factor first**, and state the values of x that make any denominator zero (they are excluded).',
    '**Simplifying:** factor the top and bottom and cancel common **factors** (never cancel terms that are added). Example: (3x² − 12)/(x² − 5x + 6) = 3(x − 2)(x + 2)/[(x − 2)(x − 3)] = 3(x + 2)/(x − 3), x ≠ 2, 3.',
    '**Multiplying:** multiply tops and bottoms, then cancel. Example: (3x − 3)/x × x²/(x² − 1) = 3(x − 1)/x × x²/[(x − 1)(x + 1)] = 3x/(x + 1), x ≠ 0, ±1.',
    '**Dividing:** multiply by the reciprocal of the second expression. Example: (x + 2)/x ÷ (x² − 4)/x² = (x + 2)/x × x²/[(x − 2)(x + 2)] = x/(x − 2).',
    '**Adding and subtracting:** Step 1: factor the denominators. Step 2: find the LCD (least common denominator). Step 3: rewrite each fraction with the LCD. Step 4: add or subtract the numerators (use brackets when subtracting). Step 5: simplify. Example: 1/x + 1/(x + 1) = (x + 1)/[x(x + 1)] + x/[x(x + 1)] = (2x + 1)/[x(x + 1)].',
    '**Common trap:** (x + 3)/x is NOT 3 — the x in "x + 3" is a term, not a factor, so it cannot be cancelled.'])

B.set('math11-u4-c04', title='4.2 The logarithmic function', body=[
    '**Definition:** for b > 0, b ≠ 1 and x > 0, $$\\log_b x = y \\iff b^y = x$$. A logarithm is an **exponent**: log₂ 8 = 3 because 2³ = 8. log₁₀ x is written log x (common log); logₑ x is written ln x (natural log).',
    'The logarithmic function f(x) = log_b x is the **inverse** of the exponential function g(x) = bˣ. So its graph is the reflection of y = bˣ in the line y = x: **domain x > 0, range all real numbers**, x-intercept (1, 0), and the y-axis is a vertical asymptote. For b > 1 it increases; for 0 < b < 1 it decreases.',
    '**Converting forms (step by step):** log₃ 81 = 4 ⇔ 3⁴ = 81; 5² = 25 ⇔ log₅ 25 = 2. To evaluate log₃ 9, ask "3 to what power gives 9?" → 2.',
    '**Laws of logarithms** (M, N > 0): log_b(MN) = log_b M + log_b N; log_b(M/N) = log_b M − log_b N; log_b(Mᵏ) = k log_b M; log_b b = 1; log_b 1 = 0; change of base: log_b M = log M / log b.',
    '**Domain of a transformed log:** the expression inside must be positive. f(x) = log₃(x − 4) needs x − 4 > 0, so the domain is x > 4 and the vertical asymptote is x = 4.',
    '**Solving log equations:** write in exponential form, then check that the answer keeps every log argument positive. Example: log₂(x − 1) = 3 → x − 1 = 2³ = 8 → x = 9 (check: log₂ 8 = 3 ✔).'])

B.set('math11-u4-c05', title='4.3 Applications of exponential and logarithmic functions', body=[
    '**Growth and decay model:** A = A₀(1 + r)ᵗ for growth at rate r per period, and A = A₀(1 − r)ᵗ for decay. A₀ is the starting amount and t the number of periods.',
    '**Compound interest:** A = P(1 + r/n)ⁿᵗ where n is the number of compounding periods per year. Example: 1000 Nakfa at 10% per year compounded yearly for 2 years: A = 1000 × 1.1² = 1210 Nakfa.',
    '**Population growth:** a town of 20 000 grows by 3% a year. After 5 years: 20 000 × 1.03⁵ ≈ 23 185 people.',
    '**Half-life (radioactive decay):** the amount halves every half-life T: A = A₀(½)^(t/T). Example: 80 g with half-life 5 years, after 15 years: 80 × (½)³ = 10 g.',
    '**Using logs to find the time:** when is 1000 Nakfa at 10% doubled? 1000 × 1.1ᵗ = 2000 → 1.1ᵗ = 2 → t = log 2 / log 1.1 ≈ 0.301/0.0414 ≈ 7.3 years.',
    '**Logarithmic scales:** pH = −log[H⁺] (a solution with [H⁺] = 10⁻³ has pH 3); the Richter scale for earthquakes and the decibel scale for sound are also logarithmic — an increase of 1 on the Richter scale means 10 times the amplitude.'])

B.set('math11-u4-c01', body=[
    'An **exponential function** is f(x) = bˣ with base b > 0, b ≠ 1. The variable is in the exponent. Example: f(x) = 2ˣ gives 1/4, 1/2, 1, 2, 4, 8 for x = −2, −1, 0, 1, 2, 3.',
    '**Graph facts:** domain all real numbers; range y > 0; y-intercept (0, 1); the x-axis (y = 0) is a horizontal asymptote. b > 1 → growth (increasing); 0 < b < 1 → decay (decreasing). y = (½)ˣ is the reflection of y = 2ˣ in the y-axis.',
    '**Laws of exponents:** aᵐ·aⁿ = aᵐ⁺ⁿ; aᵐ ÷ aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐⁿ; a⁰ = 1; a⁻ⁿ = 1/aⁿ; a^(m/n) = ⁿ√(aᵐ).',
    '**Solving exponential equations — same base method:** write both sides as powers of the same base and equate the exponents. Example: 32^(x+1) = 128 → 2^(5x+5) = 2⁷ → 5x + 5 = 7 → x = 2/5. If the bases cannot be matched, take logs of both sides: 3ˣ = 20 → x = log 20 / log 3 ≈ 2.73.',
    'Logarithm laws used with exponentials: log(MN) = log M + log N; log(M/N) = log M − log N; log(Mᵏ) = k log M.'])

B.set('math11-u5-c01', title='5.1 Similar polygons', body=[
    'Two polygons are **similar** (symbol ~) when they have the same shape but not necessarily the same size. Exactly two conditions are needed: **(1) all corresponding angles are equal**, and **(2) all corresponding sides are in the same ratio**. That common ratio k is the **scale factor**.',
    '**Naming matters:** ABCD ~ PQRS means A ↔ P, B ↔ Q, C ↔ R, D ↔ S, so AB/PQ = BC/QR = CD/RS = DA/SP = k.',
    '**Step by step — testing similarity:** Rectangle A is 4 cm × 6 cm, rectangle B is 6 cm × 9 cm. Step 1: angles are all 90°, so they are equal. Step 2: ratios of matching sides: 6/4 = 1.5 and 9/6 = 1.5. Step 3: equal ratios → similar with k = 1.5.',
    '**Both conditions are needed:** a square 2 × 2 and a rhombus with sides 2 and angles 60°/120° have proportional sides but different angles — not similar. A 2 × 2 square and a 2 × 5 rectangle have equal angles but sides not in proportion — not similar.',
    '**Finding a missing side:** if ABC ~ DEF with AB = 6, DE = 9 and AC = 8, then k = 9/6 = 1.5, so DF = 8 × 1.5 = 12.',
    'All squares are similar to each other, and so are all equilateral triangles, all circles and all regular polygons with the same number of sides.'])

B.set('math11-u5-c07', title='5.3 Applications of similar triangles', body=[
    'Similar triangles let us find lengths we cannot measure directly: the height of a tree or building, the width of a river, or a distance on a map.',
    '**Shadows (heights):** at the same time of day the sun\'s rays make equal angles with the ground, so an object and its shadow form a triangle similar to that of any other object. Example: a 2 m pole casts a 3 m shadow and a tree casts an 18 m shadow. height/shadow is the same: h/18 = 2/3, so h = 12 m.',
    '**Right triangle with the altitude to the hypotenuse:** in right triangle ABC (right angle at C) with altitude CD to the hypotenuse AB, the three triangles ABC, ACD and CBD are all similar. This gives the **geometric-mean relations**: CD² = AD × DB, AC² = AD × AB and BC² = BD × AB.',
    '**Geometric mean:** the geometric mean of positive numbers a and b is √(ab) (compare with the arithmetic mean (a + b)/2). For 2 and 8: geometric mean √16 = 4, arithmetic mean 5. Example: if AD = 4 and DB = 9, the altitude is CD = √(4 × 9) = 6.',
    '**Width of a river:** mark points so that two triangles with parallel sides are formed on your side of the river; measure the sides you can reach and use equal ratios to calculate the side across the water.',
    '**Tip:** always write the similarity statement with the matching vertices in order before writing the ratio, then put the unknown in a numerator to make solving easy.'])

B.set('math11-u5-c08', title='5.4 Ratios of perimeters, areas and volumes', body=[
    'If two similar figures have scale factor k (ratio of corresponding lengths = k), then: **ratio of perimeters = k**, **ratio of areas = k²**, and for similar solids **ratio of volumes = k³** (surface areas are also in the ratio k²).',
    '**Why k²?** Area is length × length, so each of the two lengths is multiplied by k: k × k = k². Volume uses three lengths: k³.',
    '**Example 1:** two similar triangles have sides in the ratio 3 : 4. Perimeters 3 : 4; areas 9 : 16. If the smaller area is 27 cm², the larger is 27 × 16/9 = 48 cm².',
    '**Example 2 (backwards):** the areas of two similar polygons are 25 cm² and 64 cm². Ratio of sides = √25 : √64 = 5 : 8.',
    '**Example 3 (solids):** two similar cylinders with scale factor 2 : 3 have volumes in the ratio 8 : 27. If the small one holds 16 litres, the large one holds 16 × 27/8 = 54 litres.',
    '**Map scale:** on a 1 : 50 000 map, 1 cm² represents 50 000² cm² = 25 hectares, because areas scale by k².'])

# ---------------------------------------------------------------- figure references -> self-contained questions
B.set('math11-u5-chkE1', q='Right triangles ABC and DEF are similar, ΔABC ~ ΔDEF (A ↔ D, B ↔ E, C ↔ F). The lengths are $$BC = 3$$, $$EF = 7$$ and $$AC = x$$. Find $$DF = y$$ in terms of $$x$$.')
B.set('math11-u5-chkE2', q='Points T and P lie on one line from S, and Q and R lie on a second line from S, with Q between S and R, so that $$\\Delta STQ \\sim \\Delta SPR$$. If $$TQ = 5$$, $$PR = 15$$ and $$SQ = 4$$, find the length of $$QR$$.')
for cid in ('math11-u5-chk74',):
    B.set(cid, q='In $$\\Delta ABC$$, D lies on AC and E lies on BC with $$DE \\parallel AB$$, so that triangle CDE is a smaller copy of triangle CAB. Given that $$AC = 12$$, $$CD = 4$$ and $$BC = 24$$, find the length of $$CE$$ using the Basic Proportionality Theorem.')
B.set('math11-u5-wrk1', problem='In $$\\Delta ABC$$, D lies on AC and E lies on BC with $$DE \\parallel AB$$, so that triangle CDE is a smaller copy of triangle CAB. Given that $$AC = 12$$, $$CD = 4$$ and $$BC = 24$$, find the length of $$CE$$ using the Basic Proportionality Theorem.', answer='CE = 8')

# ---------------------------------------------------------------- empty / irrelevant cards
for cid in ('math11-u1-c07', 'math11-u2-c04', 'math11-u3-c06', 'math11-u4-c06', 'math11-u5-c06', 'math11-u6-c05', 'math11-u6-c06',
            'math11-u6-wrk-extra1'):
    B.remove(cid)
B.set('math11-u1-c03', title='Polynomials by degree')
B.set('math11-u6-c02', body=['**Partnership:** two or more people put money (capital) into a business and share the profit or loss by agreement — usually in the ratio of capital × time invested.'])

# ---------------------------------------------------------------- one more check (with full reasoning) in every lesson that had only 2
T = 'Practice'
B.add('math11-u1-l1-1', [
    mnemonic('math11-u1-mn1', 'Shape of a parabola: "a decides the face"', ['**a > 0 → smile** (opens up, minimum at the vertex). **a < 0 → frown** (opens down, maximum at the vertex).', 'Vertex x-coordinate: **"minus b over two a"**, x = −b/(2a). Then put it back in to get the y-coordinate.']),
])
B.add('math11-u1-l1-2', [check('math11-u1-pc2', 'Solve $$x^2 - 2x - 8 \\le 0$$.', ['$$x \\le -2$$ or $$x \\ge 4$$', '$$-2 \\le x \\le 4$$', '$$-4 \\le x \\le 2$$', '$$x \\le 4$$'], 'B',
    '**Step 1:** Solve x² − 2x − 8 = 0: (x − 4)(x + 2) = 0, so x = −2 or x = 4.\n**Step 2:** The parabola opens upward (a = 1 > 0), so it is below or on the x-axis between the roots.\n**Step 3:** Test x = 0: −8 ≤ 0 ✔. Answer: −2 ≤ x ≤ 4 (closed ends because of ≤).', title=T)])
B.add('math11-u1-l1-3', [check('math11-u1-pc3', 'What are the vertex and the maximum or minimum value of $$f(x) = -2(x - 1)^2 + 5$$?', ['Vertex (1, 5), maximum value 5', 'Vertex (−1, 5), maximum value 5', 'Vertex (1, 5), minimum value 5', 'Vertex (1, −5), minimum value −5'], 'A',
    'In vertex form a(x − h)² + k the vertex is (h, k) = (1, 5). Since a = −2 < 0 the parabola opens downward, so the vertex is the highest point: the **maximum** value is 5. Option B uses the wrong sign for h.', title=T)])
B.add('math11-u1-l1-4', [check('math11-u1-pc4', 'Which is a factor of $$P(x) = x^3 - 2x^2 - 5x + 6$$?', ['$$x + 1$$', '$$x - 2$$', '$$x - 1$$', '$$x + 3$$'], 'C',
    '**Factor Theorem:** (x − c) is a factor when P(c) = 0.\nP(1) = 1 − 2 − 5 + 6 = 0 ✔, so (x − 1) is a factor.\nCheck the others: P(−1) = −1 − 2 + 5 + 6 = 8, P(2) = 8 − 8 − 10 + 6 = −4, P(−3) = −27 − 18 + 15 + 6 = −24. (In fact P(x) = (x − 1)(x + 2)(x − 3).)', title=T),
    mnemonic('math11-u1-mn4', 'Remainder and factor: "plug in c"', ['To divide by (x − c), **plug in c**: the answer P(c) is the remainder. **Remainder 0 ⇒ factor.**', 'Careful with the sign: dividing by (x + 3) means c = −3.'])])
B.add('math11-u2-l2-2', [check('math11-u2-pc2', 'What are the domain and range of $$f(x) = -\\sqrt{x + 3} + 2$$?', ['Domain x ≥ −3, range y ≤ 2', 'Domain x ≥ 3, range y ≥ 2', 'Domain x ≥ −3, range y ≥ 2', 'Domain x ≤ −3, range y ≤ 2'], 'A',
    '**Domain:** x + 3 ≥ 0, so x ≥ −3.\n**Range:** √(x + 3) ≥ 0, so −√(x + 3) ≤ 0 and adding 2 gives y ≤ 2. The minus sign in front reflects the curve downward from its starting point (−3, 2).', title=T)])
B.add('math11-u2-l2-3', [check('math11-u2-pc3', 'Solve $$\\sqrt{2x + 3} = x$$.', ['x = −1 or x = 3', 'x = 3 only', 'x = −1 only', 'No solution'], 'B',
    '**Square:** 2x + 3 = x², so x² − 2x − 3 = 0, (x − 3)(x + 1) = 0, x = 3 or x = −1.\n**Check x = 3:** √9 = 3 ✔. **Check x = −1:** √1 = 1 but the right side is −1 ✘ (extraneous).\nSo x = 3 only.', title=T),
    remember('math11-u2-rm3', 'Always check', ['Squaring both sides can add false (extraneous) roots. **Substitute every answer into the original equation** and reject those that fail. A square root can never equal a negative number.'])])
B.add('math11-u2-l2-4', [check('math11-u2-pc4', 'Find the inverse of $$f(x) = \\sqrt{x + 2}$$, $$x \\ge -2$$.', ['$$f^{-1}(x) = x^2 - 2$$, x ≥ 0', '$$f^{-1}(x) = x^2 + 2$$, x ≥ 0', '$$f^{-1}(x) = (x - 2)^2$$, x ≥ 2', '$$f^{-1}(x) = \\sqrt{x - 2}$$'], 'A',
    '**Swap and solve:** x = √(y + 2) → x² = y + 2 → y = x² − 2.\n**Domain of the inverse** = range of f = y ≥ 0, so f⁻¹(x) = x² − 2, x ≥ 0.\nCheck: f(f⁻¹(3)) = f(7) = √9 = 3 ✔.', title=T)])
B.add('math11-u3-l3-2', [check('math11-u3-pc2', 'What are the asymptotes of $$f(x) = \\frac{3x}{x + 2}$$?', ['x = −2 and y = 3', 'x = 2 and y = 3', 'x = −2 and y = 0', 'x = 0 and y = 3'], 'A',
    '**Vertical:** the denominator is zero at x = −2 (and the numerator 3x is not zero there).\n**Horizontal:** top and bottom both have degree 1, so y = ratio of leading coefficients = 3/1 = 3.', title=T),
    mnemonic('math11-u3-mn2', 'Horizontal asymptote: "BOBO BOTN EATS DC"', ['**BOBO** — Bigger On Bottom: y = 0. **BOTN** — Bigger On Top: None (if top is exactly one degree bigger, a slant asymptote). **EATS DC** — Exponents Are The Same: Divide the leading Coefficients.'],
             letters=[('B', 'Bigger On Bottom', 'y = 0'), ('B', 'Bigger On Top', 'no horizontal asymptote'), ('E', 'Exponents the same', 'divide the leading coefficients')])])
B.add('math11-u3-l3-3', [check('math11-u3-pc3', 'Simplify $$\\frac{2}{x} - \\frac{1}{x + 2}$$.', ['$$\\frac{1}{x + 2}$$', '$$\\frac{x + 4}{x(x + 2)}$$', '$$\\frac{x}{x(x + 2)}$$', '$$\\frac{1}{-2}$$'], 'B',
    '**LCD** = x(x + 2).\n2/x = 2(x + 2)/[x(x + 2)] and 1/(x + 2) = x/[x(x + 2)].\nSubtract the numerators: 2x + 4 − x = x + 4. Result: (x + 4)/[x(x + 2)].', title=T)])
B.add('math11-u3-l3-4', [check('math11-u3-pc4', 'Solve $$\\frac{x + 1}{x - 2} \\ge 0$$.', ['$$x \\le -1$$ or $$x > 2$$', '$$-1 \\le x < 2$$', '$$x \\le -1$$ or $$x \\ge 2$$', '$$x > 2$$ only'], 'A',
    '**Critical values:** numerator 0 at x = −1 (allowed, since ≥), denominator 0 at x = 2 (never allowed).\n**Test intervals:** x = −2: (−1)/(−4) > 0 ✔; x = 0: 1/(−2) < 0 ✘; x = 3: 4/1 > 0 ✔.\nAnswer: x ≤ −1 or x > 2.', title=T)])
B.add('math11-u4-l4-2', [check('math11-u4-pc2', 'Solve $$\\log_3(2x + 1) = 2$$.', ['x = 4', 'x = 2.5', 'x = 3', 'x = 1'], 'A',
    '**Exponential form:** 2x + 1 = 3² = 9, so 2x = 8 and x = 4.\n**Check:** the argument 2(4) + 1 = 9 > 0 and log₃ 9 = 2 ✔.', title=T),
    mnemonic('math11-u4-mn2', 'Log = exponent: "the base goes to the other side"', ['log_b x = y ⇔ b^y = x. Read it as a loop: **base b, raised to the answer y, gives x.**', 'Logs of products **add**, quotients **subtract**, powers come **down in front**.'])])
B.add('math11-u4-l4-3', [check('math11-u4-pc3', 'A sample of 64 g of a radioactive substance has a half-life of 3 days. How much remains after 12 days?', ['4 g', '8 g', '16 g', '2 g'], 'A',
    '**Number of half-lives:** 12 ÷ 3 = 4.\n**Halve four times:** 64 → 32 → 16 → 8 → 4 g. (Formula: 64 × (½)⁴ = 4.)', title=T)])
B.add('math11-u5-l5-2', [check('math11-u5-pc2', 'Which information is NOT enough to prove two triangles similar?', ['Two pairs of equal angles (AA)', 'All three pairs of sides in the same ratio (SSS)', 'Two pairs of sides in the same ratio and the included angles equal (SAS)', 'Two pairs of sides in the same ratio and a non-included angle equal'], 'D',
    'The similarity tests are **AA**, **SSS** (all sides proportional) and **SAS** (two sides proportional AND the angle between them equal). With a non-included angle the triangle is not fixed (the ambiguous case), so D is not a valid test.', title=T)])
B.add('math11-u5-l5-3', [check('math11-u5-pc3', 'In right triangle ABC with the right angle at C, the altitude CD meets AB at D with AD = 4 and DB = 9. Find CD.', ['6', '6.5', '13', '36'], 'A',
    'The altitude to the hypotenuse is the **geometric mean** of the two segments: CD² = AD × DB = 4 × 9 = 36, so CD = 6. (13 is AD + DB; 6.5 is the arithmetic mean.)', title=T),
    mnemonic('math11-u5-mn3', 'Shadows: "same sun, same ratio"', ['At the same time of day, **height ÷ shadow** is the same for every object. Write h/shadow = known height/known shadow and cross-multiply.'])])
B.add('math11-u5-l5-4', [check('math11-u5-pc4', 'Two similar triangles have areas 18 cm² and 50 cm². What is the ratio of their perimeters?', ['3 : 5', '9 : 25', '18 : 50', '√3 : √5'], 'A',
    'Area ratio = k², so 18 : 50 = 9 : 25 = k². Then k = √9 : √25 = 3 : 5. Perimeters are lengths, so they are in the ratio k = 3 : 5.', title=T),
    mnemonic('math11-u5-mn4', '"Length k, Area k², Volume k³"', ['Count the dimensions: **perimeter 1D → k, area 2D → k², volume 3D → k³.** Going backwards, take the square root (areas) or the cube root (volumes).'])])
B.add('math11-u6-l6-2', [check('math11-u6-pc2', 'A invests 40 000 Nakfa for 6 months and B invests 30 000 Nakfa for 12 months. The profit is 15 000 Nakfa. What is B\'s share?', ['9 000 Nakfa', '6 000 Nakfa', '7 500 Nakfa', '8 571 Nakfa'], 'A',
    '**Capital × time:** A: 40 000 × 6 = 240 000; B: 30 000 × 12 = 360 000. Ratio A : B = 240 000 : 360 000 = 2 : 3.\n**Share:** B gets 3/5 × 15 000 = 9 000 Nakfa (A gets 6 000).', title=T)])
B.save()
