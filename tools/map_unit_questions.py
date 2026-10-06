#!/usr/bin/env python3
"""Rebuild assets/high/notes/unit_questions.json (notes unit -> matric/model question ids) from the CURRENT eager exam bank
(every paper listed in assets/high/exams/index.json; the lazy Drive packs duplicate these papers and are not loaded when
the links are built, so they are not linked).

  python3 tools/map_unit_questions.py            # rebuild + report
  python3 tools/map_unit_questions.py --calibrate  # accuracy of the text classifier against the textbook-ref links

Evidence per question, strongest first (a question and its exact copies in other papers form one group):
  1. the previous link built from the question's textbook_ref + printed page (tools/map_questions.py, confidence high/medium),
     frozen in tool/matric_unit_sync/textbook_ref_links.json
  2. textbook_ref (grade + "Unit N - title") of any copy, resolved against the notes units of the subject family
  3. English: grammar/function rules (topic + stem) -> every unit whose lessons teach that point
  4. text classifier: TF-IDF of the question vs the notes unit text + nearest unit-tagged exercise/linked items;
     if it is unsure, an earlier text-similarity link (prior_text_links.json) is kept at low confidence
     when that unit is still in the classifier's top 3
Every group is linked once per unit (one representative copy: not broken, curated paper first, longest explanation).
Broken questions (wrong/missing key, missing figure, faulty item) are not linked; tool/matric_unit_sync/report.json lists them.
The exam papers themselves are not changed.
"""
import argparse, collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unitmap_lib import *

OUTDIR = os.path.join(ROOT, 'tool/matric_unit_sync')
OVR = json.load(open(os.path.join(OUTDIR, 'overrides.json')))

def on(s):
    return re.sub(r'\s+', ' ', str(s)).strip().lower().rstrip('.')

def ckey(q):
    st = re.sub(r'^\s*\d+[\.\)]\s*', '', q.get('stem') or '')
    st = re.sub(r'[*_`]', '', st)
    o = q.get('options') or {}
    return on(st) + '||' + '|'.join(sorted(on(v) for v in (o.values() if isinstance(o, dict) else [])))

def expl_of(q):
    return '\n'.join(str(x) for x in q.get('explanation_steps') or []) + ' ' + str(q.get('answer_key_note') or '')

# ------------------------------------------------------------------ checks
FAULT = re.compile(r"no option is (?:right|correct)|strictly no option|item is faulty|not among the options|is not printed|every option is accepted|"
                   r"low confidence|no correct option|keyed (?:only )?nominally|teacher decision", re.I)
STRONG = [r'(?i:correct answer is)\s*(?i:option\s*)?\(?\**([A-E])\b(?![\w\'])', r'\b(?i:answer)\s*[:=]\s*\**\(?([A-E])\b(?![\w\'])',
          r'\b(?i:the answer is)\s*(?i:option\s*)?\(?\**([A-E])\b(?![\w\'])', r'\b(?i:correct (?:option|choice) is)\s*\(?\**([A-E])\b(?![\w\'])']
MAPWORK = re.compile(r'\b(?:on|in|of|from) the (?:map|figure|diagram|picture)\b(?! scale)|\bthe (?:map|figure|diagram|picture) (?:above|below|shows|represents|given)|'
                     r'\bthe diagram represents\b|\bmarked points?\b|\bfrom the figure above\b|\bbetween (?:the )?points? \**[A-Z]\** and (?:point )?\**[A-Z]\**|'
                     r'\bpoints? \**[A-Z]\** (?:from|to) (?:point )?\**[A-Z]\**|\bpoints? "?[A-Z]"? to "?[A-Z]"?|\bpoint \**[A-Z]\** on the map', re.I)
MAPWORK_OK = {'bank-agriculture-model-2024-q053', 'bank-geo-matric-2025-q037', 'bank-geo-matric-2025-q069', 'bank-gkn-matric-2023-q039', 'gk-2023-matric-p1-q53',
              'bank-social-studies-matric-2024-q032', 'bank-geography-model-2020-2021-q081', 'phys-2010-matric-p1-q11', 'phys-2010-matric-p1-q12'}
