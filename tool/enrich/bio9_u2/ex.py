from common import Q

QS = []


def M(i, lab, page, q, opts, ans, why, tip, sim):
    QS.append(Q(i, 'mcq', page, q, ans, why, tip, sim, label=lab, options=opts))


def S(i, lab, page, q, ans, why, tip, sim, accept=None):
    QS.append(Q(i, 'short', page, q, ans, why, tip, sim, label=lab, accept=accept))


def F(i, lab, page, q, ans, choices, why, tip, sim):
    QS.append(Q(i, 'fill', page, q, ans, why, tip, sim, label=lab, choices=choices))


def TF(i, lab, page, q, ans, why, tip, sim):
    x = Q(i, 'tf', page, q, ans, why, tip, sim, label=lab)
    QS.append(x)


# ---------------- 2.1
a = '2.1 Practice'
M('p101', a, 55, 'Which rank comes directly between order and genus?', ['Class', 'Family', 'Species', 'Phylum'], 'B',
  ['Step 1: write KPCOFGS — Kingdom, Phylum, Class, Order, Family, Genus, Species.', 'Step 2: find order (O) and genus (G).', 'Step 3: the letter between them is F → Family.'],
  'Write the mnemonic letters across the top of your answer sheet before you start.', [('Which rank comes directly above class?', 'Phylum.')])
M('p102', a, 57, 'Which scientific name is written correctly in print?', ['Zea Mays', 'zea mays', '*Zea mays*', 'ZEA MAYS'], 'C',
  ['Step 1: genus needs a capital — rules out zea mays.', 'Step 2: species needs a small letter — rules out Zea Mays and ZEA MAYS.', 'Step 3: a printed name is in italics — *Zea mays* fits all rules.'],
  'Check three things in order: capital genus, small species, italics/underlining.', [('How is *Acacia tortilis* written the second time in a text?', '*A. tortilis*.')])
S('p103', a, 57, 'List the four rules for writing a scientific name.', '1) One organism has only one scientific name. 2) It has two parts: genus then species. 3) Genus begins with a capital letter, species with a small letter. 4) Italics when printed; genus and species underlined separately when handwritten.',
  ['Step 1: “one” — only one scientific name per organism.', 'Step 2: “two” — two parts, genus first, species second.', 'Step 3: “capital/small” — Genus capital, species small.', 'Step 4: “slanted or lined” — italics in print, separate underlines by hand.'],
  'Remember 1-2-Capital-Italics: one name, two parts, capital first, italics.', [('Write the scientific name of the house fly correctly by hand and say how it is marked.', '*Musca domestica* — by hand, underline Musca and domestica separately.')])
S('p104', a, 56, 'Why do taxonomists avoid common names and use Latin?', 'Common names differ between languages and places, so they are not universal. Latin is no longer changing, so a Latin name is fixed and the same for scientists everywhere.',
  ['Step 1: a common name changes with language — lion is ኣንበሳ in Tigrinya, simba in Swahili.', 'Step 2: one organism could have many local names, and one name could mean different organisms.', 'Step 3: Latin does not change and is used by scientists everywhere → one fixed name worldwide.'],
  'Give an example with two languages — examiners like a concrete example.', [('Why is the aloe found near Massawa called *Aloe massawana*?', 'The place name was Latinised to make the species name.')])
M('p105', a, 55, 'Which statement about the hierarchy is correct?', ['Members of a kingdom are more alike than members of a genus', 'Moving from kingdom to species, groups get smaller and members more alike', 'A species contains several genera', 'Order is larger than class'], 'B',
  ['Step 1: species is the smallest, most specific group.', 'Step 2: kingdom is the biggest, least specific group.', 'Step 3: so going down, size decreases and similarity increases → B.', 'Step 4: A, C and D reverse the order.'],
  'Draw the pyramid: wide top (kingdom), narrow bottom (species).', [('Which group has more different kinds of organisms: a phylum or a family?', 'A phylum — it is a higher rank and contains many families.')])
