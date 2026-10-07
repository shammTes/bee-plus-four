#!/usr/bin/env python3
"""Per-paper audit of the High exam bank, reading the packs the way ExamRepo does: index.json eager packs, then the
lazy Drive subject packs (matric_lazy/subjects/*.json, skipped when the exam id is already loaded).
Reports per paper: questions, blank stems, MCQs without options / key, empty options, missing-figure links,
over-escaped TeX (\\\\frac: drawn as garbage), within-paper repeats, Part I numbering holes, and per subject the
papers listed twice (same subject / year / kind). The exact flutter_math parse check is test/papers_render_test.dart.
Usage: audit.py [ROOT] [--json out.json]"""
import collections, glob, json, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
EX = os.path.join(ROOT, 'assets', 'high', 'exams')
SEG = re.compile(r'\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)')


def n(s):
    return re.sub(r'[^a-z0-9]', '', str(s).lower())


def load():
    idx = json.load(open(os.path.join(EX, 'index.json')))
    out, seen = [], set()
    for f in idx['exams']:
        try:
            d = json.load(open(os.path.join(EX, f)))
        except Exception:
            out.append(dict(file=f, broken=True))
            continue
        if not isinstance(d.get('exam'), dict) or d['exam'].get('id') in seen:
            continue
        seen.add(d['exam']['id'])
        out.append(dict(file=f, d=d, lazy=False))
    for f in sorted(glob.glob(os.path.join(EX, 'matric_lazy', 'subjects', '*.json'))):
        for d in json.load(open(f)).get('papers', []):
            if d['exam']['id'] in seen:
                continue
            seen.add(d['exam']['id'])
            out.append(dict(file='matric_lazy/' + os.path.basename(f), d=d, lazy=True))
    return out


def audit_paper(d):
    qs = d.get('questions') or []
    r = collections.Counter(questions=len(qs))
    seen = set()
    for q in qs:
        stem = str(q.get('stem') or '')
        o = q.get('options')
        if not stem.strip() and not q.get('image') and not q.get('passage_id') and not q.get('subparts'):
            r['blank_stem'] += 1
        if q.get('type') == 'mcq' and not (isinstance(o, dict) and len(o) > 1):
            r['mcq_no_options'] += 1
        if isinstance(o, dict):
            if any(not str(v).strip() for v in o.values()):
                r['empty_option'] += 1
            if q.get('answer') not in o:
                r['bad_key'] += 1
        if 'android_asset' in stem:
            r['figure_link_missing'] += 1
        if '(not available)]' in stem:
            r['figure_not_available'] += 1
        txt = stem + ' ' + ' '.join(map(str, (o or {}).values()))
        if any(re.search(r'(?<!\\)\\\\[a-zA-Z]', ''.join(x for x in m if x)) for m in SEG.findall(txt)):
            r['tex_over_escaped'] += 1
        k = (q.get('part'), n(stem), n(json.dumps(o, sort_keys=True)), q.get('passage_id'), q.get('match_list_id'))
        if len(k[1]) >= 8 and (o or len(k[1]) >= 25):
            if k in seen:
                r['repeat_in_paper'] += 1
            seen.add(k)
        if q.get('review_flag'):
            r['review_flag'] += 1
    p1 = sorted(q.get('number') for q in qs if q.get('part', 1) == 1 and isinstance(q.get('number'), int))
    if p1:
        r['part1_number_holes'] = len(set(range(1, p1[-1] + 1)) - set(p1))
    return r


def kind(e):
    t = ' '.join(str(e.get(k, '')) for k in ('id', 'title', 'type', 'exam_code')).lower()
    return 'model' if 'model' in t else 'matric'


def main():
    papers = load()
    rows = []
    for p in papers:
        if p.get('broken'):
            rows.append(dict(file=p['file'], broken=True))
            continue
        e = p['d']['exam']
        rows.append(dict(id=e['id'], file=p['file'], lazy=p['lazy'], subject=e.get('subject'), year=str(e.get('year')), kind=kind(e), **audit_paper(p['d'])))
    groups = collections.defaultdict(list)
    for r in rows:
        if 'id' in r:
            groups[(r['subject'], r['year'][:4], r['kind'])].append(r['id'])
    subj = collections.defaultdict(collections.Counter)
    for r in rows:
        if 'id' not in r:
            continue
        s = subj[r['subject']]
        s['papers'] += 1
        s['lazy_papers'] += r['lazy']
        for k, v in r.items():
            if isinstance(v, int) and not isinstance(v, bool):
                s[k] += v
        if r['questions'] == 0 or r.get('blank_stem', 0) or r.get('figure_link_missing', 0) or r.get('tex_over_escaped', 0) or r.get('repeat_in_paper', 0):
            s['papers_with_problems'] += 1
    for (sub, y, k), ids in groups.items():
        if len(ids) > 1:
            subj[sub]['same_subject_year_kind_extra'] += len(ids) - 1
    out = dict(papers=rows, subjects={k: dict(v) for k, v in sorted(subj.items())})
    if '--json' in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
    keys = ['papers', 'lazy_papers', 'questions', 'papers_with_problems', 'tex_over_escaped', 'figure_link_missing', 'repeat_in_paper', 'part1_number_holes', 'empty_option', 'bad_key', 'same_subject_year_kind_extra']
    print('subject'.ljust(24) + ''.join(k[:12].rjust(13) for k in keys))
    for s, c in out['subjects'].items():
        print(str(s).ljust(24) + ''.join(str(c.get(k, 0)).rjust(13) for k in keys))


if __name__ == '__main__':
    main()
