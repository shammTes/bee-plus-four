"""Grade 11, part C: tenses (present perfect continuous), questions, question tags, word formation, prepositions."""
from lib import grammar, table, text, worked, check, mcq, fill, tf, short, unitmap

PPC_TIP = 'Action still going on / just stopped + how long (for, since, all day) → have/has been + -ing. Finished result or how many → have/has + past participle.'


def tenses(b):
    u = b.unit('eng11-u13')
    u['title'] = 'Perfect tenses and future forms'
    u['intro'] = 'Present perfect, present perfect continuous, past perfect and the future forms (will, going to, present continuous) – explained step by step.'
    _, l = b.lesson('eng11-u13-l1')
    l['title'] = 'Perfect tenses and future forms'
    b.replace_card(grammar('eng11-u13-c01', 'Present perfect or past simple?', [
        '**Present perfect** = *have/has + past participle*. Use it when the time is **not finished** or **not said**, and the past action matters **now**: *I **have lost** my key* (I still can\'t find it). *She **has visited** Massawa twice.*',
        '**Past simple** = *verb + -ed / 2nd form*. Use it with a **finished time**: *yesterday, last week, in 2015, two days ago, when I was a child*: *I **lost** my key **yesterday**.*',
        'Time words for the present perfect: *already, yet, just, ever, never, so far, recently, since, for*. ✗ Never use the present perfect with *ago* or *yesterday*.',
        '**since** + the starting point (*since 2019, since Monday, since I came*). **for** + the length of time (*for ten years, for two hours*). ✗ *since ten years*.',
        '**Past perfect** = *had + past participle*: the **earlier** of two past actions: *When we arrived, the film **had started**.*',
    ], [
        ('I have finished my homework. Can I go out?', True),
        ('I have finished my project last week.', False, 'I finished my project last week.'),
        ('We have lived here for ten years.', True),
        ('She has worked here since five years.', False, 'She has worked here for five years.'),
    ], pattern='have/has + V3 (no finished time)  ·  V2 + finished time  ·  had + V3 (earlier past)'))
    b.replace_card(table('eng11-u13-c02', 'Time words: which tense?', ['Time word', 'Tense', 'Example'], [
        ['yesterday, last year, ago, in 2015, when…', 'past simple', 'He **left** two days ago.'],
        ['already, yet, just, ever, never, so far', 'present perfect', 'Have you **ever seen** the sea?'],
        ['since + start / for + length', 'present perfect (continuous)', 'I **have known** her **for** years.'],
        ['by the time, before, after (two past actions)', 'past perfect', 'The bus **had left** before we came.'],
        ['tomorrow, next week + plan with evidence', 'going to', 'Look at the clouds! It**\'s going to** rain.'],
        ['decision now, offer, promise', 'will', 'I**\'ll** help you.'],
        ['fixed arrangement (date, time)', 'present continuous', 'We**\'re meeting** the principal at 10.'],
    ]))
    b.put_cards('eng11-u13-l1', [
        grammar('eng11-u13-ppc1', 'Present perfect continuous', [
            '**Form:** *have/has + been + verb-ing*: *I **have been waiting**. She **has been studying**.* Negative: *haven\'t/hasn\'t been + -ing*. Question: *Have you been waiting? How long **has** she **been** studying?*',
            '**Use 1 – an action that started in the past and is still going on**, usually with *for, since, how long, all day*: *Aster **has been working** in this laboratory **since** 2019.*',
            '**Use 2 – an action that has just stopped and we can see the result now**: *I\'m tired because I **have been running**. Your eyes are red – **have** you **been crying**?*',
            '**Present perfect vs present perfect continuous:** the continuous shows the **activity / how long**; the simple shows the **result / how many**: *I **have been writing** letters all morning.* (activity) / *I **have written** five letters.* (result, number)',
            'Verbs of state (*know, like, want, believe, understand, own*) do **not** take the continuous: *I **have known** him for years.* ✗ *I have been knowing him.*',
        ], [
            ('He has been reading the old manuscript for four hours.', True),
            ('She is working here since 2019.', False, 'She has been working here since 2019.'),
            ('I have been reading three books this month.', False, 'I have read three books this month.'),
            ('I have been knowing her since childhood.', False, 'I have known her since childhood.'),
        ], pattern='have/has + been + V-ing  (+ for / since / how long)'),
        table('eng11-u13-ppc2', 'Present perfect or present perfect continuous?', ['Present perfect (have + V3)', 'Present perfect continuous (have been + V-ing)'], [
            ['Result: *I **have painted** the room.* (it is finished)', 'Activity: *I **have been painting** the room.* (maybe not finished; paint on my hands)'],
            ['How many / how much: *She **has written** three essays.*', 'How long: *She **has been writing** for three hours.*'],
            ['State verbs: *I **have known** him for years.*', '✗ not with state verbs (know, like, want, own)'],
            ['Short or finished actions: *The bus **has arrived**.*', 'Longer, repeated actions: *It **has been raining** all day.*'],
        ]),
        check('eng11-u13-ppc3', 'We ____ for the bus for forty minutes, and it still hasn\'t come.', {'A': 'are waiting', 'B': 'have been waiting', 'C': 'waited', 'D': 'had waited'}, 'B', [
            '**Step 1:** *for forty minutes* + *it still hasn\'t come* → the waiting started in the past and is still going on.',
            '**Step 2:** That is the present perfect continuous: *have been waiting*.',
            '**Step 3:** ✗ *are waiting for forty minutes* – English does not use the present continuous with *for/since* like this.', f'**Tip:** {PPC_TIP}']),
        check('eng11-u13-ppc4', 'Choose the correct sentence.', {'A': 'I have been drinking four cups of tea today.', 'B': 'I have drunk four cups of tea today.', 'C': 'I am drinking four cups of tea today.', 'D': 'I drank four cups of tea since morning.'}, 'B', [
            '**Step 1:** *four cups* is a number = a result.', '**Step 2:** Results and numbers take the present perfect simple: *have drunk*.',
            '**Step 3:** D: *since* needs a perfect tense, not the past simple.', f'**Tip:** {PPC_TIP}']),
    ], after='eng11-u13-c02')
    b.put_questions('eng11-u13', [
        mcq('eng11-u13-ppq01', 'My hands are dirty because I ____ in the garden.', {'A': 'work', 'B': 'have been working', 'C': 'had worked', 'D': 'will work'}, 'B',
            ['The activity has just stopped and we can see the result (dirty hands).', 'That is use 2 of the present perfect continuous.'], PPC_TIP,
            [('Complete: She is out of breath because she ____ (run).', 'has been running')]),
        mcq('eng11-u13-ppq02', 'How long ____ English?', {'A': 'are you learning', 'B': 'do you learn', 'C': 'have you been learning', 'D': 'you have been learning'}, 'C',
            ['*How long* + action still going on → present perfect continuous.', 'Question order: have + subject + been + -ing.'], PPC_TIP,
            [('Make a question: (how long / she / live / here?)', 'How long has she been living here?')]),
        mcq('eng11-u13-ppq03', 'She ____ him since they were at primary school.', {'A': 'has been knowing', 'B': 'has known', 'C': 'knows', 'D': 'is knowing'}, 'B',
            ['*know* is a state verb: no continuous form.', 'With *since* use the present perfect simple: *has known*.'], PPC_TIP,
            [('Correct: "I have been owning this bike for a year."', 'I have owned this bike for a year.')]),
        fill('eng11-u13-ppq04', 'It ____ (rain) all day. The roads are flooded.', 'has been raining', ['has been raining', 'is raining', 'rained', 'has rained all'],
             ['*all day* = how long; the activity is long and still has a result now.', 'Use has been + raining.'], PPC_TIP,
             [('Complete: They ____ (play) football since lunchtime.', 'have been playing')]),
        fill('eng11-u13-ppq05', 'I ____ (read) this novel for a week, but I ____ (read) only half of it.', 'have been reading / have read',
             ['have been reading / have read', 'have read / have been reading', 'read / read', 'am reading / read'],
             ['First gap: how long (*for a week*) → have been reading.', 'Second gap: how much (*only half*) → have read.'], PPC_TIP,
             [('Complete: He ____ (write) emails all morning; he ____ (send) ten so far.', 'has been writing / has sent')]),
        short('eng11-u13-ppq06', 'Correct the error: "We are living in Keren since 2018."', 'We have been living in Keren since 2018.',
              ['*since 2018* needs a perfect tense.', 'Action still going on → have been living (or have lived).'], PPC_TIP,
              [('Correct: "He is teaching here for ten years."', 'He has been teaching here for ten years.')], accept=['We have lived in Keren since 2018.', 'We have been living in Keren since 2018']),
    ])
    pair = {'a': 'present perfect continuous', 'b': 'how long an action has been going on'}
    if pair not in u['games'][0]['pairs']:
        u['games'][0]['pairs'].insert(1, pair)
    u['glossary'] = [dict(term='present perfect continuous', meaning='have/has been + -ing: I have been waiting for an hour.', page=l['pages'][0], src='notes')]
    u['unitMap'] = unitmap('eng11-u13', 'Perfect tenses and future forms', [
        ('perfect', 'Present perfect or past simple?', 'eng11-u13-l1', ['eng11-u13-c01', 'eng11-u13-c02']),
        ('ppc', 'Present perfect continuous', 'eng11-u13-l1', ['eng11-u13-ppc1', 'eng11-u13-ppc2']),
        ('future', 'Future forms', 'eng11-u13-l1', ['eng11-u13-l1-r2wk1'])])


