"""Unit 1 practice questions (unit exercise), 8+ per sub-unit, each with step-by-step answer, tip and similar questions."""
from common import set_unit, QSet

set_unit('bio11-u1')

a = QSet('1.1.1 Practice — pituitary', 's111')
a.M(3, 'Which hormone is NOT made by the anterior pituitary?', ['GH', 'TSH', 'Oxytocin', 'FSH'], 'C',
    ['Step 1: list the anterior six — FLAT PG: FSH, LH, ACTH, TSH, Prolactin, GH.', 'Step 2: oxytocin is not in the list.', 'Step 3: oxytocin is made in the hypothalamus and released by the posterior lobe.'],
    'Write “FLAT PG” in the margin before answering any pituitary question.', [('Which two hormones does the posterior pituitary release?', 'ADH and oxytocin.')])
a.M(4, 'ADH acts on the', ['bladder wall', 'kidney collecting ducts', 'liver', 'sweat glands'], 'B',
    ['Step 1: ADH = antidiuretic = “against much urine”.', 'Step 2: water is saved by reabsorbing it in the kidney.', 'Step 3: the collecting ducts become more permeable → more water returns to the blood.'],
    'Target of ADH is always the kidney (tubules / collecting ducts).', [('What happens to urine volume when ADH rises?', 'It falls and the urine becomes more concentrated.')])
a.S(17, 'Distinguish gigantism from acromegaly.', 'Both are caused by too much growth hormone. Gigantism happens in childhood (before the long bones stop growing) — the person becomes very tall with normal proportions. Acromegaly happens in adults — the bones can no longer lengthen, so the bones of the face, hands and feet thicken and enlarge.',
    ['Step 1: same hormone — excess GH.', 'Step 2: different age — child vs adult.', 'Step 3: different result — long bones lengthen (tall) vs flat/end bones thicken (big jaw, hands, feet).'],
    'Age decides the disease: child = gigantism, adult = acromegaly.', [('What does too little GH in childhood cause?', 'Pituitary dwarfism — short but proportionate, normal intelligence.')])
a.F(4, 'ADH is also called ____ because at high concentration it narrows blood vessels.', 'vasopressin', ['vasopressin', 'oxytocin', 'prolactin', 'somatotropin'],
    ['Step 1: vaso = vessel, pressin = press/squeeze.', 'Step 2: narrowing vessels raises blood pressure → vasopressin.'],
    'Split the word into its parts: vaso-pressin.', [('What is another name for growth hormone?', 'Somatotropin (somatotropic hormone).')])
a.TF(4, 'The posterior pituitary makes ADH and oxytocin.', False,
     ['Step 1: the posterior lobe has no hormone-making cells.', 'Step 2: neurosecretory cells of the hypothalamus make ADH and oxytocin.', 'Step 3: the posterior lobe only stores and releases them → false.'],
     'Watch the verb: “makes/produces/synthesises” vs “stores/releases”.', [('True or false: the anterior lobe makes its own hormones.', 'True — six of them.')])
a.M(3, 'FSH in males stimulates', ['testosterone secretion by Leydig cells', 'sperm production in the seminiferous tubules', 'growth of the prostate', 'milk production'], 'B',
    ['Step 1: FSH = follicle-stimulating in females.', 'Step 2: its male job is the “sperm factory” — seminiferous tubules.', 'Step 3: LH (not FSH) acts on Leydig cells.'],
    'FSH → Factory of sperm / Follicle. LH → Leydig cells / Luteum.', [('In females, what does LH stimulate after ovulation?', 'The corpus luteum to secrete progesterone.')])
a.S(5, 'Explain why a person under the influence of alcohol produces a lot of dilute urine (Review Part I Q8).', 'Alcohol inhibits the release of ADH from the posterior pituitary. With little ADH, the collecting ducts reabsorb little water, so a large volume of dilute urine is produced and the person becomes dehydrated.',
    ['Step 1: normal role of ADH — water reabsorption.', 'Step 2: alcohol blocks ADH release.', 'Step 3: less water reabsorbed → more dilute urine → thirst, dehydration.'],
    'Any “more urine” question: think first of ADH falling.', [('How does hypersecretion of ADH affect urine?', 'Small volume of concentrated urine.')])
