"""Grade 10: simpler English notes. Plain words, short sentences, no grammar jargon (needed terms explained),
step-by-step rules with Eritrean examples. The imported exam cards (wrkE / chkE) are rewritten in plain words and moved to
the lesson that really teaches their grammar point (as was done for Grade 9 in PR #47)."""
import re
from g9 import rw_check, rw_worked
from lib import grammar  # noqa: F401

MOD = "must / have to = necessary; mustn't = not allowed; don't have to = not necessary; should = a good idea. Guessing: must = sure yes, can't = sure no, might = maybe. Add have + 3rd form for the past."
SVA = 'Find the real subject, cover the words between it and the verb, then make the verb match the real subject.'
TENSE = ('Habit or fact → present simple. Happening now → present continuous. Finished time (yesterday, ago) → past simple. '
         'Past until now (since, for, already, yet) → present perfect. Timetable → present simple. Clear sign now → going to.')
PASS = 'If the subject does not do the action, use the passive: the right form of be + 3rd form (was given, is being raised, will have been printed).'
RS = 'Reported question: asked + if/whether (or a wh-word) + subject + verb. Move the tense one step back: past → had + 3rd form, will → would.'
PRON = 'Before the verb → I, he, she, we, they. After a verb or a small word like to / for / with → me, him, her, us, them.'
ORDER = 'English order: who? (subject) + does what? (verb) + what? (object) + how? + where? + when?'
QUANT = "Can you count it? many / few / a few + plural. Can't count it? much / little / a little. some works with both."
JOIN = 'Two full sentences cannot be joined with only a comma. Use a full stop, a semicolon (;) or one joining word (and, but, so, because).'
STATE = 'State verbs (know, understand, like, want, believe, own) stay in the simple form: I understand, she knows.'

# new exercise tips per unit (replace the long or generic old tips)
UNIT_TIP = {
    'eng10-u1': "Ask: is it necessary (must / have to), not allowed (mustn't), not necessary (don't have to) or a good idea (should)? For a guess: must = sure yes, can't = sure no, might = maybe.",
    'eng10-u2': 'After enjoy / avoid / finish → -ing. After want / decide / hope → to + verb. After in / at / of / about → -ing. -ing word = the cause, -ed word = the feeling. will be + -ing = in the middle of an action at a future time.',
    'eng10-u3': 'Inside a noun clause use statement order (where she lives, not where does she live). A noun clause before the main verb is one thing → singular verb. Starters: that (a fact), what (a thing), whether / if (yes or no), wh-words.',
    'eng10-u4': 'who = people, which = things, that = people or things, whose = belonging to, where = places. After a comma use who / which, never that. After be / seem / become use an adjective (serious, not seriously).',
    'eng10-u5': 'How sure? will (very sure) → should (expected) → might (maybe). Purpose: to / in order to + verb; so that + subject + verb. lest = so that … not. although + subject + verb; despite + noun or -ing.',
    'eng10-u6': 'Word endings: -tion / -ment / -ness = noun; -ful / -less / -ous / -able = adjective; -ify / -ise / -en = verb; -ly = adverb. Indirect question = polite start + subject + verb, no do/does/did; yes/no → if / whether.',
    'eng10-u7': 'Cover the words between the subject and the verb, then match the verb to the real subject. Passive: has/have been + 3rd form (up to now), had been + 3rd form (before a past time).',
    'eng10-u8': 'am/is/are + -ing for now or around now (this week, these days). State verbs (know, like, want, belong) stay simple. accept = say yes to; except = not including; adapt = change to fit; adopt = take as your own.',
    'eng10-u9': 'Match the tense to the time words: every day → present simple; now → present continuous; yesterday / ago → past simple; since / for / yet → present perfect; by + a future time → will have + 3rd form. Headlines: present simple = recent past, to + verb = future.',
    'eng10-u10': 'as … as = the same; not as … as = less; -er / more … than = two things; the -est / the most = the top of a group; different from; the same as.',
}
GENERIC_TIPS = {'Say the sentence aloud with your answer; it must be grammatical and make sense.',
                'Read every option before choosing; rule out the ones that contradict the notes.'}


