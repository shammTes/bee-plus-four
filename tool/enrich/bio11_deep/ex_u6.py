"""Unit 6 practice questions: 6.1.3, 6.3.2, 6.4.1, 6.4.2, 6.4.3."""
from common import set_unit, QSet

set_unit('bio11-u6')

a = QSet('6.1.3 Practice — plant hormones', 's613')
a.M(109, 'Which hormone is mainly responsible for apical dominance?', ['Cytokinin', 'Auxin', 'Ethylene', 'Gibberellin'], 'B',
    ['Step 1: apical dominance = terminal bud suppresses lateral buds.', 'Step 2: the suppressing chemical is auxin (IAA) from the tip.'], 'Auxin from the top holds the side buds back.', [('Which hormone stimulates lateral buds?', 'Cytokinin (also gibberellin).')])
a.M(111, 'The main hormone responsible for abscission (leaf and fruit fall) is', ['abscisic acid', 'ethylene', 'auxin', 'cytokinin'], 'B',
    ['Step 1: ABA was named for abscission, but that was a mistake.', 'Step 2: botanists now know ethylene is the main abscission hormone.'], 'Do not trust the name “abscisic”.', [('What is the main role of ABA?', 'Dormancy of buds and seeds; inhibits other hormones.')])
a.F(110, 'A high ratio of auxin to cytokinin in a tissue-culture medium stimulates ____ formation.', 'root', ['root', 'shoot', 'flower', 'fruit'],
    ['Step 1: auxin promotes root initiation.', 'Step 2: high auxin : cytokinin → roots; low → shoots.'], 'Auxin → roots (rooting powder is auxin).', [('What does a low auxin : cytokinin ratio produce?', 'Shoots.')])
a.TF(110, '2,4-D kills monocot crops such as maize and wheat but not broad-leaved weeds.', False,
     ['Step 1: 2,4-D is a selective synthetic auxin.', 'Step 2: it kills dicots (broad-leaved weeds) and spares monocots → false.'], 'Broad leaves die; grasses survive.', [('Name a synthetic auxin used to root cuttings.', 'NAA (naphthalene acetic acid).')])
a.S(110, 'Explain how auxin causes a shoot to bend towards light.', 'Auxin is made in the shoot tip. When light comes from one side, auxin moves to the shaded side. Cells on the shaded side elongate more than those on the lit side, so the shoot curves towards the light (positive phototropism).',
    ['Step 1: source — tip.', 'Step 2: redistribution to the shaded side.', 'Step 3: unequal elongation.', 'Step 4: bending to light.'], 'Keep the order: tip → shade → stretch → bend.', [('What would happen if the tip were covered with a foil cap?', 'No bending — the tip senses the light, so auxin is not redistributed.')])
a.M(110, 'Gibberellins are sprayed on grapes to', ['speed up leaf fall', 'increase fruit size and spacing', 'keep seeds dormant', 'kill weeds'], 'B',
    ['Step 1: gibberellins promote elongation and fruit development.', 'Step 2: on grapes they give bigger fruits farther apart.'], 'GA = grow and get bigger.', [('What happens to a dwarf plant sprayed with gibberellin?', 'It grows taller than normal.')])
a.S(110, 'Name the five groups of plant hormones and give one effect of each.', 'Auxins — cell elongation/phototropism; gibberellins — stem elongation; cytokinins — cell division; abscisic acid — dormancy of buds and seeds; ethylene — fruit ripening.',
    ['Step 1: list in order (All Good Cooks Ask Eggs).', 'Step 2: one verb each: aim, grow, cut, sleep, ripen.'], 'Use the mnemonic to remember all five quickly.', [('Which plant hormone is a gas?', 'Ethylene.')])
a.M(110, 'Which pair of hormones has opposite effects on root initiation?', ['Auxin and gibberellin', 'Cytokinin and ethylene', 'ABA and ethylene', 'Auxin and NAA'], 'A',
    ['Step 1: auxin stimulates root initiation.', 'Step 2: gibberellins inhibit root initiation.'], 'Compare the promote/inhibit table.', [('Which hormone opposes seed germination?', 'Abscisic acid (it keeps seeds dormant).')])