a.M(18, 'Over-secretion of prolactin in a woman who is not breastfeeding may cause', ['gigantism', 'lack of menses and infertility', 'diabetes insipidus', 'goitre'], 'B',
    ['Step 1: prolactin → milk.', 'Step 2: too much → milk at the wrong time, menstrual periods stop, infertility (textbook p.18).'],
    'Prolactin excess = “milk + no periods”.', [('What does prolactin excess cause in males?', 'Breast enlargement and impotence.')])
a.S(4, 'Oxytocin is said to work by positive feedback during childbirth. Explain.', 'Stretching of the cervix by the baby’s head sends impulses to the hypothalamus → more oxytocin is released → stronger uterine contractions push the baby further → more stretching → even more oxytocin. The cycle grows until the baby is born and the stretching stops.',
    ['Step 1: stimulus — stretch of the cervix.', 'Step 2: response — oxytocin → contractions.', 'Step 3: the response increases the stimulus (more stretch) → the loop amplifies.', 'Step 4: it ends with birth.'],
    'Negative feedback reverses a change; positive feedback makes it bigger.', [('Give one example of negative feedback in the pituitary.', 'High thyroxine reduces TSH; dilute blood stops ADH release.')])

b = QSet('1.1.2 Practice — thyroid', 's112')
b.M(6, 'The thyroid gland is located', ['behind the stomach', 'at the base of the neck in front of the trachea', 'on top of the kidneys', 'under the brain'], 'B',
    ['Step 1: butterfly-shaped gland in the neck.', 'Step 2: it wraps the front of the trachea (windpipe).'], 'Thyroid → throat.', [('Where are the parathyroid glands?', 'Behind the thyroid gland, usually four.')])
b.F(18, 'Under-secretion of thyroxine in childhood causes ____.', 'cretinism', ['cretinism', 'myxoedema', 'acromegaly', 'goitre'],
    ['Step 1: under-secretion = hypothyroidism.', 'Step 2: child → cretinism; adult → myxoedema.'], 'C for Child and Cretinism.', [('Under-secretion of thyroxine in an adult causes ____.', 'Myxoedema.')])
b.S(7, 'Explain how negative feedback keeps the thyroxine level constant.', 'When the thyroxine level rises too high, it acts on the hypothalamus and anterior pituitary, which then release less TRH and TSH. With less TSH the thyroid releases less thyroxine, so the level falls back to normal. When thyroxine is low, more TRH and TSH are released and the thyroid secretes more.',
    ['Step 1: chain — TRH → TSH → thyroxine.', 'Step 2: high thyroxine switches the top of the chain off.', 'Step 3: thyroxine falls → normal.', 'Step 4: low thyroxine releases the brake → more TSH.'],
    'Always draw the three-box loop and add a dashed “−” arrow back to the top.', [('In a goitre caused by iodine lack, is TSH high or low?', 'High — there is not enough thyroxine to switch it off.')])
b.M(18, 'Which is a sign of hyperthyroidism?', ['Weight gain and feeling cold', 'Weight loss, sweating and fast heartbeat', 'Puffy face and sleepiness', 'Mental retardation in a child'], 'B',
    ['Step 1: hyper = too much thyroxine = metabolic rate high.', 'Step 2: high rate burns food (weight loss), makes heat (sweating) and speeds the heart.', 'Step 3: the other options are hypothyroid signs.'],
    'Hyper = Hot, Thin, Fast. Hypo = Slow, Cold, Fat, Tired.', [('Name two signs of myxoedema.', 'Puffy swollen face, low metabolic rate, weight gain, sensitivity to cold, sluggishness.')])
b.TF(7, 'Calcitonin raises the level of calcium in the blood.', False,
     ['Step 1: calcitonin is released when blood calcium is high.', 'Step 2: it moves calcium into bone → blood calcium falls.', 'Step 3: PTH is the hormone that raises it → false.'],
     'Calci-TONE-in tones it down.', [('Which gland secretes the hormone that raises blood calcium?', 'The parathyroid glands (PTH).')])
b.S(19, 'Why does eating iodised salt prevent goitre?', 'Iodine is a component of thyroxine. With enough iodine the thyroid can make normal amounts of thyroxine, which gives negative feedback to the pituitary, so TSH does not stay high and the gland does not enlarge.',
    ['Step 1: iodine → thyroxine.', 'Step 2: normal thyroxine → feedback → normal TSH.', 'Step 3: no over-stimulation → no swelling.'],
    'Connect three things: iodine, thyroxine, TSH.', [('Which other food is rich in iodine?', 'Sea food (fish, seaweed) — e.g. from the Red Sea coast.')])
