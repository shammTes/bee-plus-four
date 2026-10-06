"""biology 9-12: replace textbook pointers / attributions with self-contained wording"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *

# ---------------- Grade 9
B = Book('biology_9')
B.sub(' — (Advanced note: plant cells have lysosome-like vacuoles, but the Grade 9 textbook treats lysosomes and centrioles as animal-only.)',
      ' — At Grade 9 level lysosomes and centrioles are treated as animal-cell organelles (plant vacuoles do a similar job to lysosomes).')
B.sub("the textbook's 'three basic structures' refers to the typica", "the 'three basic structures' refer to the typica")
B.sub("Note: the textbook speaks of 'water concentration'", "Note: osmosis can be described with 'water concentration'")
B.sub('A and C are textbook statements, and D', 'A and C are correct statements, and D')
B.sub("Textbook: 'The Red Sea periodically becomes red when the species [of cyanobacteria] bearing red pigment is abundant.'",
      'The Red Sea is named after blooms of a cyanobacterium (Trichodesmium) with red pigment that periodically colour the water.')
B.sub('Note: the textbook speaks of SEVEN ranks', 'Note: the classification hierarchy has SEVEN main ranks')
B.save()

# ---------------- Grade 10
B = Book('biology_10')
B.set('bio10-u1-wrk1', title='Worked example: daily energy needs',
      problem='An 18-year-old male needs about 14 200 kJ of energy per day. One day he eats breakfast (2 500 kJ), lunch (4 800 kJ) and dinner (4 200 kJ). Has he met his energy requirement? If not, how much more does he need?',
      steps=[{'text': 'Step 1: add the energy eaten: 2 500 + 4 800 + 4 200 = 11 500 kJ.'},
             {'text': 'Step 2: compare with the requirement: 14 200 − 11 500 = 2 700 kJ.'},
             {'text': 'Step 3: he is 2 700 kJ short. If this continued, his body would use stored fat (and later protein) for energy and he would lose mass.'},
             {'text': 'Note: an 18-year-old female needs about 9 600 kJ per day; energy needs depend on age, sex, body size and activity.'}],
      answer='No — he needs about 2 700 kJ more.')
B.set('bio10-u1-chk3', q='An 18-year-old male needs about 14 200 kJ per day, but an 18-year-old female needs about 9 600 kJ. What is the main reason for the difference?',
      options={'A': 'Males usually have a larger body mass with more muscle, so a higher metabolic rate', 'B': 'Females do not respire', 'C': 'Males cannot store fat', 'D': 'Females digest food twice as efficiently'},
      answer='A', why='Energy needs depend on body size, muscle mass, growth and activity. On average males have a larger body and more muscle tissue, which respires more, so they need more energy each day. Both sexes respire and store fat.')
B.sub("Bone marrow is not in the textbook's list of lymphatic organs, although it produces the lymphocytes (in wider biology it is a primary lymphoid organ). D is therefore also defensible from the textbook list.",
      'A macrophage is a single white blood cell, not an organ. (Bone marrow produces lymphocytes and is counted as a primary lymphoid organ in wider biology; the intended answer is E.)')
B.sub('Textbook (G10 p.176–177): 12 pairs', '12 pairs')
B.save()

# ---------------- Grade 11
B = Book('biology_11')
B.sub('Schematic body — not to scale. Coloured dots are the textbook glands.', 'Schematic body — not to scale. Coloured dots mark the main endocrine glands.')
B.set('bio11-u1-c02', body=['Tap a gland on the figure to see what it secretes.',
      'The main endocrine glands are the **hypothalamus** and **pituitary** (in the head; the pituitary is the "master gland" that controls other glands), the **thyroid** and **parathyroids** (neck), the **thymus** (chest), the **adrenal glands** (on top of the kidneys), the **islets of Langerhans** in the pancreas, and the **gonads** — ovaries and testes.',
      'Endocrine glands are ductless: they release hormones straight into the blood, which carries them to target organs.'])
B.sub('**Contraception** in the book:', '**Contraception** methods:')
B.sub('The textbook: in the islets of Langerhans, the alpha cells secrete glucagon and the beta cells secrete insulin.', 'In the islets of Langerhans, the alpha cells secrete glucagon and the beta cells secrete insulin (a protein hormone that lowers blood glucose).')
B.sub("Strictly, the textbook adds that the posterior pituitary 'does not produce hormones, but it does store and release' ADH and oxytocin", 'Strictly, the posterior pituitary does not produce hormones; it stores and releases ADH and oxytocin')
B.sub("The textbook: bones are made up of three tissue layers – periosteum, compact bone and spongy bone. 'The periosteum is a smooth, double-layered tissue, which covers the bone.'",
      'Bone has three tissue layers: the periosteum (a smooth, double-layered membrane covering the outside, with blood vessels and nerves), compact bone and spongy bone.')
B.sub('Textbook: bone develops from cartilage', 'Bone develops from cartilage')
B.sub("The textbook: 'Cartilage is gradually converted to bone by a process called ossification.' Answer: C.", 'Ossification is the gradual replacement of cartilage by bone tissue, as bone cells deposit calcium phosphate. Answer: C.')
B.sub("Textbook (G11 pp.78–79): cardiac muscle 'can continue to function without being stimulated by nerve impulses. Their contractions are also not initiated by the nervous system, but generated within the muscle tissue itself' (auto-rhythmic, pacemaker).",
      'Cardiac muscle can keep contracting without nerve impulses: its contractions start within the muscle itself (it is myogenic; the pacemaker sets the rhythm).')
u4 = B.unit('bio11-u4')['exercise']['questions']
for q, w in zip(u4[5:8], ['Muscle tissue is made of long fibres (cells) containing protein filaments that slide over each other, so the muscle can contract (shorten) and relax.',
                          'Muscles are attached to bones by tendons across joints; when a muscle contracts it pulls the bone, and antagonistic pairs (e.g. biceps and triceps) move it back and forth.',
                          'Motor nerves carry impulses from the brain and spinal cord to the muscles, and the cerebellum coordinates which muscles contract and when, so movements are smooth.']):
    q['why'] = [w]
B.sub('All four statements match the textbook. Answer: E.', 'All four statements are correct. Answer: E.')
B.save()

# ---------------- Grade 12
B = Book('biology_12')
B.sub('Figure N2. Base pairing. The textbook draws this as a twisted ladder (double helix).', 'Base pairing in DNA. In the real molecule the ladder is twisted into a double helix.')
B.set('bio12-u1-c12', title='Did you know?')
B.sub('Role in the textbook’s three functions', 'Role in protein synthesis')
B.sub('Textbook statement of the central dogma:', 'The central dogma of molecular biology:')
B.sub('(semi-conservative — the idea implied by the textbook diagrams)', '(semi-conservative replication)')
B.sub('Eukaryotic rate given in the book: 500–5000 base pairs per minute.', 'In eukaryotes DNA is copied at about 500–5 000 base pairs per minute at each replication fork.')
B.set('bio12-u1-c21', title='Think about it: DNA replication')
B.set('bio12-u1-c23', body=['Some books call the DNA strand that is transcribed the “sense” or coding strand. In modern usage the **template (antisense) strand** is the one RNA polymerase reads; the mRNA has the same sequence as the **coding strand**, except that U replaces T. Whatever the name used, mRNA is always complementary to the strand that was read.'])
B.set('bio12-u1-c24', title='C. Translation (four steps)')
B.sub('UAA is a stop codon — translation ends here (Exercise 1.1 Q5).', 'UAA is a stop codon — translation ends here.')
B.set('bio12-u1-c28', title='Interphase (six key points)')
B.sub('Human examples in the book:', 'Human examples of inherited traits:')
B.sub('This is the monohybrid ratio Mendel found across all seven traits (Table 1.6 in the book).', 'Mendel found this ratio for all seven pea traits he studied (e.g. 787 tall : 277 dwarf ≈ 2.84 : 1).')
B.sub('The 16-box Punnett square in textbook Figure 1.20 is the one you must be able to draw.', 'Combining these four gametes from each parent gives a 16-box Punnett square — be able to draw it.')
B.sub('Classic textbook example:', 'Classic example:')
B.set('bio12-u1-c58', title='Worked example: blood-group inheritance')
B.sub('Textbook example: AB blood group', 'Example: AB blood group')
B.set('bio12-u1-c65', body=['Humans have 23 pairs of chromosomes: 22 pairs of autosomes and one pair of **sex chromosomes**. Females are **XX**, males are **XY**.',
      'All eggs carry an X chromosome; half the sperm carry X and half carry Y. X sperm + egg → XX (girl); Y sperm + egg → XY (boy). So the father determines the sex of the child, and the expected ratio is **1 female : 1 male**.',
      '**Sex-linked characters** are controlled by genes on the X chromosome (e.g. red–green colour blindness, haemophilia). A male has only one X, so a single recessive allele shows in him; a female needs two copies, so she is usually a carrier (XᴴXʰ).'])
B.sub('Down’s syndrome as described in the textbook is caused by:', 'Down’s syndrome is caused by:')
B.sub('**Down’s syndrome** (textbook): extra chromosome 21', '**Down’s syndrome**: extra chromosome 21')
B.sub('The textbook presents both as historical views that students should be able to describe.', 'You should be able to describe both views and how they explain the variety of life.')
B.sub('Five points as in the book:', 'His theory has five main points:')
B.sub('Each step is one of the five points of Darwin’s theory in the textbook.', 'Each step is one of the five points of Darwin’s theory.')
B.set('bio12-u2-c09', title='Criticisms of Darwin’s theory')
B.sub('What the textbook emphasises', 'Key idea')
B.sub('Other isolating mechanisms in the book:', 'Other isolating mechanisms:')
B.sub('✓ Use the textbook wording for definitions.', '✓ Learn exact definitions (gene, allele, genotype, phenotype, species).', )
B.sub('Textbook idea', 'Example')
B.sub('The biome not found in Africa, according to the textbook review, is:', 'Which biome is NOT found in Africa?')
B.save()
