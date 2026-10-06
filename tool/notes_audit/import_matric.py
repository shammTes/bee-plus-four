"""Fill lessons with < 3 quick checks (and units with < 20 exercise questions) with past matric / model exam MC
questions from the Drive question bank, matched to the best lesson by TF-IDF similarity over the lesson text.
Usage: python3 import_matric.py [--dry] subject ..."""
import sys, os, json, re, math, collections
sys.path.insert(0, os.path.dirname(__file__))
from patch import Book, check, mcq
SRC = '/workspace/tmp-sync/drive/Matric_Questions.json'
SUBJ = {'biology': ['Biology'], 'chemistry': ['Chemistry'], 'geography': ['Geography'], 'agriculture': ['Agriculture'],
        'business_economics': ['Business and Economics', 'Business & Economics'], 'english': ['English', 'English Language']}
BAD = re.compile(r'diagram|figure|\bfig\b|graph|\bmap\b|passage|table|shown|below|above|following (?:text|paragraph|sentence pair)|underlined|picture|illustrat|\bletter[s]? [A-Z]\b|marked|labell?ed|column|curve|chart|photo|given data|in the box', re.I)
STOP = set('the a an of to in and or is are was were be by for on with as at that this which what from it its their his her who whom whose not no all any one two can may has have had do does did will would should could most more less than into each other such these those when where how why about between also only'.split())

def toks(s):
    s = re.sub(r'\$\$.*?\$\$', ' ', s or '')
    return [w for w in re.findall(r"[a-z][a-z\-']+", s.lower()) if w not in STOP and len(w) > 2]

def card_text(c):
    out = []
    def w(o):
        if isinstance(o, str): out.append(o)
        elif isinstance(o, dict): [w(v) for k, v in o.items() if k not in ('id', 'src', 'type', 'page')]
        elif isinstance(o, list): [w(v) for v in o]
    w(c); return ' '.join(out)

def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())[:70]

def load_questions(subject):
    m = json.load(open(SRC)); seen = set(); out = []
    for p in m['papers']:
        if p['subject'] not in SUBJ[subject]:
            continue
        for q in p['questions']:
            if q.get('type') != 'MC' or q.get('context'):
                continue
            opts = {}
            for o in q.get('options') or []:
                mm = re.match(r'\s*([A-E])[.)]\s*(.+)', o or '')
                if mm: opts[mm.group(1)] = mm.group(2).strip()
            ans = (q.get('correct_answer') or '').strip()[:1]
            exp = (q.get('explanation') or '').strip()
            qt = (q.get('question') or '').strip()
            if len(opts) < 4 or ans not in opts or len(exp) < 40 or len(qt) < 15:
                continue
            if re.search(r'blank\s*\**\s*\d+|^\s*\d+\s*\.|\bpoints? [A-Z]\b|between the points|^\s*\*\*[^*]+\*\*\s*$', qt):
                continue
            if BAD.search(qt) or any(BAD.search(v) for v in opts.values()) or '___' * 8 in qt:
                continue
            if any(len(v) > 160 for v in opts.values()):
                continue
            k = norm(qt)
            if k in seen:
                continue
            seen.add(k)
            fx = lambda t: re.sub(r'(?<!\$)\$(?!\$)([^$\n]{1,60}?)(?<!\$)\$(?!\$)', r'$$\1$$', t)
            qt, exp = fx(qt), fx(exp)
            opts = {k: fx(v) for k, v in opts.items()}
            out.append({'id': q['id'], 'q': qt, 'opts': opts, 'ans': ans, 'why': exp, 'topic': q.get('topic') or '', 'year': p['year']})
    return out