PRES_CONT = re.compile(r'\bat the moment\b|\bright now\b|\bcurrently\b|\bthese days\b|\bnowadays\b|\bthis (?:week|month|term|semester|year)\b', re.I)
LAB = re.compile(r'laborator|apparatus|burette|pipette|graduated cylinder|meniscus|bunsen|fume hood|lab safety|safety (?:rule|precaution|goggles)|'
                 r'scientific method|hypothes[ie]s|titration|separating funnel|distillation|filtration|chromatograph|decantation|evaporating dish', re.I)
NO_PASSAGE = re.compile(r'\b(?:paragraph|passage|the text|the writer|the author|the essay|the article|line \d|in the story|the poem|according to the)\b', re.I)

def broken(q, e, media):
    """-> reason or None (None = usable)"""
    if q['id'] in OVR['drop']:
        return OVR['drop'][q['id']]
    st = q.get('stem') or ''
    if not st.strip() and not q.get('stem_tex'):
        return 'empty stem'
    if 'android_asset' in st or 'file://' in st:
        return 'figure not shipped (image link points to another app)'
    img = q.get('image')
    if img and img.replace('media/', '') not in media and not os.path.exists(os.path.join(EXAMS, img)):
        return 'figure missing: ' + img
    if not (img or q.get('image_alt') or q.get('stem_tables')) and not st.lstrip().startswith('[') and q['id'] not in MAPWORK_OK \
            and e['subject'] in ('Geography', 'Social Studies', 'General Knowledge', 'Agriculture', 'Chemistry', 'Physics', 'Biology') and MAPWORK.search(st):
        return 'needs a map/figure that is not in the paper data'
    expl = expl_of(q)
    m = FAULT.search(expl)
    if m:
        return 'faulty item (explanation: "' + m.group(0) + '")'
    if q['type'] == 'mcq' and not q.get('match_list_id'):
        o, a = q.get('options'), q.get('answer')
        if not isinstance(o, dict) or len([v for v in o.values() if on(v)]) < 2:
            return 'MCQ without options'
        if a not in o:
            return f'key {a!r} not in options'
        vals = [on(v) for v in o.values()]
        if not on(o[a]):
            return 'key is an empty option'
        if vals.count(on(o[a])) > 1:
            return 'key text appears in two options'
        said = [x for p in STRONG for x in re.findall(p, expl) if x in o]
        if said and said[-1] != a:
            return f'explanation says {said[-1]}, key says {a}'
        if not expl.strip():
            return 'no explanation'
    elif q['type'] != 'mcq':
        if not (q.get('answer') or q.get('marking_points') or q.get('subparts') or q.get('rubric') or q.get('accepted_answers')):
            return 'written question without answer'
    return None

