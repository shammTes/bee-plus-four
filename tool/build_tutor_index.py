#!/usr/bin/env python3
"""Build the offline Tutor search index (assets/high/tutor/tutor_index.bin) from everything the app ships.

Sources (all read from the repo, nothing downloaded):
  * notes books assets/high/notes/notes/<subject>_<grade>.json, with each unit replaced by unit_<id>.json when present
    (exactly like NotesRepo), indexed per card (text, remember, mnemonic, worked, table, grammar, diagram, reading,
    check) plus unit intros, glossary terms, tips and unit-quiz questions
  * media / lab cards injected from assets/high/media/{placements,taxonomy_extra,g11_extra,commons_extra}.json
    (deep link = their card position inside the lesson)
  * exam-pack concepts (assets/high/exams/topics_index*.json)
  * exercise bank (assets/high/exercises/*.json and exercises/school/*.json)
  * matric / model papers (assets/high/exams/<files listed in index.json>) and the lazy packs
    (assets/high/exams/matric_lazy/subjects/*.json), mapped to notes units via assets/high/notes/unit_questions.json

Output: a gzip'd little-endian binary (see lib/high/tutor/tutor_index.dart for the reader):
  'KTI1' u32 version | u32 metaLen meta-JSON | u32 nDocs | kind u8[n] subj u8[n] grade u8[n] (pad 2)
  unit u16[n] lesson u16[n] pos u16[n] len u16[n] | u32 keysLen keys utf8 ('\\n' separated)
  | u32 nTerms | u32 termsLen terms utf8 ('\\n' separated, sorted) | (pad 4) u32 off[nTerms+1] | postings
  postings per term: (varint docId delta, u8 tf)*
and tool/tutor_index_sources.json (sha256 of every source file; test/tutor_index_test.dart fails when it is stale).

Re-run after any content change:   python3 tool/build_tutor_index.py
"""
import glob
import gzip
import hashlib
import json
import os
import re
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = 'assets/high/tutor/tutor_index.bin'
MANIFEST = 'tool/tutor_index_sources.json'
CONCEPTS = 'assets/high/tutor/tutor_concepts.json'  # concept texts, read only when a concept is the answer
VERSION = 1
MAX_TOKENS = 400

# ------------------------------------------------------------------ tokenizer (mirrored in lib/high/tutor/tutor_text.dart)
SUB = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9', '⁰': '0', '¹': '1', '²': '2',
       '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁺': '+', '⁻': '-'}
STOP = sorted(set('''a an the of to in on for and or is are was were be been being by with what which who whom whose how why when where
does do did can could i me my you your it its this that these those as at from about explain tell define give please show help
want know find calculate describe meaning mean means state list name write discuss briefly short note notes using use used
following mention than then there their they them he she his her we our us if so but not no yes also into out up down over
such any all each some most more very will would should shall may might must let has have had having
'''.split()))
# query-time expansions (the left word is replaced by the right words); keys are stemmed when written to the index
SYN = {
    'ph': 'ph acidity', 'kmt': 'kinetic molecular theory', 'redox': 'oxidation reduction redox', 'halflife': 'halflife half life',
    'vsepr': 'vsepr shape geometry', 'dna': 'dna gene', 'gdp': 'gdp national income', 'adowa': 'adwa', 'adua': 'adwa',
    'ww1': 'first world war', 'wwi': 'first world war', 'ww2': 'second world war', 'wwii': 'second world war',
    'emf': 'emf electromotive force', 'pd': 'potential difference', 'tir': 'total internal reflection',
    'shm': 'simple harmonic motion', 'eqn': 'equation', 'formulae': 'formula', 'lab': 'lab simulation', 'sim': 'simulation', 'simulator': 'simulation', 'experiment': 'experiment lab',
}
SUBJECT_WORDS = {
    'physics': 'physics', 'chemistry': 'chemistry', 'biology': 'biology', 'mathematics': 'mathematics', 'geography': 'geography',
    'history': 'history', 'english': 'english', 'agriculture': 'agriculture', 'economics': 'business_economics',
    'business': 'business_economics', 'maths': 'mathematics', 'math': 'mathematics', 'econ': 'business_economics',
    'bio': 'biology', 'chem': 'chemistry', 'phys': 'physics', 'geo': 'geography', 'hist': 'history', 'agri': 'agriculture',
}
_split = re.compile('[^a-z0-9\u1200-\u137f]+')
_half = re.compile('half[- ]life')
_digit = re.compile('[0-9]')