Q_TIP = 'Direct question: (wh-word) + auxiliary + subject + verb? Indirect question (after "Do you know…", "He asked…"): wh-word/if + subject + verb, no do/does/did.'


def questions(b):
    u = b.unit('eng11-u14')
    u['title'] = 'Making questions (direct and indirect)'
    u['intro'] = 'How to make yes/no questions, wh-questions, subject questions and polite indirect questions – four short rules.'
    _, l = b.lesson('eng11-u14-l1')
    l['title'] = 'Making questions'
    b.replace_card(grammar('eng11-u14-c01', 'Four rules for questions', [
        '**Yes/no question:** put the helping verb **before** the subject: *She is ready.* → ***Is she** ready?* No helping verb? Use **do / does / did** + base verb: *He plays.* → ***Does he play**?* *They left.* → ***Did they leave**?*',
        '**Wh-question:** wh-word + the yes/no question: *Where **does she live**? Why **did you leave**? What **are** they **doing**?*',
        '**Subject question:** when *who/what* **is** the subject, keep normal order and add no do/does/did: ***Who broke** the window?* (✗ Who did break…?) ***What happened**?*',
        '**Indirect question** (after *Do you know…? Can you tell me…? I wonder… He asked…*): normal order, **no** do/does/did, and **if/whether** for yes/no: *Can you tell me **where the station is**? I asked **if she was** ready.*',
    ], [
        ('Why didn\'t you submit your project?', True),
        ('Where you live?', False, 'Where do you live?'),
        ('Who did see the accident?', False, 'Who saw the accident?'),
        ('Can you tell me where is the bank?', False, 'Can you tell me where the bank is?'),
    ], pattern='(Wh) + aux + S + V?  ·  Who/What + V?  ·  …tell me + wh/if + S + V'))
    b.replace_card(table('eng11-u14-c02', 'From statement to question', ['Statement', 'Yes/no question', 'Wh-question', 'Indirect question'], [
        ['She **is** at home.', '**Is she** at home?', 'Where **is she**?', 'Do you know where **she is**?'],
        ['He **works** in Asmara.', '**Does he work** in Asmara?', 'Where **does he work**?', 'Can you tell me where **he works**?'],
        ['They **left** at six.', '**Did they leave** at six?', 'When **did they leave**?', 'I wonder when **they left**.'],
        ['She **can** swim.', '**Can she** swim?', 'How well **can she** swim?', 'He asked **if she could** swim.'],
        ['**Samuel** helped Ruth.', '**Did Samuel help** Ruth?', '**Who helped** Ruth? (subject)', 'I don\'t know **who helped** Ruth.'],
    ]))
    b.put_questions('eng11-u14', [
        mcq('eng11-u14-iq01', '____ the bus to Keren leave?', {'A': 'When', 'B': 'When does', 'C': 'When do', 'D': 'When is'}, 'B',
            ['No helping verb in *the bus leaves* → add **does** (3rd person singular).', 'The verb goes back to the base form: *leave*.'], Q_TIP,
            [('Make a question: "She teaches maths." (What…?)', 'What does she teach?')]),
        mcq('eng11-u14-iq02', 'Could you tell me ____?', {'A': 'how much does this cost', 'B': 'how much this costs', 'C': 'how much costs this', 'D': 'how much is this cost'}, 'B',
            ['After *Could you tell me* the question is indirect.', 'Indirect = normal order, no *does*: *how much this costs*.'], Q_TIP,
            [('Make it indirect: "Where is the post office?" (Do you know…)', 'Do you know where the post office is?')]),
        mcq('eng11-u14-iq03', '____ the national football match last night?', {'A': 'Who did win', 'B': 'Who won', 'C': 'Who wins did', 'D': 'Who was win'}, 'B',
            ['*Who* is the subject (someone won).', 'Subject question: normal order, no *did*.'], Q_TIP,
            [('Ask about the subject: "Ruth called the doctor."', 'Who called the doctor?')]),
        fill('eng11-u14-iq04', 'She asked me ____ I had finished my homework.', 'if', ['if', 'that', 'did', 'what'],
             ['Reported yes/no question → *if* (or *whether*).'], Q_TIP, [('Report: "Are you hungry?" he asked.', 'He asked if I was hungry.')]),
        short('eng11-u14-iq05', 'Correct the error: "I don\'t know where does he live."', 'I don\'t know where he lives.',
              ['Indirect question → no *does*, normal order.', 'Put the -s back on the verb: *he lives*.'], Q_TIP,
              [('Correct: "Tell me what did you buy."', 'Tell me what you bought.')], accept=["I don't know where he lives", 'I do not know where he lives.']),
    ])
    u['unitMap'] = unitmap('eng11-u14', 'Making questions', [
        ('direct', 'Direct questions', 'eng11-u14-l1', ['eng11-u14-c01', 'eng11-u14-l1-r2wk2']),
        ('indirect', 'Indirect questions', 'eng11-u14-l1', ['eng11-u14-c02', 'eng11-u14-c03'])])


