"""Grade 11, part A: linking verbs instead of 'copula' (Unit 1), must vs have to (Unit 3), full reported-speech
tables (Unit 5), pronouns without 'case concord' (Unit 10)."""
import re
from lib import grammar, table, text, worked, check, mcq, fill, tf, short, unitmap

# 'copula' -> 'linking verb' everywhere in the English notes (all grades); longest phrases first
COPULA_RULES = [
    (r'an overt copula \(\*is/are/was/were\*\)', 'a linking verb (*is/are/was/were*)'),
    (r'keep the verb as a middle anchor and use an overt copula', 'keep the verb in the middle and never leave out the linking verb (is/are/was/were)'),
    (r'an? explicit copula verbs? \(', 'a linking verb ('),
    (r'the essential English copula', 'the linking verb'),
    (r'Identify the sentence that contains a copula verb omission error caused by L1 interference:?', 'Which sentence is missing a linking verb (is/am/are/was/were)?'),
    (r'Identify the sentence that contains a copula verb error caused by L1 interference\.?', 'Which sentence is missing a linking verb (is/am/are/was/were)?'),
    (r'negative copular sentences', 'negative sentences with a linking verb'),
    (r'a word order error due to the negative copula', 'a word order error with "not"'),
    (r'a copula \(be-verb\)', 'a linking verb (a form of be)'),
    (r'A \*\*copula\*\* \(linking verb\)', 'A **linking verb**'),
    (r'is a copula \(linking verb\)', 'is a linking verb'),
    (r"Copula 'to be' Omission", "Missing linking verb 'to be'"),
    (r'Missing English copula\.?', 'Missing linking verb (is).'),
    (r'it can act as a main copula verb or as a helping verb', 'it can be a linking verb (*She is a doctor*) or a helping verb (*She is working*)'),
    (r'serves dual syntactic functions', 'has two jobs'),
    (r'\bcopula verbs\b', 'linking verbs'),
    (r'\bcopula verb\b', 'linking verb'),
    (r'\bcopulas\b', 'linking verbs'),
    (r'\bcopular\b', 'linking'),
    (r'\bCopula\b', 'Linking verb'),
    (r'\bcopula\b', 'linking verb'),
    (r'linking verb \(linking verb\)', 'linking verb'),
    (r'\bthe predicate nominative\b', 'the word that describes the subject'),
]

LV_TIP = 'Is there another verb after it? No → linking verb (She is tired). Yes → helping verb (She is sleeping).'
MH_TIP = "Necessary because I say so → must. Necessary because of a rule/law/timetable → have to. Forbidden → mustn't. Not necessary → don't have to / needn't. Past → had to."
RS_TIP = 'Change in this order: (1) reporting verb, (2) pronouns, (3) tense one step back, (4) time and place words, (5) word order for questions.'
PR_TIP = 'Before the verb → subject pronoun (I, he, she, we, they). After a verb or a preposition → object pronoun (me, him, her, us, them). Cover the other name and test.'


