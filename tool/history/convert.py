"""Convert the teacher-prepared History docx (Grades 9-11) into notes books. Idempotent: reads old books from tool/history/old/ (backup)."""
import docx, json, re, os, shutil, math, collections, zipfile, jsonschema
R = '/workspace/high_flutter'; N = f'{R}/assets/high/notes'; NB = f'{N}/notes'; OLD = f'{R}/tool/history/old'
DOCX = '/workspace/hist/h.docx'
os.makedirs(OLD, exist_ok=True)
for f in ['history_9.json', 'history_10.json', 'history_11.json', 'index.json']:
    if not os.path.exists(f'{OLD}/{f}'): shutil.copy(f'{NB}/{f}', f'{OLD}/{f}')
for f in ['unit_questions.json']:
    if not os.path.exists(f'{OLD}/{f}'): shutil.copy(f'{N}/{f}', f'{OLD}/{f}')
PL = f'{R}/assets/high/media/placements.json'
if not os.path.exists(f'{OLD}/placements.json'): shutil.copy(PL, f'{OLD}/placements.json')

d = docx.Document(DOCX)
# body stream: ('p', text, bold, numbered) or ('t', rows)
stream = []
for el in d.element.body.iterchildren():
    if el.tag.endswith('}p'):
        p = docx.text.paragraph.Paragraph(el, d)
        t = re.sub(r'\s+', ' ', p.text).strip()
        if not t or t in {'.', '-'}: continue
        runs = [r for r in p.runs if r.text.strip()]
        b = bool(runs) and all(r.bold for r in runs)
        pp = p._p.pPr; num = pp is not None and pp.numPr is not None
        lvl = pp.numPr.ilvl.val if num and pp.numPr.ilvl is not None else 0
        stream.append(('p', t, b, num, lvl))
    elif el.tag.endswith('}tbl'):
        tb = docx.table.Table(el, d)
        stream.append(('t', [[re.sub(r'[ \t]+', ' ', c.text).strip() for c in r.cells] for r in tb.rows]))

UNIT = re.compile(r'^unit\s*[-:;]?\s*(\d+)\s*[-:;]?\s*(.*)$', re.I)
GRADE = re.compile(r'^history grade (9|10|11)$|^history grade (\d+)$', re.I)
LES = re.compile(r'^(\d+\.\s?\d+)\.?\s+(\S.*)$')
def is_head(t, b, num, lvl):
    if len(t) > 100 or t.startswith('*'): return False
    if LES.match(t): return True
    if b and not re.match(r'^\d+\.\s', t) or (b and len(t) < 60): return True
    return len(t) <= 70 and t.isupper() and len(t) > 3
grades = {}; g = None; unit = None; issues = []
for it in stream:
    if it[0] == 'p':
        t = it[1]
        m = re.match(r'^history grade\s*(\d+)$', t, re.I)
        if m: g = int(m.group(1)); grades[g] = []; continue
        m = UNIT.match(t)
        if m and g:
            ttl = m.group(2).strip(' -;:'); extra = re.search(r'\s(\d+\.\s?\d+)\.?\s+(\S.*)$', ttl)
            unit = dict(num=int(m.group(1)), title=ttl[:extra.start()].strip() if extra else ttl, items=[]); grades[g].append(unit)
            if extra: unit['items'].append(('p', extra.group(1) + ' ' + extra.group(2), True, False, 0))
            continue
    if unit is None: continue
    unit['items'].append(it)