def run(subject, dry=False, need_checks=3, need_ex=20, thr=0.15):
    books = sorted(f[:-5] for f in os.listdir(os.path.join(os.path.dirname(__file__), '../../assets/high/notes/notes'))
                   if re.fullmatch(subject + r'_\d+\.json', f))
    B = {bk: Book(bk) for bk in books}
    existing = set()
    for b in B.values():
        for s in re.findall(r'"(?:q|problem)": "([^"]{15,})', json.dumps(b.d, ensure_ascii=False)):
            existing.add(norm(s))
    docs = []  # (bk, unit, lesson)
    for bk, b in B.items():
        for u in b.d['units']:
            for l in u['lessons']:
                text = (l.get('title', '') + ' ') * 3 + (u.get('title', '') + ' ') + ' '.join(card_text(c) for c in l['cards'])
                docs.append((bk, u, l, collections.Counter(toks(text))))
    df = collections.Counter()
    for *_, tf in docs:
        df.update(tf.keys())
    N = len(docs)
    idf = {w: math.log((N + 1) / (n + 1)) + 1 for w, n in df.items()}
    def vec(tf):
        v = {w: (1 + math.log(c)) * idf.get(w, math.log(N + 1) + 1) for w, c in tf.items()}
        nrm = math.sqrt(sum(x * x for x in v.values())) or 1
        return {w: x / nrm for w, x in v.items()}
    dv = [vec(tf) for *_, tf in docs]
    qs = [q for q in load_questions(subject) if norm(q['q']) not in existing]
    assign = collections.defaultdict(list)
    for q in qs:
        qv = vec(collections.Counter(toks((q['q'] + ' ') * 2 + ' '.join(q['opts'].values()) + ' ' + (q['topic'] + ' ') * 2 + q['why'][:200])))
        sc = [(sum(x * d.get(w, 0) for w, x in qv.items()), i) for i, d in enumerate(dv)]
        sc.sort(reverse=True)
        best, i = sc[0]
        if best >= thr and best - sc[1][0] > 0.01:
            assign[i].append((best, q))
    stats = collections.Counter(); used = set()
    for i, (bk, u, l, _) in enumerate(docs):
        cand = sorted(assign.get(i, []), key=lambda x: -x[0])
        have = sum(c.get('type') == 'check' for c in l['cards'])
        add = []
        while have + len(add) < need_checks and cand:
            s, q = cand.pop(0)
            add.append(check(f"{l['id']}-mx{len(add)+1}", q['q'], q['opts'], q['ans'], q['why'], src='matric', src_qid=q['id']))
            used.add(q['id']); stats[bk + ' checks'] += 1
            if dry: print(f'  [{s:.2f}] {bk} {l["title"][:40]!r} <- {q["q"][:90]!r}')
        if add and not dry:
            B[bk].add(l['id'], add)
        assign[i] = cand
    for bk, b in B.items():
        for u in b.d['units']:
            ex = u.setdefault('exercise', {}).setdefault('questions', [])
            if len(ex) >= need_ex:
                continue
            lids = {l['id'] for l in u['lessons']}
            pool = sorted([x for i, (bk2, u2, l2, _) in enumerate(docs) if bk2 == bk and l2['id'] in lids for x in assign.get(i, [])], key=lambda x: -x[0])
            new = []
            for s, q in pool:
                if len(ex) + len(new) >= need_ex: break
                if q['id'] in used: continue
                used.add(q['id'])
                new.append(mcq(f"{u['id']}-mx{len(new)+1}", q['q'], q['opts'], q['ans'], q['why'],
                               'Read every option before choosing; rule out the ones that contradict the notes.', src='matric', src_qid=q['id'], exam_question=q['id']))
                stats[bk + ' exercise'] += 1
                if dry: print(f'  EX [{s:.2f}] {bk} {u["title"][:30]!r} <- {q["q"][:90]!r}')
            if new and not dry:
                b.ex(u['id'], new)
    if not dry:
        for b in B.values():
            b.save()
    print(subject, dict(stats), 'questions available', len(qs))

if __name__ == '__main__':
    args = sys.argv[1:]
    dry = '--dry' in args
    for s in [a for a in args if not a.startswith('--')]:
        run(s, dry)