def linking_verbs(b):
    u = b.unit('eng11-u1')
    u['intro'] = 'English is S-V-O. Tigrinya is S-O-V, so keep the verb in the middle and never leave out the linking verb (is/are/was/were).'
    _, l = b.lesson('eng11-u1-l1-2')
    l['title'] = 'Linking verbs and clause boundaries'
    c = b.card('eng11-u1-c03')
    c['title'] = 'Linking verbs and clause boundaries'
    c['rule'][0] = 'English always needs a **linking verb** (*is/are/was/were*) between the subject and the word that describes it: *She **is** a teacher.*'
    for n in u['unitMap']['nodes']:
        if n['id'] == 'l1_2':
            n['label'] = 'Linking verbs and clause boundaries'
    for g in u['glossary']:
        if g['term'].lower() in ('copula', 'linking verb'):
            g['term'] = 'linking verb'
            g['meaning'] = 'a verb that joins the subject to a word that describes or names it: be, become, seem, look, feel (She is a nurse).'
    b.put_glossary('eng11-u1', [('helping verb', 'a verb that helps a main verb make a tense, question, negative or passive: be, have, do, can, will… (She is working).')])
    p = l['pages'][0]
    b.put_cards('eng11-u1-l1-2', [
        grammar('eng11-u1-l1-2-lv1', 'Linking verbs and helping verbs', [
            'A **linking verb** joins the subject to a word that **describes or names** it. Nothing is "done": *Aster **is** a nurse. The soup **smells** good. He **became** a doctor.*',
            'Common linking verbs: **be** (am/is/are/was/were), **become, seem, look, feel, sound, smell, taste, appear, get, grow, remain, stay**.',
            'A **helping verb** helps a main verb to make a tense, a question, a negative or the passive: *She **is** working. They **have** finished. **Do** you agree? The road **was** built.* Helping verbs: **be, have, do** and the modals (**can, will, must, should**…).',
            'The same word can do both jobs. Ask: is there another (main) verb after it? *She **is** tired* – no other verb → **linking verb**. *She **is** sleeping* – main verb *sleeping* → **helping verb**.',
            'After a linking verb use an **adjective**, not an adverb: *The food tastes **good*** (not *well*). *She looks **happy*** (not *happily*).',
            'English never leaves out the linking verb: ✗ *My brother a farmer.* → ✔ *My brother **is** a farmer.*',
        ], [
            ('My brother is a hardworking farmer.', True),
            ('The children seem happy today.', True),
            ('My brother a hardworking farmer.', False, 'My brother is a hardworking farmer.'),
            ('The injera tastes well.', False, 'The injera tastes good.'),
            ('She working in the garden.', False, 'She is working in the garden.'),
        ], pattern='Subject + linking verb + noun/adjective  ·  Subject + helping verb + main verb', page=p),
        table('eng11-u1-l1-2-lv2', 'Linking verb, helping verb or main verb?', ['Sentence', 'Verb', 'Job', 'Why'], [
            ['She is a teacher.', 'is', 'linking verb', 'no other verb; *a teacher* names her'],
            ['She is teaching now.', 'is', 'helping verb', 'helps the main verb *teaching*'],
            ['He has a car.', 'has', 'main verb', '*has* = owns'],
            ['He has bought a car.', 'has', 'helping verb', 'helps *bought* (present perfect)'],
            ['The milk smells bad.', 'smells', 'linking verb', '*bad* describes the milk'],
            ['The dog smells the food.', 'smells', 'main (action) verb', 'the dog does something to the food'],
            ['They got tired.', 'got', 'linking verb', '*tired* describes them (= became)'],
            ['Do you like tea?', 'Do', 'helping verb', 'helps make a question with *like*'],
        ], page=p),
        check('eng11-u1-l1-2-lv3', "Which sentence uses 'looks' as a linking verb?",
              {'A': 'She looks at the board.', 'B': 'She looks tired today.', 'C': 'She looks for her keys.', 'D': 'She looked through the window.'}, 'B', [
                  '**Step 1:** A linking verb is followed by a word that describes the subject.',
                  '**Step 2:** In B, *tired* describes *she* → *looks* is a linking verb (= seems).',
                  '**Step 3:** In A, C and D, *looks at / for / through* is an action (using your eyes or searching).',
                  f'**Tip:** {LV_TIP}'], page=p),
        check('eng11-u1-l1-2-lv4', "In 'They have finished the work', the word 'have' is ____.",
              {'A': 'a linking verb', 'B': 'a helping verb', 'C': "a main verb meaning 'own'", 'D': 'a noun'}, 'B', [
                  '**Step 1:** There is another verb after *have*: *finished*.',
                  '**Step 2:** *have* helps *finished* make the present perfect → **helping verb**.',
                  "**Step 3:** In *They have a car*, *have* would be a main verb (= own).",
                  f'**Tip:** {LV_TIP}'], page=p),
        check('eng11-u1-l1-2-lv5', 'Choose the correct sentence.',
              {'A': 'The flowers smell beautifully.', 'B': 'The flowers smell beautiful.', 'C': 'The flowers beautiful smell.', 'D': 'The flowers smelling beautiful.'}, 'B', [
                  '**Step 1:** *smell* here is a linking verb: it describes the flowers.',
                  '**Step 2:** After a linking verb use an **adjective**: *beautiful*.',
                  '**Step 3:** C has the verb at the end (S-O-V); D has no finite verb.',
                  '**Tip:** look / smell / taste / sound / feel + adjective.'], page=p),
    ], after='eng11-u1-c04')
    t = b.card('eng11-u1-c02')
    if not any(r[0] == 'S + helping verb + V' for r in t['rows']):
        t['rows'].insert(2, ['S + helping verb + V', 'She is working'])
    for g in u['games']:
        if g['id'] == 'eng11-u1-g1' and not any(p_['a'] == 'S + helping verb + V' for p_ in g['pairs']):
            g['pairs'].append({'a': 'S + helping verb + V', 'b': 'She is working'})
            g['pairs'].append({'a': 'linking verb + adjective', 'b': 'The soup smells good'})
    q = b.question('eng11-u1-q02')
    q['q'] = 'Which sentence is missing a linking verb (is/am/are/was/were)?'
    q['why'] = ['Answer C: My brother a hardworking farmer in the village.', 'Look at each sentence: is there a verb between the subject and the words that describe it?',
                'A (is), B (are) and D (were) all have a linking verb.', 'C has no verb: *My brother ___ a hardworking farmer.* Correct: *My brother **is** a hardworking farmer.*',
                'Tigrinya speakers sometimes leave out "is" because it can be dropped in Tigrinya. English always needs it.']
    q['similar'] = [{'q': 'Correct: "My father a teacher."', 'a': 'My father is a teacher.'}, {'q': 'Correct: "The roads busy today."', 'a': 'The roads are busy today.'}]
    q = b.question('eng11-u1-q06')
    q['q'] = 'Which sentence has a word order error with "not"?'
    q['why'] = ['Answer C: She is a doctor not in this public hospital.', 'With a linking verb, *not* comes straight after it: Subject + is/are + **not** + the rest.',
                '*She is **not** a doctor in this public hospital.*', 'In C, *not* is in the wrong place (after *a doctor*).']
    q['similar'] = [{'q': 'Correct: "He is a student not."', 'a': 'He is not a student.'}, {'q': 'Correct: "They are happy not."', 'a': 'They are not happy.'}]
    q = b.question('eng11-u1-r2q02')
    q['why'] = ['Answer D: The students very tired after the exam.', 'A subject followed by an adjective needs a linking verb such as is/are/was/were.',
                'Option D has no verb between "The students" and "very tired".', 'Options A–C all have a linking verb (became, were, felt).']
    sim = [('Correct: "My sister a nurse."', 'My sister is a nurse.'), ('Is "is" a linking verb or a helping verb in "He is reading"?', 'a helping verb (it helps "reading")')]
    b.put_questions('eng11-u1', [
        mcq('eng11-u1-lvq01', 'Choose the correct sentence.', {'A': 'The new classroom very big.', 'B': 'The new classroom is very big.', 'C': 'The new classroom very big is.', 'D': 'The new classroom being very big.'}, 'B',
            ['A sentence with an adjective (*big*) after the subject needs a linking verb: *is*.', 'A has no verb, C puts the verb at the end, D has no finite verb.'], LV_TIP, sim, page=p),
        mcq('eng11-u1-lvq02', "In 'The milk has gone sour', 'gone' is used as ____.", {'A': 'an action verb (moving)', 'B': 'a linking verb (= become)', 'C': 'a helping verb', 'D': 'a noun'}, 'B',
            ['*sour* describes the milk; the milk did not move anywhere.', '*go* here means *become* → linking verb.', '(*has* is the helping verb.)'], LV_TIP,
            [('What does "went" mean in "The old man went mad"?', 'became (linking verb)')], page=p),
        mcq('eng11-u1-lvq03', 'In which sentence is "is" a helping verb?', {'A': 'Abeba is the captain.', 'B': 'The tea is hot.', 'C': 'The road is being repaired.', 'D': 'He is in the library.'}, 'C',
            ['In C, *is* helps the main verb *repaired* (passive).', 'In A, B and D there is no other verb, so *is* is a linking verb (or main verb of place in D).'], LV_TIP, sim, page=p),
        mcq('eng11-u1-lvq04', 'The music sounds ____.', {'A': 'loudly', 'B': 'loud', 'C': 'loudness', 'D': 'louder than'}, 'B',
            ['*sounds* is a linking verb: it describes the music.', 'After a linking verb use an adjective: **loud**.'], LV_TIP,
            [('Complete: "You look ____ (happy / happily) today."', 'happy')], page=p),
        tf('eng11-u1-lvq05', 'True or false: In "She feels sad", "feels" is a linking verb.', True,
           ['True. *sad* describes *she*; nothing is done to anything.', 'feel + adjective = linking verb.'], LV_TIP,
           [('Linking or action? "She feels the cloth."', 'action (she touches it)')], page=p),
        short('eng11-u1-lvq06', 'Correct the error: "Our teachers very kind to us."', 'Our teachers are very kind to us.',
              ['Subject (*Our teachers*) + adjective (*very kind*) needs a linking verb.', 'Plural subject → **are**.'], LV_TIP, sim, page=p,
              accept=['Our teachers are very kind to us']),
    ])