TAG_TIP = 'Positive sentence → negative tag; negative sentence → positive tag. Repeat the helping verb (no helping verb → do/does/did) and use a pronoun.'
TAG_ROWS = [
    ['Positive sentence → negative tag', 'She is tired, **isn\'t she**?'],
    ['Negative sentence → positive tag', 'They aren\'t ready, **are they**?'],
    ['Repeat the same helping verb', 'You can swim, **can\'t you**? He has left, **hasn\'t he**?'],
    ['No helping verb → do / does / did', 'You live here, **don\'t you**? He played well, **didn\'t he**?'],
    ['I am → aren\'t I', 'I\'m late, **aren\'t I**?  (but: I\'m not late, **am I**?)'],
    ['Let\'s → shall we', 'Let\'s go, **shall we**?'],
    ['Orders and requests → will you / won\'t you', 'Close the door, **will you**?'],
    ['never, hardly, seldom, nobody, nothing → positive tag', 'He never comes late, **does he**?'],
    ['There is / there are → there', 'There is a problem, **isn\'t there**?'],
    ['everyone, someone, nobody → they', 'Nobody called, **did they**?'],
    ['this / that / nothing / everything → it', 'That was easy, **wasn\'t it**? Nothing happened, **did it**?'],
]


def tags(b):
    u = b.unit('eng11-u15')
    u['intro'] = 'A question tag is a short question at the end of a sentence (…, isn\'t it?). One table holds all the rules.'
    b.replace_card(grammar('eng11-u15-c01', 'Question tags: how to make them', [
        'A **question tag** is a mini-question at the end of a sentence. We use it to check something or to ask the listener to agree: *It\'s hot today, **isn\'t it**?*',
        '**Step 1:** Is the sentence positive or negative? Positive → **negative** tag. Negative → **positive** tag.',
        '**Step 2:** Find the helping verb (*is, are, was, can, will, have, should…*) and repeat it. No helping verb? Use **do / does / did**.',
        '**Step 3:** Use a **pronoun** for the subject: *Aster* → *she*; *the boys* → *they*; *this/that* → *it*.',
        'Learn the special cases in the table: *I am → aren\'t I*, *Let\'s → shall we*, orders → *will you*, *never/nobody* → positive tag.',
    ], [
        ('You are coming, aren\'t you?', True),
        ('She didn\'t call, did she?', True),
        ('He plays football, isn\'t it?', False, 'He plays football, doesn\'t he?'),
        ('I am late, am not I?', False, 'I am late, aren\'t I?'),
    ], pattern='positive sentence, negative tag?  ·  negative sentence, positive tag?'))
    b.replace_card(table('eng11-u15-c02', 'Question tags: key rules', ['Rule', 'Example'], TAG_ROWS))
    b.put_cards('eng11-u15-l1', [
        check('eng11-u15-tg1', 'Everyone enjoyed the wedding, ____?', {'A': "didn't he", 'B': "didn't they", 'C': 'did they', 'D': "wasn't it"}, 'B', [
            '**Step 1:** Positive sentence → negative tag.', '**Step 2:** No helping verb, past → *didn\'t*.', '**Step 3:** *everyone* → *they*.', f'**Tip:** {TAG_TIP}']),
        check('eng11-u15-tg2', 'She hardly ever eats meat, ____?', {'A': "doesn't she", 'B': 'does she', 'C': "isn't she", 'D': 'is she'}, 'B', [
            '**Step 1:** *hardly ever* makes the sentence negative in meaning.', '**Step 2:** Negative sentence → positive tag.',
            '**Step 3:** No helping verb, present, *she* → *does she*.', f'**Tip:** {TAG_TIP}']),
        check('eng11-u15-tg3', 'Pass me the salt, ____?', {'A': "don't you", 'B': 'will you', 'C': 'shall we', 'D': 'do you'}, 'B', [
            '**Step 1:** This is an order/request (imperative).', '**Step 2:** Orders and requests take *will you?* (or *won\'t you?* / *could you?*).',
            '**Step 3:** *shall we* is only for *Let\'s*.', f'**Tip:** {TAG_TIP}']),
    ], after='eng11-u15-l1-r2wk1')
    sim = [('Add a tag: "They have finished, ___?"', "haven't they?"), ('Add a tag: "Let\'s start, ___?"', 'shall we?')]
    b.put_questions('eng11-u15', [
        mcq('eng11-u15-tgq01', 'There isn\'t any water left, ____?', {'A': 'is it', 'B': 'is there', 'C': "isn't there", 'D': 'are there'}, 'B',
            ['Negative sentence → positive tag.', '*There is* → tag with *there*: *is there?*'], TAG_TIP, sim),
        mcq('eng11-u15-tgq02', 'Your brother works in Massawa, ____?', {'A': "isn't he", 'B': "doesn't he", 'C': "don't he", 'D': 'does he'}, 'B',
            ['Positive, no helping verb, present, *he* → *doesn\'t he?*'], TAG_TIP, sim),
        mcq('eng11-u15-tgq03', 'Nothing can stop us now, ____?', {'A': "can't it", 'B': 'can it', 'C': "can't they", 'D': 'can we'}, 'B',
            ['*Nothing* is negative → positive tag.', '*Nothing* → *it*; repeat *can*: *can it?*'], TAG_TIP, sim),
        fill('eng11-u15-tgq04', 'You won\'t forget to call me, ____?', 'will you', ['will you', "won't you", 'do you', 'shall you'],
             ['Negative sentence (*won\'t*) → positive tag *will you?*'], TAG_TIP, sim),
        fill('eng11-u15-tgq05', 'I\'m in the right room, ____?', "aren't I", ["aren't I", 'am not I', "amn't I", "isn't it"],
             ['Special case: *I am* → *aren\'t I?*'], TAG_TIP, sim),
        short('eng11-u15-tgq06', 'Correct the tag: "They had a good time, hadn\'t they?"', "They had a good time, didn't they?",
              ['Here *had* is the main verb (= enjoyed), not a helping verb.', 'Main verb in the past → *didn\'t they?*'], TAG_TIP, sim,
              accept=["didn't they?", "They had a good time, didn't they"]),
    ])
    u['unitMap'] = unitmap('eng11-u15', 'Question tags', [
        ('rules', 'How to make a tag', 'eng11-u15-l1', ['eng11-u15-c01', 'eng11-u15-l1-r2wk1']),
        ('special', 'Key rules and special cases', 'eng11-u15-l1', ['eng11-u15-c02', 'eng11-u15-tg2'])])


