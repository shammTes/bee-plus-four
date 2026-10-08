"""Grade 9: simple, student-friendly English. The imported exam cards are rewritten in plain words and moved to the
lesson that really teaches their grammar point; two new lessons (present perfect / past perfect, future forms and
modals) hold the cards that had no home; tag-question key rules; full reported-speech tables; small fixes."""
import re
from lib import grammar, table, text, worked, check, mcq, fill, tf, short
from clean import delatex
from g11a import reported_speech_tables
from g11c import TAG_ROWS, TAG_TIP

SVA_TIP = 'Find the real subject (cover phrases like "of the students" or "with his friends") and make the verb agree with it.'
PASS_TIP = 'The subject does not do the action → passive: the right form of be + past participle (is done, was done, is being done, has been done, will have been done).'
NOUN_TIP = 'Can you count it? many / few / a few + plural. Can\'t count it? much / little / a little + singular. some works with both.'
PRON_TIP = 'Before the verb → I, he, she, we, they. After a verb or a preposition → me, him, her, us, them.'
PAST_TIP = 'Finished time (yesterday, ago, last…) → past simple. Long action interrupted → was/were + -ing. Earlier of two past actions → had + past participle.'
PERF_TIP = 'since / for / already / yet / ever → present perfect (have + V3). Still going on + how long → have been + -ing. ago / yesterday → past simple.'
FUT_TIP = 'Evidence now → going to. Decision now → will. Timetable → present simple. Arrangement → present continuous.'
MOD_TIP = "must = it is necessary / I am sure; mustn't = it is not allowed; don't have to = it is not necessary; should have + V3 = it was a good idea but you didn't; must have + V3 = I'm sure it happened."


def tig(c):
    """keep the Tigrinya explanation of an imported card"""
    s = c.get('why') if c['type'] == 'check' else '\n'.join(x.get('text', '') for x in c.get('steps', []))
    m = re.search(r'\*\*In Tigrinya:\*\*\s*(.+)$', s or '', re.S) or re.search(r'(?:Tigrinya Explanation|In Tigrinya)[^\n]*\n+(.+)$', s or '', re.S)
    return delatex(m.group(1)).strip() if m else ''


def rw_check(b, cid, why, tip, lid=None, after=None):
    c = b.card(cid)
    t = tig(c)
    paras = [f'**Step {i + 1}:** {w}' for i, w in enumerate(why)] + [f'**Tip:** {tip}'] + ([f'**In Tigrinya:** {t}'] if t else [])
    c['why'] = '\n\n'.join(paras)
    c['q'] = delatex(c['q'])
    if lid:
        b.move_card(cid, lid, after=after)


def rw_worked(b, cid, title, problem, steps, answer, lid=None, after=None):
    c = b.card(cid)
    c['title'] = title
    c['problem'] = problem
    c['steps'] = [dict(text=s) for s in steps]
    c['answer'] = answer
    if lid:
        b.move_card(cid, lid, after=after)


def add_topic(u, nid, label, lid, cards):
    m = u['unitMap']
    if not any(n['id'] == nid for n in m['nodes']):
        m['nodes'].append(dict(id=nid, label=label[:40], kind='topic', lesson=lid, cards=list(cards)))
        m['edges'].append({'from': m['root'], 'to': nid, 'label': 'includes'})