def must_have_to(b):
    _, l = b.lesson('eng11-u3-l3-1')
    p = l['pages'][0]
    c = b.card('eng11-u3-c01')
    c['rule'][0] = ("**must** = obligation that comes from the **speaker** (*I must study harder*); **have to** = obligation from **outside** – a rule, law or timetable (*We have to wear a uniform*); "
                    "**should / ought to** = advice.")
    t = b.card('eng11-u3-c02')
    t['rows'] = [['must', "strong obligation from the speaker (I feel it is necessary)"], ['have to', 'obligation from outside: rule, law, timetable'],
                 ["mustn't", 'it is forbidden'], ["don't have to / needn't", 'it is not necessary'], ['had to', 'past obligation (must and have to)'],
                 ['should', 'advice'], ['might', 'possibility']]
    for g in b.unit('eng11-u3')['games']:
        if g['id'] == 'eng11-u3-g1':
            g['pairs'] = [{'a': 'must', 'b': 'obligation from the speaker'}, {'a': 'have to', 'b': 'obligation from a rule or law'},
                          {'a': "mustn't", 'b': 'forbidden'}, {'a': "don't have to", 'b': 'not necessary'}, {'a': 'had to', 'b': 'past obligation'},
                          {'a': 'should', 'b': 'advice'}, {'a': 'might', 'b': 'possibility'}]
    b.put_cards('eng11-u3-l3-1', [
        table('eng11-u3-l3-1-mh1', 'Must vs have to: the difference in one table', ['Point', 'must', 'have to'], [
            ['Who makes the rule?', 'the speaker: *I must call my mother tonight.*', 'outside (law, school, doctor, timetable): *Drivers have to carry a licence.*'],
            ['Written rules / notices', '*Passengers must wear seat belts.* (the rule-maker speaking)', '—'],
            ['Negative', "**mustn't** = forbidden: *You mustn't park here.*", "**don't have to** = not necessary: *You don't have to pay; it's free.*"],
            ['Same meaning as…', "mustn't = it is not allowed", "don't have to = needn't = there is no need"],
            ['Past', 'no past form → **had to**', '**had to**: *We had to wait for two hours.*'],
            ['Future', '*I must go tomorrow.* (decision now)', '**will have to**: *You will have to apply online.*'],
            ['Questions', '*Must I…?* (formal, rare)', '*Do I have to…? Does she have to…? Did they have to…?*'],
            ['Informal', '—', "**have got to** = have to: *I've got to go now.*"],
        ], page=p),
        worked('eng11-u3-l3-1-mh2', 'Step by step: choose the right form',
               "Complete: (a) The school rule says students ____ be in class by 7:30. (b) This film is wonderful – you ____ see it! (c) You ____ use your phone during the exam. "
               "(d) It's a holiday tomorrow, so we ____ go to school. (e) Last night I ____ finish my project, so I went to bed late.", [
                   "**Step 1: Is it necessary, forbidden or not necessary?** (a) necessary (b) necessary (c) forbidden (d) not necessary (e) necessary.",
                   '**Step 2: Necessary – who decides?** (a) the school → **have to**. (b) the speaker\'s own strong feeling → **must**.',
                   "**Step 3: Forbidden → mustn't.** (c) You **mustn't** use your phone.",
                   "**Step 4: Not necessary → don't have to (or needn't).** (d) we **don't have to** go to school.",
                   '**Step 5: Past → had to.** (e) Last night I **had to** finish my project.',
               ], "(a) have to (b) must (c) mustn't (d) don't have to (e) had to", page=p),
        check('eng11-u3-l3-1-mh3', 'In many countries, citizens ____ pay tax on what they earn. It is the law.',
              {'A': 'have to', 'B': "mustn't", 'C': "don't have to", 'D': 'had'}, 'A', [
                  '**Step 1:** The obligation comes from outside: the law.',
                  '**Step 2:** Present time → **have to**.',
                  "**Step 3:** *mustn't* = forbidden; *don't have to* = not necessary – both change the meaning.",
                  f'**Tip:** {MH_TIP}'], page=p),
        check('eng11-u3-l3-1-mh4', 'You ____ come to the airport with me. I can take a taxi.',
              {'A': "mustn't", 'B': "don't have to", 'C': 'must', 'D': 'had to'}, 'B', [
                  '**Step 1:** "I can take a taxi" shows coming is **not necessary**.',
                  "**Step 2:** Not necessary → **don't have to** (or *needn't*).",
                  "**Step 3:** *mustn't* would mean you are not allowed to come.",
                  f'**Tip:** {MH_TIP}'], page=p),
        check('eng11-u3-l3-1-mh5', 'When the bridge was broken, the villagers ____ cross the river by boat.',
              {'A': 'must', 'B': 'have to', 'C': 'had to', 'D': 'must have'}, 'C', [
                  '**Step 1:** *was broken* → past time.',
                  '**Step 2:** Past obligation = **had to** (*must* has no past form).',
                  '**Step 3:** *must have* + V3 is a guess about the past, not an obligation.',
                  f'**Tip:** {MH_TIP}'], page=p),
    ], after='eng11-u3-c02')
    sim = [('Complete: "You ____ smoke in the classroom." (forbidden)', "mustn't"), ('Complete: "We ____ wear a uniform on Saturdays." (not necessary)', "don't have to")]
    b.put_questions('eng11-u3', [
        mcq('eng11-u3-mhq01', 'My doctor says I ____ take this medicine twice a day.', {'A': 'have to', 'B': "mustn't", 'C': "don't have to", 'D': 'had to'}, 'A',
            ['The rule comes from the doctor (outside) → **have to**.', 'Present time, so not *had to*.'], MH_TIP, sim, page=p),
        mcq('eng11-u3-mhq02', 'Children ____ play with matches. It is very dangerous.', {'A': "don't have to", 'B': "mustn't", 'C': 'have to', 'D': 'needn\'t'}, 'B',
            ['Dangerous → it is **forbidden**.', "Forbidden = **mustn't**. *don't have to / needn't* = not necessary."], MH_TIP, sim, page=p),
        mcq('eng11-u3-mhq03', 'You ____ bring any food. We will cook for everyone.', {'A': "mustn't", 'B': "needn't", 'C': 'must', 'D': 'have to'}, 'B',
            ['"We will cook for everyone" → bringing food is **not necessary**.', "**needn't** = don't have to."], MH_TIP, sim, page=p),
        mcq('eng11-u3-mhq04', '____ you have to work last Saturday?', {'A': 'Do', 'B': 'Did', 'C': 'Must', 'D': 'Had'}, 'B',
            ['*last Saturday* → past.', 'Past question with have to: **Did** + subject + have to…?'], MH_TIP,
            [('Make a question: "She has to leave early."', 'Does she have to leave early?')], page=p),
        fill('eng11-u3-mhq05', 'If you fail the test, you ____ take it again next month. (future)', 'will have to', ['will have to', 'will must', 'must to', 'had to'],
             ['Future obligation → **will have to**.', '*will must* is impossible: two modals cannot stand together.'], MH_TIP,
             [('Make future: "They have to wait."', 'They will have to wait.')], page=p),
        short('eng11-u3-mhq06', 'Explain the difference: (a) "You mustn\'t tell anyone." (b) "You don\'t have to tell anyone."',
              "(a) It is forbidden to tell anyone. (b) It is not necessary to tell anyone, but you can if you want.",
              ["(a) mustn't = do not do it; it is not allowed.", "(b) don't have to = there is no need; you are free to choose."], MH_TIP, sim, page=p),
    ])