b.M(6, 'Thyroxine is chemically', ['a steroid', 'an amine containing iodine', 'a glycoprotein', 'a carbohydrate'], 'B',
    ['Step 1: thyroxine is made from the amino acid tyrosine.', 'Step 2: iodine atoms are attached → iodinated amine.'],
    'Thyroxine = tyrosine + iodine.', [('Which hormone in the thyroid is a peptide?', 'Calcitonin.')])
b.S(6, 'Give three functions of thyroxine.', 'It controls the metabolic rate of the body; it regulates bone growth; it controls the development of the brain and nervous system in children (and metamorphosis in amphibians).',
    ['Step 1: metabolism — energy and heat.', 'Step 2: growth — bones.', 'Step 3: development — brain in children; tadpole to frog.'],
    'Remember “Metabolism, Growth, Brain”.', [('Which disorder shows that thyroxine is needed for brain development?', 'Cretinism (mental retardation in children).')])

c = QSet('1.1.4 Practice — adrenal', 's114')
c.F(9, 'The outer part of the adrenal gland is the ____.', 'cortex', ['cortex', 'medulla', 'islet', 'follicle'],
    ['Step 1: cortex = bark/outer layer.', 'Step 2: medulla = inner core.'], 'Cortex = Coat (outside).', [('Which part of the adrenal gland receives nerve impulses?', 'The medulla.')])
c.M(9, 'Which group of hormones is secreted by the adrenal cortex?', ['Amines', 'Corticosteroids', 'Gonadotropins', 'Peptides'], 'B',
    ['Step 1: cortex hormones are steroids called corticosteroids (corticoids).', 'Step 2: three groups — glucocorticoids, mineralocorticoids, sex steroids.'],
    'Cortex → corticosteroids (same root).', [('Name the major glucocorticoid.', 'Cortisol.')])
c.S(9, 'Aldosterone is secreted in response to low blood sodium and high potassium. State its effect on the kidney and on the blood.', 'It makes the kidney tubules reabsorb more sodium and excrete more potassium. Water follows the sodium, so blood sodium, blood volume and blood pressure rise back to normal while extra potassium is removed.',
    ['Step 1: stimulus — low Na⁺, high K⁺.', 'Step 2: action — keep Na⁺, lose K⁺.', 'Step 3: water follows Na⁺ → blood volume restored.'],
    'Aldosterone = “salt keeper”; ADH = “water keeper”.', [('Which disease includes a lack of aldosterone?', 'Addison’s disease.')])
c.M(10, 'Which is NOT an effect of adrenaline?', ['Faster heart rate', 'Glycogen broken down to glucose', 'Blood diverted to the gut for digestion', 'Wider pupils'], 'C',
    ['Step 1: adrenaline prepares for fight or flight.', 'Step 2: blood is sent to muscles; digestion is slowed.', 'Step 3: so “blood to the gut” is the wrong one.'],
    'Ask: “Would this help me run from danger right now?”', [('Which hormone is mainly responsible for constricting blood vessels throughout the body?', 'Noradrenaline (norepinephrine).')])
c.TF(8, 'The adrenal glands are located on top of the kidneys.', True,
     ['Step 1: ad = near, renal = kidney.', 'Step 2: one sits above each kidney → true.'], 'The name tells the address.', [('What colour are the adrenal glands?', 'Yellowish.')])
c.S(20, 'Distinguish Cushing’s disease from Addison’s disease.', 'Cushing’s disease is caused by hypersecretion of glucocorticoids (cortisol): weakness, high blood pressure, bruises, high blood sugar. Addison’s disease is caused by hyposecretion of glucocorticoids and aldosterone (failure of the adrenal cortex): anorexia, nausea, vomiting, weight loss, low blood glucose, muscular weakness and bronzing of the skin.',
    ['Step 1: both are adrenal cortex disorders.', 'Step 2: Cushing = too much; Addison = too little.', 'Step 3: list two signs of each.'],
    'Cushing = Cushion (too much, round). Addison = Adds nothing (too little).', [('What happens with over-secretion of adrenaline?', 'Tumour of the medulla with high blood pressure, severe headache, sweating and faintness.')])
c.M(22, 'Emotions such as fear and anger increase the secretion of', ['calcitonin', 'epinephrine', 'secretin', 'auxin'], 'B',
    ['Step 1: fear → nerve impulses → adrenal medulla.', 'Step 2: medulla → epinephrine (adrenaline).'], 'Fear = fight or flight = epinephrine.', [('Why is the adrenal sometimes called the “emergency gland”?', 'Its medulla releases adrenaline that prepares the body for immediate action in an emergency.')])
