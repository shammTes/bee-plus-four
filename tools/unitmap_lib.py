"""Shared helpers for tools/map_unit_questions.py and tools/verify_unit_links.py (read-only on notes + exams)."""
import json, math, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES = os.path.join(ROOT, 'assets/high/notes/notes')
EXAMS = os.path.join(ROOT, 'assets/high/exams')
EXER = os.path.join(ROOT, 'assets/high/exercises')
UQ = os.path.join(ROOT, 'assets/high/notes/unit_questions.json')

# exam subject label -> notes subjects it may link to
FAMILY = {'Agriculture': ['agriculture'], 'Biology': ['biology'], 'Business and Economics': ['business_economics'],
          'Chemistry': ['chemistry'], 'English': ['english'], 'Geography': ['geography'], 'History': ['history'],
          'Mathematics': ['mathematics'], 'Physics': ['physics'],
          'Social Studies': ['history', 'geography', 'business_economics'],
          'General Science': ['biology', 'chemistry', 'physics'],
          'General Knowledge': ['history', 'geography', 'biology', 'chemistry', 'physics', 'agriculture', 'business_economics']}


def load_units():
    """-> list of dict(id, subject, grade, number, title, lessons=[titles], book, file)"""
    out, seen = [], set()
    for name in ('index.json', 'english_index.json'):
        p = os.path.join(NOTES, name)
        if not os.path.exists(p):
            continue
        for g, subs in json.load(open(p))['grades'].items():
            for s, b in subs.items():
                for u in b['units']:
                    if u['id'] in seen:
                        continue
                    seen.add(u['id'])
                    out.append({'id': u['id'], 'subject': s, 'grade': int(g), 'number': u.get('number'), 'title': u.get('title', ''),
                                'lessons': [t.get('title', '') for t in u.get('topics') or []], 'book': b['book'], 'file': b['file']})
    return out


def load_exams():
    """eager exam files listed in assets/high/exams/index.json -> list of (file, exam, question)"""
    idx = json.load(open(os.path.join(EXAMS, 'index.json')))
    out = []
    for f in idx['exams']:
        d = json.load(open(os.path.join(EXAMS, f)))
        for q in d.get('questions') or []:
            out.append((f, d['exam'], q))
    return out


def norm(s):
    return re.sub(r'[^a-z0-9]', '', str(s or '').lower())


STOP = set('''the a an and or of to in on for with by from as at is are was were be been being this that these those which what who whom whose
when where why how it its their there they them his her he she we you your our not no yes all any each both few more most other some such
than too very can could will would shall should may might must do does did done have has had having into out up down over under again
further then once here also only own same so just about above below between during before after through while because if but nor
following correct incorrect true false statement statements one two three four five answer option options none choose best given
following which except likely called known used use uses using example examples called called mean means type types main among
question questions part section unit chapter lesson page textbook grade figure table shown show shows'''.split())


def stem(w):
    for suf in ('ational', 'ization', 'ations', 'ation', 'ings', 'ing', 'edly', 'ies', 'ied', 'ed', 'es', 's'):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            w = w[: -len(suf)] + ('y' if suf in ('ies', 'ied') else '')
            break
    return w


def toks(text):
    ws = [stem(w) for w in re.findall(r'[a-z][a-z\-]{2,}', str(text).lower().replace('-', ' ')) if w not in STOP]
    ws = [w for w in ws if w not in STOP and len(w) > 2]
    return ws + [a + '_' + b for a, b in zip(ws, ws[1:])]


def strings(x, skip=('id', 'src', 'page', 'pages', 'tone', 'status', 'type', 'image', 'img', 'art', 'file', 'media', 'svg', 'cards')):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from strings(y, skip)
    elif isinstance(x, dict):
        for k, v in x.items():
            if k in skip and not isinstance(v, (list, dict)):
                continue
            if k in ('id', 'src', 'tone', 'status', 'page', 'pages'):
                continue
            yield from strings(v, skip)


class TfIdf:
    def __init__(self, docs):
        self.df = collections.Counter()
        tfs = []
        for d in docs:
            c = collections.Counter(d)
            tfs.append(c)
            self.df.update(c.keys())
        self.n = len(docs)
        self.vecs = [self._vec(c) for c in tfs]

    def idf(self, t):
        return math.log((1 + self.n) / (1 + self.df.get(t, 0))) + 1

    def _vec(self, c):
        v = {t: (1 + math.log(n)) * self.idf(t) for t, n in c.items() if t in self.df}
        z = math.sqrt(sum(x * x for x in v.values())) or 1
        return {t: x / z for t, x in v.items()}

    def query(self, tokens):
        return self._vec(collections.Counter(tokens))

    def scores(self, qv, allowed):
        out = []
        for i in allowed:
            dv = self.vecs[i]
            out.append((i, sum(x * dv.get(t, 0) for t, x in qv.items())))
        return out


class Knn:
    """cosine nearest neighbours over labelled short texts (inverted index)."""
    def __init__(self, items):  # items: list of (tokens, label, key)
        self.df = collections.Counter()
        for t, _, _ in items:
            self.df.update(set(t))
        self.n = len(items)
        self.labels = [l for _, l, _ in items]
        self.keys = [k for _, _, k in items]
        self.inv = collections.defaultdict(list)
        for i, (t, _, _) in enumerate(items):
            for w, x in self.vec(t).items():
                self.inv[w].append((i, x))

    def vec(self, t):
        c = collections.Counter(t)
        v = {w: (1 + math.log(n)) * (math.log((1 + self.n) / (1 + self.df.get(w, 0))) + 1) for w, n in c.items() if w in self.df}
        z = math.sqrt(sum(x * x for x in v.values())) or 1
        return {w: x / z for w, x in v.items()}

    def neighbours(self, t, k=15, exclude=lambda key: False, allowed=None):
        acc = collections.defaultdict(float)
        for w, x in self.vec(t).items():
            for i, y in self.inv.get(w, ()):
                acc[i] += x * y
        out = []
        for i, s in sorted(acc.items(), key=lambda kv: -kv[1]):
            if exclude(self.keys[i]) or (allowed is not None and self.labels[i] not in allowed):
                continue
            out.append((self.labels[i], s))
            if len(out) >= k:
                break
        return out
