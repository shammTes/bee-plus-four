"""Grade 9 Unit 6: fix lesson 6.2 (parts of speech 2) and add a full lesson 6.3 Prepositions
(textbook Unit 6, Lessons 6.4-6.5, pages 112-115)."""
from lib import grammar, table, text, worked, check, mcq, fill, tf, short

P = 112      # Lesson 6.4: prepositions (definition, list, examples)
PX = 114     # Lesson 6.5 B: "Put the correct prepositions in the blank spaces"
L2 = 'eng9-u6-l6-2'
L3 = 'eng9-u6-l6-3'
PREP_TIP = ('Time: at + clock time, on + day/date, in + month/year/part of the day. Place: at a point, on a surface or a line, '
            'in a space or an area. Length of time → for; starting point → since; deadline → by; all the time up to then → until; '
            'during + noun, while + subject + verb.')
PREP_TIP_WORDS = 'Many words have their own partner preposition: learn them in pairs (good at, afraid of, interested in, wait for, listen to, pay for, look after).'


def fix_lesson_62(b):
    u = b.unit('eng9-u6')
    c = b.card('eng9-u6-c03')
    c['title'] = 'Parts of speech (2): adverbs, conjunctions, prepositions, interjections'
    c['rule'] = [
        'An **adverb** tells **how, when or where** something happens. Many adverbs are an adjective + **-ly**: *slow → slowly, careful → carefully, happy → happily*: *The old man walked **slowly** along the street.* Adverbs of time and place: *yesterday, tomorrow, here, there*: *We must come to school **tomorrow**.*',
        'Watch out: the adverb of *good* is **well**: *He speaks English **well***. *fast, hard, early* stay the same: *She works **hard***. (*lately* is not the adverb of *late*; it means *recently*.)',
        'A **conjunction** joins words or sentences: *and, but, or, because, although, when, while, if*: *Suleman works badly **but** he plays games very well.*',
        'A **preposition** is a short word before a noun or a pronoun. It shows **place, time, direction** or another link: *The telephone is **in** the hall.* *The soldier fought **with** great bravery.* The next lesson (6.3) teaches them step by step.',
        'An **interjection** shows a sudden feeling. It usually has **!** after it: *Oh! Wow! Ouch! Hurrah! Whew!*: ***Hurrah!** We have won the match.*',
    ]
    c['examples'] = [dict(text='He drives carefully.', ok=True), dict(text='She sings beautiful.', ok=False, fix='She sings beautifully.'),
                     dict(text='He speaks English very good.', ok=False, fix='He speaks English very well.'),
                     dict(text='Ouch! That hurts.', ok=True)]
    c['pattern'] = 'adverb = how / when / where  ·  conjunction = joins  ·  preposition + noun  ·  interjection + !'
    w = b.card('eng9-u6-l6-2-wk1')
    w['title'] = 'Step by step: adjective or adverb?'
    w['steps'] = [dict(text=s) for s in [
        '**Step 1: Find the verb.** *sings* is the action.',
        '**Step 2: Which word tells how she sings?** *beautiful*. But *beautiful* is an adjective: it describes a noun (*a beautiful song*).',
        '**Step 3: A word that tells how an action is done must be an adverb** → adjective + -ly → **beautifully**.',
        '**Check:** *She sings beautifully.* ✔ *She has a beautiful voice.* ✔ (adjective + noun)']]
    t = b.card('eng9-u6-c04')
    t['title'] = 'Common mistakes with these word types'
    t['head'] = ['Wrong', 'Right', 'Why']
    t['rows'] = [
        ['She sings beautiful.', 'She sings beautifully.', 'It tells how she sings → adverb (-ly).'],
        ['He speaks English very good.', 'He speaks English very well.', 'The adverb of good is well.'],
        ['Although I was tired, but I finished.', 'Although I was tired, I finished.', 'Use only one joining word.'],
        ['She is good in maths.', 'She is good at maths.', 'good goes with at.'],
        ['Ouch, that hurts.', 'Ouch! That hurts.', 'An interjection takes !'],
    ]
    # the subject–verb agreement cards belong to lesson 6.1
    for cid in ('eng9-u6-c05', 'eng9-u6-l6-2-r3x1', 'eng9-u6-l6-2-r3x2', 'eng9-u6-l6-2-r3x3'):
        b.move_card(cid, 'eng9-u6-l6-1')
    b.put_cards(L2, [
        text('eng9-u6-l6-2-m1', 'Memory tip: ask what job the word does', [
            'Names a person, place or thing → **noun**. Describes a noun → **adjective**. Tells how / when / where → **adverb**.',
            'Joins two words or sentences → **conjunction**. Short word before a noun that shows place, time or direction → **preposition**. A sudden feeling with ! → **interjection**.',
        ], page=P, kind='mnemonic'),
    ], after='eng9-u6-c04')
    return u