WF_TIP = 'First decide which word class the gap needs (noun after a/the, adjective before a noun or after be, adverb for how). Then add the suffix. Prefixes change the meaning, not the word class.'


def word_formation(b):
    u = b.unit('eng11-u16')
    u['title'] = 'Word formation: prefixes, suffixes, compounds'
    u['intro'] = 'We make new words in four simple ways: add a prefix, add a suffix, join two words (compound), or use the same word as a new word class (conversion).'
    _, l = b.lesson('eng11-u16-l1')
    l['title'] = 'Prefixes, suffixes, compounds and conversion'
    b.replace_card(grammar('eng11-u16-c01', 'Four ways to make new words', [
        '**1. Prefix** = letters added at the **start** of a word. It changes the **meaning**: *happy → **un**happy, write → **re**write, agree → **dis**agree*.',
        '**2. Suffix** = letters added at the **end** of a word. It usually changes the **word class**: *depart (verb) → depart**ure** (noun), care (noun) → care**ful** (adjective), quick → quick**ly** (adverb)*.',
        '**3. Compound** = two words joined to make one: *class + room → **classroom**, black + board → **blackboard**, mother-in-law, bus stop*.',
        '**4. Conversion** = the **same word** used as a different word class, with no change: *a **text** (noun) → to **text** someone (verb); a **book** → to **book** a room*.',
        '**How to answer word-formation questions:** look at the gap. After *a/an/the* or an adjective → **noun**. Before a noun or after *be/seem* → **adjective**. Telling *how* → **adverb**. Then choose the right ending.',
    ], [
        ('The sudden departure of the principal surprised everyone.', True),
        ('The instructions were unclear.', True),
        ('The instructions were disclear.', False, 'The instructions were unclear.'),
        ('She sings beautiful.', False, 'She sings beautifully.'),
    ], pattern='prefix + word  ·  word + suffix  ·  word + word  ·  same word, new class'))
    b.replace_card(table('eng11-u16-c02', 'Common prefixes (change the meaning)', ['Prefix', 'Meaning', 'Examples'], [
        ['un-', 'not', 'unhappy, unclear, unable, unknown'], ['in- / im- / il- / ir-', 'not', 'incorrect, impossible, illegal, irregular'],
        ['dis-', 'not / opposite', 'disagree, dishonest, disappear'], ['mis-', 'wrongly', 'misunderstand, misspell, mislead'],
        ['re-', 'again', 'rewrite, rebuild, retell'], ['pre-', 'before', 'prepare, preview, pre-school'],
        ['over-', 'too much', 'overeat, overwork, overcrowded'], ['under-', 'too little / below', 'underpaid, underground'],
        ['inter-', 'between', 'international, interview'], ['co-', 'together', 'cooperate, co-worker'],
    ]))
    b.put_cards('eng11-u16-l1', [
        table('eng11-u16-wf1', 'Common suffixes (change the word class)', ['Suffix', 'Makes a…', 'Examples'], [
            ['-tion / -sion', 'noun', 'decide → decision, inform → information, educate → education'],
            ['-ment', 'noun', 'agree → agreement, develop → development'],
            ['-ness / -ity', 'noun', 'kind → kindness, able → ability, honest → honesty'],
            ['-er / -or / -ist', 'noun (person)', 'teach → teacher, act → actor, science → scientist'],
            ['-ance / -ence / -ure', 'noun', 'perform → performance, differ → difference, depart → departure'],
            ['-ful / -less', 'adjective', 'care → careful, careless; hope → hopeful, hopeless'],
            ['-ous / -ive / -al / -able', 'adjective', 'danger → dangerous, act → active, nation → national, read → readable'],
            ['-y', 'adjective', 'rain → rainy, health → healthy'],
            ['-ise / -ify / -en', 'verb', 'modern → modernise, simple → simplify, short → shorten'],
            ['-ly', 'adverb', 'quick → quickly, careful → carefully'],
        ]),
        table('eng11-u16-wf2', 'Compound words', ['Type', 'Examples'], [
            ['one word', 'classroom, blackboard, football, sunrise, homework'], ['with a hyphen', 'mother-in-law, well-known, part-time, twenty-one'],
            ['two separate words', 'bus stop, post office, high school, police station'],
        ]),
        table('eng11-u16-wf3', 'Conversion (same word, new class)', ['Word', 'As a noun', 'As a verb'], [
            ['text', 'I got your **text**.', 'Please **text** me.'], ['book', 'a good **book**', 'to **book** a room'],
            ['water', 'a glass of **water**', 'to **water** the plants'], ['email', 'send an **email**', 'to **email** the teacher'],
            ['visit', 'a short **visit**', 'to **visit** Axum'],
        ]),
        worked('eng11-u16-wf4', 'Step by step: choose the right form', 'Complete: "The ____ (develop) of the town was ____ (success) because the people worked ____ (careful)."', [
            '**Step 1: What does each gap need?** After *The* → noun. After *was* → adjective. After the verb *worked*, telling how → adverb.',
            '**Step 2: Add the ending.** develop + -ment → **development**; success + -ful → **successful**; careful + -ly → **carefully**.',
            '**Step 3: Read the sentence again** to check the meaning and spelling.',
        ], 'development, successful, carefully'),
        check('eng11-u16-wf5', 'The opposite of "legal" is ____.', {'A': 'unlegal', 'B': 'dislegal', 'C': 'illegal', 'D': 'inlegal'}, 'C', [
            '**Step 1:** All four prefixes can mean *not*.', '**Step 2:** Before a word starting with **l** we use **il-**: *illegal, illogical*.',
            '**Step 3:** Before **r** → *ir-* (irregular); before **m/p** → *im-* (impossible).', f'**Tip:** {WF_TIP}']),
        check('eng11-u16-wf6', 'Which word is a compound?', {'A': 'kindness', 'B': 'unhappy', 'C': 'classroom', 'D': 'quickly'}, 'C', [
            '**Step 1:** A compound joins two complete words.', '**Step 2:** *class + room = classroom*.',
            '**Step 3:** A has a suffix, B a prefix, D a suffix.', f'**Tip:** {WF_TIP}']),
    ], after='eng11-u16-c02')
    sim = [('Make a noun from "decide".', 'decision'), ('Make an adjective from "danger".', 'dangerous')]
    b.put_questions('eng11-u16', [
        mcq('eng11-u16-wfq01', 'Many students ____ the question and gave the wrong answer.', {'A': 'disunderstood', 'B': 'misunderstood', 'C': 'ununderstood', 'D': 'reunderstood'}, 'B',
            ['*mis-* = wrongly.', '*misunderstood* = understood wrongly.'], WF_TIP, sim),
        mcq('eng11-u16-wfq02', 'Thank you for your ____. It helped me a lot.', {'A': 'kind', 'B': 'kindly', 'C': 'kindness', 'D': 'unkind'}, 'C',
            ['After *your* we need a noun.', 'kind + -ness → *kindness*.'], WF_TIP, sim),
        mcq('eng11-u16-wfq03', 'The road was very ____ after the heavy rain.', {'A': 'danger', 'B': 'dangerous', 'C': 'dangerously', 'D': 'endanger'}, 'B',
            ['After *was very* we need an adjective.', 'danger + -ous → *dangerous*.'], WF_TIP, sim),
        fill('eng11-u16-wfq04', 'Please drive ____ (care). The road is narrow.', 'carefully', ['carefully', 'careful', 'careless', 'care'],
             ['It tells *how* to drive → adverb.', 'care + -ful + -ly → carefully.'], WF_TIP, sim),
        fill('eng11-u16-wfq05', 'Eritrea is famous for the ____ (beautiful) of its Red Sea coast.', 'beauty', ['beauty', 'beautiful', 'beautify', 'beautifully'],
             ['After *the* we need a noun.', 'The noun is *beauty*.'], WF_TIP, sim),
        fill('eng11-u16-wfq06', 'It is ____ (possible) to finish all this work in one day.', 'impossible', ['impossible', 'unpossible', 'inpossible', 'dispossible'],
             ['The meaning is *not possible*.', 'Before **p** we use *im-*.'], WF_TIP, sim),
        tf('eng11-u16-wfq07', 'True or false: In "Please text me tonight", "text" is a verb made by conversion.', True,
           ['True. *text* is usually a noun (a text message).', 'Here it is used as a verb with no change in form – that is conversion.'], WF_TIP,
           [('Which word class is "book" in "I want to book a ticket"?', 'verb (conversion)')]),
        short('eng11-u16-wfq08', 'Make two words from "employ": a person who works for someone, and the opposite of having a job.', 'employee, unemployment',
              ['employ + -ee → *employee* (the worker); employ + -er → employer (the boss).', 'un- + employ + -ment → *unemployment*.'], WF_TIP, sim,
              accept=['employee and unemployment', 'employee, unemployed']),
    ])
    u['unitMap'] = unitmap('eng11-u16', 'Word formation', [
        ('prefix', 'Prefixes', 'eng11-u16-l1', ['eng11-u16-c02']),
        ('suffix', 'Suffixes', 'eng11-u16-l1', ['eng11-u16-wf1', 'eng11-u16-l1-r2wk2']),
        ('compound', 'Compounds and conversion', 'eng11-u16-l1', ['eng11-u16-wf2', 'eng11-u16-wf3'])])


