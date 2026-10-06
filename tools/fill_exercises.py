#!/usr/bin/env python3
"""Fill empty / thin units of the Exercise bank (assets/high/exercises/<subject>_<grade>.json).

  python3 tools/fill_exercises.py [--study-notes PATH] [--report]

Sources, in priority order, per notes unit that has fewer than TARGET items (Grade 12 and English: every unit):
  1. Drive Study_Notes.json review exercises (MC only; the chapter number = the notes unit number)   src "study_notes#<id>"
  2. Hand-written items in tool/exercises_fill/<subject>_<grade>.txt (format: see load_authored)         src "authored#<unit>"
  3. "similar_questions" of the matric/model questions mapped to the unit (assets/high/notes/unit_questions.json,
     confidence high/medium). These are practice twins of exam questions, not the exam questions.      src "matric_similar#<exam q id>"
  4. MCQs of the notes unit exercise (assets/high/notes/notes/<book>.json units[].exercise)             src "notes#<id>"
Items are de-duplicated (normalised stem) against everything already in the file and in the school pack.
Every item: 4 options (5-option exam twins lose one unmentioned wrong option), answer index, step-by-step explanation.
Re-runnable: items added by this tool (ids with _sn_/_au_/_ms_/_nx_) are removed first, then rebuilt.
Also re-tags legacy Drive chapter ids (bio_g10_c1 -> bio10-u1); English 11-12 Study_Notes chapters map to eng11 units via ENG11.
Check the result with tools/verify_exercises.py.
"""
import argparse, collections, glob, json, os, random, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, 'assets/high/exercises')
NOTES = os.path.join(ROOT, 'assets/high/notes/notes')
EXAMS = os.path.join(ROOT, 'assets/high/exams')
AUTH = os.path.join(ROOT, 'tool/exercises_fill')
TARGET = 30          # a unit below this gets filled
MIN_EXPL = 45       # exam twins whose explanation is a bare restatement are skipped
CAP_SIMILAR = 45     # stop adding exam twins once a unit has this many items
FIXES = {}
ADDED = re.compile(r'_(sn|au|ms|nx)_')
SUBJ = {'Agriculture': 'agriculture', 'Biology': 'biology', 'Business and Economics': 'business_economics', 'Chemistry': 'chemistry',
        'Geography': 'geography', 'History': 'history', 'Mathematics': 'mathematics', 'Physics': 'physics', 'English': 'english'}
PREFIX = {'agriculture': 'agri', 'biology': 'bio', 'business_economics': 'be', 'chemistry': 'chem', 'geography': 'geo',
          'history': 'hist', 'mathematics': 'math', 'physics': 'phys', 'english': 'eng'}
LEGACY = {'agri': 'agriculture', 'bio': 'biology', 'chem': 'chemistry', 'history': 'history', 'econ': 'business_economics',
          'geo': 'geography', 'math': 'mathematics', 'phys': 'physics', 'physics': 'physics'}
# English 11 notes units 1-24 <- Drive "English 11-12" chapters
ENG11 = {1: 1, 2: 5, 3: 8, 4: 9, 5: 10, 6: 11, 7: 14, 8: 20, 9: 2, 10: 3, 11: 4, 12: 6, 13: 7, 14: 12, 15: 13, 16: 15, 17: 16,
         18: 17, 19: 18, 20: 19, 21: 21, 22: 22, 23: 23, 24: 24}

