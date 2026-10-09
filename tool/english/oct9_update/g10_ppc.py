"""Grade 10 Unit 8, lesson 8.3: complete the present perfect continuous lesson.
Textbook: Unit 8, Lesson 8.13 'Expressing a continuous action' (page 167) teaches the present continuous for an action that
continues over a period of time; the present perfect continuous says HOW LONG such an action has been going on.
The book itself uses it on page 170 (Lesson 8.15: 'So far you have been writing mainly individual paragraphs')."""
from lib import table, text, worked, check, mcq, fill, tf, short

P = 167
L = 'eng10-u8-l8-3'
TIP = ('Clue words: for / since / How long? / all day / lately → have been + -ing. How many? / a number / finished result → have + 3rd form. '
       'At a past moment (at 8 last night, when…) → was/were + -ing. Finished time (yesterday, ago) → past, never have been.')


def cards(b):
    new = [
        text(L + '-t1', 'Link with Lesson 8.13: from "is doing" to "has been doing"', [
            'In Lesson 8.13 the writer of the job letter says: *Currently, I**\'m attending** a three-month programme in secretarial science.* That is the **present continuous**: an action that goes on over a period around now.',
            'Now ask **How long?** – *He started two months ago and he is still on the course.* → *He **has been attending** the programme **for two months**.* That is the **present perfect continuous**.',
            'Your textbook uses it too: *So far you **have been writing** mainly individual paragraphs.* (Lesson 8.15, page 170) – the writing started in earlier lessons and goes on until now.',
            '**Step 1:** Is the action still going on (or has it just stopped)? **Step 2:** Do you say how long (for / since / all day)? **Step 3:** Use **have/has + been + verb-ing**.',
        ], page=P),
        table(L + '-t2', 'When do we use it? Three uses', ['Use', 'Clue words', 'Example'], [
            ['1. It started in the past and is **still going on now**.', 'for, since, How long…?, all day, all morning', 'Aman **has been studying** for the matric exam **since September**.'],
            ['2. It has **just stopped** and you can **see the result** now.', 'no time word; a result: tired, wet, dirty, red eyes', 'The road is wet. It **has been raining**.'],
            ['3. It has happened **again and again** in the last days or weeks.', 'recently, lately, these days', 'I**\'ve been getting up** at 5 o\'clock **lately** to study.'],
        ], page=P),
        table(L + '-t3', 'Time words: for, since, How long, recently, all day', ['Word', 'What it means', 'Example'], [
            ['**for**', 'a **length** of time: for two hours, for a week, for ten years, for a long time', 'We **have been waiting for** the bus **for** forty minutes.'],
            ['**since**', 'the **starting point**: since 8 o\'clock, since Monday, since 2020, since I was ten', 'Mr Tesfay **has been teaching** in Mendefera **since** 2015.'],
            ['**How long…?**', 'asks about the length: How long + have/has + subject + been + -ing?', '**How long have** you **been living** in Dekemhare?'],
            ['**recently / lately**', 'in the last few days or weeks (put it at the end)', 'My grandmother **has been feeling** better **lately**.'],
            ['**all day / all morning / all week**', 'the whole time (no *for* before *all*)', 'The farmers **have been ploughing all morning**.'],
            ['✗ **ago**', '*ago* is a finished time → past simple, never *have been*', 'I **started** two hours **ago**. / I **have been working for** two hours.'],
        ], page=P),
        table(L + '-t4', 'Side by side: three tenses that look alike', ['', 'Present perfect continuous', 'Present perfect simple', 'Past continuous'], [
            ['Form', 'have/has **been** + verb-ing', 'have/has + 3rd form', 'was/were + verb-ing'],
            ['Time', 'from the past **up to now**', 'a past action with a result **now**', 'in progress **at a past moment** (it is finished now)'],
            ['Question it answers', 'How long?', 'How many? How much? Is it done?', 'What was happening at that time?'],
            ['Example 1', 'Senait **has been cooking** since 6. (she is still cooking)', 'Senait **has cooked** three dishes. (they are ready – look!)', 'Senait **was cooking** at 6 yesterday. (that was yesterday)'],
            ['Example 2', 'My uncle **has been ploughing** the field all morning.', 'He **has ploughed** two fields.', 'He **was ploughing** when it started to rain.'],
            ['Time words', 'for, since, How long, all day, lately', 'already, yet, just, ever, never, so far, three times', 'at 8 last night, when…, while…, at that moment'],
            ['Connected to now?', 'Yes: still going on, or just stopped', 'Yes: the result matters now', 'No: it is about a past time'],
        ], page=P),
        worked(L + '-t5', 'Step by step: which of the three tenses?',
               'Complete with has been + -ing, has + 3rd form, or was + -ing: (a) Look at Daniel\'s hands! He ____ (repair) bicycles all morning. '
               '(b) He ____ (repair) four bicycles so far. (c) At 10 o\'clock yesterday he ____ (repair) my bicycle when the electricity went off. '
               '(d) How long ____ you ____ (wait) here? – Since 3 o\'clock.', [
                   '**Step 1: Is it about a past moment that is finished?** (c) *At 10 o\'clock yesterday … when the electricity went off* → yes → past continuous: **was repairing**.',
                   '**Step 2: Is there a number or a finished result?** (b) *four bicycles so far* → how many → present perfect simple: **has repaired**.',
                   '**Step 3: Is it an activity that lasted up to now (how long)?** (a) *all morning* + dirty hands now → **has been repairing**. (d) *How long … ? – Since 3 o\'clock* → **have you been waiting**.',
                   '**Check the helper verb:** he/she/it → *has*; I/you/we/they → *have*; past continuous → *was/were*.',
               ], '(a) has been repairing (b) has repaired (c) was repairing (d) have … been waiting', page=P),
        table(L + '-t6', 'Common mistakes', ['Wrong', 'Right', 'Why'], [
            ['I am living in Keren since 2020.', 'I have been living in Keren since 2020.', 'From a past point up to now → have been + -ing, not am/is/are + -ing.'],
            ['She has been teach here for years.', 'She has been teaching here for years.', 'After *been* use verb + -ing.'],
            ['He have been working all day.', 'He has been working all day.', 'he / she / it → has.'],
            ['I have been waiting since two hours.', 'I have been waiting for two hours.', 'A length of time → for; a starting point → since.'],
            ['How long are you waiting?', 'How long have you been waiting?', 'How long + up to now → have been + -ing.'],
            ['Been you waiting long?', 'Have you been waiting long?', 'Question: Have/Has + subject + been + -ing?'],
            ['I have been knowing her for years.', 'I have known her for years.', '*know* is a state verb: no -ing.'],
            ['We have been visiting Massawa three times.', 'We have visited Massawa three times.', 'A number (how many) → have + 3rd form.'],
            ['It has been raining yesterday.', 'It rained yesterday. / It was raining yesterday.', 'A finished time (yesterday, ago) → past tense.'],
        ], page=P),
        table(L + '-t7', 'State verbs: no -ing, so no present perfect continuous', ['Group', 'Verbs', 'Say this ✔', 'Not this ✘'], [
            ['Thinking', 'know, understand, believe, remember, mean', 'I **have known** Aster since Grade 5.', 'I have been knowing Aster…'],
            ['Feeling', 'like, love, hate, want, need, prefer', 'She **has wanted** a bicycle for a long time.', 'She has been wanting…'],
            ['Having', 'own, belong, have (= own)', 'My father **has had** this shop for 20 years.', 'My father has been having this shop…'],
            ['Being', 'be, seem, contain', 'I **have been** in Asmara for a week.', 'I have been being in Asmara…'],
            ['But: action meanings are fine', 'have lunch, think about, see (= visit/meet)', 'I **have been thinking** about your idea. We**\'ve been having** lunch.', '—'],
        ], page=P),
        check(L + '-c12', 'When I phoned you at 8 o\'clock last night, you ____ dinner.', {'A': 'have been having', 'B': 'were having', 'C': 'have had', 'D': 'are having'}, 'B', [
            '**Step 1:** *at 8 o\'clock last night* is a moment in the past. It is finished now.',
            '**Step 2:** An action in progress at a past moment → past continuous: **were having**.',
            '**Step 3:** *have been having* would connect the action to **now** – but last night is not now.', f'**Tip:** {TIP}'], page=P),
        check(L + '-c13', 'I\'m tired. I ____ for the exam since 6 o\'clock this morning.', {'A': 'was studying', 'B': 'have studied', 'C': 'have been studying', 'D': 'study'}, 'C', [
            '**Step 1:** *since 6 o\'clock* = from a starting point up to now; *I\'m tired* = we see the result now.',
            '**Step 2:** An activity from the past up to now → **have been studying**.',
            '**Step 3:** *was studying* is only about the past; *study* is a habit.', f'**Tip:** {TIP}'], page=P),
        check(L + '-c14', 'Choose the correct sentence.', {'A': 'I have been owning this bicycle since 2022.', 'B': 'I have owned this bicycle since 2022.', 'C': 'I am owning this bicycle since 2022.', 'D': 'I own this bicycle since 2022.'}, 'B', [
            '**Step 1:** *own* is a state verb: it never takes -ing.',
            '**Step 2:** From 2022 until now → present perfect simple: **have owned**.',
            '**Step 3:** *own … since* (present simple) is wrong: *since* needs have/has.', f'**Tip:** {TIP}'], page=P),
        check(L + '-c15', 'Lately, my brother ____ to work by bus, because his car is broken.', {'A': 'has been going', 'B': 'went', 'C': 'was going', 'D': 'has gone'}, 'A', [
            '**Step 1:** *Lately* = again and again in the last days or weeks, up to now.',
            '**Step 2:** A repeated activity up to now → **has been going**.',
            '**Step 3:** *has gone* means one trip with a result (he is there now) – not a repeated activity.', f'**Tip:** {TIP}'], page=P),
    ]
    b.put_cards(L, new[:5], after=L + '-c4')
    b.put_cards(L, new[5:7], after=L + '-c6')
    b.put_cards(L, new[7:], after=L + '-c11')
    # the lesson's main card: add recently / lately and the difference from the past continuous
    c = b.card(L + '-c1')
    extra = '**Use 3 – it happened again and again recently, up to now** (*recently, lately, these days*): *I**\'ve been getting up** early **lately**.*'
    if extra not in c['rule']:
        c['rule'].insert(4, extra)
    extra2 = '**Not the past continuous:** *was/were + -ing* is for a moment in the **past** (*At 8 last night I **was reading***). *have been + -ing* reaches **now** (*I **have been reading** since 8*).'
    if extra2 not in c['rule']:
        c['rule'].append(extra2)