a.S(111, 'Why do traders keep unripe fruit away from ripe fruit, in cool ventilated stores?', 'Ripe fruit gives off ethylene gas, which spreads and speeds up ripening of nearby fruit. Ventilation removes the ethylene and cool temperatures slow ripening, so the unripe fruit keeps longer.',
    ['Step 1: ripe fruit → ethylene.', 'Step 2: ethylene is a gas, spreads.', 'Step 3: ventilation + cold slow ripening.'], 'Ethylene questions: always mention it is a gas.', [('Why does putting an unripe avocado in a bag with a banana speed ripening?', 'The banana releases ethylene, trapped in the bag.')])

b = QSet('6.3.2 Practice — root growth regions', 's632')
b.M(118, 'Which region of the root tip is responsible for protecting the meristem?', ['Root cap', 'Region of elongation', 'Region of maturation', 'Pericycle'], 'A',
    ['Step 1: the meristem is delicate.', 'Step 2: the root cap covers it like a cup.'], 'Cap = helmet.', [('Why is the outside of the root cap rough?', 'Its cells are constantly worn away by the soil.')])
b.M(118, 'In which region do small vacuoles merge into one or two large vacuoles?', ['Root cap', 'Region of cell division', 'Region of elongation', 'Root-hair zone'], 'C',
    ['Step 1: elongating cells take in lots of water.', 'Step 2: the water fills merging vacuoles, up to 90 % of the cell.'], 'Big vacuole = stretching cell.', [('What do cells in the region of cell division look like?', 'Small, cube-shaped, large nuclei, few tiny vacuoles.')])
b.F(119, 'The region of maturation is also called the region of differentiation or the ____ zone.', 'root-hair', ['root-hair', 'cap', 'meristem', 'elongation'],
    ['Step 1: root hairs appear where cells specialise.', 'Step 2: so it is called the root-hair zone.'], 'Hairs grow where cells mature.', [('What forms in the region of maturation besides root hairs?', 'Permanent tissues such as xylem, phloem, cortex and endodermis.')])
b.TF(119, 'Root hairs live for the whole life of the plant.', False,
     ['Step 1: root hairs are short-lived.', 'Step 2: they wither as the root grows and new ones form nearer the tip → false.'], 'Root hairs are temporary.', [('Why must new root hairs keep forming?', 'Old ones die; new hairs are needed to keep absorbing water in fresh soil.')])
b.S(118, 'Explain why there is no further increase in root length above the region of elongation.', 'Only the root cap and the apical meristem actually move forward through the soil. Cells above the elongation zone have stopped stretching and become differentiated; they are fixed in the soil (often by root hairs), so that part of the root does not lengthen.',
    ['Step 1: what moves — cap and meristem.', 'Step 2: cells above have finished elongating.', 'Step 3: they differentiate and are anchored.'], 'Growth in length = only the tip region.', [('Which region produces new cells for root growth?', 'The region of cell division (apical meristem).')])
b.M(119, 'Most water and mineral salts are absorbed by the', ['root cap', 'region of cell division', 'root hairs', 'endodermis'], 'C',
    ['Step 1: absorption needs a large surface.', 'Step 2: root hairs greatly increase the surface and have a thin cuticle.'], 'Large surface + thin wall = absorption.', [('A root hair is an outgrowth of which cell?', 'A single epidermal cell.')])
b.S(118, 'State one structural feature and the function of each of the four root regions.', 'Root cap — cup of parenchyma cells, protects the tip. Cell division — small cube-shaped cells with large nuclei, make new cells. Elongation — cells with large vacuoles, increase root length. Maturation — root hairs and differentiated tissues, absorb water and minerals.',
    ['Step 1: cap.', 'Step 2: division.', 'Step 3: elongation.', 'Step 4: maturation.'], 'A two-column table answer earns full marks quickly.', [('List the regions from the tip upward.', 'Cap, division, elongation, maturation.')])