def clean_title(t): return t.strip().rstrip(';:,-').strip()
def build_unit(g, u, old):
    uid = f'hist{g}-u{u["num"]}'; pg = old['pages'][0]
    nles = sum(1 for it in u['items'] if it[0] == 'p' and LES.match(it[1]) and len(it[1]) <= 100)
    nles += sum(1 for it in u['items'] if it[0] == 'p' and it[2] and it[3] and it[4] >= 1 and len(it[1]) < 70 and not LES.match(it[1]))
    lessons = []; cur = None; card = None
    def new_lesson(num, title):
        nonlocal cur, card
        cur = dict(number=num, title=title, cards=[]); lessons.append(cur); card = None
    def new_card(title):
        nonlocal card
        if cur is None: new_lesson('', u['title'])
        card = dict(title=title, body=[], table=None); cur['cards'].append(card)
    for it in u['items']:
        if it[0] == 't':
            if cur is None: new_lesson('', u['title'])
            tc = dict(title=(card['title'] if card else cur['title']), body=[], table=it[1]); cur['cards'].append(tc); card = None; continue
        _, t, b, num, lvl = it
        m = LES.match(t)
        lesson_head = (m and len(t) <= 100) or (b and num and lvl >= 1 and len(t) < 70)
        if nles < 2 and is_head(t, b, num, lvl):
            lesson_head = True; m = None
        if lesson_head:
            new_lesson(m.group(1).replace(' ', '') if m else '', clean_title(m.group(2) if m else t)); continue
        if is_head(t, b, num, lvl):
            new_card(clean_title(t)); continue
        if card is None: new_card(cur['title'] if cur else u['title'])
        card['body'].append(t)
    # merge empty heading cards into the next card's title
    out = []; ci = 0
    for li, L in enumerate(lessons, 1):
        cards = []; pend = []
        for c in L['cards']:
            if not c['body'] and not c['table']: pend.append(c['title']); continue
            if pend: c = dict(c, title=' – '.join(pend + [c['title']]) if c['title'] not in pend else c['title']); pend = []
            cards.append(c)
        if pend:
            if cards: cards[-1]['body'].append(' – '.join(pend))
            else: issues.append(f'G{g} U{u["num"]}: heading(s) with no text: {pend}'); continue
        if not cards: continue
        lid = f'{uid}-t{len(out)+1}'; jc = []
        for c in cards:
            ci += 1; cid = f'{uid}-n{ci:02d}'
            if c['table']:
                jc.append(dict(id=cid, type='table', title=c['title'], page=pg, src='notes', head=c['table'][0], rows=c['table'][1:]))
            else:
                jc.append(dict(id=cid, type='text', title=c['title'], page=pg, src='notes', body=c['body']))
        num = L['number'] or str(len(out) + 1)
        out.append(dict(id=lid, number=num, title=L['title'], pages=list(old['pages']), cards=jc))
    return uid, out