S('p106', a, 56, 'Classify a human up to species level.', 'Kingdom Animalia, Phylum Chordata, Class Mammalia, Order Primates, Family Hominidae, Genus *Homo*, Species *sapiens* — *Homo sapiens*.',
  ['Step 1: kingdom — multicellular, no cell wall, ingests food → Animalia.', 'Step 2: phylum — backbone → Chordata.', 'Step 3: class — hair, milk → Mammalia.', 'Step 4: order Primates, family Hominidae.', 'Step 5: genus *Homo*, species *sapiens*.'],
  'Say KPCOFGS aloud and fill one rank per step.', [('Classify maize up to species level.', 'Plantae, Angiospermae, Monocotyledon, Commelinales, Poaceae, *Zea*, *mays*.')])
TF('p107', a, 55, 'Members of the same genus can always interbreed to produce fertile offspring.', False,
   ['Step 1: fertile offspring is the test for the **same species**.', 'Step 2: members of the same genus may interbreed, but the offspring may be infertile — the mule (horse × donkey).', 'Step 3: so the statement is false.'],
   'Mule = genus-level cross. Fertile = species.', [('Can two members of the same species produce fertile offspring?', 'Yes — that is what defines a species.')])

# ---------------- 2.2
a = '2.2 Practice'
M('p201', a, 58, 'Each pair of statements in a dichotomous key is called a', ['taxon', 'couplet', 'clade', 'lead'], 'B',
  ['Step 1: dichotomous = cut into two.', 'Step 2: a pair of mutually exclusive statements = a couplet.'], 'Couple = two → couplet.', [('What does “mutually exclusive” mean in a key?', 'Only one of the two statements can be true for the specimen.')])
M('p202', a, 59, 'Using the textbook key, an animal that is terrestrial, wingless, plant eating and has an undivided hoof is a', ['cow', 'goat', 'donkey', 'hyena'], 'C',
  ['Couplet 1: terrestrial → 2.', 'Couplet 2: wingless → 3.', 'Couplet 3: plant eating → 4.', 'Couplet 4: undivided hoof → donkey.'],
  'Always start at couplet 1 and write the path (1→2→3→4).', [('Which animal is terrestrial, wingless and flesh eating?', 'Hyena.')])
S('p203', a, 58, 'Give the four steps for constructing a dichotomous key.', 'a) List the main features of the organisms, especially those that make each one unique. b) Arrange the features in pairs. c) For each pair, write either the organism’s name or the number of the next couplet. d) Continue until every organism is named.',
  ['Step 1: features first (observe).', 'Step 2: pair them as opposites.', 'Step 3: link each statement to a name or a number.', 'Step 4: repeat until all are named.'],
  'List → Pair → Link → Repeat.', [('Why should keys use permanent, visible features?', 'So anyone can check them on any specimen; colour or size may change with age.')])
M('p204', a, 59, 'A key for 12 organisms needs at least how many couplets?', ['6', '11', '12', '24'], 'B',
  ['Step 1: each couplet names one organism and passes the rest on.', 'Step 2: n organisms → n − 1 couplets.', 'Step 3: 12 − 1 = 11.'], 'n − 1 rule.', [('How many couplets for 6 animals?', '5 — as in the textbook key.')])
M('p205', a, 58, 'Which is the best couplet for a key?', ['Big / brown', 'Legs present / legs absent', 'Pretty / ugly', 'Common / rare'], 'B',
  ['Step 1: a couplet must be two opposite states of the same, visible feature.', 'Step 2: only “legs present / legs absent” is observable and mutually exclusive.'],
  'If two people could disagree on it, it is a bad couplet.', [('Is “dangerous / harmless” a good couplet? Why?', 'No — it is not a visible structural feature and people may disagree.')])
S('p206', a, 60, 'Turn couplet 2 of the textbook key into a question with its two answers.', 'Are wings present? Yes → the animal is a bat. No → go to couplet 3.',
  ['Step 1: take the feature (wings).', 'Step 2: ask “present?”', 'Step 3: give the Yes outcome (bat) and the No outcome (go to 3).'],
  'Every couplet becomes one yes/no question.', [('Turn couplet 1 into a question.', 'Is the animal aquatic and breathing with gills? Yes → fish. No → go to 2.')])

