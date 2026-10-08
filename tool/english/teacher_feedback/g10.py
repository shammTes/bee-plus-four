"""Grade 10: must vs have to (1.1), noun clause as subject (3.1), simpler indirect questions (6.2),
present perfect continuous (new lesson 8.3)."""
from lib import Book, grammar, table, text, worked, check, mcq, fill, tf, short, unitmap

MH_TIP = 'Ask two questions: Is it necessary, forbidden or not necessary? If necessary, who makes the rule: me (must) or someone else (have to)?'
NS_TIP = 'Find the main verb. Everything before it is the subject. If that subject has its own subject + verb, it is a noun clause.'
PP_TIP = 'Clue words: for / since / How long? / all day → have been + -ing. How many? / a number / finished result → have + V3.'


def must_have_to(b):
    p = 10
    b.put_cards('eng10-u1-l1-1', [
        grammar('eng10-u1-l1-1-mh1', 'Must or have to? Who makes the rule?', [
            '**must** and **have to** both mean *it is necessary*. The difference is **who makes the rule**.',
            '**must** = the **speaker** feels it is necessary (my own rule or strong feeling): *I **must** study tonight – I want a good mark.* *You **must** visit us again!*',
            '**have to / has to** = the rule comes from **outside**: a law, the school, a doctor, a timetable, a boss: *We **have to** wear a uniform at school.* *Drivers **have to** stop at a red light.*',
            'Written rules and notices usually use **must** (the school or office is "speaking"): *Students **must** show their ID card.*',
            '**Past:** *must* has no past form. Use **had to** for every past obligation: *Yesterday I **had to** walk to school.* **Future:** **will have to**: *You **will have to** pay next year.*',
            '**Questions** usually use have to: *Do I have to…? Does she have to…? Did you have to…?*',
        ], [
            ('I must call my mother tonight; I promised her.', True),
            ('At our school we have to stand up when the teacher comes in.', True),
            ('Yesterday we must stay late at school.', False, 'Yesterday we had to stay late at school.'),
            ('She have to wear glasses.', False, 'She has to wear glasses.'),
            ('Does he has to come?', False, 'Does he have to come?'),
        ], pattern='must + base verb  ·  have/has to + base verb  ·  had to + base verb (past)', page=p),
        table('eng10-u1-l1-1-mh2', 'Must vs have to: the key differences', ['', 'must', 'have to'], [
            ['Who makes the rule?', 'the speaker (I feel it is necessary)', 'someone else: a law, the school, a doctor, a timetable'],
            ['Example', 'I must finish my essay tonight.', 'We have to be at school by 7:30.'],
            ['Negative', "mustn't = do NOT do it (not allowed)", "don't have to = it is not necessary (you can choose)"],
            ['Negative example', "You mustn't smoke in the hospital.", "You don't have to bring lunch; the school gives food."],
            ['Past', 'no past form → use had to', 'had to: We had to wait two hours.'],
            ['Future', 'must (a decision now): I must go tomorrow.', 'will have to: You will have to pay next year.'],
            ['Question', 'Must I…? (rare, formal)', 'Do I have to…? / Did you have to…?'],
        ], page=p),
        table('eng10-u1-l1-1-mh3', "Mustn't or don't have to?", ['Sentence', 'Meaning', 'Can you do it?'], [
            ["You mustn't cheat in the exam.", 'It is forbidden.', 'No! It is against the rules.'],
            ["You don't have to come on Saturday.", 'It is not necessary.', 'Yes, if you want. It is your choice.'],
            ["Students mustn't run in the corridor.", 'Running is not allowed.', 'No.'],
            ["We don't have to wear a uniform on Friday.", 'A uniform is not needed.', 'Yes, you can choose.'],
        ], page=p),
        worked('eng10-u1-l1-1-mh4', "Step by step: must, have to, mustn't or don't have to?",
               'Complete: (a) The doctor says I ____ take this medicine three times a day. (b) I ____ remember to buy bread – we have none left. '
               '(c) You ____ touch that wire! It is dangerous. (d) Tomorrow is a holiday, so we ____ get up early. (e) Last year my brother ____ work on Saturdays.', [
                   '**Step 1: Is it necessary, forbidden or not necessary?** (a) necessary (b) necessary (c) forbidden (d) not necessary (e) necessary.',
                   '**Step 2: If it is necessary, who makes the rule?** (a) the doctor (outside) → **have to**. (b) I decide myself → **must**.',
                   "**Step 3: Forbidden → mustn't.** (c) You **mustn't** touch that wire!",
                   "**Step 4: Not necessary → don't have to.** (d) We **don't have to** get up early.",
                   '**Step 5: Past time → had to.** (e) *Last year* → my brother **had to** work on Saturdays.',
                   "**Tip:** In (a) *must* is not wrong, but *have to* is better because the rule comes from the doctor.",
               ], "(a) have to (b) must (c) mustn't (d) don't have to (e) had to", page=p),
        check('eng10-u1-l1-1-mh5', "A notice at the zoo: \"Visitors ____ feed the animals.\" (Feeding is not allowed.)",
              {'A': 'must', 'B': "mustn't", 'C': "don't have to", 'D': 'had to'}, 'B', [
                  '**Step 1:** Feeding is **not allowed**, so it is forbidden.',
                  "**Step 2:** Forbidden = **mustn't**.",
                  "**Step 3:** *don't have to* would mean *you can choose* – wrong here. *must* means it is necessary.",
                  "**Tip:** mustn't = STOP, don't do it. don't have to = you are free to choose."], page=p),
        check('eng10-u1-l1-1-mh6', 'My new school is near my house, so I ____ take a bus any more. I can walk.',
              {'A': "mustn't", 'B': "don't have to", 'C': 'must', 'D': 'have to'}, 'B', [
                  '**Step 1:** "I can walk" shows the bus is **not necessary**.',
                  "**Step 2:** Not necessary = **don't have to**.",
                  "**Step 3:** *mustn't* would mean taking the bus is forbidden – that is not the meaning.",
                  "**Tip:** If you can choose, use don't have to."], page=p),
        check('eng10-u1-l1-1-mh7', 'When my father was a student, he ____ walk ten kilometres to school every day.',
              {'A': 'must', 'B': 'has to', 'C': 'had to', 'D': 'musted'}, 'C', [
                  '**Step 1:** "When my father was a student" is **past** time.',
                  '**Step 2:** *must* has no past form, so we use **had to**.',
                  '**Step 3:** *musted* is not a word; *has to* is present.',
                  "**Tip:** Past obligation = had to (for every person: I/you/he/they had to)."], page=p),
        check('eng10-u1-l1-1-mh8', "I ____ remember to call Aster tonight. It's her birthday and I don't want to forget.",
              {'A': 'must', 'B': "mustn't", 'C': "don't have to", 'D': 'had to'}, 'A', [
                  '**Step 1:** It is necessary, and the speaker decides it himself ("I don\'t want to forget").',
                  '**Step 2:** A personal feeling of necessity = **must**.',
                  "**Step 3:** *mustn't* = forbidden, *don't have to* = not necessary, *had to* = past. None fit.",
                  "**Tip:** must = I feel it is necessary; have to = someone else made the rule."], page=p),
    ], after='eng10-u1-c02')
    sim = [('Complete: "Look at the sign: you ____ park here." (parking is not allowed)', "mustn't"),
           ('Complete: "It\'s Sunday – I ____ go to school today." (not necessary)', "don't have to")]
    b.put_questions('eng10-u1', [
        mcq('eng10-u1-mhq01', 'In Eritrea, drivers ____ drive on the right side of the road. It is the law.',
            {'A': 'have to', 'B': "don't have to", 'C': 'must to', 'D': 'had to'}, 'A',
            ['The rule comes from outside (the law) and it is present: **have to**.', '*must to* is never correct: no *to* after must.', '*had to* is past.'],
            MH_TIP, [('Complete: "Students ____ wear a uniform at our school." (school rule)', 'have to'), ('Is "must to" ever correct?', 'No. must + base verb: must go.')], page=10),
        mcq('eng10-u1-mhq02', 'You ____ talk during the exam. The teacher will take your paper.',
            {'A': "don't have to", 'B': "mustn't", 'C': 'has to', 'D': "didn't have to"}, 'B',
            ['Talking is **forbidden** (the teacher will take your paper).', "Forbidden = **mustn't**.", "*don't have to* would mean talking is not necessary but allowed."],
            MH_TIP, sim, page=10),
        mcq('eng10-u1-mhq03', 'The bus was late, so we ____ wait for an hour.',
            {'A': 'must', 'B': 'have to', 'C': 'had to', 'D': 'must have'}, 'C',
            ['"The bus was late" is past.', 'Past obligation = **had to**.', '*must have* + V3 is for a guess about the past, not obligation.'],
            MH_TIP, [('Make past: "I have to work late."', 'I had to work late.'), ('Make past: "She must leave early."', 'She had to leave early.')], page=10),
        mcq('eng10-u1-mhq04', 'Water is free here, so you ____ pay for it.',
            {'A': "mustn't", 'B': "don't have to", 'C': 'must', 'D': 'has to'}, 'B',
            ['Free = paying is **not necessary**.', "Not necessary = **don't have to**.", "*mustn't* would mean paying is forbidden."],
            MH_TIP, sim, page=10),
        mcq('eng10-u1-mhq05', '____ your sister have to wear a uniform at her school?',
            {'A': 'Do', 'B': 'Does', 'C': 'Must', 'D': 'Has'}, 'B',
            ['Questions with *have to* use do/does/did.', '*your sister* = he/she → **Does**.', 'So: Does your sister have to wear a uniform?'],
            MH_TIP, [('Make a question: "They have to pay."', 'Do they have to pay?'), ('Make a past question: "He had to wait."', 'Did he have to wait?')], page=10),
        fill('eng10-u1-mhq06', 'I feel terrible. I ____ stop eating so much sugar. (my own decision)', 'must',
             ['must', 'have to', "mustn't", 'had to'],
             ['The speaker decides it himself: a personal feeling of necessity.', 'Use **must**.'], MH_TIP,
             [('Complete: "The doctor says I ____ stop eating sugar."', 'have to (the rule comes from the doctor)')], page=10),
        fill('eng10-u1-mhq07', 'Next year you ____ pay for the bus; it will not be free any more. (future)', 'will have to',
             ['will have to', 'will must', 'must to', 'had to'],
             ['Future obligation = **will have to**.', '*will must* is wrong: two modals cannot go together.'], MH_TIP,
             [('Make future: "We have to walk."', 'We will have to walk.')], page=10),
        tf('eng10-u1-mhq08', "True or false: \"You don't have to come\" and \"You mustn't come\" have the same meaning.", False,
           ["False. *You don't have to come* = it is not necessary, you can choose.", "*You mustn't come* = it is forbidden, do not come."], MH_TIP,
           [("What does \"You mustn't shout\" mean?", 'Shouting is not allowed.'), ("What does \"You don't have to shout\" mean?", 'Shouting is not necessary (we can hear you).')], page=10),
        short('eng10-u1-mhq09', 'Correct the error: "Last week I must go to the hospital."', 'Last week I had to go to the hospital.',
              ['*Last week* is past.', '*must* has no past form; use **had to**.'], MH_TIP,
              [('Correct: "Yesterday she must clean the house."', 'Yesterday she had to clean the house.')], page=10,
              accept=['Last week I had to go to the hospital']),
        short('eng10-u1-mhq10', 'Correct the error: "He have to finish his homework before he plays."', 'He has to finish his homework before he plays.',
              ['*He* is third person singular: **has to**, not *have to*.'], MH_TIP,
              [('Correct: "My brother have to work today."', 'My brother has to work today.')], page=10,
              accept=['He has to finish his homework before he plays']),
    ])
    c = b.card('eng10-u1-c01')
    c['rule'][0] = ("**must / have to** = it is necessary. **must** = the speaker's own feeling (*I **must** call her*); **have to** = a rule from outside: law, school, doctor (*You **have to** wear a helmet*). "
                    "**mustn't** = it is not allowed. **don't have to** = it is not necessary. Past of both: **had to**.")
    t = b.card('eng10-u1-c02')
    t['rows'][0] = ['Strong obligation', 'must (speaker) / have to (rule from outside)', 'I must hurry. / You have to obey the law.']
    if not any(r[0] == 'Past obligation' for r in t['rows']):
        t['rows'].insert(3, ['Past obligation', 'had to', 'We had to wait two hours.'])