STOP = set('the of and in to a was were is are by for on as with from that its it his their an at be this which or had have has who also they into been not but after during'.split())
def toks(s): return [w for w in re.findall(r"[a-z][a-z'’-]+", s.lower()) if w not in STOP and len(w) > 2]
def sentences(text): return [s.strip() for s in re.split(r'(?<=[a-z\)])\.\s+(?=[A-Z])', text) if 25 <= len(s.strip()) <= 300]
DEF = re.compile(r"^((?:The |An? )?[A-Z][\w’'\-]+(?: [A-Z(][\w’'\-)]+){0,4}) (is|was|were|are) ((?:the|a|an|one|known|called) .+)$")
PROPER = re.compile(r"\b[A-Z][a-z’'\-]+(?: (?:of |the |de )?[A-Z][a-z’'\-]+)*")
COMMON = set('The A An In On At By It He She They This These Those His Her Their During After Before When While However Since Also Although But And Some Many Most First Second Third Finally Then Thus So As For From With Europe Europeans'.split()) - {'Europe', 'Europeans'}
YEAR = re.compile(r'\b(1[0-9]{3}|20[0-2][0-9])\b')
def make_questions(uid, lessons, pg):
    cands = []
    for L in lessons:
        for c in L['cards']:
            for p in c.get('body', []):
                for s in sentences(p):
                    s = s.rstrip('.;: ')
                    m = DEF.match(s)
                    if m and len(m.group(1)) <= 45:
                        cands.append((0, s, m.group(1), '____ ' + m.group(2) + ' ' + m.group(3) + '.', c)); continue
                    ys = set(YEAR.findall(s))
                    if len(ys) == 1 and len(YEAR.findall(s)) == 1:
                        y = ys.pop(); cands.append((1, s, y, YEAR.sub('____', s) + '.', c)); continue
                    for m in PROPER.finditer(s):
                        a = m.group(0)
                        if m.start() > 0 and a.split()[0] not in COMMON and len(a) >= 4 and s.count(a) == 1:
                            cands.append((2 if ' ' in a else 3, s, a, s[:m.start()] + '____' + s[m.end():] + '.', c)); break
    seen = set(); qs = []
    BAN = {'Therefore', 'Moreover', 'However', 'Decline', 'Economy', 'Causes', 'Effects'}
    for kind, s, ans, q, c in sorted(cands, key=lambda x: x[0]):
        if ans.lower() in seen or s in seen: continue
        if not s[0].isupper() or re.match(r'^[A-Za-z0-9]{1,2}[\).]\s', s) or '-' in ans.replace('Pan-', '') or set(ans.split()) & BAN or 'Africa before 1000 years' in s: continue
        seen.add(ans.lower()); seen.add(s); qs.append((s, ans, q, c))
    pool = [a for _, a, _, _ in qs]
    qs = [x for x in qs if sum(1 for a in pool if a != x[1] and a.isdigit() == x[1].isdigit()) >= 3]
    sel = qs[:12]
    def choices(ans):
        same = [a for a in pool if a != ans and a.isdigit() == ans.isdigit()]
        import random; rnd = random.Random(ans); ch = rnd.sample(same, min(3, len(same))) + [ans]; rnd.shuffle(ch); return ch
    res = []
    for i, (s, ans, q, c) in enumerate(sel, 1):
        res.append(dict(id=f'{uid}-q{i:02d}', type='fill', q=f'Complete from the notes: {q}', answer=ans, accept=[ans], choices=choices(ans), page=pg, src='notes', why=[f'Teachers\u2019 notes ({c["title"]}): {s}.'], why_src='notes', answer_src='notes',
            tip=f'Re-read the card \u201c{c["title"]}\u201d.', similar=[dict(q=f'Write the full sentence from the notes that contains \u201c{ans}\u201d.', a=s + '.')]))
    return res

def unit_map(uid, title, lessons):
    nodes = [dict(id='unit', label=title[:40], kind='unit', cards=[lessons[0]['cards'][0]['id']])]; edges = []
    for li, L in enumerate(lessons, 1):
        tid = f't{li}'; nodes.append(dict(id=tid, label=L['title'][:40], kind='topic', lesson=L['id'], cards=[c['id'] for c in L['cards']]))
        edges.append({'from': 'unit', 'to': tid, 'label': 'topic'})
        for ci, c in enumerate([c for c in L['cards'] if c['title'] != L['title']][:4], 1):
            nid = f'{tid}_k{ci}'; nodes.append(dict(id=nid, label=c['title'][:40], kind='idea', cards=[c['id']]))
            edges.append({'from': tid, 'to': nid, 'label': 'includes'})
    return dict(root='unit', src='auto', nodes=nodes, edges=edges)

