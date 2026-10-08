"""Grade 11, part D: the other imported 'study notes' units get a short, simple rule card and a short notes card
(the long jargon text – syntactic, morphological, L1 interference… – is replaced)."""
from lib import grammar, text

CARDS = {
    'eng11-u9': (
        'Nouns: countable, uncountable and plurals', [
            '**Countable nouns** can be counted: *a student, two students*. **Uncountable nouns** cannot: *information, advice, water, furniture, luggage, equipment, progress, homework, news*.',
            'Uncountable nouns have **no plural** and no *a/an*: *some advice* (✗ advices), *a piece of advice, two items of luggage*. They take a **singular** verb: *The news **is** good.*',
            'Use **many / a few / fewer** with countable nouns and **much / a little / less** with uncountable nouns: *many books, much time*.',
            'Most plurals add **-s / -es / -ies**: *book → books, box → boxes, city → cities*. Learn the irregular ones: *man → men, child → children, tooth → teeth, criterion → criteria, phenomenon → phenomena, crisis → crises*. Some stay the same: *sheep, deer, species, series*.',
            'Abstract nouns used in general take **no article**: ***Honesty** is the best policy.* (✗ The honesty is…)',
        ], [('She gave me some useful advice.', True), ('She gave me many useful advices.', False, 'She gave me a lot of useful advice.'),
            ('There are three sheep in the field.', True), ('The informations are correct.', False, 'The information is correct.')],
        'count: a/many/few + plural  ·  uncount: some/much/little + singular verb',
        ['**In short:** ask "can I count it?" Yes → countable (a, many, few, plural). No → uncountable (much, little, a piece of, singular verb).',
         'Words that are countable in Tigrinya but **uncountable** in English: *information, advice, news, furniture, luggage, equipment, homework, knowledge*.',
         'Irregular plurals to learn: *child–children, foot–feet, mouse–mice, criterion–criteria, phenomenon–phenomena, crisis–crises, analysis–analyses*.']),
    'eng11-u11': (
        'Main verbs and helping verbs', [
            'A **main verb** tells the action or state: *She **writes**. They **are** happy.* A **helping verb** (*be, have, do*, and modals *can, will, must…*) goes before the main verb: *She **is** writing. They **have** finished. **Do** you know?*',
            '**Regular verbs** add **-ed** for the past and past participle: *work – worked – worked*. **Irregular verbs** change in other ways: *sing – sang – sung, bend – bent – bent, put – put – put*. Learn them from a list.',
            '**be + verb-ing** makes continuous tenses: *She **is working**.* (✗ She working). **be + past participle** makes the passive: *The window **was broken**.*',
            '**have + past participle** makes perfect tenses: *They **have broken** the window.* After a modal use the **base verb**: *She can **swim*** (✗ can swims, can to swim).',
        ], [('The children have broken the window.', True), ('She working in a bank.', False, 'She is working in a bank.'),
            ('He can speaks French.', False, 'He can speak French.'), ('The letter was written yesterday.', True)],
        'helping verb + main verb: is writing · has written · was written · can write',
        ['**In short:** every English sentence needs a verb. Continuous tenses and the passive need a form of **be**.',
         'Three forms to learn for every verb: base – past – past participle (*go – went – gone, write – wrote – written*).',
         'After **do/does/did** and after modals, use the base verb: *Does she **like** it? You must **go**.*']),
    'eng11-u12': (
        'Present simple, present continuous and past', [
            '**Present simple** (*I work, she works*) = habits, facts, timetables: *She **walks** to school every day. Water **boils** at 100 °C.*',
            '**Present continuous** (*am/is/are + -ing*) = happening **now** or for a short time: *Look! It**\'s raining**. I**\'m staying** with my aunt this week.*',
            '**Past simple** (*worked, went*) = finished actions at a past time: *We **visited** Keren last year.* **Past continuous** (*was/were + -ing*) = an action in progress in the past: *I **was reading** when the lights went out.*',
            '**State verbs** (*know, understand, believe, want, like, love, own, seem, belong*) do **not** take -ing: *I **understand** the lesson.* (✗ I am understanding)',
        ], [('She walks to school every day.', True), ('I am understanding the lesson now.', False, 'I understand the lesson now.'),
            ('I was reading when the phone rang.', True), ('He is go to work by bus every day.', False, 'He goes to work by bus every day.')],
        'habit → present simple · now → am/is/are + -ing · finished past → V2',
        ['**Signal words:** present simple – *every day, usually, often, never*; present continuous – *now, at the moment, look!, this week*; past simple – *yesterday, ago, last…*.',
         'Remember the **-s** in the present simple with *he/she/it*: *She work**s***.',
         'State verbs stay simple even "now": *I **know** the answer now.*']),
    'eng11-u17': (
        'Phrasal verbs', [
            'A **phrasal verb** = verb + a small word (*up, off, out, down, on, after*). The meaning is often new: *give up* = stop trying, *call off* = cancel, *look after* = take care of, *run into* = meet by chance.',
            '**Separable** phrasal verbs: a noun object can go after or in the middle: *turn off the light* / *turn the light off*.',
            'With a **pronoun** (*it, them, him*), the pronoun **must** go in the middle: *turn **it** off* (✗ turn off it), *write **them** down*.',
            '**Inseparable** ones never split: *look after the children / look after **them*** (✗ look them after); also *rely on, cope with, run into, get over*.',
        ], [('Please turn it off.', True), ('Please turn off it.', False, 'Please turn it off.'),
            ('She looks after her little brother.', True), ('The match was called off because of the rain.', True)],
        'verb + particle + noun  ·  verb + pronoun + particle',
        ['**In short:** learn each phrasal verb with its meaning, like a new word.',
         'Pronoun object → put it in the middle of a separable phrasal verb: *pick **it** up, put **them** away*.',
         'Common ones in exams: give up, call off, put off (postpone), look forward to + -ing, run out of, get on with, take after (look like a parent).']),
    'eng11-u19': (
        'Collocations, idioms and similes', [
            'A **collocation** is a pair of words that naturally go together: *make a decision, do homework, commit a crime, pay attention, take an exam, keep a promise, heavy rain, strong tea*.',
            'You cannot translate them word for word. ✗ *do a decision, give attention, strong rain*.',
            'An **idiom** has a meaning different from its words: *break the ice* = start a friendly conversation; *once in a blue moon* = very rarely; *a piece of cake* = very easy.',
            'A **simile** compares with **as … as** or **like**: *as busy as a bee, as brave as a lion, sleep like a log*.',
        ], [('She made a quick decision.', True), ('Please give attention to the teacher.', False, 'Please pay attention to the teacher.'),
            ('There was strong rain last night.', False, 'There was heavy rain last night.'), ('The test was a piece of cake.', True)],
        'make / do / take / pay + noun  ·  as + adjective + as + noun',
        ['**make** = create (a decision, a mistake, a plan, progress, noise); **do** = activity/work (homework, the dishes, an exercise, your best).',
         'Learn collocations in pairs and write your own sentence with each one.',
         'Idioms are used in speaking and stories; in formal essays use plain words.']),
    'eng11-u20': (
        'Synonyms, antonyms and analogies', [
            'A **synonym** has the same or nearly the same meaning: *big – large, begin – start, brave – courageous*. Choose the one that fits the **sentence**.',
            'An **antonym** has the opposite meaning: *hot – cold, ancient – modern*. Many are made with a prefix: *possible – **im**possible, honest – **dis**honest, compatible – **in**compatible*.',
            'Use **context clues**: words like *however, but, although, whereas* often show an opposite meaning; *and, also, in other words* show a similar meaning.',
            'An **analogy** compares two pairs that have the same relationship: *hand : glove :: foot : sock* (what you wear on it). Find the link in the first pair, then apply it to the second.',
            'Word parts help: *bene-* = good, *mal-* = bad, *chron-* = time, *auto-* = self: *benefit, malnutrition, chronological, autobiography*.',
        ], [('"Begin" and "start" are synonyms.', True), ('"Ancient" is the antonym of "old".', False, '"Ancient" is the antonym of "modern".'),
            ('Doctor : hospital :: teacher : school', True)],
        'synonym = same · antonym = opposite · A : B :: C : D (same link)',
        ['**Exam method:** read the whole sentence, cover the options, think of your own word, then choose the option closest to it.',
         'Check the word class: a noun must be replaced by a noun, an adjective by an adjective.',
         'For analogies, say the link as a sentence: "A glove is worn on a hand" → "A sock is worn on a foot".']),
    'eng11-u21': (
        'Everyday conversation: useful expressions', [
            'In dialogue questions, first decide the **function**: agreeing, disagreeing, inviting, refusing, apologising, thanking, advising, complaining.',
            '**Strong agreement:** *I couldn\'t agree more! / You can say that again!* (both mean "I agree completely", even though one has *not*).',
            '**Polite refusal:** *I\'d love to, but… / I\'m afraid I can\'t.* **Thanks:** *Thank you – You\'re welcome / Not at all / Don\'t mention it.*',
            '**Apology:** *I\'m sorry I\'m late. – That\'s all right / Never mind.* **Advice:** *You\'d better… / Why don\'t you…? / If I were you, I would…*',
        ], [('A: Thank you for your help. B: You\'re welcome.', True), ('A: I\'m sorry I\'m late. B: Yes, I\'m sorry too.', False, 'B: That\'s all right.'),
            ('A: This exam was very hard. B: You can say that again!', True)],
        'function → formula: agree · refuse · thank · apologise · advise',
        ['**Exam method:** read the line **after** the gap too – it often shows if the answer was yes or no.',
         'Polite English uses *Could you…? Would you mind + -ing? I\'m afraid…*.',
         'Some answers look negative but are positive: *I couldn\'t agree more. Not at all* (= you\'re welcome / no problem).']),
    'eng11-u22': (
        'Pronunciation: vowel sounds and silent letters', [
            'English spelling and sound do not always match: *ough* sounds different in *cough, through, though, enough*.',
            '**Silent letters:** *b* after *m* (*climb, thumb, comb*) and in *debt, doubt*; *k* before *n* (*know, knife*); *w* before *r* (*write, wrong*); *h* in *hour, honest*; *t* in *listen, castle*; *g* before *n* (*sign, foreign*).',
            '**Short and long vowels:** *ship /ɪ/ – sheep /iː/, full /ʊ/ – fool /uː/, cat /æ/ – cart /ɑː/*. Changing the vowel can change the word.',
            'The **-ed** ending has three sounds: /t/ after voiceless sounds (*walked, watched*), /d/ after voiced sounds (*played, lived*), /ɪd/ after t or d (*wanted, needed*).',
        ], [('The "b" in "climb" is silent.', True), ('"Hour" begins with an /h/ sound.', False, '"Hour" begins with a vowel sound: an hour.'),
            ('"Wanted" ends with /ɪd/.', True)],
        'silent: mb · kn · wr · (h)our · lis(t)en · si(g)n',
        ['**Exam method:** say each word quietly and listen for the odd one out.',
         'Use *an* before a vowel **sound**: *an hour, an honest man*, but *a university, a European*.',
         '-ed endings: /t/ walked, /d/ played, /ɪd/ wanted.']),
    'eng11-u23': (
        'Reading: main idea, details and reference words', [
            '**Skimming** = read quickly (title, first and last sentence of each paragraph) to find the **main idea**.',
            '**Scanning** = look quickly for one fact: a name, a number, a date.',
            '**Context clues** for new words: a definition (*…, which means…*), an example (*such as…*), a synonym (*or…*), or an opposite (*but, however*).',
            '**Reference words** (*it, they, this, that, these, which, the former, the latter*) point back to a noun before them. Replace the word with your answer and read the sentence again to check.',
        ], [('Skimming means reading for the main idea.', True), ('Scanning means reading every word slowly.', False, 'Scanning means looking quickly for a particular fact.')],
        'skim → main idea · scan → detail · reference word → the noun before it',
        ['**Exam method:** read the questions first, then read the passage.',
         'For a "meaning of the word" question, read the sentence before and after the word.',
         'For a "what does it refer to" question, look back at the nouns just before the word.']),
    'eng11-u24': (
        'Common mistakes (and how to fix them)', [
            '**Double subject:** ✗ *My father he is a teacher.* → *My father is a teacher.*',
            '**Two linking words for one idea:** ✗ *Although it rained, but we went out.* → use only one: *Although it rained, we went out.* / *It rained, but we went out.*',
            '**Missing *is/are*:** ✗ *She very clever.* → *She **is** very clever.*',
            '**Comparatives and superlatives:** ✗ *more better, most cleverest* → *better, cleverest*; ✗ *She is the most intelligent than…* → *more intelligent than* / *the most intelligent in…*.',
            '**Word order:** subject + verb + object: ✗ *Our team the final won.* → *Our team won the final.*',
        ], [('My father is a teacher.', True), ('My father he is a teacher.', False, 'My father is a teacher.'),
            ('Although it was raining, but we went out.', False, 'Although it was raining, we went out.'), ('This book is better than that one.', True)],
        'S + V + O · one linking word · better / the best',
        ['**Checklist before you hand in:** Is there a verb? Only one subject? One linking word per idea? -s with he/she/it?',
         'Many mistakes come from translating Tigrinya word by word. Read your sentence aloud in English.',
         'Compare with *-er / more … than*; use *the -est / the most* with *in / of*.']),
}

