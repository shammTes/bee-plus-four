#!/usr/bin/env python3
"""Repeated questions inside one paper (the Drive bank batches overlap, so some packs hold the same question 2x).
Same part + same stem + same options (text-normalised) = repeat; the copy with more explanation is kept, in the
earlier position. Non-MCQ repeats need a stem of >= 25 letters (short completion prompts can repeat legitimately).
Usage: dedupe_within.py [--dry]"""
import glob, json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'high', 'exams')


def n(s):
    return re.sub(r'[^a-z0-9]', '', str(s).lower())


def richness(q):
    return len(json.dumps(q.get('explanation_steps') or [])) + 50 * bool(q.get('answer'))


def dedupe(qs):
    """-> (kept questions, removed ids). Copies that disagree on the key: the majority key wins (the kept question
    takes the richest copy with that key); a tie keeps the first copy and flags the disagreement."""
    groups, order, out_simple = {}, [], []
    for q in qs:
        stem = n(q.get('stem'))
        opts = q.get('options')
        if len(stem) < 8 or (not opts and len(stem) < 25):
            order.append(('q', q))
            continue
        k = (q.get('part'), stem, n(json.dumps(opts, sort_keys=True)), q.get('passage_id'), q.get('match_list_id'))
        if k not in groups:
            groups[k] = []
            order.append(('g', k))
        groups[k].append(q)
    out, gone = [], []
    for kind, x in order:
        if kind == 'q':
            out.append(x)
            continue
        cp = groups[x]
        first = cp[0]
        if len(cp) > 1:
            votes = {}
            for c in cp:
                votes.setdefault(str(c.get('answer')), []).append(c)
            ranked = sorted(votes.items(), key=lambda kv: -len(kv[1]))
            if len(ranked) > 1 and len(ranked[0][1]) == len(ranked[1][1]):
                keep = dict(first)
                keep.setdefault('review_flag', 'Repeated copies of this question in the source disagree on the key (' + ' / '.join(a for a, _ in ranked) + '); check against the original paper.')
            else:
                best = max(ranked[0][1], key=richness)
                keep = dict(best, id=first['id'], number=first.get('number'))
            gone += [c['id'] for c in cp[1:]]
            out.append(keep)
        else:
            out.append(first)
    return out, gone


def main():
    dry = '--dry' in sys.argv
    idx = json.load(open(os.path.join(ROOT, 'index.json')))
    log = {}
    paths = [os.path.join(ROOT, f) for f in idx['exams']] + sorted(glob.glob(os.path.join(ROOT, 'matric_lazy', 'subjects', '*.json')))
    for p in paths:
        raw = open(p, encoding='utf-8').read()
        d = json.loads(raw)
        papers = d['papers'] if 'papers' in d else [d]
        ch = False
        for paper in papers:
            qs, gone = dedupe(paper.get('questions', []))
            if gone:
                ch = True
                paper['questions'] = qs
                log[paper['exam']['id']] = gone
        if ch and not dry:
            with open(p, 'w', encoding='utf-8') as f:
                if raw.startswith('{"'):
                    json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
                else:
                    json.dump(d, f, ensure_ascii=False, indent=2)
                if raw.endswith('\n'):
                    f.write('\n')
    for k, v in log.items():
        print(k, len(v))
    print('total', sum(map(len, log.values())))
    if not dry and log:  # a re-run that finds nothing keeps the log of the earlier runs
        lp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dedupe_within_log.json')
        old = json.load(open(lp)) if os.path.exists(lp) else {}
        for k, v in log.items():
            old[k] = old.get(k, []) + v
        json.dump(old, open(lp, 'w'), indent=1)


if __name__ == '__main__':
    main()