c.S(9, 'Explain why the adrenal gland is described as “two glands in one”.', 'The outer cortex and the inner medulla differ in structure, hormones and control. The cortex secretes steroid hormones (cortisol, aldosterone, sex steroids) under the control of ACTH and blood salts; the medulla secretes amines (adrenaline, noradrenaline) when it receives nerve impulses.',
    ['Step 1: structure — outer vs inner.', 'Step 2: hormones — steroids vs amines.', 'Step 3: control — hormones/salts vs nerves.'],
    'Compare three things: position, hormones, control.', [('Which part is essential for life?', 'The cortex (without aldosterone and cortisol, salt balance and blood sugar fail).')])

d = QSet('1.1.5 Practice — pancreas', 's115')
d.M(10, 'The islets of Langerhans are found in the', ['liver', 'pancreas', 'kidney', 'pituitary'], 'B',
    ['Step 1: islets = small islands of endocrine cells.', 'Step 2: they are scattered through the pancreas.'], 'Islets → pancreas.', [('Which islet cells secrete insulin?', 'β (beta) cells.')])
d.S(11, 'Explain how insulin and glucagon regulate blood glucose (Review Part IV Q2).', 'When blood glucose rises above normal, β-cells release insulin, which makes the liver and muscles take up glucose and convert it into glycogen, and cells use more glucose, so the level falls. When it falls below normal, α-cells release glucagon, which makes the liver convert glycogen into glucose and release it, so the level rises. They act antagonistically to keep about 100 mg/100 cm³.',
    ['Step 1: high glucose → insulin → store as glycogen → falls.', 'Step 2: low glucose → glucagon → glycogen to glucose → rises.', 'Step 3: opposite actions = antagonistic; controlled by negative feedback.'],
    'Write two arrows: high → insulin → down; low → glucagon → up.', [('Why must insulin be injected rather than swallowed?', 'It is a protein and would be digested in the stomach and intestine.')])
d.F(19, 'Failure of insulin secretion causes diabetes ____.', 'mellitus', ['mellitus', 'insipidus', 'tetany', 'myxoedema'],
    ['Step 1: insulin → glucose control.', 'Step 2: glucose in urine = “mellitus” (sweet).'], 'Mellitus = honey (sugar). Insipidus = no taste (ADH).', [('Lack of which hormone causes diabetes insipidus?', 'ADH.')])
d.M(19, 'A diabetic person usually has', ['glucose in the urine and frequent thirst', 'very dilute urine with no glucose', 'low blood glucose all the time', 'swollen thyroid'], 'A',
    ['Step 1: no insulin → blood glucose high.', 'Step 2: kidneys cannot reabsorb it all → glucose in urine.', 'Step 3: water lost with glucose → thirst and much urine.'],
    'Glucose in urine is the key clue for diabetes mellitus.', [('Why do untreated diabetics lose weight?', 'Cells cannot use glucose, so fats and proteins are broken down for energy.')])
d.TF(11, 'Glucagon converts glucose into glycogen.', False,
     ['Step 1: glucagon raises blood glucose.', 'Step 2: it does this by changing glycogen INTO glucose.', 'Step 3: insulin is the one that makes glycogen → false.'],
     'GlucaGON: glucose GONE → bring it back from glycogen.', [('True or false: insulin lowers blood sugar.', 'True.')])
d.S(10, 'Describe the exocrine and endocrine functions of the pancreas.', 'Exocrine: most pancreatic cells secrete pancreatic juice containing digestive enzymes, which flows through the pancreatic duct into the duodenum. Endocrine: the islets of Langerhans secrete insulin (β-cells) and glucagon (α-cells) directly into the blood to control blood glucose.',
    ['Step 1: exocrine → duct → digestive juice.', 'Step 2: endocrine → no duct → hormones into blood.'], 'Name the product and where it goes for each part.', [('Name another organ that is both exocrine and endocrine.', 'The testis or ovary (gametes + hormones).')])
d.M(11, 'Immediately after a meal rich in carbohydrate, the hormone whose secretion increases is', ['glucagon', 'insulin', 'adrenaline', 'cortisol'], 'B',
    ['Step 1: digested sugar raises blood glucose.', 'Step 2: high glucose → β-cells → insulin.'], 'Food in → insulin up.', [('Which hormone rises during a long fast?', 'Glucagon.')])