HEADS = {'Syntactic Rule / Formula': 'Pattern', 'English Phrasal Verb Type': 'Type', 'Tigrinya Concept Equivalent': 'In Tigrinya',
         'Tigrinya Concept equivalent / Note': 'In Tigrinya / note', 'Tigrinya Concept Equivalent / Note': 'In Tigrinya / note',
         'Tigrinya equivalent / Note': 'In Tigrinya / note', 'Phonic Pattern / Target': 'Pattern', 'Phonetic Sound': 'Sound',
         'Relationship / Structure': 'How it works', 'Grammatical Pattern': 'What to look at', 'Tigrinya-influenced Error': 'Mistake',
         'Correct English Structure': 'Correct', 'Grammatical Rule / Trap': 'Rule', 'Collocation Pattern': 'Pattern'}


def apply(b):
    for uid, (title, rules, examples, pattern, notes) in CARDS.items():
        b.replace_card(grammar(f'{uid}-c01', title, rules, examples, pattern=pattern))
        if b.has_card(f'{uid}-c02') and b.card(f'{uid}-c02')['type'] == 'text':
            b.replace_card(text(f'{uid}-c02', 'Notes', notes))
        u = b.unit(uid)
        if u['intro'].startswith('Grammar from Study Notes'):
            u['intro'] = title + '.'
    for u in b.d['units']:
        for l in u['lessons']:
            for c in l['cards']:
                if c['type'] == 'table':
                    c['head'] = [HEADS.get(h, h) for h in c['head']]