b.S(118, 'Where do new root cap cells come from? Comment on the textbook statement.', 'New root cap cells are produced by the growing point (region of cell division / meristem). The textbook says in one place that the cap “arises from the region of elongation”, but its next paragraph says correctly that the growing point gives rise to new root cap cells.',
    ['Step 1: the cap is worn away constantly.', 'Step 2: the meristem divides and adds cells to the cap.', 'Step 3: elongating cells only stretch; they do not divide.'], 'Only dividing (meristem) cells can make new cells.', [('Which cells in the root tip divide?', 'The meristematic cells of the region of cell division.')])

c = QSet('6.4.1 Practice — the stem', 's641')
c.M(122, 'Which is NOT one of the four functions of a stem?', ['Bears leaves', 'Holds leaves in light', 'Absorbs water from the soil', 'Conducts water and food'], 'C',
    ['Step 1: stem functions — bear leaves, hold them in light, conduct, store.', 'Step 2: absorbing soil water is the root’s job.'], 'Root absorbs; stem conducts.', [('Name a stem that stores food.', 'Potato tuber or sugar cane.')])
c.F(122, 'The point on a stem where a leaf is attached is called a ____.', 'node', ['node', 'internode', 'axil', 'petiole'],
    ['Step 1: node = leaf attachment point.', 'Step 2: internode = between nodes.'], 'Nodes have leaves; internodes are bare.', [('What is found in the axil of a leaf?', 'An axillary bud.')])
c.M(123, 'In a dicot stem the cambium is found', ['in the pith', 'between xylem and phloem', 'in the epidermis', 'scattered in the cortex'], 'B',
    ['Step 1: each vascular bundle has phloem outside and xylem inside.', 'Step 2: cambium lies between them and makes new xylem and phloem.'], 'Phloem–Cambium–Xylem (outside → inside).', [('Do monocot stems have cambium?', 'No.')])
c.TF(124, 'Monocot stems have vascular bundles arranged in a ring.', False,
     ['Step 1: dicots — ring.', 'Step 2: monocots — scattered → false.'], 'Monocot = Messy (scattered).', [('Which stem type has a large central pith?', 'Dicot.')])
c.S(123, 'State the function of each tissue in a dicot stem: epidermis, cortex, vascular bundle, pith.', 'Epidermis — protection; its cuticle reduces water loss. Cortex — parenchyma with air spaces for storage and gas exchange. Vascular bundles — xylem carries water and minerals up, phloem carries food; cambium makes new xylem and phloem. Pith — stores food and water.',
    ['Step 1: epidermis.', 'Step 2: cortex.', 'Step 3: vascular bundle.', 'Step 4: pith.'], 'Go outside → centre (Every Cat Visits Paris).', [('Which tissue has the largest cells in a stem section?', 'The pith.')])
c.M(123, 'Water and dissolved minerals move up the stem in the', ['phloem', 'xylem', 'cortex', 'pith'], 'B',
    ['Step 1: xylem = water up from roots.', 'Step 2: phloem = food from leaves.'], 'Xylem carries H₂O: think “x = water pipe”.', [('Which direction does phloem carry food?', 'From the leaves to other parts (up or down).')])
c.S(123, 'A ring of bark is removed from a tree trunk. Why does the tree eventually die even though the leaves stay green at first?', 'Removing the bark removes the phloem but leaves the xylem. Water still reaches the leaves, so they stay green, but food made in the leaves cannot reach the roots. The roots starve and die, so water uptake stops and the tree dies.',
    ['Step 1: bark = phloem.', 'Step 2: xylem intact → leaves get water.', 'Step 3: roots get no food → die.', 'Step 4: tree dies.'], 'Separate the two pipes in your answer.', [('Which tissue is damaged first when goats strip bark?', 'Phloem.')])