def noun_clause_subject(b):
    p = 66  # Textbook Lesson 3.12
    b.put_cards('eng10-u3-l3-1', [
        grammar('eng10-u3-l3-1-ns1', 'Noun clause as the subject', [
            'A noun clause can be the **subject** of a sentence. It comes **before the main verb**, just like a noun: ***What you told me** was true.* (compare: ***The story** was true.*)',
            '**How to find it:** find the main verb (*was, is, surprised, depends*…). Everything before it is the subject. If you can replace it with *It* or *This*, it is a noun-clause subject: ***That he passed** surprised everyone.* → *It surprised everyone.*',
            'A noun-clause subject is **singular**: *What we need **is** more books.* *Why they left **is** a mystery.*',
            'Starters: **That** (a fact), **What / Whatever** (a thing), **Whether** (yes/no – at the start use *whether*, not *if*), **Who / Whoever, Where, When, Why, How**.',
            'Inside the clause use **statement order** (subject + verb): ***Where she lives** is a secret* (not *Where does she live*).',
            'A long subject can move to the end with **It**: *That he lied is clear.* = ***It** is clear **that he lied**.*',
        ], [
            ('What you told me was the right information.', True),
            ('How the man was killed is still a mystery to the police.', True),
            ('Whether we go or not depends on the weather.', True),
            ('If we go or not depends on the weather.', False, 'Whether we go or not depends on the weather.'),
            ('What did he say was not clear.', False, 'What he said was not clear.'),
            ("Why she didn't come were not my problem.", False, "Why she didn't come was not my problem."),
        ], pattern='[noun clause = subject] + main verb + rest of the sentence', page=p),
        table('eng10-u3-l3-1-ns2', 'Noun clauses as subject: starters and examples', ['Starter', 'Use', 'Example (the subject is in bold)'], [
            ['That', 'a fact', "**That he didn't return the book** should be reported to the director."],
            ['What / Whatever', 'a thing', '**What I want for my graduation** is a family party.'],
            ['Whether', 'yes or no', '**Whether we can go or not** depends on the plane.'],
            ['Who / Whoever', 'a person', "**Whoever attended the lecture** liked it."],
            ['How', 'the way', '**How she passed the exam** is difficult to believe.'],
            ['Why', 'the reason', "**Why she didn't come** was not my problem."],
            ['Where / When', 'place / time', '**Where we meet** is not important. **When the bus leaves** is written on the board.'],
        ], page=p),
        table('eng10-u3-l3-1-ns3', 'One noun clause, three jobs', ['Job', 'Where it goes', 'Example'], [
            ['Subject', 'before the main verb', '**What he said** surprised me.'],
            ['Object', 'after the verb', 'I did not hear **what he said**.'],
            ['Complement', 'after be (is/was)', 'The problem is **what he said**.'],
        ], page=p),
        worked('eng10-u3-l3-1-ns4', 'Step by step: make a noun clause the subject',
               'Join the sentences. Start with a noun clause. (a) He passed the exam. It surprised everyone. (b) Where did they hide the money? It is still a secret. '
               '(c) Will the school open on Monday? It depends on the rain.', [
                   '**Step 1: Choose the starter.** (a) a fact → *That*. (b) a wh-question → keep *Where*. (c) a yes/no question → *Whether*.',
                   '**Step 2: Change question order to statement order.** *did they hide* → *they hid*; *Will the school open* → *the school will open*.',
                   '**Step 3: Put the clause before the verb and drop *It*.**',
                   '(a) **That he passed the exam** surprised everyone.',
                   '(b) **Where they hid the money** is still a secret.',
                   '(c) **Whether the school will open on Monday** depends on the rain.',
                   '**Check:** the verb after the clause is singular: *surprised, is, depends*.',
               ], '(a) That he passed the exam surprised everyone. (b) Where they hid the money is still a secret. (c) Whether the school will open on Monday depends on the rain.', page=p),
        check('eng10-u3-l3-1-ns5', '____ he said in the meeting was very useful.',
              {'A': 'What', 'B': 'That', 'C': 'Whether', 'D': 'Who'}, 'A', [
                  '**Step 1:** The main verb is *was*. The subject is "____ he said in the meeting".',
                  '**Step 2:** *said* needs an object (he said *something*). **What** = the thing that.',
                  '**Step 3:** *That he said* is incomplete (said what?); *Whether* is for yes/no ideas; *Who* is for a person.',
                  '**Tip:** If the verb in the clause has no object, *what* usually fills the gap.'], page=p),
        check('eng10-u3-l3-1-ns6', '____ the bus will come on time is not certain.',
              {'A': 'If', 'B': 'Whether', 'C': 'What', 'D': 'Who'}, 'B', [
                  '**Step 1:** The idea is yes/no: will the bus come on time or not?',
                  '**Step 2:** At the **start** of a sentence use **whether**, not *if*.',
                  '**Step 3:** So: *Whether the bus will come on time is not certain.*',
                  '**Tip:** *if* can start an object clause (*I don\'t know if…*) but not a subject clause.'], page=p),
        check('eng10-u3-l3-1-ns7', 'Which sentence has a noun clause as the SUBJECT?',
              {'A': 'I know where he lives.', 'B': 'The truth is that I forgot.', 'C': 'Why he left is a mystery.', 'D': 'This is what I want.'}, 'C', [
                  '**Step 1:** Find the main verb in each sentence and look at what comes before it.',
                  '**Step 2:** In C the main verb is *is*; before it is *Why he left* – a clause with its own subject and verb. That is the subject.',
                  '**Step 3:** A = object (after *know*); B and D = complement (after *is*).',
                  '**Tip:** Subject = before the main verb; object = after an action verb; complement = after *be*.'], page=p),
        check('eng10-u3-l3-1-ns8', "Why they were late ____ not clear to the teacher.",
              {'A': 'are', 'B': 'were', 'C': 'is', 'D': 'be'}, 'C', [
                  '**Step 1:** The subject is the whole clause *Why they were late*.',
                  '**Step 2:** A noun-clause subject is **singular** → *is*.',
                  '**Step 3:** Do not match the verb to *they*; *they* is inside the clause.',
                  '**Tip:** One clause = one idea = singular verb.'], page=p),
        check('eng10-u3-l3-1-ns9', 'Choose the correct sentence.',
              {'A': 'What did you tell me was true.', 'B': 'What you told me was true.', 'C': 'What you told me were true.', 'D': 'That you told me was true.'}, 'B', [
                  '**Step 1:** A noun clause uses statement order: *what you told me* (not *what did you tell me*).',
                  '**Step 2:** The verb after the clause is singular: *was*.',
                  '**Step 3:** D is wrong: *told me* needs an object, so we need *what*, not *that*.',
                  '**Tip:** Check order inside the clause, then the verb after it.'], page=p),
    ], after='eng10-u3-c02')
    sim2 = [('Join: "Is he coming? I don\'t know." (start with a noun clause)', 'Whether he is coming is not known. / I don\'t know whether he is coming.'),
            ('Underline the subject: "What she cooked smelled wonderful."', 'What she cooked')]
    b.put_questions('eng10-u3', [
        mcq('eng10-u3-nsq01', '____ you choose as your career is your own decision.',
            {'A': 'What', 'B': 'That', 'C': 'If', 'D': 'Which do'}, 'A',
            ['The subject is "____ you choose as your career" (before the verb *is*).', '*choose* needs an object → **What** (= the thing that).', '*If* cannot start a subject clause; *Which do* uses question order.'],
            NS_TIP, sim2, page=66),
        mcq('eng10-u3-nsq02', '____ the earth goes round the sun is a scientific fact.',
            {'A': 'What', 'B': 'That', 'C': 'Whether', 'D': 'Who'}, 'B',
            ['The clause *the earth goes round the sun* is complete (subject + verb + rest).', 'A complete fact used as subject starts with **That**.', '*What* is used when something is missing (an object).'],
            NS_TIP, [('Complete: "____ smoking is harmful is well known."', 'That')], page=66),
        mcq('eng10-u3-nsq03', '____ will win the election is still unknown.',
            {'A': 'Who', 'B': 'What', 'C': 'That', 'D': 'Whom'}, 'A',
            ['The clause needs a person as the subject of *will win*.', 'Person + subject of the clause → **Who**.', '*Whom* is an object form.'],
            NS_TIP, [('Complete: "____ broke the window should tell the teacher."', 'Whoever / Who')], page=66),
        mcq('eng10-u3-nsq04', 'How the prisoners escaped ____ a mystery.',
            {'A': 'are', 'B': 'were', 'C': 'remains', 'D': 'remain'}, 'C',
            ['The subject is the clause *How the prisoners escaped* → singular verb.', '**remains** (singular).', 'Do not match the verb with *prisoners*; it is inside the clause.'],
            NS_TIP, [('Choose: "What they want (is / are) a new road."', 'is')], page=66),
        mcq('eng10-u3-nsq05', 'Choose the correct sentence.',
            {'A': 'Where does she live is a secret.', 'B': 'Where she lives is a secret.', 'C': 'Where she lives are a secret.', 'D': 'Where lives she is a secret.'}, 'B',
            ['Statement order inside the clause: *she lives*.', 'Singular verb after the clause: *is*.', 'Only B has both.'],
            NS_TIP, [('Correct: "What time does the film start is on the poster."', 'What time the film starts is on the poster.')], page=66),
        fill('eng10-u3-nsq06', '____ we will travel by bus or by car depends on the money we have.', 'Whether',
             ['Whether', 'If', 'That', 'What'],
             ['Two choices (bus or car) = a yes/no idea.', 'At the start of a sentence use **Whether**, not *If*.'], NS_TIP,
             [('Complete: "____ it rains or not, the match will continue."', 'Whether')], page=66),
        fill('eng10-u3-nsq07', '____ he did not come to the party was not my problem. (reason)', 'Why',
             ['Why', 'What', 'Who', 'Which'],
             ['The clause gives a **reason** → **Why**.'], NS_TIP,
             [('Complete: "____ she learned English so fast surprised us." (the way)', 'How')], page=66),
        short('eng10-u3-nsq08', 'Join the sentences with a noun clause as subject: "She won the prize. It made her parents proud."',
              'That she won the prize made her parents proud.',
              ['A complete fact → start with **That**.', 'Put the clause before the verb and drop *It*: *That she won the prize made her parents proud.*'], NS_TIP,
              [('Join: "He lied. It is clear."', 'That he lied is clear. (or: It is clear that he lied.)')], page=66,
              accept=['That she won the prize made her parents proud']),
        short('eng10-u3-nsq09', 'Underline (write) the noun clause and say its job: "Whoever finishes first will get a prize."',
              'Whoever finishes first – subject',
              ['The main verb is *will get*.', 'Before it: *Whoever finishes first* (its own verb *finishes*) → noun clause as **subject**.'], NS_TIP,
              [('Write the noun clause and its job: "I know what you mean."', 'what you mean – object')], page=66),
        tf('eng10-u3-nsq10', 'True or false: "If he will come is not certain" is correct English.', False,
           ['False. A noun clause at the start of a sentence begins with **whether**, not *if*.', 'Correct: *Whether he will come is not certain.*'], NS_TIP,
           [('Correct: "If they agree is the question."', 'Whether they agree is the question.')], page=66),
    ])
    c = b.card('eng10-u3-c01')
    if not any('Subject position' in r for r in c['rule']):
        c['rule'].insert(1, '**Subject position** (before the main verb): ***What you told me** was true.* ***Whether we go** depends on the weather.* A noun-clause subject takes a singular verb.')
    t = b.card('eng10-u3-c02')
    if not any(r[0] == 'Subject' for r in t['rows']):
        t['rows'][0:0] = [['Subject', 'what', 'What you said is true.'], ['Subject', 'that / whether', 'That he lied is clear. Whether we go depends on you.']]
    u = b.unit('eng10-u3')
    u['intro'] = 'Grammar: noun clauses as subjects, objects and complements, and a review of modal verbs.'
    b.card('eng10-u3-c05')['body'][0] = ('Noun clauses (that/what/whether/wh-) act as subjects, objects or complements. A noun-clause subject comes before the main verb and takes a singular verb. '
                                         'Inside them use statement word order, and follow the sequence of tenses after a past main verb. Modals (can, could, may, might, must, should) are followed by the base verb.')
    b.put_glossary('eng10-u3', [('Noun clause', 'A clause that does the job of a noun: subject, object or complement.')])
    for g in u['games']:
        if g['id'] == 'eng10-u3-g1':
            g['title'] = 'Match the noun clause to its job'
            g['pairs'] = [{'a': 'What you said is true.', 'b': 'subject'}, {'a': 'I know that he is honest.', 'b': 'object'},
                          {'a': 'The problem is that we are late.', 'b': 'complement'}, {'a': 'Whether we go depends on you.', 'b': 'subject (yes/no)'},
                          {'a': 'Ask if the shop is open.', 'b': 'object (yes/no)'}]


