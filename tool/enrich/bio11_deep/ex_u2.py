"""Unit 2 practice questions: 2.2 male, 2.3 female (incl. 2.3.1-2.3.4)."""
from common import set_unit, QSet

set_unit('bio11-u2')

a = QSet('2.2 Practice — male reproductive system', 's22')
a.M(28, 'The site of sperm production is the', ['epididymis', 'seminiferous tubules', 'vas deferens', 'prostate gland'], 'B',
    ['Step 1: sperm are made inside the testis.', 'Step 2: the cells lining the seminiferous tubules divide to form sperm.', 'Step 3: the epididymis only stores and matures them.'],
    'Made → tubules; stored → epididymis.', [('Where is testosterone made?', 'In the interstitial (Leydig) cells between the tubules.')])
a.M(30, 'The fluid that neutralises the acidity of the sperm-containing fluid is secreted by the', ['Cowper’s glands', 'prostate gland', 'testes', 'bladder'], 'B',
    ['Step 1: neutralise acid → need an alkali.', 'Step 2: the prostate secretes a thin, milky, alkaline fluid.'],
    'Prostate = Protects from acid.', [('Which gland secretes prostaglandins?', 'The seminal vesicles.')])
a.F(29, 'The front of the sperm head that contains dissolving enzymes is the ____.', 'acrosome', ['acrosome', 'nucleus', 'middle piece', 'flagellum'],
    ['Step 1: acro = tip, some = body.', 'Step 2: its enzymes dissolve the coats of the ovum.'], 'Acrosome = Access enzymes.', [('Which organelle is abundant in the middle piece?', 'Mitochondria.')])
a.TF(30, 'Urine and semen pass through the urethra at the same time.', False,
     ['Step 1: the urethra is a common tube for both.', 'Step 2: during ejaculation a muscle closes the bladder neck.', 'Step 3: so they never pass together → false.'],
     'Shared tube, different times.', [('True or false: the vas deferens carries urine.', 'False — only sperm.')])
a.S(28, 'State two reasons why the testes are found in the scrotum.', 'Sperm production needs a temperature 3–5 °C below body temperature, which the scrotum provides; the scrotal muscles can also adjust the testes’ position (and so temperature) — relaxing to cool them and contracting to warm them.',
    ['Step 1: temperature requirement.', 'Step 2: regulation by the scrotal muscles.'], 'Always link scrotum → temperature → sperm.', [('What may tight underwear do to fertility? Why?', 'Reduce it, by holding the testes against the warm body.')])
a.M(29, 'Which hormone causes the testes to descend into the scrotum?', ['FSH', 'Testosterone', 'Prolactin', 'Oestrogen'], 'B',
    ['Step 1: the developing testes secrete testosterone.', 'Step 2: testosterone stimulates their descent (textbook p.28).'], 'The testes move themselves using their own hormone.', [('What is the condition called when the testes do not descend?', 'Undescended testes (cryptorchidism) — causes infertility.')])
a.S(29, 'Describe how spermatogenesis takes place.', 'It begins at puberty in the seminiferous tubules. Spermatogonia (formed in fetal life) divide by mitosis; some grow into spermatocytes, which divide by meiosis to form haploid spermatids; these develop a head with acrosome, a middle piece with mitochondria and a tail, becoming sperm, which are matured in the epididymis.',
    ['Step 1: where and when.', 'Step 2: mitosis → spermatocytes.', 'Step 3: meiosis → spermatids (23 chromosomes).', 'Step 4: shape change → sperm.', 'Step 5: maturation in the epididymis.'],
    'Use the order: gonia → cytes → tids → zoa.', [('Why must meiosis happen in sperm formation?', 'To halve the chromosome number so the zygote has 46, not 92.')])
a.M(30, 'Semen consists of', ['sperm only', 'sperm and secretions of the accessory glands', 'urine and sperm', 'testosterone and sperm'], 'B',
    ['Step 1: sperm come from the testes.', 'Step 2: seminal vesicles, prostate and Cowper’s glands add fluid.', 'Step 3: together = semen.'], 'Semen = sperm + seminal fluid.', [('Name two substances in semen besides sperm.', 'Sugar (food), enzymes, alkaline fluid, prostaglandins, mucus.')])