schema = json.load(open(f'{N}/notes_schema.json')); V = jsonschema.Draft202012Validator(schema)
ix = json.load(open(f'{OLD}/index.json')); report = {}
for g in (9, 10, 11):
    oldb = json.load(open(f'{OLD}/history_{g}.json')); oldu = {u['number']: u for u in oldb['units']}
    units = []; outline = []
    if [u['num'] for u in grades[g]] != sorted(oldu): issues.append(f'G{g}: docx units {[u["num"] for u in grades[g]]} vs textbook units {sorted(oldu)}')
    for u in grades[g]:
        o = oldu[u['num']]; uid, lessons = build_unit(g, u, o)
        title = o['title'] if u['title'].lower().replace(' ', '') == o['title'].lower().replace(' ', '') else u['title']
        title = o['title']  # textbook unit title (the handout's unit lines vary in spelling/case)
        if u['title'].lower() != o['title'].lower(): issues.append(f'{uid}: handout unit line \u201c{u["title"]}\u201d \u2192 textbook title \u201c{o["title"]}\u201d used')
        pg = o['pages'][0]; allc = [c for L in lessons for c in L['cards']]
        qs = make_questions(uid, lessons, pg)
        if len(qs) < 8: issues.append(f'{uid}: only {len(qs)} cloze questions could be taken verbatim from the notes')
        tips = []
        for L in lessons:
            c = next((c for c in L['cards'] if c['type'] == 'text'), None)
            if c and len(tips) < 4: tips.append(dict(text=c['body'][0], page=pg, src='notes', card=c['id']))
        fl = [dict(front=c['title'], back=c['body'][0]) for c in allc if c['type'] == 'text' and c['title'] != c['body'][0]][:8]
        games = [dict(id=f'{uid}-g1', type='flash', title='Flash cards: headings and notes', lesson=None, src='notes', cards=fl)] if len(fl) >= 3 else []
        if len(qs) >= 3: games.append(dict(id=f'{uid}-g2', type='fill', title='Fill the gap from the notes', lesson=None, src='notes', items=[dict(text=q['q'].replace('Complete from the notes: ', ''), answer=q['answer'], choices=q['choices']) for q in qs[:6]]))
        U = dict(id=uid, number=u['num'], title=title, status='done', pages=list(o['pages']), **({'tone': o['tone']} if 'tone' in o else {}),
                 lessons=lessons, glossary=[], tips=tips, games=games, exercise=dict(questions=qs), unitMap=unit_map(uid, title, lessons))
        units.append(U); outline.append(dict(level=1, text=f'Unit {u["num"]}: {title}'))
        outline += [dict(level=2, text=(L['number'] + ' ' if '.' in L['number'] else '') + L['title']) for L in lessons]
    b = oldb['book']
    book = dict(id=f'history_{g}', subject='history', grade=g, title=f'History Grade {g}', pdf=b['pdf'], page_offset=b['page_offset'], lang='en',
                source='Teacher-prepared, verified History notes (docx handout, Grades 9\u201311); text kept as written by the teachers. Page numbers are the textbook unit ranges (the handout has no pages).',
                intro=[f'Eritrea \u00b7 Grade {g} \u00b7 History', 'Teacher-prepared, verified notes'], source_outline=outline)
    B = {'$schema': oldb.get('$schema', '../notes_schema.json'), 'book': book, 'units': units}
    errs = sorted(V.iter_errors(B), key=lambda e: list(e.path))
    for e in errs[:15]: print('SCHEMA', g, list(e.path), e.message[:200])
    if errs: raise SystemExit('invalid')
    json.dump(B, open(f'{NB}/history_{g}.json', 'w'), ensure_ascii=False, indent=1)
    ix['grades'][str(g)]['history'] = dict(book=book['id'], file=f'history_{g}.json', title=book['title'], units=[dict(id=U['id'], number=U['number'], title=U['title'], pages=U['pages'], questions=len(U['exercise']['questions']),
        topics=[dict(id=l['id'], number=l['number'], title=l['title'], page=l['pages'][0], cards=[c['id'] for c in l['cards']]) for l in U['lessons']]) for U in units])
    report[g] = [dict(id=U['id'], title=U['title'], lessons=len(U['lessons']), cards=sum(len(l['cards']) for l in U['lessons']), questions=len(U['exercise']['questions']), lesson_titles=[l['number'] + ' ' + l['title'] for l in U['lessons']]) for U in units]
    globals().setdefault('BOOKS', {})[g] = B
IS = json.load(open(f'{N}/notes_index_schema.json'))
for e in list(jsonschema.Draft202012Validator(IS).iter_errors(ix))[:10]: print('INDEX', list(e.path), e.message[:200])
json.dump(ix, open(f'{NB}/index.json', 'w'), ensure_ascii=False, indent=1)

# placements: drop quick checks pointing at the old history 9-11 lessons
pl = json.load(open(f'{OLD}/placements.json')); n0 = len(pl['cards'])
pl['cards'] = [c for c in pl['cards'] if not re.match(r'^hist(9|10|11)-', c.get('lesson', ''))]
json.dump(pl, open(PL, 'w'), ensure_ascii=False, indent=1); report['placements_removed'] = n0 - len(pl['cards'])