def lesson_63(b):
    u = b.unit('eng9-u6')
    b.put_lesson('eng9-u6', dict(id=L3, number='6.3', title='Prepositions: place, time, movement and partner words', pages=[P, 115], cards=[]), after=L2)
    cards = [
        grammar(L3 + '-c1', 'What is a preposition?', [
            'A **preposition** is a short word that comes **before a noun or a pronoun** and shows how it is linked to the rest of the sentence: *The telephone is **in** the hall.* (where?) *We arrived **at** 6 o\'clock.* (when?) *She walked **to** the market.* (which direction?)',
            'Common prepositions: *at, in, on, to, from, for, of, with, by, about, after, before, under, over, above, below, between, among, across, along, through, behind, near, off, up*.',
            '**Step 1:** Ask what the preposition must show: **place**, **time**, **movement**, or is it the **partner** of another word (*good **at**, wait **for***)?',
            '**Step 2:** After a preposition use a **noun**, an **object pronoun** (*me, him, her, us, them*) or a verb + **-ing**: *with **me***, *before **leaving***.',
            '**Step 3:** Some verbs need **no** preposition: *discuss the plan, enter the room, reach Keren, go home*.',
        ], [
            ('The soldier fought with great bravery.', True),
            ('She came with I.', False, 'She came with me.'),
            ('He left without say goodbye.', False, 'He left without saying goodbye.'),
            ('We discussed about the problem.', False, 'We discussed the problem.'),
        ], pattern='preposition + noun / me, him, her… / verb-ing', page=P),
        table(L3 + '-c2', 'Place: at, on, in', ['Preposition', 'Use it for', 'Examples'], [
            ['**at**', 'a **point**: a place where something happens, a building as a meeting place, an address', 'at the bus stop, at the door, at school, at home, at the market, at 12 Harnet Avenue'],
            ['**on**', 'a **surface** or a **line**: tables, walls, floors, streets, rivers; buses, trains, planes', 'on the table, on the wall, on Harnet Avenue, on a chair, on the bus, on page 12'],
            ['**in**', '**inside** a space or an **area**: rooms, boxes, towns, countries, the sea; cars and taxis', 'in the classroom, in the hall, in Keren, in Eritrea, in the Red Sea, in a taxi'],
            ['**arrive**', 'arrive **in** a town or country; arrive **at** a building or place. Never *arrive to*.', 'We arrived in Barentu. We arrived at the station.'],
        ], page=P),
        table(L3 + '-c3', 'Place: other prepositions', ['Preposition', 'Meaning', 'Example'], [
            ['under / below', 'lower than something', 'The bag is **under** the desk. Write your name **below** the title.'],
            ['over / above', 'higher than something', 'There is a clock **above** the board. The plane flew **over** Asmara.'],
            ['between', 'in the middle of **two** people or things', 'Sit **between** Selam and Ruth.'],
            ['among', 'in a **group** of more than two', 'She was **among** the best students in her class.'],
            ['behind / in front of', 'at the back of / facing the front of', 'The garden is **behind** the house. Wait **in front of** the school.'],
            ['next to / beside', 'very close, at the side of', 'Sit **next to** (beside) me.'],
            ['near', 'not far from', 'Our house is **near** the market.'],
            ['opposite', 'on the other side, facing it', 'The bank is **opposite** the post office.'],
        ], page=P),
        table(L3 + '-c4', 'Time: at, on, in (and no preposition)', ['Preposition', 'Use it for', 'Examples'], [
            ['**at**', 'clock times and short moments', 'at 6 o\'clock, at noon, at night, at midnight, at sunrise, at the moment'],
            ['**on**', 'days and dates', 'on Monday, on 24 May, on Independence Day, on my birthday, on Monday morning'],
            ['**in**', 'longer times: parts of the day, months, seasons, years, centuries', 'in the morning, in the evening, in May, in the rainy season, in 1991, in the 20th century'],
            ['**no preposition**', 'before today, tomorrow, yesterday, tonight, and before this / next / last / every', 'See you **next Monday**. We met **last year**. I read **every evening**.'],
        ], page=P),
        text(L3 + '-c5', 'At, on, in: from small to big', [
            '**TIME:** **at** 7 o\'clock (a point) → **on** Monday (a day) → **in** May (a month) → **in** 2026 (a year).',
            '**PLACE:** **at** the door (a point) → **on** the wall (a surface) → **in** the room (a space) → **in** Asmara (an area).',
            '**AT** = a point. **ON** = a surface, a line or a day. **IN** = inside, or a longer time.',
        ], page=P, kind='mnemonic'),
        table(L3 + '-c6', 'Movement and direction', ['Preposition', 'Meaning', 'Example'], [
            ['to', 'towards a place (where you go)', 'We go **to** school by bus. (But: go **home** – no *to*.)'],
            ['from … to', 'the start and the end of a journey', 'The bus goes **from** Asmara **to** Keren.'],
            ['into', 'from outside to inside', 'He walked **into** the classroom.'],
            ['out of', 'from inside to outside', 'She looked **out of** the window.'],
            ['onto / off', 'moving onto a surface / away from it', 'The cat jumped **onto** the table. He fell **off** his bicycle.'],
            ['across', 'from one side to the other side of a flat thing', 'We walked **across** the bridge.'],
            ['through', 'in at one end and out at the other', 'The train went **through** the tunnel.'],
            ['along', 'following a line', 'We walked **along** the beach in Massawa.'],
            ['up / down', 'to a higher / lower place', 'They climbed **up** the hill and ran **down** the steps.'],
            ['towards / for', 'in the direction of', 'The ship **made for** (moved towards) the harbour.'],
            ['past', 'going by something', 'Walk **past** the bank and turn left.'],
        ], page=P),
        table(L3 + '-c7', 'Words that are easy to mix up', ['Pair', 'How they are different', 'Examples'], [
            ['**by** / **until**', '**by** = not later than (a deadline; the action happens once before it). **until** = all the time up to then (the action goes on).', 'Hand in your homework **by** Friday. / I will wait **until** 5 o\'clock.'],
            ['**for** / **since**', '**for** + a length of time. **since** + the starting point. Both often go with *have/has + 3rd form*.', 'I have lived here **for** three years. / I have lived here **since** 2023.'],
            ['**during** / **while**', '**during** + a noun. **while** + subject + verb.', '**during** the lesson / **while** the teacher was talking'],
            ['**in** / **into**', '**in** = where something is (no movement). **into** = moving from outside to inside.', 'She is **in** the room. / She ran **into** the room.'],
            ['**between** / **among**', '**between** two (or clearly separate) people or things. **among** a group.', '**between** Keren and Agordat / **among** the trees'],
            ['**on time** / **in time**', '**on time** = at the planned time, not late. **in time** = early enough to do something.', 'The bus left **on time**. / We arrived **in time** to see the start.'],
            ['**at the end** / **in the end**', '**at the end of** + something. **in the end** = finally, after a long time.', '**at the end of** the film / **In the end**, he came to the house.'],
            ['**beside** / **besides**', '**beside** = next to. **besides** = as well as.', 'Sit **beside** me. / **Besides** English, she speaks Arabic.'],
        ], page=P),
        table(L3 + '-c8', 'Partner prepositions: words that always take the same preposition', ['Word', 'Preposition', 'Example'], [
            ['live / a town; poverty', 'in', 'Abraham lived **in** Akurdet **in** great poverty.'],
            ['the story / lack / as a result', 'of', 'the story **of** her life; lack **of** food; as a result **of** the rain'],
            ['in need', 'of', 'He was **in need of** money.'],
            ['pay / wait / ask / look', 'for', 'pay **for** food; wait **for** the bus; ask **for** money; look **for** my key'],
            ['buy (something) / a price', 'for', 'I bought this hat **for** fifty-five Nakfa.'],
            ['thanks / owe / send / listen / belong', 'to', 'thanks **to** the doctor; owe your life **to** me; send the bill **to** him; listen **to** the radio; belong **to** me'],
            ['grateful', 'to (a person) for (a thing)', 'I am grateful **to** you **for** your help.'],
            ['look after', 'after', 'My grandmother **looks after** the baby. (= takes care of)'],
            ['good / bad / at times', 'at', 'good **at** maths; **at** times (= sometimes)'],
            ['afraid / proud / tired', 'of', 'afraid **of** snakes; proud **of** my country; tired **of** waiting'],
            ['interested / different', 'in / from', 'interested **in** football; different **from** her sister'],
            ['angry / agree', 'with (a person)', 'angry **with** Dawit; I agree **with** you.'],
            ['depend / married / laugh', 'on / to / at', 'depend **on** the rain; married **to** Senait; laugh **at** a joke'],
        ], page=PX),
        worked(L3 + '-c9', 'Step by step: textbook exercise (Lesson 6.5 B), sentences 1–8',
               'Put in the correct prepositions. 1. Abraham lived ___ Akurdet ___ great poverty. 2. Zeineb wrote the story ___ her life. '
               '3. Jimie was still ___ need ___ money, and he could not even pay ___ his food. 4. ___ times, as a result ___ his lack ___ food he became ill. '
               '5. He got better, thanks ___ the doctor who looked ___ him. 6. The doctor sent a report ___ his visits. '
               '7. He waited ___ several weeks and then sent the bill ___ him again. 8. ___ the end, he came ___ the house and asked ___ his money.', [
                   '**Step 1: Place or state.** 1. lived **in** Akurdet (a town → in) **in** great poverty (a state → in).',
                   '**Step 2: Partner words with "of".** 2. the story **of** her life. 3. **in** need **of** money. 4. as a result **of**, lack **of** food.',
                   '**Step 3: Partner words with "for".** 3. pay **for** his food. 7. waited **for** several weeks (a length of time). 8. asked **for** his money.',
                   '**Step 4: Fixed phrases.** 4. **At** times (= sometimes). 8. **In** the end (= finally).',
                   '**Step 5: "to" for the person who receives, or the place you go.** 5. thanks **to** the doctor. 7. sent the bill **to** him. 8. came **to** the house.',
                   '**Step 6: Other partners.** 5. looked **after** him (= took care of him). 6. a report **on** his visits (*of* is also possible).',
               ], '1. in, in  2. of  3. in, of, for  4. At, of, of  5. to, after  6. on (of)  7. for, to  8. In, to, for', page=PX),
        worked(L3 + '-c10', 'Step by step: textbook exercise (Lesson 6.5 B), sentences 9–15',
               '9. I expected gratitude ___ you, as you owe your life ___ me. 10. I am not ungrateful ___ you ___ what you did, so I will give my life ___ you. '
               '11. He is sitting ___ a chair and looking ___ ___ the window. 12. The ship made ___ the harbour. 13. We arrived ___ Barentu ___ exactly 6 o\'clock. '
               '14. I bought this hat ___ fifty-five Nakfa. 15. I have been waiting ___ over an hour and a half.', [
                   '**Step 1: Who gives and who receives?** 9. gratitude **from** you (you give it); owe your life **to** me (I receive it). 10. (un)grateful **to** a person **for** a thing; give my life **for** you (= to help you).',
                   '**Step 2: Place and movement.** 11. sitting **on** a chair (a surface); looking **out of** the window (from inside to outside). 12. made **for** the harbour (= moved towards it).',
                   '**Step 3: Place and time together.** 13. arrived **in** Barentu (a town → in) **at** exactly 6 o\'clock (a clock time → at).',
                   '**Step 4: Price.** 14. bought **for** fifty-five Nakfa.',
                   '**Step 5: Length of time.** 15. *over an hour and a half* is a length → **for** (not *since*).',
               ], '9. from, to  10. to, for, for  11. on, out of  12. for  13. in, at  14. for  15. for', page=PX),
        table(L3 + '-c11', 'Common mistakes', ['Wrong', 'Right', 'Why'], [
            ['I was born in 24 May.', 'I was born on 24 May.', 'A date → on.'],
            ['See you on next Monday.', 'See you next Monday.', 'No preposition before next / last / this / every.'],
            ['We arrived to Barentu at the evening.', 'We arrived in Barentu in the evening.', 'arrive in + town; in the evening.'],
            ['I am waiting you.', 'I am waiting for you.', 'wait for.'],
            ['Listen me, please.', 'Listen to me, please.', 'listen to.'],
            ['We discussed about the problem.', 'We discussed the problem.', 'discuss has no preposition.'],
            ['He entered into the room.', 'He entered the room. / He went into the room.', 'enter has no preposition.'],
            ['I have lived here since three years.', 'I have lived here for three years.', 'A length of time → for.'],
            ['During I was eating, the phone rang.', 'While I was eating, the phone rang.', 'Subject + verb → while.'],
            ['Finish the work until Friday.', 'Finish the work by Friday.', 'A deadline → by.'],
            ['She went to home.', 'She went home.', 'No to before home.'],
            ['He is married with Senait.', 'He is married to Senait.', 'married to.'],
        ], page=P),
        check(L3 + '-c12', 'We arrived ____ Barentu ____ exactly 6 o\'clock.', {'A': 'at / in', 'B': 'in / at', 'C': 'to / on', 'D': 'on / at'}, 'B', [
            '**Step 1:** Barentu is a town → arrive **in**.', '**Step 2:** 6 o\'clock is a clock time → **at**.',
            '**Step 3:** *arrive to* is never correct; *on* is for days and dates.', f'**Tip:** {PREP_TIP}'], page=PX),
        check(L3 + '-c13', 'Please hand in your essays ____ Friday. Late essays will not be marked.', {'A': 'until', 'B': 'by', 'C': 'since', 'D': 'during'}, 'B', [
            '**Step 1:** Friday is the **last** day: a deadline.', '**Step 2:** Deadline (not later than) → **by**.',
            '**Step 3:** *until* would mean you keep handing in the essay all the time up to Friday – wrong meaning.', f'**Tip:** {PREP_TIP}'], page=P),
        check(L3 + '-c14', 'Nobody spoke ____ the meeting.', {'A': 'while', 'B': 'during', 'C': 'for', 'D': 'since'}, 'B', [
            '**Step 1:** *the meeting* is a noun, not subject + verb.', '**Step 2:** during + noun → **during** the meeting.',
            '**Step 3:** *while* needs subject + verb: *while we were meeting*.', f'**Tip:** {PREP_TIP}'], page=P),
        check(L3 + '-c15', 'He walked ____ the classroom and sat down at his desk.', {'A': 'in', 'B': 'into', 'C': 'at', 'D': 'on'}, 'B', [
            '**Step 1:** He moved from **outside** to **inside**.', '**Step 2:** Movement to the inside → **into**.',
            '**Step 3:** *walked in the classroom* means he walked around inside it – not the meaning here.', f'**Tip:** {PREP_TIP}'], page=P),
        check(L3 + '-c16', 'I bought this hat ____ fifty-five Nakfa.', {'A': 'with', 'B': 'by', 'C': 'for', 'D': 'in'}, 'C', [
            '**Step 1:** fifty-five Nakfa is a **price**.', '**Step 2:** buy something **for** a price.',
            '**Step 3:** Same pattern: *sell it for, pay for*.', f'**Tip:** {PREP_TIP_WORDS}'], page=PX),
        check(L3 + '-c17', 'My grandmother looks ____ the children when my parents are at work.', {'A': 'for', 'B': 'after', 'C': 'at', 'D': 'to'}, 'B', [
            '**Step 1:** The meaning is *takes care of*.', '**Step 2:** take care of = **look after**.',
            '**Step 3:** *look for* = try to find; *look at* = turn your eyes to.', f'**Tip:** {PREP_TIP_WORDS}'], page=PX),
        check(L3 + '-c18', 'I have known Aster ____ we were in Grade 5.', {'A': 'for', 'B': 'since', 'C': 'from', 'D': 'during'}, 'B', [
            '**Step 1:** *we were in Grade 5* is the **starting point**.', '**Step 2:** Starting point → **since**.',
            '**Step 3:** *for* needs a length: *for four years*.', f'**Tip:** {PREP_TIP}'], page=P),
    ]
    b.put_cards(L3, cards)
    b.move_card('eng9-u6-c06', L3)   # unit summary at the end of the unit
    s = b.card('eng9-u6-c06')
    s['body'] = ['Singular subjects take singular verbs and plural subjects plural verbs; with either/or and neither/nor the verb agrees with the nearer subject. '
                 'Adverbs tell how, when or where (often -ly); conjunctions join; interjections show feelings with !. '
                 'Prepositions come before a noun or pronoun: at a point / on a surface or day / in a space or longer time; '
                 'for + length, since + start, by = deadline, until = up to then, during + noun, while + subject + verb; '
                 'and many words have a partner preposition (good at, wait for, look after).']
    return u