a.S(31, 'Circumcision is described as hygienic. Explain.', 'Circumcision removes the foreskin. Without the foreskin, secretions and dirt cannot collect under it, so there is less risk of odour and bacterial infection. An uncircumcised man must clean under the foreskin daily.',
    ['Step 1: define circumcision.', 'Step 2: what collects under the foreskin.', 'Step 3: consequence for infection.'], 'Define first, then give the reason.', [('What tissue in the penis fills with blood during an erection?', 'Spongy (erectile) tissue.')])
a.M(30, 'Prostaglandins in semen help fertilization by', ['killing bacteria', 'stimulating muscular contractions in the female tract', 'feeding the ovum', 'thickening the uterine lining'], 'B',
    ['Step 1: prostaglandins come from the seminal vesicles.', 'Step 2: they cause contractions in the female organs that help sperm move to the ovum.'], 'Prostaglandins = “push” chemicals.', [('What is the main role of Cowper’s gland mucus?', 'Lubrication.')])
a.S(29, 'Arrange in order the structures through which sperm pass from where they are made to the outside.', 'Seminiferous tubules (testis) → epididymis → vas deferens → urethra (in the penis) → outside.',
    ['Step 1: made in the tubules.', 'Step 2: stored in the epididymis.', 'Step 3: carried by the vas deferens.', 'Step 4: leave through the urethra.'], 'Use the mnemonic SEVEN UP.', [('At which point do the seminal vesicle secretions join?', 'Where the vas deferens joins the urethra (ejaculatory duct).')])
a.TF(29, 'The epididymis lies on the outer surface of each testis.', True,
     ['Step 1: it is formed by the union of the seminiferous tubules.', 'Step 2: it lies in close contact with the external surface of each testis → true.'], 'Epi = upon: “upon the testis”.', [('What happens in the epididymis?', 'Sperm are stored temporarily and mature.')])

b = QSet('2.3 Practice — female reproductive system', 's23')
b.M(33, 'Which organ produces ova?', ['Uterus', 'Ovary', 'Vagina', 'Fallopian tube'], 'B',
    ['Step 1: gametes are made in gonads.', 'Step 2: the female gonad is the ovary.'], 'Ovary → ovum (same root).', [('Which ovarian structure makes oestrogen?', 'The follicle.')])
b.M(39, 'In humans, fertilization normally takes place in the', ['uterus', 'cervix', 'upper fallopian tube', 'vagina'], 'C',
    ['Step 1: the ovum lives ≈24 h.', 'Step 2: it is still in the upper oviduct when sperm meet it.'], 'Fertilization → tube; implantation → uterus.', [('Where does the embryo implant?', 'In the thickened wall (endometrium) of the uterus.')])
b.F(36, 'The phase of the menstrual cycle between day 14 and day 28 is called the secretory or ____ phase.', 'luteal', ['luteal', 'follicular', 'menstrual', 'proliferative'],
    ['Step 1: after ovulation the corpus luteum forms.', 'Step 2: its presence gives the name luteal.'], 'Luteal ↔ corpus luteum ↔ progesterone.', [('What is the other name of the proliferative phase?', 'Follicular phase.')])
b.TF(34, 'A woman produces new ova throughout her life.', False,
     ['Step 1: about 2 million potential ova exist at birth.', 'Step 2: no new ones are made; the stock only falls → false.'], 'Eggs: fixed stock at birth. Sperm: made daily.', [('How many ova mature in a lifetime?', 'About 400–500.')])
b.M(37, 'Menopause is mainly caused by', ['too much FSH', 'age-related changes in the ovaries', 'blockage of the oviduct', 'removal of the uterus only'], 'B',
    ['Step 1: few follicles remain at 40–50 years.', 'Step 2: remaining follicles respond poorly to FSH and LH.', 'Step 3: so ovulation and cycles stop.'], 'Menopause starts in the ovary, not the pituitary.', [('Are FSH levels high or low after menopause?', 'High — little oestrogen to give negative feedback.')])
b.S(38, 'Describe the roles of FSH and LH in the female.', 'FSH stimulates the growth of follicles in the ovary and the production of oestrogen by follicle cells. LH (its mid-cycle surge) causes ovulation and makes the corpus luteum secrete progesterone.',
    ['Step 1: FSH → follicle + oestrogen.', 'Step 2: LH → ovulation.', 'Step 3: LH → corpus luteum → progesterone.'], 'F = Follicle; L = Luteum.', [('Give the roles of FSH and LH in males.', 'FSH: sperm formation in the tubules; LH: testosterone from interstitial cells.')])