# ---------------- 2.3
a = '2.3 Practice'
M('p301', a, 61, 'Which kingdom consists of prokaryotes?', ['Protista', 'Monera', 'Fungi', 'Plantae'], 'B',
  ['Step 1: prokaryote = no true nucleus.', 'Step 2: only bacteria and cyanobacteria lack a nucleus → Monera.'], 'Monera = “no nucleus”.', [('Name the two groups in kingdom Monera.', 'Bacteria and cyanobacteria.')])
F('p302', a, 61, 'A plant cell wall is made of ____, while that of fungi is made of chitin.', 'cellulose', ['cellulose', 'protein', 'starch'],
  ['Step 1: recall why fungi were separated from plants.', 'Step 2: walls differ chemically: plant = cellulose, fungi = chitin.'], 'C for Cellulose and Chlorophyll (plants); chitin for fungi.', [('Which kingdom has no cell wall?', 'Animalia.')])
S('p303', a, 63, 'Compare the five kingdoms by cell type and nutrition.', 'Monera: prokaryotic; autotrophic or heterotrophic. Protista: eukaryotic, mostly unicellular; autotrophic (algae) or heterotrophic (protozoa, slime moulds). Fungi: eukaryotic; heterotrophic, absorb food. Plantae: eukaryotic multicellular; autotrophic (photosynthesis). Animalia: eukaryotic multicellular; heterotrophic, ingest food.',
  ['Step 1: cell type — only Monera prokaryotic; all others eukaryotic.', 'Step 2: nutrition — make (plants, algae, some monera), absorb (fungi), ingest (animals, protozoa).', 'Step 3: write one line per kingdom.'],
  'Use a table in the exam — it is faster and clearer.', [('Which two kingdoms contain autotrophs that are eukaryotic?', 'Protista (algae) and Plantae.')])
M('p304', a, 61, 'Which pair is correctly matched?', ['Animalia — chitin wall', 'Fungi — ingest food', 'Plantae — cellulose wall', 'Monera — true nucleus'], 'C',
  ['Step 1: animals have no wall → A wrong.', 'Step 2: fungi absorb, not ingest → B wrong.', 'Step 3: plants have cellulose walls → C right.', 'Step 4: Monera have no true nucleus → D wrong.'],
  'Check each option against the kingdom table one by one.', [('Which kingdom absorbs digested food?', 'Fungi.')])
TF('p305', a, 61, 'Viruses belong to kingdom Monera because they are very small.', False,
   ['Step 1: kingdoms group cellular organisms.', 'Step 2: viruses are not cells — DNA or RNA in a protein coat — and reproduce only inside host cells.', 'Step 3: they are not placed in any kingdom.'],
   'Small size is not a classification feature; cell structure is.', [('Name two features that make viruses look non-living.', 'They are not cells and they can be crystallised; no metabolism outside a host.')])
M('p306', a, 61, 'In the three-domain system, fungi, plants and animals are all placed in domain', ['Bacteria', 'Archaea', 'Eukarya', 'Protista'], 'C',
  ['Step 1: domains are Bacteria, Archaea, Eukarya.', 'Step 2: fungi, plants and animals have eukaryotic cells → Eukarya.'], 'Eu-karya = true nucleus.', [('Which domains contain prokaryotes?', 'Bacteria and Archaea.')])

# ---------------- 2.3.1
a = '2.3.1 Practice'
S('p401', a, 64, 'Describe binary fission in bacteria.', 'The cell elongates; its chromosome duplicates; the cytoplasm divides into two and a new wall forms, giving two daughter cells, which grow and divide again every 20–30 minutes.',
  ['Step 1: elongate.', 'Step 2: duplicate DNA.', 'Step 3: divide cytoplasm and form a cross wall.', 'Step 4: two daughter cells, repeat in 20–30 min.'],
  'Grow → Copy → Split → Repeat.', [('Name the primitive sexual process seen in *E. coli*.', 'Conjugation — transfer of genetic material.')])
