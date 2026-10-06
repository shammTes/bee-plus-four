"""chemistry_11 u4 (metals) and u5 (gases): replace 'This section is of the textbook' placeholders with real notes,
and give every lesson >=3 quick checks and >=1 worked example."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *

B = Book('chemistry_11')
S = dict(src='notes')

# ---------------- 4.2 Sodium
B.set('chem11-u4-c04', title='4.2 Sodium and its compounds', src='notes', body=[
 "**Occurrence:** sodium is too reactive to occur free. Its main source is **rock salt / sea water (NaCl)**; other minerals include Chile saltpetre (NaNO₃), borax and soda ash (Na₂CO₃).",
 "**Extraction — Downs cell:** molten NaCl (mixed with CaCl₂ to lower the melting point from about 801 °C to about 600 °C) is electrolysed. Cathode (iron): Na⁺ + e⁻ → Na (liquid sodium floats up and is collected). Anode (graphite): 2Cl⁻ → Cl₂ + 2e⁻. A steel gauze keeps Na and Cl₂ apart so they do not recombine.",
 "**Properties:** soft silvery metal (cut with a knife), low density (floats on water), low melting point (98 °C), one valence electron → forms Na⁺. Stored under paraffin oil because it reacts with air and water. Burns with a **yellow flame** forming Na₂O / Na₂O₂.",
 "**Important compounds:** NaOH (caustic soda — soap, paper, made by electrolysis of brine); Na₂CO₃ (washing soda — glass, softening hard water, made by the Solvay process); NaHCO₃ (baking soda — baking powder, antacid, fire extinguishers); NaCl (food, preserving, raw material for Na, Cl₂ and NaOH).",
 "**Uses of sodium:** coolant in some nuclear reactors (liquid Na conducts heat well), sodium-vapour street lamps (yellow light), making sodium compounds and reducing other metals (e.g. Ti from TiCl₄)."], enriched=True)
B.add('chem11-u4-l4-2', [
 worked('chem11-u4-wrk-na1', 'Worked: mass of sodium from a Downs cell',
  'How many grams of sodium are produced at the cathode when 117 g of molten NaCl is completely electrolysed? (Na = 23, Cl = 35.5)',
  ['Moles of NaCl = 117 ÷ 58.5 = 2.0 mol.', 'Cathode: Na⁺ + e⁻ → Na, so 1 mol NaCl gives 1 mol Na.', 'Mass of Na = 2.0 × 23 = 46 g (and 1.0 mol Cl₂ = 71 g at the anode).'],
  '46 g of sodium', **S),
 check('chem11-u4-chk-na1', 'Why is CaCl₂ added to the NaCl in the Downs cell?', ['To lower the melting point of the electrolyte and save energy', 'To supply extra sodium ions', 'To stop chlorine forming', 'To make the sodium heavier so it sinks'], 'A',
  'Pure NaCl melts at about 801 °C. Adding CaCl₂ lowers the melting point to about 600 °C, so less energy is needed to keep the electrolyte molten.', **S),
 check('chem11-u4-chk-na2', 'Sodium is stored under paraffin oil because it:', ['Reacts quickly with oxygen and water vapour in air', 'Is a liquid at room temperature', 'Dissolves in water', 'Is radioactive'], 'A',
  'Sodium is very reactive: it tarnishes in air and reacts violently with water. Paraffin oil keeps air and moisture away and sodium does not react with it.', **S),
 check('chem11-u4-chk-na3', 'Which sodium compound is used as baking powder and in some fire extinguishers?', ['NaHCO₃', 'NaOH', 'NaCl', 'Na₂SO₄'], 'A',
  'Sodium hydrogencarbonate (baking soda) decomposes on heating: 2NaHCO₃ → Na₂CO₃ + H₂O + CO₂. The CO₂ makes dough rise and smothers fires.', **S),
], after='chem11-u4-c13')
B.move(['chem11-u4-xtra2'], 'chem11-u4-l4-4')

# ---------------- 4.3 Aluminium
B.set('chem11-u4-c05', title='4.3 Aluminium', src='notes', body=[
 "**Occurrence:** the most abundant metal in the Earth's crust (about 8 %), found combined in clays and mainly in **bauxite, Al₂O₃·2H₂O**.",
 "**Purification (Bayer process):** bauxite is dissolved in hot NaOH (Al₂O₃ is amphoteric), impurities such as Fe₂O₃ are filtered off, Al(OH)₃ is precipitated and heated to give pure alumina, Al₂O₃.",
 "**Extraction (Hall–Héroult process):** alumina is dissolved in molten **cryolite (Na₃AlF₆)**, which lowers the working temperature to about 950 °C, and electrolysed with carbon electrodes. Cathode: Al³⁺ + 3e⁻ → Al. Anode: 2O²⁻ → O₂ + 4e⁻; the oxygen burns the carbon anodes away (C + O₂ → CO₂), so they must be replaced regularly. The process uses a lot of electricity, so recycling aluminium saves energy.",
 "**Properties:** light (density 2.7 g/cm³), good conductor of heat and electricity, malleable, ductile. Although reactive, it is protected by a thin, tough **oxide layer** (Al₂O₃) — this can be thickened by anodising. Amphoteric: reacts with acids and with alkalis.",
 "**Uses:** overhead power cables, aircraft and vehicle bodies (as alloys such as duralumin), drink cans, cooking pots, foil, window frames. Alum, K₂SO₄·Al₂(SO₄)₃·24H₂O, is used to purify water."], enriched=True)
B.add('chem11-u4-l4-3', [
 worked('chem11-u4-wrk-al1', 'Worked: aluminium from alumina',
  'What mass of aluminium can be obtained from 204 t of pure alumina, Al₂O₃? (Al = 27, O = 16)',
  ['Molar mass Al₂O₃ = 2(27) + 3(16) = 102.', 'Each Al₂O₃ contains 2 Al, so mass fraction of Al = 54/102.', 'Mass Al = 204 × 54/102 = 108 t.'], '108 t of aluminium', **S),
 check('chem11-u4-chk-al1', 'Why is alumina dissolved in molten cryolite before electrolysis?', ['To lower the operating temperature and save energy', 'To make aluminium react faster with oxygen', 'Because cryolite is the ore of aluminium', 'To produce fluorine gas'], 'A',
  'Alumina melts above 2000 °C. Dissolved in molten cryolite it can be electrolysed at about 950 °C, which saves a great deal of energy.', **S),
 check('chem11-u4-chk-al2', 'The carbon anodes in aluminium extraction must be replaced regularly because:', ['Oxygen formed at the anode burns them to CO₂', 'Aluminium dissolves them', 'They melt at 950 °C', 'Cryolite turns them into diamond'], 'A',
  'Oxide ions are discharged at the anode as O₂; at that temperature the oxygen reacts with the carbon to form CO₂, so the anodes wear away.', **S),
 check('chem11-u4-chk-al3', 'Aluminium is high in the reactivity series, yet aluminium pots do not corrode in air. Why?', ['A thin, unreactive layer of Al₂O₃ protects the surface', 'Aluminium does not react with oxygen', 'Aluminium is a noble metal', 'Pots are coated with gold'], 'A',
  'Aluminium reacts with air at once to form a thin, tough, non-porous Al₂O₃ layer that sticks to the metal and stops further attack.', **S),
], after='chem11-u4-c05')

# ---------------- 4.4 Iron
B.set('chem11-u4-c06', title='Five important metals at a glance')
B.add('chem11-u4-l4-4', [
 text('chem11-u4-c-fe1', '4.4 Iron — extraction and steel', [
  "**Ores:** haematite (Fe₂O₃), magnetite (Fe₃O₄), limonite (2Fe₂O₃·3H₂O), siderite (FeCO₃) and iron pyrites (FeS₂ — not used for iron because of the sulphur).",
  "**Blast furnace:** iron ore, coke and limestone go in at the top; hot air is blown in at the bottom.",
  "1. Coke burns: C + O₂ → CO₂ (gives heat). 2. CO₂ + C → 2CO. 3. CO reduces the ore: Fe₂O₃ + 3CO → 2Fe + 3CO₂.",
  "4. Limestone removes sand (the main impurity): CaCO₃ → CaO + CO₂; CaO + SiO₂ → CaSiO₃ (**slag**). Molten slag floats on the molten iron and both are tapped off.",
  "**Pig/cast iron** (about 4 % C) is hard but brittle. **Steel** is made by blowing oxygen through molten iron to burn off most of the carbon, then adding controlled amounts of C, Cr, Ni, Mn etc. Mild steel (≈0.25 % C) — car bodies, nails; stainless steel (Fe + Cr + Ni) — cutlery, sinks.",
  "**Rusting** needs both water and oxygen: 4Fe + 3O₂ + 2xH₂O → 2Fe₂O₃·xH₂O. Prevented by painting, oiling, plastic coating, galvanising (zinc), tin-plating or sacrificial blocks of a more reactive metal."], **S),
 worked('chem11-u4-wrk-fe1', 'Worked: iron from haematite',
  'Calculate the mass of iron that can be obtained from 480 kg of haematite, Fe₂O₃. (Fe = 56, O = 16)',
  ['Molar mass Fe₂O₃ = 2(56) + 3(16) = 160.', 'Fe₂O₃ + 3CO → 2Fe + 3CO₂: 160 kg of ore gives 112 kg of iron.', 'Mass Fe = 480 × 112/160 = 336 kg.'], '336 kg of iron', **S),
 check('chem11-u4-chk-fe1', 'What is the main reducing agent for iron oxide in the blast furnace?', ['Carbon monoxide', 'Limestone', 'Oxygen', 'Slag'], 'A',
  'Coke burns to CO₂, which reacts with more coke to give CO. Carbon monoxide removes oxygen from the ore: Fe₂O₃ + 3CO → 2Fe + 3CO₂.', **S),
 check('chem11-u4-chk-fe2', 'Limestone is added to the blast furnace in order to:', ['Remove sandy impurities as slag', 'Reduce the iron ore', 'Raise the carbon content of the iron', 'Produce carbon monoxide'], 'A',
  'Limestone decomposes to CaO, a basic oxide, which reacts with acidic SiO₂ (sand) to form calcium silicate slag: CaO + SiO₂ → CaSiO₃.', **S),
 check('chem11-u4-chk-fe3', 'Galvanised iron does not rust even when scratched because:', ['Zinc is more reactive and corrodes in place of the iron', 'Zinc is less reactive than iron', 'Zinc blocks light', 'Zinc turns iron into steel'], 'A',
  'Zinc is above iron in the reactivity series, so it loses electrons in preference to iron (sacrificial protection), even where the coating is broken.', **S),
], after='chem11-u4-c06')

# ---------------- 4.5 Copper
B.set('chem11-u4-c07', title='4.5 Copper', src='notes', body=[
 "**Ores:** chalcopyrite (copper pyrites, CuFeS₂ — the main ore), chalcocite (Cu₂S), cuprite (Cu₂O) and malachite (CuCO₃·Cu(OH)₂). Eritrea's Bisha and Debarwa deposits contain copper sulphide ores.",
 "**Extraction from sulphide ore:** 1) the ore is crushed and concentrated by **froth flotation**; 2) it is **roasted** in air: 2CuFeS₂ + 4O₂ → Cu₂S + 2FeO + 3SO₂; 3) iron is removed as slag (FeO + SiO₂ → FeSiO₃); 4) Cu₂S is partly oxidised and the oxide reacts with the remaining sulphide (**self-reduction**): 2Cu₂O + Cu₂S → 6Cu + SO₂. This gives impure **blister copper** (about 98 %).",
 "**Electrolytic refining:** impure copper is the **anode**, a thin strip of pure copper the **cathode**, and acidified CuSO₄ solution the electrolyte. Anode: Cu → Cu²⁺ + 2e⁻; cathode: Cu²⁺ + 2e⁻ → Cu (99.98 % pure). Impurities such as Ag and Au fall as **anode sludge**.",
 "**Properties:** reddish-brown, excellent conductor of electricity and heat, ductile, malleable, does not react with dilute HCl or H₂SO₄ (below hydrogen). In moist air it slowly forms a green coating (basic copper carbonate).",
 "**Uses:** electric wires and cables, water pipes, cooking vessels, coins; alloys brass (Cu + Zn) and bronze (Cu + Sn). CuSO₄·5H₂O (blue vitriol) is used as a fungicide (Bordeaux mixture)."], enriched=True)
B.add('chem11-u4-l4-5', [
 worked('chem11-u4-wrk-cu1', 'Worked: refining copper',
  'During electrolytic refining, the anode loses 12.8 g of copper. What mass of copper is deposited on the cathode, and how many moles of electrons flowed? (Cu = 64)',
  ['Anode: Cu → Cu²⁺ + 2e⁻; cathode: Cu²⁺ + 2e⁻ → Cu — copper simply moves from anode to cathode.', 'Mass deposited = 12.8 g (ignoring impurities).', 'Moles Cu = 12.8 ÷ 64 = 0.20 mol; electrons = 2 × 0.20 = 0.40 mol.'], '12.8 g; 0.40 mol of electrons', **S),
 check('chem11-u4-chk-cu1', 'In the electrolytic refining of copper, the impure copper is made the:', ['Anode', 'Cathode', 'Electrolyte', 'Anode sludge'], 'A',
  'Copper atoms of the impure anode go into solution as Cu²⁺ and are deposited as pure copper on the cathode; impurities fall to the bottom as anode sludge.', **S),
 check('chem11-u4-chk-cu2', 'Which process concentrates a copper sulphide ore by making the ore particles stick to air bubbles?', ['Froth flotation', 'Calcination', 'Electrolysis', 'Galvanising'], 'A',
  'In froth flotation the powdered ore is mixed with water, oil and air. Sulphide particles are wetted by the oil, cling to the froth and are skimmed off; the gangue sinks.', **S),
 check('chem11-u4-chk-cu3', 'Copper is used for electrical wiring mainly because it:', ['Is a very good conductor and is ductile', 'Is the most reactive metal', 'Is very light', 'Reacts with water to give hydrogen'], 'A',
  'Copper has very high electrical conductivity (second only to silver), can be drawn into wires and resists corrosion.', **S),
], after='chem11-u4-c07')

# ---------------- 4.6 Zinc
B.set('chem11-u4-c08', title='4.6 Zinc', src='notes', body=[
 "**Ores:** zinc blende (sphalerite, ZnS — the main ore), calamine (ZnCO₃) and zincite (ZnO). Zinc is also produced at Eritrea's Bisha mine.",
 "**Extraction:** the ore is concentrated by froth flotation, then converted to the oxide — ZnS by **roasting**: 2ZnS + 3O₂ → 2ZnO + 2SO₂ (the SO₂ is used to make sulphuric acid); ZnCO₃ by **calcination**: ZnCO₃ → ZnO + CO₂.",
 "The oxide is reduced with coke at about 1400 °C: ZnO + C → Zn + CO. Zinc boils at 907 °C, so it distils off as vapour and is condensed. Alternatively ZnO is dissolved in H₂SO₄ and the ZnSO₄ solution is **electrolysed** to give very pure zinc.",
 "**Properties:** bluish-white, fairly reactive (above iron, below aluminium), amphoteric oxide; reacts with dilute acids to give H₂: Zn + 2HCl → ZnCl₂ + H₂.",
 "**Uses:** galvanising iron (roofing sheets), the casing of dry cells, brass (Cu + Zn), die-casting alloys; ZnO in paints, ointments and rubber."], enriched=True)
B.add('chem11-u4-l4-6', [
 worked('chem11-u4-wrk-zn1', 'Worked: SO₂ from roasting zinc blende',
  'What volume of SO₂ at STP is produced when 194 kg of ZnS is roasted? (Zn = 65, S = 32; molar volume 22.4 L)',
  ['Molar mass ZnS = 97 g/mol, so 194 kg = 194 000 ÷ 97 = 2000 mol.', '2ZnS + 3O₂ → 2ZnO + 2SO₂: 1 mol ZnS gives 1 mol SO₂ → 2000 mol SO₂.', 'Volume = 2000 × 22.4 = 44 800 L = 44.8 m³.'], '44.8 m³ of SO₂', **S),
 check('chem11-u4-chk-zn1', 'Zinc blende must be roasted before reduction with carbon because:', ['Carbon reduces oxides, so the sulphide must first be changed to ZnO', 'Roasting removes zinc', 'ZnS is already pure zinc', 'Roasting produces carbon monoxide'], 'A',
  'Carbon cannot easily reduce sulphides. Roasting in air converts ZnS into ZnO, which coke then reduces: ZnO + C → Zn + CO.', **S),
 check('chem11-u4-chk-zn2', 'In the carbon-reduction method, zinc is collected by condensing its vapour. This is possible because zinc:', ['Has a low boiling point (907 °C)', 'Is a gas at room temperature', 'Does not react with carbon', 'Is denser than slag'], 'A',
  'The furnace is hotter than 907 °C, so zinc forms as a vapour that is led away and condensed.', **S),
 check('chem11-u4-chk-zn3', 'Brass is an alloy of zinc with:', ['Copper', 'Tin', 'Iron', 'Lead'], 'A',
  'Brass is copper + zinc. Bronze is copper + tin.', **S),
], after='chem11-u4-c08')

# ---------------- 4.7 Gold
B.set('chem11-u4-c09', title='4.7 Gold', src='notes', body=[
 "**Occurrence:** gold is so unreactive that it occurs **native** (as the free metal) — as grains in quartz veins and in river sands (placer deposits). Eritrea has gold at Bisha, Koka, Zara and in the ancient workings of the Asmara area.",
 "**Extraction:** placer gold can be separated by **panning/washing** because gold is very dense (19.3 g/cm³). Gold in rock is crushed and dissolved by **cyanidation**: 4Au + 8NaCN + O₂ + 2H₂O → 4Na[Au(CN)₂] + 4NaOH. The gold is then displaced by zinc: 2Na[Au(CN)₂] + Zn → Na₂[Zn(CN)₄] + 2Au, and refined by electrolysis. (Cyanide is very poisonous, so mine waste must be handled carefully.)",
 "**Properties:** yellow, very dense, the most malleable and ductile metal, excellent conductor, does not tarnish or react with ordinary acids; dissolves only in **aqua regia** (3 HCl : 1 HNO₃).",
 "**Purity:** measured in **carats** — pure gold is 24 carat; 18-carat gold is 18/24 = 75 % gold alloyed with copper or silver to make it harder.",
 "**Uses:** jewellery, coins and national reserves, electronic contacts, dentistry, reflective coatings."], enriched=True)
B.add('chem11-u4-l4-7', [
 worked('chem11-u4-wrk-au1', 'Worked: carats',
  'A ring of mass 8.0 g is made of 18-carat gold. What mass of pure gold does it contain?',
  ['Pure gold = 24 carat, so 18 carat means 18/24 of the mass is gold.', '18/24 = 0.75.', 'Mass of gold = 0.75 × 8.0 = 6.0 g (the other 2.0 g is mostly copper or silver).'], '6.0 g of gold', **S),
 check('chem11-u4-chk-au1', 'Gold is found as the free metal in nature mainly because it:', ['Is very unreactive', 'Is very dense', 'Has a low melting point', 'Is magnetic'], 'A',
  'Gold is at the bottom of the reactivity series; it does not react with oxygen, water or most acids, so it stays uncombined (native).', **S),
 check('chem11-u4-chk-au2', 'Which mixture dissolves gold?', ['Aqua regia (conc. HCl and HNO₃, 3 : 1)', 'Dilute sulphuric acid', 'Sodium hydroxide solution', 'Water'], 'A',
  'Nitric acid oxidises gold slightly and chloride ions remove Au³⁺ as [AuCl₄]⁻, so the mixture dissolves gold although neither acid does alone.', **S),
 check('chem11-u4-chk-au3', 'Panning separates gold from river sand because gold:', ['Is much denser than sand', 'Floats on water', 'Dissolves in water', 'Is attracted to magnets'], 'A',
  'Gold (19.3 g/cm³) is about seven times denser than sand, so swirling with water washes the light sand away and leaves gold in the pan.', **S),
], after='chem11-u4-c09')

# ---------------- 4.8 Alloys
B.set('chem11-u4-c10', title='4.8 Alloys', body=[
 "An **alloy** is a mixture of a metal with one or more other elements (usually metals, sometimes carbon). Atoms of different sizes disturb the regular layers of the metal lattice, so layers cannot slide easily: alloys are usually **harder and stronger** than the pure metal, may resist corrosion better and often have a lower melting point.",
 "Brass (Cu + Zn) — taps, musical instruments, ornaments. Bronze (Cu + Sn) — statues, medals, bells. Steel (Fe + C) and stainless steel (Fe + Cr + Ni) — construction, cutlery. Duralumin (Al + Cu + Mg + Mn) — aircraft bodies. Solder (Sn + Pb) — joining wires, low melting point. Amalgam (Hg + another metal) — dental fillings. 18-carat gold (Au + Cu/Ag) — jewellery."])
B.add('chem11-u4-l4-8', [
 worked('chem11-u4-wrk-all1', 'Worked: composition of an alloy',
  'A 250 g bronze bell contains 88 % copper and the rest tin. Find the masses of copper and tin.',
  ['Copper = 88 % of 250 g = 0.88 × 250 = 220 g.', 'Tin = 250 − 220 = 30 g (12 %).'], '220 g Cu and 30 g Sn', **S),
 check('chem11-u4-chk-all1', 'Why are alloys usually harder than the pure metals they are made from?', ['Different-sized atoms stop the layers of atoms sliding over each other', 'Alloys contain no metallic bonds', 'Alloys are compounds with fixed formulas', 'Alloys are always heavier'], 'A',
  'In a pure metal, identical atoms form regular layers that slide easily. Atoms of another size distort the layers and make sliding harder.', **S),
 check('chem11-u4-chk-all2', 'Which alloy is used for aircraft bodies because it is light and strong?', ['Duralumin', 'Solder', 'Brass', 'Amalgam'], 'A',
  'Duralumin is mainly aluminium (light) with small amounts of copper, magnesium and manganese, which make it much stronger than pure aluminium.', **S),
 check('chem11-u4-chk-all3', 'Stainless steel resists rusting because it contains:', ['Chromium (and nickel)', 'Extra carbon', 'Zinc only', 'Gold'], 'A',
  'Chromium forms a thin protective oxide layer on the surface of stainless steel, which stops oxygen and water reaching the iron.', **S),
], after='chem11-u4-c10')

# ---------------- 5.1 The gaseous state
B.set('chem11-u5-c01', title='5.1 The gaseous state', src='notes', body=[
 "Gas particles are far apart and move rapidly and randomly, so gases **have no fixed shape or volume**, are easily **compressed**, **expand** to fill their container, have **low density** and **diffuse** quickly into each other.",
 "A gas sample is described by four measurable quantities: **pressure P** (Pa, kPa, atm, mmHg; 1 atm = 101.3 kPa = 760 mmHg), **volume V** (m³, L, cm³; 1 L = 1 dm³ = 1000 cm³), **temperature T** (always in kelvin for gas calculations: T = t °C + 273) and **amount n** (mol).",
 "**Pressure** is caused by gas particles hitting the walls of the container; it is measured with a barometer (atmospheric pressure) or a manometer (gas in a container).",
 "**STP** (standard temperature and pressure) = 0 °C (273 K) and 1 atm (101.3 kPa). At STP one mole of any ideal gas occupies about **22.4 L**."], enriched=True)
B.add('chem11-u5-l5-1', [
 worked('chem11-u5-wrk-st1', 'Worked: converting units',
  'A gas is at 25 °C and 380 mmHg in a 500 cm³ flask. Express T in kelvin, P in atm and kPa, and V in litres.',
  ['T = 25 + 273 = 298 K.', 'P = 380/760 = 0.50 atm = 0.50 × 101.3 = 50.7 kPa.', 'V = 500 cm³ = 500/1000 = 0.500 L.'], '298 K; 0.50 atm (50.7 kPa); 0.500 L', **S),
 check('chem11-u5-chk-st1', 'Gases are easily compressed because:', ['Their particles are far apart with lots of empty space', 'Their particles are very large', 'They have strong forces between particles', 'Their particles do not move'], 'A',
  'Most of the volume of a gas is empty space between particles, so pushing the particles closer together is easy.', **S),
 check('chem11-u5-chk-st2', 'What is the pressure of 2.0 atm in kPa?', ['202.6 kPa', '101.3 kPa', '1520 kPa', '50.7 kPa'], 'A',
  '1 atm = 101.3 kPa, so 2.0 atm = 2.0 × 101.3 = 202.6 kPa. (1520 would be the value in mmHg.)', **S),
], after='chem11-u5-c08')

# ---------------- 5.2 Gas laws
B.set('chem11-u5-c02', title='5.2 The gas laws', src='notes', body=[
 "**Boyle's law:** at constant temperature, the volume of a fixed mass of gas is inversely proportional to its pressure: P₁V₁ = P₂V₂ (a graph of P against 1/V is a straight line through the origin).",
 "**Charles' law:** at constant pressure, the volume of a fixed mass of gas is directly proportional to its kelvin temperature: V₁/T₁ = V₂/T₂. Extending the V–t graph to V = 0 gives **absolute zero, −273 °C (0 K)**.",
 "**Gay-Lussac's (pressure) law:** at constant volume, P₁/T₁ = P₂/T₂. **Combined gas law:** P₁V₁/T₁ = P₂V₂/T₂.",
 "**Avogadro's law:** equal volumes of all gases at the same temperature and pressure contain equal numbers of molecules (V ∝ n).",
 "**Ideal gas equation:** PV = nRT, with R = 8.314 J mol⁻¹ K⁻¹ (P in Pa, V in m³) or 0.0821 L atm mol⁻¹ K⁻¹. Using n = m/M it also gives molar mass: M = mRT/(PV), and density d = PM/(RT).",
 "**Dalton's law of partial pressures:** the total pressure of a gas mixture equals the sum of the partial pressures: P_total = P₁ + P₂ + … . **Graham's law:** rate of diffusion ∝ 1/√M, so light gases (H₂, He) diffuse fastest."], enriched=True)
B.add('chem11-u5-l5-2', [
 worked('chem11-u5-wrk-gl1', 'Worked: combined gas law',
  'A gas occupies 300 mL at 27 °C and 100 kPa. What volume will it occupy at 127 °C and 200 kPa?',
  ['T₁ = 300 K, T₂ = 400 K.', 'V₂ = V₁ × (P₁/P₂) × (T₂/T₁) = 300 × (100/200) × (400/300).', 'V₂ = 300 × 0.5 × 1.333 = 200 mL.'], '200 mL', **S),
 worked('chem11-u5-wrk-gl2', 'Worked: molar mass from PV = nRT',
  '0.64 g of a gas occupies 0.224 L at STP. Find its molar mass.',
  ['At STP 1 mol occupies 22.4 L, so n = 0.224/22.4 = 0.010 mol.', 'M = m/n = 0.64/0.010 = 64 g/mol (e.g. SO₂).'], '64 g/mol', **S),
 check('chem11-u5-chk-gl1', 'At constant temperature, the pressure on a gas is tripled. The volume becomes:', ['One third of the original', 'Three times the original', 'Nine times the original', 'Unchanged'], 'A',
  "Boyle's law: P₁V₁ = P₂V₂. If P is multiplied by 3, V must be divided by 3.", **S),
 check('chem11-u5-chk-gl2', 'A gas mixture contains N₂ at 60 kPa, O₂ at 30 kPa and CO₂ at 10 kPa. The total pressure is:', ['100 kPa', '60 kPa', '33.3 kPa', '1800 kPa'], 'A',
  "Dalton's law: P_total = 60 + 30 + 10 = 100 kPa.", **S),
 check('chem11-u5-chk-gl3', 'Which gas diffuses fastest at the same temperature?', ['H₂ (M = 2)', 'O₂ (M = 32)', 'CO₂ (M = 44)', 'Cl₂ (M = 71)'], 'A',
  "Graham's law: rate ∝ 1/√M. Hydrogen has the smallest molar mass, so it diffuses fastest — 4 times faster than O₂ (√(32/2) = 4).", **S),
], after='chem11-u5-xtra2')

# 5.3 kinetic theory: fix answer that repeated a sense check; add checks
B.set('chem11-u5-c05', answer='V₂ = 1 L')
B.set('chem11-u5-c06', answer='V₂ = 400 mL')
B.add('chem11-u5-l5-3', [
 check('chem11-u5-chk-kt1', 'According to the kinetic theory, the average kinetic energy of gas particles is proportional to:', ['The kelvin temperature', 'The pressure only', 'The volume of the container', 'The Celsius temperature'], 'A',
  'Average KE ∝ T in kelvin. At 0 K the particles would have minimum energy; doubling the kelvin temperature doubles the average KE.', **S),
 check('chem11-u5-chk-kt2', 'Real gases deviate most from ideal behaviour at:', ['High pressure and low temperature', 'Low pressure and high temperature', 'STP only', 'Any temperature above 0 °C'], 'A',
  'At high pressure particles are close, so their own volume matters; at low temperature they move slowly, so attractions matter. Both break the ideal-gas assumptions.', **S),
 check('chem11-u5-chk-kt3', 'Heating a gas in a closed rigid container increases its pressure because the particles:', ['Move faster and hit the walls harder and more often', 'Get bigger', 'Increase in number', 'Stop colliding with each other'], 'A',
  'Higher temperature means higher average speed, so collisions with the walls are more frequent and more forceful — the pressure rises (Gay-Lussac’s law).', **S),
], after='chem11-u5-c13')

u4 = B.unit('chem11-u4'); u4.pop('note', None)
u5 = B.unit('chem11-u5'); u5.pop('note', None)
B.save()