def _sim(*pairs):
    return list(pairs)


def questions(b):
    T, W = PREP_TIP, PREP_TIP_WORDS
    qs = [
        mcq('eng9-u6-pq01', 'Our English lesson starts ____ 8 o\'clock.', {'A': 'in', 'B': 'on', 'C': 'at', 'D': 'by'}, 'C',
            ['8 o\'clock is a clock time.', 'Clock time → **at**.'], T, _sim(('Complete: "The shop closes ____ noon."', 'at'), ('Complete: "I go to bed ____ 10 o\'clock."', 'at')), page=P),
        mcq('eng9-u6-pq02', 'Eritrea became independent ____ 1991.', {'A': 'on', 'B': 'at', 'C': 'in', 'D': 'since'}, 'C',
            ['1991 is a year.', 'Years, months and seasons → **in**.', '*since* needs a perfect tense: *has been independent since 1991*.'], T,
            _sim(('Complete: "I was born ____ 2011."', 'in'), ('Complete: "It often rains ____ July."', 'in')), page=P),
        mcq('eng9-u6-pq03', 'We celebrate Independence Day ____ 24 May.', {'A': 'in', 'B': 'at', 'C': 'on', 'D': 'by'}, 'C',
            ['24 May is a date.', 'Days and dates → **on**.', '*in May* (month only) but *on 24 May* (a date).'], T,
            _sim(('Complete: "My birthday is ____ 3 June."', 'on'), ('Complete: "We have no school ____ Sunday."', 'on')), page=P),
        mcq('eng9-u6-pq04', 'My mother likes to drink coffee ____ the morning.', {'A': 'at', 'B': 'on', 'C': 'in', 'D': 'by'}, 'C',
            ['*the morning* is a part of the day.', 'Parts of the day → **in** the morning / afternoon / evening (but **at** night).'], T,
            _sim(('Complete: "We study ____ the evening."', 'in'), ('Complete: "Owls hunt ____ night."', 'at')), page=P),
        mcq('eng9-u6-pq05', 'The children are ____ the classroom, and the teacher is waiting ____ the door.', {'A': 'in / at', 'B': 'at / in', 'C': 'on / in', 'D': 'into / on'}, 'A',
            ['The children are **inside** a room → **in**.', 'The teacher stands at a **point** → **at** the door.', '*into* shows movement; nobody is moving here.'], T,
            _sim(('Complete: "The picture is ____ the wall."', 'on'), ('Complete: "Meet me ____ the bus stop."', 'at')), page=P),
        mcq('eng9-u6-pq06', 'The bus goes ____ Asmara ____ Keren.', {'A': 'from / to', 'B': 'at / in', 'C': 'since / until', 'D': 'from / at'}, 'A',
            ['A journey has a start and an end.', 'Start → **from**, end → **to**.', '*since / until* are for time, not places.'], T,
            _sim(('Complete: "The train runs ____ Massawa ____ Asmara."', 'from … to'),), page=P),
        mcq('eng9-u6-pq07', 'We walked ____ the bridge to the other side of the river.', {'A': 'across', 'B': 'through', 'C': 'along', 'D': 'into'}, 'A',
            ['We went from one side to the **other side**.', 'From side to side of a flat thing → **across**.', '*through* is for going inside something (a tunnel, a forest); *along* follows a line.'], T,
            _sim(('Complete: "Look both ways before you walk ____ the road."', 'across'), ('Complete: "We walked ____ the beach."', 'along')), page=P),
        mcq('eng9-u6-pq08', 'The train went ____ the tunnel.', {'A': 'across', 'B': 'through', 'C': 'over', 'D': 'on'}, 'B',
            ['A tunnel has an inside: the train goes in at one end and out at the other.', 'In and out → **through**.'], T,
            _sim(('Complete: "The road goes ____ the forest."', 'through'),), page=P),
        mcq('eng9-u6-pq09', 'I have lived in Dekemhare ____ 2018.', {'A': 'for', 'B': 'since', 'C': 'during', 'D': 'from'}, 'B',
            ['2018 is the **starting point**.', 'Starting point + have/has + 3rd form → **since**.'], T,
            _sim(('Complete: "She has worked here ____ Monday."', 'since'), ('Complete: "She has worked here ____ three days."', 'for')), page=P),
        mcq('eng9-u6-pq10', 'She has studied English ____ six years.', {'A': 'since', 'B': 'for', 'C': 'during', 'D': 'ago'}, 'B',
            ['*six years* is a **length** of time.', 'Length of time → **for**.', '*ago* comes after the time and goes with the past simple: *six years ago*.'], T,
            _sim(('Complete: "We waited ____ two hours."', 'for'), ('Complete: "We have waited ____ 2 o\'clock."', 'since')), page=P),
        mcq('eng9-u6-pq11', 'Please wait here ____ I come back.', {'A': 'by', 'B': 'until', 'C': 'during', 'D': 'since'}, 'B',
            ['The waiting goes on **all the time** up to the moment I come back.', 'Action that continues up to a time → **until**.', '*by* is for a deadline (one action before a time).'], T,
            _sim(('Complete: "The library is open ____ 6 pm."', 'until'), ('Complete: "Return the book ____ Monday."', 'by')), page=P),
        mcq('eng9-u6-pq12', 'The phone rang ____ I was having dinner.', {'A': 'during', 'B': 'while', 'C': 'for', 'D': 'at'}, 'B',
            ['After the gap we have subject + verb: *I was having*.', 'Subject + verb → **while**.', '*during* needs a noun: *during dinner*.'], T,
            _sim(('Complete: "The phone rang ____ dinner."', 'during'), ('Complete: "I fell asleep ____ I was reading."', 'while')), page=P),
        mcq('eng9-u6-pq13', 'Zeineb wrote the story ____ her life.', {'A': 'for', 'B': 'of', 'C': 'on', 'D': 'with'}, 'B',
            ['The story **belongs to** her life: it tells about her life.', 'the story **of** …'], W,
            _sim(('Complete: "He told us the history ____ Adulis."', 'of'),), page=PX),
        mcq('eng9-u6-pq14', 'He got better, thanks ____ the doctor who looked ____ him.', {'A': 'to / after', 'B': 'for / at', 'C': 'of / for', 'D': 'to / for'}, 'A',
            ['**thanks to** = because of the help of.', '**look after** = take care of.', '*look for* would mean "try to find".'], W,
            _sim(('Complete: "Who looks ____ your little brother?"', 'after'), ('Complete: "We won, thanks ____ our goalkeeper."', 'to')), page=PX),
        mcq('eng9-u6-pq15', 'Are you afraid ____ snakes?', {'A': 'of', 'B': 'from', 'C': 'with', 'D': 'about'}, 'A',
            ['*afraid* has a partner preposition: **afraid of**.', 'Do not translate word by word: ✗ *afraid from*.'], W,
            _sim(('Complete: "She is proud ____ her son."', 'of'), ('Complete: "I am tired ____ waiting."', 'of')), page=P),
        mcq('eng9-u6-pq16', 'Senait is very good ____ mathematics.', {'A': 'in', 'B': 'on', 'C': 'at', 'D': 'with'}, 'C',
            ['**good at / bad at** + a subject or an activity.', 'So: *good **at** mathematics*.'], W,
            _sim(('Complete: "He is bad ____ football."', 'at'), ('Complete: "She is good ____ drawing."', 'at')), page=P),
        fill('eng9-u6-pq17', 'I am not interested ____ football.', 'in', ['in', 'on', 'at', 'for'],
             ['*interested* always takes **in**.', 'After the preposition use a noun or -ing: *interested in **playing***.'], W,
             _sim(('Complete: "Are you interested ____ science?"', 'in'),), page=P),
        fill('eng9-u6-pq18', 'I saved you from the river. You owe your life ____ me.', 'to', ['to', 'for', 'at', 'from'],
             ['You **owe** something **to** the person who gave it.', 'So: owe your life **to** me.'], W,
             _sim(('Complete: "I owe 100 Nakfa ____ my brother."', 'to'),), page=PX),
        fill('eng9-u6-pq19', 'He looked ____ the window and saw the rain.', 'out of', ['out of', 'out from', 'off', 'into'],
             ['His eyes went from **inside** the room to the **outside**.', 'From inside to outside → **out of**.'], T,
             _sim(('Complete: "She ran ____ the burning house."', 'out of'), ('Complete: "She ran ____ the house to get her coat." (outside → inside)', 'into')), page=PX),
        short('eng9-u6-pq20', 'Correct the errors: "We arrived to Massawa on the evening."', 'We arrived in Massawa in the evening.',
              ['Massawa is a town → arrive **in** (never *arrive to*).', 'A part of the day → **in** the evening.'], T,
              _sim(('Correct: "They arrived to the station at the morning."', 'They arrived at the station in the morning.'),), page=P,
              accept=['We arrived in Massawa in the evening', 'We arrived at Massawa in the evening.']),
        short('eng9-u6-pq21', 'Correct the errors: "I am waiting you since two hours."', 'I have been waiting for you for two hours.',
              ['**wait for** someone.', '*two hours* is a length → **for**, not *since*.', 'From the past until now → *have been waiting*.'], T,
              _sim(('Correct: "She is living here since five years."', 'She has been living here for five years.'),), page=P,
              accept=['I have been waiting for you for two hours', "I've been waiting for you for two hours."]),
        short('eng9-u6-pq22', 'Correct the error: "During I was in Keren, I visited my aunt."', 'While I was in Keren, I visited my aunt.',
              ['After the gap we have subject + verb: *I was*.', 'Subject + verb → **while** (or use a noun: *During my stay in Keren, …*).'], T,
              _sim(('Correct: "While the holidays, we went to Massawa."', 'During the holidays, we went to Massawa.'),), page=P,
              accept=['While I was in Keren, I visited my aunt', 'During my stay in Keren, I visited my aunt.']),
        tf('eng9-u6-pq23', 'True or false: "See you on next Friday" is correct English.', False,
           ['False. There is no preposition before *next, last, this, every*.', 'Correct: *See you next Friday.* (But: *See you **on** Friday.*)'], T,
           _sim(('Correct: "We went there in last year."', 'We went there last year.'),), page=P),
        tf('eng9-u6-pq24', 'True or false: "Finish it by Friday" and "Finish it until Friday" mean the same thing.', False,
           ['False. **by Friday** = not later than Friday (a deadline).', '**until** means an action that goes on all the time up to then, so *finish it until Friday* is wrong.'], T,
           _sim(('Choose: "The shop is open (by / until) 8 pm."', 'until'), ('Choose: "Pay the fees (by / until) the end of the month."', 'by')), page=P),
        mcq('eng9-u6-pq25', 'Which sentence has a mistake?', {'A': 'She is in the kitchen.', 'B': 'We discussed about the plan.', 'C': 'He jumped into the water.', 'D': 'They live on Harnet Avenue.'}, 'B',
            ['*discuss* needs no preposition: *discuss the plan*.', 'A (inside a room), C (movement inside) and D (a street → on) are correct.'], W,
            _sim(('Correct: "He entered into the room."', 'He entered the room.'),), page=P),
        short('eng9-u6-pq26', 'Put in the prepositions: "Jimie was still ___ need ___ money, and he could not even pay ___ his food."', 'in, of, for',
              ['**in need of** = needing something.', '**pay for** the thing you buy.'], W,
              _sim(('Complete: "The school is ___ need ___ more books."', 'in, of'), ('Complete: "Who paid ___ the tickets?"', 'for')), page=PX,
              accept=['in / of / for', 'in of for', 'in need of, pay for']),
    ]
    b.put_questions('eng9-u6', qs)
    return len(qs)