SUP = str.maketrans('0123456789+-=()n', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ')
SUB = str.maketrans('0123456789+-=()', '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎')
SIMPLE_CMDS = {r'\times': '×', r'\div': '÷', r'\cdot': '·', r'\le': '≤', r'\leq': '≤', r'\ge': '≥', r'\geq': '≥', r'\ne': '≠',
               r'\neq': '≠', r'\pm': '±', r'\%': '%', r'\pi': 'π', r'\circ': '°', r'\degree': '°', r'\dots': '…', r'\ldots': '…',
               r'\cdots': '⋯', r'\to': '→', r'\rightarrow': '→', r'\leftarrow': '←', r'\rightleftharpoons': '⇌', r'\approx': '≈',
               r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\Delta': 'Δ', r'\delta': 'δ', r'\lambda': 'λ', r'\mu': 'μ',
               r'\rho': 'ρ', r'\theta': 'θ', r'\sigma': 'σ', r'\Sigma': 'Σ', r'\Omega': 'Ω', r'\omega': 'ω', r'\nu': 'ν',
               r'\infty': '∞', r'\,': ' ', r'\;': ' ', r'\ ': ' ', r'\quad': ' ', r'\$': '$', r'\&': '&', r'\#': '#',
               r'\uparrow': '↑', r'\downarrow': '↓', r'\cup': '∪', r'\cap': '∩', r'\in': '∈', r'\emptyset': '∅', r'\varnothing': '∅',
               r'\subset': '⊂', r'\subseteq': '⊆', r'\prime': '′', r'\angle': '∠', r'\triangle': '△', r'\parallel': '∥', r'\perp': '⊥',
               r'\checkmark': '✓', r'\star': '★'}


def fix_bs(s):
    """'\\\\frac' (double-escaped in the source) -> '\\frac'"""
    return re.sub(r'\\\\(?=[A-Za-z%])', r'\\', s)


def simple_tex(m):
    """turn a trivial $$...$$ (numbers, words, x^2, H_2O, \\times...) into plain Unicode; else keep it"""
    src = m.group(1)
    t = src.strip()
    t = re.sub(r'\\(?:text|mathrm|textbf|mathbf|operatorname)\{([^{}]*)\}', r'\1', t)
    for k in sorted(SIMPLE_CMDS, key=len, reverse=True):
        t = re.sub(re.escape(k) + r'(?![A-Za-z])', SIMPLE_CMDS[k].replace('\\', r'\\'), t)
    t = re.sub(r'\^\{?\\circ\}?', '°', t)
    t = t.replace('\\{', '\x01').replace('\\}', '\x02')
    t = re.sub(r'\\mathbb\{([NZQR])\}', lambda mm: {'N': 'ℕ', 'Z': 'ℤ', 'Q': 'ℚ', 'R': 'ℝ'}[mm.group(1)], t)

    def sup(mm):
        b = mm.group(1) or mm.group(2)
        return b.translate(SUP) if all(c in '0123456789+-=()n' for c in b) else None

    def sub(mm):
        b = mm.group(1) or mm.group(2)
        return b.translate(SUB) if all(c in '0123456789+-=()' for c in b) else None
    for pat, f in ((r'\^\{([^{}]*)\}|\^(\w)', sup), (r'_\{([^{}]*)\}|_(\d)', sub)):
        out, ok = [], True
        pos = 0
        for mm in re.finditer(pat, t):
            r = f(mm)
            if r is None:
                ok = False
                break
            out.append(t[pos:mm.start()] + r)
            pos = mm.end()
        if not ok:
            return m.group(0)
        t = ''.join(out) + t[pos:]
    if '\\' in t or '{' in t or '}' in t or '^' in t or '_' in t:
        return m.group(0)
    return t.replace('\x01', '{').replace('\x02', '}')


def clean(s):
    if s is None:
        return ''
    s = unicodedata.normalize('NFC', str(s))
    s = fix_bs(s).replace('\r', '')
    s = re.sub(r'\\s\{(\\\{.*?\\\})\}', r'\1', s)    # stray '\s{...}' wrapper in a few Drive items
    s = re.sub(r'\$\$(.+?)\$\$', simple_tex, s, flags=re.S)
    s = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', s)
    s = re.sub(r'[ \t]+\n', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()


def ukey(s):
    return re.sub(r'\s+', ' ', str(s)).strip()


def dkey(s):
    """de-duplication / distinctness key: case and spacing only (signs and numbers matter)"""
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', str(s)).lower()).strip(' .?:')


def fkey(stem, opts):
    """dedup key: the stem, plus the option set when the stem is generic ("Choose the correct sentence.")"""
    k = dkey(stem)
    if len(k) < 60:
        k += '||' + '|'.join(sorted(dkey(o) for o in opts or []))
    return k


def norm(s):
    s = unicodedata.normalize('NFKC', str(s)).lower()
    s = re.sub(r'\$\$|\\[a-z]+|[^\w]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


LETTER_REF = re.compile(r'\b(Options?|options?|Choices?|choices?)\s+([A-E](?:\s*(?:,|and|or|&)\s*[A-E])*)\b')


def remap_letters(expl, perm):
    """perm: old index -> new index. Rewrites 'Option A', 'Options B and D'. Returns None if other bare letter refs remain."""
    def rep(m):
        letters = re.sub(r'[A-E]', lambda x: 'ABCDE'[perm[ 'ABCDE'.index(x.group(0))]] if 'ABCDE'.index(x.group(0)) in perm else '?', m.group(2))
        return f'{m.group(1)} {letters}'
    out = LETTER_REF.sub(rep, expl)
    if '?' in ''.join(m.group(2) for m in LETTER_REF.finditer(out)):
        return None
    return out


def bare_letter_refs(expl):
    return re.search(r'\(([A-E])\)|\b[Aa]nswer\s*(?:is)?\s*:?\s*\(?[A-E]\b(?![\w\'])|\b[A-E]\)\s', expl) is not None


def item(id_, unit, prompt, options, answer, expl, src):
    return {'id': id_, 'unit': unit, 'prompt': prompt, 'options': options, 'answer': answer, 'explanation': expl, 'verified': 'reviewed', 'src': src}


def bad_text(s):
    return not s or not s.strip()


# ---------------------------------------------------------------- sources

def study_notes(path):
    d = json.load(open(path, encoding='utf-8'))
    out = collections.defaultdict(list)    # (subject, grade, unit_number) -> [raw q]
    for ch in d['chapter_notes']:
        subj = SUBJ.get(ch['subject'])
        if not subj:
            continue
        if subj == 'english':
            inv = {v: k for k, v in ENG11.items()}
            key = ('english', 11, inv[int(ch['chapter_number'])])
        else:
            key = (subj, int(ch['grade']), int(ch['chapter_number']))
        for q in ch.get('review_exercises') or []:
            out[key].append(q)
    return out


def from_study_note(q, rng):
    opts = q.get('options') or []
    if not opts or len(opts) not in (4, 5):
        return None, 'no options'
    opts = [clean(o) for o in opts]
    a = clean(re.sub(r'^\s*\$\$?(.*?)\$?\$\s*$', r'\1', str(q.get('correct_answer') or ''), flags=re.S))
    a2 = clean('$$' + re.sub(r'^\s*\$\$?(.*?)\$?\$\s*$', r'\1', str(q.get('correct_answer') or ''), flags=re.S) + '$$')
    raw_a = str(q.get('correct_answer') or '').strip()
    if raw_a in (q.get('options') or []):
        k = q['options'].index(raw_a)
    elif a in opts:
        k = opts.index(a)
    elif a2 in opts:
        k = opts.index(a2)
    elif re.fullmatch(r'[A-E]', raw_a) and 'ABCDE'.index(raw_a) < len(opts):
        k = 'ABCDE'.index(raw_a)
    else:
        return None, 'key not in options'
    raw_e = str(q.get('explanation') or '')
    # English 11-12 study notes end with a "**Step 3: Tigrinya Explanation**" section; the Exercise
    # tab is English-only, so keep the English steps
    raw_e = re.split(r'\n*\*\*\s*Step\s*\d+\s*:?\s*Tigrinya', raw_e)[0]
    expl = clean(raw_e)
    stem = clean(q.get('question'))
    if bad_text(stem) or bad_text(expl) or any(bad_text(o) for o in opts) or len({ukey(o) for o in opts}) < len(opts):
        return None, 'malformed'
    if len(opts) == 5:   # drop one wrong option the explanation does not mention, keep letters valid
        cand = [i for i in range(5) if i != k and norm(opts[i]) not in norm(expl) and not re.search(r'\b(all|none|both) of|\b[A-E] and [A-E]\b', opts[i], re.I)]
        if not cand:
            return None, '5 options'
        drop = cand[-1]
        perm = {i: (i if i < drop else i - 1) for i in range(5) if i != drop}
        e2 = remap_letters(expl, perm)
        if e2 is None:
            return None, '5 options'
        expl = e2
        opts = [o for i, o in enumerate(opts) if i != drop]
        k = perm[k]
    # shuffle (source keys cluster on B/C); letter references in the explanation are rewritten
    if any(re.search(r'\b(all|none|both) of the above|\b[A-D] and [A-D]\b|^[A-D]\b', o, re.I) for o in opts) or bare_letter_refs(expl):
        return (stem, opts, k, expl), None
    perm_list = list(range(4))
    rng.shuffle(perm_list)
    perm = {old: new for new, old in enumerate(perm_list)}
    e2 = remap_letters(expl, perm)
    if e2 is None:
        return (stem, opts, k, expl), None
    return (stem, [opts[i] for i in perm_list], perm[k], e2), None


def exam_index():
    cache = {}

    def get(exam):
        if exam not in cache:
            p = os.path.join(EXAMS, exam + '.json')
            cache[exam] = {q['id']: q for q in json.load(open(p, encoding='utf-8')).get('questions', []) if isinstance(q, dict) and 'id' in q} if os.path.exists(p) else {}
        return cache[exam]
    return get


def from_similar(s, rng):
    o = s.get('options')
    if not isinstance(o, dict) or s.get('answer') not in o:
        return None, 'bad'
    keys = sorted(o)
    if keys != list('ABCDE')[:len(keys)] or len(keys) not in (4, 5):
        return None, 'bad letters'
    opts = [clean(o[x]) for x in keys]
    k = keys.index(s['answer'])
    steps = [clean(x) for x in s.get('explanation_steps') or [] if str(x).strip()]
    expl = '\n'.join(steps)
    stem = clean(s.get('stem'))
    if s.get('image') or re.search(r'\b(figure|diagram|graph|table|map|shown below|shown above|passage)\b', stem, re.I):
        return None, 'needs figure/passage'
    if bad_text(stem) or bad_text(expl) or any(bad_text(x) for x in opts) or len({ukey(x) for x in opts}) < len(opts):
        return None, 'malformed'
    body = re.sub(r'\n?\b[Aa]nswer\s*(?:is)?\s*:?.*$', '', expl).strip()
    if len(body) < MIN_EXPL:
        return None, 'explanation too short'
    if len(opts) == 5:
        # drop E when it is wrong and unmentioned, else drop D and move E's text up (rewrite 'Answer: E')
        refs = lambda L: re.search(r'(?<![\w\'’])' + L + r'(?![\w\'’])', expl)
        e_txt = norm(opts[4])
        allref = lambda t: re.search(r'\b(all|none|both)\b.*\b(above|of these)\b|\b[A-E] and [A-E]\b|\b[A-E], [A-E]\b', t, re.I)
        if any(allref(x) for x in opts[:4]):
            return None, '5 options'
        if k != 4 and not refs('E') and (not e_txt or e_txt not in norm(expl) or len(e_txt) < 4):
            opts = opts[:4]
        elif k == 4 and not refs('D') and len(re.findall(r'(?<![\w\'’])E(?![\w\'’])', expl)) <= 1 and norm(opts[3]) not in norm(expl):
            expl = re.sub(r'(?<![\w\'’])E(?![\w\'’])', 'D', expl)
            opts = opts[:3] + [opts[4]]
            k = 3
        else:
            return None, '5 options'
    return shuffle_item(stem, opts, k, expl, rng), None


def shuffle_item(stem, opts, k, expl, rng):
    """exam twins are all keyed A: name the answer in words instead of 'Answer: A', then shuffle the options"""
    expl = re.sub(r'\b[Aa]nswer\s*(?:is)?\s*:?\s*\(?([A-E])\)?(?![\w\'’])\.?', lambda m: f'Answer: {opts["ABCDE".index(m.group(1))]}.' if 'ABCDE'.index(m.group(1)) < len(opts) else m.group(0), expl)
    if any(re.search(r'\b(all|none|both) of the above|\b[A-D] and [A-D]\b|^[A-D]\b', o, re.I) for o in opts) or bare_letter_refs(expl):
        return stem, opts, k, expl
    order = list(range(len(opts)))
    rng.shuffle(order)
    perm = {old: new for new, old in enumerate(order)}
    e2 = remap_letters(expl, perm)
    if e2 is None or re.search(r'(?<![\w\'’])[A-E](?=\s*(?:is|are|was)\s+(?:wrong|incorrect|correct|right|false|true))|\b[A-E]\s*[:=]\s', expl):
        return stem, opts, k, expl
    return stem, [opts[i] for i in order], perm[k], e2


def from_notes_mcq(q):
    o = q.get('options')
    if q.get('type') != 'mcq' or not isinstance(o, dict) or q.get('answer') not in o:
        return None
    keys = sorted(o)
    if keys != list('ABCD'):
        return None
    why = [clean(x) for x in (q.get('why') or []) if str(x).strip()]
    if not why:
        return None
    d = lambda t: clean(re.sub(r'(?<![$\\])\$([^$\n]+?)\$(?!\$)', r'$$\1$$', str(t or '')))
    stem = d(q.get('q'))
    if stem and stem[-1] not in '.?!:)_' and not stem.endswith('____'):
        stem += '?'
    opts = [d(o[x]) for x in keys]
    k = keys.index(q['answer'])
    # notes 'why' starts with "Answer B: text" (a letter that is wrong after shuffling) and often
    # ends by repeating the answer; name the answer in words once and keep the reasoning lines
    lines = [d(x) for x in why if not re.match(r'^\s*Answer\s*[A-D]\s*[:.)]', str(x))]
    lines = [x for x in lines if norm(x.rstrip('.')) != norm(opts[k].rstrip('.'))]
    expl = '\n'.join([f'The correct answer is **{opts[k]}**.'] + lines)
    return stem, opts, k, expl


def load_authored(path):
    """tool/exercises_fill/<subject>_<grade>.txt:
         @ unit-id          (applies to the following items)
         Q: stem            (may continue on following lines)
         + correct option
         - wrong option     (three of them)
         E: explanation     (may continue on following lines; refer to options by their words, never by letter)
       blank line between items."""
    out, unit, cur, field = [], None, None, None

    def flush():
        nonlocal cur
        if cur:
            opts = cur['opts']
            assert len(opts) == 4 and sum(1 for ok, _ in opts if ok) == 1, (path, cur['Q'][:60], len(opts))
            assert cur['Q'].strip() and cur['E'].strip(), (path, cur['Q'][:60])
            out.append({'unit': cur['unit'], 'prompt': cur['Q'].strip(), 'options': [o for _, o in opts],
                        'answer': [ok for ok, _ in opts].index(True), 'explanation': cur['E'].strip()})
        cur = None
    for raw in open(path, encoding='utf-8').read().split('\n'):
        line = raw.rstrip()
        if line.startswith('#'):
            continue
        if line.startswith('@'):
            flush()
            unit = line[1:].strip()
            continue
        if not line.strip():
            if cur and field == 'E':
                flush()
            elif cur and field == 'Q':
                cur['Q'] += '\n'
            continue
        if line.startswith('Q:'):
            flush()
            cur = {'unit': unit, 'Q': line[2:].strip(), 'opts': [], 'E': ''}
            field = 'Q'
        elif line[:2] in ('+ ', '- ') and cur is not None and field in ('Q', 'O'):
            cur['opts'].append((line[0] == '+', line[2:].strip()))
            field = 'O'
        elif line.startswith('E:') and cur is not None:
            cur['E'] = line[2:].strip()
            field = 'E'
        elif cur is not None and field in ('Q', 'E'):
            cur[field] += '\n' + line.strip()
        else:
            raise ValueError(f'{path}: cannot parse line: {line!r}')
    flush()
    return out


def apply_fix(t, fix):
    if fix == 'drop':
        return None
    stem, opts, k, expl = t
    for a, b in fix.get('sub', []):
        stem, expl = stem.replace(a, b), expl.replace(a, b)
        opts = [o.replace(a, b) for o in opts]
    if 'explanation' in fix:
        expl = fix['explanation']
    if 'prompt' in fix:
        stem = fix['prompt']
    return stem, opts, k, expl


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study-notes', default='/workspace/tmp-sync/drive/Study_Notes.json')
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()
    rng = random.Random(1212)
    global FIXES
    fp = os.path.join(AUTH, 'fixes.json')
    FIXES = json.load(open(fp, encoding='utf-8')) if os.path.exists(fp) else {}
    unknown = set(FIXES)
    idx_notes = json.load(open(os.path.join(NOTES, 'index.json'), encoding='utf-8'))
    uq = json.load(open(os.path.join(ROOT, 'assets/high/notes/unit_questions.json'), encoding='utf-8'))['units']
    exq = exam_index()
    sn = study_notes(args.study_notes)
    ex_index = json.load(open(os.path.join(EX, 'index.json'), encoding='utf-8'))
    school_idx = json.load(open(os.path.join(EX, 'school/index.json'), encoding='utf-8'))
    stats = collections.Counter()
    report = []
    sys.path.insert(0, os.path.join(ROOT, 'tools'))

    for g, subs in sorted(idx_notes['grades'].items(), key=lambda x: int(x[0])):
        g = int(g)
        for subj, book in subs.items():
            fn = f'{subj}_{g}.json'
            path = os.path.join(EX, fn)
            data = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {'subject': subj, 'grade': g, 'questions': []}
            qs = [q for q in data['questions'] if not ADDED.search(q['id'])]
            # legacy Drive chapter ids -> notes unit ids
            for q in qs:
                m = re.fullmatch(r'([a-z]+)_g(\d+)_[cu](\d+)', str(q.get('unit') or ''))
                if m and LEGACY.get(m.group(1)) == subj and int(m.group(2)) == g:
                    q['unit'] = f'{PREFIX[subj]}{g}-u{int(m.group(3))}'
            school = []
            sp = os.path.join(EX, 'school', fn)
            if os.path.exists(sp):
                school = json.load(open(sp, encoding='utf-8'))['questions']
            seen = {fkey(q['prompt'], q['options']) for q in qs + school}
            seen_stem = {dkey(q['prompt']) for q in qs + school}
            have = collections.Counter(q.get('unit') for q in qs + school)
            auth = {}
            ap_ = os.path.join(AUTH, f'{subj}_{g}.txt')
            if os.path.exists(ap_):
                for q in load_authored(ap_):
                    auth.setdefault(q['unit'], []).append(q)
            added = []
            for u in book['units']:
                uid, un = u['id'], u['number']
                full = g == 12 or subj == 'english'
                if not full and have[uid] >= TARGET and uid not in auth:
                    continue
                n0 = have[uid]
                new = []

                def push(tag, src, t):
                    unknown.discard(src)
                    if src in FIXES:
                        t = apply_fix(t, FIXES[src])
                        if t is None:
                            stats['fix drop'] += 1
                            return False
                    stem, opts, k, expl = t
                    assert len(opts) == 4 and 0 <= k < 4 and len({ukey(o) for o in opts}) == 4, (src, opts)
                    # hand-written items may share a generic stem ("Choose the correct sentence.") with
                    # different options; sourced items are de-duplicated on the stem alone
                    key = fkey(stem, opts)
                    if not dkey(stem) or key in seen or (tag != 'au' and dkey(stem) in seen_stem):
                        stats['dup'] += 1
                        return False
                    seen.add(key)
                    seen_stem.add(dkey(stem))
                    new.append(item(f'{subj}_{g}_{tag}_{len(added) + len(new) + 1}', uid, stem, opts, k, expl, src))
                    return True
                for q in sn.get((subj, g, un), []):
                    t, why = from_study_note(q, rng)
                    if t is None:
                        stats['sn drop: ' + why] += 1
                        continue
                    push('sn', f"study_notes#{q.get('id')}", t)
                for q in auth.get(uid, []):
                    push('au', f'authored#{uid}', shuffle_item(clean(q['prompt']), [clean(o) for o in q['options']], q['answer'], clean(q['explanation']), rng))
                for ref in uq.get(uid, []):
                    if n0 + len(new) >= CAP_SIMILAR:
                        break
                    if ref.get('confidence') == 'low':
                        continue
                    eq = exq(ref['exam']).get(ref['id'])
                    if not eq:
                        continue
                    for j, s in enumerate(eq.get('similar_questions') or []):
                        if n0 + len(new) >= CAP_SIMILAR:
                            break
                        t, why = from_similar(s, rng)
                        if t is None:
                            stats['sim drop: ' + why] += 1
                            continue
                        push('ms', f"matric_similar#{ref['id']}#{j}", t)
                if n0 + len(new) < 25:
                    nb = json.load(open(os.path.join(NOTES, book['file']), encoding='utf-8'))
                    for nu in nb['units']:
                        if nu['id'] != uid:
                            continue
                        for q in (nu.get('exercise') or {}).get('questions', []):
                            t = from_notes_mcq(q)
                            if t:
                                t = shuffle_item(*t, rng)
                                push('nx', f"notes#{q.get('id')}", t)
                added += new
                report.append((g, subj, uid, u['title'], n0, len(new), collections.Counter(x['src'].split('#')[0] for x in new)))
            if not added and not os.path.exists(path):
                continue
            data['questions'] = qs + added
            if not args.dry:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
                cnt = collections.Counter(q.get('unit') or 'general' for q in data['questions'])
                ex_index['grades'].setdefault(str(g), {})[subj] = {'file': fn, 'count': len(data['questions']), 'units': dict(sorted(cnt.items()))}
    if not args.dry:
        ex_index['about'] = ('Practice MCQs for the Exercise tab, generated by tools/clean_exercises.py and topped up per unit by '
                             'tools/fill_exercises.py; check with tools/verify_exercises.py (see docs/exercises_report.md).')
        ex_index['total'] = sum(e['count'] for gg in ex_index['grades'].values() for e in gg.values())
        with open(os.path.join(EX, 'index.json'), 'w', encoding='utf-8') as f:
            json.dump(ex_index, f, ensure_ascii=False, indent=1)
            f.write('\n')
    for r in report:
        print(f'{r[0]:>2} {r[1]:<18} {r[2]:<10} {r[4]:>4} +{r[5]:<4} -> {r[4] + r[5]:>4}  {dict(r[6])}  {r[3][:40]}')
    print(dict(stats))
    if unknown - {'_about'}:
        print('fixes not applied (source item not reached):', sorted(unknown - {'_about'}))


if __name__ == '__main__':
    main()