S('p402', a, 64, 'Distinguish chemosynthetic from photosynthetic bacteria.', 'Both make their own food (autotrophs). Photosynthetic bacteria use light energy; chemosynthetic bacteria use chemical energy from inorganic substances such as ammonia, hydrogen sulphide or hydrogen.',
  ['Step 1: same — both autotrophs, carbon from CO₂.', 'Step 2: different — energy source.', 'Step 3: photo = light; chemo = inorganic chemicals.'],
  'Always say what is the same before what is different.', [('Nitrifying bacteria are examples of which type?', 'Chemoautotrophs.')])
M('p403', a, 115, 'Organisms that obtain energy by oxidising inorganic chemicals are', ['heterotrophs', 'decomposers', 'chemoautotrophs', 'photoautotrophs'], 'C',
  ['Step 1: “inorganic” + make own food → autotroph.', 'Step 2: energy from chemicals, not light → chemoautotroph.'], 'Chemo = chemicals.', [('What do photoautotrophs use for energy?', 'Light.')])
S('p404', a, 66, 'Explain fragmentation with an example.', 'In fragmentation a filament breaks into pieces and each piece grows into a new organism. Example: filamentous cyanobacteria.',
  ['Step 1: define — breaking into fragments.', 'Step 2: each fragment grows into a new individual (asexual).', 'Step 3: example — cyanobacteria filaments (sponges also fragment).'],
  'Define + example = full marks.', [('Do cyanobacteria reproduce sexually?', 'No — only by cell division or fragmentation.')])
M('p405', a, 66, 'Which is TRUE of cyanobacteria?', ['They have flagella', 'They release oxygen in photosynthesis', 'They have a true nucleus', 'They reproduce sexually'], 'B',
  ['Step 1: they lack flagella → A wrong.', 'Step 2: they photosynthesise like plants and release O₂ → B right.', 'Step 3: prokaryotes, no true nucleus → C wrong; asexual only → D wrong.'], 'Cyano = blue; think “blue-green, gives O₂”.', [('What else can many cyanobacteria fix from the air?', 'Nitrogen.')])
M('p406', a, 64, 'Saprophytic bacteria obtain food from', ['living hosts', 'dead organic matter', 'sunlight', 'ammonia'], 'B',
  ['Step 1: sapro = rotten/dead.', 'Step 2: saprophytes feed on dead matter and waste → decomposers.'], 'Sapro = dead, para = beside a living host.', [('What do parasitic bacteria feed on?', 'A living host.')])

# ---------------- 2.3.2
a = '2.3.2 Practice'
S('p501', a, 76, 'What feature identifies a protist as plant-like, animal-like or fungus-like?', 'Its mode of nutrition: plant-like protists (algae) photosynthesise; animal-like protists (protozoa) ingest food; fungus-like protists (slime moulds) absorb food.',
  ['Step 1: the three groups are split by nutrition.', 'Step 2: make food → algae.', 'Step 3: ingest → protozoa.', 'Step 4: absorb → slime moulds.'], 'Make / Ingest / Absorb.', [('Which group does *Euglena* belong to?', 'Plant-like protists (algae).')])
S('p502', a, 68, 'What type of protist is *Paramecium*? Give its distinguishing characteristics.', 'Animal-like protist (phylum Ciliophora). Covered by rows of cilia; oral groove leading to mouth pore and gullet; a small micronucleus and a large macronucleus; two contractile vacuoles; binary fission and conjugation.',
  ['Step 1: movement by cilia → Ciliophora (protozoa).', 'Step 2: list structures — cilia, oral groove, two nuclei, two contractile vacuoles.', 'Step 3: reproduction — binary fission, conjugation.'], 'Give at least three structures for “distinguishing characteristics”.', [('What is the role of the contractile vacuole?', 'Removes excess water from the cytoplasm.')])