d.S(19, 'Why is it dangerous for a diabetic to eat a diet with a lot of sugar?', 'The sugar is absorbed into the blood, but without (enough) insulin it cannot be taken up by cells or stored as glycogen. Blood glucose rises even higher; very high levels can damage brain cells and cause coma or death.',
    ['Step 1: sugar → blood glucose rises.', 'Step 2: no insulin → cannot be stored or used.', 'Step 3: very high glucose → coma risk.'],
    'Answer with cause → effect → danger.', [('What is hypoglycaemia and what can cause it in a diabetic?', 'Abnormally low blood glucose — for example after too much insulin or missing a meal.')])

e = QSet('1.1.6 Practice — sex glands', 's116')
e.M(12, 'The endocrine tissue of the testes is the', ['seminiferous tubules', 'Leydig (interstitial) cells', 'epididymis', 'vas deferens'], 'B',
    ['Step 1: tubules make sperm.', 'Step 2: Leydig cells between them make testosterone.'], 'Leydig = Lets out testosterone (under LH).', [('Which pituitary hormone stimulates Leydig cells?', 'LH.')])
e.F(12, 'The corpus luteum secretes ____.', 'progesterone', ['progesterone', 'FSH', 'testosterone', 'prolactin'],
    ['Step 1: corpus luteum forms from the empty follicle after ovulation.', 'Step 2: under LH it secretes progesterone.'], 'Luteum ↔ LH ↔ progesterone.', [('Which hormone does the growing follicle secrete?', 'Oestrogen.')])
e.S(12, 'List four male secondary sexual characteristics caused by testosterone.', 'Deepening of the voice, growth of beard and body hair, increased muscle development, broadening of the chest and shoulders (also enlargement of the testes and sperm production).',
    ['Step 1: voice.', 'Step 2: hair.', 'Step 3: muscles.', 'Step 4: body shape.'], 'Use a head-to-body order: voice, beard, chest, muscles.', [('List two female secondary sexual characteristics.', 'Breast enlargement and broadening of the hips.')])
e.TF(12, 'Sex hormones are protein hormones.', False,
     ['Step 1: testosterone, oestrogen and progesterone are made from cholesterol.', 'Step 2: they are steroids → false.'], 'Endings -sterone and -gen (oestrogen) here = steroid.', [('Name a protein hormone that controls the gonads.', 'FSH or LH (glycoproteins).')])
e.M(12, 'Which statement about the ovary is correct?', ['It produces only hormones', 'It produces ova and the hormones oestrogen and progesterone', 'It produces FSH', 'It produces testosterone only'], 'B',
    ['Step 1: gonads have two jobs — gametes and hormones.', 'Step 2: ovary → ova + oestrogen + progesterone.', 'Step 3: FSH comes from the pituitary.'], 'Gonad = gametes + sex hormones.', [('Why are gonads called mixed glands?', 'They release gametes (exocrine-like) and hormones into blood (endocrine).')])
e.S(12, 'Explain how the hypothalamus and pituitary control the secretion of sex hormones (Review Part II Q3).', 'The hypothalamus releases GnRH, which makes the anterior pituitary secrete FSH and LH. These stimulate the testes (sperm and testosterone) or ovaries (follicle growth, oestrogen; corpus luteum, progesterone). High levels of sex hormones feed back to reduce GnRH, FSH and LH.',
    ['Step 1: GnRH.', 'Step 2: FSH + LH.', 'Step 3: gonad hormones.', 'Step 4: negative feedback.'], 'Draw the loop: brain → pituitary → gonad → back.', [('Why does the combined contraceptive pill stop ovulation?', 'Its oestrogen/progesterone give negative feedback, keeping FSH and LH low.')])
e.M(26, 'Puberty begins because', ['the thymus grows', 'the hypothalamus becomes less sensitive to androgens and releases more GnRH', 'the pancreas releases insulin', 'the posterior pituitary releases oxytocin'], 'B',
    ['Step 1: before puberty small amounts of androgens inhibit GnRH.', 'Step 2: at puberty the hypothalamus becomes less sensitive → more GnRH → more FSH and LH (textbook p.38).'],
    'Puberty starts in the brain, not in the gonads.', [('Which hormone rises first at puberty: GnRH or testosterone?', 'GnRH (then FSH/LH, then testosterone).')])
