"""Grade 11, part B: Unit 8 follows Textbook Unit 8 (transitive / intransitive verbs, direct / indirect objects).
The old Unit 8 content (cohesive devices) moves, with all its ids, to a new Unit 25."""
import copy
from lib import grammar, table, text, worked, check, mcq, fill, tf, short, unitmap

TV_TIP = 'Ask "what?" or "whom?" straight after the verb. A noun that receives the action = object → transitive. Nothing, or only how/where/when → intransitive. An adjective describing the subject → linking verb + complement.'
OB_TIP = 'Person + thing → V + person + thing (gave me a pen) or V + thing + to/for + person (gave a pen to me). If the thing is "it/them", use the second pattern.'


def move_cohesion(b):
    units = b.d['units']
    if any(u['id'] == 'eng11-u25' for u in units):
        return
    old = b.unit('eng11-u8')
    new = copy.deepcopy(old)
    new['id'] = 'eng11-u25'
    new['number'] = 25
    new['title'] = 'Linking words & cohesive devices'
    new['intro'] = ('Linking words (cohesive devices) join ideas: addition, contrast, cause and purpose. Each one has its own grammar. '
                    '(This unit was Unit 8 before; Unit 8 now follows Textbook Unit 8.)')
    for i, l in enumerate(new['lessons']):
        l['number'] = f'25.{i + 1}'
    for n in new['unitMap']['nodes']:
        if n['id'] == 'unit':
            n['label'] = 'Linking words & cohesive devices'
    units.append(new)