S('p503', a, 69, 'How does *Trypanosoma* affect humans?', 'It causes African sleeping sickness, spread by the tsetse fly: irregular fever, swelling and skin eruptions, then headache, convulsions, coma and death; first in the blood, later in the nervous system.',
  ['Step 1: name the disease.', 'Step 2: name the vector — tsetse fly.', 'Step 3: list symptoms in order.'], 'Disease + vector + symptoms.', [('Which protist causes amoebic dysentery?', '*Entamoeba histolytica*.')])
M('p504', a, 70, 'Which *Plasmodium* species causes malignant malaria?', ['*P. vivax*', '*P. falciparum*', '*P. ovale*', '*P. malariae*'], 'B',
  ['Step 1: *P. vivax* — benign (mild), every 48 h.', 'Step 2: *P. falciparum* — malignant (harmful), every 36–48 h.'], 'Falciparum = fatal-ciparum.', [('Which two Plasmodium species are common in Eritrea?', '*P. vivax* and *P. falciparum*.')])
F('p505', a, 72, '*Chlamydomonas* is an example of a unicellular ____ green alga.', 'biflagellate', ['biflagellate', 'filamentous', 'colonial'],
  ['Step 1: *Chlamydomonas* has two flagella.', 'Step 2: two flagella = biflagellate.'], 'Bi = two.', [('Which green alga is filamentous with a spiral chloroplast?', '*Spirogyra*.')])
M('p506', a, 74, 'The thick-walled structure formed after conjugation in *Spirogyra* is the', ['cyst', 'zygospore', 'pyrenoid', 'holdfast'], 'B',
  ['Step 1: conjugation → nuclei fuse → zygote.', 'Step 2: zygote gets a thick coat → zygospore.'], 'Zygote + spore = zygospore.', [('What anchors *Ulva* to the sea floor?', 'A holdfast.')])
M('p507', a, 71, 'Phytoplankton are important because they', ['cause malaria', 'are the primary food source of aquatic animals', 'decompose dead fish', 'fix nitrogen in soil'], 'B',
  ['Step 1: phytoplankton = photosynthetic unicellular algae in plankton.', 'Step 2: they make food that aquatic animals eat → primary food source.'], 'Phyto = plant: producers.', [('What are zooplankton?', 'The tiny animals of the plankton.')])

# ---------------- 2.3.3
a = '2.3.3 Practice'
S('p601', a, 81, 'List the common characteristics of fungi.', 'Eukaryotic; mostly filamentous (hyphae forming a mycelium), some unicellular (yeast); cell walls of chitin; no chlorophyll; heterotrophic — secrete enzymes and absorb food (saprophytes, parasites or partners in lichens); reproduce by non-motile spores, sexually and asexually; important decomposers.',
  ['Step 1: structure — hyphae, mycelium, chitin.', 'Step 2: nutrition — no chlorophyll, absorb.', 'Step 3: reproduction — spores.', 'Step 4: role — decomposers.'], 'Structure, Nutrition, Reproduction, Role — four headings.', [('Give one distinguishing feature of Basidiomycota.', 'Spores on a club-shaped basidium, four basidiospores each.')])
M('p602', a, 77, '*Rhizopus* belongs to', ['Ascomycota', 'Basidiomycota', 'Zygomycota', 'Deuteromycota'], 'C',
  ['Step 1: *Rhizopus* = black bread mould.', 'Step 2: hyphae without cross walls; sexual reproduction by conjugation → zygosporangium → Zygomycota.'], 'Zebras Always Bite Donkeys: Z for Rhizopus.', [('To which phylum does yeast belong?', 'Ascomycota.')])
M('p603', a, 78, 'An ascus of a typical sac fungus contains', ['two spores', 'four basidiospores', 'eight ascospores', 'many zygospores'], 'C',
  ['Step 1: ascus = sac (Ascomycota).', 'Step 2: each ascus usually holds eight ascospores (yeast forms four).'], 'Sac 8, club 4.', [('How many spores does a basidium carry?', 'Four basidiospores.')])