def study_cards(b):
    # ---- quantifiers and plurals → 7.1 Articles and noun phrases
    L = 'eng9-u7-l7-1'
    rw_worked(b, 'eng9-u2-wrkE1', 'Step by step: few or little?', 'Complete: "The manager said no because ____ details were given." (too few / too little)', [
        '**Step 1: Look at the noun.** *details* ends in -s, so it is a plural noun we can count.',
        '**Step 2: Choose the word.** Countable → *few*. Uncountable → *little*.',
        '**Step 3: Check the meaning.** The manager said no, so the meaning is negative: *too few* (not enough).',
    ], 'too few', L)
    rw_worked(b, 'eng9-u2-wrkE2', 'Step by step: tricky plurals', 'Find the mistake: "The school board discussed several educational crisises."', [
        '**Step 1: Find the plural noun.** *crisises*.',
        '**Step 2: Remember the special plural.** Words ending in **-is** change to **-es**: *crisis → crises, analysis → analyses, thesis → theses*.',
        '**Step 3: Correct it.** *several educational **crises***.',
    ], 'crisises → crises', L)
    rw_check(b, 'eng9-u2-chkE1', ['*progress* is uncountable (no plural, no *a*).', '*a few, many, few* are only for countable nouns.',
                                  '*some* works with countable and uncountable nouns → **some progress**.'], NOUN_TIP, L)
    # ---- subject–verb agreement → 6.1
    L = 'eng9-u6-l6-1'
    rw_check(b, 'eng9-u2-chkE2', ['*police* means the police officers – it is always plural in English.', 'Plural subject → plural verb: **are** investigating.',
                                  'Do not be tricked: *police* has no -s, but it is still plural.'], SVA_TIP, L)
    rw_worked(b, 'eng9-u4-wrkE1', 'Step by step: "the number of" + singular verb', 'Complete: "Since the library was repaired, the number of visitors ____ (increase) a lot."', [
        '**Step 1: Find the real subject.** *the number* (of visitors) – one number → singular.',
        '**Step 2: Choose the tense.** *Since…* means from then until now → present perfect.',
        '**Step 3: Put it together.** singular + present perfect → **has increased** (not *have*).',
        '**Remember:** *the number of* + singular verb; *a number of* (= many) + plural verb.',
    ], 'has increased', L)
    rw_check(b, 'eng9-u4-chkE2', ['The subject is **Each** (each one) → singular.', 'Ignore *of the candidates who applied…* – it only describes *each*.',
                                  'Singular → **has to take**.'], SVA_TIP, L)
    rw_worked(b, 'eng9-u5-wrkE1', 'Step by step: "one of" + singular verb', 'Complete: "One of the biggest problems for school leavers ____ the cost of university."', [
        '**Step 1: Find the real subject.** *One* (of the problems) → singular.',
        '**Step 2: Cover the middle words.** *One … ____ the cost* → *One **is***.',
        '**Step 3: Do not match the verb with *problems*.** That word is inside the phrase *of the biggest problems*.',
    ], 'is', L)
    rw_worked(b, 'eng9-u5-wrkE2', 'Step by step: a group noun + singular verb', 'Complete: "The board of directors, although they had different ideas, ____ finally agreed on the budget."', [
        '**Step 1: Find the real subject.** *The board* – one group → singular.',
        '**Step 2: Cover the extra words.** *of directors* and *although they had different ideas* do not change the subject.',
        '**Step 3: Choose the verb.** *The board **has** finally agreed.*',
    ], 'has', L)
    rw_check(b, 'eng9-u5-chkE1', ['With *neither … nor*, the verb agrees with the subject **nearest** to it.', 'The nearest subject is *the senior researchers* (plural).',
                                  '*yesterday* → past → **were**.'], SVA_TIP, L)
    rw_check(b, 'eng9-u5-chkE2', ['*police* is always plural.', '*currently* = now → present → **are** searching.',
                                  '*is* and *was* are singular; *were* is past.'], SVA_TIP, L)
    rw_worked(b, 'eng9-u6-wrkE1', 'Step by step: present simple with he / she / it', 'Complete: "Every morning, my father ____ (drink) a cup of coffee."', [
        '**Step 1: Find the time words.** *Every morning* = a habit → present simple.',
        '**Step 2: Find the subject.** *my father* = he → add **-s** to the verb.',
        '**Step 3: Answer.** *my father **drinks***.',
    ], 'drinks')
    rw_worked(b, 'eng9-u6-wrkE2', 'Step by step: present continuous with a group noun', 'Complete: "Listen! The school choir ____ (sing) the national anthem right now."', [
        '**Step 1: Find the time words.** *Listen!* and *right now* = happening now → present continuous (am/is/are + -ing).',
        '**Step 2: Find the subject.** *The choir* = one group → singular → **is**.',
        '**Step 3: Answer.** *The choir **is singing***.',
    ], 'is singing')
    c = b.card('eng9-u6-chkE1')
    c['answer'] = 'B'
    rw_check(b, 'eng9-u6-chkE1', ['*understand* is a **state verb** (a verb of thinking or feeling, not an action).',
                                  'State verbs do not take -ing: ✗ *am understanding*.', 'Subject *I* → **understand** (no -s). So the answer is B.'],
             'State verbs (know, understand, like, want, believe, own) stay in the simple form: I understand, she knows.')
    # ---- past tenses → 1.1 / 1.2
    rw_worked(b, 'eng9-u4-wrkE2', 'Step by step: a past question with "did"', 'Complete: The teacher asked Dawit, "Why ____ (not / complete) your assignment yesterday?"', [
        '**Step 1: Find the tense.** *yesterday* → past simple.',
        '**Step 2: Make the question.** Wh-word + **didn\'t** + subject + **base verb**.',
        '**Step 3: Check the verb.** *did* already shows the past, so the verb stays in the base form: *complete* (✗ *completed*).',
    ], "Why didn't you complete your assignment yesterday?", 'eng9-u1-l1-1')
    rw_check(b, 'eng9-u6-chkE2', ['*While* + a long action in the past → past continuous (was/were + -ing).', 'The subject is *we* → **were**.',
                                  'The short action (*it started to rain*) is in the past simple.'], PAST_TIP, 'eng9-u1-l1-2')
    # ---- passive → 2.1 / 2.2 / 8.1
    rw_worked(b, 'eng9-u9-wrkE1', 'Step by step: past simple passive', 'Complete: "The report ____ (submit) by the committee last night."', [
        '**Step 1: Who does the action?** The committee submits the report. The report does not submit anything → **passive**.',
        '**Step 2: Find the tense.** *last night* → past simple.',
        '**Step 3: Make the passive.** was/were + past participle → singular *report* → **was submitted**.',
    ], 'was submitted', 'eng9-u2-l2-1')
    rw_check(b, 'eng9-u9-chkE1', ['The teacher did not give the gift – she **received** it from the students (*by the students*).',
                                  'So we need the passive: was + past participle → **was given**.', '*gave* would mean that the teacher gave the gift.'], PASS_TIP, 'eng9-u2-l2-2')
    L = 'eng9-u8-l8-1'
    rw_check(b, 'eng9-u4-chkE1', ['Two past actions: first the manuscript was stolen, then the guards noticed.',
                                  'The earlier action takes the past perfect; the manuscript did not steal → passive.', 'had been + past participle → **had been stolen**.'], PASS_TIP, L)
    rw_worked(b, 'eng9-u9-wrkE2', 'Step by step: present continuous passive', 'Complete: "A lot of money ____ currently ____ (raise) to build the new library."', [
        '**Step 1: Who does the action?** People raise the money; the money does not raise anything → **passive**.',
        '**Step 2: Find the tense.** *currently* = now → present continuous.',
        '**Step 3: Make the passive.** is/are + **being** + past participle → *money* is singular → **is being raised**.',
    ], 'is … being raised', L)
    rw_check(b, 'eng9-u9-chkE2', ['Papers cannot print themselves → **passive**.', '*by next Friday* = finished before a future time → future perfect.',
                                  'Future perfect passive: will have **been** + past participle → **will have been printed**.'], PASS_TIP, L)
    # ---- pronouns stay in 3.1 (parts of speech), simple wording
    rw_worked(b, 'eng9-u3-wrkE1', 'Step by step: "Aster and me" or "Aster and I"?', 'Complete: "The committee gave the prize to Aster and ____." (I / me)', [
        '**Step 1: Cover the other name.** *gave the prize to ____*.',
        '**Step 2: Test.** *to me* ✔ – *to I* ✗. After a preposition (*to*) use an object pronoun.',
        '**Step 3: Answer.** *to Aster and **me***.',
    ], 'me')
    rw_worked(b, 'eng9-u3-wrkE2', 'Step by step: its or it\'s?', 'Complete: "The old typewriter still works, but ____ keys are hard to press." (its / it\'s)', [
        '**Step 1: Test with "it is".** *it is keys* ✗ – it makes no sense.',
        '**Step 2: The word shows belonging** (the keys of the typewriter) → **its** (no apostrophe).',
        '**Step 3: Remember.** *it\'s* = it is / it has. *its* = belonging to it.',
    ], 'its')
    rw_check(b, 'eng9-u3-chkE1', ['The word refers to a person (*the candidate*).', 'After the gap comes a new subject and verb (*the board selected*), so the person is the **object** → **whom**.',
                                  '*who* = subject (*the candidate **who** won*); *whose* = belonging.'], PRON_TIP)
    rw_check(b, 'eng9-u3-chkE2', ['The subject is *they*.', 'The reflexive pronoun for *they* is **themselves**.', '*theirselves* and *themself* are not correct English.'], PRON_TIP)
    # ---- present perfect / past perfect → new lesson 8.2
    u8 = b.unit('eng9-u8')
    L = 'eng9-u8-l8-2'
    b.put_lesson('eng9-u8', dict(id=L, number='8.2', title='Present perfect and past perfect', pages=list(u8['lessons'][0]['pages']), cards=[]), after='eng9-u8-l8-1')
    b.put_cards(L, [
        grammar(L + '-c1', 'Present perfect, present perfect continuous and past perfect', [
            '**Present perfect** = *have/has + past participle*. Use it for a past action that is important **now**, or with no exact time: *I **have lost** my pen. She **has visited** Axum twice.*',
            'Use **since** + a starting point (*since 2020, since Monday*) and **for** + a length of time (*for three years*): *We **have lived** here **for** ten years.*',
            '**Present perfect continuous** = *have/has + been + -ing*. Use it for an action that started in the past and is **still going on**: *Aster **has been working** here **since** 2019.*',
            'With a **finished time** (*yesterday, last week, ago, in 2015*) use the **past simple**, not the present perfect: *They **finished** the road three weeks ago.*',
            '**Past perfect** = *had + past participle*: the **earlier** of two past actions: *When we arrived, the bus **had left**.*',
        ], [('I have finished my homework.', True), ('I have finished my homework yesterday.', False, 'I finished my homework yesterday.'),
            ('She has been waiting for an hour.', True), ('She is waiting here since 9 o\'clock.', False, 'She has been waiting here since 9 o\'clock.'),
            ('When I got to the station, the train had left.', True)],
            pattern='have/has + V3  ·  have/has been + V-ing  ·  had + V3'),
        table(L + '-c2', 'Which tense?', ['Time words', 'Tense', 'Example'], [
            ['already, yet, just, ever, never', 'present perfect', 'Have you **ever been** to Massawa?'],
            ['since + start, for + length (still true)', 'present perfect / present perfect continuous', 'I **have known** her **for** years. It **has been raining** since morning.'],
            ['yesterday, last…, ago, in 2015', 'past simple', 'They **completed** it three weeks **ago**.'],
            ['before, after, when, by the time (two past actions)', 'past perfect for the earlier one', 'The film **had started** when we arrived.'],
        ]),
    ])
    rw_worked(b, 'eng9-u7-wrkE1', 'Step by step: "since" → present perfect continuous', 'Complete: "Aster ____ (work) in this laboratory since she finished university five years ago."', [
        '**Step 1: Find the time word.** *since she finished university* = from then until **now**.',
        '**Step 2: Is she still working there?** Yes → the action is still going on.',
        '**Step 3: Choose the tense.** still going on + since → present perfect continuous: **has been working** (*has worked* is also possible).',
        '**Watch out:** ✗ *is working since…* – English does not use the present continuous with *since*.',
    ], 'has been working', L)
    rw_worked(b, 'eng9-u7-wrkE2', 'Step by step: "ago" → past simple', 'Complete: "The company ____ (complete) the new road three weeks ago."', [
        '**Step 1: Find the time word.** *three weeks ago* = a finished time in the past.',
        '**Step 2: Choose the tense.** finished time → past simple.',
        '**Step 3: Answer.** **completed** (✗ *has completed* – the present perfect never goes with *ago*).',
    ], 'completed', L)
    b.put_cards(L, [
        check(L + '-c3', 'We ____ in Asmara since 2018.', {'A': 'live', 'B': 'are living', 'C': 'have lived', 'D': 'lived'}, 'C', [
            '**Step 1:** *since 2018* = from 2018 until now.', '**Step 2:** From the past until now → present perfect: **have lived**.',
            '**Step 3:** *live / are living* are present only; *lived* is finished past.', f'**Tip:** {PERF_TIP}']),
        check(L + '-c4', 'By the time the ambulance arrived, the injured man ____ to hospital by a taxi driver.', {'A': 'was taken', 'B': 'has been taken', 'C': 'had been taken', 'D': 'takes'}, 'C', [
            '**Step 1:** Two past actions: first the man was taken, then the ambulance arrived.', '**Step 2:** Earlier action → past perfect; he did not take himself → passive.',
            '**Step 3:** had been + past participle → **had been taken**.', f'**Tip:** {PAST_TIP}']),
    ])
    add_topic(u8, 'l8_2', 'Present perfect and past perfect', L, [L + '-c1', L + '-c2'])
    # ---- future forms and modals → new lesson 9.2
    u9 = b.unit('eng9-u9')
    L = 'eng9-u9-l9-2'
    b.put_lesson('eng9-u9', dict(id=L, number='9.2', title='Future forms and modals (will, going to, must, should)', pages=list(u9['lessons'][0]['pages']), cards=[]), after='eng9-u9-l9-1')
    b.put_cards(L, [
        table(L + '-c1', 'Talking about the future', ['Form', 'Use', 'Example'], [
            ['be going to + verb', 'a plan, or a prediction from what we can see now', 'Look at those clouds! It**\'s going to** rain.'],
            ['will + verb', 'a decision made now, a promise, an offer, a general prediction', 'The phone is ringing. I**\'ll** answer it.'],
            ['present continuous', 'a fixed arrangement with a time', 'We**\'re meeting** the doctor at 10 tomorrow.'],
            ['present simple', 'timetables (buses, trains, school)', 'The train **leaves** at 7:30 tomorrow.'],
        ]),
        table(L + '-c2', 'Modals: what they mean', ['Modal', 'Meaning', 'Example'], [
            ['must', 'it is necessary / I am sure (now)', 'You **must** wear goggles. She lived in London for ten years – she **must** speak English well.'],
            ["mustn't", 'it is not allowed', "You **mustn't** enter without goggles."],
            ["don't have to", 'it is not necessary (you can choose)', "You **don't have to** come on Saturday."],
            ['should', 'it is a good idea', 'You **should** study every day.'],
            ['should have + V3', 'it was a good idea, but you did not do it (regret)', 'I failed. I **should have studied** harder.'],
            ['must have + V3', 'I am sure it happened (past)', 'The field is wet. It **must have rained**.'],
            ["can't have + V3", 'I am sure it did not happen', "He **can't have seen** us – he was asleep."],
        ]),
    ])
    rw_check(b, 'eng9-u7-chkE1', ['We can **see** the dark clouds now – that is evidence.', 'A prediction from evidence → **is going to** rain.',
                                  '*will* is for a decision made now or a general prediction.'], FUT_TIP, L)
    rw_check(b, 'eng9-u7-chkE2', ['A train leaving at a fixed time is a **timetable**.', 'Timetables use the present simple even for the future → **departs**.',
                                  'Do not choose *will depart* just because you see *tomorrow*.'], FUT_TIP, L)
    rw_worked(b, 'eng9-u8-wrkE1', 'Step by step: should have (regret)', 'Complete: "I failed the biology exam. I ____ (study) harder instead of wasting time on my phone."', [
        '**Step 1: What happened?** I did **not** study hard, and now I am sorry.',
        '**Step 2: Choose the modal.** A past regret (good idea, but I didn\'t do it) → **should have** + past participle.',
        '**Step 3: Compare.** *must have studied* means "I am sure I studied" – the wrong meaning here.',
    ], 'should have studied', L)
    rw_worked(b, 'eng9-u8-wrkE2', "Step by step: mustn't or don't have to?", 'Complete: "Lab rule: you ____ enter the chemistry room without safety goggles."', [
        '**Step 1: What does the rule say?** Entering without goggles is **not allowed**.',
        '**Step 2: Choose.** not allowed → **must not (mustn\'t)**.',
        '**Step 3: Compare.** *don\'t have to* = it is not necessary – the wrong meaning for a safety rule.',
    ], 'must not', L)
    rw_check(b, 'eng9-u8-chkE1', ['Ten years in London is strong evidence – we are sure about now.', 'Sure about the present → **must** + base verb (*must speak*).',
                                  '*must have* is for the past and needs a past participle (*must have spoken*).'], MOD_TIP, L)
    rw_check(b, 'eng9-u8-chkE2', ['We see puddles now, so we are sure it rained in the night.', 'Sure about the past → **must have** + past participle → **must have rained**.',
                                  '*should have rained* would mean it was a good idea for it to rain – that makes no sense.'], MOD_TIP, L)
    b.put_cards(L, [
        check(L + '-c3', 'You ____ bring your own lunch. The school gives free lunch to everyone.', {'A': "mustn't", 'B': "don't have to", 'C': 'must', 'D': "can't"}, 'B', [
            '**Step 1:** Lunch is free, so bringing lunch is **not necessary**.', "**Step 2:** not necessary → **don't have to**.",
            "**Step 3:** *mustn't* would mean it is forbidden to bring lunch.", f'**Tip:** {MOD_TIP}']),
    ])
    add_topic(u9, 'l9_2', 'Future forms and modals', L, [L + '-c1', L + '-c2'])