b.M(40, 'Identical twins are formed when', ['two ova are fertilized by two sperm', 'one zygote divides into two separate embryos', 'one ovum is fertilized by two sperm', 'a zygote divides but fails to separate'], 'B',
    ['Step 1: identical = same genes = one zygote.', 'Step 2: the zygote splits into two embryos that separate fully.', 'Step 3: option D describes Siamese twins.'], 'One egg → identical; two eggs → fraternal.', [('Can fraternal twins be a boy and a girl?', 'Yes — they come from two different eggs and sperm.')])
b.S(40, 'Explain why menstruation stops during pregnancy.', 'The corpus luteum and then the placenta keep secreting progesterone (and oestrogen). Progesterone maintains the uterine lining and stops new follicles developing, so there is no ovulation and the lining is not shed.',
    ['Step 1: menstruation needs progesterone to fall.', 'Step 2: in pregnancy progesterone stays high.', 'Step 3: lining kept; ovulation stopped.'], 'Link the event to the hormone level.', [('Which organ takes over hormone secretion from the corpus luteum?', 'The placenta.')])
b.M(41, 'Which of the following passes from the fetus to the mother across the placenta?', ['Oxygen', 'Glucose', 'Urea', 'Amino acids'], 'C',
    ['Step 1: food and oxygen go mother → fetus.', 'Step 2: wastes (CO₂, urea) go fetus → mother.'], 'Good things in, wastes out.', [('Name one harmful substance that can cross the placenta.', 'Alcohol, nicotine, some drugs, or viruses such as HIV.')])
b.F(41, 'The membrane containing fluid that cushions the embryo is the ____.', 'amnion', ['amnion', 'chorion', 'placenta', 'cervix'],
    ['Step 1: the amnion is the sac.', 'Step 2: its amniotic fluid acts as a shock absorber.'], 'Amnion → amniotic fluid.', [('Which membrane forms part of the placenta?', 'The chorion.')])
b.S(43, 'Describe the main events of childbirth.', 'Regular powerful contractions of the uterus begin (labour), strengthened by oxytocin; the amnion bursts and the fluid lubricates the birth canal; the cervix and vagina dilate; the baby is pushed out head first; the cord is cut; the placenta and remaining cord are expelled as the afterbirth; the cord stump falls off, leaving the navel.',
    ['Step 1: labour contractions.', 'Step 2: waters break.', 'Step 3: dilation.', 'Step 4: delivery head first.', 'Step 5: afterbirth.', 'Step 6: navel forms.'], 'Write the events in time order with one key word each.', [('What is the navel?', 'The scar left where the umbilical cord stump fell off.')])
b.M(36, 'If a woman’s cycle is 28 days and day 1 is the first day of bleeding, ovulation is most likely on', ['day 1', 'day 5', 'day 14', 'day 28'], 'C',
    ['Step 1: menstrual phase days 1–5.', 'Step 2: proliferative phase to day 14.', 'Step 3: ovulation ≈ day 14.'], 'Ovulation ≈ 14 days BEFORE the next period.', [('For a 30-day cycle, about which day is ovulation?', 'About day 16 (30 − 14).')])
b.S(34, 'State the function of each: (a) fimbriae (b) cervix (c) endometrium.', '(a) Fimbriae sweep the released ovum into the fallopian tube. (b) The cervix closes the uterus during pregnancy and dilates during birth. (c) The endometrium thickens to receive and nourish the embryo; it is shed in menstruation.',
    ['Step 1: fimbriae → catch.', 'Step 2: cervix → close/open.', 'Step 3: endometrium → bed for the embryo.'], 'One verb per structure: catch, close, cushion.', [('What is the function of cilia in the oviduct?', 'To move the ovum (or zygote) towards the uterus.')])
b.TF(35, 'In the female, the urethra and vagina open separately into the vestibule.', True,
     ['Step 1: the vestibule is the space into which both open.', 'Step 2: they are separate tubes → true.'], 'Female: separate openings; male: shared urethra.', [('What are the labia majora?', 'The outer lips of the vulva.')])

QS = a.items + b.items