def move_imported(b):
    # ---- word order and linking verbs → 4.1 (sentence patterns)
    L = 'eng10-u4-l4-1'
    rw_worked(b, 'eng10-u1-wrkE1', 'Step by step: English word order (who – does – what)',
              'Which sentence has the correct English word order?\nA. The security guard the main gate at midnight locked.\nB. The security guard locked the main gate at midnight.\nC. At midnight the main gate the security guard locked.', [
                  '**Step 1: Find the three parts.** Who? *The security guard*. Does what? *locked*. What? *the main gate*.',
                  '**Step 2: Put them in English order.** who + does + what: *The security guard locked the main gate*. The time (*at midnight*) goes at the end.',
                  '**Step 3: Watch out.** In Tigrinya the verb comes last (ሓላው ሰላም ማዕጾ ዓጸዎ). Word-by-word translation gives A or C – wrong in English.',
              ], 'B. The security guard locked the main gate at midnight.', L)
    rw_worked(b, 'eng10-u1-wrkE2', 'Step by step: do not forget is / are',
              'Which sentence is missing a verb?\nA. My brother is a hard-working farmer in the village.\nB. My brother a hard-working farmer in the village.\nC. My brothers are hard-working farmers.', [
                  '**Step 1: Look for the verb.** A has *is*, C has *are*. B has no verb at all.',
                  '**Step 2: The rule.** Every English sentence needs a verb. To say what someone **is**, use *am / is / are* (past: *was / were*). This linking verb joins *my brother* to *a hard-working farmer*.',
                  '**Step 3: Watch out.** In Tigrinya *እዩ* comes at the end (ሓወይ ኣብቲ ዓዲ ትጉህ ሓረስታይ እዩ). Do not drop it in English.',
              ], 'B is missing "is". Correct: My brother is a hard-working farmer in the village.', L)
    # ---- joining sentences and adverb position → 5.2 (adverbials and linkers)
    L = 'eng10-u5-l5-2'
    b.card('eng10-u1-chkE1')['q'] = 'Which sentence joins the two ideas correctly?'
    rw_check(b, 'eng10-u1-chkE1', ['A joins two full sentences with only a comma – that is a mistake in English. B has nothing between them at all.',
                                   'C is correct: a semicolon (;) and *therefore* join the two sentences.',
                                   'D uses two joining words (*Because … so …*). Use only one: *Because the rain was heavy, we stayed indoors.*'], JOIN, L)
    b.card('eng10-u1-chkE2')['q'] = "Complete with the correct word order: 'The school principal ________.'"
    rw_check(b, 'eng10-u1-chkE2', ['English order: who + does what + to whom/what + when.',
                                   'The how-word *warmly* can stand just before the verb (*warmly welcomed*); the time word *yesterday* goes at the end.',
                                   'D puts the object before the verb (Tigrinya order); A and C put words in unusual places. Answer: B.'], ORDER, L)
    # ---- quantity words and plurals
    rw_worked(b, 'eng10-u2-wrkE1', 'Step by step: few or little?', 'Complete: "The manager said no to the plan because ____ details were given." (too few / too little / a little / much)', [
        '**Step 1: Look at the noun.** *details* ends in -s: it is a plural noun we can count.',
        '**Step 2: Choose the word.** Countable → *few*. Uncountable → *little / much*.',
        '**Step 3: Check the meaning.** The manager said no, so the meaning is "not enough": **too few**.',
    ], 'too few', 'eng10-u10-l10-1')
    rw_check(b, 'eng10-u2-chkE1', ['*progress* is uncountable (no plural, no *a*).', '*a few, many, few* are only for nouns we can count.',
                                   '*some* works with both kinds → **some progress**.'], QUANT, 'eng10-u10-l10-1')
    rw_worked(b, 'eng10-u2-wrkE2', 'Step by step: tricky plurals',
              'Which sentence has a mistake in the plural?\nA. The school board discussed several educational crisises.\nB. Many children were waiting outside.\nC. Two analyses of the results were done.', [
                  '**Step 1: Find the plural nouns.** A: *crisises*. B: *children*. C: *analyses*.',
                  '**Step 2: Remember the special plural.** Words ending in **-is** change to **-es**: *crisis → crises, analysis → analyses, thesis → theses*.',
                  '**Step 3: Correct it.** A: *several educational **crises***.',
              ], 'A: crisises → crises', 'eng10-u6-l6-1')
    # ---- subject–verb agreement → 7.1
    L = 'eng10-u7-l7-1'
    rw_check(b, 'eng10-u2-chkE2', ['*police* means the police officers – it is always plural in English.', 'Plural subject → plural verb: **are** investigating.',
                                   'Do not be tricked: *police* has no -s, but it is still plural.'], SVA, L)
    rw_worked(b, 'eng10-u4-wrkE1', 'Step by step: "the number of" + singular verb', 'Complete: "Since the library was repaired, the number of visitors ____ (increase) a lot."', [
        '**Step 1: Find the real subject.** *the number* (of visitors) – one number → singular.',
        '**Step 2: Choose the tense.** *Since…* means from then until now → present perfect.',
        '**Step 3: Put it together.** singular + present perfect → **has increased** (not *have*).',
        '**Remember:** *the number of* + singular verb; *a number of* (= many) + plural verb.',
    ], 'has increased', L)
    rw_check(b, 'eng10-u4-chkE2', ['The subject is **Each** (each one) → singular.', 'Cover *of the candidates who applied…* – it only describes *each*.',
                                   'Singular → **has to take**.'], SVA, L)
    rw_worked(b, 'eng10-u5-wrkE1', 'Step by step: "one of" + singular verb', 'Complete: "One of the biggest problems for school leavers ____ the cost of university."', [
        '**Step 1: Find the real subject.** *One* (of the problems) → singular.',
        '**Step 2: Cover the middle words.** *One … ____ the cost* → *One **is***.',
        '**Step 3: Do not match the verb with *problems*.** That word is inside *of the biggest problems*.',
    ], 'is', L)
    rw_worked(b, 'eng10-u5-wrkE2', 'Step by step: a group word + singular verb', 'Complete: "The board of directors, although they had different ideas, ____ finally agreed on the budget." (has / have)', [
        '**Step 1: Find the real subject.** *The board* – one group → singular.',
        '**Step 2: Cover the extra words.** *of directors* and *although they had different ideas* do not change the subject.',
        '**Step 3: Choose the verb.** *The board **has** finally agreed.*',
    ], 'has', L)
    rw_check(b, 'eng10-u5-chkE1', ['With *neither … nor*, the verb matches the subject **nearest** to it.', 'The nearest subject is *the senior researchers* (plural).',
                                   '*yesterday* → past → **were**.'], SVA, L)
    rw_check(b, 'eng10-u5-chkE2', ['*police* is always plural.', '*currently* = now → present → **are** searching.',
                                   '*is* and *was* are singular; *were* is past.'], SVA, L)
    # ---- pronouns stay in Unit 3 (review), relative "whom" → 4.2
    rw_worked(b, 'eng10-u3-wrkE1', 'Step by step: "Aster and me" or "Aster and I"?', 'Complete: "The committee gave the scholarship to Aster and ____ after reading our reports." (I / me)', [
        '**Step 1: Cover the other name.** *gave the scholarship to ____*.',
        '**Step 2: Test.** *to me* ✔ – *to I* ✗. After a small word like *to* use an object pronoun.',
        '**Step 3: Answer.** *to Aster and **me***.',
    ], 'me')
    rw_worked(b, 'eng10-u3-wrkE2', "Step by step: its or it's?", 'Complete: "The old typewriter in the office still works, but ____ keys are hard to press." (its / it\'s)', [
        '**Step 1: Test with "it is".** *it is keys* ✗ – it makes no sense.',
        '**Step 2: The word shows belonging** (the keys of the typewriter) → **its** (no apostrophe).',
        "**Step 3: Remember.** *it's* = it is / it has. *its* = belonging to it.",
    ], 'its')
    rw_check(b, 'eng10-u3-chkE1', ['The word refers to a person (*the candidate*).',
                                   'After the gap comes a new subject and verb (*the board selected*), so the person receives the action → **whom**.',
                                   '*who* = the person does the action (*the candidate **who** won*); *whose* = belonging; *which* = things.'], PRON, 'eng10-u4-l4-2')
    rw_check(b, 'eng10-u3-chkE2', ['The subject is *they*.', 'The -self word for *they* is **themselves**.', '*theirselves* and *themself* are not correct English.'], PRON)
    # ---- questions and reported speech → 6.2
    L = 'eng10-u6-l6-2'
    rw_worked(b, 'eng10-u4-wrkE2', 'Step by step: a past question with "did"', 'Complete: The teacher asked Dawit, "Why ____ (not / complete) your assignment yesterday?"', [
        '**Step 1: Find the tense.** *yesterday* → past simple.',
        "**Step 2: Make the question.** question word + **didn't** + subject + **plain verb**.",
        '**Step 3: Check the verb.** *did* already shows the past, so the verb stays plain: *complete* (✗ *completed*).',
    ], "Why didn't you complete your assignment yesterday?", L)
    rw_worked(b, 'eng10-u10-wrkE1', 'Step by step: reporting a yes/no question',
              'The director asked me, "Will you come to the meeting tomorrow?" Report it: The director asked me ________ to the meeting the next day.', [
                  '**Step 1: What kind of question?** It can be answered yes or no → use **whether** (or **if**).',
                  '**Step 2: Statement order.** subject + verb: *I would come* (not *would I come*).',
                  '**Step 3: Move the tense back.** *asked* is past, so *will* → **would**; *you* → *I*; *tomorrow* → *the next day*.',
              ], 'whether (if) I would come', L)
    rw_worked(b, 'eng10-u10-wrkE2', 'Step by step: reporting a "Don\'t…" command',
              'The principal said to the students, "Don\'t run inside the laboratory." Report it: The principal warned the students ________ inside the laboratory.', [
                  "**Step 1: What kind of sentence?** A command that starts with *Don't*.",
                  '**Step 2: The pattern.** told / warned / asked + person + **not to** + plain verb.',
                  '**Step 3: Put *not* first.** *warned the students **not to run***.',
              ], 'not to run', L)
    rw_check(b, 'eng10-u10-chkE1', ['She said: "I submitted my application **yesterday**." In the report, *yesterday* becomes *the day before*.',
                                    'After *told* (past), the past simple moves one step back → had + 3rd form → **had submitted**.',
                                    '*submitted* does not show that it happened before she spoke; *has submitted* is not used after a past reporting verb here.'], RS, L)
    rw_check(b, 'eng10-u10-chkE2', ['The officer asked: "Where **did** you park your car?"', 'In a reported question use statement order: subject + verb, no *did*.',
                                    'The past simple moves back to **had parked** → *where **he had parked** his car*.'], RS, L)
    # ---- modals → 1.1 / 1.2
    rw_worked(b, 'eng10-u8-wrkE1', 'Step by step: should have (regret)', 'Complete: "I failed the biology exam. I ____ (study) harder instead of wasting my time on my phone."', [
        "**Step 1: What happened?** I did **not** study hard, and now I am sorry.",
        "**Step 2: Choose the modal.** A past regret (a good idea, but I didn't do it) → **should have** + 3rd form.",
        '**Step 3: Compare.** *must have studied* means "I am sure I studied" – the wrong meaning here.',
    ], 'should have studied', 'eng10-u1-l1-1')
    rw_worked(b, 'eng10-u8-wrkE2', "Step by step: mustn't or don't have to?", 'Complete: "Lab rule: you ____ enter the chemistry room without safety goggles."', [
        '**Step 1: What does the rule say?** Entering without goggles is **not allowed**.',
        "**Step 2: Choose.** not allowed → **must not (mustn't)**.",
        "**Step 3: Compare.** *don't have to* = it is not necessary – the wrong meaning for a safety rule.",
    ], 'must not', 'eng10-u1-l1-1')
    rw_check(b, 'eng10-u8-chkE1', ['Ten years in London is strong evidence – we are sure about now.', 'Sure about the present → **must** + plain verb (*must speak*).',
                                   '*must have* is for the past and needs a 3rd form (*must have spoken*).'], MOD, 'eng10-u1-l1-2')
    rw_check(b, 'eng10-u8-chkE2', ['We see puddles now, so we are sure it rained in the night.', 'Sure about the past → **must have** + 3rd form → **must have rained**.',
                                   '*should have rained* would mean it was a good idea for it to rain – that makes no sense.'], MOD, 'eng10-u1-l1-2')
    # ---- tenses → 8.1 and 9.1
    rw_worked(b, 'eng10-u6-wrkE2', 'Step by step: present continuous with a group word', 'Complete: "Listen! The national choir ____ (sing) the anthem in the main hall right now."', [
        '**Step 1: Find the time words.** *Listen!* and *right now* = happening now → present continuous (am/is/are + -ing).',
        '**Step 2: Find the subject.** *The choir* = one group → singular → **is**.',
        '**Step 3: Answer.** *The choir **is singing***.',
    ], 'is singing', 'eng10-u8-l8-1')
    rw_check(b, 'eng10-u6-chkE1', ['*understand* is a **state verb**: it is about thinking, not an action.',
                                   'State verbs do not take -ing: ✗ *am understanding*.', 'Subject *I* → **understand** (no -s). Answer: B.'], STATE, 'eng10-u8-l8-1')
    L = 'eng10-u9-l9-1'
    rw_worked(b, 'eng10-u6-wrkE1', 'Step by step: present simple with he / she / it', 'Complete: "Every morning, my father ____ (drink) a cup of coffee before he walks to his office."', [
        '**Step 1: Find the time words.** *Every morning* = a habit → present simple.',
        '**Step 2: Find the subject.** *my father* = he → add **-s** to the verb.',
        '**Step 3: Answer.** *my father **drinks***.',
    ], 'drinks', L)
    rw_check(b, 'eng10-u6-chkE2', ['*While* + a long action in the past → past continuous (was/were + -ing).', 'The subject is *we* → **were waiting**.',
                                   'The short action (*it started to rain*) is in the past simple.'], TENSE, L)
    rw_worked(b, 'eng10-u7-wrkE1', 'Step by step: "since" → present perfect continuous', 'Complete: "Aster ____ (work) in this laboratory since she graduated from university five years ago."', [
        '**Step 1: Find the time word.** *since she graduated* = from then until **now**.',
        '**Step 2: Is she still working there?** Yes → the action is still going on.',
        '**Step 3: Choose the tense.** still going on + since → present perfect continuous: **has been working** (*has worked* is also possible).',
        '**Watch out:** ✗ *is working since…* – English does not use the present continuous with *since*.',
    ], 'has been working', L)
    rw_worked(b, 'eng10-u7-wrkE2', 'Step by step: "ago" → past simple', 'Complete: "The construction company ____ (complete) the new road three weeks ago."', [
        '**Step 1: Find the time word.** *three weeks ago* = a finished time in the past.',
        '**Step 2: Choose the tense.** finished time → past simple.',
        '**Step 3: Answer.** **completed** (✗ *has completed* – the present perfect never goes with *ago*).',
    ], 'completed', L)
    rw_check(b, 'eng10-u7-chkE1', ['We can **see** the dark clouds now – that is a clear sign.', 'A prediction from a sign we can see → **is going to** rain.',
                                   '*will* is for a decision made now or a general prediction.'], TENSE, L)
    rw_check(b, 'eng10-u7-chkE2', ['A train leaving at a fixed time is a **timetable**.', 'Timetables use the present simple even for the future → **departs**.',
                                   'Do not choose *will depart* just because you see *tomorrow*.'], TENSE, L)
    # ---- passive → 7.2
    L = 'eng10-u7-l7-2'
    rw_check(b, 'eng10-u4-chkE1', ['Two past actions: first the manuscript was stolen, then the guards noticed.',
                                   'The earlier action takes had + 3rd form; the manuscript did not steal → passive.', 'had been + 3rd form → **had been stolen**.'], PASS, L)
    rw_worked(b, 'eng10-u9-wrkE1', 'Step by step: past simple passive', 'Complete: "The official report ____ (submit) by the committee before the deadline last night."', [
        '**Step 1: Who does the action?** The committee submits the report. The report does not submit anything → **passive**.',
        '**Step 2: Find the tense.** *last night* → past simple.',
        '**Step 3: Make the passive.** was/were + 3rd form → singular *report* → **was submitted**.',
    ], 'was submitted', L)
    rw_worked(b, 'eng10-u9-wrkE2', 'Step by step: present continuous passive', 'Complete: "A lot of money ____ currently ____ (raise) to build the new school library."', [
        '**Step 1: Who does the action?** People raise the money; the money does not raise anything → **passive**.',
        '**Step 2: Find the tense.** *currently* = now → present continuous.',
        '**Step 3: Make the passive.** is/are + **being** + 3rd form → *money* is singular → **is being raised**.',
    ], 'is … being raised', L)
    c = b.card('eng10-u9-chkE1')
    c['why'] = c['why'].replace('বልኩስ', 'ኣብ ክንዲኡ')
    rw_check(b, 'eng10-u9-chkE1', ['The teacher did not give the gift – she **received** it from the students (*by the students*).',
                                   'So we need the passive: was + 3rd form → **was given**.', '*gave* would mean that the teacher gave the gift.'], PASS, L)
    rw_check(b, 'eng10-u9-chkE2', ['Papers cannot print themselves → **passive**.', '*by next Friday* = finished before a future time → will have + 3rd form.',
                                   'Passive of that: will have **been** + 3rd form → **will have been printed**.'], PASS, L)


