#!/usr/bin/env python3
"""Attach figures cropped from the source PDFs (figures.json) to their questions: set image / image_alt, drop the
"[Figure: .. (not available)]" note and the missing-figure review flag, list the file in index.json media."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'assets', 'high', 'exams')
NOTE = re.compile(r'\s*\[Figure: [^\]]*\(not available\)\]')
FLAG = 'Figure from the original paper is not available in the app yet.'


def main():
    figs = {k: v for k, v in json.load(open(os.path.join(HERE, 'figures.json'))).items() if not k.startswith('_')}
    idx_p = os.path.join(ROOT, 'index.json')
    idx = json.load(open(idx_p))
    n = 0
    for f in idx['exams']:
        p = os.path.join(ROOT, f)
        raw = open(p, encoding='utf-8').read()
        if not any(k in raw for k in figs):
            continue
        d = json.loads(raw)
        for q in d['questions']:
            fx = figs.get(q['id'])
            if not fx:
                continue
            q['stem'] = NOTE.sub('', q['stem']).rstrip()
            if q.get('review_flag') == FLAG:
                del q['review_flag']
            if fx.get('image'):
                assert os.path.exists(os.path.join(ROOT, fx['image'])), fx['image']
                q['image'], q['image_alt'] = fx['image'], fx['alt']
                m = fx['image'].replace('media/', '')
                if m not in idx['media']:
                    idx['media'].append(m)
            n += 1
        with open(p, 'w', encoding='utf-8') as fh:
            json.dump(d, fh, ensure_ascii=False, separators=(',', ':')) if raw.startswith('{"') else json.dump(d, fh, ensure_ascii=False, indent=2)
            if raw.endswith('\n'):
                fh.write('\n')
    raw = open(idx_p).read()
    with open(idx_p, 'w') as fh:
        json.dump(idx, fh, ensure_ascii=False, indent=2)
        if raw.endswith('\n'):
            fh.write('\n')
    print('figures attached/cleared:', n)


if __name__ == '__main__':
    main()