S('p604', a, 81, 'Describe the fungal and algal association in a lichen.', 'Mutualism: the fungus holds water to keep the alga moist, digests the rock to release minerals and protects the alga; the alga photosynthesises and makes food for both.',
  ['Step 1: name the relationship — mutualism (both benefit).', 'Step 2: fungus gives water, minerals, protection.', 'Step 3: alga gives food by photosynthesis.'], 'Say what EACH partner gives.', [('What is mutualism?', 'A symbiosis in which both partners benefit.')])
S('p605', a, 81, 'How do fungal pathogens affect the way people live?', 'They cause human diseases (thrush by *Candida albicans*; ringworm and athlete’s foot by dermatophytes) and crop diseases (blight in potatoes and tomatoes; rust in wheat, barley and oats; downy mildew), causing great economic losses for farmers.',
  ['Step 1: human health examples.', 'Step 2: crop examples.', 'Step 3: consequence — food loss, money loss.'], 'Two human + two crop examples is a strong answer.', [('Name a useful product of fungi.', 'Penicillin, bread, beer, wine, edible mushrooms.')])
TF('p606', a, 80, 'Deuteromycota are fungi in which sexual reproduction is unknown.', True,
   ['Step 1: deutero = “imperfect fungi”.', 'Step 2: called imperfect because no sexual stage is known.', 'Step 3: when one is found, they are moved to Ascomycota or Basidiomycota.'], 'Imperfect = missing the sexual “perfect” stage.', [('What happens when a sexual stage is discovered?', 'The fungus is moved to Ascomycota or Basidiomycota.')])
S('p607', a, 82, 'List three differences between fungi and plants.', 'Fungi: chitin walls, no chlorophyll, absorb food (heterotrophic), body of hyphae. Plants: cellulose walls, chlorophyll, photosynthesis (autotrophic), roots, stems and leaves.',
  ['Step 1: wall chemistry.', 'Step 2: chlorophyll and nutrition.', 'Step 3: body structure or food store.'], 'Write as pairs: “Fungi …, whereas plants …”.', [('Why were fungi once placed with plants?', 'Because they have cell walls.')])

# ---------------- 2.3.4
a = '2.3.4 Practice'
S('p701', a, 82, 'Describe the life cycle of plants (alternation of generations).', 'The sporophyte produces spores; a spore grows into a gametophyte; the gametophyte produces gametes; two gametes fuse to form a zygote; the zygote grows into a new sporophyte.',
  ['Step 1: sporophyte → spores.', 'Step 2: spore → gametophyte.', 'Step 3: gametophyte → gametes.', 'Step 4: gametes fuse → zygote → sporophyte.'], 'Draw it as a circle with four arrows.', [('Which generation is dominant in ferns?', 'The sporophyte.')])
S('p702', a, 84, 'What are the general characteristics of pteridophytes?', 'Seedless vascular plants (ferns, club mosses, horsetails) with true roots, stems and leaves; underground rhizome; leaves called fronds; reproduce by spores; dominant sporophyte; independent heart-shaped gametophyte (prothallus).',
  ['Step 1: vascular but seedless.', 'Step 2: true organs; rhizome; fronds.', 'Step 3: life cycle — dominant sporophyte, independent prothallus.'], 'Vascular + seedless are the two key words.', [('What is a prothallus?', 'The small heart-shaped gametophyte of a fern.')])
S('p703', a, 86, 'Compare monocots and dicots (four differences).', 'Monocots: one cotyledon, parallel veins, flower parts in threes, fibrous roots, scattered vascular bundles (teff, maize). Dicots: two cotyledons, net veins, parts in fours or fives, tap root, bundles in a ring (beans, chickpeas).',
  ['Step 1: seed — 1 vs 2 cotyledons.', 'Step 2: leaf veins.', 'Step 3: flower parts.', 'Step 4: roots and vascular bundles.'], 'Use a two-column table.', [('Is sorghum a monocot or dicot?', 'Monocot.')])