def main_cards(b):
    def rules(cid, rule, examples=None, pattern=None, title=None):
        c = b.card(cid)
        c['rule'] = rule
        if examples is not None:
            c['examples'] = [dict(text=e[0], ok=e[1], **({'fix': e[2]} if len(e) > 2 else {})) for e in examples]
        if pattern:
            c['pattern'] = pattern
        if title:
            c['title'] = title

    def steps(cid, ss):
        b.card(cid)['steps'] = [dict(text=s) for s in ss]

    def body(cid, bb):
        b.card(cid)['body'] = bb

    def rows(cid, rr):
        b.card(cid)['rows'] = rr

    # ---------------- Unit 1
    rules('eng10-u1-c01', [
        '**must** and **have to** = it is necessary. **must** = *I* feel it is necessary: *I **must** call my mother tonight.* **have to** = someone else made the rule (the school, the law, a doctor): *We **have to** wear a uniform at school.*',
        "**mustn't** = it is not allowed. Don't do it! *You **mustn't** cross at a red light.* **don't have to** = it is not necessary; you can choose: *You **don't have to** bring injera; we have bread.*",
        '**should** = it is a good idea (advice): *You **should** drink a lot of water in Massawa – it is very hot.*',
        'After *must, should, can, might* use the **plain verb**: no *to*, no *-s*: *She must **go*** (not *must to go*, not *must goes*).',
        'Past: use **had to** for every person: *Yesterday we **had to** walk to school because the bus broke down.*',
    ], [('Students must arrive on time.', True), ('You must to finish it.', False, 'You must finish it.'),
        ('You don’t have to pay; it’s free.', True), ('In Eritrea, drivers have to stop at a red light.', True)])
    rules('eng10-u1-c03', [
        'Use these words when you **guess** something from a **clue** you can see or know.',
        'Almost sure it is **true** → **must be**: *Saba has worked in the field all day. She **must be** tired.*',
        "Almost sure it is **not true** → **can't be**: *That **can't be** Lula; she is in Keren today.*",
        "About the **past**, add **have + 3rd form** (gone, eaten, rained): *The road is wet. It **must have rained** in the night.* *He **can't have seen** us; he was asleep.*",
    ])
    steps('eng10-u1-l1-2-wk1', [
        '**Step 1: Remember the rule.** After *must* the next verb is always plain: *must be, must go, must have*.',
        "**Step 2: Test the sentence.** *must **has*** ✗ – *has* has an -s, and modals never take -s after them.",
        '**Step 3: Correct it.** *She must **have left**.* (= I am sure she left.)',
    ])
    rows('eng10-u1-c04', [['You must to go.', 'You must go.', 'No to after must.'], ['He must has gone.', 'He must have gone.', 'After must: have (not has) + 3rd form.'],
                          ['You mustn’t pay (= not necessary).', 'You don’t have to pay.', 'mustn’t = not allowed.']])
    body('eng10-u1-c05', ["**must** = I'm 99% sure it IS true (or it is a rule). **can't** = I'm 99% sure it is NOT true. Add **have + 3rd form** to talk about the past."])
    body('eng10-u1-c06', ["must / have to = necessary; mustn't = not allowed; don't have to = not necessary; should = a good idea. "
                          "For guesses: must be / can't be (now) and must have / can't have + 3rd form (past)."])
    # ---------------- Unit 2
    rules('eng10-u2-c01', [
        '**Step 1 – after some verbs use -ing:** *enjoy, avoid, finish, mind, can\'t help*: *I enjoy **climbing** Emba Soira.*',
        '**Step 2 – after other verbs use to + verb:** *want, decide, hope, plan, agree, attempt*: *We decided **to camp** near Filfil.*',
        '**Step 3 – after a small word like in, at, of, about, without, use -ing:** *She is good **at drawing**.*',
        '**to + verb** can also tell **why** (purpose): *She went to the market **to buy** berbere.*',
        '**-ing or -ed?** The thing that **causes** the feeling takes **-ing**: *an **amazing** trip*. The person who **has** the feeling takes **-ed**: *We were **amazed***.',
    ], [('I avoid travelling at night.', True), ('She wants going home.', False, 'She wants to go home.'), ('The story was horrifying; we were horrified.', True)])
    rules('eng10-u2-c03', [
        '**will be + verb-ing** = an action will be **in the middle** of happening at a future time: *This time tomorrow we **will be travelling** to Massawa.*',
        'It is also a polite way to ask about plans: ***Will** you **be using** the computer tonight?*',
    ])
    steps('eng10-u2-l2-2-wk1', ['**Step 1: Remember the form.** It has three parts: **will + be + verb-ing**.',
                                 '**Step 2: Test the sentence.** *will travelling* has *will* and *-ing*, but **be** is missing.',
                                 '**Step 3: Correct it.** *At 8 tomorrow I **will be travelling**.*'])
    body('eng10-u2-c06', ['-ing words can work like nouns and come after enjoy / avoid / finish and after in / at / of. to + verb comes after want / decide / hope and tells why. '
                          '-ing describes the cause, -ed the feeling. will be + -ing = in the middle of an action at a future time.'])
    body('eng10-u2-l2-2-r3x1', [
        '**Step 1:** Form: will + be + verb-ing: "I will be studying." Negative: won\'t be + -ing. Question: Will you be + -ing?',
        '**Step 2:** Use 1: an action that will be going on at a time in the future: "At 8 pm tomorrow I will be watching the match."',
        '**Step 3:** Use 2: a longer action that will be going on when something short happens: "When you arrive, we will be having dinner."',
        '**Step 4:** Use 3: polite questions about someone\'s plans: "Will you be using the computer this evening?"',
        '**Step 5:** Time words: this time tomorrow, at 6 o\'clock next Monday, this time next week. Do not use it with state verbs (know, like, own).',
        '**Example:** "This time next year, Aman ___ (study) at college." → will be studying. "Don\'t phone at 7; I ___ (cook)." → will be cooking.',
    ])
    # ---------------- Unit 3
    rules('eng10-u3-c01', [
        'A **noun clause** is a small sentence (with its own subject and verb) inside a bigger sentence. It does the job of a noun. It starts with **that, what, whether / if, who, where, when, why, how**.',
        'It can stand in **three places**: before the main verb (**subject**): ***What you told me** was true.* After the verb (**object**): *I know **that he is honest**.* After *is / was* (**complement**): *The problem is **that we have no time**.*',
        'Inside it, use **statement order** (subject + verb), not question order: *I don’t know **where she lives*** (not *where does she live*).',
        'If the main verb is past (*said, asked, thought*), the verb in the noun clause usually moves into the past too: *He said **that he was** ready.*',
        'A noun clause before the main verb counts as **one thing** → singular verb: ***What we need is** more books.*',
    ])
    body('eng10-u3-c05', ['A noun clause (that / what / whether / wh-word + subject + verb) works like one noun: before the main verb, after the verb, or after is/was. '
                          'Use statement order inside it; after a past main verb use a past verb inside it; a noun clause as subject takes a singular verb. '
                          'Modals (can, could, may, might, must, should) are followed by the plain verb.'])
    # ---------------- Unit 4
    rules('eng10-u4-c01', [
        '**SVC = Subject + linking Verb + Complement.** A **linking verb** (*be, become, seem, look, feel, get*) does not show an action. It joins the subject to a word that describes it.',
        'After a linking verb use an **adjective** (or a noun), **not an -ly word**: *The problem **seems serious*** (not *seriously*). *Many graduates **became doctors**.* *The injera **smells good**.*',
        'An adjective can have words after it that finish its meaning (an **adjectival complement**): *I am **happy to help**.* *She is **sure that she will return**.*',
    ])
    rules('eng10-u4-c03', [
        'An **adjective clause** is a group of words that **describes a noun**. It comes right after the noun and starts with **who** (people), **which** (things), **that** (people or things), **whose** (belonging to), **where** (places) or **when** (times): *The doctor **who works in Keren** is my aunt.*',
        '**No commas** = the clause tells us **which one**: *Students **who study abroad** often stay there.* **With commas** = the clause only adds **extra** information; we already know who it is: *Asmara, **which is the capital**, is very clean.* Never use *that* after a comma.',
        'Do not repeat the noun with *he / she / it*: ✗ *My brother who lives in Assab **he** is a nurse.* ✔ *My brother who lives in Assab is a nurse.*',
    ])
    steps('eng10-u4-l4-2-wk1', ['**Step 1: What does the clause describe?** *the book* – a thing.',
                                 '**Step 2: Choose the starter.** For things use **which** or **that**. *what* never starts a describing clause.',
                                 '**Step 3: Correct it.** *The book **that/which** I read was good.*'])
    body('eng10-u4-c06', ['SVC: a linking verb (be, become, seem, look) + an adjective or noun that describes the subject. '
                          'Adjective clauses (who, which, that, whose, where, when) describe a noun; with commas they add extra information and never use that. '
                          'Some adjectives are finished by to + verb or a that-clause (eager to, sure that).'])
    # ---------------- Unit 5
    rules('eng10-u5-c01', [
        'These words show **how sure** you are about something. **will** = very sure (about 100%): *Prices **will be** higher next year.*',
        '**should** = I expect it (about 80%): *The bus left Asmara at 7, so it **should be** in Keren by 9.*',
        '**might / may** = maybe (about 50%): *We **might** need more money for the wedding.*',
        "Negative: **won't** = sure it will not happen; **might not** = maybe not. After will / should / might use the plain verb (no *to*): *It might rain* (not *might to rain*).",
    ])
    rules('eng10-u5-c03', [
        'An **adverbial** answers *when? where? why? how?* or *for what purpose?* A **phrase** has no subject + verb (*in the morning, to save money, despite the rain*). A **clause** has a subject + verb (*because prices rose, so that we can save, although she earns a lot*).',
        '**Purpose (why you do it):** *to / in order to* + verb; *so that* + subject + can / will: *I walk to school **so that** I can save money.*',
        '**To stop something bad happening:** *so as not to* + verb, or *lest* + subject + (should) + verb (*lest* is formal and means "so that … not"): *Write your expenses down **lest** you **forget** them.*',
        '**Contrast (a surprise):** *although / even though* + subject + verb; *despite / in spite of* + a noun or -ing. Use only **one** linker: ✗ *Although…, but…*',
    ], [('She saves money in order to buy a house.', True), ('Although he earns little but he saves.', False, 'Although he earns little, he saves.'),
        ('Work hard lest you fail.', True), ('Despite having little money, they were happy.', True)])
    steps('eng10-u5-l5-2-wk1', ['**Step 1: Find the linkers.** *Although* and *but* both show contrast.',
                                 '**Step 2: The rule.** One contrast needs only **one** linker.',
                                 '**Step 3: Correct it.** *Although he earns little, he saves.* (or: *He earns little, but he saves.*)'])
    rows('eng10-u5-c04', [['Although ..., but ...', 'Although ..., ...', 'Use only one contrast linker.'], ['lest you will forget', 'lest you (should) forget', 'No will after lest.'],
                          ['in order to saving', 'in order to save', 'After to use the plain verb.']])
    body('eng10-u5-c06', ['will = very sure, should = expected, might / may = maybe; all + plain verb. Adverbial phrases and clauses tell when, why, how and for what purpose: '
                          'so that / in order to (purpose), lest / so as not to (to stop something bad), although / despite (contrast).'])
    b.card('eng10-u5-l5-2-mx2')['options']['E'] = 'In spite of'
    # ---------------- Unit 6
    rules('eng10-u6-c01', [
        'The **ending** of a word often tells you its type. **Nouns** (things, ideas): -tion, -ment, -ness, -ity, -er/-or (*instruction, payment, kindness, ability, baker*). **Adjectives** (describe a noun): -ful, -less, -ous, -able, -ive, -al (*useful, careless, famous, reliable, active, national*).',
        '**Verbs** (actions): -ise/-ize, -en, -ify (*organise, shorten, clarify*). **Adverbs** (how something is done): -ly (*carefully*).',
        'Some endings do **not** change the word type; they only change its form: -s (*books, runs*), -ed (*played*), -ing (*playing*), -er/-est (*taller, tallest*).',
        '**How to choose:** look at the word before the gap. After *the / a* → noun. After *very / is* → adjective. After *to / will / can* → verb. After an action → adverb: *Mix the flour **carefully**.*',
    ])
    rules('eng10-u6-c03', [
        'A **direct question**: *Where is the station?* An **indirect question** is more polite: *Could you tell me **where the station is**?*',
        '**Step 1:** Start politely: *Could you tell me… / Do you know… / I wonder…*',
        '**Step 2:** Use **statement order**: subject + verb (*the station is*).',
        '**Step 3:** Take out **do / does / did** and put the tense on the main verb: *What time does the bus leave?* → *Do you know what time the bus **leaves**?*',
        '**Step 4:** A yes/no question uses **if** or **whether**: *Is the shop open?* → *Do you know **if** the shop is open?*',
    ])
    steps('eng10-u6-l6-2-wk1', ['**Step 1: Spot the polite start.** *Do you know* makes the second part an indirect question.',
                                 '**Step 2: Use statement order.** subject + verb: *he lives* (not *does he live*).',
                                 '**Step 3: Take out *does* and put the -s on the verb.** *Do you know where he **lives**?*'])
    body('eng10-u6-c06', ['Endings show the word type: -tion / -ment / -ness (noun), -ful / -less / -ous / -able (adjective), -ify / -ise / -en (verb), -ly (adverb). '
                          'Indirect questions start politely and use statement order with no do/does/did; yes/no questions use if / whether.'])
    # ---------------- Unit 7
    rules('eng10-u7-c01', [
        'In long sentences other words can stand between the subject and the verb. **Step 1:** find the real subject (the main noun). **Step 2:** cover the words between it and the verb. **Step 3:** make the verb match: *The **rights** of every citizen **are** protected.* *The **list** of complaints **is** long.*',
        'In a *who / which / that* part, the verb matches the noun just before *who / which / that*: *people who **are** …; a person who **is** …*',
        'The title of one book or film is **one** thing → singular: *“Things Fall Apart” **is** a famous novel.*',
    ])
    rules('eng10-u7-c03', [
        '**Passive** = the subject does not do the action; something is done **to** it.',
        '**has / have been + 3rd form** – from the past up to now: *New laws **have been passed** to stop discrimination.*',
        '**had been + 3rd form** – done **before** another past time: *Before 1991 many people **had been denied** their rights.*',
        'Do not forget **been**, and use the 3rd form (*changed, given, written*), not the plain verb.',
    ])
    steps('eng10-u7-l7-2-wk1', ['**Step 1: Remember the form.** had + **been** + 3rd form.',
                                 '**Step 2: Test the sentence.** *change* is the plain verb. The 3rd form is *changed*.',
                                 '**Step 3: Correct it.** *The rule had been **changed**.*'])
    body('eng10-u7-c06', ['Find the real subject before you choose the verb: one of, the number of and titles are singular; a number of (= many) is plural. '
                          'Passive: has / have been + 3rd form (up to now); had been + 3rd form (before a past time).'])
    r = b.card('eng10-u7-l7-2-r3x1')['body']
    r[2] = '**Step 3:** To change active to passive: the object becomes the new subject, keep has/have/had, add "been" and the 3rd form.'
    r[4] = '**Step 5:** Add "by + the doer" only when it is important who did it.'
    u = b.unit('eng10-u7')
    for g in u['glossary']:
        if g['term'] == 'Antecedent':
            g['term'] = 'Real subject'
            g['meaning'] = 'The main noun that the verb must match. In "The list of names is long" the real subject is list, not names.'
    # ---------------- Unit 8
    rules('eng10-u8-c01', [
        '**am / is / are + -ing** is for actions happening **now**, and also for actions going on **around now**, over a period: *this week, this month, this year, these days*: *My bicycle is broken, so I **am walking** to school this week.*',
        'It also shows a **change that is happening**: *Fashion **is becoming** more expensive in Asmara.*',
        'Textbook example (Lesson 8.13): *Currently, I’**m attending** a three-month programme in secretarial science.* The writer is not in class now; the course goes on for three months.',
        '**State verbs** (*know, like, want, belong, understand*) describe a state, not an action → no -ing: *I **like** this dress* (not *am liking*).',
    ], [('These days many students are learning to sew.', True), ('I am knowing this designer.', False, 'I know this designer.'),
        ('This month my aunt is staying with us in Dekemhare.', True)])
    rules('eng10-u8-c03', [
        '**accept** = say yes to / agree to take (a verb): *accept a gift*. **except** = not including: *everyone **except** me*.',
        '**adapt** = change to fit a new situation: *adapt to the hot climate of Massawa*. **adopt** = take as your own: *adopt a new style; adopt a child*.',
    ])
    steps('eng10-u8-l8-2-wk1', ['**Step 1: Know the two words.** *accept* = say yes to (a verb). *except* = not including.',
                                 '**Step 2: Read the meaning.** Everyone came, but **not** Ruth → "not including".',
                                 '**Step 3: Correct it.** *Everyone came **except** Ruth.*'])
    body('eng10-u8-l8-2-r3x1', [
        '**Step 1:** lie – lay – lain (no object after it: rest flat): "I lie down after lunch." lay – laid – laid (needs an object: put something down): "She laid the book on the table."',
        '**Step 2:** rise – rose – risen (no object: go up): "The sun rises." raise – raised – raised (needs an object: lift): "Raise your hand."',
        '**Step 3:** sit – sat – sat (no object) vs set – set – set (put something somewhere).',
        '**Step 4:** say vs tell: say something (to someone); tell someone something: "He said that…", "He told me that…".',
        '**Step 5:** borrow (take from someone) vs lend (give to someone); bring (towards the speaker) vs take (away from the speaker).',
        '**Example:** "Yesterday the price of sugar (raised/rose)." → rose (no object). "Can you (borrow/lend) me your pen?" → lend. "She (said/told) me the answer." → told (a person follows).',
    ])
    body('eng10-u8-c06', ['am / is / are + -ing = now or around now (this week, these days) and changes that are happening; state verbs stay simple. '
                          'accept (say yes to) vs except (not including); adapt (change to fit) vs adopt (take as your own). '
                          'have / has been + -ing = from the past up to now (how long).'])
    # ---------------- Unit 9
    rules('eng10-u9-c01', [
        '**Present simple** – habits and facts: *Water **boils** at 100 °C. My mother **makes** coffee every morning.*',
        '**Present continuous** – happening now: *Look! The children **are dancing**.*',
        '**Past simple** – a finished time in the past (*yesterday, ago, in 2010*): *I **saw** him yesterday.*',
        '**Present perfect** (have/has + 3rd form) – something in the past that matters now, with *ever, never, already, yet, just, recently, since, for*: *I **have** just **finished** my exams.*',
        '**Future perfect** (will have + 3rd form) – finished **before** a future time: *By June I **will have finished** Grade 10.*',
    ])
    rules('eng10-u9-c03', [
        'Newspaper headlines are short. They leave out small words (*a, the, is, are*).',
        'The **present simple** in a headline means a recent past event: ***Students Win** National Prize* = Students have won a national prize.',
        '**to + verb** means the future: ***Minister To Open** New School* = The minister is going to open a new school.',
        'A **3rd form alone** means a passive: ***Bridge Opened** In Keren* = A bridge has been opened in Keren.',
    ])
    body('eng10-u9-c06', ['Choose the tense from the time words: habits and facts (present simple), now (present continuous), finished past (past simple), '
                          'past linked to now (present perfect), finished before a future time (will have + 3rd form). Headlines: present simple = recent past, to + verb = future.'])


