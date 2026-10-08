#!/usr/bin/env python3
"""Drive-bank stems carry markdown image links to the old Android app's assets
(`![Circuit Diagram](file:///android_asset/exam_images/x.webp)`). Those pictures were never shipped (and the source
APK keeps them encrypted), and the exam renderer has no markdown images, so the raw link showed up as text.
Replace each link with a visible note and set review_flag, so the question is honest about the missing figure.
Usage: fix_images.py [--dry]"""
import glob, json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'high', 'exams')
LINK = re.compile(r'\s*!\[([^\]]*)\]\(file:///android_asset/[^)]*\)')
FLAG = 'Figure from the original paper is not available in the app yet.'


def fix_q(q):
    hit = False
    for k in ('stem',):
        s = q.get(k)
        if isinstance(s, str) and LINK.search(s):
            s = LINK.sub(lambda m: f"\n\n[Figure: {m[1].strip() or 'diagram'} (not available)]", s).strip()
            q[k] = s
            hit = True
    if isinstance(q.get('options'), dict):
        for kk, v in q['options'].items():
            if isinstance(v, str) and LINK.search(v):
                q['options'][kk] = LINK.sub(lambda m: f"[Figure: {m[1].strip() or 'diagram'} (not available)]", v).strip()
                hit = True
    for k in ('explanation_steps', 'tips'):
        if isinstance(q.get(k), list):
            q[k] = [re.sub(r'\s*!\[[^\]]*\]\(file:///android_asset/[^)\s]*\)?', '', x) if isinstance(x, str) else x for x in q[k]]
    if hit and not q.get('review_flag'):
        q['review_flag'] = FLAG
    return hit


def main():
    dry = '--dry' in sys.argv
    idx = json.load(open(os.path.join(ROOT, 'index.json')))
    paths = [os.path.join(ROOT, f) for f in idx['exams']] + sorted(glob.glob(os.path.join(ROOT, 'matric_lazy', 'subjects', '*.json')))
    tot = 0
    for p in paths:
        raw = open(p, encoding='utf-8').read()
        if 'android_asset' not in raw:
            continue
        d = json.loads(raw)
        papers = d['papers'] if 'papers' in d else [d]
        n = sum(fix_q(q) for pp in papers for q in pp.get('questions', []))
        tot += n
        print(os.path.relpath(p, ROOT), n)
        if not dry:
            with open(p, 'w', encoding='utf-8') as fh:
                if raw.startswith('{"'):
                    json.dump(d, fh, ensure_ascii=False, separators=(',', ':'))
                else:
                    json.dump(d, fh, ensure_ascii=False, indent=2)
                if raw.endswith('\n'):
                    fh.write('\n')
    print('total', tot)


if __name__ == '__main__':
    main()
