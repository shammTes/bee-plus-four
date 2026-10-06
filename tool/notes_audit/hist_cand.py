#!/usr/bin/env python3
"""Round 3 (History, additive only): match past-exam History MC questions to History lessons (TF-IDF over the
teacher text) and find, for each, the sentence of the lesson that states the fact behind the key.
Writes /workspace/r3h/cand_<book>.json for review; nothing in the notes is changed here."""
import json, os, re, math, collections, sys
sys.path.insert(0, os.path.dirname(__file__))
from import_matric import toks, card_text, norm, BAD
NOTES = os.path.join(os.path.dirname(__file__), '../../assets/high/notes/notes')
BANK = '/workspace/tmp-sync/drive/Matric_Questions.json'
BOOKS = ['history_9', 'history_10', 'history_11', 'history_12']


def sentences(l):
    out = []
    for c in l['cards']:
        for t in ([c.get('body')] if isinstance(c.get('body'), str) else (c.get('body') or [])) + [c.get('text') or '']:
            if isinstance(t, str):
                for s in re.split(r'(?<=[.!?;])\s+|\n+', re.sub(r'[*_#>|]', ' ', t)):
                    s = s.strip(' -•\t')
                    if len(s) > 25:
                        out.append(s)
    return out


def bank():
    d = json.load(open(BANK))
    out = []
    for p in d['papers']:
        if p['subject'] != 'History':
            continue
        for q in p['questions']:
            if q['type'] != 'MC' or not q.get('options') or not q.get('correct_answer'):
                continue
            opts = {}
            for o in q['options']:
                m = re.match(r'^\s*([A-E])[.)]\s*(.*)', o)
                if m:
                    opts[m.group(1)] = m.group(2).strip()
            if q['correct_answer'] not in opts or len(opts) < 4 or BAD.search(q['question'] + ' ' + ' '.join(opts.values())):
                continue
            if q.get('context'):
                continue
            out.append({'id': q['id'], 'q': q['question'].strip(), 'opts': opts, 'ans': q['correct_answer'], 'why': q.get('explanation') or '',
                        'note': q.get('concept_note_en') or '', 'topic': q.get('topic') or '', 'year': p['year'], 'cat': p['category']})
    # same question in several papers: keep one
    seen, uniq = set(), []
    for q in out:
        k = norm(q['q'])
        if k not in seen:
            seen.add(k); uniq.append(q)
    return uniq


def main():
    B = {b: json.load(open(os.path.join(NOTES, b + '.json'))) for b in BOOKS}
    used = set(re.findall(r'history_\d{4}_q[\w]+', ' '.join(json.dumps(d) for d in B.values())))
    existing = {norm(s) for d in B.values() for s in re.findall(r'"q": "([^"]{15,})', json.dumps(d, ensure_ascii=False))}
    docs = []
    for b, d in B.items():
        for u in d['units']:
            for l in u['lessons']:
                text = (l['title'] + ' ') * 3 + u['title'] + ' ' + ' '.join(card_text(c) for c in l['cards'])
                docs.append((b, u['id'], l['id'], collections.Counter(toks(text)), sentences(l)))
    df = collections.Counter()
    for x in docs:
        df.update(x[3].keys())
    N = len(docs)
    idf = {w: math.log((N + 1) / (n + 1)) + 1 for w, n in df.items()}

    def vec(tf):
        v = {w: (1 + math.log(c)) * idf.get(w, math.log(N + 1) + 1) for w, c in tf.items()}
        n = math.sqrt(sum(x * x for x in v.values())) or 1
        return {w: x / n for w, x in v.items()}
    dv = [vec(x[3]) for x in docs]
    qs = [q for q in bank() if q['id'] not in used and norm(q['q']) not in existing]
    res = collections.defaultdict(list)
    for q in qs:
        key = q['opts'][q['ans']]
        qv = vec(collections.Counter(toks((q['q'] + ' ') * 2 + key * 2 + ' ' + q['topic'] + ' ' + q['why'][:200])))
        sc = sorted(((sum(x * d.get(w, 0) for w, x in qv.items()), i) for i, d in enumerate(dv)), reverse=True)[:2]
        s, i = sc[0]
        if s < 0.12:
            continue
        b, uid, lid, _, sents = docs[i]
        kt = set(toks(q['q'] + ' ' + key + ' ' + key))
        best = max(sents, key=lambda t: len(kt & set(toks(t))) + (2 if key.lower()[:12] in t.lower() else 0), default='')
        res[b].append({'lesson': lid, 'unit': uid, 'score': round(s, 3), 'second': docs[sc[1][1]][2], 'cite': best, **q})
    for b in BOOKS:
        json.dump(sorted(res[b], key=lambda x: (x['lesson'], -x['score'])), open(f'/workspace/r3h/cand_{b}.json', 'w'), ensure_ascii=False, indent=1)
        print(b, len(res[b]), 'candidates for', len({x['lesson'] for x in res[b]}), 'lessons')
    print('bank questions usable', len(qs))


if __name__ == '__main__':
    main()