c.M(122, 'Leaves arranged three or more at a node are described as', ['alternate', 'opposite', 'whorled', 'parallel'], 'C',
    ['Step 1: one per node = alternate; two = opposite.', 'Step 2: three or more = whorled.'], 'Whorl = ring of leaves.', [('What is the growing tip covered by young leaves called?', 'The terminal bud.')])

d = QSet('6.4.2 Practice — the leaf', 's642')
d.M(126, 'Which layer of the leaf is covered by a thick waxy cuticle?', ['Upper epidermis', 'Palisade layer', 'Spongy layer', 'Vein'], 'A',
    ['Step 1: the cuticle lies on the outside.', 'Step 2: it is thickest on the upper epidermis, which faces the sun.'], 'Cuticle = raincoat on the top.', [('What is the job of the cuticle?', 'To reduce water loss.')])
d.F(127, 'The pores in the leaf epidermis through which gases pass are called ____.', 'stomata', ['stomata', 'lenticels', 'veins', 'chloroplasts'],
    ['Step 1: tiny pores between guard cells.', 'Step 2: singular stoma, plural stomata.'], 'Stoma = mouth.', [('Where are stomata most numerous in many plants?', 'On the lower epidermis.')])
d.S(127, 'Describe the path of carbon dioxide from the air to a chloroplast in a palisade cell.', 'CO₂ diffuses through an open stoma into the air spaces of the spongy mesophyll, moves through the air channels to the palisade cells, dissolves in the water film on the wet cell walls and diffuses into the cell sap and chloroplasts.',
    ['Step 1: stoma.', 'Step 2: air spaces.', 'Step 3: wet cell wall — dissolves.', 'Step 4: chloroplast.'], 'Name every stop on the route.', [('Which gas moves out along the same path in daylight?', 'Oxygen (and water vapour).')])
d.TF(126, 'Palisade cells are loosely packed with many air spaces.', False,
     ['Step 1: palisade = long cylindrical cells closely arranged, many chloroplasts.', 'Step 2: loosely packed with air spaces = spongy layer → false.'], 'Palisade = soldiers in a row; spongy = sponge with holes.', [('Which layer has the most chloroplasts?', 'The palisade layer.')])
d.M(125, 'Parallel venation is typical of', ['bean leaves', 'monocot leaves', 'sunflower leaves', 'all dicots'], 'B',
    ['Step 1: monocots — parallel veins.', 'Step 2: dicots — branching (net) veins.'], 'Grass blade → straight parallel lines.', [('What is the edge of a leaf blade called?', 'The margin.')])
d.S(127, 'Give four ways in which a leaf is adapted for photosynthesis.', 'Broad flat blade gives a large surface for light; thin so gases diffuse a short distance; palisade cells with many chloroplasts near the upper surface; air spaces in the spongy layer for CO₂; stomata for gas exchange; veins bring water and remove food.',
    ['Step 1: shape.', 'Step 2: thinness.', 'Step 3: chloroplast position.', 'Step 4: air spaces / stomata / veins.'], 'Pair each feature with “so that…”.', [('Why is the upper epidermis transparent?', 'So light passes through to the palisade cells.')])
d.M(127, 'Glucose made in the leaf is quickly converted into', ['protein', 'insoluble starch', 'cellulose only', 'carbon dioxide'], 'B',
    ['Step 1: glucose is soluble and would affect osmosis.', 'Step 2: it is turned into insoluble starch grains for storage.'], 'Store as starch — iodine test turns blue-black.', [('Why is starch better for storage than glucose?', 'It is insoluble, so it does not draw water into the cell by osmosis.')])
d.S(126, 'Name the three parts of a typical dicot leaf and state the function of the petiole.', 'Blade (lamina), petiole and leaf base. The petiole attaches the leaf to the stem, holds the blade out towards the light and carries the vascular tissue (continuing as the midrib).',
    ['Step 1: three parts.', 'Step 2: petiole role.'], 'Lamina–petiole–base, top to bottom.', [('What is a stipule?', 'A small scale-like or leaf-like outgrowth at the base of some leaves.')])