M('p704', a, 115, 'In mosses, spores are produced inside the', ['thallus', 'capsule', 'sori', 'gemmae'], 'B',
  ['Step 1: the moss sporophyte grows on the gametophyte.', 'Step 2: its tip is a capsule that releases spores.', 'Step 3: sori are on fern fronds.'], 'Moss → capsule; fern → sori.', [('Where are spores produced in a fern?', 'In sori on the underside of the frond.')])
M('p705', a, 85, 'In angiosperms the seed is enclosed in a fruit that develops from the', ['cone scale', 'ovary wall', 'rhizome', 'prothallus'], 'B',
  ['Step 1: seeds develop in the ovary at the base of the flower.', 'Step 2: the ovary wall matures into the fruit.'], 'Angio = vessel/case: seed in a case.', [('How many species of flowering plants are there?', 'More than 250 000.')])
M('p706', a, 84, 'Which plant group has seeds but no flowers?', ['Bryophytes', 'Pteridophytes', 'Gymnosperms', 'Angiosperms'], 'C',
  ['Step 1: bryophytes and pteridophytes — no seeds.', 'Step 2: angiosperms — seeds and flowers.', 'Step 3: gymnosperms — naked seeds on cones, no flowers.'], 'Brave Pupils Get A’s — seeds start at G, flowers at A.', [('Name the two kinds of pine cones.', 'Staminate (male, small) and ovulate (female, large) cones.')])

# ---------------- 2.3.5 A
a = '2.3.5 Invertebrates practice'
M('p801', a, 89, 'Which animals are asymmetrical?', ['Jellyfish', 'Sponges', 'Starfish', 'Earthworms'], 'B',
  ['Step 1: jellyfish and starfish — radial.', 'Step 2: earthworms — bilateral.', 'Step 3: sponges — no symmetry.'], 'Simplest animal = no symmetry.', [('Name two radially symmetrical phyla.', 'Cnidaria and Echinodermata.')])
M('p802', a, 90, 'The stinging cells of cnidarians are', ['spicules', 'nematocysts', 'setae', 'choanocytes'], 'B',
  ['Step 1: spicules — sponge needles.', 'Step 2: setae — annelid bristles.', 'Step 3: choanocytes — sponge collar cells.', 'Step 4: nematocysts — cnidarian stinging cells on tentacles.'], 'Nemato-cyst: sting “thread capsule”.', [('Name the two body forms of cnidarians.', 'Polyp and medusa.')])
S('p803', a, 92, 'Why does a tapeworm not need a digestive system?', 'It lives in the host’s intestine, surrounded by food the host has already digested, and absorbs these soluble nutrients through its body surface.',
  ['Step 1: where it lives — intestine.', 'Step 2: what surrounds it — digested food.', 'Step 3: how it feeds — absorbs through body surface.'], 'Habitat explains structure.', [('What is the scolex for?', 'Attachment to the host’s gut.')])
M('p804', a, 96, 'Which group of arthropods has four pairs of legs and no antennae?', ['Insects', 'Crustaceans', 'Arachnids', 'Myriapods'], 'C',
  ['Step 1: four pairs = 8 legs.', 'Step 2: no antennae, cephalothorax + abdomen → arachnids (spiders, scorpions, ticks, mites).'], '8 legs like the 8 letters in “arachnid”? Count: a-r-a-c-h-n-i-d = 8!', [('How many pairs of antennae do crustaceans have?', 'Two pairs.')])
S('p805', a, 101, 'Distinguish complete and incomplete metamorphosis with examples.', 'Incomplete: egg → nymph → adult (three stages), e.g. grasshopper. Complete: egg → larva → pupa → adult (four stages), e.g. butterfly, house fly.',
  ['Step 1: define metamorphosis — marked change of form during growth.', 'Step 2: incomplete — 3 stages, nymph.', 'Step 3: complete — 4 stages, larva and pupa.'], 'Pupa present = complete.', [('In which type do young look like small adults?', 'Incomplete (nymphs).')])