# ------------------------------------------------------------------ English rules: (regex on topic+stem, units)
ENG_RULES = [
    (r'reported speech|indirect speech|direct (?:and|&|to) indirect|reported to direct|direct speech', ['eng9-u5', 'eng11-u5']),
    (r'passive', ['eng9-u2', 'eng9-u8', 'eng10-u7', 'eng11-u4']),
    (r'causative', ['eng11-u4', 'eng11-u7']),
    (r'conditional|\bif[- ]clause|\bwish\b', ['eng9-u9', 'eng9-u10', 'eng11-u6']),
    (r'additions?\b|short (?:answers?|responses?)|double negative|(?:negative|positive) agreement|agreement (?:responses?|and (?:dis)?agreement|and additions)|disagreement', ['eng11-u24', 'eng11-u21']),
    (r'subject[- ]verb|\bconcord\b|(?:^|\\| )agreement(?: \\||$)|en agreement|either/or|neither/nor', ['eng9-u6', 'eng10-u7', 'eng11-u2']),
    (r'\barticles?\b|determiner', ['eng9-u7']),
    (r'question tags?|tag questions?', ['eng9-u7', 'eng11-u15']),
    (r'\bmodals?\b|modal verb|semi-modal|\bability\b|deduction', ['eng10-u1', 'eng10-u5', 'eng11-u3']),
    (r'gerund|infinitive|participle|verb patterns?', ['eng10-u2', 'eng11-u7']),
    (r'relative (?:clause|pronoun)|adjective clause|adjectival clause', ['eng10-u4']),
    (r'noun clause|embedded question', ['eng10-u3']),
    (r'question formation|indirect question|embedded question|wh-question|forming questions', ['eng10-u6', 'eng11-u14']),
    (r'word formation|affix|prefix|suffix|parts? of speech|word class|derivation|(?:^|\\| )adjectives?(?: \\||$)|(?:^|\\| )adverbs?(?: \\||$)|adjectives and adverbs|grammar - adjectives|en adjectives', ['eng9-u3', 'eng9-u6', 'eng10-u6', 'eng11-u16']),
    (r'past (?:simple|continuous|perfect|tense)|simple past|used to', ['eng9-u1', 'eng11-u12']),
    (r'future (?:continuous|tense|progressive|forms?|arrangements?|perfect)', ['eng10-u2', 'eng11-u12']),
    (r'present (?:continuous|progressive)', ['eng10-u8', 'eng11-u12']),
    (r'\btenses?\b|verb tense|tense and usage|tense review|present perfect|present simple|simple present|perfect tenses|adverbs of time|still, yet', ['eng10-u9', 'eng11-u12', 'eng11-u13']),
    (r'compar(?:ison|ative)|superlative', ['eng10-u10']),
    (r'purpose|concessi|contrast|result clause', ['eng11-u8']),
    (r'clause connection|sentence joining|clause boundar|joining sentences', ['eng11-u1', 'eng12-u2', 'eng9-u4']),
    (r'linking words?|linkers?|connectors?|conjunctions?|cohesi|transition|discourse marker|conjunctive adverb|subordinat|coordinat', ['eng9-u4', 'eng11-u8', 'eng12-u2']),
    (r'punctuation|capitali[sz]ation', ['eng9-u3', 'eng9-u5']),
    (r'phrasal verb', ['eng11-u17']),
    (r'preposition', ['eng11-u18']),
    (r'collocation', ['eng11-u19', 'eng12-u2']),
    (r'idiom', ['eng11-u19', 'eng12-u5']),
    (r'synonym|antonym|analog|vocabulary|word choice|word meaning|verb meanings', ['eng11-u20']),
    (r'conversation|dialogue|communication|telephone|social expression|language function|reassurance', ['eng11-u21']),
    (r'pronunciation|vowel|consonant|word stress|syllable|phonetic|silent letter', ['eng11-u22']),
    (r'error (?:identification|correction|recognition)|common (?:grammatical )?mistake', ['eng11-u24']),
    (r'paragraph(?: writing| structure| development)?|topic sentence|supporting sentence|concluding sentence|coherence|writing skill', ['eng12-u3', 'eng12-u4']),
    (r'adverbs? of frequency', ['eng12-u4']),
    (r'inversion', ['eng12-u5']),
    (r'\bfinite|non-finite', ['eng12-u1']),
    (r'sentence (?:meaning|transformation|restatement)|paraphras', ['eng12-u1']),
    (r'\bnouns?\b|plural|countable|uncountable|quantifier', ['eng11-u9']),
    (r'pronoun|possessive', ['eng11-u10']),
    (r'confusing (?:verbs|words)|commonly confused', ['eng10-u8']),
    (r'word order|sentence structure|sentence pattern|\bsvc\b|s-v-o', ['eng10-u4', 'eng11-u1']),
    (r'adverbial (?:clause|phrase|conjunction)|adverb clause', ['eng10-u5', 'eng9-u1']),
    (r'headline', ['eng10-u9']),
    (r'(?:^|\\| )verbs?(?: \\||$)|verbs in context|verb forms?|irregular verb|auxiliar|en verbs', ['eng11-u11']),
]
# the stem is only used when the topic says nothing, and only for unambiguous wording
STEM_RULES = [
    (r'passive (?:voice|form)|into (?:the )?passive', ['eng9-u2', 'eng9-u8', 'eng10-u7', 'eng11-u4']),
    (r'reported speech|indirect speech|reported form', ['eng9-u5', 'eng11-u5']),
    (r'question tag|tag question', ['eng9-u7', 'eng11-u15']),
    (r'correct article|\barticles?\b', ['eng9-u7']),
    (r'correct preposition|\bprepositions?\b', ['eng11-u18']),
    (r'phrasal verb', ['eng11-u17']),
    (r'synonym|antonym|closest in meaning|opposite in meaning|similar in meaning', ['eng11-u20']),
    (r'correct(?:ly)? punctuated|punctuation', ['eng9-u3', 'eng9-u5']),
    (r'relative pronoun', ['eng10-u4']),
]
STEM_RULES = [(re.compile(rx, re.I), us) for rx, us in STEM_RULES]
ENG_RULES = [(re.compile(rx, re.I), us) for rx, us in ENG_RULES]

