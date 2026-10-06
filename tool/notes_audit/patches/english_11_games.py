#!/usr/bin/env python3
"""English 11 units 9-24: the 'Match key terms' games were cut from the study notes mid-sentence (a = 'Definition:',
b cut inside $$...$$). Replace them with hand-written term -> meaning/example pairs; fix two cut strings."""
import json, os
P = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets/high/notes/notes/english_11.json')
G = {
 'eng11-u9': ('Match the noun to its plural or quantifier', [('child', 'children'), ('criterion', 'criteria'), ('knife', 'knives'), ('information (uncountable)', 'much / a little information'), ('students (countable)', 'many / a few students')]),
 'eng11-u10': ('Match the pronoun to its use', [('I / he / they', 'subject: before the verb'), ('me / him / them', 'object: after verbs and prepositions'), ('mine / hers / theirs', 'possessive pronoun, no apostrophe'), ('myself / themselves', 'reflexive: refers back to the subject'), ('whom', 'formal object relative pronoun')]),
 'eng11-u11': ('Match the verb to its forms', [('go', 'went – gone'), ('write', 'wrote – written'), ('be', 'am/is/are – was/were – been'), ('have', 'perfect aspect: has/have/had + past participle'), ('do', 'dummy auxiliary in questions and negatives')]),
 'eng11-u12': ('Match the tense to its use', [('present simple', 'habits and general truths'), ('present continuous', 'actions happening now or temporary'), ('past simple', 'finished actions at a past time'), ('past continuous', 'an action in progress in the past'), ('stative verbs', 'know, believe, own: rarely continuous')]),
 'eng11-u13': ('Match the tense to its use', [('present perfect', 'past action linked to now (since, for, yet)'), ('past perfect', 'the earlier of two past actions'), ('future perfect', 'finished before a future time'), ('going to', 'plan or prediction from evidence'), ('will', 'instant decision or prediction')]),
 'eng11-u14': ('Match the question type to its pattern', [('yes/no question', 'Auxiliary + subject + verb? (Do you like tea?)'), ('wh-object question', 'Wh-word + auxiliary + subject + verb? (What did you buy?)'), ('subject question', 'Who/What + verb? (Who called?)'), ('indirect question', 'Could you tell me where the bank is?'), ('negative question', "Why didn't you come?")]),
 'eng11-u15': ('Match the statement to its tag', [('She is ready,', "isn't she?"), ("They didn't come,", 'did they?'), ('I am right,', "aren't I?"), ("Let's go,", 'shall we?'), ('Nobody called,', 'did they?')]),
 'eng11-u16': ('Match the affix to its meaning', [('un- / in- / im-', 'not'), ('re-', 'again'), ('mis-', 'wrongly'), ('-less', 'without'), ('-tion / -ment / -ness', 'make nouns')]),
 'eng11-u17': ('Match the phrasal verb to its meaning', [('give up', 'stop trying'), ('look after', 'take care of'), ('put off', 'postpone'), ('turn down', 'refuse'), ('find out', 'discover')]),
 'eng11-u18': ('Match the word to its preposition', [('proud', 'of'), ('interested', 'in'), ('depend', 'on'), ('good / clever', 'at'), ('congratulate someone', 'on')]),
 'eng11-u19': ('Match the collocation or idiom', [('make', 'a decision, a mistake, progress'), ('do', 'homework, the dishes, a favour'), ('heavy', 'rain, traffic'), ('a piece of cake', 'very easy'), ('over the moon', 'extremely happy')]),
 'eng11-u20': ('Match the word to its synonym or antonym', [('abundant (synonym)', 'plentiful'), ('generous (antonym)', 'mean'), ('ancient (antonym)', 'modern'), ('reluctant (synonym)', 'unwilling'), ('temporary (antonym)', 'permanent')]),
 'eng11-u21': ('Match the line to the best reply', [('Thank you for your help.', "You're welcome."), ("I'm sorry I'm late.", "That's all right."), ('My grandfather passed away.', "I'm so sorry to hear that."), ('Do you mind if I sit here?', 'Not at all.'), ('Have a safe journey!', 'Thanks!')]),
 'eng11-u22': ('Match the word to its vowel sound', [('seat, meet', 'long /iː/'), ('ship, sit', 'short /ɪ/'), ('food, moon', 'long /uː/'), ('good, put', 'short /ʊ/'), ('cup, blood', '/ʌ/')]),
 'eng11-u23': ('Match the context clue to its signal', [('definition clue', 'the word is explained: "X, which means ..."'), ('synonym clue', 'a similar word appears nearby'), ('contrast clue', 'however, unlike, but, whereas'), ('example clue', 'such as, for example, for instance'), ('inference', 'use details to work out what is not stated')]),
 'eng11-u24': ('Match the error to its correction', [('He a teacher.', 'He is a teacher.'), ('My brother he works.', 'My brother works.'), ('I am agree.', 'I agree.'), ("I don't know nothing.", "I don't know anything."), ('many homeworks', 'a lot of homework')]),
}
d = json.load(open(P, encoding='utf-8'))
for u in d['units']:
    if u['id'] in G:
        t, pairs = G[u['id']]
        g = u['games'][0]
        g.update(title=t, src='hand', pairs=[{'a': a, 'b': b} for a, b in pairs])
    for l in u['lessons']:
        for c in l['cards']:
            if c.get('rule'):
                c['rule'] = [r.replace('therefore/however/moreover link clauses with ; … ,', 'therefore / however / moreover join two clauses with a semicolon before and a comma after: *It rained; however, we played.*') for r in c['rule']]
            for s in c.get('steps') or []:
                s['text'] = s['text'].replace('therefore/however/moreover link clauses with ; … ,', 'therefore / however / moreover join two clauses with a semicolon before and a comma after: *It rained; however, we played.*')
            if c['id'] == 'eng11-u20-c03':
                c['rows'][4][2] = '*auto* = self, *logy* = study of (so *autobiography* = a life story written by oneself)'
    for q in u.get('exercise', {}).get('questions', []):
        q['why'] = [w if w.count('$$') % 2 == 0 else w[:w.rfind(' ($$')] + '.' for w in q['why']] if isinstance(q.get('why'), list) else q.get('why')
open(P, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
# agriculture 11 thermo-hygrograph unit cell lost a $
A = os.path.join(os.path.dirname(P), 'agriculture_11.json')
s = open(A, encoding='utf-8').read()
s = s.replace('"$^\\\\circ\\\\text{C}$$ and Percentage ($$\\\\%$$)"', '"Degrees Celsius ($$^\\\\circ\\\\text{C}$$) and percentage ($$\\\\%$$)"')
open(A, 'w', encoding='utf-8').write(s)