def reported_speech_tables(b, grade):
    """the same complete reported-speech tables for Grade 9 (Unit 5) and Grade 11 (Unit 5)"""
    lid = 'eng9-u5-l5-1' if grade == 9 else 'eng11-u5-l5-1'
    pre = lid + '-rs'
    _, l = b.lesson(lid)
    p = l['pages'][0]
    cards = [
        table(pre + '1', 'Tense changes in reported speech (all tenses)', ['Direct speech', 'Example (direct)', 'Reported speech', 'Example (reported)'], [
            ['Present simple', '"I **work** here."', 'Past simple', 'He said (that) he **worked** there.'],
            ['Present continuous', '"I **am working**."', 'Past continuous', 'He said he **was working**.'],
            ['Present perfect', '"I **have finished**."', 'Past perfect', 'He said he **had finished**.'],
            ['Present perfect continuous', '"I **have been waiting** for an hour."', 'Past perfect continuous', 'He said he **had been waiting** for an hour.'],
            ['Past simple', '"I **saw** the film."', 'Past perfect', 'He said he **had seen** the film.'],
            ['Past continuous', '"I **was reading**."', 'Past perfect continuous', 'He said he **had been reading**.'],
            ['Past perfect', '"I **had left**."', 'Past perfect (no change)', 'He said he **had left**.'],
            ['Past perfect continuous', '"I **had been working**."', 'no change', 'He said he **had been working**.'],
            ['Future simple (will)', '"I **will help** you."', 'would', 'He said he **would help** me.'],
            ['Future continuous', '"I **will be travelling**."', 'would be + -ing', 'He said he **would be travelling**.'],
            ['Future perfect', '"I **will have finished** by six."', 'would have + V3', 'He said he **would have finished** by six.'],
            ['am/is/are going to', '"I **am going to** study."', 'was/were going to', 'He said he **was going to** study.'],
        ], page=p),
        table(pre + '2', 'Modal verbs in reported speech', ['Direct', 'Reported', 'Example'], [
            ['can', 'could', '"I **can** swim." → She said she **could** swim.'],
            ['may', 'might', '"It **may** rain." → He said it **might** rain.'],
            ['must (obligation)', 'had to (or must)', '"You **must** go." → She said I **had to** go.'],
            ['shall (offer / question)', 'should', '"**Shall** I help?" → He asked if he **should** help.'],
            ['will', 'would', '"I **will** call." → She said she **would** call.'],
            ['could, would, should, might, ought to', 'no change', '"You **should** rest." → He said I **should** rest.'],
        ], page=p),
        table(pre + '3', 'Time and place words', ['Direct', 'Reported'], [
            ['now', 'then / at that time'], ['today', 'that day'], ['tonight', 'that night'],
            ['yesterday', 'the day before / the previous day'], ['tomorrow', 'the next day / the following day'],
            ['last week / month / year', 'the week before / the previous week'], ['next week / month / year', 'the following week / the week after'],
            ['two days ago', 'two days before'], ['this (book)', 'that (book)'], ['these', 'those'], ['here', 'there'],
        ], page=p),
        table(pre + '4', 'Pronouns change to match the new speaker', ['Direct', 'Reported', 'Example'], [
            ['I / me / my / mine', 'he, she / him, her / his, her / his, hers', '"**I** lost **my** pen." → Sara said **she** had lost **her** pen.'],
            ['we / us / our', 'they / them / their', '"**We** love **our** school." → They said **they** loved **their** school.'],
            ['you / your (to me)', 'I / me / my', 'He said to me, "**You** are late." → He told me **I** was late.'],
            ['you / your (to others)', 'he, she, they / his, her, their', 'I said to Abel, "**Your** bag is here." → I told Abel **his** bag was there.'],
        ], page=p),
        table(pre + '5', 'Statements, questions, requests and commands', ['Type', 'Reporting verb + pattern', 'Direct', 'Reported'], [
            ['Statement', 'said (that) … / told + person (that) …', '"I am tired," said Ruth.', 'Ruth said (that) she was tired.'],
            ['Yes/no question', 'asked (+ person) **if / whether** + statement order (no ?)', '"Are you ready?" he asked me.', 'He asked me **if I was** ready.'],
            ['Wh-question', 'asked (+ person) + **wh-word** + statement order, no do/does/did', '"Where do you live?" she asked.', 'She asked me **where I lived**.'],
            ['Request', 'asked + person + **to** + verb', '"Please close the door."', 'She asked me **to close** the door.'],
            ['Command', 'told / ordered + person + **to** + verb', '"Sit down!" said the teacher.', 'The teacher told us **to sit** down.'],
            ['Negative command', 'told + person + **not to** + verb', '"Don\'t be late."', 'He told me **not to be** late.'],
            ['Suggestion (Let\'s…)', 'suggested + -ing / suggested that we…', '"Let\'s go to the park."', 'She suggested **going** to the park.'],
        ], page=p),
        text(pre + '6', 'When the tense does NOT change', [
            '1. The reporting verb is in the **present** (*says, has said, will say*): *"I am hungry."* → *She **says** she **is** hungry.*',
            '2. The words are a **general truth** or still true: *"Water boils at 100 °C."* → *The teacher said water **boils** at 100 °C.*',
            '3. The verb is already **past perfect**, or a modal like **would, could, should, might, ought to**.',
            '**say or tell?** *say* has no person after it (*She said that…*, *She said to me…*). *tell* always has a person (*She **told me** that…*). ✗ *She said me*. ✗ *She told that*.',
        ], page=p),
        worked(pre + '7', 'Step by step: report a statement',
               'Report: Hana said to me, "I am going to visit my aunt in Keren tomorrow."', [
                   '**Step 1: Reporting verb.** *said to me* → **told me** (tell + person).',
                   '**Step 2: Pronouns.** *I* → **she**; *my* → **her** (Hana is a woman).',
                   '**Step 3: Tense one step back.** *am going to* → **was going to**.',
                   '**Step 4: Time and place words.** *tomorrow* → **the next day**. (*Keren* is a name – no change.)',
                   '**Step 5: Put it together.** Hana told me (that) she was going to visit her aunt in Keren the next day.',
               ], 'Hana told me (that) she was going to visit her aunt in Keren the next day.', page=p),
        worked(pre + '8', 'Step by step: report a question',
               'Report: He asked me, "Where did you buy this book yesterday?"', [
                   '**Step 1: Keep the question word.** *where*.',
                   '**Step 2: Statement order, no did.** *did you buy* → *you bought*.',
                   '**Step 3: Pronoun.** *you* (= me) → **I**.',
                   '**Step 4: Tense back.** past simple *bought* → past perfect **had bought**.',
                   '**Step 5: Time/place words.** *this* → **that**; *yesterday* → **the day before**.',
                   '**Step 6: Full stop, not a question mark.** He asked me where I had bought that book the day before.',
               ], 'He asked me where I had bought that book the day before.', page=p),
        check(pre + '9', 'Selam said, "I have finished my homework." → Selam said that she ____ her homework.',
              {'A': 'has finished', 'B': 'had finished', 'C': 'finished', 'D': 'have finished'}, 'B', [
                  '**Step 1:** *said* is past, so move the tense one step back.',
                  '**Step 2:** present perfect (*have finished*) → past perfect (**had finished**).',
                  '**Step 3:** *my* → *her* is already done in the sentence.',
                  f'**Tip:** {RS_TIP}'], page=p),
        check(pre + '10', 'The teacher said to us, "Don\'t open your books." → The teacher told us ____ our books.',
              {'A': "don't open", 'B': 'not to open', 'C': 'to not opening', 'D': "didn't open"}, 'B', [
                  '**Step 1:** It is a negative command.',
                  '**Step 2:** Pattern: told + person + **not to** + verb.',
                  '**Step 3:** So: *The teacher told us not to open our books.*',
                  f'**Tip:** {RS_TIP}'], page=p),
        check(pre + '11', 'He asked me, "Can you help me tomorrow?" → He asked me ____.',
              {'A': 'if I could help him the next day', 'B': 'can I help him tomorrow', 'C': 'if could I help him the next day', 'D': 'that I could help him tomorrow'}, 'A', [
                  '**Step 1:** Yes/no question → **if / whether**.',
                  '**Step 2:** Statement order: *I could* (can → could).',
                  '**Step 3:** Pronouns: you → I, me → him. Time: tomorrow → the next day.',
                  f'**Tip:** {RS_TIP}'], page=p),
        check(pre + '12', '"I will call you tonight," Dawit said to Ruth. → Dawit told Ruth that he ____ her that night.',
              {'A': 'will call', 'B': 'would call', 'C': 'called', 'D': 'is calling'}, 'B', [
                  '**Step 1:** *will* moves back to **would**.',
                  '**Step 2:** *you* (Ruth) → *her*; *tonight* → *that night* (already in the sentence).',
                  '**Step 3:** So: *Dawit told Ruth that he would call her that night.*',
                  f'**Tip:** {RS_TIP}'], page=p),
    ]
    anchor = 'eng9-u5-c02' if grade == 9 else 'eng11-u5-c02'
    b.put_cards(lid, cards, after=anchor)
    uid = 'eng9-u5' if grade == 9 else 'eng11-u5'
    qp = uid + '-rsq'
    sim_t = [('Report: "I am happy," she said.', 'She said (that) she was happy.'), ('Report: "We have won," they said.', 'They said (that) they had won.')]
    sim_q = [('Report: "Do you like tea?" he asked me.', 'He asked me if I liked tea.'), ('Report: "Why are you late?" she asked him.', 'She asked him why he was late.')]
    b.put_questions(uid, [
        mcq(qp + '01', 'Abel said, "I am reading a novel." → Abel said that he ____ a novel.', {'A': 'is reading', 'B': 'was reading', 'C': 'had read', 'D': 'reads'}, 'B',
            ['present continuous → past continuous.', 'am reading → **was reading**.'], RS_TIP, sim_t, page=p),
        mcq(qp + '02', 'She said, "I saw the accident." → She said that she ____ the accident.', {'A': 'saw', 'B': 'has seen', 'C': 'had seen', 'D': 'sees'}, 'C',
            ['past simple → past perfect.', 'saw → **had seen**.'], RS_TIP, sim_t, page=p),
        mcq(qp + '03', 'They said, "We will finish the work tomorrow." → They said that they would finish the work ____.', {'A': 'tomorrow', 'B': 'yesterday', 'C': 'the next day', 'D': 'the day before'}, 'C',
            ['tomorrow → **the next day** (or the following day).', 'will → would is already done.'], RS_TIP,
            [('Change for reported speech: "yesterday"', 'the day before / the previous day'), ('Change: "here"', 'there')], page=p),
        mcq(qp + '04', 'He asked me, "Where do you work?" → He asked me ____.', {'A': 'where do I work', 'B': 'where I worked', 'C': 'where did I work', 'D': 'that where I worked'}, 'B',
            ['Wh-question: keep *where*, use statement order, no *do*.', 'Tense back: work → worked; you → I.'], RS_TIP, sim_q, page=p),
        mcq(qp + '05', 'The nurse said to me, "Please sit down." → The nurse ____ me to sit down.', {'A': 'said', 'B': 'asked', 'C': 'said to', 'D': 'told that'}, 'B',
            ['A polite request: **asked** + person + to + verb.', '*said* cannot be followed directly by *me to…*.'], RS_TIP,
            [('Report: "Open the window, please," she said to him.', 'She asked him to open the window.')], page=p),
        mcq(qp + '06', 'Mother said, "You can go out now." → Mother said that I ____ go out then.', {'A': 'can', 'B': 'could', 'C': 'may', 'D': 'will'}, 'B',
            ['can → **could**.', 'now → then is already done.'], RS_TIP, sim_t, page=p),
        fill(qp + '07', 'She asked me, "Have you ever been to Massawa?" → She asked me ____ I had ever been to Massawa.', 'if', ['if', 'that', 'what', 'do'],
             ['A yes/no question is reported with **if** (or whether).'], RS_TIP, sim_q, page=p),
        fill(qp + '08', 'The teacher said, "The earth goes round the sun." → The teacher said that the earth ____ round the sun.', 'goes', ['goes', 'went', 'had gone', 'is going'],
             ['A general truth does not need to change tense: **goes**.'], RS_TIP,
             [('Report: "Water boils at 100 °C," he said.', 'He said that water boils at 100 °C.')], page=p),
        short(qp + '09', 'Report: Dawit said, "I have been waiting here for two hours."', 'Dawit said (that) he had been waiting there for two hours.',
              ['I → he.', 'have been waiting → **had been waiting**.', 'here → **there**.'], RS_TIP, sim_t, page=p,
              accept=['Dawit said that he had been waiting there for two hours.', 'Dawit said he had been waiting there for two hours.']),
        short(qp + '10', 'Report: The guard said to the boys, "Don\'t climb the wall!"', 'The guard told the boys not to climb the wall.',
              ['Negative command: told + person + **not to** + verb.'], RS_TIP,
              [('Report: "Don\'t touch it," she said to me.', 'She told me not to touch it.')], page=p,
              accept=['The guard told the boys not to climb the wall', 'The guard ordered the boys not to climb the wall.']),
    ])


