"""Builds assets/high/notes/notes/english_<g>.json (grammar only) from compact unit specs, registers it in index.json,
maps matching English matric questions in unit_questions.json, validates, and rebuilds the update zip. Re-running a grade
rebuilds its book from scratch (idempotent)."""
import json, re, os, glob, zipfile
try:
    import jsonschema
except ImportError:
    jsonschema = None
P = '/workspace/bee-plus-four/'; N = P + 'assets/high/notes/'
TONES = ['sage', 'peach', 'butter', 'blue', 'lilac', 'mint']
def G(title, rule, examples, pattern=None, body=None):
    return dict(title=title, rule=rule if isinstance(rule, list) else [rule], examples=examples, pattern=pattern, body=body)
def U(num, title, pages, intro, grammar, table, mist, tip, summary, Q, S, match=(), terms=()):
    return dict(num=num, title=title, pages=pages, intro=intro, grammar=grammar, table=table, mist=mist, tip=tip, summary=summary, Q=Q, S=S, match=match, terms=terms)
def build(grade, title, units, outline_src):
    p = f'eng{grade}'; book = dict(id=f'english_{grade}', subject='english', grade=grade, title=f'English Grade {grade} \u00b7 Grammar', pdf=f'textbook_english_{grade}.pdf', page_offset=0,
        source=f'Grammar sections of English for Eritrea Grade {grade} Textbook (Ministry of Education, 2011); topics from the textbook Book Map. {outline_src}', lang='en',
        intro=[f'Eritrea \u00b7 Ministry of Education \u00b7 English for Eritrea Grade {grade}', 'Grammar notes and practice for every unit'])
    out = []
    for k, s in enumerate(units):
        uid = f'{p}-u{s["num"]}'; c = [0]
        def cid(): c[0] += 1; return f'{uid}-c{c[0]:02d}'
        pg = s['pages'][0]; lessons = []; nodes = [dict(id='unit', label=s['title'][:28], kind='unit', cards=[])]; edges = []
        for j, g in enumerate(s['grammar']):
            cards = []
            gc = dict(id=cid(), type='grammar', title=g['title'], page=pg, src='notes', rule=g['rule'], examples=[dict(text=t, ok=ok, **({'fix': f} if f else {})) for t, ok, f in g['examples']])
            if g['pattern']: gc['pattern'] = g['pattern']
            if g['body']: gc['body'] = g['body']
            cards.append(gc)
            if j == 0:
                h, rows = s['table']; cards.append(dict(id=cid(), type='table', title='Forms and examples', page=pg, src='notes', head=h, rows=rows))
            if j == len(s['grammar']) - 1:
                cards.append(dict(id=cid(), type='table', title='Common mistakes', page=pg, src='notes', head=['Wrong', 'Right', 'Why'], rows=[list(m) for m in s['mist']]))
                cards.append(dict(id=cid(), type='mnemonic', title='Memory tip', page=pg, src='notes', body=[s['tip']]))
                cards.append(dict(id=cid(), type='remember', title='Unit summary', page=pg, src='notes', body=[s['summary']]))
            lid = f'{uid}-l{s["num"]}-{j+1}'; lessons.append(dict(id=lid, number=f'{s["num"]}.{j+1}', title=g['title'], pages=s['pages'], cards=cards))
            nid = f'l{s["num"]}_{j+1}'; nodes.append(dict(id=nid, label=g['title'][:28], kind='topic', lesson=lid, cards=[x['id'] for x in cards])); edges.append({'from': 'unit', 'to': nid, 'label': 'includes'})
            nodes[0]['cards'].append(cards[0]['id'])
        qs = []; S = s['S']
        for i, q in enumerate(s['Q']):
            sim = [{'q': S[(i + t) % len(S)][0], 'a': S[(i + t) % len(S)][1]} for t in range(2 if i < len(S) else 1)]
            base = dict(id=f'{uid}-q{i+1:02d}', q=q[1], src='notes', page=pg, label=f'{i+1}. {q[1][:60]}', similar=sim)
            if q[0] == 'm':
                _, qq, opts, ans, why = q; assert ans in 'ABCD'[:len(opts)], q
                base.update(type='mcq', options=dict(zip('ABCD', opts)), answer=ans, why=[f'Answer {ans}: {opts["ABCD".index(ans)]}'] + why.split(' | '), tip='Read the whole sentence, find the clue word, then test each option.')
            else:
                _, qq, ans, choices, why = q; assert ans in choices, q; assert '____' in qq, q
                base.update(type='fill', answer=ans, choices=choices, why=why.split(' | '), tip='Say the sentence aloud with your answer; it must be grammatical and make sense.')
            qs.append(base)
        h, rows = s['table']; pairs = [{'a': r[0][:40], 'b': r[1][:60]} for r in rows[:6]]
        pairs = pairs if len(pairs) >= 3 else [{'a': 'form', 'b': 'example'}, {'a': 'rule', 'b': 'use'}, {'a': 'check', 'b': 'revise'}]
        games = [dict(id=f'{uid}-g1', type='match', title='Match the form to its example', src='notes', lesson=lessons[0]['id'], pairs=pairs)]
        out.append(dict(id=uid, number=s['num'], title=s['title'], status='done', pages=s['pages'], tone=TONES[k % 6], intro=s['intro'], intro_page=pg, lessons=lessons,
            glossary=[dict(term=t, meaning=m, page=pg, src='notes') for t, m in s['terms']], tips=[dict(text=s['tip'], page=pg, src='notes')], games=games, exercise=dict(questions=qs),
            unitMap=dict(root='unit', src='hand', nodes=nodes, edges=edges)))
    d = {'$schema': '../notes_schema.json', 'book': book, 'units': out}
    sch = json.load(open(N + 'notes_schema.json'))
    if 'english' not in sch['properties']['book']['properties']['subject']['enum']:
        sch['properties']['book']['properties']['subject']['enum'].append('english'); json.dump(sch, open(N + 'notes_schema.json', 'w'), ensure_ascii=False, indent=1)
    errs = []
    if jsonschema is not None:
        errs = list(jsonschema.Draft202012Validator(sch).iter_errors(d))
        for e in errs[:12]: print('SCHEMA', list(e.path), e.message[:220])
        if errs: raise SystemExit('invalid')
    else:
        print('jsonschema not installed; skipping schema validate')
    json.dump(d, open(N + f'notes/english_{grade}.json', 'w'), ensure_ascii=False, indent=1)
    # index
    ix = json.load(open(N + 'notes/index.json'))
    ix['grades'].setdefault(str(grade), {})['english'] = dict(book=book['id'], file=f'english_{grade}.json', title=book['title'], units=[dict(id=u['id'], number=u['number'], title=u['title'], pages=u['pages'], questions=len(u['exercise']['questions']),
        topics=[dict(id=l['id'], number=l['number'], title=l['title'], page=l['pages'][0], cards=[c['id'] for c in l['cards']]) for l in u['lessons']]) for u in out])
    if jsonschema is not None:
        errs = list(jsonschema.Draft202012Validator(json.load(open(N + 'notes_index_schema.json'))).iter_errors(ix))
        if errs: raise SystemExit('index invalid: ' + errs[0].message)
    json.dump(ix, open(N + 'notes/index.json', 'w'), ensure_ascii=False, indent=1)
    # keep english_index.json in sync for NotesRepo overlay
    eix_path = N + 'notes/english_index.json'
    try:
        eix = json.load(open(eix_path))
    except Exception:
        eix = {'grades': {}}
    eix.setdefault('grades', {})[str(grade)] = {'english': ix['grades'][str(grade)]['english']}
    json.dump(eix, open(eix_path, 'w'), ensure_ascii=False, indent=1)
    # matric links (first matching unit wins; mapping kept in unit_questions.json)
    uq = json.load(open(N + 'unit_questions.json')); stem = {}
    for f in glob.glob(P + 'assets/high/exams/english_*.json'):
        for q in json.load(open(f))['questions']: stem[q['id']] = os.path.basename(f)[:-5]
    keep, n = [], 0
    for q in uq['unmapped']:
        hit = None
        if q.get('subject') == 'english':
            for s in units:
                if any(re.search(rx, q.get('topic', ''), re.I) for rx in s['match']): hit = f'{p}-u{s["num"]}'; break
        if hit and q['id'] in stem:
            uq['units'].setdefault(hit, []).append(dict(id=q['id'], confidence='medium', via='topic', exam=stem[q['id']])); n += 1
        else: keep.append(q)
    uq['unmapped'] = keep; uq['mapped'] += n; uq['unmapped_count'] = len(keep)
    st = uq['stats'].setdefault('english', {}); st['unmapped'] = sum(1 for q in keep if q.get('subject') == 'english'); st['mapped'] = st.get('mapped', 0) + n; st['medium'] = st.get('medium', 0) + n
    json.dump(uq, open(N + 'unit_questions.json', 'w'), ensure_ascii=False, indent=1)
    log = P + 'tool/english/done.json'; dn = json.load(open(log)) if os.path.exists(log) else {}
    dn[str(grade)] = dict(units=[f'{u["id"]} {u["title"]}: ' + '; '.join(l['title'] for l in u['lessons']) for u in out], questions=sum(len(u['exercise']['questions']) for u in out), matric=dn.get(str(grade), {}).get('matric', 0) + n)
    json.dump(dn, open(log, 'w'), indent=1)
    z = zipfile.ZipFile('/workspace/High-english-grammar-update.zip', 'w', zipfile.ZIP_DEFLATED)
    for g in dn: z.write(N + f'notes/english_{g}.json', f'assets/high/notes/notes/english_{g}.json')
    for f in ['assets/high/notes/notes/index.json', 'assets/high/notes/unit_questions.json', 'assets/high/notes/notes_schema.json'] + [x[len(P):] for x in glob.glob(P + 'tool/english/*.py')] + ['tool/english/done.json']: z.write(P + f, f)
    z.writestr('README.md', '# High: English grammar (Grades 9\u201312)\n\nMerge: unzip over the high_flutter project root (paths mirror the project), then `flutter pub get && flutter analyze && flutter test`.\n\n'
        '- New books: assets/high/notes/notes/english_<grade>.json (grammar only), validated against notes_schema.json; the only schema change is `english` added to book.subject.\n'
        '- index.json gains grades.<g>.english; unit_questions.json maps matching English matric questions (topic match, confidence medium) to the new units and removes them from `unmapped`.\n'
        '- No Dart change was needed: `english` is already registered in lib/high/notes/jr/data/subjects.dart (name, icon, order) and labels.dart.\n'
        '- Rebuild a grade with `python3 tool/english/eng<g>.py` (idempotent for the book; matric mapping only moves still-unmapped questions).\n\n## Units\n'
        + ''.join(f'\n### Grade {g} ({v["questions"]} exercises, {v["matric"]} matric links)\n' + ''.join(f'- {x}\n' for x in v['units']) for g, v in sorted(dn.items(), key=lambda x: int(x[0]))))
    z.close(); print(f'grade {grade}: {len(out)} units, {dn[str(grade)]["questions"]} questions, {n} matric links; zip rebuilt')