def questions(b):
    sim_p = [('Complete: "I ____ (know) him since 2015."', 'have known'), ('Complete: "She ____ (leave) an hour ago."', 'left')]
    b.put_questions('eng9-u8', [
        mcq('eng9-u8-pfq01', 'Have you ____ been to Keren?', {'A': 'ever', 'B': 'ago', 'C': 'since', 'D': 'yesterday'}, 'A',
            ['*ever* is used in present perfect questions about experience.', '*ago* and *yesterday* go with the past simple.'], PERF_TIP, sim_p),
        mcq('eng9-u8-pfq02', 'My uncle ____ in Massawa for twenty years. He still lives there.', {'A': 'lived', 'B': 'has lived', 'C': 'lives', 'D': 'had lived'}, 'B',
            ['*for twenty years* + he still lives there → from the past until now.', 'Present perfect: **has lived**.'], PERF_TIP, sim_p),
        mcq('eng9-u8-pfq03', 'They ____ the match two days ago.', {'A': 'have won', 'B': 'won', 'C': 'have been winning', 'D': 'had won'}, 'B',
            ['*two days ago* = finished time → past simple: **won**.'], PERF_TIP, sim_p),
        fill('eng9-u8-pfq04', 'I am tired because I ____ (study) since 6 o\'clock.', 'have been studying', ['have been studying', 'am studying', 'studied', 'had studied'],
             ['*since 6 o\'clock* and I am still tired now → the action has been going on until now.', 'Present perfect continuous: **have been studying**.'], PERF_TIP, sim_p),
        fill('eng9-u8-pfq05', 'When we got to the cinema, the film ____ (already / start).', 'had already started', ['had already started', 'has already started', 'already started', 'was already start'],
             ['Two past actions: the film started first.', 'Earlier action → past perfect: **had already started**.'], PAST_TIP, sim_p),
        short('eng9-u8-pfq06', 'Correct the error: "She has finished her project last week."', 'She finished her project last week.',
              ['*last week* is a finished time.', 'Finished time → past simple: *finished*.'], PERF_TIP, sim_p, accept=['She finished her project last week']),
    ])
    sim_f = [('Respond with will: "I\'m thirsty."', "I'll get you some water."), ('Complete: "You ____ smoke here. It is forbidden."', "mustn't")]
    b.put_questions('eng9-u9', [
        mcq('eng9-u9-fmq01', '"I\'ve left my book at home." – "Don\'t worry, I ____ lend you mine."', {'A': 'am going to', 'B': 'will', 'C': 'am lending', 'D': 'lend'}, 'B',
            ['The speaker decides at the moment of speaking → **will**.'], FUT_TIP, sim_f),
        mcq('eng9-u9-fmq02', 'The school bus ____ at 7:15 every morning.', {'A': 'leaves', 'B': 'is leaving', 'C': 'will leaving', 'D': 'left'}, 'A',
            ['A timetable → present simple: **leaves**.'], FUT_TIP, sim_f),
        mcq('eng9-u9-fmq03', 'You ____ come to the meeting if you are busy. It is not important.', {'A': "mustn't", 'B': "don't have to", 'C': 'must', 'D': 'should'}, 'B',
            ['*not important* = not necessary → **don\'t have to**.', "*mustn't* would mean it is forbidden."], MOD_TIP, sim_f),
        fill('eng9-u9-fmq04', 'The streets are wet. It ____ (rain) in the night.', 'must have rained', ['must have rained', 'should have rained', 'must rain', 'can rain'],
             ['We are sure about something in the past → **must have** + past participle.'], MOD_TIP, sim_f),
        fill('eng9-u9-fmq05', 'I missed the bus. I ____ (leave) home earlier.', 'should have left', ['should have left', 'must have left', 'should leave', 'must leave'],
             ['A past regret: it was a good idea, but I didn\'t do it → **should have left**.'], MOD_TIP, sim_f),
        short('eng9-u9-fmq06', 'Make a prediction from evidence: (Look at the sky! / it / rain)', "Look at the sky! It's going to rain.",
              ['We can see the evidence now → **be going to**.'], FUT_TIP, sim_f, accept=['It is going to rain.', "It's going to rain.", 'Look at the sky! It is going to rain.']),
    ])
    sim_t = [('Add a tag: "She can drive, ___?"', "can't she?"), ('Add a tag: "Nobody came, ___?"', 'did they?')]
    b.put_questions('eng9-u7', [
        mcq('eng9-u7-tgq01', 'Your sister plays volleyball, ____?', {'A': "isn't she", 'B': "doesn't she", 'C': 'does she', 'D': "don't she"}, 'B',
            ['Positive sentence → negative tag.', 'No helping verb, present, *she* → **doesn\'t she?**'], TAG_TIP, sim_t),
        mcq('eng9-u7-tgq02', "Let's go to the market, ____?", {'A': "don't we", 'B': 'shall we', 'C': 'will you', 'D': "let's we"}, 'B',
            ["*Let's* → **shall we?**"], TAG_TIP, sim_t),
        fill('eng9-u7-tgq03', 'He never eats meat, ____?', 'does he', ['does he', "doesn't he", 'is he', "isn't he"],
             ['*never* makes the sentence negative → positive tag.', 'No helping verb, present, *he* → **does he?**'], TAG_TIP, sim_t),
        fill('eng9-u7-tgq04', "I'm your best friend, ____?", "aren't I", ["aren't I", 'am not I', "isn't I", 'am I'],
             ["Special case: *I am* → **aren't I?**"], TAG_TIP, sim_t),
        short('eng9-u7-tgq05', 'Add the tag: "There is a meeting today, ___?"', "isn't there?",
              ['Positive → negative tag.', '*There is* → tag with *there*: **isn\'t there?**'], TAG_TIP, sim_t, accept=["isn't there", 'There is a meeting today, isn\'t there?']),
    ])