def reported_speech_g11(b):
    reported_speech_tables(b, 11)
    u = b.unit('eng11-u5')
    for g in u['games']:
        if g['id'] == 'eng11-u5-g1':
            g['title'] = 'Match the direct form to the reported form'
            g['pairs'] = [{'a': 'am / is', 'b': 'was'}, {'a': 'have done', 'b': 'had done'}, {'a': 'did', 'b': 'had done'}, {'a': 'will', 'b': 'would'},
                          {'a': 'can', 'b': 'could'}, {'a': 'tomorrow', 'b': 'the next day'}, {'a': 'here', 'b': 'there'}, {'a': 'yesterday', 'b': 'the day before'}]
    m = u['unitMap']
    for n in m['nodes']:
        if n['id'] == 'l5_1' and 'eng11-u5-l5-1-rs1' not in n['cards']:
            n['cards'].append('eng11-u5-l5-1-rs1')


def pronouns(b):
    u = b.unit('eng11-u10')
    u['title'] = 'Pronouns'
    u['intro'] = 'Grammar: subject, object, possessive and reflexive pronouns, and using it / its for things.'
    _, l = b.lesson('eng11-u10-l1')
    l['title'] = 'Pronouns'
    p = l['pages'][0]
    b.replace_card(grammar('eng11-u10-c01', 'Pronouns', [
        'A **pronoun** takes the place of a noun so that we do not repeat it: *Aster is late. **She** missed the bus.*',
        '**Subject pronouns** (*I, you, he, she, it, we, they*) come **before the verb**: ***She** writes.* **Object pronouns** (*me, you, him, her, it, us, them*) come **after a verb or a preposition**: *The teacher helped **her**. This letter is for **me**.*',
        '**Possessive adjectives** (*my, your, his, her, its, our, their*) go **before a noun**: *the dog wagged **its** tail.* **Possessive pronouns** (*mine, yours, his, hers, ours, theirs*) stand **alone**: *The book is **mine**.* They never take an apostrophe: *its, hers, theirs* (*it\'s* = it is).',
        '**Reflexive pronouns** (*myself, yourself, himself, herself, itself, ourselves, yourselves, themselves*) point back to the subject: *They did the work **themselves**.* (✗ *theirselves*, ✗ *hisself*)',
        'Use **it / its** for things and animals, **he / she** for people: *The school opened **its** new library.*',
        '**Two names joined by "and":** cover the other name and test the pronoun alone: *The teacher asked Ruth and (I / me)…* → *asked **me*** → *asked Ruth and **me***. *(I / Me) and Aster went…* → ***I** went* → *Aster and **I** went*.',
    ], [
        ('Aster and I went to the market.', True),
        ('The teacher gave the books to Ruth and me.', True),
        ('Me and Aster went to the market.', False, 'Aster and I went to the market.'),
        ("The dog wagged it's tail.", False, 'The dog wagged its tail.'),
        ('They did the work theirselves.', False, 'They did the work themselves.'),
    ], pattern='subject pronoun + verb  ·  verb / preposition + object pronoun  ·  possessive adjective + noun', page=p))
    b.replace_card(table('eng11-u10-c02', 'Pronoun forms', ['Subject', 'Object', 'Possessive adjective', 'Possessive pronoun', 'Reflexive'], [
        ['I', 'me', 'my', 'mine', 'myself'], ['you', 'you', 'your', 'yours', 'yourself / yourselves'], ['he', 'him', 'his', 'his', 'himself'],
        ['she', 'her', 'her', 'hers', 'herself'], ['it', 'it', 'its', '—', 'itself'], ['we', 'us', 'our', 'ours', 'ourselves'], ['they', 'them', 'their', 'theirs', 'themselves'],
    ], page=p))
    b.put_cards('eng11-u10-l1', [
        table('eng11-u10-l1-pr1', 'Common pronoun mistakes', ['Wrong', 'Right', 'Why'], [
            ['Me and my friend went home.', 'My friend and I went home.', 'before the verb → subject pronoun (I)'],
            ['Between you and I, …', 'Between you and me, …', 'after a preposition → object pronoun (me)'],
            ["The tree lost it's leaves.", 'The tree lost its leaves.', "its = belonging to it; it's = it is"],
            ['They hurt theirselves.', 'They hurt themselves.', 'theirselves is not a word'],
            ['This pen is your\'s.', 'This pen is yours.', 'possessive pronouns have no apostrophe'],
            ['My father he is a farmer.', 'My father is a farmer.', 'do not repeat the subject with a pronoun'],
        ], page=p),
        check('eng11-u10-l1-pr2', 'My sister and ____ are going to Asmara next week.', {'A': 'me', 'B': 'I', 'C': 'myself', 'D': 'mine'}, 'B', [
            '**Step 1:** The pronoun is part of the subject (before *are going*).',
            '**Step 2:** Cover *My sister and*: *__ am going* → **I**.',
            '**Step 3:** *me* is an object pronoun; *myself* needs *I* as the subject.',
            f'**Tip:** {PR_TIP}'], page=p),
        check('eng11-u10-l1-pr3', 'The company has changed ____ name.', {'A': "it's", 'B': 'its', 'C': 'their', 'D': 'it'}, 'B', [
            '**Step 1:** *company* is a thing (singular) → *it*.',
            '**Step 2:** Before a noun (*name*) we need the possessive adjective **its**.',
            "**Step 3:** *it's* means *it is* – \"has changed it is name\" makes no sense.",
            "**Tip:** If you can say *it is*, write *it's*; otherwise write *its*."], page=p),
    ], after='eng11-u10-c02')
    u['tips'] = [dict(text='Before the verb → I / he / she / we / they. After a verb or preposition → me / him / her / us / them. Cover the other name and test.', page=p, src='notes')]
    b.put_glossary('eng11-u10', [('pronoun', 'a word used instead of a noun: he, them, its, mine, themselves.'),
                                 ('possessive pronoun', 'a pronoun that shows who owns something and stands alone: mine, yours, hers, theirs.'),
                                 ('reflexive pronoun', 'a pronoun that points back to the subject: myself, themselves.')])
    u['unitMap'] = unitmap('eng11-u10', 'Pronouns', [('forms', 'Pronoun forms', 'eng11-u10-l1', ['eng11-u10-c01', 'eng11-u10-c02']),
                                                    ('mistakes', 'Common mistakes', 'eng11-u10-l1', ['eng11-u10-l1-pr1'])])
    sim = [('Complete: "The prize was given to Abel and ____." (I / me)', 'me'), ('Complete: "____ and Saba are cousins." (I / Me)', 'I')]
    b.put_questions('eng11-u10', [
        mcq('eng11-u10-prq01', 'This is not your book. It is ____.', {'A': 'my', 'B': 'mine', 'C': "mine's", 'D': 'me'}, 'B',
            ['No noun after the gap → possessive **pronoun**: *mine*.', '*my* needs a noun after it (*my book*).'], PR_TIP,
            [('Complete: "Is this bag (your / yours)?"', 'yours')], page=p),
        mcq('eng11-u10-prq02', 'The children made the cake all by ____.', {'A': 'themself', 'B': 'theirselves', 'C': 'themselves', 'D': 'them'}, 'C',
            ['The subject is *the children* (they) → **themselves**.', '*themself* and *theirselves* are not standard English.'], PR_TIP,
            [('Complete: "I hurt ____ while cooking."', 'myself')], page=p),
        mcq('eng11-u10-prq03', 'Please give these notes to Hana and ____.', {'A': 'I', 'B': 'me', 'C': 'myself', 'D': 'mine'}, 'B',
            ['After the preposition *to* → object pronoun.', 'Cover *Hana and*: *give these notes to __* → **me**.'], PR_TIP, sim, page=p),
        fill('eng11-u10-prq04', 'The cat is drinking ____ milk.', 'its', ['its', "it's", 'it', 'their'],
             ['Before a noun, for an animal → **its** (no apostrophe).'], PR_TIP, [('Complete: "____ raining again." (Its / It\'s)', "It's")], page=p),
        short('eng11-u10-prq05', 'Correct the error: "Me and my brother play football every evening."', 'My brother and I play football every evening.',
              ['The pronoun is part of the subject → **I**, not *me*.', 'It is polite to put yourself last: *My brother and I*.'], PR_TIP, sim, page=p,
              accept=['My brother and I play football every evening']),
    ])


def apply(b):
    b.sub_all(COPULA_RULES)
    linking_verbs(b)
    must_have_to(b)
    reported_speech_g11(b)
    pronouns(b)