# re-link matric questions by topic (TF-IDF cosine on the new teacher text)
uq = json.load(open(f'{OLD}/unit_questions.json'))
stem = {}
for f in os.listdir(f'{R}/assets/high/exams'):
    if re.match(r'history_\d+_matric\.json$', f):
        for q in json.load(open(f'{R}/assets/high/exams/{f}'))['questions']:
            opts = q.get('options') or {}
            stem[q['id']] = ' '.join([q.get('stem', '')] + (list(opts.values()) if isinstance(opts, dict) else []) + list(q.get('keywords') or []))
docs = {}
for g, B in BOOKS.items():
    for U in B['units']:
        docs[U['id']] = ' '.join([U['title']] * 3 + [l['title'] for l in U['lessons']] + [c.get('title', '') + ' ' + ' '.join(c.get('body', [])) + ' ' + ' '.join(' '.join(r) for r in c.get('rows', [])) for l in U['lessons'] for c in l['cards']])
df = collections.Counter(w for t in docs.values() for w in set(toks(t))); Nd = len(docs)
def vec(t):
    c = collections.Counter(toks(t)); v = {w: (1 + math.log(n)) * math.log((Nd + 1) / (df.get(w, 0) + 1)) for w, n in c.items() if w in df}
    s = math.sqrt(sum(x * x for x in v.values())) or 1; return {w: x / s for w, x in v.items()}
DV = {k: vec(t) for k, t in docs.items()}
def sims(t):
    q = vec(t); return sorted(((sum(x * DV[k].get(w, 0) for w, x in q.items()), k) for k in DV), reverse=True)
moved = []; agree = tot = 0
for k in [k for k in uq['units'] if re.match(r'^hist(9|10|11)-u', k)]:
    keep = []
    for e in uq['units'][k]:
        s = sims(stem.get(e['id'], '')); best = s[0][1]; cur = next((x for x, kk in s if kk == k), 0); tot += 1; agree += best == k
        if e['confidence'] != 'high' and best != k and s[0][0] >= 0.12 and s[0][0] >= 1.5 * cur:
            e2 = dict(e, confidence='medium', via='topic (teacher notes)'); uq['units'][best].append(e2); moved.append((e['id'], k, best)); continue
        keep.append(e)
    uq['units'][k] = keep
um = []
for e in uq['unmapped']:
    if e['subject'] == 'history':
        s = sims(e.get('stem', '') + ' ' + stem.get(e['id'], ''))
        if s[0][0] >= 0.15 and s[0][0] >= 1.5 * s[1][0]:
            uq['units'][s[0][1]].append(dict(id=e['id'], confidence='low', via='topic (teacher notes)', exam=e['id'].split('-p')[0].replace('hist-', 'history_').replace('-', '_'))); moved.append((e['id'], 'unmapped', s[0][1])); continue
    um.append(e)
uq['unmapped'] = um; uq['unmapped_count'] = len(um); uq['mapped'] = sum(len(v) for v in uq['units'].values())
st = collections.Counter(e['confidence'] for k, v in uq['units'].items() if k.startswith('hist') for e in v)
uq['stats']['history'] = dict(mapped=sum(st.values()), high=st['high'], medium=st['medium'], low=st['low'], unmapped=sum(1 for e in um if e['subject'] == 'history'))
json.dump(uq, open(f'{N}/unit_questions.json', 'w'), ensure_ascii=False, indent=1)
report['matric'] = dict(checked=tot, topic_agrees_with_link=agree, moved=moved, stats=uq['stats']['history'])
report['issues'] = issues
json.dump(report, open(f'{R}/tool/history/report.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps({g: [(u['id'], u['lessons'], u['cards'], u['questions']) for u in report[g]] for g in (9, 10, 11)}))
print(report['placements_removed'], json.dumps(report['matric'])[:1500]); print('\n'.join(issues))