def english_units(q, has_passage):
    topic = ' | '.join([x for x in [q.get('topic') or ''] + [t.replace('-', ' ') for t in q.get('topics') or []] if x])
    st = q.get('stem') or ''
    if re.search(r'paragraph writing|write (?:a |an )?(?:meaningful |short )?(?:paragraph|essay|composition)|paragraph of about', topic + ' ' + st, re.I) \
            or (q['type'] in ('essay', 'workout') and re.search(r'\b(?:describe|write about|compare|discuss)\b', st[:80], re.I)) or re.search(r'(?:^|\| )paragraph writing|topic 1|topic 2', topic, re.I):
        return ['eng12-u3', 'eng12-u4'], 'topic'  # paragraph-writing task (rubric/model answer in the paper)
    reading = re.search(r'reading|comprehension|context clue|main idea|inference|passage', topic, re.I)
    if reading or (NO_PASSAGE.search(st) and not re.search(r'tense|passive|preposition|article|agreement|paragraph', topic, re.I)):
        if has_passage:
            return ['eng11-u23'], 'reading'
        return [], 'English reading question: its passage is not in the paper data'
    if q['type'] == 'essay':
        return [], 'English writing task: no unit teaches this kind of writing'
    if re.search(r'context', topic, re.I) and re.search(r'["“‘]|context:', st, re.I):
        return ['eng11-u23', 'eng11-u20'], 'topic'  # vocabulary in context, the context sentence is in the stem
    for src, rules in ((topic, ENG_RULES), (st, STEM_RULES)):  # topic first; stem only when the topic says nothing
        hits = []
        for rx, us in rules:
            if rx.search(src):
                hits += [u for u in us if u not in hits]
        if hits and any(u in hits for u in ('eng10-u9', 'eng11-u12')) and PRES_CONT.search(st) and 'eng10-u8' not in hits:
            hits.insert(0, 'eng10-u8')  # present continuous for a period of time
        if hits:
            return hits[:5], 'topic' if src is topic else 'stem'
    return [], 'English item: no grammar point matched a unit lesson'