def unit_texts(b):
    intro = {
        'eng10-u1': "Grammar: must, have to and should (what you need to do), and must be / can't be / must have (guessing from a clue).",
        'eng10-u2': 'Grammar: -ing words used like nouns (gerunds), to + verb (infinitives), -ing and -ed describing words, and will be + -ing (future continuous).',
        'eng10-u3': 'Grammar: noun clauses – small sentences inside a sentence that work like a noun (what you said, that he is honest, where she lives) – and a review of modal verbs.',
        'eng10-u4': 'Grammar: sentences with a linking verb (Subject + be / become / seem + describing word) and groups of words that describe a noun (who, which, that, whose, where).',
        'eng10-u5': 'Grammar: will, should and might for how sure we are, and groups of words that tell when, why, how or for what purpose (so that, in order to, lest, although).',
        'eng10-u6': 'Grammar: how word endings show the word type (noun, adjective, verb, adverb), and polite indirect questions (Could you tell me where the bank is?).',
        'eng10-u7': 'Grammar: making the verb match the real subject in long sentences, and the passive with has/have been and had been (has been built, had been stolen).',
        'eng10-u8': 'Grammar: am/is/are + -ing for actions going on around now, confusing word pairs (accept/except, adapt/adopt), and have/has been + -ing (present perfect continuous) for actions from the past up to now.',
        'eng10-u9': 'Grammar: choosing the right tense from the time words, confusing verbs, and the present simple in newspaper headlines.',
        'eng10-u10': 'Grammar: comparing things with as … as, the same as, different from, -er / more … than and the -est / the most.',
    }
    gloss = {
        'eng10-u1': [('Modal verb', 'A small helping verb (must, should, can, might) before a main verb. It adds a meaning like "necessary" or "possible". The verb after it is plain: no to, no -s.'),
                     ('Inference', 'A guess you are almost sure about because of a clue (evidence): The road is wet – it must have rained.')],
        'eng10-u2': [('Gerund', 'A verb + -ing used like a noun (a thing): Swimming is fun.'), ('Infinitive', 'to + the plain verb: to go, to camp.'),
                     ('Future continuous', 'will be + verb-ing: an action that will be in the middle of happening at a future time.')],
        'eng10-u3': [('Noun clause', 'A small sentence with its own subject and verb that works like one noun: I know where she lives (= I know her address).'),
                     ('Complement', 'The words after is / was / seem that tell us more about the subject: The problem is that we have no time.')],
        'eng10-u4': [('Linking verb', 'A verb like be, become, seem, look, feel that joins the subject to a word that describes it: Massawa is hot.'),
                     ('Relative pronoun', 'who, which, that, whose: the word that starts a group of words describing a noun: the doctor who works in Keren.')],
        'eng10-u5': [('Adverbial clause', 'A part of a sentence with its own subject and verb that tells when, why, how or for what purpose: because prices rose; so that I can save.'),
                     ('Lest', 'A formal word meaning "so that … not": Write it down lest you forget (= so that you don\'t forget).')],
        'eng10-u6': [('Indirect question', 'A polite question that starts with Could you tell me… / Do you know… and then uses statement order: Do you know where the bank is?')],
        'eng10-u8': [('State verb', 'A verb for a state (thinking, feeling, having), not an action: know, like, want, belong. No -ing form.')],
        'eng10-u9': [('Present perfect', 'have / has + 3rd form: something in the past that is important now: I have finished my exams.')],
    }
    tips = {
        'eng10-u1': "**must** = I'm sure it IS true (or a rule); **can't** = I'm sure it is NOT true; add **have + 3rd form** for the past.",
        'eng10-u2': '**After in / at / of / about, always -ing.** The **-ing** thing causes the **-ed** feeling.',
        'eng10-u5': '**will** 100% → **should** 80% → **might** 50%.',
    }
    for uid, s in intro.items():
        b.unit(uid)['intro'] = s
    for uid, items in gloss.items():
        b.put_glossary(uid, items)
    for uid, s in tips.items():
        b.unit(uid)['tips'][0]['text'] = s
    b.card('eng10-u1-c05')['body'] = [tips['eng10-u1']]
    b.card('eng10-u2-c05')['body'] = [tips['eng10-u2']]