def unit8(b):
    u = b.unit('eng11-u8')
    if u['lessons'] and u['lessons'][0]['id'] == 'eng11-u8-l8-tv':
        pass
    tv_p, ob_p = 199, 202  # Textbook Unit 8: Lesson 8.4 (transitive and intransitive verbs), Lesson 8.8 (direct and indirect objects)
    u['title'] = 'Transitive & intransitive verbs; direct & indirect objects'
    u['pages'] = [191, 212]
    u['intro_page'] = 191
    u['intro'] = ('Textbook Unit 8 (Accidents) grammar: transitive verbs (with an object) and intransitive verbs (without an object), '
                  'linking verbs with a complement, and verbs with two objects (direct and indirect).')
    u['lessons'] = [dict(id='eng11-u8-l8-tv', number='8.1', title='Transitive and intransitive verbs', pages=[tv_p, tv_p], cards=[]),
                    dict(id='eng11-u8-l8-obj', number='8.2', title='Direct and indirect objects', pages=[ob_p, ob_p], cards=[])]
    b.put_cards('eng11-u8-l8-tv', [
        grammar('eng11-u8-tv-c1', 'Transitive and intransitive verbs', [
            'A **transitive verb** needs an **object**: a person or thing that receives the action. Ask *what?* or *whom?* after the verb: *He raised **his hands**.* (raised what? → his hands) *She told **a story**.*',
            'An **intransitive verb** has **no object**. The sentence is complete without one: *The dog **barks**. The sun **rises** in the east.* (*in the east* tells us where; it is not an object.)',
            'Many verbs can be **both**: *She **sings**.* (intransitive) / *She **sings** a song.* (transitive). *The door **opened**.* / *He **opened** the door.*',
            '**Linking verbs** (*be, become, seem, look, go* = become, *fall* asleep, *prove, keep*) have no object, but they need a **complement** – a word that describes the subject: *The old man **went mad**. The child **has fallen asleep**. The information **proved false**.* (The textbook calls them *verbs of incomplete predication*.)',
            'Only transitive verbs can be **passive**: *He told a story.* → *A story was told.* ✗ *An accident was happened.*',
            'Watch these pairs: **raise** (+ object: *raise your hand*) / **rise** (no object: *prices rise*); **lay** (+ object: *lay the table*) / **lie** (no object: *lie down*). **arrive** has no object: *arrive **at** school* (✗ *arrive school*). **discuss** has an object: *discuss the plan* (✗ *discuss about*).',
        ], [
            ('He raised his hands.', True),
            ('The dog barks every night.', True),
            ('We discussed about the accident.', False, 'We discussed the accident.'),
            ('She laid down on the bed.', False, 'She lay down on the bed.'),
            ('They arrived the station late.', False, 'They arrived at the station late.'),
        ], pattern='Transitive: S + V + O  ·  Intransitive: S + V (+ where/when/how)  ·  Linking: S + V + complement', page=tv_p),
        table('eng11-u8-tv-c2', 'Transitive, intransitive or both?', ['Verbs', 'Type', 'Example'], [
            ['raise, tell, make, see, bring, buy, discuss, need, find', 'transitive (needs an object)', 'He **told** a story. We **discussed** the plan.'],
            ['rise, bark, arrive, sleep, die, happen, come, go, lie, wait', 'intransitive (no object)', 'The sun **rises**. An accident **happened**.'],
            ['open, sing, read, write, eat, drive, break, start, stop', 'both', 'She **is reading**. / She **is reading** a novel.'],
            ['be, become, seem, look, feel, go (= become), fall (asleep), prove, keep', 'linking (needs a complement)', 'He **went** mad. The tea **is** hot.'],
        ], page=tv_p),
        worked('eng11-u8-tv-c3', 'Step by step: is the verb transitive or intransitive?',
               'Decide for each verb: (a) The children laughed loudly. (b) The children found a wallet. (c) The baby fell asleep. (d) We waited for the bus.', [
                   '**Step 1: Find the verb.** (a) laughed (b) found (c) fell (d) waited.',
                   '**Step 2: Ask "what?" or "whom?" straight after the verb.** (a) laughed what? – nothing (*loudly* tells how). (b) found what? – **a wallet**. (c) fell what? – nothing, but *asleep* describes the baby. (d) waited what? – nothing (*for the bus* is a phrase with a preposition).',
                   '**Step 3: Decide.** (a) intransitive. (b) transitive, object = *a wallet*. (c) linking verb, complement = *asleep*. (d) intransitive.',
                   '**Check with the passive:** *A wallet was found by the children.* ✔ (transitive) – ✗ *The children were laughed.* (intransitive)',
               ], '(a) intransitive (b) transitive – object: a wallet (c) linking – complement: asleep (d) intransitive', page=tv_p),
        table('eng11-u8-tv-c4', 'Textbook Lesson 8.4: answers', ['Sentence', 'Verb', 'Type', 'Object / complement'], [
            ['The sun rises in the east.', 'rises', 'intransitive', 'none'],
            ['The dog barks.', 'barks', 'intransitive', 'none'],
            ['He raised his hands.', 'raised', 'transitive', 'object: his hands'],
            ['The information proved false.', 'proved', 'intransitive (linking)', 'complement: false'],
            ['The child has fallen asleep.', 'has fallen', 'intransitive (linking)', 'complement: asleep'],
            ['The donkey kept braying.', 'kept', 'transitive', 'object: braying'],
            ['The tea is hot.', 'is', 'intransitive (linking)', 'complement: hot'],
            ['The results are out.', 'are', 'intransitive (linking)', 'complement: out'],
            ['She called again and again.', 'called', 'intransitive', 'none'],
            ['The old man went mad.', 'went', 'intransitive (linking)', 'complement: mad'],
            ['She waited for the bus.', 'waited', 'intransitive', 'none'],
            ['He told a story.', 'told', 'transitive', 'object: a story'],
            ['The sky is overcast.', 'is', 'intransitive (linking)', 'complement: overcast'],
            ['God called the light day.', 'called', 'transitive', 'object: the light (complement: day)'],
        ], page=tv_p),
        table('eng11-u8-tv-c5', 'Common mistakes', ['Wrong', 'Right', 'Why'], [
            ['We discussed about the plan.', 'We discussed the plan.', 'discuss is transitive: no preposition'],
            ['They arrived the airport.', 'They arrived at the airport.', 'arrive is intransitive: arrive at / in'],
            ['The prices have raised.', 'The prices have risen.', 'rise has no object; raise needs one'],
            ['She laid on the bed.', 'She lay on the bed.', 'lie (rest) has no object; lay needs one'],
            ['An accident was happened.', 'An accident happened.', 'intransitive verbs have no passive'],
            ['The driver injured.', 'The driver was injured. / The driver injured his leg.', 'injure is transitive: it needs an object, or use the passive'],
        ], page=tv_p),
        text('eng11-u8-tv-c6', 'Memory tip', ['**Transitive = TRANSfers the action** to an object (*kick **the ball***). **Intransitive = IN itself** – the action stays with the subject (*The baby **sleeps***).',
                                                'r**AI**se, l**AY**, s**E**t take an object; r**I**se, l**I**e, s**I**t do not.'], page=tv_p, kind='mnemonic'),
        check('eng11-u8-tv-c7', "In 'The injured man slept peacefully', the verb is ____.", {'A': 'transitive', 'B': 'intransitive', 'C': 'linking', 'D': 'passive'}, 'B', [
            '**Step 1:** Ask: slept what? – nothing.', '**Step 2:** *peacefully* only tells us how. There is no object → **intransitive**.',
            '**Step 3:** It is not linking: *peacefully* does not describe the man, it describes the sleeping.', f'**Tip:** {TV_TIP}'], page=tv_p),
        check('eng11-u8-tv-c8', 'Which sentence has a transitive verb?', {'A': 'The sun rises.', 'B': 'She smiled.', 'C': 'The driver stopped the car.', 'D': 'They arrived late.'}, 'C', [
            '**Step 1:** Look for an object after the verb.', '**Step 2:** In C: stopped what? → **the car** → transitive.',
            '**Step 3:** A, B and D have no object.', f'**Tip:** {TV_TIP}'], page=tv_p),
        check('eng11-u8-tv-c9', 'The number of road accidents has ____ this year.', {'A': 'raised', 'B': 'risen', 'C': 'rose', 'D': 'arose up'}, 'B', [
            '**Step 1:** There is no object after the gap → we need the intransitive verb **rise**.',
            '**Step 2:** After *has* use the past participle: rise – rose – **risen**.', '**Step 3:** *raised* needs an object (*raised the price*).', f'**Tip:** {TV_TIP}'], page=tv_p),
        check('eng11-u8-tv-c10', 'Which sentence can NOT be changed into the passive?', {'A': 'He wrote a letter.', 'B': 'They built a bridge.', 'C': 'The guests arrived early.', 'D': 'The police stopped the bus.'}, 'C', [
            '**Step 1:** Only verbs with an object can be passive.', '**Step 2:** *arrived* has no object (intransitive) → no passive.',
            '**Step 3:** A, B and D can be passive: *A letter was written. A bridge was built. The bus was stopped.*', f'**Tip:** {TV_TIP}'], page=tv_p),
    ])
    b.put_cards('eng11-u8-l8-obj', [
        grammar('eng11-u8-obj-c1', 'Direct and indirect objects', [
            'Some verbs (**give, send, show, tell, bring, buy, lend, pass, write, read, offer, teach, make, promise**) can have **two objects**: *She gave **me** **a book**.*',
            'The **direct object (DO)** is the **thing**: *a book* (ask *what?*). The **indirect object (IO)** is the **person** who receives it or gets the help: *me* (ask *to whom? / for whom?*).',
            'Two patterns, same meaning: (1) **V + IO + DO**: *He wrote **Dan** **a letter**.* (2) **V + DO + to/for + IO**: *He wrote **a letter** **to Dan**.*',
            '**to** = the person receives it (*give, send, show, tell, lend, pass, write, read, offer, teach, promise, sell*). **for** = we do it to help the person (*buy, make, get, cook, find, build, bring*): *I bought **her** a coffee.* = *I bought a coffee **for her**.*',
            'When the direct object is a **pronoun** (*it, them*), use pattern 2: *Give **it to me**.* (✗ *Give me it* in exams.)',
            'Some verbs use **only pattern 2**: **explain, describe, say, suggest, report, introduce**: *Explain **the rule to me*** (✗ *Explain me the rule*).',
        ], [
            ('They gave Simon a lot of presents.', True),
            ('They gave a lot of presents to Simon.', True),
            ('They gave a lot of presents Simon.', False, 'They gave a lot of presents to Simon.'),
            ('He wrote to Dan a letter.', False, 'He wrote Dan a letter. / He wrote a letter to Dan.'),
            ('Can you explain me this word?', False, 'Can you explain this word to me?'),
            ('Please pass me it.', False, 'Please pass it to me.'),
        ], pattern='V + IO (person) + DO (thing)  =  V + DO (thing) + to/for + IO (person)', page=ob_p),
        table('eng11-u8-obj-c2', 'Pattern 1 and pattern 2', ['Verb', 'V + IO + DO', 'V + DO + to/for + IO'], [
            ['give (to)', 'She gave me a pen.', 'She gave a pen to me.'],
            ['send (to)', 'Send your parents a card.', 'Send a card to your parents.'],
            ['show (to)', 'Show Helen the photo.', 'Show the photo to Helen.'],
            ['tell (to)', 'Tell us the truth.', 'Tell the truth to us.'],
            ['buy (for)', 'I bought my sister a dress.', 'I bought a dress for my sister.'],
            ['make (for)', 'Mother made us injera.', 'Mother made injera for us.'],
            ['explain (only pattern 2)', '✗ He explained us the lesson.', 'He explained the lesson to us.'],
            ['pronoun object', '✗ Give me it.', 'Give it to me.'],
        ], page=ob_p),
        table('eng11-u8-obj-c3', 'to or for?', ['to (the person receives it)', 'for (to help the person)'], [
            ['give, send, show, tell, lend', 'buy, make, get, cook'], ['pass, write, read, offer', 'find, build, keep, choose'],
            ['teach, promise, sell, owe', 'bring (also to), order, book'],
        ], page=ob_p),
        worked('eng11-u8-obj-c4', 'Step by step: Textbook Lesson 8.8 A – correct the sentences',
               'Correct: (1) He wrote to Dan a letter. (2) They gave a lot of presents Simon. (3) Can you show it me? (4) I have brought this book your sister.', [
                   '**Step 1: Find the person (IO) and the thing (DO).** (1) Dan / a letter (2) Simon / presents (3) me / it (4) your sister / this book.',
                   '**Step 2: Choose a pattern.** Person first → no preposition. Thing first → add *to* or *for* before the person.',
                   '(1) He wrote **Dan a letter**. / He wrote **a letter to Dan**.',
                   '(2) They gave **Simon a lot of presents**. / They gave **a lot of presents to Simon**.',
                   '(3) *it* is a pronoun → pattern 2: Can you show **it to me**?',
                   '(4) *bring* to help someone → **for**: I have brought this book **for your sister**.',
               ], '(1) He wrote Dan a letter. (2) They gave Simon a lot of presents. (3) Can you show it to me? (4) I have brought this book for your sister.', page=ob_p),
        worked('eng11-u8-obj-c5', 'Step by step: find the direct and the indirect object', 'She sent her grandmother a long letter.', [
            '**Step 1: Find the verb.** *sent*.',
            '**Step 2: Ask "sent what?"** → *a long letter* = **direct object** (the thing).',
            '**Step 3: Ask "sent it to whom?"** → *her grandmother* = **indirect object** (the person).',
            '**Step 4: Check with pattern 2.** *She sent a long letter **to** her grandmother.* ✔',
        ], 'Direct object: a long letter. Indirect object: her grandmother.', page=ob_p),
        check('eng11-u8-obj-c6', "In 'The teacher gave us homework', the indirect object is ____.", {'A': 'The teacher', 'B': 'gave', 'C': 'us', 'D': 'homework'}, 'C', [
            '**Step 1:** gave what? → *homework* (direct object).', '**Step 2:** gave it to whom? → **us** (indirect object).',
            '**Step 3:** *The teacher* is the subject.', f'**Tip:** {OB_TIP}'], page=ob_p),
        check('eng11-u8-obj-c7', 'Choose the correct sentence.', {'A': 'He explained me the problem.', 'B': 'He explained the problem to me.', 'C': 'He explained to me problem.', 'D': 'He explained for me the problem.'}, 'B', [
            '**Step 1:** *explain* uses only pattern 2: explain + thing + **to** + person.', '**Step 2:** So: *He explained the problem to me.*',
            '**Step 3:** A is a very common mistake – *explain* cannot take the person straight after it.', f'**Tip:** {OB_TIP}'], page=ob_p),
        check('eng11-u8-obj-c8', 'I bought a new dress ____ my little sister.', {'A': 'to', 'B': 'for', 'C': 'at', 'D': 'with'}, 'B', [
            '**Step 1:** *buy* = we do it to help the person → **for**.', '**Step 2:** Pattern 1 is also possible: *I bought my little sister a new dress.*',
            '**Step 3:** *to* is used with give, send, show, tell…', f'**Tip:** {OB_TIP}'], page=ob_p),
        check('eng11-u8-obj-c9', 'Please pass ____.', {'A': 'me it', 'B': 'it me', 'C': 'it to me', 'D': 'to me it'}, 'C', [
            '**Step 1:** The direct object is the pronoun *it*.', '**Step 2:** Pronoun object → pattern 2: pass **it to me**.',
            '**Step 3:** A and B are avoided in standard written English; D has the wrong order.', f'**Tip:** {OB_TIP}'], page=ob_p),
        check('eng11-u8-obj-c10', "Rewrite 'They gave a prize to the best student' with the indirect object first.",
              {'A': 'They gave the best student a prize.', 'B': 'They gave to the best student a prize.', 'C': 'They gave a prize the best student.', 'D': 'They the best student gave a prize.'}, 'A', [
                  '**Step 1:** Pattern 1 = V + person + thing, with **no** preposition.', '**Step 2:** *They gave the best student a prize.*',
                  '**Step 3:** B keeps *to* (wrong in pattern 1); C drops *to* in pattern 2.', f'**Tip:** {OB_TIP}'], page=ob_p),
    ])
    u['glossary'] = [
        dict(term='transitive verb', meaning='a verb that needs an object: raise, tell, find (He found a wallet).', page=tv_p, src='notes'),
        dict(term='intransitive verb', meaning='a verb with no object: rise, sleep, arrive (The sun rises).', page=tv_p, src='notes'),
        dict(term='complement', meaning='a word after a linking verb that describes the subject: The tea is hot.', page=tv_p, src='notes'),
        dict(term='direct object', meaning='the thing that receives the action: She gave me a book.', page=ob_p, src='notes'),
        dict(term='indirect object', meaning='the person who receives the direct object or gets the help: She gave me a book.', page=ob_p, src='notes'),
    ]
    u['tips'] = [dict(text='Ask "what?" after the verb. An answer = object (transitive). No answer = intransitive.', page=tv_p, src='notes', card='eng11-u8-tv-c6'),
                 dict(text='give/send/show + **to**; buy/make/get + **for**; explain/describe/suggest + thing + **to** + person.', page=ob_p, src='notes')]
    u['games'] = [
        dict(id='eng11-u8-g2', type='match', title='Transitive, intransitive or linking?', src='notes', lesson='eng11-u8-l8-tv', pairs=[
            {'a': 'He raised his hands.', 'b': 'transitive'}, {'a': 'The dog barks.', 'b': 'intransitive'}, {'a': 'The old man went mad.', 'b': 'linking + complement'},
            {'a': 'She told a story.', 'b': 'transitive'}, {'a': 'An accident happened.', 'b': 'intransitive'}, {'a': 'The tea is hot.', 'b': 'linking + complement'}]),
        dict(id='eng11-u8-g3', type='match', title='Match the verb to its pattern', src='notes', lesson='eng11-u8-l8-obj', pairs=[
            {'a': 'give / send / show', 'b': '+ thing + to + person'}, {'a': 'buy / make / cook', 'b': '+ thing + for + person'},
            {'a': 'explain / describe', 'b': 'only: + thing + to + person'}, {'a': 'Give it to me.', 'b': 'pronoun object → pattern 2'},
            {'a': 'She gave me a pen.', 'b': 'V + IO + DO'}]),
    ]
    u['unitMap'] = unitmap('eng11-u8', 'Transitive verbs & objects', [
        ('l8_tv', 'Transitive and intransitive verbs', 'eng11-u8-l8-tv', ['eng11-u8-tv-c1', 'eng11-u8-tv-c2', 'eng11-u8-tv-c5']),
        ('l8_obj', 'Direct and indirect objects', 'eng11-u8-l8-obj', ['eng11-u8-obj-c1', 'eng11-u8-obj-c2', 'eng11-u8-obj-c3'])])
    sim_tv = [('Transitive or intransitive? "The baby cried all night."', 'intransitive (cried what? – nothing)'),
              ('Find the object: "The mechanic repaired the car quickly."', 'the car')]
    sim_ob = [('Rewrite with "to": "She showed me her photos."', 'She showed her photos to me.'),
              ('Rewrite with the person first: "I made a cake for my mother."', 'I made my mother a cake.')]
    Q = []
    tvq = [
        ('Which verb in this list is intransitive?', {'A': 'bring', 'B': 'arrive', 'C': 'discuss', 'D': 'raise'}, 'B',
         ['*arrive* never takes an object: *arrive at school*.', '*bring, discuss, raise* need an object.']),
        ("In 'The driver lost control of the car', the object of 'lost' is ____.", {'A': 'The driver', 'B': 'control', 'C': 'the car', 'D': 'of'}, 'B',
         ['lost what? → **control**.', '*of the car* is a phrase that tells us control of what.']),
        ('The ambulance ____ at the hospital ten minutes later.', {'A': 'reached', 'B': 'arrived', 'C': 'got to', 'D': 'reached at'}, 'B',
         ['*at the hospital* follows the gap, so we need an intransitive verb + at: **arrived at**.', '*reached* is transitive: *reached the hospital* (no *at*).']),
        ('Many people ____ in road accidents every year.', {'A': 'die', 'B': 'are died', 'C': 'kill', 'D': 'are dying them'}, 'A',
         ['*die* is intransitive: it has no object and no passive.', '✗ *are died*. (Compare: *Accidents kill many people.* – *kill* is transitive.)']),
        ('Which sentence has a linking verb and a complement?', {'A': 'The witness told the truth.', 'B': 'The road became very slippery.', 'C': 'The car hit a tree.', 'D': 'The cyclist fell off his bike.'}, 'B',
         ['*slippery* describes *the road* → *became* is a linking verb, *very slippery* is the complement.', 'A and C have objects; D is intransitive with a place phrase.']),
        ('Please ____ your hand if you know the answer.', {'A': 'rise', 'B': 'raise', 'C': 'arise', 'D': 'rising'}, 'B',
         ['*your hand* is an object → transitive **raise**.', '*rise* has no object (*The sun rises*).']),
        ('After the long journey she went to her room and ____ down on the bed.', {'A': 'laid', 'B': 'lay', 'C': 'lied', 'D': 'layed'}, 'B',
         ['No object → intransitive *lie* (rest). Past: lie – **lay** – lain.', '*laid* is the past of *lay* (+ object); *lied* = told a lie.']),
        ('The committee ____ the causes of the accident for two hours.', {'A': 'discussed about', 'B': 'discussed', 'C': 'discussed on', 'D': 'discussion'}, 'B',
         ['*discuss* is transitive: discuss + object, with no preposition.']),
    ]
    for i, (q, o, a, w) in enumerate(tvq, 1):
        Q.append(mcq(f'eng11-u8-tq{i:02d}', q, o, a, w, TV_TIP, sim_tv, page=tv_p))
    obq = [
        ("In 'The nurse handed the doctor a bandage', the direct object is ____.", {'A': 'The nurse', 'B': 'handed', 'C': 'the doctor', 'D': 'a bandage'}, 'D',
         ['handed what? → **a bandage** (the thing) = direct object.', '*the doctor* is the indirect object (the person).']),
        ('Can you lend ____?', {'A': 'me your pen', 'B': 'to me your pen', 'C': 'your pen me', 'D': 'me to your pen'}, 'A',
         ['Pattern 1: V + person + thing, no preposition: *lend me your pen*.', 'Or pattern 2: *lend your pen to me*.']),
        ('My uncle cooked a delicious meal ____ us.', {'A': 'to', 'B': 'for', 'C': 'at', 'D': 'by'}, 'B',
         ['*cook* = to help/please someone → **for**.']),
        ('Could you describe ____?', {'A': 'me the thief', 'B': 'the thief to me', 'C': 'to me the thief', 'D': 'the thief me'}, 'B',
         ['*describe* uses only pattern 2: describe + thing/person described + **to** + listener.']),
        ('Which sentence is correct?', {'A': 'She sent to her friend a message.', 'B': 'She sent her friend a message.', 'C': 'She sent a message her friend.', 'D': 'She sent her friend to a message.'}, 'B',
         ['Pattern 1: V + person + thing (no *to*).', 'Pattern 2 would be: *She sent a message to her friend.*']),
        ('The police officer showed ____ his identity card.', {'A': 'to us', 'B': 'us', 'C': 'for us', 'D': 'we'}, 'B',
         ['Person before the thing → no preposition: *showed us his identity card*.', '*we* is a subject pronoun.']),
    ]
    for i, (q, o, a, w) in enumerate(obq, len(tvq) + 1):
        Q.append(mcq(f'eng11-u8-tq{i:02d}', q, o, a, w, OB_TIP, sim_ob, page=ob_p))
    n = len(Q)
    Q += [
        fill(f'eng11-u8-tq{n + 1:02d}', 'Prices ____ (rise / raise) every year.', 'rise', ['rise', 'raise', 'raises', 'rises up'],
             ['No object after the verb → intransitive **rise**.', 'Plural subject *prices* → *rise* (no -s).'], TV_TIP, sim_tv, page=tv_p),
        fill(f'eng11-u8-tq{n + 2:02d}', 'The government has ____ (rise / raise) the price of fuel.', 'raised', ['raised', 'risen', 'rose', 'rised'],
             ['*the price of fuel* is an object → transitive **raise**.', 'After *has*: past participle *raised*.'], TV_TIP, sim_tv, page=tv_p),
        fill(f'eng11-u8-tq{n + 3:02d}', 'Can you explain this word ____ me?', 'to', ['to', 'for', 'at', '(nothing)'],
             ['*explain* + thing + **to** + person.'], OB_TIP, sim_ob, page=ob_p),
        fill(f'eng11-u8-tq{n + 4:02d}', 'I will get a glass of water ____ you.', 'for', ['for', 'to', 'at', 'with'],
             ['*get* (fetch something to help someone) → **for**.'], OB_TIP, sim_ob, page=ob_p),
        tf(f'eng11-u8-tq{n + 5:02d}', 'True or false: "The accident was happened at night" is correct.', False,
           ['False. *happen* is intransitive, so it has no passive form.', 'Correct: *The accident happened at night.*'], TV_TIP,
           [('Correct: "The bus was arrived late."', 'The bus arrived late.')], page=tv_p),
        tf(f'eng11-u8-tq{n + 6:02d}', 'True or false: In "She seems tired", "tired" is the object of "seems".', False,
           ['False. *seems* is a linking verb; *tired* describes the subject *she*.', 'So *tired* is a **complement**, not an object.'], TV_TIP, sim_tv, page=tv_p),
        short(f'eng11-u8-tq{n + 7:02d}', 'Write the verb, say if it is transitive or intransitive, and give the object if there is one: "The witness told the police everything."',
              'told – transitive – objects: the police (indirect) and everything (direct)',
              ['told what? → *everything* (direct object).', 'told it to whom? → *the police* (indirect object).', 'It has objects → transitive.'], TV_TIP, sim_tv, page=tv_p),
        short(f'eng11-u8-tq{n + 8:02d}', 'Rewrite with "to" or "for": "My father bought me a bicycle."', 'My father bought a bicycle for me.',
              ['*buy* → **for**.', 'Pattern 2: V + thing + for + person.'], OB_TIP, sim_ob, page=ob_p, accept=['My father bought a bicycle for me']),
        short(f'eng11-u8-tq{n + 9:02d}', 'Correct the error: "The teacher explained us the new rule."', 'The teacher explained the new rule to us.',
              ['*explain* cannot take the person straight after it.', 'Use: explain + thing + **to** + person.'], OB_TIP, sim_ob, page=ob_p,
              accept=['The teacher explained the new rule to us']),
        short(f'eng11-u8-tq{n + 10:02d}', 'Correct the error: "We arrived the accident scene after the police."', 'We arrived at the accident scene after the police.',
              ['*arrive* is intransitive: it needs *at* (a place) or *in* (a city/country) before the place.'], TV_TIP, sim_tv, page=tv_p,
              accept=['We arrived at the accident scene after the police']),
        short(f'eng11-u8-tq{n + 11:02d}', 'Rewrite with the indirect object first: "Please read a story to the children."', 'Please read the children a story.',
              ['Pattern 1: V + person + thing, with no *to*.'], OB_TIP, sim_ob, page=ob_p, accept=['Please read the children a story']),
    ]
    u['exercise'] = dict(questions=Q)


def apply(b):
    move_cohesion(b)
    unit8(b)