def questions(b):
    sim = [('Complete: "It ____ (rain) since morning."', 'has been raining'), ('Complete: "How long ____ you ____ (learn) English?"', 'have … been learning')]
    qs = [
        mcq('eng10-u8-ppq13', 'Mr Tesfay ____ mathematics at our school since 2015.', {'A': 'teaches', 'B': 'is teaching', 'C': 'has been teaching', 'D': 'taught'}, 'C',
            ['*since 2015* = a starting point; he is still teaching now.', 'From the past up to now → **has been teaching**.', '*is teaching since* is a common mistake: present continuous never goes with *since*.'], TIP, sim, page=P),
        mcq('eng10-u8-ppq14', 'At 7 o\'clock yesterday evening, my sister ____ her homework.', {'A': 'has been doing', 'B': 'was doing', 'C': 'has done', 'D': 'does'}, 'B',
            ['*At 7 o\'clock yesterday evening* = a moment in the past. It is finished now.', 'In progress at a past moment → past continuous: **was doing**.', '*has been doing* would reach now – wrong with *yesterday*.'], TIP,
            [('Complete: "At midnight we ____ (sleep)."', 'were sleeping'), ('Complete: "We ____ (sleep) for eight hours." (and we are still in bed)', 'have been sleeping')], page=P),
        mcq('eng10-u8-ppq15', 'Senait ____ three cups of coffee for the guests, and now she is making the fourth.', {'A': 'has been making', 'B': 'has made', 'C': 'was making', 'D': 'makes'}, 'B',
            ['*three cups* = a number (how many are ready).', 'How many → present perfect simple: **has made**.', 'Compare: *She has been making coffee for an hour* (how long).'], TIP,
            [('Choose: "I (have written / have been writing) two letters today."', 'have written'), ('Choose: "I (have written / have been writing) letters all morning."', 'have been writing')], page=P),
        mcq('eng10-u8-ppq16', 'How long ____ in Massawa?', {'A': 'do they live', 'B': 'are they living', 'C': 'have they been living', 'D': 'they have been living'}, 'C',
            ['*How long* asks about the time from the past up to now.', 'Question order: How long + **have** + subject + **been** + -ing?', 'D has statement order – wrong in a direct question.'], TIP,
            [('Make a question: "She has been working here." (How long…?)', 'How long has she been working here?')], page=P),
        mcq('eng10-u8-ppq17', 'I ____ him since we were in Grade 9.', {'A': 'have known', 'B': 'have been knowing', 'C': 'know', 'D': 'am knowing'}, 'A',
            ['*know* is a state verb → no -ing.', 'From Grade 9 until now → present perfect simple: **have known**.'], TIP,
            [('Complete: "She ____ (like) music since she was a child."', 'has liked'), ('Complete: "We ____ (have) this radio for ten years."', 'have had')], page=P),
        fill('eng10-u8-ppq18', 'The farmers ____ (wait) for the rain for three weeks.', 'have been waiting',
             ['have been waiting', 'has been waiting', 'are waiting', 'were waited'],
             ['*for three weeks* + still no rain → from the past up to now.', '*The farmers* = they → **have been waiting**.'], TIP,
             [('Complete: "The children ____ (play) since lunch."', 'have been playing')], page=P),
        fill('eng10-u8-ppq19', 'She ____ (work) at the clinic in Keren for six years, and she still loves it.', 'has been working',
             ['has been working', 'have been working', 'was working', 'works'],
             ['*for six years* + *still* → it started in the past and goes on now.', '*She* → **has been working**.'], TIP,
             [('Complete: "My father ____ (drive) taxis for twenty years."', 'has been driving')], page=P),
        fill('eng10-u8-ppq20', 'We have been living in Mendefera ____ 2019.', 'since', ['since', 'for', 'from', 'ago'],
             ['2019 is the **starting point**.', 'Starting point → **since**.'], TIP,
             [('Complete: "We have been living here ____ five years."', 'for')], page=P),
        fill('eng10-u8-ppq21', 'Abraham has been playing the krar ____ ten years.', 'for', ['for', 'since', 'during', 'ago'],
             ['*ten years* is a **length** of time.', 'Length of time → **for**.', '*ago* goes with the past simple: *He started ten years ago.*'], TIP,
             [('Complete: "Abraham has been playing the krar ____ he was twelve."', 'since')], page=P),
        short('eng10-u8-ppq22', 'Correct the error: "My parents have been owning this house for twenty years."', 'My parents have owned this house for twenty years.',
              ['*own* is a state verb: never -ing.', 'Use the present perfect simple: **have owned**.'], TIP,
              [('Correct: "She has been knowing the answer for a long time."', 'She has known the answer for a long time.')], page=P,
              accept=['My parents have owned this house for twenty years', 'My parents have owned this house for 20 years.']),
        short('eng10-u8-ppq23', 'Make one sentence with "for": "Hagos started repairing radios at 9 o\'clock. It is 12 o\'clock now and he is still repairing them."',
              'Hagos has been repairing radios for three hours.',
              ['From 9 to 12 = three hours, and he is still working.', 'Still going on + how long → **has been repairing** + **for three hours**.', '(With *since*: *Hagos has been repairing radios since 9 o\'clock.*)'], TIP,
              [('Make one sentence with "since": "It started to rain on Monday. It is still raining."', 'It has been raining since Monday.')], page=P,
              accept=['Hagos has been repairing radios for three hours', "Hagos has been repairing radios since 9 o'clock.", 'He has been repairing radios for three hours.']),
        tf('eng10-u8-ppq24', 'True or false: "It has been raining all day" tells us how long the rain has lasted up to now.', True,
           ['True. *has been raining* + *all day* = the rain started in the morning and has gone on until now.', 'The present perfect continuous answers **How long?**'], TIP,
           [('True or false: "It has rained three times this week" tells us how long it rained.', 'False – it tells us how many times.')], page=P),
        mcq('eng10-u8-ppq25', 'Which sentence is about a finished time in the past?', {'A': 'I have been reading since lunch.', 'B': 'I was reading at 2 o\'clock yesterday.', 'C': 'I have read two chapters.', 'D': 'I have been reading a lot lately.'}, 'B',
            ['*at 2 o\'clock yesterday* is a finished past time → past continuous.', 'A and D reach **now** (since lunch, lately); C has a result now (two chapters).'], TIP,
            [('Which tense: "At 6 this morning I ____ (run)."', 'was running'), ('Which tense: "I ____ (run) for an hour – I\'m so tired!"', 'have been running')], page=P),
        short('eng10-u8-ppq26', 'Ask a question with How long: "Aster is learning French. She started in January."', 'How long has Aster been learning French?',
              ['*How long* + up to now → present perfect continuous.', 'Order: How long + **has** + Aster + **been learning** + French?'], TIP,
              [('Ask with How long: "They are building the school. They started last year."', 'How long have they been building the school?')], page=P,
              accept=['How long has Aster been learning French', 'How long has she been learning French?']),
    ]
    b.put_questions('eng10-u8', qs)
    return len(qs)


def apply(b):
    cards(b)
    n = questions(b)
    u = b.unit('eng10-u8')
    if not any('lately' in t['text'] for t in u['tips']):
        u['tips'].append(dict(text='**since / for / all day / lately → have been + -ing**, but **at 8 last night → was/were + -ing** and **three times → have + 3rd form**.', page=P, src='notes'))
    m = u['unitMap']
    for n_ in m['nodes']:
        if n_.get('lesson') == L:
            for cid in (L + '-t2', L + '-t4', L + '-t7'):
                if cid not in n_['cards']:
                    n_['cards'].append(cid)
    return n