JARGON = [
    (r'\bhead noun\b', 'main noun'), (r'\ban indefinite pronoun\b', 'a word like everyone / nobody'), (r'\bbare infinitive\b', 'plain verb (no to)'),
    (r'\ba concession clause\b', 'a contrast clause'), (r'\bA perfect participle \(Having \+ past participle\)', '"Having + 3rd form"'),
    (r'\bA present participle \(-ing\)', 'An -ing form'), (r'\bis a prepositional phrase that does not change agreement\b', 'is only an extra phrase; it does not change the verb'),
    (r'\bdeclarative word order\b', 'statement order'), (r'\binterrogative inversion\b', 'question order'), (r'\bPresent Progressive\b', 'present continuous'),
    (r'\bSimple Past\b', 'past simple'), (r'\bthe agent\b', 'the doer'), (r'\bproximity rule\b', 'nearer-subject rule'), (r'\(Proximity Rule\)', ''),
    (r'\(progressive aspect\)', ''), (r'\(double-object passive\)', ''), (r'\(present logical deduction\)', ''), (r'\(past logical deduction\)', ''),
    (r'\(inversion\)', ''), (r'\(Reported Wh-question\)', ''),
]


def tips_and_fixes(b):
    for uid, new in UNIT_TIP.items():
        u = b.unit(uid)
        qs = u['exercise']['questions']
        # the old unit-wide tip = the most common tip on the original exercise items (q01-q08, r2q.., mx..)
        cnt = {}
        for q in qs:
            if re.search(r'-(q\d+|r2q\d+|mx\d+)$', q['id']) and q.get('tip') not in GENERIC_TIPS and q.get('tip') != new:
                cnt[q.get('tip')] = cnt.get(q.get('tip'), 0) + 1
        old = max(cnt, key=cnt.get) if cnt else None
        for q in qs:
            if q.get('tip') in GENERIC_TIPS or (old and q.get('tip') == old):
                q['tip'] = new
        if old:
            for l in u['lessons']:
                for c in l['cards']:
                    if c.get('type') == 'check' and old in c.get('why', ''):
                        c['why'] = c['why'].replace(old, new)
    q = b.question('eng10-u3-r2q09')
    q['why'] = [w.replace('In option B, "that she wrote"', 'In option A, "that she wrote"') for w in q['why']]
    b.sub_all(JARGON)
    # tidy spaces left by removed brackets
    b.sub_all([(r' {2,}', ' '), (r' ([,.;:።])', r'\1'), (r'\s+$', '')], where={c['id'] for u in b.d['units'] for l in u['lessons'] for c in l['cards'] if c['id'].endswith(('chkE1', 'chkE2'))})