def indirect_questions(b):
    p = b.lesson('eng10-u6-l6-2')[1]['pages'][0]
    c = b.card('eng10-u6-c03')
    c['rule'] = [
        '**Direct question:** *Where is the station?* **Indirect question** (more polite): *Could you tell me **where the station is**?*',
        'Two rules: (1) after the polite start, use **statement order** (subject + verb); (2) **no do/does/did** – put the tense on the main verb.',
        'Yes/no questions use **if** or **whether**: *Is the shop open?* → *Do you know **if the shop is open**?*',
    ]
    c['pattern'] = 'Could you tell me / Do you know + wh-word or if + subject + verb'
    c['examples'] = [dict(text='Can you tell me how I bake bread?', ok=True), dict(text='Do you know where does he live?', ok=False, fix='Do you know where he lives?')]
    t = b.card('eng10-u6-c04')
    t['rows'] = [['Could you tell me where is the bank?', 'Could you tell me where the bank is?', 'Statement order.'],
                 ['Do you know when did it start?', 'Do you know when it started?', 'No did; past form of the verb.'],
                 ['Can you tell me is the doctor in?', 'Can you tell me if the doctor is in?', 'Yes/no question → if.']]
    b.card('eng10-u6-c05')['body'] = ['Polite start + **statement order** + **no do/does/did**. Yes/no → **if**.']
    b.put_cards('eng10-u6-l6-2', [
        table('eng10-u6-l6-2-iq1', 'Direct → indirect in three steps', ['Direct question', 'Indirect question'], [
            ['Where is the bank?', 'Could you tell me where the bank is?'],
            ['What time does the bus leave?', 'Do you know what time the bus leaves?'],
            ['Did she pass?', 'Do you know if she passed?'],
            ['Can he swim?', 'I wonder if he can swim.'],
        ], page=p),
    ], after='eng10-u6-c04')
    ch = b.card('eng10-u6-l6-2-r2c1')
    ch['why'] = ('**Step 1:** Indirect questions use statement order.\n\n**Step 2:** No "does" is needed: the shop closes.\n\n**Step 3:** Option B is correct.\n\n'
                 '**Tip:** Polite start + statement order + no do/does/did.')