e = QSet('6.4.3 Practice — the flower', 's643')
e.M(128, 'The outermost whorl of a flower is the', ['corolla', 'calyx', 'androecium', 'gynoecium'], 'B',
    ['Step 1: outside → in: calyx, corolla, androecium, gynoecium.', 'Step 2: calyx (sepals) is outermost.'], 'Some People Sing Professionally.', [('What is the function of sepals?', 'They protect the flower in the bud.')])
e.F(129, 'The stamen consists of a filament and an ____.', 'anther', ['anther', 'ovary', 'stigma', 'style'],
    ['Step 1: stamen = male part.', 'Step 2: filament (stalk) + anther (pollen sac).'], 'Anther holds pollen.', [('Name the three parts of the pistil.', 'Stigma, style and ovary.')])
e.M(129, 'A flower that has both stamens and pistil is called', ['incomplete', 'unisexual', 'perfect (bisexual)', 'dioecious'], 'C',
    ['Step 1: essential parts = stamens + pistil.', 'Step 2: both present = perfect/bisexual.'], 'Perfect = has both sexes.', [('What is a flower with all four whorls called?', 'Complete.')])
e.TF(129, 'Papaya is a monoecious plant.', False,
     ['Step 1: in papaya male and female flowers are on different plants.', 'Step 2: that is dioecious → false.'], 'Di = two houses (two plants).', [('Give an example of a monoecious plant.', 'Maize or pumpkin.')])
e.S(130, 'Describe double fertilization in flowering plants.', 'The pollen tube enters the ovule through the micropyle and releases two male nuclei. One male nucleus fuses with the egg nucleus to form the zygote, which becomes the embryo; the second fuses with the two polar nuclei to form the endosperm, the food store. Two fusions occur, so it is called double fertilization; it is found only in flowering plants.',
    ['Step 1: pollen tube delivers two male nuclei.', 'Step 2: fusion 1 → zygote.', 'Step 3: fusion 2 → endosperm.', 'Step 4: name and uniqueness.'], 'Count the fusions: two.', [('What does the generative nucleus divide into?', 'Two male nuclei.')])
e.M(130, 'After fertilization the ovary develops into the', ['seed', 'fruit', 'embryo', 'endosperm'], 'B',
    ['Step 1: ovule → seed.', 'Step 2: ovary → fruit.'], 'OvarY → fruit (bigger word, bigger structure).', [('What does the ovule develop into?', 'The seed.')])
e.S(129, 'Distinguish between pollination and fertilization.', 'Pollination is the transfer of pollen grains from an anther to a stigma of a flower of the same species. Fertilization is the fusion of a male nucleus with the egg nucleus (and, in flowering plants, another male nucleus with the polar nuclei) inside the ovule. Pollination comes first.',
    ['Step 1: define pollination.', 'Step 2: define fertilization.', 'Step 3: order.'], 'Pollination moves pollen; fertilization fuses nuclei.', [('Through which opening does the pollen tube enter the ovule?', 'The micropyle.')])
e.M(130, 'Which part of the pollen grain leads the pollen tube down the style?', ['Generative nucleus', 'Tube nucleus', 'Polar nucleus', 'Antipodal cell'], 'B',
    ['Step 1: the pollen grain has a tube nucleus and a generative nucleus.', 'Step 2: the tube nucleus is associated with growth of the tube; the generative nucleus makes two male nuclei.'], 'Tube nucleus → tube.', [('How many antipodal cells are in the ovule?', 'Three.')])
e.S(129, 'Why do insect-pollinated flowers usually have large, brightly coloured, scented petals?', 'The petals (corolla) attract insect pollinators by their colour and scent. Insects visiting for nectar pick up pollen from the anthers and carry it to the stigma of another flower, bringing about (cross-)pollination.',
    ['Step 1: role of petals — attraction.', 'Step 2: insects move pollen.', 'Step 3: result — pollination.'], 'Structure → attraction → pollination.', [('Which type of pollination gives more variation?', 'Cross-pollination.')])

QS = a.items + b.items + c.items + d.items + e.items