def fixes(b):
    for cid in ('eng9-u1-l1-1-r2c3', 'eng9-u1-l1-1-r2c4'):
        c = b.card(cid)
        c['why'] = re.sub(r'\*\*Tip:\*\*.*$', f'**Tip:** {PAST_TIP}', c['why'], flags=re.S)
    for cid in ('eng9-u6-l6-2-r2c1', 'eng9-u6-l6-2-r2c2', 'eng9-u6-l6-2-r2c3'):
        c = b.card(cid)
        c['why'] = re.sub(r'\*\*Tip:\*\*.*$', '**Tip:** Ask what job the word does: names a thing → noun; describes a noun → adjective; tells how/when/where → adverb; shows place or time before a noun → preposition.', c['why'], flags=re.S)
    c = b.card('eng9-u5-l5-2-wk1')
    if c['steps'][0]['text'].strip() == '**Step 1: Recall the rule for this pattern.**':
        c['steps'][0]['text'] = "**Step 1: Recall the rule.** For a plural noun ending in -s, put the apostrophe **after** the s: *the boys' bags* (the bags of the boys). For one boy: *the boy's bag*."
    for g in b.unit('eng9-u7')['games']:
        if g['id'] == 'eng9-u7-g1':
            g['lesson'] = 'eng9-u7-l7-2'
    b.put_cards('eng9-u7-l7-2', [table('eng9-u7-l7-2-tg1', 'Tag questions: key rules', ['Rule', 'Example'], TAG_ROWS)], after='eng9-u7-c03')
    u7 = b.unit('eng9-u7')
    for n in u7['unitMap']['nodes']:
        if n.get('lesson') == 'eng9-u7-l7-2' and 'eng9-u7-l7-2-tg1' not in n['cards']:
            n['cards'].append('eng9-u7-l7-2-tg1')


SIMPLE = [
    (r'\bstative verbs\b', 'state verbs'), (r'\bstative verb\b', 'state verb'), (r'\bhypothetical\b', 'imaginary'),
    (r'\bhabitual\b', 'repeated (habit)'), (r'\bprogressive aspect\b', 'continuous form'), (r'\bcontinuous/progressive aspects?\b', 'continuous forms'),
    (r'\bsubject-auxiliary inversion\b', 'helping verb before the subject'), (r'\bcorrelative conjunction\b', 'pair of joining words'),
    (r'\bproximity rule\b', 'nearest-subject rule'), (r'\binanimate\b', 'not a person'), (r'\binverted form\b', 'question word order'),
    (r'\bpolarity\b', 'positive/negative form'), (r'\bintervening elements\b', 'extra words in the middle'),
]


def apply(b):
    study_cards(b)
    questions(b)
    fixes(b)
    reported_speech_tables(b, 9)
    b.sub_all(SIMPLE)