def apply(b):
    move_imported(b)
    main_cards(b)
    unit_texts(b)
    thin_lessons(b)
    tips_and_fixes(b)


def thin_lessons(b):
    """lessons that lost the off-topic imported cards get their own worked example and quick checks"""
    from lib import worked, check
    T2, T4, T5, T6, T8 = (UNIT_TIP[k] for k in ('eng10-u2', 'eng10-u4', 'eng10-u5', 'eng10-u6', 'eng10-u8'))
    L = 'eng10-u2-l2-1'
    b.put_cards(L, [
        worked(L + '-s1', 'Step by step: -ing or to + verb?',
               'Complete: (a) We enjoy ____ (walk) along the beach in Massawa. (b) They decided ____ (travel) to Nakfa by bus. '
               '(c) She is interested in ____ (learn) Arabic. (d) He went to the market ____ (buy) coffee beans. (e) The football match was ____ (excite); we were all ____ (excite).', [
                   '**Step 1: Look at the word just before the gap.**',
                   '**Step 2: enjoy / avoid / finish → -ing.** (a) enjoy **walking**.',
                   '**Step 3: want / decide / hope / plan → to + verb.** (b) decided **to travel**.',
                   '**Step 4: a small word like in / at / of / about → -ing.** (c) interested in **learning**.',
                   '**Step 5: Why did he go? → to + verb (purpose).** (d) **to buy**.',
                   '**Step 6: cause → -ing, feeling → -ed.** (e) The match was **exciting**; we were **excited**.',
               ], '(a) walking (b) to travel (c) learning (d) to buy (e) exciting, excited'),
        check(L + '-s2', 'My grandfather finished ____ the field before the rain came.', {'A': 'to plough', 'B': 'ploughing', 'C': 'plough', 'D': 'ploughed'}, 'B', [
            '**Step 1:** The word before the gap is *finished*.', '**Step 2:** *finish* is always followed by **-ing** → **ploughing**.',
            '**Step 3:** *to plough* follows verbs like *want, decide, hope* – not *finish*.', f'**Tip:** {T2}']),
        check(L + '-s3', 'We hope ____ Emba Soira next summer.', {'A': 'climbing', 'B': 'to climb', 'C': 'climb', 'D': 'climbed'}, 'B', [
            '**Step 1:** The word before the gap is *hope*.', '**Step 2:** *hope* is followed by **to + verb** → **to climb**.',
            '**Step 3:** ✗ *hope climbing* is not English.', f'**Tip:** {T2}']),
        check(L + '-s4', 'The long walk to Debre Bizen was very ____.', {'A': 'tired', 'B': 'tiring', 'C': 'tire', 'D': 'tiredly'}, 'B', [
            '**Step 1:** The walk is the **thing** that causes the feeling.', '**Step 2:** cause → **-ing**: *tiring*.',
            '**Step 3:** The people feel **tired** (-ed): *We were tired after the tiring walk.*', f'**Tip:** {T2}']),
    ])
    L = 'eng10-u4-l4-1'
    b.put_cards(L, [
        check(L + '-s1', 'After the long journey from Assab, the passengers looked ____.', {'A': 'tiredly', 'B': 'tired', 'C': 'tiredness', 'D': 'tire'}, 'B', [
            '**Step 1:** Here *looked* is a linking verb (= seemed); it joins *the passengers* to a describing word.',
            '**Step 2:** After a linking verb use an **adjective**: **tired**.', '**Step 3:** *tiredly* is an -ly word – it would describe an action, not the passengers.', f'**Tip:** {T4}']),
        check(L + '-s2', 'Which sentence has the pattern Subject + linking verb + complement?', {'A': 'My sister became a nurse.', 'B': 'My sister helps sick people.', 'C': 'My sister works in Barentu.', 'D': 'My sister runs fast.'}, 'A', [
            '**Step 1:** Look for a linking verb: *be, become, seem, look, feel*.',
            '**Step 2:** In A, *became* joins *my sister* to *a nurse* (what she is) → S + V + C.',
            '**Step 3:** B, C and D have action verbs (*helps, works, runs*).', f'**Tip:** {T4}']),
    ])
    L = 'eng10-u5-l5-1'
    b.put_cards(L, [
        worked(L + '-s1', 'Step by step: will, should or might?',
               'Complete: (a) Don\'t worry about the fees – my father ____ pay them; he has already got the money. '
               '(b) The bus left Asmara at 7, so it ____ be in Keren by 9. (c) I\'m not sure, but prices ____ go down after the harvest.', [
                   '**Step 1: How sure is the speaker?** Look for clue words.',
                   '**Step 2: very sure → will.** (a) *he has already got the money* → **will**.',
                   '**Step 3: expected (it normally happens) → should.** (b) a normal journey time → **should**.',
                   '**Step 4: maybe → might.** (c) *I\'m not sure* → **might**.',
               ], '(a) will (b) should (c) might'),
        check(L + '-s2', 'Ruth studied every day for the exam, so she ____ pass easily.', {'A': 'should', 'B': "can't", 'C': 'might not', 'D': "mustn't"}, 'A', [
            '**Step 1:** Studying every day makes passing **expected**.', '**Step 2:** expected → **should**.',
            "**Step 3:** *can't* and *might not* say the opposite; *mustn't* means not allowed.", f'**Tip:** {T5}']),
        check(L + '-s3', 'Take an umbrella. It ____ rain this afternoon – the sky is grey, but I\'m not sure.', {'A': 'will certainly', 'B': 'might', 'C': 'must', 'D': "can't"}, 'B', [
            "**Step 1:** *I'm not sure* = maybe.", '**Step 2:** maybe → **might**.', '**Step 3:** *will certainly* and *must* are too sure; *can\'t* = sure it won\'t.', f'**Tip:** {T5}']),
    ])
    L = 'eng10-u6-l6-1'
    b.put_cards(L, [
        worked(L + '-s1', 'Step by step: choose the word type from the gap',
               'Complete with the right form of the word in brackets: (a) Please read the ____ (instruct) on the packet. (b) This knife is very ____ (use) in the kitchen. '
               '(c) Mix the flour and water ____ (slow). (d) Can you ____ (clear) what you mean?', [
                   '**Step 1: Look at the word before the gap.**',
                   '**Step 2: after *the* → a noun.** (a) **instructions** (-tion).',
                   '**Step 3: after *very* / *is* → an adjective.** (b) **useful** (-ful).',
                   '**Step 4: after an action (*mix*) → an adverb.** (c) **slowly** (-ly).',
                   '**Step 5: after *can / to / will* → a verb.** (d) **clarify** (-ify).',
               ], '(a) instructions (b) useful (c) slowly (d) clarify'),
        check(L + '-s2', 'The ____ of the new road to Massawa took two years.', {'A': 'construct', 'B': 'constructive', 'C': 'construction', 'D': 'constructively'}, 'C', [
            '**Step 1:** After *The* we need a **noun**.', '**Step 2:** The ending **-tion** makes nouns → **construction**.',
            '**Step 3:** *construct* = verb, *constructive* = adjective, *constructively* = adverb.', f'**Tip:** {T6}']),
        check(L + '-s3', 'Bake the bread ____ so that it does not burn.', {'A': 'careful', 'B': 'carefully', 'C': 'care', 'D': 'carefulness'}, 'B', [
            '**Step 1:** The word tells **how** to bake.', '**Step 2:** how an action is done → adverb (**-ly**): **carefully**.',
            '**Step 3:** *careful* is an adjective (a careful cook).', f'**Tip:** {T6}']),
    ])
    L = 'eng10-u8-l8-1'
    b.put_cards(L, [
        worked(L + '-s1', 'Step by step: now, around now, or always?',
               'Complete: (a) Look! Selam ____ (wear) a new zuria. (b) This term I ____ (take) extra maths lessons on Saturdays. '
               '(c) My father ____ (work) at the port in Massawa; he has worked there for years. (d) I ____ (like) your new shoes.', [
                   '**Step 1: Happening at this moment?** (a) *Look!* → **is wearing**.',
                   '**Step 2: Going on around now, for a limited period?** (b) *This term* → **am taking**.',
                   '**Step 3: Always true / a permanent job?** (c) → present simple **works**.',
                   '**Step 4: A state verb?** (d) *like* → no -ing → **like**.',
               ], '(a) is wearing (b) am taking (c) works (d) like'),
        check(L + '-s2', 'These days more and more young people in Asmara ____ online.', {'A': 'shop', 'B': 'are shopping', 'C': 'shopped', 'D': 'have shop'}, 'B', [
            '**Step 1:** *These days* = a period around now, and a change that is happening.', '**Step 2:** → present continuous: **are shopping**.',
            '**Step 3:** *have shop* is not a correct form.', f'**Tip:** {T8}']),
    ])