M('p806', a, 102, 'The water vascular system is found in', ['molluscs', 'echinoderms', 'annelids', 'cnidarians'], 'B',
  ['Step 1: unique to echinoderms (starfish, sea urchins).', 'Step 2: used in feeding, locomotion, respiration, sensing.'], 'Echino = spiny skin, water feet.', [('Do echinoderms have a brain?', 'No — no head, eyes or brain.')])
M('p807', a, 93, 'The part of a mollusc that secretes the shell is the', ['foot', 'radula', 'mantle', 'visceral mass'], 'C',
  ['Step 1: foot — movement; radula — scraping; visceral mass — organs.', 'Step 2: mantle — fold over the visceral mass that secretes the shell.'], 'Mantle = a coat that builds the shell.', [('What is a radula?', 'A toothed structure for scraping food or rock.')])

# ---------------- 2.3.5 B
a = '2.3.5 Vertebrates practice'
S('p901', a, 103, 'How do vertebrates differ from other animals?', 'They have a true, usually bony, endoskeleton with a backbone around the spinal cord and a skull around the brain; invertebrates have no backbone.',
  ['Step 1: name the key structure — backbone.', 'Step 2: add skull and endoskeleton.'], 'Back-bone + brain-box (skull).', [('Name the five vertebrate classes.', 'Fishes, amphibians, reptiles, birds, mammals.')])
S('p902', a, 106, 'Explain why reptiles were among the first vertebrates fully adapted to land.', 'Dry waterproof scaly skin reduces water loss; they breathe only by lungs; fertilisation is internal; eggs have shells, so they do not need water to reproduce.',
  ['Step 1: water loss — scaly skin.', 'Step 2: breathing — lungs.', 'Step 3: reproduction — internal fertilisation, shelled eggs.'], 'Skin, lungs, eggs — three points.', [('Why must frogs return to water to breed?', 'External fertilisation and eggs without shells; tadpoles live in water.')])
S('p903', a, 103, 'Differentiate between internal and external fertilisation.', 'External: sperm and eggs fuse outside the female’s body, usually in water (most fishes, frogs). Internal: fusion inside the female’s body (sharks, reptiles, birds, mammals).',
  ['Step 1: define each by where the gametes meet.', 'Step 2: give examples of each.'], 'Out = water animals, In = land animals (mostly).', [('Which fish uses internal fertilisation?', 'Sharks.')])
M('p904', a, 107, 'Which feature is unique to birds?', ['Four-chambered heart', 'Feathers', 'Laying eggs', 'Being warm-blooded'], 'B',
  ['Step 1: mammals also have four chambers and are warm-blooded.', 'Step 2: reptiles and monotremes lay eggs.', 'Step 3: only birds have feathers.'], '“Unique” = no other class has it.', [('Give three functions of feathers.', 'Insulation, flight, waterproofing (also UV protection, colour).')])
M('p905', a, 112, 'The kangaroo is an example of a', ['monotreme', 'marsupial', 'placental mammal', 'reptile'], 'B',
  ['Step 1: monotremes lay eggs (platypus).', 'Step 2: marsupials have a short placenta then a pouch → kangaroo.'], 'Marsupial = pouch.', [('Name an egg-laying mammal.', 'Platypus or spiny anteater.')])
F('p906', a, 103, 'Fishes are animals with a variable body temperature, known as ____.', 'poikilothermic', ['poikilothermic', 'homoeothermic', 'hermaphrodite'],
  ['Step 1: variable temperature = cold-blooded.', 'Step 2: the term is poikilothermic.'], 'Poikilo = changing.', [('What are animals with a constant body temperature called?', 'Homoeothermic.')])
M('p907', a, 111, 'An animal with long, flat grinding teeth is most likely a', ['carnivore', 'herbivore', 'insectivore', 'parasite'], 'B',
  ['Step 1: teeth match diet.', 'Step 2: grinding plant material needs flat teeth → herbivore.'], 'Look at teeth → know the diet.', [('Give two examples of omnivorous mammals.', 'Humans and pigs.')])