def present_perfect_continuous(b):
    u = b.unit('eng10-u8')
    p = 167  # Textbook Lesson 8.13 (actions continuing for a period of time)
    b.put_lesson('eng10-u8', dict(id='eng10-u8-l8-3', number='8.3', title='Present perfect continuous', pages=[p, u['pages'][1]], cards=[]), after='eng10-u8-l8-2')
    b.put_cards('eng10-u8-l8-3', [
        grammar('eng10-u8-l8-3-c1', 'Present perfect continuous: form and use', [
            '**Form:** have/has + been + verb-ing. *I **have been waiting**. She **has been studying**.*',
            "**Negative:** have/has + not + been + -ing: *They **haven't been sleeping** well.* **Question:** Have/Has + subject + been + -ing? ***Has** she **been working** here long?*",
            '**Use 1 – it started in the past and is still going on now** (often with *for, since, How long…?*): *I **have been learning** English **for** six years.* *It **has been raining since** 8 o\'clock.*',
            "**Use 2 – it has just stopped and we can see the result now:** *Your eyes are red. **Have** you **been crying**?* *I'm hot because I**'ve been running**.*",
            '**for** + a period of time (*for two hours, for a week*); **since** + the starting point (*since Monday, since 2020, since I was ten*).',
            'State verbs (*know, like, believe, own, understand*) do not take -ing: *I **have known** her for years* (not *have been knowing*).',
        ], [
            ('She has been sewing dresses since this morning.', True),
            ('We have been waiting for the bus for forty minutes.', True),
            ('I am living in Keren since 2020.', False, 'I have been living in Keren since 2020.'),
            ('He has been knowing me for years.', False, 'He has known me for years.'),
            ('They have been work all day.', False, 'They have been working all day.'),
        ], pattern='have/has + been + verb-ing (+ for / since)', page=p),
        text('eng10-u8-l8-3-c2', 'Timeline: the action continues up to now', [
            '**PAST** ●———————————————→ **NOW** (and it may continue)',
            '8:00 am – Selam starts sewing.  →  11:00 am (now) – she is still sewing.',
            '**Selam has been sewing for three hours.** / **Selam has been sewing since 8 o\'clock.**',
            'The line starts in the past and reaches **now**. The present perfect continuous looks at the **whole line** and says **how long** it has lasted.',
            'Compare: *Selam **is sewing**.* (only now) – *Selam **has been sewing** for three hours.* (from 8:00 until now)',
        ], page=p),
        table('eng10-u8-l8-3-c3', 'All the forms', ['', 'I / you / we / they', 'he / she / it'], [
            ['Positive', 'have been working', 'has been working'],
            ['Short form', "I've / we've been working", "she's / it's been working"],
            ['Negative', "haven't been working", "hasn't been working"],
            ['Question', 'Have they been working?', 'Has she been working?'],
            ['Short answer', 'Yes, they have. / No, they haven\'t.', 'Yes, she has. / No, she hasn\'t.'],
            ['How long…?', 'How long have you been waiting?', 'How long has it been raining?'],
        ], page=p),
        table('eng10-u8-l8-3-c4', 'Present perfect or present perfect continuous?', ['', 'Present perfect (have + V3)', 'Present perfect continuous (have been + -ing)'], [
            ['Focus', 'the result: how much / how many', 'the activity: how long'],
            ['Example', 'I have written three letters.', 'I have been writing letters all morning.'],
            ['Finished?', 'Usually finished.', 'Maybe not finished: still going on, or just stopped.'],
            ['Question', 'How many…? How much…?', 'How long…?'],
            ['State verbs', 'I have known him for years. ✔', 'I have been knowing him… ✘'],
            ['Example 2', 'She has read the book. (she finished it)', 'She has been reading the book. (not finished yet)'],
        ], page=p),
        worked('eng10-u8-l8-3-c5', 'Step by step: present perfect or present perfect continuous?',
               "Complete: (a) Dawit ____ (play) football since 3 o'clock. He is very tired. (b) He ____ (score) two goals. "
               '(c) How long ____ you ____ (wait) for me? (d) I ____ (know) Ruth since primary school.', [
                   '**Step 1: Look for the clue words.** (a) *since 3 o\'clock* + tired → an activity that has lasted until now. (b) *two goals* → a number = result. (c) *How long* → activity. (d) *know* → a state verb.',
                   '**Step 2: Activity + how long → have/has been + -ing.** (a) Dawit **has been playing**. (c) How long **have** you **been waiting**?',
                   '**Step 3: Result / number → have/has + V3.** (b) He **has scored** two goals.',
                   '**Step 4: State verb → never -ing.** (d) I **have known** Ruth since primary school.',
                   '**Check:** he/she/it → *has*; I/you/we/they → *have*.',
               ], '(a) has been playing (b) has scored (c) have … been waiting (d) have known', page=p),
        text('eng10-u8-l8-3-c6', 'Memory tip', ['**HAVE BEEN + -ING = How long?** Ask *How long?* → have been + -ing. Ask *How many?* → have + V3.',
                                                '**For** a period (*for 3 hours*), **since** a point (*since 3 o\'clock*).'], page=p, kind='mnemonic'),
        check('eng10-u8-l8-3-c7', 'We ____ for the bus for forty minutes, and it still hasn\'t come.',
              {'A': 'wait', 'B': 'are waiting', 'C': 'have been waiting', 'D': 'had waited'}, 'C', [
                  '**Step 1:** *for forty minutes* + *it still hasn\'t come* → the waiting started in the past and is still going on.',
                  '**Step 2:** Use **have been + -ing**: *have been waiting*.',
                  '**Step 3:** *are waiting* does not show how long; *had waited* is past perfect.',
                  '**Tip:** for/since + still going on → present perfect continuous.'], page=p),
        check('eng10-u8-l8-3-c8', 'Aster ____ in this laboratory since she finished university five years ago.',
              {'A': 'is working', 'B': 'works', 'C': 'has been working', 'D': 'worked'}, 'C', [
                  '**Step 1:** *since she finished university* gives the starting point; she still works there.',
                  '**Step 2:** Started in the past + still true now → **has been working**.',
                  '**Step 3:** *is working* is a common mistake: English does not use the present continuous with *since*.',
                  '**Tip:** since + a starting point → have/has (been).'], page=p),
        check('eng10-u8-l8-3-c9', 'Your hands are dirty. What ____?',
              {'A': 'have you been doing', 'B': 'have you done', 'C': 'are you doing', 'D': 'did you do'}, 'A', [
                  '**Step 1:** We can see a result now (dirty hands) of an activity that has just stopped.',
                  '**Step 2:** Use the present perfect continuous: *What have you been doing?*',
                  '**Step 3:** *have you done* asks about a finished result, not the activity that made your hands dirty.',
                  '**Tip:** A visible result of a recent activity → have been + -ing.'], page=p),
        check('eng10-u8-l8-3-c10', 'I ____ three chapters of the book today.',
              {'A': 'have been reading', 'B': 'have read', 'C': 'am reading', 'D': 'have been read'}, 'B', [
                  '**Step 1:** *three chapters* is a number – the result.',
                  '**Step 2:** Result / how many → present perfect: **have read**.',
                  '**Step 3:** *have been read* is a passive form – wrong here.',
                  '**Tip:** How many? → have + V3. How long? → have been + -ing.'], page=p),
        check('eng10-u8-l8-3-c11', 'Choose the correct sentence.',
              {'A': 'I have been knowing Saba for ten years.', 'B': 'I know Saba since ten years.', 'C': 'I have known Saba for ten years.', 'D': 'I am knowing Saba for ten years.'}, 'C', [
                  '**Step 1:** *know* is a state verb: no -ing.',
                  '**Step 2:** Started in the past and still true → present perfect: *have known*.',
                  '**Step 3:** *for* + a period (*ten years*), not *since*.',
                  '**Tip:** State verbs (know, like, own, believe) use the present perfect, not the continuous.'], page=p),
    ])
    sim = [('Complete: "It ____ (rain) since morning."', 'has been raining'), ('Complete: "How long ____ you ____ (learn) English?"', 'have … been learning')]
    b.put_questions('eng10-u8', [
        mcq('eng10-u8-ppq01', 'My father ____ as a teacher for twenty years. He still loves his job.',
            {'A': 'works', 'B': 'has been working', 'C': 'is working', 'D': 'worked'}, 'B',
            ['*for twenty years* + *still* → started in the past, still true now.', 'Present perfect continuous: **has been working**.'], PP_TIP, sim, page=p),
        mcq('eng10-u8-ppq02', 'It ____ since early morning, so the roads are flooded.',
            {'A': 'rains', 'B': 'is raining', 'C': 'has been raining', 'D': 'has rain'}, 'C',
            ['*since early morning* gives the starting point.', 'Still going on (or just stopped, with a result: floods) → **has been raining**.'], PP_TIP, sim, page=p),
        mcq('eng10-u8-ppq03', 'How long ____ English?',
            {'A': 'are you learning', 'B': 'have you been learning', 'C': 'do you learn', 'D': 'you have been learning'}, 'B',
            ['*How long* asks about the length of an activity up to now.', 'Question order: **have you been learning**.', 'D has statement order – wrong in a direct question.'], PP_TIP, sim, page=p),
        mcq('eng10-u8-ppq04', "She's tired because she ____ all afternoon.",
            {'A': 'has been cleaning', 'B': 'has cleaned', 'C': 'cleans', 'D': 'is clean'}, 'A',
            ['A result now (tired) of an activity that lasted all afternoon.', 'Present perfect continuous: **has been cleaning**.'], PP_TIP, sim, page=p),
        mcq('eng10-u8-ppq05', 'I ____ my homework. Here it is.',
            {'A': 'have been doing', 'B': 'have done', 'C': 'am doing', 'D': 'have been done'}, 'B',
            ['*Here it is* → the homework is finished: a result.', 'Present perfect: **have done**.'], PP_TIP,
            [('Choose: "I (have painted / have been painting) the room. It looks great now."', 'have painted (finished result)')], page=p),
        mcq('eng10-u8-ppq06', 'They have been building the new school ____ last year.',
            {'A': 'for', 'B': 'since', 'C': 'ago', 'D': 'during'}, 'B',
            ['*last year* is a starting point.', 'Starting point → **since**.'], PP_TIP,
            [('Complete: "I have been waiting ____ two hours."', 'for'), ('Complete: "She has been ill ____ Monday."', 'since')], page=p),
        fill('eng10-u8-ppq07', 'We ____ (wait) for you for an hour! Where were you?', 'have been waiting',
             ['have been waiting', 'are waiting', 'have waited been', 'waited'],
             ['*for an hour* up to now → **have been waiting**.'], PP_TIP, sim, page=p),
        fill('eng10-u8-ppq08', 'Selam ____ (sew) traditional dresses since she was fifteen.', 'has been sewing',
             ['has been sewing', 'have been sewing', 'is sewing', 'sews'],
             ['*since she was fifteen* + still doing it → present perfect continuous.', '*Selam* = she → **has** been sewing.'], PP_TIP, sim, page=p),
        fill('eng10-u8-ppq09', 'I ____ (know) my best friend since primary school.', 'have known',
             ['have known', 'have been knowing', 'am knowing', 'know'],
             ['*know* is a state verb: no -ing.', 'Started in the past and still true → **have known**.'], PP_TIP,
             [('Complete: "He ____ (own) this shop for ten years."', 'has owned')], page=p),
        short('eng10-u8-ppq10', 'Correct the error: "I am studying English since 2019."', 'I have been studying English since 2019.',
              ['*since 2019* → from a past point until now.', 'Do not use the present continuous with since: **have been studying**.'], PP_TIP,
              [('Correct: "She is living here for five years."', 'She has been living here for five years.')], page=p,
              accept=['I have been studying English since 2019', "I've been studying English since 2019."]),
        short('eng10-u8-ppq11', 'Make a question with "How long": "They have been playing football." (How long…?)', 'How long have they been playing football?',
              ['Question order: How long + have + subject + been + -ing?'], PP_TIP,
              [('Make a question: "She has been crying." (How long…?)', 'How long has she been crying?')], page=p,
              accept=['How long have they been playing football']),
        tf('eng10-u8-ppq12', 'True or false: "He has been writing five letters" is the best way to say that he finished five letters.', False,
           ['False. A number of finished things (*five letters*) is a result → present perfect: *He has written five letters.*',
            '*has been writing* tells us about the activity and how long, not how many.'], PP_TIP,
           [('Which is correct for a finished result: "I have read / have been reading two books this week"?', 'have read')], page=p),
    ])
    u['intro'] = ('Grammar: the present continuous for actions continuing over a period, confusing verbs (accept/except, adapt/adopt), '
                  'and the present perfect continuous for actions that started in the past and are still going on.')
    b.put_glossary('eng10-u8', [('Present perfect continuous', 'have/has + been + verb-ing: an action that started in the past and is still going on (or has just stopped).'),
                                ('for / since', 'for + a period (for two hours); since + a starting point (since Monday).')])
    if not any(g['id'] == 'eng10-u8-g2' for g in u['games']):
        u['games'].append(dict(id='eng10-u8-g2', type='match', title='Match the sentence to its meaning', src='notes', lesson='eng10-u8-l8-3', pairs=[
            {'a': 'I have been reading for two hours.', 'b': 'activity, how long (maybe not finished)'},
            {'a': 'I have read two books.', 'b': 'result, how many (finished)'},
            {'a': 'since Monday', 'b': 'starting point'},
            {'a': 'for three days', 'b': 'period of time'},
            {'a': 'I have known her for years.', 'b': 'state verb: no -ing'}]))
    m = u['unitMap']
    if not any(n['id'] == 'l8_3' for n in m['nodes']):
        m['nodes'].append(dict(id='l8_3', label='Present perfect continuous', kind='topic', lesson='eng10-u8-l8-3', cards=['eng10-u8-l8-3-c1', 'eng10-u8-l8-3-c4']))
        m['edges'].append({'from': 'unit', 'to': 'l8_3', 'label': 'includes'})
    u['tips'] = [t for t in u['tips'] if t.get('card') != 'eng10-u8-l8-3-c6'] + [dict(text='**How long?** → have been + -ing. **How many?** → have + V3.', page=p, src='notes', card='eng10-u8-l8-3-c6')]


def apply():
    b = Book(10)
    must_have_to(b)
    noun_clause_subject(b)
    indirect_questions(b)
    present_perfect_continuous(b)
    return b