# ------------------------------------------------------------------ textbook ref
def ref_units(ref, fam, units_by_book):
    g = ref.get('grade')
    if not g or not ref.get('unit'):
        return None
    m = re.match(r'\s*(?:Unit|Chapter)\s+(\d+)\s*[–\-:.]?\s*(.*)', str(ref['unit']))
    num = int(m.group(1)) if m else None
    title = norm(m.group(2) if m else ref['unit'])
    rs = (ref.get('subject') or '').lower().replace(' ', '_').replace('&', 'and')
    rs = {'business_and_economics': 'business_economics', 'maths': 'mathematics', 'math': 'mathematics'}.get(rs, rs)
    cands = [rs] if rs in fam else fam
    import difflib
    best = None
    for s in cands:
        for u in units_by_book.get((s, int(g)), []):
            r = difflib.SequenceMatcher(None, title, norm(u['title'])).ratio() if title else 0
            sc = r + (0.45 if num == u['number'] else 0)
            if not best or sc > best[0]:
                best = (sc, u, r, num == u['number'])
    if not best or best[0] < 0.55:
        return None
    return best[1]['id'], ('high' if best[2] >= 0.6 and best[3] else 'medium')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--calibrate', action='store_true')
    args = ap.parse_args()
    units = load_units()
    U = {u['id']: u for u in units}
    units_by_book = collections.defaultdict(list)
    for u in units:
        units_by_book[(u['subject'], u['grade'])].append(u)
    uid = [u['id'] for u in units]
    # unit documents
    docs, books = [], {}
    for u in units:
        nb = books.get(u['file']) or books.setdefault(u['file'], json.load(open(os.path.join(NOTES, u['file']))))
        uu = next(x for x in nb['units'] if x['id'] == u['id'])
        body = ' '.join(strings({k: v for k, v in uu.items() if k != 'exercise'}))
        docs.append(toks((u['title'] + ' ') * 4 + (' '.join(u['lessons']) + ' ') * 2 + body))
    tf = TfIdf(docs)
    idxj = json.load(open(os.path.join(EXAMS, 'index.json')))
    media = set(idxj['media'])
    exams = load_exams()
    byid = {q['id']: (f, e, q) for f, e, q in exams}
    passages = collections.defaultdict(set)
    for f in idxj['exams']:
        d = json.load(open(os.path.join(EXAMS, f)))
        for p in d.get('passages') or []:
            passages[f].add(p.get('id'))
    snap = json.load(open(os.path.join(OUTDIR, 'textbook_ref_links.json')))['units']
    oldmap = collections.defaultdict(list)  # id -> [(unit, conf, secondary, via)]
    for k, v in snap.items():
        for i, c, sec, via in v:
            oldmap[i].append((k, c, bool(sec), via))
    old_count = json.load(open(os.path.join(OUTDIR, 'before_counts.json')))
    # text-similarity links of the previous unit_questions.json (non-English); kept as a low-confidence
    # fallback when the classifier is unsure but still ranks that unit near the top
    prior = json.load(open(os.path.join(OUTDIR, 'prior_text_links.json')))

    def qtext(q):
        p = [q.get('stem') or '']
        o = q.get('options')
        if isinstance(o, dict):
            p += [str(x) for x in o.values()]
        p += list(q.get('keywords') or []) + [t.replace('-', ' ') for t in q.get('topics') or []]
        if q.get('topic'):
            p += [q['topic']] * 2
        p += [str(x) for x in q.get('explanation_steps') or []]
        return ' '.join(p)

    # gold (textbook-ref links) for kNN + calibration
    gold = {}
    for i, l in oldmap.items():
        for k, c, sec, via in l:
            if not sec and c == 'high' and i in byid and not k.startswith('eng'):
                gold[i] = k
    train = []
    for f in glob.glob(EXER + '/*.json') + glob.glob(EXER + '/school/*.json'):
        if f.endswith('index.json'):
            continue
        for q in json.load(open(f)).get('questions', []):
            if q.get('unit') in U and U[q['unit']]['subject'] != 'english':
                train.append((toks(q['prompt'] + ' ' + ' '.join(map(str, q.get('options') or [])) + ' ' + (q.get('explanation') or '')[:600]), q['unit'], 'ex|' + str(q.get('src', ''))))
    for i, k in gold.items():
        q = byid[i][2]
        train.append((toks(qtext(q)), k, 'mx|' + i + '|' + norm(q.get('stem'))[:60]))
    knn = Knn(train)

    def classify(q, fam, exclude_self=False):
        allowed_i = [i for i, u in enumerate(units) if u['subject'] in fam]
        if not allowed_i:
            return []
        allowed = {uid[i] for i in allowed_i}
        t = toks(qtext(q))
        ds = dict((uid[i], s) for i, s in tf.scores(tf.query(t), allowed_i))
        st = norm(q.get('stem'))[:60]
        ex = (lambda k: q['id'] in k or (st and k.endswith('|' + st))) if exclude_self else (lambda k: q['id'] in k)
        kv = collections.defaultdict(float)
        for l, s in knn.neighbours(t, 10, exclude=ex, allowed=allowed):
            kv[l] += s
        return sorted(((u, ds.get(u, 0) + 0.05 * kv.get(u, 0)) for u in allowed), key=lambda x: -x[1])

    def conf_of(sc, subj):
        top, mar = sc[0][1], sc[0][1] - sc[1][1]
        strict = subj == 'General Knowledge'
        if top >= (0.24 if strict else 0.2) and mar >= 0.05:
            return 'medium'
        if top >= (0.16 if strict else 0.12) and mar >= (0.03 if strict else 0.015):
            return 'low'
        return None

    if args.calibrate:
        rows = []
        for i, k in gold.items():
            f, e, q = byid[i]
            sc = classify(q, FAMILY[e['subject']], exclude_self=True)
            rows.append((sc[0][0] == k, conf_of(sc, e['subject'])))
        for c in ('medium', 'low', None):
            r = [x for x in rows if x[1] == c]
            print(c, len(r), round(sum(x[0] for x in r) / max(1, len(r)), 3))
        print('all', len(rows), round(sum(x[0] for x in rows) / len(rows), 3))
        return

    # ---------------------------------------------------------------- groups of identical questions
    groups = collections.defaultdict(list)
    for f, e, q in exams:
        groups[(FAMILY.get(e['subject'], ['?'])[0] if e['subject'] != 'English' else 'english', ckey(q)) if q.get('stem') else ('solo', q['id'])].append((f, e, q))
    dropped, unmapped, conflicts = [], [], []
    links = collections.defaultdict(dict)  # unit -> id -> entry
    curated = lambda f: not f.startswith('bank_')
    for key, members in groups.items():
        reasons = {q['id']: broken(q, e, media) for f, e, q in members}
        for f, e, q in members:
            if reasons[q['id']]:
                dropped.append({'id': q['id'], 'paper': f, 'reason': reasons[q['id']], 'stem': (q.get('stem') or '')[:120]})
        ok = [(f, e, q) for f, e, q in members if not reasons[q['id']]]
        if not ok:
            continue
        # key conflicts between copies: trust the curated (textbook-checked) paper, else drop the group
        if ok[0][2]['type'] == 'mcq' and not ok[0][2].get('match_list_id'):
            keytext = {q['id']: on(q['options'][q['answer']]) for f, e, q in ok}
            if len(set(keytext.values())) > 1:
                cur = [(f, e, q) for f, e, q in ok if curated(f)]
                if cur and len({keytext[q['id']] for f, e, q in cur}) == 1:
                    for f, e, q in ok:
                        if not curated(f):
                            dropped.append({'id': q['id'], 'paper': f, 'reason': f'key differs from the textbook-checked copy {cur[0][2]["id"]}', 'stem': (q.get('stem') or '')[:120]})
                    conflicts.append({'kept': cur[0][2]['id'], 'dropped': [q['id'] for f, e, q in ok if not curated(f)]})
                    ok = cur
                else:
                    for f, e, q in ok:
                        dropped.append({'id': q['id'], 'paper': f, 'reason': 'copies of this question have different keys', 'stem': (q.get('stem') or '')[:120]})
                    conflicts.append({'kept': None, 'dropped': [q['id'] for f, e, q in ok]})
                    continue
        # representative
        def rank(m):
            f, e, q = m
            return (curated(f), bool(q.get('textbook_ref')), len(expl_of(q)), str(e.get('year')))
        rep_f, rep_e, rep = max(ok, key=rank)
        subj = rep_e['subject']
        fam = FAMILY.get(subj, [])
        targets = []  # (unit, conf, via, secondary)
        if subj == 'English':
            has_p = any(q.get('passage_id') in passages[f] for f, e, q in ok if q.get('passage_id'))
            # a passage question must be represented by a copy that carries the passage
            if has_p:
                rep_f, rep_e, rep = next((f, e, q) for f, e, q in ok if q.get('passage_id') in passages[f])
            us, why = english_units(rep, has_p)
            if not us:
                unmapped.append({'id': rep['id'], 'subject': subj, 'reason': why, 'topic': rep.get('topic') or ''})
                continue
            targets = [(u, 'medium', why, i > 0) for i, u in enumerate(us) if u in U]
        else:
            for f, e, q in ok:  # 1. previous textbook-ref link of any copy
                for k, c, sec, via in oldmap.get(q['id'], []):
                    if k in U and c in ('high', 'medium') and not k.startswith('eng') and U[k]['subject'] in fam:
                        targets.append((k, c, via or 'textbook_ref', sec))
            if not targets:  # 2. textbook_ref
                for f, e, q in ok:
                    for j, r in enumerate([q.get('textbook_ref') or {}] + [x for x in q.get('additional_textbook_refs') or [] if isinstance(x, dict)]):
                        x = ref_units(r, fam, units_by_book)
                        if x:
                            targets.append((x[0], x[1] if j == 0 else 'medium', 'textbook_ref', j > 0))
                    if targets:
                        break
            if not targets:  # 3. classifier
                sc = classify(rep, fam)
                c = conf_of(sc, subj) if sc else None
                top3 = {u for u, x in sc[:3] if x >= 0.08}
                keep = [u for f, e, q in ok for u in prior.get(q['id'], []) if u in top3]
                if c:
                    targets = [(sc[0][0], c, 'text', False)]
                elif keep:
                    targets = [(keep[0], 'low', 'earlier text link', False)]
                else:
                    unmapped.append({'id': rep['id'], 'subject': subj, 'reason': 'no textbook ref and no clear match to a notes unit' if fam else 'subject has no notes book',
                                     'topic': rep.get('topic') or ''})
                    continue
        if subj in ('Chemistry', 'General Science') and LAB.search(rep.get('stem') or '') and 'chem9-u4' in U:
            targets.append(('chem9-u4', 'medium', 'lab rule', bool(targets)))  # Grade 9 lab guide & practical review unit
        seen = set()
        for u, c, via, sec in targets:
            if u in seen:
                continue
            seen.add(u)
            ent = {'id': rep['id'], 'confidence': c, 'via': via}
            if sec:
                ent['secondary'] = True
            if len(ok) > 1:
                ent['copies'] = len(ok)
            prev = links[u].get(rep['id'])
            if not prev or (prev.get('secondary') and not sec):
                links[u][rep['id']] = ent

    # ---------------------------------------------------------------- order + write
    CR = {'high': 0, 'medium': 1, 'low': 2}
    def year(i):
        e = byid[i][1]
        m = re.search(r'(19|20)\d\d', str(e.get('year')))
        return int(m.group()) if m else 0
    out_units = {}
    for u in units:
        l = list(links.get(u['id'], {}).values())
        l.sort(key=lambda m: (bool(m.get('secondary')), CR[m['confidence']], byid[m['id']][2]['type'] != 'mcq', -year(m['id']), m['id']))
        out_units[u['id']] = l
    stats = collections.defaultdict(collections.Counter)
    linked_ids = {m['id'] for l in out_units.values() for m in l}
    for i in linked_ids:
        stats[byid[i][1]['subject']]['linked'] += 1
    for x in unmapped:
        stats[x['subject']]['unmapped'] += 1
    for x in dropped:
        stats[byid[x['id']][1]['subject']]['dropped'] += 1
    out = {'about': 'Matric/model question ids per notes unit, built by tools/map_unit_questions.py from every paper in assets/high/exams/index.json. '
                    'confidence: high = textbook_ref unit and page agree; medium = textbook_ref only, English grammar rule, or clear text match; low = weaker text match. '
                    'secondary = the question also practises this unit. Identical copies of a question in several papers are linked once (copies = how many). '
                    'Broken, figure-less and unplaceable questions are listed in tool/matric_unit_sync/report.json.',
           'total_questions': len(exams), 'mapped': len(linked_ids), 'unmapped_count': len(unmapped), 'dropped_count': len({x['id'] for x in dropped}),
           'units': out_units, 'unmapped': [],
           'stats': {s: dict(v) for s, v in sorted(stats.items())}}
    with open(UQ, 'w') as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(',', ':'))
    rep = {'dropped': sorted(dropped, key=lambda x: x['id']), 'key_conflicts': conflicts, 'unmapped': unmapped,
           'before': old_count, 'after': {k: len(v) for k, v in out_units.items()}}
    with open(os.path.join(OUTDIR, 'report.json'), 'w') as fh:
        json.dump(rep, fh, ensure_ascii=False, indent=0)
    print('papers', len(idxj['exams']), 'questions', len(exams), 'groups', len(groups), 'linked', len(linked_ids), 'unmapped', len(unmapped), 'dropped', len({x['id'] for x in dropped}))
    print(json.dumps(out['stats']))


if __name__ == '__main__':
    main()