def stem(w):
    n = len(w)
    if n > 4 and w.endswith('ies'):
        return w[:-3] + 'y'
    if n > 4 and w.endswith('sses'):
        return w[:-2]
    if n > 4 and w.endswith('es') and w[-4:-2] in ('sh', 'ch') or (n > 3 and w.endswith('es') and w[-3] in 'xz'):
        return w[:-2]
    if n > 3 and w.endswith('s') and not w.endswith(('ss', 'us', 'is')):
        return w[:-1]
    return w


def tokens(s):
    s = ''.join(SUB.get(ch, ch) for ch in s).lower()
    s = _half.sub('halflife', s)
    out = []
    for w in _split.split(s):
        if not w or w in STOP_SET:
            continue
        if len(w) == 1 and not _digit.search(w):
            continue
        if len(w) > 30:
            continue
        out.append(stem(w))
    return out


STOP_SET = set(STOP)

# ------------------------------------------------------------------ helpers
def load(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return json.load(f)


def exists(p):
    return os.path.exists(os.path.join(ROOT, p))


def flat(x):
    """every string inside a JSON value"""
    if x is None:
        return ''
    if isinstance(x, str):
        return x
    if isinstance(x, (int, float, bool)):
        return ''
    if isinstance(x, list):
        return ' '.join(flat(v) for v in x)
    if isinstance(x, dict):
        return ' '.join(flat(v) for k, v in x.items() if k not in ('id', 'src', 'svg', 'page', 'type', 'mode', 'diagram', 'img', 'file', 'kind'))
    return ''


def short(s, n=90):
    s = re.sub(r'\s+', ' ', re.sub(r'[#*_`]|\$\$?|\\[()\[\]]', '', s or '')).strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + '…'


EXAM_SUBJ = {'business and economics': 'business_economics', 'business & economics': 'business_economics'}


def subj_key(label):
    l = (label or '').strip().lower()
    return EXAM_SUBJ.get(l, re.sub('[^a-z]+', '_', l).strip('_') or 'general')


# kinds (keep in sync with TutorKind in lib/high/tutor/tutor_index.dart)
K = {'text': 0, 'remember': 1, 'mnemonic': 2, 'worked': 3, 'table': 4, 'grammar': 5, 'diagram': 6, 'reading': 7, 'check': 8,
     'steps': 0, 'states': 0, 'vocab': 5, 'model': 6, 'graph': 6,
     'glossary': 9, 'tip': 10, 'unitq': 11, 'intro': 12, 'media': 13, 'concept': 14,
     'exercise': 20, 'school': 21, 'exam': 22, 'lazy': 23}


class Builder:
    def __init__(self):
        self.subjects = []
        self.units = []      # [id, bookId, grade, subjIdx, number, title]
        self.unit_ix = {}
        self.lessons = []    # [id, unitIdx, number, title]
        self.concept_text = {}  # doc id -> [concept text, textbook ref]
        self.docs = []       # (kind, subj, grade, unit, lesson, pos, key, toks)
        self.qseen = set()
        self.qsig = set()

    def sidx(self, s):
        if s not in self.subjects:
            self.subjects.append(s)
        return self.subjects.index(s)

    def add(self, kind, subj, grade, unit, lesson, pos, key, text):
        toks = tokens(text)[:MAX_TOKENS]
        if not toks:
            return
        key = key.replace('\n', ' ').replace('\r', ' ')
        self.docs.append((K[kind], self.sidx(subj), grade or 0, 0xFFFF if unit is None else unit, 0xFFFF if lesson is None else lesson,
                          min(pos, 0xFFFF), key, toks))

    # -------------------------------------------------------------- notes
    def notes(self):
        base = 'assets/high/notes/notes'
        books = []
        seen = set()
        for ixf in ('index.json', 'english_index.json'):
            if not exists(f'{base}/{ixf}'):
                continue
            for g, subs in load(f'{base}/{ixf}')['grades'].items():
                for s, b in subs.items():
                    if b['book'] in seen:
                        continue
                    seen.add(b['book'])
                    books.append((int(g), s, b['book'], b['file']))
        books.sort()
        placements = []
        for p in ('placements', 'taxonomy_extra', 'g11_extra', 'commons_extra'):
            if exists(f'assets/high/media/{p}.json'):
                placements += [x for x in load(f'assets/high/media/{p}.json').get('cards', []) if isinstance(x, dict)]
        by_lesson = {}
        for x in placements:
            by_lesson.setdefault(str(x.get('lesson')), []).append(x.get('card') or {})
        for grade, subj, bid, file in books:
            raw = load(f'{base}/{file}')
            units = raw.get('units', [])
            for i, u in enumerate(units):
                if isinstance(u, dict) and u.get('id') and exists(f"{base}/unit_{u['id']}.json"):
                    try:
                        units[i] = load(f"{base}/unit_{u['id']}.json")
                    except Exception:
                        pass
            for u in units:
                if not isinstance(u, dict):
                    continue
                ui = len(self.units)
                self.unit_ix[u['id']] = ui
                self.units.append([u['id'], bid, grade, self.sidx(subj), u.get('number', 0), u.get('title', '')])
                ut = u.get('title', '')
                if u.get('intro'):
                    self.add('intro', subj, grade, ui, None, 0, f"Unit {u.get('number', '')}: {ut}", f"{ut} {ut} {u['intro']}")
                for l in u.get('lessons', []):
                    li = len(self.lessons)
                    self.lessons.append([l['id'], ui, str(l.get('number', '')), l.get('title', '')])
                    lt = l.get('title', '')
                    cards = l.get('cards', [])
                    for ci, c in enumerate(cards):
                        t = c.get('type')
                        title = c.get('title') or ''
                        if t == 'worked':
                            text = f"{title} {title} {title} {flat(c.get('problem'))} {flat(c.get('problem'))} {flat(c.get('steps'))} {flat(c.get('answer'))}"
                            key = title or short(flat(c.get('problem')))
                        elif t == 'check':
                            text = f"{title} {flat(c.get('q'))} {flat(c.get('q'))} {flat(c.get('options'))} {flat(c.get('why'))}"
                            key = short(flat(c.get('q'))) or title
                        else:
                            body = flat({k: v for k, v in c.items() if k != 'title'})
                            text = f"{title} {title} {title} {body}"
                            key = title or short(body)
                        self.add(t if t in K else 'text', subj, grade, ui, li, ci, key or lt, f"{lt} {text}")
                    for mi, m in enumerate(by_lesson.get(l['id'], [])):
                        title = m.get('title') or ''
                        kind = m.get('kind', '')
                        extra = {'sim': 'lab simulation interactive experiment', 'model': '3d model', 'photo': 'photo picture',
                                 'label': 'label diagram', 'quick': 'quick check', 'match': 'match game'}.get(kind, '')
                        sim = (m.get('sim') or '').replace('_', ' ')
                        text = f"{title} {title} {title} {flat(m.get('body'))} {sim} {extra} {lt}"
                        self.add('media', subj, grade, ui, li, len(cards) + mi, f"{kind}\t{title}", text)
                for gi, g in enumerate(u.get('glossary', [])):
                    term = g.get('term', '')
                    self.add('glossary', subj, grade, ui, None, gi, term, f"{term} {term} {term} {term} {flat(g.get('forms'))} {g.get('meaning', '')}")
                for ti, tp in enumerate(u.get('tips', [])):
                    self.add('tip', subj, grade, ui, None, ti, short(tp.get('text', ''), 80), tp.get('text', ''))
                ex = u.get('exercise') or {}
                for qi, q in enumerate(ex.get('questions', []) if isinstance(ex, dict) else []):
                    self.add('unitq', subj, grade, ui, None, qi, short(flat(q.get('q'))), f"{flat(q.get('q'))} {flat(q.get('q'))} {flat(q.get('options'))} {flat(q.get('answer'))} {flat(q.get('why'))}")

    # -------------------------------------------------------------- exam-pack concepts
    def concepts(self, ix):
        self.exam_subject, self.exam_labels = {}, []
        for f in ix.get('exams', []):
            try:
                ex = load(f'assets/high/exams/{f}').get('exam') or {}
            except Exception:
                continue
            if ex.get('id'):
                self.exam_subject.setdefault(ex['id'], ex.get('subject'))
                if ex.get('subject') not in self.exam_labels:
                    self.exam_labels.append(ex.get('subject'))
        seen = set()
        for f in ix.get('topics', []):
            try:
                d = load(f'assets/high/exams/{f}')
            except Exception:
                continue
            subj = next((self.exam_subject[e] for e in d.get('exam_ids') or [] if e in self.exam_subject), None) or d.get('subject')
            if not subj:  # same fallback as ExamRepo: the file-name prefix
                pre = re.sub('[^a-z]', '', re.split(r'[_.]', f)[0].lower())
                subj = next((x for x in self.exam_labels if re.sub('[^a-z]', '', x.lower()).startswith(pre)), 'General')
            subj = subj_key(subj)
            for t in d.get('topics', []):
                for s in t.get('subtopics', []):
                    if not s.get('id') or (subj, s['id']) in seen:
                        continue
                    seen.add((subj, s['id']))
                    grade = 0
                    refs = s.get('textbook_refs') or []
                    if refs and isinstance(refs[0], dict) and isinstance(refs[0].get('grade'), int):
                        grade = refs[0]['grade']
                    kw = flat(s.get('keywords'))
                    ref = ''
                    if refs and isinstance(refs[0], dict):
                        r0 = refs[0]
                        ref = f"Textbook: Grade {r0.get('grade')} · {r0.get('section') or r0.get('unit') or ''} · p.{r0.get('page')}"
                    self.concept_text[str(len(self.docs))] = [str(s.get('concept') or ''), ref]
                    self.add('concept', subj, grade, None, None, 0, f"{s['id']}\t{s.get('title', '')}",
                             f"{s.get('title', '')} {s.get('title', '')} {s.get('concept', '')} {kw} {kw} {t.get('title', '')}")

    # -------------------------------------------------------------- questions
    def unit_of(self, uid):
        return self.unit_ix.get(uid)

    def exercises(self):
        for pack, kind in (('assets/high/exercises', 'exercise'), ('assets/high/exercises/school', 'school')):
            if not exists(f'{pack}/index.json'):
                continue
            for g in load(f'{pack}/index.json')['grades'].values():
                for e in g.values():
                    d = load(f"{pack}/{e['file']}")
                    subj, grade = d['subject'], int(d['grade'])
                    for q in d['questions']:
                        qid = str(q['id'])
                        if qid in self.qseen:
                            continue
                        self.qseen.add(qid)
                        opts = q.get('options') or []
                        a = q.get('answer')
                        right = opts[a] if isinstance(a, int) and 0 <= a < len(opts) else ''
                        p = flat(q.get('prompt'))
                        self.add(kind, subj, grade, self.unit_of(q.get('unit')), None, 0, qid, f"{p} {p} {flat(right)} {flat(q.get('explanation'))}")

    def exam_q(self, q, exam, kind, best_unit):
        qid = str(q['id'])
        if qid in self.qseen:
            return
        self.qseen.add(qid)
        # the same paper often ships twice (an eager bank and a lazy Drive pack): keep the first copy of a question
        sig = (subj_key(exam.get('subject')), ' '.join(tokens(flat(q.get('stem'))))[:240], flat(q.get('answer'))[:60])
        if sig[1] and sig in self.qsig:
            return
        self.qsig.add(sig)
        ui = best_unit.get(qid)
        grade = self.units[ui][2] if ui is not None else (exam.get('grade') or 12)
        subj = subj_key(exam.get('subject'))
        stem = ' '.join(tokens(flat(q.get('stem')))[:80])
        opts = q.get('options') or {}
        ans = q.get('answer')
        right = flat(opts.get(ans)) if isinstance(opts, dict) and isinstance(ans, str) and ans in opts else flat(ans)
        kw = flat(q.get('keywords'))
        text = f"{stem} {stem} {right} {flat(q.get('explanation_steps'))} {kw} {kw} {flat(q.get('topics')).replace('-', ' ')} {flat(q.get('tips'))}"
        self.add(kind, subj, grade, ui, None, 0, qid, text)

    def exams(self, ix):
        best = {}
        conf = {'high': 3, 'medium': 2, 'low': 1}
        bestc = {}
        if exists('assets/high/notes/unit_questions.json'):
            for uid, l in load('assets/high/notes/unit_questions.json').get('units', {}).items():
                ui = self.unit_of(uid)
                if ui is None:
                    continue
                for m in l:
                    c = m.get('confidence')
                    c = c if isinstance(c, (int, float)) else conf.get(c, .5)
                    if c > bestc.get(m.get('id'), -1):
                        bestc[m.get('id')] = c
                        best[m.get('id')] = ui
        eager_exams = set()
        for f in ix.get('exams', []):
            try:
                d = load(f'assets/high/exams/{f}')
            except Exception:
                continue
            ex = d.get('exam')
            if not isinstance(ex, dict) or ex.get('id') in eager_exams:
                continue
            eager_exams.add(ex.get('id'))
            for q in d.get('questions', []):
                if isinstance(q, dict) and q.get('id'):
                    self.exam_q(q, ex, 'exam', best)
        lazy_labels = {}
        for f in sorted(glob.glob(os.path.join(ROOT, 'assets/high/exams/matric_lazy/subjects/*.json'))):
            d = load(os.path.relpath(f, ROOT))
            for p in d.get('papers', []):
                ex = p.get('exam')
                if not isinstance(ex, dict) or ex.get('id') in eager_exams:
                    continue
                lazy_labels[subj_key(ex.get('subject'))] = ex.get('subject')
                for q in p.get('questions', []):
                    if isinstance(q, dict) and q.get('id'):
                        self.exam_q(q, ex, 'lazy', best)
        return lazy_labels

    # -------------------------------------------------------------- write
    def write(self, meta):
        docs = self.docs
        n = len(docs)
        post = {}
        for i, d in enumerate(docs):
            tf = {}
            for w in d[7]:
                tf[w] = tf.get(w, 0) + 1
            for w, c in tf.items():
                post.setdefault(w, []).append((i, min(c, 255)))
        terms = sorted(post)
        lens = [min(len(d[7]), 0xFFFF) for d in docs]
        meta = dict(meta, avgLen=sum(lens) / max(1, n), nDocs=n)
        mj = json.dumps(meta, ensure_ascii=False, separators=(',', ':')).encode()
        b = bytearray(b'KTI1')
        b += struct.pack('<I', VERSION)
        b += struct.pack('<I', len(mj)) + mj
        b += struct.pack('<I', n)
        b += bytes(d[0] for d in docs) + bytes(d[1] for d in docs) + bytes(d[2] for d in docs)
        while len(b) % 2:
            b += b'\0'
        b += struct.pack(f'<{n}H', *[d[3] for d in docs])
        b += struct.pack(f'<{n}H', *[d[4] for d in docs])
        b += struct.pack(f'<{n}H', *[d[5] for d in docs])
        b += struct.pack(f'<{n}H', *lens)
        keys = '\n'.join(d[6] for d in docs).encode()
        b += struct.pack('<I', len(keys)) + keys
        tb = '\n'.join(terms).encode()
        b += struct.pack('<I', len(terms)) + struct.pack('<I', len(tb)) + tb
        while len(b) % 4:
            b += b'\0'
        pb = bytearray()
        offs = []
        for w in terms:
            offs.append(len(pb))
            last = 0
            for i, c in post[w]:
                dlt = i - last
                last = i
                while dlt >= 0x80:
                    pb.append((dlt & 0x7F) | 0x80)
                    dlt >>= 7
                pb.append(dlt)
                pb.append(c)
        offs.append(len(pb))
        b += struct.pack(f'<{len(offs)}I', *offs)
        b += pb
        os.makedirs(os.path.join(ROOT, os.path.dirname(OUT)), exist_ok=True)
        gz = gzip.compress(bytes(b), compresslevel=9, mtime=0)
        with open(os.path.join(ROOT, OUT), 'wb') as f:
            f.write(gz)
        return len(b), len(gz), len(terms), sum(len(v) for v in post.values())


def source_files():
    """every file the index depends on (test/tutor_index_test.dart lists the same set)"""
    pats = ['assets/high/notes/notes/*.json', 'assets/high/notes/unit_questions.json', 'assets/high/media/placements.json',
            'assets/high/media/taxonomy_extra.json', 'assets/high/media/g11_extra.json', 'assets/high/media/commons_extra.json',
            'assets/high/exams/*.json', 'assets/high/exams/matric_lazy/subjects/*.json', 'assets/high/exercises/*.json',
            'assets/high/exercises/school/*.json', 'tool/build_tutor_index.py']
    out = set()
    for p in pats:
        out.update(os.path.relpath(f, ROOT).replace(os.sep, '/') for f in glob.glob(os.path.join(ROOT, p)))
    return sorted(out)


def sha(p):
    with open(os.path.join(ROOT, p), 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


TOK_SAMPLES = ['What is REFRACTION?', 'Newton’s 2nd law: F = ma', 'The causes of the Battle of Adwa (1896)', 'H₂O and CO₂ molecules',
               'present perfect tense; boxes, matches, studies, classes, gases', 'half-life of radioactive isotopes', 'ሰላም ሓወይ']


def main():
    b = Builder()
    b.notes()
    ix = load('assets/high/exams/index.json')
    b.concepts(ix)
    b.exercises()
    lazy = b.exams(ix)
    srcs = source_files()
    hashes = {p: sha(p) for p in srcs}
    digest = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()[:16]
    meta = {
        'version': VERSION, 'sources': digest, 'subjects': b.subjects, 'units': b.units, 'lessons': b.lessons,
        'stop': STOP, 'syn': {stem(k): v for k, v in SYN.items()}, 'subjectWords': {stem(k): v for k, v in SUBJECT_WORDS.items()}, 'lazySubjects': lazy,
        'tokSamples': [[s, tokens(s)] for s in TOK_SAMPLES],
    }
    raw, gz, nt, npost = b.write(meta)
    with open(os.path.join(ROOT, CONCEPTS), 'w', encoding='utf-8') as f:
        json.dump({'sources': digest, 'concepts': b.concept_text}, f, ensure_ascii=False, separators=(',', ':'))
        f.write('\n')
    with open(os.path.join(ROOT, MANIFEST), 'w', encoding='utf-8') as f:
        json.dump({'about': 'sha256[:16] of every Tutor index source; regenerate with: python3 tool/build_tutor_index.py',
                   'index': OUT, 'digest': digest, 'files': hashes}, f, indent=1, sort_keys=True)
        f.write('\n')
    kinds = {}
    for d in b.docs:
        kinds[d[0]] = kinds.get(d[0], 0) + 1
    inv = {v: k for k, v in K.items() if k not in ('steps', 'states', 'vocab', 'model', 'graph')}
    print(f'{len(b.docs)} docs, {nt} terms, {npost} postings; raw {raw / 1e6:.2f} MB, gzip {gz / 1e6:.2f} MB -> {OUT}')
    print('  ' + ', '.join(f'{inv[k]}={v}' for k, v in sorted(kinds.items())))
    print(f'  concept texts: {os.path.getsize(os.path.join(ROOT, CONCEPTS)) / 1e3:.0f} KB -> {CONCEPTS}')
    print(f'  {len(b.units)} units, {len(b.lessons)} lessons, subjects: {", ".join(b.subjects)}')


if __name__ == '__main__':
    sys.exit(main())