def unit_extras(b):
    u = b.unit('eng9-u6')
    u['intro'] = ('Grammar: subject–verb agreement (including neither/nor, either/or, together with) and the other parts of speech: '
                  'adverbs, conjunctions, interjections, and prepositions of place, time and movement with their partner words.')
    b.put_glossary('eng9-u6', [('Preposition', 'A short word before a noun or pronoun that shows place, time, direction or another link: in, on, at, to, for, since, by, with.')])
    if not any('**AT** a point' in t['text'] for t in u['tips']):
        u['tips'].append(dict(text='**AT** a point, **ON** a surface or a day, **IN** a space or a longer time.', page=P, src='notes'))
    if not any(g['id'] == 'eng9-u6-g2' for g in u['games']):
        u['games'].append(dict(id='eng9-u6-g2', type='match', title='Match the preposition to its use', src='notes', lesson=L3, pairs=[
            dict(a='at', b='7 o\'clock / night / the bus stop'), dict(a='on', b='Monday / 24 May / the table'),
            dict(a='in', b='May / 1991 / Keren / the morning'), dict(a='since', b='2019 (a starting point)'),
            dict(a='for', b='three years (a length of time)'), dict(a='by', b='Friday (not later than)')]))
    m = u['unitMap']
    nodes = {n['id']: n for n in m['nodes']}
    nodes['unit']['cards'] = ['eng9-u6-c01', 'eng9-u6-c03', L3 + '-c1']
    nodes['l6_1']['cards'] = ['eng9-u6-c01', 'eng9-u6-c02', 'eng9-u6-c05']
    nodes['l6_2']['cards'] = ['eng9-u6-c03', 'eng9-u6-c04', 'eng9-u6-l6-2-m1']
    if 'l6_3' not in nodes:
        m['nodes'].append(dict(id='l6_3', label='Prepositions', kind='topic', lesson=L3, cards=[L3 + '-c1', L3 + '-c2', L3 + '-c4', L3 + '-c7', L3 + '-c8']))
        m['edges'].append({'from': m['root'], 'to': 'l6_3', 'label': 'includes'})


def apply(b):
    fix_lesson_62(b)
    lesson_63(b)
    n = questions(b)
    unit_extras(b)
    return n