e.S(12, 'A woman’s ovaries stop working at menopause. Predict the levels of oestrogen and FSH, and explain.', 'Oestrogen falls because there are almost no follicles to make it. FSH (and LH) rise, because low oestrogen no longer gives negative feedback to the hypothalamus and pituitary.',
    ['Step 1: no follicles → little oestrogen.', 'Step 2: less negative feedback → more GnRH → more FSH, LH.'], 'When a gland fails, its own hormone falls but the pituitary hormone that drives it rises.', [('What happens to TSH when the thyroid fails?', 'TSH rises.')])

f = QSet('1.1.7 Practice — thymus', 's117')
f.M(13, 'The thymus gland is found', ['in the neck behind the thyroid', 'in the chest behind the sternum, below the thyroid', 'on top of the kidney', 'inside the brain'], 'B',
    ['Step 1: thymus — central chest cavity.', 'Step 2: below the thyroid, behind the breastbone, above the heart.'], 'Thymus = thorax (chest).', [('Which endocrine gland is inside the brain and light-sensitive?', 'The pineal gland.')])
f.F(13, 'The thymus secretes the hormone ____.', 'thymosin', ['thymosin', 'thyroxine', 'melatonin', 'insulin'],
    ['Step 1: thymus → thymosin (same root).', 'Step 2: thyroxine is from the thyroid — do not mix them.'], 'Thym-osin ↔ Thym-us; Thyr-oxine ↔ Thyr-oid.', [('Which gland secretes melatonin?', 'The pineal gland.')])
f.TF(13, 'The thymus gland grows larger in adults than in children.', False,
     ['Step 1: it is relatively large in newborns and children.', 'Step 2: it shrinks after puberty and nearly disappears in adults → false.'], 'Thymus = childhood gland.', [('What tissue replaces the thymus in adults?', 'Fibrous and fatty connective tissue.')])
f.S(13, 'State the function of thymosin and explain why it is important.', 'Thymosin stimulates the production and maturation of T lymphocytes (T cells), white blood cells that multiply, differentiate and mature in the thymus and then defend the body against pathogens. Without them the body has weak immunity and suffers frequent infections.',
    ['Step 1: thymosin → T cells.', 'Step 2: T cells → immunity.', 'Step 3: no T cells → infections.'], 'Function + reason = full marks.', [('Which virus attacks a type of T cell?', 'HIV (it attacks helper T cells, causing AIDS).')])
f.M(13, 'The thymus is functional primarily during', ['old age', 'childhood', 'pregnancy', 'sleep'], 'B',
    ['Step 1: it is largest and most active in childhood.', 'Step 2: after puberty it degenerates.'], 'Think “T-cell school is open in childhood”.', [('After which stage of life does the thymus shrink sharply?', 'Puberty.')])
f.M(23, 'Which gland is matched correctly?', ['Thymus — raises blood calcium', 'Thymus — plays a role in immunity', 'Thymus — source of cortisol', 'Thymus — needs iodine'], 'B',
    ['Step 1: thymus → thymosin → T cells.', 'Step 2: T cells → immunity.', 'Step 3: the other jobs belong to parathyroids, adrenal cortex and thyroid.'], 'Match by the hormone first, then the job.', [('Which gland matches “hormones that need iodine for secretion”?', 'The thyroid gland.')])
f.S(13, 'Why does removing the thymus from a newborn animal weaken its immunity much more than removing it from an adult?', 'In the newborn, T cells have not yet matured; without the thymus (thymosin) they never develop, so immunity fails. In the adult, most T cells have already been produced and continue to work, so removal has little effect.',
    ['Step 1: thymus works mostly early in life.', 'Step 2: newborn — no T cells will mature.', 'Step 3: adult — T cells already made.'], 'Age is the key word in thymus questions.', [('Why is the thymus large in children?', 'Because most T cells are being produced and trained during childhood.')])
f.S(13, 'Compare the thymus and the thyroid: location, hormone and function.', 'Thymus: in the chest behind the sternum; thymosin; T-cell maturation (immunity). Thyroid: base of the neck in front of the trachea; thyroxine and calcitonin; metabolic rate, growth and blood calcium.',
    ['Step 1: location.', 'Step 2: hormone.', 'Step 3: function.'], 'Use a three-column table when asked to compare.', [('Which of the two needs iodine?', 'The thyroid (for thyroxine).')])

QS = a.items + b.items + c.items + d.items + e.items + f.items
