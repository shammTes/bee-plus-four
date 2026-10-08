#!/usr/bin/env python3
"""Duplicate matric / model papers.
Lazy Drive packs (matric_lazy/subjects/*.json, ids drive-*) repeat papers that are already eager packs (ids bank-*,
phys-*, ...) under another id, so the app listed them twice. A pair is a duplicate when it has the same subject, year
and kind (matric / model) and >= 80% of either paper's stems match (fuzzy, OCR-tolerant). The more complete copy is
kept (eager wins a tie: it is in summary.json, unit links, tutor index); questions only the dropped copy has are
appended to the kept one (new ids, numbered after the last question, review_flag noting the merge).
Usage: dedupe.py [--dry]"""
import difflib, glob, json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'high', 'exams')
THR = 0.8
# Files the 'Build 4 APK' workflow (.github/workflows/build-four-apk.yml, step "Add Sawa model exams") requires to
# exist, be listed in index.json and hold >= 383 questions; otherwise it re-downloads an expired pack and the build
# fails. When one of these duplicates a bank paper, the pinned file is kept and the bank copy dropped (its unique
# questions merged in), whatever the completeness score says.
PINNED = {
    'chemistry_2010-11_model_sem2.json', 'chemistry_2016-17_model.json', 'chemistry_2017-18_model.json',
    'history_2016-17_model.json', 'physics_2017-18_model.json',
}


def norm(s):
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', str(s))
    return re.sub(r'\\+[a-zA-Z]+|[^a-z0-9]', '', s.lower())[-160:]


def kind(e):
    t = ' '.join(str(e.get(k, '')) for k in ('id', 'title', 'type', 'exam_code')).lower()
    return 'model' if 'model' in t else 'matric'


def key(d):
    e = d['exam']
    return (e.get('subject'), str(e.get('year'))[:4], kind(e))


def same(a, b):
    if not a or not b:
        return a == b
    if a == b or (min(len(a), len(b)) >= 20 and (a in b or b in a)):
        return True  # one copy inlines the reading passage / an "Refer to ..." lead-in
    m = difflib.SequenceMatcher(None, a, b)
    return m.real_quick_ratio() > .85 and m.quick_ratio() > .85 and m.ratio() > .85


def unmatched(qa, qb):
    nb = [norm(q.get('stem', '')) for q in qb]
    return [q for q in qa if not any(same(norm(q.get('stem', '')), b) for b in nb)]


def overlap(qa, qb):
    ua, ub = unmatched(qa, qb), unmatched(qb, qa)
    return max(1 - len(ua) / max(1, len(qa)), 1 - len(ub) / max(1, len(qb))), ua, ub


def renderable(d):
    return sum(1 for q in d.get('questions', []) if str(q.get('stem', '')).strip())


def quality(d):
    """renderable questions, a missing-picture question (android_asset link, no image shipped) counting half"""
    return sum(1 - .5 * ('android_asset' in str(q.get('stem', ''))) for q in d.get('questions', []) if str(q.get('stem', '')).strip())


def truly_new(extra, keep, room):
    """of the unmatched questions, at most [room] (the question-count gap) that resemble nothing in [keep]"""
    kn = [norm(q.get('stem', '')) for q in keep['questions']]
    sc = []
    for q in extra:
        n = norm(q.get('stem', ''))
        best = max([difflib.SequenceMatcher(None, n, b).ratio() for b in kn] or [0])
        if best < .7 and n:
            sc.append((best, q))
    sc.sort(key=lambda x: x[0])
    keep_ids = {id(q) for _, q in sc[:max(0, room)]}
    out, seen = [], []
    for q in sorted((q for q in extra if id(q) in keep_ids), key=lambda q: -len(json.dumps(q))):
        n = norm(q.get('stem', ''))  # the dropped copy may repeat a question itself: merge it once (fullest copy)
        if not any(difflib.SequenceMatcher(None, n, b).ratio() >= .7 for b in seen):
            seen.append(n)
            out.append(q)
    return [q for q in extra if any(q is o for o in out)]


def merge_into(keep, extra, src_id):
    qs = keep['questions']
    eid = keep['exam']['id']
    ids = {q['id'] for q in qs}
    n = max([q.get('number', 0) for q in qs] or [0])
    added = []
    for q in extra:
        if isinstance(q.get('options'), dict) and q.get('answer') not in q['options']:
            continue  # a broken copy-only item (e.g. options of another question, no key) is not merged
        q = json.loads(json.dumps(q))
        n += 1
        k = len(qs) + 1
        nid = f'{eid}-q{k:03d}'
        while nid in ids:
            k += 1
            nid = f'{eid}-q{k:03d}'
        ids.add(nid)
        q['id'], q['exam_id'], q['number'] = nid, eid, n
        q.setdefault('review_flag', f'Merged from duplicate copy {src_id}; question number in the original paper unknown.')
        qs.append(q)
        added.append(nid)
    return added