PREP_TIP = 'at = a point (at 6, at the door); on = a surface / a day (on the table, on Monday); in = inside / a longer period (in the box, in May, in 2026).'


def prepositions(b):
    u = b.unit('eng11-u18')
    u['title'] = 'Prepositions'
    u['intro'] = 'Prepositions of place, time and movement in simple tables, the most common mistakes, then the word + preposition pairs you must learn by heart.'
    _, l1 = b.lesson('eng11-u18-l1')
    l1['title'] = 'Prepositions of place, time and movement'
    b.put_lesson('eng11-u18', dict(id='eng11-u18-l2', number='18.2', title='Word + preposition (fixed pairs)', pages=list(l1['pages']), cards=[]), after='eng11-u18-l1')
    for cid in ('eng11-u18-c02', 'eng11-u18-c03', 'eng11-u18-c11', 'eng11-u18-chk1', 'eng11-u18-c12', 'eng11-u18-chk2', 'eng11-u18-c13', 'eng11-u18-chk3'):
        b.move_card(cid, 'eng11-u18-l2')
    b.replace_card(grammar('eng11-u18-c01', 'What is a preposition?', [
        'A **preposition** is a small word before a noun or pronoun. It shows **where** (*in the box*), **when** (*on Monday*) or **how something moves** (*into the room*).',
        '**at, on, in** are the most common. Think of size: **at** = a point, **on** = a surface or a day, **in** = inside or a longer time.',
        'After a preposition use a **noun**, an **object pronoun** (*me, him, them*) or a verb + **-ing**: *with **him**, before **leaving*** (✗ before leave).',
        'Many words have a fixed partner: *good **at**, interested **in**, depend **on***. Learn them as pairs (see 18.2).',
    ], [
        ('The meeting is at 3 o\'clock on Friday.', True),
        ('I was born on 2008.', False, 'I was born in 2008.'),
        ('She is good at maths.', True),
        ('He entered into the room.', False, 'He entered the room. / He went into the room.'),
    ], pattern='at (point) · on (surface / day) · in (inside / long time)'))
    b.put_cards('eng11-u18-l1', [
        table('eng11-u18-pp1', 'Prepositions of place', ['Preposition', 'Use', 'Example'], [
            ['in', 'inside something; towns, countries', 'in the box, in the classroom, in Asmara, in Eritrea'],
            ['on', 'on a surface; streets (US), floors', 'on the table, on the wall, on the second floor'],
            ['at', 'a point or a place for an activity', 'at the door, at the bus stop, at school, at home'],
            ['under / below', 'lower than', 'The cat is under the chair.'],
            ['above / over', 'higher than', 'The clock is above the board.'],
            ['next to / beside', 'at the side of', 'Sit next to Helen.'],
            ['between', 'in the middle of two', 'The bank is between the post office and the school.'],
            ['in front of / behind', 'before / at the back of', 'The car is in front of the house.'],
            ['opposite', 'facing, on the other side', 'The shop is opposite the church.'],
        ]),
        table('eng11-u18-pp2', 'Prepositions of time', ['Preposition', 'Use', 'Example'], [
            ['at', 'clock times; night; festivals (short)', 'at 7 o\'clock, at night, at noon, at the weekend (UK)'],
            ['on', 'days and dates', 'on Monday, on 24 May, on Independence Day, on my birthday'],
            ['in', 'months, years, seasons, parts of the day', 'in May, in 2026, in summer, in the morning'],
            ['for', 'a length of time', 'for two hours, for ten years'],
            ['since', 'from a starting point until now', 'since 2019, since Monday'],
            ['during', 'all through a period', 'during the holiday'],
            ['by', 'not later than', 'Finish it by Friday.'],
            ['until / till', 'up to a time', 'Wait until six.'],
            ['from … to', 'start and end', 'from 8 to 12'],
        ]),
        table('eng11-u18-pp3', 'Prepositions of movement', ['Preposition', 'Meaning', 'Example'], [
            ['to', 'towards a place (goal)', 'We went to Massawa.'], ['into / out of', 'entering / leaving', 'She walked into the room. He ran out of the house.'],
            ['onto / off', 'moving on / away from a surface', 'The cat jumped onto the table. He fell off his bike.'],
            ['across', 'from one side to the other', 'Walk across the bridge.'], ['through', 'inside, from one end to the other', 'The train went through the tunnel.'],
            ['along', 'following a line', 'We walked along the river.'], ['up / down', 'higher / lower', 'They climbed up the hill.'],
            ['past', 'going by', 'We drove past the school.'], ['towards', 'in the direction of', 'He ran towards the gate.'],
            ['over / under', 'above / below, to the other side', 'The plane flew over the city.'],
        ]),
        table('eng11-u18-pp4', 'Common mistakes', ['Wrong', 'Right', 'Why'], [
            ['in Monday', 'on Monday', 'days → on'], ['on 2008 / at May', 'in 2008 / in May', 'years and months → in'],
            ['at the morning', 'in the morning', 'parts of the day → in (but at night)'], ['since three years', 'for three years', 'length of time → for'],
            ['arrive to Asmara', 'arrive in Asmara / arrive at the station', 'arrive in (city) / at (place)'],
            ['enter into the room', 'enter the room', 'enter needs no preposition'], ['discuss about', 'discuss (no preposition)', 'discuss + object'],
            ['married with', 'married to', 'fixed pair'], ['angry on him', 'angry with him', 'angry with a person'], ['good in maths', 'good at maths', 'fixed pair'],
        ]),
        check('eng11-u18-pp5', 'The school year in Eritrea usually starts ____ September.', {'A': 'on', 'B': 'at', 'C': 'in', 'D': 'by'}, 'C', [
            '**Step 1:** *September* is a month.', '**Step 2:** Months, years and seasons take **in**.',
            '**Step 3:** For a date we would say *on 1 September*.', f'**Tip:** {PREP_TIP}']),
        check('eng11-u18-pp6', 'The children ran ____ the classroom when the bell rang.', {'A': 'out of', 'B': 'at', 'C': 'on', 'D': 'since'}, 'A', [
            '**Step 1:** *ran* shows movement.', '**Step 2:** Leaving an inside place → **out of**.',
            '**Step 3:** *at* and *on* show position, not movement.', f'**Tip:** {PREP_TIP}']),
        check('eng11-u18-pp7', 'I\'ll meet you ____ the bus stop ____ 4 o\'clock.', {'A': 'in / on', 'B': 'at / at', 'C': 'on / in', 'D': 'at / on'}, 'B', [
            '**Step 1:** *the bus stop* is a point → **at**.', '**Step 2:** Clock times → **at**.', '**Step 3:** So: *at the bus stop at 4 o\'clock*.', f'**Tip:** {PREP_TIP}']),
    ], after='eng11-u18-c01')
    b.replace_card(text('eng11-u18-c02', 'Word + preposition: learn them as pairs', [
        'Some verbs, adjectives and nouns always go with the **same** preposition. We cannot guess it from Tigrinya, so learn each word **with** its partner.',
        '**Adjective + preposition:** good/bad **at**, interested **in**, afraid/proud/tired **of**, famous **for**, angry **with** (a person), married **to**, different **from**.',
        '**Verb + preposition:** depend/rely **on**, congratulate someone **on**, accuse someone **of**, suffer **from**, listen **to**, belong **to**, wait **for**, apologise **for**.',
        '**Noun + preposition:** the reason **for**, the key/answer/solution **to**, an increase **in**, a cause **of**.',
        'After these prepositions a verb takes **-ing**: *interested in **learning**, congratulated on **passing**.*',
    ]))
    b.replace_card(table('eng11-u18-c03', 'Fixed pairs', ['Word', 'Preposition', 'Example'], [
        ['good / bad / clever', 'at', 'She is good **at** chemistry.'], ['proud / afraid / tired', 'of', 'We are proud **of** your results.'],
        ['interested', 'in', 'He is interested **in** history.'], ['congratulate (someone)', 'on', 'I congratulate you **on** passing.'],
        ['accuse (someone)', 'of', 'They accused him **of** theft.'], ['depend / rely', 'on', 'It depends **on** the weather.'],
        ['suffer', 'from', 'She suffers **from** headaches.'], ['solution / key / answer', 'to', 'What is the key **to** success?'],
        ['reason', 'for', 'There is no reason **for** anger.'],
    ]))
    sim = [('Complete: "My birthday is ___ 12 June."', 'on'), ('Complete: "She is afraid ___ dogs."', 'of')]
    b.put_questions('eng11-u18', [
        mcq('eng11-u18-ppq01', 'We usually go to church ____ Sunday morning.', {'A': 'in', 'B': 'at', 'C': 'on', 'D': 'by'}, 'C',
            ['*Sunday morning* is a particular day → **on**.', '(But: *in the morning* alone.)'], PREP_TIP, sim),
        mcq('eng11-u18-ppq02', 'The cat jumped ____ the wall and ran away.', {'A': 'over', 'B': 'at', 'C': 'in', 'D': 'since'}, 'A',
            ['Movement from one side to the other, higher up → **over**.'], PREP_TIP, sim),
        mcq('eng11-u18-ppq03', 'The pharmacy is ____ the bank and the post office.', {'A': 'among', 'B': 'between', 'C': 'across', 'D': 'through'}, 'B',
            ['In the middle of **two** things → **between**.', '*among* is for more than two.'], PREP_TIP, sim),
        mcq('eng11-u18-ppq04', 'I have lived in Mendefera ____ 2015.', {'A': 'for', 'B': 'since', 'C': 'from', 'D': 'in'}, 'B',
            ['*2015* is the starting point and the action continues now → **since**.'], PREP_TIP, sim),
        fill('eng11-u18-ppq05', 'Please hand in your essays ____ Friday at the latest.', 'by', ['by', 'until', 'since', 'during'],
             ['*by* = not later than.', '*until* = continuing up to a time (*wait until Friday*).'], PREP_TIP, sim),
        fill('eng11-u18-ppq06', 'The train went ____ a long dark tunnel.', 'through', ['through', 'across', 'along', 'onto'],
             ['Inside something, from one end to the other → **through**.'], PREP_TIP, sim),
        fill('eng11-u18-ppq07', 'Many people suffer ____ malaria in the lowlands.', 'from', ['from', 'of', 'with', 'by'],
             ['Fixed pair: *suffer from*.'], PREP_TIP, sim),
        short('eng11-u18-ppq08', 'Correct the two errors: "I will see you in Monday at the afternoon."', 'I will see you on Monday in the afternoon.',
              ['Days → **on** (*on Monday*).', 'Parts of the day → **in** (*in the afternoon*).'], PREP_TIP, sim,
              accept=['I will see you on Monday in the afternoon', "I'll see you on Monday in the afternoon."]),
    ])
    u['games'][0]['lesson'] = 'eng11-u18-l2'
    u['games'] = [g for g in u['games'] if g['id'] != 'eng11-u18-g2']
    u['games'].append(dict(id='eng11-u18-g2', type='match', title='Place, time or movement?', src='notes', lesson='eng11-u18-l1', pairs=[
        {'a': 'on Monday', 'b': 'time (day)'}, {'a': 'in 2026', 'b': 'time (year)'}, {'a': 'at the bus stop', 'b': 'place (point)'},
        {'a': 'on the table', 'b': 'place (surface)'}, {'a': 'into the room', 'b': 'movement (entering)'}, {'a': 'across the road', 'b': 'movement (side to side)'}]))
    u['tips'] = [dict(text=PREP_TIP, page=l1['pages'][0], src='notes', card='eng11-u18-pp2'),
                 dict(text='Learn fixed pairs together: good at, interested in, depend on, congratulate on, suffer from.', page=l1['pages'][0], src='notes')]
    u['unitMap'] = unitmap('eng11-u18', 'Prepositions', [
        ('place', 'Place', 'eng11-u18-l1', ['eng11-u18-pp1']), ('time', 'Time', 'eng11-u18-l1', ['eng11-u18-pp2']),
        ('movement', 'Movement', 'eng11-u18-l1', ['eng11-u18-pp3', 'eng11-u18-pp4']),
        ('pairs', 'Word + preposition', 'eng11-u18-l2', ['eng11-u18-c02', 'eng11-u18-c03'])])


def apply(b):
    tenses(b)
    questions(b)
    tags(b)
    word_formation(b)
    prepositions(b)