def main():
    dry = '--dry' in sys.argv
    idx = json.load(open(os.path.join(ROOT, 'index.json')))
    eager = {}
    for f in idx['exams']:
        d = json.load(open(os.path.join(ROOT, f)))
        eager[f] = d
    lazy_files = sorted(glob.glob(os.path.join(ROOT, 'matric_lazy', 'subjects', '*.json')))
    lazy = {p: json.load(open(p)) for p in lazy_files}
    log = []
    drop_eager = set()
    touched = set()
    # 1) eager vs eager
    fl = list(eager)
    for i, a in enumerate(fl):
        for b in fl[i + 1:]:
            if a in drop_eager or b in drop_eager or key(eager[a]) != key(eager[b]) or None in key(eager[a]):
                continue
            ov, ua, ub = overlap(eager[a]['questions'], eager[b]['questions'])
            if ov < THR:
                continue
            if (a in PINNED) != (b in PINNED):
                ka, kb = (a, b) if a in PINNED else (b, a)
            else:
                ka, kb = (a, b) if quality(eager[a]) >= quality(eager[b]) else (b, a)
            extra = ub if ka == a else ua
            room = renderable(eager[kb]) - renderable(eager[ka])
            if ka in PINNED:
                room = len(extra)  # the bank copy goes; keep every question it alone has
            added = merge_into(eager[ka], truly_new(extra, eager[ka], room), eager[kb]['exam']['id'])
            drop_eager.add(kb)
            touched.add(ka)
            log.append(dict(kind='eager', subject=key(eager[ka])[0], kept=eager[ka]['exam']['id'], dropped=eager[kb]['exam']['id'], overlap=round(ov, 2), merged=added))
    # 2) lazy vs eager
    for p, pack in lazy.items():
        keep_papers = []
        for d in pack['papers']:
            best = None
            for f, e in eager.items():
                if f in drop_eager or key(e) != key(d):
                    continue
                ov, ua, ub = overlap(e['questions'], d['questions'])
                if ov >= THR and (best is None or ov > best[1]):
                    best = (f, ov, ub)
            if best is None:
                keep_papers.append(d)
                continue
            f, ov, ub = best
            e = eager[f]
            added = []
            room = renderable(d) - renderable(e)
            if room > 0:
                added = merge_into(e, truly_new(ub, e, room), d['exam']['id'])
                touched.add(f)
            log.append(dict(kind='lazy', subject=d['exam'].get('subject'), kept=e['exam']['id'], dropped=d['exam']['id'], overlap=round(ov, 2), merged=added))
        pack['papers'] = keep_papers
    for x in log:
        print(json.dumps(x))
    if dry:
        return
    for f in touched - drop_eager:
        _write(os.path.join(ROOT, f), eager[f])
    assert not drop_eager & PINNED, drop_eager & PINNED
    for f in drop_eager:
        os.remove(os.path.join(ROOT, f))
    idx['exams'] = [f for f in idx['exams'] if f not in drop_eager]
    _write(os.path.join(ROOT, 'index.json'), idx)
    for p, pack in lazy.items():
        _write(p, pack)
    cat_p = os.path.join(ROOT, 'matric_lazy', 'catalog.json')
    cat = json.load(open(cat_p))
    left = {d['exam']['id'] for pack in lazy.values() for d in pack['papers']}
    cat['papers'] = [c for c in cat['papers'] if c['exam_id'] in left]
    cat['totals']['papers'] = len(cat['papers'])
    cat['totals']['questions'] = sum(c.get('questions', 0) for c in cat['papers'])
    cat['note'] = cat['note'].split(' Duplicates')[0] + ' Duplicates of eager packs removed by tool/matric_audit/dedupe.py.'
    _write(cat_p, cat)
    ec_p = os.path.join(ROOT, '..', '..', 'content', 'exam_catalog.json')
    if os.path.exists(ec_p):
        ec = json.load(open(ec_p))
        ec['exams'] = [x for x in ec['exams'] if not (isinstance(x, dict) and str(x.get('file', '')).startswith('assets/high/exams/') and os.path.basename(x['file']) in drop_eager)]
        with open(ec_p, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(ec, ensure_ascii=False, indent=2) + '\n')
    lp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dedupe_log.json')
    old = json.load(open(lp)) if os.path.exists(lp) else []  # a re-run updates the log of the earlier runs
    new = {frozenset((x['kept'], x['dropped'])): x for x in log}
    old = [new.pop(frozenset((x['kept'], x['dropped'])), x) for x in old]
    json.dump(old + list(new.values()), open(lp, 'w'), indent=1)


def _write(p, d):
    raw = open(p, encoding='utf-8').read()
    with open(p, 'w', encoding='utf-8') as f:
        if raw.startswith('{"') or raw.startswith('['):
            json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
        else:
            json.dump(d, f, ensure_ascii=False, indent=2)
        if raw.endswith('\n'):
            f.write('\n')


if __name__ == '__main__':
    main()
